# Ready-to-copy covering email

Replace the three bracketed placeholders before sending. The two conversation entries may be accessible share/export links or the filenames of actual attached exports. Do not send this file with unresolved placeholders.

To: assessment@enam.com
Subject: IIT Delhi – AI Engineer - 2027

Hello,

I built FINN, a mobile-first investment briefing prototype for a mock portfolio of 15 companies. It supports source-backed event investigation, document-grounded research, one saved question per company and configurable EOD alerts.

Prototype: https://finn-source-probe-tkef.onrender.com
Repository: https://github.com/jim-jam-jim/ENAM_AI
Actual AI conversations:
- Initial planning: [PLANNING CONVERSATION LINK OR ATTACHMENT FILENAME]
- Development, debugging and deployment: [DEVELOPMENT CONVERSATION LINK OR ATTACHMENT FILENAME]

I used static Next.js served by one FastAPI application, Neon PostgreSQL for evidence and job state, and object storage for PDFs. Durable checkpoints resume interrupted extraction. Gemini uses the configured free tier with application caps and no paid fallback. This keeps deployment simple, with manual refresh rather than an always-running service.

For a short demo, select Historical example → Infosys and inspect the cash-flow calculation, passage and original PDF. This stored, manually curated example makes no model call; recent windows preserve actual dates. Then inspect portfolio coverage and alerts. Prior hosted research for Dabur, HCLTech and VOLTAS is recorded in data/checks/mvp-hosted-research.json. These records are not a shared in-app cache: new browser workspaces make new research requests.

Hosted announcement refresh succeeded for all 15 companies, and eight annual reports/transcripts completed hosted download and extraction. Persistence, checkpoint recovery and alert calculations were tested. Hosted Yahoo retrieval returned HTTP 429; real cached prices are retained and labelled stale, and the restriction's cause and duration are unknown. Infosys Gemini attempts returned HTTP 503 availability failures, while other hosted research succeeded. Some supported quotations did not adequately answer the question, so research quality remains partial. Final deployed browser checks remain a verification gap; HTTP/API and earlier local layout checks are recorded in docs/MVP_ACCEPTANCE.md.

Scheduled monitoring, trading, voice and elaborate authentication are deliberately deferred. Next I would improve retrieval, financial context and prompts, evaluate whether a stronger model helps without assuming it will, and address reliable refresh and unattended monitoring. The prototype is not fully verified.

Regards,
[YOUR NAME]
