"""MVP routes; anonymous per-browser settings, shared public-source cache."""
import re
import uuid
from datetime import datetime,timezone
from fastapi import APIRouter,HTTPException,Header
from pydantic import BaseModel,Field
from . import store,market,documents,research

router=APIRouter(prefix='/api')

def ticker(value):
    value=value.strip().upper()
    if not re.fullmatch(r'[A-Z0-9&-]{1,20}',value):raise HTTPException(422,'Enter an NSE symbol')
    return value

def owner(header):
    try:return str(uuid.UUID(header or ''))
    except ValueError:raise HTTPException(400,'Browser workspace is missing; reload the page') from None

class Question(BaseModel):
    question:str=Field(min_length=8,max_length=600)

class Thresholds(BaseModel):
    price_threshold:float=Field(default=3,ge=0.1,le=100)
    volume_multiple:float=Field(default=2,ge=1,le=100)

@router.get('/portfolio')
def portfolio():
    companies=[];events=[]
    prices={p['ticker']:p for p in store.all_records('prices')}
    filings={p['ticker']:p for p in store.all_records('filings')}
    for symbol in market.PORTFOLIO:
        p=prices.get(symbol,{});f=filings.get(symbol,{})
        companies.append({'ticker':symbol,'price':p,'filings':{k:v for k,v in f.items() if k!='events'}})
        events.extend(f.get('events',[]))
    return {'companies':companies,'events':events,'refresh':store.get('refresh','portfolio',{'phase':'queued','cursor':0}),'refresh_mode':'Manual or while this page is open; no scheduled monitoring','research_available':research.configured()}

@router.post('/refresh/advance')
def advance_refresh():return market.advance_refresh()

@router.get('/companies/{symbol}')
def company(symbol:str,x_finn_workspace:str|None=Header(default=None)):
    symbol=ticker(symbol);workspace=owner(x_finn_workspace)
    saved=store.get('question',workspace+':'+symbol)
    newer=[]
    if saved:
        newer=[e for e in store.get('filings',symbol,{}).get('events',[]) if datetime.fromisoformat(e['published_at'])>datetime.fromisoformat(saved['saved_at'])]
    return {'ticker':symbol,'documents':[d for d in store.all_records('document') if d['ticker']==symbol],'saved_question':saved,'subsequent_events':newer,'monitoring_note':'Only disclosures dated after the saved question appear here. Unrelated material events remain in the briefing.','research_available':research.configured()}

@router.post('/companies/{symbol}/discover')
def discover(symbol:str):
    symbol=ticker(symbol)
    with store.lock('discover:'+symbol) as acquired:
        if not acquired:raise HTTPException(409,'Discovery in progress')
        state=store.get('discovery',symbol)
        if state and (datetime.now(timezone.utc)-datetime.fromisoformat(state['at'])).total_seconds()<3600:
            return {'documents':[d for d in store.all_records('document') if d['ticker']==symbol],'cached':True,'error':state.get('error')}
        try:
            found=documents.discover(symbol);store.put('discovery',symbol,{'at':market.now()});return {'documents':found}
        except Exception as exc:
            store.put('discovery',symbol,{'at':market.now(),'error':type(exc).__name__})
            raise HTTPException(503,'Primary-source discovery unavailable; no documents fabricated') from None

@router.post('/documents/{key}/advance')
def advance_document(key:str):
    if not re.fullmatch(r'[0-9a-f]{24}',key):raise HTTPException(422,'Invalid source ID')
    try:return documents.advance(key)
    except ValueError:raise HTTPException(404,'Document unavailable') from None

@router.get('/passages/{key}')
def passage(key:str):
    if not re.fullmatch(r'[0-9a-f]{24}:\d{1,5}',key):raise HTTPException(422,'Invalid passage ID')
    result=store.get('passage',key)
    if not result:raise HTTPException(404,'Passage unavailable')
    return result

@router.put('/companies/{symbol}/question')
def save_question(symbol:str,body:Question,x_finn_workspace:str|None=Header(default=None)):
    symbol=ticker(symbol);workspace=owner(x_finn_workspace)
    return store.put('question',workspace+':'+symbol,{'ticker':symbol,'question':body.question.strip(),'saved_at':market.now()})

@router.post('/events/{event_id}/document')
def event_document(event_id:str):
    event=next((e for f in store.all_records('filings') for e in f.get('events',[]) if e['id']==event_id),None)
    if not event:raise HTTPException(404,'Filing not available in stored feed')
    d=documents.register(event['ticker'],event['company'],'filing',event['source_url'])
    d['document_date']=event['published_at'];store.put('document',d['id'],d)
    return d

@router.get('/events/{event_id}/passage')
def event_passage(event_id:str):
    event=next((e for f in store.all_records('filings') for e in f.get('events',[]) if e['id']==event_id),None)
    if not event:raise HTTPException(404,'Filing unavailable')
    d=store.get('document',market.digest(event['ticker']+'|'+event['source_url']))
    if not d:raise HTTPException(409,'Load document first')
    candidates=[p for p in store.for_ticker('passage',event['ticker']) if p['document_id']==d['id']]
    if not candidates:raise HTTPException(409,'No readable pages yet')
    terms=set(re.findall(r'[a-z]{4,}',event.get('summary','').lower()))-{'limited','informed','exchange','regarding','about','company'}
    score=lambda p:sum(min(p['text'].lower().count(t),3) for t in terms)
    best=max(candidates,key=score)
    return dict(best,document=d,match_score=score(best),scope='Text matched to exchange description; not independent verification of every claim. Extracted pages: '+str(d['completed_pages']))

@router.post('/companies/{symbol}/monitor/{event_id}')
def monitor(symbol:str,event_id:str,x_finn_workspace:str|None=Header(default=None)):
    symbol=ticker(symbol);workspace=owner(x_finn_workspace);saved=store.get('question',workspace+':'+symbol)
    if not saved:raise HTTPException(409,'Save a question first')
    event=next((e for e in store.get('filings',symbol,{}).get('events',[]) if e['id']==event_id),None)
    if not event or datetime.fromisoformat(event['published_at'])<=datetime.fromisoformat(saved['saved_at']):raise HTTPException(409,'This is not a subsequent disclosure')
    d=event_document(event_id)
    if d['phase']!='complete':return {'phase':'needs_document','document':d}
    evidence=[dict(p,document=d) for p in store.for_ticker('passage',symbol) if p['document_id']==d['id'] and len(p['text'])>80][:8]
    try:
        result=research.run(symbol,'Assess whether this subsequent disclosure supports, challenges or is inconclusive for: '+saved['question'],workspace,evidence_override=evidence)
        store.put('monitor',workspace+':'+symbol+':'+event_id,{'event_id':event_id,'saved_at':saved['saved_at'],'answer':result})
        return {'phase':'complete','answer':result}
    except ValueError as exc:raise HTTPException(409,str(exc)) from None

@router.post('/companies/{symbol}/research')
def ask(symbol:str,body:Question,x_finn_workspace:str|None=Header(default=None)):
    symbol=ticker(symbol);workspace=owner(x_finn_workspace)
    try:return research.run(symbol,body.question,workspace)
    except ValueError as exc:raise HTTPException(409,str(exc)) from None
    except Exception:raise HTTPException(503,'Research interrupted; stored sources remain available. Retry to use cached results where completed.') from None

@router.get('/alerts')
def alerts(x_finn_workspace:str|None=Header(default=None)):
    workspace=owner(x_finn_workspace);settings=store.get('settings',workspace,{'price_threshold':3,'volume_multiple':2})
    rows=[]
    prices={p['ticker']:p for p in store.all_records('prices')}
    for symbol in market.PORTFOLIO:
        price=prices.get(symbol,{})
        rows.append(dict(market.alert_values(price,**settings),ticker=symbol,fetched_at=price.get('fetched_at'),source_status=price.get('status','unavailable')))
    return {'settings':settings,'alerts':rows}

@router.put('/alerts')
def save_alerts(body:Thresholds,x_finn_workspace:str|None=Header(default=None)):
    return store.put('settings',owner(x_finn_workspace),body.model_dump())
