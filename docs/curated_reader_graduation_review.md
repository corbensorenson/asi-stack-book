# Curated Reader Graduation Review

Last updated: 2026-06-29

This note records the v1.0 decision about whether the normal human-reader book
should graduate from generated reader source plus semantic overlays into a
tracked curated reader manuscript. It is not a reader release record, not an
ebook/document/PDF/audio artifact record, and not a support-state promotion.

## Inputs

- Reader manuscript manifest: `editions/reader_manuscript/v1_0/manifest.json`
- Curated source contract: `editions/reader_manuscript/v1_0/curation_contract.json`
- Contract summary: `docs/curated_reader_source_contract.md`
- Reconciliation template: `editions/reader_manuscript/v1_0/reconciliation_report.md`
- Chapter review matrix: `editions/reader_manuscript/v1_0/chapter_review_matrix.json`
- Public review summary: `docs/reader_chapter_review_matrix.md`
- Reader overlay manifest: `editions/reader_overlays/v1_0/manifest.json`
- Generated reader source: `build/reader_edition/`

## Current State

- Curated reader manuscript status: `drafting`
- Generated-reader chapter-text review: complete for all 54 current chapters
- Active reader-overlay operations: 33
- Companion-note candidates: 3
- Curated-manuscript candidates: 10
- Curated chapter records: 17 drafting records for
  `asi-is-a-stack-not-a-model`,
  `the-efficient-asi-hypothesis`,
  `system-boundaries-and-authority`,
  `failure-modes-of-ungoverned-intelligence`,
  `evidence-states-and-claim-discipline`,
  `human-intent-as-a-formal-input`,
  `security-kernel-and-digital-scifs`,
  `stable-capability-fields`,
  `capability-replacement-and-rollback`,
  `readiness-gates-residual-escrow-and-quarantine`,
  `context-transactions-snapshots-mounts-and-taint`,
  `verification-bandwidth-and-context-adequacy`,
  `claim-ledgers-and-belief-revision`,
  `recursive-self-improvement-boundaries`,
  `circle-calculus-and-proof-carrying-ai-contracts`,
  `executable-specifications-and-lean-proof-envelope`, and
  `artifact-steward-agents-and-living-project-governance`
- Release blockers: reader release records and format artifact review remain
  open for every chapter
- Consolidation gate: `docs/chapter_consolidation_decision_review.md` defers
  the Part I alignment/governance manifest merge for this v1.x cycle, so
  reader curation may proceed outside the pending merge cluster without
  locking in avoidable duplicate skeletons.

## Decision

Graduate drafting-only curated reader sources for the opener, Efficient ASI,
System Boundaries, Failure Modes, Evidence States, Human Intent, Security
Kernel, Stable Capability Fields, Capability Replacement and Rollback,
Readiness Gates, Context Transactions, Verification Bandwidth, Claim Ledgers,
Recursive Self-Improvement,
`circle-calculus-and-proof-carrying-ai-contracts`,
`executable-specifications-and-lean-proof-envelope`, and
`artifact-steward-agents-and-living-project-governance`; do not treat any file
as a reader release artifact.

Generated reader source plus tracked semantic overlays is still the right
release baseline for v1.0 because most current reader problems are localized:
table-to-prose transformations, proof-vocabulary density, companion-note
routing, and artifact-layout review. Those are better handled by overlays,
companion notes, and release-review records than by creating a full parallel
manuscript before the human edition has release artifacts.

The curated manuscript path remains necessary for the future. It should be used
when reader editing becomes paragraph- and chapter-structural rather than
section-local: reordering examples, rewriting openings and closings across
multiple sections, compressing long implementation ladders, adding sustained
reader examples, or producing a final bedtime-readable major-version prose
source.

After the consolidation decision review, curated-reader work should start with
pilot chapters outside the pending Part I merge cluster. The four source
chapters named in the alignment/governance consolidation pilot should not
receive broad reader-only graduation until their merge is executed or
permanently rejected; otherwise the human manuscript would preserve the same
duplicate skeletons the consolidation pilot is trying to remove.

## Candidate Chapters

| Chapter | Current disposition | Graduation decision |
|---|---|---|
| `asi-is-a-stack-not-a-model` | pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_asi_stack_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `the-efficient-asi-hypothesis` | pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_efficient_asi_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `system-boundaries-and-authority` | foundational protected standalone chapter outside the pending consolidation cluster; active overlay already existed for permission-class prose | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_system_boundaries_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and deployed authorization enforcement is not claimed. |
| `failure-modes-of-ungoverned-intelligence` | foundational protected standalone chapter outside the pending consolidation cluster; owns the failure-obligation map that follows authority boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_failure_modes_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no scenario-coverage, deployed-detection, or deployed-prevention claim is implied. |
| `evidence-states-and-claim-discipline` | protected standalone evidence-discipline chapter and active evidence-cycle lane outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_evidence_states_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no claim-support movement is implied. |
| `human-intent-as-a-formal-input` | local prose improvement allowed by the consolidation decision review; outside the pending four-chapter merge cluster but adjacent to a possible future Constitutional Alignment destination | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_human_intent_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and the handoff must be revisited if the Part I consolidation changes the Constitutional Alignment destination. |
| `security-kernel-and-digital-scifs` | protected standalone security-boundary chapter outside the pending consolidation cluster; owns least-exposure, handle-lease, Digital SCIF, and authority-receipt reader vocabulary | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_security_kernel_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed security, sandbox-isolation, side-channel-resistance, prompt-injection-containment, OWASP-conformance, or NIST-zero-trust-implementation claim is implied. |
| `stable-capability-fields` | protected standalone capability-identity chapter outside the pending consolidation cluster; owns field/implementation separation, qualification leases, route-validation boundaries, authority ceilings, and rollback obligations | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_stable_capability_fields_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed route validation, authority enforcement, replacement safety, rollback execution, SLSA workflow, SemVer checker, object-capability implementation, or MoECOT runtime reproduction claim is implied. |
| `capability-replacement-and-rollback` | protected standalone replacement-control chapter outside the pending consolidation cluster; owns candidate/accepted replacement separation, regression floors, residual escrow, monitor windows, rollback receipts, and evaluator independence | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_capability_replacement_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed replacement behavior, real regression-suite quality, monitor-window success, rollback execution, evaluator-integrity enforcement, authority enforcement, MoECOT runtime reproduction, or implemented-corrigibility claim is implied. |
| `readiness-gates-residual-escrow-and-quarantine` | protected standalone readiness-control chapter outside the pending consolidation cluster; owns scoped permission, residual escrow, productive quarantine, stale-gate prevention, inherited residuals, and lifecycle control | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_readiness_gates_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no deployed readiness engine, residual-ledger storage, benchmark quality, live quarantine routing, gate-expiry enforcement, live rerouting, current Theseus runtime behavior, or MoECOT replay claim is implied. |
| `context-transactions-snapshots-mounts-and-taint` | protected standalone transaction-memory chapter outside the pending static context ABI merge package; owns memory-as-accountable-state, mounted snapshots, branches, taint/deletion closure, typed faults, and downstream artifact inheritance | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_context_transactions_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no memory-store behavior, read-your-writes result, branch-isolation result, mount-visibility result, replay correctness, poisoning resistance, side-channel defense, VCM conformance, or Digital SCIF implementation claim is implied. |
| `verification-bandwidth-and-context-adequacy` | protected standalone context-adequacy chapter outside the pending static context ABI merge package; owns generation-versus-verification, target-claim scoped adequacy, semantic-unit comparison, escalation, and mode-confusion boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_verification_bandwidth_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no contradiction-rate benchmark, distractor-resistance result, summary-fidelity result, adequacy-classifier correctness, deployed VCM behavior, deployed escalation, or support-state movement claim is implied. |
| `claim-ledgers-and-belief-revision` | protected standalone belief-revision substrate outside the pending verification/adversarial-review merge package; owns claim identity, support states, contradiction links, revision history, downgrade behavior, and confidence-laundering boundaries | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_claim_ledgers_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, no reader artifact is approved, and no claim-extraction, contradiction-detection, semantic-equivalence, citation-correctness, belief-engine, deployed-epistemic-correctness, or support-state movement claim is implied. |
| `recursive-self-improvement-boundaries` | pilot curated reader chapter outside the pending consolidation cluster | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_recursive_self_improvement_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `artifact-steward-agents-and-living-project-governance` | `curated_manuscript_candidate`, `companion_note_candidate`, active overlays | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_artifact_steward_prose_pass.md`. Reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `circle-calculus-and-proof-carrying-ai-contracts` | `companion_note_candidate`, active overlays | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_circle_contracts_prose_pass.md`; companion/glossary treatment remains active, reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |
| `executable-specifications-and-lean-proof-envelope` | `companion_note_candidate`, active overlay | First drafting-only curated reader prose pass completed and recorded in `docs/curated_reader_executable_specs_prose_pass.md`; companion/glossary treatment remains active, reconciliation remains incomplete, release blockers remain active, and no reader artifact is approved. |

## Graduation Triggers

Graduate a chapter into curated reader source only when at least one of these is
true:

- a reader-only change touches multiple sections and would be brittle as overlay
  replacements;
- the chapter needs sustained example, analogy, pacing, or paragraph-order
  changes that should not alter the AI/research source;
- companion-note routing is not enough to make dense proof, schema, or
  governance material readable;
- release editing identifies human-prose improvements that are too broad for
  `editions/reader_overlays/` but do not belong in the canonical live chapter.

## Required Controls If Graduation Starts

- Add a curated chapter record under
  `editions/reader_manuscript/v1_0/manifest.json`.
- Store curated chapter files under
  `editions/reader_manuscript/v1_0/chapters/`.
- Follow `editions/reader_manuscript/v1_0/curation_contract.json` for required
  record fields, allowed edit scopes, blocked divergence, meaning-preservation
  checks, and pre-release blockers.
- Update `editions/reader_manuscript/v1_0/reconciliation_report.md`.
- Preserve generated-reader baseline refs, live-source refs, claim boundaries,
  source boundaries, proof/test status, implementation horizons, and release
  blockers.
- Run `python3 scripts/validate_reader_manuscript_manifest.py`.
- Run `python3 scripts/sync_reader_chapter_review_matrix.py --check`.

## Non-Claims

- This review creates seventeen drafting-only curated reader chapter files for
  future prose editing; it does not approve any file for release.
- This review does not create or approve EPUB, PDF, DOCX, HTML, audio, or
  audio-embedded EPUB artifacts.
- This review does not remove release blockers from any chapter.
- This review does not promote any support state.
- This review does not make the reader manuscript an equal source of truth
  beside the live AI/research book.
