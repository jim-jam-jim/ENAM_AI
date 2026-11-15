"""Publish reviewed metadata with the actual Render-extracted passage into Neon.

Does not modify probe jobs or stored PDFs. No local-data fallback in the API.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import psycopg
from psycopg.types.json import Jsonb
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')

def publish():
    data=json.loads((ROOT/'data/curated/infy.json').read_text(encoding='utf-8'))
    with psycopg.connect(os.environ['DATABASE_URL'],connect_timeout=15) as conn:
        row=conn.execute('SELECT phase,payload FROM finn_probe_jobs WHERE id=%s',
                         ('54ee3a54-ff5c-4206-b1d1-77066dd28ab2',)).fetchone()
        if not row or row[0]!='complete':
            raise ValueError('Hosted source incomplete')
        source=row[1]
        evidence=data['evidence']['infy-fcf-202609']
        if source['sha256']!=evidence['sha256'] or source['source_url']!=evidence['url']:
            raise ValueError('Source identity mismatch')
        passage=next(p['text'] for p in source['pages'] if p['page']==4)
        if not all(v in passage for v in ['8,898','9,677','Sep 30, 2026','Sep 30, 2025']):
            raise ValueError('Reviewed figures missing from hosted passage')
        evidence.update(passage=passage,retrieved_at=source['fetched_at_utc'])
        data['coverage'].update(retrieved_at=source['fetched_at_utc'],note='Infosys only · 2 curated disclosures; partial coverage')
        data['published_at']=datetime.now(timezone.utc).isoformat()
        for event in data['events']:
            event['summary_origin']='Manually curated summary · no AI synthesis'
        data['events'][0].update(document_date='2026-10-23',reporting_period='Q2 FY2027 · quarter ended 30 Sep 2026',retrieved_at=source['fetched_at_utc'],pdf_page=4)
        conn.execute('CREATE TABLE IF NOT EXISTS finn_read_models (id text PRIMARY KEY,payload jsonb NOT NULL,updated_at timestamptz NOT NULL DEFAULT now())')
        conn.execute('INSERT INTO finn_read_models(id,payload) VALUES (%s,%s) ON CONFLICT(id) DO UPDATE SET payload=EXCLUDED.payload,updated_at=now()',('infy-q2-fy2027',Jsonb(data)))
    print(json.dumps({'published':True,'source':'Render-extracted Neon passage','page':4,'events':len(data['events'])}))

if __name__=='__main__':
    try:
        publish()
    except Exception as exc:
        print(json.dumps({'published':False,'error_type':type(exc).__name__}))
        raise SystemExit(1)
