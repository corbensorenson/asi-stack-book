# Reader Chapter Review Matrix

Last updated: 2026-07-03

This document is generated from `editions/reader_manuscript/v1_0/chapter_review_matrix.json` by `python3 scripts/sync_reader_chapter_review_matrix.py --write`.

It is a Phase 2 review-control surface for the normal human-reader manuscript. It is not a reader release, not an ebook/document/PDF/audio release, and not a support-state promotion.

Format-artifact blockers are reconciled against `editions/reader_manuscript/v1_0/format_review_matrix.json`; chapter rows cannot clear `format_artifact_not_reviewed` while reader formats or the edition release record remain blocked.

## Counts

| Kind | Count |
|---|---:|
| review_status:reviewed | 44 |
| disposition:companion_note_candidate | 12 |
| disposition:curated_manuscript_candidate | 44 |
| disposition:no_immediate_action | 44 |
| disposition:reader_overlay_active | 29 |
| release_blocker:format_artifact_not_reviewed | 44 |
| release_blocker:reader_release_record_not_created | 44 |

## Chapter Queue

| Part | Chapter | Review status | Depth | Overlays | Dispositions | Release blockers |
|---|---|---|---|---:|---|---|
| Part I - Foundations, Alignment, and Governance | `asi-is-a-stack-not-a-model` | reviewed | full_chapter_review | 2 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `the-efficient-asi-hypothesis` | reviewed | full_chapter_review | 1 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `system-boundaries-and-authority` | reviewed | full_chapter_review | 2 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `failure-modes-of-ungoverned-intelligence` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `evidence-states-and-claim-discipline` | reviewed | full_chapter_review | 3 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `human-intent-as-a-formal-input` | reviewed | full_chapter_review | 1 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `constitutional-alignment-substrate` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `moral-uncertainty-and-value-conflict` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `stable-capability-fields` | reviewed | full_chapter_review | 0 | no_immediate_action, curated_manuscript_candidate | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `capability-replacement-and-rollback` | reviewed | full_chapter_review | 0 | no_immediate_action, curated_manuscript_candidate | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `security-kernel-and-digital-scifs` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part I - Foundations, Alignment, and Governance | `recursive-self-improvement-boundaries` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `intent-to-execution-contracts` | reviewed | full_chapter_review | 2 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `planning-as-a-control-layer` | reviewed | full_chapter_review | 1 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `cognitive-compilation-and-semantic-ir` | reviewed | full_chapter_review | 0 | no_immediate_action, curated_manuscript_candidate | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `virtual-context-abi` | reviewed | full_chapter_review | 2 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `context-transactions-snapshots-mounts-and-taint` | reviewed | full_chapter_review | 1 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `verification-bandwidth-and-context-adequacy` | reviewed | full_chapter_review | 1 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `claim-ledgers-and-belief-revision` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `spinoza-verification-and-proof-carrying-claims` | reviewed | full_chapter_review | 2 | reader_overlay_active, no_immediate_action, curated_manuscript_candidate | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `labor-os-and-typed-jobs` | reviewed | full_chapter_review | 1 | curated_manuscript_candidate, reader_overlay_active, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `artifact-graphs-audit-logs-and-replay` | reviewed | full_chapter_review | 1 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `runtime-adapters-tool-permissions-and-human-approval` | reviewed | full_chapter_review | 2 | curated_manuscript_candidate, reader_overlay_active, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part II - Planning, Memory, Reasoning, and Execution | `procedural-memory-and-cognitive-loop-closure` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `routing-heads-and-specialist-cores` | reviewed | full_chapter_review | 1 | reader_overlay_active, companion_note_candidate, no_immediate_action, curated_manuscript_candidate | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `readiness-gates-residual-escrow-and-quarantine` | reviewed | full_chapter_review | 1 | reader_overlay_active, no_immediate_action, curated_manuscript_candidate | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `personal-compute-hives-and-federated-edge-intelligence` | reviewed | full_chapter_review | 7 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `compact-generative-systems-and-residual-honesty` | reviewed | full_chapter_review | 3 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `fast-generation-architectures` | reviewed | full_chapter_review | 3 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `rankfold-neuralfold-and-artifact-compression` | reviewed | full_chapter_review | 2 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `resource-economics-and-token-budgets` | reviewed | full_chapter_review | 0 | companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `mathematical-and-search-substrates` | reviewed | full_chapter_review | 1 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `circle-calculus-and-proof-carrying-ai-contracts` | reviewed | full_chapter_review | 6 | reader_overlay_active, curated_manuscript_candidate, companion_note_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `coil-attention-cyclic-memory-and-recurrence-contracts` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part III - Routing, Compression, Representation, and Substrates | `coilra-multicoil-rope-and-cyclic-mixers` | reviewed | full_chapter_review | 0 | companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `executable-specifications-and-lean-proof-envelope` | reviewed | full_chapter_review | 9 | reader_overlay_active, curated_manuscript_candidate, companion_note_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `benchmark-ratchets-and-anti-goodhart-evidence` | reviewed | full_chapter_review | 3 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `policy-optimization-and-learning-from-feedback` | reviewed | full_chapter_review | 2 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `artifact-steward-agents-and-living-project-governance` | reviewed | full_chapter_review | 4 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `integrated-reference-architecture` | reviewed | full_chapter_review | 2 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `project-theseus-as-report-first-implementation-reference` | reviewed | full_chapter_review | 1 | reader_overlay_active, companion_note_candidate, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `prototype-roadmap` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `living-book-methodology` | reviewed | full_chapter_review | 3 | reader_overlay_active, curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |
| Part IV - Evidence, Implementation, and the Living Book | `open-research-agenda-and-bibliography-plan` | reviewed | full_chapter_review | 0 | curated_manuscript_candidate, no_immediate_action | reader_release_record_not_created, format_artifact_not_reviewed |

## Non-Claims

- This matrix is a reader-review queue, not a reviewed reader release.
- This matrix does not create EPUB, PDF, DOCX, HTML, audio, or audio-embedded EPUB artifacts.
- This matrix does not promote any claim support state.
- This matrix does not supersede the live Quarto book for claims, source boundaries, proof/test status, implementation horizons, or release records.
