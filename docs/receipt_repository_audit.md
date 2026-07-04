# Receipt Repository Audit

Date: 2026-07-03

Command: `python3 scripts/validate_receipt_repository_audit.py`

Result: `experiments/receipt_repository_audit/results/2026-07-03-local.json`

## Purpose

This audit is the next bounded step after the receipt-faithfulness adversarial
fixture. The fixture rejects malformed or overclaiming synthetic receipt
records. This audit reads selected real repository receipt surfaces and checks
whether their artifact references, tracked digests, command records, external
receipt fingerprints, non-claims, and support-state boundaries still line up.

It is not a deployed attestation system and it is not a proof of open-world
receipt truth. It is a repository-level receipt/reality audit over the records
the book already uses.

## Audited Receipts

| Receipt | Record shape | Checked boundary |
|---|---|---|
| Resource flagship | Local aggregate digest bundle | 10 command records, 27 artifact refs, 26 tracked digest checks, no chapter-core support effect. |
| Theseus/Fast support | Public-safe project support bundle | 4 replay commands, 17 artifact refs, 16 tracked digest checks, no clean-live-replay or model-quality claim. |
| Reference trace replay | Local reference-trace replay | 1 replay command, 14 artifact refs, 13 tracked digest checks, record-shape-only support effect. |
| Circle external rope | External receipt fingerprint summary | 5 passing external-command summaries and 5 receipt/contract fingerprints; no vendored-public-dependency or broad Circle claim. |

## Mutation Controls

The validator rejects five expected-invalid controls:

- `invalid_missing_artifact_ref`
- `invalid_tracked_digest_mismatch`
- `invalid_failed_command_replay`
- `invalid_missing_non_claims`
- `invalid_support_promotion_overclaim`

Those controls are deliberately small. They test that a receipt cannot stay
accepted if it points to a missing artifact, carries a stale tracked digest,
records a failed command replay, loses its non-claim boundary, or tries to
turn repository receipt shape into chapter-core promotion.

## Current Result

The current result accepts four selected receipt records, checks 55 tracked
artifact digests, recognizes one external fingerprint receipt, and rejects all
five mutation controls while preserving no support-state promotion.

Lean bridge: `receipt_repository_audit_fixture_bridge` in
`AsiStackProofs.ArtifactGraph`.

## Receipt Challenge Layer

Command: `python3 scripts/validate_receipt_repository_challenge.py`

Result:
`experiments/receipt_repository_audit/results/2026-07-04-challenge.json`

The challenge layer is a deterministic challenge over the audit above. It uses
seed `asi-stack-receipt-reality-challenge-v1-2026-07-04` to select one
challenge response per audited receipt:

- Resource flagship: tracked digest for
  `evidence_transitions/v1_x_measured/resource_workload_quality_selector_empirical_test_backed.json`.
- Theseus/Fast support: tracked digest for
  `docs/theseus_public_task_bundle_import.md`.
- Reference trace replay: tracked digest for
  `docs/resource_flagship_lane_run.md`.
- Circle external rope: external `contract_content_fingerprint`.

The validator accepts all four deterministic challenge responses and rejects
five expected-invalid controls:

- `invalid_challenge_tracked_digest_mismatch`
- `invalid_challenge_artifact_missing`
- `invalid_external_fingerprint_mismatch`
- `invalid_challenge_missing_non_claims`
- `invalid_challenge_support_promotion_overclaim`

Lean bridge: `receipt_repository_challenge_fixture_bridge` in
`AsiStackProofs.ArtifactGraph`.

This challenge makes the repository audit harder to fake than a static summary:
the chosen files or fingerprint fields must still answer a reproducible
challenge. It remains a repository challenge, not a deployed or open-world
attestation system.

## Boundaries

- This audit does not prove open-world receipt faithfulness.
- This audit does not prove deployed attestation or audit behavior.
- This audit does not prove verifier correctness or external project truth.
- This audit does not promote any chapter core claim.
- This audit does not create a support-state transition.
