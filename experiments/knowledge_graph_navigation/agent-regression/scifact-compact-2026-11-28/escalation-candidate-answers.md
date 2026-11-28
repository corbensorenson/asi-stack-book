## SE1

The reserved release study used the official labeled SciFact train split to develop and freeze thresholds and the official labeled dev split for reserved evaluation. It excluded dev claim 3, the dataset-card example, and every claim sharing its cited paper. It also removed training claims sharing any reserved dev citation. Research annotations were used for partitioning and scoring. The official unlabeled test was outside the study. These exclusions control overlap within the local study. The reserved split was already public, and the model’s pretraining exposure is unknown. [Pinned SciFact release protocol](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/6e782c3b914451609f9f73bd063071e70bb440dc/experiments/scifact_citation_check/protocol.md) · [Reserved release run](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release)

## SE2

For each of the top three lexical hits, the selector summed the three-class vectors from the context reading and the citation-only reading. On the summed vector, it computed `max(SUPPORT, CONTRADICT) − NEUTRAL`. The largest margin won, with ties going to the better original document rank. The selected paper’s winning label determined release or hold, with neutral held. Annotation labels entered only after selection, when scoring the verdict and citation against the benchmark. [Pinned three-paper selector protocol](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/c965253fceea696df439dbd60bf8fbe54220d725/experiments/scifact_three_papers/protocol.md) · [Three-paper selection run](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-three-paper-selection)

## SE3

The annotated paper was **18064113**, *Characterization of the adipocyte cellular lineage in vivo*, with a SUPPORT annotation and citation-provenance highlights at zero-based sentence indices 4 and 5. The TF–IDF baseline and sentence-selector-only arm returned unjudged paper **54468511**. The document-ranker-only arm and the arm that changed both stages returned unjudged paper **15432317**. All four predicted neutral and held, so no arm released a verdict. A paper in the candidate catalog could satisfy the two-sentence benchmark rule, but every tested arm returned a different paper. [SciFact-Open paired case 83](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval--case-83)

## SE4

From the repository root with retained predictions, run these commands in order.

1. `python experiments/scifact_citation_check/score.py select` chooses the operating policies using only the development rows.
2. `python experiments/scifact_citation_check/score.py evaluate` verifies the saved policy against development and scores the reserved rows.

This replays policy selection and evaluation conditional on the saved inputs. It leaves untested whether the upstream prediction pipeline would regenerate the same retrievals, citations, and model probabilities. [Pinned SciFact release protocol](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/6e782c3b914451609f9f73bd063071e70bb440dc/experiments/scifact_citation_check/protocol.md)
