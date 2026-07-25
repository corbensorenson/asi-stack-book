# C2PA Content Credentials Technical Specification 2.3

| Field | Value |
|---|---|
| Source ID | `ext_c2pa_specification_2_3_2025` |

## Source identity

- Source ID: `ext_c2pa_specification_2_3_2025`
- Publisher: Coalition for Content Provenance and Authenticity
- Public source: <https://spec.c2pa.org/specifications/specifications/2.3/index.html>
- Version: 2.3
- Reviewed: 2026-07-24

## Thesis

C2PA defines an interoperable way to bind signed manifests, assertions,
ingredients, actions, and validation information to digital assets. Content
Credentials can preserve a verifiable chain of claims about origin and editing
history when producers, tools, platforms, trust stores, and viewers retain and
validate the credential.

## Mechanisms

- signed manifests and assertions;
- content bindings that associate a manifest with an asset;
- ingredient and action histories;
- signer and trust-chain validation;
- validation status and explicit failure handling;
- update manifests and provenance continuity through transformations.

## Evidence

The specification establishes data structures, algorithms, and validation
semantics. It does not prove that a depicted event happened, that a claim is
truthful, that the signer is the human readers assume, or that platforms will
retain metadata. A valid credential is evidence about a signed claim and
history under a trust policy, not proof of semantic truth. Missing credentials
do not prove synthetic origin, and present credentials do not prove
non-deception.

## Failure Modes

- metadata stripping or unsupported transformations;
- broken ingredient chains;
- compromised signers or trust stores;
- validly signed false claims;
- screenshot, re-encoding, and analog-hole laundering;
- viewer omission or confusing user interfaces;
- trust-list fragmentation;
- credential presence used as a universal authenticity score.

## Book Chapters Supported

- Primary: `content-authenticity-watermarking-and-synthetic-media-integrity`
- Supporting: `ai-supply-chain-integrity-and-lifecycle-provenance`

## Claims To Add Or Update

- Content provenance should preserve signed claims, bindings, ingredients,
  actions, trust policy, validation state, transformations, and explicit
  lineage breaks.
- Credential validity, semantic truth, consent, authorship legitimacy, and
  harmlessness remain separate claims.

## Open Questions

- How should provenance survive lossy and cross-platform transformation?
- How should systems present partial, invalid, or conflicting histories?
- How should provenance, watermark, detector, and contextual evidence combine
  without collapsing into one brittle truth score?
