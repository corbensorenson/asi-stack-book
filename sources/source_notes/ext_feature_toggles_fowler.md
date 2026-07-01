# Source Note: Feature Toggles (aka Feature Flags)

| Field | Value |
|---|---|
| Source ID | `ext_feature_toggles_fowler` |
| Source title | Feature Toggles (aka Feature Flags) |
| Ingestion date | 2026-07-01 |
| Source version / URL | https://martinfowler.com/articles/feature-toggles.html |
| Citation label | Hodgson (2017), Feature Toggles (aka Feature Flags) |
| Published / updated | 2017-10-09 / 2017-10-09 |
| Ingestion basis | Public Martin Fowler site article inspected for feature-flag and canary-release vocabulary; no feature-flag service, toggle router, cohort assignment, or production release was implemented from this repository. |

## Thesis

Feature toggles are an external comparator for controlled exposure and release decoupling. They support the replacement chapter's distinction between candidate availability, scoped canary exposure, ordinary default use, and retirement. The ASI Stack should borrow the controlled-exposure pattern while making every toggle-like replacement state accountable to authority, evidence, residual, rollback, and non-claim records.

## Mechanisms

- Decouple code deployment from feature exposure.
- Use release, experiment, ops, and permissioning toggles for different operational purposes.
- Use canary releasing to expose a change to a small cohort before broader rollout.
- Treat toggle configuration as a managed operational surface rather than hidden conditional logic.
- Recognize that feature flags add validation and carrying-cost complexity.

## Evidence

- The article presents feature toggles as a technique for changing system behavior without deploying new code and organizes toggle usage into release, experiment, ops, and permissioning categories.
- It explicitly includes canary releasing, A/B testing, static and dynamic toggles, long-lived and transient toggles, and validation complexity.
- This repository has not implemented a toggle service, cohort router, feature-flag test matrix, or live canary release.

## Failure Modes

- Feature flags can create invisible state space and validation burden.
- Long-lived toggles can become debt or undeclared policy.
- A toggle can control exposure without proving that the replacement preserves semantic field identity, regression floors, authority boundaries, or rollback solvency.
- Canary exposure can be read as safety evidence even when cohort selection, metrics, and negative controls are weak.

## Book Chapters Supported

- `capability-replacement-and-rollback` (Capability Replacement and Rollback)

## Claims To Add Or Update

- Use this note to ground the chapter's distinction among shadow, canary, default-candidate, default, retired, and blocked states.
- Name feature flags as a prior controlled-exposure pattern, then explain why ASI Stack replacement requires stronger transaction records than ordinary release toggles.
- Do not claim a working feature-flag platform or release-management system.

## Open Questions

- Should future replacement fixtures include an explicit cohort/exposure policy field, separate from authority scope?
- Which toggle categories map cleanly to replacement states, and which should remain deployment-only analogies?
- What validation matrix is needed to prevent toggle-state explosion from hiding regressions?
