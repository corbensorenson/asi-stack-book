# Source Note: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

| Field | Value |
|---|---|
| Source ID | `ext_llm_as_judge_mt_bench_2023` |
| Source title | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena |
| Ingestion date | 2026-07-01 |
| Source version / URL | arXiv:2306.05685v4, https://arxiv.org/abs/2306.05685 |
| Citation label | Zheng et al. (2023), Judging LLM-as-a-Judge |
| Published / updated | 2023-06-09 / 2023-12-24 |
| DOI | 10.48550/arXiv.2306.05685 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the LLM-as-judge evaluation queue; MT-Bench prompts, Chatbot Arena conversations, expert votes, model outputs, and judge evaluations are not imported into this repository. |

## Thesis

This source belongs in `spinoza-verification-and-proof-carrying-claims` as the main external comparator for model-graded evaluation. It grounds the chapter's warning that an LLM judge can be useful as an evaluation route while still needing bias checks, human-preference calibration, and non-claim boundaries.

## Mechanisms

- Use strong LLMs as judges for open-ended assistant responses.
- Evaluate judge agreement with human preference data through MT-Bench and Chatbot Arena.
- Record judge limitations such as position, verbosity, self-enhancement bias, and limited reasoning.
- Treat model-graded evaluation and traditional benchmarks as complementary rather than interchangeable.

## Evidence

- The source reports LLM-as-judge agreement with human preferences in its evaluated settings and documents important judge biases.
- This repository has not run MT-Bench, imported Chatbot Arena data, used an LLM judge, or measured local judge/human agreement.
- Use this source as external model-evaluation vocabulary, not as evidence that ASI Stack tribunals, reviewers, or proof-carrying-claim routes are accurate.

## Failure Modes

- Judge bias can turn a scalable evaluation route into a hidden preference or formatting proxy.
- A model judge can reward verbosity or familiar style rather than evidence adequacy.
- Agreement in one benchmark setting can be overextended to high-risk claims, formal proof adequacy, or tribunal verdict correctness.

## Book Chapters Supported

- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to ground LLM-as-judge positioning and the requirement for judge-bias, calibration, and non-promotion boundaries.
- Do not claim the ASI Stack uses or validates LLM judges unless a local run, benchmark, or review record exists.
- Keep support state at `argument` until judge-route fixtures, human comparison, bias probes, and verdict-quality evidence exist.

## Open Questions

- Which tribunal fields should record judge identity, calibration state, position-order controls, verbosity controls, and known bias probes?
- What minimum local fixture would reject an LLM-judge verdict that lacks human-calibration or bias-control evidence?
- How should model-graded evaluation be routed differently from formal proof, citation dossiers, or executable replay?
