# Artifact Randomized Attestation Audit

Status: bounded randomized artifact attestation audit over a deterministic pseudo-random
multi-artifact repository sample. It is not
a deployed attestation service, not external review, not open-world receipt
faithfulness, not verifier-correctness evidence, and not support-state
promotion.

The audit is run by:

```bash
python3 scripts/validate_artifact_randomized_attestation_audit.py
```

The generated result is:

`experiments/artifact_randomized_attestation/results/2026-07-04-local.json`

## What Is Sampled

The validator uses a fixed public seed:

`asi-stack.record-reality.randomized-live-audit.2026-07-04`

It scores a six-artifact public-safe candidate pool with
`sha256(seed + ':' + artifact_path)`, sorts by score, and selects the first
four artifacts. The current selected artifacts are:

- `experiments/artifact_steward_lifecycle_probe/results/2026-07-02-local.json`
- `experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json`
- `experiments/capability_replacement_trace/results/2026-07-02-local.json`
- `experiments/residual_honesty_conservation/results/2026-07-03-local.json`

## What Is Checked

For each selected artifact, the validator checks:

- filesystem bytes for the tracked target path;
- git object bytes from `HEAD:<target path>`;
- command replay of the validator that owns the selected result artifact;
- a shape-valid wrong-digest trap receipt that must be rejected;
- clean-worktree status for the selected target artifact;
- explicit non-claim and no-promotion boundaries.

The current result records 4 selected artifacts, 12 accepted observation
routes, 4 rejected trap receipts, and 8 rejected mutation controls:

- `invalid_missing_selection_seed`
- `invalid_filesystem_digest_mismatch_in_sample`
- `invalid_git_object_digest_mismatch_in_sample`
- `invalid_command_replay_failure_in_sample`
- `invalid_not_beyond_one_selected_artifact`
- `invalid_same_component_self_check_laundering`
- `invalid_unbounded_randomized_attestation`
- `invalid_support_promotion_from_randomized_audit`

## Boundary

This audit moves the Artifact Graphs record-reality lane beyond one hand-picked
target artifact. It shows that a reproducible, deterministic sample of current
public-safe repository evidence artifacts can be checked through separate
filesystem, git-object, and command-replay routes while trap, same-component
self-check, unbounded-attestation, and support-promotion controls remain
rejected.

It still does not prove open-world receipt faithfulness, deployed attestation
behavior, deployed audit behavior, verifier correctness, external project
truth, complete provenance, model quality, benchmark quality, safety, ASI, or
the Artifact Graphs chapter core claim.

`evidence_transitions/v1_x_measured/artifact_randomized_attestation_no_change.json`
records the accepted no-promotion decision for this side lane. It keeps support
at `argument` and records `blocks_promotion` until deployed or externally
reviewable attestation, stronger verifier-quality evidence, or broader
trust-base storage/replay evidence exists.
