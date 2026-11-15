"""Check configured private bucket access without printing credentials."""
import json
import os
from dotenv import load_dotenv
from scripts.host_probe import storage
load_dotenv()
try:
    client=storage()
    client.head_bucket(Bucket=os.environ['DOCUMENT_BUCKET'])
    print(json.dumps({'bucket_access':True,'origin':'local; not Render'}))
except Exception as exc:
    print(json.dumps({'bucket_access':False,'error_type':type(exc).__name__,'details':'Provider error omitted to protect credentials'}))
    raise SystemExit(1)
