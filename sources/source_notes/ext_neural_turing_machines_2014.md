# Source Note: Neural Turing Machines

| Field | Value |
|---|---|
| Source ID | `ext_neural_turing_machines_2014` |
| Source title | Neural Turing Machines |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:1410.5401, https://arxiv.org/abs/1410.5401 |
| Ingestion basis | Primary paper abstract and architecture/task sections reviewed; no reproduction. |

## Thesis

A neural controller can learn differentiable read/write access to an external
memory, expanding computation beyond a fixed hidden-state vector.

## Mechanisms

- Content- and location-based differentiable addressing.
- External memory matrix with learned read and write heads.
- End-to-end training on algorithmic tasks.

## Evidence

The source reports copying, sorting, and associative-recall tasks. No local NTM
implementation or extrapolation result exists.

## Failure Modes

- Soft addressing can blur exact identity and order.
- Toy-distribution success may collapse outside trained lengths.
- External memory can hide answer-bearing retrieval or high access cost.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Include learned external-memory controllers in architecture tournaments.
- Test size extrapolation and compare against exact data structures and programs.

## Open Questions

- When does differentiable addressing beat an exact memory interface?
- Can learned memory operations expose auditable failure and rollback semantics?
