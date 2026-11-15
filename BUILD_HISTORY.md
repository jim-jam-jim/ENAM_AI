# Actual build history index

This file supplements the original conversations; it is not their replacement. No share links or exports have been supplied yet. Do not invent them. Preserve this Codex chat and the user's earlier planning conversation for submission; earlier planning details outside this chat have not been inspected.

## 15 November 2026 — this development conversation
- Initial request: read two challenge PDFs, inspect workspace, distinguish examples from requirements, draft PRD before implementation.
- Read all six PDF pages; found two existing preview images and no application. Proposed evidence-first briefing and saved-question MVP. No project files changed in that initial stage.
- PDF extraction initially failed on Windows cp1252 Unicode output; rerunning Python with `-X utf8` succeeded. A temporary render path was inaccessible across tools; rendering to the writable visualization directory allowed inspection.
- User approved MVP, three views, one question/company, 15-company target, three examples plus separate unfamiliar ticker test, visual constraints and project documentation. Supplied empty GitHub repository.
- GitHub connector confirmed public repository size 0. Sandboxed Git DNS failed; approved external `git ls-remote` returned no refs. Initialised local main and origin without overwriting previews or pushing.
- Initial source probe failed entirely on sandbox DNS. Approved outside-sandbox run downloaded actual sources successfully. Both failure and success logs retained in data/checks.
- Discovered further annual-report/transcript URLs from downloaded indices and results attachments from the NSE feed, then fetched them. This is a discovery spike, not completed generic research.
- Infosys PDF text extraction surfaced an obsolete Fiscal 2023 header; rendered pages visibly show Fiscal 2027. Verified the displayed period and cash figures before using an example. Text readability alone is insufficient financial validation.
- User selected Neon PostgreSQL, asked for Neon object-storage checks, accepted Render as a candidate and explicitly left hosted probe pending until actual execution. No credentials pasted; no runtime model selected.
- Prepared a small standard-library hosted diagnostic, environment template, Render blueprint and Dockerfile; no application framework was committed. Hosted run and Docker image build are unverified (Docker command unavailable locally).
- Created a manually populated real-evidence briefing preview. Sandboxed preview was inaccessible to the browser; approved outside-sandbox server was reachable. Verified 390px and 320px widths, time-window selection and disclosure expansion; saved preview/mobile-briefing.jpg. No AI research was claimed.
- Four local HTTP boundary tests initially failed because sandbox denied loopback sockets. Approved outside-sandbox rerun passed all four. pypdf successfully parsed 22/22 transcript pages. This does not establish PostgreSQL/object-store or hosted recovery integration.
- Saved initial local milestone commit aefdbd7 after sandbox denied Git index writes and approved external execution succeeded. Staged whitespace check found a trailing space in preview CSS; removed it in a follow-up. No GitHub push or deployment performed.

## Export/link status
- Safe diagnostic update confirmed HTTP 403 from www.infosys.com for both documents on Render. Added separate NSE-hosted transcript/results sources from the already-downloaded announcement feed; original failed jobs/reports retained. This tests legitimate alternative primary sources, not a bypass of the company website restriction. No fallback success claimed before execution.
- User confirmed Render DATABASE_URL format looked correct. Retry reached Neon and returned queued job via authenticated verify; download failed HTTPError instead of ProgrammingError. Added safe source status/hostname diagnostics (no headers, credentials or response bodies). Database connectivity is now verified from Render; storage/extraction remain unverified.
- User supplied deployed Render URL. Real host health returned 200 and unauthorized request 401; first protected source step failed 503 ProgrammingError. No hosted job row exists in the locally accessible Neon database. Investigating Render connection-string formatting without exposing secrets; no integration success inferred from health. Sanitized response record: data/checks/render-small.json.
- User confirmed GitHub access fixed. Rechecked clean working tree and repository audit (46 candidate files, no detected secret patterns or forbidden artifacts), then normal push succeeded: main now tracks origin/main. No force push. Source: https://github.com/jim-jam-jim/ENAM_AI/tree/e046663 . Render setup is next; no hosted verification claimed.
- Small local-to-Neon probe passed through stored -> extracting (20 pages) -> complete (22 pages) across separate Python processes. Retrieved hash matched. Completed retry retained 22 unique pages and unchanged updated_at. Results retained in data/checks/local-neon-job-small.json; no forced-kill/Render/large-document claim.
- Commit 01b7362 saved; normal push rejected by GitHub (403, authenticated as wonx2983 without repo write permission). Asked user to authenticate correct owner or grant repository access. No force push or global credential changes.
- Running local static/API HTTP smoke passed (home, briefing, calculated comparison, passage and missing-source response). Browser tool remains unavailable, so no working-app screenshot claimed.
- Follow-up user approvals: static Next.js + FastAPI, durable checkpoints, neutral direction, INFY first and DABUR/HCLTECH examples, audited non-force push.
- Implemented local read-only evidence workflow and static export. npm sandbox DNS failed; approved installation succeeded. Eight tests pass. A later Windows connection reset on unauthorized POST was fixed by consuming its bounded body before rejecting it.
- Secret scanner initially matched its own broad private-key regex; narrowed to actual key headers. Candidate files contain no detected secrets or forbidden PDFs/environment files. Metadata/test records retained.
- User configured Neon Singapore/private bucket and credentials privately. Local SELECT 1, client TLS and HeadBucket passed. Initial pg_stat_ssl check described the pooler upstream hop; actual client TLS verified instead. No hosted tests yet.
- Browser tool unavailable for new app verification in this chat; previous design preview is not a screenshot of the working app. Large-document diagnostic checkpoint code prepared, host measurements pending.
- Documentation patch attempts with stale context failed without applying; a shell quoting error in a proposed documentation update was corrected by using direct patches.

- Current chat: original conversation exists in Codex; export/share location not yet available.
- Earlier planning chat: user says it exists; link/export not supplied.
- Repository: https://github.com/jim-jam-jim/ENAM_AI (local changes not yet pushed).

## Hosted NSE run and restart — 15 November 2026
- Both NSE PDFs downloaded on Render and passed Neon object hash checks. User manually restarted the service: completed 48-page transcript persisted; results bundle resumed from 20 to 195 unique pages. Completed retry retained timestamp. Large document active steps totalled 124.958 seconds with observed 170.03 MiB peak RSS; source company/type/period verified from persisted passages. Raw responses and identity checks retained.
- Read-only identity inspection initially hit python-dotenv stdin discovery AssertionError; explicit .env path fixed it without logging credentials. Documentation update hit Windows default encoding failure; UTF-8 read/write fixed it.
- No forced in-flight kill, cold-start or annual-report success claimed. Original Infosys HTTP 403 remains recorded. Original chat remains the development-history source, with export/link still pending.

## Resume after usage limit
Implemented Neon read-model publication, static frontend root and protected diagnostic adapters. Production build and 10 tests passed. Local server restart was rejected when automatic approval review reached its usage limit; no bypass attempted. User asked to retry after reset; normal approval succeeded. Final local browser check passed at 1280px and 390px, with historical navigation and hosted-extracted cash passage. Full MVP continuation authorised; Gemini free-tier setup requested.
