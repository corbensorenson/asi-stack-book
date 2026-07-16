# Measurement and Reproduction Foundation

Status: sacrificial preflight passed on 2026-07-16. This is M2 instrument
readiness, not an outcome-bearing experiment.

## Frozen foundation

The machine authority is
`experiments/research_foundation/foundation.json`. It binds a 24-task public-
safe natural-language corpus across governed work, governed learning, and
assurance/control. Each slice has two sacrificial, two tuning, and four held-out
tasks. Candidate-visible task records contain no route or residual labels; the
twelve held-out labels live in a separately hashed evaluator-only file that a
runner may open only after candidate artifacts close.

The dated model roster has three roles. `gemini-3.5-flash` is the current strong
general candidate, selected from the provider's official model catalog on
2026-07-16. The exact provider identity must be resolved again before a run and
any change forces requalification. The independent local comparison is the
pinned `mlx-community/Qwen3-4B-4bit` snapshot already used by the repository;
the smaller reproducible control is the pinned Qwen2.5-Coder 0.5B snapshot.
Provider selection is not evidence of access or performance. See the
[official Gemini model catalog](https://ai.google.dev/gemini-api/docs/models).

## Instrument boundary

Only a registered final-decision object is scored. Reasoning, if available, is
diagnostic and separate. The candidate process cannot read held-out labels or
adjudicate itself. Two independently implemented evaluator paths compare route
and residual semantics after schema admission. Disagreement produces
abstention and an adjudication record.

The sacrificial packet contains ten deliberately simple parser/evaluator
canaries: eight are schema-admissible, seven of those eight are semantically
correct, one valid object is intentionally wrong, and two objects are
intentionally malformed. Both evaluator paths agree, false accept and false
reject counts are zero, and the exact 80% admissibility floor passes. These are
hand-authored canaries, not model outputs; they validate plumbing only.

## Research controls

The shared policy freezes joint useful-release, unsafe-release, abstention,
fallback, recovery, latency, visible-cost, governance-cost, and residual-burden
estimands. Every campaign must still justify its own minimum effect, sample
size, uncertainty, hierarchy, multiplicity, missingness, stopping, and
robustness plan before held-out work.

The environment record fixes the local OS, hardware, toolchain, seeds, locale,
clock and network rules, file/process boundary, and known nondeterminism. The
safety envelope forbids unbounded external action, publication, messaging,
account mutation, self-propagation, or uncontrolled spending. The artifact
protocol is append-only and requires raw failures, checksums, environment and
cost records, effect and residual ledgers, redaction receipts, adjudication,
and replay receipts.

## Non-claims

This foundation does not show that the corpus is representative, that any
model can solve it, that evaluators generalize beyond the canaries, that a
campaign is adequately powered, or that governed execution, learning,
rollback, safety, reproduction, transfer, SOTA, AGI, or ASI has been
established. It grants no support, release, publication, or external-action
authority.
