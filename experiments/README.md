# Experiments

Layer-specific experiments and benchmark harnesses go here.

Current synthetic harness workspaces:

- `support_state_transitions/`
- `authority_transitions/`
- `plan_execution_contracts/`
- `context_admission_adequacy/`
- `readiness_residual_gates/`
- `benchmark_antigoodhart/`

`phase5_harness_registry.json` is the machine-readable registry for the
initial Phase 5 harness set. It is checked by
`python3 scripts/validate_phase5_harness_registry.py`.

These fixtures test deterministic record and cross-record semantics only. They
do not prove deployed runtime behavior, benchmark performance, or support-state
promotion.
