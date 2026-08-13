# Repository Map

This file identifies authority and storage boundaries. It is intentionally not an inventory of every tracked file.

## Authority order

When two files appear to describe the same state, use this order:

1. `book_structure.json` owns parts, chapter order, IDs, source assignments, chapter-core claims, implementation horizons, and appendix order.
2. `docs/book_outline.md` owns chapter jobs, source-loading queues, and formal-target planning.
3. `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md` is the sole active roadmap. Machine authority lives in `roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json`.
4. `sources/source_inventory.json` owns public-safe source metadata.
5. Accepted evidence transitions and claim decisions own support movement.
6. `appendices/F_changelog.qmd` records meaningful public changes but does not supersede any owner above.

Earlier roadmaps are immutable execution history, not competing current plans. Exactly one current record may correspond to the active-roadmap marker.

## Storage and lifecycle classes

| Class | Paths | Rule |
|---|---|---|
| Canonical manuscript | `book_structure.json`, `index.qmd`, `preface.qmd`, `chapters/`, `appendices/`, `docs/book_outline.md` | Tracked and edited through the book workflow. |
| Sources and citations | `sources/source_inventory.json`, `sources/source_notes/`, `research_backlog_records/`, `new_paper_triage_scenarios/`, `citations/` | Track public-safe metadata, reviewed synthesis, and schema-bound source-intake decisions; keep raw/private exports ignored. |
| Public author-paper library | `papers/paper_library.json`, `papers/index.qmd`, `papers/*.qmd`, `papers/source/`, `schemas/paper_library.schema.json` | The manifest selects exact Corben-supplied paper and architecture-source bytes for public reading while preserving manuscript-level authorship and collaborator credits. Tracked source copies preserve digest identity; generated QMD pages provide HTML presentation, chapter lineage, and evidence/rights boundaries. Adding a paper requires explicit publication authority, a receipt, a source note, and a deterministic reader route. |
| Governed evidence | `evidence_quality/`, `evidence_transitions/`, `claim_decisions/`, `experiments/`, `proofs/`, `release_records/`, `roadmap_records/` | Preserve exact lineage when the bytes are part of an evidence, governance, or release contract. |
| Implementation | `scripts/`, `schemas/`, `lean/`, `tests/`, `protocols/` | Track reusable code, fixtures, schemas, and formal source. |
| Governed visual edition | `visual_edition/`, `skills/asi-stack-manim-videos/`, `schemas/manim_*`, `scripts/*manim*` | Track the repository-local audiovisual authoring standard; machine-auditable beat, experience-review, and generation-2 ledger contracts; Manim scene source, storyboards, narration, reviewed captions, descriptive transcripts, thumbnails, manifests, the canonical YouTube channel contract, exact generation-N supersession plans, and immutable render/platform receipts. `visual_edition/manim_v2_production_ledger.json` owns the current 84-target remediation state and preserves the generation-one predecessors; `visual_edition/youtube_ledger.json` owns platform identity after acceptance. Keep animatics, final video, narration audio, review frames, and Manim caches in ignored `build/`; YouTube owns published binaries. |
| Generated local output | `build/`, `_site/`, `.quarto/`, `lean/.lake/`, `site_libs/` | Ignored and non-authoritative; delete after the active review no longer needs it. |
| Private/local intake | `sources/inbox/`, `sources/raw/`, `sources/cache/`, `_archive/local_context/` | Ignored except explicit policy or readiness manifests. |
| Public history | `archive/` | Retain only when current URLs, provenance, or consolidation lineage require tracked bytes. Git history is the default home for superseded process artifacts. |

Tracked files above 40 MiB require an explicit validator allowlist and evidence rationale. 60 MiB is the project hard ceiling for new tracked files.

## Write discipline

Every new tracked file must have:

1. a durable role that cannot be served by an existing canonical owner;
2. a named consumer such as the manuscript, a validator, a governance decision, or a release record;
3. a lifecycle class from the table above.

Do not create one report per work session, validator run, chapter edit, or failed experiment. Update an existing ledger or roadmap when the information is state, use an append-only governed record when exact history is evidence, and keep transient diagnostics under ignored `build/` or `/tmp`.

Prefer targeted checks during drafting. Run the full HTML render when manuscript, navigation, assets, or site behavior changes. EPUB, PDF, DOCX, e-reader, and audio work is reserved for an explicitly approved major-version release gate. This prevents repeated writes and avoids spending compute on derivatives that the next content edit will replace.

## Common workflows

| Change | Owner and action |
|---|---|
| Add, move, merge, or remove a chapter | Edit `book_structure.json`, run `python3 scripts/sync_scaffold.py`, then repair affected handoffs. |
| Change proof scope | Edit the Lean target table in `docs/book_outline.md`, then run `python3 scripts/sync_proof_manifest.py`. |
| Add a source | Update `sources/source_inventory.json`; add a source note only after reviewing the source; regenerate `docs/chapter_external_grounding_status.md` when chapter coverage changes. |
| Publish or update an author paper | Update `papers/paper_library.json`, the Corben corpus closure and receipt when needed, then run `python3 scripts/sync_paper_library.py` followed by `python3 scripts/sync_scaffold.py`. The exact source copy and HTML projection must remain digest-bound; publication does not promote evidence. |
| Change support state | Add or revise the governed transition/decision record; regenerate Appendix C. |
| Audit defended-contribution prior art | Review `docs/defended_contribution_prior_art_positioning.md`, then run `scripts/validate_defended_contribution_prior_art.py`. Positioning is not proof of novelty. |
| Audit evidence-laundering defenses | Review `docs/evidence_laundering_prevention_case_studies.md`, then run `scripts/validate_evidence_laundering_case_studies.py`. Passing preserves case-study boundaries; it does not promote a claim. |
| Audit historical chapter consolidation | Use `docs/chapter_consolidation_sequence.md` and `docs/chapter_consolidation_url_history_policy.md` as public entrypoints; run `scripts/validate_chapter_consolidation_sequence.py` for the complete retained history. |
| Review or execute current publication consolidation | Use the `P7.1-EM` section of `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md` and `editorial_product_migration` in `roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json`; preserve the 87 stable technical identities until a gated semantic merge executes. |
| Write the independent human-reader edition | Use `docs/human_reader_26_unit_outline.md` as the canonical 26-unit writing specification and `docs/book_outline.md` as the 87-owner technical-reference outline. Preserve `products/narrative_product_spine.json` as the historical 22-unit candidate until the 26-unit manuscript passes its cutover gate. |
| Audit chapter-template inheritance | Use `docs/p7_1a_w3_inheritance_guard.md` and `evidence_quality/p7_1a_w3_inheritance_guard.json`; rebuild with `scripts/build_p7_1a_w3_inheritance_guard.py` and validate the current prose plus copied/distinct fixtures with `scripts/validate_p7_1a_w3_inheritance_guard.py`. |
| Audit Round 20 chapter substance and atom custody | Use `docs/round_20_depth_and_substance_reconciliation_2026_07_27.md` as the reader decision, `evidence_quality/chapter_substance_contract.json` as the regenerated current-book editorial contract, and `evidence_quality/round20_four_chapter_claim_atom_addendum.json` as the append-only custody packet. Rebuild and validate them with the matching `build_*` and `validate_*` scripts. The substance contract is refreshed after manifest, chapter, or atom-source changes; the atom addendum is immutable evidence-history once superseded. Passing either does not promote support. |
| Inspect or run the Phase 5 harness set | Use `experiments/phase5_harness_registry.json` and `docs/test_harness_status_ledger.md` as the canonical registry and public summary; check them with `scripts/validate_phase5_harness_registry.py` and execute them through `scripts/run_phase5_harnesses.py`. |
| Inspect the P5 natural publication path | Use `experiments/p5_natural_publication_service_trace/results/2026-07-27-development.json` as the governed external-observation record and `docs/p5_natural_publication_service_development_trace.md` as its reader boundary; `scripts/validate_p5_natural_publication_service_trace.py` is the named consumer. The record is retained as evidence-history under the governed-evidence lifecycle class and is superseded only by a later dated trace, never rewritten into prospective or claim-bearing evidence. |
| Run the P5-U1 governed repository-change demonstrator | Run `python3 scripts/run_p5_u1_governed_repository_change.py`, inspect `build/p5_u1/latest/result.json` and the twelve route/path workspaces, then run `python3 scripts/validate_p5_u1_governed_repository_change.py` against the tracked result. The task is a retrospective replay of a real Human Reader source-link defect; it compares direct, record-only, and fully governed local Git routes but is not a prospective utility, human-effort, production, safety, or support-state result. |
| Inspect or advance the P5 natural stateful-service campaign | Use `experiments/governed_operations_argument_exit/preregistration.json` as the sole prospective campaign authority and `docs/p5_natural_stateful_service_campaign_preregistration.md` as its design decision. The authored implementation receipt is `experiments/governed_operations_argument_exit/qualification/2026-07-28-local.json`; its reader boundary is `docs/p5_natural_stateful_service_campaign_qualification.md`, and `scripts/validate_p5_natural_service_campaign_qualification.py` reruns and adversarially validates it. Preserve dated amendments before held-out opening; after opening, task/arm/metric/denominator changes are forbidden. The qualification ran no natural tasks and cannot borrow P2/Q1/Q2 tasks, substitute for Theseus T4, create a public effect, or move support/release state. |
| Revise human prose | Edit the chapter's human path or governed reader overlay while preserving evidence boundaries. |
| Build or update a chapter visual abstract | Follow `skills/asi-stack-manim-videos/SKILL.md`; place generation-2 source under `visual_edition/chapters/<chapter-id>/generation-2/`; keep animatics and review frames under ignored `build/visual_edition/`; update and validate `visual_edition/manim_v2_production_ledger.json`; and do not promote a valid render past animatic, picture-and-sound lock, release candidate, independent review, technical, claim-fidelity, and acceptance gates. After acceptance, regenerate the publication ledger and use `scripts/prepare_youtube_supersession.py`, `scripts/record_youtube_supersession_receipt.py`, and `scripts/reconcile_youtube_supersession_receipt.py`. Each replacement requires its own exact plan-digest authority, keeps immutable generation receipts, makes the predecessor unlisted and points it to the successor, removes only its canonical playlist item, and never deletes either generation automatically. A video becomes current in Quarto only after the reconciled current YouTube identity exists. |
| Prepare a major release | Follow `docs/major_version_release_runbook.md` only after the roadmap opens that gate. |
| Validate ordinary work | Run targeted validators and `python3 scripts/validate_book.py`. For a complete public site, render the 85-chapter book with `quarto render --to html`, then render the unnumbered sibling paper library with `quarto render papers --to html`. |

## Non-claims

- A tracked file is not evidence merely because it passes schema validation.
- A source note is not a claim promotion.
- A Lean theorem proves its encoded model, not the whole chapter.
- A local render is not a public release.
- Historical files do not reopen completed work.
