# Where Do the Joules Go? Diagnosing Inference Energy Consumption

| Field | Value |
|---|---|
| Source ID | `ext_inference_joules_2026` |

Jae-Won Chung, Ruofan Wu, Jeff J. Ma, Mosharaf Chowdhury. [Primary paper, arXiv 2601.22076v2](https://arxiv.org/html/2601.22076v2).

## Thesis

A per-token energy average can hide the cost of a much longer answer.

## Mechanisms

Meter GPU energy per request under the actual output-length and batching policy.

## Evidence

At batch size 128 the authors report 0.209 and 0.312 GPU joules per token for conversation and problem solving. At the respective maximum batch sizes (512 and 128), Table 1 gives 95 and 2,192 GPU joules per response.

## Failure Modes

Table 1, Qwen3-32B on one B200. The tasks differ in output length and maximum feasible batch size. GPU energy excludes other facility loads and cannot by itself determine emissions.

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints` — [From a token meter to an answer bill](https://corbensorenson.github.io/asi-stack-book/chapters/physical-compute-infrastructure-energy-and-environmental-constraints.html#from-a-token-meter-to-an-answer-bill)

## Claims To Add Or Update

Report request energy beside output length, batch size and measurement boundary.

## Open Questions

Does the apparent energy advantage hold for equal useful output quality and a shared latency requirement?
