# Source Note: The Llama 3 Herd of Models

| Field | Value |
|---|---|
| Source ID | `ext_llama3_herd_2024` |
| Source title | The Llama 3 Herd of Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2407.21783v3, https://arxiv.org/abs/2407.21783 |
| Citation label | Grattafiori et al. (2024), The Llama 3 Herd of Models |
| Published / updated | 2024-07-31 / 2024-11-23 |
| DOI | 10.48550/arXiv.2407.21783 |
| Review state | Paper-body review complete for the bounded training-systems use; no local reproduction. |
| Ingestion basis | Official arXiv v3 paper inspected, especially Sections 3.3.1--3.3.4 and Tables 4--5. Code, model artifacts, raw training logs, checkpoints, and evaluations were not ingested or run locally. |

## Thesis

The paper presents Llama 3 as a family of foundation models whose largest
reported member was trained across up to 16,384 H100 GPUs. Its training-systems
sections make topology, parallelism, numerical policy, checkpoint I/O, failure
denominators, and effective training time visible. This is a useful large-run
case, not an independent audit or a recipe that proves faithful execution.

## Mechanisms

- Four-dimensional tensor, pipeline, context, and fully sharded data
  parallelism arranged against network topology (Section 3.3.2).
- Explicit BF16/FP32 numerical choices used after cross-topology loss
  comparisons exposed numerical stability defects (Section 3.3.2).
- Distributed storage and per-GPU checkpoint shards used for debugging and
  recovery, with checkpoint cadence treated as lost-work control (Section
  3.3.1).
- A reliability denominator covering planned and unexpected interruptions over
  a stated 54-day window, plus effective training time and manual-intervention
  counts (Section 3.3.4 and Table 5).

## Evidence

The reviewed paper reports 38--43% BF16 model-FLOPs utilization across three
configurations, 466 interruptions in the 54-day snapshot, and more than 90%
effective training time. Those are provider-reported results and were not
reproduced. The paper supports the need to record topology, numerical policy,
checkpoint behavior, interruption denominators, and recovery burden; it does
not disclose enough retained state or replay evidence to establish exact resume
equivalence.

## Failure Modes

- Treating model scale as evidence that the intended training process executed
  faithfully.
- Collapsing pre-trained, post-trained, safety, and unreleased multimodal
  artifacts into one checkpoint identity.
- Importing source-reported evaluations as local benchmark evidence.
- Treating effective training time, model-FLOPs utilization, or eventual
  convergence as proof that no silent drift occurred.
- Assuming a recovered run is trajectory-equivalent when exact data cursor,
  RNG, scheduler, scaler, and communication state are not demonstrated.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- Existing boundary owners: `replaceable-cognitive-substrates-beyond-transformer-monoculture`,
  `policy-optimization-and-learning-from-feedback`,
  `data-engines-continual-learning-and-unlearning`, and
  `ai-supply-chain-integrity-and-lifecycle-provenance`

## Claims To Add Or Update

- Use the case to require topology-complete run manifests, numerical-policy
  identity, failure denominators, checkpoint receipts, and effective-time
  accounting.
- Keep provider results and recovery claims source-scoped; do not infer exact
  resume, independent qualification, or local performance.

## Open Questions

- What state beyond model and optimizer shards is required to resume without
  silent drift?
- How are checkpoint-family denominators and qualification boundaries recorded?
