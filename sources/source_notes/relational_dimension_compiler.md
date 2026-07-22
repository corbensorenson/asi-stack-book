# Source Note: The Relational Dimension Compiler

| Field | Value |
|---|---|
| Source ID | `relational_dimension_compiler` |
| Source title | The Relational Dimension Compiler: Adaptive Polyadic Cognition with Bounded Computational Arity and Unbounded Semantic Structure |
| Author / date | Corben Sorenson; July 2026; conceptual architecture and research program |
| Ingestion date | 2026-07-22 |
| Canonical local text | `sources/raw/corben_papers/relational_dimension_compiler/relational_dimension_compiler.md`; SHA-256 `85bcb1865da74ffe57d04c763557993799065ec975c2b0eca5e093c23e9eaa5a` |
| Supplied presentation copy | `sources/raw/corben_papers/relational_dimension_compiler/relational_dimension_compiler.docx`; SHA-256 `34a33f767fb596f0b9f3530afda47748ad60950a4531349f3f6d56d452b5b19a` |
| Pair verification | Markdown and DOCX have the same section hierarchy and substantive paper identity. Pandoc extraction produced 17,986 DOCX words versus 17,661 canonical Markdown words; the difference is presentation/export material rather than a competing paper version. |
| Storage boundary | Both supplied files are retained in the ignored local raw-source cache. This tracked note is public-safe; ingestion does not itself authorize publication of the raw paper. |
| Evidence boundary | The paper is a design architecture with formal sketches, conditional propositions, failure analysis, implementation contracts, and a proposed benchmark. It supplies argument and research direction, not an implemented RDC, measured advantage, verified natural relation, universal arity theorem, or support-state promotion. |

## Thesis

The paper rejects the idea that “higher-dimensional AI” should mean replacing
an attention matrix with one permanently denser tensor. Its stronger proposal
is a **Relational Dimension Compiler (RDC)** that constructs a typed,
branch-aware relational topology for the current consumer, selects the least
expensive qualified operator for that topology, persists accepted relations as
role-bearing objects, and reversibly contracts stable subcomplexes into
macro-objects.

Its central distinction is between:

- **semantic arity**: how many typed roles a relation contains;
- **primitive computational arity**: how many items one kernel scores jointly;
- **storage arity**: how the accepted relation is represented persistently.

Arbitrary finite semantic arity can be stored exactly as a relation-instance
node connected to its participants by typed binary role incidences. Selective
triadic or higher-order kernels may still improve discovery or inference, but
the system does not need an unbounded ladder of dense primitive tensors. The
architectural target is therefore a self-constructing computational topology,
not a fixed tensor order.

## Mechanisms

1. **Dimensional type system.** Geometry, tensor order, semantic arity,
   primitive arity, topological grade, time, scale, branch, epistemic state,
   and budget are independent axes. Each axis declares carrier, semantics,
   symmetry, metric/unit where relevant, variance law, and legal operations.
2. **Typed relational complex.** Persistent state contains versioned entities,
   continuous or discretized fields, typed relation objects, branch DAGs,
   contraction maps, provenance, uncertainty, defeaters, and lifecycle state.
3. **Role-preserving reification.** A finite n-ary fact becomes one relation
   object plus role-labelled binary incidences. Ordered, symmetric, optional,
   repeated, temporal, branch, provenance, and uncertainty semantics remain
   explicit, allowing relations to participate in metarelations.
4. **Operational relational order.** “True order” is treated as consumer,
   representation, resource, and tolerance relative. Interaction dividends,
   lower-order surrogate families, interventions, and matched rescues estimate
   whether a higher-order path adds useful information.
5. **Sparse candidate proposal.** Geometry, time, schema completion, pairwise
   salience, memory, residual hotspots, planning demand, exact joins, and field
   events narrow the candidate denominator before any polyadic kernel runs.
   Proposal recall remains a measured quantity.
6. **Adaptive relational-order routing.** Candidate/operator pairs compete
   under compute, memory, communication, latency, verifier, risk, and repair
   budgets. The router chooses topology, order, operator, precision, scale,
   branch resolution, verification effort, and stopping or abstention.
7. **Operator registry.** Pairwise attention, tree/poly-attention, triadic
   kernels, graphs, hypergraphs, simplicial/cellular operators, equivariant
   kernels, neural operators, tensor contractions, exact solvers, and database
   joins expose typed input/output contracts, symmetries, arity, cost, state,
   approximation, and failure modes.
8. **Independent-enough relation qualification.** Type/role validity, branch
   consistency, evidence, lower-order sufficiency, counterfactual necessity,
   invariance/equivariance, calibration, alternatives, downstream risk, and
   total cost are checked separately from proposal.
9. **Branch-indexed epistemic lifecycle.** Proposed, qualified, believed,
   observed/executed, weakened, contradicted, superseded, archived, and retired
   relations remain distinct. Hypothetical state cannot enter actuality without
   an explicit observation, adoption, execution, or reconciliation event.
10. **Object–field coupling.** Persistent entities and role-sensitive events
    coexist with continuous fields. Typed interfaces cover sampling, source
    terms, boundary constraints, event creation, and macro-object summaries.
11. **Semantic renormalization.** A stable subcomplex may become a macro-object
    only relative to a declared query family, environment class, discrepancy
    tolerance, boundary interface, uncertainty, provenance, and expansion or
    invalidation triggers.
12. **Slow-path compilation.** Repeatedly qualified relation programs can become
    cheaper recognizers, indexes, rules, kernels, planner operators, cached
    macro-objects, or specialists. Every compiled path retains scope,
    counterexamples, expiry, monitoring, rollback, and the slower recheck path.
13. **Relational IR lowering.** Semantic, evidence, computational, and
    abstraction layers form an intermediate representation that can lower into
    tensor kernels, graphs, databases, symbolic logic, event records, planning,
    geometric constraints, explanations, or verification queries.
14. **Hardware compilation.** Columnar entity/relation/incidence tables,
    schema batching, block sparsity, structured factorization, caches, branch
    sharing, and partitioning turn irregular semantic state into regular kernels
    while preserving identity and approximation receipts.
15. **Schema evolution.** Persistent residuals may propose new role schemas,
    but adoption requires comparison, testing, versioning, migration, plural
    representation, historical interpretation, and rollback.
16. **RODIE evaluation.** The proposed benchmark suite separates minimum order,
    role binding, latent topology, causal/counterfactual fidelity, dynamic
    identity, multiscale contraction, geometry/fields, branch separation, and
    compilation/reuse, with strong lower-order rescues and total-system cost.

## Formal and Conditional Results

- The finite role-reification construction is representational: given stable
  relation identity, schema, and typed role incidences, the original finite
  relation structure is recoverable up to identifier renaming.
- This does not prove that the representation is easy to learn, query, update,
  or execute efficiently.
- Unary, pairwise, and selective triadic kernels are a falsifiable default, not
  a theorem that order four or above is unnecessary.
- Least sufficient order depends on the admitted model families, information,
  resource envelope, consumer loss, distribution, and error tolerance.
- A contraction certificate is query- and environment-relative; certificate
  composition and transfer cannot be assumed.
- A qualified relation packet does not establish world truth or effect
  authority.

## Proposed Artifact Family

- `RelationalConstructionRequest`.
- `QualifiedRelationalComplexPacket`.
- Dimensional Axis Type and legality record.
- Entity, Field, Relation Schema, Relation Instance, and Typed Incidence records.
- Candidate Proposal Denominator and Proposal Recall receipt.
- Relational Order Decision and total-cost receipt.
- Lower-Order Rescue and Relational-Order Certificate.
- Relation Qualification and lifecycle event records.
- Branch Delta and cross-branch comparison record.
- Contraction Certificate, Macro-Object Boundary Contract, and Expansion event.
- Operator Registry entry and kernel-lowering receipt.
- Compiled Specialist Certificate and slow-path rollback route.
- Schema Evolution Proposal and migration disposition.
- RODIE corpus, preregistration, evaluator, and vector result bundle.

## Evidence and Falsification Program

The paper proposes a complete causal loop in a bounded generated environment:
raw observations; entity/field state; pairwise proposal; adaptive order routing;
qualification/reification; branch-local prediction; contraction/expansion;
separate action authority; outcome reconciliation; and compilation of one
repeated relation program. A serious comparison includes standard, deeper, and
wider Transformers; recurrent/state-space models; pairwise and higher-order
GNNs; fixed hypergraph/simplicial and fixed triadic systems; relation-token
models; symbolic/exact baselines; oracle structure/order bounds; and RDC
ablations.

The proposal loses or narrows when competent lower-order rescues match quality
and transfer at lower total cost, routing creates persistent regret on simple
tasks, role/topology gains disappear under shortcut controls, branch state does
not improve counterfactual behavior, contraction triggers fail, higher direct
arity repeatedly proves necessary, compiled routes cannot retain scope, learned
topology is unstable or non-diagnostic, object–field hybrids add no value, or
the end-to-end proposal/qualification/compiler burden consumes component gains.

## Failure Modes

- Relational hallucination and authoritative-looking false structure.
- Candidate/hyperedge overproduction and hidden rejected-candidate burden.
- False reduction of a real joint dependency to inadequate lower-order terms.
- Pairwise laundering of several correlations into one higher-order claim.
- Correct participants with incorrect role binding.
- Axis confusion across branch, batch, role, time, space, confidence, or
  authority.
- Branch leakage and false actualization of simulated state.
- False objecthood, over-contraction, abstraction debt, and missed expansion.
- Topology, schema, certificate, cache, or relation-lifecycle drift.
- Relation poisoning, provenance forgery, and evaluator capture.
- Hidden proposal oracle burden and weak lower-order baselines.
- Hardware illusion from counting contractions but not irregular data movement.
- Schema capture, representational lock-in, and premature ontology commitment.
- Privacy inference amplification through explicit derived relations.
- Explanation overclaiming from an inspectable but non-causal graph.
- Self-modification risk from schema, operator, contraction, or specialist
  changes certified by their own dependent evaluator.

## Book Chapters Supported

| Chapter | Contribution | Source locus | Boundary |
|---|---|---|---|
| `cognitive-compilation-and-semantic-ir` | Adds a relational IR whose semantic, evidence, computational, and abstraction layers preserve dimensional types, role identity, branch, approximation, and lifecycle through lowering. | §§2, 4–5, 7, 10–11, 17 | The existing chapter owns accepted-obligation translation; it should not silently absorb the full RDC world-structure lifecycle. |
| `governed-world-models-and-reality-grounding` | Adds versioned entity/relation/field state, branch-local hypotheses, object–field coupling, relation qualification, discrepancy attribution, and reversible macro-objects. | §§4–5, 8–9, 12, 15 | Explicit relational structure does not establish correct perception, grounding, causality, or world truth. |
| `routing-heads-and-specialist-cores` | Extends routing across relational order, candidate topology, operator family, precision, verification, and abstention under total cost and lower-order fallback. | §§5–7, 10–11 | No trained order router, proposal-recall result, regret bound, or useful routing advantage is supplied. |
| `replaceable-cognitive-substrates-beyond-transformer-monoculture` | Separates semantic, computational, and storage arity; frames graph, hypergraph, topological, field, symbolic, and tensor operators as replaceable lowerings behind a stable relational contract. | §§2–7, 10–11, 18 | Reification proves representational sufficiency only; bounded primitive arity and substrate advantage remain empirical. |
| `procedural-memory-and-cognitive-loop-closure` | Turns repeatedly qualified relation programs into monitored specialists while preserving the slow path, counterexamples, expiry, requalification, and rollback. | §§8, 10, 12, 17 | No compilation gain, specialist equivalence, or shift detector is demonstrated. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | Supplies RODIE, matched lower-order rescue, candidate-denominator, role-permutation, intervention, transfer, calibration, no-regret, contraction, compilation, and total-cost requirements. | §§6, 13–14, Appendix C | RODIE is a proposed suite, not a corpus, evaluator, benchmark run, or empirical result. |
| `resource-economics-and-token-budgets` | Expands cost accounting to candidate proposal, rejected tuples, sparse gathers, kernel work, state, communication, qualification, verification, contraction, expansion, repair, and compiler burden. | §§5–6, 10–11, 13 | The paper supplies cost categories and asymptotic envelopes, not measurements. |
| `integrated-reference-architecture` | Adds the relational complex as a joined semantic/evidence/computational/abstraction state that can connect world models, routing, compilation, memory, effects, and reconciliation. | §§5, 9–12, 17–18 | The integrated RDC lifecycle has not been implemented or joined to Theseus. |
| `open-research-agenda-and-bibliography-plan` | Adds a coherent research program for polyadic cognition, relation lifecycle, topology learning, semantic contraction, hardware lowering, and RODIE. | §§3, 11–18, references | The paper bibliography is author-supplied and needs source-by-source external verification before external-literature promotion. |

## Chapter Boundary Decision

The paper introduces a genuinely distinct prospective owner:
`relational-dimension-compilation-and-polyadic-cognition`. That owner would be
responsible for dimensional typing, semantic/computational/storage arity,
relation reification, relation qualification/lifecycle, adaptive order,
reversible contraction, and RODIE. Existing chapters own adjacent concerns but
not this conjunction:

- Cognitive Compilation owns accepted-obligation-to-artifact translation.
- Governed World Models owns predictive state and reality reconciliation.
- Routing owns request/capability/operator dispatch.
- Replaceable Substrates owns ABI-neutral component replacement.
- Procedural Memory owns consolidation of repeated successful behavior.

The candidate therefore merits later chapter adjudication, but the active
roadmap freezes all new manifest admission. Immediate work is bounded
integration into existing owners plus a deferred candidate packet. No chapter
path, manifest entry, proof target, or admission receipt is created during the
freeze.

## Claims To Add Or Update

- Distinguish semantic, computational, and storage arity wherever the book
  discusses higher-order attention or relational substrates.
- Require typed role incidence and persistent relation identity when an n-ary
  relation must survive beyond one transient kernel.
- Treat relational order as one routed resource, alongside model, depth,
  precision, context, verification, and abstention.
- Require proposal recall and the complete candidate/rejection denominator in
  sparse relational evaluations.
- Keep proposed, qualified, believed, observed/executed, contradicted, and
  retired relations distinct from effect authority.
- Treat abstraction as query-relative contraction with a boundary contract and
  mandatory expansion triggers rather than irreversible pooling.
- Preserve the slow qualified route whenever a repeated relational program is
  compiled into a cheaper recognizer or specialist.
- Measure useful relational structure per unit total lifecycle cost rather than
  celebrating nominal tensor order or asymptotic kernel cost.

These are design-rationale updates at `argument`. The source does not by itself
promote any chapter core or non-core mechanism claim.

## Open Questions

- Which natural tasks have independently defensible irreducible order after
  strong latent-mediator and deeper-pairwise rescues?
- Can proposal recall be measured without giving the proposer privileged latent
  structure unavailable to baselines?
- Which relation schemas remain stable across model, domain, language, and
  measurement changes?
- How should uncertainty over entity count, role binding, topology, and schema
  identity be represented without premature collapse?
- When do typed relation objects improve downstream behavior rather than merely
  producing a more inspectable intermediate state?
- What lowerings preserve role, branch, provenance, uncertainty, and
  counterfactual semantics across neural, symbolic, database, and simulator
  implementations?
- Can query-relative contraction certificates compose safely, or must every
  consumer requalify the abstraction?
- How should privacy, rights, and deletion propagate through inferred relations
  and macro-object contractions?
- When does a compiled relational specialist save enough cost to repay
  monitoring, requalification, and rollback?
- Does bounded primitive arity remain competitive on competent order-four and
  higher controls?
- What hardware/runtime representation gives sparse relational state a real
  end-to-end advantage over optimized dense kernels?
- Can RODIE avoid becoming a synthetic ontology benchmark that rewards the RDC
  assumptions used to generate it?

## Non-Claims

- No RDC implementation, training run, benchmark corpus, evaluator, or result
  exists in this source packet.
- The reification proposition does not establish efficient learning, inference,
  updating, or hardware execution.
- Pairwise Transformers are not claimed incapable of higher-order behavior.
- Unary/pairwise/selective-triadic primitives are not proven universally
  sufficient.
- Explicit relations are not assumed to be unique, true, causal, grounded,
  interpretable, safe, private, or authorized.
- No source-reported external result has been independently verified or
  reproduced through this ingestion.
- No chapter-core claim, release state, publication state, AGI claim, or ASI
  claim changes.
