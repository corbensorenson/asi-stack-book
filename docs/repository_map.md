# Repository Map

This repository is organized around the living book and its validation loop.

| Path | Role | Public status |
|---|---|---|
| `book_structure.json` | Source of truth for parts, chapters, stable IDs, source assignments, and appendices. | tracked |
| `_quarto.yml` | Generated Quarto configuration. | tracked; do not hand-edit |
| `index.qmd`, `preface.qmd` | Front matter for the rendered book. | tracked |
| `chapters/` | Chapter source files. | tracked |
| `appendices/` | Generated and curated appendices: source matrix, glossary, claims, schemas, tests, changelog, bibliography, and author-intent lineage. | tracked |
| `docs/book_outline.md` | Full-book drafting outline, source loading queues, and Lean proof target source of truth. | tracked |
| `docs/source_mining_synthesis.md` | Source-mining coverage, architecture cluster map, split rationale, and remaining source gaps. | tracked |
| `docs/local_project_mining_theseus_circle.md` | Public-safe local mining report for Project Theseus and Circle Calculus. | tracked |
| `docs/conversation_context_ingestion_report.md` | Public-safe synthesis of conversation-mined author intent and recovery tasks. | tracked |
| `docs/fast_generation_context_ingestion_report.md` | Public-safe synthesis of the fast-generation browser-GPT planning note and evidence boundaries. | tracked |
| `docs/` | Runbooks, quality standards, readiness reports, and publication guidance. | tracked |
| `sources/source_inventory.json` | Public-safe source metadata inventory. | tracked |
| `sources/cache/cache_manifest.json` | Public-safe cache metadata and hashes. | tracked |
| `sources/raw/` | Local raw source exports. | ignored |
| `sources/inbox/` | Local source drop area, including private or conversation-mined packets before public-safe synthesis. | ignored except README |
| `sources/source_notes/` | Public-safe notes created after source text is actually read. | tracked when notes are added |
| `proofs/` | Proof plans and generated proof target manifest. | tracked |
| `lean/` | Lean 4 proof workspace. | tracked except `.lake/` |
| `schemas/` | JSON Schemas for protocol records. | tracked |
| `release_records/` | Public-safe living-book release validation records checked against `schemas/living_book_release_record.schema.json`. | tracked |
| `experiments/` | Synthetic experiment and benchmark harness workspace. | tracked |
| `scripts/` | Manifest sync, source cache, proof manifest, and validation tools. | tracked |
| `skills/asi-stack-book/` | Project-specific Codex skill for maintaining and drafting the book. | tracked |
| `.github/` | GitHub Pages workflow, issue templates, and PR template. | tracked |
| `_site/`, `.quarto/`, `site_libs/` | Render/build outputs and Quarto cache. | ignored |

## Ownership Rules

- Edit `book_structure.json`, then run `python3 scripts/sync_scaffold.py`.
- Edit `docs/book_outline.md`, then run `python3 scripts/sync_proof_manifest.py`.
- Edit public source metadata in `sources/source_inventory.json`; keep raw source text out of git unless publication is explicitly approved.
- Update `appendices/F_changelog.qmd` for meaningful changes.

## Public Readiness Invariants

- No raw source exports are tracked.
- No rendered `_site/` output is tracked.
- No `.quarto/` cache is tracked.
- No Lean `.lake/` build output is tracked.
- No claim support state is promoted without a recorded basis.
- No proof or test result is reported unless the command was run and the result is recorded.
- Conversation-mined context is treated as author intent and lineage, not as external evidence or quotable source text.
