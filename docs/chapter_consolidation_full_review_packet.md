# Chapter Consolidation Full Review Packet

Last updated: 2026-06-29

This packet is a supplemental review surface for the governed consolidation
sequence. It is designed for human or external reviewers who can judge whether
the current 54-chapter living-book shape should execute, revise, defer, or
reject specific merge/fold packages before any canonical manifest edit.

Public review request issue:
<https://github.com/corbensorenson/asi-stack-book/issues/1>

## Review Boundary

This packet does not edit `book_structure.json`, merge chapters, fold chapters,
delete rendered pages, change URLs, change source mappings, change proof
targets, change support states, approve reader artifacts, or create an
external-review result. It is a request surface. A future review response must
be recorded separately before it is treated as accepted review input.

Reviewer comments are review input, not source evidence, proof results,
benchmark evidence, support-state promotion, or artifact approval. Reviewers
are asked to choose execute, revise, defer, reject, or no opinion for each
package. A reviewer cannot promote a claim unless a separate accepted
evidence-transition record later names independently source-noted material,
proof results, replay artifacts, test results, or artifact-review evidence.

## Review Inputs

Reviewers should read these files first:

1. `docs/v1_x_beyond_sota_roadmap.md`
2. `docs/chapter_consolidation_sequence.md`
3. `docs/chapter_consolidation_decision_review.md`
4. `docs/chapter_consolidation_external_review_packet.md`

Then read the package files relevant to any decision they want to make:

| Package | Review files |
|---|---|
| Constitutional alignment and agency/corrigibility | `docs/chapter_consolidation_dry_run_constitutional_alignment.md`; `docs/chapter_consolidation_destination_draft_constitutional_alignment.md` |
| Value conflict and contestable governance | `docs/chapter_consolidation_dry_run_contestable_governance.md`; `docs/chapter_consolidation_destination_draft_contestable_governance.md` |
| Compression and residual honesty | `docs/chapter_consolidation_dry_run_compression.md`; `docs/chapter_consolidation_destination_draft_compression.md` |
| Intent and executable contracts | `docs/chapter_consolidation_dry_run_intent_contracts.md`; `docs/chapter_consolidation_destination_draft_intent_contracts.md` |
| Static context ABI | `docs/chapter_consolidation_dry_run_context_abi.md`; `docs/chapter_consolidation_destination_draft_context_abi.md` |
| Proof-carrying claims and adversarial review | `docs/chapter_consolidation_dry_run_verification_review.md`; `docs/chapter_consolidation_destination_draft_verification_review.md` |
| Planning and DAG control | `docs/chapter_consolidation_dry_run_planning_dag.md`; `docs/chapter_consolidation_destination_draft_planning_dag.md` |
| MoECOT runtime fold | `docs/chapter_consolidation_fold_moecot_runtime.md` |
| Simulation fidelity fold | `docs/chapter_consolidation_fold_simulation_fidelity.md` |
| Semantic representation fold | `docs/chapter_consolidation_fold_semantic_representation.md` |

Optional context:

- `docs/book_outline.md`
- `book_structure.json`
- `docs/chapter_external_grounding_status.md`
- `docs/external_sota_positioning_audit.md`
- `docs/proof_depth_classification.md`
- `docs/proof_adequacy_review.md`
- `docs/reader_chapter_review_matrix.md`
- `docs/non_core_evidence_ledger.md`
- rendered pages for any source or destination chapters under review

## Decision Queue Under Review

The current default is no manifest edit. Each package needs a reviewed
decision before execution.

| Order | Package | Current state | Review decision needed |
|---|---|---|---|
| 1 | Constitutional Alignment: Agency, Dignity, and Corrigibility | `review_ready` | Execute, revise, defer, reject, or no opinion. |
| 2 | Moral Uncertainty, Value Conflict, and Contestable Governance | `review_ready` | Execute, revise, defer, reject, or no opinion. |
| 3 | Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty | `review_ready` | Execute full merge, execute conservative merge, revise, defer, reject, or no opinion. |
| 4 | Command Contracts: From Intent to Executable Work | `review_ready` | Execute, revise, defer, reject, or no opinion. |
| 5 | The Virtual Context ABI: Typed Pages, Cells, and Certificates | `review_ready` | Execute, revise, defer, reject, or no opinion. |
| 6 | Proof-Carrying Claims and Adversarial Review | `review_ready` | Execute, revise, defer, reject, or no opinion. |
| 7 | Planning as a Control Layer: DAGs and Intelligence Arbitrage | `review_ready` | Execute, revise, defer, reject, or no opinion. |
| 8 | MoECOT Runtime Crosswalk fold | `fold_disposition_ready` | Execute fold, revise, defer, reject/retain, or no opinion. |
| 9 | Simulation Fidelity and Claim Transport fold | `fold_disposition_ready` | Execute fold, revise, defer, reject/retain, or no opinion. |
| 10 | Semantic Representation Leasing fold | `fold_disposition_ready` | Execute fold after destination-package review, revise, defer, reject/retain, or no opinion. |

If any package is accepted for execution, it should still be executed one
package per commit, with source/proof/claim/reader reconciliation, URL/history
policy, local validation, and Quarto render in that execution commit.

## Review Questions

1. Does each destination draft or fold disposition reduce repeated skeleton
   load while preserving the idea as a named mechanism, subclaim, proof hook,
   record, source row, reader section, or restoration condition?
2. Does a proposed destination read as one chapter with one skeleton, or does
   it still read as source chapters pasted together?
3. Does any package lose a source ID, external comparator, subclaim, proof tag,
   Lean module, schema, fixture, harness row, implementation horizon, reader
   path, or handoff that should remain visible?
4. Does any proposed core claim become broader than Appendix C, the source
   crosswalks, proof limitations, or evidence-transition boundaries allow?
5. Would execution make the human-reader book clearer, or would separate
   chapters better preserve safety, governance, citation, teaching, or evidence
   clarity?
6. Are the proposed dependency constraints correct, especially the semantic
   representation fold's dependency on the compression/representation package?
7. Are the proposed stable-ID, URL, redirect, or historical-note defaults
   acceptable for a public living book?
8. Which external comparator families should be source-noted before any package
   becomes canonical?
9. Which packages should be executed in v1.x, which should be revised, which
   should be deferred, and which should be rejected or retained standalone?

## Response Template

Reviewers can respond in GitHub issue #1 or in a separate review note using
this shape:

| Field | Reviewer input |
|---|---|
| Reviewer background | Safety, formal methods, governance/evals, agent systems, ML systems, publishing, technical editing, or other. |
| Review scope | Which packages, destination drafts, fold dispositions, roadmap sections, appendices, rendered pages, or source surfaces were reviewed. |
| Package decisions | Execute, revise, defer, reject, or no opinion for each reviewed package, with reason. |
| Highest-severity issue | The most serious preservation, evidence, novelty, reader-flow, support-boundary, proof-scope, or public-URL issue. |
| Missing source or comparator | Any external paper, standard, system, benchmark, or citation family to source-note before merge/fold execution. |
| Specific required change | Source to add, proof tag to preserve, section to rewrite, URL policy to add, claim to narrow, dependency to revise, or blocker to record. |
| Attributability | Public attributable, public anonymous, private/non-attributable, or other. |

## Accepted Review Record Requirements

A future accepted review record should name:

- reviewer background or anonymized expertise area;
- review date;
- exact files, rendered pages, appendices, or artifacts reviewed;
- decision for each package reviewed;
- required revisions or blockers;
- source/proof/claim/reader preservation concerns;
- any claim that appears wrong, already solved, too weakly sourced, not novel,
  or over-framed;
- publication and attribution boundary;
- exact support-state, release, and artifact non-claims.

## Non-Claims

- This packet does not mean an external review has happened.
- This packet does not authorize any merge or fold.
- This packet does not change `book_structure.json`.
- This packet does not change any source, proof, test, reader, artifact, or
  support-state surface.
- This packet does not approve v1.x, reader, ebook, PDF, DOCX, audio, DOI, or
  archive readiness.
