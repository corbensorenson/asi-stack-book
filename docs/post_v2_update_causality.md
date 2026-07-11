# Post-v2 Real Update-Causality Campaign

Executed: 2026-07-10

This campaign trains a small local PyTorch policy network on the frozen
1,200-example nonlinear workload. For seeds 17, 29, and 43 it creates a trained
base checkpoint, then compares no update, bounded fine-tuning, regularized
fine-tuning, and deletion-aware retraining. Best checkpoints are selected only
by validation accuracy; final checkpoints are retained separately. Every
checkpoint has byte and tensor-state digests, parameter deltas, fixed-probe and
test-output digests, forgetting measures, deletion-cohort measures, and
rollback lineage.

## Actual Mutation and Utility

The no-update arm had zero parameter delta, zero changed test decisions, and
zero fixed-probe changes for all seeds. Every challenger had a nonzero tensor
delta and changed outputs:

| Arm (final checkpoints, three seeds) | Mean test accuracy | Changed test decisions | Fixed-probe changes | Mean retained-base accuracy |
|---|---:|---:|---:|---:|
| No update | 0.7722 | 0 | 0 | 0.7597 |
| Bounded fine-tune | 0.7792 | 41 | 9 | 0.7542 |
| Regularized challenger | 0.7778 | 40 | 9 | 0.7549 |
| Deletion-aware retrain | 0.7778 | 28 | 6 | 0.7597 |

Mutation was real but gains were small and seed-dependent. Fine-tuning also
reduced retained-base accuracy on average, so the packet preserves forgetting
rather than reporting only test improvement.

## Best Versus Final Authority

Validation-selected best and mandatory final checkpoints disagreed on 30 test
decisions for bounded fine-tuning, 29 for the regularized arm, and 3 for
deletion-aware retraining. Best epochs ranged from 1 to 40. The record retains
both checkpoint identities and does not substitute the better-looking one
after test evaluation.

## Deletion Request

The 60-member deletion cohort consists of update examples with deliberately
flipped training labels and retained true labels. Across seeds, deletion-aware
retraining (which excludes this cohort) achieved mean true-label accuracy
0.8222 on those members versus 0.7944 for final bounded fine-tuning and 0.7833
for the base. Its mean flipped-training-label accuracy was 0.1778. It changed
nine cohort responses relative to the three bases.

This is evidence of a bounded causal difference from excluding a poisoned
cohort. It is not proof that member influence is absent, that stored data was
erased, that privacy improved, or that a production unlearning request was
satisfied.

## Rollback and Invalidation

Each seed loaded the pinned base checkpoint after the challenger campaign and
matched its tensor-state digest exactly. The three rollbacks invalidated nine
descendant challenger arms in total. Digest equality establishes checkpoint
identity inside this artifact set; it does not establish deletion from caches,
backups, optimizer state, or systems outside the experiment.

## Claim Dispositions

All four affected core claims receive `no_change`:

- Data Engines, Continual Learning, and Unlearning gains a real local
  mutation/deletion packet but not production unlearning transfer.
- Policy Optimization gains checkpoint/output causality but no human- or
  model-feedback learning result.
- Open-Ended Improvement remains unsupported by a fixed, stopped four-arm
  campaign.
- Recursive Self-Improvement gains only a bounded rollback/invalidation
  transaction, not recursive improvement evidence.

## Reproduction

```bash
python3 scripts/validate_post_v2_update_causality_setup.py
python3 scripts/validate_post_v2_update_causality.py
```
