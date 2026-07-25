# International AI Safety Report 2026

| Field | Value |
|---|---|
| Source ID | `ext_international_ai_safety_report_2026` |

## Source identity

- Source ID: `ext_international_ai_safety_report_2026`
- Public source: <https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026>
- Published: 2026-02-03
- Reviewed: 2026-07-24

## Thesis

The report synthesizes the state of evidence on general-purpose AI
capabilities, misuse, loss of control, systemic risks, safeguards,
open-weight releases, and societal resilience. Its central operational lesson
is that technical safeguards are improving but remain bypassable and
incompletely tested, so risk management must combine threat modeling,
capability evaluation, layered safeguards, monitoring, incident response, and
resilience outside the model boundary.

## Mechanisms

- Cyber and biological/chemical capability assessment must be connected to
  realistic workflows and access conditions, not only knowledge questions.
- Open-weight release has asymmetric control semantics: benefits may diffuse,
  but weights cannot be recalled, safeguards are easier to remove, and use is
  harder to monitor.
- Marginal-risk analysis compares a release with the actual counterfactual
  frontier, but small repeated increments and ecosystem composition remain
  consequential.
- Synthetic-media defenses include provenance, disclosure, detection,
  education, correction, and institutional recovery; none is sufficient alone.
- Societal resilience spans resist, absorb, recover, and adapt functions.

## Evidence

The report is a large international literature synthesis backed by an expert
panel nominated by more than thirty countries and international organizations.
It is valuable for taxonomy, current evidence summaries, and uncertainty. The
underlying studies retain their own limitations; this repository has not
reproduced them. The report does not validate the ASI Stack, establish that an
open release is safe or unsafe, or show that a provenance or resilience system
works in every setting.

## Failure Modes

- safeguards evaluated only against non-adaptive attacks;
- open-release irreversibility omitted from release decisions;
- capability frontier and accessible frontier conflated;
- provenance detection treated as ground truth;
- societal recovery assumed rather than exercised;
- uneven coverage across geography, language, and socioeconomic setting;
- unknown hazards hidden by a closed taxonomy.

## Book Chapters Supported

- `dangerous-capability-domains-and-misuse-uplift`
- `open-weight-release-and-post-release-control`
- `content-authenticity-watermarking-and-synthetic-media-integrity`
- `societal-resilience-and-misuse-defense`

## Claims To Add Or Update

- Frontier-risk governance should join threat modeling, capability and
  safeguard evaluation, access semantics, monitoring, incident response, and
  societal resilience without treating any one layer as sufficient.
- Open-weight irreversibility and synthetic-media evidence limits belong in
  the relevant release and authenticity contracts.

## Open Questions

- How should cumulative marginal risk from repeated releases be measured?
- Which resilience measures have causal evidence in AI-mediated incidents?
- How should evaluations account for scaffolding, fine-tuning, and distributed
  misuse?
