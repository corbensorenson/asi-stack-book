# Source Note: OWASP Top 10 for LLMs and Gen AI Apps

| Field | Value |
|---|---|
| Source ID | `ext_owasp_llm_top_10_2025` |
| Source title | OWASP Top 10 for LLMs and Gen AI Apps |
| Ingestion date | 2026-06-29 |
| Source version / URL | OWASP GenAI Security Project page, https://genai.owasp.org/llm-top-10/ |
| Citation label | OWASP GenAI Security Project (2025), OWASP Top 10 for LLMs and Gen AI Apps |
| Published / updated | 2025 / 2025 |
| DOI | none recorded |
| Ingestion basis | Official OWASP GenAI project page and prompt-injection risk page inspected for the AI-security grounding queue; guidance not vendored into this repository and no security assessment or penetration test performed. |

## Thesis

This source gives the security-kernel chapter an external AI-application security baseline. It grounds prompt injection, sensitive information disclosure, and excessive agency as recognized LLM/GenAI risks, which maps directly to the book's claim that privileged context and action authority should not be exposed as ordinary model-visible text.

## Mechanisms

- Treat prompt injection as a first-class LLM application risk.
- Treat sensitive information disclosure as a risk created by model-visible data and application behavior.
- Treat excessive agency as a security risk when systems can take actions, use tools, or reach external systems.
- Motivate explicit authorization, least exposure, tool/action mediation, output filtering, and audit boundaries around LLM applications.

## Evidence

- The source contributes public security taxonomy and mitigation framing for GenAI systems.
- This repository has not performed an OWASP-style assessment, penetration test, red-team exercise, or control mapping.
- Use it as external security grounding for threat vocabulary and non-claim boundaries, not as evidence that the ASI Stack satisfies OWASP guidance.

## Failure Modes

- Treating prompt-level warnings as enough to contain prompt injection.
- Letting a model see secrets or privileged context when a handle-mediated action boundary would be narrower.
- Equating awareness of OWASP risks with implemented controls or tested containment.

## Book Chapters Supported

- `security-kernel-and-digital-scifs` (Security Kernel and Digital SCIFs)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use this note to replace the security-kernel chapter's external-baseline exception with an AI-security comparator.
- Keep support state at `argument` until threat models, runtime containment tests, security reviews, or accepted evidence transitions exist.
- Do not claim OWASP conformance, control coverage, or prompt-injection containment.

## Open Questions

- Which OWASP LLM risks should become explicit fields on security receipts or SCIF commit records?
- What prompt-injection fixture would be strong enough to test non-disclosure of secret handles?
- How should agentic workflow injection and artifact-steward risks share the same event-taint model?
