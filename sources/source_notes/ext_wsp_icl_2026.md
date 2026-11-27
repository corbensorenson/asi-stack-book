# Weight-Space Programming Writes In-Context Learning and Matches Fine-Tuning in Language Models

| Field | Value |
|---|---|
| Source ID | `ext_wsp_icl_2026` |
| Publication | Skianis and Likas (2026). [Primary source](https://arxiv.org/abs/2611.26841v2) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2611.26841v2) |

## Thesis

Test an ordinary prompt and a learned adapter on the same examples.

## Mechanisms

An edit can encode a residual-stream shift associated with examples in the prompt.

## Evidence

The six-task comparison includes few-shot prompting and fine-tuning on matched examples. Changes in wording weakened edited performance.

## Failure Modes

Prompt sensitivity and unfinished editor runs affect the comparison. A small perplexity change cannot establish retention on every task.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir`

## Claims To Add Or Update

Use this source to frame the worked comparison in [cognitive-compilation-and-semantic-ir](../../chapters/cognitive-compilation-and-semantic-ir.qmd). The chapter core retains argument-level support.

## Open Questions

Can a cheaper prompt meet the same quality floor on paraphrases?
