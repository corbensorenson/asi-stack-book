# Source Note: PlanForge Compiler Architecture

| Field | Value |
|---|---|
| Source ID | `planforge_compiler_arch` |
| Source title | PlanForge: A Compiler Architecture for AI Task Orchestration |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1ute1JJLsMfQyRFgKKveSr8U-w_MM-hk5fGxm7Vp5z1o |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/planforge_compiler_arch.txt`; raw text is not published. |

## Thesis

PlanForge Compiler Architecture sharpens the planner-as-compiler frame. Agentic systems waste cost and time when every task is handled by the same expensive model in a serial chain; a compiler layer can decompose work, type primitives, route by minimum viable intelligence, and schedule dependency-aware execution.

## Mechanisms

- Convert natural-language goals into a task graph or intermediate representation.
- Break work into primitives with dependencies, interfaces, and quality gates.
- Route nodes by model tier, tool type, and cost/latency profile.
- Parallelize independent nodes and prioritize the critical path.
- Treat orchestration as compilation rather than chat.
- Use market/cost comparisons as motivating estimates, not validated local results.

## Evidence

- The cache is compact and appears to be a planning/compiler architecture note with market-style estimates.
- The repo has not reproduced cost, time, or quality numbers.
- Use this source to support the PlanForge compiler framing, not as benchmark evidence.

## Failure Modes

- Under-typing a primitive so routing selects an inadequate worker.
- Over-fragmenting work until coordination dominates.
- Treating cost savings as quality-neutral without validator evidence.
- Serializing a DAG through a single chat context.
- Letting the planner silently gain execution authority.

## Book Chapters Supported

- `planforge-dags-and-intelligence-arbitrage` (PlanForge DAGs and Intelligence Arbitrage)
- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)

## Claims To Add Or Update

- Use this source to reinforce the compiler analogy and intelligence-arbitrage mechanism.
- Keep numerical savings source-reported until a reproducible scheduler experiment exists.

## Open Questions

- Should PlanForge and Cognitive Compilation share one semantic IR schema?
- What toy DAG benchmark should validate routing and parallelism claims?
