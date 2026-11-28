## SC1

Pooling returned `CONTRADICT`, graded `unsupported`. Requiring agreement returned `HOLD`, graded `held`. The chosen abstract contained no human-annotated evidence for this claim under the frozen rationale rule. Reciting the abstract would reproduce the model's source text without establishing the contradiction as scientific proof. The benchmark result is scoped to one held-out claim and its selected abstract. [Claim 1 triage row](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release--case-1-triage) · [Case record](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/?node=evidence_case%3Ascifact-release--1-triage)

The case ID is `evidence_case:scifact-release--1-triage` and its pinned result locator is `/cases/0`. [Pinned result file](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/6e782c3b914451609f9f73bd063071e70bb440dc/experiments/scifact_citation_check/results.json)

## SC2

Pooling retained the annotated contradiction and returned `CONTRADICT`, graded `contains`. Agreement returned `HOLD`. Pooling cited sentence 4, which a human annotated, together with sentence 0. The permissive grade gives credit when the selection includes the complete annotated rationale alongside an extra sentence. An exact match requires the annotated rationale alone, so the extra sentence costs exact-match credit in this case. [Claim 51 triage row](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release--case-51-triage) · [Case record](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/?node=evidence_case%3Ascifact-release--51-triage)

The case ID is `evidence_case:scifact-release--51-triage` and its pinned result locator is `/cases/8`. [Pinned result file](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/6e782c3b914451609f9f73bd063071e70bb440dc/experiments/scifact_citation_check/results.json)

## SC3

**38 of 65** claims were certifiable in principle. The baseline returned a paper capable of earning credit for **12 of those 38** claims, and its selected sentence pair covered the human highlights in **7 of those 12**. Only four of the seven also received the annotated verdict, yielding four justified releases across all 65. The retrospective ceiling assumes a perfect ranker and verifier within the fixed eligible catalog, human annotations, and two-sentence budget. Twenty claims lacked eligible papers with human citation evidence, and seven more had highlights that exceeded the budget. The ceiling leaves the merits of unjudged papers, evidence outside the catalog, and credit under a longer citation budget unresolved. [Retrospective scoring ceiling, record `evidence_passage:scifact-scoring-ceiling`](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#citation-scoring-ceiling)

## SC4

Under the publication policy, pooling held **299 of 299** claims and agreement held **299 of 299**. In each arm, **187 held claims** had human-annotated evidence. Both variants released zero claims, so the result gives no basis for unattended publication under either policy. Holds included claims with annotated evidence, and the study left human review time unmeasured. The result is scoped to the local reserved split and the frozen policies. [Reserved-claims run, record `study_run:scifact-release`](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release)

The book revision is `d5d8c2f7c11985af1a7f9a4393f0771745610639`. For SC1, SC2, and SC4, the run's evidence revision is `6e782c3b914451609f9f73bd063071e70bb440dc` and its result SHA-256 is `6b2bc735ddb6b823b08ed5afe38ed6dbd9a5307b95ca52fa44e248640bb575d6`. [Run citation](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-scientific-citation.html#run-scifact-release)
