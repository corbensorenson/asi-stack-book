# Defended Contribution Prior-Art Positioning

Last updated: 2026-06-29

This record positions the five selected v1.x defended contribution tracks
against source-noted external literature already present in the repository. It
is source-noted prior-art positioning, not an exhaustive literature review, not
an external novelty decision, not source-derived support for any chapter core
claim, and not support-state movement.

This record does not prove novelty. It does not promote any chapter core claim
above `argument`. External records here are comparators, not evidence that the
ASI Stack mechanisms work, not evidence that a local artifact reproduces an
external result, and not evidence that a reader or release artifact is approved.

## Positioning Boundary

- Use only external sources that already have public-safe source notes in
  `sources/source_notes/`.
- Treat each external source as relation, vocabulary, and comparator material
  unless a separate accepted evidence-transition record says otherwise.
- Separate "near prior art exists" from "the ASI Stack contribution is
  defended." Prior-art relation is necessary for credibility; it is not enough
  for support-state promotion.
- Record gaps plainly where a track still needs better comparator coverage,
  external review, replay evidence, or proof depth.
- Keep the selected contribution tracks at roadmap status only until review,
  replay, proof, or evidence-transition artifacts justify stronger language.

## Track Positioning Summary

| Track ID | Current prior-art status | Source-noted comparators | ASI Stack positioning move | Remaining blocker |
|---|---|---|---|---|
| `living-evidence-book-methodology` | source-noted comparator set exists | `ext_model_cards_2019`; `ext_datasheets_datasets_2021`; `ext_factsheets_ai_services_2019`; `ext_ml_reproducibility_program_2021`; `ext_helm_2022`; `ext_livebench_2024`; `ext_nist_ai_rmf_1_0_2023`; `ext_frontier_ai_regulation_2023` | Positions the living book as a CI-gated claim/source/proof/test/release/non-claim surface that combines documentation, reproducibility, evaluation, and release-status discipline rather than another static anthology. | Accepted external review and a tighter novelty note that distinguishes book-method contribution from model-reporting, benchmark, reproducibility, and governance-framework practice. |
| `claim-support-states-and-evidence-laundering-prevention` | source-noted comparator set exists | `ext_model_cards_2019`; `ext_datasheets_datasets_2021`; `ext_factsheets_ai_services_2019`; `ext_ml_reproducibility_program_2021`; `ext_helm_2022`; `ext_livebench_2024`; `ext_proof_carrying_code_1997`; `ext_lean4_theorem_proving` | Positions support states, non-claims, failed transitions, proof receipts, and release blockers as first-class engineering records that prevent documentation or proof syntax from laundering a stronger claim. | Reviewer pressure test plus a sharper demotion/refutation workflow that shows how the method handles an actually wrong or overclaimed chapter. |
| `governed-self-improvement-boundary` | source-noted comparator set exists | `ext_corrigibility_2015`; `ext_off_switch_game_2016`; `ext_optimal_policies_power_2019`; `ext_model_evaluation_extreme_risks_2023`; `ext_nist_ai_rmf_1_0_2023`; `ext_frontier_ai_regulation_2023`; `ext_slsa_v1_0` | Positions self-improvement as a governed candidate-change lifecycle with protected invariants, evaluator independence, authority ceilings, rollback handles, residual custody, readiness gates, and artifact provenance instead of an unconstrained capability-improvement loop. | Clean Theseus replay or archived public fixture, richer self-improvement Lean semantics, and external safety/formal review. |
| `proof-carrying-claims-and-ai-contracts` | source-noted comparator set exists | `ext_proof_carrying_code_1997`; `ext_lean4_theorem_proving`; `ext_model_cards_2019`; `ext_ml_reproducibility_program_2021` | Positions proof-carrying AI contracts as a bounded extension of proof-carrying artifact discipline: a receipt can make a narrow artifact claim checkable without implying model quality, semantic adequacy, runtime safety, or broad ASI capability. | Clean Circle replay, public contract pack, or archived upstream pack; stronger receipt negative controls remain required before any broader claim. |
| `costed-routing-residual-accounting-resource-discipline` | source-noted comparator set exists, residual-governance gap remains | `ext_frugalgpt_2023`; `ext_hybrid_llm_2024`; `ext_routellm_2024`; `ext_sparse_moe_2017`; `ext_switch_transformer_2021`; `ext_helm_2022` | Positions ASI Stack routing as a cost/quality/adequacy/authority/residual control surface rather than only cheap model selection, sparse expert activation, or learned LLM routing. | Larger public trace with quality, adequacy, displaced-cost, fallback, and residual accounting. The residual-governance comparator gap remains open: current routing literature comparators are useful, but they do not fully cover authority and residual custody. |

## Track Notes

### Living Evidence Book Methodology

Model Cards, Datasheets, FactSheets, and ML reproducibility work give the book
fair adjacent documentation and reproducibility baselines. HELM and LiveBench
add evaluation-surface comparators: multi-metric reporting and living
benchmark-update discipline. NIST AI RMF and frontier-governance literature
connect the release/status surface to risk-management vocabulary.

The ASI Stack should not claim to replace any of those practices. The narrower
candidate contribution is the integrated book-as-evidence system: a public
Quarto text that keeps chapter identity, source inventories, claim states,
proof targets, tests, release profiles, reader artifacts, non-claims, and
validation gates in one CI-checked architecture surface. This is promising, but
still needs accepted external review and a concise novelty note before it can
be called defended.

### Claim Support States And Evidence Laundering Prevention

Structured reports and reproducibility checklists help readers see what a
system claims. Proof-Carrying Code and Lean 4 help readers see what a machine
check can establish inside a formal boundary. The ASI Stack contribution target
is the negative space between those practices: the method must stop a polished
report, passed test, theorem build, or reader artifact from being laundered
into a stronger support state.

The current repository already has no-promotion records and a non-core
evidence ledger, but a defended contribution still needs a reviewer-readable
case where a tempting promotion is refused, demoted, or refuted with exact
reason and downstream repair path.

### Governed Self-Improvement Boundary

Corrigibility, shutdown incentives, power-seeking analysis, extreme-risk
evaluation, AI RMF, frontier governance, and SLSA all supply nearby external
vocabulary for the hard parts: correction channels, authority expansion,
deployment/release decisions, risk management, and artifact provenance.

The ASI Stack's positioning move is to make self-improvement a candidate-change
transaction. A candidate improvement is not accepted because it is newer or
better on a score; it must preserve protected invariants, keep evaluator
independence, avoid authority widening, retain rollback handles, and route
residuals to custody. This remains argument-level until the Theseus lane,
Lean state machine, and external review are stronger.

### Proof-Carrying Claims And AI Contracts

Proof-Carrying Code is the obvious formal ancestor: the consumer checks a proof
against a policy before accepting an artifact. Lean 4 supplies the local
proof-assistant vocabulary and warns against over-reading a successful build.
Model-reporting and reproducibility sources add the reporting side: a proof
receipt still needs provenance, versioning, command/replay context, and
non-claims.

The ASI Stack move is not "proofs make AI safe." The candidate contribution is
a proof-carrying claim discipline where a claim cites the exact theorem,
policy, digest, artifact, consumer gate, failure modes, and non-claims. A valid
receipt can support a narrow artifact statement while leaving model quality,
semantic adequacy, and deployment safety unpromoted.

### Costed Routing, Residual Accounting, And Resource Discipline

FrugalGPT, Hybrid LLM, RouteLLM, sparse MoE, and Switch Transformers are fair
comparators for cost-aware, quality-aware, learned, and sparse routing. HELM
adds a multi-metric evaluation warning: routing cannot collapse to one
leaderboard number.

The ASI Stack should position its routing track as a stricter control surface:
route choice must record adequacy, cost, fallback, hidden or displaced cost,
authority ceiling, verification burden, and residuals. The current synthetic
slice is useful but narrow. It does not reproduce the external routing papers,
does not prove deployed routing, and does not cover the residual-governance
comparator gap.

## Current Gaps

| Gap | Why it matters | Next evidence or source action |
|---|---|---|
| External review still missing | Prior-art positioning by the authoring system is not independent scrutiny. | Record accepted external review or dated blocker with exact reviewer scope. |
| Novelty is not proven | Source-noted comparators show relation, not novelty. | Write a contribution-specific prior-art/novelty note before any preprint or stronger claim. |
| Routing residual-governance comparator gap remains open | Existing routing papers ground cost/quality routing, but not the full ASI Stack residual and authority ledger. | Mine routing, safety, and governance literature for residual/accountability comparators; keep route claims at `argument`. |
| Self-improvement evidence is still narrow | Current Theseus import is digest-verified static implementation-reference evidence, not a clean replay. | Produce clean Theseus replay or archived public fixture plus negative controls before support-state movement. |
| Proof-carrying contract evidence is still narrow | Circle consumer gate is CI-verifiable by digest, but not a clean upstream replay or public contract pack. | Create a public Circle contract pack, clean replay, or archived upstream pack. |
| Demotion/refutation path needs a live example | `docs/evidence_laundering_prevention_case_studies.md` now records three no-promotion examples, but no chapter core claim has yet been truly demoted or refuted. | Add a future demotion/refutation case when evidence, prior art, review, proof limits, or replay failure requires narrowing, retirement, demotion, or refutation. |

## Non-Claims

- This record is not an exhaustive literature review.
- This record does not prove novelty.
- This record is not an accepted external review.
- This record is not support-state movement.
- This record does not promote any chapter core claim above `argument`.
- This record does not claim A+ completion for any defended contribution track.
- This record does not create new source records, source notes, test results,
  proof results, replay results, reader artifacts, release artifacts, or
  artifact approvals.
- Each external source listed here is a comparator, not evidence that the ASI
  Stack reproduces its results or satisfies its framework.
