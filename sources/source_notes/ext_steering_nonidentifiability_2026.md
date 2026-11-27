# On the Non-Identifiability of Steering Vectors in Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_steering_nonidentifiability_2026` |

Sohan Venkatesh, Ashish Mahendran Kurapath. [Primary paper, arXiv 2602.06801v4](https://arxiv.org/html/2602.06801v4).

## Thesis

Similar observed behavior under different steering directions limits identification of a unique internal cause.

## Mechanisms

Challenge the identity of a proposed steering direction using controlled perturbations and matched controls.

## Evidence

The authors found similar semantic scores across many tested traits and prompts. Appendix B reports smaller logit shifts for the perturbed steering directions than for the reported random controls, with nonzero distances in all ten model–trait conditions.

## Failure Modes

Figure 1, the finite-strength perturbation experiments, and Appendices B and C. Exact first-order equality requires a perturbation in the null space of the particular readout Jacobian. Orthogonality to the original steering vector alone does not imply that condition. Finite interventions and new prompt distributions require behavioral checks.

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance` — [Can two directions pass the same persona test?](../../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#can-two-directions-pass-the-same-persona-test)

## Claims To Add Or Update

State which readout, intervention strength and controls support a steering interpretation.

## Open Questions

Does an alternative direction that matches the chosen readout also match on held-out behaviors?
