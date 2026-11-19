# Where Do the Joules Go? Diagnosing Inference Energy Consumption

Jae-Won Chung, Ruofan Wu, Jeff J. Ma, Mosharaf Chowdhury. [Primary paper, arXiv 2601.22076v2](https://arxiv.org/html/2601.22076v2).

## Mechanism and evidence

Meter GPU energy per request under the actual output-length and batching policy.

At batch size 128 the authors report 0.209 and 0.312 GPU joules per token for conversation and problem solving. Their per-response figures are 95 and 2,192 GPU joules.

## Reviewed passage and limits

Table 1, Qwen3-32B on one B200. The tasks differ in output length and maximum feasible batch size. GPU energy excludes other facility loads and cannot by itself determine emissions.

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints`
