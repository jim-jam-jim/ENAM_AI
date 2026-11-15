"""Bounded primary-document jobs; discovery pages are never research evidence."""
import hashlib
import io
import re
import time
from urllib.parse import urlparse,urljoin
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from scripts.host_probe import storage,read_object,MAX_BYTES
import os
from . import store
from .market import now,digest

PRIMARY_HOSTS={'nsearchives.nseindia.in','nsearchives.nseindia.com','www.bseindia.com','www.infosys.com','www.hcltech.com','www.dabur.com','dabur.com'}

def safe_url(url):
    p=urlparse(url)
    if p.scheme!='https' or p.hostname not in PRIMARY_HOSTS or p.username or p.port not in (None,443):raise ValueError('Unsupported primary source host')
    return url

def download(url):
    start=time.monotonic()
    for _ in range(4):
        safe_url(url)
        with requests.get(url,timeout=(10,20),stream=True,allow_redirects=False,headers={'User-Agent':'FINN/0.2'}) as r:
            if r.is_redirect:
                url=urljoin(url,r.headers['Location']);continue
            r.raise_for_status();chunks=[];size=0
            for chunk in r.iter_content(65536):
                size+=len(chunk)
                if size>MAX_BYTES or time.monotonic()-start>45:raise ValueError('Source exceeds processing budget')
                chunks.append(chunk)
            data=b''.join(chunks)
            if not data.startswith(b'%PDF'):raise ValueError('Source is not a PDF')
            return data
    raise ValueError('Too many redirects')

def discover(ticker):
    url=f'https://www.screener.in/company/{ticker}/consolidated/'
    r=requests.get(url,timeout=(10,20));r.raise_for_status()
    soup=BeautifulSoup(r.text,'html.parser');heading=soup.find('h1')
    if heading is None:raise ValueError('Company not found')
    company=heading.get_text(' ',strip=True)
    candidates=[]
    for kind,label in [('annual_report',r'Annual Report\s+20\d{2}'),('transcript',r'^Transcript$')]:
        for a in soup.select('a[href]'):
            if re.search(label,a.get_text(' ',strip=True),re.I):
                source=urljoin(url,a['href'])
                try:safe_url(source)
                except ValueError:continue
                candidates.append(register(ticker,company,kind,source,a.get_text(' ',strip=True),url));break
    if not candidates:raise ValueError('No supported primary document links found')
    return candidates

def register(ticker,company,kind,url,label='',discovery_url=None):
    safe_url(url);key=digest(ticker+'|'+url)
    existing=store.get('document',key)
    if existing:return existing
    value={'id':key,'ticker':ticker,'company':company,'kind':kind,'url':url,'discovery_url':discovery_url,'discovery_label':label,'phase':'queued','completed_pages':0,'created_at':now()}
    return store.put('document',key,value)

def advance(key):
    with store.lock('document-worker') as acquired:
        if not acquired:return {'phase':'busy','id':key}
        d=store.get('document',key)
        if not d:raise ValueError('Document missing')
        if d['phase']=='complete':return d
        if d.get('attempts',0)>=3 and d.get('error'):return d
        try:
            client=storage()
            if not d.get('sha256'):
                data=download(d['url']);sha=hashlib.sha256(data).hexdigest();object_key=f'sources/sha256/{sha}.pdf'
                client.put_object(Bucket=os.environ['DOCUMENT_BUCKET'],Key=object_key,Body=data,ContentType='application/pdf')
                if hashlib.sha256(read_object(client,object_key)).hexdigest()!=sha:raise ValueError('Storage hash mismatch')
                d.update(sha256=sha,object_key=object_key,bytes=len(data),fetched_at=now(),phase='stored',host=os.environ.get('RENDER_SERVICE_NAME','local'))
            else:
                data=read_object(client,d['object_key'])
                if hashlib.sha256(data).hexdigest()!=d['sha256']:raise ValueError('Stored source changed')
                reader=PdfReader(io.BytesIO(data));d['page_count']=len(reader.pages)
                started=time.monotonic()
                with store.connect() as checkpoint_conn:
                    for index in range(d['completed_pages'],min(d['completed_pages']+20,len(reader.pages))):
                        text=reader.pages[index].extract_text() or ''
                        store.put('passage',f'{key}:{index+1}',{'id':f'{key}:{index+1}','document_id':key,'ticker':d['ticker'],'kind':d['kind'],'page':index+1,'text':text,'url':d['url'],'sha256':d['sha256']},connection=checkpoint_conn)
                        d.update(completed_pages=index+1,phase='extracting',updated_at=now())
                        store.put('document',key,d,connection=checkpoint_conn)
                        if time.monotonic()-started>12:break
                if d['completed_pages']==d['page_count']:
                    sample=' '.join((store.get('passage',f'{key}:{i}',{}) or {}).get('text','') for i in range(1,min(12,d['page_count'])+1))
                    tokens=[t for t in re.findall(r'[a-z]+',d['company'].lower()) if len(t)>2 and t not in ['limited','ltd','india','industries']]
                    matched=any(t in sample.lower() for t in tokens)
                    kind_match=True if d['kind']=='filing' else (bool(re.search(r'annual\s+report',sample,re.I)) if d['kind']=='annual_report' else bool(re.search(r'(earnings|conference|investor).*call|transcript',sample,re.I|re.S)))
                    d.update(phase='complete' if matched and kind_match else 'identity_review',identity_match=matched,document_type_match=kind_match,period_mentions=list(dict.fromkeys(re.findall(r'(?:FY\s*20?\d{2}|20\d{2}\s*[-–]\s*(?:20)?\d{2})',sample,re.I)))[:12],completed_at=now())
            d.pop('error',None)
        except Exception as exc:
            d.update(phase='failed',error=type(exc).__name__,attempts=d.get('attempts',0)+1,updated_at=now())
            if isinstance(exc,requests.HTTPError):d['http_status']=exc.response.status_code
        return store.put('document',key,d)

def passages(ticker,question,limit=10):
    docs={d['id']:d for d in store.all_records('document') if d['ticker']==ticker and d['phase']=='complete'}
    terms=set(re.findall(r'[a-z]{3,}',question.lower()))-{'the','and','this','company','with','what','does','how'}
    candidates=[]
    for p in store.for_ticker('passage',ticker):
        if p['document_id'] not in docs or len(p['text'].strip())<100:continue
        text=p['text'].lower();score=sum(min(text.count(t),8) for t in terms)
        if score:candidates.append((score,p))
    candidates.sort(key=lambda x:x[0],reverse=True)
    # Include evidence from both source types when relevant, not only the longest report.
    selected=[]
    for kind in ['annual_report','transcript']:
        selected.extend(p for _,p in [x for x in candidates if x[1]['kind']==kind][:limit//2])
    return [dict(p,text=p['text'][:6500],document=docs[p['document_id']]) for p in selected]
