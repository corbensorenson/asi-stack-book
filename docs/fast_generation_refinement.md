# Fast Generation context-to-closure refinement

The replacement model has eight reachable stages: request, context binding, mode selection, draft generation, verification or fallback, complete accounting, governed decision, and closure. It exposes 60 routes and separates task, mode, evaluator, result, residual, event, draft, verification, fallback, useful-outcome, decision, support, and external-effect state.

`python3 scripts/validate_fast_generation_refinement.py` independently reaches all 60 routes, rejects 51/51 non-accepting mutations, recompiles Lean, runs the exact 2-valid/4-invalid generation-mode baseline harness, revalidates the three-route four-task bundle, revalidates the 1-valid/6-invalid Theseus import, and SHA-256 binds every consumed result and baseline fixture.

The verified witness reaches closure with one draft, one verification, one authored useful-outcome accounting event, and no support or external effect. A separate fallback witness reaches closure with fallback cost required. These are finite local lifecycle facts, not model generation, wall-clock speed, evaluator independence, useful throughput, quality superiority, deployed fallback, reproduction, transfer, or state of the art. Support-state and external-effect authority remain exactly `none`.
