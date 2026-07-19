# Contributing

This repository is the canonical source for a living technical book. The manuscript is in an author-only prepublication phase: external contributions, review requests, unsolicited patches, and manuscript submissions are not being accepted before the author declares the book complete.

Issues and pull requests may be closed without incorporation during this phase. Public visibility is not an invitation to contribute and does not grant reuse rights. The technical rules below document the repository's internal discipline and the standard a future contribution policy would inherit; they are not current contribution acceptance terms.

## Ground Rules

- Treat `book_structure.json` as the source of truth for parts, chapters, source assignments, and appendices.
- Do not hand-edit `_quarto.yml`; run `python3 scripts/sync_scaffold.py`.
- Treat `docs/book_outline.md` as the source of truth for full-book drafting and Lean proof scope.
- Treat `docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md` as the sole active execution roadmap and `docs/repository_map.md` as the repository authority/storage map; historical roadmaps remain lineage, not competing work queues.
- Keep book work on `main`. Put new artifacts under their governed directory rather than the repository root, and do not track `build/`, `_site/`, `.quarto/`, private intake, or local caches.
- Do not publish private raw source exports.
- Do not fabricate source content, citations, proof results, benchmark results, or test results.
- Keep speculative claims explicitly labeled.
- Update `appendices/F_changelog.qmd` for meaningful structural, source, evidence, proof, or publication changes.

## Internal change gate

Run:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_post_v2_3_maintenance_transfer_and_publication_roadmap.py
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
quarto render --to html
```

If you changed Lean files, also run:

```bash
cd lean
lake build
```

## Source Changes

When adding or updating a source:

- Add metadata to `sources/source_inventory.json`.
- Keep raw files local unless publication is explicitly approved.
- Create `sources/source_notes/<source-id>.md` only after actually reading the source.
- Update chapter source assignments in `book_structure.json` when appropriate.
- Update Appendix C only when a claim's support state changes.

## Proof Changes

When adding or updating Lean proof scope:

- Edit the `Lean proof targets` table in `docs/book_outline.md`.
- Run `python3 scripts/sync_proof_manifest.py`.
- Implement executable proofs under `lean/` only when the formal target is operationally precise.
- Do not call a target proven unless `lake build` passes.

## Public Site Changes

The GitHub Pages workflow renders the Quarto book from `main`. Site-facing changes should preserve:

- readable navigation,
- stable chapter IDs,
- generated appendices,
- no raw/private source publication,
- no unverified evidence-state promotion.
