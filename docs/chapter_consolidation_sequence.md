# Governed Chapter Consolidation Sequence

Last updated: 2026-06-29

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

## Consolidation State Model

| State | Meaning | Required next move |
|---|---|---|
| `planned_candidate` | The cluster is directionally plausible but has no dry-run package or destination draft. | Create a cluster-specific reconciliation plan before any manifest or reader-manuscript change depends on it. |
| `fold_review_candidate` | The source chapter may be a section rather than a chapter-owning artifact. | Produce a fold disposition that names preserved sections, subclaims, source IDs, proof hooks, reader paths, and restoration conditions. |
| `dry_run_packaged` | A package proposes the manifest diff, claim/source/proof/reader reconciliation, and validation path, but no destination prose is accepted. | Write a one-skeleton destination draft or reject the merge as not improving chapter ownership. |
| `review_ready` | The dry-run package and one-skeleton destination draft exist and can be judged by Corben, an editor, or an external reviewer. | Record an execute, revise, defer, or reject decision before touching `book_structure.json`. |
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
- `docs/chapter_consolidation_decision_review.md`;
- `docs/chapter_consolidation_external_review_packet.md`.

The current decision is still deferral, and the current pilot state is
`review_ready`: both destination drafts are review-ready, but no manifest merge
is authorized until human or external review accepts, revises, or rejects the
destination shapes and the project has a public URL or redirect policy for
folded chapters.

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
| Compression and residual honesty | `dry_run_packaged` | Write a one-skeleton destination draft or reject the merge as not improving chapter ownership. | Avoid curated graduation of the source cluster unless explicitly deferred. |
| Intent and executable contracts | `planned_candidate` | Build a dry-run package and slim the intent-intake handoff only if the package passes. | Keep `human-intent-as-a-formal-input` reader work local until the contract boundary is clear. |
| Static context ABI | `planned_candidate` | Build a dry-run package that protects dynamic transaction and verification-bandwidth chapters. | Reader curation may continue outside the static ABI pair. |
| Verification and adversarial review | `planned_candidate` | Build a dry-run package that keeps claim ledgers separate. | Avoid merging review vocabulary into claim-ledger prose prematurely. |
| Planning and DAG control | `planned_candidate` | Build a dry-run package that keeps semantic IR separate unless evidence says otherwise. | Reader curation may continue on non-overlapping planning chapters. |
| Source-blocked MoECOT runtime | `fold_review_candidate` | Decide whether to fold as a named routing-runtime section until source mining catches up. | Do not promote MoECOT runtime as standalone reader material while source-blocked. |
| Simulation fidelity | `fold_review_candidate` | Decide whether the feasibility-bound argument belongs in resource economics or the efficient-ASI frame. | Preserve physical-constraint caveats if folded. |
| Semantic representation | `fold_review_candidate` | Decide whether representation is a substrate section in the compression cluster or a standalone artifact. | Preserve proof/test hooks if folded. |
| Runtime adapters and Labor OS | `rejected_or_retained` unless later evidence changes artifact ownership | Revisit only if tool-permission adapters stop owning a distinct artifact. | Reader curation may proceed because the current split has artifact ownership. |

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
| Fold review | Simulation fidelity | `simulation-fidelity-and-physical-constraints`; `resource-economics-and-token-budgets` or the efficient-ASI frame | Fold if the standalone claim remains only a feasibility-bound note. | Preserve physical/resource bounds, fidelity limitations, and no-overclaim language as a named section. |
| Fold review | Semantic representation | `semantic-representation-and-tree-structured-models`; compression/representation cluster | Fold only if representation remains a substrate facet rather than a chapter-owning artifact. | Preserve tree-structured representation, source mappings, and proof/test hooks as a named section or companion note. |
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

## Reader Work Sequencing

Broad human-reader curation should avoid source chapters inside a pending
consolidation cluster until that cluster is executed, revised, rejected, or
explicitly deferred for the release. Local prose fixes remain allowed when they
do not entrench duplicate structure.

Reader curation may continue outside pending clusters, especially where the
chapter owns a distinct artifact, proof lane, evidence lane, or implementation
path. The current allowed pilot-reader set remains:

- `asi-is-a-stack-not-a-model`
- `the-efficient-asi-hypothesis`
- `recursive-self-improvement-boundaries`
- `circle-calculus-and-proof-carrying-ai-contracts`
- `artifact-steward-agents-and-living-project-governance`

## Non-Pilot Dry-Run Packages

- `docs/chapter_consolidation_dry_run_compression.md` records the Tier 1B
  dry-run package for the compression and residual-honesty cluster. It does not
  edit `book_structure.json`, authorize a manifest merge, or move support
  states. It keeps the RankFold/NeuralFold Conservative option open and leaves
  `semantic-representation-and-tree-structured-models` as a separate
  fold-review candidate.

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
