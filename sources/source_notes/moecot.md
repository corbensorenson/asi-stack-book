# Source Note: MoECOT-Agent Architecture Whitepaper

| Field | Value |
|---|---|
| Source ID | `moecot` |
| Source title | MoECOT-Agent Architecture Whitepaper |
| Ingestion date | 2026-06-24 |
| Source version / URL | Version 1.1, 2026-03-02; https://docs.google.com/document/d/1Lw5qjIFLK1gxGxqYw3_zLneFF5JT_Ihn5VI1CntjtvM |
| Ingestion basis | Authenticated Google Drive connector fetch succeeded; raw text is not published. |

## Thesis

MoECOT is an implementation-reference architecture for governed, skill-native, low-parameter orchestration. It uses a compact orchestrator, specialist lanes, fail-closed control plane, ledgers, readiness gates, replay, and handoff to turn the ASI Stack into an operational runtime candidate.

## Mechanisms

- Compact orchestrator with routed specialist lanes.
- Fail-closed control plane, run/task/control-plane ledgers, replay, and handoff.
- Readiness gates, benchmark artifacts, promotion blockers, and residual tracking.
- Explicit current limitations around Track H, multimodal work, and promotion readiness.

## Evidence

- Connector access established that the source is readable for future drafting.
- The source reports architecture state and benchmark artifacts, but this repo has not ingested or reproduced those artifacts.
- Use as implementation-reference context until code, logs, or release artifacts are inspected.

## Failure Modes

- Treating source-reported benchmark claims as book-verified test results.
- Promoting unavailable or uninspected runtime claims above `argument`.
- Letting specialist lanes mutate or escalate authority without control-plane approval and evidence.

## Book Chapters Supported

- MoECOT Runtime and Multi-Core Orchestration
- Routing Heads and Specialist Cores
- Readiness Gates, Residual Escrow, and Quarantine
- Integrated Reference Architecture
- Prototype Roadmap

## Claims To Add Or Update

- Use MoECOT as the concrete runtime/reference implementation lane.
- Keep runtime and benchmark claims visibly bounded until artifacts are available.
- Tie MoECOT promotion to readiness, regression, replay, and ledger evidence.

## Open Questions

- Which MoECOT repository artifacts are public-safe to inspect and cite?
- Which benchmark artifacts should be imported into `test_results/` as source-reported versus reproduced?
- Which MoECOT readiness gates should become executable schemas or tests?
