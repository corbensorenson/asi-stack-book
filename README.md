# The ASI Stack

**The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI** is Corben Sorenson's living technical book about AI systems architecture.

Public book site: <https://corbensorenson.github.io/asi-stack-book/>

Public repository: <https://github.com/corbensorenson/asi-stack-book>

This repository is the canonical Quarto source for the book, its scaffolding, validation scripts, schemas, Lean proof workspace, and public-safe source/evidence metadata. The book treats the source papers as fragments of one architecture: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

## Current Status

The project is ready for manuscript drafting, but it is not yet a completed book.

- Quarto book structure is initialized and renders to HTML.
- All 16 outline chapters exist as guarded stubs.
- `docs/book_outline.md` is the source of truth for the full-book drafting plan and Lean proof scope.
- `book_structure.json` controls parts, chapter order, stable chapter IDs, and appendix order.
- `_quarto.yml`, Appendix A, Appendix C, and Appendix G are generated.
- `proofs/proof_manifest.json` is generated from `lean:*` proof tags in the outline.
- Source documents are cached locally when available, but raw exports are ignored and not published.
- Claims remain `argument` level unless source notes, prototypes, tests, proofs, or external literature justify promotion.
- Codex tests are planned; test results are not recorded unless they have actually been run.

## Start Here

| File or page | Purpose |
|---|---|
| [Live book](https://corbensorenson.github.io/asi-stack-book/) | Rendered public site. |
| [docs/book_outline.md](docs/book_outline.md) | Cohesive full-book outline and proof target source of truth. |
| [book_structure.json](book_structure.json) | Manifest for dynamic parts, chapters, source assignments, and appendices. |
| [appendices/A_source_matrix.qmd](appendices/A_source_matrix.qmd) | Generated source-to-chapter matrix. |
| [appendices/C_claim_evidence_matrix.qmd](appendices/C_claim_evidence_matrix.qmd) | Generated claim/evidence matrix. |
| [appendices/G_bibliography.qmd](appendices/G_bibliography.qmd) | Generated bibliography and source-corpus appendix. |
| [proofs/proof_manifest.json](proofs/proof_manifest.json) | Generated Lean proof target manifest. |
| [docs/repository_map.md](docs/repository_map.md) | Repository layout and ownership map. |
| [docs/publication_readiness.md](docs/publication_readiness.md) | Public-readiness checklist and known blockers. |

## Local Validation

Run this before committing structural, source, proof, or publication changes:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
quarto render --to html
```

For Lean proof work:

```bash
cd lean
lake build
```

The rendered HTML is written to `_site/`, which is ignored by git.

## Dynamic Book Structure

Do not hand-edit `_quarto.yml` or use numbered chapter filenames. Edit `book_structure.json`, then run:

```bash
python3 scripts/sync_scaffold.py
```

Useful helpers:

```bash
python3 scripts/add_part.py --title "Part IV - New Research Track"
python3 scripts/add_chapter.py --part stack-layers --title "New AI Topic" --after planning-and-control
```

Quarto generates displayed chapter numbers at render time, so chapters can be inserted, moved, merged, or removed without renumbering files.

## Source Discipline

Raw source exports are private/local and ignored by git.

```bash
python3 scripts/cache_drive_sources.py
python3 scripts/source_readiness_report.py
```

The tracked readiness report is `docs/source_readiness_report.md`. Raw exports stay under `sources/raw/`.

Do not mark a claim as `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` unless the source ingestion, prototype review, proof check, or test execution actually happened and is recorded.

## Proof Discipline

`docs/book_outline.md` is the source of truth for Lean proof scope. Every chapter has `lean:*` proof tags under `Lean proof targets`.

Generate the machine-readable proof manifest from the outline:

```bash
python3 scripts/sync_proof_manifest.py
```

Do not report a theorem as proven unless the corresponding Lean module exists and `lake build` passes.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version:

- Preserve the manifest-driven structure.
- Keep speculative claims labeled.
- Do not publish private raw sources.
- Do not fabricate source content, citations, proofs, benchmark results, or test results.
- Run validation and render locally before proposing changes.

## Rights

See [LICENSE.md](LICENSE.md). This public repository is available for reading and review, but no reuse license is granted unless Corben Sorenson provides one separately.
