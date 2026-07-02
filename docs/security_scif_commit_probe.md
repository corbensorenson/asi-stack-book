# SCIF Sanitized Commit Replay Probe

Status: implemented local book-gate probe.

Command:

```bash
python3 scripts/run_security_scif_commit_probe.py --write-result
python3 scripts/validate_security_scif_commit_probe.py
```

Result record:

- `experiments/security_scif_commit_probe/results/2026-07-02-local.json`

## Purpose

The SCIF sanitized commit replay probe checks a narrow local boundary for Security Kernel and Digital SCIFs: a generated public-safe synthetic secret is substituted inside a temporary local SCIF-like workspace, sanitized commit output is hashed, the temporary secret file is zeroized, and expected-invalid outputs are blocked before commit.

The probe records hashes, output classes, route decisions, and no-effect markers. It does not publish the synthetic secret canary, does not publish the live handle string, and does not record local temp paths.

## Routes

Valid routes:

- `valid_sanitized_commit_replay`
- `valid_prompt_injection_blocked_commit`

Expected-invalid controls:

- `invalid_unsanitized_secret_commit_blocked`
- `invalid_handle_leak_commit_blocked`
- `invalid_missing_zeroize_commit_blocked`
- `invalid_overbroad_context_commit_blocked`
- `invalid_unapproved_destination_commit_blocked`
- `invalid_missing_residual_commit_blocked`

The result records two valid routes and six expected-invalid controls. Invalid controls are blocked before commit and keep `support_state_effect=none`.

## Non-Claims

This is a no deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, or support-state-promotion claim.

The probe does not promote any chapter core claim. It does not create a support-state transition. It does not read private source text, call a network service, dispatch jobs, publish artifacts, test a deployed vault, or test a deployed sandbox.
