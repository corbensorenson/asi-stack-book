# External AI Review Remediation Program

Status: coherence remediation release completed 2026-07-10; remaining book-depth work is governed by `docs/asi_stack_completion_roadmap.md`.

This document converts a user-supplied, browser-assisted ChatGPT review into a
bounded remediation program. The review is useful review input. It is not an
independent human review, external evidence, proof, benchmark evidence,
publication approval, or a support-state transition.

The raw review remains outside the public repository. The inspected input had
561 lines, 4,178 words, and SHA-256
`a8df4487473913eaf3f6fb5b0ca71cdd1ba79d476d8090583350f5720aae89ec`.
This file paraphrases its actionable findings rather than publishing the raw
text or presenting its wording as an external source.

## Review of the Review

The review is unusually good. Its strongest diagnosis is that the project's
most mature contribution is its evidence and release discipline, which makes a
record/reality disagreement especially damaging. It also correctly separates
finite Lean specifications from runtime assurance, recognizes the value of the
source-note system, and focuses the next empirical program on one governed
end-to-end trace rather than additional breadth.

The review is not treated as automatically correct. Its factual snapshot was
checked against the current worktree, a fresh local render, and the public
GitHub Pages output on 2026-07-10.

| Check | Current audit result |
|---|---|
| Active manifest | 54 chapters; 54 unique IDs; 54 unique titles; all 54 chapter files present. |
| Source inventory | 271 public-safe records. |
| Chapter-core support states | 54 of 54 remain `argument`; no chapter-core support state was changed by this intake. |
| Proof envelope | 225 proof targets; 13 classified as adequate finite-record invariants and 139 as useful but too narrow. The new combined trace target remains in the useful-but-too-narrow class. |
| Local validation | Canonical-status, schema, validator-coverage, trust-surface, publication-surface, and rendered-site checks pass; the full-book gate is rerun after each coherence change. |
| Fresh local HTML | 67 expected book pages render, including all 54 chapters; sidebar order/titles/URLs match the manifest, each chapter has one H1, and active public count claims now agree at 54 chapters and 271 sources. |
| Public deployment | The negative re-audit at `2026-07-10T15:45:29Z` is preserved in `docs/external_ai_review_live_reaudit_2026-07-10.md`. The replacement chain succeeded for merge commit `68b0902ea1b3cc29ef0f9ffb48933ed96e17500d`: build run `29108462406` passed, deploy/attest run `29108700945` consumed the run-bound artifact without rebuilding, and both CI and a fresh local crawl attested 54 chapters, 271 sources, canonical status, `/latest/`, the version index, and all three product routes. |
| Duplicate first chapter | Not reproduced as a navigation defect. The live sidebar contains one link for each of 53 chapter URLs; the repeated visible title comes from normal sidebar, breadcrumb, and page-heading presentation. |
| Count contradiction | Reproduced in the reviewed baseline and repaired locally. The new relational validator rejects stale active counts and permits older counts only under explicit historical scope; deployment remains pending. |

The review's older 44/217 and 53/249 observations are therefore partly stale,
but the underlying coherence critique is accepted. The correct response is not
to dismiss the review because the numbers moved; it is to make stale active
numbers structurally impossible.

## Finding Dispositions

Every negative critique is retained below. `accepted` means the weakness is
currently observable or its proposed control is clearly warranted. `partly
accepted` means the direction is valid but part of the reported factual state
has changed. `not reproduced` means the specific defect was not observed and
must not be repeated as fact. `decision required` identifies a product or legal
choice that should not be silently made by automation.

| ID | Critique | Disposition | Evidence or reason | Closure condition |
|---|---|---|---|---|
| R01 | Public release state is incoherent. | closed by deployed coherence release | The negative legacy observation remains recorded. Merge commit `68b0902ea1b3...` passed build `29108462406` and deploy/attest `29108700945`; the public canonical status identifies that exact clean commit, 54 chapters, 271 sources, live profile, and the manifest-derived order. | Reopen on any future source/artifact/deployment disagreement; the generated invariant, not this one success, is the durable control. |
| R02 | Trust validation checks required phrases but misses contradictory stale phrases. | accepted, P0 | `validate_trust_surface.py` proves current phrases occur but does not extract and reject all incompatible active counts. | A contradiction detector enumerates every active count occurrence, classifies historical snapshots explicitly, and fails any unscoped mismatch. |
| R03 | The project lacks one generated canonical status object. | accepted, P0 | Counts are derived in several scripts and embedded in prose rather than emitted as one build record. | A schema-validated generated status object contains active line/version, source commit, tree state, chapter/source counts, claim distribution, transition counts, build timestamp, and release profile. |
| R04 | Generated snippets do not control all active status surfaces. | closed for the coherence release; invariant remains active | README, landing, candidate-status, and publication-readiness surfaces each contain exactly one canonical-builder-owned block; validation rejects missing, duplicate, stale, or hand-edited blocks and contradictory surrounding prose. Rendered navigation derives from `book_structure.json` and is checked against canonical status. The successful deployed crawl observed the generated fields and graph. | Reopen on any generated-block, navigation, count, or historical-scope drift. |
| R05 | Clean render and deployed-site integrity are under-specified. | closed by clean tested build and deployed crawl | Build `29108462406` rendered from an empty directory, generated status/products/channels, validated the graph and Human view, and uploaded a commit-bound bundle. Attest run `29108700945` crawled the deployed URLs, order, H1/navigation identity, commit marker, and product/status surfaces. | Reopen on any failed clean render, bundle validation, deployment, or deployed crawl. |
| R06 | Immutable releases and a moving latest surface are not cleanly separated. | policy implemented; v1.0.0 backfill explicitly declined | The tested build creates a byte-equivalent `/latest/` mirror before hashing. `/versions/index.json` is metadata, not archival storage. The deterministic archive builder/validator rejects wrong commits, false publication, changed bytes, and path traversal. The author declined a v1.0.0 full-site backfill because a later render would not be the historical tested site. The v1.0.0 row remains honestly unpublished; immutable full-site archives begin with the next eligible clean tag. | Observe `/latest/` and the version index in deployed attestation; at the next eligible tagged release, publish/redownload/digest-check the first immutable full-site asset and record its exact URL/digest. |
| R07 | Lean work may be read as more assurance than it provides. | partly accepted | The repository already publishes proof-adequacy limits, but theorem totals remain prominent and most targets are narrow. | Public proof headlines lead with adequacy class and claim scope; four selected trace invariants are deepened and connected to runtime records. |
| R08 | Several validators are policy linters or executable documentation rather than semantic verification. | high-impact exact contract audit implemented; long-tail audit remains | `validation/unit_contract_overrides.json` gives the highest-impact coherence, deployment, supply-chain, release, evidence-quality, reviewer, decision/review, product/contribution, vertical-slice, trace-invariant, proof-manifest, schema, publication, and registry units exact input artifacts, output assertions, mutation cases, claim scope, and prohibited inference. All other units retain explicit class-level limits. Every override is labeled internal and not independent. | Progressively replace inherited metadata on long-tail units and preserve exact prohibited-inference language; exact contracts and mutation tests still do not prove validator completeness or independent adequacy. |
| R09 | `validate_book.py` is an overgrown hard-coded inventory. | migration complete: registry is sole inventory and execution authority | `validation/registry.json` owns 734 unique required artifacts and 238 ordered units. `validate_book.py` was reduced from 1,350+ lines to a 418-line structural base gate, loads required artifacts from the registry, and contains no child-validator list or dispatcher. The registry maintainer no longer parses Python. The registry validator rejects legacy list/dispatcher/environment markers, duplicate order, missing scripts, unresolved overrides, and any legacy authority field. | Observe the sole-source design in CI and maintain changes directly in the registry; no second inventory may be introduced. |
| R10 | CI correctness, deep verification, and deployment are too tightly coupled. | closed by observed commit-bound handoff | Pull-request, scheduled deep, manual major-release, tested Pages build, deployment, and post-deployment attestation have distinct triggers and authorities. Build `29108462406` uploaded the tested bundle; workflow-run `29108700945` downloaded that exact run-ID-bound artifact, verified commit and bytes, deployed without rebuilding, and passed attestation. | Reopen if deploy can rebuild, accept a non-successful or mismatched run, or bypass artifact/commit checks. |
| R11 | CI supply-chain pinning is weaker than the book's own standard. | immutable pins, Node 24 refresh, and fail-closed review-age inventory implemented | Every workflow action uses a full commit SHA with tag context; the first PR run exposed GitHub's Node 20 deprecation shim, so checkout, setup-python, setup-node, upload-artifact, and download-artifact were reviewed against official releases and moved to Node 24 commits before merge. Elan remains commit- and SHA-256-bound. The inventory rejects unregistered, mismatched, expired, mutable, and duplicate pins. | Perform the governed upstream review by 2026-10-08 and keep runner images, transitive packages, hosted infrastructure, and networks as explicit residual TCB. |
| R12 | The landing trust surface is administratively overloaded. | compact surface implemented and visually reviewed | README and landing keep canonical counts, core-claim state, non-state, product choice, and audit links while routing transition IDs, hashes, theorem IDs, and fixture detail to owning ledgers. A clean local render was inspected at 1280×720 with no horizontal overflow; the product selector was moved above the hero after visual review showed it began 1,257 px down. `docs/landing_visual_review_2026-07-10.md` records the review and residuals. | Preserve the compact hierarchy, keep fixture/theorem detail one click deeper, and complete the author-controlled accessibility and layout pass before final release. |
| R13 | The full chapter template is tiring as continuous reading. | bounded narrative derivative implemented; authorial completion pass remains | `products/narrative_product_spine.json` selects a canonical-order 15-chapter thesis-to-method route. Every selected chapter has a reader question, running example, strongest objection, failure story, evidence-changing condition, and handoff. `build_reader_edition.py --narrative-spine ...` generates only those chapters, hides the live scaffold, applies relevant overlays, and routes the other 39 chapters to the reference. The continuity audit still has 0 high-priority and 1 medium-priority heuristic row. | Complete author-controlled continuity, repetition, accessibility, figure, and final-format passes; a generated candidate and heuristic continuity are not release approval. |
| R14 | The project conflates one product with three. | executable separation deployed; authorial product completion remains in roadmap | The deployed Narrative route indexes 15 chapters and preserves 39 reference-only routes; Architecture Reference indexes all 54 chapters; Evidence Registry publishes 17 content-addressed routes. All three public URLs returned 200 and passed the deployed graph contract. | Complete the author-controlled narrative/reference/registry quality work in the canonical roadmap; generated separation does not approve a reader release, deployed AI stack, or independent evidence registry. |
| R15 | The `ASI` title creates a credibility tax. | author selected retain-brand/reframe; migration deployed | The active title is **The ASI Stack: A Governed Systems Architecture for Advanced AI, with ASI as the Stress Case**. Source, current citation, repository description, rendered site, and public deployment now use the stress-case framing; historical v1.0.0 citation records retain the former subtitle. | Preserve the migration and non-claims; positioning creates no ASI, safety, novelty, or readiness evidence. |
| R16 | A stack need not imply multiple models or physically separate cognitive modules. | substrate-neutral responsibility contract implemented | The opener now defines a layer as a logical responsibility/authority boundary and explicitly permits one model across roles, several implementations behind one role, or monolithic, modular, hybrid, and human/AI substrates when handoffs remain enforceable. The integrated trace, source-of-truth outline, glossary, and control-plane figure repeat the boundary. `validate_substrate_neutral_stack.py` rejects one-model-per-layer language. | Preserve the invariant during future diagrams and prose edits; it is conceptual scope clarification, not empirical proof that every substrate can enforce the contracts. |
| R17 | Records can become governance theater. | accepted, flagship empirical gap | Rich records do not prove faithful effects or competent verification. | Vertical slice measures false attestations and includes independent effect observation, challenge sampling, adversarial receipts, reconciliation, tamper evidence, and reviewer separation. |
| R18 | Scalar support states hide multidimensional evidence quality. | full core-claim vector migration implemented | `evidence_quality/core_claim_vectors.json` covers all 54 chapter-core claims across independence, reproducibility, recency, coverage, adversarial strength, validity, artifact access, and transfer distance. It is generated from authoritative dispositions, preserves all claims at `argument`, exposes unknown/absent evidence, and prohibits numeric aggregation or automatic support derivation. Claim and transition schemas accept optional vector references for backward-compatible adoption. Four mutation controls reject dimension omission, scalar scoring, summary forgery, and automatic promotion effect. | Future accepted transitions must populate before/after vector refs and dimension deltas; current vectors expose gaps but do not independently validate their own rationales or produce missing evidence. |
| R19 | Governance overhead is not quantitatively justified. | accepted, flagship empirical gap | Existing resource/governance-tax work is bounded and not a real matched workload. | Vertical slice compares governed and simpler baselines on success, unsafe effects, false accepts/rejects, cost, latency, operator burden, rollback, and residual discovery. |
| R20 | A named human owner does not establish qualified or available oversight. | reviewer-capacity contract implemented; external roles deferred by author policy | `governance/reviewer_capacity_registry.json` separates assignment, competence scope, independence, conflicts, measured load, response/expiry, escalation substitute, review-quality measurement, authority ceiling, and unavailable behavior. The internal owner is explicitly non-independent with unmeasured load/quality. Formal-methods, safety/governance, and systems/editorial roles are deferred until post-publication and cannot be used to claim independent oversight. | Preserve the distinction between author authority and independent review. No external-human capacity is required for prepublication completion, and no independent-review claim may be made. |
| R21 | Breadth and coined terminology exceed defended contribution depth. | three-contribution contract implemented | `products/contribution_focus_contract.json` constrains deep work to governed-cognition interface contracts, public claim-state transition discipline, and record/reality plus residual honesty; all 54 chapters have one assignment, 11 are primary owners, 43 support or integrate, and 0 are independent chapter flagships. | Defend the three program claims through source-noted prior art, empirical lanes, bounded formal work, objections, and residuals; the assignment map is scope control, not novelty proof. |
| R22 | One real end-to-end vertical slice is missing. | local execution implemented; deployed/generalization boundary open, P1 | `governed_repository_change_slice` executes actual disposable Git mutations, tests, independent effect observation, commits, refusals, rollback, and quarantine. Against the simple matched route it records eight baseline false accepts, zero governed false accepts, zero governed unsafe releases, and three rollback attempts across the eight required attacks. | Re-execution and tracked validation pass locally; an independently operated or deployed replay is still required before broad system claims, but not before the book can finish with a bounded local claim. |
| R23 | Cross-stack formal invariants need deeper trace, timing, and concurrency semantics. | bounded local trace implementation complete; deployed/distributed generalization open, P1 | `governed_trace_invariants` derives authority monotonicity, revocation-before-effect with a revocation-wins tie rule, evidence-transition integrity, residual conservation, and causal order from the executed repository-change log; Python and `AsiStackProofs.GovernedRepositoryTrace` reject one mutation per invariant. | Local re-derivation, all mutations, proof-manifest linkage, and Lean build pass; distributed clocks, deployed enforcement, residual completeness, and evidence validity remain explicit open-world limits rather than prepublication review gates. |
| R24 | Independent external review is missing. | closed as a prepublication requirement by explicit author policy | Formal-methods, safety/governance, and systems/editorial packets remain preserved for optional post-publication use. Roles are `deferred_postpublication`; issue #1 was closed `not_planned` on 2026-07-10 with no reviewer outreach, evidence transition, or approval. | Preserve the explicit non-claim that no independent review occurred. A later post-publication review may reopen work but is not required for completion. |
| R25 | All-rights-reserved licensing constrains reuse and adoption. | delayed opening selected; current operative rights intentionally reserved | `governance/licensing_decision.json` selects delayed opening. The 2,219-path deterministic inventory clears zero paths, so the drafting repository remains all-rights-reserved and prepublication contributions are closed. At the first author-declared completed major release, cleared author-owned prose/figures are intended for CC BY 4.0 and cleared software-like artifacts for Apache-2.0; metadata and mixed/imported/local/third-party material remain reserved unless separately cleared. | Before the completed release, resolve ownership/exceptions, install exact texts/notices/routing, and snapshot the rights state atomically. The selection is not a present open-license grant or legal conclusion. |
| R26 | The project needs to follow its own roadmap instead of continuing scope growth. | accepted governance rule | Recent work improved completeness but also increased active chapter count. | Freeze new chapter additions until P0 coherence closes and any exception names the critique it closes, the owning chapter, and the removal/defer alternative considered. |

## Program Order

### P0 — Coherence release

No new chapter may be added during P0 unless it is the only defensible owner of
a remediation invariant and an explicit add-or-reject review approves it.

1. Define the canonical status schema and deterministic build procedure.
2. Generate active status snippets and replace hand-maintained active counts.
3. Add semantic contradiction detection with explicit historical-snapshot
   annotations rather than a blanket ban on old numbers.
4. Render from an empty output directory and validate the local site graph.
5. Split tested artifact creation from deployment and add post-deployment
   attestation.
6. Publish immutable-version versus moving-latest URL and release-record rules.

P0 is complete only when the same source commit produces one chapter order,
one chapter count, one source count, one claim distribution, one release
profile, and one discoverable version across source, local render, uploaded
artifact, and deployed site.

### P0 implementation ledger

| Control | Current state | Evidence | Remaining closure work |
|---|---|---|---|
| Canonical status object | implemented and observed publicly | `status/public_status_config.json`; public `/status/canonical-public-status.json`; build `29108462406`; attest `29108700945` | Reopen on source/public disagreement. |
| Active contradiction detection | generated blocks plus relational contradiction checks implemented | `scripts/validate_public_status_consistency.py`; four canonical-builder-owned surface blocks; chapter-header global-count exclusion; historical reader scope | Observe the same blocks and graph in a clean tested bundle and deployed attestation. |
| Clean rendered graph | implemented in release CI; passed locally on the 67-page render | `.github/workflows/publish.yml`; `python3 scripts/validate_public_status_consistency.py --site _site` | CI must produce the clean `tested_commit` attestation. |
| Post-deployment attestation | implemented and passed | deploy/attest run `29108700945` crawled canonical status, landing sidebar, 54 chapter URLs, H1 shape, and product/status routes after deploying the exact build-run artifact | Reopen on any future failed attest job or fresh-crawl disagreement. |
| Immutable versus moving URLs | full moving mirror plus deterministic tested-bundle archive builder/validator implemented; archive not fabricated | `status/versioned_release_policy.json`; `docs/versioned_release_channels.md`; `docs/immutable_site_archive_pipeline.md`; `scripts/build_immutable_site_archive.py`; `scripts/validate_immutable_site_archive.py` | Run the builder on the authorized clean tag bundle, publish/redownload it, and record the exact URL/digest; deployment observation remains required. |

No P0 item changes a chapter-core support state. R01, R04, R05, and R10 closed
for the observed coherence release. R06 closes the historical v1.0.0 decision
without claiming a site archive; the first real immutable full-site archive is
a future eligible-release task.

### Latest local verification — 2026-07-10

- PR tier: structural base plus 21 units passed.
- Deep tier: structural base plus 214 units passed.
- Registry: 238 ordered units, 734 required artifacts, and 21 exact
  high-impact contracts passed its sole-authority checks.
- Lean: 66 jobs passed in the latest proof build recorded by this remediation
  run; proof scope remains finite and claim-bounded.
- Clean HTML: all 67 book pages rendered from an empty `_site/` after the
  interrupted-render residue was removed and the original render session was
  allowed to complete.
- Products: 15 narrative chapters, 39 explicit reference-only routes, all 54
  reference chapters, and 17 evidence routes passed source and rendered-site
  validation; content snapshots matched their SHA-256 records.
- Browser: 112 chapter/appendix viewport pairs passed Human-view checks.
- Diagnostic tested bundle: 259 files passed full content-addressed bundle
  validation. Exact bytes and tree digest remain in the generated bundle
  manifest rather than this source because this document is itself a published
  registry snapshot inside that bundle. The bundle is marked dirty/local and
  is not a deployable release artifact.

The clean GitHub build, run-bound deployment, and post-deployment crawl now
supplement these local results. They do not create an immutable v1.0.0 site
archive, independent human review, or evidence for the chapter-core claims.

### P1 — One governed vertical slice and four deep invariants

The initial workload is a bounded repository code change. It must include:

- intent and authority scope;
- command contract and plan DAG;
- source-bound context packet;
- route selection and independent verification;
- sandboxed execution, diff, and tests;
- evidence and residual updates;
- rollback; and
- final release or refusal.

Required adversarial cases are retrieved-context prompt injection, stale
authorization, revocation during execution, forged or mismatched receipt,
correlated proposer/verifier, hidden residual cost, failed rollback, and a
cheaper route that violates a safety constraint.

The same event vocabulary must feed executable checks and the four deeper
trace models: authority monotonicity, revocation-before-effect,
evidence-transition integrity, and residual conservation.

### P1 — Product and contribution focus

The three products are:

1. a narrative technical book;
2. an architecture reference specification; and
3. an evidence, proof, and release registry.

The three defended contribution tracks are:

1. governed-cognition interface contracts;
2. public claim-state transition discipline; and
3. record/reality plus residual honesty.

Verification bandwidth and governance economics are the shared empirical lane.
Every other chapter must state which product and contribution it serves; it is
not an independent flagship by default.

### P1/P2 — Validation, review, and licensing

- Migrate the hard-coded validation inventory to a declarative registry with
  parity checks before deleting existing orchestration.
- Generate PR, nightly/deep, and release/deploy execution plans from the
  registry.
- Pin the CI supply chain immutably and document controlled upgrades.
- Preserve three specialist packets for optional post-publication use without
  prepublication outreach or a release gate.
- Enforce the selected retain-brand/reframed-subtitle and delayed-opening
  decisions without changing claim support.

## Closure Ledger Requirements

Each finding must eventually record:

- current disposition;
- owning artifact and owner role;
- implementation or decision references;
- negative controls;
- commands actually run;
- local and deployed results where applicable;
- residual risks;
- support-state effect; and
- exact non-claims.

A critique is not closed because a field or document exists. Closure requires
the relevant global invariant, behavior, measurement, review, or explicit
human decision named in the table above.

## Non-Claims

- This program does not establish that every review observation is correct.
- This program does not treat an AI-generated review as independent human
  review or external evidence.
- Passing repository validators does not close the release-coherence finding
  while the deployed site or active prose disagrees.
- The current 54 chapter-core claims remain at `argument`.
- This program records author authorization for the reframed active title,
  delayed-opening policy, no-v1.0.0-backfill decision, and deployment of the
  current remediation release. It does not authorize support-state promotion,
  private-source publication, a new release tag, or chapter addition.
