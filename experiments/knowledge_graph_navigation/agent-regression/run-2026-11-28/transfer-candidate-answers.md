## TR1

In the authored b23 board-routing cell with a descriptive query and forward order, the query-aware routine verified after **72 proposals and 1,296 executed steps**. The query-aware whole-program arm exhausted its screening budget after **76 proposals and 1,432 executed steps**. Both had a cap of 1,450 expanded execution steps. Exhaustion leaves solvability by the whole-program arm open beyond this capped search. [b23 descriptive expanded-work case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-factorial--case-b23-descriptive-expanded-forward)

Record `evidence_case:transfer-factorial--b23-descriptive-expanded-forward`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `e9ee7d0f7e6f58294de860149d0bbd1c8b5bf0c9`, result SHA-256 `f4d9e6dce8a433c3cf660b566a0d3546f0951c51dc5bd0f75c6c8b00793cdc89`, result pointer `/cases/36`.

## TR2

With both queue orders reversed, the query-aware whole-program arm verified under **handle depth at 88 proposals and 1,976 executed steps**. Under **expanded length it exhausted the budget at 96 proposals and 1,776 executed steps**. The paired test used the same library, descriptive query, and 96-proposal cap on one authored b24 board-routing task. The difference shows sensitivity to queue priority in that case. Executed work differed between schedules, and the test does not establish a ranking for other programs. [b24 both-reversed scheduler case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit--case-b24-descriptive-proposals-both-reversed)

Record `evidence_case:transfer-scheduler-audit--b24-descriptive-proposals-both-reversed`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `420775ef7b7b2db2112f3949ab63aa0ed572254d`, result SHA-256 `ae3da5ac97370c34de883a0c2469e63572807ee3a8e1f04547154d75869d61a8`, result pointer `/cases/51`.

## TR3

Of 12 later tasks, **no library verified 5**, **ordinary retrieval verified 8**, and **extracted routines verified 5**. All three arms exhausted their budgets on all **three out-of-family tasks**. The sample comprised fixed, authored four-bit transformations with disjoint fixture identities, lineages, and full target vectors. Each arm used the same breadth-first enumerator, eight visible examples and a 96-proposal cap per task, with an independent full-domain checker. The measured advantage belongs to this pilot sample and search budget. [Original four-bit pilot](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-pilot)

Record `study_run:transfer-pilot`. Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `ba85f30ebd59cbbce91bdd2e30240e18f8c23474`, result SHA-256 `56a03a24fb560b4842f212da6554680b3e356eecb5f76fc68683dd3d2b05829e`.

## TR4

For the external SyGuS permutation task hd-19, the empty library, whole programs, and extracted routines **all hit 12,000 proposals with zero universal checks under each schedule**. No arm verified under either handle size or expanded size. The six capped searches used the study's operator subset, libraries, and semantic pruning. Whether a legal program exists remains open. [Handle-size case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-handles) · [Expanded-size case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-expanded)

Records `evidence_case:sygus-external-transfer--hd-19-handles` (result pointers `/cases/60`, `/cases/62`, `/cases/64`) and `evidence_case:sygus-external-transfer--hd-19-expanded` (result pointers `/cases/61`, `/cases/63`, `/cases/65`). Book revision `552fb37f379249f6a726b98cbbbd06384710c55c`. Evidence revision `7c34af73b33448608aed888f74538c21cc1dec44`, result SHA-256 `d684de246308863cc317846a528e0ad6fa82847687250bfe743a3a1e79c38bc9`.
