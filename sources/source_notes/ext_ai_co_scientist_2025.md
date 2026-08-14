# Source Note: Towards an AI Co-Scientist

| Field | Value |
|---|---|
| Source ID | `ext_ai_co_scientist_2025` |
| Source title | Towards an AI co-scientist |
| Ingestion date | 2026-08-13 |
| Source version / URL | arXiv record, https://arxiv.org/abs/2502.18864; official Google Research overview, https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/ |
| Citation label | Gottweis et al. (2025), Towards an AI co-scientist |
| Published / updated | 2025-02-26 / 2025-03-11 |
| Review state | Passage-bounded preprint and provider-report source for hypothesis generation and ranking; no source-reported expert or laboratory result is local evidence. |
| Ingestion basis | Official arXiv metadata and abstract plus the authors' Google Research overview of architecture, expert evaluation, laboratory cases, and stated limitations. The full experimental package was not reproduced locally. |

## Thesis

The proposed AI co-scientist uses specialized agents and additional inference
compute to generate, critique, rank, evolve, and synthesize research hypotheses.
It is a useful comparator for the proposal side of science, but its internal
ranking and expert preference signals must not be mistaken for experimental
confirmation.

## Mechanisms

- A supervisor coordinates Generation, Reflection, Ranking, Evolution,
  Proximity, and Meta-review agents.
- Pairwise comparisons and an Elo-style process rank candidate hypotheses.
- Additional test-time compute expands and iterates the hypothesis search.
- Expert review and selected laboratory cases provide downstream appraisal.

## Evidence

The authors report expert studies across 15 research goals, a smaller shared
human-evaluation subset, and biomedical cases that include laboratory
validation or rediscovery. The provider overview explicitly identifies limits
in literature review, factuality, external cross-checking, auto-evaluation, and
expert-sample size. These provider-reported results have not been independently
reproduced here. Elo rank, expert preference, and a selected laboratory case
remain different evidence objects.

## Failure Modes

- Treating self-ranking or debate among related agents as independent review.
- Publishing only the winning hypothesis while hiding the generated population,
  pruning decisions, compute allocation, and abandoned alternatives.
- Conflating expert interest or preference with causal or experimental support.
- Allowing a shared model family to create evaluator monoculture.
- Generalizing selected biomedical examples to scientific competence.

## Book Chapters Supported

- `scientific-discovery-and-experimental-governance`
- Adjacent boundary owners: `governed-deliberation-and-test-time-scaling`,
  `multi-agent-dynamics-collective-intelligence-and-systemic-risk`, and
  `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Record the full hypothesis population, ranking process, model dependencies,
  test-time compute, pruning, and human selection before reporting a winner.
- Classify internal ranking, expert appraisal, and experimental confirmation as
  separate evidence stages.
- Require independently qualified evaluation before a model-generated proposal
  can inherit a discovery claim.

## Open Questions

- How sensitive are rankings to model family, prompt, debate structure, and Elo
  initialization?
- What fraction of generated alternatives receive expert or experimental review?
- Which claims survive independent laboratories and non-provider evaluators?
