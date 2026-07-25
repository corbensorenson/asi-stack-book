# Source Note: No Free Lunch and Inductive Bias

| Field | Value |
|---|---|
| Source ID | `ext_no_free_lunch_inductive_bias_2024` |
| Source title | Position: The No Free Lunch Theorem, Kolmogorov Complexity, and the Role of Inductive Biases in Machine Learning |
| Authors / date | Micah Goldblum, Marc Anton Finzi, Keefer Rowan, and Andrew Gordon Wilson; ICML 2024 |
| Primary URL | https://proceedings.mlr.press/v235/goldblum24a.html |
| Source type | peer-reviewed position and empirical paper |
| Evidence boundary | Theoretical interpretation and source-reported experiments; not proof that one universal model is optimal for real-world tasks. |

## Thesis

The paper explains that no-free-lunch results average over a uniform space of
learning problems, while real data and modern models can share
low-complexity-biased structure. It is valuable precisely because it prevents
two opposite errors: claiming one learner wins on every possible problem, and
using no-free-lunch as proof that every domain requires a wholly bespoke
architecture.

## Failure Modes

- Kolmogorov complexity is not generally computable, and a compression proxy
  does not reveal the true data-generating process.
- Observed inductive preferences do not guarantee transfer, robustness,
  interpretability, or safety.
- Assumptions, distributions, hypothesis classes, resources, and loss
  functions remain part of the claim.

## Book Chapters Supported

- `learning-theory-generalization-and-scaling-science`: explicit
  assumption-and-impossibility boundary.
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`: empirical
  architecture choice rather than universal ideology.

## Mechanisms

- Make hypothesis class, distribution, loss, resource limit, and inductive bias
  explicit in every generalization comparison.

## Evidence

The ICML paper develops theoretical relationships among no-free-lunch results,
Kolmogorov complexity, and inductive bias. It does not identify a universally
correct bias.

## Claims To Add Or Update

- Attach an assumption and identifiability ledger to learning, scaling,
  emergence, and architecture claims.

## Open Questions

- Which assumptions actually carry observed transfer, and which controls can
  break them without changing the construct being measured?
