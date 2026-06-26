# Paper Triage Reference

Use this reference when a new AI paper or source arrives.

## Required Intake Gate

Before chapter prose changes, record or decide:

- Source storage policy: public source, public note only, connector only, local private cache, external URL only, or blocked.
- Public-safety state: public-safe, needs redaction, permission required, private/restricted, or blocked.
- Deduplication state: unique boundary, overlaps an existing chapter, duplicate source, superseded variant, or blocked.
- Chapter decision refs: `book_structure.json`, `docs/book_outline.md`, Appendix C, source notes, or backlog records that justify the decision.
- Required pre-drafting work: inventory, source note, passage review, claim mapping, permission check, or citation normalization.
- Evidence-transition preconditions and promotion blockers.
- Explicit non-claims.

Use `schemas/research_backlog_record.schema.json` for durable backlog items and `schemas/new_paper_triage_scenario.schema.json` as the decision-shape model for update, add, defer, appendix-only, or reject decisions.

## Update an Existing Chapter When

- The source primarily strengthens or challenges an existing layer.
- Its concepts map cleanly to an existing chapter's problem, mechanism, invariant, or failure mode.
- It supplies evidence, counterevidence, implementation detail, or terminology for an existing claim.
- It is a variant or later version of an already-inventoried source family.

Required updates:

- Add the source ID to the chapter's `source_ids` in `book_structure.json`.
- Add or update `sources/source_notes/<source-id>.md` if the source text was actually read.
- Record why the source is not a distinct new chapter boundary.
- Update Appendix C only if claim text or support state changes.
- Update the changelog.

## Add a New Chapter When

- The source introduces a distinct stack layer, substrate, governance mechanism, or evidence program that does not fit existing chapter boundaries.
- Folding it into an existing chapter would blur layer responsibilities.
- It needs its own interface/invariant/failure-mode treatment.
- It will likely collect multiple future sources.

Required updates:

- Add the chapter with `scripts/add_chapter.py`.
- Fill in the new chapter object in `book_structure.json`.
- Run `python3 scripts/sync_scaffold.py`.
- Draft the chapter stub from source-backed material and clearly labeled design reasoning.
- Keep support at `argument` until evidence transitions, proof, or tests justify movement.
- Update the changelog.

## Keep It Unassigned When

- The source is unavailable or cannot be read.
- It appears duplicative but version ordering is unclear.
- It is speculative and not yet relevant to the architecture.
- Publication/storage rights are unclear.
- It needs external citation verification before it can support a claim.

Record this as an open source-ingestion gap rather than forcing it into the book.

## Merge or Remove a Chapter When

- Two chapters now share the same problem, mechanism, interfaces, and evidence base.
- A chapter is better represented as a section inside another chapter.
- A chapter's core claim is deprecated or unsupported and no longer deserves top-level status.

When merging, preserve useful source IDs, claim IDs, open evidence gaps, and changelog history.
