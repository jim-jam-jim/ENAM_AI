# Plan and progress

## Current milestone: first evidence workflow and hosted feasibility
Approved scope is in PRD.md. First read-only Next.js/FastAPI workflow is implemented; validation is in progress. No deadline schedule is assumed.

Completed:
- Read both challenge PDFs fully in initial planning; inspected local workspace and empty remote repository; connected origin without overwriting or publishing.
- Created project rules and approved product documentation.
- Local public-source probe: prices for INFY/DABUR/HCLTECH/CERA; readable annual reports/transcripts; NSE feeds; downloaded exchange attachments. See data/checks and docs/DATA_ACCESS.md.
- Checked official free-tier hosting/storage documentation; Neon is user-selected for PostgreSQL. Host and object-storage verification remain pending.
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
- Neon Singapore and Object Storage tab confirmed by user; private finn-sources bucket exists. DATABASE_URL setup pending. Render account/hosted probe PENDING.
- Approved backend: static Next.js export served by FastAPI; one Python application API.
- Runtime API provider and key unavailable; no working AI research claim.
- Exact cutoff and time available unknown; any scope reduction requires user choice.
- Free-tier unattended refresh mechanism unresolved; app must show actual freshness rather than imply continuous updates.

At each milestone: report working behaviour, checks actually run, incomplete work and user decisions. Update these files without replacing the actual development conversations.

## Follow-up verification
- Static Next.js build passed; FastAPI briefing/event/passage path implemented with curated INFY evidence and limited coverage labels. Eight local tests pass after fixing unread rejected POST body handling.
- New application browser check unavailable in this chat. Prior design-preview screenshot/checks are separate; no new mobile visual verification claimed.
- Neon SELECT 1 and actual client TLS passed locally; HeadBucket passed. Credentials are in ignored .env. These are not hosted checks.
- Large-document probe extended with per-page checkpoints and Linux memory counters. Hosted upload/hash/restart/interruption/large-document checks all pending. Unattended refresh remains unresolved.
