"""Small protected deployment diagnostic, not the FINN application API.

POST /step {"job_id": UUID} twice: fetch/upload, then extract/checkpoint.
GET /verify?job_id=UUID after restart: read DB and object, compare hash.
No model, no local persistent state, no arbitrary URL fetch endpoint.
"""
import hashlib
import hmac
import io
import json
import os
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import boto3
from botocore.config import Config
from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Jsonb
from pypdf import PdfReader
import requests

load_dotenv()
SOURCE = 'https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q4/documents/transcripts/earningscall.pdf'
SOURCES = {'small': SOURCE, 'large': 'https://www.infosys.com/investors/reports-filings/annual-report/annual/documents/infosys-ar-26.pdf'}
SOURCES.update({
    'small-exchange': 'https://nsearchives.nseindia.in/corporate/Infosys_28102026173824_SE_filing_Earnings_call_transcript.pdf',
    'large-exchange': 'https://nsearchives.nseindia.in/corporate/Infosys_23102026160704_BM_Outcome_Oct232026_1.pdf',
})
REQUIRED = ['DATABASE_URL', 'AWS_ENDPOINT_URL_S3', 'AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'DOCUMENT_BUCKET', 'PROBE_TOKEN']
BOOT = str(uuid.uuid4())
MAX_BYTES = 50 * 1024 * 1024

def storage():
    return boto3.client('s3', endpoint_url=os.environ['AWS_ENDPOINT_URL_S3'],
                        region_name=os.environ['AWS_REGION'],
                        config=Config(s3={'addressing_style': 'path'}, connect_timeout=10,
                                      read_timeout=20, retries={'max_attempts': 1}))

def db():
    conn = psycopg.connect(os.environ['DATABASE_URL'], connect_timeout=15, autocommit=True)
    conn.execute("SET statement_timeout = '15s'")
    conn.execute('''CREATE TABLE IF NOT EXISTS finn_probe_jobs (
        id uuid PRIMARY KEY, phase text NOT NULL, payload jsonb NOT NULL,
        updated_at timestamptz NOT NULL DEFAULT now())''')
    return conn

def read_object(client, key):
    body = client.get_object(Bucket=os.environ['DOCUMENT_BUCKET'], Key=key)['Body']
    try:
        data = body.read(MAX_BYTES + 1)
    finally:
        body.close()
    if len(data) > MAX_BYTES:
        raise ValueError('Probe object exceeds size limit')
    return data

def step(job_id, source_name='small'):
    if source_name not in SOURCES:
        raise ValueError('Unknown diagnostic source')
    with db() as conn:
        conn.execute('INSERT INTO finn_probe_jobs(id, phase, payload) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING',
                     (job_id, 'queued', Jsonb({'source_url': SOURCES[source_name], 'created_at_utc': datetime.now(timezone.utc).isoformat()})))
        phase, payload = conn.execute('SELECT phase,payload FROM finn_probe_jobs WHERE id=%s', (job_id,)).fetchone()
        client = storage()
        if phase == 'queued':
            started = time.monotonic()
            with requests.get(payload['source_url'], stream=True, timeout=(10,20), headers={'User-Agent':'FINN-host-probe/0.1'}) as response:
                response.raise_for_status()
                chunks, size = [], 0
                for chunk in response.iter_content(64*1024):
                    size += len(chunk)
                    if size > MAX_BYTES or time.monotonic()-started > 60:
                        raise ValueError('Download exceeded diagnostic budget')
                    chunks.append(chunk)
                data = b''.join(chunks)
            if not data.startswith(b'%PDF'):
                raise ValueError('Expected a PDF')
            digest = hashlib.sha256(data).hexdigest()
            key = f'probe/sha256/{digest}.pdf'
            client.put_object(Bucket=os.environ['DOCUMENT_BUCKET'], Key=key, Body=data, ContentType='application/pdf')
            payload.update(sha256=digest, object_key=key, bytes=len(data), fetched_at_utc=datetime.now(timezone.utc).isoformat(), fetch_seconds=round(time.monotonic()-started,3))
            phase = 'stored'
        elif phase in ['stored','extracting']:
            data = read_object(client, payload['object_key'])
            if hashlib.sha256(data).hexdigest() != payload['sha256']:
                raise ValueError('Object hash mismatch')
            reader = PdfReader(io.BytesIO(data))
            passages = payload.get('pages',[])
            cursor = len(passages)
            stage_start = time.monotonic()
            # Commit page checkpoints individually so a killed operation can resume.
            for i in range(cursor,min(cursor+20,len(reader.pages))):
                passages.append({'page':i+1,'text':reader.pages[i].extract_text()})
                phase='complete' if len(passages)==len(reader.pages) else 'extracting'
                payload.update(pages=passages,page_count=len(reader.pages),extraction='pypdf',completed_pages=len(passages))
                if phase=='complete':
                    if not any(len(p['text'].strip())>80 for p in passages):
                        raise ValueError('No readable source passages')
                    payload['completed_at_utc']=datetime.now(timezone.utc).isoformat()
                conn.execute('UPDATE finn_probe_jobs SET phase=%s,payload=%s,updated_at=now() WHERE id=%s',(phase,Jsonb(payload),job_id))
                if time.monotonic()-stage_start>20:
                    break
        if phase != 'complete' or not payload.get('completed_at_utc'):
            conn.execute('UPDATE finn_probe_jobs SET phase=%s,payload=%s,updated_at=now() WHERE id=%s', (phase, Jsonb(payload), job_id))
    return {'job_id':str(job_id), 'phase':phase, 'boot_id':BOOT,
            'page_count':payload.get('page_count'), 'completed_pages':payload.get('completed_pages'), 'sha256':payload.get('sha256'), 'memory':memory_usage()}

def memory_usage():
    if os.name != 'posix':
        return {'measurement':'host measurement unavailable on this OS'}
    import resource
    return {'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'cgroup_peak_bytes':Path('/sys/fs/cgroup/memory.peak').read_text().strip() if Path('/sys/fs/cgroup/memory.peak').exists() else None,
            'cgroup_limit_bytes':Path('/sys/fs/cgroup/memory.max').read_text().strip() if Path('/sys/fs/cgroup/memory.max').exists() else None}

def verify(job_id):
    with db() as conn:
        row = conn.execute('SELECT phase,payload,updated_at FROM finn_probe_jobs WHERE id=%s', (job_id,)).fetchone()
    if not row:
        return {'job_id':str(job_id), 'phase':'not_found', 'boot_id':BOOT}
    phase,payload,updated_at = row
    matches = None
    if payload.get('object_key'):
        matches = hashlib.sha256(read_object(storage(),payload['object_key'])).hexdigest() == payload['sha256']
    return {'job_id':str(job_id),'phase':phase,'boot_id':BOOT,'object_hash_matches':matches,
            'page_count':payload.get('page_count'),'passages_present':bool(payload.get('pages')),
            'completed_pages':len(payload.get('pages',[])),
            'unique_pages':len({p['page'] for p in payload.get('pages',[])}),
            'updated_at':updated_at.isoformat()}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Do not log credentials, query strings or provider errors.

    def reply(self, status, payload):
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def allowed(self):
        token = os.environ.get('PROBE_TOKEN','')
        supplied = self.headers.get('Authorization','').removeprefix('Bearer ')
        if len(token) < 32 or not hmac.compare_digest(token, supplied):
            self.reply(401, {'error':'Unauthorised or probe token not configured'})
            return False
        missing = [key for key in REQUIRED if not os.environ.get(key)]
        if missing:
            self.reply(503, {'error':'Configuration incomplete','missing_keys':missing})
            return False
        return True

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/healthz':
            self.reply(200, {'service':'FINN diagnostic only','boot_id':BOOT,'configured':all(os.environ.get(k) for k in REQUIRED)})
            return
        if parsed.path != '/verify':
            self.reply(404, {'error':'Not found'})
            return
        if not self.allowed():
            return
        try:
            job_id = uuid.UUID(parse_qs(parsed.query).get('job_id',[''])[0])
        except ValueError:
            self.reply(400, {'error':'A UUID job_id is required'})
            return
        self.execute(lambda: verify(job_id))

    def do_POST(self):
        if self.path != '/step':
            self.reply(404, {'error':'Not found'})
            return
        try:
            length = int(self.headers.get('Content-Length','0'))
            if length < 1 or length > 1024:
                raise ValueError('Invalid body size')
            body = self.rfile.read(length)
        except ValueError:
            self.reply(400, {'error':'Invalid body size'})
            return
        if not self.allowed():
            return
        try:
            payload = json.loads(body)
            job_id = uuid.UUID(payload['job_id'])
            source_name=payload.get('source','small')
            if source_name not in SOURCES:
                raise ValueError('Invalid source')
        except (ValueError, KeyError, TypeError):
            self.reply(400, {'error':'Expected a small JSON body with UUID job_id'})
            return
        self.execute(lambda: step(job_id,source_name))

    def execute(self, action):
        started = time.monotonic()
        try:
            result = action()
            result['seconds'] = round(time.monotonic()-started,3)
            self.reply(200,result)
        except Exception as exc:
            # Deliberately omit message/traceback: drivers may include secrets/DSNs.
            details = {}
            if isinstance(exc, requests.HTTPError) and exc.response is not None:
                details = {'source_http_status':exc.response.status_code,
                           'source_host':urlparse(exc.response.url).hostname}
            self.reply(503, {'error_type':type(exc).__name__, **details, 'message':'Probe stage failed; last committed checkpoint is retained. Inspect provider dashboards and retry the same job ID.', 'boot_id':BOOT})

if __name__ == '__main__':
    # One diagnostic operation at a time; no background execution guarantee.
    HTTPServer(('0.0.0.0',int(os.environ.get('PORT','10000'))),Handler).serve_forever()
