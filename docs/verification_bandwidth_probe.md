# Verification Bandwidth Probe

The Verification Bandwidth Probe is a deterministic synthetic contradiction
and adequacy fixture for the chapter
`verification-bandwidth-and-context-adequacy`.

It validates two valid synthetic adequacy traces and seven expected-invalid controls.
The valid traces cover a pairwise semantic-unit check that detects a planted
cross-document contradiction and blocks verified support, plus a drafting-only
context packet that is useful but inadequate for verification. The controls
reject summary-derived promotion, dominant-distractor contradiction misses,
high-risk inadequate context without escalation, schema-mode support for an
empirical runtime claim, ignored negative evidence, verified support with
unidentified semantic units, and support-state promotion from the fixture.

Run:

```bash
python3 scripts/validate_verification_bandwidth_probe.py
```

The local result record is:

```text
experiments/verification_bandwidth/results/2026-07-02-local.json
```

This probe does not measure model verification bandwidth, prove
contradiction-rate performance, prove distractor resistance, validate an
adequacy classifier, execute a deployed claim ledger or escalation service, or
promote the chapter support state. In short: no support-state transition.
