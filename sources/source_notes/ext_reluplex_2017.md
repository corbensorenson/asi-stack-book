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
| Ingestion basis | Primary arXiv abstract and metadata inspected for AI verification vocabulary; paper not vendored into this repository and no Reluplex run or ACAS Xu property check reproduced. |

## Thesis

Reluplex belongs in the verification-bandwidth, proof-envelope, benchmark, and simulation chapters as an external example of formal verification applied to neural networks under scoped properties. It gives the ASI Stack a comparison point for property-specific AI verification without implying that broad model behavior, context adequacy, or ASI safety is verified.

## Mechanisms

- Extend SMT-style reasoning to ReLU neural networks.
- Verify specified properties or produce counterexamples.
- Treat a safety-critical neural-network application as a property-checking target.
- Evaluate the source technique on an ACAS Xu prototype setting in the paper's own scope.

## Evidence

- The source reports a verification technique and paper-scope evaluation for ReLU neural networks.
- This repository has not run Reluplex, imported ACAS Xu networks, reproduced property checks, or verified any ASI Stack model.
- Use this source for external AI verification vocabulary and limits, not as local evidence for model safety.

## Failure Modes

- Verifying one property can leave many behaviorally important properties unmodeled.
- Neural-network verification may not cover distribution shift, tool use, memory retrieval, governance policy, or user-intent interpretation.
- A counterexample-friendly formal method still depends on the property being well chosen and tied to the deployment context.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `simulation-fidelity-and-physical-constraints` (Simulation Fidelity and Physical Constraints)

## Claims To Add Or Update

- Use this note to distinguish property-specific formal verification from broad model or system safety.
- Do not claim any local neural-network verification, ACAS Xu reproduction, or ASI Stack model guarantee.
- Keep support state at `argument` until a scoped model, property, command, result, and evidence transition exist.

## Open Questions

- Which ASI Stack properties are precise enough for neural-network or route-verification tooling?
- How should counterexamples flow into the claim ledger and benchmark ratchet?
- What simulation-fidelity record would be needed before a verified property matters operationally?
