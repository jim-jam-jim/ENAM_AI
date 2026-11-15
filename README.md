# FINN

FINN is a mobile investor briefing with inspectable evidence, a 15-company mock portfolio, company research, one saved question per company, and configurable in-app EOD alerts. Static Next.js assets are served by one FastAPI application. See docs/MVP_ACCEPTANCE.md for the authoritative verification status: implemented features are not all accepted yet.

## Actual local app
Install requirements.txt, run `npm ci` and `npm run build` inside web, then run `python -m uvicorn server.main:app --host 127.0.0.1 --port 8766` from the project root. Open http://127.0.0.1:8766. All application APIs are Python-owned. data/curated/infy.json is the reviewed seed for the historical example; the running API reads Neon records and stored source passages. The original design-review preview remains separate and labelled.

## Current contents
- PRD.md: approved scope/acceptance criteria; PLAN.md: progress and blockers.
- DECISIONS.md: accepted decisions versus proposals; AGENTS.md: stable working rules.
- BUILD_HISTORY.md: index to actual conversations and meaningful failures/fixes; original exports still needed.
- scripts/probe_sources.py: public HTTP downloads, PDF text extraction, price/feed checks.
- data/checks/: timestamped observed results, including sandbox failures.
- Downloaded originals and extracted full text are in ignored data/raw and data/extracted folders. Original temporary PDF previews remain untouched.

## Run the local source spike
Python 3.11 is available in the inspected environment. Dependencies currently used: requests, PyMuPDF (import fitz), beautifulsoup4. These are spike tools, not a final production dependency decision.

```powershell
python -m pip install requests PyMuPDF beautifulsoup4
python -X utf8 scripts/probe_sources.py
python -X utf8 scripts/discover_probe_candidates.py
python -X utf8 scripts/probe_sources.py --manifest data/discovered_candidates.json
```

The discovery script currently targets the recorded first successful download directory; it is a reproducible investigation helper, not a generic ticker engine. The checked-in discovered manifest can be fetched independently. No API key is needed for these local public-source checks. Network restrictions may require approval outside the execution sandbox.

## Deployment and secrets
Neon PostgreSQL is selected; Render and Neon Object Storage have passed the bounded NSE PDF diagnostic; full application deployment remains pending. See docs/DEPLOYMENT.md and .env.example for setup. Do not store secrets in Git or chat. Do not store full PDF bytes in PostgreSQL. No runtime model provider is selected or required for the source check.

## Verification and limitations
Successful download/text extraction does not prove numeric table correctness, automatic discovery coverage, production reliability or deployment success. Prepared URLs and date windows are explicit in data manifests. Full PDF text can contain stale hidden headers; use rendered checks for selected evidence. NSE PDF downloads, object hash round trips and checkpoint persistence across a Render restart have passed. See docs/HOSTED_CHECKS.md for measurements and limits. Cold-start testing, production research, continuous refresh and the 15-company portfolio remain incomplete.

## Visual review and diagnostic checks
```powershell
python -X utf8 scripts/build_preview.py
python -m http.server 8766 --bind 127.0.0.1 --directory preview
```
Open http://127.0.0.1:8766. This is one manually populated visual-review screen with real figures, not the working app. A screenshot is saved in preview/mobile-briefing.jpg.

```powershell
python -m pip install -r requirements-probe.txt
python -m unittest discover -s tests -v
python scripts/host_probe.py
```
The standard-library diagnostic listens on PORT (default 10000); set .env before cloud integration checks. Its diagnostic Docker image is deployed on Render; it does not yet serve the application. requirements-probe.txt uses bounded version ranges; a deployment lock and Docker build remain pending.

After setting PROBE_BASE_URL and PROBE_TOKEN privately, use `python scripts/probe_client.py health`, then `python scripts/probe_client.py step --job-id UUID` and `python scripts/probe_client.py verify --job-id UUID` with the same locally generated UUID. See docs/DEPLOYMENT.md for restart sequence.

Runtime model access first becomes necessary for grounded answer synthesis/evidence interpretation in milestone 2. Minimum: server-side text inference, sufficient context for selected passages, reliable structured claim/evidence IDs (native JSON schema preferred), and known limits/costs. Vision, embeddings, external search and agent frameworks are not initially required. No runtime model fixtures are presented as AI research.

Current application reads finn_read_models from Neon; it never falls back to frontend fixtures. Run python scripts/publish_read_model.py once to publish reviewed metadata joined to the existing hosted-extracted Infosys source (requires completed diagnostic job). Dockerfile.probe now builds Next.js then serves it through FastAPI; existing protected /verify and /step remain available. Existing documents/checkpoints are preserved.

## Full MVP runtime additions
The API initialises additive finn_records storage on startup, preserving diagnostic and published data. /api/portfolio reads 15 mock holdings. Refresh sources advances a durable 30-step price/filing refresh; progress resumes on request, with a one-hour reuse interval. Company research discovers primary report/transcript links using Screener only as an index, stores PDFs in Neon object storage and page passages in PostgreSQL. Process documents before asking Gemini. Research sends selected passages, validates exact quotations and caches answers. Saved questions and thresholds belong to an anonymous browser workspace retained in localStorage; no account recovery or cross-device sync.

Gemini variables: GEMINI_API_KEY, GEMINI_MODEL=gemini-3.5-flash-lite, GEMINI_FREE_TIER_CONFIRMED=true only after confirming paid billing is disabled, GEMINI_REQUESTS_PER_DAY=20, GEMINI_REQUESTS_PER_MINUTE=2. No frontend secret variables. Failed attempts consume the conservative application quota. App caps cannot disable billing on a Google project; use an unbilled project.

## Current service limitations
Hosted announcement refresh works for all 15 companies. Yahoo returns HTTP 429 from Render; retained EOD histories are real but stale, and alert results use that cached data. Manual refresh only, no scheduler. Model generation is free-tier Gemini 3.5 Flash-Lite; provider errors stop generation without canned answers or paid fallback. The original Infosys company-site PDFs return hosted HTTP 403; BSE/NSE primary filings are retained as separately identified sources. See docs/MVP_ACCEPTANCE.md and docs/SUBMISSION_DRAFT.md before review or submission.

Current verified corpus sizes (annual/transcript pages): INFY 383/48, DABUR 623/20, HCLTECH 485/26, VOLTAS 278/21. Hosted research answers passed for DABUR/HCLTECH/VOLTAS, but remain limited to retrieved excerpts; INFY broad research encountered provider 503. Final UI fixes are in 37dac53; see acceptance record for live deployment status.

Handoff: user confirmed final UI-fix deployment; live readiness, prediction guard, served contrast rules and cached-answer evidence endpoints verified. Final browser interaction verification unavailable. Research usefulness remains partial despite matching quotations; detailed review and exact manual checks in docs/MVP_ACCEPTANCE.md. No further scope additions or submission email.
