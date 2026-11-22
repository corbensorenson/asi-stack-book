# Source Note: On the conversational persuasiveness of GPT-4

| Field | Value |
|---|---|
| Source ID | `ext_conversational_persuasion_gpt4_2025` |
| Source title | On the conversational persuasiveness of GPT-4 |
| Ingestion date | 2026-07-19 |
| Source version / URL | Open Nature Human Behaviour version of record, https://www.nature.com/articles/s41562-025-02194-6 |
| Citation label | Salvi et al. (2025), Conversational Persuasiveness of GPT-4 |
| Published / updated | 2025-05-19 / 2025-05-19 |
| DOI | 10.1038/s41562-025-02194-6 |
| Review state | Selected primary passages reviewed for the communication chapter. |
| Ingestion basis | Official open article abstract, experimental-design, aggregate-result, limitations, ethics, and citation passages inspected. Supplementary files, released debate data, code, individual transcripts, and downstream replications were not audited or reproduced locally. |

## Thesis

Personalized conversational LLM arguments can influence stated agreement in a
controlled debate setting, making personalization data and dialogue dynamics
part of an AI communication risk boundary. This source supports the need to
measure influence as an outcome rather than infer it from stylistic ratings; it
does not prove durable real-world behavior change or a particular mitigation.

## Mechanisms

- Randomly assign participants to human or GPT-4 opponents, with or without
  limited sociodemographic information.
- Randomize debate topics and initial opinion-strength strata.
- Use a short opening, rebuttal, and conclusion sequence.
- Compare pre- and post-debate agreement with the opponent's assigned position.
- Debrief participants about opponent identity and record experimental ethics.

## Evidence

The preregistered study reports 900 participants across a 2 x 2 x 3 design.
Its strongest reported aggregate effect is in the personalized GPT-4 condition.
The unpersonalized GPT-4 and personalized-human comparisons do not establish a
statistically distinguishable effect from the human baseline at the reported
threshold. Outcomes are stated agreement after a short structured debate, not
durable action, broad population transfer, or deployed-platform evidence.

### Selected primary passages reviewed on 2026-11-18

Reviewed Methods (Participant recruitment and Experimental design), Results (Aggregate results and Table 2), and Discussion (limitations). In the version of record, the preregistered study assigns US adults recruited through Prolific to short structured debates. Personalized GPT-4 versus the human baseline increases the modeled odds of higher post-debate agreement by 81.2% (95% CI 26.0% to 160.7%, N=900). The chapter uses this result to justify evaluating the audience and personalization context in approval workflows. The estimate concerns ordinal self-reported agreement in this study. It does not establish durable behavior change, reviewer approval effects, mitigation efficacy, transfer, or a local result.
[Primary record](https://pmc.ncbi.nlm.nih.gov/articles/PMC12367540/).

The headline contrast changes both the opponent type and access to
personalization. Estimating an effect of personalization alone requires
comparing opponents of the same type. The contrast also reports relative
odds of a higher ordinal response, leaving absolute changes in probabilities
dependent on the response distribution.

## Failure Modes

- Generalizing a short US online debate result to other populations, domains,
  relationships, channels, decisions, or time horizons.
- Treating personalization as uniformly effective or demographics as a complete
  audience model.
- Equating opinion movement with truthful correction, welfare, informed consent,
  autonomy, or beneficial action.
- Reusing an influence study as evidence that disclosure, abstention, correction,
  or communication limits work.

## Book Chapters Supported

- Applied in `human-ai-communication-persuasion-and-epistemic-security`
- Existing boundary owners: `human-factors-and-meaningful-control-in-oversight`,
  `scalable-oversight-and-adversarial-ai-control`,
  `claim-ledgers-and-belief-revision`, `moral-uncertainty-and-value-conflict`,
  `runtime-adapters-tool-permissions-and-human-approval`, and
  `capability-thresholds-and-deployment-commitments`

## Claims To Add Or Update

- Treat audience data, personalization, dialogue state, message objective,
  disclosure, and observed belief or choice effects as separate records.
- Compare personalized and unpersonalized AI with human and non-persuasive
  baselines; preserve null as well as positive conditions.
- Require human-subject ethics, delayed outcomes, heterogeneity, correction, and
  autonomy/welfare measures before any broad influence or mitigation claim.
- Do not infer manifest admission, real-world persuasion, safety, or support
  movement from this study.

## Open Questions

- Which communication effects persist, reverse, or change behavior after delay?
- How should a system distinguish legitimate explanation, advice, negotiation,
  therapy, teaching, and advocacy from covert or autonomy-eroding influence?
- Which disclosures and correction channels actually restore informed choice?
