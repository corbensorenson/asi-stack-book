# Source Note: Anthropic's Responsible Scaling Policy

| Field | Value |
|---|---|
| Source ID | `ext_anthropic_rsp_2026` |
| Source title | Anthropic's Responsible Scaling Policy |
| Ingestion date | 2026-07-10 |
| Source version / URL | Version 3.4, effective 2026-07-08, https://www.anthropic.com/responsible-scaling-policy |
| Citation label | Anthropic (2026), Responsible Scaling Policy v3.4 |
| Published / updated | 2023-09-19 / 2026-07-08 |
| Ingestion basis | Official policy page inspected for version history, capability-threshold language, safeguard commitments, risk-report handling, revision process, and the page's stated implementation limitations. No Anthropic model, evaluation, safeguard, policy-compliance review, or reported risk outcome was reproduced in this repository. |

## Thesis

The policy is an organization-specific framework that binds specified capability
thresholds to stronger security and deployment safeguards, versioned risk
reports, and change-control processes. It is useful as a comparator for a
recorded pre-commitment: a capability assessment, threshold definition,
required response, verification obligation, and exception path must remain
linked over time. It is not evidence that the policy's thresholds are complete,
that its safeguards are sufficient, or that its implementation works.

## Mechanisms

- Define versioned capability thresholds and required safeguard standards that
  apply when a threshold is reached.
- Preserve policy versions, revisions, risk-report practices, and reasons for
  threshold or safeguard changes rather than treating a current policy page as
  timeless.
- Associate capability assessments with deployment or security safeguards,
  reporting, and organizational review rather than with model self-attestation.
- Acknowledge uncertainty and revision: threshold definitions, evaluations, and
  safeguards can change, but a change needs an explicit policy and review path.

## Evidence

- The official page describes the policy's own threshold, safeguard, report,
  governance, and revision commitments for its stated versions.
- The page reports policy updates and implementation intentions within that
  organization's framework; those are not independent effectiveness findings.
- This repository has not implemented the policy, evaluated a capability
  threshold, verified a safeguard, inspected a risk report, or audited policy
  compliance. The source is a governance-contract comparator only.

## Failure Modes

- A threshold may be evaluated with incomplete elicitation, stale evidence, or
  an unstated coverage date.
- A later policy revision can retroactively weaken, obscure, or reframe a
  commitment unless version, exception authority, and rationale are preserved.
- A stated safeguard can be mistaken for verified effectiveness or sufficient
  residual-risk reduction.
- A company policy can be treated as a universal deployment standard without
  its threat model, scope, authority, and implementation limits.

## Book Chapters Supported

- `capability-thresholds-and-deployment-commitments` (Capability Thresholds and Deployment Commitments)

## Claims To Add Or Update

- Use this note for threshold-to-safeguard pre-commitment, versioning, coverage
  date, exception, verification, and reassessment vocabulary.
- Keep threshold evidence, safeguard completion, residual-risk review, release
  authority, and actual deployment effects as separate records.
- Do not claim an ASI Stack threshold is adequate, a safeguard works, policy
  compliance exists, deployment is safe, or ASI has been reached.

## Open Questions

- Which commitment fields must be immutable once a covered evaluation begins,
  and which can change only through a versioned exception route?
- How should a capability threshold record name the threat model and the
  evidence it does not cover?
- What public-safe fixture can block a release request when a crossed threshold
  lacks verified safeguards, an accountable exception, or residual ownership?
