# Reference Trace Harness

Command: `python3 scripts/validate_reference_trace.py`

The reference trace harness checks deterministic fixture records for the
Integrated Reference Architecture chapter. It validates each nested
`reference_trace_record` against `schemas/reference_trace_record.schema.json`,
then applies semantic checks for parent artifact continuity, authority-chain and
authority-delta visibility, layer coverage from intent through SCF, artifact
count, evidence and residual deltas, validation command refs, source-note refs,
blocked-path stop conditions, promotion blockers, non-promoting support effects,
and explicit non-claims.

## Boundary

Passing this check proves deterministic fixture consistency only. It does not
prove an integrated ASI Stack runtime, deployed layer behavior, artifact
continuity in a live trace, authority-stop enforcement, runtime replay,
model-quality, benchmark performance, safety, or support-state promotion.

## Current Result

Result record: `experiments/reference_trace/results/2026-06-30-local.md`

Expected command output:

`Reference trace harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).`

## Reference Trace Replay

Command: `python3 scripts/run_reference_trace_replay.py --write-result`

Validation command: `python3 scripts/validate_reference_trace_replay.py`

Replay result:
`experiments/reference_trace/replay_results/2026-07-02-resource-flagship.json`

The replay runs `python3 scripts/validate_resource_flagship_lane.py`, records
the command output digest, checks a tracked artifact bundle, and emits a
Reference Trace Record with intent, authority, handoffs, evidence deltas,
residual deltas, validation commands, source refs, and non-claims. It also
attaches the blocked-authority fixture as the blocked-path stop-condition
reference.

This is local replay evidence only. It does not prove an integrated ASI Stack
runtime, deployed layer behavior, live artifact-continuity service,
authority-stop enforcement outside the blocked-authority fixture, scheduler
behavior, model quality, benchmark quality, safety, economic outcomes, or
support-state promotion.
