# Source Note: Corrigibility

| Field | Value |
|---|---|
| Source ID | `ext_corrigibility_2015` |
| Source title | Corrigibility |
| Ingestion date | 2026-06-28 |
| Source version / URL | PDF, https://intelligence.org/files/Corrigibility.pdf |
| Citation label | Soares et al. (2015), Corrigibility |
| Published / updated | 2015 / 2015 |
| DOI | none recorded |
| Ingestion basis | Primary paper PDF metadata and visible paper text inspected for the alignment/control literature queue; paper not vendored into this repository and no formal result imported. |

## Thesis

This source belongs in the corrigibility chapter as the external reference for systems that do not resist correction, shutdown, or modification by authorized operators. It supports the book's separation between capability, authority, intervention rights, and self-modification.

## Mechanisms

- Treat shutdown permission and operator correction as design targets rather than afterthoughts.
- Analyze incentives around resisting shutdown, manipulating operators, and preserving correction channels.
- Consider how corrigibility properties must persist through subsystem composition and self-modification.
- Motivate explicit governance rights, intervention routes, and replacement/rollback boundaries.

## Evidence

- The source contributes conceptual and formal framing for corrigibility.
- This repository has not imported the paper's formal model, reproduced proofs, or implemented an agent that satisfies its criteria.
- Use it as external alignment literature for problem framing and vocabulary, not as evidence that ASI Stack agency-rights mechanisms are sufficient.

## Failure Modes

- Corrigibility language can be overstated into a safety guarantee.
- Shutdown acceptance in a toy model may not survive tool use, delegation, multi-agent settings, or recursive self-improvement.
- Human intervention rights can become symbolic unless tied to runtime authority and audit mechanisms.

## Book Chapters Supported

- `constitutional-alignment-substrate` (Constitutional Alignment: Agency, Dignity, and Corrigibility)
- `governance-rights-fork-exit-and-audit` (Governance Rights, Fork, Exit, and Audit)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `capability-replacement-and-rollback` (Capability Replacement and Rollback)

## Claims To Add Or Update

- Use this note to compare the ASI Stack's agency-rights and rollback layers against external corrigibility framing.
- Do not claim that the ASI Stack implements or proves corrigibility.
- Keep support state at `argument` unless later formalization, behavior tests, source review, or accepted evidence transitions justify a narrower claim.

## Open Questions

- What is the smallest runtime fixture that can test preservation of correction channels?
- How should the book separate corrigibility for a model, tool adapter, hive, steward agent, and whole stack?
- Which Lean targets need richer lifecycle semantics before they can say anything useful about corrigibility?
