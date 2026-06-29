# Defended Contribution Track Selection

Last updated: 2026-06-29

This record selects the v1.x defended contribution tracks from
`docs/a_plus_quality_scorecard.md` and binds them to the current active evidence
cycle in `docs/v1_x_active_evidence_cycle.md`. It is a planning and
release-control surface, not evidence, not an accepted review, and not a
support-state transition.

The book remains broad, but this cycle does not try to make all 54 chapter
claims equally defensible. It selects five contribution tracks for v1.x focus
and marks three of them as deep-work tracks. The other two remain selected but
supporting for this cycle.

## Selection Boundary

| Field | Value |
|---|---|
| Selected contribution tracks | 5 |
| Deep-work tracks this cycle | 3 |
| Deep-work cap | At most 3 tracks per v1.x cycle |
| Active evidence-cycle lanes | 7 selected chapter lanes, 47 planned-only lanes |
| Chapter core support effect | None; all 54 chapter core claims remain `argument`. |
| Non-core support effect | Existing non-core transitions remain scoped to accepted records only. |
| Release effect | None; no reader, ebook, PDF, DOCX, audio, DOI, or archive artifact is approved. |

## Track Selection

| Track ID | Track | Cycle status | Primary lane anchors | Current evidence surface | Next hard blocker |
|---|---|---|---|---|---|
| `living-evidence-book-methodology` | Living evidence book methodology | deep-work | `living-book-methodology`; `evidence-states-and-claim-discipline` | `docs/non_core_evidence_ledger.md`; `docs/phase5_harness_runner.md`; `docs/external_review_status.md`; `external_reviews/request_updates/consolidation_review_request_2026-06-29.json`; `docs/v1_0_release_gate_audit.md`; `docs/defended_contribution_prior_art_positioning.md` | Accepted external review and a tighter novelty note distinguishing the living-book method from model-reporting, reproducibility, benchmark, and governance-framework practice. |
| `claim-support-states-and-evidence-laundering-prevention` | Claim support states and evidence laundering prevention | selected-supporting | `evidence-states-and-claim-discipline`; `executable-specifications-and-lean-proof-envelope` | `appendices/C_claim_evidence_matrix.qmd`; `claim_decisions/v1_0_core_claim_no_promotion.json`; `docs/core_claim_transition_coverage.md`; `docs/non_core_evidence_ledger.md`; `docs/defended_contribution_prior_art_positioning.md` | Reviewer pressure test and a demotion/refutation case study before making a defended methodology claim. |
| `governed-self-improvement-boundary` | Governed self-improvement boundary | deep-work | `recursive-self-improvement-boundaries`; `project-theseus-as-report-first-implementation-reference`; `executable-specifications-and-lean-proof-envelope` | `lean/AsiStackProofs/SelfImprovement.lean`; `docs/proof_depth_classification.md`; `docs/proof_adequacy_review.md`; `docs/theseus_report_import_slice.md`; `experiments/theseus_import/results/2026-06-29-local.json` | Clean Theseus replay or archived public fixture, plus external safety/formal review of the boundary. |
| `proof-carrying-claims-and-ai-contracts` | Proof-carrying claims and proof-carrying AI contracts | deep-work | `circle-calculus-and-proof-carrying-ai-contracts`; `executable-specifications-and-lean-proof-envelope` | `docs/circle_external_receipt_slice.md`; `docs/circle_public_replay_consumer_gate.md`; `experiments/circle_public_replay/results/2026-06-29-local.json`; `docs/proof_carrying_claim_harness.md`; `docs/defended_contribution_prior_art_positioning.md` | Clean Circle replay, public contract pack, or archived upstream pack; stronger receipt negative controls before broader claims. |
| `costed-routing-residual-accounting-resource-discipline` | Costed routing, residual accounting, and resource discipline | selected-supporting | `resource-economics-and-token-budgets`; `readiness-gates-residual-escrow-and-quarantine` | `docs/costed_route_resource_slice.md`; `experiments/costed_route_resource_slice/results/2026-06-29-local.json`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `docs/readiness_residual_harness.md`; `docs/defended_contribution_prior_art_positioning.md` | Larger public trace with quality, adequacy, displaced-cost, fallback, and residual accounting; no economic overclaim; residual-governance comparator gap remains open. |

## Why These Three Deep-Work Tracks

The deep-work tracks are selected because their next evidence artifacts are
public-safe, externally reviewable, and capable of failing:

- **Living evidence book methodology** has the clearest current contribution:
  a CI-gated living book with claim-state, source, proof, test, reader, release,
  non-claim, and external-review controls.
- **Governed self-improvement boundary** is the most safety-critical
  architecture claim and already has safety-critical Lean depth plus a bounded
  Project Theseus static import.
- **Proof-carrying claims and proof-carrying AI contracts** has a concrete
  Circle receipt slice and an ASI-side consumer gate with mutation controls.

The selected-supporting tracks stay visible because they constrain the deep
tracks, but this cycle should not widen into five simultaneous deep campaigns.

## Evidence And No-Promotion Boundaries

- `docs/v1_x_active_evidence_cycle.md` remains the source for selected chapter
  lanes and planned-only lanes.
- `docs/per_chapter_evidence_plan.md` remains the 54-chapter backlog.
- This record does not create new fixtures, tests, source records, proof
  results, external-review results, or support-state transitions.
- This record does not promote any chapter core claim above `argument`.
- This record does not claim selected tracks are complete at A+ depth.
- `docs/defended_contribution_prior_art_positioning.md` is a source-noted
  comparator record only; it is not novelty proof, accepted external review, or
  support-state movement.
- Non-core transitions remain limited to their accepted evidence-transition
  records.
- A selected track can be revised, demoted, split, retired, or blocked if
  external review, prior-art work, proof work, replay work, or reader review
  shows that the target is wrong, already solved, too weakly sourced, not
  novel, or not public-safe.

## Release-Gate Effect

This record satisfies the selection part of the v1.x defended-contribution
release gate: the project names three to five contribution tracks and at most
three deep-work tracks for the current cycle. It does not satisfy the evidence
depth required for a v1.x evidence release. That still requires accepted
review, prior-art comparison, stronger replay/proof artifacts, and explicit
release records where applicable.

## Non-Claims

- This record does not create evidence.
- This record does not approve any merge, chapter rewrite, reader artifact,
  ebook artifact, PDF, DOCX, audio, DOI, or archive.
- This record does not change `book_structure.json`.
- This record does not change Appendix C support states.
- This record does not create source-derived, prototype-backed,
  synthetic-test-backed, empirical-test-backed, or external-literature-backed
  support for any chapter core claim.
