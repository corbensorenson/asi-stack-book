# Artifact Graph Record-Reality Sequence

Command:

```bash
python3 scripts/validate_artifact_graph_record_reality_sequence.py
```

Fixture:

`experiments/artifact_graph_record_reality_sequence/input/record_reality_sequence.json`

Result:

`experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json`

## Scope

This bounded fixture tests a finite record-reality sequence for the Artifact
Graphs chapter. It starts from an eligible byte-exact replay/provenance event,
records a stale-certificate blocker, records a partial-replay blocker, and
then restores bounded-review eligibility only after a fresh byte-exact
replay/provenance event with replay-validated transaction state, digest
verification, independent checking, non-claim boundaries, and no support-state
effect.

## Accepted Sequence

The valid sequence has four events:

- initial byte-exact replay eligible for bounded review;
- stale certificate event that blocks reuse;
- partial replay event that remains blocked from bounded review;
- fresh byte-exact replay/provenance event that restores bounded-review
  eligibility.

The validator records `fresh_replay_restores_after_block: true`,
`valid_sequences_end_eligible: true`, `support_state_effect: none`,
`chapter_core_support_effect: none`, and `evidence_transition_created: false`.

## Expected-Invalid Controls

The four expected-invalid controls cover:

- support-state effect after a stale certificate;
- claimed restoration without a fresh replay/provenance event;
- missing non-claim boundary;
- support review without a replay-validated transaction.

All four controls are rejected by the validator.

## Lean Bridge

`AsiStackProofs.ArtifactGraph` mirrors the sequence fixture through
`artifact_record_reality_sequence_fixture_bridge` and route theorems for stale
certificates, incomplete replay, and fresh byte-exact replay restoration.

## Non-Claims

- This fixture does not promote any chapter core support state.
- This fixture does not create an evidence transition.
- This fixture does not prove deployed artifact graph behavior, real replay,
  verifier correctness, audit durability, source interpretation, or open-world
  receipt faithfulness.
