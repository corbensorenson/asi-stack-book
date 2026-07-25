# An Example Safety Case for Safeguards Against Misuse

## Source identity

- Source ID: `ext_aisi_misuse_safeguards_safety_case_2026`
- Authors: Joshua Clymer, Jonah Weinbaum, Robert Kirk, Kimberly Mai, Selena
  Zhang, Xander Davies
- Publisher: UK AI Security Institute
- Public source: <https://www.aisi.gov.uk/research/an-example-safety-case-for-safeguards-against-misuse>
- Reviewed: 2026-07-24

## Thesis

The report demonstrates how safeguard red-team evidence, estimated attacker
effort, an uplift model, and deployment monitoring can be assembled into an
explicit misuse safety case. The value is the argument structure: evaluation
results must connect to a decision-relevant risk model instead of remaining a
patchwork of disconnected benchmarks.

## Mechanisms used by the book

- estimate attack success and effort against safeguards;
- connect bypass evidence to a quantitative uplift model;
- carry uncertainty and assumptions into the safety case;
- monitor deployment and update the argument as threats change;
- preserve the difference between model capability, safeguard bypass, actor
  uplift, and realized harm.

## Evidence and limitations

This is an example argument and methodology, not a universal empirical result.
Its assumptions, attacker model, data, and quantitative links require
validation in each domain. It does not establish that safeguards reduce real
misuse to any specific level or that the ASI Stack's proposed contracts work.

## Failure modes surfaced

- benchmark scores disconnected from harm pathways;
- uplift inferred from raw capability;
- attacker effort estimated without adaptive challenge;
- uncertainty dropped at the deployment decision;
- monitoring unable to update the safety case;
- one domain's parameters transferred to another.

## Chapter routing

- `dangerous-capability-domains-and-misuse-uplift`
- `safety-cases-and-structured-assurance`
- `societal-resilience-and-misuse-defense`

## Open questions

- Which uplift functions remain identifiable with sparse incident data?
- How should defender adaptation and attacker substitution enter the model?
- What independent evidence is needed before a misuse safety case can carry
  release authority?

