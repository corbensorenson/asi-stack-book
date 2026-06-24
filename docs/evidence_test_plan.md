# Evidence and Test Plan

## Claim labels

| Label | Meaning |
|---|---|
| Demonstrated | Shown by a recorded artifact, derivation, implementation, or source-backed example in scope |
| Measured | Quantified by a recorded measurement or benchmark result |
| Mechanized | Expressed as runnable code, executable schema, or formal proof target |
| Hypothesized | Proposed as a testable claim that still needs evidence |
| Design rationale | Architectural choice supported by reasoning and constraints |
| Speculative | Exploratory or conjectural; not a deployed-system guarantee |

## Claim support states

| State | Meaning |
|---|---|
| unsupported | Not yet supported; likely remove or mark as speculative |
| argument | Supported by reasoning only |
| source-derived | Derived from supplied source papers |
| prototype-backed | Implemented in a prototype but not robustly tested |
| synthetic-test-backed | Supported by controlled synthetic tests |
| empirical-test-backed | Supported by external/realistic tests |
| external-literature-backed | Supported by third-party literature |
| deprecated | Superseded, merged, or retired; retained for lineage and review |
| refuted | Contradicted by later evidence or tests; retained to preserve negative results |

## Evidence bundle fields

Promoted claims should record source hash, code revision, environment manifest, baseline, test command, metrics, raw logs, negative results, ablations, failure reproduction, artifacts, provenance, conclusion, limitations, and release notes where applicable.

## Minimum test specs by layer

### Alignment
- Constitutional consistency tests.
- Value conflict classification.
- Self-modification ethics scenarios.
- Power-seeking / agency-dominance scenarios.

### SCF
- Qualification predicate tests.
- Route validity tests.
- Mutation tests.
- Authority non-escalation tests.
- Rollback and recovery tests.

### Planning
- Decomposition accuracy.
- Dependency ordering.
- Constraint preservation.
- Runtime replanning.
- Tool selection.
- Budget and risk allocation.
- Scope creep prevention.

### VCM
- Context packet adequacy.
- Distractor resistance.
- Authority label preservation.
- Proof-carrying summary fidelity.
- Planner-guided prefetch accuracy.
- Privacy/behavioral authority checks.

### Talos / execution
- Typed job lifecycle.
- Tool permission enforcement.
- Audit log reconstruction.
- Replay determinism.
- Human approval gates.
- Adversarial job injection.

### Spinoza / verification
- Claim extraction.
- Contradiction detection.
- Belief revision.
- Evidence tier assignment.
- Uncertainty calibration.
- Refusal/silence when evidence is insufficient.

### Routing/modularity
- Specialist routing accuracy.
- Readiness gate enforcement.
- Benchmark promotion.
- Quarantine.
- Regression preservation.
- Residual escrow.

### Compression
- Reconstruction quality.
- Residual burden.
- Probe-and-route fallback.
- Compression ratio.
- Latency cost.
- Downstream utility preservation.

### Benchmark ratchets
- Saturation detection.
- Hidden benchmark transfer.
- Regression generation.
- Anti-Goodhart checks.
- Residual backlog integrity.
