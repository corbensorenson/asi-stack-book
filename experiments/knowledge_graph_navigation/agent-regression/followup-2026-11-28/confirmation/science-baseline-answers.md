## CS1

Both policies use the same two predictions from a single frozen MiniLM NLI cross-encoder. Pass A sees the claim paired with the title, the selected citation sentences, and their immediate neighbors. Pass B sees the claim paired with only the exact citation sentences. Each policy used **598 readings** on the 299 reserved claims, including holds. Agreement applies a release gate to those shared predictions. The two passes share model errors, so agreement adds no independent-model evidence. On claim 51, pooling released CONTRADICT and agreement held. [Pinned protocol, “What both policies see”](https://github.com/corbensorenson/asi-stack-book/blob/6e782c3b914451609f9f73bd063071e70bb440dc/experiments/scifact_citation_check/protocol.md#what-both-policies-see) · [Reserved run](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release) · [Claim 51 paired case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release--case-51-triage)

Record `evidence_case:scifact-release--51-triage`, raw result pointer `/cases/8`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `6e782c3b914451609f9f73bd063071e70bb440dc`. Result SHA-256 `6b2bc735ddb6b823b08ed5afe38ed6dbd9a5307b95ca52fa44e248640bb575d6`.

## CS2

**Keep pooling as the experimental reference.** Agreement minus pooling was **+1.67 triage utility per 100 claims**, with a **95% paired bootstrap interval of −2.36 to +5.77**. The frozen rule requires the lower limit to exceed zero and agreement to hold at most half the reserved intake. The lower limit was below zero, and agreement held 247/299 claims (82.6%). Pooling also exceeded the budget with 212/299 holds. The publication policies held all 299 claims. These results concern the reserved labeled SciFact split and the study’s annotation-based scoring. [Pinned protocol, “Freeze and adjudicate”](https://github.com/corbensorenson/asi-stack-book/blob/6e782c3b914451609f9f73bd063071e70bb440dc/experiments/scifact_citation_check/protocol.md#freeze-and-adjudicate) · [Reserved run, “Result” and “Disposition”](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release)

Record `study_run:scifact-release`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `6e782c3b914451609f9f73bd063071e70bb440dc`. Result SHA-256 `6b2bc735ddb6b823b08ed5afe38ed6dbd9a5307b95ca52fa44e248640bb575d6`.

## CS3

On 213 paired SciFact-Open claims, selecting among three papers reduced holds from **140 to 108** (32 fewer) and increased actual input tokens from **61,267 to 185,582** (124,315 more, about 3.03×). The study kept the first-paper reference. A deployment cost estimate would need measured end-to-end wall time, energy and human labor, including review work, under the intended serving conditions and the applicable compute, energy and labor rates. The run reports those resource quantities as unmeasured. [Three-paper run, “213 paired claims,” “Scope and limits,” and “Disposition”](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-three-paper-selection)

Record `study_run:three-paper-selection`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `c965253fceea696df439dbd60bf8fbe54220d725`. Result SHA-256 `cdc7dcdc97f0db428cdede74e1779732309f1d2d8fe92ca9457a45aad1e1970d`.

## CS4

The second annotated paper is **52095986**, with zero-based highlight index **5** and a CONTRADICT annotation. The alternate document ranker returned paper **34256713**, and its selected sentences [1, 2] elicited a NEUTRAL prediction that the policy held. The paper has no benchmark judgment. A model prediction on those selected sentences establishes the release outcome under this policy, while the scientific relevance of the paper remains unadjudicated. [Claim 833, “Inspect papers and annotation” and paired outcomes](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-citation-retrieval.html#run-fresh-citation-retrieval--case-833)

Record `evidence_case:fresh-citation-retrieval--833`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`.
