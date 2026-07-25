# The 2026 Singapore Consensus on Global AI Safety Research Priorities

## Source identity

- Source ID: `ext_singapore_consensus_2026`
- Publisher: 2026 International Scientific Exchange on AI Safety
- Public source: <https://aisafetypriorities.org/>
- Reviewed: 2026-07-24

## Thesis

The report organizes technical AI-safety research around four coupled pillars:
risk assessment, safer development, control, and societal resilience. It
elevates dangerous-capability and propensity assessment across cyber, chemical,
biological, radiological, nuclear, psychological-manipulation, deception,
autonomy, and AI-R&D domains; it also treats openly released models,
multi-agent monitoring, incident reporting, and defense-favoring capabilities
as first-class research problems.

## Mechanisms and distinctions used by the book

- A threat model must name the actor, access, target, capability, propensity,
  pathway, and consequence rather than treating “dangerous capability” as one
  scalar.
- Capability elicitation and propensity assessment are distinct. A model may
  possess a capability without exercising it under the tested policy, and a
  refusal test can understate capability.
- Open-weight assessment must include malicious fine-tuning and the control
  consequences of unmonitored deployment.
- Societal resilience is not a synonym for model safeguards. It covers
  resistance, detection, incident coordination, recovery, adaptation, and
  defense-favoring infrastructure after prevention is imperfect.
- Agentic systems require identity, authentication, runtime monitoring,
  intervention, multi-agent red teaming, and incident reporting.

## Evidence and limitations

This is a consensus research-priority synthesis produced by more than one
hundred contributors across thirteen countries. It supplies a current taxonomy
and research agenda. It does not demonstrate that a listed safeguard works,
that any threat threshold is calibrated, that the ASI Stack covers every
domain, or that the book's proposed contracts are safe or complete.

## Failure modes surfaced

- stale threat models;
- benchmark capability mistaken for real-world uplift;
- refusal behavior mistaken for capability absence;
- malicious fine-tuning omitted from open-release review;
- model-level safeguards treated as the whole defense;
- incident data and cross-organization response omitted;
- offensive capabilities advancing faster than defensive evaluation;
- autonomous or multi-agent misuse escaping single-session monitoring.

## Chapter routing

- Primary: `dangerous-capability-domains-and-misuse-uplift`
- Primary: `societal-resilience-and-misuse-defense`
- Supporting: `open-weight-release-and-post-release-control`
- Supporting: `capability-thresholds-and-deployment-commitments`

## Open questions

- Which uplift measures remain valid across expertise levels and tool access?
- How can high-hazard evaluations avoid creating reusable operational harm?
- Which societal-resilience interventions transfer across languages,
  jurisdictions, and infrastructure?
- How should defensive benefit and offensive enablement be measured jointly?

