# v1.0 Evidence Transition Pilot

Last updated: 2026-06-28

This pilot tests the evidence-transition process on a small set of narrow book-method and architecture-control claims. It does not promote any claim above `argument`.

## Records

The machine-readable records live under `evidence_transitions/v1_0_pilot/` and validate against `schemas/evidence_transition_record.schema.json`.

| Claim ID | Decision | Reason |
|---|---|---|
| `evidence-states-and-claim-discipline.core` | no change; remains `argument` | The repository has claim labels, support states, source mappings, passage-reviewed mapping counts, and validators, but that process evidence does not prove semantic source-interpretation adequacy. |
| `system-boundaries-and-authority.core` | no change; remains `argument` | Exact source mappings, the synthetic authority-transition harness, and the stronger finite Authority Lean decision envelope support the design discipline, but they do not prove deployed permission enforcement, runtime adapter safety, revocation propagation, or live confused-deputy resistance. |
| `planning-as-a-control-layer.core` | no change; remains `argument` | Exact source mappings, the synthetic plan-execution harness, and the stronger finite Planning Lean control envelope support dispatch-gate discipline, but they do not establish planner quality, decomposition accuracy, context-demand prediction, scheduler behavior, deployed execution, or runtime replanning behavior. |
| `virtual-context-abi.core` | no change; remains `argument` | Exact source mappings, context ABI/packet schemas, the synthetic context admission/adequacy harness, and external context literature support admission/adequacy discipline, but they do not establish VCM resolver behavior, context compiler behavior, memory-store correctness, summary fidelity, contradiction-rate performance, distractor resistance, or model-facing context adequacy. |
| `living-book-methodology.core` | no change; remains `argument` | The repository demonstrates manifest-driven Quarto, source queues, proof manifests, validation gates, changelogs, release records, and reader generation, but full evidence-release review, proof adequacy review, and behavior tests remain open. |
| `executable-specifications-and-lean-proof-envelope.core` | no change; remains `argument` | The Lean build and proof audit pass for finite-record predicates, but proof adequacy has not been reviewed and the predicates do not imply broad runtime guarantees. |
| `open-research-agenda-and-bibliography-plan.core` | no change; remains `argument` | Source inventory, source appendices, and backlog schema mechanics exist, but external literature normalization, citation verification, and backlog closure remain incomplete. |

## Validation

Run:

```bash
python3 scripts/validate_evidence_transitions.py
```

The validator checks every JSON record in `evidence_transitions/` against the evidence-transition schema, rejects duplicate transition IDs, and keeps no-change pilot records at `argument`.

## Interpretation

The useful outcome is conservative. The pilot proves that the book can record an evidence review without pretending the review strengthens a claim. That matters because v1.0 should not promote claims merely because the repository is more organized, the prose is clearer, a local validator passed, a synthetic harness passed, or a finite-record proof was strengthened.

The next evidence pass should either narrow a claim enough that repository artifacts can support a bounded transition, or keep recording no-change decisions until an external review, stronger proof adequacy review, source interpretation review, or behavior test justifies movement.

## Non-Claims

- No chapter support state moved above `argument`.
- No AI capability, safety property, benchmark result, runtime behavior, source interpretation, or proof adequacy claim is promoted.
- Local validation remains process evidence unless a separate accepted transition says otherwise.
