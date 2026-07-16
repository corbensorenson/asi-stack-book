# Source Note: Learning to Learn at Test Time

| Field | Value |
|---|---|
| Source ID | `ext_ttt_layers_2024` |
| Source title | Learning to (Learn at Test Time): RNNs with Expressive Hidden States |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2407.04620, https://arxiv.org/abs/2407.04620 |
| Ingestion basis | Primary paper abstract and architecture/evaluation sections reviewed; no reproduction. |

## Thesis

Test-time training layers make the hidden state itself a learned model updated
while processing a sequence, expanding the capacity and risk of recurrent state.

## Mechanisms

- Online self-supervised update rule inside a sequence layer.
- Hidden state represented by model parameters rather than a fixed-size vector.
- Parallelization strategies for test-time updates.

## Evidence

The paper reports sequence-modeling results. No local training, online update,
quality, contamination, or rollback result exists.

## Failure Modes

- Online state can absorb malicious, private, revoked, or low-quality inputs.
- Model, optimizer, update rule, and cache may be checkpointed inconsistently.
- Adaptation gains can hide extra compute and delayed failure.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat test-time learned state as governed mutable state with provenance.
- Require reset, rollback, contamination, and delayed-outcome tests.

## Open Questions

- What is the authoritative checkpoint for online-updated hidden state?
- Can harmful influence be removed without destroying useful adaptation?
