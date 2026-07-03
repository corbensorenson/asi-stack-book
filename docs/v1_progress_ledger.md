# v1.0 Progress Ledger

Date: 2026-06-29

This ledger is the compact process-control surface for the v1.0 goal. It keeps
the detailed roadmap from becoming the only place where completed work,
remaining blockers, and release-classification boundaries are visible.

The current state is a tagged v1.0.0 living-book evidence-and-reader release
boundary for source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`. It has a
release-gate audit, reviewed local reader HTML artifact, complete chapter-core
no-promotion coverage, four bounded synthetic-test-backed measured/replayed
transitions plus one prototype-backed imported Circle receipt transition outside
chapter core claims, proof-depth honesty, protocol crosswalks, external-SOTA
placement, architecture desk red-team coverage, final citation metadata, and a
tracked living-book release record. DOI and Zenodo archive metadata remain
pending because no archive identifier has been issued.

## Phase Ledger

| Phase | Gate | Current state | Remaining v1.0 blocker or residual |
|---|---|---|---|
| Phase 0 | Operating discipline and CI honesty | Validator coverage meta-check, prior-run check discipline, manifest schema, and public-surface validation are active | Keep prior Pages run checks and all validators green before each commit. |
| Phase 1 | Reader-visible voice and de-templating | Complete for current tree; repeated-prose guards reject known scaffold formulas | Keep guards passing after future chapter edits. |
| Phase 2 | Reviewed reader manuscript path | Generated reader review matrix is complete; local reader HTML artifact has an edition release record | EPUB/DOCX/PDF/audio remain unapproved unless separately reviewed and release-recorded. |
| Phase 3 | Claim-state coverage | All 44 chapter core claims have an accepted no-change transition or explicit no-promotion decision | No chapter core claim can move above `argument` without a specific accepted evidence transition. |
| Phase 3B | First measured or replayed slice | Registry-runner infrastructure slice, costed-route/resource-budget selector slice, finite load-smoothing selector slice, and compact GVR receipt slice are accepted as bounded `synthetic-test-backed` transitions; Circle external rope receipt replay is accepted as a bounded `prototype-backed` transition | Deeper prototype or empirical measured/replayed slices remain needed before stronger chapter claims. |
| Phase 4 | Proof-depth honesty | Proof-depth classifier and safety-critical projection-only classifications are recorded | Richer state-machine proofs remain future quality work unless claims widen. |
| Phase 5 | Test harness and evidence depth | Twenty-two harnesses, registry runner, costed-route selector slice, and Circle external receipt slice are wired and validated | Next useful evidence should be real trace, additional imported prototype receipt, or empirical replay rather than more synthetic scaffolding. |
| Phase 5A | Protocol source-of-truth hardening | v1-critical schema/fixture/harness/Lean crosswalk exists and validates | Keep crosswalk current when protocol records or evidence transitions change. |
| Phase 6 | External-SOTA prose placement | 44 chapters positioned, 10 exceptions recorded, 0 release placement rows open | Deeper external-literature synthesis remains v1.x unless a new claim widens. |
| Phase 7 | Visual, site, toolchain, archival review | Site visual review, release reproducibility, public-site accessibility readiness, tag `v1.0.0`, GitHub Release, and living-book release record are recorded | DOI/Zenodo archive metadata remains pending; manual keyboard/screen-reader review remains a quality residual. |
| Phase 7A | Architecture-level red-team | Six desk-review attack scenarios are recorded and validator-checked | Runtime/security validation and external audit remain future evidence work. |
| Phase 8 | Reader and audio packaging | Local reader HTML has exact release record; reader-format probes exist for EPUB/DOCX/PDF | EPUB, DOCX, PDF, e-reader, audio, and audio-embedded EPUB are still unapproved. |
| Phase 9 | Externalization and contribution extraction | Deferred | Does not block v1.0. |

## Current Release Classification

- Release classification: tagged v1.0.0 living-book evidence-and-reader release boundary.
- Source tag: `v1.0.0`.
- Source commit: `96d0ca3c6b62f3530202535573941b1f6e50a83d`.
- GitHub Release: `https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0`.
- Living-book release record: `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`.
- Reader artifact classification: one reviewed local generated reader HTML
  artifact has an edition release record; other formats are blocked.
- Evidence classification: all chapter core claims remain at `argument`.
- Accepted upward transitions: `living-book-methodology.phase5_harness_registry_runner`
  and `resource-economics.costed_route_budget_slice` as bounded
  `synthetic-test-backed` transitions, plus
  `circle-calculus.external_rope_receipt_replay` as a bounded
  `prototype-backed` imported external receipt transition; all remain outside
  chapter core claims.
- Final metadata state: tag `v1.0.0`, GitHub Release, final release citation metadata, and living-book release record exist; DOI/Zenodo archive metadata remains pending until an archive exists.
- Release-gate audit: `docs/v1_0_release_gate_audit.md` records all eleven
  Definition-of-Done gates and preserves the release residuals.

## Next Work Queue

1. Keep validation, render, Lean, and browser gates green after every roadmap
   increment.
2. Pursue the next prototype or empirical measured/replayed slice with public-safe
   command, input, output, baseline or negative control, residuals, and
   non-claims.
3. Preserve the DOI/Zenodo boundary until an archive is actually created.
4. Continue public-site quality review with manual keyboard and screen-reader
   passes if the project wants stronger accessibility claims.
5. Continue EPUB/DOCX/PDF work only through exact artifact review records and
   format-review matrix updates.

## Non-Claims

- This ledger does not create a DOI or Zenodo archive.
- This ledger does not approve EPUB, DOCX, PDF, e-reader, audio, or
  audio-embedded EPUB artifacts.
- This ledger does not promote any chapter core claim above `argument`.
- This ledger does not prove ASI capability, deployed safety, model quality,
  benchmark performance, runtime behavior, source interpretation, transfer, or
  economic outcomes.
