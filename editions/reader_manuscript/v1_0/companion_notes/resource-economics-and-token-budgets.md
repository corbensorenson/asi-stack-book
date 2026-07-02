# Resource Economics Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `resource-economics-and-token-budgets`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/resource-economics-and-token-budgets.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/resource-economics-and-token-budgets.qmd`

Evidence references: `docs/curated_reader_resource_economics_prose_pass.md`,
`docs/resource_flagship_lane_run.md`, `docs/v1_x_active_evidence_cycle.md`,
`experiments/resource_flagship_lane/results/2026-07-01-local.json`,
`schemas/resource_budget_record.schema.json`, and
`proofs/lean/AsiStackProofs/ResourceEconomics.lean`.

This note helps e-reader and audio review for the Resource Economics chapter.
It does not replace the chapter prose or the curated prose draft.
Meaning-critical limits must still stay in the reader spine: budgets are
control records, not permission to erase verification; cost savings must count
verifier cost, repair burden, fallback frequency, human-review load, evidence
loss, memory pressure, and residual ownership; and local synthetic slices do
not prove deployed scheduler, production workload, or economic outcomes.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
why the chapter treats resource use as governance rather than bookkeeping. The
point is not to make the stack cheap by cutting the expensive checks. The point
is to decide which work is worth doing only after protected costs and residuals
are visible.

## Dense Material Routed Here

| Dense item | Plain meaning | Boundary |
|---|---|---|
| `ResourceBudgetRecord` | The record that ties task value, risk, cost, capacity, verification tax, serving pressure, protected gates, budget decision, escalation, residuals, and evidence refs to a route or plan. | It makes cost pressure inspectable; it does not prove economic optimality. |
| Costed-route slice | A four-route synthetic selector fixture where failed verification and hidden residuals are rejected before the lowest-cost eligible route is selected. | It is a bounded public fixture, not a deployed scheduler. |
| Workflow trace | A deterministic dispatch record that checks ordering, protected high-risk review, displaced-cost residuals, and no-promotion boundaries. | It is trace discipline, not production workload evidence. |
| Local replay probe | A local command replay across Resource validators with output digests and artifact hashes. | It improves reproducibility of local checks but does not create a support-state transition. |
| Workload-quality probe | A small local timing comparison for scoped validator routes with a rejected no-op control. | It is not an external workload-quality review or stable speedup result. |
| Load-stability probe | A finite synthetic burst workload that checks overload reduction, residualized deferrals, review-erasure rejection, and Lean fixture alignment. | It does not prove real load stability or reviewer-capacity optimization. |
| CI cost profile | Publication-pipeline run metadata that records duration and failure/repair patterns. | It is pipeline metadata only, not a book-quality or economic result. |

## Main Spine Must Keep

The reader chapter should not move these boundaries exclusively into companion
material:

- verification tax is protected cost, not waste;
- budgets cannot bypass safety, source, proof, privacy, or human-review gates;
- a cheaper route that hides residuals or drops review is rejected;
- the accepted Resource transition is narrow and non-core;
- the workflow, live-probe, workload-quality, load-stability, and CI-cost
  sublanes currently have explicit no-change/no-promotion decisions;
- no deployed scheduler, production workload, stable speedup, economic outcome,
  welfare result, serving-throughput result, KV-cache behavior result, or
  chapter-core support-state promotion is claimed.

## Audio Treatment

In an audio script, do not read every validator, fixture, and result field as a
list. Narrate the chapter around a recurring question:

What did this route make cheaper, and where did the cost go?

The spoken path should preserve five beats:

- cost is a governance signal only after protected checks are priced in;
- hidden residuals are rejected even when they look cheap;
- local fixtures are useful because they make the boundary inspectable;
- no-promotion decisions are honest progress because they prevent evidence
  laundering;
- stronger claims require live or external workload evidence.

Detailed validator names, result fields, and sublane records can be routed to
this companion note. The main audio should keep the ordinary reader focused on
resource economics as disciplined choice, not austerity.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim a deployed scheduler, production workload,
  live cost-quality experiment, stable speedup, economic optimality, welfare
  result, serving-throughput result, KV-cache behavior result, model-quality
  result, or external workload-quality review.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
