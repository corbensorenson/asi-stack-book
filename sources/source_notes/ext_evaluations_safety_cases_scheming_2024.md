# Source Note: Towards Evaluations-Based Safety Cases for AI Scheming

| Field | Value |
|---|---|
| Source ID | `ext_evaluations_safety_cases_scheming_2024` |
| Source title | Towards Evaluations-Based Safety Cases for AI Scheming |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:2411.03336, https://arxiv.org/abs/2411.03336 |
| Citation label | Balesni et al. (2024), Evaluations-Based Safety Cases for AI Scheming |
| Published / updated | 2024-10-29 / 2024-10-29 |
| DOI | 10.48550/arXiv.2411.03336 |
| Ingestion basis | Primary arXiv paper inspected for its scoped safety-case framing, proposed scheming inability/harm inability/harm control/alignment arguments, evaluation evidence dependencies, and stated unresolved assumptions. No evaluation, threat model, safety case, control protocol, or result was reproduced in this repository. |

## Thesis

The paper sketches how a developer could structure an evaluations-based
argument that an AI system is unlikely to cause catastrophic outcomes through
scheming. It distinguishes scheming inability, harm inability, harm control,
and alignment arguments, and explains that strong assurance depends on
substantial empirical evidence and assumptions that are not confidently
satisfied. It is a framework for identifying missing evidence, not a completed
general safety demonstration.

## Mechanisms

- Scope a top-level unacceptable-outcome claim to a threat model and deployment
  context instead of treating safety as a context-free system property.
- Decompose the case into distinct incapability, harm, control, or alignment
  arguments, each with its own empirical-evaluation needs and assumptions.
- Preserve assumptions about elicitation, evaluation reliability, model
  capability, deployment conditions, and controls rather than collapsing them
  into an evaluation score.
- Use the argument's weak points to identify research gaps, countercases, and
  evidence needed for a stronger claim.

## Evidence

- The paper provides a structured conceptual safety-case sketch and examples of
  how empirical evaluations could contribute to its arguments.
- It explicitly states that many required assumptions have not been confidently
  satisfied and that multiple open research problems remain.
- This repository has not run scheming evaluations, performed a threat-model
  assessment, verified control measures, or assembled an ASI Stack safety case.
  The paper is a scoped methodology comparator only.

## Failure Modes

- Treating a safety-case sketch as a demonstrated probability bound or a broad
  safety conclusion.
- Confusing no observed dangerous capability with a reliable inability argument
  when elicitation, scope, or evaluation reliability are unresolved.
- Treating a proposed control measure as effective without evidence that it
  remains effective in the relevant deployment setting.
- Hiding unresolved assumptions, countercases, or threat-model disagreement in
  a polished narrative.

## Book Chapters Supported

- `safety-cases-and-structured-assurance` (Safety Cases and Structured Assurance)

## Claims To Add Or Update

- Use this note for scoped unacceptable-outcome claims, distinct incapability,
  harm, control, and alignment argument families, and explicit assumption and
  countercase handling.
- Require the compiled case to retain its threat model, evidence limits,
  unresolved defeaters, and residual owner.
- Do not claim local scheming absence, alignment, control effectiveness, safety,
  readiness, deployment authorization, or ASI from this source or a case graph.

## Open Questions

- Which argument families are appropriate for a public-safe book artifact that
  names risks without manufacturing a local threat-model result?
- How should the case compiler distinguish missing evidence from evidence that
  actively defeats a proposed argument?
- Which independent evaluation and review records would be necessary before any
  case fragment could support a narrow release or safeguard claim?
