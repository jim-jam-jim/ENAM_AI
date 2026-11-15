"""First read-only evidence workflow. Curated evidence is explicit; no synthesis."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
import json
import os
import hmac
import threading
import uuid
import psycopg
from dotenv import load_dotenv
from fastapi import Header
from scripts import host_probe
from server import store
from server.features import router
from server import documents
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT/'.env')
app = FastAPI(title='FINN', docs_url=None, redoc_url=None, openapi_url=None)
probe_lock = threading.Lock()
app.include_router(router)

@app.on_event('startup')
def initialise_store():
    store.initialise()

@app.exception_handler(psycopg.Error)
def database_unavailable(request,exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=503,content={'detail':'Database temporarily unavailable; retry shortly'})

def percentage(current, previous):
    current, previous = Decimal(str(current)), Decimal(str(previous))
    if previous <= 0:
        return None
    return str(((current/previous-1)*100).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP))

def dataset():
    try:
        with psycopg.connect(os.environ['DATABASE_URL'], connect_timeout=10) as conn:
            conn.execute("SET statement_timeout = '10s'")
            row = conn.execute("SELECT payload FROM finn_read_models WHERE id='infy-q2-fy2027'").fetchone()
        if not row:
            raise ValueError('Missing published data')
        return row[0]
    except Exception:
        raise HTTPException(503, 'Stored briefing temporarily unavailable; please retry') from None

def events_in_window(data, days, now):
    cutoff = now-timedelta(days=days)
    seen, items = set(), []
    for item in data['events']:
        date=datetime.fromisoformat(item['published_at'])
        key=item['id']
        if cutoff <= date <= now and key not in seen:
            seen.add(key)
            items.append(item)
    return sorted(items,key=lambda e:(e['priority']!='material',-datetime.fromisoformat(e['published_at']).timestamp()))

@app.get('/api/health')
def health():
    return {'status':'ok','scope':'read-only briefing','data_source':'Neon PostgreSQL'}

@app.get('/api/briefing')
def briefing(days:int=Query(1,ge=1,le=30), historical:bool=False):
    data=dataset()
    now=datetime.now(timezone.utc)
    return {'as_of':now.isoformat(),'coverage':data['coverage'], 'price':data['price'],
            'events':data['events'] if historical else events_in_window(data,days,now),
            'historical':historical,'research_available':False}

@app.get('/api/events/{event_id}')
def event(event_id:str):
    data=dataset()
    item=next((x for x in data['events'] if x['id']==event_id),None)
    if item is None:
        item=next((e for f in store.all_records('filings') for e in f.get('events',[]) if e['id']==event_id),None)
    if item is None:
        raise HTTPException(404,'Event unavailable')
    if item.get('metric'):
        metric=dict(item['metric'])
        metric['change_percent']=percentage(metric['current'],metric['previous'])
        return dict(item,metric=metric)
    return item

@app.get('/api/evidence/{evidence_id}')
def evidence(evidence_id:str):
    item=dataset()['evidence'].get(evidence_id)
    if item is None:
        raise HTTPException(404,'Source passage unavailable')
    return dict(item,relevant_passage=item['passage'][item['passage'].find('Cash Metrics'):]) if 'Cash Metrics' in item['passage'] else item

@app.get('/healthz')
def liveness():
    return {'service':'FINN','boot_id':host_probe.BOOT}

def protect(authorization):
    token=os.environ.get('PROBE_TOKEN','')
    if len(token)<32 or not hmac.compare_digest(authorization or '', 'Bearer '+token):
        raise HTTPException(401,'Unauthorised')

@app.post('/diagnostics/documents/{key}/fetch')
def verify_source_host(key:str,authorization:str|None=Header(default=None)):
    protect(authorization)
    import hashlib
    d=store.get('document',key)
    if not d:raise HTTPException(404,'Unknown document')
    try:
        data=documents.download(d['url'])
        sha=hashlib.sha256(data).hexdigest()
        result={'origin':os.environ.get('RENDER_SERVICE_NAME','local'),'sha256':sha,'bytes':len(data),'matches_stored':sha==d.get('sha256'),'checked_at':datetime.now(timezone.utc).isoformat()}
        d['host_fetch_check']=result;store.put('document',key,d)
        return result
    except Exception as exc:
        import requests
        return {'error_type':type(exc).__name__,'http_status':exc.response.status_code if isinstance(exc,requests.HTTPError) else None}

@app.get('/verify')
def diagnostic_verify(job_id:uuid.UUID, authorization:str|None=Header(default=None)):
    protect(authorization)
    try:
        return host_probe.verify(job_id)
    except Exception:
        raise HTTPException(503,'Diagnostic unavailable; checkpoint retained') from None

@app.post('/step')
def diagnostic_step(payload:dict, authorization:str|None=Header(default=None)):
    protect(authorization)
    try:
        job_id=uuid.UUID(payload.get('job_id',''))
        source=payload.get('source','small')
        if source not in host_probe.SOURCES: raise ValueError()
    except (ValueError,TypeError,AttributeError):
        raise HTTPException(400,'Invalid diagnostic job') from None
    if not probe_lock.acquire(blocking=False):
        raise HTTPException(409,'Diagnostic already running')
    try:
        return host_probe.step(job_id,source)
    except Exception:
        raise HTTPException(503,'Diagnostic failed; checkpoint retained') from None
    finally:
        probe_lock.release()

if (ROOT/'web/out').exists():
    app.mount('/',StaticFiles(directory=ROOT/'web/out',html=True),name='frontend')
