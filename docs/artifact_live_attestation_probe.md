# Artifact Live Attestation Probe

Status: bounded local live repository attestation. It is not a deployed
attestation service, not open-world receipt faithfulness, not external review,
and not support-state promotion.

The probe is run by:

```bash
python3 scripts/validate_artifact_live_attestation_probe.py
```

The generated result is:

`experiments/artifact_live_attestation/results/2026-07-04-local.json`

## Target

The selected target artifact is the clean tracked record-reality sequence result:

`experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json`

This target is public-safe, already part of the Artifact Graph receipt-reality
lane, clean relative to its tracked Git object, and validates through:

```bash
python3 scripts/validate_artifact_graph_record_reality_sequence.py
```

## What Is Checked

The validator checks one produced artifact through filesystem bytes, git object bytes, and command replay across three bounded observation routes:

- filesystem bytes over the tracked target path;
- git object bytes from `HEAD:<target path>`;
- command replay of the selected validator output.

It also records independent observer roles, rejects same-component self-check
laundering, includes a shape-valid wrong-digest trap receipt, records explicit
attestation limits, preserves no support-state effect, and rejects seven
expected-invalid controls:

- `invalid_filesystem_digest_mismatch`
- `invalid_git_blob_digest_mismatch`
- `invalid_command_replay_failure`
- `invalid_same_component_self_check_laundering`
- `invalid_trap_receipt_accepted`
- `invalid_unbounded_attestation`
- `invalid_support_promotion_from_attestation`

## Boundary

This is local live repository attestation for one selected artifact. It shows
that a current committed file, a git object, and a command replay can agree
under explicit observer and non-claim boundaries.

It does not prove open-world receipt faithfulness, deployed attestation
behavior, deployed audit behavior, verifier correctness, external project
truth, complete provenance, model quality, benchmark quality, safety, ASI, or
the Artifact Graphs chapter core claim.

`evidence_transitions/v1_x_measured/artifact_live_attestation_no_change.json`
records the accepted no-promotion decision for the side lane. That transition
keeps support at `argument` and records `blocks_promotion` until stronger live
or externally reviewable attestation evidence exists.
