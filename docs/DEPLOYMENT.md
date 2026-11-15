# Deployment feasibility — bounded hosted diagnostic verified

Neon PostgreSQL is user-selected. Render is the accepted initial candidate. The diagnostic is deployed on Render. NSE downloads, object round trips and checkpoint persistence across restart passed; see HOSTED_CHECKS.md for measurements. The full application is not deployed. No paid dependency authorised.

## Backend comparison — static Next.js + FastAPI approved
| Option | Benefit | Cost/risk |
| --- | --- | --- |
| Next.js server + bounded Python subprocesses in one container | One application API in Next.js; familiar server rendering | Node and Python share 512 MB; Python job protocol/cancellation and durable orchestration must be maintained across languages |
| Next.js static export + Python/FastAPI, served together | One Python application API owns ingestion, research and jobs; one runtime process and domain; frontend stays TypeScript/React | No SSR/server actions; unknown tickers need client-side query-param routes rather than prebuilt dynamic pages |

Recommend the second option based on observed 195–623-page documents and Python-owned processing. Build Next.js assets in a Node build stage, then serve them from Python alongside /api. Do not add Next API routes. FastAPI does not itself make background work durable.

The diagnostic uses Python's standard HTTP server, deliberately independent of the unresolved application framework. It is not production application code.

## Job behaviour proposed for the application
Accept unfamiliar ticker -> resolve identifier -> discover allowed primary sources -> cache original by SHA-256 -> extract page batches -> retrieve passages -> synthesise/citation-check -> persist result. Store each stage and its checkpoint in PostgreSQL, not RAM.

POST returns a job ID promptly. A bounded advance operation claims a database lease and executes a stage; UI polls status. Keep one document worker active to start. Retries use the same job ID and content keys. Network deadlines, job attempt limits and lease expiry prevent indefinite spinners. Restart recovers expired leases and resumes the last committed stage; completed results remain readable. A model call interrupted before commit may need replay, so cache request hashes and account for possible duplicate provider charges.

On a sleeping free service, progress can pause. Say “Paused; resumes when service wakes” rather than claiming background completion. Status checks must not falsely mark work complete. A platform scheduler or another approved wake mechanism is needed for unattended daily refresh; unresolved, not implemented. No laptop scripts may be required by the finished deployed product.

## Current free-tier constraints (official docs checked 15 Nov 2026)
- Render Free: 512 MB RAM, 0.1 CPU; sleeps after 15 idle minutes, wake approximately one minute; 750 instance hours/workspace/month. Local disk is ephemeral. No free background-worker service or one-off jobs. Render may restart services or suspend unusually high outbound traffic. No-card quota exhaustion can suspend service/builds; avoid paid overages. HTTP platform limit is up to 100 minutes, but our stage deadlines must be much shorter. Account bandwidth/build quotas must also be checked in dashboard before deployment.
- Neon Free: 1 GB PostgreSQL/project, 100 CU-hours/project/month, 5 GB object storage/project and 5 GB public transfer/project/month shared across products. Database scales to zero after five idle minutes. Keep connections brief and retry transient wake failures with a bounded delay.
- Neon Object Storage: generally available, including Free. Supported regions currently Ohio, N. Virginia, Frankfurt and Singapore. Choose Singapore for both candidates if available. Existing Neon projects in unsupported regions need a supported-region project; do not assume the user's current project qualifies.
- Storage supports Put/Get/Head and signed URLs; S3 lifecycle/versioning rules are not fully enforced. Use immutable content-hash keys and application-controlled retention. No full PDFs in database rows. Keep source copies private.
- Initial application budgets proposed: one active document job; 50 MB source limit with explicit oversized-document state; cached originals and extracted passages; avoid fetching all portfolio annual reports on every refresh. Measured diagnostic memory and duration are in HOSTED_CHECKS.md; these are not universal document bounds.

Sources: [Render free](https://render.com/docs/free), [compute](https://render.com/docs/compute-plans), [request duration](https://render.com/docs/render-vs-vercel-comparison), [Neon pricing](https://neon.com/pricing), [storage limits](https://neon.com/docs/storage/overview), [S3 compatibility](https://neon.com/docs/storage/s3-compatibility).

## Exact account setup
1. In Neon Free, select/create a FINN project in a supported object-storage region (Singapore preferred). Keep one branch for this probe. Copy its **pooled** PostgreSQL connection string with the SSL parameters supplied by Neon into DATABASE_URL. Never paste it into chat.
2. On the same branch, open Object storage -> New bucket -> `finn-sources` -> **private**. Confirm Free allowance in the account. If Object storage is absent, stop and report the selected region/account limitation; no automatic paid fallback.
3. Create branch-scoped storage read/write credentials. Map `token_id` to AWS_ACCESS_KEY_ID and `s3_secret_access_key` to AWS_SECRET_ACCESS_KEY. Copy the branch endpoint and signing region into AWS_ENDPOINT_URL_S3 and AWS_REGION. Use the generated values, not a guessed endpoint/region. No AWS account is required. See [authentication](https://neon.com/docs/storage/authentication) and [buckets](https://neon.com/docs/storage/buckets).
4. Set PROBE_TOKEN to a locally generated random value of at least 32 characters. Copy .env.example to .env locally or set keys in the Render dashboard. Keep `.env` ignored. Model credentials are not needed.
5. Once source is pushed to the user repo and Render account exists, connect `jim-jam-jim/ENAM_AI` and create the `render.yaml` Blueprint, or a Free Docker web service using Dockerfile.probe. Confirm **Free**, Singapore, health check `/healthz`, no disk, no Render database, no paid worker. Auto deploy is disabled in the proposed blueprint. Fill the seven secret/config keys prompted by the blueprint.

Required keys: DATABASE_URL, AWS_ENDPOINT_URL_S3, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DOCUMENT_BUCKET, PROBE_TOKEN. PORT defaults to 10000 (Render supplies it). Optional local client key PROBE_BASE_URL is the eventual HTTPS URL. No NEXT_PUBLIC_* secrets and no Neon admin API token in runtime.

## Hosted probe acceptance procedure
Diagnostic resources use `finn_probe_jobs` table and `probe/` object prefix. The credential needs CREATE TABLE in the probe database. The probe fetches a fixed small real Infosys transcript, not user-supplied URLs. No model output is generated.

1. `/healthz` must return 200. This proves only process health, NOT database/storage readiness. Protected endpoints reject missing token.
2. Choose a UUID; POST `/step` with that job_id and Bearer PROBE_TOKEN. It connects to Neon, creates/reads a row, downloads from the host and stores PDF in object storage. Response phase must be `stored`.
3. Restart Render before the next step. GET `/verify?job_id=...` must show a different boot_id, `stored`, and `object_hash_matches: true`.
4. POST `/step` again with the same ID. Read the original from object storage, parse pages, persist extracted passages and `complete`. Repeat calls must not duplicate the row/object.
5. Restart again and verify `complete`, page_count > 0, passages_present and matching PDF hash. This proves diagnostic document/metadata durability, not yet full saved-question/research durability.
6. Let service and database sleep normally. Measure first request and show a waking state in the later UI. Deliberately time out the client mid-stage, then query the same ID; retry the last checkpoint rather than create a new job. The diagnostic is serial and checkpointed; application leases/cancellation remain to implement.
7. Repeat representative prices/feed/large-PDF checks from Render in the next extension; the small transcript alone does not establish all-source or memory coverage. Record actual memory, duration, cold start and quota usage before accepting deployment.

This is the original acceptance procedure; completed checks and remaining gaps are recorded in HOSTED_CHECKS.md. No model or account setup is inferred from coding-agent access. The initial diagnostic has no scheduler, multi-user authentication or full research pipeline.

Local verification completed: Python compilation; four HTTP boundary tests (health accuracy, rejected missing token, missing config names without secret values, malformed UUID before DB access); pypdf extraction of all 22 transcript pages. Docker executable was unavailable, so no image build is claimed. Local tests initially failed under sandbox socket restrictions and passed after approved rerun outside the sandbox.

Client commands after configuring PROBE_BASE_URL privately:
```powershell
python scripts/probe_client.py health
python scripts/probe_client.py step --job-id YOUR-LOCALLY-GENERATED-UUID
# Restart the Render service, keeping the same UUID.
python scripts/probe_client.py verify --job-id YOUR-LOCALLY-GENERATED-UUID
python scripts/probe_client.py step --job-id YOUR-LOCALLY-GENERATED-UUID
# Restart again, then verify the completed checkpoint.
python scripts/probe_client.py verify --job-id YOUR-LOCALLY-GENERATED-UUID
```
The client is a diagnostic operator tool, not a dependency of the future deployed app. No credentials are accepted on its command line.

## Current account observations and extended probe
Render now verifies database access, but direct Infosys transcript and annual-report URLs return HTTP 403. New `small-exchange` and `large-exchange` presets use actual NSE-feed transcript/results URLs. Use separate new job IDs for these; the large exchange file is a 195-page/26.7 MB results bundle, not the annual report. Its success would not prove annual-report ingestion. Original company-site failure remains a source coverage limitation.
User confirmed Neon Singapore, Object Storage tab, private finn-sources bucket. Local SELECT 1/client TLS and HeadBucket passed. Hosted NSE checks have now run; see HOSTED_CHECKS.md.

Small local-to-Neon probe also passed: hash round trip, persisted 22 extracted pages and job state across fresh processes, completed retry with 22 unique pages and unchanged update timestamp. This does not establish forced interruption recovery or Render restart behaviour. Record: data/checks/local-neon-job-small.json.

Large probe: start a new UUID with `--source large`, then repeat step using the same ID until complete. It processes at most 20 pages per call and commits each page checkpoint. Response includes completed_pages and Linux peak RSS/cgroup peak/limit where available. This supersedes the earlier two-step extraction description; the small probe can require multiple extraction calls too. The first source URL is fixed for the lifetime of the job ID.

Downloads are capped at 50 MB/60 seconds. Whole-file pypdf memory and individual slow pages remain limitations requiring host measurements. No claim of large-document verification until that run. Completed jobs skip extraction; runtime app leases/concurrency are still future work, while diagnostic requests execute serially.
