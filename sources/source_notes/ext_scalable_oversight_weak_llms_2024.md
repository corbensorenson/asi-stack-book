# Source Note: On scalable oversight with weak LLMs judging strong LLMs

| Field | Value |
|---|---|
| Source ID | `ext_scalable_oversight_weak_llms_2024` |
| Source title | On scalable oversight with weak LLMs judging strong LLMs |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:2407.04622v2, https://arxiv.org/abs/2407.04622 |
| Citation label | Kenton et al. (2024), On scalable oversight with weak LLMs judging strong LLMs |
| Published / updated | 2024-07-05 / 2024-07-12 |
| DOI | 10.48550/arXiv.2407.04622 |
| Ingestion basis | Primary arXiv HTML paper inspected for protocol definitions, task and capability-gap choices, baseline comparisons, reported results, and stated limitations. No judge, debater, consultant, passage verifier, prompt, task, baseline, or reported result was reproduced in this repository. |

## Thesis

The paper evaluates debate and consultancy as scalable-oversight protocols with
LLMs used as stronger agents and weaker judges. Its results depend on protocol
and task: debate outperforms consultancy in the reported assigned-role setting,
but comparisons with direct question answering are mixed outside the
information-asymmetry tasks. Open-role consultancy exposes a persuasion risk,
and the paper does not provide direct evidence that debate is safe or effective
as a training protocol.

## Mechanisms

- Compare direct question-answering baselines with assigned-role consultancy,
  assigned-role debate, open consultancy, and open debate.
- Vary tasks, protocol, and relative judge/debater capability rather than treat
  "oversight" as a single model score.
- In extractive tasks, distinguish an available source article from a judge that
  sees only debater-selected passages, with an external passage check in the
  source setting.
- Separate inference-time judge accuracy from the stronger claim that a protocol
  supplies a safe training signal; track cases in which an agent chooses which
  answer to advocate.

## Evidence

- The primary paper reports evaluations across its selected tasks, LLMs,
  prompts, protocol variants, and score definitions. Its reported comparative
  findings are conditional on those settings.
- It reports mixed results against direct-QA baselines outside extractive
  information-asymmetry tasks and warns that its inference-only study is not
  direct evidence for debate as a training protocol.
- This repository has not run debate, consultancy, weak-judge calibration,
  passage verification, persuasion testing, human-subject review, or a training
  study. The source is a protocol-evaluation comparator only.

## Failure Modes

- A persuasive but wrong agent can induce an inadequately calibrated judge to
  accept an incorrect answer.
- Shared model family, prompting, evaluator, or information access can create
  correlated failure that role separation alone does not remove.
- A protocol can beat a weak baseline while failing to beat an appropriately
  informed direct-review baseline.
- A source-setting inference result can be overextended into a claim about
  training safety, general supervision, execution authority, or deployment.

## Book Chapters Supported

- `scalable-oversight-and-adversarial-ai-control` (Scalable Oversight and Adversarial AI Control)

## Claims To Add Or Update

- Use this note for protocol-specific oversight records, direct-review
  baselines, independent outcome-audit requirements, information-access
  declarations, and persuasion or correlation residuals.
- Treat debate, consultancy, and AI-aided review as candidate protocols whose
  interpretation depends on task, capability gap, evaluator access, baseline,
  and outcome audit.
- Do not claim local judge calibration, debate superiority, evaluator
  independence, training safety, execution permission, model quality, safety,
  or ASI.

## Open Questions

- How can a public-safe fixture reject a high-risk oversight result with no
  independent outcome audit, baseline, or residual owner?
- Which negative controls distinguish an independent reviewer from a correlated
  model vote or a protocol transcript that merely appears adversarial?
- How should a system handle fleet-scale approval latency and operator-load
  residuals without equating faster review with safer review?
