# Runtime Adapter Adversarial Boundary Probe

This experiment records a deterministic synthetic runtime-adapter boundary
fixture for the Runtime Adapters chapter.

Run:

```bash
python3 scripts/validate_runtime_adapter_adversarial_boundary_probe.py --write-result
python3 scripts/validate_runtime_adapter_adversarial_boundary_probe.py
```

Current result:
`results/2026-07-02-local.json`

Boundary: this fixture checks finite records only. It does not execute a
deployed adapter, prove sandbox isolation, prove approval-service behavior,
prove secret-handle safety, prove policy-enforcement correctness, prove
rollback-service behavior, prove revocation propagation, perform security
review, or promote the Runtime Adapters chapter core claim.
