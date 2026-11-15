"""Run actual-host acceptance steps and keep credential-free results."""
import argparse,json,os,time,uuid
from datetime import datetime,timezone
from pathlib import Path
import requests
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1]/'.env')
BASE='https://finn-source-probe-tkef.onrender.com'
PATH=Path('data/checks/mvp-hosted.json')
parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['refresh','documents','research','smoke']);parser.add_argument('--ticker');args=parser.parse_args()
PATH=Path('data/checks/mvp-hosted-'+args.stage+'.json')
record=json.loads(PATH.read_text()) if PATH.exists() else {'origin':BASE,'workspace':str(uuid.uuid4()),'results':[]}
headers={'X-Finn-Workspace':record['workspace']}

def call(method,path,body=None,protected=False):
    started=time.monotonic();h=dict(headers)
    if protected:h['Authorization']='Bearer '+os.environ.get('PROBE_TOKEN','')
    try:
        r=requests.request(method,BASE+path,headers=h,json=body,timeout=(15,90),allow_redirects=False)
        data=r.json();entry={'at':datetime.now(timezone.utc).isoformat(),'path':path,'method':method,'status':r.status_code,'seconds':round(time.monotonic()-started,3),'data':data}
    except Exception as exc:
        data={};entry={'path':path,'error_type':type(exc).__name__}
    record['results'].append(entry);PATH.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in entry.items() if k!='data'}|{k:data[k] for k in ['phase','completed_pages','page_count','error','http_status','detail','matches_stored','verdict'] if k in data}),flush=True)
    return data

if args.stage=='refresh':
    for _ in range(30):
        state=call('POST','/api/refresh/advance')
        if state.get('phase') in ['complete','busy'] or not state.get('phase'):break
    call('GET','/api/portfolio')
elif args.stage=='documents':
    for ticker in ([args.ticker] if args.ticker else ['INFY','DABUR','HCLTECH','VOLTAS']):
        data=call('GET','/api/companies/'+ticker)
        for doc in data.get('documents',[]):
            if doc['kind'] not in ['annual_report','transcript']:continue
            call('POST','/diagnostics/documents/'+doc['id']+'/fetch',protected=True)
            for _ in range(100):
                state=call('POST','/api/documents/'+doc['id']+'/advance')
                if state.get('phase') in ['complete','failed','identity_review','busy'] or not state.get('phase'):break
        call('GET','/api/companies/'+ticker)
elif args.stage=='research':
    ticker=args.ticker or 'INFY'
    question='What do the annual report and earnings call say about cash generation and growth? Separate reported facts from interpretation and identify missing comparisons.'
    call('POST','/api/companies/'+ticker+'/research',{'question':question})
elif args.stage=='smoke':
    call('GET','/api/briefing?historical=true')
    call('GET','/api/events/infy-results-20261023')
    call('GET','/api/evidence/infy-fcf-202609')
    call('PUT','/api/companies/INFY/question',{'question':'Is growth supported by cash generation?'})
    call('PUT','/api/alerts',{'price_threshold':1.5,'volume_multiple':1.5})
    call('GET','/api/alerts')
    call('GET','/api/companies/INFY')
