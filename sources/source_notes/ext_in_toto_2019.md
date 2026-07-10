# Source Note: in-toto: Providing farm-to-table guarantees for bits and bytes

| Field | Value |
|---|---|
| Source ID | `ext_in_toto_2019` |
| Source title | in-toto: Providing farm-to-table guarantees for bits and bytes |
| Ingestion date | 2026-07-10 |
| Source version / URL | USENIX Security 2019, https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias |
| Citation label | Torres-Arias et al. (2019), in-toto |
| Published / updated | 2019-08 / 2019-08 |
| Ingestion basis | Metadata-first intake from the public conference record and repository inventory; no local in-toto layout, attestation, or verification run was inspected. |

## Thesis

in-toto is a comparator for cryptographically checking authorized software-supply-chain steps from source through deployment.

## Mechanisms

- The inventory identifies authorized steps and attestations as the relevant supply-chain mechanism.
- It is routed to model-weight custody, lifecycle provenance, and artifact-audit discussions.

## Evidence

- This source note records a bounded comparator only.
- Valid attestations do not establish artifact correctness, uncompromised authorized actors, model safety, data fitness, or deployment merit.

## Failure Modes

- Assuming signed authorized steps are complete or trustworthy in their surrounding environment.
- Treating supply-chain verification as a substitute for model evaluation or governance review.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `artifact-graphs-audit-logs-and-replay`

## Claims To Add Or Update

- Use as a comparator for signed lifecycle controls and preserve the gap between provenance and artifact quality.

## Open Questions

- How should the book distinguish an authorized lineage step from a verified-safe model or data artifact?
