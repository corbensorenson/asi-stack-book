# Source Note: Differentiable Neural Computer

| Field | Value |
|---|---|
| Source ID | `ext_differentiable_neural_computer_2016` |
| Source title | Hybrid computing using a neural network with dynamic external memory |
| Ingestion date | 2026-07-15 |
| Source version / URL | Nature 538, https://doi.org/10.1038/nature20101 |
| Ingestion basis | Primary article abstract and architecture/task description reviewed; no reproduction. |

## Thesis

The Differentiable Neural Computer extends neural controllers with dynamic
external memory, allocation, and temporal linkage for structured tasks.

## Mechanisms

- Learned memory allocation and deallocation.
- Temporal link structure for traversing write order.
- Content lookup combined with dynamic memory management.

## Evidence

The article reports graph, question-answering, and reinforcement-learning tasks.
No local DNC result exists.

## Failure Modes

- Learned allocation can corrupt or leak state.
- Differentiable access does not provide exact storage guarantees.
- Task demonstrations can conceal scaling and distribution-shift failures.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Compare learned memory with exact databases, graphs, and program state.
- Require custody, checkpoint, revocation, and migration contracts.

## Open Questions

- Can learned allocation remain reliable as memory and task topology scale?
- Which memory errors can an independent checker detect before effect?
