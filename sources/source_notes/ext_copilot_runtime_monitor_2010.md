# Source Note: Copilot: A Hard Real-Time Runtime Monitor

| Field | Value |
|---|---|
| Source ID | `ext_copilot_runtime_monitor_2010` |
| Source title | Copilot: A Hard Real-Time Runtime Monitor |
| Ingestion date | 2026-06-28 |
| Source version / URL | Author publication page, https://leepike.github.io/pub_pages/rv2010.html |
| Citation label | Pike et al. (2010), Copilot |
| Published / updated | 2010-11 /  |
| DOI |  |
| Ingestion basis | Author publication page inspected for the runtime-monitoring queue; paper PDF, compiler, generated monitors, and embedded examples are not imported into this repository. |

## Thesis

Copilot belongs in the runtime-adapter, proof-envelope, readiness-gate, and prototype chapters as an external reference for monitor generation. It helps the ASI Stack distinguish a prose policy from a generated runtime monitor with bounded execution cost.

## Mechanisms

- Use a stream-based dataflow language for hard real-time runtime monitoring.
- Compile monitor specifications into small C programs.
- Target constant-time and constant-space monitor execution.
- Generate the monitor's own scheduler instead of relying on a real-time operating system.

## Evidence

- The source describes Copilot's runtime-monitoring language/compiler approach for hard real-time programs.
- This repository has not run Copilot, written monitor specs, generated C monitors, or tested constant-time/constant-space behavior.
- Use this source as external runtime-monitoring vocabulary, not as evidence that ASI Stack adapters enforce runtime policies.

## Failure Modes

- Monitor generation can create confidence in a property that was never specified.
- Runtime-monitor cost can interfere with the system being monitored if boundedness is not measured.
- A monitor can detect violations but still leave rollback, quarantine, or residual handling underspecified.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to compare ASI Stack runtime policy checks against generated monitor approaches.
- Do not claim monitor generation, timing bounds, or policy enforcement unless local monitor artifacts exist and have been run.
- Keep support state at `argument` until monitor specs, generated artifacts, timing checks, or accepted evidence transitions exist.

## Open Questions

- Which ASI Stack runtime-adapter policy is small enough to compile into a monitor fixture first?
- What receipt should record monitor version, checked property, execution cost, and violation action?
- How should monitor violation routes connect to residual escrow and quarantine states?
