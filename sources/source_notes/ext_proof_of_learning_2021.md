# Source Note: Proof-of-Learning: Definitions and Practice

| Field | Value |
|---|---|
| Source ID | `ext_proof_of_learning_2021` |
| Source title | Proof-of-Learning: Definitions and Practice |
| Source version / URL | <https://arxiv.org/abs/2103.05633> |
| Ingestion date | 2026-07-24 |

## Thesis

Jia and colleagues propose checkpoint and stochastic-training evidence to
support a claim that final parameters resulted from a stated iterative
learning process. Verification challenges selected transitions rather than
retraining the entire model.

## Mechanisms

- committed intermediate checkpoints;
- logged data-batch and update sequence;
- challenge selection and transition replay;
- tolerances for stochastic or hardware variation;
- prover cost, verifier cost, and storage tradeoffs.

## Evidence

The paper defines and evaluates proof-of-learning methods in studied settings.
The protocol does not prove lawful data, legitimate objectives, absence of
poisoning or hidden training, exact reproducibility, useful capability, or safe
behavior.

## Failure Modes

- forged or strategically spaced checkpoints;
- verifier tolerance hiding invalid transitions;
- omitted optimizer, scheduler, RNG, or preprocessing state;
- alternative hidden training outside the witnessed run;
- challenge predictability;
- proof presence inflated into correctness or compliance.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- `ai-supply-chain-integrity-and-lifecycle-provenance`

## Claims To Add Or Update

- A training witness manifest should bind model, optimizer, scheduler, RNG,
  batches, checkpoints, challenges, tolerances, omissions, and verifier
  identity.
- Proof of a learning history remains one provenance witness, not proof of
  dataset rights, objective quality, safety, or uniqueness.

## Open Questions

- How can proof cost remain practical for distributed frontier training?
- Which omitted states allow convincing but false histories?
- How should privacy and data-rights constraints shape verification?
