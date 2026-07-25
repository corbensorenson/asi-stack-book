# Source Note: Reluplex: An Efficient SMT Solver for Verifying Deep Neural Networks

| Field | Value |
|---|---|
| Source ID | `ext_reluplex_2017` |
| Source title | Reluplex: An Efficient SMT Solver for Verifying Deep Neural Networks |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1702.01135, https://arxiv.org/abs/1702.01135 |
| Citation label | Katz et al. (2017), Reluplex |
| Published / updated | 2017-02-03 / 2017-05-19 |
| DOI | 10.48550/arXiv.1702.01135 |
| Ingestion basis | Primary arXiv abstract and metadata plus the official Stanford publication page inspected for AI-verification vocabulary; paper not vendored into this repository and no Reluplex run or ACAS Xu property check reproduced. |

## Thesis

Reluplex belongs in the verification-bandwidth, proof-envelope, benchmark,
resource, and adversarial-ML chapters as an external example of formal
verification applied to neural networks under scoped properties. It gives the
ASI Stack a comparison point for property-specific AI verification without
implying that broad model behavior, context adequacy, robustness, or ASI safety
is verified.

## Mechanisms

- Extend SMT-style reasoning to ReLU neural networks.
- Verify specified properties or produce counterexamples.
- Bind the claim to a particular network, input region, arithmetic model, and property.
- Treat a safety-critical neural-network application as a property-checking target.
- Evaluate the source technique on an ACAS Xu prototype setting in the paper's own scope.

## Evidence

- The source reports a verification technique and paper-scope evaluation for ReLU neural networks.
- This repository has not run Reluplex, imported ACAS Xu networks, reproduced property checks, or verified any ASI Stack model.
- Use this source for external AI-verification vocabulary and limits, not as local evidence for model safety or empirical robustness.

## Failure Modes

- Verifying one property can leave many behaviorally important properties unmodeled.
- A certificate can be invalidated by a different checkpoint, preprocessing path, numerical semantics, or deployment implementation.
- Neural-network verification may not cover natural distribution shift, tool use, memory retrieval, governance policy, or user-intent interpretation.
- Unsupported operators or broad input regions can make a verifier time out or require abstractions whose losses must remain visible.
- A counterexample-friendly formal method still depends on the property being well chosen and tied to the deployment context.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets; includes Simulation Fidelity and Claim Transport)
- `adversarial-machine-learning-and-model-attack-surface` (Adversarial Machine Learning and the Model Attack Surface)

## Claims To Add Or Update

- Use this note to distinguish property-specific formal verification from broad model or system safety.
- Treat a neural certificate as one bounded defense artifact beside adaptive empirical attacks, clean utility, monitoring, recovery, and residuals.
- Record unknown and timeout outcomes rather than counting only proved properties.
- Do not claim any local neural-network verification, ACAS Xu reproduction, robustness result, or ASI Stack model guarantee.
- Keep support state at `argument` until a scoped model, property, command, result, implementation binding, and evidence transition exist.

## Open Questions

- Which ASI Stack properties are precise enough for neural-network or route-verification tooling?
- How should counterexamples flow into the model-attack ledger, claim ledger, and benchmark ratchet?
- Which numerical and preprocessing semantics must be reproduced before a certificate binds to the deployed model?
- What simulation-fidelity record inside Resource Economics would be needed before a verified property matters operationally?
