# Source Note: Scaling and evaluating sparse autoencoders

| Field | Value |
|---|---|
| Source ID | `ext_scaling_sparse_autoencoders_2024` |
| Source title | Scaling and evaluating sparse autoencoders |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2406.04093, https://arxiv.org/abs/2406.04093 |
| Citation label | Gao et al. (2024), Scaling and evaluating sparse autoencoders |
| Published / updated | 2024-06-06 / 2024-06-06 |
| DOI | 10.48550/arXiv.2406.04093 |
| Ingestion basis | Primary arXiv abstract, methods, scaling, evaluation, and stated metric boundaries inspected; released code and autoencoders were not run locally. |

## Thesis

Sparse autoencoders can be scaled to large latent dictionaries, but
reconstruction, sparsity, dead features, explainability, and downstream-effect
metrics remain separate objectives. The paper makes the gap between feature
extraction and trustworthy semantic or causal interpretation concrete.

## Mechanisms

- Use TopK sparsity to control active latent count directly.
- Scale autoencoder width and training compute while measuring reconstruction.
- Reduce dead latents through initialization and auxiliary-loss choices.
- Evaluate hypothesized-feature recovery, activation explainability, and
  downstream-effect sparsity rather than reconstruction alone.

## Evidence

The paper reports scaling behavior through a 16-million-latent GPT-4
autoencoder and releases tools for open models. The repository has not
reproduced an SAE or any reported result.

## Failure Modes

- Low reconstruction loss can coexist with poor semantic usefulness.
- Dead, split, duplicated, or polysemantic latents frustrate interpretation.
- Automated labels can overstate precision or recall.
- Feature steering can have distributed off-target effects.

## Book Chapters Supported

- Proposed: `white-box-evidence-interpretability-and-activation-governance`
- Existing boundary owner: `evidence-states-and-claim-discipline`

## Claims To Add Or Update

- Require a metric bundle rather than a single interpretability score.
- Track feature identity and stability across checkpoints and contexts.
- Keep feature discovery, causal validation, intervention, and release authority
  as distinct states.

## Open Questions

- How stable must a feature be before it can enter an activation policy?
- What matched behavioral controls detect off-target steering?
- How should replacement, deletion, or rollback migrate feature identities?
