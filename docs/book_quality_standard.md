# Book Quality Standard

The book should read like a serious systems architecture text.

## Manuscript Standards

- The book must explain one architecture, not collect isolated papers.
- Each chapter must state the layer's problem, mechanism, interfaces, invariants, failure modes, minimal implementation, test plan, and source crosswalk.
- Philosophical material must be translated into engineering-compatible constraints, claims, and failure modes.
- Speculative material must remain visibly speculative.
- Claims must not outrun support states.
- Repeated terms must use glossary definitions consistently.

## Evidence Standards

- No fabricated citations.
- No fabricated test results.
- No source-derived label without source text.
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
- Experimental results must include command, date, environment, and result summary.
- Validation scripts should fail on structural drift rather than silently tolerating it.
