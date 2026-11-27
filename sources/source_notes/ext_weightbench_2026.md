# WeightBench: Evaluating Language Models as Weight-Space Programmers

| Field | Value |
|---|---|
| Source ID | `ext_weightbench_2026` |
| Publication | Marasini et al. (2026). [Primary source](https://arxiv.org/abs/2611.18553v1) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2611.18553v1) |

## Thesis

Allow an editor to report that an edit is infeasible under the supplied interface.

## Mechanisms

Editors attempt weight reading, repair, construction, infeasibility recognition and data-free compression under specified access restrictions.

## Evidence

Across 42 tasks the authors find stronger results on small networks and difficulty with the LM patching and infeasibility cases.

## Failure Modes

The allowed observations and operations differ by track. An unsuccessful constrained attempt does not establish that a repair with calibration data is impossible.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir`

## Claims To Add Or Update

Use this source to frame the worked comparison in [cognitive-compilation-and-semantic-ir](../../chapters/cognitive-compilation-and-semantic-ir.qmd). The chapter core retains argument-level support.

## Open Questions

Which edits remain feasible under the same write budget if the editor can use calibration examples?
