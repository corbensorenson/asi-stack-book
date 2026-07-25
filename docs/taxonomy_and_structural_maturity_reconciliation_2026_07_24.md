# Taxonomy and Structural-Maturity Reconciliation

Date: 2026-07-24  
Authority: active Post-v2.3 maintenance roadmap  
Support-state effect: none  
Release effect: none

## Decision

The two external reviews contained four material findings with teeth:

1. the book’s danger treatment was organized mainly around governance controls and did not give dangerous-capability domains and misuse uplift one explicit owner;
2. provenance, watermarking, synthetic-media authenticity, semantic truth, consent, and remedy were distributed across adjacent chapters without one end-to-end content-integrity lifecycle;
3. misuse prevention and incident response lacked a population- and institution-scale resilience owner;
4. deliberate open-weight release was treated mainly as custody and release policy, not as an irreversible post-release control transition.

All four are distinct interface and lifecycle owners. They are admitted now as:

- `dangerous-capability-domains-and-misuse-uplift`;
- `content-authenticity-watermarking-and-synthetic-media-integrity`;
- `societal-resilience-and-misuse-defense`; and
- `open-weight-release-and-post-release-control`.

The manifest moves from 76 to 80 chapters. All four chapters remain `Design rationale` at `argument`. Admission creates no empirical, formal, safety, readiness, release, deployment, transfer, or SOTA result.

## Structural-maturity correction

The criticism that several recent chapters were title-complete but territory-thin was valid. Word count alone is not the repair criterion. A new or materially revised chapter now has to demonstrate:

1. a problem and interface that no adjacent owner can absorb without losing an authority or lifecycle boundary;
2. named internal sections whose mechanisms differ rather than repeating a shared template;
3. at least one mechanism, one realistic failure family, one strongest challenge or simpler baseline, and one explicit nonclaim;
4. source engagement that states what each source contributes and what cannot be inferred from it;
5. a reader handoff that preserves ownership rather than restating the chapter;
6. a claim/evidence mapping and source note sufficient for independent audit.

This standard was applied to the four admitted chapters. It was also used to repair the three title/content mismatches identified by the review:

- Adversarial Machine Learning now treats adversarial examples, extraction and inversion, poisoning, backdoors, adaptive attacks, and bounded certification explicitly.
- Learning Theory now treats PAC/sample complexity, interpolation and double descent, description-length priors, scaling laws, and emergence-versus-metric artifacts explicitly.
- Autonomous Replication now defines replication, names a six-level replication ladder, preserves complete attempt denominators, and models containment as a competing mechanism rather than using autonomy as a proxy.

## Existing-owner integrations

The remaining worthwhile findings do not own new chapters. They are integrated into the following existing owners:

| Finding | Owner | Required boundary |
|---|---|---|
| Secure researcher access, clean rooms, third-party audits | Institutions, International Coordination, and Public Legitimacy | Independent scrutiny, protected disclosure, conflicts, result custody, and sponsor non-veto |
| Eliciting latent knowledge | White-Box Evidence, Interpretability, and Activation Governance | Predictor/report separation; research agenda, not solved truth elicitation |
| Mechanistic anomaly detection | White-Box Evidence, Interpretability, and Activation Governance | Deviation evidence, causal tests, false-alarm burden, and no intent inference |
| Training-data attribution and influence functions | White-Box Evidence; Data Engines | Approximate attribution is not causal responsibility, privacy proof, or erasure |
| Hardware-enabled guarantees | Model-Weight Custody; Physical Compute; Institutions | Exact coverage, update authority, bypass, privacy, abuse, and legitimacy |
| Proof of learning/training | Governed Training; Supply-Chain Integrity | Auditable state sequence without laundering it into data, quality, or safety proof |
| Test-time training | Governed Training; Replaceable Cognitive Substrates | Mutable inference state, isolation, reset, rollback, and cross-tenant influence |
| Curriculum learning | Governed Training; Data Engines | Exposure order as versioned training state; matched schedule ablations |
| Legal alignment | Constitutional Alignment; Institutions | Jurisdiction, interpretation, conflicts, authority, appeal, and legitimacy |
| Certified neural verification | Executable Specifications; Adversarial ML | Network, region, property, arithmetic, verifier, timeout, and implementation binding |
| Causal discovery and do-calculus | Governed World Models | Observational/interventional separation and assumption custody |
| Digital twins and sim-to-real | Embodied Agency | Plant identity, synchronization, validity envelope, transfer residual, and physical fallback |
| Diffusion language models | Replaceable Cognitive Substrates | Non-autoregressive state, schedule, remasking, stopping, rollback, and matched cost |

These integrations are present as named manuscript sections, citations, manifest source assignments, claim-source mappings, and source-note chapter routes. They are not roadmap-only promises.

## Findings not accepted as new chapters

- “AI R&D acceleration” remains a capability domain, evaluation target, and recursive-self-improvement input. Splitting it into another chapter would duplicate Dangerous Capabilities, Scientific Discovery, Capability Thresholds, and Recursive Self-Improvement.
- “Limiting generality” remains a cross-cutting least-power and architecture-design principle owned by System Boundaries, Capability Thresholds, Routing, and Replaceable Substrates. It is not one lifecycle.
- “AI welfare” remains owned by Moral Uncertainty and Constitutional Alignment until a distinct operational interface can be stated without pretending that moral-patient detection is solved.
- Flow matching, diffusion models outside language, and other generative families remain routed to Fast Generation and Replaceable Substrates; architecture names alone do not justify chapters.

## Evidence and publication boundary

This transaction improves conceptual coverage and source alignment. It does not answer the active roadmap’s central empirical question. The shared Theseus flagship, competent natural workloads, independent evaluators, transfer, meaning-preserving editorial compression, and exact build/deploy/attestation chain remain unfinished work.

The no-deferral policy remains active: future ideas must be integrated, admitted, or rejected immediately. “No live candidate queue” does not mean the taxonomy is permanently frozen; it means no identified manuscript idea is being hidden in a deferred list.
