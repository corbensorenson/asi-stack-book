# The ASI Stack

**The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI**

This repository is the canonical Quarto source for Corben Sorenson's living technical book. The project treats the source papers as fragments of one architecture: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement.

## Current Status

This is a v0.1 scaffold seed.

- Quarto book structure is initialized.
- All 16 outline chapters have stubs.
- The source matrix is generated from `sources/source_inventory.json`.
- The claim/evidence matrix is initialized with `argument`-level placeholders.
- Source documents have not yet been ingested into this repo.
- Codex tests are planned but not implemented or run.

## Local Commands

```bash
python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
quarto render --to html
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

The rendered HTML is written to `_site/`. The full render also writes `_site/The-ASI-Stack.pdf`.

## Public Site

The GitHub Pages workflow publishes the rendered Quarto book from `main`:

<https://corbensorenson.github.io/asi-stack-book/>

## Evidence Discipline

Do not mark a claim as `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` unless the source ingestion, prototype review, or test execution actually happened and is recorded.
