# Estimating Worst-Case Frontier Risks of Open-Weight LLMs

## Source identity

- Source ID: `ext_openai_worst_case_open_weight_risks_2025`
- Authors: Eric Wallace, Olivia Watkins, Miles Wang, Kai Chen, Chris Koch
- Public source: <https://openai.com/index/estimating-worst-case-frontier-risks-of-open-weight-llms/>
- Published: 2025-08-05
- Reviewed: 2026-07-24

## Thesis

The study treats malicious fine-tuning as a release-time worst-case elicitation
problem. It fine-tunes gpt-oss variants for biology and cybersecurity tasks and
compares the resulting systems with open- and closed-weight models under the
provider's evaluation framework.

## Mechanisms used by the book

- evaluate the exact release artifact and a bounded maliciously fine-tuned
  derivative;
- preserve domain-specific training, tool, scaffold, and evaluation budgets;
- compare against the accessible open frontier and the closed frontier;
- separate default refusal behavior from latent capability;
- use results as one input to a release decision, not as permanent immunity.

## Evidence and limitations

The authors report that their maliciously fine-tuned gpt-oss variants remained
below the tested high-capability thresholds and did not substantially advance
the tested open frontier. These are provider-authored, model- and protocol-
specific results. They do not establish resistance to future fine-tuning,
unknown domains, different tools, distributed actors, or larger budgets. The
book does not reproduce the experiments.

## Failure modes surfaced

- evaluating only the default aligned model;
- comparing only against obsolete open models;
- calling a bounded fine-tuning attempt a worst-case proof;
- omitting scaffold and tool access;
- treating absence of threshold crossing as zero marginal risk;
- failing to renew the analysis as the accessible frontier changes.

## Chapter routing

- Primary: `open-weight-release-and-post-release-control`
- Supporting: `dangerous-capability-domains-and-misuse-uplift`

## Open questions

- How should an evaluation budget approximate capable adversaries?
- How quickly does a release decision stale as methods and open comparators
  improve?
- Which mitigations remain meaningful after unrestricted weight access?

