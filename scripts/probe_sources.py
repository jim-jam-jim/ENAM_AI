"""Read-only public-source spike. Not FINN's production ingestion pipeline.

Run from repository root: python -X utf8 scripts/probe_sources.py
Each run writes a new timestamped directory; it never replaces an earlier result.
"""
import concurrent.futures
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import fitz

ROOT = Path(__file__).resolve().parents[1]
RUN = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
RAW = ROOT / 'data' / 'raw' / RUN
TEXT = ROOT / 'data' / 'extracted' / RUN
REPORT = ROOT / 'data' / 'checks'

def probe(item):
    start = time.monotonic()
    result = dict(item, checked_at_utc=datetime.now(timezone.utc).isoformat())
    try:
        response = requests.get(item['url'], headers={'User-Agent': 'Mozilla/5.0 (compatible; FINN-source-check/0.1)'}, timeout=(12, 45))
        result.update(status=response.status_code, final_url=response.url,
                      content_type=response.headers.get('content-type'), bytes=len(response.content),
                      sha256=hashlib.sha256(response.content).hexdigest())
        response.raise_for_status()
        kind = item['kind']
        extension = 'pdf' if response.content.startswith(b'%PDF') else ('json' if 'json' in response.headers.get('content-type', '') else 'html')
        path = RAW / (item['id'] + '.' + extension)
        path.write_bytes(response.content)
        result['local_path'] = str(path.relative_to(ROOT))
        if extension == 'pdf':
            with fitz.open(stream=response.content, filetype='pdf') as doc:
                pages = [{'page': i+1, 'text': page.get_text()} for i, page in enumerate(doc)]
            target = TEXT / (item['id'] + '.json')
            target.write_text(json.dumps(pages, ensure_ascii=False), encoding='utf-8')
            readable = sum(len(p['text'].strip()) > 80 for p in pages)
            result.update(pages=len(pages), readable_pages=readable,
                          extracted_path=str(target.relative_to(ROOT)),
                          sample=next((p['text'][:450] for p in pages if len(p['text'].strip()) > 80), ''),
                          outcome='readable_pdf' if readable else 'needs_ocr')
        elif kind == 'prices':
            chart = response.json()['chart']['result'][0]
            quotes = chart['indicators']['quote'][0]
            rows = [{'date': datetime.fromtimestamp(t, timezone.utc).isoformat(),
                     'close': c, 'volume': v} for t,c,v in zip(chart['timestamp'], quotes['close'], quotes['volume']) if c is not None and v is not None]
            result.update(outcome='price_rows' if rows else 'empty_prices', rows=len(rows), currency=chart['meta'].get('currency'), symbol=chart['meta'].get('symbol'), first=rows[0] if rows else None, last=rows[-1] if rows else None)
        elif kind == 'announcements':
            payload = response.json()
            rows = payload if isinstance(payload, list) else payload.get('data', [])
            result.update(outcome='announcement_rows' if rows else 'empty_announcements', rows=len(rows), sample=rows[:1])
        else:
            result['outcome'] = 'html_downloaded_not_yet_validated'
    except Exception as exc:
        result.update(outcome='failed', error=f'{type(exc).__name__}: {exc}')
    result['seconds'] = round(time.monotonic()-start, 2)
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', default='data/source_candidates.json')
    args = parser.parse_args()
    items = json.loads((ROOT / args.manifest).read_text(encoding='utf-8'))
    for directory in [RAW, TEXT, REPORT]:
        directory.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(probe, items))
    report = REPORT / (RUN + '.json')
    report.write_text(json.dumps({'environment': 'local Windows; NOT deployed-host verification', 'results': results}, indent=2, ensure_ascii=False), encoding='utf-8')
    for result in results:
        print(json.dumps({k:result[k] for k in ['id','outcome','status','bytes','pages','readable_pages','rows','seconds','error'] if k in result}))
    print(f'Report: {report}')

if __name__ == '__main__':
    main()
