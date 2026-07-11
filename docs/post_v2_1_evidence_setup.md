# Post-v2.1 Executable Evidence Setup

Recorded: 2026-07-11

State: frozen against corrected setup commit
`707fc10969b04bd31e135c8a711b33e9505e0d87`; outcomes unopened

The three active empirical programs now have executable, non-overwriting local
runners. P1 and P2 use the pinned eligible Qwen3 4B MLX snapshot with local-only
loading. P3 uses a disposable deterministic PyTorch policy network. No runner
will execute unless the shared preregistration is in its final frozen state.

## Execution schedule

| Program | Order | Calls | Maximum generated tokens |
|---|---|---:|---:|
| P1 | development -> calibration -> test | 12 + 24 + 36 = 72 | 18,360 |
| P2 | validation -> test | 20 + 240 = 260 | 41,600 |
| P3 | three seeds x five arms | 0 model calls | 0 |
| **Combined** | sequential, no budget borrowing | **332** | **59,960** |

The combined ceilings remain below the registered 340 calls and 60,000
generated tokens. Every result path is create-once. There is no overwrite,
retry, service-spend, or post-freeze network option.

## Separation that actually exists

- P1 candidate tests and filesystem inventories run through
  `post_v2_1_p1_observer.py` as a subprocess separate from the MLX proposer.
- P2 answers and route choices run through `post_v2_1_p2_evaluator.py`, which
  sees evaluator-only answer keys but no router score or training interface.
- P3 maps and hashes all 24 registered state surfaces through
  `post_v2_1_p3_observer.py`, separate from training and checkpoint selection.
- P3 checkpoint authority uses validation target utility subject to the frozen
  retained-family bound; test, deletion, and probe records do not select it.

These are implementation boundaries operated inside one project. They are not
external-human, institutional, or evidence-vector independence.

## Preflight and red-team result

All three preflights passed without loading a model for outcome generation,
training a P3 arm, or opening held-out results. The combined validator checks
the exact implementation digests, amended corpus bindings, phased call counts,
token arithmetic, local-only runtime, role interfaces, overwrite/retry absence,
P2 learned-feature boundary, P3 selection boundary, and outcome absence. Ten
mutations are rejected.

## Freeze receipt

Commit `0f259710c15ec1b4c982b878bef325f0c6712b02` remains the superseded first
attempt. Corrected setup commit
`707fc10969b04bd31e135c8a711b33e9505e0d87` contains every exact runner,
observer, evaluator, builder, validator, and schema blob plus both pre-outcome
amendments, and none of the six registered outcome files. The shared
preregistration is frozen, all three priorities are preregistered, and the final
validator rejects all ten mutations before permitting M3.

## Non-claims

- Passing setup checks is not an empirical result.
- A bounded exact evaluator is not an open-world truth oracle.
- A 24-surface inventory is complete only for the declared local experiment.
- No residual, support state, chapter claim, release, or format changes here.
