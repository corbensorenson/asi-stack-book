# Evidence Bundle Completeness Probe

The Evidence Bundle Completeness Probe is a deterministic synthetic
evidence-bundle fixture for the `evidence-states-and-claim-discipline`
chapter.

It validates two valid synthetic evidence bundles and seven expected-invalid controls.
The valid bundles cover a no-change lineage/source-note bundle and a
blocked-promotion bundle that records why a tempting move from `argument` to
`synthetic-test-backed` still has no support effect. The controls reject
missing claim IDs, missing artifact or result references, missing commands,
support promotion without an accepted transition record, missing changelog
references, missing limitations or non-claims, stale changelog linkage, and
evidence-truth overclaiming from a fixture.

Run:

```bash
python3 scripts/validate_evidence_bundle_completeness_probe.py
```

The local result record is:

```text
experiments/evidence_bundle_completeness/results/2026-07-02-local.json
```

This probe does not prove evidence truth, prove source interpretation, prove
artifact correctness, create a support-state transition, promote the chapter
support state, or prove deployed release governance. In short: no
no support-state transition.
