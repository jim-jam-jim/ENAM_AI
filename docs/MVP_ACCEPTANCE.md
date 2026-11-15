# MVP acceptance — in progress

Live application: https://finn-source-probe-tkef.onrender.com

## Verified on Render
- Public root serves FINN. Prepared Infosys event and page-4 cash-flow evidence return from Neon; reported figures 8,898 / 9,677 INR crore produce -8.1% in code.
- Full refresh attempted all 15 companies. Announcement feeds succeeded for all 15. Yahoo price requests returned HTTP 429 for all 15; existing real 63-session histories remain cached and stale. No hosted price-refresh success claimed.
- All eight primary BSE annual-report/transcript URLs for INFY, DABUR, HCLTECH and VOLTAS downloaded from Render and matched the retained object hashes.
- Infosys annual report completed 383 pages and transcript completed 48 pages. Both passed company/type checks. Annual report identifies FY2025–26; transcript is Q2 FY2027.
- Question and alert thresholds written through Render survived deployment restart, with the same stored question timestamp and threshold values.
- Nine eligible alert calculations independently matched deployed results. Price compares prior close; volume averages 20 prior completed sessions, excluding latest. Six corporate-action windows were explicitly unavailable. These use stale cached market data, not fresh hosted prices.
- Empty 24-hour prepared window returns zero events; invalid window returns 422; missing evidence/passages return 404; unauthenticated diagnostic returns 401.

## Tests and failures retained
- 17 automated tests passed, including citation rejection, duplicate/revised filings, lease contention/expiry, unsafe calculation baselines, quota guards and protected routes.
- Production Next.js build passed.
- Session advisory locks failed through the database pooler. Replaced by expiring row leases; restarted jobs retain page checkpoints. Deployment interrupted Dabur processing; the lease expired automatically and processing resumed from page 455 to 475 without duplicating earlier pages.
- Gemini 2.5 Flash-Lite metadata succeeded but generation returned 404: unavailable to new users. Explicitly selected current free-tier 3.5 Flash-Lite. A real local answer returned matched source quotations; first hosted generation and one bounded retry returned provider 503. Hosted cited research is not yet accepted.
- Browser access became unavailable in this chat. Earlier local mobile/desktop checks are retained; final deployed visual/interaction testing is not claimed.

## Remaining acceptance
Finish other document extraction, inspect reporting periods, verify one useful cited hosted answer per prepared company plus VOLTAS, and run isolated historical-replay saved-question assessment. Preserve limitations if provider quota/service blocks a check. No canned answers.

## Deliberate limits
Manual refresh only. No scheduled monitoring, trading, voice, paid fallback or cross-device login. OCR and automatic financial-table validation are not guaranteed. Exact citation quotes prove provenance, not that every model inference is correct.

Raw records are in data/checks/mvp-*.json. Original development conversation exports remain required alongside BUILD_HISTORY.md.

## Final verification update
All eight research documents completed on Render: INFY annual/transcript 383/48 pages; DABUR 623/20; HCLTECH 485/26; VOLTAS 278/21. Hosted Gemini answers succeeded for DABUR, HCLTECH and VOLTAS; inspected answers have exact source quotations but limited analytical coverage. Dabur cash evidence is indirect, and HCLTECH/VOLTAS each retained one verifiable claim. Infosys broad research remained blocked by two provider 503s; a separate local Infosys answer succeeded. No repeated Dabur generation.

Saved-question assessment completed on Render using an isolated, explicitly labelled historical replay. The test question timestamp predates a real transcript; original filing dates are unchanged. User questions persist across redeploy; the replay does not claim a new disclosure arrived after the user saved a question.

Blocking UI fixes in commit 37dac53: contrast across primary/disabled/focus states; consistent identity-checked source readiness; question-specific retrieval errors; unsupported price-prediction explanation; clearing company-change errors and bounded loading states. Production build passed, 17 existing tests passed plus two new regression tests. Deployment of this commit requires the user dashboard action; final live readiness verification pending. Browser tools still report unavailable, so final visual interaction verification is not claimed.

## Handoff status — final deployed checks
User confirmed deployment. Live API reports Infosys sources ready, and the next-day prediction guard returns its specific explanation before model usage. Served CSS contains the normal and disabled primary-button contrast fixes. All four cached successful-answer citation passages return HTTP 200 from the deployed API and match their quotations. This is HTTP/API verification, not visual browser verification; browser access remains unavailable.

### Answer usefulness review
- Dabur: the growth observation is supported by transcript page 12, but the impairment-testing projection on annual-report page 437 is not evidence of actual operating cash generation. The broad cash-generation question is only partially answered. Both observations are labelled interpretation even though much of their content is reported fact. Its claim that the provided documents lack full cash-flow statements should be understood as a retrieval limitation, not a finding that the annual report lacks them.
- HCLTech: the cash-generation figures are supported by transcript page 15 and are useful as a narrow reported observation. The retained answer does not establish growth quality or a multi-period comparison.
- VOLTAS: annual-report page 84 supports the cited consolidated income/profit amounts and period. This is useful business context, but does not answer cash generation; its interpretation label is overly broad.
- Infosys: a real local answer exists, but the broad hosted research call returned provider 503 twice. No further repetitive calls were made. The separate hosted saved-question replay completed with an inconclusive assessment.

Research therefore passes generation/provenance checks for three companies but remains PARTIAL on answer usefulness and completeness. Do not call this fully accepted research or complete challenge scope.

### Five-minute manual browser review still required
1. Open the live root at phone width (~390px), then desktop. Confirm primary buttons have readable white-on-green text, disabled controls remain readable, and keyboard focus is visible.
2. Select Historical example, open Infosys results, inspect the cash passage and original page-4 PDF. Confirm figures and dates wrap without horizontal overflow.
3. Open Company research → INFY. Confirm sources ready, no old processing error. Ask “stock prediction tomorrow?” and confirm the specific limitation; change company and confirm the error clears.
4. Open HCLTECH and ask “What cash generation did management report for the last twelve months?” Check loading clears after success/failure; inspect the cited passage and original PDF. This suggested question has not itself been generated in acceptance testing.
5. Save a question, reload, and confirm it persists. Change alert thresholds, save and reload. Inspect stale-price labels and the manual-refresh label. No scheduled monitoring is implied.

Submission: repository and honest covering-note draft are prepared. Original chat exports/share links still need attachment; BUILD_HISTORY is only an index. No email sent.
