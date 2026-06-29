# External Review Packet

Last updated: 2026-06-29

This packet is the public request surface for early external human review of
**The ASI Stack** v1.x roadmap. It is designed for reviewers with expertise in
AI safety, formal methods, AI governance and evaluations, agent systems,
machine-learning systems, or technical publishing.

Public request issue:
<https://github.com/corbensorenson/asi-stack-book/issues/1>

## Review Boundary

External review is review input. It is not source evidence, a proof result, a
benchmark result, artifact approval, or a support-state transition. A reviewer
comment can create a roadmap task, GitHub issue, source candidate, proof target,
chapter rewrite task, demotion, or blocker. It can promote a claim only if a
separate accepted evidence-transition record later names independently
source-noted material, a proof, a replay, a test, an artifact review, or other
accepted evidence.

## Primary Review Targets

| Target | Why it matters | Suggested entry point |
|---|---|---|
| Safety-critical proof scope | The current Lean hooks are broad but shallow in the five safety-critical modules. | `docs/proof_depth_classification.md`; `docs/proof_adequacy_review.md` |
| Support-state honesty | Readers need to see what is argued, what is source-noted, and what is actually tested or replayed. | `appendices/C_claim_evidence_matrix.qmd`; `docs/non_core_evidence_ledger.md` |
| v1.x roadmap aim | The roadmap should focus on defended contribution tracks rather than broad self-sourced coverage. | `docs/v1_x_beyond_sota_roadmap.md`; `docs/a_plus_quality_scorecard.md` |
| External grounding | Corben-originated terminology should be related to known literature and systems without overclaiming novelty. | `docs/external_sota_positioning_audit.md`; `appendices/H_external_sources.qmd` |
| Human readability | Human view and future reader editions should read as a book while preserving evidence boundaries. | Live site Human view; `docs/reader_chapter_review_matrix.md` |

## Requested Questions

1. Which claim, chapter, proof target, or roadmap item is most likely wrong,
   already solved elsewhere, too weakly sourced, or over-framed?
2. Do the 60-second trust surface and non-core evidence ledger make the current
   support boundary legible quickly?
3. Are the five safety-critical Lean modules scoped honestly, and which richer
   state, transition, negative case, or theorem should come first?
4. Which external papers, standards, tools, systems, or benchmarks should be
   added before the book asks readers to accept its terminology?
5. Which chapter should be used as the first human-reader curation pilot, and
   what would make it feel like a high-quality book chapter?

## Response Template

Reviewers can respond in GitHub issue #1 or in a separate review note with this
shape:

| Field | Reviewer input |
|---|---|
| Reviewer background | Safety, formal methods, governance/evals, agent systems, ML systems, publishing, or other. |
| Review scope | Files, chapters, appendices, rendered pages, or artifacts reviewed. |
| Strongest issue | The highest-severity correctness, evidence, novelty, proof, or readability finding. |
| Specific recommended action | Source to add, theorem to deepen, test to run, chapter to rewrite, claim to demote, or blocker to record. |
| Attributability | Public attributable, public anonymous, private/non-attributable, or other. |

## Non-Claims

- This packet does not mean an independent external review has happened.
- This packet does not create source evidence or external-literature support.
- This packet does not promote any chapter core claim above `argument`.
- This packet does not approve v1.x, reader, ebook, PDF, DOCX, or audio release
  readiness.
