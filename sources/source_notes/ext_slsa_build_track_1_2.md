# Source Note: SLSA Build Track Basics v1.2

| Field | Value |
|---|---|
| Source ID | `ext_slsa_build_track_1_2` |
| Source title | SLSA Build Track Basics, version 1.2 |
| Ingestion date | 2026-07-10 |
| Source version / URL | SLSA Build Track v1.2, https://slsa.dev/spec/v1.2/build-track-basics |
| Citation label | SLSA (2025), Build Track Basics v1.2 |
| Published / updated | 2025 / 2026-07-10 |
| Ingestion basis | Official specification inspected for its graduated build-provenance requirements, signed hosted-build framing, verification benefits, and explicit lower-level limits. No ASI Stack build platform, provenance attestation, signature, rebuild, or verification workflow ran. |

## Thesis

Build provenance can describe how a package was built and, at stronger levels,
make forgery or verification evasion more difficult. The assurance is graduated:
the existence of provenance can be incomplete or forgeable, and build provenance
does not establish the correctness, safety, fitness, or permitted use of an
artifact.

## Mechanisms

- Record the builder, build process, and top-level inputs that produced an
  artifact.
- Distribute provenance so consumers can inspect the stated source version and
  build process and verify it against a declared policy.
- Use hosted and signed build mechanisms for stronger resistance to tampering
  after a build, while preserving scope and threat assumptions.
- Treat level labels as bounded assurance claims with explicit requirements,
  rather than as generic proof that a package is safe.

## Evidence

- The specification describes graduated build-provenance requirements and their
  stated security benefits and limits.
- It addresses software build provenance, not a complete AI training-data,
  weight-custody, model-behavior, or release-governance system.
- This repository has not produced, signed, verified, or audited a SLSA
  provenance statement or reproduced a build under its requirements.

## Failure Modes

- A provenance record is present but incomplete, unsigned, stale, mis-bound, or
  not verified against the correct policy.
- A build guarantee is stretched to cover training data, model behavior, runtime
  security, legal compliance, or deployment approval.
- A trusted build process produces an artifact from unsuitable or compromised
  inputs that provenance merely records.
- A higher-level label is asserted without the scoped platform and verification
  conditions that the specification requires.

## Book Chapters Supported

- `ai-supply-chain-integrity-and-lifecycle-provenance` (AI Supply-Chain Integrity and Lifecycle Provenance)

## Claims To Add Or Update

- Use this note for build provenance, builder, process, inputs, signing,
  verification, and graduated-assurance vocabulary.
- Keep provenance verification separate from artifact correctness, data fitness,
  model safety, readiness, authority, and ASI.
- Do not claim a local SLSA level, provenance statement, secure build platform,
  reproducible build, or verified artifact.

## Open Questions

- How should training and fine-tuning runs extend a build-provenance record
  without claiming reproducibility or data quality from metadata alone?
- Which policy changes should invalidate an earlier provenance verification?
- What public-safe fixture could distinguish unsigned, stale, mismatched, and
  verified provenance without handling a real model or private build input?
