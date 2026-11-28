## TR1

In the forward-order `b23` descriptive cell, both arms ran under the 1,450-expanded-execution-step cap. The query-aware routine verified `roll → flip → left` after **72 proposals and 1,296 executed steps**. The query-aware whole-program arm exhausted its screening budget after **76 proposals and 1,432 executed steps**. That outcome establishes a bounded search miss for this arm under the original handle-depth queue. Whether that arm would find a solution with a different cap or ordering remains unresolved. [Exact case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-factorial--case-b23-descriptive-expanded-forward) · [Run scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-factorial)

Case `evidence_case:transfer-factorial--b23-descriptive-expanded-forward`. Evidence revision `e9ee7d0f7e6f58294de860149d0bbd1c8b5bf0c9`. Result SHA-256 `f4d9e6dce8a433c3cf660b566a0d3546f0951c51dc5bd0f75c6c8b00793cdc89`.

## TR2

For descriptive `b24` with both orders reversed, the query-aware whole-program arm **verified under handle depth** at **88 proposals and 1,976 executed steps**, finding `odd → roll → flip → right`. Under expanded primitive length it **exhausted the cap** at **96 proposals and 1,776 executed steps**. The replay changed queue priority while holding inputs, library, verifier, order condition and the 96-proposal cap fixed. Execution work differed, and this single authored five-bit case establishes scheduler sensitivity at that cap. The broader audit reuses 16 authored tasks across 256 cells and is exploratory for unseen families. [Exact case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit--case-b24-descriptive-proposals-both-reversed) · [Run scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit)

Case `evidence_case:transfer-scheduler-audit--b24-descriptive-proposals-both-reversed`. Evidence revision `420775ef7b7b2db2112f3949ab63aa0ed572254d`. Result SHA-256 `ae3da5ac97370c34de883a0c2469e63572807ee3a8e1f04547154d75869d61a8`.

## TR3

On the 12 authored later four-bit tasks, **no library verified 5/12, ordinary retrieval verified 8/12, and extracted routines verified 5/12**. All three arms exhausted their budgets on all three out-of-family tasks. Each search had eight visible probe examples and a 96-proposal cap per task, with an independently implemented full-domain checker for verification. The observed advantage for ordinary retrieval is scoped to this authored sample, search order and probe budget. [Original pilot and paired cases](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-pilot)

Run `study_run:transfer-pilot`. Evidence revision `ba85f30ebd59cbbce91bdd2e30240e18f8c23474`. Result SHA-256 `56a03a24fb560b4842f212da6554680b3e356eecb5f76fc68683dd3d2b05829e`.

## TR4

On the external SyGuS permutation task `hd-19`, the empty library, whole-program library and extracted-routine library each exhausted **12,000 proposals** under **both handle-size and expanded-size schedules**. All six searches produced zero universal checks and zero verifications. In library order, the primitive evaluation counts were 612,528, 836,736 and 654,552 under handle size, and 612,528, 612,528 and 612,192 under expanded size. This is a bounded miss under the tested grammar subset, pruning and proposal cap. Existence of a legal program remains unresolved by the run. [Handle-size case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-handles) · [Expanded-size case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-expanded) · [Run scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer)

Cases `evidence_case:sygus-external-transfer--hd-19-handles` and `evidence_case:sygus-external-transfer--hd-19-expanded`. Evidence revision `7c34af73b33448608aed888f74538c21cc1dec44`. Result SHA-256 `d684de246308863cc317846a528e0ad6fa82847687250bfe743a3a1e79c38bc9`.

Book revision for all citations `d5d8c2f7c11985af1a7f9a4393f0771745610639`.
