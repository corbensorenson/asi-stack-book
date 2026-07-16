# Model-adequacy dossier: Artifact record-reality refinement

## Ownership

- Chapter: `artifact-graphs-audit-logs-and-replay`
- Frozen targets: all ten `lean:artifacts.graph.*` targets
- Stronger model: `lean/AsiStackProofs/ArtifactRealityRefinement.lean`
- Independent consumer: `scripts/validate_artifact_reality_refinement.py`
- Result: `experiments/artifact_reality_refinement/results/2026-07-15-local.json`
- Support-state effect: exactly `none`

## Reachable model

The model owns one artifact-specific event sequence from exact registration
through provenance binding, replay validation, independently challengeable
reality cross-check, epistemic trusted-base binding, revocation closure, and
consumer-acknowledged admission. It deliberately prevents a schema-valid
receipt, replay label, attestation, or named verifier from skipping the next
gate or assigning support.

## Consequences, countermodels, and consumer

General consequences preserve artifact, content, parent, source, context,
transaction, and certificate identity and prevent support assignment or
external-effect counts from changing. Each accepted step adds exactly one
receipt. Countermodels reject parentage and provenance gaps, stale certificates,
unvalidated replay, missing observations, dependent cross-checks, unbounded
attestation, self-verifier laundering, missing recursion stops, and incomplete
revocation closure. A six-event witness reaches admission with one represented
reality observation, six receipts, zero assigned support, and zero effects.

The independent consumer covers all thirty-three routes, consumes eight exact
bounded suites, and rejects 53 mutations across identity, lineage, ordering,
authority, provenance, replay, observation, cross-check, trap, attestation,
trust-base, recursion, residual, revocation, and consumer boundaries.

## Assumptions, exclusions, and adequacy verdict

Identifiers, digests, reference-presence flags, replay-grade judgments,
certificate status, replay-validation results, observed-artifact flags,
cross-check and trap outcomes, attestation limits, trust roots, verifier-
independence labels, recursion stops, residuals, revocation closure, and
consumer acknowledgments are trusted inputs. The model is adequate for exact
represented lifecycle custody, route priority, receipt accounting, and
authority separation. It is inadequate for open-world provenance, causal
truth, artifact/source/content correctness, replay semantics, verifier
correctness, external independence, root security, repository completeness,
deployed propagation, natural workloads, usefulness, causality, safety,
reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Retire the produced-artifact projection and seven generic authored fixture-
summary bridges in `AsiStackProofs.ArtifactGraph`. Retain the missing-reference,
provenance, replay-grade, nineteen artifact-admission, nine replay-packet, and
three record-reality sequence consequences at bounded legacy scope. Move all
ten public targets to the refinement module. No support state changes.
