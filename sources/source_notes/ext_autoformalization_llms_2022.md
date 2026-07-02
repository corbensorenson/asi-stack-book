# Source Note: Autoformalization with Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_autoformalization_llms_2022` |
| Source title | Autoformalization with Large Language Models |
| Ingestion date | 2026-07-01 |
| Source version / URL | arXiv:2205.12615, https://arxiv.org/abs/2205.12615 |
| Citation label | Wu et al. (2022), Autoformalization with Large Language Models |
| Published / updated | 2022-05-25 / 2022-05-25 |
| DOI | 10.48550/arXiv.2205.12615 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the autoformalization and proof-carrying-claim literature queue; dataset splits, Isabelle/HOL artifacts, model outputs, and theorem-proving runs are not imported into this repository. |

## Thesis

This source belongs in `spinoza-verification-and-proof-carrying-claims` as the main external comparator for automatic translation from informal mathematical language to formal specifications and proofs. It grounds the chapter's interpretation-mapping risk: a formal artifact can only support a prose claim if the informal-to-formal mapping is itself adequate.

## Mechanisms

- Translate natural-language mathematics into formal specifications and proofs.
- Use LLM-generated formalizations to support neural theorem-proving workflows.
- Evaluate translation quality against formal systems rather than treating fluent mathematical prose as proof.
- Expose the semantic gap between informal statements and machine-checkable targets.

## Evidence

- The source reports autoformalization results over mathematical competition problems and an improvement on MiniF2F theorem proving in its own setup.
- This repository has not reproduced those results, imported the problem set, run Isabelle/HOL, or checked any autoformalized theorem from the paper.
- Use this source as external autoformalization lineage and a semantic-adequacy warning, not as local proof-carrying-claim evidence.

## Failure Modes

- A natural-language claim can be translated into a formal statement that is valid but not equivalent to the intended claim.
- A theorem-proving result can be over-read as evidence for a broader systems claim.
- Autoformalization benchmarks can hide practical source interpretation, proof target selection, and consumer-policy gaps.

## Book Chapters Supported

- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to ground interpretation mapping, semantic adequacy, and autoformalization limits in proof-carrying claims.
- Do not claim this repository implements autoformalization or proves arbitrary natural-language claims.
- Keep support state at `argument` until a local autoformalization, semantic-equivalence, and verifier pipeline exists.

## Open Questions

- What minimum local fixture would demonstrate a correct and an incorrect informal-to-formal mapping?
- Which proof-carrying-claim fields should record the formal target, source prose, mapping confidence, and reviewer decision separately?
- Could a future Lean/Python bridge reject a proof receipt when the interpretation mapping is missing or contested?
