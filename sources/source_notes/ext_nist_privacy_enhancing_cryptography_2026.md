# Source Note: NIST Privacy-Enhancing Cryptography

| Field | Value |
|---|---|
| Source ID | `ext_nist_privacy_enhancing_cryptography_2026` |
| Source title | Privacy-Enhancing Cryptography |
| Author / date | National Institute of Standards and Technology; living project page reviewed 2026-07-25 |
| Primary URL | https://csrc.nist.gov/Projects/pec/fhe |
| Source type | official standards and research program |
| Evidence boundary | Authoritative terminology and standards-program context; not a performance benchmark, security proof for an implementation, or end-to-end privacy result. |

## Thesis

NIST identifies fully homomorphic encryption, secure multiparty computation,
zero-knowledge proofs, private-set intersection, and related techniques as
privacy-enhancing cryptography. The FHE material distinguishes encrypted
evaluation from ordinary encrypted storage and explicitly names
privacy-preserving model development and model querying as AI use cases. It
also emphasizes composition: cryptographic privacy tools can be combined with
differential privacy and other controls because no one primitive covers the
whole information lifecycle.

## Failure Modes

- A primitive's formal definition does not establish correct parameters,
  implementation security, side-channel resistance, availability, or usable
  performance.
- Keeping inputs or model weights hidden does not prove that the function,
  output, purpose, authorization, or downstream use is legitimate.
- FHE, MPC, ZKP, trusted execution, and differential privacy expose different
  trust and leakage surfaces and must not share one generic “private” label.

## Book Chapters Supported

- `confidential-and-verifiable-ai-computation`: primary guarantee-family and
  composition source.
- `privacy-data-rights-and-information-flow-governance`: technical privacy is
  kept separate from purpose limitation and rights.
- `personal-compute-hives-and-federated-edge-intelligence`: collaborative
  computation across distrust boundaries.

## Mechanisms

- Select and compose FHE, MPC, ZK, PSI, differential privacy, or related
  primitives against an explicit adversary, leakage, and lifecycle model.

## Evidence

NIST supplies authoritative terminology and standards-program context. No
construction, performance result, or security claim was reproduced locally.

## Claims To Add Or Update

- Separate each confidentiality, integrity, leakage, and trust guarantee from
  consent, purpose, authorization, and semantic correctness.

## Open Questions

- Which compositions preserve usable AI quality and latency under a complete
  end-to-end leakage and cost boundary?
