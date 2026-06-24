# Source Note: Spinoza Composer / Spinoza Trinity

| Field | Value |
|---|---|
| Source ID | `spinoza_composer` |
| Source title | Spinoza Composer / Spinoza Trinity |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1pWHPNCFL5dnphZxKUhj5c_yk3juskWQZPTzPjxE7nEE |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/spinoza_composer.txt`; raw text is not published. |

## Thesis

Spinoza Composer, also framed as the Spinoza Trinity, separates world logic from narrative rendering. It treats a corpus as a source for world graphs, belief states, causal history, constraints, and rendering policy so generated text can preserve continuity and compliance rather than improvise unconstrained prose.

## Mechanisms

- Extract world graphs, definitions, axioms, scope tags, and belief states from source text.
- Represent state history as a causal DAG or narrative tree.
- Distinguish ontological fact from agent-relative belief.
- Verify candidate additions by constraint solving against established axioms and state.
- Render verified logical state into prose through a composer layer.
- Attach disclosures, exports, baselines, and evaluation plans in operational variants.

## Evidence

- The source is a technical whitepaper with multiple variants, implementation strategy, and evaluation plans.
- It provides useful artifact-graph and continuity architecture material.
- The repository has not implemented the composer, run continuity benchmarks, or validated extraction quality.

## Failure Modes

- Extracting an incorrect world graph from ambiguous source text.
- Mistaking a character's or source's belief for objective domain fact.
- Overconstraining creative or uncertain domains until useful variation disappears.
- Rendering fluent prose that hides unresolved constraint violations.
- Treating planned evaluation as completed evidence.

## Book Chapters Supported

- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)

## Claims To Add Or Update

- Use this source to enrich artifact graphs, belief-state scoping, causal history, and render-from-verified-state patterns.
- Keep compliance and continuity performance claims unpromoted until evaluated.

## Open Questions

- Should artifact graphs include separate fact, belief, and scope-tag nodes?
- Can a tiny fiction or policy corpus fixture test state-drift detection?
