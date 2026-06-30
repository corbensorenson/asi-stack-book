# Chapter Consolidation Release-Stability Review

Last updated: 2026-06-30

Decision: defer all unexecuted consolidation packages for the current
reader-curation cycle.

This record creates a `deferred_for_release` reader-work outcome for the
pending merge and fold packages. It does not edit `book_structure.json`, does
not merge chapters, does not fold chapters, does not retire chapter URLs, does
not change Appendix C, does not change Appendix K, does not change proof
targets, does not change source records, does not approve any reader artifact,
does not create external review, and does not change support states.

The current canonical manifest remains 54 chapters.

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

Executing any merge now would require coordinated manifest, outline, Appendix
C, Appendix K, proof-manifest, source, reader, handoff, URL/history, and
validation changes. It would also require human or external judgment that the
destination draft is stronger than the source chapters as one chapter. That
review has been requested but not accepted into the repository.

At the same time, the human-reader manuscript cannot stay blocked indefinitely
while every consolidation package waits for outside review. The practical
current release choice is to preserve the 54-chapter manifest for the current
reader-curation cycle, record the duplicate skeletons as accepted temporary
debt, and continue reader prose work with explicit consolidation caveats.

This is a deferral, not a rejection. It keeps the merge/fold queue alive for a
future execution package.

## Reader Curation Outcome Table

| Package | Prior package state | Reader-work outcome | Reason | Reader curation consequence |
|---|---|---|---|---|
| Constitutional alignment and agency/corrigibility | `review_ready` | `deferred_for_release` | Destination draft is review-ready, but no human/external review has accepted the merged chapter and no retired URL treatment has been implemented. | Curated prose may proceed for both source chapters only with a caveat that a future Constitutional Alignment merge may supersede the current chapter boundary. |
| Value conflict and contestable governance | `review_ready` | `deferred_for_release` | Destination draft is review-ready, but fork/exit/audit interfaces and value-conflict records need human judgment before the chapter identity changes. | Curated prose may proceed for both source chapters only with a caveat that a future contestable-governance merge may supersede the current chapter boundary. |
| Compression and residual honesty | `review_ready` | `deferred_for_release` | The full-versus-conservative merge choice still needs review, especially whether RankFold/NeuralFold owns enough concrete technique to remain standalone. | Curated prose may proceed for Compact Generative Systems, Generate-Verify-Repair, and RankFold/NeuralFold with explicit merge-debt caveats. |
| Intent and executable contracts | `review_ready` | `deferred_for_release` | The destination draft is plausible, but the current release keeps intent-to-execution and command-interface chapters separate until the contract boundary is reviewed. | Curated prose may proceed for both Part II source chapters; `human-intent-as-a-formal-input` keeps its existing handoff caveat. |
| Static context ABI | `review_ready` | `deferred_for_release` | The typed-page/certificate fold is plausible, but VCM addressing and semantic-cell certificate ownership need review before canonical identity changes. | Curated prose may proceed for `virtual-context-abi` and `semantic-pages-context-cells-and-certificates` with a static-ABI merge caveat. |
| Proof-carrying claims and adversarial review | `review_ready` | `deferred_for_release` | The destination draft may reduce repetition, but proof-carrying claim tiers and tribunal review need reviewer judgment before they become one chapter. | Curated prose may proceed for both verification/review source chapters with a proof/review merge caveat. |
| Planning and DAG control | `review_ready` | `deferred_for_release` | The destination draft is plausible, but planning-control and PlanForge DAG ownership should be reviewed before a canonical merge. | Curated prose may proceed for both planning source chapters with a planning/DAG merge caveat. |
| MoECOT runtime fold | `fold_disposition_ready` | `deferred_for_release` | The fold remains likely while MoECOT is source-blocked, but folding into routing heads still needs an execution package. | Curated prose may proceed only if it preserves the source-blocked boundary and future fold/restoration condition. |
| Simulation fidelity fold | `fold_disposition_ready` | `deferred_for_release` | The physical-constraint idea may belong in resource economics, but the current release keeps the chapter boundary until fold execution is accepted. | Curated prose may proceed only if it preserves the feasibility-bound and future fold caveat. |
| Semantic representation fold | `fold_disposition_ready` | `deferred_for_release` | The fold depends on the compression/representation package decision, which is deferred for this release. | Curated prose may proceed only if it preserves the dependency on the future compression/representation decision. |

## Accepted Temporary Debt

For the current reader-curation cycle, the release accepts these forms of
temporary debt:

- repeated Problem, Insufficiency, Mechanism, Interface, Evidence,
  Implementation, and Handoff skeletons in the pending clusters;
- stable chapter IDs and URLs for all 54 current chapters;
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
- `agency-dignity-and-corrigibility`
- `moral-uncertainty-and-value-conflict`
- `governance-rights-fork-exit-and-audit`
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
- `generate-verify-repair-compression`
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

- This review does not execute any merge or fold.
- This review does not merge chapters.
- This review does not fold chapters.
- This review does not reject any package permanently.
- This review does not approve any destination draft.
- This review does not implement redirects or historical stubs.
- This review does not change `book_structure.json`.
- This review does not change chapter count.
- This review does not create human review, external review, peer review, proof
  evidence, test evidence, benchmark evidence, source-derived evidence, or
  artifact-review evidence.
- This review does not promote, demote, deprecate, or refute any chapter core
  claim.
- This review does not approve EPUB, DOCX, PDF, HTML, audio, or
  audio-embedded EPUB artifacts.
