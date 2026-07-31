# Source Note: PlanForge Compiler Architecture

| Field | Value |
|---|---|
| Source ID | `planforge_compiler_arch` |
| Source title | PlanForge: A Compiler Architecture for AI Task Orchestration |
| Ingestion date | 2026-06-24; fidelity audit 2026-07-31 |
| Source version / URL | Google Docs inventory source: https://docs.google.com/document/d/1ute1JJLsMfQyRFgKKveSr8U-w_MM-hk5fGxm7Vp5z1o |
| Canonical local cache | `sources/raw/google_docs/planforge_compiler_arch.txt`; SHA-256 `5cb241085015bb7f85b9a1d7bc453b5cf00207837bd03e615e3e398d515a6793` |
| Variant relation | After removing its UTF-8 BOM, this file is byte-identical to Tab 4 embedded in `sources/raw/google_docs/planforge.txt`. It is a separately inventoried presentation variant, not a second conceptual or empirical source. |
| Evidence boundary | Architecture prose, analogies, illustrative tier/cost table, two synthetic arithmetic scenarios, and related-work positioning. No implementation, trace, measurement, or reproduction. |

## Claim Boundary

This variant sharpens the compiler analogy and ties PlanForge to BeastBrain OS
as a proposed kernel-level scheduler and to Aletheia as inspiration for a
primitive vocabulary and falsification-oriented Watchdog. Those ecosystem
links are author-lineage claims. They do not establish that the systems are
implemented, compatible, safe, or empirically validated.

Its abstract says synthetic benchmarks “validate” 60–85% routine-task savings.
The body contains the same two assumed-price, assumed-parallelism arithmetic
scenarios reconciled in `sources/source_notes/planforge.md`; there are no raw
traces, outputs, quality checks, planner costs, confidence intervals, failure
rates, or hardware/service observations. The numeric language is retained only
as source-reported motivation.

## Thesis

This variant presents PlanForge as a cognitive compiler and potential OS
scheduler: translate admitted natural-language intent into a typed task graph,
optimize common work, assign the least costly adequate worker, schedule the
critical path, and supervise execution through a Watchdog. Its useful content
is the compiler/runtime boundary, not the paper's promotional performance or
novelty wording.

## Mechanisms

- **OS scheduling role.** PlanForge is positioned as an intelligence-native
  scheduler for heterogeneous cognitive work, not merely a chat-agent library.
  The book routes this to Planning and Personal Compute Hives while preserving
  their security, authority, identity, partition, and privacy owners.
- **Compiler phases.** A front end decomposes natural language, a middle end
  proposes semantic deduplication and consistency repair, a back end annotates
  MVI and schedules a typed DAG, and a Watchdog executes and escalates.
- **Semantic primitive claim.** The source mentions an immutable catalog of
  roughly 300 abstract Aletheia-inspired atoms such as `CAUSE`, `PREVENT`,
  `ENABLE`, `KNOW`, `BELIEVE`, and `VERIFY`. No catalog or coverage proof is
  supplied. The book distinguishes these semantic relation families from
  executable primitives with typed operands, effects, authority, evidence, and
  recovery.
- **Dedup threshold.** Cosine similarity above an illustrative 0.92 threshold
  proposes merges. The book treats this only as candidate retrieval and
  requires semantic/effect/consumer/authority compatibility before a merge.
- **Critical-path arbitrage.** Zero-slack nodes may justify faster workers;
  positive-slack nodes may use cheaper slower qualified workers. Duration,
  queue, retry, merge, and verifier uncertainty prevent an optimality claim.
- **Watchdog.** Schema validation, contextual tier escalation, and delayed
  stronger-worker speculation are integrated with idempotence, isolation,
  cancellation, duplicate-effect, privacy, capacity, and complete-cost rules.

## Variant Delta From the Main Family

Most content duplicates the main PlanForge tabs. The meaningful presentation
delta is the explicit BeastBrain kernel-scheduler role, the Aletheia-inspired
primitive and tribunal analogy, a more concise five-phase stack, and a feature
comparison table against then-current agent frameworks. The comparison table's
“none” cells are not independently verified and may be stale. The source adds
no distinct data, experiment, algorithm implementation, or support.

## Evidence

The evidence is one architecture description and the same two synthetic
arithmetic scenarios already present in the main family. The exact duplicate
relationship is verified by normalized byte comparison. No implementation,
natural-task output, benchmark trace, cost observation, quality evaluation,
failure record, or independent reproduction is supplied.

## Failure Modes

- Counting the duplicate cache as independent support.
- Treating a semantic atom or embedding match as an executable or equivalent
  obligation.
- Converting named model tiers and assumed prices into stable MVI evidence.
- Calling an acyclic or critical-path schedule correct without dependency,
  outcome, and cost validation.
- Letting Watchdog retry or speculation duplicate effects or expand authority.
- Importing stale “none” cells in framework comparisons as novelty evidence.

## Interfaces and Invariants

- Planning consumes accepted goals and emits dispatch requests, never
  self-authorized effects.
- The task DAG is an intermediate representation; serialization alone does not
  make it deterministic machine code.
- Semantic hashes propose common work and retain split/rollback lineage.
- MVI is a calibrated node/route/contract estimate, not a fixed model tier.
- Watchdog schema validity is not outcome adequacy or plan correctness.
- Speculation is disabled or isolated for irreversible and non-idempotent
  effects.
- BeastBrain, Aletheia, and separate PlanForge variants do not corroborate one
  another merely because the same architectural prose names them.

## Book Chapters Supported

- `planning-as-a-control-layer`
- `cognitive-compilation-and-semantic-ir`

The main `planforge` source separately supports broader intent, runtime,
resource, hive, steward, architecture, prototype, and research owners.

## Claims To Add Or Update

- Preserve the front/middle/back compiler decomposition and strict
  planner/runtime boundary.
- Distinguish semantic relation vocabularies from bound executable primitives.
- Treat semantic hashes, MVI scores, and critical-path estimates as uncertain
  proposals with independent checks and complete receipts.
- Count the separate cache once with embedded Tab 4 and keep its synthetic
  savings outside empirical support.

## Open Questions

- Does the compiler-architecture variant contain any recoverable artifact or
  source revision beyond the exact embedded text?
- Can one typed IR serve PlanForge scheduling and Cognitive Compilation
  lowering without collapsing their ownership boundaries?
- Which Watchdog invariants can be proven on a finite runtime while preserving
  open-world outcome uncertainty?

## Section-Family Coverage

| Variant section | Actual owner | Disposition |
|---|---|---|
| Abstract and §1 | Planning; this note | Orchestration-gap and compiler framing integrated; savings and novelty language bounded. |
| §2 | Planning; Cognitive Compilation | Planner/executor split and intelligence-arbitrage principle integrated without deterministic or authority overclaim. |
| §3 phases 1–2 | Planning; Cognitive Compilation | Typed decomposition, atom distinction, semantic dedup, subtree merge, consistency checks, and DAG IR integrated. |
| §3 phases 3–5 | Planning; Routing; Runtime | MVI, critical path, HEFT, timed schedule, and handoff integrated as proposed mechanisms. |
| §4 | Planning; Runtime | Watchdog schema validation, escalation, and speculation integrated with missing safety/cost controls repaired. |
| §5 | main PlanForge note; empirical backlog | Synthetic scenario values retained once as non-empirical arithmetic examples. |
| §6 and references | source note; Appendix H backlog | Framework comparison and HTN/TAMP relations retained for independent current-primary-source review; no novelty claim. |
| §7 | Planning summary; this note | Infrastructure-layer conclusion retained at `argument`. |

## Closure Status

**Exact duplicate-variant audit complete as of 2026-07-31.** The normalized
source is byte-identical to PlanForge Tab 4; all distinct presentation content
is integrated or explicitly bounded, and repeated prose/numbers count once.
No implementation, benchmark, saving, reliability, scheduler, security,
deployment, transfer, or ASI claim is established.
