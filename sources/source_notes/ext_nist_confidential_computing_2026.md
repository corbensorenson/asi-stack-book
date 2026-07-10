# Source Note: NIST IR 8320E Confidential Computing Draft

| Field | Value |
|---|---|
| Source ID | `ext_nist_confidential_computing_2026` |
| Source title | Hardware-Enabled Security: Confidential Computing of Data in Cloud Workloads |
| Ingestion date | 2026-07-10 |
| Source version / URL | NIST IR 8320E initial public draft, May 2026, https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8320E.ipd.pdf |
| Citation label | NIST (2026), IR 8320E Initial Public Draft |
| Published / updated | 2026-05 / 2026-05 |
| Ingestion basis | Primary NIST draft inspected for confidential-computing trust-domain, encrypted-memory, hardware-attestation, and key-release framing for AI workloads. It remains draft guidance; no local confidential-computing environment was configured or assessed. |

## Thesis

Hardware-enabled confidential computing can protect AI model and data memory in
use by restricting decryption to authorized code within an attested trust
domain. It is an architectural security layer, not a general proof that the
hardware, vendor, workload, policy, key service, or model is trustworthy.

## Mechanisms

- Use a TEE-capable environment and a stated trust domain for workloads that
  process sensitive model or data material.
- Bind decryption-key release to attestation of the computing environment's
  claimed hardware capabilities and authorized code.
- Keep memory-in-use protection distinct from storage, network, identity,
  key-management, configuration, and operational security controls.
- Treat hardware roots of trust and attestation claims as inputs to a policy
  decision with explicit trust assumptions and residuals.

## Evidence

- The draft describes hardware-enabled mechanisms for encrypted AI model memory
  and attestation-gated key access in cloud workloads.
- It describes an intended security architecture, not a verified deployment
  result for this repository.
- This repository has not run a TEE, generated an attestation, released a key,
  loaded a model weight, or evaluated confidential-computing security.

## Failure Modes

- Treating attestation as proof of all software, firmware, vendor, operator,
  or workload behavior outside its measured scope.
- Releasing a key on stale, unverifiable, mismatched, or policy-incomplete
  attestation evidence.
- Treating encrypted memory as protection for backups, copied weights, output
  exfiltration, authorized misuse, or model behavior.
- Citing a draft standard as final compliance, local conformance, or security
  effectiveness evidence.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust` (Model-Weight Custody and Hardware Roots of Trust)

## Claims To Add Or Update

- Use this note for trust-domain, attestation-gated key release, encrypted
  model-memory, and hardware-root boundary vocabulary.
- Retain the distinction between attestation evidence and verified custody,
  model safety, readiness, or deployment authority.
- Do not claim a local TEE, attestation, root of trust, key-release policy,
  confidential inference result, or compliance result.

## Open Questions

- Which measurement claims must be bound into a custody attestation before a
  weight-decryption key can be considered for release?
- How are vendor trust, firmware updates, revocation, rollback, side channels,
  and compromised operators represented as residuals?
- What independent evidence would show that an attested environment enforced a
  stated custody policy rather than merely presented a token?
