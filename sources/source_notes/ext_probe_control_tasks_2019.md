# Source Note: Designing and Interpreting Probes with Control Tasks

| Field | Value |
|---|---|
| Source ID | `ext_probe_control_tasks_2019` |
| Source title | Designing and Interpreting Probes with Control Tasks |
| Ingestion date | 2026-07-26 |
| Source version / URL | EMNLP-IJCNLP 2019, https://aclanthology.org/D19-1275/ |
| Citation label | Hewitt and Liang (2019), Designing and Interpreting Probes with Control Tasks |
| Published / updated | 2019-11 / 2019-11 |
| DOI | 10.18653/v1/D19-1275 |
| Ingestion basis | Primary paper inspected at the abstract, Sections 1–2, the probe-family results summarized in Section 1, and the conclusion. No experiment was reproduced locally. |

## Thesis

High task accuracy from a diagnostic probe is not, by itself, evidence that a
representation carries the named structure in an accessible or simple form.
The probe may be learning the task. A matched control task gives the probe the
same input and output spaces while randomizing the word-type-to-label mapping,
so success on that control exposes memorization capacity. The paper defines
**selectivity** as linguistic-task accuracy minus control-task accuracy.

## Mechanisms

- Construct control labels as deterministic but randomly sampled functions of
  word identity, keeping the linguistic task's output space.
- Train the same probe family on the linguistic and control tasks.
- Compare linear, bilinear, and multilayer probes across capacity,
  regularization, sample size, and representation layer.
- Interpret task accuracy jointly with control accuracy rather than preferring
  a high-capacity probe merely because it wins the target task.

## Evidence

Sections 1–2 report that popular ELMo multilayer probes could obtain high task
accuracy while also learning the control mapping, whereas simpler probes could
have similar linguistic accuracy and higher selectivity. The reported study is
about English part-of-speech and dependency-edge probes on ELMo. It is
source-reported evidence, not a local result.

## Failure Modes

- A powerful probe can turn weak traces or word identity into apparent concept
  decoding.
- Dropout alone need not control probe selectivity.
- Comparing layers only by target accuracy can reverse the interpretation
  obtained after accounting for memorization.
- A control task can test one shortcut while missing evaluator leakage,
  distribution shift, causal non-use, or a badly operationalized construct.

## Book Chapters Supported

- Primary: `white-box-evidence-interpretability-and-activation-governance`
- Handoff: `evidence-states-and-claim-discipline`

## Claims To Add Or Update

- Report probe capacity, regularization, control-task performance, label
  leakage checks, and a simpler baseline with every decoding claim.
- Treat decodability as method-relative observation until intervention and
  transfer tests establish stronger scope.
- Do not turn a failed probe into evidence that the model lacks the information
  or mechanism.

## Open Questions

- What control tasks best match modern generative, multimodal, and agentic
  probes without becoming easier than the target task?
- How should selectivity combine with causal use, calibration, transfer, and
  intervention specificity?
- Which probe families are competent enough to detect a mechanism without
  becoming capable enough to create the apparent signal?
