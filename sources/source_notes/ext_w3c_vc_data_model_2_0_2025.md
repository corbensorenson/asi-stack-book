# Source Note: Verifiable Credentials Data Model v2.0

| Field | Value |
|---|---|
| Source ID | `ext_w3c_vc_data_model_2_0_2025` |
| Source title | Verifiable Credentials Data Model v2.0 |
| Ingestion date | 2026-07-10 |
| Source version / URL | W3C Recommendation, 15 May 2025, https://www.w3.org/TR/vc-data-model/ |
| Citation label | W3C (2025), Verifiable Credentials Data Model v2.0 |
| Published / updated | 2025-05-15 / 2025-05-15 |
| Ingestion basis | W3C Recommendation inspected for issuer/holder/verifier roles, credential and presentation fields, validity/status, evidence, securing mechanisms, related-resource integrity, refresh, and its authorization boundary. No ASI Stack credential, verifier, issuance, status, or authorization flow ran. |

## Thesis

Verifiable Credentials provide a structured way to express claims about a
subject, bind them to an issuer and securing mechanism, and present them to a
verifier with validity, status, and evidence context. The data model expressly
does not supply a complete authorization framework.

## Mechanisms

- Model credentials and presentations with issuer, subject, identifier,
  validity, status, schema, terms, evidence, and securing-mechanism fields.
- Distinguish issuer, holder, verifier, and credential-repository expectations.
- Bind related resources to stated integrity information where the applicable
  verifier checks the retrieved digest.
- Support credential refresh and status handling while preserving a separate
  authorization-layer decision.

## Evidence

- The recommendation specifies the stated data model and verifier requirements
  for conforming documents and securing mechanisms.
- It explicitly states that authorization requires an accompanying framework.
- This repository has not issued, held, presented, verified, refreshed, revoked,
  or authorized a credential.

## Failure Modes

- Treating a valid credential or issuer signature as a complete authorization
  decision for a high-impact action.
- Reusing a credential outside its audience, purpose, validity, status, or
  local policy scope.
- Treating a credential claim as proof that a remote task, artifact, payment, or
  effect is correct.
- Ignoring issuer trust, subject binding, disclosure, correlation, and revocation
  decisions that the data model leaves to the surrounding system.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange` (Inter-Stack Protocols, Identity, and Economic Exchange)

## Claims To Add Or Update

- Use VC Data Model v2.0 as a comparator for scoped identity and credential
  evidence, status, validity, issuer/holder/verifier roles, and resource
  integrity references.
- Keep credential verification separate from policy authorization, delegation,
  task truth, payment settlement, and safety decisions.
- Do not claim local credential issuance, verification, authorization,
  revocation, privacy, or safety.

## Open Questions

- What audience, purpose, capability, budget, and action-binding fields must a
  governed delegation record add beyond a credential presentation?
- Which credential-status failure modes should route a cross-stack request to
  repair, review, or quarantine?
