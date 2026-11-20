# Beyond Compilation: Evaluating Faithful Natural-Language-to-Lean Statement Formalization

| Field | Value |
|---|---|
| Source ID | `ext_beyond_compilation_2026` |
| Publication | Ke Zhang et al. (2026). [Primary publication](https://arxiv.org/html/2606.31002v4). |

## Thesis

Use a counterexample to test the translated statement before checking the implementation binding.

## Mechanisms

Check Lean elaboration, obtain semantic judgments from two model families and calibrate the rejection decision against human review.

## Evidence

In revision 4 the tool-augmented system compiled 87.2% of 227 statements and passed both semantic judges plus compilation on 57.7%.

## Failure Modes

The dataset contains mathematics statements. Human audit found some faithful translations among the rejections.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope`

## Claims To Add Or Update

The chapter uses the paper as an external comparison in “Who has to approve the export?” and retains its existing core support state.

## Open Questions

What minimal export trace distinguishes the proposed statement from the policy owner’s intended rule?
