# Beyond Update Counts: A Control Map for Evaluating Test-Time Model Updates

| Field | Value |
|---|---|
| Source ID | `ext_control_map_2026` |

Zhao et al. (2026). [Primary publication](https://arxiv.org/html/2610.36109v1).

## Thesis

Equal numbers of updates can leave a model in different behavioral states.

## Mechanisms

Record the ordered commits visible to each answer. Probe immediate acquisition, later retention and collateral changes independently.

## Evidence

At one 760M checkpoint, accuracy across 24 equal-count update schedules ranged from 19.7% to 34.2%. In a separate comparison ROME retained edits at all 13 tested operating points and exceeded the specified locality tolerance at each.

## Failure Modes

Sections 3–6. Locality depends on the test prompts and damage threshold. These model- and task-specific checks leave transfer to other settings open.

## Book Chapters Supported

- `adjudicated-persistence-and-the-adaptive-commit-boundary` — [Which edits reached this answer?](../../chapters/adjudicated-persistence-and-the-adaptive-commit-boundary.qmd#which-edits-reached-this-answer)

## Claims To Add Or Update

Retain update order when evaluating a changed model and test collateral behavior as well as the requested acquisition.

## Open Questions

Which schedule preserves the edit after unrelated later updates at an acceptable locality cost?
