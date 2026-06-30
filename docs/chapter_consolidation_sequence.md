# Governed Chapter Consolidation Sequence

Last updated: 2026-06-30

This record preserves the consolidation sequence accepted for roadmap
execution after review of the latest 54-to-44/47 chapter-shape critique. It is a
planning and release-control artifact plus an execution ledger for completed
packages, not source evidence, not an external review result, and not a
support-state transition.

The recommendation has teeth: most of the current repetition is not caused by
bad ideas. It comes from rendering adjacent ideas as separate chapters that
repeat the same Problem, Insufficiency, Mechanism, Interface, Evidence,
Implementation, and Handoff skeleton. The roadmap response is governed
re-consolidation: fewer deeper chapter-owning artifacts, with every useful idea
preserved as a section, subclaim, source mapping, proof hook, reader path,
implementation horizon, or explicit retirement decision.

The Part I pilot, the conservative compression merge, the intent/contracts
merge, the MoECOT runtime fold, the simulation-fidelity fold, the static
context ABI merge, and the verification/adversarial-review merge have now
executed through `book_structure.json`; the current canonical book has 46
manifest chapters. The remaining candidate packages still require their own
package-specific decision and execution commit before any further manifest
change. This is not a support-state transition. The current canonical count is
46 manifest chapters after the executed Part I pilot, conservative compression
merge, intent/contracts merge, MoECOT runtime fold, simulation-fidelity fold,
static context ABI merge, and verification/adversarial-review merge.

## Decision Boundary

- Accept the critique as directionally correct roadmap guidance.
- Do not run a broad 54-to-44 manifest edit from the critique alone.
- Do not target a fixed chapter count. A 44-chapter aggressive shape and a
  roughly 47-chapter conservative shape are diagnostic estimates only.
- Do not delete ideas merely to reduce repetition.
- Do not merge, fold, or retire any remaining chapter without a cluster-specific
  dry-run package, one-skeleton destination draft where applicable,
  claim/source/proof and reader reconciliation, URL/history treatment, and a
  recorded execute/revise/defer/reject decision.
- Do not promote any chapter core claim above `argument` through
  consolidation.

## Follow-Up Review Outcome

A follow-up review of the latest re-consolidation idea accepts the core
recommendation: the book should reduce repeated chapter skeletons where adjacent
chapters are trying to express one architectural artifact. This is a good
roadmap direction because it preserves ideas while improving depth, reader
flow, and claim ownership. It is not a reason to make an immediate
`book_structure.json` edit.

The actionable update is state discipline. Each cluster should move through a
named consolidation state before any manifest change, and broad human-reader
curation should not polish a pending duplicate skeleton unless the project has
explicitly deferred or rejected that merge for the release.

The implementation update from the critique is equally important: the output of
a successful merge is one deeper chapter with one Problem, Insufficiency,
Mechanism, Interface, Evidence, Implementation, and Handoff skeleton. Preserved
ideas become named mechanisms, sections, subclaims, source mappings, proof
hooks, examples, or implementation-horizon facets. They do not survive by
copying multiple full source-chapter skeletons into the destination draft.

The 2026-06-30 attachment review does not add a new consolidation cluster. It
confirms that the current decision queue is aimed correctly: the next useful
work is to judge the already packaged merge and fold candidates, starting with
the Part I alignment/governance pilot, rather than drafting another abstract
consolidation plan or editing the manifest broadly from the critique alone. A
successful consolidation must be one deeper chapter, not multiple source
chapter skeletons concatenated under a new title.

The specific answer to the proposal is yes, with constraints: it is a good
roadmap improvement because it attacks structural repetition at the chapter
boundary, not because fewer chapters are automatically better. The repository
should therefore treat the proposed 44-ish aggressive shape and 47-ish
conservative shape as diagnostic pressure tests. It should not treat either
number as a release target. A retained chapter is correct when it owns a real
artifact, interface, proof family, evidence lane, implementation horizon, or
reader throughline; a folded chapter is correct only when its idea survives as
a named section, subclaim, source mapping, proof hook, reader path, or explicit
retirement/restoration decision.

## Attachment Disposition Summary

Accepted into the roadmap:

- Alignment philosophy is the highest-payoff pilot: consolidate
  constitutional-alignment plus agency/corrigibility, and consolidate moral
  uncertainty plus fork/exit/audit governance, if review accepts the destination
  drafts.
- Verification/adversarial review and planning/DAG control remain real merge
  candidates because they currently carry overlapping source families, claim
  motions, and chapter skeletons.
- Semantic representation remains a fold candidate, not a deletion target. The
  MoECOT runtime fold has executed into a named runtime crosswalk inside
  Routing Heads and Specialist Cores, the simulation-fidelity fold has
  executed into a named Simulation Fidelity and Claim Transport section inside
  Resource Economics and Token Budgets, the intent/contracts merge has
  executed into Command Contracts: From Intent to Executable Work, the static
  context ABI merge has executed into The Virtual Context ABI: Typed Pages,
  Cells, and Certificates, and the verification/adversarial-review merge has
  executed into Proof-Carrying Claims and Adversarial Review. These executed
  packages preserve source mappings, proof hooks, implementation-horizon
  facets, restoration conditions, and no-support-state-change boundaries.
- The 44-chapter aggressive shape and roughly 47-chapter conservative shape
  are useful pressure tests only. They are not release goals.
- The implementation rule is one skeleton per destination chapter. A successful
  merge collapses repeated Problem, Insufficiency, Mechanism, Interface,
  Evidence, Implementation, and Handoff scaffolding, then spends the recovered
  space on mechanisms, examples, failure modes, proof specificity, external
  positioning, and reader flow.

Not accepted without later evidence or review:

- A broad 54-to-44 `book_structure.json` edit.
- Deleting ideas simply because they are currently in thin chapters.
- Folding Project Theseus, Circle/coil chapters, or other protected standalone
  artifacts merely to reduce the table of contents.
- Treating consolidation as source evidence, support-state promotion, external
  review, reader-release approval, or proof/test improvement.

## Consolidation State Model

| State | Meaning | Required next move |
|---|---|---|
| `planned_candidate` | The cluster is directionally plausible but has no dry-run package or destination draft. | Create a cluster-specific reconciliation plan before any manifest or reader-manuscript change depends on it. |
| `fold_review_candidate` | The source chapter may be a section rather than a chapter-owning artifact. | Produce a fold disposition that names preserved sections, subclaims, source IDs, proof hooks, reader paths, and restoration conditions. |
| `dry_run_packaged` | A package proposes the manifest diff, claim/source/proof/reader reconciliation, and validation path, but no destination prose is accepted. | Write a one-skeleton destination draft or reject the merge as not improving chapter ownership. |
| `review_ready` | The dry-run package and one-skeleton destination draft exist and can be judged by Corben, an editor, or an external reviewer. | Record an execute, revise, defer, or reject decision before touching `book_structure.json`. |
| `fold_disposition_ready` | A fold disposition exists and can be judged without a full destination chapter draft. | Record an execute fold, revise, defer, or reject/retain decision before touching `book_structure.json`. |
| `executed` | The manifest, outline, chapter prose, appendices, proof manifest, reader records, handoffs, and redirects were updated and validated. | Keep the no-support-state-change boundary unless a separate evidence transition exists. |
| `deferred_for_release` | The merge remains plausible, but the current release proceeds without it for a recorded reason. | Reader curation may continue with an explicit note that duplicate structure is accepted for that release only. |
| `rejected_or_retained` | Review finds the separate chapter boundary stronger. | Preserve both chapters and record the artifact, evidence, proof, or reader reason. |

## Current Pilot Status

The Part I alignment/governance philosophy cluster has executed as the pilot:

- `constitutional-alignment-substrate` plus
  `agency-dignity-and-corrigibility` into **Constitutional Alignment: Agency,
  Dignity, and Corrigibility**.
- `moral-uncertainty-and-value-conflict` plus
  `governance-rights-fork-exit-and-audit` into **Moral Uncertainty, Value
  Conflict, and Contestable Governance**.

The executed pilot used these review inputs and execution surfaces:

- `docs/chapter_consolidation_pilot_plan.md`;
- `docs/chapter_consolidation_dry_run_constitutional_alignment.md`;
- `docs/chapter_consolidation_destination_draft_constitutional_alignment.md`;
- `docs/chapter_consolidation_dry_run_contestable_governance.md`;
- `docs/chapter_consolidation_destination_draft_contestable_governance.md`;
- `docs/chapter_consolidation_url_history_policy.md`;
- `docs/chapter_consolidation_decision_review.md`;
- `docs/chapter_consolidation_external_review_packet.md`.

The full consolidation decision queue now also has
`docs/chapter_consolidation_full_review_packet.md`, a request surface for all
review-ready merge packages and fold dispositions. That packet now asks
reviewers to apply the 54-to-44/47 critique as a one-skeleton depth test by
naming the repeated skeleton load removed and the mechanism-depth,
negative-control, external-positioning, proof-limit, implementation-trace,
example, or reader-continuity work where the saved space should be reinvested.
It records no accepted external review and no support-state effect.

`docs/chapter_consolidation_release_stability_review.md` now records a
`deferred_for_release` reader-work outcome for every unexecuted review-ready or
fold-disposition package in the current queue. It now applies to the remaining
unexecuted packages only. The reader-curation cycle continues against the
46-chapter manifest with explicit consolidation caveats while preserving every
unexecuted package for later human or external review.

The public URL/history precondition now has a policy surface:
`docs/chapter_consolidation_url_history_policy.md`. It sets the default
continuity URL, retired URL, redirect or historical-stub, and chapter-history
ledger requirements for future execution commits. It has now been applied to
the Part I pilot, conservative compression merge, intent/contracts merge,
MoECOT runtime fold, simulation-fidelity fold, static context ABI merge, and
verification/adversarial-review merge
through static historical stubs and
`docs/chapter_history_ledger.md`; it
remains the policy for future unexecuted packages.

The current pilot state is `executed`: both destination chapters are now
canonical, the folded source chapters are removed from the book spine, and the
retired public slugs are preserved through historical stubs. The remaining
queue stays governed by the same execute, revise, defer, or reject discipline.

## Chapter-Ownership Rubric

Use this rubric before any non-pilot consolidation package:

- A chapter is chapter-owning when it owns a distinct artifact, interface,
  evidence lane, proof family, implementation horizon, or reader throughline
  that would become weaker if buried.
- A chapter is a consolidation candidate when most of its reader-visible load
  repeats another chapter's source family, claim motion, mechanism, interface,
  failure modes, implementation horizon, and handoff while adding only a
  supporting facet.
- A merge is justified only if the destination draft reduces repeated skeleton
  load and increases mechanism depth, external positioning, proof specificity,
  negative-case treatment, or reader clarity.
- A merge is rejected or deferred when the proposed destination loses a useful
  artifact boundary, makes claim ownership less legible, weakens proof/evidence
  routing, or merely compresses the table of contents without improving the
  argument.

## Cluster Decision Scorecard

Use this scorecard when reviewing each package. A package should execute only
when the execute side wins on the whole review, not merely because the proposed
merge lowers the chapter count.

| Check | Execute signal | Revise, defer, or reject signal |
|---|---|---|
| Chapter ownership | The destination owns one artifact, interface, proof family, evidence lane, implementation horizon, or reader throughline more clearly than the source chapters. | The source chapters still own distinct artifacts or the destination becomes a generic umbrella. |
| Skeleton removal | One Problem, Insufficiency, Mechanism, Interface, Evidence, Implementation, and Handoff skeleton can carry the whole argument. | The draft reads like multiple full source-chapter skeletons pasted together. |
| Claim reconciliation | One destination core claim is narrower or clearer, and folded claims survive as subclaims, sections, proof hooks, source rows, or explicit retirements. | Core-claim meaning broadens, subclaims disappear, or support-state pressure appears without new evidence. |
| Evidence and proof routing | Lean modules, harness rows, source notes, external comparators, negative cases, and no-promotion blockers become easier to see. | Proof tags, harnesses, external baselines, or source queues become harder to locate or weaker to audit. |
| Reader value | The merge reduces repeated exposition and makes the human-reader path smoother without hiding evidence boundaries. | The merge saves pages but makes the concept harder to understand, cite, or listen to. |
| Release hygiene | URL/history policy, handoff repairs, reader-overlay or curated-reader repairs, Appendix C, Appendix K, scaffold sync, validation, and changelog can ship in one reviewable commit. | The merge would leave stale URLs, orphaned chapter IDs, broken handoffs, unreviewed reader deltas, or ambiguous generated state. |

## Current Cluster Register

| Cluster | Current state | Next allowed action | Reader-work consequence |
|---|---|---|---|
| Part I alignment and agency/corrigibility | `executed` | Use as the template for future one-package execution commits. | Reader work should target the consolidated destination chapter. |
| Part I value conflict and contestable governance | `executed` | Use as the template for future one-package execution commits. | Reader work should target the consolidated destination chapter. |
| Compression and residual honesty | `executed` | Use the conservative merge as the template for future packages; keep RankFold/NeuralFold standalone unless later evidence changes its artifact ownership. | Reader work should target the merged compact-generative destination plus the retained RankFold technique chapter. |
| Intent and executable contracts | `executed` | Use the executed merge as the template for future one-skeleton packages; restore a standalone command-contract chapter only if parser, dispatcher, approval-enforcement, or semantic-interface evidence makes it chapter-owning again. | Reader work should target Command Contracts: From Intent to Executable Work; the archived standalone command-contract reader draft remains historical only. |
| Static context ABI | `executed` | Use the executed merge as the template for future one-skeleton context packages; restore a standalone semantic-pages chapter only if paired source/derived cells, certificate truthfulness tests, summary-fidelity tests, or independent interoperability evidence makes it chapter-owning again. | Reader work should target The Virtual Context ABI: Typed Pages, Cells, and Certificates; the archived semantic-pages reader draft remains historical only. |
| Verification and adversarial review | `executed` | Use the executed merge as the template for future proof/review packages; restore a standalone tribunal chapter only if independent tribunal-pipeline evidence, reviewer-independence measurements, adversarial-probe-quality tests, verdict-correctness audits, or institutional contestability evidence makes it chapter-owning again. | Reader work should target Proof-Carrying Claims and Adversarial Review; the archived standalone tribunal reader draft remains historical only. |
| Planning and DAG control | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Avoid curated graduation of the planning/DAG pair unless explicitly deferred or retained; reader curation may continue on semantic IR. |
| Source-blocked MoECOT runtime | `executed` | Use the executed fold as the template for future source-blocked fold packages; restore a standalone chapter only if public-safe runtime, replay, benchmark, and corroboration evidence makes it chapter-owning. | Reader work should target Routing Heads and Specialist Cores plus the folded MoECOT Runtime Crosswalk; the archived standalone reader draft remains historical only. |
| Simulation fidelity | `executed` | Use the executed fold as the template for future feasibility-bound fold packages; restore a standalone chapter only if public-safe simulation, physical-computation, benchmark-transfer, or independent review evidence makes it chapter-owning. | Reader work should target Resource Economics and Token Budgets plus the folded Simulation Fidelity and Claim Transport section; the archived standalone source manuscript remains historical only. |
| Semantic representation | `fold_disposition_ready` | Review the fold disposition and decide execute fold after destination-package review, revise, defer, or reject/retain. | Preserve proof/test hooks, semantic-node records, dependency on compression-package review, and reader repairs if folded. |
| Runtime adapters and Labor OS | `rejected_or_retained` unless later evidence changes artifact ownership | Revisit only if tool-permission adapters stop owning a distinct artifact. | Reader curation may proceed because the current split has artifact ownership. |

## Consolidation Decision Queue

Do not create more destination drafts for packages that are already
`review_ready`. The next consolidation work should record decisions against
the existing review-ready merge packages and fold-disposition candidates. A
review-ready package moves to `executed`, `deferred_for_release`, or
`rejected_or_retained` only through a recorded decision; a revised package stays
blocked until the revision is reviewed.

| Order | Package | Required decision | Execution note |
|---|---|---|---|
| 1 | Part I constitutional alignment and agency/corrigibility | Executed on 2026-06-30. | Retired agency/corrigibility slug preserved through historical stub; source chapter archived; no support-state change. |
| 2 | Part I value conflict and contestable governance | Executed on 2026-06-30. | Retired governance-rights slug preserved through historical stub; source chapter archived; no support-state change. |
| 3 | Compression and residual honesty | Conservative merge executed on 2026-06-30. | Retired GVR slug preserved through historical stub; source chapter archived; RankFold/NeuralFold retained as standalone technique chapter; no support-state change. |
| 4 | Intent and executable contracts | Executed on 2026-06-30. | Retired command-contract slug preserved through historical stub; source chapter archived; `human-intent-as-a-formal-input` retained as intent intake; no support-state change. |
| 5 | Static context ABI | Executed on 2026-06-30. | Retired semantic-pages slug preserved through historical stub; source chapter and curated reader draft archived; transaction/snapshot/taint and verification-bandwidth chapters retained standalone; no support-state change. |
| 6 | Verification and adversarial review | Merge executed on 2026-06-30. | Retired tribunal slug preserved through historical stub; source chapter and curated reader draft archived; `claim-ledgers-and-belief-revision` retained as the durable belief-revision substrate; no support-state change. |
| 7 | Planning and DAG control | Execute, revise, defer, or reject. | Keep `cognitive-compilation-and-semantic-ir` as the semantic-IR and lowering-receipt layer. |
| 8 | Fold-disposition candidates | Execute fold, revise, defer, or reject/retain. | MoECOT runtime has executed into Routing Heads and Specialist Cores; simulation fidelity has executed into Resource Economics and Token Budgets; semantic representation still has a fold disposition and requires review and decision before any manifest edit. |

Every decision record should name the reviewed package, reviewer or review
source, one-skeleton destination judgment, claim/source/proof/reader impact,
external-grounding adequacy, URL or redirect policy, validation scope,
support-state effect, non-claims, and the exact decision. If a package is
executed, apply only one merge or fold package per commit. If a package is
deferred or rejected, record whether curated-reader work is unblocked, still
paused, or allowed only as local cleanup.

## Execution Gate

The consolidation critique is now a release-control gate, not a direct
manifest-edit instruction. A package can move to `executed` only when the
review record shows that the destination chapter is stronger than the source
chapters as one chapter, not merely shorter as a table-of-contents entry.

Before executing a merge or fold, the change set must include:

- the accepted decision record and reviewer or review-source reference;
- the `book_structure.json` edit, outline update, Appendix C reconciliation,
  Appendix K implementation-horizon reconciliation, source-union handling,
  proof-manifest handling, reader-overlay or curated-reader repair,
  URL/history treatment, scaffold sync, validation output, and changelog entry;
- a repetition-removal ledger naming which repeated skeleton sections were
  removed and how the saved space became mechanism depth, external comparison,
  negative cases, proof-limit clarity, examples, implementation traces, or
  reader continuity;
- a no-support-state-change boundary unless a separate accepted evidence
  transition exists.

Before graduating curated-reader prose for a source chapter inside a pending
merge or fold package, the package must have a recorded `executed`,
`deferred_for_release`, or `rejected_or_retained` outcome. If the outcome is
`deferred_for_release`, the record must name the reader confusion and duplicate
structure accepted for the release plus the condition for revisiting the
decision. If the outcome is `rejected_or_retained`, the record must name the
artifact, proof lane, evidence lane, implementation horizon, or reader
throughline that justifies keeping the separate chapter boundary.

## Candidate Sequence

| Tier | Candidate cluster | Source chapters | Default destination or action | Preservation requirement |
|---|---|---|---|---|
| 1A | Alignment philosophy | `constitutional-alignment-substrate`; `agency-dignity-and-corrigibility` | **Constitutional Alignment: Agency, Dignity, and Corrigibility** | Preserve constitutional predicates, agency/dignity/corrigibility interfaces, both Lean modules, all proof tags, source unions, and review paths. |
| 1A | Value conflict and contestable governance | `moral-uncertainty-and-value-conflict`; `governance-rights-fork-exit-and-audit` | **Moral Uncertainty, Value Conflict, and Contestable Governance** | Preserve value-conflict records, fork/exit/audit/redaction/appeal interfaces, dissent/revisit paths, both Lean modules, all proof tags, and source unions. |
| 1B | Compression and residual honesty | `compact-generative-systems-and-residual-honesty`; `generate-verify-repair-compression`; `rankfold-neuralfold-and-artifact-compression` | **Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty** | Preserve the compact-generator principle, GVR loop, RankFold/NeuralFold technique, residual honesty, compression limits, source unions, proof hooks, and implementation horizons. Conservative option: keep `rankfold-neuralfold-and-artifact-compression` standalone if it still owns a concrete technique. |
| 1C | Intent and executable contracts | `intent-to-execution-contracts`; `command-contracts-and-semantic-interfaces` | Executed: merged command-contract semantic-interface material into **Command Contracts: From Intent to Executable Work** while keeping `human-intent-as-a-formal-input` separate. | Preserved intent-to-contract conversion, semantic interface rules, authority fields, execution receipts, validation states, field provenance/confidence, test hooks, proof tags, source mappings, URL stub, archive record, and no-support-state-change boundary. |
| 1D | Static context ABI | `virtual-context-abi`; `semantic-pages-context-cells-and-certificates` | Executed: merged semantic-pages and context-cell certificate material into **The Virtual Context ABI: Typed Pages, Cells, and Certificates** while keeping `context-transactions-snapshots-mounts-and-taint` and `verification-bandwidth-and-context-adequacy` separate. | Preserved pages, cells, certificates, context addressing, source unions, proof hooks, implementation horizons, URL stub, archive record, and no-support-state-change boundary. |
| 2A | Verification and adversarial review | `spinoza-verification-and-proof-carrying-claims`; `unified-adaptive-tribunal-and-adversarial-review` | **Proof-Carrying Claims and Adversarial Review** | Preserve proof-carrying claim tiers, tribunal review, adversarial dossiers, dissent, no-theorem-laundering boundaries, proof hooks, harness rows, and source unions. Keep `claim-ledgers-and-belief-revision` separate. |
| 2B | Planning and DAG control | `planning-as-a-control-layer`; `planforge-dags-and-intelligence-arbitrage` | **Planning as a Control Layer: DAGs and Intelligence Arbitrage** | Preserve control-layer semantics, PlanForge DAGs, intelligence arbitrage, negative cases, proof hooks, and source unions. Keep `cognitive-compilation-and-semantic-ir` separate unless later review shows the IR has no independent chapter ownership. |
| 2C | Source-blocked MoECOT runtime | `moecot-runtime-and-multi-core-orchestration`; `routing-heads-and-specialist-cores` | Executed: folded MoECOT runtime into Routing Heads and Specialist Cores until public-safe runtime, replay, benchmark, and corroboration evidence makes a standalone chapter chapter-owning again. | Preserved the multi-core orchestration runtime as the named MoECOT Runtime Crosswalk, source queue, proof tags, schema/fixture lane, blocker set, URL stub, archive record, and future chapter-restoration condition. |
| Fold review | Simulation fidelity | `simulation-fidelity-and-physical-constraints`; `resource-economics-and-token-budgets`; efficient-ASI frame as secondary context only | Executed: folded simulation fidelity into Resource Economics and Token Budgets until public-safe simulation, physical-computation, benchmark-transfer, or independent review evidence makes a standalone chapter chapter-owning again. | Preserved physical/resource bounds, fidelity limitations, simulation contract fields, claim-transport boundaries, proof hooks, source queue, schema/fixture lane, URL stub, archive record, and no-overclaim language as the named Simulation Fidelity and Claim Transport section. |
| Fold review | Semantic representation | `semantic-representation-and-tree-structured-models`; compression/representation cluster | Fold only if representation remains a substrate facet rather than a chapter-owning artifact, and only after the compression/representation destination package has a reviewed decision. | Preserve tree-structured representation, semantic-node records, source mappings, proof/test hooks, and restoration conditions as a named section or companion note. |
| Low priority | Runtime adapters and Labor OS | `runtime-adapters-tool-permissions-and-human-approval`; `labor-os-and-typed-jobs` | No current merge; only revisit if tool-permission adapters stop owning a distinct artifact. | Preserve permissioning, human approval, runtime receipts, Labor OS typed jobs, and execution-harness separation. |

## Protected Standalone Chapters

The following chapters remain standalone unless a later evidence review finds a
real duplicate artifact owner:

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `system-boundaries-and-authority`
- `failure-modes-of-ungoverned-intelligence`
- `evidence-states-and-claim-discipline`
- `stable-capability-fields`
- `capability-replacement-and-rollback`
- `security-kernel-and-digital-scifs`
- `recursive-self-improvement-boundaries`
- `verification-bandwidth-and-context-adequacy`
- `claim-ledgers-and-belief-revision`
- `readiness-gates-residual-escrow-and-quarantine`
- `context-transactions-snapshots-mounts-and-taint`
- `labor-os-and-typed-jobs`
- `artifact-graphs-audit-logs-and-replay`
- `runtime-adapters-tool-permissions-and-human-approval`
- `procedural-memory-and-cognitive-loop-closure`
- `circle-calculus-and-proof-carrying-ai-contracts`
- `coil-attention-cyclic-memory-and-recurrence-contracts`
- `coilra-multicoil-rope-and-cyclic-mixers`
- `mathematical-and-search-substrates`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `project-theseus-as-report-first-implementation-reference`
- `artifact-steward-agents-and-living-project-governance`
- `executable-specifications-and-lean-proof-envelope`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `living-book-methodology`
- `open-research-agenda-and-bibliography-plan`

## Required Package Before Any Non-Pilot Merge

Every non-pilot consolidation candidate must get the same treatment as the
Part I pilot before any manifest edit:

1. A cluster-specific reconciliation plan.
2. A proposed one-skeleton destination outline or fold disposition.
3. An illustrative, unapplied `book_structure.json` diff.
4. Appendix C core-claim and subclaim reconciliation.
5. Source-ID union and external-source union.
6. Lean module, proof-tag, harness, schema, and fixture treatment.
7. Reader-overlay, Human Reading Path, handoff, and reader-review repairs.
8. MVI and Beyond-SOTA implementation-horizon merge.
9. Public URL, redirect, or retired-file policy.
10. Validation command list and expected generated-file updates.
11. No-support-state-change and no-evidence-creation boundary.
12. Chapter-ownership rubric result: preserved artifact boundary, repeated
    skeleton load removed, proof/evidence path clarified, reader confusion
    reduced, and reason to execute, revise, defer, or reject.
13. Repetition-removal ledger: what skeleton sections are removed, what ideas
    are preserved as named substructures, and where the saved space goes.
14. Reader-work disposition: whether curated-reader work for source chapters is
    paused, allowed as local cleanup, explicitly deferred, or allowed because
    the merge has been rejected/retained.
15. URL/history treatment: destination continuity URL, retired source URL,
    redirect or historical-stub implementation, and chapter-history ledger row
    required by `docs/chapter_consolidation_url_history_policy.md`.

## Reader Work Sequencing

Broad human-reader curation should avoid source chapters inside a pending
consolidation cluster until that cluster is executed, revised, rejected, or
explicitly deferred for the release. Local prose fixes remain allowed when they
do not entrench duplicate structure.

The current release-stability decision explicitly defers all unexecuted
review-ready merge packages and fold-disposition packages for this
reader-curation cycle. This means reader work may proceed inside those source
chapters only with a recorded consolidation caveat; it does not mean the
packages are rejected, executed, or authorized for manifest changes.

Reader curation may continue outside pending clusters, especially where the
chapter owns a distinct artifact, proof lane, evidence lane, or implementation
path. The current rule is consolidation-aware, not chapter-count driven:
protected standalone chapters may graduate into drafting-only curated prose,
while source chapters inside pending merge or fold packages should wait for an
execute, revise, defer, or reject decision unless the edit is explicitly scoped
as local cleanup.

The current allowed protected-reader set is:

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `system-boundaries-and-authority`
- `failure-modes-of-ungoverned-intelligence`
- `evidence-states-and-claim-discipline`
- `security-kernel-and-digital-scifs`
- `stable-capability-fields`
- `capability-replacement-and-rollback`
- `readiness-gates-residual-escrow-and-quarantine`
- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `verification-bandwidth-and-context-adequacy`
- `claim-ledgers-and-belief-revision`
- `labor-os-and-typed-jobs`
- `artifact-graphs-audit-logs-and-replay`
- `runtime-adapters-tool-permissions-and-human-approval`
- `procedural-memory-and-cognitive-loop-closure`
- `mathematical-and-search-substrates`
- `coil-attention-cyclic-memory-and-recurrence-contracts`
- `coilra-multicoil-rope-and-cyclic-mixers`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `policy-optimization-and-learning-from-feedback`
- `integrated-reference-architecture`
- `project-theseus-as-report-first-implementation-reference`
- `prototype-roadmap`
- `living-book-methodology`
- `open-research-agenda-and-bibliography-plan`
- `recursive-self-improvement-boundaries`
- `circle-calculus-and-proof-carrying-ai-contracts`
- `executable-specifications-and-lean-proof-envelope`
- `artifact-steward-agents-and-living-project-governance`

`human-intent-as-a-formal-input` remains allowed for local reader prose only
because the current consolidation queue keeps it as the intent-intake chapter;
its handoff must be revisited if the intent/contracts or Part I alignment
decisions change the downstream destination shape.

The current deferred-for-release reader-work set is:

- `planning-as-a-control-layer`
- `planforge-dags-and-intelligence-arbitrage`
- `semantic-representation-and-tree-structured-models`

Any curated reader prose pass for pending-package chapters must cite
`docs/chapter_consolidation_release_stability_review.md` or record an
equivalent consolidation caveat in its prose-pass review note. Curated reader
work for executed packages should cite the chapter-history ledger or folded
destination chapter when it needs historical context.

## Non-Pilot Review-Ready Packages

- `docs/chapter_consolidation_dry_run_compression.md` records the Tier 1B
  dry-run package for the compression and residual-honesty cluster. It does not
  edit `book_structure.json`, authorize a manifest merge, or move support
  states. It keeps the RankFold/NeuralFold Conservative option open and leaves
  `semantic-representation-and-tree-structured-models` dependency-bound until a
  separate fold disposition is reviewed.
- `docs/chapter_consolidation_destination_draft_compression.md` records the
  one-skeleton destination draft for **Compact Generative Systems: Generate,
  Verify, Repair, and Residual Honesty**. It is review-ready but not reviewed,
  not canonical, and not a manifest edit. The next decision is execute full
  merge, execute conservative merge, revise, defer, or reject.
- `docs/chapter_consolidation_dry_run_intent_contracts.md` records the Tier 1C
  dry-run package for the intent and executable-contracts cluster. It has now
  executed through the 2026-06-30 intent/contracts merge package. It kept
  `human-intent-as-a-formal-input` standalone as the intake chapter and
  preserved command-interface material inside the destination chapter.
- `docs/chapter_consolidation_destination_draft_intent_contracts.md` records
  the one-skeleton destination draft for **Command Contracts: From Intent to
  Executable Work**. It is now canonical through the executed merge; the draft
  remains historical review/control lineage, not source evidence and not a
  support-state transition.
- `docs/chapter_consolidation_dry_run_context_abi.md` records the Tier 1D
  dry-run package for the static context ABI cluster. It has now executed
  through the 2026-06-30 static context ABI merge package. It kept
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`, and
  `claim-ledgers-and-belief-revision` standalone.
- `docs/chapter_consolidation_destination_draft_context_abi.md` records the
  one-skeleton destination draft for **The Virtual Context ABI: Typed Pages,
  Cells, and Certificates**. It is now canonical through the executed merge;
  the draft remains historical review/control lineage, not source evidence and
  not a support-state transition.
- `docs/chapter_consolidation_dry_run_verification_review.md` records the Tier
  2A dry-run package for the verification and adversarial-review cluster. It
  has now executed through the 2026-06-30 verification/adversarial-review merge
  package. It keeps `claim-ledgers-and-belief-revision` standalone as the
  durable claim identity, support-state, contradiction, uncertainty, and
  revision-history substrate.
- `docs/chapter_consolidation_destination_draft_verification_review.md` records
  the one-skeleton destination draft for **Proof-Carrying Claims and
  Adversarial Review**. It is now canonical through the executed merge; the
  draft remains historical review/control lineage, not source evidence and not
  a support-state transition.
- `docs/chapter_consolidation_dry_run_planning_dag.md` records the Tier 2B
  dry-run package for the planning and DAG-control cluster. It does not edit
  `book_structure.json`, authorize a manifest merge, or move support states.
  It keeps `cognitive-compilation-and-semantic-ir` standalone as the semantic
  atom, IR validity, lowering receipt, repair-ledger, and target-artifact
  compilation layer.
- `docs/chapter_consolidation_destination_draft_planning_dag.md` records the
  one-skeleton destination draft for **Planning as a Control Layer: DAGs and
  Intelligence Arbitrage**. It is review-ready but not reviewed, not canonical,
  and not a manifest edit. The next decision is execute, revise, defer, or
  reject.

## Executed Fold-Disposition History

This section is also the executed merge and fold history for consolidation
packages that have already changed the manifest.

- `docs/chapter_consolidation_dry_run_intent_contracts.md` and
  `docs/chapter_consolidation_destination_draft_intent_contracts.md` record
  the executed merge package for `command-contracts-and-semantic-interfaces`
  into **Command Contracts: From Intent to Executable Work**. It is now
  executed through the 2026-06-30 intent/contracts merge package. The retired
  public slug is preserved with a static historical stub, the live source
  manuscript and curated reader draft are archived, and the current canonical
  route for reader and research work is `intent-to-execution-contracts`. It
  preserves `AsiStackProofs.IntentToExecution`,
  `AsiStackProofs.CommandContracts`, `schemas/intent_contract.schema.json`,
  `schemas/command_contract.schema.json`,
  `schemas/intent_execution_trace.schema.json`, the plan-execution contract
  harness, source unions, external comparator unions, reader-overlay repairs,
  URL/history policy, restoration conditions, and the no-support-state-change
  boundary.

- `docs/chapter_consolidation_dry_run_context_abi.md` and
  `docs/chapter_consolidation_destination_draft_context_abi.md` record the
  executed merge package for `semantic-pages-context-cells-and-certificates`
  into **The Virtual Context ABI: Typed Pages, Cells, and Certificates**. It is
  now executed through the 2026-06-30 static context ABI merge package. The
  retired public slug is preserved with a static historical stub, the live
  source manuscript and curated reader draft are archived, and the current
  canonical route for reader and research work is `virtual-context-abi`. It
  preserves `AsiStackProofs.VirtualContextABI`,
  `AsiStackProofs.ContextCertificates`,
  `schemas/context_abi_record.schema.json`,
  `schemas/semantic_page_certificate.schema.json`,
  `schemas/context_packet.schema.json`, the context admission/adequacy harness,
  source unions, external comparator unions, reader repair requirements,
  URL/history policy, restoration conditions, and the no-support-state-change
  boundary.

- `docs/chapter_consolidation_dry_run_verification_review.md` and
  `docs/chapter_consolidation_destination_draft_verification_review.md` record
  the executed merge package for
  `unified-adaptive-tribunal-and-adversarial-review` into
  **Proof-Carrying Claims and Adversarial Review**. It is now executed through
  the 2026-06-30 verification/adversarial-review merge package. The retired
  public slug is preserved with a static historical stub, the live source
  manuscript and curated reader draft are archived, and the current canonical
  route for reader and research work is
  `spinoza-verification-and-proof-carrying-claims`. It preserves
  `AsiStackProofs.ProofCarryingClaims`, `AsiStackProofs.Tribunal`,
  `schemas/proof_carrying_claim.schema.json`,
  `schemas/tribunal_review_record.schema.json`, proof-carrying claim and
  tribunal review harness rows, source unions, external comparator unions,
  reader repair requirements, URL/history policy, restoration conditions, and
  the no-support-state-change boundary.

- `docs/chapter_consolidation_fold_moecot_runtime.md` records the first fold
  disposition package, for `moecot-runtime-and-multi-core-orchestration` into a
  named MoECOT Runtime Crosswalk section inside
  `routing-heads-and-specialist-cores`. It is now executed through the
  2026-06-30 MoECOT runtime fold package. The retired public slug is preserved
  with a static historical stub, the live source manuscript and curated reader
  draft are archived, and the current canonical route for reader and research
  work is Routing Heads and Specialist Cores. It preserves
  `AsiStackProofs.Routing`, `AsiStackProofs.MoECOTRuntime`,
  `schemas/specialist_registry_record.schema.json`,
  `schemas/routing_decision_record.schema.json`,
  `schemas/moecot_orchestration_record.schema.json`, source unions, external
  comparator unions, reader repair requirements, URL/history policy, restoration
  conditions, and the no-support-state-change boundary.
- `docs/chapter_consolidation_fold_simulation_fidelity.md` records the second
  fold disposition package, for `simulation-fidelity-and-physical-constraints`
  into a named Simulation Fidelity and Claim Transport section inside
  `resource-economics-and-token-budgets`. It is now executed through the
  2026-06-30 simulation-fidelity fold package. The retired public slug is
  preserved with a static historical stub, the live source manuscript is
  archived, and the current canonical route for reader and research work is
  Resource Economics and Token Budgets. It preserves
  `AsiStackProofs.ResourceEconomics`, `AsiStackProofs.SimulationFidelity`,
  `schemas/resource_budget_record.schema.json`,
  `schemas/simulation_contract_record.schema.json`, source unions, external
  comparator unions, reader repair requirements, URL/history policy,
  restoration conditions, and the no-support-state-change boundary.

## Remaining Fold-Disposition Packages

- `docs/chapter_consolidation_fold_semantic_representation.md` records the
  remaining fold disposition package, for
  `semantic-representation-and-tree-structured-models` into a named Semantic
  Representation Leasing section inside the compression/representation
  destination package if review accepts that dependency. It is
  fold-disposition ready but not reviewed, not executed, not canonical, and not
  a manifest edit. The next decision is execute fold after destination-package
  review, revise, defer, or reject/retain. It preserves
  `AsiStackProofs.SemanticRepresentation`,
  `schemas/semantic_node_record.schema.json`,
  `schemas/semantic_atom.schema.json`,
  `schemas/semantic_page_certificate.schema.json`, source unions, external
  comparator unions, reader repair requirements, URL/history policy,
  restoration conditions, the compression-package dependency, and the
  no-support-state-change boundary.

## Non-Claims

- This sequence records the executed Part I pilot, conservative compression
  merge, intent/contracts merge, MoECOT runtime fold, simulation-fidelity fold,
  static context ABI merge, and verification/adversarial-review merge and does
  not merge any remaining package by itself.
- This sequence reflects the 2026-06-30 Part I, compression,
  intent/contracts, MoECOT, simulation-fidelity, static context ABI, and
  verification/adversarial-review manifest changes and does not authorize any
  further `book_structure.json` change by itself.
- Exact boundary: this sequence does not authorize any further `book_structure.json` change.
- This sequence does not change Appendix C support states.
- This sequence does not create source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support.
- This sequence does not approve reader, ebook, PDF, DOCX, audio, DOI, archive,
  or release artifacts.
- This sequence does not prove that any future merged chapter will be better;
  that judgment requires review of the destination draft and reconciliation
  package.
