# The Structured Output Benchmark: A Multi-Source Benchmark for Evaluating Structured Output Quality in Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_structured_output_benchmark_2026` |

Abhinav Kumar Singh, Harsha Vardhan Khurdula, Yoeven D Khemlani, Vineet Agarwal. [Primary paper, arXiv 2604.25359v1](https://arxiv.org/html/2604.25359v1).

## Thesis

A schema-valid extraction can assign a valid value to the wrong field.

## Mechanisms

Score schema compliance and correctness against source evidence separately.

## Evidence

Best exact leaf-value accuracy across 21 models reached 83.0% on the text set and 23.7% on the audio-derived set.

## Failure Modes

Source-normalized evaluation and exact leaf-value metric. All inputs were text-normalized. Dataset and context differences limit comparisons across source modalities.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir` — [A valid field can hold the wrong limit](../../chapters/cognitive-compilation-and-semantic-ir.qmd#a-valid-field-can-hold-the-wrong-limit)

## Claims To Add Or Update

Check each consequential field against the source passage before lowering it into an action.

## Open Questions

Which incorrect but well-typed values survive the proposed target validator?
