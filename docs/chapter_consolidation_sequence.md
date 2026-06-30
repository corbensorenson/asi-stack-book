# Governed Chapter Consolidation Sequence

Last updated: 2026-06-30

This record preserves the full consolidation sequence accepted for roadmap
planning after review of the latest 54-to-44/47 chapter-shape critique. It is a
planning and release-control artifact, not source evidence, not an external
review result, not a manifest edit, and not a support-state transition.

The recommendation has teeth: most of the current repetition is not caused by
bad ideas. It comes from rendering adjacent ideas as separate chapters that
repeat the same Problem, Insufficiency, Mechanism, Interface, Evidence,
Implementation, and Handoff skeleton. The roadmap response is governed
re-consolidation: fewer deeper chapter-owning artifacts, with every useful idea
preserved as a section, subclaim, source mapping, proof hook, reader path,
implementation horizon, or explicit retirement decision.

This record does not change `book_structure.json`. The current canonical book
still has 54 manifest chapters.

## Decision Boundary

- Accept the critique as directionally correct roadmap guidance.
- Do not run a broad 54-to-44 manifest edit from the critique alone.
- Do not target a fixed chapter count. A 44-chapter aggressive shape and a
  roughly 47-chapter conservative shape are diagnostic estimates only.
- Do not delete ideas merely to reduce repetition.
- Do not merge, fold, or retire any chapter without a cluster-specific dry-run
  package, one-skeleton destination draft where applicable, claim/source/proof
  and reader reconciliation, and human or external review of the tradeoff.
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

## Attachment Disposition Summary

Accepted into the roadmap:

- Alignment philosophy is the highest-payoff pilot: consolidate
  constitutional-alignment plus agency/corrigibility, and consolidate moral
  uncertainty plus fork/exit/audit governance, if review accepts the destination
  drafts.
- Compression, intent/contracts, static context ABI, verification/adversarial
  review, and planning/DAG control are real merge candidates because they
  currently carry overlapping source families, claim motions, and chapter
  skeletons.
- MoECOT runtime, simulation fidelity, and semantic representation are fold
  candidates, not deletion targets. Each idea must survive as a named section,
  source mapping, proof hook, implementation-horizon facet, restoration
  condition, or explicit retained-chapter decision.
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

The active pilot remains the Part I alignment/governance philosophy cluster:

- `constitutional-alignment-substrate` plus
  `agency-dignity-and-corrigibility` into **Constitutional Alignment: Agency,
  Dignity, and Corrigibility**.
- `moral-uncertainty-and-value-conflict` plus
  `governance-rights-fork-exit-and-audit` into **Moral Uncertainty, Value
  Conflict, and Contestable Governance**.

The pilot already has:

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
review-ready merge packages and fold dispositions. It records no accepted
review, no manifest authorization, and no support-state effect.

The public URL/history precondition now has a policy surface:
`docs/chapter_consolidation_url_history_policy.md`. It sets the default
continuity URL, retired URL, redirect or historical-stub, and chapter-history
ledger requirements for future execution commits. It does not implement a
redirect or authorize a merge.

The current decision is still deferral, and the current pilot state is
`review_ready`: both destination drafts are review-ready, but no manifest merge
is authorized until human or external review accepts, revises, or rejects the
destination shapes and an execution package implements the retired URL
treatment required by the URL/history policy.

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

## Current Cluster Register

| Cluster | Current state | Next allowed action | Reader-work consequence |
|---|---|---|---|
| Part I alignment and agency/corrigibility | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Avoid broad curation of the two source chapters until decision. |
| Part I value conflict and contestable governance | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Avoid broad curation of the two source chapters until decision. |
| Compression and residual honesty | `review_ready` | Review the destination draft and decide execute full merge, execute conservative merge, revise, defer, or reject. | Avoid curated graduation of the source cluster unless explicitly deferred or retained. |
| Intent and executable contracts | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Keep `human-intent-as-a-formal-input` reader work local until the contract boundary is clear. |
| Static context ABI | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Avoid curated graduation of the static ABI pair unless explicitly deferred or retained; reader curation may continue on protected adjacent chapters. |
| Verification and adversarial review | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Avoid curated graduation of the verification/review pair unless explicitly deferred or retained; reader curation may continue on claim ledgers. |
| Planning and DAG control | `review_ready` | Review the destination draft and decide execute, revise, defer, or reject. | Avoid curated graduation of the planning/DAG pair unless explicitly deferred or retained; reader curation may continue on semantic IR. |
| Source-blocked MoECOT runtime | `fold_disposition_ready` | Review the fold disposition and decide execute fold, revise, defer, or reject/retain. | Do not promote MoECOT runtime as standalone reader material while source-blocked. |
| Simulation fidelity | `fold_disposition_ready` | Review the fold disposition and decide execute fold, revise, defer, or reject/retain. | Preserve physical-constraint caveats, simulation contract fields, proof hooks, and reader repairs if folded. |
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
| 1 | Part I constitutional alignment and agency/corrigibility | Execute, revise, defer, or reject. | Apply the URL/history policy for the retired agency/corrigibility slug before any manifest edit. |
| 2 | Part I value conflict and contestable governance | Execute, revise, defer, or reject. | Apply the URL/history policy for the retired governance-rights slug and preserve fork, exit, audit, redaction, appeal, dissent, and revisit interfaces. |
| 3 | Compression and residual honesty | Execute full merge, execute conservative merge, revise, defer, or reject. | Keep RankFold/NeuralFold standalone if review finds concrete technique ownership. |
| 4 | Intent and executable contracts | Execute, revise, defer, or reject. | Keep `human-intent-as-a-formal-input` as intent intake and remove only duplicated contract skeleton. |
| 5 | Static context ABI | Execute, revise, defer, or reject. | Keep transaction/snapshot/taint and verification-bandwidth chapters standalone unless later review changes artifact ownership. |
| 6 | Verification and adversarial review | Execute, revise, defer, or reject. | Keep `claim-ledgers-and-belief-revision` as the durable belief-revision substrate. |
| 7 | Planning and DAG control | Execute, revise, defer, or reject. | Keep `cognitive-compilation-and-semantic-ir` as the semantic-IR and lowering-receipt layer. |
| 8 | Fold-disposition candidates | Execute fold, revise, defer, or reject/retain. | MoECOT runtime, simulation fidelity, and semantic representation already have fold dispositions; the next work is review and decision, not more packaging, before any manifest edit. |

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
| 1C | Intent and executable contracts | `intent-to-execution-contracts`; `command-contracts-and-semantic-interfaces` | **Command Contracts: From Intent to Executable Work** | Preserve intent-to-contract conversion, semantic interface rules, authority fields, execution receipts, test hooks, and handoff from `human-intent-as-a-formal-input`. Keep `human-intent-as-a-formal-input` separate but slim it to intent intake, ambiguity, and authority extraction. |
| 1D | Static context ABI | `virtual-context-abi`; `semantic-pages-context-cells-and-certificates` | **The Virtual Context ABI: Typed Pages, Cells, and Certificates** | Preserve pages, cells, certificates, context addressing, source unions, proof hooks, and implementation horizons. Keep `context-transactions-snapshots-mounts-and-taint` and `verification-bandwidth-and-context-adequacy` separate. |
| 2A | Verification and adversarial review | `spinoza-verification-and-proof-carrying-claims`; `unified-adaptive-tribunal-and-adversarial-review` | **Proof-Carrying Claims and Adversarial Review** | Preserve proof-carrying claim tiers, tribunal review, adversarial dossiers, dissent, no-theorem-laundering boundaries, proof hooks, harness rows, and source unions. Keep `claim-ledgers-and-belief-revision` separate. |
| 2B | Planning and DAG control | `planning-as-a-control-layer`; `planforge-dags-and-intelligence-arbitrage` | **Planning as a Control Layer: DAGs and Intelligence Arbitrage** | Preserve control-layer semantics, PlanForge DAGs, intelligence arbitrage, negative cases, proof hooks, and source unions. Keep `cognitive-compilation-and-semantic-ir` separate unless later review shows the IR has no independent chapter ownership. |
| 2C | Source-blocked MoECOT runtime | `moecot-runtime-and-multi-core-orchestration`; `routing-heads-and-specialist-cores` | Fold MoECOT runtime into routing heads until the MoECOT source is fully mined enough for standalone evidence. | Preserve the multi-core orchestration runtime as a named section, blocker, source queue, and future chapter-restoration condition. |
| Fold review | Simulation fidelity | `simulation-fidelity-and-physical-constraints`; `resource-economics-and-token-budgets`; efficient-ASI frame as secondary context only | Fold if the standalone claim remains only a feasibility-bound note. | Preserve physical/resource bounds, fidelity limitations, simulation contract fields, claim-transport boundaries, proof hooks, and no-overclaim language as a named section. |
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
- `context-transactions-snapshots-mounts-and-taint`
- `verification-bandwidth-and-context-adequacy`
- `claim-ledgers-and-belief-revision`
- `labor-os-and-typed-jobs`
- `artifact-graphs-audit-logs-and-replay`
- `runtime-adapters-tool-permissions-and-human-approval`
- `procedural-memory-and-cognitive-loop-closure`
- `mathematical-and-search-substrates`
- `coil-attention-cyclic-memory-and-recurrence-contracts`
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
  dry-run package for the intent and executable-contracts cluster. It does not
  edit `book_structure.json`, authorize a manifest merge, or move support
  states. It keeps `human-intent-as-a-formal-input` standalone as the intake
  chapter.
- `docs/chapter_consolidation_destination_draft_intent_contracts.md` records
  the one-skeleton destination draft for **Command Contracts: From Intent to
  Executable Work**. It is review-ready but not reviewed, not canonical, and
  not a manifest edit. The next decision is execute, revise, defer, or reject.
- `docs/chapter_consolidation_dry_run_context_abi.md` records the Tier 1D
  dry-run package for the static context ABI cluster. It does not edit
  `book_structure.json`, authorize a manifest merge, or move support states.
  It keeps `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`, and
  `claim-ledgers-and-belief-revision` standalone.
- `docs/chapter_consolidation_destination_draft_context_abi.md` records the
  one-skeleton destination draft for **The Virtual Context ABI: Typed Pages,
  Cells, and Certificates**. It is review-ready but not reviewed, not
  canonical, and not a manifest edit. The next decision is execute, revise,
  defer, or reject.
- `docs/chapter_consolidation_dry_run_verification_review.md` records the Tier
  2A dry-run package for the verification and adversarial-review cluster. It
  does not edit `book_structure.json`, authorize a manifest merge, or move
  support states. It keeps `claim-ledgers-and-belief-revision` standalone as
  the durable claim identity, support-state, contradiction, uncertainty, and
  revision-history substrate.
- `docs/chapter_consolidation_destination_draft_verification_review.md` records
  the one-skeleton destination draft for **Proof-Carrying Claims and
  Adversarial Review**. It is review-ready but not reviewed, not canonical, and
  not a manifest edit. The next decision is execute, revise, defer, or reject.
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

## Remaining Fold-Disposition Packages

- `docs/chapter_consolidation_fold_moecot_runtime.md` records the first fold
  disposition package, for `moecot-runtime-and-multi-core-orchestration` into a
  named MoECOT Runtime Crosswalk section inside
  `routing-heads-and-specialist-cores`. It is fold-disposition ready but not
  reviewed, not executed, not canonical, and not a manifest edit. The next
  decision is execute fold, revise, defer, or reject/retain. It preserves
  `AsiStackProofs.Routing`, `AsiStackProofs.MoECOTRuntime`,
  `schemas/specialist_registry_record.schema.json`,
  `schemas/routing_decision_record.schema.json`,
  `schemas/moecot_orchestration_record.schema.json`, source unions, external
  comparator unions, reader repair requirements, URL/history policy, restoration
  conditions, and the no-support-state-change boundary.
- `docs/chapter_consolidation_fold_simulation_fidelity.md` records the second
  fold disposition package, for `simulation-fidelity-and-physical-constraints`
  into a named Simulation Fidelity and Claim Transport section inside
  `resource-economics-and-token-budgets`. It is fold-disposition ready but not
  reviewed, not executed, not canonical, and not a manifest edit. The next
  decision is execute fold, revise, defer, or reject/retain. It preserves
  `AsiStackProofs.ResourceEconomics`, `AsiStackProofs.SimulationFidelity`,
  `schemas/resource_budget_record.schema.json`,
  `schemas/simulation_contract_record.schema.json`, source unions, external
  comparator unions, reader repair requirements, URL/history policy,
  restoration conditions, and the no-support-state-change boundary.
- `docs/chapter_consolidation_fold_semantic_representation.md` records the
  third fold disposition package, for
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

- This sequence does not merge chapters.
- This sequence does not change `book_structure.json`.
- This sequence does not change Appendix C support states.
- This sequence does not create source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support.
- This sequence does not approve reader, ebook, PDF, DOCX, audio, DOI, archive,
  or release artifacts.
- This sequence does not prove that any future merged chapter will be better;
  that judgment requires review of the destination draft and reconciliation
  package.
