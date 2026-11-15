"""First read-only evidence workflow. Curated evidence is explicit; no synthesis."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title='FINN', docs_url=None, redoc_url=None)

def percentage(current, previous):
    current, previous = Decimal(str(current)), Decimal(str(previous))
    if previous <= 0:
        return None
    return str(((current/previous-1)*100).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP))

def dataset():
    return json.loads((ROOT/'data/curated/infy.json').read_text(encoding='utf-8'))

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
    return {'status':'ok','scope':'read-only briefing','hosted_integration_verified':False}

@app.get('/api/briefing')
def briefing(days:int=Query(30,ge=1,le=30)):
    data=dataset()
    now=datetime.now(timezone.utc)
    return {'as_of':now.isoformat(),'coverage':data['coverage'], 'price':data['price'],
            'events':events_in_window(data,days,now),'research_available':False}

@app.get('/api/events/{event_id}')
def event(event_id:str):
    data=dataset()
    item=next((x for x in data['events'] if x['id']==event_id),None)
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
    return item

if (ROOT/'web/out').exists():
    app.mount('/',StaticFiles(directory=ROOT/'web/out',html=True),name='frontend')
