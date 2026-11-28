## TR1

Under the matched cap of 1,450 expanded execution steps, the query-aware routine arm verified `roll → flip → left` after 72 proposals and 1,296 executed steps. The query-aware whole-program arm exhausted its screening budget after 76 proposals and 1,432 executed steps. This was one authored board-routing case with a descriptive query and forward order. Exhaustion leaves open whether the whole-program arm could solve it with a different budget or schedule. [b23 descriptive expanded-work result](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-factorial--case-b23-descriptive-expanded-forward)

## TR2

The query-aware whole-program arm verified `odd → roll → flip → right` under handle depth after 88 proposals and 1,976 executed steps. Under expanded length it exhausted the cap at 96 proposals and 1,776 executed steps. This comparison holds the descriptive query, library, both-reversed order and 96-proposal cap fixed for one authored b24 case. The comparison shows sensitivity to queue priority under a matched proposal cap, with different amounts of executed work. [b24 both-reversed scheduler result](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit--case-b24-descriptive-proposals-both-reversed)

## TR3

No library verified 5 of 12 tasks, ordinary retrieval verified 8 of 12, and extracted routines verified 5 of 12. All three arms exhausted their budgets on all three out-of-family tasks. The sample comprised 12 fixed, authored four-bit transformations with disjoint fixture identities, lineages and full target vectors. Each arm used the same breadth-first enumerator, eight visible examples and a 96-proposal cap per task, with an independent full-domain checker. The result is limited to that sample and search setup. [Original four-bit pilot, result and scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-pilot)

## TR4

For the external SyGuS `hd-19` permutation task, the empty library, whole-program library and routine library each hit the 12,000-proposal cap under both handle size and expanded size. All six runs performed zero universal checks and verified no program. The result leaves the existence of a legal program open because the search was bounded by the tested operator subset, libraries, semantic pruning and proposal budget. [Handle-size case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-handles) · [Expanded-size case](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer--case-hd-19-expanded) · [External study scope](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-sygus-external-transfer)
