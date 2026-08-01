# Source Note: MoECOT-Agent Architecture Whitepaper

| Field | Value |
|---|---|
| Source ID | `moecot` |
| Source title | MoECOT-Agent Architecture Whitepaper |
| Ingestion date | 2026-07-31 |
| Source version / URL | Version 1.1, 2026-03-02; https://docs.google.com/document/d/1Lw5qjIFLK1gxGxqYw3_zLneFF5JT_Ihn5VI1CntjtvM |
| Ingestion basis | Full authenticated Google Drive connector text passage-reviewed; raw private text is not published. The stronger pinned local implementation dossier remains a separate source record. |

## Thesis

MoECOT proposes a small, explicit orchestrator over bounded specialist lanes, with deterministic control flow, fail-closed side-effect policy, durable ledgers, readiness separate from routability, and replayable handoff. Its most durable contribution to the book is not a named runtime but a separation rule: a specialist may be available without being ready, selected without being authorized, and successful without being promotable.

## Mechanisms

- A compact orchestrator routes typed work to specialist lanes rather than asking one model to own planning, execution, verification, memory, and policy.
- A task state machine, leases, retries, dead-letter handling, and first-error localization make non-success explicit.
- Run, task, and control-plane ledgers bind route decisions, effects, evidence, replay, and handoff.
- Skills and context envelopes constrain what a lane receives; side-effect envelopes bind approval, budget, MCP/tool policy, secrets, redaction, and vault use.
- Readiness is evaluated separately from default routing through core, hard, holdout, red-team, and stretch benchmark lanes.
- Independent artifact judges, backend provenance, architecture fingerprints, and promotion blockers reduce benchmark and implementation self-reporting.
- Pressure-driven escalation and controlled improvement lanes can propose changes, but no weight, route, authority, or default change follows without the relevant gate.

## Evidence

- The complete v1.1 connector text was reviewed, including architecture, state-machine, ledger, permission, benchmark, replay, and limitation sections.
- The document reports an implementation state and benchmark artifacts. Those runtime artifacts, commands, logs, and results were not imported or reproduced in this repository.
- The pinned `moecot_manifest_project` dossier independently inspects tracked project artifacts and is the stronger implementation-reference record; this whitepaper supplies authorial design intent and terminology, not independent corroboration.
- The source itself describes a deterministic control-flow runtime with lexical/policy routing and multiple non-default cores. It does not establish a learned router, production safety, or broad empirical superiority.

## Failure Modes

- Confusing `available`, `ready`, `authorized`, `selected`, and `promoted`.
- Treating a successful route as evidence when denied routes, failed gates, missing replay references, and residual handoffs are omitted.
- Letting a specialist, benchmark author, or runtime self-ratify its own promotion.
- Allowing task retries, handoffs, or improvement lanes to exceed the original side-effect envelope.
- Treating the whitepaper and its Markdown export as two independent sources.

## Book Chapters Supported

- ASI Is a Stack, Not a Model
- The Efficient ASI Hypothesis
- System Boundaries and Authority
- Failure Modes of Ungoverned Intelligence
- Stable Capability Fields
- Capability Replacement and Rollback
- Recursive Self-Improvement Boundaries
- Command Contracts: From Intent to Executable Work
- Planning as a Control Layer: DAGs and Intelligence Arbitrage
- The Virtual Context ABI: Typed Pages, Cells, and Certificates
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

- Model route admission as the conjunction of capability fit, readiness, authority, context/tool leases, and effect policy rather than one router score.
- Require runtime evidence packets to preserve denied routes and failed gates alongside successful execution.
- Keep improvement lanes proposal-producing and non-self-ratifying.
- Describe MoECOT as an authenticated architecture whitepaper and implementation reference; reserve implemented or measured language for inspected runtime artifacts.

## Open Questions

- Which source-reported runtime artifacts can be imported with stable digests and public-safe provenance?
- Can replay be implemented by an independent consumer rather than the runtime that emitted the ledger?
- How do learned routing and heterogeneous model backends change the deterministic control-plane assumptions?

## Section-Family Closure Ledger

| Family | Disposition | Book effect |
|---|---|---|
| Orchestrator and specialists | integrated | Routing and stack chapters own the bounded-head/bounded-lane pattern. |
| State, leases, retries, dead letter | integrated | Labor, runtime, and artifact-ledger chapters own explicit task lifecycle. |
| Skills, context, and side-effect envelopes | integrated | VCM, runtime, authority, and command-contract chapters own the lease surfaces. |
| Readiness and benchmark lanes | integrated | Readiness and benchmark chapters own promotion discipline. |
| Replay, provenance, fingerprints, handoff | integrated | Artifact/replay and integrated-architecture chapters own durable receipts. |
| Improvement lanes | integrated with non-promotion boundary | RSI and policy-learning chapters treat them as governed proposal paths. |
| Source-reported implementation and benchmarks | research obligation | Import and independent reproduction remain open. |

## Non-Claims

This note does not establish a reproduced MoECOT runtime, learned routing advantage, replay correctness, production safety, benchmark validity, specialist quality, authority enforcement, or ASI. Connector access is not publication of the private source text.
