# Do We Really Need an LLM for Weight-Space Programming? A Deterministic Forward-Only Paradigm and Its Capability Boundaries

| Field | Value |
|---|---|
| Source ID | `ext_fwsp_2026` |
| Publication | Yao (2026). [Primary source](https://arxiv.org/abs/2611.34612v1) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2611.34612v1) |

## Thesis

Include a fixed router when the editing operators are already known.

## Mechanisms

A fixed rule selects from four edit operators using measurements of the target network.

## Evidence

Table 1(b) gives 15/18 exact dispatches for deterministic routing and 6/18 for the 27B tool router with access to the same operators.

## Failure Modes

This is operator selection on a bounded fault suite. Success on other editing tasks needs separate evidence.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir`

## Claims To Add Or Update

Use this source to frame the worked comparison in [cognitive-compilation-and-semantic-ir](../../chapters/cognitive-compilation-and-semantic-ir.qmd). The chapter core retains argument-level support.

## Open Questions

Does an LLM discover an effective operator when the fixed library cannot express the repair?
