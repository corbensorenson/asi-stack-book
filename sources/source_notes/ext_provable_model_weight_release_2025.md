# Source Note: Towards Provable (In)Secure Model Weight Release Schemes

| Field | Value |
|---|---|
| Source ID | `ext_provable_model_weight_release_2025` |
| Source title | Towards Provable (In)Secure Model Weight Release Schemes |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:2506.19874, https://arxiv.org/abs/2506.19874 |
| Citation label | Yang et al. (2025), Provable (In)Secure Model Weight Release Schemes |
| Published / updated | 2025-06-23 / 2025-06-23 |
| DOI | 10.48550/arXiv.2506.19874 |
| Ingestion basis | Primary arXiv abstract inspected for its formal-security framing of model-weight release schemes, informal-guarantee critique, and parameter-extraction case study. No release scheme, extraction test, or open-weight release was run in this repository. |

## Thesis

Claims that a model-weight release scheme protects ownership or prevents misuse
need explicit security definitions and adversarial analysis. The paper shows a
case in which a prominent scheme failed its informal goals through parameter
extraction, so a security label or release mechanism is not sufficient evidence
of its desired property.

## Mechanisms

- Specify concrete security properties and attacker capabilities for any claimed
  protected weight-release mechanism.
- Evaluate a scheme against extraction and other adversarial paths rather than
  relying on informal descriptions of what a release restriction should do.
- Separate release purpose, distribution scope, recovery/rollback limits, and
  security claim from a mechanism's name or implementation convenience.
- Treat broadly distributed weight release as a distinct, potentially
  irreversible custody transition rather than an ordinary deployment event.

## Evidence

- The paper defines a formal-security research problem and reports a case study
  vulnerability for its named scheme.
- It does not establish that all release schemes fail or that any particular
  release policy is correct.
- This repository has not designed, released, extracted, tested, or audited a
  weight-release scheme. The source is a formal-critique comparator only.

## Failure Modes

- Informal security language hides an attacker model, extraction path, or
  untested assumption.
- A restricted, encrypted, or mediated release is treated as reversible when
  recipients can extract, copy, or redistribute the effective artifact.
- A custody decision is made from commercial convenience or a generic openness
  label without scope, recipient, policy, residual, and incident records.
- A vulnerability in one scheme is generalized into a blanket conclusion about
  all open-weight releases.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust` (Model-Weight Custody and Hardware Roots of Trust)

## Claims To Add Or Update

- Use this note for explicit adversary, security-property, extraction, and
  irreversibility vocabulary in release decisions.
- Treat open-weight release as a custody transition with a separate authority,
  residual, and no-rollback boundary.
- Do not claim a local release mechanism, extraction resistance, secure open
  weights, correct release policy, safety, or ASI.

## Open Questions

- Which properties can an ASI Stack custody record state without pretending to
  prove the security of a release mechanism?
- How should recipient scope, derivative copies, revocation infeasibility, and
  rediscovery risk be recorded as release residuals?
- What independent adversarial testing would be needed before a narrower
  protected-release claim could be considered?
