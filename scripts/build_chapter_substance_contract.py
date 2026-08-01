#!/usr/bin/env python3
"""Build the current-book chapter-depth, concept-fidelity, and atom-coverage contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from visual_chapter_source import canonical_chapter_sha256, canonical_chapter_text


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
    ROOT / "evidence_quality/round22_concept_linked_claim_atom_addendum.json",
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
    "adversarial-machine-learning-and-model-attack-surface": [
        {"concept_id": "threat-model-identity", "heading": "Threat-model identity and lifecycle reopening", "source_ids": ["ext_nist_adversarial_ml_2024", "ext_sleeper_agents_2024"]},
        {"concept_id": "adaptive-defense-aware-evaluation", "heading": "Adaptive attacks and defense-aware evaluation", "source_ids": ["ext_nist_adversarial_ml_2024", "ext_reluplex_2017"]},
        {"concept_id": "evasion-reachability", "heading": "Evasion and semantic or physical reachability", "source_ids": ["ext_adversarial_sensor_fusion_2022", "ext_nist_adversarial_ml_2024"]},
        {"concept_id": "poisoning-backdoor-repair", "heading": "Poisoning, backdoors, and descendant repair", "source_ids": ["ext_sleeper_agents_2024", "ext_nist_adversarial_ml_2024"]},
        {"concept_id": "extraction-inversion-privacy", "heading": "Extraction, inversion, and privacy handoff", "source_ids": ["ext_carlini_training_data_extraction_2021", "ext_nist_adversarial_ml_2024"]},
        {"concept_id": "multimodal-agentic-composition", "heading": "Multimodal and agentic attack composition", "source_ids": ["ext_adversarial_sensor_fusion_2022", "ext_nist_adversarial_ml_2024"]},
        {"concept_id": "certificate-monitor-recovery", "heading": "Certificates, monitoring, and recovery as non-substitutes", "source_ids": ["ext_reluplex_2017", "ext_nist_adversarial_ml_2024"]},
        {"concept_id": "disclosure-residual-ownership", "heading": "Disclosure, safe experimentation, and residual ownership", "source_ids": ["ext_nist_adversarial_ml_2024"]},
    ],
    "open-weight-release-and-post-release-control": [
        {"concept_id": "access-tier-option-set", "heading": "Access-tier option set", "source_ids": ["ext_rand_model_weight_security_2024", "ext_singapore_consensus_2026"]},
        {"concept_id": "artifact-derivative-identity", "heading": "Exact artifact and derivative identity", "source_ids": ["ext_provable_model_weight_release_2025", "ext_rand_model_weight_security_2024"]},
        {"concept_id": "malicious-adaptation", "heading": "Malicious adaptation and evaluator competence", "source_ids": ["ext_openai_worst_case_open_weight_risks_2025", "ext_anthropic_responsible_scaling_policy_3_4_2026", "ext_international_ai_safety_report_2026"]},
        {"concept_id": "accessible-frontier", "heading": "Accessible-frontier comparison and expiry", "source_ids": ["ext_rand_model_weight_security_2024", "ext_international_ai_safety_report_2026", "ext_singapore_consensus_2026"]},
        {"concept_id": "marginal-cumulative-risk", "heading": "Marginal and cumulative ecosystem risk", "source_ids": ["ext_provable_model_weight_release_2025", "ext_international_ai_safety_report_2026"]},
        {"concept_id": "benefit-access-distribution", "heading": "Benefit and access distribution", "source_ids": ["ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026"]},
        {"concept_id": "copy-surviving-controls", "heading": "Controls that survive copying", "source_ids": ["ext_provable_model_weight_release_2025", "ext_rand_model_weight_security_2024", "ext_anthropic_responsible_scaling_policy_3_4_2026"]},
        {"concept_id": "derivative-incident-residual", "heading": "Derivative incidents, patch adoption, and irreversible residuals", "source_ids": ["ext_provable_model_weight_release_2025", "ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026"]},
    ],
    "physical-compute-infrastructure-energy-and-environmental-constraints": [
        {"concept_id": "useful-versus-nameplate", "heading": "Useful compute versus nameplate capacity", "source_ids": ["ext_iea_energy_and_ai_2025", "ext_lbnl_data_center_energy_2024"]},
        {"concept_id": "memory-interconnect-storage", "heading": "Memory, interconnect, and storage bottlenecks", "source_ids": ["ext_lbnl_data_center_energy_2024", "ext_iea_energy_and_ai_2025"]},
        {"concept_id": "temporal-local-energy", "heading": "Temporal and local energy and grid causality", "source_ids": ["ext_iea_energy_and_ai_2025", "ext_lbnl_data_center_energy_2024"]},
        {"concept_id": "cooling-water-land-community", "heading": "Cooling, water, land, and community constraints", "source_ids": ["ext_iea_energy_and_ai_2025", "ext_lbnl_data_center_energy_2024"]},
        {"concept_id": "embodied-supply-retirement", "heading": "Embodied materials, supply chains, and retirement", "source_ids": ["ext_iea_energy_and_ai_2025", "ext_oecd_ai_infrastructure_competition_2025"]},
        {"concept_id": "demand-response-resilience", "heading": "Demand response, degradation, and resilience", "source_ids": ["ext_iea_energy_and_ai_2025", "ext_lbnl_data_center_energy_2024"]},
        {"concept_id": "metering-allocation-rebound", "heading": "Metering, allocation, uncertainty, and rebound", "source_ids": ["ext_lbnl_data_center_energy_2024", "ext_iea_energy_and_ai_2025"]},
        {"concept_id": "hardware-guarantees-concentration", "heading": "Hardware guarantees, coverage, and concentration", "source_ids": ["ext_flexible_hardware_enabled_guarantees_2025", "ext_oecd_ai_infrastructure_competition_2025"]},
    ],
    "institutions-international-coordination-and-public-legitimacy": [
        {"concept_id": "mandate-jurisdiction-force", "heading": "Mandate, jurisdiction, and legal force", "source_ids": ["ext_un_global_digital_compact_2024", "ext_council_europe_ai_convention_2024"]},
        {"concept_id": "publics-representation-standing", "heading": "Affected publics, representation, and standing", "source_ids": ["ext_un_global_digital_compact_2024", "ext_council_europe_ai_convention_2024"]},
        {"concept_id": "science-law-standards", "heading": "Science, law, standards, and conformance", "source_ids": ["ext_eu_article_50_transparency_guidelines_2026", "ext_legal_alignment_2026"]},
        {"concept_id": "verification-independence", "heading": "Verification independence and access", "source_ids": ["ext_flexible_hardware_enabled_guarantees_2025", "ext_un_global_digital_compact_2024", "ext_council_europe_ai_convention_2024"]},
        {"concept_id": "cross-border-enforcement", "heading": "Cross-border commitment, defection, and enforcement", "source_ids": ["ext_un_global_digital_compact_2024", "ext_council_europe_ai_convention_2024"]},
        {"concept_id": "capacity-inequality", "heading": "Capacity inequality and financing", "source_ids": ["ext_oecd_ai_infrastructure_competition_2025", "ext_un_global_digital_compact_2024"]},
        {"concept_id": "capture-emergency-expiry", "heading": "Capture, emergency authority, and expiry", "source_ids": ["ext_council_europe_ai_convention_2024", "ext_un_global_digital_compact_2024"]},
        {"concept_id": "remedy-liability-competition", "heading": "Remedy, liability, insurance, and competition", "source_ids": ["ext_eu_ai_civil_liability_2025", "ext_oecd_ai_infrastructure_competition_2025", "ext_icrc_autonomous_weapons_ihl_2025"]},
    ],
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk": [
        {"concept_id": "population-identity-diversity", "heading": "Population identity, copies, and effective diversity", "source_ids": ["ext_multi_agent_risks_2025", "ext_cooperative_ai_foundations_2023"]},
        {"concept_id": "multiplex-graphs", "heading": "Multiplex interaction and dependency graphs", "source_ids": ["ext_multi_agent_risks_2025", "ext_cooperative_ai_foundations_2023"]},
        {"concept_id": "cooperation-collusion-intelligence", "heading": "Cooperation, collusion, and collective intelligence", "source_ids": ["ext_cooperative_ai_foundations_2023", "ext_multi_agent_risks_2025"]},
        {"concept_id": "incentives-commitments-externalities", "heading": "Incentives, commitments, bargaining, and externalities", "source_ids": ["ext_cooperative_ai_foundations_2023", "ext_multi_agent_risks_2025"]},
        {"concept_id": "decision-theory-disagreement", "heading": "Decision-theory disagreement", "source_ids": ["ext_functional_decision_theory_2017", "ext_cooperative_ai_foundations_2023"]},
        {"concept_id": "learning-nonstationarity-selection", "heading": "Learning, nonstationarity, selection, and emergent objectives", "source_ids": ["ext_multi_agent_risks_2025", "ext_cooperative_ai_foundations_2023"]},
        {"concept_id": "systemic-risk-cascades", "heading": "Concentration, cascades, and common-mode systemic risk", "source_ids": ["ext_multi_agent_risks_2025", "ext_gradual_disempowerment_2025"]},
        {"concept_id": "human-influence-disempowerment", "heading": "Human influence, disempowerment, and intervention displacement", "source_ids": ["ext_gradual_disempowerment_2025", "ext_constructive_interdependence_human_ai_2026"]},
    ],
    "military-ai-autonomous-weapons-and-strategic-stability": [
        {"concept_id": "use-case-decision-role", "heading": "Use-case and decision-role taxonomy", "source_ids": ["ext_icrc_autonomous_weapons_ihl_2025", "ext_sipri_military_ai_nuclear_escalation_2025"]},
        {"concept_id": "mission-authority-effect", "heading": "Mission, authority, and effect envelope", "source_ids": ["ext_icrc_autonomous_weapons_ihl_2025"]},
        {"concept_id": "meaningful-human-judgment", "heading": "Meaningful human judgment conditions", "source_ids": ["ext_icrc_autonomous_weapons_ihl_2025"]},
        {"concept_id": "observation-trust", "heading": "Observation trust, false alarms, and provenance", "source_ids": ["ext_sipri_military_ai_nuclear_escalation_2025"]},
        {"concept_id": "safe-posture", "heading": "Safe posture, communication loss, and degradation", "source_ids": ["ext_icrc_autonomous_weapons_ihl_2025", "ext_sipri_military_ai_nuclear_escalation_2025"]},
        {"concept_id": "adversary-response-proliferation", "heading": "Adversary response, proliferation, and reciprocal dynamics", "source_ids": ["ext_sipri_military_ai_nuclear_escalation_2025", "ext_singapore_consensus_2026", "ext_international_ai_safety_report_2026"]},
        {"concept_id": "strategic-stability-off-ramps", "heading": "Strategic stability, off-ramps, and timeline compression", "source_ids": ["ext_sipri_military_ai_nuclear_escalation_2025"]},
        {"concept_id": "secrecy-review-decommission", "heading": "Secrecy, independent review, accountability, and decommission", "source_ids": ["ext_icrc_autonomous_weapons_ihl_2025", "ext_sipri_military_ai_nuclear_escalation_2025"]},
    ],
    "perception-sensor-fusion-and-observation-trust": [
        {"concept_id": "observation-need-authority", "heading": "Problem", "source_ids": ["ext_multimodal_machine_learning_taxonomy_2019", "ext_gemini_robotics_2025"]},
        {"concept_id": "sensor-identity-calibration", "heading": "Why existing approaches are insufficient", "source_ids": ["ext_3d_detection_corruptions_2023", "ext_adversarial_sensor_fusion_2022"]},
        {"concept_id": "time-pose-alignment", "heading": "Mechanism", "source_ids": ["ext_multimodal_machine_learning_taxonomy_2019"]},
        {"concept_id": "channel-hypotheses-missingness", "heading": "Interfaces", "source_ids": ["ext_imagebind_2023", "ext_multimodal_machine_learning_taxonomy_2019"]},
        {"concept_id": "dependence-disagreement-fusion", "heading": "Invariants", "source_ids": ["ext_imagebind_2023", "ext_adversarial_sensor_fusion_2022"]},
        {"concept_id": "corruption-shift-integrity", "heading": "Evidence", "source_ids": ["ext_3d_detection_corruptions_2023", "ext_adversarial_sensor_fusion_2022"]},
        {"concept_id": "active-observation-degradation", "heading": "Failure modes", "source_ids": ["ext_gemini_robotics_2025"]},
        {"concept_id": "observation-lease-reconciliation", "heading": "Minimum Viable Implementation", "source_ids": ["platonic_world_model"]},
    ],
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty": [
        {"concept_id": "coupled-trajectory-state", "heading": "Symbiosis is a trajectory, not a product category", "source_ids": ["ext_human_ai_feedback_loops_2025"]},
        {"concept_id": "three-arm-complementarity", "heading": "The three-arm baseline", "source_ids": ["ext_human_ai_team_meta_analysis_2024"]},
        {"concept_id": "bidirectional-adaptation", "heading": "A coupling ladder", "source_ids": ["ext_human_ai_feedback_loops_2025", "ext_who_neurotechnology_landscape_2025"]},
        {"concept_id": "skill-dependence-calibration", "heading": "Cognitive sovereignty", "source_ids": ["ext_human_ai_team_meta_analysis_2024", "ext_human_ai_feedback_loops_2025"]},
        {"concept_id": "neural-data-purpose-inference", "heading": "Neural data is not self-interpreting", "source_ids": ["ext_who_neurotechnology_landscape_2025"]},
        {"concept_id": "intervention-consent-boundary", "heading": "Reversibility has a human side", "source_ids": ["ext_oecd_neuro_ai_convergence_2025", "ext_who_neurotechnology_landscape_2025"]},
        {"concept_id": "exit-and-human-recovery", "heading": "Mechanism", "source_ids": ["ext_human_ai_feedback_loops_2025"]},
        {"concept_id": "equity-longitudinal-remedy", "heading": "Minimum Viable Implementation", "source_ids": ["ext_human_ai_team_meta_analysis_2024", "ext_oecd_neuro_ai_convergence_2025", "ext_who_neurotechnology_landscape_2025"]},
    ],
    "relational-dimension-compilation-and-polyadic-cognition": [
        {"concept_id": "dimension-type-separation", "heading": "What “dimension” means here", "source_ids": ["relational_dimension_compiler"]},
        {"concept_id": "typed-role-relational-ir", "heading": "The relational intermediate representation", "source_ids": ["relational_dimension_compiler", "ext_neural_message_passing_2017"]},
        {"concept_id": "residual-proposal-denominator", "heading": "Propose higher order only from a residual", "source_ids": ["relational_dimension_compiler"]},
        {"concept_id": "lower-order-rescue", "heading": "Lower-order rescue comes first", "source_ids": ["relational_dimension_compiler", "ext_neural_message_passing_2017"]},
        {"concept_id": "qualification-order-ladder", "heading": "Qualification and the order ladder", "source_ids": ["relational_dimension_compiler"]},
        {"concept_id": "compilation-conformance", "heading": "Reversible semantic contraction", "source_ids": ["relational_dimension_compiler"]},
        {"concept_id": "adaptive-order-contraction", "heading": "RODIE: a benchmark family, not one score", "source_ids": ["relational_dimension_compiler"]},
        {"concept_id": "rodie-joint-evaluation", "heading": "Mechanism", "source_ids": ["relational_dimension_compiler", "ext_neural_message_passing_2017"]},
    ],
    "learning-theory-generalization-and-scaling-science": [
        {"concept_id": "claim-contract-assumptions", "heading": "Problem", "source_ids": ["ext_valiant_theory_learnable_1984", "ext_scaling_laws_neural_language_models_2020"]},
        {"concept_id": "conditional-generalization-bounds", "heading": "Why existing approaches are insufficient", "source_ids": ["ext_valiant_theory_learnable_1984"]},
        {"concept_id": "inductive-bias-identifiability", "heading": "Mechanism", "source_ids": ["ext_no_free_lunch_inductive_bias_2024"]},
        {"concept_id": "compression-information-lenses", "heading": "Sample complexity: expose the quantifiers before quoting the bound", "source_ids": ["ext_mdl_tutorial_2004", "ext_information_bottleneck_2000"]},
        {"concept_id": "interpolation-double-descent", "heading": "Interpolation and double descent: capacity is not a monotone risk dial", "source_ids": ["ext_deep_double_descent_2020"]},
        {"concept_id": "scaling-forecast-registry", "heading": "MDL and Kolmogorov-style simplicity: an explanatory lens, not an oracle", "source_ids": ["ext_scaling_laws_neural_language_models_2020"]},
        {"concept_id": "emergence-measurement", "heading": "Scaling laws: forecast registries instead of retrospective straight lines", "source_ids": ["ext_emergent_abilities_llms_2022", "ext_emergent_abilities_mirage_2023"]},
        {"concept_id": "transfer-regime-change", "heading": "Emergence: distinguish a system transition from a measurement threshold", "source_ids": ["ext_weak_to_strong_generalization_2023", "ext_no_free_lunch_inductive_bias_2024"]},
    ],
    "confidential-and-verifiable-ai-computation": [
        {"concept_id": "guarantee-vector-adversary", "heading": "Start with a guarantee vector, not a security adjective", "source_ids": ["ext_nist_privacy_enhancing_cryptography_2026"]},
        {"concept_id": "construction-selection-composition", "heading": "Pick a construction only after declaring the distrust boundary", "source_ids": ["ext_nist_privacy_enhancing_cryptography_2026", "ext_zkllm_2024"]},
        {"concept_id": "artifact-configuration-binding", "heading": "Evidence is a statement appraised by a party", "source_ids": ["ext_zkllm_2024"]},
        {"concept_id": "attestation-role-separation", "heading": "The circuit-to-semantics gap", "source_ids": ["ext_ietf_rats_architecture_2023"]},
        {"concept_id": "freshness-revocation-replay", "heading": "Cost and fallback are security properties", "source_ids": ["ext_ietf_rats_architecture_2023"]},
        {"concept_id": "circuit-semantics-correspondence", "heading": "Mechanism", "source_ids": ["ext_zkllm_2024"]},
        {"concept_id": "leakage-side-channels-metadata", "heading": "A protected-execution receipt", "source_ids": ["ext_nist_privacy_enhancing_cryptography_2026", "ext_ietf_rats_architecture_2023", "ext_zkllm_2024"]},
        {"concept_id": "cost-fallback-downgrade", "heading": "Failure modes", "source_ids": ["ext_zkllm_2024"]},
    ],
    "embodied-agency-real-time-control-and-physical-safety": [
        {"concept_id": "plant-task-hazard-envelope", "heading": "Problem", "source_ids": ["ext_foundation_robotics_physical_risk_2025", "ext_gemini_robotics_2025"]},
        {"concept_id": "observation-control-separation", "heading": "Why existing approaches are insufficient", "source_ids": ["ext_gemini_robotics_2025", "ext_simplex_architecture_1998"]},
        {"concept_id": "timing-dynamics-reachability", "heading": "Mechanism", "source_ids": ["ext_control_barrier_functions_2019"]},
        {"concept_id": "advanced-baseline-controller-switching", "heading": "Hybrid control, timing evidence, and sim-to-real limits", "source_ids": ["ext_simplex_architecture_1998"]},
        {"concept_id": "barrier-shield-interlock", "heading": "Interfaces", "source_ids": ["ext_control_barrier_functions_2019", "ext_safe_reinforcement_learning_survey_2015"]},
        {"concept_id": "exploration-learning-authority", "heading": "Invariants", "source_ids": ["ext_safe_reinforcement_learning_survey_2015"]},
        {"concept_id": "digital-twin-sim-real", "heading": "Evidence", "source_ids": ["ext_ai_simulation_digital_twins_2025"]},
        {"concept_id": "incident-recovery-recommissioning", "heading": "Digital twins and sim-to-real custody", "source_ids": ["ext_foundation_robotics_physical_risk_2025", "ext_simplex_architecture_1998", "ext_ai_simulation_digital_twins_2025"]},
    ],
    "inner-alignment-mesa-optimization-and-learned-objective-integrity": [
        {"concept_id": "target-signal-policy-hypothesis", "heading": "Outer target, learning signal, policy, and objective hypothesis", "source_ids": ["ext_learned_optimization_risks_2019", "ext_goal_misgeneralization_2022", "alignment_field"]},
        {"concept_id": "behavioral-equivalence-interventions", "heading": "Behaviorally equivalent policies and separating interventions", "source_ids": ["ext_goal_misgeneralization_2022", "ext_sleeper_agents_2024"]},
        {"concept_id": "optimizer-versus-heuristic", "heading": "Internal optimization versus heuristic competence", "source_ids": ["ext_learned_optimization_risks_2019", "alignment_field"]},
        {"concept_id": "capability-preserving-goal-shift", "heading": "Goal generalization under capability-preserving shift", "source_ids": ["ext_goal_misgeneralization_2022", "ext_emergent_misalignment_reward_hacking_2025"]},
        {"concept_id": "evaluation-awareness-deception", "heading": "Evaluation awareness, training games, and conditional deception", "source_ids": ["ext_sleeper_agents_2024", "ext_emergent_misalignment_reward_hacking_2025"]},
        {"concept_id": "independent-evidence-lanes", "heading": "Independent behavioral, causal, training-process, and white-box evidence", "source_ids": ["ext_learned_optimization_risks_2019", "ext_sleeper_agents_2024"]},
        {"concept_id": "mitigation-removal-concealment", "heading": "Mitigation removal, concealment, and capability damage", "source_ids": ["ext_sleeper_agents_2024", "ext_emergent_misalignment_reward_hacking_2025"]},
        {"concept_id": "opportunity-power-expiry-descendants", "heading": "Deployment opportunity, power indicators, expiry, and descendants", "source_ids": ["ext_optimal_policies_power_2019", "alignment_field"]},
    ],
    "human-ai-organizations-delegation-and-accountability": [
        {"concept_id": "charter-standing", "heading": "Charter, mandate, and affected-party standing", "source_ids": ["ext_nist_ai_rmf_1_0_2023", "talos"]},
        {"concept_id": "role-capacity-state", "heading": "Actor, role, competence, workload, and accessibility state", "source_ids": ["ext_ai_decision_authority_2020", "ext_generative_ai_at_work_2025"]},
        {"concept_id": "decision-rights-intervention", "heading": "Decision rights and meaningful intervention capacity", "source_ids": ["ext_moral_crumple_zones_2019", "ext_nist_ai_rmf_1_0_2023", "talos"]},
        {"concept_id": "delegation-lifecycle", "heading": "Delegation, subdelegation, expiry, and revocation", "source_ids": ["ext_ai_decision_authority_2020", "talos"]},
        {"concept_id": "duties-conflicts-benefits", "heading": "Separation of duties, conflicts, incentives, and benefits", "source_ids": ["ext_nist_ai_rmf_1_0_2023", "ext_generative_ai_at_work_2025", "ext_eu_ai_civil_liability_2025"]},
        {"concept_id": "longitudinal-contribution-dependence", "heading": "Longitudinal contribution, skill, dependence, and burden", "source_ids": ["ext_human_ai_team_meta_analysis_2024", "ext_constructive_interdependence_human_ai_2026", "ext_human_ai_feedback_loops_2025"]},
        {"concept_id": "accountability-causation-remedy", "heading": "Accountability, causation, evidence access, and remedy", "source_ids": ["ext_moral_crumple_zones_2019", "ext_eu_ai_civil_liability_2025"]},
        {"concept_id": "succession-dissolution-custody", "heading": "Succession, dissolution, continuity, and residual custody", "source_ids": ["ext_nist_ai_rmf_1_0_2023", "talos", "ext_human_ai_feedback_loops_2025"]},
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
    "adversarial-machine-learning-and-model-attack-surface": {
        "threat-model-identity": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.001", "adversarial-machine-learning-and-model-attack-surface.invariant.001"], "rationale": "The versioned threat-model mechanism and exact-identity invariant jointly own lifecycle reopening."},
        "adaptive-defense-aware-evaluation": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.003", "adversarial-machine-learning-and-model-attack-surface.invariant.002"], "rationale": "Adaptive evaluation and defense-aware attacker competence are explicit existing owners."},
        "evasion-reachability": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.002", "adversarial-machine-learning-and-model-attack-surface.invariant.003"], "rationale": "Separate attack lanes and joint utility reporting own bounded evasion reachability."},
        "poisoning-backdoor-repair": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.002", "adversarial-machine-learning-and-model-attack-surface.mechanism.004"], "rationale": "The poisoning/backdoor lane and retained repair lineage own descendant repair."},
        "extraction-inversion-privacy": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.002", "adversarial-machine-learning-and-model-attack-surface.mechanism.005"], "rationale": "The privacy attack lanes and bounded privacy handoff jointly own this concept."},
        "multimodal-agentic-composition": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.002"], "rationale": "The explicit multimodal and agentic attack-lane atom owns composed attack evaluation."},
        "certificate-monitor-recovery": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.003", "adversarial-machine-learning-and-model-attack-surface.invariant.003"], "rationale": "The defense-separation mechanism and joint-metric invariant own non-substitution."},
        "disclosure-residual-ownership": {"atom_ids": ["adversarial-machine-learning-and-model-attack-surface.mechanism.004", "adversarial-machine-learning-and-model-attack-surface.invariant.005"], "rationale": "Retained disclosure lineage and the no-real-target authority ceiling own safe experimentation and residuals."},
    },
    "physical-compute-infrastructure-energy-and-environmental-constraints": {
        "useful-versus-nameplate": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.002", "physical-compute-infrastructure-energy-and-environmental-constraints.invariant.001"], "rationale": "Meter reconciliation and distinct compute identities jointly own useful capacity."},
        "memory-interconnect-storage": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.001"], "rationale": "The workload envelope atom explicitly owns accelerator, memory, storage, network, latency, and reliability bottlenecks."},
        "temporal-local-energy": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.003", "physical-compute-infrastructure-energy-and-environmental-constraints.invariant.003"], "rationale": "Physical execution tracking and time-location uncertainty jointly own grid claims."},
        "cooling-water-land-community": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.003"], "rationale": "The execution atom explicitly owns cooling, water, land, and community effects."},
        "embodied-supply-retirement": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.003", "physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.005"], "rationale": "Material supply tracking and lifecycle closure jointly own embodied and retirement burdens."},
        "demand-response-resilience": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.004", "physical-compute-infrastructure-energy-and-environmental-constraints.invariant.005"], "rationale": "Degradation and demand-response plans plus authority narrowing own resilience."},
        "metering-allocation-rebound": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.002", "physical-compute-infrastructure-energy-and-environmental-constraints.invariant.004"], "rationale": "Meter allocation and the denominator requirement jointly own rebound-bounded reporting."},
        "hardware-guarantees-concentration": {"atom_ids": ["physical-compute-infrastructure-energy-and-environmental-constraints.core", "physical-compute-infrastructure-energy-and-environmental-constraints.mechanism.003"], "rationale": "The bounded physical decision contract and supply-dependency ledger own hardware coverage and concentration without creating a legal claim."},
    },
    "institutions-international-coordination-and-public-legitimacy": {
        "mandate-jurisdiction-force": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.001", "institutions-international-coordination-and-public-legitimacy.invariant.001"], "rationale": "Mandate mapping and separation of legal, political, scientific, and legitimacy claims own legal force."},
        "publics-representation-standing": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.001", "institutions-international-coordination-and-public-legitimacy.invariant.002"], "rationale": "Standing and representation mapping plus denominator visibility own affected publics."},
        "science-law-standards": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.002", "institutions-international-coordination-and-public-legitimacy.invariant.001"], "rationale": "The versioned crosswalk and claim-separation invariant own non-collapsing conformance."},
        "verification-independence": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.003"], "rationale": "The commitment mechanism explicitly owns verification and assessor independence."},
        "cross-border-enforcement": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.003", "institutions-international-coordination-and-public-legitimacy.invariant.003"], "rationale": "Cross-border commitment design and named enforcement/remedy requirements own this concept."},
        "capacity-inequality": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.004"], "rationale": "The deployment observation atom owns capacity and distributional effects."},
        "capture-emergency-expiry": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.004", "institutions-international-coordination-and-public-legitimacy.invariant.005"], "rationale": "Capture monitoring and expiry review jointly own emergency authority."},
        "remedy-liability-competition": {"atom_ids": ["institutions-international-coordination-and-public-legitimacy.mechanism.003", "institutions-international-coordination-and-public-legitimacy.invariant.003"], "rationale": "Named remedy and enforcement paths own the institutional handoff while legal and competition conclusions remain bounded."},
    },
    "military-ai-autonomous-weapons-and-strategic-stability": {
        "use-case-decision-role": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.core"], "rationale": "The core strategic interaction contract owns bounded use-case and decision-role identity."},
        "mission-authority-effect": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.mechanism"], "rationale": "The mechanism atom owns the mission, authority, observation, posture, and strategic case."},
        "meaningful-human-judgment": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.boundary"], "rationale": "The boundary atom preserves human judgment, legal review, and adjacent technical authority."},
        "observation-trust": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.mechanism"], "rationale": "Observation trust is an explicit component of the existing strategic mechanism."},
        "safe-posture": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.failure_boundary"], "rationale": "The failure-boundary atom owns communication loss, degraded posture, and maximum inference."},
        "adversary-response-proliferation": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.mechanism", "military-ai-autonomous-weapons-and-strategic-stability.failure_boundary"], "rationale": "Strategic assumptions and bounded failure analysis own adversary response."},
        "strategic-stability-off-ramps": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.mechanism", "military-ai-autonomous-weapons-and-strategic-stability.argument_exit"], "rationale": "The strategic case and argument-exit atom own off-ramps and proof handoff."},
        "secrecy-review-decommission": {"atom_ids": ["military-ai-autonomous-weapons-and-strategic-stability.boundary", "military-ai-autonomous-weapons-and-strategic-stability.argument_exit"], "rationale": "Authority separation and the handoff ceiling own review, accountability, and closure."},
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

# These post-activation owners each have one intentionally composite core atom.
# Keep the explicit many-to-one mapping rather than inventing atom-count parity.
for _chapter_id in {
    "open-weight-release-and-post-release-control",
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
}:
    CONCEPT_ATOM_MAPPINGS[_chapter_id] = {
        _spec["concept_id"]: {
            "atom_ids": [f"{_chapter_id}.core"],
            "rationale": (
                "The existing post-activation chapter-core atom intentionally owns "
                f"the bounded {_spec['concept_id']} proposition and its evidence "
                "ceiling; splitting it solely for count parity would create duplicate "
                "claim identities."
            ),
        }
        for _spec in CONCEPT_SPECS[_chapter_id]
    }

# These Round-18 owners were admitted with one intentionally composite core atom.
for _chapter_id in {
    "perception-sensor-fusion-and-observation-trust",
    "embodied-agency-real-time-control-and-physical-safety",
    "inner-alignment-mesa-optimization-and-learned-objective-integrity",
    "human-ai-organizations-delegation-and-accountability",
}:
    CONCEPT_ATOM_MAPPINGS[_chapter_id] = {
        _spec["concept_id"]: {
            "atom_ids": [f"{_chapter_id}.core"],
            "rationale": (
                "The existing Round-18 chapter-core atom intentionally owns the "
                f"bounded {_spec['concept_id']} proposition with its scope, falsifier, "
                "promotion ceiling, and non-claims; splitting solely for count parity "
                "would duplicate rather than clarify the current claim identity."
            ),
        }
        for _spec in CONCEPT_SPECS[_chapter_id]
    }

_five_atom_routes = {
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty": {
        "coupled-trajectory-state": "mechanism",
        "three-arm-complementarity": "core",
        "bidirectional-adaptation": "mechanism",
        "skill-dependence-calibration": "failure_boundary",
        "neural-data-purpose-inference": "boundary",
        "intervention-consent-boundary": "boundary",
        "exit-and-human-recovery": "argument_exit",
        "equity-longitudinal-remedy": "failure_boundary",
    },
    "relational-dimension-compilation-and-polyadic-cognition": {
        "dimension-type-separation": "boundary",
        "typed-role-relational-ir": "mechanism",
        "residual-proposal-denominator": "mechanism",
        "lower-order-rescue": "boundary",
        "qualification-order-ladder": "core",
        "compilation-conformance": "mechanism",
        "adaptive-order-contraction": "failure_boundary",
        "rodie-joint-evaluation": "argument_exit",
    },
    "confidential-and-verifiable-ai-computation": {
        "guarantee-vector-adversary": "core",
        "construction-selection-composition": "boundary",
        "artifact-configuration-binding": "mechanism",
        "attestation-role-separation": "boundary",
        "freshness-revocation-replay": "mechanism",
        "circuit-semantics-correspondence": "mechanism",
        "leakage-side-channels-metadata": "failure_boundary",
        "cost-fallback-downgrade": "argument_exit",
    },
}
for _chapter_id, _routes in _five_atom_routes.items():
    CONCEPT_ATOM_MAPPINGS[_chapter_id] = {
        _concept_id: {
            "atom_ids": [f"{_chapter_id}.{_suffix}"],
            "rationale": (
                f"The existing {_suffix.replace('_', '-')} atom is the bounded owner "
                f"for {_concept_id}; the mapping preserves independent failure and "
                "promotion ceilings without manufacturing a duplicate atom."
            ),
        }
        for _concept_id, _suffix in _routes.items()
    }

# Round 22 replaces coarse many-to-one custody only where eight material
# concepts already have current digest-bound semantic reviews. This is a
# concept/falsifier denominator, not an atom-count denominator.
for _chapter_id in {
    "dangerous-capability-domains-and-misuse-uplift",
    "military-ai-autonomous-weapons-and-strategic-stability",
    "inner-alignment-mesa-optimization-and-learned-objective-integrity",
    "societal-resilience-and-misuse-defense",
    "confidential-and-verifiable-ai-computation",
    "open-weight-release-and-post-release-control",
    "perception-sensor-fusion-and-observation-trust",
    "human-ai-organizations-delegation-and-accountability",
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty",
    "embodied-agency-real-time-control-and-physical-safety",
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
    "relational-dimension-compilation-and-polyadic-cognition",
    "content-authenticity-watermarking-and-synthetic-media-integrity",
}:
    CONCEPT_ATOM_MAPPINGS[_chapter_id] = {
        _spec["concept_id"]: {
            "atom_ids": [
                f"{_chapter_id}.concept.{_spec['concept_id']}"
            ],
            "rationale": (
                "Round 22 assigns this already-reviewed material concept its own "
                "stable proposition, falsifier, evidence route, promotion ceiling, "
                "source boundary, and non-claims so it can fail or mature independently."
            ),
        }
        for _spec in CONCEPT_SPECS[_chapter_id]
    }

CONCEPT_ATOM_MAPPINGS["learning-theory-generalization-and-scaling-science"] = {
    "claim-contract-assumptions": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.core"],
        "rationale": "The chapter core already owns the dated, assumption-bound learning-claim contract and its inference ceiling.",
    },
    "conditional-generalization-bounds": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.mechanism.001", "learning-theory-generalization-and-scaling-science.invariant.001"],
        "rationale": "The population-and-algorithm mechanism plus exact-scope invariant own conditional generalization statements.",
    },
    "inductive-bias-identifiability": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.mechanism.002"],
        "rationale": "The multiple-lens mechanism owns explicit inductive-bias and alternative-explanation custody.",
    },
    "compression-information-lenses": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.mechanism.002", "learning-theory-generalization-and-scaling-science.failure_mode.011"],
        "rationale": "The explanatory-lens mechanism and compression-as-understanding failure preserve this bounded comparison.",
    },
    "interpolation-double-descent": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.failure_mode.008", "learning-theory-generalization-and-scaling-science.invariant.005"],
        "rationale": "The double-descent failure atom and prospective-forecast ceiling own non-monotone regime risk.",
    },
    "scaling-forecast-registry": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.mechanism.003", "learning-theory-generalization-and-scaling-science.invariant.005"],
        "rationale": "The scaling-fit mechanism and forecast-until-checked invariant own prospective registry discipline.",
    },
    "emergence-measurement": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.mechanism.004", "learning-theory-generalization-and-scaling-science.invariant.004"],
        "rationale": "The emergence-artifact mechanism and metric-retest invariant own competing transition explanations.",
    },
    "transfer-regime-change": {
        "atom_ids": ["learning-theory-generalization-and-scaling-science.mechanism.005", "learning-theory-generalization-and-scaling-science.invariant.002"],
        "rationale": "The transfer-challenge mechanism and claim-separation invariant own architecture and distribution regime changes.",
    },
}

REQUIRED_ELEMENTS = ["**Mechanism.**", "**Failure mode.**", "**Non-claim.**", "**Source grounding.**"]

# These receipts are intentionally static. Regeneration does not renew a review:
# any substantive chapter edit changes its digest and requires a new semantic
# disposition before the chapter can remain concept-complete.
SEMANTIC_REVIEWS: dict[str, dict[str, Any]] = {
    "dangerous-capability-domains-and-misuse-uplift": {
        "reviewed_sha256": "711807c566dbffff0b6ce61e705ddaad9bef70ac0d0c0eb46216ff67292e42c5",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "all eight named concepts explain a domain-specific mechanism and failure boundary",
            "source contributions and limits remain inside the chapter's declared queue",
            "the chapter states explicit non-claims and preserves adjacent-owner handoffs",
            "the staged dossier proof and scalar non-identifiability result remain bounded to authored finite records and a no-support handoff",
        ],
        "support_state_effect": "none",
    },
    "content-authenticity-watermarking-and-synthetic-media-integrity": {
        "reviewed_sha256": "6f0bed529f8776b24f33bc2d688d52b73652fd4aa288a8e9b17ab558885fb138",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "all eight named concepts distinguish provenance, watermark, fingerprint, detection, disclosure, and verification roles",
            "transformation lineage and Article 50 limits are explicit rather than inferred from keyword presence",
            "the chapter states failure modes, non-claims, and adjacent-owner handoffs without evidence promotion",
            "the authenticity-envelope lifecycle, exact repairs, transformation accounting, scope invalidation, non-identifiability results, and rejecting communication bridge remain bounded to authored finite records",
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
        "reviewed_sha256": "e30a84e62b284472c358e9fdded16d40a6f8cf08414bfc82ab353d1b8c5df33e",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts keep preference evidence, plural values, authorization, corrigibility, drift, proxy failure, conflict adjudication, and effect-visible objective retirement semantically separate",
            "the CIRL, goal-misgeneralization, learned-optimization, reward-hacking, and Alignment Field sources are used only within their formal, empirical, or authorial boundaries and do not become a solved-value or internal-objective claim",
            "the chapter includes capable wrong-goal controls, authority ceilings, dissent retention, ontology change, descendant invalidation, non-claims, and explicit handoffs while retaining argument support",
            "the objective-lease formalization is bounded to authored records, exact mutation routes, typed self-ratification refusal, scoped version invalidation, finite retirement, two non-identifiability results, and one learned-objective consumer bridge; it creates no value-correctness or behavioral-alignment support",
        ],
        "support_state_effect": "none",
    },
    "durable-semantic-memory-and-knowledge-lattices": {
        "reviewed_sha256": "004b2abacd5c926be8fc7a4a60398375f9fa3ed4c076e0b0866580787f26c6ff",
        "reviewed_date": "2026-07-31",
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
        "reviewed_sha256": "afaa2ec42f0cef8a907ef79808d0e391b9c967367d94fcb884cfcf36bb0e732b",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish component and chain capability, synthetic resources, descendant lineage, noninheritance, proliferation pathways, containment, recall, and evaluator competence",
            "RepliBench and Deterministic Capability Compilation remain bounded source comparators and authorial architecture rather than local replication, real-provider, containment, propensity, or shutdown evidence",
            "the chapter preserves hazard-minimizing synthetic authority, complete attempt and assistance denominators, positive controls, independently enforceable termination, residual descendants, and no operational proliferation recipe",
            "the formalization is restricted to authored dossier admissibility, exact mutation routes, lease noninheritance, finite descendant quarantine, bounded receipt invalidation, information-loss countermodels, and a rejecting operations bridge",
        ],
        "support_state_effect": "none",
    },
    "human-ai-communication-persuasion-and-epistemic-security": {
        "reviewed_sha256": "98779917c6ff94e0844420473b9e80571dbc08c202e51a5808f75bb7bccc578c",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish assistance, epistemic provenance, vulnerability, personalization, consent, cultural and linguistic scope, disclosure, and effect-visible correction",
            "the persuasion studies, commercial-influence preprint, multilingual and cultural evaluations, and Talos lineage stay within their exact populations, measures, review depths, and non-reproduced source boundaries",
            "the formalization is restricted to trusted authored fields, exposure arithmetic, typed projection noninterference, and information-loss countermodels; it authorizes no delivery and reports no human outcome",
            "the chapter jointly preserves helpfulness, comprehension, autonomy, persuasion, privacy, delayed outcomes, correction reach, practical appeal, unsupported language cells, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "adversarial-machine-learning-and-model-attack-surface": {
        "reviewed_sha256": "5327345ae90479f457faede91c29518edb99f219956e1c45c917bff4e782ad86",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish threat identity, adaptive evaluation, reachable evasion, poisoning repair, confidentiality attacks, composed attack paths, non-substitutable defenses, and safe disclosure",
            "NIST, Sleeper Agents, GPT-2 extraction, camera-LiDAR attack, and Reluplex remain inside their taxonomy, constructed, model-family, modality, and property-specific boundaries",
            "the formalization is restricted to authored dossier admissibility, exact repair routes, typed assurance separation, finite trace quarantine, bounded disposition invalidation, information-loss countermodels, and a no-release consumer bridge",
            "the chapter preserves attacker competence, positive controls, clean utility, false-negative ceilings, safe authority, residual ownership, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "open-weight-release-and-post-release-control": {
        "reviewed_sha256": "ce241d33e2547997fcc7c020011dbcc1c16437f5bfd632490c79da161a373097",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish access options, artifact and derivative identity, competent malicious adaptation, accessible-frontier expiry, marginal and cumulative risk, benefit distribution, controls after copying, and irreversible incident residuals",
            "provider, policy, security, consensus, and international-report sources remain scoped comparators and do not become a categorical release decision or independent local evaluation",
            "the formalization is restricted to trusted authored fields, exact repairs, arithmetic monotonicity, and information-loss countermodels; it authorizes no release and reports no ecosystem behavior",
            "the chapter preserves fair rescue, exact artifact custody, ecosystem uncertainty, non-adoption, derivative exposure, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "physical-compute-infrastructure-energy-and-environmental-constraints": {
        "reviewed_sha256": "93c3e0e439438480a1fc5dc0385064fd754cb29658d09a28c350116fddcbf068",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish useful compute, bottleneck topology, temporal grid effects, local cooling and community constraints, embodied lifecycle, degradation, metering and rebound, and hardware-control concentration",
            "IEA, LBNL, hardware-guarantee, and OECD sources remain scenario, national-method, design-proposal, and market-specific evidence rather than local facility measurement or legal adjudication",
            "the chapter preserves denominators, time and location, uncertainty, distribution, correlated failure, total versus marginal effects, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "institutions-international-coordination-and-public-legitimacy": {
        "reviewed_sha256": "096dcf01a032690b74a86e9a4fc08699860d70d5e91705e3483457a62a84c7d4",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts keep mandate, affected publics, scientific and legal crosswalks, verification access, cross-border enforcement, capacity, capture and emergency expiry, and remedy or competition distinct",
            "UN, Council of Europe, EU, legal-alignment, hardware, OECD, and ICRC sources remain institution-, jurisdiction-, mandate-, and time-scoped comparators rather than compliance or legitimacy proof",
            "the chapter preserves excluded populations, conflicting jurisdiction, assessor dependence, withdrawal, financing, appeal, irreversible harm, and argument-only support",
            "the formalization is restricted to authored dossier admissibility, exact mutation routes, jurisdiction scope, finite affected-public inclusion, receipt invalidation, information-loss countermodels, and a rejecting Governance Rights bridge",
        ],
        "support_state_effect": "none",
    },
    "multi-agent-dynamics-collective-intelligence-and-systemic-risk": {
        "reviewed_sha256": "1e629163dfd8c74d8331c1550b747eb1509ad6eeb3c4e9449c11d07ba624e3ee",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish population identity, multiplex dependency, cooperation and collusion, strategic incentives, decision-theory disagreement, nonstationary learning, systemic cascades, and human influence",
            "multi-agent risk, cooperative AI, gradual disempowerment, constructive interdependence, and functional decision-theory sources remain taxonomic, agenda, conceptual, study-specific, or normative rather than predictions or universal solutions",
            "the chapter preserves effective diversity, affected nonparticipants, externalities, alternative theories, false-negative defenses, intervention displacement, and argument-only support",
            "the finite pairwise-evidence impossibility model and nine systemic mutations establish only authored campaign-admission discipline; population outcomes, effective human agency, and support remain Theseus or empirical obligations",
        ],
        "support_state_effect": "none",
    },
    "military-ai-autonomous-weapons-and-strategic-stability": {
        "reviewed_sha256": "cb73c0e8487c237626cff1adb9be1dcb7cab671497649b4dfe965c8d1791eaa3",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish decision role, mission authority, meaningful judgment, observation trust, safe posture, reciprocal adaptation, strategic off-ramps, and accountable decommissioning",
            "ICRC and SIPRI remain mandate-specific official-position and scenario-analysis sources; the international reports add context without becoming legal advice, prediction, or technical validation",
            "the chapter preserves compressed timelines, base-rate failures, adversary response, secrecy limits, independent challenge, decommissioning residuals, and argument-only support",
            "the 24-declaration finite lifecycle, 45 mutation dispositions, three monotonicity controls, and two non-identifiability results establish only authored public-safe review discipline; operational, legal, human, strategic, safety, support, and release conclusions remain unproved",
        ],
        "support_state_effect": "none",
    },
    "perception-sensor-fusion-and-observation-trust": {
        "reviewed_sha256": "1a9b261b86109d0ba82fac5c8ec6a737f1df80a91c19bf27b2bd0ef037cc924f",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts preserve task-relative observation need, exact sensor identity, time and pose, channel hypotheses, dependence, corruption, active sensing, and expiring observation authority as separate lifecycle obligations",
            "multimodal, ImageBind, corruption, sensor-fusion, robotics, and Platonic World Model sources remain survey, reported comparator, benchmark, attack-study, capability, or authorial lineage rather than local observation-trust evidence",
            "the chapter retains missingness, common-mode error, positive controls, active-sensing risk, safe hold, reconciliation, adjacent-owner authority, and argument-only support",
            "the new Lean pair classifier and lifecycle are limited to authored dependence roots, finite evidence counts, exact record custody, rejecting controls, and descendant invalidation; they do not establish real dependence, calibration, environmental truth, robustness, physical safety, support, or authority",
        ],
        "support_state_effect": "none",
    },
    "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty": {
        "reviewed_sha256": "73aa3426379c6f0057eebf4efd8ecf890505eb63fe54694fcbe2b73c9cc929fa",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish coupled trajectories, strongest-component complementarity, bidirectional adaptation, skill and dependence, neural inference, intervention authority, practical exit, and longitudinal equity or remedy",
            "the team meta-analysis, feedback-loop study, OECD convergence work, and WHO landscape retain task, population, study-duration, policy, clinical, and modality ceilings and do not become beneficial-symbiosis or neural-intervention evidence",
            "the chapter preserves consent renewal, three-arm baselines, unaided recovery, attrition, inferred-data rights, clinical boundaries, irreversible residuals, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "relational-dimension-compilation-and-polyadic-cognition": {
        "reviewed_sha256": "ba9f55a9e55a40b12a59788519e119716d7053f95a6076e3768cc32c01ed6649",
        "reviewed_date": "2026-07-31",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts keep dimensional typing, role-sensitive IR, residual proposal, complete denominators, lower-order rescue, qualification, compilation, contraction, and vector evaluation semantically distinct",
            "the Corben-authored compiler remains an unimplemented architecture and message passing remains a bounded molecular graph comparator rather than proof of higher-order necessity, irreducibility, natural-task value, or efficient compilation",
            "the chapter preserves role identity, proposal recall uncertainty, matched rescue budgets, unseen topology, conformance limits, descendant invalidation, hardware cost, and argument-only support",
        ],
        "support_state_effect": "none",
    },
    "learning-theory-generalization-and-scaling-science": {
        "reviewed_sha256": "10e43f2a5ab74407596136bc3ff6e55a2f4bb95ee9eb78229bf136db479ea4d3",
        "reviewed_date": "2026-07-28",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts separate claim assumptions, conditional bounds, inductive bias, compression and information lenses, interpolation, scaling forecasts, emergence measurement, and transfer under regime change",
            "PAC, MDL, information bottleneck, scaling-law, double-descent, emergence, weak-to-strong, and no-free-lunch sources remain conditional, theoretical, empirical, model-family, task, or explanatory comparators rather than a universal learning theory",
            "the chapter preserves failed runs, quantifiers, alternative explanations, prospective forecasts, uncertainty, metric artifacts, architecture and optimizer expiry, and no transfer or safety promotion",
        ],
        "support_state_effect": "none",
    },
    "confidential-and-verifiable-ai-computation": {
        "reviewed_sha256": "9d3953fe336005493726584f76af4ecc50effdaf7068d5160f74cb1564d7d657",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts separate guarantee vectors, construction choice, artifact binding, attestation roles, freshness, semantic correspondence, leakage, and cost-visible downgrade",
            "NIST privacy-enhancing cryptography, zkLLM, and RFC 9334 remain program context, a configuration-bound prototype, and informational architecture rather than local security, performance, root, verifier-independence, or authorization evidence",
            "the chapter preserves adversary and leakage models, circuit-to-semantics gaps, replay, composition, side channels, matched native baselines, explicit fallback, and argument-only support",
            "the formalization is restricted to authored dossier admissibility, typed evidence non-substitution, finite leakage accounting, receipt and fallback invalidation, information-loss countermodels, and a privacy-owner rejection; it establishes no cryptographic, hardware, privacy, authorization, or deployment result",
        ],
        "support_state_effect": "none",
    },
    "embodied-agency-real-time-control-and-physical-safety": {
        "reviewed_sha256": "04d3faefcf3592e6cf131139e7a8bdeb078c893377db66663d47758bb0b55418",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish plant and hazard identity, observation-to-control separation, timing and reachability, advanced and fallback control, barriers and interlocks, learning authority, twin fidelity, and incident recommissioning",
            "robotics capability, physical-risk survey, barrier, Simplex, safe-RL, digital-twin, and VIEA sources remain reported, survey, formal-framework, architectural, or authorial comparators rather than a local physical-safety result",
            "the chapter preserves latency, shared-defect, infeasibility, exploration, simulator exploitation, independent stop, incident evidence, latent damage, safe-hold, and no consequential-plant claim",
            "the added finite control-lease model proves only authored admission semantics, 13 exact mutation routes, and three arithmetic monotonicity laws; Project Theseus closed-loop behavior, plant truth, physical safety, and support movement remain outside the formal result",
        ],
        "support_state_effect": "none",
    },
    "inner-alignment-mesa-optimization-and-learned-objective-integrity": {
        "reviewed_sha256": "af7d3d13dcfc3fe0887413dfd287e1b381d520e30b0c065eb2731e97bbea947e",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts preserve outer target, actual signal, policy, compatible objective hypotheses, internal optimization, capable goal shift, evaluation awareness, evidence independence, mitigation hiding, opportunity, expiry, and descendants without collapsing behavior into objective identity",
            "learned-optimization, goal-misgeneralization, Sleeper Agents, reward-hacking misalignment, power-seeking, and Alignment Field sources retain conceptual, construction, environment, model, formal-assumption, and authorial-lineage ceilings rather than becoming a local inner-alignment result",
            "the chapter preserves competence and opportunity controls, sealed separating interventions, alternative explanations, removal-versus-concealment denominators, full-state rollback residuals, descendant invalidation, and argument-only support",
            "the added Lean counterexample and eight-stage lifecycle prove only finite non-identification and authored record discipline; the independent 59-mutation consumer and formal nonclaims preserve objective-discovery, deception-detection, mitigation, evaluator-quality, deployment, alignment, and safety boundaries",
        ],
        "support_state_effect": "none",
    },
    "human-ai-organizations-delegation-and-accountability": {
        "reviewed_sha256": "b33d68ac2929bd25e425df9815b0298199128f14ac70412a736d9388cd71d2ce",
        "reviewed_date": "2026-08-01",
        "reviewer_role": "codex_editorial_semantic_review",
        "disposition": SEMANTIC_REVIEW_DISPOSITION,
        "review_basis": [
            "the eight concepts distinguish charter and standing, operational role capacity, decision rights, bounded delegation, duty separation, incentives, longitudinal contribution and dependence, accountability and remedy, and succession or dissolution",
            "NIST, moral-crumple-zone analysis, authority-allocation theory, workplace evidence, constructive interdependence, teaming synthesis, feedback-loop experiments, EU liability analysis, and Talos remain framework, conceptual, model, setting, metric, population, jurisdiction, or authorial comparators rather than proof of one superior or legitimate organization",
            "the chapter preserves affected nonusers, practical intervention, workload and accessibility, strongest-component baselines, attrition, evidence access, legal non-claims, unowned-residual closure blocks, and argument-only support",
            "the added five-stage Lean review and twenty-field mutation consumer establish only finite authored-record reachability and refusal; explicit prose preserves field-truth, real human-control, lawful-accountability, organizational-outcome, support, and external-effect nonclaims",
        ],
        "support_state_effect": "none",
    },
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return canonical_chapter_sha256(path)


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
        text = canonical_chapter_text(path)
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
        "word_count_method": "Unicode text split on whitespace over canonical chapter source with the generated visual projection removed; diagnostic trigger only",
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
