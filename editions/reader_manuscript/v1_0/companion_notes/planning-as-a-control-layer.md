# Planning Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `planning-as-a-control-layer`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/planning-as-a-control-layer.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/planning-as-a-control-layer.qmd`

Evidence references: `docs/curated_reader_planning_control_prose_pass.md`,
`schemas/plan_graph.schema.json`, `schemas/planforge_dag.schema.json`,
`schemas/typed_job_record.schema.json`, `scripts/validate_plan_execution_contracts.py`,
and `proofs/lean/AsiStackProofs/Planning.lean`.

This note helps e-reader and audio review for the Planning chapter. It does not
replace the chapter prose or the curated prose draft. Meaning-critical limits
must still stay in the reader spine: a plan is not execution, a useful node is
not automatically dispatchable, replanning may not widen authority silently, and
local schemas/proofs validate finite control boundaries rather than open-world
planner quality.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
why planning is treated as a governed control layer rather than a nicer to-do
list. The central question is not whether a plan looks plausible. It is which
nodes may dispatch, which nodes must block, what authority they inherit, what
evidence they require, and what residuals survive replanning.

## Dense Material Routed Here

| Dense item | Plain meaning | Boundary |
|---|---|---|
| Plan graph | The record that connects a command contract to nodes, dependencies, context needs, authority, risk, budget, verification, residuals, and dispatch state. | A graph makes planning inspectable; it does not prove the planner decomposes well. |
| DAG scheduling | A schedulable dependency structure with acyclicity and ordered work. | A valid DAG is not a guarantee of good task strategy or runtime success. |
| Adequacy contract | The condition that makes a node's output usable by downstream work. | Cheap work is unacceptable if it fails adequacy. |
| Dispatch receipt | The record that allows a plan node to become typed work. | Useful, proposed, or blocked nodes do not dispatch without this receipt. |
| Replanning history | The record of how feedback changed order, routes, assumptions, or residuals. | Replanning may not erase authority deltas, stop conditions, or failure evidence. |
| Residual register | The visible list of unresolved context, authority, quality, dependency, cost, or verification gaps. | Residuals are planning outputs, not cleanup details. |

## Main Spine Must Keep

The reader chapter should not move these boundaries exclusively into companion
material:

- accepted command contracts bound the plan;
- only dispatchable nodes lower into typed jobs;
- blocked nodes, missing context, failed adequacy, cyclic dependencies,
  authority gaps, and stop conditions are valid planning outcomes;
- replanning preserves authority, stop-condition, source, and residual deltas;
- local proof and fixture artifacts do not prove planner quality, task
  decomposition, scheduler performance, selected-tier adequacy, live runtime
  dispatch, or tool execution.

## Audio Treatment

In an audio script, do not read every plan-field name as a list. Narrate
planning as controlled dispatch:

- a command becomes a graph;
- graph nodes can be proposed, blocked, dispatchable, replanned, stopped, or
  residual;
- dispatch needs context, authority, dependencies, adequacy, and verification;
- replanning is allowed only when it preserves the boundary that changed;
- the local artifacts check finite record discipline, not general planning
  intelligence.

Detailed field names can be routed to this companion note. The main audio
should keep the ordinary reader focused on the bridge from accepted command to
lawful work.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim planner quality, decomposition quality,
  dependency discovery, selected-tier adequacy, scheduler performance, runtime
  replanning, live dispatch safety, tool execution, cost savings, or deployed
  planning control.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
