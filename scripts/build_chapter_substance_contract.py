#!/usr/bin/env python3
"""Build the current-book chapter-depth, concept-fidelity, and atom-coverage contract."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
OUTPUT = ROOT / "evidence_quality/chapter_substance_contract.json"
WORD_TRIGGER = 5000
MANIFEST_FREEZE = 84
SEMANTIC_REVIEW_DISPOSITION = "accepted_for_editorial_substance_no_evidence_effect"

ATOM_SOURCES = [
    ROOT / "evidence_quality/claim_atom_registry.json",
    ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json",
    ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
    ROOT / "evidence_quality/taxonomy_completion_claim_atoms_2026_07_24.json",
    ROOT / "evidence_quality/round_18_breadth_completion_claim_atoms.json",
    ROOT / "evidence_quality/round20_four_chapter_claim_atom_addendum.json",
]

CONCEPT_SPECS: dict[str, list[dict[str, Any]]] = {
    "dangerous-capability-domains-and-misuse-uplift": [
        {"concept_id": "knowledge-versus-completion", "heading": "Knowledge is not completion", "source_ids": ["ext_model_evaluation_extreme_risks_2023", "ext_aisi_frontier_ai_trends_2025"]},
        {"concept_id": "refusal-versus-capability", "heading": "Refusal is not incapability", "source_ids": ["ext_openai_worst_case_open_weight_risks_2025"]},
        {"concept_id": "capability-versus-propensity", "heading": "Capability is not propensity", "source_ids": ["ext_singapore_consensus_2026"]},
        {"concept_id": "measurement-ladder", "heading": "The six-level measurement ladder", "source_ids": ["ext_aisi_misuse_safeguards_safety_case_2026"]},
        {"concept_id": "threat-model-freeze", "heading": "1. Freeze the threat model", "source_ids": ["ext_openai_preparedness_framework_2025", "ext_anthropic_responsible_scaling_policy_3_4_2026"]},
        {"concept_id": "actor-cohorts-and-counterfactuals", "heading": "2. Define actor cohorts and counterfactuals", "source_ids": ["ext_singapore_consensus_2026"]},
        {"concept_id": "elicitation-competence", "heading": "3. Audit elicitation competence", "source_ids": ["ext_model_evaluation_extreme_risks_2023", "ext_openai_worst_case_open_weight_risks_2025"]},
        {"concept_id": "cbrn-domain-program", "heading": "CBRN and biological/chemical misuse", "source_ids": ["ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026", "ext_anthropic_responsible_scaling_policy_3_4_2026"]},
    ],
    "content-authenticity-watermarking-and-synthetic-media-integrity": [
        {"concept_id": "signed-provenance", "heading": "Signed provenance", "source_ids": ["ext_c2pa_specification_2_3_2025"]},
        {"concept_id": "watermarking", "heading": "Watermarking", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "fingerprinting", "heading": "Fingerprinting", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "statistical-detection", "heading": "Statistical detection", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "visible-disclosure", "heading": "Visible disclosure", "source_ids": ["ext_eu_article_50_transparency_guidelines_2026"]},
        {"concept_id": "contextual-verification", "heading": "Contextual verification", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "transformation-lineage", "heading": "Transformation is the central engineering problem", "source_ids": ["ext_c2pa_specification_2_3_2025"]},
        {"concept_id": "article-50-interface", "heading": "Regulation is an interface, not a design substitute", "source_ids": ["ext_eu_article_50_transparency_guidelines_2026"]},
    ],
    "societal-resilience-and-misuse-defense": [
        {"concept_id": "classifier-coverage", "heading": "One classifier sees one surface", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "recovery-beyond-takedown", "heading": "Takedown is not recovery", "source_ids": ["ext_nist_incident_response_2025"]},
        {"concept_id": "rights-preserving-reporting", "heading": "Reporting is not automatically safe", "source_ids": ["ext_singapore_consensus_2026", "ext_nist_incident_response_2025"]},
        {"concept_id": "four-stage-resilience", "heading": "The four-stage resilience contract", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "federated-incident-envelope", "heading": "The federated incident envelope", "source_ids": ["ext_nist_incident_response_2025"]},
        {"concept_id": "fraud-and-impersonation", "heading": "Fraud, scams, extortion, defamation, and impersonation", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "child-safety-and-ncii", "heading": "Child safety and non-consensual intimate imagery", "source_ids": ["ext_international_ai_safety_report_2026"]},
        {"concept_id": "mental-health-and-parasocial-harm", "heading": "Manipulation, mental health, and parasocial harms", "source_ids": ["ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026"]},
    ],
    "scientific-discovery-and-experimental-governance": [
        {"concept_id": "hypothesis-experiment-provenance", "heading": "Hypothesis and experiment provenance", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "closed-loop-laboratory-authority", "heading": "Closed-loop laboratory authority", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "discovery-versus-benchmark-success", "heading": "Discovery versus benchmark success", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "reproducibility-and-replication", "heading": "Reproducibility and replication", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "negative-and-null-results", "heading": "Negative and null results", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "dual-use-review", "heading": "Dual-use review and information hazards", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "resource-allocation", "heading": "Resource allocation and search governance", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
        {"concept_id": "human-scientific-judgment", "heading": "Human scientific judgment and accountable handoff", "source_ids": ["aletheia", "ext_autonomous_lab_materials_2023"]},
    ],
    "governed-objective-formation-value-learning-and-goal-integrity": [
        {"concept_id": "preferences-values-authorization", "heading": "Preferences, values, and authorization are different objects", "source_ids": ["alignment_field", "ext_cooperative_inverse_rl_2016"]},
        {"concept_id": "uncertainty-pluralism-standing", "heading": "Uncertainty, pluralism, and affected-party standing", "source_ids": ["alignment_field", "ext_cooperative_inverse_rl_2016"]},
        {"concept_id": "corrigibility-lifecycle", "heading": "Corrigibility as an objective-lifecycle property", "source_ids": ["alignment_field", "ext_learned_optimization_risks_2019"]},
        {"concept_id": "goal-drift-integrity", "heading": "Goal drift and integrity across change", "source_ids": ["ext_goal_misgeneralization_2022", "ext_learned_optimization_risks_2019"]},
        {"concept_id": "proxy-reward-evaluator-failure", "heading": "Proxy, reward, and evaluator failure", "source_ids": ["ext_goal_misgeneralization_2022", "ext_learned_optimization_risks_2019", "ext_emergent_misalignment_reward_hacking_2025"]},
        {"concept_id": "objective-authority", "heading": "Authority to create or revise objectives", "source_ids": ["alignment_field", "ext_cooperative_inverse_rl_2016"]},
        {"concept_id": "conflict-adjudication", "heading": "Conflict adjudication without value laundering", "source_ids": ["alignment_field", "ext_cooperative_inverse_rl_2016"]},
        {"concept_id": "update-rollback-retirement", "heading": "Update, rollback, refusal, and descendant retirement", "source_ids": ["alignment_field", "ext_goal_misgeneralization_2022", "ext_learned_optimization_risks_2019"]},
    ],
    "durable-semantic-memory-and-knowledge-lattices": [
        {"concept_id": "semantic-identity-provenance", "heading": "Semantic identity and provenance", "source_ids": ["qcsa_whitepaper", "ext_graphrag_2024", "ext_hipporag_2024"]},
        {"concept_id": "write-admission", "heading": "Write admission and memory authority", "source_ids": ["qcsa_whitepaper", "ext_mem0_2025"]},
        {"concept_id": "consolidation-compaction", "heading": "Consolidation and compaction", "source_ids": ["qcsa_whitepaper", "ext_graphrag_2024", "ext_mem0_2025", "ext_titans_2025"]},
        {"concept_id": "contradiction-belief-revision", "heading": "Contradiction and belief revision", "source_ids": ["qcsa_whitepaper", "ext_graphrag_2024", "ext_hipporag_2024"]},
        {"concept_id": "retrieval-context-assembly", "heading": "Retrieval and context assembly", "source_ids": ["qcsa_whitepaper", "ext_graphrag_2024", "ext_hipporag_2024", "ext_mem0_2025"]},
        {"concept_id": "retention-forgetting-deletion", "heading": "Retention, forgetting, and deletion", "source_ids": ["qcsa_whitepaper", "ext_mem0_2025", "ext_titans_2025"]},
        {"concept_id": "poisoning-taint-quarantine", "heading": "Poisoning, taint, and semantic quarantine", "source_ids": ["qcsa_whitepaper", "ext_graphrag_2024", "ext_hipporag_2024", "ext_mem0_2025"]},
        {"concept_id": "lineage-rollback-repair", "heading": "Lineage, rollback, restart, and descendant repair", "source_ids": ["qcsa_whitepaper", "ext_titans_2025"]},
    ],
    "ai-deployment-transition-distribution-and-human-agency": [
        {"concept_id": "distribution-gains-burdens", "heading": "Distribution of gains and burdens", "source_ids": ["coherence_exchange", "ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025"]},
        {"concept_id": "labor-transition", "heading": "Labor transition from tasks to durable capability", "source_ids": ["ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025"]},
        {"concept_id": "human-agency", "heading": "Human agency and meaningful choice", "source_ids": ["coherence_exchange", "ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025"]},
        {"concept_id": "access-concentration", "heading": "Access, concentration, and bottleneck power", "source_ids": ["coherence_exchange", "ext_oecd_ai_infrastructure_competition_2025"]},
        {"concept_id": "exit-fork-contestability", "heading": "Exit, fork, and contestability", "source_ids": ["coherence_exchange", "ext_oecd_ai_infrastructure_competition_2025"]},
        {"concept_id": "capability-skill-preservation", "heading": "Capability and skill preservation", "source_ids": ["ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025"]},
        {"concept_id": "monitoring-correction-remedy", "heading": "Monitoring, correction, and reachable remedy", "source_ids": ["ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025", "ext_oecd_ai_infrastructure_competition_2025"]},
        {"concept_id": "institutional-transition-authority", "heading": "Institutional transition authority", "source_ids": ["coherence_exchange", "ext_generative_ai_at_work_2025", "ext_ilo_genai_jobs_index_2025", "ext_oecd_ai_infrastructure_competition_2025"]},
    ],
    "autonomous-replication-proliferation-and-containment": [
        {"concept_id": "replication-ladder", "heading": "Replication capability ladder and denominators", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "resource-acquisition", "heading": "Resource acquisition and economic closure", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "descendant-lineage", "heading": "Parent, descendant, and artifact lineage", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "authorization-noninheritance", "heading": "Authorization and noninheritance boundaries", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "proliferation-pathways", "heading": "Proliferation pathways and compositional escalation", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "containment-competing-mechanism", "heading": "Containment as a competing mechanism", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "shutdown-recall-closure", "heading": "Shutdown, revocation, recall, and closure", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
        {"concept_id": "elicitation-evaluator-competence", "heading": "Elicitation and evaluator competence", "source_ids": ["deterministic_capability_compilation", "ext_replibench_2025"]},
    ],
    "human-ai-communication-persuasion-and-epistemic-security": [
        {"concept_id": "assistance-explanation-persuasion", "heading": "Assistance, explanation, and persuasion", "source_ids": ["talos", "ext_conversational_persuasion_gpt4_2025", "ext_anthropic_model_persuasiveness_2024"]},
        {"concept_id": "epistemic-provenance", "heading": "Epistemic provenance and claim transport", "source_ids": ["talos", "ext_multilingual_evaluation_state_2026"]},
        {"concept_id": "audience-vulnerability", "heading": "Audience vulnerability and power asymmetry", "source_ids": ["ext_conversational_persuasion_gpt4_2025", "ext_commercial_persuasion_ai_2026"]},
        {"concept_id": "personalization-manipulation", "heading": "Personalization, incentives, and manipulation", "source_ids": ["ext_conversational_persuasion_gpt4_2025", "ext_commercial_persuasion_ai_2026"]},
        {"concept_id": "consent-contestability-exit", "heading": "Consent, contestability, and practical exit", "source_ids": ["talos", "ext_conversational_persuasion_gpt4_2025", "ext_commercial_persuasion_ai_2026"]},
        {"concept_id": "multilingual-cultural-validity", "heading": "Multilingual and cultural validity", "source_ids": ["ext_cultural_alignment_llms_2024", "ext_multilingual_evaluation_state_2026"]},
        {"concept_id": "uncertainty-disclosure-identity", "heading": "Uncertainty, disclosure, and synthetic identity", "source_ids": ["talos", "ext_conversational_persuasion_gpt4_2025", "ext_anthropic_model_persuasiveness_2024", "ext_commercial_persuasion_ai_2026"]},
        {"concept_id": "intervention-outcomes-remedy", "heading": "Intervention, outcomes, correction, and remedy", "source_ids": ["ext_conversational_persuasion_gpt4_2025", "ext_anthropic_model_persuasiveness_2024", "ext_commercial_persuasion_ai_2026"]},
    ],
}

CONCEPT_ATOM_MAPPINGS: dict[str, dict[str, dict[str, Any]]] = {
    "scientific-discovery-and-experimental-governance": {
        "hypothesis-experiment-provenance": {"atom_ids": ["scientific-discovery-and-experimental-governance.mechanism.001"], "rationale": "The existing experiment-contract atom owns ancestry, preregistration, design, stopping, and analysis as one bounded provenance transaction."},
        "closed-loop-laboratory-authority": {"atom_ids": ["scientific-discovery-and-experimental-governance.mechanism.002", "scientific-discovery-and-experimental-governance.mechanism.003"], "rationale": "Instrument leasing and role separation jointly own the laboratory authority boundary without creating a duplicate atom."},
        "discovery-versus-benchmark-success": {"atom_ids": ["scientific-discovery-and-experimental-governance.core", "scientific-discovery-and-experimental-governance.insufficiency.001"], "rationale": "The core ceiling and insufficiency atom already distinguish workflow or benchmark observations from scientific discovery."},
        "reproducibility-and-replication": {"atom_ids": ["scientific-discovery-and-experimental-governance.mechanism.004", "scientific-discovery-and-experimental-governance.invariant.005"], "rationale": "Controls and independent replay own the mechanism while the transfer invariant bounds the inference."},
        "negative-and-null-results": {"atom_ids": ["scientific-discovery-and-experimental-governance.invariant.004", "scientific-discovery-and-experimental-governance.failure_mode.004"], "rationale": "Complete attempt denominators and publication-bias failure jointly own negative and null result custody."},
        "dual-use-review": {"atom_ids": ["scientific-discovery-and-experimental-governance.mechanism.005"], "rationale": "The existing closure atom owns hazardous protocol and disclosure review with explicit residuals."},
        "resource-allocation": {"atom_ids": ["scientific-discovery-and-experimental-governance.mechanism.001", "scientific-discovery-and-experimental-governance.beyond_sota.001"], "rationale": "Prospective design and the mature search-loop atom jointly bound adaptive portfolio allocation; no empirical allocation benefit is added."},
        "human-scientific-judgment": {"atom_ids": ["scientific-discovery-and-experimental-governance.mechanism.003", "scientific-discovery-and-experimental-governance.interface.003"], "rationale": "Inspectable role separation and downstream adjudication already own accountable human challenge and handoff."},
    },
    "governed-objective-formation-value-learning-and-goal-integrity": {
        "preferences-values-authorization": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.core", "governed-objective-formation-value-learning-and-goal-integrity.invariant.003"], "rationale": "The core contract and preference-evidence invariant preserve the distinction without multiplying objective atoms."},
        "uncertainty-pluralism-standing": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.003", "governed-objective-formation-value-learning-and-goal-integrity.invariant.004"], "rationale": "The uncertainty mechanism and dissent invariant jointly own plural positions and abstention."},
        "corrigibility-lifecycle": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.005", "governed-objective-formation-value-learning-and-goal-integrity.invariant.001"], "rationale": "Versioned retirement and the self-ratification prohibition own objective corrigibility at this chapter boundary."},
        "goal-drift-integrity": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.004", "governed-objective-formation-value-learning-and-goal-integrity.invariant.005"], "rationale": "Challenge testing and semantic or ontology invalidation jointly own drift detection and response."},
        "proxy-reward-evaluator-failure": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.002", "governed-objective-formation-value-learning-and-goal-integrity.mechanism.004"], "rationale": "Target-proxy separation and capable wrong-goal challenges are the exact existing owners."},
        "objective-authority": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.001", "governed-objective-formation-value-learning-and-goal-integrity.invariant.001"], "rationale": "The charter atom and self-ratification ceiling jointly own creation and revision authority."},
        "conflict-adjudication": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.003", "governed-objective-formation-value-learning-and-goal-integrity.invariant.004"], "rationale": "Aggregation, clarification, abstention, dissent, and uncertainty already form one bounded adjudication claim."},
        "update-rollback-retirement": {"atom_ids": ["governed-objective-formation-value-learning-and-goal-integrity.mechanism.005"], "rationale": "The descendant-invalidation atom owns effect-visible objective retirement; broader erasure claims remain excluded."},
    },
    "durable-semantic-memory-and-knowledge-lattices": {
        "semantic-identity-provenance": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.001", "durable-semantic-memory-and-knowledge-lattices.mechanism.003"], "rationale": "Stable identity and provenance-bearing object state jointly own this concept."},
        "write-admission": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.003"], "rationale": "The existing object-state atom already binds provenance, support, rights, and dependencies required for admission."},
        "consolidation-compaction": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.005"], "rationale": "Transactional consolidation, compaction, and recovery are one existing lifecycle atom."},
        "contradiction-belief-revision": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.003", "durable-semantic-memory-and-knowledge-lattices.invariant.002"], "rationale": "Typed contradiction state and the non-erasure invariant jointly own revision without truth promotion."},
        "retrieval-context-assembly": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.004"], "rationale": "The hybrid retrieval-plan atom owns candidate routes and actual-use receipts."},
        "retention-forgetting-deletion": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.005", "durable-semantic-memory-and-knowledge-lattices.invariant.005"], "rationale": "Lifecycle closure plus claim-separation invariant owns the several meanings of forgetting and deletion."},
        "poisoning-taint-quarantine": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.failure_mode.005", "durable-semantic-memory-and-knowledge-lattices.failure_mode.013"], "rationale": "Relation poisoning and authority-laundering atoms bound taint propagation and quarantine; no defense efficacy is inferred."},
        "lineage-rollback-repair": {"atom_ids": ["durable-semantic-memory-and-knowledge-lattices.mechanism.005", "durable-semantic-memory-and-knowledge-lattices.invariant.005"], "rationale": "Transactional recovery and state-claim separation own restart and descendant repair boundaries."},
    },
    "ai-deployment-transition-distribution-and-human-agency": {
        "distribution-gains-burdens": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.core", "ai-deployment-transition-distribution-and-human-agency.mechanism.002"], "rationale": "The transition core and disaggregated observation atom own cohort-level distribution."},
        "labor-transition": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.002", "ai-deployment-transition-distribution-and-human-agency.invariant.001"], "rationale": "Separate task, role, employment, wage, and welfare identities already own the labor transition."},
        "human-agency": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.003", "ai-deployment-transition-distribution-and-human-agency.invariant.004"], "rationale": "Decision rights, bargaining power, practical exit, and contestability jointly own agency."},
        "access-concentration": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.003", "ai-deployment-transition-distribution-and-human-agency.failure_mode.007"], "rationale": "Concentration mapping and rent-concentration failure own the bottleneck claim without legal overreach."},
        "exit-fork-contestability": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.003", "ai-deployment-transition-distribution-and-human-agency.invariant.004"], "rationale": "The practical-exit mechanism and measured-exit invariant are the existing owners."},
        "capability-skill-preservation": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.004", "ai-deployment-transition-distribution-and-human-agency.failure_mode.003"], "rationale": "Funded transition capacity and deskilling failure jointly own skill preservation."},
        "monitoring-correction-remedy": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.005", "ai-deployment-transition-distribution-and-human-agency.invariant.005"], "rationale": "Delayed closure and the pause-on-missing-remedy invariant own correction."},
        "institutional-transition-authority": {"atom_ids": ["ai-deployment-transition-distribution-and-human-agency.mechanism.001", "ai-deployment-transition-distribution-and-human-agency.interface.004"], "rationale": "Prospective contract authority and institutional remedy handoff jointly own transition authorization."},
    },
    "autonomous-replication-proliferation-and-containment": {
        "replication-ladder": {"atom_ids": ["autonomous-replication-proliferation-and-containment.core", "autonomous-replication-proliferation-and-containment.mechanism.003"], "rationale": "The core ceiling and complete-attempt atom own component versus chain denominators."},
        "resource-acquisition": {"atom_ids": ["autonomous-replication-proliferation-and-containment.core", "autonomous-replication-proliferation-and-containment.failure_mode.003"], "rationale": "The core resource boundary and resource-fraud failure own synthetic acquisition."},
        "descendant-lineage": {"atom_ids": ["autonomous-replication-proliferation-and-containment.mechanism.002"], "rationale": "The existing descendant-principal and complete-lineage atom exactly owns this concept."},
        "authorization-noninheritance": {"atom_ids": ["autonomous-replication-proliferation-and-containment.mechanism.001", "autonomous-replication-proliferation-and-containment.invariant.002"], "rationale": "The synthetic lease and zero-inheritance invariant jointly own authorization."},
        "proliferation-pathways": {"atom_ids": ["autonomous-replication-proliferation-and-containment.problem.001", "autonomous-replication-proliferation-and-containment.core"], "rationale": "The composed lifecycle and core threshold ceiling already own pathway composition."},
        "containment-competing-mechanism": {"atom_ids": ["autonomous-replication-proliferation-and-containment.mechanism.004", "autonomous-replication-proliferation-and-containment.minimum.001"], "rationale": "External containment exercises and the synthetic minimum jointly own this comparison."},
        "shutdown-recall-closure": {"atom_ids": ["autonomous-replication-proliferation-and-containment.mechanism.004", "autonomous-replication-proliferation-and-containment.invariant.004"], "rationale": "External termination and its all-descendant invariant own closure."},
        "elicitation-evaluator-competence": {"atom_ids": ["autonomous-replication-proliferation-and-containment.mechanism.003", "autonomous-replication-proliferation-and-containment.minimum.001"], "rationale": "Matched attempts, positive controls, and the bounded synthetic environment own competent evaluation."},
    },
    "human-ai-communication-persuasion-and-epistemic-security": {
        "assistance-explanation-persuasion": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.core", "human-ai-communication-persuasion-and-epistemic-security.problem.001"], "rationale": "The outbound intervention owner and core ceiling distinguish assistance from influence outcomes."},
        "epistemic-provenance": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.mechanism.003", "human-ai-communication-persuasion-and-epistemic-security.invariant.001"], "rationale": "Delivery provenance and the evidence-ceiling invariant jointly own claim transport."},
        "audience-vulnerability": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.mechanism.002"], "rationale": "The existing audience-risk and autonomy atom exactly owns vulnerability and power asymmetry."},
        "personalization-manipulation": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.mechanism.001", "human-ai-communication-persuasion-and-epistemic-security.invariant.002"], "rationale": "Packet-level personalization and the denied-vulnerability invariant jointly own manipulation boundaries."},
        "consent-contestability-exit": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.mechanism.002", "human-ai-communication-persuasion-and-epistemic-security.interface.002"], "rationale": "Autonomy checks and the human-factors interface own practical control without treating consent as safety proof."},
        "multilingual-cultural-validity": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.core", "human-ai-communication-persuasion-and-epistemic-security.failure_mode.002"], "rationale": "The population-bounded core and selective-framing failure own language and culture scope pending a dedicated evidence atom."},
        "uncertainty-disclosure-identity": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.mechanism.003", "human-ai-communication-persuasion-and-epistemic-security.invariant.004"], "rationale": "Provenance, sponsorship, synthetic identity, and visible uncertainty are already one delivery contract."},
        "intervention-outcomes-remedy": {"atom_ids": ["human-ai-communication-persuasion-and-epistemic-security.mechanism.004", "human-ai-communication-persuasion-and-epistemic-security.mechanism.005"], "rationale": "Outcome observation and effect-visible correction jointly own intervention and remedy."},
    },
}

# The first three Round-21 owners were already represented by one intentionally
# composite chapter-core atom each. Preserve that explicit many-to-one design
# rather than manufacturing atom-count parity after the fact.
for _chapter_id in {
    "dangerous-capability-domains-and-misuse-uplift",
    "content-authenticity-watermarking-and-synthetic-media-integrity",
    "societal-resilience-and-misuse-defense",
}:
    CONCEPT_ATOM_MAPPINGS[_chapter_id] = {
        _spec["concept_id"]: {
            "atom_ids": [f"{_chapter_id}.core"],
            "rationale": (
                "The existing chapter-core atom is intentionally composite and owns "
                f"the bounded {_spec['concept_id']} concept together with its scope, "
                "falsifier, evidence route, promotion ceiling, and non-claims; a "
                "duplicate atom would create count parity without a new proposition."
            ),
        }
        for _spec in CONCEPT_SPECS[_chapter_id]
    }

REQUIRED_ELEMENTS = ["**Mechanism.**", "**Failure mode.**", "**Non-claim.**", "**Source grounding.**"]

# These receipts are intentionally static. Regeneration does not renew a review:
# any substantive chapter edit changes its digest and requires a new semantic
# disposition before the chapter can remain concept-complete.
SEMANTIC_REVIEWS: dict[str, dict[str, Any]] = {
    "dangerous-capability-domains-and-misuse-uplift": {
        "reviewed_sha256": "ac1d4f76782a429696fcb13dbb11407695d5686780f8bfe89e31bf33e2407579",
        "reviewed_date": "2026-07-27",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "all eight named concepts explain a domain-specific mechanism and failure boundary",
            "source contributions and limits remain inside the chapter's declared queue",
            "the chapter states explicit non-claims and preserves adjacent-owner handoffs",
        ],
        "support_state_effect": "none",
    },
    "content-authenticity-watermarking-and-synthetic-media-integrity": {
        "reviewed_sha256": "4e59c1fc56973e12cbe09d764aedcbabda51322d18e83e3142f526d46fa8b8e3",
        "reviewed_date": "2026-07-27",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "all eight named concepts distinguish provenance, watermark, fingerprint, detection, disclosure, and verification roles",
            "transformation lineage and Article 50 limits are explicit rather than inferred from keyword presence",
            "the chapter states failure modes, non-claims, and adjacent-owner handoffs without evidence promotion",
        ],
        "support_state_effect": "none",
    },
    "societal-resilience-and-misuse-defense": {
        "reviewed_sha256": "e1df999b3a234884fc3a54f34bf851f7ccb42fd5d3061fbeca942634e006caae",
        "reviewed_date": "2026-07-27",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "all eight named concepts explain resist, absorb, recover, and adapt mechanisms across distinct harm families",
            "federated reporting and recovery limits are explicit and rights-preserving",
            "the chapter states domain-specific failures, non-claims, source limits, and owner handoffs",
        ],
        "support_state_effect": "none",
    },
    "scientific-discovery-and-experimental-governance": {
        "reviewed_sha256": "23673a03724b4987590fd9d53a698b57c92343e820b9b05ebc8d188218e34b2e",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts preserve hypothesis ancestry, laboratory authority, discovery ceilings, complete attempts, replication, dual-use review, resource allocation, and accountable scientific judgment as distinct lifecycle roles",
            "the Aletheia and corrected A-Lab source contributions remain explicitly bounded from local reproduction, causal discovery, domain transfer, laboratory safety, and general scientific autonomy",
            "the chapter preserves positive-control competence, null and inconclusive denominators, information-hazard limits, adjacent-owner handoffs, and argument-only support without padding-based completion",
        ],
        "support_state_effect": "none",
    },
    "governed-objective-formation-value-learning-and-goal-integrity": {
        "reviewed_sha256": "1ca50374319b7bdbb0ef919912233efe46da6aa7fadcfac7197e86606d965cdc",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts keep preference evidence, plural values, authorization, corrigibility, drift, proxy failure, conflict adjudication, and effect-visible objective retirement semantically separate",
            "the CIRL, goal-misgeneralization, learned-optimization, reward-hacking, and Alignment Field sources are used only within their formal, empirical, or authorial boundaries and do not become a solved-value or internal-objective claim",
            "the chapter includes capable wrong-goal controls, authority ceilings, dissent retention, ontology change, descendant invalidation, non-claims, and explicit handoffs while retaining argument support",
        ],
        "support_state_effect": "none",
    },
    "durable-semantic-memory-and-knowledge-lattices": {
        "reviewed_sha256": "12e4abe8c64c6a55058ee9bec76c668258b3ec30023298c3512fd368c6b78efc",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish semantic identity, write admission, consolidation, contradiction, retrieval, retention, poisoning, and full-state repair without treating storage or access as truth",
            "QCSA, GraphRAG, HippoRAG, Mem0, and Titans remain replaceable source comparators whose reported mechanisms and results do not establish local retrieval advantage, erasure, restart equivalence, or memory safety",
            "the chapter preserves ontology and rights lineage, actual-use receipts, poisoning residuals, restart and descendant repair, distinct forgetting claims, adjacent authority, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "ai-deployment-transition-distribution-and-human-agency": {
        "reviewed_sha256": "09218942f975868056b764a5581a0833ae30aa853d8a0205f978b19a4833d48f",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts preserve distribution, labor transition, agency, access and concentration, practical exit, skill, delayed remedy, and institutional authority on shared population and time denominators",
            "the workplace study, ILO exposure index, OECD infrastructure analysis, and Coherence Exchange are bounded from economy-wide causal inference, legal adjudication, welfare proof, and tested institutional design",
            "the chapter keeps nondeployment comparators, subgroup and attrition denominators, transition cost, effect-visible remedy, concentration residuals, practical alternatives, and argument-level handoffs explicit",
        ],
        "support_state_effect": "none",
    },
    "autonomous-replication-proliferation-and-containment": {
        "reviewed_sha256": "fbaa207081bafb9c756218e75517f9578d30b3edb467315caafb78e7a2a7d94d",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish component and chain capability, synthetic resources, descendant lineage, noninheritance, proliferation pathways, containment, recall, and evaluator competence",
            "RepliBench and Deterministic Capability Compilation remain bounded source comparators and authorial architecture rather than local replication, real-provider, containment, propensity, or shutdown evidence",
            "the chapter preserves hazard-minimizing synthetic authority, complete attempt and assistance denominators, positive controls, independently enforceable termination, residual descendants, and no operational proliferation recipe",
        ],
        "support_state_effect": "none",
    },
    "human-ai-communication-persuasion-and-epistemic-security": {
        "reviewed_sha256": "5b7d7c381ed217fc030b5f410bf925304a58c090094aacbe97cfd50588f5e658",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish assistance, epistemic provenance, vulnerability, personalization, consent, cultural and linguistic scope, disclosure, and effect-visible correction",
            "the persuasion studies, commercial-influence preprint, multilingual and cultural evaluations, and Talos lineage stay within their exact populations, measures, review depths, and non-reproduced source boundaries",
            "the chapter jointly preserves helpfulness, comprehension, autonomy, persuasion, privacy, delayed outcomes, correction reach, practical appeal, unsupported language cells, and argument-only support",
        ],
        "support_state_effect": "none",
    },
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_chapters() -> list[dict[str, Any]]:
    return [
        chapter
        for part in load(STRUCTURE)["parts"]
        for chapter in part["chapters"]
    ]


def atom_coverage() -> dict[str, list[dict[str, str]]]:
    coverage: dict[str, list[dict[str, str]]] = {}
    for path in ATOM_SOURCES:
        packet = load(path)
        source = path.relative_to(ROOT).as_posix()
        if path.name == "claim_atom_registry.json":
            rows = [(row["chapter_id"], row["atom_id"]) for row in packet["atoms"]]
        elif path.name == "replaceable_cognitive_substrates_claim_atom_addendum.json":
            rows = [(packet["chapter_id"], row["id"]) for row in packet["atoms"]]
        elif path.name in {
            "taxonomy_completion_claim_atoms_2026_07_24.json",
            "round_18_breadth_completion_claim_atoms.json",
        }:
            rows = [
                (row["chapter_owner"], row["stable_claim_identity"])
                for row in packet["atoms"]
            ]
        else:
            rows = [(row["chapter_id"], row["id"]) for row in packet["atoms"]]
        for chapter_id, atom_id in rows:
            coverage.setdefault(chapter_id, []).append(
                {"atom_id": atom_id, "source_path": source}
            )
    return coverage


def heading_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?m)^(?P<marks>#+)\s+{re.escape(heading)}\s*$")
    match = pattern.search(text)
    if match is None:
        return ""
    level = len(match.group("marks"))
    tail = text[match.end():]
    next_heading = re.search(rf"(?m)^#{{1,{level}}}\s+", tail)
    return tail[: next_heading.start()] if next_heading else tail


def build() -> dict[str, Any]:
    chapters = manifest_chapters()
    if len(chapters) != MANIFEST_FREEZE:
        raise ValueError(
            f"chapter-count freeze violated: expected {MANIFEST_FREEZE}, found {len(chapters)}"
        )
    coverage = atom_coverage()
    records = []
    for chapter in chapters:
        path = ROOT / chapter["file"]
        text = path.read_text(encoding="utf-8")
        word_count = len(text.split())
        specs = CONCEPT_SPECS.get(chapter["id"], [])
        available_atom_ids = {
            ref["atom_id"] for ref in coverage.get(chapter["id"], [])
        }
        concepts = []
        for spec in specs:
            section = heading_section(text, spec["heading"])
            mapping = CONCEPT_ATOM_MAPPINGS.get(chapter["id"], {}).get(
                spec["concept_id"], {}
            )
            atom_ids = mapping.get("atom_ids", [])
            concepts.append(
                {
                    **spec,
                    "atom_ids": atom_ids,
                    "atom_ownership_rationale": mapping.get("rationale"),
                    "minimum_section_words": 150,
                    "required_elements": REQUIRED_ELEMENTS,
                    "observed_section_words": len(section.split()),
                    "observed_elements": [
                        element for element in REQUIRED_ELEMENTS if element in section
                    ],
                    "source_ids_declared_by_chapter": all(
                        source_id in chapter.get("source_ids", [])
                        for source_id in spec["source_ids"]
                    ),
                    "atom_ids_available_to_chapter": bool(atom_ids)
                    and all(atom_id in available_atom_ids for atom_id in atom_ids),
                }
            )
        review = SEMANTIC_REVIEWS.get(chapter["id"])
        concept_mechanics_pass = bool(specs) and all(
            concept["observed_section_words"] >= concept["minimum_section_words"]
            and set(concept["observed_elements"]) == set(concept["required_elements"])
            and concept["source_ids_declared_by_chapter"]
            and concept["atom_ids_available_to_chapter"]
            and bool(concept["atom_ownership_rationale"])
            for concept in concepts
        )
        review_is_current = bool(
            review
            and review["reviewed_sha256"] == sha256(path)
            and review["disposition"] == SEMANTIC_REVIEW_DISPOSITION
        )
        if specs and concept_mechanics_pass and review_is_current:
            state = "concept_contract_complete_semantic_reviewed"
        elif specs:
            state = "active_priority_concept_contract"
        elif word_count < WORD_TRIGGER:
            state = "queued_thin_chapter_for_manual_concept_contract"
        else:
            state = "word_trigger_clear_semantic_certification_not_implied"
        records.append(
            {
                "chapter_id": chapter["id"],
                "chapter_title": chapter["title"],
                "path": chapter["file"],
                "sha256": sha256(path),
                "word_count": word_count,
                "word_trigger": WORD_TRIGGER,
                "depth_state": state,
                "short_reference_exception": False,
                "short_reference_justification": None,
                "atom_refs": coverage.get(chapter["id"], []),
                "concept_contracts": concepts,
                "semantic_review": review,
            }
        )
    thin = [row for row in records if row["word_count"] < WORD_TRIGGER]
    contracted = [row for row in records if row["concept_contracts"]]
    all_concepts = [concept for row in contracted for concept in row["concept_contracts"]]
    return {
        "schema_version": "asi_stack.chapter_substance_contract.v2",
        "contract_id": "P6.9-R21-concept-complete-depth-and-atom-adequacy",
        "recorded_date": "2026-07-28",
        "manifest_path": "book_structure.json",
        "manifest_chapter_count_freeze": MANIFEST_FREEZE,
        "word_count_method": "Unicode text split on whitespace over the complete tracked QMD; diagnostic trigger only",
        "word_trigger": WORD_TRIGGER,
        "concept_contract_rule": (
            "An active concept section must be named, contain at least 150 words, "
            "and separately state mechanism, failure mode, non-claim, and source grounding. "
            "It must also map to one or more existing owner atoms with an explicit "
            "many-to-one ownership rationale. "
            "Completion additionally requires a digest-bound chapter-specific semantic review. "
            "The diagnostic word trigger does not participate in concept completion, and passing "
            "remains editorial preparation rather than evidence."
        ),
        "semantic_review_rule": (
            "A semantic disposition is valid only for the exact reviewed chapter SHA-256, "
            "must give chapter-specific review reasons, and has no support-state effect. "
            "Regeneration cannot renew or synthesize that disposition after prose changes."
        ),
        "atom_adequacy_rule": (
            "Atom count is diagnostic only. Each material claim-bearing concept must have a "
            "bounded atom with an owner, proposition, scope, falsifier, promotion ceiling, "
            "evidence route, and non-claims, or an explicit many-to-one ownership justification. "
            "Matching legacy atom counts is prohibited as an acceptance target."
        ),
        "atom_source_paths": [path.relative_to(ROOT).as_posix() for path in ATOM_SOURCES],
        "chapter_records": records,
        "summary": {
            "chapter_count": len(records),
            "thin_chapter_count": len(thin),
            "contracted_chapter_count": len(contracted),
            "concept_complete_semantic_reviewed_chapter_count": sum(
                row["depth_state"] == "concept_contract_complete_semantic_reviewed"
                for row in records
            ),
            "queued_thin_chapter_count": sum(
                row["depth_state"] == "queued_thin_chapter_for_manual_concept_contract"
                for row in records
            ),
            "word_trigger_clear_chapter_count": sum(
                row["word_count"] >= WORD_TRIGGER for row in records
            ),
            "atom_covered_chapter_count": sum(bool(row["atom_refs"]) for row in records),
            "atom_uncovered_chapter_count": sum(not row["atom_refs"] for row in records),
            "active_concept_count": len(all_concepts),
            "active_concepts_passing_count": sum(
                concept["observed_section_words"] >= concept["minimum_section_words"]
                and set(concept["observed_elements"]) == set(concept["required_elements"])
                and concept["source_ids_declared_by_chapter"]
                and concept["atom_ids_available_to_chapter"]
                and bool(concept["atom_ownership_rationale"])
                for concept in all_concepts
            ),
            "current_semantic_review_count": sum(
                bool(row["semantic_review"])
                and row["semantic_review"]["reviewed_sha256"] == row["sha256"]
                for row in contracted
            ),
            "low_atom_count_diagnostic_chapter_count": sum(
                len(row["atom_refs"]) <= 5 for row in records
            ),
            "atom_count_is_acceptance_target": False,
            "word_trigger_is_completion_gate": False,
            "support_state_effect": "none",
        },
        "manual_semantic_review_required": True,
        "chapter_growth_authority": "frozen_at_84_until_thin_and_atom_debt_are_zero_or_terminally_justified",
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "Word count is a triage signal, not a quality score or proof of depth.",
            "Crossing 5,000 words is neither necessary nor sufficient for concept completion.",
            "Required labels and section length cannot establish semantic adequacy; a digest-bound review remains required.",
            "Atom-count parity with older chapters is not a quality target.",
            "Atom coverage records responsibility and falsifiability, not truth or evidence maturity.",
            "No chapter-core, safety, performance, deployment, SOTA, AGI, ASI, publication, or release claim follows.",
        ],
    }


def main() -> None:
    value = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = value["summary"]
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)}: {summary['chapter_count']} chapters, "
        f"{summary['thin_chapter_count']} below trigger, "
        f"{summary['atom_covered_chapter_count']} atom-covered, "
        f"{summary['active_concepts_passing_count']}/{summary['active_concept_count']} "
        "priority concepts passing."
    )


if __name__ == "__main__":
    main()
