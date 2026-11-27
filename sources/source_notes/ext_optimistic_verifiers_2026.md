# Optimistic Verifiers Get Hacked: Reward Hacking Under an Exact Process Oracle

| Field | Value |
|---|---|
| Source ID | `ext_optimistic_verifiers_2026` |

Arunkumar V, Manoranjan Gandhudi, Gangadharan G. R., Arun Prakash, S. Senthilkumar. [Primary paper, arXiv 2611.21538v1](https://arxiv.org/html/2611.21538v1).

## Thesis

Optimizing a sufficiency proxy can reward traces that disagree with the known generating process.

## Mechanisms

Track a proxy reward against an exact process oracle over the same rollouts.

## Evidence

The sufficiency proxy reached 0.940 while the exact faithfulness score dropped from 0.731 to 0.667 on 96 held-out episodes.

## Failure Modes

Sufficiency comparison and replication. Replication supported the direction of damage more consistently than its magnitude. The exact oracle depends on executable rules.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` — [A longer justification earns the wrong reward](../../chapters/policy-optimization-and-learning-from-feedback.qmd#a-longer-justification-earns-the-wrong-reward)

## Claims To Add Or Update

Follow both the optimized reward and an independently computable criterion over the same trajectories.

## Open Questions

Does the proxy retain its ranking on tasks with a different rule vocabulary?
