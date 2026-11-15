# FINN

[Prototype](https://finn-source-probe-tkef.onrender.com) · [Repository](https://github.com/jim-jam-jim/ENAM_AI)

FINN is a mobile-first investor briefing for a mock 15-company portfolio, with inspectable event evidence, document-grounded research, one saved question per company and configurable in-app EOD alerts. A static Next.js frontend is served by one FastAPI application on Render. Neon PostgreSQL retains structured evidence, questions and durable jobs; private object storage retains PDFs.

This is a deployed prototype with partial research acceptance, not a fully verified finished product. See [acceptance evidence](docs/MVP_ACCEPTANCE.md), [covering email](docs/SUBMISSION_DRAFT.md) and [submission checklist](docs/SUBMISSION_CHECKLIST.md).

## Quick review
Select Historical example, open the Infosys event and inspect the figures, code-calculated comparison, supporting passage and original PDF. This stored, manually curated example uses real dates and does not call Gemini. Recent windows can be empty. Inspect all 15 companies and their freshness/coverage, then company research and alert settings.

Prior hosted research for Dabur, HCLTech and VOLTAS is retained in data/checks/mvp-hosted-research.json. Those test results are not a shared in-app cache for new visitors. Research caches belong to anonymous browser workspaces; a new question/workspace can make a new model call. Suggested HCLTech question: “What cash generation did management report for the last twelve months?” That exact question is a suggestion, not a previously verified answer.

## Setup and running
Use Python 3.11 and Node.js 22. Copy .env.example to ignored .env, enter values privately, then:

```powershell
python -m pip install -r requirements.txt
cd web
npm ci
npm run build
cd ..
python -m uvicorn server.main:app --host 127.0.0.1 --port 8766
```

Open http://127.0.0.1:8766. All application APIs are Python-owned. The historical API reads Neon records/passages, with no frontend fixture fallback. data/curated/infy.json is the reviewed seed; scripts/publish_read_model.py joins it to an existing completed hosted diagnostic source. A fresh empty database needs source processing and this seed publication before that historical example is available.

Required private configuration (no secret values belong in Git):
- DATABASE_URL: Neon connection string with SSL parameters.
- AWS_ENDPOINT_URL_S3, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DOCUMENT_BUCKET: private object storage configuration.
- PROBE_TOKEN: protects diagnostic routes. PROBE_BASE_URL is used by local diagnostic clients; PORT defaults to the deployment setting.
- GEMINI_API_KEY; GEMINI_MODEL=gemini-3.5-flash-lite; GEMINI_FREE_TIER_CONFIRMED=true only after confirming paid billing is disabled; GEMINI_REQUESTS_PER_DAY=20; GEMINI_REQUESTS_PER_MINUTE=2. Use lower caps if the account requires them. Failed attempts consume the conservative app quota. App caps cannot disable Google billing; use an unbilled project. No paid or model fallback.

Dockerfile.probe builds the static frontend and serves it through FastAPI. render.yaml targets the existing service; docs/DEPLOYMENT.md retains setup/probe instructions. No local laptop process is required for the deployed app. No new deployment is required for submission-only documentation updates.

## Tests and evidence
```powershell
python -m unittest discover -s tests -v
python scripts/audit_repository.py
```

The recorded production build passed, as did 17 existing tests and two focused regressions. data/checks contains hosted/API verification records and failures; docs/HOSTED_CHECKS.md contains the original bounded PDF restart/memory diagnostic. scripts/probe_sources.py and scripts/discover_probe_candidates.py are historical source-investigation helpers; preview/ is a labelled design review, not the deployed app. Downloaded full PDFs/text remain ignored locally or in private object storage, not in this repository.

## Verified capabilities
- Hosted announcement retrieval for all 15 companies; eight annual reports/transcripts fetched, hash-checked and extracted for INFY, DABUR, HCLTECH and separate unfamiliar ticker VOLTAS.
- Real hosted cited Gemini responses for Dabur, HCLTech and VOLTAS; exact quotation checks and independently reviewed relevance limitations.
- Durable document checkpoints, restart recovery, persisted questions/alert settings and a labelled historical saved-question assessment.
- Deterministic price change vs prior close and volume vs mean of 20 prior completed sessions, excluding latest. Insufficient/corporate-action windows suspend comparisons.
- Final deployed HTTP/API evidence, readiness, prediction guard and protected-diagnostic checks. Anonymous prototype/repository access returned 200 on 15 November 2026.

## External service limitations
Yahoo hosted price requests returned HTTP 429: rate-limited hosted retrieval with real cached prices retained and labelled stale. The restriction's duration and whether it is daily, IP-based or otherwise have not been established. Alerts use cached data; no recovery promise or definitive free-tier explanation.

Infosys hosted Gemini requests returned HTTP 503 twice: provider availability failures during those attempts, not a proven rate limit. Other hosted Gemini requests succeeded. Original Infosys company-hosted documents returned HTTP 403; separately identified exchange-hosted sources succeeded.

## Product-quality limitations
Some supported quotations do not adequately answer the research question. Exact quotation validation is not semantic relevance or complete financial analysis. Dabur cash evidence was indirect; HCLTech's narrow cash figures were useful without a growth comparison; VOLTAS's income/profit figures did not answer cash generation. Improvements to evaluate: retrieval, financial context, prompts and potentially a stronger model, without assuming a model change solves this. No model changes or paid usage are introduced.

## Deliberate omissions and verification gap
Manual refresh is implemented with durable progress and a one-hour reuse interval. Scheduled background refresh/unattended monitoring is deliberately deferred; progress while the service sleeps is not promised. No trading, voice or elaborate authentication. Workspace IDs live in browser storage; clearing them loses access to that workspace, and there is no cross-device recovery. No general OCR/table-validation guarantee.

Final deployed browser verification was unavailable. HTTP/API checks and served CSS checks passed; earlier local phone/desktop checks do not verify final rendered contrast, focus, loading recovery, link clicks or save/reload interactions. Exact manual checks are in docs/SUBMISSION_CHECKLIST.md. Original planning and development conversation exports are still needed; BUILD_HISTORY.md is only an index.

## Project records
PRD.md records scope; PLAN.md current status and historical progress; DECISIONS.md approvals/trade-offs; AGENTS.md working rules; BUILD_HISTORY.md actual development history. The submission email is prepared, not sent.
