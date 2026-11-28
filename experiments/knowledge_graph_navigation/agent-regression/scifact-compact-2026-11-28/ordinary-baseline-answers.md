## SO1

On the same 299 reserved claims, requiring agreement instead of pooling raised triage holds from **212 to 247** (+35). Holds with annotated evidence rose from **121 to 151** (+30), so the other holds rose from **91 to 96** (+5). If each hold goes to review, agreement sends 35 additional claims to the queue, 30 with annotated evidence. These counts measure the size and composition of that queue. The study measured neither reviewer time nor effort per case. [Reserved SciFact run and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release)

## SO2

Across the same 65 claims, changing only document ranking from TF–IDF to BM25 produced **16 unsupported releases, 47 holds, and 20,748 input tokens**. Changing only sentence selection to coverage-weighted ranking produced **17 unsupported releases, 45 holds, and 19,725 input tokens**. Document-only therefore had one fewer unsupported release, two more holds, and 1,023 more input tokens than sentence-only. The TF–IDF baseline had 15 unsupported releases, 46 holds, and 19,669 input tokens. [Paired ranking run](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval)

Input tokens measure the aggregate size of the inputs supplied to the verifier. Each arm used one document per claim and 130 model readings, with equal call and setting ceilings. Unsupported releases and holds are decision counts. The run reports no wall-clock serving latency, so the token difference cannot establish a serving-time difference. [Retrieval protocol and scope](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#fresh-citation-retrieval)

## SO3

- **First paper:** 52 unsupported out of 73 releases (21 justified + 52 unsupported), or **71.23%**.
- **Choose among three:** 81 unsupported out of 105 releases (24 justified + 81 unsupported), or **77.14%**.

Each arm faced 213 claims. The percentages condition on release and exclude the 140 one-paper holds and 108 three-paper holds. They measure how often this benchmark's citation-provenance scoring rule failed to certify a released verdict and citation. The cohort and annotation rule provide no estimate of the prevalence of scientific errors outside the benchmark. [One-versus-three-paper run and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-three-paper-selection)

## SO4

- **12 of 15** returned an unjudged paper. Assess whether the paper supports or contradicts the claim. For example, baseline claim 1076 cited unjudged paper 29309824. [Claim 1076 decision](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval--case-1076)
- **1 of 15** returned a paper with pooled highlights. Obtain a human sentence-level rationale because the pooled highlights were model-proposed.
- **2 of 15** missed part of the human citation. Improve selection within the two-sentence budget so the citation includes the necessary highlights.

The retrospective audit holds the 65-claim cohort, eligible catalog, annotations, and two-sentence rule fixed. A citation can contain real evidence while missing benchmark credit because the paper lacks a judgment, the highlights lack human citation provenance, or the selected sentences cover only part of the required rationale. The flattened union of alternative human highlights can also reject an adequate shorter citation. The audit establishes why the benchmark withheld credit. Scientific validity in an individual case requires assessment of the evidence. [Scoring ceiling and scope](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#citation-scoring-ceiling) · [All 15 cases](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#ceiling-unsupported) · [Annotation rules](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#fresh-citation-retrieval)
