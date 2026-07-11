# Source Note: MUSE

| Field | Value |
|---|---|
| Source ID | `ext_muse_unlearning_2025` |
| Source title | MUSE: Machine Unlearning Six-Way Evaluation for Language Models |
| Ingestion date | 2026-07-11 |
| Source version / URL | ICLR 2025 proceedings; arXiv:2407.06460 |
| Citation label | Shi et al. (2025), MUSE |
| Published / updated | 2025 / 2025 |
| DOI | 10.48550/arXiv.2407.06460 |
| Ingestion basis | Primary ICLR proceedings abstract and benchmark criteria reviewed; models, corpora, and algorithms were not run. |

## Thesis

Unlearning evaluation must span memorization, privacy, retained utility, scale,
and repeated requests rather than collapse success into one forgetting score.

## Mechanisms

- Six-way evaluation over owner and deployer interests.
- Verbatim/knowledge memory and privacy-leakage probes.
- Utility, removal-scale, and sequential-sustainability measurements.

## Evidence

MUSE reports eight methods on 7B language models. P3's tiny classifier bears
only on measurement separation, not on MUSE performance or LLM unlearning.

## Failure Modes

Behavioral suppression can coexist with privacy leakage; retained utility can
collapse; repeated requests and scale can defeat apparently useful methods.

## Book Chapters Supported

- `data-engines-continual-learning-and-unlearning`
- `policy-optimization-and-learning-from-feedback`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

Keep behavioral, influence/privacy, utility, lineage, storage, scale, and
sequential-request claims separate.

## Open Questions

- Which six-way dimensions can a local stateful test observe honestly?
- How should sequential deletion invalidate descendants and caches?
