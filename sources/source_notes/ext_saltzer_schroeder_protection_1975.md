# Source Note: The Protection of Information in Computer Systems

| Field | Value |
|---|---|
| Source ID | `ext_saltzer_schroeder_protection_1975` |
| Source title | The Protection of Information in Computer Systems |
| Ingestion date | 2026-06-29 |
| Source version / URL | MIT-hosted paper page, https://web.mit.edu/Saltzer/www/publications/protection/ |
| Citation label | Saltzer and Schroeder (1975), The Protection of Information in Computer Systems |
| Published / updated | 1975 / 1975 |
| DOI | 10.1109/PROC.1975.9939 |
| Ingestion basis | MIT-hosted paper page and DOI metadata inspected for the security-principles grounding queue; paper not vendored into this repository and no implementation or formal security model imported. |

## Thesis

This classic source gives the security-kernel chapter a durable security-principles baseline. Least privilege, complete mediation, fail-safe defaults, and related principles map cleanly to handle leases, Digital SCIF admission, secret substitution boundaries, and authority-use receipts.

## Mechanisms

- Prefer least privilege over broad authority.
- Mediate access completely rather than checking only at initial admission.
- Use fail-safe defaults and separation of privilege where relevant.
- Keep mechanisms simple and open enough to evaluate.

## Evidence

- The source contributes foundational security-design principles.
- This repository has not formalized those principles, implemented a security kernel, or audited ASI Stack mechanisms against them.
- Use it as external grounding for design comparison, not as proof of security.

## Failure Modes

- Name-checking least privilege while granting broad model-visible context.
- Checking authority once and then letting downstream tools reuse it indefinitely.
- Treating a handle label as complete mediation without enforcement and receipts.

## Book Chapters Supported

- `security-kernel-and-digital-scifs` (Security Kernel and Digital SCIFs)
- `system-boundaries-and-authority` (System Boundaries and Authority)

## Claims To Add Or Update

- Use this note to ground least-privilege, complete-mediation, and fail-safe-default language in the security-kernel chapter.
- Keep support state at `argument` until receipt validation, isolation tests, threat models, or formal security work justify narrower claims.
- Do not claim that Digital SCIFs implement the Saltzer-Schroeder principles completely.

## Open Questions

- Which classic protection principles should become explicit validator checks for authority receipts?
- How should complete mediation be represented for model/tool/context boundaries?
- What side channels remain out of scope for the current security-kernel fixture set?
