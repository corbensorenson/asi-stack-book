# Chapter Consolidation Decision Review

Last updated: 2026-06-29

Decision: defer manifest consolidation for the current v1.x cycle.

This review covers the governed Part I alignment/governance consolidation
pilot. It does not edit `book_structure.json`, does not remove rendered
chapters, does not rewrite chapter files, does not change source mappings, does
not change proof targets, does not change support states, does not authorize a merge, and does not approve a reader artifact.

## Reviewed Inputs

- `docs/chapter_consolidation_pilot_plan.md`
- `docs/chapter_consolidation_dry_run_constitutional_alignment.md`
- `docs/chapter_consolidation_dry_run_contestable_governance.md`
- `docs/chapter_consolidation_destination_draft_constitutional_alignment.md`
- `docs/chapter_consolidation_destination_draft_contestable_governance.md`
- `docs/chapter_consolidation_external_review_packet.md`
- `docs/v1_x_beyond_sota_roadmap.md`
- `docs/chapter_external_grounding_status.md`
- `docs/external_sota_positioning_audit.md`
- `docs/reader_chapter_review_matrix.md`
- `docs/proof_depth_classification.md`
- `docs/proof_adequacy_review.md`
- `book_structure.json`
- `docs/book_outline.md`

## Decision

The two proposed destination chapters remain viable consolidation candidates:

- **Constitutional Alignment: Agency, Dignity, and Corrigibility**
- **Moral Uncertainty, Value Conflict, and Contestable Governance**

Both dry-run packages now preserve source IDs, external comparators, Appendix C
claim dispositions, Lean proof tags, harness rows, reader repairs, handoff
repairs, implementation horizons, generated-file expectations, validation
commands, and no-support-state-change boundaries.

Destination drafts now exist for both proposed pilot chapters:

- **Constitutional Alignment: Agency, Dignity, and Corrigibility**
- **Moral Uncertainty, Value Conflict, and Contestable Governance**

They are review-ready objects, not accepted review results. They give human or
external reviewers two merged chapter skeletons to judge before any canonical
chapter identity changes.

`docs/chapter_consolidation_external_review_packet.md` is now the supplemental
request surface for that judgment. It asks reviewers to execute, revise, defer,
or reject each proposed merge and preserves the boundary that review input is
not source evidence, proof evidence, support-state movement, or artifact
approval.

The manifest merge is deferred because the next honest decision needs human or
external review of the actual chapter-shape tradeoff before canonical chapter
identity changes. The dry-runs show that a merge is technically possible, but
they do not yet prove that the resulting reader flow is better, that the public
URL policy is acceptable, that the folded chapter history should disappear
from rendered navigation, or that the merged prose has been written and
reviewed as one chapter rather than only planned.

## Why Deferral Is The Right Current Action

- The current manifest still validates as 54 chapters, and many release-control
  surfaces intentionally count and review those 54 chapters.
- `docs/book_outline.md`, Appendix C, reader-review matrices, active evidence
  lanes, status snapshots, external-grounding reports, and rendered handoffs
  would all need coordinated updates for a real merge.
- The two dry-run packages name the required source/proof/claim/reader
  reconciliation. The two destination drafts now supply merged prose for both
  proposed chapters, but neither has been accepted by a human or external
  reviewer and neither is a canonical chapter.
- The external review request is still open and no independent external review
  has been accepted into the repo.
- The project has no redirect policy yet for retired chapter URLs.
- Human-reader curation may proceed on chapters outside the pending
  consolidation cluster without locking in the duplicate Part I skeletons.

## Allowed Next Work

human-reader curation may proceed for the roadmap's pilot chapters that are not
inside the pending Part I consolidation cluster:

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `recursive-self-improvement-boundaries`
- `circle-calculus-and-proof-carrying-ai-contracts`
- `artifact-steward-agents-and-living-project-governance`

`human-intent-as-a-formal-input` may receive local prose improvements, but any
reader graduation should account for the future handoff to a possible
Constitutional Alignment destination chapter. The four pending consolidation
source chapters should avoid broad reader-only polish until their merge is
executed or permanently rejected, because polishing duplicate skeletons would
preserve the repetition the pilot is meant to remove.

## Conditions To Execute A Future Merge

Before either manifest merge can proceed, require:

- a human- or external-reviewed destination chapter draft with one chapter
  skeleton, not two pasted skeletons;
- a public URL or redirect policy for the folded chapter;
- updated `book_structure.json` and `docs/book_outline.md` in the same merge
  commit;
- Appendix C claim-history treatment for the folded core row;
- source and external-source target updates through inventory/source-note
  workflow;
- proof-tag movement without retiring the existing Lean modules;
- regenerated reader review matrices and handoff checks;
- updated chapter external-grounding and external-SOTA ledgers;
- full local validation, Lean build, and Quarto render;
- explicit no-support-state-change language unless a separate accepted
  evidence-transition record justifies movement.

## Conditions To Permanently Reject A Merge

A future review should reject a proposed merge if:

- the merged chapter reads as two chapters pasted together;
- a source, subclaim, proof hook, harness row, implementation horizon, or
  reader path is silently lost;
- the public URL or redirect behavior is unacceptable;
- external review says separate chapters are clearer for safety, governance, or
  citation reasons;
- the merged core claim becomes broader than the retained evidence boundaries;
- the merge would pressure support-state movement without new evidence.

## Release Boundary

No support state changes. No chapter core claim is promoted. No chapter is
merged. No source-derived support, proof result, test result, external-review
result, reader release, EPUB, DOCX, PDF, audio artifact, DOI, or archive is
created by this decision.
