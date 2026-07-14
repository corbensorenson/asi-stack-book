# Post-v2.3 External Anchoring and Completeness Audit

Status: **completed** on 2026-07-14. This is a source and prose reconciliation, not an evidence promotion or release.

## Decision

Four passage-reviewed primary sources changed a boundary or evidence design. No new chapter passed the ownership test; the 54-chapter spine remains intact. Immutable reader v1.0 and v2.0 remain unchanged, while accepted prose is carried by source-only reader successor v2.1.

## Ten-chapter audit

| Chapter | Strongest comparator | Weak neighbor | Disposition | Accepted source(s) |
|---|---|---|---|---|
| `scalable-oversight-and-adversarial-ai-control` | `ext_scalable_oversight_weak_llms_2024` | Monitorability under adversarial pressure and capability scaling was weakly treated. | `insert` | `ext_monitorbench_2026` |
| `model-weight-custody-and-hardware-roots-of-trust` | `ext_rand_model_weight_security_2024` | NIST COSAiS control overlays are current but still discussion-draft material and do not beat the assigned custody comparators. | `watch` | none |
| `ai-supply-chain-integrity-and-lifecycle-provenance` | `ext_slsa_build_track_1_2` | NIST COSAiS and SP 1326 add current overlay/due-diligence framing but no stronger finalized mechanism than the existing SLSA, in-toto, SPDX AI, Croissant, signing, and C-SCRM set. | `already_covered` | none |
| `open-ended-improvement-engines` | `ext_darwin_godel_machine_2025` | Newer discovery systems were screened, but none changes the existing POET, Voyager, FunSearch, ADAS, and Darwin-Godel boundary enough to justify another citation. | `already_covered` | none |
| `inter-stack-protocols-identity-and-economic-exchange` | `ext_mcp_protocol_2025_11_25` | No omitted current protocol changes the existing MCP, A2A, DID, VC, Interledger, and agentic-security division of responsibility. | `already_covered` | none |
| `governed-deliberation-and-test-time-scaling` | `ext_test_time_compute_scaling_2024` | Causal faithfulness of the visible reasoning trace was only a prose caution, not an owned evaluation gate. | `insert` | `ext_faithfulness_information_flow_2026` |
| `capability-thresholds-and-deployment-commitments` | `ext_metr_time_horizons_2025` | Current frontier policies and Inspect already cover the strongest operational neighbor; broader policy catalogs would add count rather than a new decision boundary. | `already_covered` | none |
| `adversarial-evaluation-sandbagging-and-training-time-deception` | `ext_alignment_faking_2024` | Trace/action causal inconsistency and multi-task monitorability stress testing were missing as explicit evidence-design surfaces. | `insert` | `ext_faithfulness_information_flow_2026`, `ext_monitorbench_2026` |
| `safety-cases-and-structured-assurance` | `ext_aisi_safety_cases_2024` | No current primary neighbor materially improves the existing GSN, AISI, and scheming-evaluation safety-case boundary without duplicating the chapter. | `already_covered` | none |
| `data-engines-continual-learning-and-unlearning` | `ext_openunlearning_2025` | Predictive encoders and action-conditioned world-model predictors added a distinct data/version/error lineage not owned by the existing unlearning sources. | `insert` | `ext_v_jepa_2_2025` |

## Accepted and screened sources

| Source | Decision | Reason |
|---|---|---|
| `ext_faithfulness_information_flow_2026` | `insert` | Changes the trace/action evidence design and authoritative-receipt boundary. |
| `ext_monitorbench_2026` | `insert` | Adds a distinct multi-task adversarial monitorability benchmark design. |
| `ext_v_jepa_2_2025` | `insert` | Adds a concrete predictive-state and MPC interface plus explicit adoption residuals. |
| `ext_embedded_agency_2019` | `insert` | Adds the missing foundations boundary between finite records and an embedded agent/world. |
| `watch_nist_cosais_2026` | `watch` | Official 2026 control-overlay work remains a discussion draft and is redundant with stronger finalized custody/supply-chain comparators. |
| `watch_nist_sp_1326_2026` | `already_covered` | Due-diligence and provenance framing does not change the existing C-SCRM/SLSA/in-toto/SPDX/Croissant mechanism. |
| `watch_preliminary_jepa_neighbors_2026` | `reject` | Preliminary JEPA/energy-based neighbors do not beat V-JEPA 2 as the mature empirical interface comparator for this pass. |

## Cross-cutting ownership

- Reasoning-trace faithfulness is owned by Artifact Graphs, Governed Deliberation, Adversarial Evaluation, Policy Optimization, and Scalable Oversight. Private reasoning, reported rationale, action trace, receipt, monitorability evidence, and authoritative effect remain separate.
- V-JEPA and latent world-model material is owned by Mathematical/Search Substrates, Planning, Data Engines, and the Integrated Reference Architecture. Structural prediction, benchmark quality, causal understanding, controller quality, and sim-to-real transfer remain separate.
- Embedded agency joins the already-reviewed CAIS, corrigibility, off-switch, and Goodhart foundations family. Finite record proofs do not become whole-agent or open-world guarantees.

## New-chapter ownership test

Decision: `keep_54_chapter_spine`. Existing owners already provide the distinct interfaces, invariants, artifacts, failure modes, and evidence lanes; a new chapter would duplicate them.

## Tier-2 audit

| ID | Finding | Owner | Disposition | Current refs |
|---|---|---|---|---:|
| `T2-01` | Output content provenance | `artifact-graphs-audit-logs-and-replay` | `defer` | 0 |
| `T2-02` | Interpretability as runtime control | `evidence-states-and-claim-discipline` | `narrow` | 5 |
| `T2-03` | Memory consolidation lifecycle | `procedural-memory-and-cognitive-loop-closure` | `already_covered` | 12 |
| `T2-04` | Calibration selective prediction and abstention | `claim-ledgers-and-belief-revision` | `already_covered` | 12 |
| `T2-05` | Metacognition and capability self-knowledge | `readiness-gates-residual-escrow-and-quarantine` | `defer` | 0 |
| `T2-06` | Collusion between components against oversight | `scalable-oversight-and-adversarial-ai-control` | `already_covered` | 2 |
| `T2-07` | Oversight latency and fleet-scale monitoring | `scalable-oversight-and-adversarial-ai-control` | `defer` | 0 |
| `T2-08` | Control tax as governance-tax comparator | `resource-economics-and-token-budgets` | `already_covered` | 3 |
| `T2-09` | Automated AI R&D acceleration thresholds | `capability-thresholds-and-deployment-commitments` | `already_covered` | 7 |
| `T2-10` | STPA-style systematic hazard analysis | `safety-cases-and-structured-assurance` | `watch` | 2 |
| `T2-11` | Autonomous insider | `security-kernel-and-digital-scifs` | `defer` | 0 |
| `T2-12` | Hardware attestation trust-root class | `model-weight-custody-and-hardware-roots-of-trust` | `already_covered` | 12 |
| `T2-13` | Open-weight release decision record | `model-weight-custody-and-hardware-roots-of-trust` | `already_covered` | 6 |
| `T2-14` | Public governance graphs for market collusion | `inter-stack-protocols-identity-and-economic-exchange` | `defer` | 0 |
| `T2-15` | Guaranteed-safe AI positioning | `executable-specifications-and-lean-proof-envelope` | `defer` | 0 |
| `T2-16` | Machine unlearning and parametric deletion closure | `data-engines-continual-learning-and-unlearning` | `already_covered` | 12 |
| `T2-17` | Prompt-injection impossibility as strongest objection | `security-kernel-and-digital-scifs` | `already_covered` | 12 |
| `T2-18` | Scheming-oriented safety cases | `safety-cases-and-structured-assurance` | `already_covered` | 3 |
| `T2-19` | Non-agentic Scientist AI position | `asi-is-a-stack-not-a-model` | `defer` | 0 |
| `T2-20` | CAIS prior-art mandate | `asi-is-a-stack-not-a-model` | `already_covered` | 12 |
| `T2-21` | Behavior-specification practice crosswalk | `constitutional-alignment-substrate` | `defer` | 0 |
| `T2-22` | Formal-mathematics agents | `circle-calculus-and-proof-carrying-ai-contracts` | `defer` | 0 |
| `T2-23` | ARC-style program synthesis and test-time training | `cognitive-compilation-and-semantic-ir` | `already_covered` | 3 |
| `T2-24` | Compute governance and distributed-training tension | `personal-compute-hives-and-federated-edge-intelligence` | `defer` | 0 |
| `T2-25` | Introspection-training evidence | `readiness-gates-residual-escrow-and-quarantine` | `defer` | 0 |
| `T2-26` | Goal continuity under inherited trajectory pressure | `human-intent-as-a-formal-input` | `already_covered` | 7 |
| `T2-27` | Causal and counterfactual reasoning | `planning-as-a-control-layer` | `narrow` | 12 |
| `T2-28` | Distribution shift OOD detection and runtime uncertainty | `readiness-gates-residual-escrow-and-quarantine` | `already_covered` | 12 |
| `T2-29` | Temporal-logic monitoring and physical safety envelopes | `runtime-adapters-tool-permissions-and-human-approval` | `narrow` | 1 |
| `T2-30` | Human-AI delegation calibration | `scalable-oversight-and-adversarial-ai-control` | `defer` | 0 |
| `T2-31` | Evaluator-access levels and environment custody | `adversarial-evaluation-sandbagging-and-training-time-deception` | `already_covered` | 6 |
| `T2-32` | Domain-specific dangerous-capability profiles | `capability-thresholds-and-deployment-commitments` | `already_covered` | 7 |
| `T2-33` | Post-deployment monitoring and incident disclosure | `safety-cases-and-structured-assurance` | `defer` | 1 |
| `T2-34` | AIBOM lineage and signed build attestations | `ai-supply-chain-integrity-and-lifecycle-provenance` | `already_covered` | 4 |
| `T2-35` | Purpose limitation privacy budgets and internal-channel leakage | `data-engines-continual-learning-and-unlearning` | `defer` | 0 |
| `T2-36` | Unlearning privacy paradox | `data-engines-continual-learning-and-unlearning` | `narrow` | 4 |
| `T2-37` | Provider concentration substitutability and impact tolerances | `resource-economics-and-token-budgets` | `defer` | 0 |

Only `defer`, `watch`, and `narrow` rows remain in the event-driven queue. `Already_covered` rows are not copied into a new roadmap, and deferred rows are not silently cited from search-result-depth material.

## Evidence boundary

All 54 core claims remain at `argument`. The audit does not reproduce any external result, approve a reader format, change public release v2.3.0, require external-human prepublication review, or establish model quality, monitorability, causal world modeling, corrigibility, safety, AGI, or ASI.
