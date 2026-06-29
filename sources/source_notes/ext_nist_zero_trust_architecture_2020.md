# Source Note: Zero Trust Architecture

| Field | Value |
|---|---|
| Source ID | `ext_nist_zero_trust_architecture_2020` |
| Source title | Zero Trust Architecture |
| Ingestion date | 2026-06-29 |
| Source version / URL | NIST SP 800-207 DOI, https://doi.org/10.6028/NIST.SP.800-207 |
| Citation label | Rose et al. (2020), Zero Trust Architecture |
| Published / updated | 2020-08-11 / 2020-08-11 |
| DOI | 10.6028/NIST.SP.800-207 |
| Ingestion basis | Primary NIST DOI/official PDF landing inspected for the security-governance grounding queue; publication not vendored into this repository and no zero-trust architecture assessment performed. |

## Thesis

This source grounds the security-kernel chapter against an official zero-trust architecture baseline. It supports the book's move from ambient trust to mediated access: every privileged action should be scoped, evaluated, enforced, and recorded rather than assumed safe because it occurs inside a trusted application boundary.

## Mechanisms

- Treat resources as individually protected rather than relying on broad perimeter trust.
- Use policy decision and enforcement points to mediate access.
- Prefer least-privilege and session-scoped authorization.
- Support continuous evaluation of identity, device, policy, and resource access context.

## Evidence

- The source contributes official architecture vocabulary for zero-trust access mediation.
- This repository has not performed a NIST zero-trust mapping, implementation, compliance audit, or control assessment.
- Use it as external grounding for access-boundary structure, not as evidence that the ASI Stack implements zero trust.

## Failure Modes

- Treating an AI agent, model, or runtime as implicitly trusted after one approval.
- Letting a handle, SCIF clearance, or runtime adapter permission become ambient authority.
- Claiming zero-trust conformance without resource, policy, enforcement, and monitoring artifacts.

## Book Chapters Supported

- `security-kernel-and-digital-scifs` (Security Kernel and Digital SCIFs)
- `system-boundaries-and-authority` (System Boundaries and Authority)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)

## Claims To Add Or Update

- Use this note to compare handle leases, authority receipts, and Digital SCIF admission against zero-trust access-mediation principles.
- Keep support state at `argument` until implementation or review artifacts evaluate actual access-control behavior.
- Do not claim NIST zero-trust compliance or certification.

## Open Questions

- Which Authority Use Receipt fields correspond to policy decision and enforcement points?
- How should continuous evaluation work for long-running AI jobs and self-improvement transitions?
- What minimum fixture would show that stale or scope-widened handle reuse is blocked?
