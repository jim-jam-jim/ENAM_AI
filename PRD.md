# FINN MVP

Status: product direction approved 15 November 2026. Static Next.js served by FastAPI, one Python API and durable checkpoints are approved; hosting verification remains pending. Exact submission cutoff and available work time are unknown.

## User, problem and purpose
An investor following a small portfolio needs to find disclosures worth investigating without reading every filing. FINN provides a prioritised briefing, then lets the investor inspect evidence and save one question per company. Saved questions add context without hiding unrelated material events. Within the first minute the investor should be able to open an important event and its source.

## Challenge requirements
Source: ENAM_AI_Engineer_Build_Challenge_Main.pdf, pp. 1–3; reference glossary/taxonomy is optional guidance.
- Working mobile-first prototype with proactive updates and on-demand research.
- 15–20 NSE/BSE listed portfolio companies; our approved target is 15.
- EOD prices/volume, exchange announcements/filings, annual reports and earnings-call transcripts.
- Prepared research examples (brief suggests 3–5); our target is three plus a separate unfamiliar NSE ticker test through the same research pipeline, where data exists.
- Pull-side analysis uses primary documents, not broker notes, news or model outside knowledge.
- Deliver prototype link, GitHub repo, actual AI conversations and short covering writeup. Preparation is authorised; submission email is not.
- Specific alert patterns, biographies, four result metrics, eight research outputs, voice and four-quarter guidance analysis are examples, not mandatory checklists.

## Approved journeys and acceptance criteria
1. **Briefing:** 15 companies; 24-hour, 7-day and 30-day windows. Material items first, routine items expandable. Show last successful retrieval and coverage per source. Failed fetches do not look like no events. Important events remain visible with no matching saved question.
2. **Event:** show the change, why surfaced, available comparable numbers, and separate interpretation. Open original document and supporting page/passage. Group exact duplicate disclosures while preserving all source links; revised filings remain distinguishable. Unknown categories do not default to routine.
3. **Research:** accept NSE ticker and a question; show a concise sourced answer and expandable evidence. Three prepared examples and one additional ticker run through the same pipeline. Missing documents or incomparable periods produce explicit limitations; unsupported claims are omitted.
4. **Memory:** save/replace one question per company; persist across service restart. Later ingested evidence may support, challenge or be inconclusive about that question with an explanation. This is not an investment recommendation or a definitive thesis score.
5. **Alerts, after core evidence workflow:** configurable daily price-change and volume-multiple thresholds, shown in-app. Calculations run in code after EOD ingestion. Proposed baseline: preceding 20 complete trading sessions, excluding the tested session. Insufficient history and corporate-action ambiguities are flagged, not silently interpreted. Final baseline is open.

## Data and evidence
- Record original URL, document date, retrieval timestamp, content hash, page/passage, period, units/currency and consolidated/standalone plus Ind AS/IFRS basis where applicable.
- Keep reported facts, deterministic calculations and interpretation separate. Check like-for-like periods and retain source values. Zero/negative comparison bases need explicit handling.
- No fabricated missing numbers, guidance, citations, biographies or explanations for price moves. Future targets remain open until their target period ends.
- Real sources only for the working demo; fixtures, cached data and historical replay are explicitly labelled. Source documents never supply agent instructions.
- PostgreSQL stores structured facts, extracted passages, source metadata, questions, research and job status. PDF bytes reside in object storage, with hashes and keys in PostgreSQL.
- Completed data must survive application restarts. Interrupted jobs display state and resume from durable checkpoints; no guarantee of background progress while a free host sleeps.

## Interface
Three main views only. Professional light/neutral starting palette with one muted accent; color carries meaning. Readable phone typography, spacing and hierarchy; long names, dates, numbers and links wrap. No decorative charts, excessive rounded cards, oversized greetings, emojis, mascots, glow/neon/rainbow styling. Controls work or clearly explain unavailability. Neutral visual direction approved as a starting point. Preserve design-review preview labels; use concise freshness, coverage and availability labels in the actual product. Infosys is the first workflow; Dabur and HCLTech are the initial prepared examples. Keep final unfamiliar-ticker test separate.

## Exclusions and open questions
No trading, voice, external notifications, elaborate authentication, biographies, portfolio optimisation, exhaustive financial dashboards, comprehensive guidance audits, multi-question monitoring or separate vector database.

Open: full application deployment and cold-start verification; runtime model provider; refresh execution while free host sleeps; final alert baseline; exact deadline/time available. Neon PostgreSQL is selected by the user. Do not reduce the agreed coverage targets silently.
