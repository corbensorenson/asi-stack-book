# Source Note: Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context

| Field | Value |
|---|---|
| Source ID | `ext_transformer_xl_2019` |
| Source title | Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:1901.02860, https://arxiv.org/abs/1901.02860 |
| Citation label | Dai et al. (2019), Transformer-XL |
| Published / updated | 2019-01-09 / 2019-06-02 |
| DOI | 10.48550/arXiv.1901.02860 |
| Ingestion basis | Public arXiv abstract and metadata inspected for cyclic-memory external positioning; paper not vendored into this repository and no model or benchmark reproduced. |

## Thesis

Transformer-XL is a direct external comparator for recurrent long-context language modeling. It gives the Coil Attention chapter an established baseline family for segment-level recurrence and positional treatment without supporting any local retrieval-quality, reasoning-quality, speed, or long-context result.

## Mechanisms

- Add segment-level recurrence to let hidden states from previous segments inform later segments.
- Use a positional encoding scheme designed to preserve temporal coherence across reused memory.
- Compare long-dependency language modeling against fixed-context Transformer baselines.
- Separate recurrent memory structure from task-specific evidence about useful retrieval.

## Evidence

- The source reports language-modeling, long-dependency, and evaluation-speed results under its own experimental setup.
- This repository has not run Transformer-XL, reproduced its datasets, or checked its reported performance.
- Use this source as a comparator for recurrence and memory baselines, not as evidence that Coil Attention improves memory or reasoning.

## Failure Modes

- Recurrent state can be mistaken for governed memory authority.
- Longer dependency capture does not imply a task has adequate context or verified source grounding.
- Reported speed and perplexity results do not transfer to cyclic-memory contracts without local tests.
- Segment recurrence does not by itself solve stale reads, aliasing, or authority-boundary problems.

## Book Chapters Supported

- `coil-attention-cyclic-memory-and-recurrence-contracts` (Coil Attention, Cyclic Memory, and Recurrence Contracts)

## Claims To Add Or Update

- Use Transformer-XL as a source-noted external baseline for recurrent Transformer memory.
- State that Coil memory contracts add governance and structural non-claim boundaries rather than replacing empirical recurrence baselines.
- Keep retrieval quality, reasoning quality, speed, and long-context support at `argument` until local workload evidence exists.

## Open Questions

- Which recurrence trace should become the first ASI Stack negative-control fixture?
- Should a future cyclic-memory harness compare slot-plus-winding traces against a Transformer-XL-style recurrence baseline?
- What record fields are needed to preserve authority and freshness when recurrent state crosses segment boundaries?
