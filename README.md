# The ASI Stack

**The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI**

This repository is the canonical Quarto source for Corben Sorenson's living technical book. The project treats the source papers as fragments of one architecture: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

## Current Status

This is a v0.1 scaffold seed.

- Quarto book structure is initialized.
- All 16 outline chapters have stubs.
- `docs/book_outline.md` contains the cohesive full-book drafting outline.
- Parts and chapters are controlled by `book_structure.json`; `_quarto.yml` is generated.
- The source matrix is generated from `sources/source_inventory.json`.
- The bibliography/source-corpus appendix is generated from `sources/source_inventory.json`.
- The claim/evidence matrix is initialized with `argument`-level placeholders.
- Source documents are cached locally when available, but source-derived claims require source notes before support-state promotion.
- Codex tests are planned but not implemented or run.

## Local Commands

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
quarto render --to html
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

The rendered HTML is written to `_site/`.

## Dynamic Structure

Do not hand-edit `_quarto.yml` or number chapter filenames. Edit `book_structure.json`, then run:

```bash
python3 scripts/sync_scaffold.py
```

Useful helpers:

```bash
python3 scripts/add_part.py --title "Part IV - New Research Track"
python3 scripts/add_chapter.py --part stack-layers --title "New AI Topic" --after planning-and-control
```

The helpers update the manifest. The sync script updates Quarto, generated matrices, and missing chapter stubs.

## Proof Targets

`docs/book_outline.md` is the source of truth for Lean proof scope. Every chapter has `lean:*` proof tags under `Lean proof targets`.

Generate the machine-readable proof manifest from the outline:

```bash
python3 scripts/sync_proof_manifest.py
```

The generated file is `proofs/proof_manifest.json`. Do not report a theorem as proven unless the corresponding Lean module exists and `lake build` passes.

## Source Cache

Raw source exports are private/local and ignored by git.

```bash
python3 scripts/cache_drive_sources.py
python3 scripts/source_readiness_report.py
```

The tracked readiness report is `docs/source_readiness_report.md`. Raw exports stay under `sources/raw/`.

## Codex Skill

The project-specific writing/maintenance skill lives at `skills/asi-stack-book/` and has also been installed locally to `~/.codex/skills/asi-stack-book`.

To reinstall from the repo copy:

```bash
rsync -a --exclude='.DS_Store' skills/asi-stack-book/ ~/.codex/skills/asi-stack-book/
```

## Public Site

The GitHub Pages workflow publishes the rendered Quarto book from `main`:

<https://corbensorenson.github.io/asi-stack-book/>

## Evidence Discipline

Do not mark a claim as `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` unless the source ingestion, prototype review, or test execution actually happened and is recorded.
