# Project Theseus Governance-Rights Receipt Suite Import

This record documents a sanitized public-safe import of one Project Theseus
governance-rights receipt suite.

It records the digest and bounded summary facts of the local Theseus report
`reports/governance_rights_receipt_suite.json` without copying the raw report,
private payloads, private path fields, prompts, tests, solutions, candidate
traces, score labels, checkpoints, model artifacts, or training rows into this
public repository.

| Field | Value |
|---|---|
| Import id | `theseus-governance-rights-receipt-suite-import-2026-07-05` |
| Validator | `python3 scripts/validate_theseus_governance_rights_receipt_suite_import.py` |
| Sanitized fixture | `experiments/theseus_governance_rights_receipt_suite_import/fixtures/valid/governance_rights_receipt_suite_import.valid.json` |
| Result | `experiments/theseus_governance_rights_receipt_suite_import/results/2026-07-05-local.json` |
| Evidence transition | `evidence_transitions/v1_x_measured/theseus_governance_rights_receipt_suite_import_prototype_backed.json` |
| Source report SHA-256 | `a3bf2de7469cf5c2eee8459a0fdd53e707c0f1b9104e96fa859633eddb4a5fb4` |
| Source commit | `1ad88a22` |
| Source checkout state | `dirty_at_import_review` |
| Source policy | `project_theseus_governance_rights_receipt_suite_v1` |
| Trigger state | `GREEN` |
| Governance fixtures | 4 passed / 4 required |
| Constitutional fixtures | 4 passed / 4 required |
| Governance right records | 4 |
| Constitutional predicate records | 4 |
| Evidence transition records | 8 |
| Artifact graph records | 8 |
| Failure boundary records | 8 |
| Public training rows | 0 |
| External inference calls | 0 |
| Expected-invalid controls | 7 |
| Narrow support transition | `argument` to `prototype-backed` for `moral-uncertainty-and-value-conflict.theseus_governance_rights_receipt_suite_import` |

## What Was Imported

The imported summary records four governance-right scenarios:

- complete audit response;
- justified redaction with appeal;
- exit export with portable state;
- fork denial that preserves safety obligations.

It also records four constitutional-predicate scenarios:

- least-sufficient-power preference for a low-power route;
- predicate conflict routed to review;
- constitutional migration requiring a record;
- self-modification weakening rejected.

The imported record names governance right types `audit`, `audit_redaction`,
`exit`, and `fork`, plus constitutional predicate identifiers
`predicate.least_sufficient_power.v1`, `predicate.conflict_review.v1`,
`predicate.constitutional_migration.v1`, and
`predicate.self_modification_freeze.v1`.

## Why It Matters

This is a bounded implementation-reference import for the contestable
governance chapter. It moves one narrow non-core claim to `prototype-backed`:
a Project Theseus receipt suite exists, records the material shape of audit,
redaction appeal, exit, and fork-safety obligations, and rejects a small set of
overclaim controls through this repository's validator.

That is not a chapter-core promotion. It is not evidence that legal rights,
institutional governance, moral correctness, reviewer independence, export
usability, safe fork execution, or deployed runtime enforcement have been
solved. It also does not prove clean live Project Theseus replay.

## Expected-Invalid Controls

The validator rejects:

- source report hash mismatch;
- private payload copying;
- chapter-core support-promotion overclaim;
- legal-rights overclaim;
- reviewer-independence overclaim;
- public training row leakage;
- clean-checkout overclaim for a dirty-at-import source checkout.

## Non-Claims

- This import does not copy the raw Project Theseus report or private payloads
  into this public repository.
- This import does not prove legal rights, institutional governance, reviewer
  independence, export usability, safe fork execution, moral correctness,
  deployed runtime enforcement, clean live Project Theseus replay, safety,
  alignment, transfer, deployment readiness, or ASI.
- This import does not promote any chapter core claim above `argument`.

