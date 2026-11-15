"""Record real Render responses; never emit credentials or arbitrary response text."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()
BASE='https://finn-source-probe-tkef.onrender.com'
parser=argparse.ArgumentParser()
parser.add_argument('action',choices=['health','step','verify','unauthorised'])
parser.add_argument('--source',choices=['small','large'],default='small')
parser.add_argument('--count',type=int,default=1)
args=parser.parse_args()
path=Path('data/checks/render-'+args.source+'.json')
record=json.loads(path.read_text()) if path.exists() else {'origin':BASE,'job_id':str(uuid.uuid4()),'results':[]}
for _ in range(min(args.count,25)):
    start=time.monotonic()
    result={'action':args.action,'at_utc':datetime.now(timezone.utc).isoformat()}
    try:
        headers={'Authorization':'Bearer '+os.environ.get('PROBE_TOKEN','')}
        if args.action=='step':
            response=requests.post(BASE+'/step',headers=headers,json={'job_id':record['job_id'],'source':args.source},timeout=(15,90),allow_redirects=False)
        elif args.action=='health':
            response=requests.get(BASE+'/healthz',timeout=(15,90),allow_redirects=False)
        else:
            response=requests.get(BASE+'/verify',params={'job_id':record['job_id']},headers=headers if args.action=='verify' else {},timeout=(15,90),allow_redirects=False)
        result['http_status']=response.status_code
        try:
            payload=response.json()
            allowed=['job_id','phase','boot_id','page_count','completed_pages','unique_pages','sha256','memory','seconds','object_hash_matches','passages_present','updated_at','service','configured','error_type','missing_keys','source_http_status','source_host']
            result['response']={k:v for k,v in payload.items() if k in allowed}
        except (ValueError,AttributeError):
            result['response']={'non_json':True}
    except requests.RequestException as exc:
        result['error_type']=type(exc).__name__
    result['elapsed_seconds']=round(time.monotonic()-start,3)
    record['results'].append(result)
    path.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)
    if result.get('http_status')!=200 or result.get('response',{}).get('phase')=='complete':
        break
