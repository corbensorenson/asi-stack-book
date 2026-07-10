# Source Note: OWASP Top 10 for Agentic Applications for 2026

| Field | Value |
|---|---|
| Source ID | `ext_owasp_agentic_top_10_2026` |
| Source title | OWASP Top 10 for Agentic Applications for 2026 |
| Ingestion date | 2026-07-10 |
| Source version / URL | Official guidance, https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| Citation label | OWASP (2025), Top 10 for Agentic Applications for 2026 |
| Published / updated | 2025-12-09 / 2026-07-10 |
| Ingestion basis | Metadata-first intake from the OWASP public guidance and repository inventory; this is a risk-taxonomy comparator, not a local security assessment. |

## Thesis

The OWASP agentic-applications list is a comparator for threat categories including goal hijacking, tool misuse, identity abuse, supply-chain risk, code execution, memory poisoning, inter-agent communication, cascading failures, human trust exploitation, and rogue agents.

## Mechanisms

- The inventory records a community risk taxonomy spanning agent inputs, tools, identity, memory, supply chain, and multi-agent interaction.
- It is routed to boundaries, the security kernel, supply chain, runtime effects, inter-stack exchange, and adversarial evaluation.

## Evidence

- A risk list is not proof of completeness, control effectiveness, local testing, or safety.
- No local OWASP assessment or control validation was performed in this increment.

## Failure Modes

- Treating taxonomy coverage as threat-model completeness.
- Treating named risks as evidence that a local control detects or mitigates them.

## Book Chapters Supported

- `system-boundaries-and-authority`
- `security-kernel-and-digital-scifs`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `runtime-adapters-tool-permissions-and-human-approval`
- `inter-stack-protocols-identity-and-economic-exchange`
- `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Use as a threat-taxonomy comparator and route each claimed mitigation to a testable local owner.

## Open Questions

- Which taxonomy items need distinct fixtures rather than being merged into a generic prompt-injection control?
