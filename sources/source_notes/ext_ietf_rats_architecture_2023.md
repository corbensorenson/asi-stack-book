# Source Note: Remote ATtestation procedureS (RATS) Architecture

| Field | Value |
|---|---|
| Source ID | `ext_ietf_rats_architecture_2023` |
| Source title | Remote ATtestation procedureS (RATS) Architecture |
| Ingestion date | 2026-07-14 |
| Source version / URL | RFC 9334, January 2023, https://www.rfc-editor.org/rfc/rfc9334.html |
| Citation label | Birkholz et al. (2023), RATS Architecture |
| Published / updated | 2023-01 / 2023-01 |
| DOI | 10.17487/RFC9334 |
| Ingestion basis | Primary RFC reviewed for architecture, roles, evidence/result separation, appraisal policies, reference values, freshness, layered attestation, confidential-model key release, privacy, and security considerations. It is an informational architecture rather than a protocol or implementation; no local attestation was run. |

## Thesis

Remote attestation separates an Attester that produces Evidence, a Verifier that
appraises Evidence against reference values and policy, and a Relying Party that
uses an Attestation Result under its own policy. Trust is a relying-party
decision; an attestation result is not a universal fact that a device, workload,
vendor, model, or release is trustworthy.

## Mechanisms

- Bind Attester, Target Environment, Attesting Environment, Evidence, Verifier,
  Reference Value Provider, Endorser, Relying Party, and policy-owner roles.
- Separate Evidence from Attestation Results and separate the Verifier's
  appraisal policy from the Relying Party's policy for using the result.
- Bind freshness through a stated timestamp, nonce, or epoch mechanism rather
  than treating a signed but replayable token as current.
- Model layered and composite attestation environments, reference values, trust
  anchors, endorsements, verifier dependencies, and strength of function.
- Treat confidential-model or key release as one relying-party action after
  appraisal, not as an automatic consequence of an attestation token.
- Protect sensitive Evidence and preserve the privacy costs of revealing device,
  firmware, software, configuration, or user state.

## Evidence

- RFC 9334 is an IETF-consensus informational architecture and terminology
  document with an explicit confidential-machine-learning-model use case.
- It supplies role, evidence, policy, freshness, composition, privacy, and trust
  vocabulary; it does not specify a complete wire protocol or implementation.
- The book did not produce Evidence, appraise it, generate an Attestation Result,
  implement a Relying Party, or assess any root of trust.

## Failure Modes

- Collapsing Attester, Verifier, Relying Party, endorser, reference-value, and
  policy-owner roles into one self-ratifying system.
- Treating Evidence, a verifier result, and a relying-party authorization as the
  same proposition.
- Replaying stale evidence or ignoring changes in artifact, firmware, workload,
  policy, reference values, trust anchors, recipient, or requested use.
- Ignoring composite/layered environments, shared roots, verifier compromise,
  attestation-key provisioning, sensitive evidence, or privacy leakage.
- Treating informational architecture as a security protocol, assurance level,
  conformance result, or proof of hardware trustworthiness.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust`

## Claims To Add Or Update

- Give attester evidence, verifier appraisal, attestation result, and
  relying-party key/load decision separate identities, policies, owners, expiry,
  and consequences.
- Bind freshness, reference values, endorsements, trust anchors, target and
  attesting environments, and privacy residuals into custody decisions.
- Do not claim that attestation truth, verifier independence, root strength,
  weight confidentiality, safe loading, or release authority follows from the
  architecture.

## Open Questions

- Which attestation topology and freshness mechanism best fits a public-safe
  mock weight-load campaign?
- How should verifier, endorser, reference-value, vendor, and policy-owner
  dependencies be represented and ablated?
- Which attestation evidence is too sensitive to publish while still allowing
  an independently checkable custody receipt?

## Non-claims

- No attestation protocol, root of trust, verifier, key release, confidential
  model, conformance, security, or deployment result is established.
- The RFC does not make an Attestation Result equivalent to trustworthy hardware,
  uncompromised software, correct policy, safe model behavior, or release merit.
