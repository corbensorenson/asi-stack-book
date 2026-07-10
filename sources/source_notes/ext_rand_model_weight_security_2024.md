# Source Note: Securing AI Model Weights

| Field | Value |
|---|---|
| Source ID | `ext_rand_model_weight_security_2024` |
| Source title | Securing AI Model Weights: Preventing Theft and Misuse of Frontier Models |
| Ingestion date | 2026-07-10 |
| Source version / URL | RAND research report, 2024, https://www.rand.org/content/dam/rand/pubs/research_reports/RRA2800/RRA2849-1/RAND_RRA2849-1.pdf |
| Citation label | Nevo et al. (2024), Securing AI Model Weights |
| Published / updated | 2024-06-12 / 2024-06-12 |
| Ingestion basis | Primary RAND report inspected for its foundation-model scope, attack-vector taxonomy, security-level framing, defense-in-depth controls, and documented limitations. No model-weight security assessment or control was run in this repository. |

## Thesis

Frontier model weights are a security-critical asset with multiple theft and
misuse paths that require varied technical, operational, physical, and
organizational controls. The report proposes graduated security levels and
emphasizes defense in depth rather than one control or one access boundary.

## Mechanisms

- Classify custody threats across diverse attack vectors rather than assuming
  external network intrusion is the only route to weight loss.
- Apply layered controls to storage, transit, access, credentials, personnel,
  hardware, maintenance, and incident response.
- Match a security posture to a declared adversary and operational context, with
  stronger requirements for more capable or resourced attackers.
- Preserve operational resilience and incident handling instead of treating
  encryption or isolation as an exhaustive defense.

## Evidence

- The report analyzes foundation-model-weight security threats and proposed
  controls at the report's stated scope and date.
- It frames defenses as varied and comprehensive because attack vectors differ.
- This repository has not classified a real adversary, protected model weights,
  performed a penetration test, audited controls, or measured resistance to
  theft or misuse. The report is a security-architecture comparator only.

## Failure Modes

- Treating a storage or network control as adequate against all attacker types.
- Ignoring insiders, credentials, supply chain, physical access, maintenance,
  backups, or deployment copies in a weight-custody story.
- Treating a target security level as a demonstrated property without a scoped
  adversary, control evidence, incident response, and independent assessment.
- Confusing weight secrecy with model safety, authorized use, or release merit.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust` (Model-Weight Custody and Hardware Roots of Trust)

## Claims To Add Or Update

- Use this note for multi-vector threat-model, defense-in-depth, security-level,
  custody, access, and incident-response vocabulary.
- Keep custody assurance separate from runtime authority, model behavior,
  capability, safety, and release desirability.
- Do not claim a local security level, protected weight store, theft resistance,
  confidentiality, or safe deployment.

## Open Questions

- Which custody states and adversary assumptions can be represented publicly
  without revealing exploitable operational detail?
- How should incident, revocation, and backup-copy records propagate through a
  model lineage and release decision?
- Which independently auditable controls would be required before a custody
  claim could move beyond architecture rationale?
