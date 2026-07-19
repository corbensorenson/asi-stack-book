# Source Note: Challenges to the Monitoring of Deployed AI Systems

| Field | Value |
|---|---|
| Source ID | `ext_nist_deployed_ai_monitoring_2026` |
| Source title | Challenges to the Monitoring of Deployed AI Systems |
| Ingestion date | 2026-07-19 |
| Source version / URL | NIST AI 800-4, https://doi.org/10.6028/NIST.AI.800-4 |
| Citation label | Rao et al. (2026), Challenges to the Monitoring of Deployed AI Systems |
| Published / updated | 2026-03-06 / 2026-03-18 |
| DOI | 10.6028/NIST.AI.800-4 |
| Ingestion basis | Official NIST publication page, report abstract, monitoring taxonomy, and highlighted gaps inspected; no compliance mapping or monitoring implementation performed. |

## Thesis

Pre-deployment evaluation cannot substitute for monitoring behavior and impact
under real deployment conditions. NIST AI 800-4 organizes a fragmented field
into monitoring categories while emphasizing that validated methods, common
terminology, and human-AI feedback-loop evidence remain immature.

## Mechanisms

- Distinguish functionality, operations, inputs, outputs, impacts, and security
  monitoring.
- Choose monitoring subject, cadence, method, and accountable actor by context.
- Combine automated signals, human validation, field study, and incident data.
- Preserve visibility across distributed infrastructure and changing policy.

## Evidence

The report synthesizes practitioner workshops and literature. It maps gaps and
questions; it is not a validated incident-response blueprint or evidence that
the ASI Stack monitors deployed systems effectively.

## Failure Modes

- Controlled evaluations miss dynamic inputs and real-world consequences.
- Fragmented logging prevents end-to-end diagnosis.
- Monitoring burden overwhelms users or reviewers.
- Drift, deceptive behavior, and human-AI feedback loops remain hard to detect.
- Monitoring data can be collected without actionable incident authority.

## Book Chapters Supported

- Proposed: `governed-operations-incident-command-and-graceful-degradation`
- Existing boundary owners: `readiness-gates-residual-escrow-and-quarantine`,
  `safety-cases-and-structured-assurance`, `artifact-graphs-audit-logs-and-replay`

## Claims To Add Or Update

- Separate release readiness from field observability and incident command.
- Require service, model, policy, dependency, and human-impact signals plus
  explicit trigger, owner, containment, recovery, and disclosure routes.
- Treat missing or fragmented telemetry as an operational residual.

## Open Questions

- Which signals trigger degrade, contain, roll back, or decommission actions?
- How can monitor quality be evaluated without waiting for severe incidents?
- What evidence is required before declaring recovery complete?
