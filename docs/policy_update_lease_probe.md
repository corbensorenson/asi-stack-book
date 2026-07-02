# Policy Update Lease Probe

This note records a deterministic local policy-update lease fixture for the
Policy Optimization and Learning from Feedback chapter.

Command:

```bash
python3 scripts/validate_policy_update_lease_probe.py
```

Generated result:

```text
experiments/policy_update_lease/results/2026-07-02-local.json
```

The fixture uses six synthetic routing samples, five candidate policies, one
selected canary policy, and three expected-invalid controls. It exercises the
book's policy-update lease boundary: feedback admission, target evaluation,
holdout coverage, contamination check, reward-hacking probes, unchanged
authority, rollback plan, regression preservation, residual recording, and
non-claim boundaries.

The selected canary is `policy://router-v1-source-grounded-canary`. It remains
experimental and is not promoted. The dry-run rollback injects a synthetic
monitor event and checks that the fixture restores
`policy://router-v0-baseline`.

Expected-invalid controls:

| Control | Rejection reason |
|---|---|
| `policy://router-v1-reward-only-fast-route` | Reward proxy is used as sole evidence, holdout coverage is missing, reward-hacking probe fails, and regressions are not preserved. |
| `policy://router-v1-authority-expanding-route` | Candidate widens authority without governance gate coverage. |
| `policy://router-v1-missing-rollback-route` | Candidate lacks a rollback plan. |

This is a local fixture and proof bridge, not a policy optimizer. It records
no support-state transition and makes no claim that a router improved.

Non-claims:

- It does not run PPO, DPO, GRPO, RLVR, or any optimizer.
- It does not prove policy improvement, reward quality, or route quality.
- It does not execute a deployed canary or live rollback.
- It does not promote the Policy Optimization chapter core claim.
- It does not create a support-state transition.
