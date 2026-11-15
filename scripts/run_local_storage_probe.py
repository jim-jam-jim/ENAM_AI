"""One local-origin checkpoint operation using real Neon; not a Render test."""
import argparse
import json
import uuid
from pathlib import Path
from scripts.host_probe import step,verify

parser=argparse.ArgumentParser()
parser.add_argument('action',choices=['step','verify'])
parser.add_argument('--source',choices=['small','large'],default='small')
args=parser.parse_args()
path=Path('data/checks/local-neon-job-'+args.source+'.json')
if path.exists():
    record=json.loads(path.read_text())
else:
    record={'job_id':str(uuid.uuid4()),'origin':'local Windows; NOT Render','results':[]}
try:
    result=step(uuid.UUID(record['job_id']),args.source) if args.action=='step' else verify(uuid.UUID(record['job_id']))
    record['results'].append(result)
    path.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
except Exception as exc:
    print(json.dumps({'error_type':type(exc).__name__,'details':'Provider error omitted; no hosted success claimed'}))
    raise SystemExit(1)
