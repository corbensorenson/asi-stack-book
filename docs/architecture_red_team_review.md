# Architecture-Level Red-Team Review

Date: 2026-06-29

This is a public-safe desk red-team review for the v1.0 release gate. It attacks the ASI Stack as a composed architecture, not as isolated chapter mechanisms. It does not run a deployed ASI system, model, sandbox, tool adapter, benchmark, reader release, or external audit.

The review outcome is deliberately conservative: the current book has strong record discipline for many surfaces, but every scenario still has residual risk because the architecture is mostly design rationale, finite-record proofs, synthetic fixtures, and publication validators rather than a deployed runtime.

## Summary

| Scenario | Current defense class | Residual route | v1.0 disposition |
|---|---|---|---|
| Authority ladder attack | Authority records, runtime-adapter receipts, SCF/replacement gates, no-promotion coverage | Runtime adapter traces, revocation propagation, cross-layer reference trace | v1.x runtime test required |
| SCIF/context leakage attack | Context taint records, SCIF receipt fixtures, Human-view strip checks, reader overlays | Side-channel tests, redaction/declassification replay, e-reader artifact review | v1.x security test required |
| Evaluator capture attack | Evaluator-separation fields, replacement/self-improvement fixtures, proof-depth honesty | Independent evaluators, real regression suites, monitor-window traces | v1.x runtime/prototype test required |
| Support-state inflation attack | Evidence-transition schema, core-claim no-promotion ledger, status snapshot validator | External review and source-interpretation audits | v1.0 controlled, not eliminated |
| Benchmark gaming attack | Benchmark ratchet fixtures, resource-budget records, negative-control expectations | Real benchmark traces, contamination checks, hidden-cost audits | v1.x empirical test required |
| Reader-release laundering attack | Live/Human view validators, reader overlays, reader matrix, format blockers | Full application review for EPUB/DOCX/PDF and curated-reader reconciliation | v1.0 blocked until artifact review |

## Authority Ladder Attack

**Attack setup:** Chain locally valid records so each layer sees only a narrow permission: a command contract requests a benign plan node, the planner delegates to a runtime adapter, the adapter emits an authority-use receipt, a stable capability field records readiness, and a replacement or self-improvement gate treats the accumulated path as permission to widen authority.

**Expected failure:** No single record violates its local schema, but the composed path grants more end-to-end authority than the original human intent allowed.

**Observed current defense:** The book has authority-transition fixtures, runtime-adapter permission fixtures, stable-capability-field fixtures, replacement fixtures, self-improvement boundary fixtures, and finite Lean hooks for authority ceilings and non-widening transitions. The Phase 5 registry runner can replay those synthetic checks. The core-claim no-promotion gate prevents these checks from becoming a deployed enforcement claim.

**Residual risk:** The defenses are record-level and synthetic. They do not prove revocation propagation, cross-adapter enforcement, delegated approval expiry, confused-deputy resistance, or end-to-end authority conservation in a live runtime.

**Routed follow-up:** Route to the non-infrastructure measured/replayed evidence lane: a planner-to-adapter-to-receipt trace with a blocked escalation negative case. Also route to `runtime-adapters-tool-permissions-and-human-approval.core`, `system-boundaries-and-authority.core`, `stable-capability-fields.core`, and `integrated-reference-architecture.core` as future transition candidates only after real traces exist.

## SCIF/Context Leakage Attack

**Attack setup:** Feed protected context through summaries, semantic cells, residual ledgers, embeddings, tool receipts, diagrams, generated reader overlays, or source cards so restricted material is not copied verbatim but is still inferable or operationally useful outside the permitted scope.

**Expected failure:** The system passes literal text-stripping and schema checks while leaking sensitive information through derived artifacts, metadata, residual notes, or reader-edition transformations.

**Observed current defense:** The book has context transaction and taint proof hooks, context admission/adequacy synthetic fixtures, security-kernel authority-use receipt fixtures, source-publication boundaries, ignored raw source directories, Human-view stripping checks, reader-overlay validation, and reader-format blockers. The live Human view validation checks mode-specific hiding behavior after render.

**Residual risk:** The current checks do not perform side-channel analysis, embedding leakage tests, semantic declassification review, redaction adversarial review, or e-reader application inspection over exact release artifacts.

**Routed follow-up:** Route to a context-admission replay with tainted and stale packet negatives, plus a reader artifact inspection pass before any EPUB/DOCX/PDF approval. Keep `security-kernel-and-digital-scifs.core`, `context-transactions-snapshots-mounts-and-taint.core`, and reader-release artifacts at `argument` or blocked status until those tests exist.

## Evaluator Capture Attack

**Attack setup:** Let a candidate capability, policy update, benchmark ratchet, or self-improvement proposal influence the evaluator, reviewer, benchmark, hidden holdout, or proof predicate that decides whether it passes.

**Expected failure:** The system records an apparently valid promotion because the evaluator has become coupled to the candidate, losing independence while preserving the appearance of review.

**Observed current defense:** Replacement, self-improvement, stable-capability-field, benchmark anti-Goodhart, policy-optimization, and resource-budget surfaces all name evaluator separation or promotion blockers. The proof-depth report explicitly labels projection-only safety-critical hooks rather than treating them as substantive safety proofs.

**Residual risk:** The repository has no independent evaluator service, real holdout management, reviewer-independence audit, monitor-window run, rollback dry run, or adversarial attempt to corrupt evaluation inputs.

**Routed follow-up:** Route to a benchmark/policy update replay with evaluator identity separation, hidden-holdout refs, failed-candidate preservation, rollback plan, and monitor-window artifacts. Keep self-improvement, replacement, benchmark, and policy-optimization core claims at `argument`.

## Support-State Inflation Attack

**Attack setup:** Use polished prose, complete source notes, passage-reviewed mappings, passing synthetic fixtures, or finite Lean proofs as social pressure to raise support states even though no accepted transition supports the broader chapter claim.

**Expected failure:** Claims quietly move from design rationale into stronger evidence language without the correct artifact, command, limitation, counterevidence, and non-claim record.

**Observed current defense:** The evidence-transition schema distinguishes no-change, upward, downward, deprecated, and refuted transitions. `scripts/validate_evidence_transitions.py` rejects upward transitions without passing verification and bounded review fields. `scripts/validate_core_claim_decisions.py` proves every chapter core claim is covered by an accepted transition or explicit no-promotion decision. `docs/core_claim_transition_coverage.md` records zero missing core claims and all chapter core claims at `argument`.

**Residual risk:** The current controls are local maintainer-agent checks. They do not replace independent source-interpretation review, external peer review, or empirical reproduction. Prose can still over-imply strength if future edits bypass review discipline.

**Routed follow-up:** Keep validator coverage mandatory, require future support-state changes to update Appendix C only through accepted transition records, and add external review before any evidence-release label. Treat this scenario as controlled for v1.0 process integrity, not as eliminated.

## Benchmark Gaming Attack

**Attack setup:** Optimize a route, policy, steward action, generation mode, or resource-budget decision for a proxy metric while hiding residual burden, contamination, regression loss, verification cost, or human review displacement.

**Expected failure:** The system appears more efficient or more capable on a benchmark while actually increasing unpriced risk or downstream cost.

**Observed current defense:** Benchmark ratchet fixtures, generation-mode baseline fixtures, resource-budget ledger fixtures, capacity-smoothing toy traces, and no-promotion decisions require baselines, negative controls, residual accounting, and non-claim boundaries. The measured registry-runner transition is scoped to infrastructure replay only, the bounded costed-route/resource-budget transition rejects a cheaper failed negative control while preserving baseline, fallback, residual, and non-claim boundaries, and the Circle external receipt transition records discarded procedural attempts without treating the narrow receipt replay as chapter-core or deployed proof-transport evidence.

**Residual risk:** No real benchmark, route-quality measurement, model run, hidden-holdout integrity check, contamination audit, useful-solution-per-second result, or cost-quality economic review has been accepted.

**Routed follow-up:** The small synthetic costed-route/resource-budget slice and first Circle external receipt slice are now recorded; route the next follow-up to real route-quality/resource-budget traces, benchmark contamination checks, hidden-cost audits, load/serving-system measurements, public proof-contract consumer gates, or additional imported prototype receipts. Keep routing, resource economics, fast generation, benchmark ratchets, proof-contract, and policy optimization core claims at `argument`.

## Reader-Release Laundering Attack

**Attack setup:** Derive the Human view, reader manuscript, EPUB, DOCX, PDF, or audio script from the live book while stripping repeated support scaffolding, then accidentally remove a caveat that carried a meaning-critical evidence boundary.

**Expected failure:** The human-readable edition becomes smoother but more misleading, causing readers to treat argument-level architecture as implemented or validated.

**Observed current defense:** The live Human view preserves compact evidence boundaries near core claims. Reader overlays are section-anchored and validated. Generated reader chapters must preserve claim text and evidence boundaries. The reader chapter review matrix and format review matrix keep release blockers on all rows until artifact review exists.

**Residual risk:** Generated-reader checks are not a substitute for full application review. EPUB has no e-reader application approval, DOCX has no full application review, PDF has no full page-by-page layout review, and audio remains downstream of a reviewed reader edition.

**Routed follow-up:** Keep Phase 8 blocked until exact reader artifacts are reviewed and named in release records. Before curated reader graduation, require reconciliation back to live-book claims, support states, caveats, source boundaries, and implementation horizons.

## Non-Claims

- This red-team report is a desk review, not an exploit run, model evaluation, sandbox test, benchmark, source-interpretation audit, external peer review, or deployment review.
- It does not prove the ASI Stack is safe, aligned, secure, efficient, or implemented.
- It does not promote any chapter core claim above `argument`.
- It does not approve any reader, ebook, document, PDF, audio, DOI, release, or benchmark artifact.
