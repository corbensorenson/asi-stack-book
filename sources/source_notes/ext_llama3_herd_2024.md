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
| Review state | Preliminary second-tranche audit note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official arXiv metadata and abstract inspected. The paper body, code, model artifacts, training logs, checkpoints, and evaluations were not ingested or run locally. |

## Thesis

The reviewed abstract presents Llama 3 as a family of foundation models that
includes a 405-billion-parameter dense Transformer, supports a context window
up to 128K tokens, and has released pre-trained and post-trained versions. It
supplies a preliminary scale and artifact-family comparator for the proposed
training owner, but the abstract alone does not support claims about
distributed-run integrity, optimizer state, fault recovery, exact resume, or
checkpoint selection.

## Mechanisms

- A family of language models rather than one undifferentiated checkpoint.
- A largest described member with 405 billion parameters and dense Transformer
  architecture.
- Separate pre-trained and post-trained released artifacts.
- Extensive source-reported evaluation and a compositional multimodal research
  route, neither of which was inspected beyond the abstract.

## Evidence

The abstract reports multilingual, coding, reasoning, tool-use, evaluation,
release, and multimodal-extension results. None has been reproduced here. The
reviewed basis contains no passage-level evidence for the proposed chapter's
training-run transaction, distributed topology, numerical-state, anomaly,
resume, or qualification contracts.

## Failure Modes

- Treating model scale as evidence that the intended training process executed
  faithfully.
- Collapsing pre-trained, post-trained, safety, and unreleased multimodal
  artifacts into one checkpoint identity.
- Importing source-reported evaluations as local benchmark evidence.
- Filling training-run details from memory or secondary summaries before a
  bounded paper-body passage review.

## Book Chapters Supported

- Proposed: `governed-model-training-distributed-optimization-and-scaling`
- Existing boundary owners: `replaceable-cognitive-substrates-beyond-transformer-monoculture`,
  `policy-optimization-and-learning-from-feedback`,
  `data-engines-continual-learning-and-unlearning`, and
  `ai-supply-chain-integrity-and-lifecycle-provenance`

## Claims To Add Or Update

- Retain Llama 3 as a preliminary scale and artifact-family comparator.
- Require paper-body passage review before attributing a training topology,
  optimizer policy, numerical policy, recovery mechanism, or checkpoint
  selection procedure to this source.
- Do not change chapter support, manifest admission, or training evidence state
  from this abstract-only note.

## Open Questions

- Which paper passages specify distributed topology and failure handling?
- What state is required to resume a training run without silent drift?
- How are checkpoint-family denominators and qualification boundaries recorded?
