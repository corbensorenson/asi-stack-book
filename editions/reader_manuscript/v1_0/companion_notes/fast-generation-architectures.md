# Fast Generation Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `fast-generation-architectures`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/fast-generation-architectures.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/fast-generation-architectures.qmd`

Evidence references: `docs/curated_reader_fast_generation_prose_pass.md`,
`schemas/generation_mode_record.schema.json`,
`schemas/generation_mode_baseline.schema.json`,
`scripts/validate_generation_mode_baselines.py`, and
`proofs/lean/AsiStackProofs/FastGeneration.lean`.

This note helps e-reader and audio review for the Fast Generation chapter. It
does not replace the chapter prose or the curated prose draft. Meaning-critical
limits must still stay in the reader spine: speed is useful only when accepted
output, verifier cost, repair, fallback, memory pressure, task success, and
promotion evidence remain visible.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
why the chapter refuses to treat tokens per second as intelligence. A faster
route is an architecture win only when the useful accepted work per unit time
survives verification, fallback, repair, memory, and risk accounting.

## Dense Material Routed Here

| Dense item | Plain meaning | Boundary |
|---|---|---|
| Autoregressive baseline | The slower fallback and measurement anchor. | Without a baseline, speedup is not interpretable. |
| Speculative decoding | Draft output is proposed cheaply and accepted or rejected by a verifier. | Proposed output is not accepted output. |
| Multi-token prediction or multi-head drafting | The model proposes more than one future token/span at once. | More proposals can simply move work into rejection, repair, or fallback. |
| Diffusion or refinement route | A draft is generated in a different shape and then repaired toward an accepted answer. | Repair and verifier burden count against the speed claim. |
| Early-exit or self-speculative route | Cheaper intermediate outputs act as drafts and later computation verifies or corrects them. | Missing or overloaded verification blocks promotion. |
| State-space, recurrent, KV-cache, batching, and serving routes | Serving and memory-path changes can improve throughput or memory use. | Aggregate throughput is not single-request quality or reasoning improvement. |
| Speed-quality ledger | The record that separates proposed work, accepted work, wall-clock time, verifier cost, memory pressure, fallback, repair, and promotion decision. | The ledger is a claim-control surface, not a reproduced benchmark by itself. |

## Main Spine Must Keep

The reader chapter should not move these boundaries exclusively into companion
material:

- proposed tokens, spans, or artifacts are separate from accepted verified
  output;
- raw latency, aggregate throughput, and serving-memory wins do not equal task
  success, quality, reasoning, or safety;
- verifier cost, fallback, repair, memory pressure, and negative cases are part
  of the speed claim;
- missing or failed verification blocks promotion even when generation is
  faster;
- no local fast-decoding benchmark, MTP run, speculative-acceptance experiment,
  serving deployment, KV-cache audit, useful-solution-per-second result, or
  reproduced external speedup is claimed.

## Audio Treatment

In an audio script, do not read the entire generation-method taxonomy as a
catalog. Narrate it through one recurring distinction:

What did the system propose, and what did the stack actually accept?

The spoken path should preserve five beats:

- the autoregressive path remains the fallback and baseline;
- accelerated modes produce proposals or alternate routes;
- verification decides what counts;
- repair, fallback, memory pressure, and verifier backlog are real costs;
- promotion requires evidence over accepted useful work, not raw output speed.

Detailed method names and record fields can be routed to this companion note.
The main audio should keep the ordinary reader focused on the boundary between
feeling fast and being useful.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim local fast-decoding performance,
  multi-token prediction performance, speculative-acceptance performance,
  diffusion-language performance, serving throughput, KV-cache behavior,
  useful-solution-per-second improvement, quality improvement, task-success
  improvement, or reproduced external speedup.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
