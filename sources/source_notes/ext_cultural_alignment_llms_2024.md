# Source Note: Investigating Cultural Alignment of Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_cultural_alignment_llms_2024` |
| Source title | Investigating Cultural Alignment of Large Language Models |
| Authors / date | Tao et al.; 2024 |
| Primary URL | https://arxiv.org/abs/2402.13231 |
| Source type | empirical preprint |
| Evidence boundary | Survey-simulation evidence for the selected models, languages, questions, and reference populations; not a measurement of one true national culture. |

## Thesis

The paper compares model responses with human survey distributions to study
cultural alignment. It demonstrates why language coverage, cultural reference
population, prompt language, within-group variation, and normative authority
must remain explicit in an ASI communication or intent interface.

## Failure Modes

- National survey aggregates do not define every member's values or create a
  legitimate policy objective.
- Matching a response distribution can reproduce undesirable norms and does
  not establish understanding, respect, consent, or fairness.
- Translation and model self-report can introduce measurement artifacts.

## Book Chapters Supported

- `human-ai-communication-persuasion-and-epistemic-security`: audience and
  cultural-context scope.
- `human-intent-as-a-formal-input`: interpretation and clarification across
  cultures.
- `benchmark-ratchets-and-anti-goodhart-evidence`: construct validity for
  cultural evaluation.

## Mechanisms

The study compares model-generated answers with human survey distributions
across prompt languages and reference populations. The method makes the choice
of population, survey instrument, language, and similarity statistic part of
the claimed alignment result.

## Evidence

The experiments show measurable response differences for the tested models
and settings. They do not establish stable cultural understanding, legitimate
normative authority, or individual-level fit.

## Claims To Add Or Update

- Intent interpretation and communication evaluations must declare their
  linguistic and cultural reference population.
- Distributional similarity can diagnose mismatch, but cannot serve as an
  automatic target for value alignment or policy legitimacy.

## Open Questions

- How should within-community pluralism and dissent appear in evaluation?
- Which locally authored instruments separate translation artifacts from
  genuine model behavior?
