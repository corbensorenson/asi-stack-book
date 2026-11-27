# Recursive Self-Editing: LLMs Program Their Own Weight Edits for Self-Improvement

| Field | Value |
|---|---|
| Source ID | `ext_selfwrite_2026` |
| Publication | Zhang and Li (2026). [Primary source](https://arxiv.org/abs/2611.29513v1) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2611.29513v1) |

## Thesis

Test solver and editor performance in separate comparisons.

## Mechanisms

The current checkpoint writes a low-rank change. An external scoring rule selects an update for the next generation.

## Evidence

Table 2 reports four accepted updates across five generations and a gain of 1.45 percentage points in average per-sample accuracy on 500 held-out math problems.

## Failure Modes

One task family, a reused selection set and retained search history limit attribution to improved editing ability.

## Book Chapters Supported

- `recursive-self-improvement-boundaries`

## Claims To Add Or Update

Use this source to frame the worked comparison in [recursive-self-improvement-boundaries](../../chapters/recursive-self-improvement-boundaries.qmd). The chapter core retains argument-level support.

## Open Questions

Can the successor improve a fresh checkpoint more than the original editor given identical records and compute?
