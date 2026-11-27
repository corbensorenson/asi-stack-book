# RSI-Env: An Open-Ended Environment for Recursive Self-Improvement of Agents

| Field | Value |
|---|---|
| Source ID | `ext_rsi_env_2026` |
| Publication | Qu et al. (2026). [Primary source](https://arxiv.org/abs/2611.01736v1) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2611.01736v1) |

## Thesis

Compare successor control with a fixed teacher under the same feedback.

## Mechanisms

An accepted model and harness take the next turn while a host controls evaluation and versioning.

## Evidence

The experiments compare evolving agents with fixed teachers at different levels of goal specificity and feedback.

## Failure Modes

Changing the teacher, feedback and target can change the outcome. Gains on one capability can coexist with losses elsewhere.

## Book Chapters Supported

- `recursive-self-improvement-boundaries`

## Claims To Add Or Update

Use this source to frame the worked comparison in [recursive-self-improvement-boundaries](../../chapters/recursive-self-improvement-boundaries.qmd). The chapter core retains argument-level support.

## Open Questions

Does letting the successor conduct the next round outperform keeping the original teacher?
