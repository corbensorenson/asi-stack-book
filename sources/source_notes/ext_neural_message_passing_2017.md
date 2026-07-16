# Source Note: Neural Message Passing for Quantum Chemistry

| Field | Value |
|---|---|
| Source ID | `ext_neural_message_passing_2017` |
| Source title | Neural Message Passing for Quantum Chemistry |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:1704.01212v2, https://arxiv.org/abs/1704.01212 |
| Ingestion basis | Primary paper abstract and framework/method sections reviewed; no reproduction. |

## Thesis

Message Passing Neural Networks learn local message and aggregation functions
over graph-structured inputs, providing a non-token-native relational substrate.

## Mechanisms

- Repeated learned messages along graph edges.
- Node-state updates and graph-level readout.
- Structural inductive bias supplied by the input graph and its symmetries.

## Evidence

The paper reports molecular-property prediction results under its evaluated
datasets. No local message-passing model, dynamic-graph task, reasoning test, or
architecture comparison exists.

## Failure Modes

- Message-passing depth can cause oversmoothing, bottlenecks, or poor long-range propagation.
- A supplied graph can leak task structure or encode the answer-bearing relation.
- Molecular prediction does not establish general reasoning or reliable exact graph memory.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Include graph/relational processors as a distinct ABI family.
- Separate exact graph identity and provenance from learned messages and node state.

## Open Questions

- When do relational inductive biases improve transfer rather than constrain it?
- Can dynamic graph state be checkpointed, migrated, and revoked without semantic loss?
