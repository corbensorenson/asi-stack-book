# Source Note: NIST Post-Quantum Cryptography Standards

| Field | Value |
|---|---|
| Source ID | `ext_nist_pqc_standards_2024` |
| Source title | Approval of FIPS 203, FIPS 204, and FIPS 205 for Post-Quantum Cryptography |
| Author / date | National Institute of Standards and Technology; 2024 |
| Primary URL | https://www.nist.gov/news-events/news/2024/08/announcing-approval-three-federal-information-processing-standards-fips |
| Source type | official standards announcement and standards family |
| Evidence boundary | Authoritative identity and intended use of the approved standards; not proof that migration or any implementation is secure. |

## Thesis

NIST approved ML-KEM for key establishment and ML-DSA and SLH-DSA for digital
signatures. The book's durable artifacts, attestations, model custody, releases,
and long-lived audit chains therefore need cryptographic inventory and
algorithm agility rather than silently assuming today's signatures remain
adequate for every retention horizon.

## Failure Modes

- Standardization does not validate a specific library, parameter choice,
  protocol composition, side-channel posture, key lifecycle, or migration.
- Hybrid migration, rollback, interoperability, artifact re-signing, and
  historical verification need explicit policies.
- Post-quantum cryptography does not make the underlying AI safe or correct.

## Book Chapters Supported

- `security-kernel-and-digital-scifs`: crypto inventory and agility.
- `model-weight-custody-and-hardware-roots-of-trust`: long-lived model and
  attestation signatures.
- `ai-supply-chain-integrity-and-lifecycle-provenance`: provenance migration
  without historical erasure.

## Mechanisms

ML-KEM supplies a standardized key-establishment primitive, while ML-DSA and
SLH-DSA supply standardized signature families. Migration requires an
inventory of every signed or encrypted artifact, algorithm identifiers,
dual-verification periods, key rotation, and downgrade-resistant policy.

## Evidence

The NIST approval is authoritative evidence that these federal standards
exist and are intended for deployment. It does not validate any particular
implementation or the book's proposed migration procedure.

## Claims To Add Or Update

- Long-lived AI custody and assurance records need cryptographic agility and a
  prospective post-quantum migration plan.
- Historical attestations must remain verifiable across migration without
  permitting silent re-signing or provenance rewriting.

## Open Questions

- Which artifacts need hybrid signatures during the transition?
- How should revoked, retired, or cryptographically obsolete attestations be
  represented without erasing their historical state?
