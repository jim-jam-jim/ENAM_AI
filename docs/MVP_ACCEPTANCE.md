# FINN prototype acceptance — 15 November 2026

Live: https://finn-source-probe-tkef.onrender.com

Status: deployed prototype with verified engineering and partial research acceptance. This is not a claim that every MVP acceptance criterion passed. Application commit: 37dac53; subsequent submission commits update documentation and records only.

## Verified on Render
- Root serves FINN. The prepared historical Infosys event and page-4 cash-flow evidence come from Neon. Reported figures 8,898 / 9,677 INR crore produce -8.1% in code.
- Announcement refresh succeeded for all 15 portfolio companies. Price refresh was attempted for all 15; real 63-session cached histories were retained after HTTP 429 responses and labelled stale.
- All eight primary BSE annual-report/transcript PDFs downloaded from Render, matched retained object hashes and completed extraction: INFY 383/48 pages, DABUR 623/20, HCLTECH 485/26, VOLTAS 278/21. Company/type checks passed. Infosys annual report identifies FY2025–26; transcript Q2 FY2027. This does not establish accuracy of every extracted table or period in each document.
- Real hosted Gemini answers succeeded for Dabur, HCLTech and the separate unfamiliar ticker VOLTAS. Four retained citation passages returned HTTP 200 and matched their quotations. Analytical usefulness is assessed separately below.
- Saved questions and alert thresholds survived deployment restart with unchanged values/timestamp. A saved-question assessment completed with an inconclusive result in an isolated, labelled historical replay; this is not proof of a new live disclosure arriving after a user's question.
- Nine eligible alert calculations independently matched deployed results. Price compares prior close; volume uses the mean of 20 prior completed sessions, excluding latest. Six corporate-action windows were explicitly unavailable. Calculations use the stale cached histories.
- Empty 24-hour prepared window returns zero events; invalid window 422; missing passages 404; unauthenticated diagnostic 401.
- Interrupted document extraction resumed from durable checkpoints without duplicate page keys. Earlier 48-page/195-page diagnostics verified restart persistence and object round trips; large-bundle active processing was 124.958 seconds, observed peak RSS 170.03 MiB. These bounded measurements are not a guarantee for every PDF.

## Build and regression checks
Production Next.js build passed. Seventeen existing automated tests plus two focused regression checks passed, covering citations, duplicates/revised filings, lease contention/expiry, calculation baselines, quota guards, protected routes and question-specific errors. Recorded failures and fixes remain in BUILD_HISTORY.md and data/checks; checks were reused rather than rerun without a relevant code change.

## External service failures
- Yahoo hosted retrieval returned HTTP 429 for all 15 companies. This is rate-limited hosted retrieval; whether the restriction is daily, IP-based or otherwise is unknown. No promised recovery time or definitive free-tier-quota attribution. Real cached prices remain available and labelled stale.
- Infosys hosted Gemini research returned HTTP 503 on two attempts: provider availability failures during those attempts, not a proven rate-limit issue. Other hosted Gemini research requests succeeded; a local Infosys answer also succeeded.
- Original Infosys company-site documents returned HTTP 403. Separately identified exchange-hosted primary documents were successfully processed; the original failure remains recorded.

## Product-quality limitations
Exact quote matching establishes provenance, not relevance, completeness or correct inference. Better retrieval, financial context and prompts are improvements to evaluate; a stronger model could also be evaluated later, without assuming it would solve the problem. No model change or paid usage is part of this submission.

### Answer usefulness review
- Dabur: the growth observation is supported by transcript page 12, but the impairment-testing projection on annual-report page 437 is not evidence of actual operating cash generation. The broad cash-generation question is only partially answered. Both observations are labelled interpretation even though much of their content is reported fact. Its claim that the provided documents lack full cash-flow statements should be understood as a retrieval limitation, not a finding that the annual report lacks them.
- HCLTech: the cash-generation figures are supported by transcript page 15 and are useful as a narrow reported observation. The retained answer does not establish growth quality or a multi-period comparison.
- VOLTAS: annual-report page 84 supports the cited consolidated income/profit amounts and period. This is useful business context, but does not answer cash generation; its interpretation label is overly broad.
- Infosys: a real local answer exists, but the broad hosted research call returned provider 503 twice. No further repetitive calls were made. The separate hosted saved-question replay completed with an inconclusive assessment.

Research therefore passes generation/provenance checks for three companies but remains PARTIAL on answer usefulness and completeness. Do not call this fully accepted research or complete challenge scope.

## Deliberately deferred features
Scheduled background refresh and unattended monitoring are deferred by the user's decision. Manual refresh is implemented; background progress while Render sleeps is not promised. This is an intentional prototype boundary, not a broken implemented scheduler. Trading, voice, paid fallbacks and cross-device accounts are also excluded. No OCR or automatic financial-table-validation guarantee.

## Verification gap and public accessibility
Final deployed browser interaction/visual verification was unavailable. Earlier local phone/desktop checks are recorded but do not verify the final deployed UI. Final HTTP/API checks confirmed root availability, identity-checked Infosys readiness, the prediction-specific explanation, served normal/disabled button CSS, and accessible citation passages. They do not prove rendered contrast, keyboard focus, loading recovery or working clicks.

Anonymous HTTP GETs on 15 November 2026 returned 200 for both the prototype and public GitHub repository, with expected content. See data/checks/submission-public-access.json. This is not an interactive browser test.

### Five-minute manual browser review still required
1. Open the live root at phone width (~390px), then desktop. Confirm primary buttons have readable white-on-green text, disabled controls remain readable, and keyboard focus is visible.
2. Select Historical example, open Infosys results, inspect the cash passage and original page-4 PDF. Confirm figures and dates wrap without horizontal overflow.
3. Open Company research → INFY. Confirm sources ready, no old processing error. Ask “stock prediction tomorrow?” and confirm the specific limitation; change company and confirm the error clears.
4. Open HCLTECH and ask “What cash generation did management report for the last twelve months?” Check loading clears after success/failure; inspect the cited passage and original PDF. This suggested question has not itself been generated in acceptance testing.
5. Save a question, reload, and confirm it persists. Change alert thresholds, save and reload. Inspect stale-price labels and the manual-refresh label. No scheduled monitoring is implied.

## Submission records
See SUBMISSION_DRAFT.md for the exact covering email and SUBMISSION_CHECKLIST.md for required links/attachments. Original planning and development conversations are still required; BUILD_HISTORY.md only indexes them. No email sent.
