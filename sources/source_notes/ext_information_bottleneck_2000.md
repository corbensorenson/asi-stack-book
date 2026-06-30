# Source Note: The information bottleneck method

| Field | Value |
|---|---|
| Source ID | `ext_information_bottleneck_2000` |
| Source title | The information bottleneck method |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:physics/0004057, https://arxiv.org/abs/physics/0004057 |
| Citation label | Tishby et al. (2000), Information Bottleneck |
| Published / updated | 2000-04-24 / 2000-04-24 |
| DOI | 10.48550/arXiv.physics/0004057 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the representation-compression literature queue; no information-bottleneck experiment or derivation is imported into this repository. |

## Thesis

The information bottleneck method belongs in the representation and compression chapters as an external reference for compressing a variable while preserving relevance to another variable. It gives the ASI Stack a precise comparison point for separating smaller representations from useful representations.

## Mechanisms

- Represent an observed variable through a compressed bottleneck variable.
- Preserve information that remains relevant to a target variable.
- Frame compression as a tradeoff between retained relevance and reduced representation burden.
- Use information-theoretic quantities to reason about the compression objective.

## Evidence

- The source provides the method and information-theoretic framing in its own scope.
- This repository has not derived an ASI Stack information-bottleneck objective, run an experiment, or measured utility preservation.
- Use the source as external representation-compression vocabulary, not as evidence for local semantic representation quality.

## Failure Modes

- Compression objectives can preserve the wrong target variable.
- Relevance can be underspecified when downstream authority, safety, or provenance obligations matter.
- A smaller representation can appear efficient while increasing verification burden.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)

## Claims To Add Or Update

- Use this note to frame compression as a relevance-preservation problem rather than a size-only target.
- Do not claim any local information-bottleneck measurement, derivation, or representation adequacy.
- Keep support state at `argument` until local metrics and acceptance tests exist.

## Open Questions

- Which ASI Stack records should declare the target variable that compression must preserve?
- How should residual escrow capture information lost by a bottleneck?
- Can context adequacy tests estimate relevance loss without overclaiming information-theoretic proof?
