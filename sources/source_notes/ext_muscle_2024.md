# MUSCLE: A Model Update Strategy for Compatible LLM Evolution

| Field | Value |
|---|---|
| Source ID | `ext_muscle_2024` |
| Publication | Jessica Echterhoff et al. (2024). [Primary publication](https://machinelearning.apple.com/research/model-compatibility). |

## Thesis

Compare both versions on identical adjudicated cases and count previously correct cases that regress.

## Mechanisms

Train a compatibility adapter during the base-model update and evaluate downstream adapters on paired instances.

## Evidence

The compatibility adapter reduced negative flips by up to 40% for tested update and task configurations.

## Failure Modes

Instance regressions depend on the grading criterion, versions and task.

## Book Chapters Supported

- `capability-replacement-and-rollback`

## Claims To Add Or Update

The chapter uses the paper as an external comparison in “Which five cases did the upgrade break?” and retains its existing core support state.

## Open Questions

Do the old-only successes cluster in a route with a mandatory acceptance threshold?
