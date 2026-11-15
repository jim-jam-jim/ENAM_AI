"""Public source ingestion and deterministic alert rules, never model summaries."""
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
import hashlib
import math
import os
import requests
from . import store

PORTFOLIO=['INFY','DABUR','HCLTECH','TCS','RELIANCE','HDFCBANK','ICICIBANK','SBIN','ITC','HINDUNILVR','LT','MARUTI','SUNPHARMA','TITAN','ASIANPAINT']
IST=ZoneInfo('Asia/Kolkata')

def now():return datetime.now(timezone.utc).isoformat()
def digest(value):return hashlib.sha256(value.encode()).hexdigest()[:24]

def classify(subject):
    text=subject.lower()
    if any(w in text for w in ['financial result','dividend','acquisition','default','resignation','fraud','litigation','buyback','outcome of board']):return 'material'
    if any(w in text for w in ['newspaper','certificate under','trading window','investor meet','conference','loss of share','duplicate share']):return 'routine'
    return 'review'  # Unknown is visible, never silently routine.

def normalise(rows,ticker):
    events={}
    for row in rows:
        if row.get('symbol')!=ticker:continue
        url=row.get('attchmntFile') or ''
        if not url.startswith('https://'):continue
        try:published=datetime.strptime(row['an_dt'],'%d-%b-%Y %H:%M:%S').replace(tzinfo=IST).isoformat()
        except (KeyError,ValueError):continue
        key=digest(ticker+'|'+url)  # Same attachment is one disclosure; revised URL stays separate.
        subject=row.get('desc','Unclassified disclosure')
        events[key]={'id':key,'ticker':ticker,'company':row.get('sm_name',ticker),'published_at':published,'category':subject,'title':subject,'summary':row.get('attchmntText',''), 'summary_origin':'Exchange filing description · not AI analysis','priority':classify(subject),'source_url':url,'source_urls':[url],'evidence_id':None,'availability':'Open the original filing or load its passage. Figures have not been verified.','reason':'Rule-based category priority; unknown categories remain visible for review.'}
    return list(events.values())

def prices(ticker):
    url=f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}.NS?range=3mo&interval=1d&events=splits%2Cdiv'
    r=requests.get(url,timeout=(10,25),headers={'User-Agent':'FINN/0.2'});r.raise_for_status()
    chart=r.json()['chart']['result'][0]
    if chart['meta']['symbol']!=ticker+'.NS':raise ValueError('Symbol mismatch')
    quotes=chart['indicators']['quote'][0];today=datetime.now(IST)
    rows=[]
    for t,c,v in zip(chart.get('timestamp',[]),quotes['close'],quotes['volume']):
        date=datetime.fromtimestamp(t,IST)
        if date.date()==today.date() and (today.hour,today.minute)<(16,0):continue
        if c is not None and v is not None and math.isfinite(c) and c>0 and v>=0:
            rows.append({'date':date.date().isoformat(),'close':round(c,4),'volume':v})
    return {'rows':rows,'currency':chart['meta'].get('currency'),'url':url,'fetched_at':now(),'corporate_actions':chart.get('events',{})}

def filings(ticker):
    end=datetime.now(IST);start=end-timedelta(days=30)
    url=f'https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={ticker}&from_date={start:%d-%m-%Y}&to_date={end:%d-%m-%Y}'
    r=requests.get(url,timeout=(10,25),headers={'User-Agent':'FINN/0.2'});r.raise_for_status()
    rows=r.json()
    if not isinstance(rows,list):raise ValueError('Unexpected feed')
    return {'events':normalise(rows,ticker),'url':url,'fetched_at':now(),'window_start':start.date().isoformat(),'window_end':end.date().isoformat()}

def advance_refresh():
    with store.lock('market-refresh') as acquired:
        if not acquired:return {'phase':'busy'}
        state=store.get('refresh','portfolio',{'cursor':0,'phase':'queued'})
        origin=os.environ.get('RENDER_SERVICE_NAME','local')
        if state['phase']=='complete' and state.get('origin')==origin and (datetime.now(timezone.utc)-datetime.fromisoformat(state['finished_at'])).total_seconds()<3600:return state
        if state['phase']=='complete':state={'cursor':0,'phase':'queued'}
        cursor=state['cursor'];ticker=PORTFOLIO[cursor//2];kind=['prices','filings'][cursor%2]
        old=store.get(kind,ticker,{})
        try:
            value=(prices if kind=='prices' else filings)(ticker)
            value.update(ticker=ticker,status='available',attempted_at=now(),origin=origin)
        except Exception as exc:
            value=dict(old,ticker=ticker,status='stale' if old.get('fetched_at') else 'unavailable',attempted_at=now(),error=type(exc).__name__)
            if isinstance(exc,requests.HTTPError):value['http_status']=exc.response.status_code
        store.put(kind,ticker,value)
        state.update(cursor=cursor+1,phase='complete' if cursor+1==len(PORTFOLIO)*2 else 'running',last_ticker=ticker,last_source=kind,updated_at=now(),origin=origin)
        if state['phase']=='complete':state['finished_at']=now()
        return store.put('refresh','portfolio',state)

def alert_values(prices_data,price_threshold=3,volume_multiple=2):
    rows=prices_data.get('rows',[])
    if len(rows)<21:return {'available':False,'reason':'Requires 21 completed sessions (latest plus 20 prior).'}
    latest=rows[-1];previous=rows[-2];baseline=sum(r['volume'] for r in rows[-21:-1])/20
    actions=prices_data.get('corporate_actions',{})
    dates=[datetime.fromtimestamp(int(t),IST).date().isoformat() for group in actions.values() for t in group]
    if any(d>=rows[-21]['date'] for d in dates):return {'available':False,'reason':'Corporate action in comparison window; review unadjusted price/volume before alerting.'}
    if previous['close']<=0 or baseline<=0:return {'available':False,'reason':'Invalid comparison baseline.'}
    change=(latest['close']/previous['close']-1)*100;multiple=latest['volume']/baseline
    return {'available':True,'date':latest['date'],'price_change_percent':round(change,2),'volume_multiple':round(multiple,2),'volume_baseline':round(baseline,2),'price_triggered':abs(change)>=price_threshold,'volume_triggered':multiple>=volume_multiple,'baseline':'Unadjusted close vs prior session; volume vs mean of preceding 20 completed sessions, excluding latest.'}
