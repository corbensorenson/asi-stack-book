# Source Note: AI safety via debate

| Field | Value |
|---|---|
| Source ID | `ext_ai_safety_debate_2018` |
| Source title | AI safety via debate |
| Ingestion date | 2026-07-01 |
| Source version / URL | arXiv:1805.00899v2, https://arxiv.org/abs/1805.00899 |
| Citation label | Irving, Christiano, and Amodei (2018), AI safety via debate |
| Published / updated | 2018-05-02 / 2018-10-22 |
| DOI | 10.48550/arXiv.1805.00899 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the debate/adversarial-review literature queue; debate code, MNIST experiments, and any training data are not imported into this repository. |

## Thesis

This source belongs in `spinoza-verification-and-proof-carrying-claims` as an external comparator for adversarial review. It helps distinguish a tribunal-style record from mere consensus: competing agents or reviewers may surface evidence that a single judge would miss, but the debate setup still depends on judge quality, task structure, incentives, and empirical validation.

## Mechanisms

- Train agents through a zero-sum debate game.
- Have agents make short statements about a question or proposed action.
- Use a human judge to decide which side provides the most true or useful information.
- Analyze debate through a complexity-theoretic analogy and through small empirical experiments.

## Evidence

- The source reports initial MNIST debate experiments and explicitly frames debate success as depending on empirical and theoretical questions.
- This repository has not reproduced the debate experiments, trained debate agents, measured human judge quality, or implemented debate routing.
- Use this source as external debate lineage for adversarial review, not as evidence that ASI Stack tribunal review works.

## Failure Modes

- Debate can become persuasion theater if the judge cannot detect the relevant failure.
- Shared context, incentives, or model family can make two debaters fail in correlated ways.
- A debate verdict can be over-read as truth rather than as a scoped review result with dissent, limits, and residuals.

## Book Chapters Supported

- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to ground debate/adversarial-review language and the need for dossier boundaries, reviewer roles, dissent preservation, and verdict constraints.
- Do not claim the ASI Stack has implemented debate, improved judge accuracy, or solved scalable oversight.
- Keep support state at `argument` until local debate, reviewer-independence, adversarial-probe-quality, and verdict-correctness evidence exists.

## Open Questions

- What tribunal fixture would distinguish evidence-surfacing debate from consensus theater?
- Which review records should preserve both winning arguments and unresolved dissent?
- How should a high-risk claim route differently when a judge is weak, biased, or missing key context?
