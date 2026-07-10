# Source Note: Defeating Prompt Injections by Design

| Field | Value |
|---|---|
| Source ID | `ext_camel_prompt_injection_2025` |
| Source title | Defeating Prompt Injections by Design |
| Ingestion date | 2026-07-10 |
| Source version / URL | Preprint, https://arxiv.org/abs/2503.18813 |
| Citation label | Debenedetti et al. (2025), Defeating Prompt Injections by Design |
| Published / updated | 2025-03-24 / 2025-06-24 |
| Ingestion basis | Metadata-first intake from the public preprint record and repository inventory; no local policy-extraction or tool-call enforcement implementation was inspected. |

## Thesis

CaMeL is a comparator for separating trusted control flow from untrusted data and enforcing capability policy at tool calls.

## Mechanisms

- The inventory identifies control/data separation and tool-call capability enforcement as the central comparison.
- It is routed to authority boundaries, the security kernel, contracts, and runtime adapters.

## Evidence

- Source-reported AgentDojo results are not local evidence.
- This note does not establish universal injection resistance, correct policy extraction, local implementation, or safe deployment.

## Failure Modes

- Treating a control/data boundary as a proof that every policy was extracted correctly.
- Allowing model interpretation to become the sole authority for external effects.

## Book Chapters Supported

- `system-boundaries-and-authority`
- `security-kernel-and-digital-scifs`
- `intent-to-execution-contracts`
- `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

- Use as an external comparator for keeping untrusted content outside policy and effect authority.

## Open Questions

- What explicit failure fixtures distinguish policy parsing errors from capability-enforcement failures?
