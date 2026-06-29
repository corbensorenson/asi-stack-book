# v1.0 Release Gate Audit

Date: 2026-06-29

Status: tagged v1.0.0 release-gate audit for source commit
`96d0ca3c6b62f3530202535573941b1f6e50a83d`.

This audit checks the roadmap's eleven v1.0 Definition-of-Done gates against
tracked evidence. It preserves the exact release scope: a tagged living-book
evidence-and-reader release boundary with DOI pending, one approved local reader
HTML artifact, and no chapter-core support-state promotion.

## Gate Matrix

| # | Gate | Current status | Evidence | Residual after v1.0.0 |
|---:|---|---|---|---|
| 1 | Reader artifact gate | satisfied for the minimum HTML reader artifact | `release_records/2026-06-29-v1-reader-html-855dc277.json`; `docs/reader_html_artifact_browser_review.md`; `docs/reader_format_review_matrix.md` | EPUB, DOCX, PDF, e-reader, audio, and audio-embedded EPUB remain unapproved and outside the minimum gate unless separately promoted. |
| 2 | Claim-state gate | satisfied for v1.0 coverage | `docs/core_claim_transition_coverage.md`; `claim_decisions/v1_0_core_claim_no_promotion.json`; `docs/evidence_transition_pilot.md`; `python3 scripts/validate_core_claim_decisions.py`; `python3 scripts/validate_evidence_transitions.py` | All 54 chapter core claims remain at `argument`; no chapter core claim can move without a new accepted transition. |
| 3 | First measured/replayed result gate | satisfied for bounded synthetic-test-backed slices plus one bounded prototype-backed imported receipt slice | `docs/first_measured_replayed_slice.md`; `docs/costed_route_resource_slice.md`; `docs/circle_external_receipt_slice.md`; `evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json`; `evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json`; `evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json`; `python3 scripts/validate_circle_external_receipt_slice.py` | These transitions support only `living-book-methodology.phase5_harness_registry_runner`, `resource-economics.costed_route_budget_slice`, and `circle-calculus.external_rope_receipt_replay`, not chapter core claims or deployed capability. |
| 4 | Proof-depth gate | satisfied by explicit projection-only classification | `docs/proof_depth_classification.md`; `docs/proof_adequacy_review.md`; `python3 scripts/validate_proof_depth.py`; `python3 scripts/validate_proof_readiness.py`; `lake build` | Stronger safety-critical state-machine proofs remain future quality work unless claims widen. |
| 5 | Validator coverage gate | satisfied | `scripts/validate_validator_coverage.py`; `.github/workflows/publish.yml`; `scripts/validate_book.py`; `experiments/phase5_harness_registry.json` | Keep this gate green whenever validators or harness registry entries change. |
| 6 | Protocol record gate | satisfied for v1-critical records | `protocols/v1_critical_protocol_crosswalk.json`; `docs/protocol_record_crosswalk.md`; `python3 scripts/validate_protocol_crosswalk.py` | A full schema/Lean/fixture generator and executable Lean/Python equivalence remain v1.x work. |
| 7 | External-SOTA prose gate | satisfied for placement | `docs/external_sota_positioning_audit.md`; `python3 scripts/validate_external_sota_positioning.py --release` | Exhaustive literature synthesis remains v1.x unless a claim widens. |
| 8 | Beyond-SOTA map gate | satisfied for current roadmap | `docs/v1_0_roadmap.md#beyond-sota-reference-map-v10-blocking`; `docs/v1_progress_ledger.md` | The map must be refreshed if new evidence, chapters, or external positioning changes the release classification. |
| 9 | Architecture red-team gate | satisfied for desk review | `docs/architecture_red_team_review.md`; `python3 scripts/validate_architecture_red_team.py` | This is not runtime security validation, external audit, or deployed safety evidence. |
| 10 | Reproducibility and citability gate | satisfied for v1.0.0 with DOI pending | `docs/release_reproducibility.md`; `CITATION.cff`; `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`; `.github/workflows/publish.yml`; `lean/lean-toolchain`; `python3 scripts/validate_release_reproducibility.py` | DOI/Zenodo remains pending because no archive identifier has been issued. |
| 11 | Green release gate | satisfied for the exact v1.0.0 source commit | local validation commands recorded in `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`; GitHub Pages workflow run `28360079172`; tag `v1.0.0`; GitHub Release `https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0` | Future commits must run their own gates; this audit applies to source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`. |

## Release Classification

- Current classification: tagged v1.0.0 living-book evidence-and-reader release boundary.
- Source tag: `v1.0.0`.
- Source commit: `96d0ca3c6b62f3530202535573941b1f6e50a83d`.
- GitHub Release: `https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0`.
- Living-book release record: `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`.
- Reader artifact state: one local generated reader HTML artifact is reviewed
  and release-recorded; other reader formats remain unapproved.
- Evidence state: all chapter core claims remain at `argument`.
- Accepted upward transitions: `living-book-methodology.phase5_harness_registry_runner`
  and `resource-economics.costed_route_budget_slice` as bounded
  `synthetic-test-backed` transitions, plus
  `circle-calculus.external_rope_receipt_replay` as a bounded
  `prototype-backed` imported external receipt transition; all are outside
  chapter core claims.
- Citation metadata: `CITATION.cff` records version `1.0.0`; DOI and Zenodo
  archive facts remain pending because no DOI or archive has been issued.

## Final Release Facts

1. The v1.0.0 source commit is
   `96d0ca3c6b62f3530202535573941b1f6e50a83d`.
2. The full local gate passed on that exact source commit before tagging.
3. The GitHub Pages run for that exact commit succeeded: workflow run
   `28360079172`.
4. The tagged source state is published as Git tag `v1.0.0` and GitHub Release
   `https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0`.
5. `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json` names the
   exact commit, release classification, local validation commands, GitHub
   Pages run, DOI/Zenodo state, reader artifact state, residuals, and
   non-claims.
6. DOI/Zenodo remains pending; no DOI is cited until an archive exists.

## Validation Command

```bash
python3 scripts/validate_v1_release_gate_audit.py
```

This command checks that the gate audit names all eleven release gates, records
the v1.0.0 tag facts, references the relevant evidence files and validators, and
keeps DOI and artifact residuals visible.

## Non-Claims

- This audit does not create a DOI or Zenodo archive.
- This audit does not approve EPUB, DOCX, PDF, e-reader, audio, or
  audio-embedded EPUB artifacts.
- This audit does not promote any chapter core claim above `argument`.
- This audit does not prove ASI capability, deployed safety, model quality,
  benchmark performance, runtime behavior, source interpretation, transfer, or
  economic outcomes.
