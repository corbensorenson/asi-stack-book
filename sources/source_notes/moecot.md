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

- ASI Is a Stack, Not a Model
- The Efficient ASI Hypothesis
- System Boundaries and Authority
- Failure Modes of Ungoverned Intelligence
- Stable Capability Fields
- Capability Replacement and Rollback
- Recursive Self-Improvement Boundaries
- Intent-to-Execution Contracts
- Planning as a Control Layer
- PlanForge DAGs and Intelligence Arbitrage
- Virtual Context ABI
- Labor OS and Typed Jobs
- Artifact Graphs, Audit Logs, and Replay
- Runtime Adapters, Tool Permissions, and Human Approval
- Procedural Memory and Cognitive Loop Closure
- Routing Heads and Specialist Cores
- Readiness Gates, Residual Escrow, and Quarantine
- Benchmark Ratchets and Anti-Goodhart Evidence
- Policy Optimization and Learning from Feedback
- Integrated Reference Architecture
- Prototype Roadmap
- Living Book Methodology
- Open Research Agenda and Bibliography Plan

## Claims To Add Or Update

- Use MoECOT as the concrete runtime/reference implementation lane.
- Use MoECOT as implementation-reference context for compact orchestration, specialist lanes, fail-closed control planes, ledgers, readiness gates, replay, and promotion blockers.
- Use MoECOT to connect planner handoff, labor execution, artifact logs, runtime adapters, procedural reuse, and benchmark gates as runtime-reference context only until concrete artifacts are inspected.
- Use MoECOT to frame policy optimization as a runtime-adjacent update path for specialist routing and orchestration that still requires readiness, regression, replay, and ledger evidence.
- Keep runtime and benchmark claims visibly bounded until artifacts are available.
- Tie MoECOT promotion to readiness, regression, replay, and ledger evidence.

## Open Questions

- Which MoECOT repository artifacts are public-safe to inspect and cite?
- Which benchmark artifacts should be imported into `test_results/` as source-reported versus reproduced?
- Which MoECOT readiness gates should become executable schemas or tests?
