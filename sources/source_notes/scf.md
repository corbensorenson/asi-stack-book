# Source Note: Stable Capability Fields

| Field | Value |
|---|---|
| Source ID | `scf` |
| Source title | Stable Capability Fields |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public Release 1.0, 23 June 2026; https://docs.google.com/document/d/1hQ9LqEgpeHo2SAntUVk15Eegms_xRVfOhtndVM5TDS4 |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/scf.txt`; raw text is not published. |

## Thesis

SCF separates a capability's durable semantic identity from the replaceable machinery that realizes it. A field is a governed substitution boundary binding contracts, artifacts, profiles, state, evaluator policy, evidence, qualification, routing, authority, lifecycle events, and recovery paths.

## Mechanisms

- Stable field identity with versioned contracts and exact content-bound implementation artifacts.
- Append-only evidence and consequence registry with deterministic views.
- Scoped, defeasible, expiring qualification claims.
- Untrusted route proposer paired with a narrow validator for claims, leases, profiles, grants, state paths, and composition certificates.
- State migration solvency, canary stages, online adaptation envelopes, federation, incidents, appeals, and constitutional governance controls.

## Evidence

- The source is a research synthesis, formal architecture, executable specification fragment, and evaluation agenda.
- It includes conditional safety properties and proof sketches, but the note does not treat companion measurements as independent AI-safety evidence.
- Strong claims about production safety, global alignment, strategic deception, or reversibility remain explicitly out of scope.

## Failure Modes

- Capability slots laundering authority from one implementation to another.
- Contract drift, evaluator capture, state migration insolvency, dependency drift, bad reliance annotations, and recovery failure.
- Procedural self-ratification when candidates affect the evaluator or governance process that judges them.

## Book Chapters Supported

- Stable Capability Fields
- Capability Replacement and Rollback
- Recursive Self-Improvement Boundaries
- Routing Heads and Specialist Cores
- Readiness Gates, Residual Escrow, and Quarantine
- Policy Optimization and Learning from Feedback
- Prototype Roadmap

## Claims To Add Or Update

- Use SCF as the core governed self-improvement substrate.
- Use SCF to govern whether policy updates are promoted, quarantined, rolled back, or kept experimental, especially when an update could affect authority, evaluator policy, or lifecycle state.
- Distinguish implementation updates from contract/evaluator/governance updates.
- Formalize exact identity binding, qualification, route validation, lifecycle ordering, and authority non-escalation as priority Lean/code targets.

## Open Questions

- Which SCF executable fragment should be ported into the book repo first?
- Which qualification and route records should be represented as JSON Schemas?
- How should the public book distinguish SCF's own reported executable fragment from proofs implemented in this repo?
