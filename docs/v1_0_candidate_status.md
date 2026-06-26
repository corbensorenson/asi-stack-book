# v1.0 Candidate Status

Last updated: 2026-06-26

This document is the current public-safe status surface for the extended v1.0 improvement goal. It supersedes the older prewriting and v0.2 launch-status documents for current readiness decisions, while those older documents remain useful historical records.

The book is a stronger v1.0 candidate than the original v0.2 manuscript baseline, but it is not a v1.0 evidence release yet. The repository now has a complete manifest-driven manuscript, source-note and claim-source traceability, finite-record Lean coverage, schema fixtures, release-profile scaffolding, and a deployed Quarto site. All core chapter support states remain `argument`.

## Current Snapshot

| Surface | Current state | Evidence |
|---|---|---|
| Book structure | 4 parts, 54 manifest-driven chapters, 9 appendices | `book_structure.json`; `python3 scripts/sync_scaffold.py` |
| Manuscript scale | 54 chapter files; 112,603 chapter words excluding YAML front matter; 119,341 raw chapter-file words including metadata and live scaffolding | Local word-count check on `chapters/*.qmd` |
| Source inventory | 101 public-safe source records and 101 public source notes | `sources/source_inventory.json`; `sources/source_notes/` |
| Claim/source traceability | 461 assigned source/chapter pairs, 461 exact claim-source mappings, 461 passage-reviewed mappings | `docs/source_evidence_audit.md`; `python3 scripts/validate_source_evidence_audit.py` |
| Support states | 54 chapter core claims at `argument`; no support-state promotion in the v1.0 improvement pass | `book_structure.json`; Appendix C |
| Proof envelope | 112 proof targets, all implemented as narrow finite-record Lean predicates | `proofs/proof_manifest.json`; `docs/proof_artifact_audit.md`; `lake build` |
| Schemas and fixtures | 70 JSON Schemas, 69 valid protocol fixtures, 1 public release record | `schemas/`; `tests/fixtures/protocol_records/`; `release_records/`; `python3 scripts/validate_protocol_examples.py` |
| Visual coverage | Every chapter has at least one Mermaid diagram; landing page has a generated visual asset | `python3 scripts/validate_visual_coverage.py` |
| Release surfaces | Live, research, reader, and audio profiles exist; reader/audio derivation scripts exist | `editions/release_profiles.json`; `docs/major_version_release_runbook.md` |
| Public site | GitHub Pages renders the live Quarto book | <https://corbensorenson.github.io/asi-stack-book/> |

## What The Current Candidate Proves

- The book order is dynamic and manifest-driven.
- The outline is a usable source of truth for drafting, source queues, and Lean proof targets.
- Every manifest chapter exists and has the required chapter contract: problem, insufficiency, core claim, mechanism, interfaces, invariants, failure modes, minimal implementation, test plan, source crosswalk, and summary.
- Current source-note coverage, source-to-chapter assignment, core claim mapping, and passage-review mapping are internally traceable.
- Current proof targets are wired through outline tags, generated manifest records, triage records, Lean modules, root imports, chapter hooks, limitation prose, and Appendix E.
- Current schemas and example fixtures validate record shape for the protocol surfaces created so far.
- The live book renders locally and through GitHub Pages when the publication workflow passes.

## What It Does Not Prove

- It does not prove any ASI capability, model quality, deployment readiness, safety property, benchmark result, simulation result, or runtime behavior.
- It does not prove that source interpretation is semantically adequate for support-state promotion.
- It does not prove that the finite-record Lean predicates are the best formalization of each intended chapter boundary.
- It does not reproduce MoECOT, Theseus, Circle, Talos, VCM, PlanForge, policy-optimization, compression, routing, benchmark, or simulation results.
- It does not generate or publish EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts.
- It does not replace a final human editorial read for continuity, exposition, pedagogy, and reader-edition quality.

## Remaining Work Before v1.0 Evidence Release

- Perform claim-to-mechanism support review after the passage-reviewed mappings and record accepted evidence transitions before any claim moves above `argument`.
- Run semantic proof adequacy review for all 112 finite-record Lean targets.
- Implement or defer chapter-level Codex tests beyond protocol fixture validation, with explicit command, environment, and result records.
- Normalize additional external literature where the book currently has queues rather than direct source records and source notes.
- Import or reproduce any prototype, benchmark, Circle, Theseus, MoECOT, VCM, Talos, PlanForge, compression, routing, or policy-training artifact before using it as stronger evidence.
- Generate and review reader-edition artifacts only after a tagged live-book candidate passes the live/research gate.
- Generate audio scripts and audio artifacts only from a reviewed reader edition and record exact produced artifacts.
- Complete a final reader-facing editorial pass to reduce remaining scaffolding feel without weakening evidence boundaries.

## Candidate Gate

Before tagging or continuing to describe a state as a v1.0 candidate, run:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
```

Before describing a state as a v1.0 evidence release, also record the accepted evidence transitions, rendered reader artifacts if any, audio artifacts if any, and release records that actually exist.
