# Source Note: SLSA v1.0

| Field | Value |
|---|---|
| Source ID | `ext_slsa_v1_0` |
| Source title | SLSA v1.0 |
| Ingestion date | 2026-06-29 |
| Source version / URL | SLSA v1.0 specification, https://slsa.dev/spec/v1.0/ |
| Citation label | OpenSSF SLSA (2023), SLSA v1.0 |
| Published / updated | 2023 / 2026 |
| Ingestion basis | Public SLSA v1.0 specification page inspected for the SCF external-positioning queue; no SLSA workflow, provenance attestation, or build-level verification implemented in this repository. |

## Thesis

SLSA is an external comparator for artifact integrity and provenance in software supply chains. It helps position SCF qualification evidence and artifact identity against an established provenance discipline, while SCF remains broader: a governed capability field includes semantic identity, authority ceilings, route validity, evaluator policy, lifecycle state, and rollback obligations.

## Mechanisms

- Define supply-chain levels around build and provenance guarantees.
- Treat provenance and artifact identity as security-relevant evidence.
- Separate source, build, dependency, and package integrity concerns.
- Make promotion depend on verifiable artifact and process metadata rather than names alone.

## Evidence

- The source is an official specification for software supply-chain assurance.
- This repository has not implemented SLSA provenance, build attestation, dependency verification, or release-level SLSA compliance for SCF artifacts.
- Use it as a provenance and artifact-integrity comparator, not as a support-state promotion.

## Failure Modes

- Provenance can be mistaken for capability adequacy.
- Artifact integrity does not prove semantic field identity, evaluator independence, or runtime behavior.
- A build process can be well-attested while the replacement still changes authority or loses rollback.
- Compliance language can overrun the actual local evidence.

## Book Chapters Supported

- `stable-capability-fields` (Stable Capability Fields)

## Claims To Add Or Update

- Use SLSA to ground the need for artifact identity and provenance before replacement or default-route promotion.
- Keep SCF qualification evidence separate from SLSA compliance unless a future workflow actually implements and verifies it.
- Do not claim supply-chain conformance, provenance completeness, or safe route promotion.

## Open Questions

- Should future SCF fixtures include provenance-attestation refs separately from field-qualification refs?
- What minimum public-safe provenance record is needed before an implementation can become an SCF canary route?
- How should provenance failures feed rollback, quarantine, or requalification states?
