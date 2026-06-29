# v1.0 Release Gate Audit

Date: 2026-06-29

Status: gate audit for the current v1.0 candidate, not a final v1.0 release record.

This audit checks the roadmap's eleven v1.0 Definition-of-Done gates against
tracked evidence. It exists to prevent the project from confusing a strong
candidate state with a final evidence release.

## Gate Matrix

| # | Gate | Current status | Evidence | Residual before final v1.0 evidence-release claim |
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
| 10 | Reproducibility and citability gate | candidate-satisfied; final release metadata pending | `docs/release_reproducibility.md`; `CITATION.cff`; `.github/workflows/publish.yml`; `lean/lean-toolchain`; `python3 scripts/validate_release_reproducibility.py` | Final v1.0 tag, final release record, and DOI/Zenodo facts remain pending until they actually exist; DOI may remain pending only if the final release record says so. |
| 11 | Green release gate | locally satisfied for the latest validation run; final commit/tag check pending | local validation commands recorded in this audit and changelog; latest checked prior Pages run before this audit was green | Before any final tag, run the local gate again on the exact source commit and confirm that the GitHub Pages run for that commit succeeds. |

## Release Classification

- Current classification: v1.0 candidate.
- Not final classification: not a final v1.0 evidence release.
- Reader artifact state: one local generated reader HTML artifact is reviewed
  and release-recorded; other reader formats remain unapproved.
- Evidence state: all chapter core claims remain at `argument`.
- Accepted upward transitions: `living-book-methodology.phase5_harness_registry_runner`
  and `resource-economics.costed_route_budget_slice` as bounded
  `synthetic-test-backed` transitions, plus
  `circle-calculus.external_rope_receipt_replay` as a bounded
  `prototype-backed` imported external receipt transition; all are outside
  chapter core claims.
- Final release metadata: final v1.0 tag, final release record, DOI/Zenodo
  archive facts, and "how to cite this version" final text remain pending.

## Final Release Blockers

1. The final v1.0 source commit must be known.
2. The full local gate must pass on that exact commit.
3. The GitHub Pages run for that exact commit must succeed.
4. A final release record must name the exact commit, release classification,
   local validation commands, GitHub Pages run, DOI/Zenodo state, reader
   artifact state, residuals, and non-claims.
5. `CITATION.cff` and `docs/release_reproducibility.md` must stay at candidate
   status until the final release tag or record actually exists.

## Validation Command

```bash
python3 scripts/validate_v1_release_gate_audit.py
```

This command checks that the gate audit names all eleven release gates, preserves
the candidate-versus-final boundary, references the relevant evidence files and
validators, and keeps final metadata blockers visible.

## Non-Claims

- This audit does not create a final v1.0 tag, final release record, DOI,
  Zenodo archive, or GitHub release.
- This audit does not approve EPUB, DOCX, PDF, e-reader, audio, or
  audio-embedded EPUB artifacts.
- This audit does not promote any chapter core claim above `argument`.
- This audit does not prove ASI capability, deployed safety, model quality,
  benchmark performance, runtime behavior, source interpretation, transfer, or
  economic outcomes.
