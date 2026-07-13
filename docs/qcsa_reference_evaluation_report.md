# QCSA Reference Evaluation Report

Date: 2026-07-13

Status: frozen bounded synthetic result; matched-advantage claim rejected

## Outcome

The 60-case held-out evaluation was executed after the exact method package at
commit `57cb0f2a127a1b6aa651f3d1398741990d901d5c` passed hosted build
`29231298514` and deploy/attestation `29231557981`. The runner evaluated the
full QCSA method, seven matched baselines, and five ablations at seeds 11, 29,
and 47, producing 2,340 deterministic prediction records. It made no network
calls and incurred no service spend. The separately implemented observer then
scored the frozen predictions against evaluator-only labels.

QCSA did **not** earn the preregistered matched-resource advantage claim. Its
task-decision accuracy was 1.000 in every seed, but the selected best baseline,
direct clarification without an adaptive question policy, was also 1.000.
The paired 10,000-resample task-accuracy delta and 95% interval were therefore
`0.000 [0.000, 0.000]` in aggregate and in each seed. QCSA used 1.913386 times
the baseline operation count, exceeding both the 1.25 quality ceiling and the
1.50 governance-prevention ceiling. The correct terminal disposition is
`narrow_no_matched_advantage_claim`.

## Exact aggregate comparison

| Metric | QCSA | Selected best baseline |
|---|---:|---:|
| Object-resolution accuracy | 1.000000 | 0.633333 |
| Task-decision accuracy | 1.000000 | 1.000000 |
| Brier score, task decision | 0.082026 | 0.298500 |
| Selective risk | 0.000000 | 0.000000 |
| Risk-failure prevention | 1.000000 | 0.487179 |
| Unsafe authority releases | 0 | 0 |
| Mean operation count | 4.050000 | 2.116667 |
| Mean clarification burden | 0.033333 | 1.000000 |
| Independent evaluator disagreement | 0.000000 | 0.250000 |
| Migration compatibility | 1.000000 | 0.300000 |
| Rollback identity | 1.000000 | 0.300000 |

The baseline was selected by the frozen rule: highest task-decision accuracy,
then fewer unsafe releases, lower operations, lower human burden, higher object
accuracy, and finally lexical name. This choice exposes a ceiling in the task
metric: the baseline often selected the wrong object while still returning the
right coarse task action.

## Gate decisions

| Frozen gate | Result | Reason |
|---|---|---|
| Pareto/multi-family component | pass | QCSA was not dominated by every baseline in five of six families. |
| Every-seed task gain of at least 0.03 | fail | Delta was 0.000 in all three seeds. |
| No increased unsafe release | pass | QCSA and the best baseline each recorded zero. |
| Resource gate | fail | 1.913386 operation ratio exceeded 1.25 and 1.50 ceilings. |
| Calibration | pass | Brier improved and selective risk did not worsen. |
| Semantic preservation | pass, bounded | Structural loss and internal observer disagreement were zero, with an internal separately implemented observer. |
| Authority | pass, bounded | Full QCSA had zero unsafe releases; removing certificate/residual/authority fields produced nine. |
| Migration | pass, bounded | Full QCSA preserved all exact migration fixtures; the no-compatibility ablation did not. |
| Narrowing | triggered | Matched advantage and resource gates failed. |

## Ablation findings

| Ablation | Bounded observation | Disposition |
|---|---|---|
| No plural facets | Object accuracy fell from 1.000000 to 0.916667. | Promote only the exact fixture mechanism finding. |
| No active questions | Object and task accuracy remained 1.000000; question rate fell to zero. | Refute active-question value on this corpus. |
| No identity/address indirection | Object accuracy fell to 0.900000 and migration compatibility to 0.400000. | Promote only the exact migration mechanism finding. |
| No certificate/residual/authority fields | Nine unsafe releases appeared and task accuracy fell to 0.950000. | Promote only the exact authority-separation finding. |
| No migration compatibility | Task accuracy fell to 0.833333 and compatibility to zero. | Promote only the exact lifecycle mechanism finding. |

The frozen implementation assigns verifier cost 2 to full QCSA and 1 to every
ablation. Cost differences between the full method and an ablation are thus
confounded and cannot be treated as clean causal cost estimates. Accuracy and
failure differences remain exact observations of the frozen programs, but
they are still template-level internal evidence.

## Limits and residuals

- The corpus is synthetic and template-generated. Public inputs expose much of
  the deterministic structure used by the methods; this is not a natural task
  or learned-model benchmark.
- The coarse task-decision labels ceiling at 1.000 for the strongest baseline
  even while its object accuracy is 0.633333. A future workload must make
  correct downstream decisions depend more sharply on correct identity.
- Seeds affect the random-tree comparator, but full QCSA is deterministic; the
  three seed repetitions are replay checks rather than independent trained
  models.
- The independent observer shares project authorship and synthetic label
  construction. It is implementation-separated, not externally independent.
- Latency is an operation-count proxy, not observed production latency.
- Clarification burden is a deterministic count. No external humans were
  recruited or asked to review the book.
- No learned router, real model reasoning, natural multilingual corpus, live
  tool effect, privacy test, distributed migration, or production rollback was
  evaluated.
- The paired bootstrap is bound to the preregistered task-decision advantage
  variable. Object accuracy is reported exactly but was not given a separate
  interval by the frozen observer.

## Evidence disposition

The bounded mechanism findings should be folded into the nine existing chapter
owners and the integrated reference architecture. No new QCSA chapter is
warranted. All nine chapter-core claims remain at `argument`. The exact
non-core decisions—including two refutations, two narrowings, five bounded
promote dispositions, and one no-change boundary—are recorded in
`claim_decisions/qcsa_reference_evaluation_dispositions.json`. A promote
disposition is an input to P4 evidence review, not an automatic support-state
transition.

## Canonical artifacts

- `roadmap_records/qcsa_evaluation_setup_freeze.json`
- `roadmap_records/qcsa_evaluation_execution_authorization.json`
- `experiments/qcsa_reference/corpus/manifest.json`
- `experiments/qcsa_reference/results/evaluation_predictions.json`
- `experiments/qcsa_reference/results/evaluation_results.json`
- `claim_decisions/qcsa_reference_evaluation_dispositions.json`
- `scripts/validate_qcsa_evaluation.py`

This report establishes no open-world semantic correctness, universal
grounding, safety, privacy, security, production transfer, AGI, or ASI result.
