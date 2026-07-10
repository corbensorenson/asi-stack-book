# Source Note: Reframing Superintelligence: Comprehensive AI Services as General Intelligence

| Field | Value |
|---|---|
| Source ID | `ext_drexler_cais_2019` |
| Source title | Reframing Superintelligence: Comprehensive AI Services as General Intelligence |
| Ingestion date | 2026-07-10 |
| Source version / URL | Future of Humanity Institute Technical Report 2019-1; Oxford University Research Archive version of record, https://ora.ox.ac.uk/objects/uuid%3A9c05427a-6390-4b42-9c55-ee45f73a26ad/files/sf4752j50k |
| Citation label | Drexler (2019), Reframing Superintelligence: Comprehensive AI Services as General Intelligence |
| Published / updated | 2019-01-01 / 2019-01-01 |
| DOI | none recorded |
| Ingestion basis | Primary-report passages on service composition, R&D automation, structural safety, and structured development reviewed through the Oxford University Research Archive; the PDF is not vendored into this repository and no CAIS system or result was reproduced. |

## Thesis

Drexler argues that broad advanced AI is usefully modeled as a composition of
AI services and AI-enabled research-and-development processes rather than as a
single, opaque, self-modifying utility-directed agent. The report treats
recursive technology improvement as an R&D-automation problem and presents
structured, task-focused systems as an important control and safety framing.

## Mechanisms

- Describe desired functionality as services and use familiar software
  engineering concepts such as separation of concerns, abstraction,
  encapsulation, modularity, composition, and client/server organization
  (Section I.5, pp. 20-21 of the report PDF).
- Separate AI-development systems from AI-enabled products; the report argues
  that AI R&D is a set of loosely coupled tasks rather than a natural role for
  one self-transforming agent (Section 1, pp. 34-36).
- Treat R&D automation as the direct route by which AI technology can improve,
  while treating AI agents as potential products of that development process
  rather than its necessary engine (Sections 1 and 10).
- Use structured components, independent contributors, and adversarial checks
  as potential safety affordances; the report explicitly notes that these
  affordances mitigate rather than solve control problems (Section 12,
  pp. 76-78).
- Frame deeply structured systems as composed components produced by structured
  development, not merely as a unitary system partitioned after the fact
  (Section 15, pp. 85-88).

## Evidence

- This is a primary technical report that develops conceptual, architectural,
  and safety arguments. It is not a benchmark report, system evaluation, or
  empirical demonstration of CAIS.
- The report supports the existence and content of the CAIS framing, including
  its emphasis on service composition, R&D automation, structural affordances,
  and risks from structured systems.
- This repository has not implemented, reproduced, evaluated, or formally
  compared a CAIS system. It therefore uses the report for prior-art
  positioning and terminology, not for chapter-core support-state promotion.

## Failure Modes

- Service composition does not by itself establish safety, alignment,
  corrigibility, or reliable human control; Drexler explicitly treats CAIS
  affordances as mitigations rather than complete solutions.
- Capabilities that can build or coordinate services can also lower barriers to
  dangerous agents, disruptive applications, or harmful service combinations.
- Structural decomposition can hide authority, evidence, lifecycle, or
  residual ownership unless those interfaces are specified and reviewed.
- A generic claim that a system is a governed stack is not novel merely because
  it is decomposed into services; the book must state its narrower local delta.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model` (ASI Is a Stack, Not a Model)
- `constitutional-alignment-substrate` (Constitutional Alignment: Agency,
  Dignity, and Corrigibility)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement
  Boundaries)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Position the book's stack thesis as a narrower operational-governance
  proposal beside CAIS, not as the first claim that capable AI can be composed
  from services or that R&D automation can drive technology improvement.
- State the book's candidate local delta precisely: typed handoffs, explicit
  authority ceilings, claim/support-state transitions, evidence and residual
  custody, rollback/quarantine routes, and release records attached to each
  interface.
- Use CAIS to distinguish product-level service composition from the book's
  proposed governance contract; do not claim that CAIS proves the contract,
  that the ASI Stack implements CAIS, or that either architecture is safe.
- Keep all affected chapter core claims at `argument` support unless separate
  local evidence-transition records justify a narrower move.

## Open Questions

- Which CAIS structural affordances can be represented by a trace-level
  authority/evidence model rather than prose comparison alone?
- Which CAIS risks around emergent agent-like behavior, misuse, and service
  composition need dedicated owners in the controlled expansion waves?
- What source-noted comparison would show that an ASI Stack interface adds
  operational control beyond a generic modular-service decomposition?
