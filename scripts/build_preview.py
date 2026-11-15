"""Build a labelled visual-review snapshot from manually verified source figures."""
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source_url = 'https://nsearchives.nseindia.in/corporate/Infosys_23102026160704_BM_Outcome_Oct232026_1.pdf'
current, previous = Decimal('8898'), Decimal('9677')
change = ((current / previous - 1) * 100).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
output = {
    'mode':'Design review — manually selected real evidence, not working AI research',
    'as_of':'2026-11-15',
    'source_checked_at':'2026-11-15',
    'company':'Infosys Limited',
    'ticker':'INFY',
    'question':'Is this company growing without weakening cash generation?',
    'question_state':'Example question — not saved',
    'event_date':'2026-10-23',
    'current_fcf':str(current), 'previous_fcf':str(previous), 'change_percent':str(change),
    'units':'INR crore',
    'current_period':'Quarter ended 30 Sep 2026',
    'previous_period':'Quarter ended 30 Sep 2025',
    'basis':'Consolidated; company-defined FCF based on IFRS cash flows',
    'source_url':source_url,
    'pdf_page':4, 'printed_page':'Fact sheet 2 of 4',
    'selection_note':'Manual example: results contain comparable cash figures relevant to the question. This observation alone does not establish the reason for the decline.',
    'routine_date':'2026-11-04',
    'routine_title':'Investor conference notice',
    'routine_url':'https://nsearchives.nseindia.in/corporate/INFY_04112026210117_SE_filing_Investor_conference_04112026_signed.pdf',
    'routine_evidence':'Title and timestamp verified in NSE feed; attachment not downloaded in this check.'
}
(ROOT/'preview').mkdir(exist_ok=True)
(ROOT/'preview/evidence.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
print(f'Computed FCF change: {change}% from source values {current} and {previous} INR crore.')
