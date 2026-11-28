## SP1

For case C3, the versioned register opened **1 record** and earned credit for the decision with supporting facts, a usable citation, and correct scope. The linked register opened **2 records**, spent them on earlier comparisons, and earned none of those three credits. Both policies **held** the operator-time claim. The linked register missed the determining verifier-labor citation and did not promote the claim. Human review time was unmeasured. This was one authored decision scored under a two-open budget. [Case C3](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-claim-review.html#run-claim-review-matched--case-c3) · [Matched study](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-claim-review.html#run-claim-review-matched)

## SP2

The live observations were version-pinned HTTP reads from jsDelivr and UNPKG. Each service returned all 12 exact reference package manifests. The client recorded statuses, redirects, received bytes, digests, and fetch timings. The offline replay masked the primary, masked both paths, or masked the primary and substituted a different lineage’s second-path manifest. With the primary masked, caller and gateway fallback each verified 12 lineages. The replay accounted for the requests each arm would use and modeled the gateway’s JSON status envelope. Its timing used captured fetch durations and did not measure gateway execution latency. The two services offered separate delivery paths to one client and shared the same npm release origin. The study did not establish independent origins or measure natural outage rates. [Distribution study](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-crossed-receiver.html#run-receiver-distribution) · [Pinned protocol](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/a3e9a06203978c6c3b9c5bbeb8d1f1acd640762f/experiments/p5_u1_governed_repository_change/public_distribution_observation/protocol.md)

The original observation is retained in `public_distribution_observation/results.json` at evidence revision `a3e9a06203978c6c3b9c5bbeb8d1f1acd640762f` (SHA-256 `2b714ba994d960a02a0c3ff049d92dfbaefc17079109778c9c4b1f2431e98a6f`). Running the observation command again would make fresh network reads and capture what the services return at the new observation time. [Pinned original result](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/a3e9a06203978c6c3b9c5bbeb8d1f1acd640762f/experiments/p5_u1_governed_repository_change/public_distribution_observation/results.json)

## SP3

Under the expanded-work cap, the counts below are verified cells out of 64 for each query condition.

| Query | Queue priority | Query-aware whole programs | Query-aware routines |
| --- | --- | ---: | ---: |
| Neutral | Handle depth | 4 | 10 |
| Neutral | Expanded primitive length | 4 | 10 |
| Descriptive | Handle depth | 4 | 16 |
| Descriptive | Expanded primitive length | 4 | 16 |

Routines verified more cells under both priorities, with a larger lead on descriptive queries. The 256 matched cells repeat conditions over 16 authored tasks. The unit for inference on new tasks is the **task lineage**. The focal pattern was seen before the pinned rerun, so the result is exploratory for unseen families. [Scheduler audit](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-forward-transfer.html#run-transfer-scheduler-audit)

## SP4

Both formats took the expected route at all 38 paired checkpoints. The local revision authority and worker shared an operator.

| Measure | Conventional memoization | Serialized handoff |
| --- | ---: | ---: |
| Specialist decisions | 10 | 10 |
| Authority and worker pipe messages | 164 | 164 |
| Pipe payload bytes | 16,816 | 16,816 |
| Local cache serialization bytes | 0 | 1,616 |

The serialized arm’s extra 1,616 bytes were written into its local cache. Pipe accounting excluded framing, work-counter collection, and startup. The study did not measure active operator time, wall time, network latency, independently operated services, production fault isolation, cache restart behavior, or concurrent changes between permission checks and effects. [Separate revision authority process study](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-verifier-rollout.html#run-verifier-process-boundary)
