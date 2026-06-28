# Source Note: GPQA: A Graduate-Level Google-Proof Q&A Benchmark

| Field | Value |
|---|---|
| Source ID | `ext_gpqa_2023` |
| Source title | GPQA: A Graduate-Level Google-Proof Q&A Benchmark |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2311.12022, https://arxiv.org/abs/2311.12022 |
| Citation label | Rein et al. (2023), GPQA |
| Published / updated | 2023-11-20 / 2023-11-20 |
| DOI | 10.48550/arXiv.2311.12022 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the benchmark-science literature queue; paper not vendored into this repository and no GPQA evaluation reproduced. |

## Thesis

GPQA belongs in the benchmark, verification-bandwidth, evidence-state, and open-research chapters as an external reference for hard expert-written questions and scalable-oversight pressure. It helps the ASI Stack distinguish benchmark difficulty, expert validation, non-expert supervision limits, and truthful-answer evaluation.

## Mechanisms

- Use expert-written multiple-choice questions in biology, physics, and chemistry.
- Compare expert performance, skilled non-expert validation with web access, and frontier model baselines in the source setting.
- Emphasize difficulty for scalable oversight where supervisors may be weaker than the system being checked.
- Treat "Google-proof" as a benchmark-design pressure rather than a general anti-contamination proof.

## Evidence

- The source reports benchmark construction and baseline evaluation in its own setting.
- This repository has not run GPQA, reproduced model scores, audited question quality, or integrated the dataset into a benchmark ratchet.
- Use this source as benchmark-design and oversight vocabulary, not as local model-quality evidence.

## Failure Modes

- Hard expert questions can test knowledge and reasoning without proving tool-use safety, source discipline, or governance behavior.
- Multiple-choice format can hide calibration, explanation quality, or evidence-use failures.
- Google-proof validation does not automatically eliminate training contamination or benchmark gaming.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to ground scalable-oversight and hard-question benchmark vocabulary.
- Do not claim local GPQA performance, expert-review reproduction, or benchmark adoption.
- Keep support state at `argument` until benchmark runs, contamination checks, and accepted evidence transitions exist.

## Open Questions

- Which ASI Stack claims require expert-level validation rather than ordinary reader plausibility?
- How should benchmark ratchets treat hard questions whose answers may become public training data?
- What evidence record should preserve expert disagreement or post-hoc correction?
