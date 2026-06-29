# Chapter Consolidation Fold Disposition: Simulation Fidelity

Status: fold-disposition ready; human/external review not completed.

This is a review artifact for the governed consolidation sequence. It does not
edit `book_structure.json`, merge chapters, fold chapters, change Appendix C
support states, create source/proof/test evidence, approve reader artifacts, or
promote any claim above `argument`.

This disposition does not edit `book_structure.json`.

## Candidate

| Field | Value |
|---|---|
| Fold candidate | `simulation-fidelity-and-physical-constraints` |
| Candidate title | Simulation Fidelity and Physical Constraints |
| Proposed destination | `resource-economics-and-token-budgets` |
| Destination title | Resource Economics and Token Budgets |
| Secondary frame | `the-efficient-asi-hypothesis` may keep the high-level efficiency implication, but should not own the fold. |
| Proposed fold section | Simulation Fidelity and Claim Transport |
| Current state | `fold_disposition_ready` |
| Required decision | Execute fold, revise fold disposition, defer for release, or reject and retain standalone. |

## Rationale

The fold recommendation is not that simulation fidelity is unimportant. The
recommendation is that its current standalone chapter is mostly a
contract-relative resource and fidelity constraint over claims that the
resource-economics chapter already owns. `resource-economics-and-token-budgets`
owns budget ledgers, protected overhead, displaced costs, review capacity,
verification tax, and physical bottleneck accounting. Simulation fidelity adds
the transfer rule: a simulated or synthetic result travels only as far as its
declared scope, fidelity, resource bill, assumptions, omitted variables, and
transfer decision allow.

`the-efficient-asi-hypothesis` should still cite the idea as an efficiency
guardrail, but the destination with the cleanest artifact boundary is Resource
Economics. Folding into the high-level Efficient ASI frame would make
simulation fidelity feel like philosophy. Folding into Resource Economics keeps
it as a concrete resource contract and claim-transport mechanism.

The chapter should remain standalone only if simulation fidelity gains a
distinct evidence lane: a feasibility calculator, a physical-computation audit,
simulation benchmarks with negative controls, an independent external
literature review, or executable simulator evidence that cannot be carried
cleanly as a section inside resource economics.

## Preservation Ledger

| Preserved item | Destination treatment |
|---|---|
| Contract-relative simulation feasibility | Keep as the opening rule for the Simulation Fidelity and Claim Transport section. |
| `Simulation Contract Record` | Preserve as a companion/extension record beside the `Resource Budget Record`. |
| Scope, clockspeed, fidelity, temporal semantics, demand, and capacity | Preserve as required contract fields before a simulated result can support a claim. |
| Resource bill, bottlenecks, instrumentation effects, and omitted variables | Preserve as resource-economics fields that can block transfer or force residualization. |
| Transfer decision and supported-claim boundary | Preserve as the claim-transport gate: transfer only within declared support. |
| Approximation liberties and residual risks | Preserve as failure-mode and no-promotion language. |
| Normative/speculative simulation boundaries from `alignment_field` | Preserve only as scenario-boundary caution, not physics or engineering evidence. |
| Formal verification comparator from `ext_reluplex_2017` | Preserve as an external example of scoped property verification, not as a simulation result. |
| Simulation restoration condition | Restore standalone only after public-safe simulation/physical-computation evidence creates chapter-owning evidence. |

## Proposed Destination Outline

If executed, the resource-economics chapter should keep one chapter skeleton.
Do not paste the full simulation-fidelity chapter after the resource-economics
chapter. The fold should add or revise these named pieces:

1. In `Why existing approaches are insufficient`, add the warning that budget
   ledgers can still launder synthetic results if the fidelity and transfer
   boundary are missing.
2. In `Mechanism`, add **Simulation Fidelity and Claim Transport** as a
   subsection that binds scope, fidelity, temporal semantics, demand,
   bottlenecks, resource bill, omitted variables, approximation liberties,
   instrumentation effects, and transfer decision to resource-governed claims.
3. In `Interfaces`, keep the `Simulation Contract Record` as a companion
   record to `schemas/resource_budget_record.schema.json`, with a clear
   handoff to claim ledgers and benchmark records when a simulated result is
   used as evidence.
4. In `Invariants`, preserve the rule that a simulation claim used as evidence
   must declare scope, fidelity, and resource bounds, and that a promoted
   experiment result cannot exceed declared fidelity support.
5. In `Failure modes`, keep simulation laundering, same-physics overclaim,
   sandbox-to-world transfer, missing bottleneck, missing instrumentation cost,
   hidden approximation liberty, and speculative-metaphysics creep.
6. In `Minimum Viable Implementation`, keep
   `schemas/simulation_contract_record.schema.json` and
   `tests/fixtures/protocol_records/simulation_contract_record.valid.json` as
   record-shape fixtures only.
7. In `Beyond the State of the Art`, keep simulation as a claim-transport
   layer for synthetic worlds, unit simulators, benchmark environments, safety
   rehearsals, and scenario models, while preventing results from traveling
   beyond their declared contract.

## Source Union

If the fold executes, the destination chapter's source queue should union the
current resource-economics and simulation-fidelity sources:

- `tokenmana`
- `planforge`
- `coherence_exchange`
- `simulation_scaling`
- `viea`
- `project_theseus_whitepaper`
- `coilra_multicoil_rope`
- `cgs`
- `rankfold_neuralfold`
- `alignment_field`
- `ext_pagedattention_vllm_2023`
- `ext_reluplex_2017`

`simulation_scaling` remains the central Corben-authored source for
contract-relative simulation feasibility, but it is still theoretical synthesis
here. It does not supply a physical experiment, simulation benchmark,
feasibility calculator, or independent literature audit.

## External-Source Union

The destination should preserve the external comparators already used by the
source chapters:

- `ext_pagedattention_vllm_2023`
- `ext_reluplex_2017`

`ext_pagedattention_vllm_2023` positions memory, batching, and serving
throughput as resource-economics lanes. `ext_reluplex_2017` positions scoped
property verification as a boundary example for what a formal or synthetic
result can and cannot support. Neither source proves ASI simulation fidelity,
physical feasibility, deployed budget scheduling, or local model behavior.

## Appendix C Row Plan

If executed, `resource-economics-and-token-budgets.core` remains the
destination core claim. The current simulation-fidelity core claim should
become a section-level subclaim inside the resource-economics chapter:

> Simulation and fidelity results are resource-governed claim-transport records
> whose support cannot exceed declared scope, fidelity, resource bill,
> assumptions, omitted variables, instrumentation effects, residual risks, and
> transfer decision.

Support remains `argument`. The fold does not create source-derived,
prototype-backed, synthetic-test-backed, empirical-test-backed, mechanized, or
external-literature-backed support for the destination core claim.

No support-state movement is authorized by this disposition.

## Lean Module And Proof-Manifest Treatment

Preserve both Lean modules and all proof tags:

- `AsiStackProofs.ResourceEconomics`
- `lean:resources.budgets.operational_invariant`
- `lean:resources.budgets.failure_blocks_promotion`
- `AsiStackProofs.SimulationFidelity`
- `lean:simulation.fidelity.operational_invariant`
- `lean:simulation.fidelity.failure_blocks_promotion`

If the fold executes, these tags should stay attached to the destination
chapter in `docs/book_outline.md` and the generated proof manifest. Do not
retire simulation-fidelity proof tags merely because the chapter is folded; the
scope, fidelity, and support-bound gates become more important after folding.

## Schemas, Fixtures, And Harnesses

Preserve the resource and simulation record shapes:

- `schemas/resource_budget_record.schema.json`
- `schemas/simulation_contract_record.schema.json`
- `tests/fixtures/protocol_records/resource_budget_record.valid.json`
- `tests/fixtures/protocol_records/simulation_contract_record.valid.json`
- `python3 scripts/validate_schemas.py`
- `python3 scripts/validate_protocol_examples.py`
- `python3 scripts/validate_generation_mode_baselines.py`
- `python3 scripts/validate_resource_budget_ledgers.py`
- `python3 scripts/validate_capacity_smoothing.py`

The simulation contract fixture remains a public record-shape validator only.
It is not a simulator, a physical-computation audit, a feasibility calculator,
a benchmark-transfer result, or a support-state promotion.

## Reader Path And Handoff Repairs

If executed:

- The resource-economics chapter's Human Reading Path should absorb simulation
  fidelity as the practical rule that a simulation result cannot outrun its
  fidelity and resource contract.
- The folded simulation-fidelity chapter should not remain in the reader spine
  as a second full chapter skeleton.
- The predecessor Handoff before the folded chapter and the Handoff in the
  destination resource-economics chapter must be repaired with
  `python3 scripts/chapter_adjacency_report.py --if-removing simulation-fidelity-and-physical-constraints`
  and
  `python3 scripts/chapter_adjacency_report.py --chapter resource-economics-and-token-budgets`.
- Reader overlays, curated-reader records, companion-note routing, and review
  matrix rows that refer to the standalone simulation-fidelity chapter must
  either point to the new section or record a release deferral.

## URL, Redirect, And History Policy

Before any manifest edit, choose one public-history policy:

- keep `chapters/simulation-fidelity-and-physical-constraints.qmd` as an
  archival source file excluded from the manifest with a clear historical note;
- add a public redirect or link note from the old chapter path to the
  resource-economics section; or
- defer the fold until the site has a durable folded-chapter URL policy.

Do not silently remove a public chapter path.

## Restoration Conditions

Simulation fidelity should be restored as a standalone chapter if one or more
of these public-safe artifacts becomes available and source-reviewed:

- a simulation feasibility calculator with documented assumptions, bottlenecks,
  negative cases, and result boundaries;
- a physical-computation audit tied to actual simulation claims;
- simulation benchmark runs with baseline, negative control, residual, and
  transfer-boundary records;
- an executable simulator whose outputs are checked against a declared
  `Simulation Contract Record`;
- independent external literature review finding that simulation fidelity owns
  a distinct evidence lane not representable inside resource economics;
- external review finding that the simulation contract is central enough to the
  ASI Stack that burying it as a resource-economics section weakens the book.

## Review Decision Surface

Reviewers should choose one:

- **Execute fold:** Simulation Fidelity and Physical Constraints becomes a
  named Simulation Fidelity and Claim Transport section inside Resource
  Economics, while all source, proof, schema, reader, and restoration
  boundaries are preserved.
- **Revise fold disposition:** Keep the candidate unexecuted and revise the
  destination, subclaim, source, proof, reader, or restoration treatment.
- **Defer for release:** Keep both chapters unchanged for the current release
  and pause curated-reader graduation for the standalone chapter until the
  consolidation decision is made.
- **Reject and retain standalone:** Keep Simulation Fidelity and Physical
  Constraints as a standalone chapter because review finds distinct artifact,
  proof, evidence, or reader ownership.

## Non-Claims

- This disposition does not merge or fold chapters.
- This disposition does not change `book_structure.json`.
- This disposition does not change Appendix C support states.
- This disposition does not create source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support.
- This disposition does not approve reader, ebook, PDF, DOCX, audio, DOI,
  archive, or release artifacts.
- This disposition does not prove physical simulation feasibility, simulator
  adequacy, benchmark transfer, or resource optimality.
