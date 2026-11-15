# FINN submission preparation — not ready to send

Working URL: https://finn-source-probe-tkef.onrender.com
Repository: https://github.com/jim-jam-jim/ENAM_AI

FINN starts with a portfolio briefing and lets an investor inspect the source behind a disclosure, research a company using annual reports and earnings calls, and save one question to watch. The prototype uses a mock 15-company portfolio, a static Next.js interface, one FastAPI application, and Neon PostgreSQL/object storage. Gemini is restricted to the configured free-tier model and application quotas.

## Review walkthrough to validate before submission
1. Open the briefing; choose 24 hours, 7 days, or 30 days. Empty windows keep the real event dates. Open Historical example for the prepared Infosys cash-flow comparison.
2. Inspect the reported figures, calculation, interpretation and source passage; follow the original PDF link.
3. Expand portfolio coverage and EOD alerts. Inspect per-source freshness/failures and change the thresholds.
4. Open Company research for INFY, DABUR or HCLTECH. Check source readiness, ask a question, inspect quotations, and save the question.
5. Try an unfamiliar NSE ticker through the same document workflow. VOLTAS is the separate acceptance-test ticker, not a prepared example.

## Must be resolved before calling the MVP complete
- Finish hosted annual-report/transcript extraction and identity/period review for all four tested companies.
- Verify real Gemini answers and citations on the host, without repeating successful calls unnecessarily.
- Finish full Render-origin portfolio refresh and saved-question/alert persistence checks.
- Test subsequent-evidence assessment with clearly labelled test history, without changing real disclosure dates.
- Complete final deployed mobile/desktop interaction checks after fixes.

## Deliberate limits
Manual refresh only; no scheduled or continuous monitoring. A sleeping service pauses work. Source coverage is partial and access can fail. No trading, voice, elaborate authentication, OCR guarantee or paid model fallback. Browser workspace settings have no cross-device account recovery.

## Actual build history
BUILD_HISTORY.md indexes this real development conversation and meaningful failures/fixes. Original conversation exports/share links still need to be supplied; do not replace them with a generated summary or invent URLs. Earlier planning-chat export is also pending.

This is a draft covering-note source, not a statement that every workflow has passed. No submission email has been sent.
