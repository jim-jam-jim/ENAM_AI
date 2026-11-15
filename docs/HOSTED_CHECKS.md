# Hosted diagnostic results — 15 November 2026

Actual host: https://finn-source-probe-tkef.onrender.com. These are protected diagnostic results, not full application acceptance. Source files were downloaded by Render, not uploaded manually.

| Check | Transcript bundle | Results bundle |
| --- | --- | --- |
| NSE download and Neon object hash round trip | Passed | Passed |
| PDF size | 3,742,339 bytes | 26,721,438 bytes |
| Extracted checkpoints | 48/48 unique pages | 195/195 unique pages |
| Active server processing, download/upload plus extraction stages | 7.650 s | 124.958 s |
| Extraction stages including object reads and DB writes | 5.880 s | 122.430 s |
| Sum of client step durations | 8.687 s | 127.656 s |
| Elapsed from first download to completion, including operator pauses/restart | 24.133 s | 334.385 s |
| Observed process peak RSS | 131.85 MiB | 170.03 MiB |
| Observed cgroup peak | 119.10 MiB | 164.05 MiB |
| Longest processing request | 2.552 s | 14.046 s |

Timing excludes verification calls and completed-job retries. Peak counters are process/container lifetime high-water marks, not isolated per-document allocations; the large run spans two processes. Observed cgroup limit was 536,870,912 bytes (512 MiB). These results establish that these documents fit this diagnostic, not all PDFs or concurrent model workloads.

## Restart and retry evidence
- Before restart boot: `94d5cefc-79ef-4ebb-83d0-9b40d4b08a53`; after user restart: `6c662e1b-0abc-4919-a569-d1174044b16b`.
- Transcript retained all 48 passages, matching object hash and unchanged `updated_at` (14:42:48.152986 UTC).
- Results retained exactly 20 unique pages and the same checkpoint timestamp after restart. The next batch advanced to 40; remaining batches finished at 195.
- Final verify: 195 unique pages, passages present, matching hash. Completed retry preserved `updated_at` at 14:48:02.197568 UTC, with no duplicated pages.
- This proves unfinished-job recovery across a restart **between requests**. A forced kill during a page write, sleep/wake cold-start latency and production job leases/concurrency remain untested.

## Source identity and coverage
- Transcript: Infosys Limited, combined media conference and earnings-call transcripts, call 23 October 2026, filing 28 October. PDF page 1 identifies the company/date and Q2 results URL; page 25 explicitly says Q2 FY27 Earnings Conference Call. Page 2 has a stale 2025 copyright footer, which is not the reporting period.
- Results: Infosys Limited board outcome dated 23 October 2026, quarter and half year ended 30 September 2026 (Q2 FY2027), confirmed on PDF pages 1–2. Contains consolidated/standalone Ind AS and IFRS material; each metric needs its own basis. Earlier rendered checks resolved a stale hidden Fiscal 2023 factsheet header against Fiscal 2027.
- These are not equivalent replacements for the original Q4 FY2026 transcript and FY2026 annual report. Both original Infosys-hosted downloads returned HTTP 403 from Render; retain that limitation. Annual-report ingestion is still unverified on the host.
- Full extraction does not validate every table, financial number, OCR requirement or citation. Generic ticker discovery, hosted prices/feeds, automatic refresh, quota headroom and full app deployment remain outstanding.

Raw sanitized responses: `data/checks/render-small-exchange.json` and `render-large-exchange.json`. Identity, URLs, hashes and page references: `data/checks/hosted-source-identity.json`. Original failures remain in `render-small.json` and `render-large.json`.
