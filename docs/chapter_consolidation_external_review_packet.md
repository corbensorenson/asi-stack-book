# Chapter Consolidation External Review Packet

Last updated: 2026-06-29

This packet is a supplemental review surface for the governed Part I
alignment/governance consolidation pilot. It is designed for human or external
reviewers who can judge chapter shape, source/proof preservation, governance
clarity, and reader flow before any canonical manifest merge is attempted.

Public review request issue:
<https://github.com/corbensorenson/asi-stack-book/issues/1>

## Review Boundary

This packet does not edit `book_structure.json`, merge chapters, delete rendered
pages, change URLs, change source mappings, change proof targets, change
support states, approve a reader artifact, or create an external-review result.
It is a request surface. A future review response should be recorded separately
before it is treated as accepted review input.

Reviewer comments are review input, not source evidence, proof results,
benchmark evidence, support-state promotion, or artifact approval. Reviewers
are asked to execute, revise, defer, or reject each proposed merge. A reviewer
cannot promote a claim unless a separate accepted evidence-transition record
later names independently source-noted material, proof results, replay
artifacts, test results, or artifact-review evidence.

## Review Inputs

Reviewers should read these files in order:

1. `docs/chapter_consolidation_pilot_plan.md`
2. `docs/chapter_consolidation_sequence.md`
3. `docs/chapter_consolidation_dry_run_constitutional_alignment.md`
4. `docs/chapter_consolidation_destination_draft_constitutional_alignment.md`
5. `docs/chapter_consolidation_dry_run_contestable_governance.md`
6. `docs/chapter_consolidation_destination_draft_contestable_governance.md`
7. `docs/chapter_consolidation_decision_review.md`

Optional context:

- `docs/v1_x_beyond_sota_roadmap.md`
- `docs/chapter_external_grounding_status.md`
- `docs/external_sota_positioning_audit.md`
- `docs/proof_depth_classification.md`
- `docs/proof_adequacy_review.md`
- `docs/reader_chapter_review_matrix.md`
- `book_structure.json`
- `docs/book_outline.md`

## Proposed Decisions Under Review

| Proposed destination | Source chapters | Default current decision |
|---|---|---|
| **Constitutional Alignment: Agency, Dignity, and Corrigibility** | `constitutional-alignment-substrate`; `agency-dignity-and-corrigibility` | Defer manifest merge until review accepts, revises, or rejects the destination shape. |
| **Moral Uncertainty, Value Conflict, and Contestable Governance** | `moral-uncertainty-and-value-conflict`; `governance-rights-fork-exit-and-audit` | Defer manifest merge until review accepts, revises, or rejects the destination shape. |

## Review Questions

1. Does each destination draft read as one chapter with one skeleton, or does it
   still read as two chapters pasted together?
2. Does either destination draft lose a source, external comparator, subclaim,
   proof tag, Lean module, harness lane, implementation horizon, reader path, or
   handoff that should remain visible?
3. Does either merged core claim become broader than the evidence boundary
   recorded in Appendix C, the proof limitations, or the source crosswalks?
4. Would the merge make the human-reader book clearer, or would separate
   chapters better preserve safety, governance, citation, or teaching clarity?
5. Are the proposed stable-ID and retired-file defaults acceptable for a public
   living book, or should the project add an explicit redirect/historical-note
   mechanism before any manifest change?
6. Which additional external comparator families should be source-noted before
   either destination chapter becomes canonical?
7. Should the project execute, revise, defer, or reject each proposed merge?

## Response Template

Reviewers can respond in GitHub issue #1 or in a separate review note using
this shape:

| Field | Reviewer input |
|---|---|
| Reviewer background | Safety, formal methods, governance/evals, agent systems, ML systems, publishing, technical editing, or other. |
| Review scope | Which dry-run packages, destination drafts, roadmap sections, appendices, rendered pages, or source surfaces were reviewed. |
| Constitutional Alignment decision | Execute, revise, defer, reject, or no opinion, with reason. |
| Contestable Governance decision | Execute, revise, defer, reject, or no opinion, with reason. |
| Highest-severity issue | The most serious preservation, evidence, novelty, reader-flow, support-boundary, proof-scope, or public-URL issue. |
| Missing source or comparator | Any external paper, standard, system, benchmark, or citation family to source-note before merge. |
| Specific required change | Source to add, proof tag to preserve, section to rewrite, URL policy to add, claim to narrow, or blocker to record. |
| Attributability | Public attributable, public anonymous, private/non-attributable, or other. |

## Accepted Review Record Requirements

A future accepted review record should name:

- reviewer background or anonymized expertise area;
- review date;
- exact files, rendered pages, appendices, or artifacts reviewed;
- decision for each proposed merge;
- required revisions or blockers;
- source/proof/claim/reader preservation concerns;
- any claim that appears wrong, already solved, too weakly sourced, not novel,
  or over-framed;
- publication and attribution boundary;
- exact support-state, release, and artifact non-claims.

## Non-Claims

- This packet does not mean an external review has happened.
- This packet does not authorize either merge.
- This packet does not change `book_structure.json`.
- This packet does not change any source, proof, test, reader, artifact, or
  support-state surface.
- This packet does not approve v1.x, reader, ebook, PDF, DOCX, audio, DOI, or
  archive readiness.
