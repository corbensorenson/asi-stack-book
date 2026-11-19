# When Stored Evidence Stops Being Usable: Scale-Conditioned Evaluation of Agent Memory

Shao et al. (2026). [Primary publication](https://arxiv.org/html/2605.07313v2).

## Mechanism and evidence

Hold relevant evidence fixed while growing the surrounding history. Count wrong answers inside the call allowance separately from attempts exceeding it.

On LongMemEval the reported decline for HippoRAG was 16–20 percentage points in correct answers within two retrieval calls as irrelevant sessions accumulated.

## Review scope and open question

Sections 3–5 and Appendix A.9. The authors scored completed trajectories against a call budget. Enforcing a hard stop changes the interaction and requires a separate evaluation.

## Book Chapters Supported

- `virtual-context-abi`
