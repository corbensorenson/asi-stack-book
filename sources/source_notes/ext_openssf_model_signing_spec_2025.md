# Source Note: OpenSSF Model Signing Specification

| Field | Value |
|---|---|
| Source ID | `ext_openssf_model_signing_spec_2025` |
| Source title | OpenSSF Model Signing Specification |
| Ingestion date | 2026-07-10 |
| Source version / URL | OpenSSF AI/ML Security Working Group specification, https://github.com/ossf/model-signing-spec |
| Citation label | OpenSSF (2025), Model Signing Specification |
| Published / updated | 2025 / 2026-07-10 |
| Ingestion basis | Official specification repository inspected for detached signed bundles, artifact hashes, provenance metadata, test-vector scope, lifecycle verification points, and explicit statements of what signing does not establish. No local signer, verifier, model, dataset, signature, key, or transparency service ran. |

## Thesis

Model signing can make a signed model or dataset bundle tamper-evident and can
bind provenance metadata to a named artifact set. It is a narrowly scoped
integrity and authenticity mechanism, not proof of model quality, safety,
fairness, confidentiality, secure development, appropriate access, or permitted
use.

## Mechanisms

- Represent model-related artifacts as a signed bundle containing hashes and
  optional metadata, using a detached signature format.
- Verify a signature at lifecycle points such as upload, selection for
  deployment, and use as an input to another model.
- Bind model weights, configuration, tokenizers, datasets, and related files
  into a verifiable unit rather than treating a model file in isolation.
- Preserve the distinction between a signature's integrity/authenticity scope
  and broader security, privacy, access-control, or behavior claims.

## Evidence

- The specification defines an AI-artifact signing format, metadata envelope,
  and test-vector scope, with explicit non-guarantees.
- It is a specification and reference framing, not independent efficacy
  evidence or a local signing/verification result.
- This repository has not signed, verified, deployed, or audited a model,
  dataset, bundle, signature, signer, verifier, or key service.

## Failure Modes

- A valid signature is read as proof that a model is good, safe, fair, private,
  or fit for a particular deployment.
- A trusted signature covers the wrong artifact set, stale metadata, compromised
  upstream input, or an unauthorized distribution path.
- Signature verification is skipped at a lifecycle transition where an artifact
  is selected, repackaged, or consumed downstream.
- A signing mechanism is treated as a substitute for weight custody, runtime
  authorization, vulnerability management, or release governance.

## Book Chapters Supported

- `ai-supply-chain-integrity-and-lifecycle-provenance` (AI Supply-Chain Integrity and Lifecycle Provenance)

## Claims To Add Or Update

- Use this note for signed model/dataset bundle, hash, provenance metadata,
  verification-point, and explicit non-guarantee vocabulary.
- Keep signature status separate from confidentiality, artifact correctness,
  data fitness, model safety, readiness, authority, and ASI.
- Do not claim local model signing, signature verification, artifact integrity,
  tamper resistance, provenance completeness, or deployment security.

## Open Questions

- Which metadata predicates should a governed AI supply-chain record require
  beyond a valid signature, and who owns verification policy?
- How are revoked signer identities, compromised bundles, derivative models,
  and downstream consumers linked to incident and re-review records?
- What independent tests would be needed before a signing claim could be made
  for a bounded local artifact path?
