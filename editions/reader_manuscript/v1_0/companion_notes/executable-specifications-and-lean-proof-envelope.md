# Executable Specifications Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `executable-specifications-and-lean-proof-envelope`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/executable-specifications-and-lean-proof-envelope.qmd`

Evidence references: `proofs/proof_manifest.json`,
`proofs/proof_triage.json`, `docs/proof_adequacy_review.md`,
`docs/proof_depth_classification.md`, and
`appendices/E_codex_test_specs.qmd`.

This note helps e-reader and audio review for the proof-envelope chapter. It
does not replace the chapter prose. Meaning-critical limits must still stay in
the reader spine: a passed Lean build supports only the finite predicate it
checks; schemas, tests, benchmarks, and theorem references are different
evidence lanes; and semantic adequacy remains required before proof artifacts
can strengthen broader prose claims.

## Reader Promise

After reading or hearing this companion note, a human should be able to tell why
the book treats Lean proofs, schemas, process validators, behavior tests,
benchmarks, external theorem references, and semantic adequacy review as
different kinds of authority rather than one generic proof bucket.

## Proof-Lane Glossary

| Lane | Plain meaning | Boundary |
|---|---|---|
| Lean predicate | A finite proposition or record invariant checked by the local Lean build. | It proves only the stated predicate, not deployed enforcement or model quality. |
| Schema validation | A JSON or protocol record has the required shape and fields. | It does not prove that the represented event happened. |
| Process validator | A script checks wiring, references, registry consistency, or record discipline. | It does not prove semantic truth unless that is exactly what the validator checks. |
| Behavior test | A fixture or local harness exercises a path or rejects a negative case. | It does not become a theorem or broad empirical result. |
| Benchmark | A measured run compares behavior under stated data, baselines, and metrics. | It says nothing outside the recorded setup. |
| External theorem reference | A theorem or formal-methods artifact from another source is named as comparator or context. | It is not local proof ownership unless imported, built, and reviewed under the repo's rules. |
| Semantic adequacy review | A review that asks whether the finite predicate is the right predicate for the prose boundary. | It is not a second proof; it prevents proof laundering. |
| Research backlog | A target that matters but lacks the artifact, predicate, or review needed for stronger status. | It keeps the work visible without pretending completion. |

## Example Boundary

A Lean theorem can show that a finite `SupportTransition` record does not move
above `argument` unless required evidence fields are present. That is useful.
It does not prove that every future agent will enforce the rule in production,
that the evidence fields are truthful, that source interpretation is correct,
or that the surrounding ASI architecture is safe.

The proof envelope exists so the book can say the first sentence without
quietly implying the others.

## Audio Treatment

In an audio script, narrate the proof envelope as claims-control discipline:

- a broad claim is lowered into a small target before it can be checked;
- the artifact lane determines what kind of authority the result has;
- a passed verifier changes only the narrow state it actually checked;
- semantic adequacy asks whether the narrow predicate matches the prose use;
- no proof lane removes the need for evidence boundaries, source review, or
  release records.

The detailed proof-lane table can be routed to this companion note. The main
audio should keep the distinction between proof, validation, test, benchmark,
and review clear in ordinary language.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim proof adequacy beyond the recorded finite
  predicates.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
