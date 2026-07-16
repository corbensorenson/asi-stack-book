# Source Note: Recommendation for Key Management: Part 1 – General

| Field | Value |
|---|---|
| Source ID | `ext_nist_key_management_2020` |
| Source title | Recommendation for Key Management: Part 1 – General |
| Ingestion date | 2026-07-14 |
| Source version / URL | NIST SP 800-57 Part 1 Rev. 5 final, https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final |
| Citation label | Barker (2020), NIST SP 800-57 Part 1 Rev. 5 |
| Published / updated | 2020-05-04 / official page updated 2025-04-25 |
| DOI | 10.6028/NIST.SP.800-57pt1r5 |
| Ingestion basis | Official final publication page reviewed for key and metadata protection, inventory, access control, authorization, usage periods, compromise, backup, recovery, trust anchors, and policy scope. NIST lists Revision 6 as a 2025 draft; Rev. 5 remains the current final baseline. No local cryptographic key-management system was assessed. |

## Thesis

Weight confidentiality depends on a governed lifecycle for the cryptographic
keys and metadata that protect it. Encryption at rest is not a custody result if
key generation, inventory, access, usage period, backup, recovery, compromise,
revocation, destruction, trust anchors, or policy changes are unowned.

## Mechanisms

- Inventory keys and associated metadata with exact purpose, owner, protection,
  algorithm, state, originator/recipient usage period, and authorized use.
- Protect keys in storage, transit, backup, recovery, use, archival, and
  destruction according to their security function and sensitivity.
- Separate authorization, identity authentication, access control, audit,
  contingency, compromise response, and trust-anchor management.
- Treat generation, activation, rotation, expiry, suspension, revocation,
  compromise, recovery, archival, and destruction as distinct lifecycle events.
- Preserve availability and recovery requirements without widening routine key
  access or hiding emergency authority.

## Evidence

- SP 800-57 Part 1 Rev. 5 is the current final NIST general key-management
  recommendation as of the 2026-07-14 review; Revision 6 is still draft.
- It supplies a stable lifecycle and policy comparator, not a local compliance
  or cryptographic-strength result.
- This repository has no model-weight key inventory, HSM/KMS, rotation,
  compromise, recovery, split-knowledge, archival, or destruction exercise.

## Failure Modes

- Encrypting weights while keys, backups, recovery material, metadata, or trust
  anchors remain broadly accessible or untracked.
- Reusing a key beyond its purpose, scope, recipient, algorithm, usage period, or
  compromise boundary.
- Emergency recovery becomes an unaudited bypass or leaves permanent widened
  access after the incident.
- A revoked key is described as recalling plaintext or recipient copies that no
  longer depend on the key service.
- Treating a final standard, or a passing KMS policy check, as proof of local
  conformance, confidentiality, safe release, or correct cryptography.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust`

## Claims To Add Or Update

- Give every weight-protection key and metadata object a versioned lifecycle,
  usage scope, compromise path, backup/recovery policy, emergency authority,
  and observed terminal state.
- Separate key denial/revocation from artifact recall and from media
  sanitization.
- Measure false denial, recovery success and latency, emergency authority, and
  residual plaintext/copies alongside confidentiality controls.

## Open Questions

- What minimal mock KMS can exercise rotation, stale-key rejection, compromise,
  recovery, and reconciliation without real secrets?
- Which key metadata can be public while preserving operational security?
- How should split knowledge and threshold authority interact with attestation
  verifier and release-authority independence?

## Non-claims

- No key-management implementation, NIST conformance, cryptographic correctness,
  weight confidentiality, recovery reliability, or safe release is established.
- Revocation or destruction of key material does not prove recall or erasure of
  plaintext weights or their derivatives.
