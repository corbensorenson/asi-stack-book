# Writing Runbook

This is the operating runbook for turning the scaffold into the full living book.

## Start Every Major Writing Run

1. Read `prompts/MASTER_CODEX_PROMPT.md`.
2. Read `skills/asi-stack-book/SKILL.md`.
3. Read `book_structure.json`.
4. Read `docs/book_outline.md`, including the part-level and chapter-level source loading queues.
5. Read `sources/cache/cache_manifest.json` and `docs/source_readiness_report.md`.
6. Read the chapter files in scope.
7. Read source notes and raw cache files only for the sources in scope.
8. Read `docs/prewriting_readiness.md` and `docs/external_literature_queue.md` when starting a full-book or part-level writing run.

## Source Hierarchy

Use source material in this order:

1. Local raw source cache under `sources/raw/` when available.
2. Google Drive connector export/fetch when the local cache is missing or stale.
3. `sources/source_inventory.json` metadata when source text is unavailable.
4. Handoff notes only as planning/context, not as source-derived evidence.
5. Conversation-mined packets only as author intent, architecture lineage, terminology, and recovery cues, not as external evidence or quotable source text.

Use the source queue in `docs/book_outline.md` to decide what is in scope:

- Primary sources are loaded first for chapter claims and mechanisms.
- Supporting sources are loaded after primary sources for synthesis, variants, failure modes, and cross-layer context.
- Variant sources are used to compare versions or recover missing details.
- Connector or recovery sources must be loaded through Google Drive or kept as explicit blockers before source-derived claims.

Do not mark a claim as `source-derived` unless the actual source text was read. Do not publish private conversation wording verbatim unless the user explicitly approves that exact text.

## Chapter Drafting Loop

For each chapter:

1. Read assigned source text or source notes.
2. Extract source-backed mechanisms, claims, failure modes, and evidence.
3. Decide which claims remain design hypotheses.
4. Draft the chapter as one architecture layer, not a pasted anthology.
5. Update the chapter source crosswalk.
6. Update Appendix C if claim text, claim label, or support state changes.
7. Update glossary terms introduced by the chapter.
8. Add planned proof/code hooks when a mechanism can be formalized or tested.
9. Update `appendices/F_changelog.qmd`.
10. Run validation and render.

## Per-Chapter Definition of Done

Each chapter must maintain these sections:

- Chapter status
- Drafting guardrail
- Problem
- Why existing approaches are insufficient
- Core Claim
- Mechanism
- Interfaces
- Invariants
- Failure modes
- Minimal implementation
- Codex test plan
- Source crosswalk
- Summary

The scaffold-level contract is enforced by `python3 scripts/validate_chapter_dod.py`. A complete manuscript chapter must also keep source-derived claims mapped to source notes, keep support states honest, and avoid reporting tests, proofs, benchmarks, or external literature unless those artifacts exist.

## Claim Labels

Claim labels describe what kind of statement is being made. Support states describe what currently supports it.

| Label | Use |
|---|---|
| `Demonstrated` | A recorded artifact, derivation, implementation, or source-backed example demonstrates the claim in scope. |
| `Measured` | The claim reports a recorded measurement or benchmark result. |
| `Mechanized` | The claim is expressed as runnable code, an executable schema, or a formal proof target. |
| `Hypothesized` | The claim is testable but still needs evidence. |
| `Design rationale` | The claim is an architectural choice supported by reasoning and constraints. |
| `Speculative` | The claim is exploratory and cannot support deployment guarantees. |

## Evidence Movement Rules

| Movement | Required basis |
|---|---|
| `argument` -> `source-derived` | Actual source text read and mapped to claim. |
| `source-derived` -> `prototype-backed` | Prototype or code inspected. |
| `prototype-backed` -> `synthetic-test-backed` | Test implemented and run on synthetic cases. |
| `synthetic-test-backed` -> `empirical-test-backed` | Realistic external or field-like test run. |
| any state -> `unsupported` | Source missing, contradiction found, or claim overreaches evidence. |
| any state -> `deprecated` chapter/status | Claim or chapter superseded, failed, or merged. |
| any state -> `refuted` | Later evidence or tests contradict the claim; preserve the negative result. |

Promoted evidence records should include the relevant evidence bundle fields: source hash, code revision, environment manifest, baseline, test command, metrics, raw logs, negative results, ablations, failure reproduction, artifacts, provenance, conclusion, limitations, and release notes.

## End Every Major Writing Run

Run:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
```

For release or PDF checks:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

Then commit and push only tracked source, metadata, notes, scripts, and public-safe artifacts.
