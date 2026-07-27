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
| Sources and citations | `sources/source_inventory.json`, `sources/source_notes/`, `citations/` | Track public-safe metadata and reviewed synthesis; keep raw/private exports ignored. |
| Governed evidence | `evidence_quality/`, `evidence_transitions/`, `claim_decisions/`, `experiments/`, `proofs/`, `release_records/`, `roadmap_records/` | Preserve exact lineage when the bytes are part of an evidence, governance, or release contract. |
| Implementation | `scripts/`, `schemas/`, `lean/`, `tests/`, `protocols/` | Track reusable code, fixtures, schemas, and formal source. |
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
| Change support state | Add or revise the governed transition/decision record; regenerate Appendix C. |
| Audit defended-contribution prior art | Review `docs/defended_contribution_prior_art_positioning.md`, then run `scripts/validate_defended_contribution_prior_art.py`. Positioning is not proof of novelty. |
| Audit evidence-laundering defenses | Review `docs/evidence_laundering_prevention_case_studies.md`, then run `scripts/validate_evidence_laundering_case_studies.py`. Passing preserves case-study boundaries; it does not promote a claim. |
| Audit historical chapter consolidation | Use `docs/chapter_consolidation_sequence.md` and `docs/chapter_consolidation_url_history_policy.md` as public entrypoints; run `scripts/validate_chapter_consolidation_sequence.py` for the complete retained history. |
| Audit chapter-template inheritance | Use `docs/p7_1a_w3_inheritance_guard.md` and `evidence_quality/p7_1a_w3_inheritance_guard.json`; rebuild with `scripts/build_p7_1a_w3_inheritance_guard.py` and validate the current prose plus copied/distinct fixtures with `scripts/validate_p7_1a_w3_inheritance_guard.py`. |
| Inspect or run the Phase 5 harness set | Use `experiments/phase5_harness_registry.json` and `docs/test_harness_status_ledger.md` as the canonical registry and public summary; check them with `scripts/validate_phase5_harness_registry.py` and execute them through `scripts/run_phase5_harnesses.py`. |
| Revise human prose | Edit the chapter's human path or governed reader overlay while preserving evidence boundaries. |
| Prepare a major release | Follow `docs/major_version_release_runbook.md` only after the roadmap opens that gate. |
| Validate ordinary work | Run targeted validators, `python3 scripts/validate_book.py`, and HTML rendering when the public book changed. |

## Non-claims

- A tracked file is not evidence merely because it passes schema validation.
- A source note is not a claim promotion.
- A Lean theorem proves its encoded model, not the whole chapter.
- A local render is not a public release.
- Historical files do not reopen completed work.
