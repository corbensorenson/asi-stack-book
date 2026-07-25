# Source Note: Flexible Hardware-Enabled Guarantees for AI Compute

| Field | Value |
|---|---|
| Source ID | `ext_flexible_hardware_enabled_guarantees_2025` |
| Source title | Flexible Hardware-Enabled Guarantees for AI Compute |
| Source version / URL | <https://arxiv.org/abs/2506.15093> |
| Ingestion date | 2026-07-24 |

## Thesis

The report proposes an auditable guarantee processor and tamper-resistant
enclosure that can verify or enforce updateable claims about accelerator use
while limiting disclosure of sensitive workloads.

## Mechanisms

- hardware-rooted measurement and enforcement;
- updateable policies interpreted by a constrained guarantee processor;
- attestation of device identity, configuration, and policy state;
- privacy-preserving reporting of bounded compute claims;
- tamper evidence and controlled update authority.

## Evidence

This is a design proposal, not a deployed universal guarantee. Its security
depends on hardware, firmware, manufacturing, attestation roots, update
authority, deployment coverage, and operational governance.

## Failure Modes

- compromised roots, firmware, supply chain, or update keys;
- legacy and uninstrumented accelerators outside coverage;
- side channels and workload migration;
- policy updates expanding authority or weakening guarantees;
- attestation used for surveillance or coercion;
- technically valid reports attached to illegitimate governance.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust`
- `physical-compute-infrastructure-energy-and-environmental-constraints`
- `institutions-international-coordination-and-public-legitimacy`

## Claims To Add Or Update

- Hardware-enabled guarantees need an explicit root-of-trust, measurement,
  policy-update, coverage, privacy, revocation, and institutional-authority
  contract.
- Attestation establishes only the measured claim under that trust chain, not
  safe or legitimate compute use.

## Open Questions

- How can guarantees cover heterogeneous and legacy accelerators?
- Who may update policies, and how are abusive updates contested?
- Which side channels and off-device dependencies remain outside the envelope?
