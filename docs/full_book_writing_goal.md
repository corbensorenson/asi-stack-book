# Full Book Writing Goal Template

Use this when starting or resuming a long-running goal to improve the whole book toward a v1.0 candidate.

## Recommended Goal

Run an extended end-to-end improvement pass on **The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI** to turn the current v0.2 manuscript baseline into a final-draft-quality v1.0 candidate.

Treat `docs/book_outline.md` as the source of truth for parts, chapters, source queues, proof targets, and drafting jobs. Treat `book_structure.json` as the source of truth for part/chapter order, stable chapter IDs, and the first-build/mature-endpoint fields published into Appendix K, `Implementation Horizons`. Use the `asi-stack-book` skill and follow the living-book workflow.

For every chapter in scope, produce cohesive systems-architecture prose rather than a paper-by-paper anthology. Preserve the required chapter contract: problem, insufficiency of existing approaches, core claim, mechanism, interfaces, invariants, failure modes, minimum viable implementation, beyond-state-of-the-art end state, Codex test plan, source crosswalk, and summary. The minimum viable implementation must name the smallest honest artifact or validated slice that can start the idea without promoting the chapter claim. The beyond-SOTA section must name the mature product-level logical conclusion without claiming it already exists: final product surface, operational contract, evidence flow, governance boundary, failure closure, and composition with the rest of the stack. Mine the assigned source notes and available raw/cache/connector sources before making source-derived claims. Create missing source notes when a chapter depends on a source that has not yet been mined.

Maintain the three-audience publication model while drafting: the live book must remain useful to AIs and human researchers through source/evidence/proof scaffolding, while the prose outside stripped live-only headings must form a clean reader-facing spine for future EPUB, PDF, DOCX, and audio releases. Do not put meaning-changing caveats only in sections that `reader_release` strips. Keep Human Reading Path bridges as direct book prose rather than meta-reader scaffolding, and keep diagrams and images meaningful for the live site and convertible into spoken summaries for audio.

Do not fabricate citations, source content, benchmark results, test results, proofs, or implementation status. Keep all claims at the support state justified by recorded artifacts. Use `source-derived` only after a source note or equivalent ingested-source artifact is mapped to the claim. Use `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` only when the relevant code, run record, external source, or evidence artifact exists. Keep speculative/metaphysical material visibly speculative.

Implement Lean proofs, executable schemas, or small tests only where the current `proofs/proof_triage.json` route supports it and the predicate is sufficiently operational. Keep schema/process/research targets planned unless real artifacts are added. Record any implemented proof or test in the relevant chapter, Appendix C, appendices, and changelog.

Update source notes, Appendix C, Appendix D/E/G/H/K as needed, keeping Appendix G reserved as its own top-level appendix for Corben's papers, Corben-supplied materials, recovered project records, and local project records and Appendix H reserved as its own top-level appendix for external sources and third-party literature. Do not present H as a second part of G. Keep `_quarto.yml`, Appendix A, Appendix C, Appendix E, Appendix G, Appendix H, and Appendix K generated through `scripts/sync_scaffold.py`. Before reporting completion, run the full launch gate:

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

Final deliverable: a rendered, public-safe v1.0-candidate living-book manuscript with an honest report of completed chapter improvements, added visuals, support-state promotions, implemented proofs/tests, reader-edition readiness, audio-script readiness, missing evidence, unresolved source gaps, and remaining release risks.
