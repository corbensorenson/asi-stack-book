# Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation

| Field | Value |
|---|---|
| Source ID | `ext_stop_2024` |
| Publication | Zelikman et al. (2024). [Primary source](https://arxiv.org/abs/2310.02304v3) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/abs/2310.02304v3) |

## Thesis

Identify the scaffolding program as the object that persists.

## Mechanisms

A program that searches over proposed code improvements can itself become the program under improvement.

## Evidence

On the tested downstream tasks the evolved scaffolding generated better programs using the same underlying model.

## Failure Modes

Model parameters stayed fixed. Results depend on the chosen utility and tasks.

## Book Chapters Supported

- `recursive-self-improvement-boundaries`

## Claims To Add Or Update

Use this source to frame the worked comparison in [recursive-self-improvement-boundaries](../../chapters/recursive-self-improvement-boundaries.qmd). The chapter core retains argument-level support.

## Open Questions

Does the changed search procedure help on a different utility under matched compute?
