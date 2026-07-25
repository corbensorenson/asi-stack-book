# Source Note: A Theory of the Learnable

| Field | Value |
|---|---|
| Source ID | `ext_valiant_theory_learnable_1984` |
| Source title | A Theory of the Learnable |
| Source version / URL | <https://dl.acm.org/doi/10.1145/1968.1972> |
| Ingestion date | 2026-07-24 |

## Thesis

Valiant's PAC formulation makes a learning claim conditional on a concept or
hypothesis class, data-generating assumptions, target error, confidence, and
resource bound. Learnability is a quantified statement, not a synonym for
successful training.

## Mechanisms

- probably approximately correct guarantees;
- sample and computational complexity;
- hypothesis-class and distribution assumptions;
- explicit error and confidence parameters;
- learnability reductions between representation classes.

## Evidence

The paper provides foundational formal results under its model assumptions.
It does not directly explain modern foundation-model behavior, distribution
shift, in-context learning, open-ended agency, or safety, and it certifies no
trained ASI Stack model.

## Failure Modes

- quantifiers or distribution assumptions omitted from a “generalization”
  claim;
- asymptotic feasibility mistaken for practical trainability;
- iid assumptions applied under adaptive deployment;
- hypothesis-class mismatch;
- low average error hiding catastrophic tail behavior;
- learnability conflated with aligned or safe behavior.

## Book Chapters Supported

- `learning-theory-generalization-and-scaling-science`

## Claims To Add Or Update

- Learning-theory statements should expose hypothesis class, distribution,
  error, confidence, sample, compute, and loss assumptions.
- PAC-style guarantees illuminate claim structure but do not automatically
  transfer to foundation-model capability or safety.

## Open Questions

- Which modern model properties admit meaningful finite-sample guarantees?
- How should adaptive, non-iid deployment alter the contract?
- What learning guarantees capture rare high-consequence failures?
