# Source Note: NIST SP 800-61 Rev. 3

| Field | Value |
|---|---|
| Source ID | `ext_nist_incident_response_2025` |
| Source title | Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile |
| Ingestion date | 2026-07-19 |
| Source version / URL | Final NIST SP 800-61 Rev. 3, https://csrc.nist.gov/pubs/sp/800/61/r3/final |
| Citation label | Nelson et al. (2025), NIST SP 800-61 Rev. 3 |
| Published / updated | 2025-04-03 / 2025-04-03 |
| DOI | 10.6028/NIST.SP.800-61r3 |
| Ingestion basis | Official final publication page, abstract, revision notice, and NIST incident-response lifecycle explanation inspected; no compliance assessment, exercise, or local response implementation performed. |

## Thesis

Incident response should be integrated into organization-wide cybersecurity
risk management rather than isolated as an emergency procedure. Preparation
spans Govern, Identify, and Protect; incident handling emphasizes Detect,
Respond, and Recover; lessons continuously feed improvement.

## Mechanisms

- Establish incident-response roles, resources, communications, and preparation.
- Detect and analyze events using risk-appropriate information and coordination.
- Respond through prioritized containment and accountable action.
- Recover services and feed lessons into continuing risk management.
- Use external implementation resources because one static guide cannot encode
  every technology, environment, or organization.

## Evidence

This is an official general incident-response baseline. It supports lifecycle
and role design but does not prove response effectiveness, AI-specific monitor
coverage, safe degradation, or recovery in this project.

## Failure Modes

- Treating response as a late operational add-on instead of a prepared capacity.
- Missing roles, communications, evidence, or recovery criteria.
- Failing to connect incident lessons to governance and system improvement.
- Applying generic cybersecurity guidance without AI model, data, evaluator,
  human-feedback, or learning-state adaptations.

## Book Chapters Supported

- `governed-operations-incident-command-and-graceful-degradation`
- `safety-cases-and-structured-assurance`
- `artifact-graphs-audit-logs-and-replay`

## Claims To Add Or Update

- Use Detect/Respond/Recover and continuous improvement as the generic baseline.
- Add AI-specific model, policy, data, evaluator, dependency, human-impact, and
  full-state recovery extensions rather than relabeling ordinary incident response.
- Require independent restoration checks before incident closure.

## Open Questions

- Which AI failures require new incident classes or command roles?
- How should model/policy rollback interact with service recovery?
- What evidence proves that a degraded mode remains both useful and safe?
