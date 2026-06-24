# Source Note: Ratcheting Generative Systems

| Field | Value |
|---|---|
| Source ID | `rgs` |
| Source title | Ratcheting Generative Systems |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1jxbgwiBzgUgdTjpPiOkEQNZz2ehcDioTG-lUBV-f4FA |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/rgs.txt`; raw text is not published. |

## Thesis

Ratcheting Generative Systems describe an improvement loop in which AI systems convert repeated successful behavior into verified generative structure, preserve failures as residuals, and advance through benchmark pressure only when regression and safety checks hold.

## Mechanisms

- Start from a frontier benchmark or task pressure.
- Attempt the task, log traces, and classify successes and failures.
- Promote repeated successful procedures into verified tools or procedural memory.
- Preserve failures in a residual escrow rather than hiding them.
- Use residuals to guide interventions across data, training, inference, memory, tools, architecture, and routing.
- Maintain regression suites so new ratchets cannot erase prior competence.
- Distinguish interpreter mode, compiled-tool mode, and reflex or failsafe mode.
- Keep ledgers for benchmarks, models, tools, residuals, calibration, safety, routing, and interventions.

## Evidence

- The source is a conceptual framework and public-release methodology.
- It gives a loop structure, vocabulary, system-state decomposition, and research agenda.
- It does not provide local benchmark runs, tool-promotion traces, or regression data in this repository.
- Use it as architecture support for residual honesty and ratcheting, not as empirical proof that a specific system improves.

## Failure Modes

- Promoting brittle task-specific behavior into tools too early.
- Hiding residual failures and thereby losing the signal needed for improvement.
- Goodharting benchmark frontiers while regression capability decays.
- Treating benchmark success as general competence without calibration.
- Letting compiled tools bypass safety/reflex layers.
- Creating ratchets that increase capability faster than evidence, governance, or interpretability.

## Book Chapters Supported

- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)

## Claims To Add Or Update

- Use RGS to connect procedural memory, compact generative structure, residual escrow, benchmark ratchets, and governance.
- Treat residuals as first-class artifacts in recursive improvement.
- Keep ratchet language tied to regression gates and evidence ledgers, not ambient self-improvement.

## Open Questions

- What is the smallest benchmark-ledger schema the book should include?
- Should procedural memory promotion require a proof, a test suite, or a human approval record?
- How should residual escrow interact with Appendix C claim states?
