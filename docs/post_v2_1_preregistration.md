# Post-v2.1 Evidence Preregistration

Recorded: 2026-07-11

State: inputs frozen and outcomes unopened; final runner/code binding pending

This record translates the active roadmap into three finite programs without
claiming that any result exists. The selected 4B MLX runtime is restricted to
P1 proposal and P2 observable candidate generation. P3 uses a separately
trainable, disposable PyTorch policy workload.

## Frozen input summary

| Program | Input | Frozen scope |
|---|---|---|
| P1 | `p1/input/corpus.json` | 36 tasks, six families, 6/12/18 development/calibration/test, nine effect surfaces, preserved attack families |
| P2 | `p2/input/corpus.json` | 240 requests, 120/60/60 train/validation/test, four overlapping families, six actions with ten test requests each |
| P2 regression | `p2/input/known_harm_regression.json` | fifteen v2.1 fixed-step harms, regression-only and excluded from the new held-out split |
| P3 | `p3/input/corpus.json` | 1,600 examples across train, update, validation, test, deletion, and fixed-probe splits |
| P3 state | `p3/state_inventory.json` | 24 owned state surfaces plus explicit remote/production exclusions |

All five inputs are deterministic and content-addressed. Runtime-eligibility
prompts and task IDs are excluded from the P1/P2 corpora. P2 routers cannot see
gold action, answer key, specialist-competence, or global split statistics. P3
test, deletion, and probe splits cannot select checkpoints or hyperparameters.

## Shared decision discipline

The programs report finite-workload counts and paired effects. If uncertainty
intervals are used, the preregistered method is 10,000 paired bootstrap
resamples with seed 71011. Missing outputs, timeouts, parse failures, OOMs,
refusals, and invalid records remain denominator states. Optional stopping,
post-test threshold tuning, unregistered arms, retries, and borrowing budget
across programs are prohibited without a versioned amendment.

## Program boundaries

P1 pairs direct and governed decisions over the same model candidate and
observer. Its primary endpoints are useful release, unsafe release, and exact
rollback over the declared effect inventory. P2 separately dispositions routing
and deliberation, forces fallback/abstention/clarification coverage, and never
publishes hidden chain-of-thought. P3 prospectively selects checkpoint authority
by validation subject to a forgetting bound, inventories full state, and keeps
behavioral change, influence reduction, lineage propagation, and storage
erasure as four different claims.

## Remaining M2 blockers

The preregistration is not yet final. Exact runner, observer, and evaluator code
must be installed and content-addressed; the setup commit must be bound; and the
combined setup validator plus rejecting mutations must pass. Until then P1–P3
remain pending and no outcome execution is authorized.

## Non-claims

- Input generation is not an empirical result.
- Forced coverage does not estimate natural request prevalence.
- Synthetic repository and policy tasks do not establish production transfer.
- A state inventory does not prove runtime control of every real system.
- No support state, chapter, release, or optional format changes here.
