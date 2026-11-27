# What Does an LLM-Agent Leaderboard Rank Actually Compare?

| Field | Value |
|---|---|
| Source ID | `ext_agent_leaderboard_estimands_2026` |

Wei-Jung Huang. [Primary paper, arXiv 2609.07785v1](https://arxiv.org/html/2609.07785v1).

## Thesis

Agent rankings can change when the deployment mix or smallest meaningful difference changes.

## Mechanisms

Define a deployment mixture, a practical margin and an uncertainty rule before comparing releases.

## Evidence

Among 45 pairs selected from the observed SWE-bench Verified top ten, five were stable under pointwise intervals and a two-point margin. Simultaneous intervals resolved none.

## Failure Modes

Figure 2 and pairwise decision procedure. Selection of the observed top ten and the choice of interval affect inference. An unresolved difference leaves equivalence open.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` — [Would a one-point lead justify replacement?](https://corbensorenson.github.io/asi-stack-book/chapters/benchmark-ratchets-and-anti-goodhart-evidence.html#would-a-one-point-lead-justify-replacement)

## Claims To Add Or Update

Count stable pairwise decisions under the declared workload mix before using a leaderboard rank to replace an agent.

## Open Questions

Which pairs still clear the margin on a prospectively chosen task mix?
