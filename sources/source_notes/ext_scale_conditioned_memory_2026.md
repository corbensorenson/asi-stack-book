# When Stored Evidence Stops Being Usable: Scale-Conditioned Evaluation of Agent Memory

| Field | Value |
|---|---|
| Source ID | `ext_scale_conditioned_memory_2026` |

Shao et al. (2026). [Primary publication](https://arxiv.org/html/2605.07313v2).

## Thesis

An unchanged fact can become harder to recover as irrelevant history grows.

## Mechanisms

Hold relevant evidence fixed while growing the surrounding history. Count wrong answers inside the call allowance separately from attempts exceeding it.

## Evidence

On LongMemEval the reported decline for HippoRAG was 16–20 percentage points in correct answers within two retrieval calls as irrelevant sessions accumulated.

## Failure Modes

Sections 3–5 and Appendix A.9. The authors scored completed trajectories against a call budget. Enforcing a hard stop changes the interaction and requires a separate evaluation.

## Book Chapters Supported

- `virtual-context-abi` — [Can the worker still find the correction?](https://corbensorenson.github.io/asi-stack-book/chapters/virtual-context-abi.html#can-the-worker-still-find-the-correction)

## Claims To Add Or Update

Include retrieval calls and completion within budget in a memory comparison.

## Open Questions

What changes if the two-call budget is enforced during execution?
