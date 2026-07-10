# Source Note: Decentralized Identifiers (DIDs) v1.0

| Field | Value |
|---|---|
| Source ID | `ext_w3c_did_core_1_0_2022` |
| Source title | Decentralized Identifiers (DIDs) v1.0 |
| Ingestion date | 2026-07-10 |
| Source version / URL | W3C Recommendation, 19 July 2022, https://www.w3.org/TR/did-core/ |
| Citation label | W3C (2022), Decentralized Identifiers v1.0 |
| Published / updated | 2022-07-19 / 2022-07-19 |
| Ingestion basis | W3C Recommendation inspected for DID syntax, common data model, core properties, controller-related metadata, resolution, and privacy considerations. No ASI Stack DID method, resolver, controller, key, or policy route ran. |

## Thesis

DID Core supplies a method-neutral identifier and resolution model for subjects
and controller-associated metadata. It creates a vocabulary for identity and
verification methods, not a decision that a controller is trustworthy or
authorized for a requested action.

## Mechanisms

- Define DID syntax, DID URLs, documents, core properties, and resolution.
- Associate verification methods, service endpoints, and controller-related
  metadata with a resolved document.
- Keep methods independent of any one registry or underlying technology.
- State privacy considerations, including avoiding personal data in public DID
  documents and using scoped identities where appropriate.

## Evidence

- The recommendation defines an identity data model and resolution framework at
  its stated scope.
- It does not establish a universal trust registry, authorization framework,
  correct resolver, secure controller, revocation outcome, or task authority.
- This repository has not issued, resolved, verified, revoked, or audited a DID.

## Failure Modes

- Treating identifier control as authority over an unrelated task, asset, or
  principal's approval.
- Publishing personal, sensitive, or correlation-enabling data in a public
  identifier document.
- Trusting a resolved document or verification method without a scoped issuer,
  policy, audience, freshness, and revocation decision.
- Mistaking DID method interoperability for secure cross-stack execution.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange` (Inter-Stack Protocols, Identity, and Economic Exchange)

## Claims To Add Or Update

- Use DID Core as a comparator for identity, controller, verification-method,
  service-endpoint, resolution, and privacy vocabulary.
- Require a cross-stack record to bind an identity reference to a local policy,
  scope, audience, expiry, and revocation result before it affects authority.
- Do not claim a local decentralized identity, resolver, controller trust,
  authorization, revocation, or safety result.

## Open Questions

- Which identity fields are necessary to distinguish a remote agent, its owner,
  its endpoint, and a delegated principal without creating a correlation trap?
- Which local policy owner evaluates a DID resolution result before dispatch?
