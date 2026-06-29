# Chapter Consolidation Fold Disposition: MoECOT Runtime

Status: fold-disposition ready; human/external review not completed.

This is a review artifact for the governed consolidation sequence. It does not
edit `book_structure.json`, merge chapters, change Appendix C support states,
create source/proof/test evidence, approve reader artifacts, or promote any
claim above `argument`.

This disposition does not edit `book_structure.json`.

## Candidate

| Field | Value |
|---|---|
| Fold candidate | `moecot-runtime-and-multi-core-orchestration` |
| Candidate title | MoECOT Runtime and Multi-Core Orchestration |
| Proposed destination | `routing-heads-and-specialist-cores` |
| Destination title | Routing Heads and Specialist Cores |
| Proposed fold section | MoECOT Runtime Crosswalk |
| Current state | `fold_disposition_ready` |
| Required decision | Execute fold, revise fold disposition, defer for release, or reject and retain standalone. |

## Rationale

The fold recommendation is not that MoECOT is unimportant. The recommendation
is that its current standalone chapter is mostly an implementation-reference
crosswalk over the routing/runtime evidence packet the routing chapter already
owns. Routing owns the durable artifact boundary: the specialist registry,
routing decision record, route receipt, authority lease, readiness check,
fallback, and residual owner. MoECOT currently supplies a concrete runtime
shape for that boundary: compact orchestrator, specialist lanes, control-plane
gates, ledgers, replay refs, handoff, residuals, and promotion blockers.

The chapter should remain standalone only if MoECOT gains a distinct
public-safe evidence lane: imported runtime packets, replay records, benchmark
artifacts, control-plane ledgers, current report bundles, or reproduced local
runs that cannot be carried cleanly as a section inside the routing chapter.
Until then, the runtime crosswalk can become a named section under routing
without deleting the idea.

## Preservation Ledger

| Preserved item | Destination treatment |
|---|---|
| Compact orchestrator and route head vocabulary | Keep as a named MoECOT Runtime Crosswalk section inside `routing-heads-and-specialist-cores`. |
| Specialist lanes / multi-core orchestration | Preserve as runtime-specific examples of bounded specialist cores and route leases. |
| Control-plane gates and fail-closed behavior | Preserve beside routing readiness, denied-route, failed-gate, and fallback discussion. |
| Run/task/control-plane ledgers | Preserve as evidence-packet fields that extend route receipts. |
| Replay refs, handoff refs, and residual escrow | Preserve in the route-receipt and runtime-packet interface discussion. |
| Source-reported versus locally reproduced fields | Preserve as a support-state boundary and no-promotion rule. |
| MoECOT restoration condition | Restore standalone only after public-safe runtime artifacts or reproduced runs create chapter-owning evidence. |

## Proposed Destination Outline

If executed, the routing chapter should keep one chapter skeleton. Do not paste
the full MoECOT chapter after the routing chapter. The fold should add or
revise these named pieces:

1. In `Why existing approaches are insufficient`, keep MoECOT as the
   source-reported runtime-crosswalk warning: a named implementation does not
   prove runtime behavior without artifacts.
2. In `Mechanism`, add **MoECOT Runtime Crosswalk** as a subsection that maps
   compact orchestrator, route head, specialist lanes, control-plane gates,
   ledgers, replay refs, handoffs, residuals, and promotion blockers onto the
   routing lease.
3. In `Interfaces`, preserve the `MoECOT Orchestration Record` fields as the
   runtime-packet extension of specialist registry and routing decision
   records.
4. In `Invariants`, keep the unavailable-source and replay-evidence promotion
   gates from `AsiStackProofs.MoECOTRuntime`.
5. In `Failure modes`, keep runtime branding, source-reported benchmark
   laundering, happy-path replay, missing ledgers, and authority escalation.
6. In `Minimum Viable Implementation`, keep
   `schemas/moecot_orchestration_record.schema.json` as a runtime-crosswalk
   fixture shape only.
7. In `Beyond the State of the Art`, keep MoECOT-style orchestration as an
   evidence-packet factory, not as a reproduced implementation claim.

## Source Union

If the fold executes, the destination chapter's source queue should union the
current routing and MoECOT runtime sources:

- `octopus_router`
- `rmi`
- `beastbrain`
- `cognitive_loop_closure`
- `rgs`
- `moecot`
- `project_theseus_whitepaper`
- `theseus_operator_os`
- `benchmaxxing`
- `viea`
- `scf`
- `talos`
- `moecot_md`
- `theseus_architecture_gate`

`moecot` and `moecot_md` must remain bounded as connector/variant context
unless public-safe artifacts, durable extracts, or reproduced runs are imported
and reviewed.

## External-Source Union

The destination should preserve the routing/MoECOT external comparators already
used by the source chapters:

- `ext_sparse_moe_2017`
- `ext_gshard_2020`
- `ext_switch_transformer_2021`
- `ext_expert_choice_routing_2022`
- `ext_mixtral_2024`
- `ext_moe_llm_survey_2024`
- `ext_frugalgpt_2023`
- `ext_hybrid_llm_2024`
- `ext_routellm_2024`
- `ext_three_states_plan_fear_2006`

These sources position routing, conditional computation, cost-quality routing,
and practical planning/routing baselines. They do not prove MoECOT runtime
behavior.

## Appendix C Row Plan

If executed, `routing-heads-and-specialist-cores.core` remains the destination
core claim. The current MoECOT runtime core claim should become a subclaim or
section-level claim inside the routing chapter:

> MoECOT is an implementation-reference runtime crosswalk for governed
> multi-core routing only when its source-reported fields remain separated from
> imported or reproduced runtime evidence.

Support remains `argument`. The fold does not create source-derived,
prototype-backed, synthetic-test-backed, empirical-test-backed, or
external-literature-backed support.

No support-state movement is authorized by this disposition.

## Lean Module And Proof-Manifest Treatment

Preserve both Lean modules and all proof tags:

- `AsiStackProofs.Routing`
- `lean:routing.specialists.operational_invariant`
- `lean:routing.specialists.failure_blocks_promotion`
- `AsiStackProofs.MoECOTRuntime`
- `lean:moecot.runtime.operational_invariant`
- `lean:moecot.runtime.failure_blocks_promotion`

If the fold executes, these tags should stay attached to the destination
chapter in `docs/book_outline.md` and the generated proof manifest. Do not
retire MoECOT proof tags merely because the chapter is folded; the unavailable
source and replay-evidence promotion gates become more important after folding.

## Schemas, Fixtures, And Harnesses

Preserve the runtime and routing record shapes:

- `schemas/specialist_registry_record.schema.json`
- `schemas/routing_decision_record.schema.json`
- `schemas/moecot_orchestration_record.schema.json`
- `experiments/moecot/README.md`
- `python3 scripts/validate_schemas.py`
- `python3 scripts/validate_protocol_examples.py`
- `python3 scripts/validate_readiness_residual_gates.py`

The MoECOT schema remains a public record-shape validator only. It is not a
runtime replay, benchmark, deployed route, or source-derived support-state
promotion.

## Reader Path And Handoff Repairs

If executed:

- The routing chapter's Human Reading Path should absorb MoECOT as a concrete
  runtime-crosswalk example after route leases and rejected alternatives.
- The folded MoECOT chapter should not remain in the reader spine as a second
  full chapter skeleton.
- The predecessor Handoff before the folded chapter and the Handoff in the
  destination routing chapter must be repaired with
  `python3 scripts/chapter_adjacency_report.py --if-removing moecot-runtime-and-multi-core-orchestration`
  and `python3 scripts/chapter_adjacency_report.py --chapter routing-heads-and-specialist-cores`.
- Reader overlays or curated-reader records that refer to the standalone
  MoECOT chapter must either point to the new section or record a release
  deferral.

## URL, Redirect, And History Policy

Before any manifest edit, choose one public-history policy:

- keep `chapters/moecot-runtime-and-multi-core-orchestration.qmd` as an
  archival source file excluded from the manifest with a clear historical note;
- add a public redirect or link note from the old chapter path to the routing
  section; or
- defer the fold until the site has a durable folded-chapter URL policy.

Do not silently remove a public chapter path.

## Restoration Conditions

MoECOT should be restored as a standalone chapter if one or more of these
public-safe artifacts becomes available and source-reviewed:

- run/task/control-plane ledgers from a real MoECOT run;
- replay refs with accepted and rejected paths;
- benchmark artifacts with baseline, negative control, residual, and
  reproduction boundary;
- readiness gate reports tied to runtime promotion blockers;
- public-safe code, command, or report bundle that the ASI Stack can verify by
  digest or replay;
- external review finding that the MoECOT runtime owns a distinct evidence lane
  not representable inside routing.

## Review Decision Surface

Reviewers should choose one:

- **Execute fold:** MoECOT becomes a named runtime-crosswalk section inside
  routing, while all source, proof, schema, reader, and restoration boundaries
  are preserved.
- **Revise fold disposition:** The fold may be right, but the destination
  treatment, source/proof preservation, or URL policy needs revision.
- **Defer for release:** The fold remains plausible, but current reader or
  publication work proceeds with the standalone chapter for a recorded reason.
- **Reject and retain standalone:** MoECOT currently owns a distinct chapter
  artifact, evidence lane, proof family, implementation horizon, or reader
  throughline.

## Validation If Executed

Before an executed fold is committed, run at minimum:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing moecot-runtime-and-multi-core-orchestration
python3 scripts/chapter_adjacency_report.py --chapter routing-heads-and-specialist-cores
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_chapter_consolidation_sequence.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_readiness_residual_gates.py
python3 scripts/validate_book.py
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
```

## Non-Claims

- This disposition does not merge or fold chapters.
- This disposition does not change `book_structure.json`.
- This disposition does not change Appendix C support states.
- This disposition does not create MoECOT runtime evidence.
- This disposition does not reproduce MoECOT benchmark, replay, readiness, or
  deployment behavior.
- This disposition does not approve reader, EPUB, DOCX, PDF, audio, DOI, or
  archive artifacts.
