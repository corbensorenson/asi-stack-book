# Source Note: SWE-rebench V2: Language-Agnostic SWE Task Collection at Scale

| Field | Value |
|---|---|
| Source ID | `ext_swe_rebench_v2_2026` |
| Source title | SWE-rebench V2: Language-Agnostic SWE Task Collection at Scale |
| Ingestion date | 2026-07-17 |
| Source version / URL | arXiv:2602.23866v2, https://arxiv.org/abs/2602.23866 |
| Citation label | Badertdinov et al. (2026), SWE-rebench V2 |
| Published / updated | 2026-02-27 / 2026-06-01 |
| DOI | 10.48550/arXiv.2602.23866 |
| Code / data | https://github.com/SWE-rebench/SWE-rebench-V2 and https://huggingface.co/datasets/nebius/SWE-rebench-V2 |
| Ingestion basis | Passage review of arXiv v2, official code README/evaluator, pinned Hugging Face dataset metadata and parquet object, public GitHub pull-request receipts, and remote image manifests. |

## Thesis

SWE-rebench V2 is a useful natural-task substrate, not an automatic validity
certificate. It contributes a multilingual construction funnel from public
merged pull requests to containerized repository states, separated solution
and test patches, fail-to-pass/pass-to-pass oracles, full-suite execution, and
per-instance diagnostics. For the ASI Stack it is most valuable as a way to
replace authored repository tasks with traceable natural development work while
retaining explicit construct, evaluator, contamination, rights, and resource
gates.

## Mechanisms

- Mine public pull-request and linked-issue histories, retaining resolved issues,
  merged changes, permissive repositories, and changes that introduce tests.
- Split non-test solution changes from test changes and construct containerized
  repository environments with language-specific base images, runners, and
  parsers under one common workflow.
- Execute a full test suite before and after the human solution patch, retaining
  instances with at least one fail-to-pass test.
- Use an interactive setup agent and repository-specific log parsers, then
  recheck generated installation/test procedures for reproducibility.
- Apply automated issue-clarity filtering and attach diagnostic labels for test
  coupling, implicit naming, external dependencies, ambiguous specifications,
  patch artifacts, implicit knowledge, and inline tests.

## Evidence and passage review

- The paper reports 32,079 containerized tasks from 3,617 repositories across
  20 languages, with an additional PR-derived training collection. Sections
  3.1–3.3 describe collection, environment synthesis, paired execution, and
  full-suite validation.
- The construction funnel retains only 32,079 of 29.5 million initial PRs. The
  setup ablation reports materially higher pass-at-k from interactive and
  repeated setup, which is direct evidence against treating a one-shot naive
  environment builder as an adequate failure test.
- The clarity-filter ablations have limited recall and depend on model/prompt/
  ensemble choice. They are useful screening signals, not independent labels.
- The diagnostic study covers 300 tasks in five languages with seven models,
  and identifies test coupling, hidden naming requirements, and external
  context as false-negative risks. It does not validate every released task.
- Local preflight, distinct from the paper's reported results, found 1,117 rows
  created after the pinned local model snapshot across 532 repositories and 20
  languages. Only compact metadata and content digests are retained in the
  repository; the 409 MiB source parquet remains a transient acquisition.

## Failure Modes

- A container manifest can resolve while the image fails to pull, emulate,
  start, or reproduce the gold test transition. Manifest availability is not
  gold execution.
- The released images are `linux/amd64`; the local Apple Silicon host must
  measure emulation cost, expanded disk, runtime, and cleanup before the
  resource gate can pass.
- A candidate patch touching any test-patch path can create an evaluator
  collision. Candidate admission must reject those edits before applying the
  hidden test patch.
- Passing project tests does not observe authority scope, evidence freshness,
  rollback completeness, residual debt, or governance cost. Those require
  separately implemented observers.
- Post-snapshot task creation reduces one contamination route but cannot prove
  that the model never encountered the repository, analogous code, mirrored
  content, or later training data.
- Dataset CC-BY-4.0 terms coexist with per-repository licenses. Preserve source
  URLs, commit identity, attribution, and redistribution boundaries.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence`
- `artifact-graphs-audit-logs-and-replay`
- `integrated-reference-architecture`
- `prototype-roadmap`
- `readiness-gates-residual-escrow-and-quarantine`

## Claims To Add Or Update

- Natural repository benchmarks still require a task lease: exact source,
  commit, model snapshot, contamination boundary, license, harness, tests,
  evaluator, cost, and known pathology state.
- Failed setup, parsing, image acquisition, positive controls, or gold execution
  closes the denominator as an instrument failure; it cannot become evidence
  that a model, governance route, or architecture failed.
- Strong development preflight should include repeated setup or repair
  opportunity, successful human-gold execution, explicit test-path collision
  guards, independent task review, and favorable controls before final holdout.

## Local boundary

No SWE-rebench V2 task has yet completed the local gold execution, candidate
generation, governed admission, independent evaluator, sensitivity, or final
held-out pipeline. Source ingestion and development-corpus qualification create
no benchmark result, support-state promotion, coding-capability result,
governance benefit, safety result, transfer, reproduction, SOTA, AGI, or ASI
claim.

## Open Questions

- Which development tasks survive local gold execution and independent
  specification review without hidden naming or external-context obligations?
- What final sample size can detect the preregistered useful-safe-release effect
  after clustering by repository and task family?
- How much disk, runtime, and variance does `linux/amd64` emulation add on the
  pinned Apple Silicon host, and should the final corpus use a separate native
  execution environment?
- Which candidate failures are genuine governance opportunities rather than
  generator incompetence, task ambiguity, or evaluator blindness?
