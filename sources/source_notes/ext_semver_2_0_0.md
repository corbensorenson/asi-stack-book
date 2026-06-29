# Source Note: Semantic Versioning 2.0.0

| Field | Value |
|---|---|
| Source ID | `ext_semver_2_0_0` |
| Source title | Semantic Versioning 2.0.0 |
| Ingestion date | 2026-06-29 |
| Source version / URL | SemVer 2.0.0 specification, https://semver.org/spec/v2.0.0.html |
| Citation label | Semantic Versioning (2013), SemVer 2.0.0 |
| Published / updated | 2013 / 2026 |
| Ingestion basis | Public SemVer specification page inspected for the SCF external-positioning queue; no package manager, API compatibility checker, or version policy implemented in this repository. |

## Thesis

Semantic Versioning is an external comparator for public API compatibility and breaking-change signaling. It helps position the SCF field-version and interface-contract ideas against a familiar versioned-interface discipline, while SCF adds authority, qualification, evidence, evaluator, and rollback fields that SemVer does not supply by itself.

## Mechanisms

- Use major, minor, and patch version components.
- Treat a declared public API as the compatibility boundary.
- Signal incompatible public API changes with a major version increment.
- Separate compatibility signaling from implementation behavior.

## Evidence

- The source is an official specification for version labeling and compatibility semantics.
- This repository has not implemented SemVer enforcement, API diffing, package compatibility tests, or release-policy automation for SCF.
- Use it as a versioned-interface comparator, not as evidence that SCF replacement behavior is safe.

## Failure Modes

- Version numbers can be correct while behavior, authority, or evidence changes are unsafe.
- Public API compatibility does not imply evaluator integrity, route permission safety, or rollback readiness.
- Breaking-change signals can be missing, ignored, or insufficient for high-risk capability changes.
- Version compatibility can be mistaken for semantic capability preservation.

## Book Chapters Supported

- `stable-capability-fields` (Stable Capability Fields)

## Claims To Add Or Update

- Use SemVer as a narrow comparator for field versions and public interface contracts.
- State that SCF requires more than version compatibility: authority ceilings, qualification leases, evidence refs, evaluator policy, lifecycle state, and rollback obligations.
- Do not claim automated compatibility checking or safe replacement until tests exist.

## Open Questions

- Should SCF field versions adopt SemVer-like breaking-change categories or a stricter governance-specific version scheme?
- What validator should reject a replacement whose version looks compatible but changes authority?
- How should deprecated or retired SCF versions be represented in reader and AI/research editions?
