# Source Note: Cognitive Compilation

| Field | Value |
|---|---|
| Source ID | `cognitive_compilation` |
| Source title | Cognitive Compilation |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1spEWiRnk1NUFuK3BLh3X80r_Up_SyebO1c3JSEzTUis |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/cognitive_compilation.txt`; raw text is not published. |

## Thesis

Cognitive Compilation reframes complex generative work as a compiler pipeline. Instead of asking a model to directly emit the final artifact, the system compiles goals into a structured source plan, typed semantic intermediate representation, target-specific instructions, and validator-backed artifacts.

## Mechanisms

- Separate plan formation, semantic compilation, target compilation, execution, and repair.
- Convert user goals, constraints, interfaces, resources, and quality gates into a source plan.
- Compile the source plan into typed semantic atoms with explicit inputs, outputs, constraints, dependencies, and validation requirements.
- Run compiler-style passes: extraction, normalization, typing, dependency analysis, linting, scheduling, and target lowering.
- Use a DAG to expose parallelism, critical path, slack, and localized recompilation opportunities.
- Route subtasks to different capability tiers for intelligence arbitrage.
- Repair failed nodes locally instead of regenerating the whole artifact.
- Evaluate with tests, validator pass rate, token use, wall-clock time, repair locality, and cross-artifact consistency.

## Evidence

- The source is an architecture and evaluation-plan paper.
- It provides concrete compiler analogies, IR roles, pipeline stages, ablation ideas, and measurement proposals.
- It does not provide local benchmark results, a working compiler in this repository, or validated task traces.
- Its claims should remain architectural unless the repo adds a prototype, trace suite, or empirical ablation.

## Failure Modes

- Semantic under-specification in the source plan.
- Validator scarcity for non-code artifacts.
- IR overhead that outweighs benefits for small tasks.
- Type or dependency errors that make a graph appear executable when it is underspecified.
- Capability routing that saves tokens while degrading quality.
- Global regeneration that erases traceability and repair locality.

## Book Chapters Supported

- `human-intent-as-a-formal-input` (Human Intent as a Formal Input)
- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work; includes folded command-contract semantic-interface material)
- `planning-as-a-control-layer` (Planning as a Control Layer: DAGs and Intelligence Arbitrage)
- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)
- `semantic-representation-and-tree-structured-models` (Semantic Representation and Tree-Structured Models)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)

## Claims To Add Or Update

- Use this source as a backbone for the book's compile-time view of cognition: intent becomes an IR before it becomes action.
- Tie PlanForge, artifact graphs, command contracts, and localized repair into one build-system metaphor.
- Keep direct-generation criticism focused on failure surfaces: entangled requirements, state drift, serialized work, and uniform overuse of expensive cognition.

## Open Questions

- Which S-IR fields should become stable schemas in this repo?
- Should the first prototype target book-writing tasks, code-generation tasks, or both?
- What validator suite would make repair-locality claims measurable?
