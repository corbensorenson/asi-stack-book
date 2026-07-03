# Curated Reader Prose Pass: Benchmark Ratchets and Anti-Goodhart Evidence

Last updated: 2026-07-02

Follow-up: 2026-07-02

Follow-up: 2026-07-03

Status: reconciled for prose meaning on 2026-07-03.

Chapter ID: `benchmark-ratchets-and-anti-goodhart-evidence`

Curated reader file:
`editions/reader_manuscript/v1_0/chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd`

## Reader Promise

A human reader should leave this chapter understanding that benchmark scores
are pressure signals, not evidence by themselves. A benchmark result can move a
claim only when the stack preserves the run record, baseline, residuals,
negative cases, contamination and transfer boundaries, regression floors, and
the exact support-state effect.

## Scope

This pass turns the generated reader baseline for Benchmark Ratchets and
Anti-Goodhart Evidence into a first booklike curated reader draft. It is a
reader-prose derivative only.

Allowed curation scopes used:

- chapter openings and closings;
- pacing;
- paragraph ordering;
- section flow;
- transition prose;
- sentence-level voice;
- chapter compression.

Proof/test boundary clarification is recorded as meaning preservation, not as
permission to change proof or test status.

## What Changed

- Added a second 2026-07-03 reconciliation pass that distinguishes formal
  proof lanes from measurement lanes: benchmark pressure can expose workload
  behavior, regression, saturation, contamination, and transfer limits, but it
  cannot write a broader claim by itself.
- Reframed the chapter around the distinction between a benchmark score and an
  evidence packet.
- Organized the mechanism around evidence-state classification, run records,
  baselines, residuals, regression floors, anti-Goodhart checks, contamination
  and transfer boundaries, and claim-specific promotion decisions.
- Added a toy ratchet-decision example that distinguishes frontier progress,
  old-floor regression, residual creation, contamination checks, promotion
  review, and no-support-promotion boundaries.
- Preserved external benchmark-science orientation for MMLU, BIG-bench, HELM,
  GPQA, SWE-bench, LiveBench, Dynabench, CheckList, contamination analysis, and
  Goodhart variants without claiming local reproduction.
- Preserved Benchmaxxing, RMI, Cognitive Loop Closure, UAT, Coherence Exchange,
  TokenMana, MoECOT, Road To AGI, Project Theseus, and Theseus transfer-source
  boundaries.
- Preserved the evidence boundary that the benchmark-ratchet fixture, finite
  Lean predicates, and synthetic anti-Goodhart harness support protocol
  discipline only.
- Added a 2026-07-03 evidence-boundary alignment that surfaces the
  `2026-07-02` fixture bridge: `validate_benchmark_antigoodhart.py`,
  `validate_benchmark_fixture_bridge.py`, result record
  `experiments/benchmark_antigoodhart/results/2026-07-02-fixture-bridge.json`,
  2 valid synthetic fixtures, 5 expected-invalid controls, one promotion-ready
  path, one saturated-regression-floor path, `support_state_effect: none`,
  `chapter_core_support_effect: none`, `evidence_transition_created: false`,
  and the three finite Lean theorem refs.
- Preserved the missing-work boundary: no empirical benchmark run, hidden
  holdout, transfer check, contamination audit, regression-suite quality,
  source-reported replay, Theseus readiness, deployment readiness, model
  quality, or ASI-progress result is claimed.
- Preserved the minimum viable implementation, beyond-state-of-the-art
  endpoint, and handoff into Policy Optimization and Learning from Feedback.
- Preserved the release and measurement boundary: the new example is
  reader-facing explanation only and does not claim an empirical benchmark run,
  hidden-holdout quality, transfer validity, contamination resistance,
  source-reported replay, Theseus readiness, model quality, or support-state
  movement.

## Meaning Preservation Checks

| Check | Result |
|---|---|
| Core claim meaning preserved | Pass. The curated draft keeps the claim that benchmark ratchets should preserve regressions, create harder frontiers, record residuals, and resist Goodhart pressure. |
| Support-state boundary preserved | Pass. The curated draft states that the live book keeps the claim at `argument` support. |
| Source boundary preserved | Pass. No new source IDs, source facts, citations, or external claims were introduced by this pass; benchmark-science sources remain orientation and vocabulary, not local reproduction. |
| Proof/test status preserved | Pass. The curated draft keeps the boundary that fixture validation, finite Lean predicates, and the synthetic anti-Goodhart harness do not prove benchmark success, hidden-holdout validity, transfer, contamination resistance, regression-suite quality, source-reported replay, Theseus readiness, deployment readiness, model quality, support-state movement, or ASI progress. |
| Implementation horizon preserved | Pass. The minimum viable implementation remains a benchmark-evidence decision record plus a small validation harness and finite fixture bridge; the mature endpoint remains an unimplemented benchmark operating system. |
| Part arc preserved | Pass. The 2026-07-03 reconciliation connects executable-spec lanes to benchmark pressure and benchmark pressure to policy-update custody without changing claim, source, proof/test, implementation, or release meaning. |
| Release blockers preserved | Pass. No reader release record, format review, reconciliation approval, EPUB, DOCX, PDF, HTML, or audio artifact is approved by this pass. |

## Non-Claims

- This pass does not change the live AI/research chapter.
- This pass does not change `book_structure.json`.
- This pass does not alter Appendix C, source assignments, proof targets, test
  status, implementation horizons, or release records.
- This pass does not approve the curated chapter for reader release.
- This pass does not create EPUB, DOCX, PDF, HTML, audio, or audio-embedded EPUB
  artifacts.
- This pass does not promote any chapter core claim or non-core claim.
- This pass does not claim empirical benchmark success, hidden-holdout
  validity, benchmark transfer, contamination resistance, regression-suite
  quality, anti-Goodhart effectiveness, source-reported benchmark replay,
  current Theseus readiness, deployment readiness, model quality, support-state
  movement, or ASI progress.

## Remaining Blockers

- `reader_release_record_not_created`
- `format_artifact_not_reviewed`
- `curated_reconciliation_not_approved`

Chapter-level prose meaning is reconciled for this pass, but reader release,
format artifact review, and final curated-reconciliation approval remain
blocked.
