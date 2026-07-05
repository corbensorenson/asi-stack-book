# Project Theseus Artifact-Retention Replay Import

This record documents a sanitized public-safe import of one Project Theseus
artifact-retention replay gate.

It records the shape and digest facts of the local Theseus report
`reports/theseus_artifact_retention_replay_gate.json` without copying the raw
report, private payloads, private path fields, candidate traces, prompts,
tests, solutions, score labels, or model artifacts into this public repository.

| Field | Value |
|---|---|
| Import id | `theseus-artifact-retention-replay-import-2026-07-05` |
| Validator | `python3 scripts/validate_theseus_artifact_retention_replay_import.py` |
| Sanitized fixture | `experiments/theseus_artifact_retention_replay_import/fixtures/valid/artifact_retention_replay_import.valid.json` |
| Result | `experiments/theseus_artifact_retention_replay_import/results/2026-07-05-local.json` |
| Evidence transition | `evidence_transitions/v1_x_measured/theseus_artifact_retention_replay_import_prototype_backed.json` |
| Source report SHA-256 | `a3d35452ec3a8f0db233f5985d5d0824a1d9f571ee9012970d52303bfece9759` |
| Source policy | `project_theseus_artifact_retention_replay_gate_v1` |
| Trigger state | `GREEN` |
| Replayed payload bytes | 41,943,527 |
| Archived bytes | 2,389,576 |
| Observed compression ratio | 17.552, not benchmarked |
| Public training rows | 0 |
| External inference calls | 0 |
| Expected-invalid controls | 7 |
| Narrow support transition | `argument` to `prototype-backed` for `project-theseus-as-report-first-implementation-reference.artifact_retention_replay_gate_import` |

## What Was Imported

The imported summary records one retained artifact replay in Theseus:

- one eligible retention action;
- one passed replay check;
- zero failed replay checks;
- one pointer verification;
- one defeater verification;
- one JSON parse verification;
- zero hard gaps;
- one compressed artifact record;
- one compression receipt;
- one proof-contract receipt record;
- one claim record;
- one artifact-graph record;
- one storage evidence-transition record;
- one defeater record.

The replay check states that the decoded payload SHA-256 equals the expected
payload SHA-256:
`5d26d57612479e1b5a0547af49e34d8ae779aef41e91b3eb2e676ad415a99da3`.

The exact retained artifact path, archive path, pointer path, and raw payload
remain outside this public repository. The public fixture records that those
path fields were redacted.

## Why It Matters

This is the first Theseus import in the book that moves beyond static
report-shape checking toward a real implementation-reference replay fact: a
retained artifact pointer was followed, the archive payload was decoded, the
payload hash matched the expected hash, the JSON parsed, and the defeater was
resolved for storage replay.

That is enough for a narrow non-core `prototype-backed` transition about the
Project Theseus artifact-retention replay gate import. It is not enough for
the Project Theseus chapter core claim, a deployed residual-ledger claim, a
deployed artifact-graph claim, model-quality evidence, benchmark evidence, or
clean live Project Theseus replay.

## Expected-Invalid Controls

The validator rejects:

- replay hash mismatch;
- private payload copying;
- chapter-core support-promotion overclaim;
- public training row leakage;
- hard-gap erasure;
- missing chapter-core non-claim boundary;
- disabled private-path redaction.

## Non-Claims

- This import does not copy the raw Project Theseus report or private payloads
  into this public repository.
- This import does not prove clean live Project Theseus replay.
- This import does not prove deployed residual-ledger storage or deployed
  artifact-graph behavior.
- This import does not prove model quality, benchmark performance, generation
  speed, safety, alignment, transfer, deployment readiness, or ASI.
- This import does not promote any chapter core claim above `argument`.
