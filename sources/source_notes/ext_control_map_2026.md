# Beyond Update Counts: A Control Map for Evaluating Test-Time Model Updates

Zhao et al. (2026). [Primary publication](https://arxiv.org/html/2610.36109v1).

## Mechanism and evidence

Record the ordered commits visible to each answer. Probe immediate acquisition, later retention and collateral changes independently.

At one 760M checkpoint, accuracy across 24 equal-count update schedules ranged from 19.7% to 34.2%. In a separate comparison ROME retained edits at all 13 tested operating points and exceeded the specified locality tolerance at each.

## Review scope and open question

Sections 3–6. Locality depends on the test prompts and damage threshold. These model- and task-specific checks leave transfer to other settings open.

## Book Chapters Supported

- `adjudicated-persistence-and-the-adaptive-commit-boundary`
