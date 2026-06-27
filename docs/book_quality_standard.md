# Book Quality Standard

The book should read like a serious systems architecture text.

## Manuscript Standards

- The book must explain one architecture, not collect isolated papers.
- Each chapter must state the layer's problem, mechanism, interfaces, invariants, failure modes, minimum viable implementation, beyond-state-of-the-art end state, test plan, and source crosswalk.
- The minimum viable implementation must identify the smallest honest artifact, fixture, proof predicate, schema, trace, or validated slice that can start the idea. The beyond-state-of-the-art end state must identify the mature product-level logical conclusion, including how it composes with neighboring layers and what evidence would be required before support-state promotion.
- Each chapter must satisfy the machine-checked scaffold DoD in `scripts/validate_chapter_dod.py`.
- Philosophical material must be translated into engineering-compatible constraints, claims, and failure modes.
- Speculative material must remain visibly speculative.
- Claims must not outrun support states.
- Repeated terms must use glossary definitions consistently.

## Evidence Standards

- No fabricated citations.
- No fabricated test results.
- No source-derived label without source text.
- No source-derived label without a source note or equivalent ingested-source artifact.
- No source-derived label from source-note mapping alone; the mapped claim needs passage review or an accepted evidence transition with limitations.
- No prototype-backed label without inspected prototype/code.
- No test-backed label without an actual run record.
- Negative, inconclusive, or failed results stay visible.

## Site Standards

- The first page should orient readers immediately: what the book is, current status, how to read support labels, and where the source/evidence appendices are.
- Navigation must work after chapter insertion, deletion, or movement.
- Public pages should not expose private raw source text.
- The site should make the living status obvious rather than pretending to be a finished static book.
- Rendered HTML and PDF should both remain available when local tooling supports PDF.

## Engineering Standards

- Any runnable test, proof, or benchmark must live in a reproducible folder.
- Proofs and code examples must be linked from chapters only after they exist.
- Proof targets must stay aligned with `proofs/proof_triage.json`; schema/process/research targets need executable contracts or clearer predicates before they become implemented Lean.
- Proof triage status must match the generated proof manifest; implemented proof targets must remain formal Lean candidates backed by root-imported modules and a passing Lean build.
- Experimental results must include command, date, environment, and result summary.
- Validation scripts should fail on structural drift or placeholder chapter sections rather than silently tolerating them.
