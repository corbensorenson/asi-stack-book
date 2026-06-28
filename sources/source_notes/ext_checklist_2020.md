# Source Note: Beyond Accuracy: Behavioral Testing of NLP models with CheckList

| Field | Value |
|---|---|
| Source ID | `ext_checklist_2020` |
| Source title | Beyond Accuracy: Behavioral Testing of NLP models with CheckList |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2005.04118, https://arxiv.org/abs/2005.04118 |
| Citation label | Ribeiro et al. (2020), CheckList |
| Published / updated | 2020-05-08 / 2020-05-08 |
| DOI | 10.48550/arXiv.2005.04118 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the behavioral-evaluation literature queue; test suites, software, and model results are not imported into this repository. |

## Thesis

CheckList belongs in the benchmark, verification-bandwidth, claim-ledger, and prototype chapters as an external reference for testing model behavior by capability and perturbation class rather than by aggregate accuracy alone. It helps the ASI Stack phrase benchmark ratchets as structured behavioral probes with visible failures.

## Mechanisms

- Organize tests by expected capability.
- Use minimum functionality tests to check targeted behavior.
- Use invariance tests to detect behavior that should not change under perturbation.
- Use directional expectation tests to check monotonic or expected output movement.

## Evidence

- The source reports behavioral-testing findings in its own NLP model settings.
- This repository has not run CheckList, imported test templates, or reproduced any failure finding.
- Use the source as external behavioral-evaluation vocabulary, not as evidence that ASI Stack tests cover real model behavior.

## Failure Modes

- Behavioral test templates can miss deployment-specific hazards.
- Passing a capability matrix can still hide source-use, authority, or context-adequacy failures.
- Human-designed tests can become stale when models learn the test style.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to ground benchmark-ratchet language about targeted behavioral probes and failure-preserving test matrices.
- Do not claim local CheckList execution, behavioral coverage, or model-quality evidence.
- Keep support state at `argument` until local behavioral tests and evidence records exist.

## Open Questions

- Which ASI Stack chapter claims need minimum-functionality, invariance, and directional expectation tests?
- How should failure discoveries be preserved in the claim ledger after a model improves?
- What generator should create fresh perturbation families without leaking the holdout?
