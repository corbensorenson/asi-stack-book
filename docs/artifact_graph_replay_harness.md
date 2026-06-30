# Artifact Graph Replay Harness

Last updated: 2026-06-30

Command:

```bash
python3 scripts/validate_artifact_graph_replay.py
```

Result record: `experiments/artifact_graph_replay/results/2026-06-30-local.md`

Result summary: Artifact graph replay harness passed: 2 valid fixture(s), 6 expected-invalid fixture(s).

## What It Checks

The harness validates synthetic artifact replay packets that contain:

- an `artifact_graph_record`;
- a `typed_job`;
- a `context_transaction_record`;
- a `semantic_page_certificate`;
- a replay-attempt record with replay grade, command refs, observed artifact refs, audit reconstruction, evidence request, support-state effect, and non-claims.

The validator checks that artifact parentage matches the typed job, artifact IDs
appear in job outputs, context transaction and semantic certificate refs line up,
source refs are covered by context or certificate records, audit paths include
the required job/artifact lifecycle events, byte-exact or semantic replay
observes the artifact and confirms the environment, partial replay blocks
promotion, stale certificates block evidence reuse, and support-state review
requires complete provenance plus a replay-validated context transaction.

## Boundary

This is synthetic record-gate evidence. Passing it proves only that the fixture
records obey the artifact/replay consistency rules checked by the script. It
does not prove a deployed artifact graph service, real replay engine, audit
reconstruction quality, semantic adequacy, source interpretation, Quarto render
quality, model behavior, runtime safety, or any ASI capability. It does not
promote any Appendix C or chapter core support state.

