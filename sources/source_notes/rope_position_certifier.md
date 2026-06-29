# Source Note: Proof-Carrying RoPE Position Distinguishability

| Field | Value |
|---|---|
| Source ID | `rope_position_certifier` |
| Source title | Proof-Carrying RoPE Position Distinguishability |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project source text; raw source text is not copied here |

## Thesis

The RoPE position-distinguishability paper ships an externally usable proof-carrying contract for rotary-position configurations. It separates exact integer-period or discretized phase-bank distinguishability, finite-margin certificates, numerical real-phase diagnostics, and explicit non-claims about model quality, context length, speed, memory, and deployment readiness.

## Mechanisms

- Model one declared phase channel as `position mod period` and a phase bank as a list of residues.
- Characterize exact bank collisions by divisibility of the position gap by every declared period.
- Use common collision gaps, bounded prefix reports, selected-subfamily pass reports, count fields, theorem ids, and machine-readable certificates to make position-bookkeeping auditable.
- Provide public commands for RoPE-style certifier runs, exact-only phase-bank certifier runs, named presets, JSON output, and sidecar result regeneration.
- Label real-valued RoPE margin scans as numerical diagnostics rather than Lean proof over real-valued trigonometric RoPE.

## Evidence

- The source is a proof-linked AI application paper with theorem spine, certifier interface, preset-result sidecars, exact discrete model, real-phase diagnostic discussion, proved core, and guardrail.
- It states that exact discrete preset rows are reproducible configuration certificates rather than evidence of better perplexity, reasoning, context length, runtime, memory, training stability, or deployment readiness.
- The source includes theorem-linked positive and negative boundaries for the exact/discretized contract layer.
- This source note itself did not run a RoPE certifier command, sidecar regeneration, or Circle Lean build from the ASI Stack repo. A later bounded external receipt slice is recorded separately in `docs/circle_external_receipt_slice.md` for one local rope-position contract replay; that slice keeps model-quality, context-length, speed, memory, training-stability, and deployment claims out of scope.

## Failure Modes

- Treating integer-period/discretized phase-bank results as proof about arbitrary real-valued RoPE behavior.
- Treating a passing certifier as evidence that a model improves or has extended usable context.
- Omitting assumptions, theorem ids, exact collision counts, margin status, or explicit non-claims from downstream receipts.
- Using numerical real-phase margin scans as formal proof.

## Book Chapters Supported

- `circle-calculus-and-proof-carrying-ai-contracts` (Circle Calculus and Proof-Carrying AI Contracts)
- `coilra-multicoil-rope-and-cyclic-mixers` (CoilRA, MultiCoil RoPE, and Cyclic Mixers)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)

## Claims To Add Or Update

- The source can support source-derived discussion of proof-carrying position-bookkeeping contracts and the boundary between exact/discretized proof and numerical diagnostics.
- It should not be used to claim model-quality, context-length, speed, memory, or deployment-safety gains.

## Open Questions

- Should the ASI Stack proof envelope include a small independent RoPE-style finite-period theorem?
- Which receipt fields are essential for downstream architecture chapters?
- How should exact/discretized proof be presented without confusing it with full real-RoPE guarantees?
