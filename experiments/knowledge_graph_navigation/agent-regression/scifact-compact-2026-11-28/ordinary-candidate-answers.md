## SO1

Across the same 299 reserved SciFact claims, requiring agreement instead of pooling the two readings increased triage holds from 212 to 247, a net increase of 35. Holds with annotated evidence rose from 121 to 151, a net increase of 30. These counts describe the number and composition of cases routed to review in this comparison. The study did not measure reviewer effort or time. [Reserved SciFact release comparison](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release)

## SO2

On the same 65 claims, changing only document ranking yielded 16 unsupported releases, 47 holds, and 20,748 input tokens. Changing only sentence selection yielded 17 unsupported releases, 45 holds, and 19,725 input tokens. The document-only change therefore had one fewer unsupported release, two more holds, and 1,023 more input tokens. Each arm returned one paper per claim, allowed up to two citation sentences, and used 130 model readings with matched ceilings. The token counts measure the actual input supplied to the model. Serving time was unmeasured, so the counts cannot establish a latency difference. The release outcomes are scoped to the study’s candidate catalog and annotation rules. [Paired ranking comparison](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval) · [Pinned protocol](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/6635c1e1b605e5fb426a44e8a47ad3a01dca1a46/experiments/scifact_retrieval_followup/protocol.md)

## SO3

The first-paper arm had 52 unsupported releases out of 73 releases (52 unsupported + 21 justified), or **71.2%**. The choose-among-three arm had 81 unsupported releases out of 105 releases (81 unsupported + 24 justified), or **77.1%**. Each arm ran on 213 paired SciFact-Open claims. Holds are excluded from the release denominators. These shares describe how often released verdict-and-citation pairs failed the benchmark’s citation-provenance scoring rule on that cohort. They do not estimate the prevalence of scientific errors outside the benchmark. [One-versus-three-paper comparison](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-three-paper-selection)

## SO4

- **12 unjudged papers.** Judge whether each returned paper supports or refutes the claim.
- **1 paper with pooled highlights.** Obtain a human sentence-level rationale because the pooled highlights do not qualify for citation-provenance credit.
- **2 incomplete human citations.** The selected sentences missed part of the annotated rationale. These cases motivate improving sentence selection.

The retrospective audit used the original 65-claim cohort, eligible paper catalog, annotation rules, and two-sentence limit. A release can cite real evidence and still fail certification if its paper is unjudged, its highlights lack qualifying human provenance, or its citation omits highlights that the scoring rule requires. The rule combines alternative human rationales and can therefore reject an adequate shorter citation. [Retrospective scoring ceiling](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#citation-scoring-ceiling) · [Unsupported baseline cases](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#ceiling-unsupported) · [Retrieval scoring scope](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#fresh-citation-retrieval)
