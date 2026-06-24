# Full Book Writing Goal Template

Use this when starting the long-running goal to draft the whole book.

## Recommended Goal

Write the complete v0.2 manuscript draft of **The ASI Stack: A Systems Architecture for Governed, Efficient, Self-Improving AI** from the current Quarto scaffold.

Treat `docs/book_outline.md` as the source of truth for parts, chapters, source queues, proof targets, and drafting jobs. Treat `book_structure.json` as the source of truth for part/chapter order and stable chapter IDs. Use the `asi-stack-book` skill and follow the living-book workflow.

For every chapter, produce cohesive systems-architecture prose rather than a paper-by-paper anthology. Preserve the required chapter contract: problem, insufficiency of existing approaches, core claim, mechanism, interfaces, invariants, failure modes, minimal implementation, Codex test plan, source crosswalk, and summary. Mine the assigned source notes and available raw/cache/connector sources before making source-derived claims. Create missing source notes when a chapter depends on a source that has not yet been mined.

Do not fabricate citations, source content, benchmark results, test results, proofs, or implementation status. Keep all claims at the support state justified by recorded artifacts. Use `source-derived` only after a source note or equivalent ingested-source artifact is mapped to the claim. Use `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` only when the relevant code, run record, external source, or evidence artifact exists. Keep speculative/metaphysical material visibly speculative.

Implement Lean proofs, executable schemas, or small tests only where the current `proofs/proof_triage.json` route supports it and the predicate is sufficiently operational. Keep schema/process/research targets planned unless real artifacts are added. Record any implemented proof or test in the relevant chapter, Appendix C, appendices, and changelog.

Update source notes, Appendix C, Appendix D/E/G as needed, and keep `_quarto.yml`, Appendix A, Appendix C, Appendix E, and Appendix G generated through `scripts/sync_scaffold.py`. Before reporting completion, run the full launch gate:

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
(cd lean && lake build)
quarto render --to html
```

Final deliverable: a rendered, public-safe, complete v0.2 living-book manuscript draft with an honest report of completed chapters, support-state promotions, implemented proofs/tests, missing evidence, unresolved source gaps, and remaining v1.0 work.
