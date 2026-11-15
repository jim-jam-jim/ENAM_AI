"""Historical replay acceptance: isolated test question, unchanged real event dates.

The replay workspace is test-only. This does not claim live subsequent evidence
has arrived since the user's own saved question.
"""
import json,uuid,time
from pathlib import Path
from datetime import datetime,timedelta
import requests
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1]/'.env')
from server import store
BASE='https://finn-source-probe-tkef.onrender.com'
path=Path('data/checks/monitor-historical-replay.json')
record=json.loads(path.read_text()) if path.exists() else {'workspace':str(uuid.uuid4()),'label':'Historical replay; test question predates a real filing; real event dates unchanged','checks':[]}
headers={'X-Finn-Workspace':record['workspace']}
events=store.get('filings','INFY',{}).get('events',[])
event=next(e for e in events if 'transcript' in (e.get('summary','')+' '+e['category']).lower())
key=record['workspace']+':INFY'
if not store.get('question',key):
    saved_at=(datetime.fromisoformat(event['published_at'])-timedelta(days=1)).isoformat()
    store.put('question',key,{'ticker':'INFY','question':'Is growth supported by cash generation?','saved_at':saved_at,'test_label':record['label']})

def call(method,url):
    r=requests.request(method,BASE+url,headers=headers,timeout=(15,90));data=r.json()
    record['checks'].append({'path':url,'status':r.status_code,'data':data});path.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print({'path':url,'status':r.status_code,'phase':data.get('phase'),'detail':data.get('detail')},flush=True)
    return data

call('GET','/api/companies/INFY')
d=call('POST','/api/events/'+event['id']+'/document')
for _ in range(10):
    if d.get('phase')=='complete':break
    d=call('POST','/api/documents/'+d['id']+'/advance')
    if d.get('phase') in ['busy','failed','identity_review']:break
if d.get('phase')=='complete':call('POST','/api/companies/INFY/monitor/'+event['id'])
