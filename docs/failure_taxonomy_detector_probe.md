# Failure Taxonomy Detector Probe

The Failure Taxonomy Detector Probe is a deterministic synthetic
failure-taxonomy detector fixture for the
`failure-modes-of-ungoverned-intelligence` chapter.

It validates two valid synthetic failure incidents and seven expected-invalid controls.
The valid incidents cover authority creep blocked at an authority ceiling and
Goodhart/evaluator drift residualized through evaluator freeze and review
escalation. The controls reject missing failure classes, missing boundary
owners, mitigation without receipts, authority creep that continues as
ordinary operation, Goodhart/proxy failure with no residual, recurrence
without escalation, and support-state promotion from the fixture.

Run:

```bash
python3 scripts/validate_failure_taxonomy_detector_probe.py
```

The local result record is:

```text
experiments/failure_taxonomy_detector/results/2026-07-02-local.json
```

This probe does not prove failure detection, prove prevention, prove
mitigation effectiveness, run a deployed detector, prove evaluator
independence, or promote the chapter support state. In short: no support-state transition.
