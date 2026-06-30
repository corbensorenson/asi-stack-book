# Source Note: Collective Constitutional AI: Aligning a Language Model with Public Input

| Field | Value |
|---|---|
| Source ID | `ext_collective_constitutional_ai_2024` |
| Source title | Collective Constitutional AI: Aligning a Language Model with Public Input |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2406.07814, https://arxiv.org/abs/2406.07814 |
| Citation label | Huang et al. (2024), Collective Constitutional AI |
| Published / updated | 2024-06-12 / 2024-06-12 |
| DOI | 10.1145/3630106.3658979 |
| Ingestion basis | Primary arXiv abstract/metadata and ACM DOI metadata inspected for the constitutional-AI governance queue; paper not vendored into this repository and no public-input process, fine-tuning run, or evaluation reproduced. |

## Thesis

This source grounds the book's constitutional and governance chapters against a public-input constitutional-AI baseline. It is especially useful because the ASI Stack distinguishes constitution content from authorship, contestability, migration rules, and review rights.

## Mechanisms

- Source principles from a target population rather than only from model developers.
- Integrate public input into a language-model constitution and train/evaluate a model against that constitution.
- Treat broader participation as an alignment-governance problem, not merely a prompt-engineering problem.
- Provide a comparator for ASI Stack questions about who can propose, contest, migrate, or audit constitutional predicates.

## Evidence

- The source contributes an external process for constitutional principle sourcing and model fine-tuning with public input.
- This repository has not reproduced the public-input process, evaluated the resulting model, or imported any governance dataset.
- Use it as a comparator for constitution authorship and public input, not as evidence that the ASI Stack has legitimate institutional governance.

## Failure Modes

- Treating public input as automatically representative, legitimate, or sufficient.
- Letting model-level constitutional training substitute for runtime appeal, audit, fork, or exit interfaces.
- Collapsing contestability into one-time principle selection.

## Book Chapters Supported

- `constitutional-alignment-substrate` (Constitutional Alignment: Agency, Dignity, and Corrigibility)
- `governance-rights-fork-exit-and-audit` (Governance Rights, Fork, Exit, and Audit)

## Claims To Add Or Update

- Use this note to add external grounding for public-input constitutional AI in the constitutional-alignment chapter.
- Use it to sharpen governance-rights prose around authorship, contestability, and migration without claiming institutional legitimacy.
- Keep support state at `argument` unless future review or evidence artifacts evaluate actual governance processes.

## Open Questions

- What counts as adequate public or stakeholder input for a self-improving AI constitution?
- How should a constitution record dissent from the population that supplied its principles?
- Which migration records are needed when public-input principles change after deployment?
