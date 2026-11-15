# Plan and progress

## Current milestone: first evidence workflow and hosted feasibility

Latest status (supersedes pending entries below): NSE documents have passed hosted download, object round trip and restart persistence. See docs/HOSTED_CHECKS.md and data/checks/render-*-exchange.json. Full application deployment, cold-start testing and forced in-flight interruption remain pending.
Approved scope is in PRD.md. First read-only Next.js/FastAPI workflow is implemented; validation is in progress. No deadline schedule is assumed.

Completed:
- Read both challenge PDFs fully in initial planning; inspected local workspace and empty remote repository; connected origin without overwriting or publishing.
- Created project rules and approved product documentation.
- Local public-source probe: prices for INFY/DABUR/HCLTECH/CERA; readable annual reports/transcripts; NSE feeds; downloaded exchange attachments. See data/checks and docs/DATA_ACCESS.md.
- Checked official free-tier hosting/storage documentation; Neon is user-selected for PostgreSQL. Bounded hosted object-storage verification has now passed; see latest status.
- Prepared render.yaml, Dockerfile.probe, .env.example, a protected two-stage diagnostic and private-credential client. Docker is not installed in the inspected environment, so image build remains unverified.
- Built one labelled briefing review with manually verified Infosys figures and code-calculated FCF change. Browser checked at 390x844 and 320x740: no horizontal overflow; window filter and expandable evidence/routine sections work. Screenshot: preview/mobile-briefing.jpg.
- Four diagnostic HTTP boundary tests passed outside the sandbox; sandbox loopback restrictions initially caused failures. pypdf read all 22 pages of the chosen transcript. Python compile checks passed. These are not cloud integration tests.

Awaiting review/setup:
- Architecture, neutral direction and initial companies approved.
- Render account plus Neon project/branch/storage setup using docs/DEPLOYMENT.md. No secrets in chat.

## Next milestones
1. **Hosted feasibility + one briefing:** user creates Render/Neon resources and supplies credentials privately. Verify DB connection, host-origin downloads/parsing, object upload/read and restart persistence. Measure cold start/memory and simulate interrupted job recovery. Review phone briefing before further screens.
2. **Core evidence path:** one real event -> source passage; then one model-grounded research question -> save -> later evidence. Model API access first required for synthesis, not preceding plumbing.
3. **Coverage and alerts:** 15 companies, three prepared examples, separate unfamiliar ticker; configurable EOD alerts only after core path works.
4. **Submission preparation:** mobile browser tests; calculations, citations, duplicates, missing documents and restart checks; working link, repository, original history links/exports and honest covering note. No email sending.

## Blockers/open decisions
- Neon Singapore and Object Storage tab confirmed by user; private finn-sources bucket exists. Database and storage credentials configured privately and tested locally. Render diagnostic is deployed and NSE ingestion/restart checks have run.
- Approved backend: static Next.js export served by FastAPI; one Python application API.
- Runtime API provider and key unavailable; no working AI research claim.
- Exact cutoff and time available unknown; any scope reduction requires user choice.
- Free-tier unattended refresh mechanism unresolved; app must show actual freshness rather than imply continuous updates.

At each milestone: report working behaviour, checks actually run, incomplete work and user decisions. Update these files without replacing the actual development conversations.

## Follow-up verification
- Confirmed actual host download failure: www.infosys.com returns HTTP 403 for both prepared sources after diagnostic redeploy. Added small-exchange (October earnings transcript) and large-exchange (October results bundle, locally observed 195 pages/26.7 MB) using original NSE-feed URLs. Separate job IDs/reports preserve original failures. New host execution pending; no spoofing or proxy workaround.
- Hosted retry after user checked configuration: database now works (queued job created/read from Render); source download fails with HTTPError. Initial ProgrammingError no longer reproduced. Both outcomes retained. Source HTTP status instrumentation added; host deployment of this change pending. Do not continue attributing the failure to DATABASE_URL.
- Render diagnostic deployed by user at https://finn-source-probe-tkef.onrender.com. Initial hosted checks: health 200, unauthenticated verify 401, protected source step 503 ProgrammingError. Local Neon query confirms no row for this hosted job ID, so hosted DB/storage/extraction has NOT passed. Asked user to verify Render DATABASE_URL format privately. Results: data/checks/render-small.json. Restart/interruption/large-document tests remain pending.
- Static Next.js build passed; FastAPI briefing/event/passage path implemented with curated INFY evidence and limited coverage labels. Eight local tests pass after fixing unread rejected POST body handling.
- New application browser check unavailable in this chat. Prior design-preview screenshot/checks are separate; no new mobile visual verification claimed.
- Neon SELECT 1 and actual client TLS passed locally; HeadBucket passed. Credentials are in ignored .env. These are not hosted checks.
- Large-document probe extended with per-page checkpoints and Linux memory counters. Hosted upload/hash/restart/interruption/large-document checks all pending. Unattended refresh remains unresolved.
- Actual local HTTP smoke passed: static home 200, briefing contains two available disclosures, event calculation -8.1%, evidence page 4 includes both source figures, missing evidence returns 404. Browser remains unavailable for the new app.
- Commit 01b7362 saved after audit. Normal GitHub push rejected with 403: local Git credential authenticates as wonx2983, lacking permission to jim-jam-jim/ENAM_AI. Await user repository authentication/access fix; do not replace global credentials or force-push.
- Resolved: user confirmed repository access fixed; repeated audit passed, and normal push of main through e046663 succeeded. Remote tracking is configured. Next: Render Free diagnostic setup; all Render-origin checks still pending.
- Small local-to-Neon diagnostic passed: original PDF uploaded/retrieved with same SHA-256, 22 extracted pages/checkpoint survived fresh processes, completed retry retained 22 unique pages and unchanged updated_at. Evidence: data/checks/local-neon-job-small.json. This is not Render restart/forced interruption or large-document verification.

## Hosted milestone result
NSE transcript (48 pages) and results bundle (195 pages) passed Render download, object hash verification and extraction. Restart preserved the completed transcript and the 20-page results checkpoint; resume completed 195 unique pages. Completed retry was unchanged. Active large-document processing 124.958 s; observed peak RSS 170.03 MiB against 512 MiB. Next: integrate the verified source path into the first application workflow; test cold start and forced in-flight recovery. Annual-report source access, runtime provider and unattended refresh remain unresolved. See docs/HOSTED_CHECKS.md.

## Resumed implementation
The interrupted final local server start was retried through normal approval and succeeded. Neon-backed briefing/event/passage workflow and static production build are ready; 10 tests passed before interruption. Browser checked at 1280px and 390px after restart; cash passage loads from Neon. Full MVP work continues without milestone review gates. Gemini setup pending.

## Full MVP implementation in progress
15-company prices/filings fetched locally and stored in Neon (all 15 returned histories and feeds). New bounded document discovery/extraction, manual refresh, anonymous per-browser saved questions/settings, deterministic EOD alerts, and Gemini grounded research routes implemented; hosted verification and research acceptance still pending. Prepared discovery INFY/DABUR/HCLTECH plus separate VOLTAS all found primary annual-report/transcript links. No annual-report hosted success claimed yet.
