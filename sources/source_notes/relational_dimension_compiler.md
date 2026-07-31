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

## Claim Boundary and Status

- RDC is a proposed relational representation/compiler architecture and
  falsification program, not evidence that explicit polyadic structure improves
  a model.
- “Higher dimensional” is not used as a synonym for higher tensor rank,
  geometric dimension, more hidden width, more branches, more abstraction
  levels, or greater intelligence.
- Finite role-preserving reification establishes representational recoverability
  under stated identity/schema assumptions. It does not establish learnability,
  efficient queries, causal correctness, natural usefulness, or hardware gain.
- Bounded primitive arity is a default research hypothesis with an explicit
  order-four-and-above escape route, not a universal theorem.
- Qualified relations are scoped epistemic artifacts. They do not become world
  truth, effect authority, causal explanations, or unique ontologies.
- Reversible contraction restores declared representation paths only; it does
  not undo external effects or guarantee removal of learned influence.
- All manuscript integrations remain `Design rationale` / `argument`; no
  support transition follows from the paper.

## Conceptual Primitives

- **Dimensional axis type:** carrier, semantics, role or coordinate meaning,
  symmetry, unit/metric, variance law, legal operations, and compatibility.
- **Relation schema:** stable role-bearing type with optional/repeated roles,
  symmetry, branch/time policy, constraints, and version.
- **Relation instance:** persistent identity plus schema, typed incidences,
  provenance, uncertainty, defeaters, branch, lifecycle, and dependencies.
- **Typed incidence:** participant-to-relation binding whose role, order,
  multiplicity, time, confidence, and provenance survive storage and lowering.
- **Candidate denominator:** every proposed, rejected, retried, filtered,
  shadowed, admitted, demoted, and failed relation/operator pair plus cost.
- **Relational-order certificate:** evidence that a selected topology,
  primitive order, operator, factorization, precision, and verifier are
  qualified for one consumer and envelope after lower-order rescue.
- **Branch-indexed state:** actual, believed, predicted, planned, simulated,
  counterfactual, fictional, and normative structures with explicit bridges.
- **Macro-object:** a query-relative contraction of a stable subcomplex plus a
  boundary interface, tolerance, uncertainty, provenance, and expansion rule.
- **Compiled relational specialist:** a cheaper recognizer or operator bound to
  its qualified slow program, scope, counterexamples, drift checks, expiry,
  fallback, and rollback.

## Interfaces, Artifacts, and State Machines

A `RelationalConstructionRequest` names the consumer, task/query family,
entities and fields, observations, branch, candidate sources, allowed schemas,
cost/risk envelope, evidence floor, primitive-order ceiling, verifier policy,
and fallback. The compiler returns a `QualifiedRelationalComplexPacket` or a
typed residual. The packet binds relation and incidence tables, field state,
branch DAG, operator schedule, candidate denominator, order decisions,
qualification, contraction maps, provenance, uncertainty, lifecycle events,
and descendant refs.

Relation instances move through proposed, qualified, believed, observed or
executed, weakened, contradicted, superseded, archived, and retired states.
Macro-objects and compiled specialists have parallel proposal, shadow,
qualification, canary, active, demotion, expiry, contraction/decompilation, and
retirement transitions. Observation, action, adoption, reconciliation, and
governance events—not model confidence—authorize crossings between epistemic
or lifecycle states.

## Assumptions and Invariants

- Semantic arity, primitive computational arity, and storage arity remain
  separate through every record and receipt.
- Typed role identity survives permutation, persistence, branching, lowering,
  caching, contraction, expansion, explanation, migration, and rollback.
- Candidate sparsity does not hide proposal recall or rejected-candidate cost.
- A higher-order path competes with competent reification, message passing,
  factorization, sequence, retrieval, tool, solver, and ordinary-model rescues
  under matched information and budgets.
- Qualification is independent enough from proposal and cannot be created by a
  higher proposer score.
- Confidence, evidence, belief, observation, execution, and authority remain
  distinct axes.
- Hypothetical or branch-local state cannot actualize without an authorized
  bridge event.
- Object–field exchange declares sampling, source, boundary, event-creation,
  scale, unit, uncertainty, and conservation behavior.
- Contraction is sound only for a declared query/environment envelope and must
  retain expansion and invalidation triggers.
- Every compiled fast path retains the exact slower qualified route and
  dependency-closed decompilation.
- Schema evolution preserves historical interpretation, plural alternatives,
  migration dispositions, and rollback rather than overwriting one ontology.
- Hardware credit includes irregular data movement, state, communication,
  qualification, verification, cache invalidation, repair, and fallback.

## Algorithms and Conditional Results

The paper specifies sparse candidate narrowing, adaptive order routing,
relation qualification, typed reification, branch-local update, contraction,
expansion, reconciliation, schema evolution, and slow-path compilation as
proposed algorithms. A composite learning objective covers structure,
dynamics, order, qualification, contraction, calibration, sparsity, cost, and
security. These are not implemented procedures.

The exact finite-reification result is conditional on stable relation identity,
schema, and typed incidences, with recovery only up to identifier renaming. The
least-sufficient-order and contraction results remain consumer-, model-family-,
information-, resource-, environment-, query-, and tolerance-relative.
Certificates do not automatically compose or transfer.

## Threats, Costs, and Governance

The complete threat surface includes hallucinated relations, combinatorial
overproduction, false reduction, pairwise laundering, role failure, axis
confusion, branch leakage, false objecthood, contraction debt, topology/schema/
cache drift, poisoning, provenance forgery, evaluator capture, hidden proposal
oracles, hardware illusion, schema capture, privacy amplification, explanation
overclaiming, and self-certifying modification. Governance owns schema and
operator registries, proposal budgets, qualification independence, branch
bridges, actuality, lifecycle movement, contraction, migration, privacy,
appeal, expiry, rollback, and emergency retirement.

Total cost includes observation and entity construction; proposal and rejected
tuples; schema/role inference; relation and incidence storage; sparse gathers,
kernel work, and scatters; data movement; communication; factorization;
precision; branch copies; fields; qualification and verification; caching and
invalidation; contraction and expansion; learning; compilation; monitoring;
repair; human review; migration; privacy; and rollback.

## Cross-Paper Synthesis

- QCSA supplies stable semantic identity, plural addresses, question-guided
  evidence acquisition, and typed hypergraph memory; RDC supplies adaptive
  role-bearing relation construction and computational lowering.
- Platonic World Model supplies semantic basis, branch, proposition,
  attestation, commitment, proof, grounding, and governed ontology change;
  RDC's relation graph cannot replace those epistemic distinctions.
- Cognitive Compilation owns obligation-preserving translation; RDC supplies a
  relational IR with semantic, evidence, computational, and abstraction
  layers.
- Governed World Models own observation, dynamics, counterfactuals, and reality
  reconciliation; RDC supplies candidate object/field topology and branch-local
  relation state.
- Routing and Replaceable Substrates own qualified operator selection and ABI-
  neutral implementation; RDC makes relational order, factorization, precision,
  and topology routed resources.
- Procedural Memory owns compiled-specialist lifecycle and slow-path recovery;
  Resource Economics and Benchmark Ratchets own complete cost and RODIE.

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

The candidate passed chapter adjudication in the 2026-07-25 full-coverage
audit and is now admitted as
`relational-dimension-compilation-and-polyadic-cognition`. The chapter owns the
joined compiler lifecycle while adjacent chapters retain their narrower jobs.
Admission is structural only: it creates no implementation, benchmark result,
proof of irreducibility, efficiency result, or support-state promotion.

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

## Section-Family Coverage

| Paper section family | Actual manuscript or durable owner | Disposition and boundary |
|---|---|---|
| §§1–2 | `relational-dimension-compilation-and-polyadic-cognition`; Replaceable Substrates | Thesis, contribution, axis type system, and semantic/primitive/storage separation integrated. “Higher dimension” remains typed rather than valorized. |
| §3 related work | source note; Appendix H backlog | Comparator families and missing-conjunction claim retained pending independent current-primary-source review. |
| §4 formal model | RDC chapter; Governed World Models; Cognitive Compilation | Typed relational state, exact role reification, operational order, branch state, and object–field complementarity integrated. Recoverability is representational only. |
| §5 compiler architecture | RDC chapter; Integrated Reference Architecture | Request/packet contracts, typechecker, proposer, order router, operator registry, qualifier, store, contraction compiler, and reconciler integrated or retained as proposed components. |
| §6 sparse adaptive order | RDC chapter; Routing; Benchmark Ratchets | Candidate narrowing, factorized kernels, order routing, least sufficient order, order certificates, counterfactual deletion, lower-order rescue, controls, and update loop integrated. |
| §7 bounded computational/unbounded semantic arity | RDC chapter; Replaceable Substrates; Cognitive Compilation | Relation-instance objects, exact reification boundary, metarelations, bounded default, selective triadic and higher-order escape routes, and relational calculus integrated. |
| §8 semantic renormalization | RDC chapter; Governed World Models; Procedural Memory | Stable subcomplexes, query-relative soundness, contraction/expansion, recursive scale, compilation, and learned-topology hypothesis integrated. No universal objecthood or certificate composition. |
| §9 branches and action boundary | Governed World Models; RDC chapter; Runtime/Claim owners | Branch identity, epistemic lifecycle, confidence/authority separation, provenance, and non-retroactive reconciliation integrated. |
| §10 self-constructing topology | RDC chapter; Integrated Architecture; VCM; Procedural Memory | Relational IR, learned contraction graph, persistent complex, possible worlds, schema evolution, reflex formation, and substrate neutrality integrated as a speculative endpoint. |
| §11 implementation and hardware | RDC chapter; Replaceable Substrates; Resource Economics | Entity/relation/incidence tables, schedules, schema batching, sparsity/locality, factorization, caches, distribution, complexity envelopes, and service decomposition integrated. No hardware result. |
| §12 learning/training | source note; Governed Model Training; Benchmark Ratchets | Structured data, observation-to-topology, dynamics, router/qualifier/contraction learning, joint objective, and curriculum retained as a concrete research program. |
| §13 RODIE | RDC chapter; Benchmark Ratchets | Nine diagnostic suites, natural-domain transfer, vector metrics, baselines, proposal denominators, and lower-order rescues integrated. RODIE remains a proposal, not a benchmark result. |
| §14 hypotheses and negatives | source note; RDC/benchmark falsifiers | Ten hypotheses and decisive negative dispositions retained, including order, regret, transfer, causal, multiscale, bounded-order, compilation, topology, object–field, and total-system tests. |
| §15 threats/hazards | RDC chapter; Security/Privacy/Evidence owners; source note | All eighteen failure families integrated or retained with cost and governance routes. Explicit structure creates no truth, causality, privacy, or explanatory privilege. |
| §16 limitations/non-claims | source note; chapter non-claims | Paper's limitations preserved without softening; no universal arity, relation truth, natural-task, hardware, safety, self-improvement, or ASI result. |
| §17 reference implementation | RDC Minimum Viable Implementation; `prototype-roadmap`; source note | Required components, comparisons, acceptance conditions, and public interface routed to implementation work. No implementation exists. |
| §18 discussion | RDC summary; Replaceable Substrates; Governed World Models; source note | Transformer delta, neural/symbolic bridge, representation–compute co-design, scaling-axis hypothesis, science/language/planning implications, and “not universal graph/tensor” boundaries retained. |
| §19 conclusion | RDC chapter summary; this note | Self-constructing typed-topology thesis integrated at `argument`. |
| Appendix A | source note; executable-specification backlog | Formal schema, incidence, branch copy-on-write, contraction certificate, and order-regret definitions retained as proposed formal objects. |
| Appendix B | source note; RDC lifecycle; Procedural Memory | Relation, macro-object, and compiled-specialist state sketches integrated or retained as lifecycle requirements. |
| Appendix C and references | Benchmark Ratchets; Appendix H backlog | Evaluation checklist retained; external bibliography requires independent passage review before support or novelty use. |

## Closure Status

**Section-family audit complete as of 2026-07-31.** All 19 numbered sections,
three appendices, and references terminate in manuscript integration,
public-safe note retention, a concrete implementation/evaluation obligation, or
an explicit non-claim. The dedicated RDC chapter already preserved the core
arity, reification, rescue, routing, contraction, lifecycle, and RODIE model.
This pass repaired the remaining compression: all nine RODIE diagnostic suites
plus natural transfer, the operator-registry and hardware-lowering contract,
learning-release separation, and the full epistemic/security hazard surface.
No substantive section is orphaned.

Closure does not establish an RDC implementation, learned topology, natural
relation, proposal recall, order-router calibration, irreducible polyadic
advantage, bounded-arity theorem, contraction fidelity, compiled-specialist
gain, hardware efficiency, RODIE corpus/result, privacy or safety result,
external reproduction, production transfer, or ASI claim. Support remains
`argument`; reopen on material paper or receiving-chapter drift.
