# Curated Reader Prose Pass: Compact Generative Systems

Date: 2026-07-01

Evidence-boundary alignment: 2026-07-03

Chapter: `compact-generative-systems-and-residual-honesty`

Reader manuscript file: `editions/reader_manuscript/v1_0/chapters/compact-generative-systems-and-residual-honesty.qmd`

Live source file: `chapters/compact-generative-systems-and-residual-honesty.qmd`

## Reader Promise

This pass should let a human reader understand why compactness counts only after reconstruction, verification, repair, fallback, semantic grounding, consumer policy, and residual burden remain visible.

The reader throughline is:

> small only counts after the remainder is named.

## Curation Scope

- Reworked the generated reader opening into a continuous chapter premise about compactness as burden accounting.
- Centered the chapter stakes on the difference between genuine compact structure and residual displacement.
- Preserved the CGS, BBVCA/GVR, RGS, semantic-leasing, and TreeLLM-facing mechanisms without turning them into benchmark claims.
- Preserved the compression receipt and semantic-node Mermaid diagrams and their meaning.
- Preserved the minimum viable implementation and beyond-SOTA sections without implying that a codec, utility benchmark, TreeLLM implementation, or semantic graph benchmark already exists.
- Aligned the reader MVI with the implemented Compact GVR synthetic slice: `python3 scripts/validate_compact_gvr_slice.py` recomputes five public-safe receipt records, selects a 78-byte exact repeat-generator-plus-repair receipt against a 368-byte literal baseline, rejects three controls, and checks a finite Lean bridge.
- Preserved proof/test boundaries for `AsiStackProofs.CompactGenerativeSystems`, generate/verify/repair receipts, semantic representation fixtures, the Compact GVR synthetic slice, and current record-shape validation.

## Meaning-Preservation Checks

- The live core claim remains a design-rationale claim with `argument` support.
- No Appendix C, Appendix K, proof manifest, source note, or support-state promotion is changed by this reader pass.
- External sources remain comparators and grounding context, not local evidence for CGS performance.
- Source-reported CGS, BBVCA, RGS, TreeLLM, RankFold, BugBrain, and Simulation Scaling ideas remain architectural material unless the repository has a local run or proof.
- Current fixtures and the Compact GVR synthetic slice validate record shape, bounded receipt discipline, finite negative cases, and a non-core evidence transition; they do not establish codec quality, utility, rate, semantic adequacy, fallback execution, or deployment readiness.

## Non-Claims

- This pass does not claim a working CGS implementation.
- This pass does not claim a measured compression ratio, utility result, TreeLLM result, semantic graph result, or generate/verify/repair codec result.
- This pass does not claim that compactness implies safety, interpretability, exactness, or evidence promotion.
- This pass does not promote the chapter core claim above `argument`; only the existing subordinate Compact GVR receipt-slice claim has a recorded `synthetic-test-backed` transition.

## Remaining Blockers

- Human editorial review has not approved the curated reader chapter.
- Stronger evidence still needs behavioral CGS utility tests, real fallback traces, corpus reconstruction/repair receipts, semantic grounding tests, hierarchy-update tests, consumer-policy-specific rejection cases, and downstream utility examples.
- Any future support-state promotion needs an accepted evidence-transition record.
