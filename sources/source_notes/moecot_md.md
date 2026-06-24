# Source Note: moecot_agent_whitepaper.md

| Field | Value |
|---|---|
| Source ID | `moecot_md` |
| Source title | moecot_agent_whitepaper.md |
| Ingestion date | 2026-06-24 |
| Source version / URL | Markdown source/export; https://drive.google.com/file/d/1F0KW0-TR54xKGeetIPkDTV1Tn5_9w3i0 |
| Ingestion basis | Authenticated Google Drive connector fetch succeeded; local cache is an auth-gate placeholder and raw text is not published. |

## Thesis

The Markdown MoECOT file is a variant/source export of the MoECOT whitepaper. It should be used to normalize terminology, recover sections, and compare public-release wording against the editable document.

## Mechanisms

- Same core MoECOT mechanisms as the primary whitepaper: compact orchestrator, specialist lanes, control-plane ledgers, readiness gates, replay, and fail-closed promotion.
- Markdown format may make it easier to extract stable section headings and public-safe citations.

## Evidence

- Connector access established that the file is readable.
- It is a variant, not an independent evidence source.
- Any benchmark or readiness statement remains source-reported unless supported by ingested artifacts.

## Failure Modes

- Double-counting a Markdown variant as separate corroboration.
- Losing version differences between the primary editable source and Markdown export.
- Treating design/spec content as empirical performance evidence.

## Book Chapters Supported

- MoECOT Runtime and Multi-Core Orchestration
- Integrated Reference Architecture
- Prototype Roadmap

## Claims To Add Or Update

- Use as a variant source when drafting MoECOT chapters.
- Prefer primary artifact/log evidence for any implemented or measured claims.

## Open Questions

- Which MoECOT text should be canonical when `moecot` and `moecot_md` differ?
- Can the Markdown export be safely cached locally outside the public repo for repeat drafting?
