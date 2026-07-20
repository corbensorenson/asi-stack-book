# Source Note: DataStates-LLM: Lazy Asynchronous Checkpointing for Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_datastates_llm_2024` |
| Source title | DataStates-LLM: Lazy Asynchronous Checkpointing for Large Language Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | HPDC 2024 / arXiv:2406.10707, https://arxiv.org/abs/2406.10707 |
| Citation label | Maurya et al. (2024), DataStates-LLM |
| Published / updated | 2024-06-15 / 2024-06-15 |
| DOI | 10.1145/3625549.3658685 |
| Ingestion basis | Primary paper reviewed, especially Sections 1--2, 4, 6, and limitations; no implementation, checkpoint, or performance result reproduced. |

## Thesis

Checkpoint creation is itself a distributed consistency and performance
problem. DataStates-LLM exploits intervals in which model and optimizer shards
are immutable to copy them asynchronously across memory and storage tiers while
coordinating a consistent checkpoint.

## Mechanisms

- Lazy device-to-host copies during immutable portions of an iteration.
- Multi-level asynchronous flushing and later consolidation of distributed
  model and optimizer shards.
- Coordination across data, pipeline, and tensor parallelism.
- Explicit distinction between blocking checkpoint creation and persistent
  background completion.

## Evidence

The paper evaluates several models and parallelism configurations, reporting up
to 180 GPUs, faster checkpoint operations, and end-to-end runtime gains. Those
results are source-reported and were not reproduced. The scope is checkpoint
performance and consistency, not complete trajectory equivalence.

## Failure Modes

- A torn checkpoint mixes shards from different logical steps.
- “Save returned” is treated as durable completion while asynchronous writes
  remain in flight.
- Model and optimizer shards are retained but scheduler, RNG, scaler, data
  cursor, compiler, or external state is omitted.
- High checkpoint frequency hides I/O contention, host-memory pressure, or
  incomplete failure recovery.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- Boundary context: `model-weight-custody-and-hardware-roots-of-trust`

## Claims To Add Or Update

- Separate checkpoint request, staged copy, persistent commit, validation, and
  resume authority.
- Require logical-step consistency and complete declared state, not merely file
  presence or checkpoint throughput.

## Open Questions

- What is the minimum complete state for exact versus statistically equivalent
  resume?
- How should asynchronous checkpoint failures be represented in the run
  denominator and recovery policy?
