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
