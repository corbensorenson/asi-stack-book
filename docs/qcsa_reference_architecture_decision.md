# QCSA Reference Architecture Decision

Decision ID: `ADR-QCSA-001`

Date: 2026-07-13

State: frozen for implementation; outcomes unopened

Roadmap: `docs/post_v2_2_implementation_completion_roadmap.md`

## Decision

Implement the bounded Question-Compiled Semantic Addressing reference as a
standard-library Python package under `experiments/qcsa_reference/qcsa_ref`.
Use canonical JSON files as the durable interchange format and deterministic
in-memory adapters for retrieval, model, sensor, specialist, authority, tool,
and verification behavior. The implementation may later add optional adapters,
but the frozen tests and replay path cannot require network access, paid
services, nondeterministic models, or irreversible effects.

The package has twelve separately owned lanes, `QI-01` through `QI-12`. A
shared artifact envelope binds lane identity, opaque artifact identity,
version, owner, input digests, payload, non-claim boundary, and a digest over
the canonical artifact body. Lane modules add exact payload checks and
behavioral invariants. The content-addressed manifest is produced last and
rejects missing or mutated descendants.

## Architectural boundaries

The reference preserves four separate state machines:

1. **Identity:** SOIDs and their alias, merge, and split lineage.
2. **Evidence:** propositions, evidence, provenance, belief, contradiction,
   authority metadata, lifecycle, and permitted use.
3. **Address and route:** atlas paths, candidate resolution, questions, and
   physical execution plans.
4. **Effect authority:** an independent decision over actor, target, scope,
   policy, approval, reversibility, expiry, and requested effect.

No function may infer authority from identity, address confidence, graph
position, certificate integrity, retrieval similarity, or route selection.
No address migration may silently retarget an old address to another SOID.
No graph edge or certificate may be treated as truth or support-state evidence
without a separate evidence decision.

## Package layout

```text
experiments/qcsa_reference/
  qcsa_ref/
    canonical.py
    identity.py
    evidence_graph.py
    atlas.py
    certificate.py
    questions.py
    routes.py
    migration.py
    adversarial.py
    grounding.py
    round_trip.py
    ledger.py
    manifest.py
  corpus/
  fixtures/
  results/
  package_manifest.json
  budgets.json
  test_plan.json
```

Implementation files and outcome-bearing directories are intentionally absent
at this freeze. Their later creation must match the manifest and test plan.

## Canonicalization and digest rule

Canonical JSON is UTF-8, sorted by key, encoded with compact separators, and
terminated by one newline when stored. An artifact `content_digest` is the
lowercase SHA-256 of the canonical object after removing only the
`content_digest` field. Input digests bind exact parents. IDs use the opaque
form `qa:<16 lowercase hexadecimal characters>` in fixtures; neither IDs nor
split assignment may encode labels or expected answers.

## Failure policy

The package fails closed for malformed schema, noncanonical serialization,
digest mismatch, duplicate identity, silent alias retarget, dangling graph
reference, stale or candidate epoch used as authoritative, missing residual,
certificate tampering, authority widening, missing effect receipt, unresolved
migration, incomplete descendant inventory, or artifact-manifest mutation.
Unknown, conflicting, abstain, clarification, fallback, typed migration
failure, and explicit refusal are successful protocol outcomes when specified
by the case.

## Evaluation separation

The implementation developer may inspect train and development cases. The
held-out labels and aggregate results remain unopened until the package,
baselines, ablations, evaluator interface, budgets, seeds, and decision rules
pass the freeze validator at a committed revision. The round-trip evaluator is
implemented independently from the candidate generator and preserves
disagreement rather than forcing consensus.

## Rejected alternatives

- A single universal tree: rejected because it collapses plural views.
- Semantic IDs as durable identity: rejected because atlas revision would
  retarget references.
- A database or service first: rejected because it adds deployment state before
  the protocol is falsifiable.
- A model-dependent implementation: rejected because deterministic replay and
  negative controls would depend on external availability.
- One blended score: rejected because quality, unsafe release, latency,
  governance cost, fallback, and human burden have different meanings.
- A new book chapter at freeze: rejected because the existing nine owners
  already own the interfaces and no measured chapter-owning result exists.

## Evidence boundary

This decision and its schemas establish implementation intent and frozen record
contracts only. They do not establish semantic correctness, useful routing,
performance advantage, safety, privacy, migration completeness, production
transfer, external independence, AGI, ASI, or chapter-core support movement.
