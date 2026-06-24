# Writing Runbook

This is the operating runbook for turning the scaffold into the full living book.

## Start Every Major Writing Run

1. Read `prompts/MASTER_CODEX_PROMPT.md`.
2. Read `skills/asi-stack-book/SKILL.md`.
3. Read `book_structure.json`.
4. Read `sources/cache/cache_manifest.json`.
5. Read the chapter files in scope.
6. Read source notes and raw cache files only for the sources in scope.

## Source Hierarchy

Use source material in this order:

1. Local raw source cache under `sources/raw/` when available.
2. Google Drive connector export/fetch when the local cache is missing or stale.
3. `sources/source_inventory.json` metadata when source text is unavailable.
4. Handoff notes only as planning/context, not as source-derived evidence.

Do not mark a claim as `source-derived` unless the actual source text was read.

## Chapter Drafting Loop

For each chapter:

1. Read assigned source text or source notes.
2. Extract source-backed mechanisms, claims, failure modes, and evidence.
3. Decide which claims remain design hypotheses.
4. Draft the chapter as one architecture layer, not a pasted anthology.
5. Update the chapter source crosswalk.
6. Update Appendix C if claim text or support state changes.
7. Update glossary terms introduced by the chapter.
8. Add planned proof/code hooks when a mechanism can be formalized or tested.
9. Update `appendices/F_changelog.qmd`.
10. Run validation and render.

## Evidence Movement Rules

| Movement | Required basis |
|---|---|
| `argument` -> `source-derived` | Actual source text read and mapped to claim. |
| `source-derived` -> `prototype-backed` | Prototype or code inspected. |
| `prototype-backed` -> `synthetic-test-backed` | Test implemented and run on synthetic cases. |
| `synthetic-test-backed` -> `empirical-test-backed` | Realistic external or field-like test run. |
| any state -> `unsupported` | Source missing, contradiction found, or claim overreaches evidence. |
| any state -> `deprecated` chapter/status | Claim or chapter superseded, failed, or merged. |

## End Every Major Writing Run

Run:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/validate_book.py
quarto render --to html
```

For release or PDF checks:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

Then commit and push only tracked source, metadata, notes, scripts, and public-safe artifacts.
