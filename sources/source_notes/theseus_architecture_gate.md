# Source Note: Theseus Architecture Gate

| Field | Value |
|---|---|
| Source ID | `theseus_architecture_gate` |
| Source title | Theseus Architecture Gate |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project checkout source text; raw source text is not copied here |

## Thesis

The Theseus architecture gate is a pre-training promotion check. It prevents heavy local training from starting until the ratchet, routing, safety, residual, benchmark, procedural-tool, memory, lifecycle, and external-inference boundaries are coherent.

## Mechanisms

- Run a gate report directly or at the end of the compiled ratchet.
- Check ratcheting completion, RMI completion, ORA completion, rule-router evaluation, learned router-head promotion, safety ledger, regression suite, public calibration, residual escrow, bridge benchmark, procedural tools, routing memory, arm lifecycle governance, and external-inference zero.
- Treat failed gates as ratchet residuals.
- Re-run after architecture changes, frontier updates, or arm lifecycle changes.
- Treat the gate as necessary but not sufficient; longer runs also require training preflight, candidate promotion gate, and resource-governor agreement.

## Evidence

- The source is a short gate-definition and usage note.
- It reports a current gate snapshot with ready-for-heavy-training true, 14/14 checks passed, and zero external inference calls.
- A later ASI Stack import, recorded in `docs/theseus_report_import_slice.md`,
  verifies one public-safe static architecture-gate report fixture by digest and
  expected-invalid controls. That import is not a clean live Theseus rerun and
  does not promote chapter core claims.

## Failure Modes

- Treating a green architecture gate as sufficient for deployment or broad safety.
- Starting heavy training after stale gate state, architecture changes, or lifecycle changes.
- Hiding failed gates instead of turning them into residuals.
- Allowing external inference leakage to pass as local training evidence.

## Book Chapters Supported

- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores; includes folded MoECOT Runtime Crosswalk)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `project-theseus-as-report-first-implementation-reference` (Project Theseus as Report-First Implementation Reference)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- The source can support source-derived discussion of readiness gates as pre-training controls and residual-producing promotion checks.
- It should not be used to claim current readiness unless the latest report artifacts are inspected or regenerated; the static ASI-side import supports only bounded implementation-reference discussion.

## Open Questions

- Should the book define a minimal gate schema for architecture promotion?
- Which gate predicates are candidates for Lean invariants, and which are operational report checks?
- How should stale gate state be represented in the claim/evidence matrix?
- What clean Project Theseus release or archive should replace the current static digest import for stronger replay evidence?
