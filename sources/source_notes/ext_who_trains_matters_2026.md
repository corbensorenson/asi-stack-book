# Who Trains Matters: Federated Learning under Enrollment and Participation Selection Biases

| Field | Value |
|---|---|
| Source ID | `ext_who_trains_matters_2026` |
| Publication | Gota Morishita (2026). [Primary publication](https://arxiv.org/html/2604.26604v1). |

## Thesis

Separate enrollment in the reachable pool from participation in an individual training round.

## Mechanisms

Model enrollment and round-level participation as distinct selection stages and reweight observed updates for both.

## Evidence

The authors analyze two-stage inverse-probability weighting and evaluate it on synthetic federated logistic regression.

## Failure Modes

Inference for the target population needs suitable measured selection factors and positive inclusion probabilities.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence`

## Claims To Add Or Update

The chapter uses the paper as an external comparison in “Which devices could ever contribute to training?” and retains its existing core support state.

## Open Questions

Which intended clients have zero probability of enrollment, and what population claim remains supportable?
