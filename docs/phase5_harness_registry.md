# Phase 5 Harness Registry

Last updated: 2026-06-28

This registry records the Phase 5 executable harness set for the v1.0 candidate pass. The machine-readable source is `experiments/phase5_harness_registry.json`; the guard is `scripts/validate_phase5_harness_registry.py`.

The registry exists to keep the public evidence surface aligned. A Phase 5 harness is not considered fully wired unless it has a command, script, fixture directory, expected valid and expected-invalid fixtures, result record, public summary document, Appendix E row, roadmap/status references, and inclusion in `scripts/validate_book.py`.

## Registered Harnesses

| Harness | Command | Fixture expectation | Result record |
|---|---|---:|---|
| Claim ledger revision harness | `python3 scripts/validate_claim_ledger_revision.py` | 3 valid, 4 expected-invalid | `experiments/claim_ledger_revision/results/2026-06-28-local.md` |
| Proof-carrying claim harness | `python3 scripts/validate_proof_carrying_claims.py` | 3 valid, 5 expected-invalid | `experiments/proof_carrying_claims/results/2026-06-28-local.md` |
| Tribunal review harness | `python3 scripts/validate_tribunal_review.py` | 3 valid, 5 expected-invalid | `experiments/tribunal_review/results/2026-06-28-local.md` |
| Value conflict harness | `python3 scripts/validate_value_conflicts.py` | 3 valid, 5 expected-invalid | `experiments/value_conflicts/results/2026-06-28-local.md` |
| Constitutional alignment harness | `python3 scripts/validate_constitutional_alignment.py` | 3 valid, 5 expected-invalid | `experiments/constitutional_alignment/results/2026-06-28-local.md` |
| Governance rights harness | `python3 scripts/validate_governance_rights.py` | 3 valid, 5 expected-invalid | `experiments/governance_rights/results/2026-06-28-local.md` |
| Agency rights harness | `python3 scripts/validate_agency_rights.py` | 3 valid, 6 expected-invalid | `experiments/agency_rights/results/2026-06-28-local.md` |
| Support-state transition harness | `python3 scripts/validate_support_state_transitions.py` | 2 valid, 2 expected-invalid | `experiments/support_state_transitions/results/2026-06-28-local.md` |
| Authority transition harness | `python3 scripts/validate_authority_transitions.py` | 3 valid, 3 expected-invalid | `experiments/authority_transitions/results/2026-06-28-local.md` |
| Security kernel harness | `python3 scripts/validate_security_kernel.py` | 3 valid, 6 expected-invalid | `experiments/security_kernel/results/2026-06-28-local.md` |
| Stable capability fields harness | `python3 scripts/validate_stable_capability_fields.py` | 3 valid, 6 expected-invalid | `experiments/stable_capability_fields/results/2026-06-28-local.md` |
| Plan-execution contract harness | `python3 scripts/validate_plan_execution_contracts.py` | 2 valid, 5 expected-invalid | `experiments/plan_execution_contracts/results/2026-06-28-local.md` |
| Runtime adapter permission harness | `python3 scripts/validate_runtime_adapter_permissions.py` | 2 valid, 5 expected-invalid | `experiments/runtime_adapter_permissions/results/2026-06-28-local.md` |
| Context admission/adequacy harness | `python3 scripts/validate_context_admission_adequacy.py` | 3 valid, 5 expected-invalid | `experiments/context_admission_adequacy/results/2026-06-28-local.md` |
| Readiness/residual gate harness | `python3 scripts/validate_readiness_residual_gates.py` | 4 valid, 5 expected-invalid | `experiments/readiness_residual_gates/results/2026-06-28-local.md` |
| Benchmark anti-Goodhart harness | `python3 scripts/validate_benchmark_antigoodhart.py` | 2 valid, 5 expected-invalid | `experiments/benchmark_antigoodhart/results/2026-06-28-local.md` |
| Generation mode baseline harness | `python3 scripts/validate_generation_mode_baselines.py` | 2 valid, 4 expected-invalid | `experiments/generation_mode_baselines/results/2026-06-28-local.md` |
| Resource budget ledger harness | `python3 scripts/validate_resource_budget_ledgers.py` | 5 valid, 5 expected-invalid | `experiments/resource_budget_ledgers/results/2026-06-28-local.md` |
| Capacity smoothing toy harness | `python3 scripts/validate_capacity_smoothing.py` | 2 valid, 3 expected-invalid | `experiments/capacity_smoothing/results/2026-06-28-local.md` |

## Validation Contract

`python3 scripts/validate_phase5_harness_registry.py` checks:

- every registry entry has a stable ID, command, script, documentation page, experiment workspace, fixture directory, result record, primary chapter list, and non-claim list;
- valid and expected-invalid fixture counts match the registry;
- each result record and public harness document contains the recorded command and result summary;
- each harness command is included in `scripts/validate_book.py`;
- each harness command appears in generated Appendix E and in the public v1.0 status/roadmap surfaces;
- registered primary chapters exist in `book_structure.json`;
- the registry itself does not promote support states or claim deployed runtime behavior.

## Boundary

This registry is evidence plumbing. It preserves traceability for the synthetic and deterministic harness set, but it is not a behavior result by itself. It does not prove runtime behavior, benchmark quality, generation speed, model quality, proof adequacy, source interpretation, deployed enforcement, or ASI safety, and it does not move any Appendix C support state.
