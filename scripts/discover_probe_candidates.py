"""Extract follow-up URLs from downloaded indices; discovery is not validation."""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'data/raw/20261115T091353Z'
items = []
for ticker in ['DABUR', 'CERA']:
    soup = BeautifulSoup((source / f'{ticker}-discovery.html').read_text(encoding='utf-8'), 'html.parser')
    for kind, label in [('annual_report', 'Annual Report 2026'), ('transcript', 'Transcript')]:
        link = next(a for a in soup.select('a[href]') if a.get_text(' ', strip=True) == label)
        items.append(dict(id=f'{ticker}-{kind}-discovered', ticker=ticker, kind=kind, url=link['href'], discovery_source=f'https://www.screener.in/company/{ticker}/consolidated/'))
for kind, filename, label in [('annual_report','HCLTECH-annual-index','Annual Report 2025-26'),('transcript','HCLTECH-transcript-index','Earnings Conference Call Transcript')]:
    soup = BeautifulSoup((source / f'{filename}.html').read_text(encoding='utf-8'), 'html.parser')
    link = next(a for a in soup.select('a[href]') if a.get_text(' ', strip=True) == label)
    items.append(dict(id=f'HCLTECH-{kind}-discovered', ticker='HCLTECH', kind=kind, url=link['href']))
rows = json.loads((source / 'INFY-announcements.json').read_text())
for row in rows:
    if 'financial results' in row.get('attchmntText','').lower() and 'intimation' not in row.get('desc','').lower():
        items.append(dict(id='INFY-results-discovered', ticker='INFY', kind='filing', url=row['attchmntFile'], exchange_date=row['an_dt']))
        break
for ticker in ['DABUR','HCLTECH','CERA']:
    items.append(dict(id=f'{ticker}-announcements', ticker=ticker, kind='announcements', url=f'https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={ticker}&from_date=01-10-2026&to_date=15-11-2026'))
target = ROOT / 'data/discovered_candidates.json'
target.write_text(json.dumps(items, indent=2), encoding='utf-8')
print(target)
