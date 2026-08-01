# Source Note: Assembly-Theoretic Technical Debt

| Field | Value |
|---|---|
| Source ID | `attd` |
| Source title | Assembly-Theoretic Technical Debt: A Deterministic Outer Loop for Self-Improving Codebases |
| Ingestion date | 2026-07-31 |
| Source version / URL | Authenticated Google Doc; https://docs.google.com/document/d/1mv69yelFkJ-deJ1BkVMZANqPQzzaERTpG108LhU1BKk |
| Ingestion basis | Full authenticated connector text section-audited; raw private text is not published. |

## Thesis

A self-modifying project needs a deterministic outer loop that governs not only whether a patch works now, but whether its construction history is accumulating irreducible burden. Assembly-theoretic technical debt is best understood as a vector of approximate structural, reuse, role-entropy, lineage, residue, and growth signals with local caps—not as a universal scalar law.

## Mechanisms

- Analyze active authored code separately from generated, vendored, deprecated, and inert material.
- Estimate intrinsic assembly burden through compressed descriptions and reusable motif dictionaries.
- Measure reuse failure and role-internal pattern entropy so duplicated or incoherent structures cannot hide behind total line counts.
- Preserve region lineage and rolling construction history to detect repeated compensating patches and assembly residue.
- Compute debt pressure for prioritization, while retaining non-compensating local caps and growth-rate guards.
- Credit verified simplification so safe deletion, convergence, and consolidation are not misclassified as harmful change.
- Route GREEN, YELLOW, and RED states deterministically; non-GREEN emits a bounded maintenance packet with location, cause, target, budget, owner, test, and expiry.
- Keep patch generation stochastic if useful, but make admission back to GREEN deterministic and abstain when role classification is uncertain.

## Evidence

- The complete paper was reviewed for metric definitions, history model, role classification, simplification credit, local caps, state machine, maintenance packets, evaluation arms, and limitations.
- The source proposes a four-arm long-horizon comparison: ungated, scalar-only, ATTD without simplification credit, and full ATTD.
- No analyzer, motif miner, lineage tracker, benchmark, threshold calibration, causal ablation, or long-horizon codebase result is reproduced here.
- Assembly theory is used as design inspiration, not as a claim that software debt obeys a fundamental physical law.

## Failure Modes

- Collapsing the vector into one compensating score that lets a catastrophic local region hide behind global cleanliness.
- Penalizing healthy diversity, generated code, migrations, or verified simplification.
- Treating noisy motif, lineage, or role classifiers as ground truth.
- Refactoring to game the metric while leaving maintenance burden unchanged.
- Allowing the same modifying agent to redefine thresholds after seeing the result.
- Stopping growth without a bounded repair packet, owner, or acceptance test.

## Book Chapters Supported

- Artifact Steward Agents and Living Project Governance
- Recursive Self-Improvement Boundaries
- Benchmark Ratchets and Anti-Goodhart Evidence

## Claims To Add Or Update

- Add repository health as a governed, historical, vector-valued state rather than a current-snapshot lint score.
- Require verified simplification credit and explicit class separation before debt metrics affect admission.
- Make non-GREEN states produce bounded maintenance work rather than vague cleanup pressure.
- Evaluate the governance mechanism causally against scalar-only and no-credit ablations over long horizons.

## Open Questions

- Which motif and lineage representations stay stable across languages and refactors?
- How should thresholds be calibrated for different repository roles without inviting metric gaming?
- Can independent maintainers predict future defects or maintenance time better from the vector than from ordinary complexity and churn baselines?

## Section-Family Closure Ledger

| Family | Disposition | Book effect |
|---|---|---|
| Artifact classes and role classification | integrated | Steward chapter owns analyzer scope and abstention. |
| Assembly, reuse, entropy, lineage, residue vector | integrated | Steward chapter owns the health record. |
| Simplification credit | integrated | Prevents deletion/convergence penalties. |
| Local caps, growth guards, GREEN/YELLOW/RED | integrated | Steward and RSI chapters own admission effects. |
| Maintenance packets | integrated | Steward work contracts carry repair obligations. |
| Four-arm long-horizon evaluation | research obligation | Benchmark chapter owns the causal campaign. |
| Fundamental assembly-theory interpretation | non-claim | Inspiration only. |

## Non-Claims

This source does not establish a universal technical-debt equation, future-defect predictor, calibrated threshold, language-independent motif system, safe self-modifying codebase, or superior maintenance outcome. The proposed metrics are approximate and gameable until independently tested.
