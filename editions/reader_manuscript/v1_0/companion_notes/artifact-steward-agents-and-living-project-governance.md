# Artifact Steward Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `artifact-steward-agents-and-living-project-governance`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/artifact-steward-agents-and-living-project-governance.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/artifact-steward-agents-and-living-project-governance.qmd`

Evidence references: `docs/curated_reader_artifact_steward_prose_pass.md`,
`schemas/artifact_steward_charter.schema.json`,
`schemas/project_work_contract.schema.json`,
`schemas/contribution_ledger_entry.schema.json`,
`schemas/treasury_policy_record.schema.json`,
`schemas/event_taint_record.schema.json`,
`schemas/steward_action_decision.schema.json`, and
`schemas/sunset_review_record.schema.json`.

This note helps e-reader and audio review for the Artifact Steward chapter. It
does not replace the chapter prose or the curated prose draft. Meaning-critical
limits must still stay in the reader spine: the steward is not the owner;
authority, spending, governance, and release actions remain bounded by explicit
records and human approval; and event taint and sunset policy are governance
boundaries, not optional details.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
the steward's project objects and implementation ladder without mistaking
project memory, issue triage, treasury proposals, or worker coordination for
ownership, governance legitimacy, release approval, or deployed steward
execution.

## Project-Object Quick Reference

| Object | What it records | Boundary |
|---|---|---|
| `ArtifactStewardCharter` | Mission, non-goals, maintainers, authority ceiling, evidence policy, release policy, budget policy, federation policy, and sunset criteria. | The charter bounds the steward; it does not grant ownership. |
| `ProjectWorkContract` | Objective, context refs, allowed files/tools, forbidden tools, outputs, acceptance tests, review gates, evidence obligations, rollback, and non-claims. | Work authority comes from the contract, not from convenience. |
| `ContributionLedgerEntry` | Authorship, review, evidence credit, compensation status, governance effect, reputation signal, and conflicts. | Credit, money, votes, and evidence must not collapse into one score. |
| `TreasuryPolicyRecord` | Spend modes, caps, protected spend classes, approval thresholds, compute/rental limits, freezes, and audit duties. | The steward may propose or execute only inside the policy mode. |
| `EventTaintRecord` | Source, actor, surface, trusted fields, untrusted fields, forbidden control uses, review needs, sanitized artifacts, and residuals. | Issues, PRs, comments, and worker outputs are not privileged control text. |
| `StewardActionDecision` | What the steward proposed, ran, blocked, or escalated, plus authority basis, evidence refs, approvals, rejected options, residuals, and non-claims. | Decisions remain reviewable and appealable. |
| `SunsetReviewRecord` | Value signal, users, maintainers, open risks, funds, dependencies, archive plan, transfer/fork path, and appeal path. | Project continuity must be allowed to stop. |

## Implementation Ladder

For reader and audio treatment, compress the implementation ladder into this
sequence:

1. Start with a `PROJECT_STEWARD.yml` charter and zero or proposal-only spend.
2. Add a GitHub-oriented assistant that labels, summarizes, drafts plans, and
   proposes work contracts without merge, release, spending, or governance
   authority.
3. Add machine-readable work contracts, verification gates, and contribution
   ledgers.
4. Add treasury policy only as explicit proposal, bounty, recurring-ops, or
   compute records with caps and approvals.
5. Add worker federation only through sandboxed contracts and evidence bundles.
6. Add governance votes, appeals, fork/exit paths, and sunset mode only when the
   artifact actually needs them.

The important reader boundary is that each step adds inspection before it adds
autonomy.

## Audio Treatment

In an audio script, do not read every schema field as a long catalog. Narrate
the steward as a continuity layer with seven project objects:

- a charter for mission and authority;
- a work contract for scoped labor;
- a contribution ledger for separated credit;
- a treasury policy for bounded money and compute;
- an event-taint record for untrusted project inputs;
- an action decision for reviewable steward behavior;
- a sunset review for knowing when to stop.

The detailed object table can be routed to this companion note. The main audio
should keep repeating the practical boundary: a steward helps humans govern a
project; it does not own the project.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim steward workflow execution, treasury
  execution, governance correctness, release readiness, or deployed project
  autonomy.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
