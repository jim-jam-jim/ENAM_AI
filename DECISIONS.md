# Decisions

## Accepted by user — 15 November 2026
- Three views: briefing, event evidence, company research. Briefing is the foundation; one saved question per company adds context without suppressing material unrelated events.
- Build one verified end-to-end workflow first. Target 15 portfolio companies, three prepared research examples and a separate unfamiliar ticker test. Configurable in-app alerts follow the core evidence workflow.
- TypeScript/Next.js interface and Python data/document work are acceptable. Static Next.js export served by FastAPI is now approved, with one Python application API and durable job checkpoints. Avoid overlapping application APIs.
- Professional mobile design: neutral palette, muted accent, readable typography, useful density; no emojis, mascots, neon/glow/rainbow effects or decorative AI branding. Review an early briefing screen.
- Repository: https://github.com/jim-jam-jim/ENAM_AI. Inspect before connecting; preserve existing work. Initial inspection showed remote size 0 and no refs; local workspace contained two PDF preview PNGs only. Initialised local main and configured origin; no push yet.
- Free-tier deployment target. Neon PostgreSQL replaces the earlier Supabase proposal. No PDF collection in database rows. Render is an acceptable initial hosting candidate, not a verified deployment. User will create Render account when needed.
- Coding-agent access does not establish runtime model access. Provider still pending. Source checks, parsing, calculations and interface work may continue without it.
- Create and maintain PRD, PLAN, DECISIONS, README, BUILD_HISTORY and AGENTS. Preserve original conversations. Exact submission cutoff/time budget remains unconfirmed.

## Approved implementation direction — follow-up approval, 15 November 2026
- Approved: start with INFY: downloaded sources and a visually verified cash-flow observation support a useful evidence-first example. DABUR and HCLTECH are the other prepared candidates. CERA has passed a discovery spike, not the final unfamiliar-ticker research test.
- Approved: a static Next.js frontend served by a single Python/FastAPI process on Render, with all application API/job ownership in Python. This removes a permanent Node process from the 512 MB runtime while retaining React/TypeScript. Trade-off: no Next server actions/SSR; new tickers use client-side routing/query parameters.

## Remaining proposals and account checks
- Neon Object Storage is suitable in principle for PDFs; current docs show general availability and Free allowance, but only specified regions. Account/project eligibility and upload/retrieval must still be tested.
- Use PostgreSQL job leases and checkpoints, one document job at a time, content-addressed PDF keys, and idempotent stage writes. Free service sleeps interrupt progress; resume on next active request. Scheduler decision remains open; do not imply continuous monitoring.
- No paid model/provider or hosting upgrade authorised. Minimum model need is grounded text synthesis with structured claim/evidence IDs; no embeddings, vision, web browsing or provider-hosted agents initially.

- User approved neutral visual direction as a starting point, not a final product; preview retains design-review labels. Actual product uses concise freshness/coverage/availability labels.
- User authorised a normal push after tracked/staged secret and artifact inspection; no force push. Account setup proceeds step by step. Hosted small and large document checks must actually run before claiming deployment readiness.

## Account observations reported by user
- Neon project region Singapore; Object Storage tab present; private finn-sources bucket created. These are user-confirmed account facts, not verified credential access or successful API operations. Database connection setup is next.

## Verified hosting observations — 15 November 2026
Render plus Neon passed bounded NSE PDF ingestion, storage and restart/resume checks (48 and 195 pages). Retain the approved architecture without adding infrastructure. This is evidence of diagnostic feasibility, not a new scope approval or proof of full production readiness. The NSE Q2 FY2027 documents are explicitly different from the blocked original Q4 transcript/annual report. See docs/HOSTED_CHECKS.md.

## Latest user approvals
Complete the full agreed MVP and deploy without waiting for each milestone review. Gemini runtime free tier only; use gemini-2.5-flash-lite after account verification, no paid fallback. Refresh will be explicit manual/refresh-on-open bounded work on the existing service; no new scheduler or continuous-monitoring claim.

## Runtime and refresh implementation
User configured Gemini privately and confirmed free billing. Model metadata access returned 200 for gemini-2.5-flash-lite. Cap at 20 reserved calls/Pacific day and 2/minute, including failures; no automatic paid/model fallback. Manual bounded refresh while page stays open, one source at a time, cached for one hour. No scheduler added. Alert baseline implemented as 20 prior completed sessions, latest excluded; corporate-action windows suspend alerts. Anonymous browser UUID isolates settings without login; clearing browser storage loses workspace access, but not server records.

Scope frozen: finish acceptance and blocking fixes only. Do not add price infrastructure to work around hosted Yahoo 429; retain source failure and stale-cache labels. Session advisory locks replaced with expiring row leases for the Neon transaction pooler. Reuse one database connection within a page batch while retaining per-page durable writes.

Runtime generation revealed Gemini 2.5 Flash-Lite is unavailable to new users (HTTP 404), despite model metadata success. Google directs new users to gemini-3.5-flash-lite; official pricing checked and standard text input/output are free tier. Explicitly changed selected model to 3.5 Flash-Lite under user-approved free-tier Gemini choice, retaining the same caps and no paid fallback.

Final review posture: hand over the deployed prototype with explicit partial research acceptance, stale-price/provider limits, and required manual visual checks. Do not equate exact-quote validation with a complete or useful answer. Scope remains frozen.
