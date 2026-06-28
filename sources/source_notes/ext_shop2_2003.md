# Source Note: SHOP2: An HTN Planning System

| Field | Value |
|---|---|
| Source ID | `ext_shop2_2003` |
| Source title | SHOP2: An HTN Planning System |
| Ingestion date | 2026-06-28 |
| Source version / URL | JAIR article page, https://www.jair.org/index.php/jair/article/view/10362 |
| Citation label | Nau et al. (2003), SHOP2 |
| Published / updated | 2003-12-01 / not recorded |
| DOI | 10.1613/jair.1141 |
| Ingestion basis | Primary JAIR article page/PDF metadata inspected for the planning/control literature queue; paper not vendored into this repository and no HTN planner run reproduced. |

## Thesis

SHOP2 belongs in the planning chapters as an external reference for hierarchical task-network planning and ordered task decomposition. It gives PlanForge a comparison point for decomposing goals into method-governed tasks without implying that PlanForge implements SHOP2 or reproduces its competition performance.

## Mechanisms

- Use hierarchical task networks to decompose tasks into ordered subtasks.
- Select methods for decomposing compound tasks into executable or further-decomposed tasks.
- Address temporal and metric planning-domain features in the source system.
- Report distinguished performance in the 2002 International Planning Competition as source-reported context, not local evidence.

## Evidence

- The source reports the design and competition context of SHOP2.
- This repository has not run SHOP2, imported IPC domains, translated PlanForge DAGs into HTN methods, or reproduced competition results.
- Use this source as external task-decomposition vocabulary, not as evidence for ASI Stack planning quality.

## Failure Modes

- Hierarchical decomposition can preserve procedural assumptions that should have been questioned.
- Method libraries can hide authority expansion, context gaps, or unsafe inherited defaults.
- Source-reported competition performance cannot become evidence for local task decomposition, replanning, or execution safety.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer)
- `planforge-dags-and-intelligence-arbitrage` (PlanForge DAGs and Intelligence Arbitrage)
- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to ground external HTN and ordered task-decomposition vocabulary.
- Do not claim that ASI Stack planning implements SHOP2, imports SHOP2 methods, or reproduces IPC results.
- Keep support state at `argument` until deterministic decomposition fixtures, planner translations, or accepted evidence transitions exist.

## Open Questions

- Which PlanForge DAG fields correspond to HTN tasks, methods, and decomposition choices?
- How should an ASI Stack planner record a rejected decomposition method?
- What fixture would prove that authority ceilings survive hierarchical decomposition?
