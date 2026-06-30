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

`Reference trace harness passed: 2 valid fixture(s), 6 expected-invalid fixture(s).`

