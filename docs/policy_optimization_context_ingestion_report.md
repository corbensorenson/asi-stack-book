# Policy Optimization Context Ingestion Report

Date: 2026-06-24

Raw packet location: `sources/inbox/policy_optimization_browser_note_2026-06-24/`

Public status: raw packet is local-only and ignored by git. This report is the public-safe synthesis.

## Ingestion Boundaries

- The browser-GPT packet was treated as author intent, chapter-scoping guidance, and external-literature queue context.
- No private conversation wording was copied verbatim into the public manuscript.
- No third-party benchmark, training, or model-quality claim was promoted from the packet.
- No claim was promoted to `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed`.
- External papers named by the packet were spot-checked as real public records, but source notes still need to be created before they can support claims.

## Added or Strengthened

| Area | Public update |
|---|---|
| Chapter structure | Added `Policy Optimization and Learning from Feedback` as a Part IV chapter after Benchmark Ratchets and before Integrated Reference Architecture. |
| Stack interface | Framed policy optimization as the stack's learning actuator, with governance deciding which feedback is admissible and whether updates may be promoted. |
| Evidence discipline | Separated reward, preference, verifier, benchmark, latency, and governance feedback from evidence and authority claims. |
| Record schema | Added `policy_optimization_record.schema.json` and a valid fixture for target layer, feedback source, update constraint, evaluation refs, governance gates, rollback, residuals, and non-claims. |
| Lean hooks | Added `AsiStackProofs.PolicyOptimization` finite predicates for admitted update records and unverified-reward or missing-governance promotion blocking. |
| Research direction | Preserved REINFORCE/RLOO/ReMax, TRPO/PPO/RLHF, GRPO/DAPO/GSPO, DPO/IPO/ORPO/KTO/SimPO, RLVR, process rewards, reasoning-budget RL, router-policy RL, and context-policy RL as external-literature and experiment backlog rather than reported results. |

## External Literature Queue

The packet suggested these external literature families for future source-note work:

| Area | Needed before use |
|---|---|
| Foundational policy gradients | Add source records/source notes for REINFORCE-style methods, RLOO, ReMax, and REINFORCE++-style work before claiming method behavior. |
| Trust-region and clipped online RL | Add source records/source notes for TRPO, PPO/RLHF, GRPO, and relevant variants before claiming method behavior. |
| Critic-free, group-relative, and sequence-level RL | Source-note ReMax, RLOO/GRPO descendants, DAPO, GSPO, S-GRPO, and related methods before using reported results. |
| Offline preference optimization | Source-note DPO, IPO, ORPO, KTO, SimPO, and related methods before using them as external support. |
| Verifier-based RL / RLVR | Source-note RLVR, process-reward, and long-context verifier-reward papers before connecting them to VCM as external evidence. |
| Reward hacking and RLHF limitations | Source-note limitation surveys and evaluator-gaming papers before using them as external literature support. |
| Stack control-policy RL | Design local experiments for planner, router, VCM, execution, verifier, and generation-mode policies before claiming prototype-backed support. |

## Remaining Missing or Blocked Items

| Item | Needed before claim promotion |
|---|---|
| Third-party bibliography | Add citation-normalized external records to `sources/source_inventory.json`. |
| External source notes | Read the primary papers and create source notes under `sources/source_notes/`. |
| Policy optimization implementation | The JSON Schema fixture and finite Lean predicates exist; no trainer, simulator, reward function, or policy update has been implemented. |
| Experiments | Implement and run toy router-policy, context-policy, reward-hacking, reasoning-budget, and rollback/promotion-gate tests. |
| Claim support | Keep the chapter at `argument` until external source notes, local experiments, or reproducible artifacts support stronger states. |

## Validation Requirement

After this ingestion, the required validation loop is:

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_proof_readiness.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
```
