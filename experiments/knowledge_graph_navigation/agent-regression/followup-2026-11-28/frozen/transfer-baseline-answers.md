## TR1

In the `b23-descriptive-expanded-forward` cell, the query-aware routine arm verified `roll → flip → left` after 72 proposals and 1,296 executed steps. The query-aware whole-program arm exhausted its screening budget at 76 proposals and 1,432 executed steps. Both had a cap of 1,450 expanded execution steps and used the forward order under the original handle-depth queue. The whole-program arm’s exhaustion establishes only that it found no verified solution within that budget and queue order. The expanded-work cap excluded indexing and queue costs. [Exact case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-factorial--case-b23-descriptive-expanded-forward) · [Run and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-factorial)

Case record `evidence_case:transfer-factorial--b23-descriptive-expanded-forward`. Evidence revision `e9ee7d0f7e6f58294de860149d0bbd1c8b5bf0c9`, result SHA-256 `f4d9e6dce8a433c3cf660b566a0d3546f0951c51dc5bd0f75c6c8b00793cdc89`.

## TR2

In the `b24-descriptive-proposals-both-reversed` cell, the query-aware whole-program arm verified `odd → roll → flip → right` under handle depth after 88 proposals and 1,976 executed steps. Under expanded primitive length, the same arm exhausted the cap at 96 proposals and 1,776 executed steps without verifying. Both schedules had a 96-proposal cap, with the same inputs, library, verifier and reversed primitive and library ordering. The runs matched on proposals allowed, and their executed work differed. This is a scheduler effect in one authored five-bit task and condition. The audit reuses 16 tasks across 256 cells, and its result is exploratory for unseen families. [Exact case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit--case-b24-descriptive-proposals-both-reversed) · [Run and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit)

Case record `evidence_case:transfer-scheduler-audit--b24-descriptive-proposals-both-reversed`. Evidence revision `420775ef7b7b2db2112f3949ab63aa0ed572254d`, result SHA-256 `ae3da5ac97370c34de883a0c2469e63572807ee3a8e1f04547154d75869d61a8`.

## TR3

No library verified 5 of 12 tasks, ordinary retrieval verified 8 of 12, and extracted routines verified 5 of 12. All three arms exhausted their budgets on all three out-of-family cases. The sample was 12 fixed, authored four-bit transformations with disjoint fixture identities, lineages and full target vectors. Each arm shared the breadth-first enumerator, eight visible examples per task, a 96-proposal cap per task and an independent full-domain checker. The result applies to that sample and bounded probe. [Original pilot, result and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-pilot)

Run record `study_run:transfer-pilot`. Evidence revision `ba85f30ebd59cbbce91bdd2e30240e18f8c23474`, result SHA-256 `56a03a24fb560b4842f212da6554680b3e356eecb5f76fc68683dd3d2b05829e`.

## TR4

For the external SyGuS permutation task `hd-19`, all three library conditions (empty, whole programs and extracted routines) hit the 12,000-proposal cap under both handle size and expanded size. Each of the six runs recorded zero universal checks and verified no program. This is bounded search exhaustion under the tested operator subset, library history, semantic pruning and budgets. It leaves open whether a legal program exists. [Handle-size row](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-handles) · [Expanded-size row](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-expanded) · [Run and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer)

Case records `evidence_case:sygus-external-transfer--hd-19-handles` and `evidence_case:sygus-external-transfer--hd-19-expanded`. Evidence revision `7c34af73b33448608aed888f74538c21cc1dec44`, result SHA-256 `d684de246308863cc317846a528e0ad6fa82847687250bfe743a3a1e79c38bc9`.

Book revision for all passages `d5d8c2f7c11985af1a7f9a4393f0771745610639`.
