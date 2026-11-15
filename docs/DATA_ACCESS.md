# Local source-access findings

Checked 15 November 2026 from Windows, outside the execution sandbox after approval. These are real downloads, not web-search snippets. Hosted verification is PENDING.

| Candidate | EOD | NSE announcements (1 Oct–15 Nov) | Annual report | Earnings transcript |
| --- | --- | --- | --- | --- |
| INFY | 63 daily rows, INR | 20 rows; results attachment fetched | FY26: 383 PDF pages, 381 with >80 text characters | Q4 FY26: 22/22 readable pages |
| DABUR | 63 daily rows, INR | 34 rows; exchange presentation fetched | FY26: 623 pages, 617 readable | Latest discovered transcript: 20/20 readable |
| HCLTECH | 63 daily rows, INR | 25 rows | FY26: 462 pages, 458 readable | Latest discovered transcript: 26/26 readable |
| CERA | 63 daily rows, INR | 10 rows | FY26: 207 pages, 205 readable | Latest discovered transcript: 15/15 readable |

Price responses cover 13 August–13 November 2026; this is cached EOD data, not live quotes. The text-length threshold is an extraction heuristic, not a claim that all tables/figures are understood. Source IDs, original/final URLs, timestamps, response status, SHA-256 hashes, sizes and local paths are recorded in data/checks/20261115T091353Z.json and 20261115T091548Z.json. Full originals/extractions are ignored local artifacts.

## What passed
- Yahoo chart API returned real closes/volume without runtime credentials for all four symbols.
- NSE announcement JSON downloaded; linked Infosys October results PDF downloaded from the URL actually supplied by the feed.
- Screener used only as a link index, not research evidence: Dabur/CERA annual reports and transcripts were discovered then downloaded from BSE. HCLTech links came from its IR pages.
- Read first pages to check company identity and document type/date. Visually inspected Infosys results PDF pages 3–4 (printed fact-sheet pages 1–2) before choosing demonstration figures.
- INFY consolidated company-defined FCF: INR 8,898 crore for quarter ended 30 Sep 2026 versus INR 9,677 crore for 30 Sep 2025. Code calculates `(8898 / 9677 - 1) * 100 = -8.1%` rounded to one decimal. FCF definition is based on IFRS consolidated cash flow; do not silently treat it as Ind AS or mix with another basis.

## Failures, caveats and fixes
- Initial sandbox run: every source failed DNS. Preserved in data/checks/20261115T091339Z.json. Retried outside sandbox with approval; source access succeeded. This was an environment failure, not evidence the sources were unavailable.
- Extracted Infosys PDF contains a stale Fiscal 2023 text header alongside Fiscal 2027. Rendered page confirms Fiscal 2027. Source period validation must use surrounding table dates and visual inspection for prepared examples.
- Exchange bundles can be large: April Infosys outcome 43.1 MB/379 pages; October outcome 26.7 MB/195 pages; Dabur AR 28.3 MB/623 pages. A download succeeding locally does not prove parsing fits a 512 MB host. Process sequentially, stream downloads, checkpoint page batches, and measure host memory before acceptance.
- No tested source returned an HTTP failure in the successful runs; that does not establish future reliability, pagination completeness, or rights for unrestricted redistribution.
- No OCR/image-table processing verified. No final metric extraction engine, source-date normaliser, deduplication or generic research workflow exists yet.
- CERA passed source discovery beyond the proposed three examples. It does NOT satisfy the final unfamiliar-ticker research acceptance test. Use a fresh non-demo ticker for that later test.

## Recommendation
Start INFY because evidence, dates and comparable cash figures have been inspected, not because of familiarity. DABUR adds a consumer business and different document formatting; HCLTECH adds another available, readable corpus. These three are proposed, not silently fixed portfolio choices. Select the remaining portfolio across sectors/sizes after access checks. Do not imply the four-company spike covers all 15.
