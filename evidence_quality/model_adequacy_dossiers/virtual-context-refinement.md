# Model-adequacy dossier: Virtual Context ABI reachable refinement

## Ownership

- Chapter: `virtual-context-abi`
- Frozen targets: `lean:vcm.abi.operational_invariant`, `lean:vcm.abi.failure_blocks_promotion`, `lean:vcm.abi.context_admission_route_envelope`
- Stronger model: `lean/AsiStackProofs/VirtualContextRefinement.lean`
- Independent consumer: `scripts/validate_virtual_context_refinement.py`
- Result: `experiments/virtual_context_refinement/results/2026-07-15-local.json`
- Schema: `schemas/virtual_context_refinement.schema.json`
- Support-state effect: exactly `none`

## Reachable model

The state machine moves through raw, request-bound, resolved, certified, materialized, typed-fault, and denied stages. The narrowed state uses one request identity; exact address, version, snapshot, and mount identities; source and derived hashes; an authority ceiling and approved authority; lease expiry; four receipt flags; materialization emission; mandatory status; and logical time.

Binding requires nonzero request and location identities, authority within the ceiling, and a live lease. A resolver hit requires the exact bound request tuple, a permitted mount, live lease, nonzero source hash, resolver receipt, and no premature fault or materialization. Certification preserves the request and source, binds a derived hash, forbids authority widening, requires a certificate receipt and declared omission, and rejects exact-completeness overclaim and taint. Materialization preserves request, source, and derived identities, requires resolver and certificate receipt custody plus its own receipt, and excludes taint and a simultaneous typed fault. A mandatory miss instead reaches typed-fault state only with a fault receipt and no materialization receipt or emission.

## Consequences, countermodels, and consumer

The kernel checks accepted-transition validity, exact represented binding and authority preservation at materialization, mandatory-miss fault/materialization exclusion, a four-event successful materialization trace, a two-event fault trace, and twelve countermodels. The independent consumer implements the transition relation separately and rejects 55 single-fault mutations.

The prior resolver/certificate packet is consumed at its exact boundary: two intended valid routes and nine expected-invalid controls, with no model call, network access, private-source read, or support effect. The eight admission/adequacy fixtures remain a different layer and a different judgment: the suite passes three valid and five expected-invalid records, but admission validity is never treated as resolver correctness.

## Assumptions, exclusions, and adequacy verdict

Numeric identifiers, authority values, mount permission, lease time, source and derived hashes, omission declarations, taint flags, receipts, and scenario labels are trusted. The model is finite, sequential, and deterministic. It does not dereference an address, authenticate authority, calculate a hash, inspect payloads, validate a certificate claim, measure summary loss, observe storage, model concurrent snapshot change, propagate deletion, or call a model.

The model is adequate for the narrowed claim that this exact finite transition system preserves represented bindings and authority on accepted materialization and routes a represented mandatory miss to a typed fault without materialization. It is inadequate for natural-language address truth, real payload identity, summary fidelity, certificate truthfulness, deployed resolver or store correctness, transaction isolation, deletion enforcement, context quality, natural workloads, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Physically retire the two projection-only declarations while preserving frozen lineage. Retain the eleven original route theorems as bounded admission, residual, and promotion branches. Make the reachable refinement the current owner of the operational and failure targets and a stronger consumer of the admission route envelope. Promotion requires a real resolver/store boundary, authenticated request and authority inputs, concurrent snapshot and lease tests, certificate and payload validation, deletion/taint propagation, natural held-out workloads, matched strong baselines, complete costs and failures, reproduction, and transfer.
