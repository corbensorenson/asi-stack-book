# Source Note: The Precision Contract

| Field | Value |
|---|---|
| Source ID | `precision_contract` |
| Source title | The Precision Contract: A Functional Rate–Distortion Theory for Behavior-Preserving Neural Computation |
| Author / date | Corben Sorenson; July 2026; theoretical and systems research program |
| Ingestion date | 2026-07-24 |
| Canonical local text | `sources/raw/corben_papers/precision_contract/precision_contract.md`; SHA-256 `c8c5eeedf72f5fad4132d9916971f1c1853c74f01fc4a6bab9ad8c0700b39ac7` |
| Supplied presentation copy | `sources/raw/corben_papers/precision_contract/precision_contract.docx`; SHA-256 `9a6d8a1f4b033866225ef48d223e26883fcee934e16614a02cf93ee0dbf18924` |
| Pair verification | The DOCX contains the same title, section sequence, tables, reference family, and conclusion as the Markdown paper. Direct text hashes differ because the files encode equations, tables, and presentation structure differently; neither is treated as a byte-identical export of the other. |
| Storage boundary | Both supplied files are retained in the ignored local raw-source cache. This tracked note is public-safe; ingestion does not itself authorize publication of the raw paper. |
| Evidence boundary | The paper supplies representation arguments, definitions, conditional propositions, an architecture, and a falsifiable experimental program. It does not supply a frontier-model implementation, a measured compression result, a universal optimality theorem, an independently verified certificate, or support-state promotion. |

## Thesis

The paper rejects a representation-independent answer to “how many bits does a
neural network really need?” Exact reparameterizations, coordinate symmetries,
codebooks, limb decompositions, external algorithms, and decoder choices can
change the apparent magnitude or precision of stored numbers without changing
the realized function. A fixed per-weight bit-width is therefore not a stable
property of capability.

The proposed replacement is a **functional precision contract**: find the
shortest complete executable description whose behavior satisfies a declared
deployment contract within stated tolerances. The unit of analysis is not one
weight in one coordinate system, but an equivalence class of implementations
that preserve protected behavior. Precision becomes a routed, consumer-relative
field over the computation, and compression becomes an auditable program
transformation with explicit fallback and certification.

## Claim Boundary and Status

The source contains six principal claims, but they occupy different evidence
lanes. Exact positive-homogeneity rescaling supports the narrow mathematical
claim that raw per-weight magnitude cannot be a representation-invariant
property for the stated network class. Limb decomposition, parameter-count
changes, codebooks, and decoder dependence support additional constructive
counterexamples to nominal bits-per-weight as an invariant. The formal
functional-rate definitions and monotonicity statements are conditional
properties of a declared feasible set. The compiler, precision field,
progressive bundle, router, certificate, and advanced-system implications are
architectural proposals. The eight experiments are a falsification program,
not results.

The paper consequently does **not** establish a universal numerical ceiling,
the globally shortest implementation, a general behavioral quotient, useful
compression, safe low-bit operation, router calibration, certificate validity,
formal verification at frontier scale, security improvement, production
transfer, or an ASI result. The reference list is an author-supplied research
map. It cannot promote a book claim until each external result is independently
resolved and passage-reviewed.

## Conceptual Primitives

- **Reference system $M_\theta$.** The complete behavior-producing system,
  including learned parameters, preprocessing, tokenizer, sampler, retrieval,
  tools, and runtime components inside the declared boundary.
- **Candidate description $z$ and decoder $\mathsf{Dec}$.** A finite package
  and the exact machinery that realizes $\widehat M_z=\mathsf{Dec}(z)$; shared
  side information is named or counted.
- **Precision contract $\mathcal C$.** Domain, protected behaviors, metric
  vector, thresholds, aggregation, confidence or proof coverage, physical
  resource terms, and escalation/fallback policy.
- **Contract-acceptable set $[M]_\mathcal C$.** Candidates that satisfy the
  declared predicate. It is a true quotient class only when the relation has
  the required reflexive, symmetric, and transitive properties.
- **Functional contract rate $R^\star$.** The minimum complete description
  length over acceptable candidates inside named decoder and code families.
  In practice a compiler supplies an achieved upper bound, not the exact
  optimum.
- **Behavioral distortion vector.** Output-distribution, decision,
  calibration, trajectory, safety/property, invariant, and resource
  components with explicit conditional or tail aggregation.
- **Precision field.** A mapping from component, input, internal state, and
  contract to a representation/execution choice. Static mixed precision is a
  restricted case.
- **Base/residual bundle.** A cumulative executable base plus ordered bit
  planes, sparse exceptions, low-rank corrections, codebook additions,
  protected blocks, adapters, or exact tools.
- **Safe operating envelope.** Predicates under which one low-cost level is
  admitted, with higher precision, reference execution, abstention, or review
  outside the envelope.
- **Precision certificate.** A scoped, expiring receipt binding exact
  artifacts, system boundary, contract, evidence, costs, known failures,
  routing, fallback, and status; it is not deployment authority.

## Interfaces, Artifacts, and State Machines

The compiler input packet freezes the reference package, contract, disjoint
calibration and validation suites where independence is required, target
platform semantics, encoding grammar, and assurance budget. Its output is not
one weight file but a package
`({z^(0), …, z^(K)}, router, decoder, certificate)` plus lineage, transform,
accounting, and evidence records. The durable artifact family listed below is
therefore a connected lifecycle rather than interchangeable documentation.

The contract state machine begins as a draft, becomes frozen for a compile and
evaluation transaction, and can be superseded only through versioned review.
Candidate levels move from proposed through proxy search to independently
evaluated acceptance, restriction, rejection, or quarantine. The router is a
separate qualified artifact. Certificate state is one of `CERTIFIED`,
`PROVISIONAL`, `DOMAIN_RESTRICTED`, `UNSAT`, `UNVERIFIED`, or `REVOKED`.
Artifact, decoder, kernel, platform, domain, evaluator, policy, or drift changes
can narrow, expire, or revoke a status. Readmission re-evaluates the changed
predicates; old history remains append-only.

The full ownership split is important. Compression owns candidate transforms
and complete-description receipts; routing owns runtime selection but not
certificate status; evidence owners qualify metrics and proof/test artifacts;
resource governance owns physical and assurance cost; custody and release own
copies and derivative closure; readiness owns admission; runtime enforcement
owns fallback and abstention; incident response owns revocation propagation;
and human/legal owners retain any review, rights, or public-release authority.

## Core Distinctions

1. **Parameter precision versus functional precision.** Parameter distance is
   coordinate-dependent; contract-relevant behavior is the protected object.
2. **Artifact bytes versus complete executable description.** Values,
   structures, indices, scales, codebooks, residuals, routing, decoder,
   runtime, metadata, and assurance material all count.
3. **Average quality versus protected behavior.** Aggregate parity can conceal
   regressions on rare, safety-critical, calibrated, or abstention-sensitive
   cases.
4. **Static bit width versus a precision field.** Required precision may vary
   by layer, channel, direction, token, task, uncertainty, and consequence.
5. **Base representation versus residual precision.** A cheap base path can be
   refined by ordered residuals when the contract or uncertainty requires it.
6. **Stored bits versus physical cost.** Moved bits, operations, latency,
   energy, memory pressure, repair, verification, and assurance-generation
   cost remain separate.
7. **Certificate existence versus certificate validity.** A receipt describes
   a scoped artifact and evaluation; it does not inherit trust, freshness,
   transfer, or deployment authority automatically.

## Precision Contract

A usable contract binds at least:

- deployment domain and excluded conditions;
- protected behaviors, slices, and failure families;
- metric vector and per-metric thresholds;
- aggregation and worst-case or tail rules;
- confidence and evidence requirements;
- memory, bandwidth, latency, energy, and verification budgets;
- escalation, abstention, fallback, and revocation behavior;
- exact reference, transformed artifact, decoder, kernel, platform, and
  evaluator identities.

The acceptable set contains every complete implementation satisfying those
obligations. The functional rate–distortion problem minimizes complete
description length or physical cost over that set. The formulation is
conditional on the chosen contract and implementation language; it is not a
universal Kolmogorov-complexity oracle.

## Mechanisms

- Canonicalize known representation freedoms before treating numerical
  magnitude or local sensitivity as meaningful.
- Define a metric-vector contract over protected behavior rather than one
  aggregate score.
- Search over complete executable implementations, counting metadata,
  residuals, decoders, routing, verification, and fallback.
- Allocate a precision field by marginal contract benefit per marginal
  physical cost.
- Encode a low-cost base plus ordered residual precision planes.
- Route conservatively among base, refined, fallback, abstention, and
  escalation paths.
- Verify protected slices, shifts, calibration, physical cost, and recovery.
- Bind the qualified scope, identities, evidence, limits, expiry, and
  revocation into a precision certificate.

## Functional Precision Compiler

The proposed compiler lifecycle is:

1. **Reference:** freeze the source model, runtime, task contract, evaluator,
   evidence policy, and resource envelope.
2. **Canonicalize:** remove or normalize known coordinate and serialization
   freedoms before interpreting sensitivity or precision.
3. **Measure:** instrument functional sensitivity and contract-level
   distortion, treating local curvature and salience only as proxies.
4. **Transform:** generate quantization, factorization, pruning, codebook,
   mixed-precision, and residual candidates.
5. **Allocate:** assign precision by marginal contract value per marginal
   physical cost rather than by tensor name alone.
6. **Encode:** count the complete executable package, including indices,
   metadata, decoder, routing, and verification material.
7. **Layer residuals:** order optional refinement planes by expected contract
   benefit per added cost and preserve a safe terminal route.
8. **Route:** select base, refined, or fallback execution using observable
   uncertainty and consequence signals.
9. **Verify:** test protected slices, shifts, calibration, rare failures,
   latency, energy, memory, and rollback under independently implemented
   evaluation where the claim requires it.
10. **Certify:** bind the qualified result, limits, expiry, revocation,
    identities, evidence, and complete accounting into a precision certificate.

## Assumptions and Invariants

- Reference and candidate behavior are evaluated within an explicit system
  boundary; changing preprocessing, sampling, retrieval, tools, or target
  arithmetic can define a different system rather than a harmless format
  variant.
- Description length is relative to a fixed code/decoder and declared shared
  side information. Moving complexity into a library or pretrained decoder is
  not a free reduction.
- Contract satisfaction is vector-valued. Safety-critical or no-tradeoff
  clauses are not averaged away by broad utility gains.
- Search proxies and acceptance evidence remain separate. Curvature, Fisher,
  Jacobian, activation salience, tensor reconstruction, and calibration-set
  fit may rank candidates but cannot waive held-out contract obligations.
- Calibration and validation data are disjoint whenever the confidence claim
  depends on independence. Dependence, adaptive sampling, multiplicity, and
  zero-observed-failure uncertainty are recorded explicitly.
- Canonicalization is behavior-preserving within its own named numerical
  tolerance, reversible enough for audit, and not assumed unique or optimal.
- Every cumulative precision level is evaluated. Extra numeric bits can cross
  decision or routing boundaries and therefore do not inherit behavioral
  monotonicity from smaller reconstruction error.
- The router sees only deployable signals. It cannot use answer keys, post hoc
  oracle labels, or confidence that was never calibrated for the transformed
  level.
- Complete physical accounting separates stored bits, moved bits, operations,
  latency, energy, peak memory, decoder work, routing, fallback, repair,
  verification, certificate generation, monitoring, and retained reference
  cost.
- No protected property transfers by presumption. It needs evidence bound to
  the exact candidate implementation and property scope.
- Certificate identity, evidence class, domain, time window, expiry, and
  revocation travel with every rendered status. Status alone is invalid.
- Fidelity to a reference is not fitness for deployment; external safety,
  correctness, rights, or policy predicates can be stricter than reference
  imitation.

## Algorithms and Conditional Results

The ten-stage compiler is intentionally search-and-check rather than a closed
form optimizer. Canonicalization balances known scale freedoms and records the
transform. Instrumentation translates each contract clause into probes or
formal specifications with destructive negative controls and known-invariance
positive controls. Sensitivity estimation combines local curvature, output
Jacobians, salience, causal ablation, candidate replacement, adversarial
search, trajectory effects, and protected-boundary disagreement while
recording uncertainty and stability. Transformation proposes equalization,
rotations, codebooks, sparsity, factors, outlier extraction, and residual
forms. A multiple-choice allocation approximation selects component formats
under metric constraints, then end-to-end validation repairs the additivity
fiction. Accepted candidates form a nested Pareto set; a conservative router
is trained and evaluated as part of the system; exact exported artifacts are
then verified and certified.

Four formal facts remain conditional rather than empirical results:

1. positive-homogeneous rescaling makes a raw per-weight magnitude ceiling
   non-invariant for the stated class;
2. relaxing a scalar tolerance cannot increase the exact functional optimum;
3. functionally identical implementations can have different parameter counts
   and nominal bits per parameter; and
4. strengthening a contract cannot reduce the exact optimum when its feasible
   set is a subset of the weaker contract's set.

Local sensitivity yields an idealized allocation heuristic only after fixing a
canonical parameterization and small-error regime. If the contract distortion
is locally quadratic, transformed directions with larger curvature receive
finer steps. Flat directions, indefinite curvature, discrete low-bit errors,
rare events, long-horizon amplification, and discontinuous boundaries break
the approximation. The operational floor is likewise contract-specific: once
additional fidelity cannot be shown to improve a protected outcome under the
available evidence and accepted risk, it lacks demonstrated operational value;
this does not make the bits metaphysically meaningless.

## Formal and Conditional Results

- Exact reparameterization examples defeat any universal
  representation-independent upper bound stated solely as maximum weight
  magnitude or per-weight bit width.
- Functional equivalence is a relation over implementations relative to a
  contract, not proof that two parameter vectors are close.
- Progressive precision can dominate a single static encoding only when the
  router, residual ordering, decoder, and added verification burden are counted
  and the protected contract is preserved.
- A functional sensitivity score may help allocate precision, but it is not
  automatically causal, stable under reparameterization, or sufficient for a
  protected-behavior guarantee.
- A certificate is valid only for its named artifact, decoder, runtime,
  platform, domain, evidence, and time window.

## Proposed Artifact Family

- `PrecisionContract`.
- `CanonicalizationReceipt`.
- `FunctionalSensitivityMap`.
- `PrecisionFieldPlan`.
- `CompleteDescriptionLedger`.
- `BaseResidualPrecisionBundle`.
- `PrecisionRouteDecision`.
- `FallbackAndEscalationPolicy`.
- `BehavioralEquivalenceReport`.
- `PrecisionCertificate`.
- `CertificateExpiryOrRevocationEvent`.
- `PrecisionTransformationLineage`.

## Evidence and Falsification Program

The paper proposes a claim-commensurate program rather than one headline
compression number:

- **Reparameterization stress:** show that naïve magnitude and precision rules
  move under function-preserving coordinate changes.
- **Distance comparison:** compare parameter-space distances with
  contract-level behavioral distances.
- **Complete accounting:** include codebooks, scales, indices, residuals,
  decoders, routing, metadata, verification, and assurance cost.
- **Progressive residual curves:** measure contract benefit and physical cost
  for each added precision plane, including fallback frequency.
- **Aggregate-equivalence traps:** construct rare or protected slices where
  average parity hides important regressions.
- **Static versus routed precision:** compare strong tuned static,
  layer-wise, mixed, progressive, and dynamically routed policies.
- **Certificate discrimination:** test whether invalid identities, stale
  domains, missing costs, changed kernels, expired evidence, and revoked
  artifacts are rejected.
- **Distribution shift:** evaluate whether sensitivity, routing, and
  certificate scope fail conservatively outside the qualification domain.

The idea loses or narrows when a strong static policy matches protected
behavior at lower total cost, routing adds more overhead or attack surface than
it saves, residual ordering fails to transfer, complete description length
eliminates the apparent gain, canonicalization does not improve allocation
stability, certificates fail to discriminate invalid deployments, or protected
behavior cannot be specified and measured competently.

## Failure Modes

- Treating bits per weight as an invariant capability property.
- Counting only payload values while hiding scales, codebooks, indices,
  residuals, decoder logic, or assurance artifacts.
- Using parameter distance as a behavioral guarantee.
- Protecting average accuracy while rare or high-consequence slices regress.
- Allocating precision from unstable or non-causal salience proxies.
- Router oscillation, route gaming, adversarial escalation suppression, or
  silent fallback retirement.
- Approximate decoder or kernel changes outside the certified scope.
- Certificate laundering across hardware, runtime, domain, or artifact
  versions.
- Omitting verification and assurance-generation costs from efficiency claims.
- Equating a formal record invariant with correct contract selection or
  real-world safety.

## Threats, Costs, and Governance

The central governance hazard is contract gaming: the compiler can optimize
every listed clause while failing an unmodeled behavior. Distribution shift,
rare cases, measurement dependence, evaluator capture, reference fallibility,
and incomplete threat models keep unknowns open. The contract therefore needs
adversarial review, conditional slices, explicit exclusions, monitoring,
expiry, and conservative fallback. “Zero failures observed” receives a
confidence bound, not a proof label.

The runtime threat surface includes adversarial suppression of escalation,
forced expensive escalation, route oscillation, confidence manipulation,
protected-domain evasion, residual omission, corrupted or unavailable
fallback, and denial of service through precision purchases. The artifact
surface includes malicious codebooks, transforms, scales, kernels, decoder
substitution, sparse-index corruption, certificate laundering, stale caches,
and reconstructed descendants outside custody. The epistemic surface includes
equating aggregate parity with protected equivalence, treating a local
sensitivity proxy as causal, hiding complexity in shared side information, and
describing a bounded formal result as whole-system safety.

Four classes of bits must be reported separately: representational values;
structural interpretation such as shapes, scales, codebooks, indices,
transforms, factors, and routing tables; residual corrections and protected
modules; and assurance identities, manifests, tests, proofs, exception lists,
and expiry rules. Assurance-generation work—testing, verification, review, and
monitoring—is a separate cost from stored assurance bits. A larger, regular
representation can be cheaper over its lifecycle when it is substantially
easier to execute, qualify, and maintain.

## Cross-Paper Synthesis

- **RankFold/NeuralFold and BBVCA.** Precision Contract supplies the missing
  acceptance object for weight-like compression: complete package accounting,
  behavior rather than coordinate fidelity, protected tails, and scoped
  qualification. RankFold/BBVCA contribute archive, reconstruction, repair,
  residual, and fallback discipline. Neither establishes the other's
  empirical result.
- **Compact Generative Systems and KERC.** Base/residual precision is one
  instance of residual honesty. KERC's semantic residual hierarchy generalizes
  the same rule: what leaves the hot path remains stored, scoped, versioned,
  recoverable, and costed rather than disappearing from the denominator.
- **Reflexive Router.** Both papers use risk–coverage reasoning, explicit
  abstention, and deadline-aware fallback. Precision Contract adds a numerical
  resource lane; Reflexive Router adds intent, OOD, and authority boundaries.
  Neither permits a learned route outcome to learn authorization.
- **Deterministic Capability Compilation.** A transformed precision level can
  become a compiled specialist only after protected behavior, residuals,
  fallback, monitoring, and rollback qualify. The reference/teacher remains a
  test oracle and recovery route while those obligations persist.
- **QCSA and Kernel English.** All three reject a monolithic scalar target.
  Precision must preserve the vector contract of the receiving architecture,
  including cyclic-memory, semantic compiler, renderer, exact-object, and
  residual state; a small checkpoint cannot hide expanded decoder or assurance
  complexity.
- **RDC.** Relational operators, schemas, incidence tables, caches, and
  contraction certificates introduce irregular structural and assurance cost.
  Precision allocation can vary by operator or role, but topology, branch, and
  authority distinctions cannot be quantized away merely because average
  outputs remain close.
- **Resource economics and readiness.** Functional precision joins model,
  context, search, tool, and verification routes on one complete frontier.
  Certificate state informs readiness but does not grant deployment or public
  release authority.

## Book Chapters Supported

| Chapter | Contribution | Boundary |
|---|---|---|
| `rankfold-neuralfold-and-artifact-compression` | Primary owner. Reframes compression admission around functional rate–distortion, representation invariance, complete executable accounting, protected behavior, the compiler lifecycle, and precision certificates. | Does not establish that RankFold, NeuralFold, or any proposed encoding achieves the optimum or preserves behavior. |
| `compact-generative-systems-and-residual-honesty` | Makes numeric precision a concrete compact-representation case; adds ordered base/residual precision and contract-benefit-per-cost accounting. | Reconstruction, behavioral adequacy, downstream utility, and total cost remain separate. |
| `fast-generation-architectures` | Adds static, mixed, progressive, and dynamically routed precision as execution policies with escalation and safe fallback. | No speedup, model-quality, router-quality, or hardware result is imported. |
| `resource-economics-and-token-budgets` | Separates stored, moved, decoded, verified, and assurance-generating costs and makes precision one governed resource. | The paper supplies a cost model, not measured economics. |
| `readiness-gates-residual-escrow-and-quarantine` | Adds scoped precision-certificate status, expiry, domain restriction, revocation, residual custody, and readmission. | Certification records do not establish readiness or deployment authority. |
| `executable-specifications-and-lean-proof-envelope` | Treats quantization and compression as program transformations with explicit refinement obligations from reference behavior to bit-exact execution. | Finite formal refinement cannot prove evaluator adequacy, protected-property completeness, or natural-world safety. |
| `model-weight-custody-and-hardware-roots-of-trust` | Extends derivative closure to quantized shards, codebooks, residuals, decoders, kernels, caches, and exact platform-bound identities. | Custody and identity do not prove behavioral equivalence. |
| `the-efficient-asi-hypothesis` | Positions precision as one adaptively routed resource alongside model choice, search, context, verification, and fallback. | The paper does not establish an efficiency advantage. |
| `open-weight-release-and-post-release-control` | Treats precision variants, residuals, decoders, and derivative artifacts as release-scope objects whose governance must survive transformation. | A precision contract does not make an irreversible public release recallable. |

## Chapter Decision

**Update existing chapters first; do not add a chapter now.** The paper's
distinctive lifecycle is substantial, but the existing RankFold/NeuralFold
chapter already owns compressed-artifact admission and the Compact Generative
chapter already owns residual honesty. A new chapter today would duplicate
those owners and violate the active structural freeze.

A standalone `functional-precision-and-behavior-preserving-computation`
chapter may be reconsidered only after the bounded integrations are drafted and
reviewed. Reconsideration requires evidence that representation invariance,
precision-field allocation, compiler/certificate lifecycle, and experimental
program cannot be taught coherently under the current owners without blurring
their jobs. This is a contingency, not an admitted research candidate, chapter
reservation, manifest row, or promised chapter count.

## External-Literature Resolution

The paper's reference list is an author-supplied research map, not automatic
Appendix H admission. Before external-support use:

1. deduplicate every cited item against the source inventory by title, DOI,
   arXiv identifier, and canonical URL;
2. verify primary publication pages and current bibliographic status;
3. passage-review the exact result used;
4. separate foundational rate–distortion, MDL, numerical-analysis,
   quantization, mixed/progressive precision, verification, and security roles;
5. preserve source-reported results as unreproduced unless the book runs an
   accepted claim-specific replication.

Priority resolution families are Shannon rate–distortion, classical
quantization and floating-point analysis, MDL, LLM quantization and
mixed/progressive precision, formal verification of quantized networks, and
quantization-specific attack surfaces.

## Claims To Add Or Update

- Replace universal bits-per-weight language with contract-relative functional
  precision wherever the book discusses quantization or compact weights.
- Require the full executable package and physical-cost denominator for a
  compression or efficiency claim.
- Treat progressive and dynamic precision as governed routes with escalation
  and fallback rather than intrinsic properties of a tensor.
- Bind every admitted precision artifact to exact source, decoder, kernel,
  runtime, platform, domain, evidence, expiry, and revocation identity.
- Treat quantization and compression as program transformations whose
  protected properties require explicit refinement or competent empirical
  verification.
- Keep sensitivity, reconstruction, protected behavior, utility, cost,
  authority, and support as separate claim axes.

## Open Questions

- Which canonicalization families make functional sensitivity stable enough to
  guide allocation across model families?
- How should contracts combine tail risk, calibration, abstention, and
  high-consequence slices without becoming impossible to evaluate?
- When does dynamic routing outperform a strong static mixed-precision policy
  after router, attack-surface, verification, and fallback costs?
- How should certificate evidence expire under model, runtime, platform, data,
  and deployment drift?
- Can residual planes be ordered robustly across workloads, or must the order
  itself be routed?
- Which parts of the compiler lifecycle warrant a distinct chapter after the
  current-owner integration is complete?

## Nonclaims

- No universal optimal precision, bit width, or compression ratio is proved.
- No frontier model was quantized, compressed, routed, or certified.
- No source-reported quantization or verification result is reproduced.
- No precision certificate is implemented or independently validated.
- No chapter, support state, release, readiness, deployment, AGI, or ASI claim
  is added by this intake.
- The raw supplied files are not published by the tracked source note.

## Section-Family Coverage

| Paper section family | Actual manuscript or durable owner | Disposition and boundary |
|---|---|---|
| Abstract and §1 | RankFold/NeuralFold; Efficient ASI; this note | Five-part thesis, six claims, contribution boundary, and architecture integrated. No implementation or universal bit claim inferred. |
| §2 universal-bound critique | RankFold/NeuralFold; Executable Specifications; source note | Magnitude/range/resolution/description separation, exact rescaling, limb redistribution, coordinate design, global-physical-bound boundary, and measurement-precision boundary retained. Exact proposition is class-scoped. |
| §3 prior work and novelty | source note; Appendix H external-resolution backlog | Rate–distortion, MDL, quantization, mixed/progressive precision, verification, security, and novelty boundaries retained. All 49 citations require independent primary-source resolution before support use. |
| §4.1–4.3 formal system and distortion | RankFold/NeuralFold; source note | Complete deployed boundary, decoder dependence, metric vector, aggregation, SAT predicate, agent trajectories, and property violations integrated or retained. A metric vector is not automatically adequate. |
| §4.4–4.6 rate and acceptable set | RankFold/NeuralFold; Resource Economics; source note | Complete executable length, functional contract rate, code-family dependence, achieved-upper-bound boundary, and quotient/neighborhood distinction integrated. $R^\star$ is not computable “bits in intelligence.” |
| §4.7 elementary properties | RankFold/NeuralFold; source note | Tolerance monotonicity, nominal-rate representation dependence, and contract-strengthening monotonicity retained as conditional mathematical results; no heuristic monotonicity inferred. |
| §4.8–4.9 sensitivity and operational floor | source note; RankFold/NeuralFold; Efficient ASI | Local curvature allocation, its failure conditions, and contract-specific operational floor retained. Sensitivity is a search proxy; unsupported precision is not metaphysical fiction. |
| §5 contract | RankFold/NeuralFold; Readiness; Resource Economics | Required fields, distributional/conditional/formal/adaptive classes, consequence-aware behavior, statistical acceptance, resource vector, versioning, expiry, and reference-versus-deployment distinction integrated. |
| §6 compiler | RankFold/NeuralFold; Executable Specifications; source note | Inputs, nine operational stages plus frozen reference, reversible canonicalization, instrumentation controls, multi-estimator sensitivity, transforms, allocation, residuals, router, exported-artifact verification, certificate, and pseudocode retained. No compiler exists. |
| §7 progressive precision | Compact Generative; Fast Generation; Efficient ASI | Precision field, cumulative levels, nonmonotone behavior warning, residual-form family, benefit/cost ordering, metareasoning, safe envelope, any-precision handoff, and substitute resources integrated. No dynamic-route gain is claimed. |
| §8 verification/certification | Executable Specifications; Readiness; RankFold/NeuralFold; Custody | Program-transformation rule, four bit classes, six statuses, certificate fields, evidence hierarchy, regional margin refinement, monitoring, drift, and revocation integrated. No certificate proves broad safety or release merit. |
| §9 experimental program | RankFold/NeuralFold; source note; roadmap empirical backlog | Seven research questions, five model/task classes, eight experiments, strong baselines, positive/negative controls, falsifiers, and full reporting standard retained. No result exists. |
| §10 advanced-system implications | Efficient ASI; Compact Generative; Fast Generation; source note | Functional distinguishability, governed precision, common-base/exceptional-residual architecture, capability-consequence assurance, and anti-metaphysical conclusion integrated as implications. |
| §11 limitations/open problems | receiving-chapter failure modes; source note | All eleven limitation families plus research directions retained: incompleteness, distribution, verification, side information, hardware, discontinuity, reference fallibility, assurance dominance, router attack, other fidelity approximations, and intractable optimum. |
| §12 conclusion | RankFold/NeuralFold summary; this note | Contract-relative optimization and research-proposal status integrated without support promotion. |
| Appendix A | source note; glossary | Notation retained as the formal vocabulary for future implementation and schema work. |
| Appendix B | source note; future schema/fixture work | Illustrative contract preserves boundary, protected behaviors, no-tradeoff clauses, resource objective, precision levels, evidence, expiry, and status rules. Placeholder thresholds are not admitted facts. |
| Appendix C | source note; future schema/fixture work; Custody/Readiness | Illustrative certificate preserves exact identities, four-class accounting, evidence outcomes, envelope, limitations, and revocation triggers. It is an example, not a validated artifact. |
| Appendix D | RankFold/NeuralFold; Executable Specifications; Resource Economics; source note | Magnitude/precision interpretation, non-metaphysical $R^\star$, submeasurement-bit utility, and separated assurance length/generation cost integrated. |
| References | Appendix H external-resolution backlog | Forty-nine author-supplied references retained as a research map. No bibliography entry was converted into local reproduction or claim support by this audit. |

## Closure Status

**Section-family audit complete as of 2026-07-31.** All twelve numbered
sections, four appendices, and references terminate in manuscript integration,
public-safe note retention, an explicit implementation/evaluation obligation,
or a non-claim. The earlier eight-owner prose transaction already preserved
the central lifecycle. This audit repaired the material compression: the four
contract classes, formal rate and acceptable-set caveats, conditional
monotonicity results, precision-level nonmonotonicity, full residual family,
safe operating envelope, four bit classes, six certificate states, evidence
hierarchy, regional refinement condition, progressive release-package closure,
and exact eight-experiment/five-model program are now visible in their logical
owners.

Closure does not establish a Functional Precision Compiler, an achieved or
optimal functional rate, canonicalization benefit, stable sensitivity map,
behavior-preserving quantization, progressive residual gain, safe router,
certificate discrimination, formal frontier-model refinement, complete cost
advantage, release control, security or safety result, external reproduction,
production transfer, or ASI support. The source remains `argument`; reopen on
material source or receiving-chapter drift.
