# Chapter Consolidation Release-Stability Review

Last updated: 2026-06-30

Decision: defer all remaining unexecuted consolidation packages for the
current reader-curation cycle after the Part I pilot and conservative
compression merge execution.

This record creates a `deferred_for_release` reader-work outcome for the
remaining pending merge and fold packages. It records that the Part I pilot and
conservative compression merge are no longer deferred. This review itself does
not edit `book_structure.json`, does not execute any additional remaining merge
or fold, does not approve any reader artifact, does not create external review,
and does not change support states.

The current canonical manifest has 51 chapters after the executed conservative compression merge.

## Reviewed Inputs

- `docs/chapter_consolidation_sequence.md`
- `docs/chapter_consolidation_decision_review.md`
- `docs/chapter_consolidation_full_review_packet.md`
- `docs/chapter_consolidation_url_history_policy.md`
- all current dry-run merge packages and destination drafts listed in the full
  review packet
- all current fold dispositions listed in the full review packet
- `docs/v1_x_beyond_sota_roadmap.md`
- `docs/reader_chapter_review_matrix.md`
- `editions/reader_manuscript/v1_0/manifest.json`
- `editions/reader_manuscript/v1_0/reconciliation_report.md`

This review source is internal release-control review. It is not human review,
not external review, not peer review, and not accepted review evidence.

## Decision Rationale

The consolidation critique remains directionally correct: several current
chapter clusters repeat the same rendered skeleton around adjacent ideas. The
destination drafts and fold dispositions are useful review objects, but they
are not accepted canonical chapters.

Executing any remaining merge now would require coordinated manifest, outline,
Appendix C, Appendix K, proof-manifest, source, reader, handoff, URL/history,
and validation changes. Each remaining package still needs a recorded decision
that the destination is stronger than the source chapters as one chapter.

At the same time, the human-reader manuscript cannot stay blocked indefinitely
while every consolidation package waits for outside review. The practical
current release choice is to preserve the 51-chapter manifest after the Part I
pilot and conservative compression merge for the current reader-curation cycle, record remaining duplicate skeletons as
accepted temporary debt, and continue reader prose work with explicit
consolidation caveats.

This is a deferral, not a rejection. It keeps the merge/fold queue alive for a
future execution package for the remaining queue.

## Reader Curation Outcome Table

| Package | Prior package state | Reader-work outcome | Reason | Reader curation consequence |
|---|---|---|---|---|
| Constitutional alignment and agency/corrigibility | `review_ready` | `executed` | The 2026-06-30 pilot accepted the destination chapter, preserved the retired URL through a historical stub, archived the source chapter, and kept support at `argument`. | Curated prose should target `constitutional-alignment-substrate` as the consolidated chapter. |
| Value conflict and contestable governance | `review_ready` | `executed` | The 2026-06-30 pilot accepted the destination chapter, preserved the retired URL through a historical stub, archived the source chapter, and kept support at `argument`. | Curated prose should target `moral-uncertainty-and-value-conflict` as the consolidated chapter. |
| Compression and residual honesty | `review_ready` | `executed` | The 2026-06-30 conservative merge accepted the destination chapter, folded Generate-Verify-Repair into compact-generative systems, preserved the retired URL through a historical stub, archived the source chapter, retained RankFold/NeuralFold as a standalone technique chapter, and kept support at `argument`. | Curated prose should target `compact-generative-systems-and-residual-honesty` as the merged chapter plus `rankfold-neuralfold-and-artifact-compression` as the retained technique chapter. |
| Intent and executable contracts | `review_ready` | `deferred_for_release` | The destination draft is plausible, but the current release keeps intent-to-execution and command-interface chapters separate until the contract boundary is reviewed. | Curated prose may proceed for both Part II source chapters; `human-intent-as-a-formal-input` keeps its existing handoff caveat. |
| Static context ABI | `review_ready` | `deferred_for_release` | The typed-page/certificate fold is plausible, but VCM addressing and semantic-cell certificate ownership need review before canonical identity changes. | Curated prose may proceed for `virtual-context-abi` and `semantic-pages-context-cells-and-certificates` with a static-ABI merge caveat. |
| Proof-carrying claims and adversarial review | `review_ready` | `deferred_for_release` | The destination draft may reduce repetition, but proof-carrying claim tiers and tribunal review need reviewer judgment before they become one chapter. | Curated prose may proceed for both verification/review source chapters with a proof/review merge caveat. |
| Planning and DAG control | `review_ready` | `deferred_for_release` | The destination draft is plausible, but planning-control and PlanForge DAG ownership should be reviewed before a canonical merge. | Curated prose may proceed for both planning source chapters with a planning/DAG merge caveat. |
| MoECOT runtime fold | `fold_disposition_ready` | `deferred_for_release` | The fold remains likely while MoECOT is source-blocked, but folding into routing heads still needs an execution package. | Curated prose may proceed only if it preserves the source-blocked boundary and future fold/restoration condition. |
| Simulation fidelity fold | `fold_disposition_ready` | `deferred_for_release` | The physical-constraint idea may belong in resource economics, but the current release keeps the chapter boundary until fold execution is accepted. | Curated prose may proceed only if it preserves the feasibility-bound and future fold caveat. |
| Semantic representation fold | `fold_disposition_ready` | `deferred_for_release` | The fold remains dependent on a later representation-package execution decision after the conservative compression merge retained RankFold/NeuralFold as a standalone technique chapter. | Curated prose may proceed only if it preserves the dependency on the future representation-package decision. |

## Accepted Temporary Debt

For the current reader-curation cycle, the release accepts these forms of
temporary debt:

- repeated Problem, Insufficiency, Mechanism, Interface, Evidence,
  Implementation, and Handoff skeletons in the pending clusters;
- stable chapter IDs and URLs for the 51 current manifest chapters plus historical stubs for the two folded Part I slugs and the folded GVR slug;
- reader curation against source chapter boundaries that may later be merged or
  folded;
- reconciliation work if a later consolidation package executes and supersedes
  a curated source chapter.

This debt is allowed because the alternative would either freeze human-reader
work or execute unreviewed manifest changes.

## Deferred Chapter ID Set

The deferred-for-release reader-work outcome applies to these current manifest
chapter IDs:

- `constitutional-alignment-substrate`
- `moral-uncertainty-and-value-conflict`
- `intent-to-execution-contracts`
- `command-contracts-and-semantic-interfaces`
- `planning-as-a-control-layer`
- `planforge-dags-and-intelligence-arbitrage`
- `virtual-context-abi`
- `semantic-pages-context-cells-and-certificates`
- `spinoza-verification-and-proof-carrying-claims`
- `unified-adaptive-tribunal-and-adversarial-review`
- `routing-heads-and-specialist-cores`
- `moecot-runtime-and-multi-core-orchestration`
- `compact-generative-systems-and-residual-honesty`
- `rankfold-neuralfold-and-artifact-compression`
- `semantic-representation-and-tree-structured-models`
- `simulation-fidelity-and-physical-constraints`
- `resource-economics-and-token-budgets`

## Revisit Conditions

Revisit the deferred packages when one of these becomes true:

- Corben, an editor, or an external reviewer accepts, revises, rejects, or
  gives no-opinion feedback on a destination draft or fold disposition;
- duplicate skeletons become a blocking issue during human manuscript review;
- URL/history treatment can be implemented and validated for a specific
  accepted merge or fold;
- a chapter-level evidence, proof, source, or external-grounding update makes
  the separate chapter boundary clearly stronger or clearly weaker;
- a future major-version reader release requires a stable table-of-contents
  decision before artifact approval.

## Requirements For Curated Reader Passes Inside Deferred Packages

Every curated reader pass inside a deferred package must:

- record the relevant consolidation caveat in its prose-pass review note;
- avoid changing claim meaning, support states, source boundaries, proof/test
  status, implementation horizons, or release records;
- avoid claiming the merge, fold, or retention decision has been accepted;
- preserve source IDs, proof hooks, implementation horizons, and non-claims so
  a future execution package can reconcile the prose;
- keep release blockers active until a reader release record explicitly clears
  them.

## Non-Claims

- This review does not execute any additional remaining merge or fold.
- This review does not reject any package permanently.
- This review does not approve any destination draft.
- This review records that the Part I pilot and conservative compression merge implemented historical stubs and changed chapter count in their separate execution packages.
- This review does not create human review, external review, peer review, proof
  evidence, test evidence, benchmark evidence, source-derived evidence, or
  artifact-review evidence.
- This review does not promote, demote, deprecate, or refute any chapter core
  claim.
- This review does not approve EPUB, DOCX, PDF, HTML, audio, or
  audio-embedded EPUB artifacts.
