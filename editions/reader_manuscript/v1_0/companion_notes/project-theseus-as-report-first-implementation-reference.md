# Project Theseus Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `project-theseus-as-report-first-implementation-reference`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/project-theseus-as-report-first-implementation-reference.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/project-theseus-as-report-first-implementation-reference.qmd`

Evidence references: `docs/curated_reader_project_theseus_prose_pass.md`,
`docs/theseus_report_import_slice.md`,
`docs/theseus_generation_mode_import_slice.md`,
`docs/theseus_support_replay_probe.md`,
`schemas/theseus_report_crosswalk_record.schema.json`,
`schemas/theseus_report.schema.json`,
`schemas/theseus_generation_mode_import.schema.json`,
`scripts/validate_theseus_report.py`,
`scripts/validate_theseus_generation_mode_import.py`,
`scripts/validate_theseus_support_replay_probe.py`, and
`lean/AsiStackProofs/TheseusReference.lean`.

This note helps e-reader and audio review for the Project Theseus chapter. It
does not replace the chapter prose or the curated prose draft.
Meaning-critical limits must still stay in the reader spine: Theseus is used as
report-first implementation-reference context, not proof that the ASI Stack is
implemented, benchmarked, deployed, or safe.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
why Project Theseus belongs in the book without mistaking it for public runtime
proof. The point is report discipline: a prototype should leave behind the
contract, route, work item, gate, residual, checksum, replay note, missing
artifact, and non-claim that make its status inspectable.

## Dense Material Routed Here

| Dense item | Plain meaning | Boundary |
|---|---|---|
| Report-first reference | A prototype is useful only through the report bundle that survives the run. | Dashboard prose is not evidence by itself. |
| Static architecture-gate import | A public-safe imported report with digest and boundary checks. | It is not a clean current Theseus rerun. |
| Static generation-mode import | A public-safe imported generation-mode gate summary with speed-boundary checks. | It does not prove useful-solution-per-second improvement or model quality. |
| Support replay probe | A local ASI-side rerun of validators against tracked import artifacts. | It reruns this repository's validators, not Project Theseus itself. |
| Missing-artifact row | A visible record that a needed report, command, environment, permission, or artifact is absent. | Missing status blocks promotion instead of becoming prose confidence. |
| Theseus Report Crosswalk Record | The record that maps one ASI layer to one Theseus report/config/tool surface with source, replay, publication, residual, and non-claim fields. | It is a public-boundary map, not a runtime capability. |

## Main Spine Must Keep

The reader chapter should not move these boundaries exclusively into companion
material:

- imported reports, historical source notes, support probes, current dashboard
  state, and clean reruns are different evidence states;
- source-reported status does not become reproduced evidence by being retold;
- promotion requires present passing gate records where policy demands them;
- private or non-public artifacts cannot be treated as public evidence;
- no clean live Theseus replay, reproduced benchmark run, current dashboard
  verification, deployed Theseus runtime behavior, generation-speed result,
  model-quality result, training-readiness result, deployment-readiness result,
  or support-state promotion is claimed.

## Audio Treatment

In an audio script, narrate Theseus as a report discipline, not as a triumphant
prototype story:

- a dashboard can point to reports, but it is not the report;
- imported reports can be useful and still historical;
- replay boundaries say what was rerun and what was not;
- missing artifacts are first-class blockers;
- the value is making implementation evidence falsifiable.

Detailed report IDs, digest fields, and validator names can be routed to this
companion note. The main audio should keep the ordinary reader focused on the
question: what survives the run as public evidence?

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim a clean live Project Theseus replay,
  reproduced benchmark, current dashboard state, runtime evidence, generation
  speed, useful-solution-per-second improvement, model quality, training
  readiness, deployment readiness, or support-state movement.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
