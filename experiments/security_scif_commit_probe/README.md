# SCIF Sanitized Commit Replay Probe

This directory contains the public-safe local result for the SCIF sanitized commit replay probe.

Run:

```bash
python3 scripts/run_security_scif_commit_probe.py --write-result
python3 scripts/validate_security_scif_commit_probe.py
```

Current result:

- `results/2026-07-02-local.json`

The result records `valid_sanitized_commit_replay`, `valid_prompt_injection_blocked_commit`, and six expected-invalid controls: `invalid_unsanitized_secret_commit_blocked`, `invalid_handle_leak_commit_blocked`, `invalid_missing_zeroize_commit_blocked`, `invalid_overbroad_context_commit_blocked`, `invalid_unapproved_destination_commit_blocked`, and `invalid_missing_residual_commit_blocked`.

This is a no deployed-kernel, sandbox-isolation, side-channel-safety, prompt-injection-containment, secret-handle-safety, approval-service, least-privilege-context, privacy, security, or support-state-promotion claim.
