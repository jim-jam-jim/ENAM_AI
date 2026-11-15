"""Run one hosted diagnostic step; credentials stay in .env or environment."""
import argparse
import json
import os
import uuid
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv

load_dotenv()
parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['step','verify','health'])
parser.add_argument('--job-id', type=uuid.UUID)
parser.add_argument('--source',choices=['small','large'],default='small')
args = parser.parse_args()
base = os.environ.get('PROBE_BASE_URL','').rstrip('/')
url = urlparse(base)
if not base or (url.scheme != 'https' and not (url.scheme == 'http' and url.hostname in ['localhost','127.0.0.1'])):
    parser.error('Set PROBE_BASE_URL to the HTTPS host URL (or local HTTP for local checks).')
if args.action != 'health' and not args.job_id:
    parser.error('Supply --job-id UUID; reuse it across steps and restarts.')
headers = {'Authorization':'Bearer '+os.environ.get('PROBE_TOKEN','')}
try:
    if args.action == 'step':
        response = requests.post(base+'/step',json={'job_id':str(args.job_id),'source':args.source},headers=headers,timeout=(15,90))
    elif args.action == 'verify':
        response = requests.get(base+'/verify',params={'job_id':str(args.job_id)},headers=headers,timeout=(15,90))
    else:
        response = requests.get(base+'/healthz',timeout=(15,90))
    print('HTTP',response.status_code)
    print(json.dumps(response.json(),indent=2))
except requests.RequestException as exc:
    print(type(exc).__name__+': request did not finish. Query the same job ID before retrying; do not assume it failed or completed.')
    raise SystemExit(1)
