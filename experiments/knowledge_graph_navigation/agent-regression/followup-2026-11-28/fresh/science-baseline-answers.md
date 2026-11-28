## FS1

Under triage, both pooling the two readings and requiring agreement released `SUPPORT` for SciFact claim 75. The citation rationale scored **unsupported** in both arms. The retrieved paper had no annotated rationale for this claim. Both policies used the same two readings from one model, so the case shows a shared error that survived agreement and leaves cross-model error independence untested.

[SciFact claim 75 under triage](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release--case-75-triage), record `evidence_case:scifact-release--75-triage`, book revision `552fb37f379249f6a726b98cbbbd06384710c55c`, evidence revision `6e782c3b914451609f9f73bd063071e70bb440dc`, result SHA-256 `6b2bc735ddb6b823b08ed5afe38ed6dbd9a5307b95ca52fa44e248640bb575d6`, case pointer `/cases/15`.

## FS2

The alternate selector retained annotated sentence **6** and replaced annotated sentence **1** with sentence **2**, using zero-based abstract indices. Changing sentence selection alone kept the annotated paper, **5811042**, and returned `CONTRADICT` with an **unsupported** citation because the required highlights were incomplete. Changing only document ranking returned the unjudged paper **34256713**, selected sentences `[1, 2]`, and returned `NEUTRAL`, which was **held**. Baseline TF–IDF returned paper 5811042 with `[1, 6]` and a justified `CONTRADICT`. This single reserved claim shows two ways the baseline’s justified answer was lost. The frequency and aggregate effect of these losses require the paired cohort.

[SciFact-Open claim 833](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval--case-833), record `evidence_case:fresh-citation-retrieval--833`, book revision `552fb37f379249f6a726b98cbbbd06384710c55c`, evidence revision `6635c1e1b605e5fb426a44e8a47ad3a01dca1a46`, result SHA-256 `88141d1942d02989af9cb07046858abd071501c2099081df40730c2354ea6503`, case pointer `/cases/35`.

## FS3

Choosing among three papers added **29 unsupported releases** (52 to 81) and **852 model readings** (426 to 1,278) for the three additional justified releases (21 to 24). The study kept the one-paper reference on this 213-claim paired SciFact-Open workload with a two-sentence limit. Wall-clock time, energy, and human review work were unmeasured.

[Three-paper selection run](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-three-paper-selection), record `study_run:three-paper-selection`, book revision `552fb37f379249f6a726b98cbbbd06384710c55c`, evidence revision `c965253fceea696df439dbd60bf8fbe54220d725`, result SHA-256 `cdc7dcdc97f0db428cdede74e1779732309f1d2d8fe92ca9457a45aad1e1970d`.

## FS4

Across 65 paired SciFact-Open claims, baseline TF–IDF and the arm changing both stages each delivered **7 complete highlights**. The baseline delivered **4 justified answers** at **19,669 input tokens**, while the changed arm delivered **2** at **20,737 input tokens**. The baseline remained the reference for this workload. Equal totals can cover different claims, and each justified answer also requires the verifier to release the annotated verdict. Even on the same claim, complete highlights can therefore yield different decisions. The comparison used one paper and two readings per claim and scored completeness against the benchmark’s citation-provenance highlights.

[Four paired rankings on fresh citation papers](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval), record `study_run:fresh-citation-retrieval`, book revision `552fb37f379249f6a726b98cbbbd06384710c55c`, evidence revision `6635c1e1b605e5fb426a44e8a47ad3a01dca1a46`, result SHA-256 `88141d1942d02989af9cb07046858abd071501c2099081df40730c2354ea6503`. [Chapter section explaining how complete highlights and the verdict enter the score](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#fresh-citation-retrieval).
