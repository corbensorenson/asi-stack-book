# Tracr: Compiled Transformers as a Laboratory for Interpretability

| Field | Value |
|---|---|
| Source ID | `ext_tracr_2023` |
| Publication | Lindner et al. (2023). [Primary source](https://arxiv.org/abs/2301.05062v5) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2301.05062v5) |

## Thesis

Use a program with known behavior as a control for the compiler.

## Mechanisms

A compiler turns a restricted symbolic program into a transformer with known internal structure.

## Evidence

Sorting and parenthesis checking illustrate how to evaluate an interpretation against a known construction.

## Failure Modes

The compiler takes a program in its supported language. Arbitrary learned checkpoints lack that specification.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir`

## Claims To Add Or Update

Use this source to frame the worked comparison in [cognitive-compilation-and-semantic-ir](../../chapters/cognitive-compilation-and-semantic-ir.qmd). The chapter core retains argument-level support.

## Open Questions

What representation permits an exact check of the generated computation?
