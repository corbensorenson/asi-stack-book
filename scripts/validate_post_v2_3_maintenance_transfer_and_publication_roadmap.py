#!/usr/bin/env python3
"""Validate the active evidence-competence, transfer, and publication roadmap."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
SCHEMA = ROOT / "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json"
COMPETENCE = ROOT / "docs/claim_bearing_experiment_competence_standard.md"
PREDECESSOR_STATUS = ROOT / "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
TERMINAL = ROOT / "release_records/2026-07-16-post-v2-3-claim-proof-sota-roadmap-complete-no-public-release.json"
X_MANIFEST = ROOT / "editions/x_article/manifest.json"
X_RELEASE = ROOT / "release_records/2026-07-16-x-article-synopsis-ready-not-published.json"
ATOM_REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
ATOM_ADDENDUM = ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json"
POST_ACTIVATION_SIX_CHAPTER_ADDENDUM = (
    ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json"
)
P7_1A_W3_INHERITANCE_GUARD = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"
PROOF_REVIEW = ROOT / "docs/proof_adequacy_review.md"
PROOF_MANIFEST = ROOT / "proofs/proof_manifest.json"
IDENTITY_GRAPH = ROOT / "evidence_quality/claim_identity_graph.json"
NEGATIVE_REHABILITATION = ROOT / "evidence_quality/negative_result_rehabilitation.json"
NEGATIVE_SURFACE_AUDIT = ROOT / "evidence_quality/negative_inference_surface_audit.json"
P2_SELECTION = ROOT / "evidence_quality/p2_frontier_selection.json"
P2_CORPUS = ROOT / "evidence_quality/p2_development_corpus_preflight.json"
P2_GOLD = ROOT / "evidence_quality/p2_gold_preflight_diagnosis.json"
P2_POLICY = ROOT / "evidence_quality/p2_task_qualification_and_replacement_policy.json"
P2_RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
P2_REPLACEMENT_QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
P5_STATEFUL_RESULT = ROOT / "experiments/effect_complete_service/results/2026-07-27-local.json"
P5_NATURAL_TRACE = ROOT / "experiments/p5_natural_publication_service_trace/results/2026-07-27-development.json"
P5_NATURAL_CAMPAIGN = ROOT / "experiments/governed_operations_argument_exit/preregistration.json"
P5_NATURAL_QUALIFICATION = ROOT / "experiments/governed_operations_argument_exit/qualification/2026-07-28-local.json"
READER_MANIFEST = ROOT / "editions/reader_manuscript/reader_2026_07_18/manifest.json"
READER_RELEASE_RECORD = ROOT / "release_records/2026-07-18-reader-2026-07-18-0921a924.json"
STRUCTURAL_RESEARCH = ROOT / "docs/structural_completeness_chapter_research_2026_07_19.md"
STRUCTURAL_GAP_AUDIT = ROOT / "docs/structural_completeness_gap_audit_2026_07_19.md"
OPTIMIZER_RESEARCH = ROOT / "docs/optimizer_landscape_chapter_research_2026_07_21.md"
POST_ROUND_18_DEPTH_REVIEW = ROOT / "docs/post_round_18_depth_and_coverage_review_reconciliation_2026_07_24.md"
ROUND_20_DEPTH_RECONCILIATION = ROOT / "docs/round_20_depth_and_substance_reconciliation_2026_07_27.md"
ROUND_21_DEPTH_ADJUDICATION = ROOT / "docs/round_21_depth_contract_and_atom_adequacy_adjudication_2026_07_28.md"
ROUND_20_CHAPTER_SUBSTANCE = ROOT / "evidence_quality/chapter_substance_contract.json"
ROUND_20_FOUR_CHAPTER_ATOMS = ROOT / "evidence_quality/round20_four_chapter_claim_atom_addendum.json"
P6_9_RAW_SCAFFOLD_AUDIT = ROOT / "evidence_quality/p6_9_raw_scaffold_ownership_audit.json"
P6_9_PROOF_EVIDENCE_HANDOFF = ROOT / "evidence_quality/p6_9_proof_evidence_handoff.json"
PRECISION_CONTRACT_RECONCILIATION = ROOT / "docs/precision_contract_source_reconciliation_2026_07_24.md"
PRECISION_CONTRACT_SOURCE_NOTE = ROOT / "sources/source_notes/precision_contract.md"
PRECISION_CONTRACT_BACKLOG = ROOT / "research_backlog_records/precision_contract_2026_07_24.json"
PRECISION_CONTRACT_TRIAGE = ROOT / "new_paper_triage_scenarios/precision_contract_2026_07_24.json"
SOURCE_INVENTORY = ROOT / "sources/source_inventory.json"
BOOK_MANIFEST = ROOT / "book_structure.json"
VISUAL_EDITION_MANIFEST = ROOT / "visual_edition/manifest.json"
MANIM_V2_LEDGER = ROOT / "visual_edition/manim_v2_production_ledger.json"
REVIEW_ADJUDICATION = ROOT / "docs/chatgpt_pro_full_book_review_adjudication_2026_07_25.md"
CURRENT_ROLE_MAP = ROOT / "evidence_quality/current_chapter_role_map.json"
PROOF_SEMANTIC_DEPTH_OVERLAY = ROOT / "proofs/proof_semantic_depth_overlay.json"
PROOF_SEMANTIC_RATIONALIZATION_LEDGER = (
    ROOT / "proofs/proof_semantic_rationalization_ledger.json"
)
STRUCTURAL_CHAPTER_PATHS = {
    "white-box-evidence-interpretability-and-activation-governance": ROOT / "chapters/white-box-evidence-interpretability-and-activation-governance.qmd",
    "governed-world-models-and-reality-grounding": ROOT / "chapters/governed-world-models-and-reality-grounding.qmd",
    "human-factors-and-meaningful-control-in-oversight": ROOT / "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
    "governed-operations-incident-command-and-graceful-degradation": ROOT / "chapters/governed-operations-incident-command-and-graceful-degradation.qmd",
}
MANUSCRIPT_COMPLETION_PATHS = {
    "inner_alignment_depth": ROOT / "chapters/inner-alignment-mesa-optimization-and-learned-objective-integrity.qmd",
    "multi_agent_depth": ROOT / "chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd",
    "perception_depth": ROOT / "chapters/perception-sensor-fusion-and-observation-trust.qmd",
    "embodied_depth": ROOT / "chapters/embodied-agency-real-time-control-and-physical-safety.qmd",
    "organization_depth": ROOT / "chapters/human-ai-organizations-delegation-and-accountability.qmd",
    "white_box_depth": ROOT / "chapters/white-box-evidence-interpretability-and-activation-governance.qmd",
    "uncertainty_repair": ROOT / "chapters/governed-world-models-and-reality-grounding.qmd",
    "types_and_transformation_repair": ROOT / "chapters/executable-specifications-and-lean-proof-envelope.qmd",
    "synthetic_data_repair": ROOT / "chapters/data-engines-continual-learning-and-unlearning.qmd",
    "explanation_repair": ROOT / "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
    "precision_primary": ROOT / "chapters/rankfold-neuralfold-and-artifact-compression.qmd",
    "precision_residual": ROOT / "chapters/compact-generative-systems-and-residual-honesty.qmd",
    "precision_runtime": ROOT / "chapters/fast-generation-architectures.qmd",
    "precision_economics": ROOT / "chapters/resource-economics-and-token-budgets.qmd",
    "precision_readiness": ROOT / "chapters/readiness-gates-residual-escrow-and-quarantine.qmd",
    "precision_custody": ROOT / "chapters/model-weight-custody-and-hardware-roots-of-trust.qmd",
    "precision_efficiency": ROOT / "chapters/the-efficient-asi-hypothesis.qmd",
    "precision_synthesis": ROOT / "chapters/integrated-reference-architecture.qmd",
}
STRUCTURAL_SOURCE_IDS = [
    "ext_circuit_tracing_2025",
    "ext_scaling_sparse_autoencoders_2024",
    "ext_world_models_2018",
    "ext_dreamer_v3_2025",
    "ext_meaningful_human_control_actionable_2022",
    "ext_agentic_oversight_practice_2026",
    "ext_nist_deployed_ai_monitoring_2026",
    "ext_nist_incident_response_2025",
]
STRUCTURAL_GAP_SOURCE_IDS = [
    "ext_llama3_herd_2024",
    "ext_megatron_distributed_training_2021",
    "ext_zero_optimizer_2019",
    "ext_gspmd_2021",
    "ext_datastates_llm_2024",
    "ext_pytorch_distributed_checkpoint_2026",
    "ext_mlperf_training_v6_2026",
    "ext_3d_detection_corruptions_2023",
    "ext_foundation_robotics_physical_risk_2025",
    "ext_nist_differential_privacy_2025",
    "ext_moral_crumple_zones_2019",
    "ext_multi_agent_risks_2025",
    "ext_replibench_2025",
    "ext_autonomous_lab_materials_2023",
    "ext_conversational_persuasion_gpt4_2025",
    "ext_anthropic_model_persuasiveness_2024",
    "ext_commercial_persuasion_ai_2026",
    "ext_un_global_digital_compact_2024",
    "ext_council_europe_ai_convention_2024",
    "ext_generative_ai_at_work_2025",
    "ext_ilo_genai_jobs_index_2025",
    "ext_iea_energy_and_ai_2025",
    "ext_lbnl_data_center_energy_2024",
    "ext_cooperative_inverse_rl_2016",
    "ext_goal_misgeneralization_2022",
    "ext_learned_optimization_risks_2019",
    "ext_emergent_misalignment_reward_hacking_2025",
]
PUBLIC_SURFACES = [
    ROOT / p
    for p in ["README.md", "index.qmd", "docs/publication_readiness.md", "docs/public_status_contract.md"]
]
ACTIVE_MARKER = "Status: **active canonical successor**"
EXPECTED_CONCEPT_ANCHORS = [
    ("C1", "C1-noninheritance-law", "chapters/asi-is-a-stack-not-a-model.qmd", "Together these separations form the book's **noninheritance law**"),
    ("C1", "C1-three-projections", "chapters/asi-is-a-stack-not-a-model.qmd", "The thesis has three projections, each with a different job"),
    ("C1", "C1-theorem-runtime-boundary", "chapters/asi-is-a-stack-not-a-model.qmd", "A theorem is not runtime enforcement"),
    ("C1", "C1-proposal-ratification-boundary", "chapters/asi-is-a-stack-not-a-model.qmd", "A proposal is not ratification"),
    ("C2", "C2-twenty-two-unit-spine", "products/narrative_product_spine.json", "A twenty-two-unit thesis-to-method route through the canonical manifest"),
    ("C2", "C2-all-eighty-four-crosswalk", "products/narrative_unit_crosswalk.json", '"canonical_chapter_count": 84'),
    ("C2", "C2-nonabsorption-prose", "chapters/living-book-methodology.qmd", "Narrative compression without claim absorption"),
    ("C3", "C3-calculus-owner", "chapters/executable-specifications-and-lean-proof-envelope.qmd", "Governed Transition Calculus"),
    ("C3", "C3-authority-projection", "chapters/system-boundaries-and-authority.qmd", "authority-specific projection of the shared Governed Transition Calculus"),
    ("C3", "C3-joined-reference-trace", "chapters/integrated-reference-architecture.qmd", "every material handoff can be projected through the Governed Transition Calculus"),
    ("C3", "C3-protocol-projection", "appendices/D_protocol_schemas.qmd", "Governed Transition Calculus projection"),
    ("C4", "C4-developmental-loop-owner", "chapters/governed-model-training-distributed-optimization-and-scaling.qmd", "The Developmental Intelligence Loop"),
    ("C4", "C4-developmental-stage-chain", "chapters/governed-model-training-distributed-optimization-and-scaling.qmd", "curriculum construction -> world interaction -> prediction error"),
    ("C4", "C4-readiness-review-owner", "chapters/readiness-gates-residual-escrow-and-quarantine.qmd", "Within the Developmental Intelligence Loop, this chapter owns the readiness review"),
    ("C4", "C4-joined-reference-trace", "chapters/integrated-reference-architecture.qmd", "learned capability enters through the Developmental Intelligence Loop"),
    ("C5", "C5-trusted-kernel-owner", "chapters/security-kernel-and-digital-scifs.qmd", "Minimum trusted kernel"),
    ("C5", "C5-bounded-liveness-owner", "chapters/security-kernel-and-digital-scifs.qmd", "Bounded liveness"),
    ("C5", "C5-effect-boundary-projection", "chapters/runtime-adapters-tool-permissions-and-human-approval.qmd", "effect-boundary projection of the minimum trusted kernel and bounded liveness"),
    ("C5", "C5-economic-projection", "chapters/resource-economics-and-token-budgets.qmd", "Resource Economics owns the accounting projection of bounded liveness"),
    ("C6", "C6-semantic-depth-owner", "chapters/executable-specifications-and-lean-proof-envelope.qmd", "P0--P6 semantic-depth overlay"),
    ("C6", "C6-target-obligation-fields", "chapters/executable-specifications-and-lean-proof-envelope.qmd", "Each target eventually needs its assumptions, consumer, witness or explicit unreachability"),
    ("C7", "C7-flagship-owner", "chapters/project-theseus-as-report-first-implementation-reference.qmd", "ASI-THESEUS-FLAGSHIP-01"),
    ("C7", "C7-five-matched-routes", "chapters/project-theseus-as-report-first-implementation-reference.qmd", "Five routes answer different alternatives on the same eligible task set"),
    ("C7", "C7-one-way-preregistration-handoff", "chapters/prototype-roadmap.qmd", "The handoff is one-way until the protected campaign is opened"),
    ("C8", "C8-evidence-led-program", "chapters/living-book-methodology.qmd", "Evidence-led derivative program"),
    ("C8", "C8-contribution-owned-outlines", "chapters/open-research-agenda-and-bibliography-plan.qmd", "Contribution-owned derivative outlines"),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def transition_snapshot(atom_ids: set[str]) -> dict:
    paths = sorted((ROOT / "evidence_transitions").glob("**/*.json"))
    accepted: list[dict] = []
    for path in paths:
        item = load(path)
        if item.get("review_status") == "accepted" and item.get("transition_validity_state") == "review_accepted":
            accepted.append(item)
    states = Counter(item.get("new_support_state") for item in accepted)
    effects = Counter(item.get("transition_effect") for item in accepted)
    direct = sum(item.get("claim_id") in atom_ids for item in accepted)
    return {
        "file_count": len(paths),
        "accepted_count": len(accepted),
        "direct_count": direct,
        "indirect_count": len(accepted) - direct,
        "states": states,
        "effects": effects,
    }


def inputs() -> dict:
    atom_registry = load(ATOM_REGISTRY)
    atom_addendum = load(ATOM_ADDENDUM)
    post_activation_six_chapter_addendum = load(POST_ACTIVATION_SIX_CHAPTER_ADDENDUM)
    atom_ids = {row["atom_id"] for row in atom_registry["atoms"]}
    atom_ids.update(row["id"] for row in atom_addendum["atoms"])
    atom_ids.update(row["id"] for row in post_activation_six_chapter_addendum["atoms"])
    porcelain = git_output("status", "--porcelain=v1")
    return {
        "status": load(STATUS),
        "schema": load(SCHEMA),
        "roadmap": ROADMAP.read_text(encoding="utf-8"),
        "competence": COMPETENCE.read_text(encoding="utf-8"),
        "predecessor": load(PREDECESSOR_STATUS),
        "terminal": load(TERMINAL),
        "x_manifest": load(X_MANIFEST),
        "x_release": load(X_RELEASE),
        "atom_registry": atom_registry,
        "atom_addendum": atom_addendum,
        "post_activation_six_chapter_addendum": post_activation_six_chapter_addendum,
        "p7_1a_w3_inheritance_guard": load(P7_1A_W3_INHERITANCE_GUARD),
        "identity_graph": load(IDENTITY_GRAPH),
        "negative_rehabilitation": load(NEGATIVE_REHABILITATION),
        "negative_surface_audit": load(NEGATIVE_SURFACE_AUDIT),
        "p2_selection": load(P2_SELECTION),
        "p2_corpus": load(P2_CORPUS),
        "p2_gold": load(P2_GOLD),
        "p2_policy": load(P2_POLICY),
        "p2_resource": load(P2_RESOURCE),
        "p2_replacement_queue": load(P2_REPLACEMENT_QUEUE),
        "p5_stateful_result": load(P5_STATEFUL_RESULT),
        "p5_natural_trace": load(P5_NATURAL_TRACE),
        "p5_natural_campaign": load(P5_NATURAL_CAMPAIGN),
        "p5_natural_qualification": load(P5_NATURAL_QUALIFICATION),
        "reader_manifest": load(READER_MANIFEST),
        "reader_release_record": load(READER_RELEASE_RECORD),
        "structural_research": STRUCTURAL_RESEARCH.read_text(encoding="utf-8"),
        "structural_gap_audit": STRUCTURAL_GAP_AUDIT.read_text(encoding="utf-8"),
        "optimizer_research": OPTIMIZER_RESEARCH.read_text(encoding="utf-8"),
        "post_round_18_depth_review": POST_ROUND_18_DEPTH_REVIEW.read_text(encoding="utf-8"),
        "round_20_depth_reconciliation": ROUND_20_DEPTH_RECONCILIATION.read_text(encoding="utf-8"),
        "round_21_depth_adjudication": ROUND_21_DEPTH_ADJUDICATION.read_text(encoding="utf-8"),
        "round_20_chapter_substance": load(ROUND_20_CHAPTER_SUBSTANCE),
        "round_20_four_chapter_atoms": load(ROUND_20_FOUR_CHAPTER_ATOMS),
        "p6_9_raw_scaffold_audit": load(P6_9_RAW_SCAFFOLD_AUDIT),
        "p6_9_proof_evidence_handoff": load(P6_9_PROOF_EVIDENCE_HANDOFF),
        "precision_contract_reconciliation": PRECISION_CONTRACT_RECONCILIATION.read_text(encoding="utf-8"),
        "precision_contract_source_note": PRECISION_CONTRACT_SOURCE_NOTE.read_text(encoding="utf-8"),
        "precision_contract_backlog": load(PRECISION_CONTRACT_BACKLOG),
        "precision_contract_triage": load(PRECISION_CONTRACT_TRIAGE),
        "source_inventory": load(SOURCE_INVENTORY),
        "book_manifest": load(BOOK_MANIFEST),
        "visual_edition_manifest": load(VISUAL_EDITION_MANIFEST),
        "manim_v2_ledger": load(MANIM_V2_LEDGER),
        "review_adjudication": REVIEW_ADJUDICATION.read_text(encoding="utf-8"),
        "current_role_map": load(CURRENT_ROLE_MAP),
        "proof_semantic_depth_overlay": load(PROOF_SEMANTIC_DEPTH_OVERLAY),
        "proof_semantic_rationalization_ledger": load(
            PROOF_SEMANTIC_RATIONALIZATION_LEDGER
        ),
        "manuscript_completion": {
            key: path.read_text(encoding="utf-8")
            for key, path in MANUSCRIPT_COMPLETION_PATHS.items()
        },
        "transition_snapshot": transition_snapshot(atom_ids),
        "proof_review": PROOF_REVIEW.read_text(encoding="utf-8"),
        "proof_manifest": load(PROOF_MANIFEST),
        "git": {
            "branch": git_output("branch", "--show-current"),
            "head": git_output("rev-parse", "HEAD"),
            "dirty_count": 0 if not porcelain else len(porcelain.splitlines()),
        },
        "public": {
            p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
            for p in PUBLIC_SURFACES
        },
    }


def errors(data: dict) -> list[str]:
    out: list[str] = []
    status = data["status"]
    for err in sorted(
        Draft202012Validator(data["schema"]).iter_errors(status),
        key=lambda e: list(e.path),
    ):
        out.append(f"schema:{'.'.join(map(str, err.path))}: {err.message}")
    no_deferral = status.get("no_deferral_manuscript_admission", {})
    no_deferral_ids = set(no_deferral.get("admitted_chapter_ids", []))
    if (
        no_deferral.get("state") != "terminal_argument_level_admission"
        or no_deferral.get("previous_manifest_chapter_count") != 66
        or no_deferral.get("current_manifest_chapter_count") != 80
        or len(no_deferral_ids) != 14
        or no_deferral.get("remaining_live_candidate_queue_count") != 0
        or no_deferral.get("structural_freeze_for_manuscript_ideas") is not False
        or no_deferral.get("all_chapter_core_support_states") != "argument"
        or no_deferral.get("current_semantically_reviewed_chapter_count") != 68
        or no_deferral.get("current_structured_atom_count") != 4059
    ):
        out.append("no-deferral manuscript admission state drifted")

    roadmap = data["roadmap"]
    required_sections = [
        "## Purpose",
        "### Taxonomy and structural-maturity reconciliation",
        "## Strategic quality diagnosis",
        "## Execution-ready work board",
        "## Shared ASI Stack–Theseus flagship",
        "## Review adjudication and corrected baseline",
        "## Round 16 evidence-first adjudication and amendment",
        "## Round 17 priority enforcement and blocker recheck",
        "## Post-Round-18 depth and coverage amendment",
        "## Operating rules",
        "## P0 — Public truth, claim identity, and attestation continuity",
        "## P1 — Negative-result rehabilitation and false-negative defense",
        "## P2 — Competence-qualified natural empirical frontier",
        "### P2-R3a exact capacity and Docker receipt — 2026-07-28",
        "## P3 — Independent reproduction, transfer, and SOTA challenge",
        "## P4 — Semantically meaningful formal evidence",
        "## P5 — Effect-complete governed reference system",
        "### P5 stateful-service vertical-slice checkpoint — 2026-07-27",
        "### P5 natural publication-service development checkpoint — 2026-07-27",
        "### P5 prospective natural stateful-service campaign freeze — 2026-07-28",
        "### P5 natural stateful-service implementation qualification — 2026-07-28",
        "## P6 — Evidence, instrument, and source renewal",
        "### P6.4-R18 — terminal bounded conceptual-completeness packet",
        "### P6.5 — Round 16 post-activation integration debt",
        "### P6.8 — Functional precision and behavior-preserving computation",
        "### P6.9 — Round 20 chapter substance and concept fidelity",
        "## P7 — Reader remediation and owner-authorized publication",
        "### P7.3 — Governed Manim visual edition",
        "## P8 — Closure, residual ownership, and successor continuity",
        "## Execution order and decision rules",
        "## Current owned queue",
        "## Checkpoint receipt",
        "## Milestones",
        "## Definition of done",
    ]
    for section in required_sections:
        if roadmap.count(section) != 1:
            out.append(f"roadmap section missing or duplicated: {section}")
    roadmap_normalized = re.sub(r"\s+", " ", roadmap).casefold()
    for phrase in [
        "No false-negative laundering",
        "A fair chance to succeed comes before a right to refute",
        "claim-commensurate competence",
        "Final held-out data is opened once",
        "Main-only repository continuity",
        "Manim Community Edition",
        "five-pilot ratchet",
        "YouTube is the canonical host",
        "84/84 `ready_not_published`",
        "A video may explain",
        "It may not strengthen",
        "subclaim_of",
        "proxy_for",
        "N0 instrument failure",
        "N5 broad refutation",
        "KERC",
        "natural, non-authored corpus",
        "independently implemented evaluator",
        "fair rescue ladder",
        "positive-control-failing",
        "native_decide",
        "DataEngineLifecycleRefinement",
        "reader-2026-07-18",
        "public assets were redownloaded",
        "Microsoft-Word-quality claim",
        "draft `2077875347220041728`",
        "publish only with explicit action-time authorization",
        "The held-out set is not a debugging interface",
        "Do not reduce the denominator from twelve to eight",
        "frozen deterministic sequential replacement rule",
        "62 compressed arm logs",
        "ASI-THESEUS-FLAGSHIP-01",
        "15–25% less repeated",
        "P7.1 — Narrative synthesis and editorial compression",
        "P2-Q1-D1",
        "ASI-THESEUS-Q2-D2",
        "non-overlapping, independently sealed held-out denominators",
        "all 30 candidates hold sealed recipes and receipts",
        "P6.3 — Structural-completeness source and chapter tranche",
        "P6.4 — Second structural-boundary completeness audit",
        "P7.2 — Structural-tranche reader integration",
        "no chapter merges",
        "Manifest admission is not chapter completion",
        "bringing the manifest to 66",
        "human-ai-communication-persuasion-and-epistemic-security",
        "ai-deployment-transition-distribution-and-human-agency",
        "physical-compute-infrastructure-energy-and-environmental-constraints",
        "governed-objective-formation-value-learning-and-goal-integrity",
        "whether Candidates I, J, K, or L pass, are narrowed, or return to those owners",
        "Candidates J, K, and L each have two new source-noted comparators",
        "whether Candidate M passes",
        "Organizations, Institutions, and Societal Transition",
        "Work-in-progress limit",
        "P7.1a-W1-template-centralization-and-boundary-coverage",
        "P4-C1-evidence-claim-and-proof-custody-semantic-audit",
        "P7.1a-W2-opening-variation-and-thesis-depth-leveling",
        "P4-C2-safety-assurance-and-oversight-semantic-audit",
        "P7.2-T1-white-box-evidence-interpretability-and-activation-governance",
        "P4-C3-authority-effect-rollback-and-corrigibility-semantic-audit",
        "A blocked packet does not consume a slot",
        "The structural window is therefore closed again",
        "P2-R3-storage-materialization-and-replacement-qualification",
        "P6.5-R16-A-six-chapter-atom-pack",
        "P7.1a-W3 — prospective inheritance guard",
        "append-only post-activation atom pack",
        "material empirical/evidence checkpoint",
        "Are Sparse Autoencoder Benchmarks Reliable?",
        "R16-E — Governed optimizer landscape and optimizer-policy qualification",
        "AdamW",
        "Muon",
        "method-specific rescue",
        "a toy or under-tuned experiment cannot close the protocol",
        "capacity_entry_condition_met_materialization_not_yet_run",
        "71,648,034,816",
        "R16-A terminal receipt",
        "There is no open book-organization packet",
        "812→0 repeated 12-grams",
        "R16-C terminal receipt",
        "30 reviewed atoms",
        "30/30",
        "P7.2-T1D — proof-readiness depth pack",
        "Claim-bearing chapter maturity gate",
        "adversarial-machine-learning-and-model-attack-surface",
        "learning-theory-generalization-and-scaling-science",
        "Sixty-eight chapters is a possible result if both pass, not a target",
        "P6.8-functional-precision-and-behavior-preserving-computation",
        "The contingency title",
        "is not an active chapter candidate",
        "The paper's 49 references are an author-supplied research map, not automatic Appendix H records",
        "A naïve quantizer",
        "may not displace P2",
        "P6.9-R21-concept-complete-depth-and-atom-adequacy",
        "84/84 unified atom custody",
        "separate fifteen-chapter diagnostic-thin list",
        "diagnostics only",
        "digest-bound semantic",
        "zero unjustified widest raw blocks",
    ]:
        if phrase.casefold() not in roadmap_normalized:
            out.append(f"roadmap governing boundary missing: {phrase}")

    depth_review_normalized = re.sub(
        r"\s+", " ", data["post_round_18_depth_review"]
    ).casefold()
    for phrase in [
        "binding roadmap amendment; no support or release effect",
        "The working manifest contains **66 chapters**, not 61",
        "Claim-bearing chapter maturity gate",
        "Field decomposition",
        "Strongest challenge",
        "Implementation determination",
        "Failure and non-claim envelope",
        "Literature engagement by role",
        "Territory-sized reader value",
        "P7.2-T1D-proof-readiness-depth-pack",
        "Adversarial Machine Learning and the Model Attack Surface",
        "Learning Theory, Generalization, and Scaling Science",
        "approved for research and adjudication, not for immediate manifest admission",
        "Sixty-eight chapters is a possible result if both candidates pass, not a target",
        "Raw keyword counts do not adjudicate completeness",
    ]:
        if phrase.casefold() not in depth_review_normalized:
            out.append(f"post-Round-18 depth-review boundary missing: {phrase}")

    round_20 = status.get("round_20_chapter_substance_recovery", {})
    substance = data["round_20_chapter_substance"]
    substance_summary = substance.get("summary", {})
    round_20_atoms = data["round_20_four_chapter_atoms"]
    expected_round_20_diagnostic_thin = [
        "human-ai-communication-persuasion-and-epistemic-security",
        "governed-objective-formation-value-learning-and-goal-integrity",
        "institutions-international-coordination-and-public-legitimacy",
        "adversarial-machine-learning-and-model-attack-surface",
        "confidential-and-verifiable-ai-computation",
        "open-weight-release-and-post-release-control",
        "autonomous-replication-proliferation-and-containment",
        "perception-sensor-fusion-and-observation-trust",
        "human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty",
        "ai-deployment-transition-distribution-and-human-agency",
        "learning-theory-generalization-and-scaling-science",
        "physical-compute-infrastructure-energy-and-environmental-constraints",
        "scientific-discovery-and-experimental-governance",
    ]
    expected_round_20_remaining = []
    if (
        round_20.get("id") != "P6.9-R21-concept-complete-depth-and-atom-adequacy"
        or round_20.get("state") != "terminal_concept_raw_scaffold_and_handoff_complete"
        or round_20.get("manifest_chapter_count_freeze") != 84
        or round_20.get("word_trigger") != 5000
        or round_20.get("word_trigger_is_acceptance_or_evidence_gate") is not False
        or round_20.get("baseline_thin_chapter_count") != 23
        or round_20.get("current_thin_chapter_count") != 12
        or round_20.get("priority_chapter_count") != 23
        or round_20.get("priority_concept_count") != 184
        or round_20.get("priority_concepts_passing") != 184
        or round_20.get("current_unified_atom_covered_chapter_count") != 84
        or round_20.get("diagnostic_thin_chapters") != expected_round_20_diagnostic_thin
        or round_20.get("remaining_concept_completion_queue") != expected_round_20_remaining
        or round_20.get("completion_authority")
        != "named_concept_contract_plus_current_digest_bound_semantic_disposition"
        or round_20.get("current_digest_bound_semantic_review_count") != 23
        or round_20.get("next_priority_batch_size") != 0
        or round_20.get("next_priority_batch") != expected_round_20_remaining
        or round_20.get("throughput_unit")
        != "concept_complete_digest_bound_semantic_dispositions"
        or round_20.get("round_22_adjudication_path")
        != "docs/round_22_evidence_pivot_and_concept_atom_adjudication_2026_07_30.md"
        or round_20.get("concept_linked_atom_addendum_path")
        != "evidence_quality/round22_concept_linked_claim_atom_addendum.json"
        or round_20.get("initial_low_atom_count_diagnostic_chapter_count") != 19
        or round_20.get("concept_linked_decomposition_chapter_count") != 13
        or round_20.get("concept_linked_decomposition_atom_count") != 104
        or round_20.get("low_atom_count_diagnostic_chapter_count") != 6
        or round_20.get("single_atom_diagnostic_chapter_count") != 0
        or round_20.get("remaining_manual_decomposition_chapters")
        != [
            "human-factors-and-meaningful-control-in-oversight",
            "privacy-data-rights-and-information-flow-governance",
            "governed-world-models-and-reality-grounding",
            "governed-model-training-distributed-optimization-and-scaling",
            "white-box-evidence-interpretability-and-activation-governance",
            "governed-operations-incident-command-and-graceful-degradation",
        ]
        or round_20.get("atom_count_parity_is_acceptance_target") is not False
        or round_20.get("reader_facing_w3_repeated_12_grams") != 0
        or round_20.get("raw_qmd_repeated_12_grams") != 905
        or round_20.get("raw_qmd_maximum_chapter_spread") != 65
        or round_20.get("raw_scaffold_audit_required") is not True
        or round_20.get("raw_scaffold_exit") != "zero_unjustified_widest_spread_blocks"
        or round_20.get("raw_scaffold_audit_path")
        != "evidence_quality/p6_9_raw_scaffold_ownership_audit.json"
        or round_20.get("raw_scaffold_audit_state") != "terminal_complete"
        or round_20.get("raw_scaffold_widest_block_count") != 21
        or round_20.get("raw_scaffold_generated_owned_block_count") != 21
        or round_20.get("raw_scaffold_reader_visible_block_count") != 0
        or round_20.get("raw_scaffold_unjustified_block_count") != 0
        or len(round_20.get("evidence_handoff_requires", [])) != 8
        or round_20.get("evidence_handoff_path")
        != "evidence_quality/p6_9_proof_evidence_handoff.json"
        or round_20.get("evidence_handoff_state") != "terminal_complete"
        or round_20.get("evidence_handoff_chapter_count") != 23
        or round_20.get("evidence_handoff_concept_count") != 184
        or round_20.get("evidence_handoff_missing_identity_count") != 0
        or round_20.get("p6_9_terminal") is not True
        or round_20.get("manual_semantic_review_required") is not True
        or round_20.get("support_state_effect") != "none"
        or round_20.get("release_effect") != "none"
    ):
        out.append("Round 20 chapter-substance terminal identity or receipt drifted")
    raw_audit = data["p6_9_raw_scaffold_audit"]
    if (
        raw_audit.get("state") != "terminal_complete"
        or raw_audit.get("summary", {}).get("widest_block_count") != 21
        or raw_audit.get("summary", {}).get(
            "generated_source_reconciliation_block_count"
        )
        != 21
        or raw_audit.get("summary", {}).get("reader_visible_widest_block_count") != 0
        or raw_audit.get("summary", {}).get("unjustified_widest_block_count") != 0
        or raw_audit.get("summary", {}).get("exit_passed") is not True
    ):
        out.append("P6.9 raw-scaffold terminal receipt drifted")
    handoff = data["p6_9_proof_evidence_handoff"]
    if (
        handoff.get("state") != "terminal_complete"
        or handoff.get("summary", {}).get("chapter_count") != 23
        or handoff.get("summary", {}).get("concept_count") != 184
        or handoff.get("summary", {}).get("concepts_with_source_identity_count")
        != 184
        or handoff.get("summary", {}).get("concepts_with_atom_identity_count")
        != 184
        or handoff.get("summary", {}).get("concepts_with_falsifier_count") != 184
        or handoff.get("summary", {}).get("concepts_with_evidence_lane_count") != 184
        or handoff.get("summary", {}).get("concepts_with_maximum_inference_count")
        != 184
        or handoff.get("summary", {}).get(
            "concepts_with_unresolved_challenge_count"
        )
        != 184
        or handoff.get("summary", {}).get("missing_handoff_identity_count") != 0
        or handoff.get("support_state_effect") != "none"
    ):
        out.append("P6.9 proof/evidence handoff terminal receipt drifted")
    if (
        substance.get("manifest_chapter_count_freeze") != 84
        or substance_summary.get("thin_chapter_count") != 12
        or substance_summary.get("atom_covered_chapter_count") != 84
        or substance_summary.get("atom_uncovered_chapter_count") != 0
        or substance_summary.get("active_concept_count") != 184
        or substance_summary.get("active_concepts_passing_count") != 184
        or substance_summary.get("concept_complete_semantic_reviewed_chapter_count") != 23
        or substance_summary.get("current_semantic_review_count") != 23
        or substance_summary.get("low_atom_count_diagnostic_chapter_count") != 6
        or substance_summary.get("atom_count_is_acceptance_target") is not False
        or substance_summary.get("word_trigger_is_completion_gate") is not False
        or substance.get("manual_semantic_review_required") is not True
        or substance.get("support_state_effect") != "none"
    ):
        out.append("Round 20 chapter-substance contract drifted from the terminal concept queue")
    if (
        round_20_atoms.get("chapter_count") != 4
        or round_20_atoms.get("atom_count") != 20
        or round_20_atoms.get("support_state_effect") != "none"
        or round_20_atoms.get("release_effect") != "none"
    ):
        out.append("Round 20 four-chapter atom packet drifted")
    round_20_text = re.sub(
        r"\s+", " ", data["round_20_depth_reconciliation"]
    ).casefold()
    for phrase in [
        "the chapter count is frozen at 84",
        "word count is a triage signal, not an acceptance test",
        "unified current-manifest atom coverage is now 84/84",
        "first priority tranche complete, twenty-chapter depth queue active",
    ]:
        if phrase.casefold() not in round_20_text:
            out.append(f"Round 20 reconciliation boundary missing: {phrase}")

    round_21_text = re.sub(
        r"\s+", " ", data["round_21_depth_adjudication"]
    ).casefold()
    for phrase in [
        "crossing 5,000 words is neither necessary nor sufficient",
        "digest-bound, semantically reviewed concept manifests",
        "nineteen chapters have five or fewer atom references",
        "matching legacy atom counts is prohibited as an acceptance target",
        "zero unjustified widest-spread raw blocks",
        "clean evidence handoff",
    ]:
        if phrase.casefold() not in round_21_text:
            out.append(f"Round 21 depth-contract boundary missing: {phrase}")

    precision_reconciliation_normalized = re.sub(
        r"\s+", " ", data["precision_contract_reconciliation"]
    ).casefold()
    for phrase in [
        "integrate into existing owners; no new chapter now",
        "rankfold-neuralfold-and-artifact-compression",
        "functional-precision-and-behavior-preserving-computation",
        "not a chapter candidate in active research",
        "The paper cites 49 external works",
        "A small broken quantizer or weak average-accuracy probe",
        "cannot displace P2",
    ]:
        if phrase.casefold() not in precision_reconciliation_normalized:
            out.append(f"Precision Contract reconciliation boundary missing: {phrase}")

    precision_note_normalized = re.sub(
        r"\s+", " ", data["precision_contract_source_note"]
    ).casefold()
    for phrase in [
        "Functional Precision Compiler",
        "CompleteDescriptionLedger",
        "update existing chapters first; do not add a chapter now",
        "No universal optimal precision",
    ]:
        if phrase.casefold() not in precision_note_normalized:
            out.append(f"Precision Contract source-note boundary missing: {phrase}")

    precision_status = status.get("post_round_18_depth_and_coverage_amendment", {}).get(
        "precision_contract_source_amendment", {}
    )
    if precision_status.get("state") != "source_and_existing_owner_prose_terminal_evidence_queued":
        out.append("Precision Contract source intake state drifted")
    if precision_status.get("primary_owner") != "rankfold-neuralfold-and-artifact-compression":
        out.append("Precision Contract primary owner drifted")
    if precision_status.get("new_chapter_allowed_now") is not False:
        out.append("Precision Contract prematurely authorizes a new chapter")
    if precision_status.get("contingency_is_active_candidate") is not False:
        out.append("Precision Contract contingency became an active candidate")
    if precision_status.get("p2_displacement_allowed") is not False:
        out.append("Precision Contract packet displaces P2")
    if precision_status.get("third_wip_lane_allowed") is not False:
        out.append("Precision Contract packet creates a third WIP lane")
    if precision_status.get("automatic_appendix_h_admission_allowed") is not False:
        out.append("Precision Contract packet automatically admits cited sources")
    if precision_status.get("support_state_effect") != "none" or precision_status.get("release_effect") != "none":
        out.append("Precision Contract packet launders support or release state")

    required_manuscript_phrases = {
        "inner_alignment_depth": "### Deceptive alignment, training games, and gradient hacking",
        "multi_agent_depth": "### Strategic foundations: games, bargaining, choice, and adaptation",
        "perception_depth": "### Bayesian state estimation and concrete fusion regimes",
        "embodied_depth": "### Hybrid control, timing evidence, and sim-to-real limits",
        "organization_depth": "### Organizational transition: tasks, jobs, power, and public capacity",
        "white_box_depth": "### Probes, sparse dictionaries, circuits, and causal challenge",
        "uncertainty_repair": "Four uncertainty families receive separate fields and remedies",
        "types_and_transformation_repair": "### Compression as a verified program transformation",
        "synthetic_data_repair": "### Governed synthetic-data and self-play lifecycle",
        "explanation_repair": "### Explanation generation as a governed translation",
        "precision_primary": "### Functional precision: preserve behavior, not coordinates",
        "precision_residual": "### Progressive numerical precision as residual honesty",
        "precision_runtime": "### Precision routing is an execution policy",
        "precision_economics": "### The full economics of precision",
        "precision_readiness": "### Precision certificates, expiry, and readmission",
        "precision_custody": "### Precision derivatives extend the custody graph",
        "precision_efficiency": "### Functional precision as one routed resource",
        "precision_synthesis": "### Functional precision across the reference trace",
    }
    for key, phrase in required_manuscript_phrases.items():
        if phrase not in data["manuscript_completion"].get(key, ""):
            out.append(f"roadmap manuscript completion missing: {key}")

    precision_inventory_rows = [
        row for row in data["source_inventory"] if row.get("id") == "precision_contract"
    ]
    if len(precision_inventory_rows) != 1:
        out.append("Precision Contract source inventory row missing or duplicated")
    else:
        expected_precision_targets = {
            "rankfold-neuralfold-and-artifact-compression",
            "compact-generative-systems-and-residual-honesty",
            "fast-generation-architectures",
            "resource-economics-and-token-budgets",
            "readiness-gates-residual-escrow-and-quarantine",
            "executable-specifications-and-lean-proof-envelope",
            "model-weight-custody-and-hardware-roots-of-trust",
            "open-weight-release-and-post-release-control",
            "the-efficient-asi-hypothesis",
        }
        if set(precision_inventory_rows[0].get("chapter_targets", [])) != expected_precision_targets:
            out.append("Precision Contract source target set drifted")
        assigned_precision_chapters = {
            chapter["id"]
            for part in data["book_manifest"]["parts"]
            for chapter in part["chapters"]
            if "precision_contract" in chapter.get("source_ids", [])
        }
        if assigned_precision_chapters != expected_precision_targets:
            out.append("Precision Contract manifest assignment set drifted")
    if data["precision_contract_backlog"].get("insertion_decision") != "update_existing_chapter":
        out.append("Precision Contract backlog insertion decision drifted")
    if data["precision_contract_backlog"].get("support_state_effect") != "argument_only":
        out.append("Precision Contract backlog support boundary drifted")
    if data["precision_contract_triage"].get("support_state_effect") != "backlog_only":
        out.append("Precision Contract triage support boundary drifted")

    structural = data["structural_research"]
    structural_normalized = re.sub(r"\s+", " ", structural).casefold()
    for phrase in [
        "Status: **first tranche manifest-admitted; initial drafts complete; evidence and reader integration gated**",
        "Merge no chapters",
        "White-Box Evidence, Interpretability, and Activation Governance",
        "Governed World Models and Reality Grounding",
        "Human Factors and Meaningful Control in Oversight",
        "Governed Operations, Incident Command, and Graceful Degradation",
        "Tranche-wide admission and completion gates",
        "Corben-source crosswalk",
        "No cited result promotes a chapter core claim",
    ]:
        if phrase.casefold() not in structural_normalized:
            out.append(f"structural research boundary missing: {phrase}")

    structural_gap = data["structural_gap_audit"]
    structural_gap_normalized = re.sub(r"\s+", " ", structural_gap).casefold()
    for phrase in [
        "Status: **historical second-tranche audit, amended by the terminal Round 18 breadth transaction**",
        "bounded thirteen-candidate second tranche",
        "Governed Model Training, Distributed Optimization, and Scaling",
        "Perception, Sensor Fusion, and Observation Trust",
        "Embodied Agency, Real-Time Control, and Physical Safety",
        "Privacy, Data Rights, and Information-Flow Governance",
        "Human–AI Organizations, Delegation, and Accountability",
        "Multi-Agent Dynamics, Collective Intelligence, and Systemic Risk",
        "Autonomous Replication, Proliferation, and Containment",
        "Scientific Discovery and Experimental Governance",
        "Human–AI Communication, Persuasion, and Epistemic Security",
        "Institutions, International Coordination, and Public Legitimacy",
        "AI Deployment, Transition, Distribution, and Human Agency",
        "Physical Compute Infrastructure, Energy, and Environmental Constraints",
        "Governed Objective Formation, Value Learning, and Goal Integrity",
        "ext_conversational_persuasion_gpt4_2025",
        "ext_anthropic_model_persuasiveness_2024",
        "ext_commercial_persuasion_ai_2026",
        "ext_un_global_digital_compact_2024",
        "ext_council_europe_ai_convention_2024",
        "ext_generative_ai_at_work_2025",
        "ext_ilo_genai_jobs_index_2025",
        "ext_iea_energy_and_ai_2025",
        "ext_lbnl_data_center_energy_2024",
        "required source-role admission gate is **not** satisfied",
        "Candidate J's source-role gate remains open",
        "Candidate K's source gate remains open",
        "Candidate L's source gate remains open",
        "Candidate M's source-role gate remains open",
        "Required section-scale additions, not chapters",
        "Seventy-two is not a target",
        "remain required whether Candidate I is admitted, rejected, or narrowed",
        "Embedded agency, self-reference, and robust delegation",
        "mechanism or capability, limitation or failure, competing design, and measurement or evaluation",
    ]:
        if phrase.casefold() not in structural_gap_normalized:
            out.append(f"structural gap audit boundary missing: {phrase}")

    optimizer_research_normalized = re.sub(r"\s+", " ", data["optimizer_research"]).casefold()
    for phrase in [
        "The book has the correct owner but not yet the required optimizer depth",
        "Do not create a separate optimizer chapter",
        "AdamW as the modern reference baseline",
        "Structure-aware alternatives",
        "Muon and qualified variants",
        "Optimizer choice is a run-policy choice",
        "Competent comparison and argument-exit protocol",
        "equal or explicitly accounted tuning budgets",
        "at least three independent seeds",
        "Failure of a naive, under-tuned, incorrectly grouped, or resource-starved arm",
        "Optimizer selection creates no automatic safety, governance, readiness, release, RSI, or ASI claim",
    ]:
        if phrase.casefold() not in optimizer_research_normalized:
            out.append(f"optimizer research boundary missing: {phrase}")
    inventory = {row.get("id"): row for row in data["source_inventory"]}
    for source_id in STRUCTURAL_SOURCE_IDS + STRUCTURAL_GAP_SOURCE_IDS:
        if source_id not in inventory:
            out.append(f"structural source missing from inventory: {source_id}")
        note = ROOT / f"sources/source_notes/{source_id}.md"
        if not note.exists():
            out.append(f"structural source note missing: {source_id}")

    manifest_chapters = [
        chapter
        for part in data["book_manifest"].get("parts", [])
        for chapter in part.get("chapters", [])
    ]
    manifest_ids = {chapter.get("id") for chapter in manifest_chapters}
    first_ids = set(status["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]["candidate_ids"])
    second_ids = set(status["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"]["candidate_ids"])
    if len(manifest_chapters) != 84:
        out.append(f"working manifest chapter count is {len(manifest_chapters)}, expected 84")
    if not first_ids.issubset(manifest_ids):
        out.append(f"first structural tranche missing manifest IDs: {sorted(first_ids - manifest_ids)}")
    if set(STRUCTURAL_CHAPTER_PATHS) != first_ids:
        out.append("first structural tranche chapter-path contract drifted")
    missing_drafts = sorted(
        chapter_id for chapter_id, path in STRUCTURAL_CHAPTER_PATHS.items()
        if not path.exists() or not path.read_text(encoding="utf-8").strip()
    )
    if missing_drafts:
        out.append(f"first structural tranche initial drafts missing or empty: {missing_drafts}")
    admitted_second = second_ids.intersection(manifest_ids)
    expected_admitted_second = second_ids
    if admitted_second != expected_admitted_second:
        out.append(f"second structural tranche terminal/admission set drifted: {sorted(admitted_second)}")

    contract = data["competence"]
    for section in [
        "## Exploration versus claim-bearing work",
        "## Competence dossier required before held-out opening",
        "### 1. Claim and mechanism identity",
        "### 2. Implementation competence",
        "### 3. Construct and task validity",
        "### 4. Evaluator competence",
        "### 5. Sensitivity and statistical adequacy",
        "### 6. Fair rescue ladder",
        "## Negative-inference ladder",
        "## Current-result rehabilitation",
        "## Completion gate",
    ]:
        if contract.count(section) != 1:
            out.append(f"competence-contract section missing or duplicated: {section}")
    contract_normalized = re.sub(r"\s+", " ", contract).casefold()
    for phrase in [
        "natural, non-authored corpus",
        "materially independent second implementation",
        "known effect injection",
        "minimum effect of practical interest",
        "N0 — Instrument failure",
        "N1 — Implementation failure",
        "N2 — Proxy or regime failure",
        "N3 — Exact implementation result",
        "N4 — Mechanism-level counterevidence",
        "N5 — Broad claim refutation",
        "at least two materially different transfer settings",
        "implementation-to-architecture generalization",
    ]:
        if phrase.casefold() not in contract_normalized:
            out.append(f"competence-contract boundary missing: {phrase}")

    predecessor = data["predecessor"]
    if predecessor.get("status") != "completed" or predecessor.get("current_priority") is not None:
        out.append("predecessor must be terminally completed with no current priority")
    if data["terminal"].get("decision") != "roadmap_complete_no_public_release":
        out.append("predecessor terminal record is absent or drifted")
    if data["terminal"].get("successor", {}).get("path") != status.get("roadmap_path"):
        out.append("terminal record does not activate this exact successor")

    x_manifest = data["x_manifest"]
    if x_manifest.get("publication", {}).get("state") != "source_ready_composer_refresh_required":
        out.append("X synopsis publication boundary drifted")
    if x_manifest.get("staleness", {}).get("successor_authority") != status.get("roadmap_path"):
        out.append("X synopsis does not bind this maintenance authority")
    if data["x_release"].get("successor") != status.get("roadmap_path"):
        out.append("X disposition does not bind this maintenance authority")

    truth = status.get("activation_truth", {})
    snapshot = data["transition_snapshot"]
    expected_snapshot = {
        "file_count": truth.get("transition_file_count"),
        "accepted_count": truth.get("review_accepted_transition_count"),
        "direct_count": truth.get("direct_atom_bound_transition_count"),
        "indirect_count": truth.get("indirect_identity_mapped_transition_count"),
    }
    for key, expected in expected_snapshot.items():
        if snapshot[key] != expected:
            out.append(f"transition snapshot drift for {key}: {snapshot[key]} != {expected}")
    state_bindings = {
        "argument": "accepted_no_change_transition_count",
        "refuted": "accepted_refuted_transition_count",
        "synthetic-test-backed": "accepted_synthetic_test_backed_transition_count",
        "prototype-backed": "accepted_prototype_backed_transition_count",
        "empirical-test-backed": "accepted_empirical_test_backed_transition_count",
    }
    for state, field in state_bindings.items():
        if snapshot["states"].get(state, 0) != truth.get(field):
            out.append(f"accepted transition state drift for {state}")
    if snapshot["effects"].get("no_change", 0) != 87 or snapshot["effects"].get("refuted", 0) != 3:
        out.append("negative/no-change transition denominator drifted")

    identity = data["identity_graph"]
    identity_summary = identity.get("summary", {})
    identity_status = status.get("claim_identity_graph", {})
    for field, expected in {
        "review_accepted_transition_count": 115,
        "direct_atom_relation_count": 25,
        "indirect_relation_count": 90,
        "resolved_transition_count": 115,
        "unresolved_transition_count": 0,
    }.items():
        if identity_summary.get(field) != expected:
            out.append(f"claim identity graph summary drift: {field}")
    if identity_status.get("state") != "complete":
        out.append("claim identity graph is not complete")
    if identity_status.get("resolved_transition_count") != 115 or identity_status.get("unresolved_transition_count") != 0:
        out.append("roadmap status does not preserve complete identity resolution")
    if truth.get("resolved_transition_claim_mapping_count") != 115 or truth.get("unresolved_transition_claim_mapping_count") != 0:
        out.append("activation truth still reports unresolved accepted identities")
    if status.get("competence_and_identity_contract", {}).get("unresolved_claim_mapping_count") != 0:
        out.append("competence contract still reports unresolved accepted identities")

    rehabilitation = data["negative_rehabilitation"]
    rehabilitation_summary = rehabilitation.get("summary", {})
    rehabilitation_status = status.get("negative_result_rehabilitation", {})
    expected_rehabilitation = {
        "accepted_negative_or_no_change_transition_count": 90,
        "n0_count": 1,
        "n1_count": 15,
        "n2_count": 74,
        "n3_count": 0,
        "n4_count": 0,
        "n5_count": 0,
        "broad_negative_inference_count": 0,
        "chapter_core_negative_inference_count": 0,
    }
    for field, expected in expected_rehabilitation.items():
        ledger_value = (
            rehabilitation_summary.get("n_level_counts", {}).get(field[0:2].upper())
            if re.fullmatch(r"n[0-5]_count", field)
            else rehabilitation_summary.get(field)
        )
        if ledger_value != expected:
            out.append(f"negative-result rehabilitation summary drift: {field}")
        if rehabilitation_status.get(field) != expected:
            out.append(f"roadmap rehabilitation status drift: {field}")
    if rehabilitation_status.get("historical_raw_outcomes_preserved") is not True:
        out.append("roadmap status does not preserve immutable historical outcomes")
    if rehabilitation_status.get("support_state_effect") != "none" or rehabilitation_status.get("release_effect") != "none":
        out.append("negative-result rehabilitation cannot create support or release effects")
    surface_summary = data["negative_surface_audit"].get("summary", {})
    surface_scope = data["negative_surface_audit"].get("scope", {})
    for field, expected in {
        "forbidden_overbroad_phrase_count": 0,
        "missing_required_rehabilitation_boundary_count": 0,
        "blocked_chapter_boundary_failure_count": 0,
        "broad_negative_inference_count": 0,
        "chapter_core_refutation_count": 0,
    }.items():
        if surface_summary.get(field) != expected:
            out.append(f"negative-inference surface audit drift: {field}")
    current_live_chapters = status.get("activation_truth", {}).get("live_working_chapter_count")
    if surface_scope.get("surface_count") != (
        surface_scope.get("chapter_count", 0)
        + surface_scope.get("public_and_derivative_surface_count", 0)
    ):
        out.append("negative-inference current surface denominator drifted")
    if surface_scope.get("chapter_count") != current_live_chapters:
        out.append("negative-inference live chapter denominator drifted")
    if surface_scope.get("public_and_derivative_surface_count") != 20:
        out.append("negative-inference public/derivative surface denominator drifted")
    for field, expected in {
        "forbidden_overbroad_phrase_count": 0,
        "missing_rehabilitation_boundary_count": 0,
        "blocked_chapter_boundary_failure_count": 0,
    }.items():
        if rehabilitation_status.get(field) != expected:
            out.append(f"roadmap surface-rehabilitation status drift: {field}")
    frozen_commit = rehabilitation_status.get("frozen_snapshot_commit")
    frozen_digest = rehabilitation_status.get("frozen_snapshot_sha256")
    if rehabilitation_status.get("frozen_surface_count") != 75 or rehabilitation_status.get("frozen_chapter_surface_count") != 55:
        out.append("frozen negative-inference snapshot denominator drifted")
    try:
        frozen = subprocess.run(
            ["git", "show", f"{frozen_commit}:evidence_quality/negative_inference_surface_audit.json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    except subprocess.CalledProcessError:
        out.append("frozen negative-inference snapshot commit is unavailable")
    else:
        if hashlib.sha256(frozen).hexdigest() != frozen_digest:
            out.append("frozen negative-inference snapshot digest drifted")

    p2 = data["p2_selection"]
    p2_status = status.get("p2_frontier_selection", {})
    if len(p2.get("candidates", [])) != 5:
        out.append("P2 frontier candidate denominator drifted")
    selected_claim = p2.get("selected_claim", {})
    if selected_claim.get("claim_id") != "p2.governed_natural_repository_change_admission_joint_frontier":
        out.append("P2 selected claim identity drifted")
    if selected_claim.get("canonical_parent_atom") != "integrated-reference-architecture.invariant.015":
        out.append("P2 canonical parent identity drifted")
    gates = {row.get("id"): row.get("state") for row in p2.get("preflight_gates", [])}
    if sum(state == "pending" for state in gates.values()) != 7 or gates.get("heldout") != "closed":
        out.append("P2 competence or heldout gate state drifted")
    if p2.get("local_feasibility_snapshot", {}).get("final_denominator_opened") is not False:
        out.append("P2 final denominator opened before competence gates")
    for field, expected in {
        "candidate_count": 5,
        "selected_claim_id": "p2.governed_natural_repository_change_admission_joint_frontier",
        "canonical_parent_atom": "integrated-reference-architecture.invariant.015",
        "pending_competence_gate_count": 7,
        "final_heldout_gate_state": "closed",
        "final_denominator_opened": False,
    }.items():
        if p2_status.get(field) != expected:
            out.append(f"P2 roadmap selection status drift: {field}")

    p2_corpus = data["p2_corpus"]
    p2_corpus_status = status.get("p2_development_corpus_preflight", {})
    corpus_expected = {
        "source_id": "ext_swe_rebench_v2_2026",
        "eligible_post_snapshot_task_count": 1117,
        "eligible_repository_count": 532,
        "eligible_language_count": 20,
        "development_task_count": 12,
        "development_repository_count": 12,
        "development_language_count": 7,
        "resolvable_image_manifest_count": 12,
        "construct_gate_state": "pending_four_replacements_dual_evaluator_and_independent_task_review",
        "resource_gate_state": "pending_peak_memory_cpu_and_frozen_ceiling_before_replacement_draw",
        "final_pool_selected": False,
        "final_denominator_opened": False,
    }
    observed_corpus = {
        "source_id": p2_corpus.get("source", {}).get("source_id"),
        "eligible_post_snapshot_task_count": p2_corpus.get("eligible_universe", {}).get("row_count"),
        "eligible_repository_count": p2_corpus.get("eligible_universe", {}).get("repository_count"),
        "eligible_language_count": p2_corpus.get("eligible_universe", {}).get("language_count"),
        "development_task_count": p2_corpus.get("development_pool", {}).get("row_count"),
        "development_repository_count": p2_corpus.get("development_pool", {}).get("repository_count"),
        "development_language_count": p2_corpus.get("development_pool", {}).get("language_count"),
        "resolvable_image_manifest_count": 12,
        "construct_gate_state": p2_corpus.get("preflight_effect", {}).get("construct_gate"),
        "resource_gate_state": p2_corpus.get("preflight_effect", {}).get("resource_gate"),
        "final_pool_selected": False,
        "final_denominator_opened": p2.get("local_feasibility_snapshot", {}).get("final_denominator_opened"),
    }
    for field, expected in corpus_expected.items():
        if observed_corpus.get(field) != expected:
            out.append(f"P2 corpus record drift: {field}")
        if p2_corpus_status.get(field) != expected:
            out.append(f"P2 corpus status drift: {field}")
    if p2_corpus.get("preflight_effect", {}).get("support_state_effect") != "none":
        out.append("P2 development corpus preflight promoted support")

    p2_gold = data["p2_gold"]
    p2_policy = data["p2_policy"]
    p2_gold_status = status.get("p2_gold_preflight_diagnosis", {})
    terminal = p2_gold.get("terminal_disposition", {})
    custody = p2_gold.get("custody_and_raw_evidence", {})
    next_action = p2_gold.get("next_required_action", {})
    gold_expected = {
        "original_development_task_count": 12,
        "original_exact_pass_count": 7,
        "independent_parser_recovered_task_count": 1,
        "qualified_task_count": 8,
        "excluded_n0_task_count": 4,
        "replacement_slot_count": 4,
        "verified_arm_log_count": 62,
        "attempt_record_count": 8,
        "replacement_draw_started": True,
        "resource_ceiling_state": "frozen_queue_drawn_measurement_gate_pending",
        "construct_gate_state": "pending_four_replacements_dual_evaluator_and_independent_task_review",
        "final_pool_selected": False,
        "final_denominator_opened": False,
    }
    observed_gold = {
        "original_development_task_count": p2_gold.get("original_fixed_denominator", {}).get("task_count"),
        "original_exact_pass_count": p2_gold.get("original_fixed_denominator", {}).get("exact_pass_count"),
        "independent_parser_recovered_task_count": p2_gold.get("false_negative_findings", {}).get("upstream_parser_false_reject_count"),
        "qualified_task_count": terminal.get("qualified_task_count"),
        "excluded_n0_task_count": terminal.get("excluded_n0_task_count"),
        "replacement_slot_count": terminal.get("replacement_slot_count"),
        "verified_arm_log_count": custody.get("verified_compressed_arm_log_count"),
        "attempt_record_count": custody.get("attempt_record_count"),
        "replacement_draw_started": next_action.get("replacement_draw_started"),
        "resource_ceiling_state": (
            "frozen_queue_drawn_measurement_gate_pending"
            if data["p2_resource"].get("qualification_state", {}).get("ceiling_frozen") is True
            and data["p2_resource"].get("qualification_state", {}).get("replacement_draw_started") is True
            and data["p2_resource"].get("qualification_state", {}).get("resource_gate_passed") is False
            else "drift"
        ),
        "construct_gate_state": "pending_four_replacements_dual_evaluator_and_independent_task_review",
        "final_pool_selected": custody.get("final_pool_selected"),
        "final_denominator_opened": custody.get("final_pool_opened"),
    }
    for field, expected in gold_expected.items():
        if observed_gold.get(field) != expected:
            out.append(f"P2 gold diagnosis record drift: {field}")
        if p2_gold_status.get(field) != expected:
            out.append(f"P2 gold diagnosis status drift: {field}")
    if p2_gold.get("false_negative_findings", {}).get("idea_or_mechanism_negative_inference_count") != 0:
        out.append("P2 instrument failure laundered into mechanism inference")
    if p2_policy.get("replacement_rule", {}).get("replacement_draw_state") != "metadata_queue_frozen_candidate_content_unopened":
        out.append("P2 replacement policy does not record the frozen metadata-only queue")
    if p2_policy.get("replacement_rule", {}).get("skipping_candidate_after_outcome_allowed") is not False:
        out.append("P2 replacement policy allows outcome-aware skipping")
    if p2_gold.get("support_state_effect") != "none" or p2_policy.get("support_state_effect") != "none":
        out.append("P2 gold diagnosis or policy promoted support")

    p2_queue = data["p2_replacement_queue"]
    p2_queue_status = status.get("p2_replacement_queue", {})
    queue_candidates = [candidate for slot in p2_queue.get("slots", []) for candidate in slot.get("candidates", [])]
    queue_expected = {
        "slot_count": 4,
        "candidate_count": 30,
        "unique_candidate_repository_count": 30,
        "rust_candidate_count": 9,
        "go_candidate_count": 20,
        "java_candidate_count": 1,
        "candidate_task_content_opened": False,
        "replacement_qualification_started": False,
        "final_pool_selected": False,
        "final_denominator_opened": False,
    }
    observed_queue = {
        "slot_count": p2_queue.get("slot_count"),
        "candidate_count": p2_queue.get("candidate_count"),
        "unique_candidate_repository_count": len({row.get("repo") for row in queue_candidates}),
        "rust_candidate_count": sum(row.get("language") == "rust" for row in queue_candidates),
        "go_candidate_count": sum(row.get("language") == "go" for row in queue_candidates),
        "java_candidate_count": sum(row.get("language") == "java" for row in queue_candidates),
        "candidate_task_content_opened": p2_queue.get("task_text_opened"),
        "replacement_qualification_started": p2_queue.get("replacement_qualification_started"),
        "final_pool_selected": p2_queue.get("final_pool_selected"),
        "final_denominator_opened": p2_queue.get("final_pool_opened"),
    }
    for field, expected in queue_expected.items():
        if observed_queue.get(field) != expected:
            out.append(f"P2 replacement queue record drift: {field}")
        if p2_queue_status.get(field) != expected:
            out.append(f"P2 replacement queue status drift: {field}")
    if p2_queue.get("support_state_effect") != "none":
        out.append("P2 replacement queue promoted support")

    quality_program = status.get("quality_uplift_program", {})
    execution_readiness = status.get("execution_readiness", {})
    if execution_readiness.get("state") != "p2_resource_blocked_p7_3_visual_edition_active":
        out.append("execution board does not preserve the P2 resource block while activating P7.3 visual-edition work")
    if execution_readiness.get("headline_priority") != "P2" or execution_readiness.get("headline_priority_state") != "latest_exact_preflight_failed_capacity_and_docker_restore_both_before_retry":
        out.append("execution board obscures the P2 headline or the current below-floor attempt requirement")
    if execution_readiness.get("work_in_progress_limit") != 2 or execution_readiness.get("blocked_lane_consumes_work_in_progress") is not False:
        out.append("execution board lost its bounded WIP or blocked-lane rule")
    if execution_readiness.get("protected_outcome_inspection_allowed") is not False:
        out.append("execution board permits protected-outcome inspection")
    if execution_readiness.get("structural_admission_freeze") is not False:
        out.append("execution board contradicts the superseding no-deferral manuscript policy")
    if execution_readiness.get("immediate_empirical_packet") != "P2-R3-storage-materialization-and-replacement-qualification":
        out.append("execution board does not make P2-R3 the operative empirical headline")
    if execution_readiness.get("immediate_book_packet") != "P7.3-governed-manim-visual-edition":
        out.append("execution board does not activate the governed Manim visual-edition packet")
    if execution_readiness.get("immediate_formal_packet") != "P4-terminal-no-open-formal-packet":
        out.append("execution board reopens terminal P4 formal work")
    if execution_readiness.get("maximum_concurrent_second_tranche_candidates") != 0:
        out.append("execution board permits a structural candidate during the freeze")
    expected_resume_gates = [
        "P2-pool-materialization-terminal-receipt",
        "P2-four-replacement-slots-qualified-and-twelve-task-denominator-restored",
        "P6.5-R16-six-chapter-claim-atom-addendum-terminal",
        "P6.5-R16-current-eighty-four-chapter-reader-freshness-terminal",
        "P7.1a-W3-admission-template-inheritance-guard-terminal",
        "P7.2-T1D-six-chapter-proof-readiness-depth-pack-terminal",
    ]
    if execution_readiness.get("structural_resume_requires") != expected_resume_gates:
        out.append("execution board structural-resume gate set drifted")

    manim = status.get("manim_visual_edition", {})
    expected_pilots = [
        "asi-is-a-stack-not-a-model",
        "capability-replacement-and-rollback",
        "context-transactions-snapshots-mounts-and-taint",
        "replaceable-cognitive-substrates-beyond-transformer-monoculture",
        "living-book-methodology",
    ]
    if manim.get("id") != "P7.3-governed-manim-visual-edition":
        out.append("Manim visual-edition identity drifted")
    if manim.get("state") != "active_generation_2_production_with_12_predecessor_previews_preserved":
        out.append("Manim visual-edition state does not preserve active generation-2 production and 12 predecessor previews")
    if manim.get("canonical_chapter_count") != len(manifest_chapters) or len(manifest_chapters) != 84:
        out.append("Manim visual-edition chapter target does not match the canonical manifest")
    if manim.get("pilot_chapter_ids") != expected_pilots:
        out.append("Manim five-pilot order drifted")
    missing_pilots = sorted(set(expected_pilots) - manifest_ids)
    if missing_pilots:
        out.append(f"Manim pilot chapter IDs missing from manifest: {missing_pilots}")
    toolchain = manim.get("toolchain", {})
    if (
        toolchain.get("implementation") != "Manim Community Edition"
        or toolchain.get("initial_pin") != "0.20.1"
        or toolchain.get("contract_path") != "visual_edition/toolchain.json"
        or toolchain.get("requirements_lock_path") != "visual_edition/requirements.lock.txt"
        or toolchain.get("qualification_state") != "qualified_for_all_non_latex_chapters"
        or toolchain.get("manimgl_allowed") is not False
        or toolchain.get("isolated_arm_native_environment_required") is not True
        or toolchain.get("broken_global_environment_allowed") is not False
    ):
        out.append("Manim toolchain boundary drifted")
    hosting = manim.get("hosting", {})
    if (
        hosting.get("canonical_binary_host") != "YouTube"
        or hosting.get("canonical_playlist_required") is not True
        or hosting.get("youtube_video_count_target") != 84
        or hosting.get("quarto_embed_only_after_published_current") is not True
        or hosting.get("action_time_authority_required") is not True
        or hosting.get("external_publication_authorized_now") is not False
    ):
        out.append("Manim YouTube hosting or action-time authority boundary drifted")
    repository_boundary = manim.get("repository_boundary", {})
    if (
        repository_boundary.get("rendered_video_binary_tracked_in_git") is not False
        or repository_boundary.get("rendered_video_binary_in_pages_artifact") is not False
        or repository_boundary.get("local_render_location_class") != "ignored_build_space"
    ):
        out.append("Manim repository and Pages binary boundary drifted")
    counts = manim.get("current_counts", {})
    expected_counts = {
        "toolchain_contracts": 1,
        "candidate_visual_grammars": 0,
        "ratified_visual_grammars": 1,
        "pilot_packets_present": 5,
        "pilot_packets_rendered_local": 5,
        "pilot_packets_validated": 5,
        "chapter_packets_validated": 84,
        "current_rendered_videos": 84,
        "youtube_videos_unlisted_preview": 12,
        "youtube_videos_published": 0,
        "current_quarto_preview_embeds": 12,
        "current_quarto_embeds": 0,
        "stale_videos": 0,
    }
    if counts != expected_counts:
        out.append("Manim visual-edition foundation or production counts drifted")
    visual_manifest = data["visual_edition_manifest"]
    visual_counts = visual_manifest.get("counts", {})
    if (
        manim.get("visual_manifest_path") != "visual_edition/manifest.json"
        or visual_manifest.get("canonical_chapter_count") != 84
        or visual_manifest.get("pilot_chapter_ids") != expected_pilots
        or visual_counts.get("packets_present") != counts.get("chapter_packets_validated")
        or visual_counts.get("ready_not_published") != counts.get("chapter_packets_validated")
        or visual_counts.get("planned") != 0
        or visual_counts.get("validated") != 0
        or visual_counts.get("current_rendered_videos") != counts.get("current_rendered_videos")
        or visual_counts.get("youtube_videos_published") != counts.get("youtube_videos_published")
        or visual_counts.get("current_quarto_embeds") != counts.get("current_quarto_embeds")
    ):
        out.append("Manim roadmap counts do not reconcile with the canonical visual-edition manifest")
    grammar = manim.get("visual_grammar", {})
    if grammar != {
        "contract_path": "visual_edition/visual_grammar.json",
        "state": "technical_visual_grammar_v1_ratified_pedagogical_acceptance_reopened",
        "ratification_requires_all_five_pilots_validated": True,
    }:
        out.append("Manim ratified visual-grammar boundary drifted")
    ratchet = manim.get("pedagogical_and_aesthetic_ratchet", {})
    if (
        ratchet.get("id") != "P7.3-F9"
        or ratchet.get("state") != "active_repository_tracked_v2_production"
        or ratchet.get("skill_path") != "skills/asi-stack-manim-videos/SKILL.md"
        or ratchet.get("beat_plan_schema_version") != "asi_stack.manim_beat_plan.v2"
        or ratchet.get("beat_plan_schema_path") != "schemas/manim_beat_plan.schema.json"
        or ratchet.get("experience_review_schema_path") != "schemas/manim_experience_review.schema.json"
        or ratchet.get("production_ledger_path") != "visual_edition/manim_v2_production_ledger.json"
        or ratchet.get("production_ledger_schema_path") != "schemas/manim_v2_production_ledger.schema.json"
        or ratchet.get("production_validator_path") != "scripts/validate_manim_v2_production_ledger.py"
        or ratchet.get("target_generation") != 2
        or ratchet.get("minimum_score_each_dimension") != 4
        or ratchet.get("averaging_may_hide_failure") is not False
        or ratchet.get("external_human_prepublication_gate_required") is not False
        or ratchet.get("beat_density_and_technique_counts_are_diagnostic_only") is not True
        or ratchet.get("mechanical_diagnostic_is_aesthetic_verdict") is not False
    ):
        out.append("Manim pedagogical and aesthetic ratchet drifted")
    v2_ledger = data["manim_v2_ledger"]
    v2_entries = v2_ledger.get("entries", [])
    v2_revision_count = sum(
        row.get("target", {}).get("stage") == "animatic"
        and row.get("target", {}).get("gates", {}).get("animatic") == "revise"
        for row in v2_entries
    )
    expected_v2_counts = {
        "planned": v2_ledger.get("counts", {}).get("planned"),
        "animatic_revision": v2_revision_count,
        "animatic_passed": v2_ledger.get("counts", {}).get("animatic_passed"),
        "picture_and_sound_lock_passed": v2_ledger.get("counts", {}).get("picture_and_sound_lock_passed"),
        "release_candidate_passed": v2_ledger.get("counts", {}).get("release_candidate_passed"),
        "accepted": v2_ledger.get("counts", {}).get("accepted_generation_2"),
        "youtube_current": v2_ledger.get("counts", {}).get("youtube_generation_2_current"),
        "quarto_current": v2_ledger.get("counts", {}).get("quarto_generation_2_current"),
    }
    if ratchet.get("generation_2_counts") != expected_v2_counts:
        out.append("Manim generation-2 roadmap counts drifted from the canonical production ledger")
    first_replacement = ratchet.get("first_replacement", {})
    first_target = v2_entries[0].get("target", {}) if v2_entries else {}
    if (
        first_replacement.get("chapter_id") != "asi-is-a-stack-not-a-model"
        or first_replacement.get("stage") != first_target.get("stage")
        or first_replacement.get("gate_state") != first_target.get("gates", {}).get("animatic")
        or first_replacement.get("current_review_path") != first_target.get("experience_review_paths", {}).get("animatic")
        or not isinstance(first_replacement.get("current_candidate_review_state"), str)
        or not first_replacement.get("current_candidate_review_state")
        or first_replacement.get("support_state_effect") != "none"
        or first_replacement.get("publication_effect") != "none"
    ):
        out.append("Manim first generation-2 replacement checkpoint drifted or overclaimed")
    first_pilot = manim.get("first_pilot_checkpoint", {})
    if first_pilot != {
        "chapter_id": "asi-is-a-stack-not-a-model",
        "packet_path": "visual_edition/chapters/asi-is-a-stack-not-a-model/packet.json",
        "lifecycle_state": "ready_not_published",
        "draft_duration_seconds": 284.99707,
        "draft_dimensions": "854x480",
        "draft_frame_rate": 15,
        "visual_review_sample_count": 8,
        "release_visual_render_present": True,
        "release_visual_duration_seconds": 284.999023,
        "release_visual_dimensions": "1920x1080",
        "release_visual_frame_rate": 30,
        "release_visual_review_sample_count": 2,
        "local_timing_audio_publication_rights_cleared": False,
        "remaining_release_gates": [
            "exact_action_time_youtube_authority",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
    }:
        out.append("Manim first-pilot checkpoint drifted or overclaimed")
    if manim.get("five_pilot_checkpoint") != {
        "state": "all_five_final_av_masters_validated",
        "packet_count": 5,
        "rendered_lifecycle_count": 5,
        "validated_final_av_count": 5,
        "rights_cleared_narration_count": 5,
        "release_visual_review_count": 5,
        "visual_grammar_state": "ratified",
        "remaining_release_gates": [
            "exact_action_time_youtube_authority",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
    }:
        out.append("Manim five-pilot release-visual checkpoint drifted or overclaimed")
    if manim.get("all_chapter_checkpoint") != {
        "state": "all_84_ready_not_published",
        "publication_preflight_path": "visual_edition/youtube_publication_preflight.json",
        "mutation_scope_path": "visual_edition/youtube_mutation_scope.json",
        "mutation_scope_sha256": "3f901ca06169b3df555b6e8dbc6a327c6dab9e623b6712407cf0a9366eeb55f0",
        "mutation_scope_requires_exact_action_time_authorization": True,
        "platform_receipt_schema_path": "schemas/youtube_platform_receipt.schema.json",
        "platform_receipt_recorder_path": "scripts/record_youtube_platform_receipt.py",
        "publication_reconciler_path": "scripts/reconcile_youtube_publication_receipts.py",
        "supersession_plan_schema_path": "schemas/youtube_supersession_plan.schema.json",
        "supersession_lifecycle_helper_path": "scripts/visual_publication_lifecycle.py",
        "supersession_preparer_path": "scripts/prepare_youtube_supersession.py",
        "supersession_receipt_recorder_path": "scripts/record_youtube_supersession_receipt.py",
        "supersession_reconciler_path": "scripts/reconcile_youtube_supersession_receipt.py",
        "supersession_validator_path": "scripts/validate_youtube_supersession_workflow.py",
        "generation_history_derived_from_immutable_receipts": True,
        "supersession_negative_mutations_rejected": 12,
        "current_supersession_plan_count": 0,
        "real_generation_two_exercise_state": "awaiting_generation_one_publication_and_author_feedback",
        "canonical_chapter_digest_excludes_managed_visual_block": True,
        "repository_reconciliation_rollback_complete": True,
        "published_receipt_set_all_or_nothing": True,
        "publication_input_triples_ready": 84,
        "studio_browser_batch_count": 6,
        "data_api_default_minimum_quota_days": 5,
        "packet_count": 84,
        "validated_final_av_count": 84,
        "reviewed_caption_count": 84,
        "descriptive_transcript_count": 84,
        "reviewed_thumbnail_count": 84,
        "scene_midpoint_review_frame_count": 588,
        "scene_midpoint_review_sheet_count": 21,
        "content_word_error_rate_minimum": 0.0,
        "content_word_error_rate_maximum": 0.028658,
        "maximum_contiguous_expected_token_gap": 4,
        "duration_seconds_minimum": 227.765,
        "duration_seconds_maximum": 331.005,
        "local_final_master_bytes": 1015153522,
        "youtube_platform_object_count": 0,
        "current_quarto_embed_count": 0,
        "remaining_release_gates": [
            "exact_action_time_youtube_authority",
            "youtube_playlist_upload_metadata_caption_thumbnail_processing_publication_receipts",
            "quarto_embed_and_public_crawl_reconciliation",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
    }:
        out.append("Manim all-chapter ready-not-published checkpoint drifted or overclaimed")
    if manim.get("support_state_effect") != "none":
        out.append("Manim visual edition moves claim support")
    expected_first_tranche_order = [
        "white-box-evidence-interpretability-and-activation-governance",
        "governed-world-models-and-reality-grounding",
        "human-factors-and-meaningful-control-in-oversight",
        "governed-operations-incident-command-and-graceful-degradation",
    ]
    if execution_readiness.get("first_tranche_completion_order") != expected_first_tranche_order:
        out.append("execution board first-tranche completion order drifted")
    batched_second_ids = [
        item
        for batch in execution_readiness.get("second_tranche_adjudication_batches", [])
        for item in batch
    ]
    if batched_second_ids != status["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"]["candidate_ids"][:1] + [
        "privacy-data-rights-and-information-flow-governance",
        "governed-objective-formation-value-learning-and-goal-integrity",
        "perception-sensor-fusion-and-observation-trust",
        "embodied-agency-real-time-control-and-physical-safety",
        "human-ai-organizations-delegation-and-accountability",
        "human-ai-communication-persuasion-and-epistemic-security",
        "institutions-international-coordination-and-public-legitimacy",
        "ai-deployment-transition-distribution-and-human-agency",
        "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
        "autonomous-replication-proliferation-and-containment",
        "physical-compute-infrastructure-energy-and-environmental-constraints",
        "scientific-discovery-and-experimental-governance",
    ]:
        out.append("execution board second-tranche dependency batches drifted")
    if len(batched_second_ids) != 13 or len(set(batched_second_ids)) != 13:
        out.append("execution board does not disposition every second-tranche candidate exactly once")
    if execution_readiness.get("repository_authority_map") != "docs/repository_map.md":
        out.append("execution board lost the repository authority map")
    if execution_readiness.get("support_state_effect") != "none" or execution_readiness.get("release_effect") != "none":
        out.append("execution board laundered support or release state")
    critical_path = quality_program.get("critical_path", [])
    if quality_program.get("shared_flagship_id") != "ASI-THESEUS-FLAGSHIP-01":
        out.append("shared quality flagship identity drifted")
    if [row.get("id") for row in critical_path] != ["T0", "T0A", "T1", "T2", "T3", "T4", "T5", "T6"]:
        out.append("shared quality critical path must preserve historical T0, successor T0A, then T1 through T6")
    t0a_currentness = quality_program.get("t0a_currentness", {})
    expected_t0a_currentness = {
        "source_commit": "264a31ee288fc288727c45a1166b4dbe36180b6b",
        "source_branch": "main",
        "published_on_origin_main": True,
        "historical_freeze": {
            "source_commit": "2bd2f0b1f240b826c1606556313926084e9f3592",
            "package_identity": "sha256:0b83c4b55616679d636df84ec14dea5825e79357b228fe441f399241acc9ae9c",
            "artifact_count": 143,
            "architecture_contract_count": 15,
            "accelerator_replay_receipt_count": 14,
            "cpu_replay_pass_count": 7,
            "trigger_state": "GREEN",
            "disposition": "architecture_frozen_training_not_started",
        },
        "t1_lineage": {
            "state": "active_step_9048_prospectively_anchored_not_evaluated",
            "optimizer_steps": 9048,
            "optimizer_positions": 69310840,
            "target_pretrain_optimizer_positions": 1096734920,
            "checkpoint_sha256": "ed28acc8cc9a82b4bd00dbd8487f17b8131157df3c828f66eb458902d4e3c16d",
            "optimizer_state_sha256": "7b19ceb6880954a845bdb79914d84a6d388992abe45e98d63dfdfa3a2ed6c829",
            "mlx_rng_state_sha256": "9209383f5b4eb599c89462f922957b13e60f03eb6fac3b73f6af9003c023850f",
            "receipt_sha256": "e46683967238fd79c328bd7465bf7030e30bb5127f0afee7b02fbf936b0fed06",
            "current_plan_sha256": "38951e6bc9605b86c0e0c793b37eef7ae5c6b3d5ea89f7aef4180f1b40aaa60d",
            "full_segment_predecessor_chain_available": False,
            "t0a_payload_still_materialized_at_frozen_identity": False,
            "prospective_append_only_lineage_trigger_state": "GREEN",
            "prospective_ledger_manifest_count": 0,
        },
        "currentness_gate": {
            "pre_training_architecture_ready": True,
            "pre_training_architecture_blocker_count": 0,
            "historical_source_drift_count": 12,
            "historical_source_drift_accepted_only_after_activation": True,
            "project_registry_trigger_state": "GREEN",
            "aibom_missing_identity_count": 0,
        },
        "evaluation_boundary": {
            "private_development_freeze": "configs/neural_seed_architecture_review_freeze_v5.json",
            "confirmation_surface_consumed": False,
            "public_surface_consumed": False,
            "capability_claim": "NOT_EVALUATED",
            "t2_numerator_opened": False,
        },
        "next_legal_action": "continue only the frozen T1 shared-trunk campaign through the append-only lineage controller when its exact resource and process-inventory gates pass; preserve evaluator non-consumption until its preregistered review boundary",
        "protected_outcomes_opened": 0,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    if t0a_currentness != expected_t0a_currentness:
        out.append("T0A-to-T1 currentness custody record drifted from the published prospective-anchor state")
    if quality_program.get("support_state_effect") != "none" or quality_program.get("release_effect") != "none":
        out.append("quality roadmap laundered support or release state")
    empirical_lanes = quality_program.get("empirical_lanes", {})
    q1 = empirical_lanes.get("q1_governed_admission", {})
    q2 = empirical_lanes.get("q2_theseus_student", {})
    if q1.get("denominator_id") == q2.get("denominator_id"):
        out.append("Q1 and Q2 share a denominator identity")
    if q1.get("denominator_id") != "P2-Q1-D1" or q2.get("denominator_id") != "ASI-THESEUS-Q2-D2":
        out.append("Q1/Q2 denominator identity drifted")
    if q1.get("may_open_before_T2") is not True or q1.get("depends_on") != ["P2-seven-gate-competence"]:
        out.append("Q1 is incorrectly blocked by Theseus student gates")
    if q2.get("depends_on") != ["T2", "T4"]:
        out.append("Q2 lost its student or joined-path dependency")
    if any(
        empirical_lanes.get(field) is not False
        for field in ["denominator_overlap_allowed", "q1_outcomes_may_tune_q2_or_student", "support_transfer_allowed"]
    ):
        out.append("Q1/Q2 isolation or support boundary weakened")
    narrative_gate = quality_program.get("narrative_quality_gate", {})
    if narrative_gate.get("case_independent_compression_state") != "first_tranche_and_a1_a2_historical_receipts_terminal_round16_integration_debt_active":
        out.append("narrative gate does not preserve historical receipts while routing current integration debt")
    if narrative_gate.get("flagship_threading_state") != "blocked_by_T4":
        out.append("flagship-dependent P7.1b work lost its T4 gate")
    if not all(
        narrative_gate.get(field) is True
        for field in [
            "requires_chapter_role_classification",
            "requires_shared_case_threading",
            "requires_strongest_alternative_and_simpler_baseline",
            "requires_meaning_preservation_audit",
        ]
    ):
        out.append("narrative quality gate lost a required meaning-preservation control")
    convergence = quality_program.get("post_review_convergence", {})
    expected_convergence_order = [
        "C0-canonical-public-truth-incident-and-regression",
        "C1-noninheritance-thesis-and-terminology-convergence",
        "C2-twenty-two-unit-narrative-book",
        "C3-governed-transition-calculus",
        "C4-developmental-intelligence-loop",
        "C5-minimal-trusted-kernel-and-bounded-liveness",
        "C6-p0-p6-semantic-proof-rationalization",
        "C7-natural-governed-repository-change-flagship",
        "C8-evidence-led-publication-and-derivative-papers",
    ]
    if (
        convergence.get("state") != "phase2_active_after_concept_first_reconciliation"
        or convergence.get("active_work_mode")
        != "phase2_smallest_consumed_conclusions_and_natural_evidence"
        or convergence.get("current_priority")
        != "phase2_proof_rationalization_then_natural_flagship"
        or convergence.get("proof_work_priority")
        != "current_only_for_named_consumers_after_phase1_exit"
        or convergence.get("concept_first_exit_gate") != "all_84_distinct_responsibilities_reader_visible_and_roadmap_only_idea_audit_reconciled"
        or convergence.get("concept_first_exit_gate_state")
        != "passed_84_responsibilities_62_specialist_routes_26_c1_c8_anchors_zero_roadmap_only_remainder"
        or convergence.get("phase1_audit_path") != "docs/c1_c8_phase1_idea_placement_and_prose_audit_2026_07_25.md"
        or convergence.get("narrative_spine_path") != "products/narrative_product_spine.json"
        or convergence.get("narrative_unit_crosswalk_path") != "products/narrative_unit_crosswalk.json"
        or convergence.get("all_84_idea_placement_gate_state") != "passed_exact_84_coverage_22_unit_meaning_render_browser_and_accessibility_preparation"
        or convergence.get("phase2_proof_execution_allowed") is not True
        or convergence.get("reference_chapter_count") != 84
        or convergence.get("narrative_unit_target") != 22
        or convergence.get("defended_contribution_count") != 3
        or convergence.get("packet_order") != expected_convergence_order
        or convergence.get("flagship_id") != "ASI-THESEUS-FLAGSHIP-01"
    ):
        out.append("post-review convergence identity, denominator, or packet order drifted")
    concept_audit = convergence.get("concept_first_idea_audit", {})
    concept_packets = concept_audit.get("packets", [])
    actual_concept_anchors = [
        (
            packet.get("packet_id"),
            anchor.get("anchor_id"),
            anchor.get("owner_path"),
            anchor.get("required_phrase"),
        )
        for packet in concept_packets
        for anchor in packet.get("anchors", [])
    ]
    if (
        concept_audit.get("state") != "reconciled_exact_eight_packet_anchor_set"
        or concept_audit.get("packet_count") != 8
        or concept_audit.get("exact_anchor_count") != len(EXPECTED_CONCEPT_ANCHORS)
        or concept_audit.get("roadmap_only_idea_count") != 0
        or concept_audit.get("all_structural_candidate_queues_empty") is not True
        or concept_audit.get("support_state_effect") != "none"
        or [packet.get("packet_id") for packet in concept_packets]
        != [f"C{index}" for index in range(1, 9)]
        or any(
            packet.get("disposition") != "placed_in_existing_owners"
            for packet in concept_packets
        )
        or actual_concept_anchors != EXPECTED_CONCEPT_ANCHORS
        or len({anchor[1] for anchor in actual_concept_anchors})
        != len(actual_concept_anchors)
    ):
        out.append("concept-first C1-C8 anchor audit identity or zero-remainder disposition drifted")
    for _, anchor_id, owner_path, required_phrase in EXPECTED_CONCEPT_ANCHORS:
        path = ROOT / owner_path
        if not path.is_file():
            out.append(f"concept-first anchor owner missing: {anchor_id} -> {owner_path}")
            continue
        normalized_owner = re.sub(
            r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")
        )
        if required_phrase not in normalized_owner:
            out.append(f"concept-first prose anchor missing: {anchor_id} -> {owner_path}")
    phase1_audit_text = (ROOT / convergence.get("phase1_audit_path", "")).read_text(
        encoding="utf-8", errors="ignore"
    )
    for phrase in [
        "## Exact C1–C8 roadmap-only idea reconciliation",
        "26 exact prose or product anchors",
        "Roadmap-only remainder | `0`",
        "all current structural candidate queues are empty",
    ]:
        if phrase not in phase1_audit_text:
            out.append(f"concept-first readable audit missing: {phrase}")
    c6_overlay_status = convergence.get("c6_current_semantic_overlay", {})
    c6_overlay = data["proof_semantic_depth_overlay"]
    expected_c6_levels = {
        "P0": 25,
        "P1": 881,
        "P2": 174,
        "P3": 751,
        "P4": 105,
        "P5": 116,
        "P6": 0,
    }
    expected_c6_dispositions = {
        "retain": 2052,
    }
    if (
        c6_overlay_status.get("state")
        != "dependency_safe_execution_complete_after_one_hundred_fifty_seven_retirements_two_scope_rewrites_and_one_inverse_route_replacement"
        or c6_overlay_status.get("classification_baseline_commit")
        != "d0f9bda14f1253999f2c40d556d925d31e4b36a4"
        or c6_overlay_status.get("classification_baseline_theorem_count") != 1370
        or c6_overlay_status.get("overlay_path")
        != "proofs/proof_semantic_depth_overlay.json"
        or c6_overlay_status.get("report_path")
        != "docs/proof_semantic_depth_overlay.md"
        or c6_overlay_status.get("rationalization_ledger_path")
        != "proofs/proof_semantic_rationalization_ledger.json"
        or c6_overlay_status.get("theorem_count") != 2052
        or c6_overlay_status.get("theorem_bearing_module_count") != 130
        or c6_overlay_status.get("semantic_owner_chapter_count") != 84
        or c6_overlay_status.get("semantic_level_counts") != expected_c6_levels
        or c6_overlay_status.get("disposition_counts")
        != expected_c6_dispositions
        or c6_overlay_status.get("executed_retirement_count") != 157
        or c6_overlay_status.get("executed_scope_rewrite_count") != 2
        or c6_overlay_status.get("remaining_action_count") != 0
        or c6_overlay_status.get("mutation_coverage_missing_count") != 0
        or c6_overlay_status.get("frozen_historical_theorem_count") != 1151
        or c6_overlay_status.get("frozen_historical_target_count") != 298
        or c6_overlay_status.get("next_action")
        != "preserve_terminal_semantic_custody_and_reopen_only_for_a_dated_consumer_owned_semantic_defect"
        or c6_overlay_status.get("support_state_effect") != "none"
    ):
        out.append("C6 current semantic-overlay status drifted")
    c6_summary = c6_overlay.get("summary", {})
    if (
        c6_summary.get("current_theorem_count") != 2052
        or c6_summary.get("current_module_count") != 130
        or c6_summary.get("semantic_owner_chapter_count") != 84
        or c6_summary.get("semantic_level_counts") != expected_c6_levels
        or c6_summary.get("disposition_counts") != expected_c6_dispositions
        or any(not row.get("mutation_refs") for row in c6_overlay.get("records", []))
        or c6_summary.get("support_state_effect") != "none"
    ):
        out.append("C6 status no longer matches the generated semantic-depth overlay")
    c6_ledger = data["proof_semantic_rationalization_ledger"]
    if (
        c6_ledger.get("state") != "dependency_safe_execution_complete"
        or c6_ledger.get("classification_baseline", {}).get("live_theorem_count") != 1370
        or c6_ledger.get("summary", {}).get("executed_retirement_count") != 157
        or c6_ledger.get("summary", {}).get("executed_scope_rewrite_count") != 2
        or c6_ledger.get("summary", {}).get("current_live_theorem_count") != 1219
        or c6_ledger.get("summary", {}).get("remaining_action_count") != 0
        or c6_ledger.get("support_state_effect") != "none"
        or c6_ledger.get("release_effect") != "none"
    ):
        out.append("C6 semantic-rationalization transaction ledger drifted")
    for required_phrase in [
        "### C6 current-estate classification and cumulative execution receipt — 2026-07-26",
        "1,370\nbaseline declarations",
        "all 1,219 live theorem",
        "zero P6 empirically bound results",
        "1,219 retain",
        "Search Substrates theorems negate different predicates",
        "zero stronger-model actions remain",
        "first narrow-projection tranche",
        "second narrow-projection tranche",
        "third narrow-projection tranche",
        "fourth narrow-projection tranche",
        "fifth narrow-projection tranche",
        "sixth narrow-projection tranche",
        "eighth narrow-projection tranche",
        "ninth narrow-projection tranche",
        "tenth narrow-projection tranche",
        "eleventh narrow-projection tranche",
        "twelfth narrow-projection tranche",
        "thirteenth narrow-projection tranche",
        "fourteenth scope-and-refinement tranche",
        "fifteenth route-economy consolidation tranche",
        "sixteenth evidence-transition consolidation tranche",
        "Zero stronger-model actions remain",
        "`proofs/proof_semantic_rationalization_ledger.json`",
    ]:
        if required_phrase not in data["roadmap"]:
            out.append(f"C6 roadmap receipt lost required phrase: {required_phrase}")
    if (
        len(convergence.get("governed_transition_calculus_properties", [])) != 12
        or convergence.get("proof_depth_levels")
        != [
            "P0-record-shape",
            "P1-finite-route",
            "P2-reachability-and-nonvacuity",
            "P3-implementation-refinement",
            "P4-cross-component-safety",
            "P5-liveness-and-recovery",
            "P6-empirically-bound-semantics",
        ]
        or len(convergence.get("developmental_loop_stages", [])) != 11
        or len(convergence.get("minimal_trusted_kernel_components", [])) != 11
        or len(convergence.get("new_chapter_requires", [])) != 6
    ):
        out.append("post-review calculus, proof, developmental, kernel, or chapter-admission contract drifted")
    if (
        convergence.get("bounded_liveness_required") is not True
        or convergence.get("existing_owner_first") is not True
        or convergence.get("worthwhile_manuscript_idea_deferral_allowed") is not False
        or convergence.get("prepublication_external_human_required") is not False
        or convergence.get("support_state_effect") != "none"
        or convergence.get("release_effect") != "none"
    ):
        out.append("post-review liveness, no-deferral, human-review, support, or release boundary drifted")
    for heading in [
        "### C0 — Canonical public-truth incident and regression",
        "### C1 — Noninheritance thesis and terminology convergence",
        "### C2 — Twenty-two-unit narrative book over the 84-module reference",
        "### C3 — Governed Transition Calculus",
        "### C4 — Developmental Intelligence Loop",
        "### C5 — Minimal trusted kernel and bounded liveness",
        "### C6 — P0–P6 semantic proof rationalization",
        "### C7 — Natural governed repository-change flagship",
        "### C8 — Evidence-led publication and derivative papers",
    ]:
        if heading not in roadmap:
            out.append(f"post-review roadmap packet missing: {heading}")
    review_adjudication = data["review_adjudication"]
    for required_review_phrase in [
        "The controlling architectural law is **noninheritance**",
        "The existing three-contribution contract remains the right organizing surface",
        "Prepublication specialist human review should be required.",
        "**Rejected as a gate by author instruction.**",
    ]:
        if required_review_phrase not in review_adjudication:
            out.append(f"review adjudication boundary missing: {required_review_phrase}")
    role_map = data["current_role_map"]
    role_assignments = [
        chapter_id
        for role_chapters in role_map.get("roles", {}).values()
        for chapter_id in role_chapters
    ]
    role_counts = Counter(role_assignments)
    role_summary = role_map.get("summary", {})
    if (
        role_map.get("manifest_chapter_count") != 84
        or set(role_assignments) != manifest_ids
        or len(role_assignments) != 84
        or any(count != 1 for count in role_counts.values())
        or role_summary.get("thesis_bearing_count") != 11
        or role_summary.get("load_bearing_reference_count") != 54
        or role_summary.get("implementation_case_count") != 7
        or role_summary.get("speculative_research_count") != 12
        or role_summary.get("total_count") != 84
        or role_summary.get("unassigned_count") != 0
        or role_summary.get("duplicate_assignment_count") != 0
    ):
        out.append("current 84-chapter role map is incomplete, duplicated, or count-inconsistent")
    first_tranche = quality_program.get("structural_completeness_tranche", {}).get("first_tranche", {})
    if first_tranche.get("state") != "terminal_four_reader_chapters":
        out.append("first structural tranche terminal state drifted")
    if first_tranche.get("completed_reader_chapter_count") != 4:
        out.append("first structural tranche completion count drifted")
    if first_tranche.get("terminal_reader_chapter_ids") != expected_first_tranche_order:
        out.append("T1/T2/T3/T4 terminal reader custody drifted")
    if first_tranche.get("remaining_reader_chapter_ids") != []:
        out.append("terminal first structural tranche retains a residual chapter")
    second_tranche = quality_program.get("structural_completeness_tranche", {}).get("second_tranche", {})
    if second_tranche.get("active_candidate_id") is not None:
        out.append("a second-tranche candidate is active during the post-breadth freeze")
    if second_tranche.get("next_queued_candidate_id") is not None:
        out.append("post-breadth freeze retains an unauthorized chapter queue")
    if second_tranche.get("admission_state") != "all_distinct_owners_admitted_no_live_candidate_queue":
        out.append("second-tranche admission state does not preserve terminal no-queue admission")
    round18 = quality_program.get("structural_completeness_tranche", {}).get("round_18_breadth_completion", {})
    expected_round18_chapters = [
        "perception-sensor-fusion-and-observation-trust",
        "embodied-agency-real-time-control-and-physical-safety",
        "human-ai-organizations-delegation-and-accountability",
        "multi-agent-dynamics-collective-intelligence-and-systemic-risk",
        "inner-alignment-mesa-optimization-and-learned-objective-integrity",
    ]
    if round18.get("state") != "terminal_argument_integration_post_transaction_freeze":
        out.append("Round 18 breadth transaction is not terminal at argument support")
    if round18.get("new_chapter_ids") != expected_round18_chapters:
        out.append("Round 18 new-chapter identity set drifted")
    if not set(expected_round18_chapters).issubset(manifest_ids):
        out.append("Round 18 manifest chapters are incomplete")
    if round18.get("new_external_source_record_count") != 21 or round18.get("birth_claim_atom_count") != 5:
        out.append("Round 18 source or birth-atom count drifted")
    if round18.get("post_transaction_structural_freeze") is not True:
        out.append("Round 18 does not restore the structural freeze")
    for path_field in ["adjudication_path", "research_backlog_path", "triage_path", "claim_atom_path", "reader_projection_path", "inheritance_audit_path"]:
        path_value = round18.get(path_field)
        if not isinstance(path_value, str) or not (ROOT / path_value).exists():
            out.append(f"Round 18 artifact missing: {path_field}")

    round16 = status.get("round_16_evidence_first_amendment", {})
    expected_round16_chapters = expected_first_tranche_order + [
        "governed-model-training-distributed-optimization-and-scaling",
        "privacy-data-rights-and-information-flow-governance",
    ]
    if round16.get("structural_admission_freeze") is not False:
        out.append("Round 16 amendment was not superseded by the no-deferral manuscript policy")
    if round16.get("post_activation_atom_pack", {}).get("chapter_ids") != expected_round16_chapters:
        out.append("Round 16 six-chapter atom-pack scope drifted")
    atom_pack = round16.get("post_activation_atom_pack", {})
    if atom_pack.get("state") != "terminal_six_of_six_reviewed_append_only_pack":
        out.append("R16-A six-chapter atom pack is not terminal")
    if not all(
        atom_pack.get(field) is True
        for field in [
            "historical_3730_activation_atom_denominator_is_immutable",
            "historical_15_atom_addendum_is_immutable",
        ]
    ):
        out.append("Round 16 amendment permits rewriting a historical atom denominator")
    required_r16a_paths = {
        "addendum_path": "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
        "schema_path": "schemas/post_activation_six_chapter_claim_atom_addendum.schema.json",
        "builder_path": "scripts/build_post_activation_six_chapter_claim_atom_addendum.py",
        "validator_path": "scripts/validate_post_activation_six_chapter_claim_atom_addendum.py",
    }
    for field, relative in required_r16a_paths.items():
        if atom_pack.get(field) != relative or not (ROOT / relative).exists():
            out.append(f"R16-A artifact route missing or drifted: {field}")
    if (
        atom_pack.get("chapter_review_count") != 6
        or atom_pack.get("atom_count") != 30
        or atom_pack.get("identity_graph_canonical_atom_count") != 4112
        or atom_pack.get("appendix_c_projection_complete") is not True
        or atom_pack.get("mutation_rejection_count") != 14
    ):
        out.append("R16-A terminal receipt denominator or projection drifted")
    r16a = data.get("post_activation_six_chapter_addendum", {})
    if (
        r16a.get("chapter_count") != 6
        or r16a.get("atom_count") != 30
        or r16a.get("support_state_effect") != "none"
        or r16a.get("summary", {}).get("promoted_atom_count") != 0
    ):
        out.append("R16-A machine addendum is incomplete or promotional")
    reader_freshness = round16.get("current_reader_freshness_packet", {})
    if reader_freshness.get("current_working_manifest_chapter_count") != 84 or reader_freshness.get("must_cover_all_current_manifest_chapters") is not True:
        out.append("Round 16 current-reader packet does not cover the live 84-chapter manifest")
    expected_reader_receipt = {
        "state": "terminal_local_source_freshness_formats_deferred",
        "source_content_commit": "56563e1b2b64405e2e944c521bf4df9f29eba6e6",
        "artifact_path": "editions/reader_manuscript/reader_2026_07_26/manifest.json",
        "report_path": "editions/reader_manuscript/reader_2026_07_26/freshness_report.md",
        "schema_path": "schemas/r16_b_current_reader_freshness.schema.json",
        "builder_path": "scripts/build_r16_b_current_reader_freshness.py",
        "validator_path": "scripts/validate_r16_b_current_reader_freshness.py",
        "chapter_projection_count": 84,
        "narrative_unit_count": 22,
        "reader_surface_count": 8,
        "mutation_rejection_count": 16,
        "virtual_qmd_terminal": True,
        "unreviewed_format_count_deferred": 5,
        "source_duplication_avoided": True,
        "support_state_effect": "none",
        "release_effect": "none",
        "publication_effect": "none",
    }
    for field, expected in expected_reader_receipt.items():
        if reader_freshness.get(field) != expected:
            out.append(f"R16-B terminal receipt drifted: {field}")
    for field in ("artifact_path", "report_path", "schema_path", "builder_path", "validator_path"):
        path = reader_freshness.get(field)
        if not isinstance(path, str) or not (ROOT / path).is_file():
            out.append(f"R16-B terminal artifact missing: {field}")
    recovery = round16.get("p2_empirical_recovery", {})
    if (
        recovery.get("state") != "latest_exact_preflight_failed_capacity_and_docker_restore_both_before_retry"
        or recovery.get("observed_host_free_bytes_2026_07_22") != 71648034816
        or recovery.get("docker_daemon_available_2026_07_22") is not True
        or recovery.get("docker_storage_zero_2026_07_22") is not True
        or recovery.get("observed_host_available_1k_blocks_2026_07_24") != 22337556
        or recovery.get("observed_host_available_bytes_2026_07_24") != 22873657344
        or recovery.get("docker_inspection_state_2026_07_24") != "permission_denied_local_socket"
        or recovery.get("latest_preflight_attempt_id") != "2026-07-28-r3a-003"
        or recovery.get("latest_preflight_source_commit") != "cef11abd5fca0a421087b3123c1defb31f2b4e6d"
        or recovery.get("observed_host_available_bytes_2026_07_27") != 25627230208
        or recovery.get("observed_host_shortfall_bytes_2026_07_27") != 28059860992
        or recovery.get("docker_daemon_available_2026_07_27") is not False
        or recovery.get("observed_host_available_bytes_2026_07_28") != 4690223104
        or recovery.get("observed_host_shortfall_bytes_2026_07_28") != 48996868096
        or recovery.get("docker_daemon_available_2026_07_28") is not False
    ):
        out.append("P2 historical or current capacity truth drifted")
    for field in ("latest_preflight_receipt_path", "latest_preflight_human_receipt_path"):
        relative = recovery.get(field)
        if not isinstance(relative, str) or not (ROOT / relative).is_file():
            out.append(f"P2 latest preflight artifact missing: {field}")
    template_guard = round16.get("template_inheritance_guard", {})
    if template_guard.get("provisional_current_61_chapter_repeated_12_gram_count") != 738 or template_guard.get("provisional_current_61_chapter_maximum_spread") != 55:
        out.append("Round 17 provisional W3 diagnostic drifted")
    if (
        template_guard.get("state") != "terminal_current_84_chapter_inheritance_guard"
        or template_guard.get("current_live_chapter_scope") != 84
        or template_guard.get("requires_reproducible_current_baseline") is not False
        or template_guard.get("baseline_editorial_repeated_12_gram_count") != 812
        or template_guard.get("current_editorial_repeated_12_gram_count") != 0
        or template_guard.get("baseline_editorial_maximum_spread") != 14
        or template_guard.get("current_editorial_maximum_spread") != 0
        or template_guard.get("baseline_copied_diagram_and_test_spread") != 10
        or template_guard.get("current_copied_diagram_and_test_spread") != 0
        or template_guard.get("repaired_chapter_count") != 10
        or template_guard.get("baseline_prose_candidate_count") != 3444
        or template_guard.get("current_prose_candidate_count") != 3864
        or template_guard.get("retired_inherited_prose_candidate_count") != 252
        or template_guard.get("added_domain_specific_prose_candidate_count") != 672
        or template_guard.get("baseline_structured_atom_count") != 4067
        or template_guard.get("current_structured_atom_count") != 4059
        or template_guard.get("pending_prose_candidate_count") != 0
        or template_guard.get("affected_semantic_review_chapter_count") != 11
        or template_guard.get("copied_scaffold_fixture_rejected") is not True
        or template_guard.get("distinct_chapter_fixture_accepted") is not True
        or template_guard.get("mutation_rejection_count") != 18
        or template_guard.get("meaning_custody_deletion_count") != 0
        or template_guard.get("support_state_effect") != "none"
        or template_guard.get("release_effect") != "none"
    ):
        out.append("W3 terminal current-84 inheritance receipt drifted")
    for field, relative in {
        "artifact_path": "evidence_quality/p7_1a_w3_inheritance_guard.json",
        "report_path": "docs/p7_1a_w3_inheritance_guard.md",
        "schema_path": "schemas/p7_1a_w3_inheritance_guard.schema.json",
        "builder_path": "scripts/build_p7_1a_w3_inheritance_guard.py",
        "validator_path": "scripts/validate_p7_1a_w3_inheritance_guard.py",
    }.items():
        if template_guard.get(field) != relative or not (ROOT / relative).exists():
            out.append(f"W3 terminal artifact path drifted: {field}")
    w3 = data.get("p7_1a_w3_inheritance_guard", {})
    if (
        w3.get("state") != "terminal_complete"
        or w3.get("corpus", {}).get("manifest_chapter_count") != 84
        or w3.get("measurements", {}).get("editorial_narrative", {}).get("baseline", {}).get("distinct_repeated_12_grams") != 812
        or w3.get("measurements", {}).get("editorial_narrative", {}).get("current", {}).get("distinct_repeated_12_grams") != 0
        or w3.get("claim_review_reconciliation", {}).get("retired_inherited_prose_candidate_count") != 252
        or w3.get("claim_review_reconciliation", {}).get("added_domain_specific_prose_candidate_count") != 672
        or w3.get("claim_review_reconciliation", {}).get("current_pending_prose_candidate_count") != 0
        or w3.get("meaning_custody", {}).get("chapter_core_support_movements") != 0
    ):
        out.append("W3 machine artifact is incomplete or promotional")
    optimizer_amendment = round16.get("optimizer_landscape_depth_amendment", {})
    if optimizer_amendment.get("chapter_id") != "governed-model-training-distributed-optimization-and-scaling":
        out.append("optimizer landscape lost its existing governed-training owner")
    if optimizer_amendment.get("new_chapter_allowed") is not False:
        out.append("optimizer landscape permits a duplicate chapter owner")
    if optimizer_amendment.get("optimizer_is_coupled_run_policy") is not True:
        out.append("optimizer landscape lost coupled run-policy identity")
    if optimizer_amendment.get("matched_tuning_budget_required") is not True:
        out.append("optimizer landscape permits unmatched tuning budgets")
    if optimizer_amendment.get("method_specific_rescue_required_before_negative_inference") is not True:
        out.append("optimizer landscape permits naive negative inference")
    if optimizer_amendment.get("minimum_independent_seed_count", 0) < 3:
        out.append("optimizer landscape permits an inadequate seed count")
    optimizer_families = " ".join(optimizer_amendment.get("required_families", []))
    for family in ["adamw", "muon", "shampoo", "soap", "schedule_free", "modular_norm"]:
        if family not in optimizer_families:
            out.append(f"optimizer landscape family missing: {family}")
    if optimizer_amendment.get("support_state_effect") != "none" or optimizer_amendment.get("release_effect") != "none":
        out.append("optimizer roadmap amendment laundered support or release state")
    admission_contract = round16.get("future_admission_contract", {})
    if admission_contract.get("maximum_new_chapters_per_empirical_checkpoint") != 0 or admission_contract.get("manifest_admission_without_all_birth_artifacts_allowed") is not False:
        out.append("post-Round-18 freeze or birth-artifact gate weakened")
    if not all(
        admission_contract.get(field) is True
        for field in [
            "material_empirical_or_evidence_milestone_since_previous_admission_required",
            "claim_atom_pack_required_at_birth",
            "reader_projection_required_at_birth",
            "template_inheritance_guard_required_at_birth",
        ]
    ):
        out.append("Round 16 future-admission contract lost a required evidence or integration gate")
    if round16.get("support_state_effect") != "none" or round16.get("release_effect") != "none":
        out.append("Round 16 roadmap amendment laundered support or release state")

    p2_execution = status.get("p2_replacement_execution", {})
    execution_expected = {
        "state": "latest_capacity_and_docker_entry_failed_pool_materialization_not_run_rank5_setup_retry_pending_rank6_closed",
        "independent_evaluator_calibration_case_count": 32,
        "rank_one_task_spec_opened_count": 4,
        "unique_candidate_task_spec_opened_count": 5,
        "slot1_terminal_candidate_count": 5,
        "historical_next_rank_before_amendment": 6,
        "current_setup_retry_rank": 5,
        "rank6_authorized": False,
        "pool_materialization_gate_passed": False,
        "slot1_qualified": False,
        "candidate_execution_started_count": 2,
        "candidate_outcome_custody_incident_count": 1,
        "other_slot_candidate_outcome_opened_count": 0,
        "final_pool_selected": False,
        "final_denominator_opened": False,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    for field, expected in execution_expected.items():
        if p2_execution.get(field) != expected:
            out.append(f"P2 replacement execution status drift: {field}")
    for relative in p2_execution.get("lineage_paths", []):
        if not (ROOT / relative).exists():
            out.append(f"P2 replacement execution lineage missing: {relative}")

    p2_resource = data["p2_resource"]
    p2_resource_status = status.get("p2_resource_ceiling", {})
    resource_expected = {
        "image_pull_ceiling_seconds": 300,
        "engine_content_size_ceiling_bytes": 1500000000,
        "virtual_size_upper_bound_ceiling_bytes": 7000000000,
        "cleanup_stabilization_timeout_seconds": 60,
        "dependency_setup_ceiling_seconds": 300,
        "arm_wall_ceiling_seconds": 600,
        "peak_memory_ceiling_bytes": 6442450944,
        "minimum_host_free_bytes": 53687091200,
        "minimum_qualified_task_count": 12,
        "ceiling_frozen": True,
        "all_qualified_tasks_remeasured": False,
        "resource_gate_passed": False,
        "replacement_draw_started": True,
        "final_pool_selected": False,
        "final_denominator_opened": False,
    }
    task_ceiling = p2_resource.get("task_acceptance_ceilings", {})
    campaign_ceiling = p2_resource.get("campaign_ceilings", {})
    qualification = p2_resource.get("qualification_state", {})
    observed_resource = {
        "image_pull_ceiling_seconds": task_ceiling.get("image_pull_seconds"),
        "engine_content_size_ceiling_bytes": task_ceiling.get("engine_content_size_bytes"),
        "virtual_size_upper_bound_ceiling_bytes": task_ceiling.get("virtual_size_conservative_upper_bound_bytes"),
        "cleanup_stabilization_timeout_seconds": task_ceiling.get("cleanup_stabilization_timeout_seconds"),
        "dependency_setup_ceiling_seconds": task_ceiling.get("dependency_materialization_seconds"),
        "arm_wall_ceiling_seconds": task_ceiling.get("arm_wall_seconds"),
        "peak_memory_ceiling_bytes": task_ceiling.get("peak_memory_bytes"),
        "minimum_host_free_bytes": task_ceiling.get("minimum_host_free_bytes_before_task"),
        "minimum_qualified_task_count": campaign_ceiling.get("minimum_qualified_task_count"),
        "ceiling_frozen": qualification.get("ceiling_frozen"),
        "all_qualified_tasks_remeasured": qualification.get("all_qualified_tasks_remeasured"),
        "resource_gate_passed": qualification.get("resource_gate_passed"),
        "replacement_draw_started": qualification.get("replacement_draw_started"),
        "final_pool_selected": qualification.get("final_pool_selected"),
        "final_denominator_opened": qualification.get("final_pool_opened"),
    }
    for field, expected in resource_expected.items():
        if observed_resource.get(field) != expected:
            out.append(f"P2 resource ceiling record drift: {field}")
        if p2_resource_status.get(field) != expected:
            out.append(f"P2 resource ceiling status drift: {field}")
    if p2_resource.get("measurement_contract", {}).get("cpu_seconds_semantics") != "sampled_estimate_not_exact_billing_measure":
        out.append("P2 resource sampled CPU overclaimed")
    if campaign_ceiling.get("resource_exhaustion_effect") != "corpus_gate_blocked_not_claim_failure":
        out.append("P2 resource failure laundered into claim failure")
    if p2_resource.get("support_state_effect") != "none":
        out.append("P2 resource ceiling promoted support")

    materialization = status.get("p2_sequential_materialization_contract", {})
    materialization_expected = {
        "state": "latest_entry_failed_pending_capacity_and_docker_recovery_before_complete_pool_recipe_and_receipt_set",
        "candidate_count": 30,
        "complete_pool_recipe_set_required_before_rank_opening": True,
        "task_content_must_remain_closed_during_materialization": True,
        "pre_content_exact_image_retry_limit": 3,
        "pre_content_failure_may_skip_or_burn_rank": False,
        "post_content_infrastructure_failure_may_advance_rank": False,
        "post_content_replay_allowed": False,
        "docker_scoped_reclamation_only": True,
        "non_docker_user_data_deletion_allowed": False,
        "minimum_host_free_bytes": 53687091200,
        "support_state_effect": "none",
        "release_effect": "none",
    }
    for field, expected in materialization_expected.items():
        if materialization.get(field) != expected:
            out.append(f"P2 sequential materialization contract drift: {field}")

    if data["atom_registry"].get("summary", {}).get("atom_count") != 4059:
        out.append("current semantic atom registry denominator drifted")
    if len(data["atom_addendum"].get("atoms", [])) != 15:
        out.append("post-activation addendum denominator drifted")
    registry_states = Counter(row.get("support_state") for row in data["atom_registry"].get("atoms", []))
    if sum(count for state, count in registry_states.items() if state != "argument") != 2:
        out.append("activation-registry non-argument count drifted")

    proof_match = re.search(
        r"Current proof-depth snapshot: (\d+) proof targets, (\d+) Lean modules, "
        r"(\d+) theorem declarations, (\d+) derived/decomposed, (\d+) direct/projection, "
        r"(\d+) unknown/mixed",
        data["proof_review"],
    )
    expected_proof = (324, 130, 2052, 1194, 405, 453)
    if not proof_match or tuple(map(int, proof_match.groups())) != expected_proof:
        out.append("proof-depth baseline drifted without roadmap reconciliation")
    if data["proof_manifest"].get("proof_target_count") != 324:
        out.append("proof manifest target count disagrees with the 324 implemented targets")
    if data["proof_manifest"].get("status_counts") != {"implemented": 324}:
        out.append("taxonomy-completion proof targets altered the frozen implemented-proof denominator")

    proof_inventory = status.get("semantic_proof_cluster_inventory", {})
    proof_clusters = proof_inventory.get("clusters", [])
    expected_cluster_ids = [
        "evidence_claim_and_proof_custody",
        "safety_assurance_and_oversight",
        "authority_effect_rollback_and_corrigibility",
        "learning_update_state_and_unlearning",
        "self_improvement_and_readiness",
        "resource_artifact_and_lifecycle_economics",
    ]
    if [row.get("id") for row in proof_clusters] != expected_cluster_ids:
        out.append("semantic proof cluster inventory is not the frozen six-cluster set")
    listed_modules = [module for row in proof_clusters for module in row.get("modules", [])]
    if len(listed_modules) != 25 or len(set(listed_modules)) != 25:
        out.append("semantic proof cluster inventory must contain 25 unique modules")
    manifest_modules = {row.get("module") for row in data["proof_manifest"].get("records", [])}
    missing_modules = sorted(set(listed_modules) - manifest_modules)
    if missing_modules:
        out.append(f"semantic proof inventory names absent modules: {missing_modules}")
    if proof_inventory.get("state") != "all_6_clusters_terminal":
        out.append("semantic proof inventory terminal state drifted")
    if len(proof_clusters) != 6 or any(row.get("state") != "adequate" for row in proof_clusters):
        out.append("P4-C1 through P4-C6 lack terminal adequate bounded-scope dispositions")

    p5 = status.get("p5_effect_complete_reference", {})
    p5_service = p5.get("stateful_service_slice", {})
    p5_result = data["p5_stateful_result"]
    if p5.get("state") != "in_progress_prospective_natural_campaign_frozen_outcomes_closed":
        out.append("P5 prospective natural-campaign state drifted")
    if (
        p5_service.get("source_commit")
        != p5_result.get("custody", {}).get("attested_source_commit")
        or p5_service.get("case_count") != p5_result.get("case_count")
        or p5_service.get("passed_case_count") != p5_result.get("passed_case_count")
        or p5_service.get("loss_before")
        != p5_result.get("learning_state", {}).get("loss_before")
        or p5_service.get("loss_after")
        != p5_result.get("learning_state", {}).get("loss_after")
        or p5_service.get("weights_only_rollback_rejected")
        != p5_result.get("rollback", {}).get("artifact_only_control_rejected")
        or p5_service.get("restored_state_class_count")
        != p5_result.get("rollback", {}).get("restored_state_class_count")
        or p5_service.get("accepted_external_effect_count")
        != p5_result.get("external_effect", {}).get("accepted_effect_count")
        or p5_service.get("revoked_effect_count")
        != p5_result.get("external_effect", {}).get("revoked_effect_count")
        or p5_service.get("attestation_scope")
        != "local_source_and_runtime_identity_not_deployment"
    ):
        out.append("P5 stateful-service result and roadmap status diverged")
    if (
        p5.get("support_state_effect") != "none"
        or p5.get("release_effect") != "none"
        or p5_result.get("support_state_effect") != "none"
        or p5_result.get("release_effect") != "none"
    ):
        out.append("P5 stateful-service slice laundered support or release state")

    p5_natural = p5.get("natural_publication_service_development_trace", {})
    p5_trace = data["p5_natural_trace"]
    if (
        p5_natural.get("source_commit")
        != p5_trace.get("service", {}).get("source_commit")
        or p5_natural.get("trace_path")
        != "experiments/p5_natural_publication_service_trace/results/2026-07-27-development.json"
        or p5_natural.get("build_run_id")
        != p5_trace.get("build_receipt", {}).get("run_id")
        or p5_natural.get("deploy_run_id")
        != p5_trace.get("deploy_receipt", {}).get("run_id")
        or p5_natural.get("artifact_id")
        != p5_trace.get("build_receipt", {}).get("artifact", {}).get("artifact_id")
        or p5_natural.get("artifact_digest")
        != p5_trace.get("build_receipt", {}).get("artifact", {}).get("digest")
        or p5_natural.get("deployment_id")
        != p5_trace.get("deploy_receipt", {}).get("deployment", {}).get("deployment_id")
        or p5_natural.get("source_to_deployment_status_seconds")
        != p5_trace.get("observed_outcome", {}).get(
            "commit_to_deployment_status_seconds"
        )
        or p5_natural.get("source_to_monitor_completion_seconds")
        != p5_trace.get("observed_outcome", {}).get(
            "commit_to_post_deploy_monitor_completion_seconds"
        )
        or p5_natural.get("classification") != p5_trace.get("campaign_role")
    ):
        out.append("P5 natural publication trace and roadmap status diverged")
    if (
        p5_natural.get("eligible_for_held_out_denominator") is not False
        or p5_natural.get("claim_bearing") is not False
        or p5_natural.get("institutionally_independent") is not False
        or p5_trace.get("classification", {}).get("outcome_known_before_trace_freeze")
        is not True
        or p5_trace.get("support_state_effect") != "none"
        or p5_trace.get("record_policy_effect") != "none"
    ):
        out.append("P5 natural publication development trace laundered evidence authority")

    p5_campaign = p5.get("prospective_natural_stateful_campaign", {})
    campaign = data["p5_natural_campaign"]
    if (
        p5_campaign.get("campaign_id") != campaign.get("campaign_id")
        or p5_campaign.get("protocol_path")
        != "experiments/governed_operations_argument_exit/preregistration.json"
        or p5_campaign.get("report_path")
        != "docs/p5_natural_stateful_service_campaign_preregistration.md"
        or p5_campaign.get("schema_path")
        != "schemas/governed_operations_campaign_preregistration.schema.json"
        or p5_campaign.get("frozen_date") != campaign.get("frozen_date")
        or p5_campaign.get("service_id") != campaign.get("service", {}).get("service_id")
        or p5_campaign.get("model_repository")
        != campaign.get("service", {}).get("model_custody", {}).get("repository")
        or p5_campaign.get("model_snapshot_commit")
        != campaign.get("service", {}).get("model_custody", {}).get("snapshot_commit")
        or p5_campaign.get("arm_count") != len(campaign.get("arms", []))
        or p5_campaign.get("task_family_count")
        != len(campaign.get("service", {}).get("task_families", []))
        or p5_campaign.get("development_task_count")
        != campaign.get("population", {}).get("development_task_count")
        or p5_campaign.get("heldout_task_count")
        != campaign.get("population", {}).get("heldout_task_count")
        or p5_campaign.get("fault_class_count") != len(campaign.get("fault_envelope", []))
        or p5_campaign.get("state_class_count") != len(campaign.get("state_inventory", []))
        or p5_campaign.get("external_dependency_count")
        != len(campaign.get("service", {}).get("external_dependencies", []))
        or p5_campaign.get("competence_gate_count")
        != len(campaign.get("competence_gates", []))
        or p5_campaign.get("positive_control_count")
        != len(campaign.get("positive_controls", []))
        or p5_campaign.get("adversarial_control_count")
        != len(campaign.get("adversarial_controls", []))
        or p5_campaign.get("fair_rescue_step_count")
        != len(campaign.get("fair_rescue_steps", []))
        or p5_campaign.get("co_primary_outcome_count")
        != len(campaign.get("outcomes", {}).get("co_primary", []))
        or p5_campaign.get("secondary_outcome_count")
        != len(campaign.get("outcomes", {}).get("secondary", []))
        or p5_campaign.get("cost_metric_count")
        != len(campaign.get("outcomes", {}).get("costs", []))
        or p5_campaign.get("task_content_opened")
        != campaign.get("population", {}).get("task_content_opened")
        or p5_campaign.get("protected_outcomes_opened")
        != campaign.get("heldout", {}).get("protected_outcomes_opened")
        or p5_campaign.get("institutionally_independent")
        != campaign.get("evaluator_and_monitor", {}).get("institutionally_independent")
        or p5_campaign.get("t4_substitution_allowed")
        != campaign.get("heldout", {}).get("t4_substitution_allowed")
        or p5_campaign.get("public_effects_during_trials")
        != campaign.get("matching", {}).get("public_effects_during_trials")
    ):
        out.append("P5 prospective natural campaign and roadmap status diverged")
    if (
        p5_campaign.get("task_content_opened") != 0
        or p5_campaign.get("protected_outcomes_opened") is not False
        or p5_campaign.get("institutionally_independent") is not False
        or p5_campaign.get("t4_substitution_allowed") is not False
        or p5_campaign.get("public_effects_during_trials") is not False
        or campaign.get("execution", {}).get("natural_tasks_run") != 0
        or campaign.get("execution", {}).get("fault_injections_run") != 0
        or campaign.get("execution", {}).get("operators_recruited") != 0
        or campaign.get("execution", {}).get("empirical_result") != "none"
        or campaign.get("support_state_effect") != "none"
        or campaign.get("release_effect") != "none"
    ):
        out.append("P5 prospective campaign opened outcomes or laundered authority")

    p5_qualification = data["p5_natural_qualification"]
    qualification_status = p5_campaign.get("qualification", {})
    expected_qualification_status = {
        "result_path": "experiments/governed_operations_argument_exit/qualification/2026-07-28-local.json",
        "schema_path": "schemas/governed_operations_campaign_qualification.schema.json",
        "runner_path": "scripts/run_p5_natural_service_campaign_qualification.py",
        "validator_path": "scripts/validate_p5_natural_service_campaign_qualification.py",
        "report_path": "docs/p5_natural_stateful_service_campaign_qualification.md",
        "trial_count": p5_qualification.get("trial_count"),
        "process_launch_count": p5_qualification.get("process_launch_count"),
        "calibration_case_count": p5_qualification.get("evaluator_calibration", {}).get("case_count"),
        "qualification_gate_count": p5_qualification.get("qualification_gate_count"),
        "natural_tasks_run": p5_qualification.get("natural_tasks_run"),
        "development_opening_gate_passed": p5_qualification.get("development_opening_gate_passed"),
        "development_task_content_opened": p5_qualification.get("development_task_content_opened"),
        "heldout_opening_gate_passed": p5_qualification.get("heldout_opening_gate_passed"),
        "actual_twenty_four_hour_elapsed_monitor_evidence": p5_qualification.get(
            "actual_twenty_four_hour_elapsed_monitor_evidence"
        ),
        "model_quality_evaluated": p5_qualification.get("model_runtime_canary", {}).get(
            "model_quality_evaluated"
        ),
        "support_state_effect": p5_qualification.get("support_state_effect"),
        "release_effect": p5_qualification.get("release_effect"),
    }
    if qualification_status != expected_qualification_status:
        out.append("P5 qualification result and roadmap status diverged")
    if (
        p5_campaign.get("state")
        != "implementation_and_instrument_qualified_development_content_still_closed"
        or p5_qualification.get("result_role")
        != "authored_implementation_and_instrument_qualification_not_natural_task_evidence"
        or p5_qualification.get("trial_count") != 60
        or p5_qualification.get("process_launch_count") != 213
        or p5_qualification.get("qualification_gates_passed") != 14
        or p5_qualification.get("development_opening_gate_passed") is not True
        or p5_qualification.get("development_task_content_opened") is not False
        or p5_qualification.get("heldout_opening_gate_passed") is not False
        or p5_qualification.get("logical_time_monitor_only") is not True
        or p5_qualification.get("actual_twenty_four_hour_elapsed_monitor_evidence") is not False
        or p5_qualification.get("natural_tasks_run") != 0
        or p5_qualification.get("fault_injections_on_natural_tasks") != 0
        or p5_qualification.get("model_runtime_canary", {}).get("model_quality_evaluated") is not False
        or p5_qualification.get("support_state_effect") != "none"
        or p5_qualification.get("release_effect") != "none"
    ):
        out.append("P5 authored qualification opened natural evidence or laundered authority")

    expected_ids = [f"P{i}" for i in range(9)]
    if [row.get("id") for row in status.get("priorities", [])] != expected_ids:
        out.append("priority order must be exactly P0 through P8")
    if [row.get("id") for row in status.get("milestones", [])] != [f"M{i}" for i in range(9)]:
        out.append("milestone order must be exactly M0 through M8")

    git = data["git"]
    attestation = status.get("attestation", {})
    if git["branch"] != "main" or attestation.get("required_branch") != "main":
        out.append("active book work must remain on main")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", attestation.get("attested_head", ""), git["head"]],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        out.append("attested custody checkpoint is not an ancestor of current main")
    if attestation.get("state") != "pushed_deployed_clean_ancestral_checkpoint":
        out.append("attestation must describe an ancestral checkpoint, not self-reference current HEAD")
    if attestation.get("working_tree_delta_file_count_at_review") != 0:
        out.append("attested custody checkpoint was not clean when reviewed")
    if (
        attestation.get("attested_head")
        != "cef11abd5fca0a421087b3123c1defb31f2b4e6d"
        or attestation.get("build_run_id") != 30410938617
        or attestation.get("deploy_run_id") != 30411437258
        or attestation.get("tested_artifact_verified") is not True
        or attestation.get("deploy_rebuilt") is not False
        or attestation.get("public_crawl_passed") is not True
    ):
        out.append("latest clean build/deploy/public-crawl custody receipt drifted")

    for path, text in data["public"].items():
        if "post_v2_3_maintenance_transfer_and_publication_roadmap.md" not in text:
            out.append(f"{path} lacks the active successor pointer")
    for path in ("docs/publication_readiness.md", "docs/public_status_contract.md"):
        text = data["public"][path]
        if "post_v2_3_claim_proof_and_sota_challenge_roadmap.md" not in text:
            out.append(f"{path} lacks predecessor history")
        if "v2.3.0" not in text:
            out.append(f"{path} erases the latest public release identity")

    active_markers = []
    for path in (ROOT / "docs").glob("*roadmap.md"):
        if ACTIVE_MARKER in path.read_text(encoding="utf-8"):
            active_markers.append(path.relative_to(ROOT).as_posix())
    if active_markers != ["docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"]:
        out.append(f"active roadmap marker set drifted: {active_markers}")
    if status.get("support_state_effect") != "none" or status.get("release_effect") != "none":
        out.append("roadmap revision cannot create support or release effects")

    reader_receipt = status.get("reader_release_receipt", {})
    if truth.get("current_published_reader_release_id") != reader_receipt.get("release_id"):
        out.append("activation truth and reader release identity disagree")
    if truth.get("current_published_reader_formats") != reader_receipt.get("published_formats"):
        out.append("activation truth and current published reader formats disagree")
    reader_manifest = data["reader_manifest"]
    reader_release_record = data["reader_release_record"]
    if reader_manifest.get("release_state") != "published":
        out.append("Round 15 reader manifest is not published")
    if reader_manifest.get("release_commit") != reader_receipt.get("release_commit"):
        out.append("reader manifest and roadmap release commit disagree")
    if reader_manifest.get("release_url") != reader_receipt.get("release_url"):
        out.append("reader manifest and roadmap release URL disagree")
    if [row.get("format") for row in reader_manifest.get("artifacts", [])] != reader_receipt.get("published_formats"):
        out.append("reader manifest and roadmap published-format inventory disagree")
    if any(row.get("status") != "published" or not row.get("download_url") for row in reader_manifest.get("artifacts", [])):
        out.append("reader manifest retains an unpublished or URL-less artifact")
    if reader_release_record.get("release_id") != reader_receipt.get("release_id") or reader_release_record.get("validation_status") != "pass":
        out.append("exact reader edition-release record is absent or invalid")
    if reader_release_record.get("source_commit") != reader_receipt.get("release_commit"):
        out.append("reader edition-release record commit disagrees with roadmap receipt")
    return out


def main() -> None:
    base = inputs()
    failures = errors(base)
    mutations: list[tuple[str, dict]] = []

    def mutate(label: str, edit) -> None:
        candidate = copy.deepcopy(base)
        edit(candidate)
        mutations.append((label, candidate))

    mutate("false publication", lambda c: c["status"].__setitem__("release_effect", "published"))
    mutate("support laundering", lambda c: c["status"].__setitem__("support_state_effect", "promoted"))
    mutate("hosted-chat dependency", lambda c: c["status"]["self_contained_execution"].__setitem__("hosted_chat_dependency", True))
    mutate("private-review gate", lambda c: c["status"]["self_contained_execution"].__setitem__("external_human_prepublication_required", True))
    mutate("authority widening", lambda c: c["status"]["self_contained_execution"].__setitem__("external_mutation_action_time_authority_required", False))
    mutate("claim mapping erasure", lambda c: c["status"]["activation_truth"].__setitem__("resolved_transition_claim_mapping_count", 0))
    mutate("unresolved mapping regression", lambda c: c["status"]["claim_identity_graph"].__setitem__("unresolved_transition_count", 1))
    mutate("natural empirical invention", lambda c: c["status"]["activation_truth"].__setitem__("competence_qualified_natural_non_authored_empirical_transition_count", 1))
    mutate("exploration promotion", lambda c: c["status"]["competence_and_identity_contract"].__setitem__("exploratory_work_may_change_claim_support", True))
    mutate("rehabilitation reopening", lambda c: c["status"]["competence_and_identity_contract"].__setitem__("historical_broad_negative_inference_quarantined_pending_audit", True))
    mutate("broad-refutation weakening", lambda c: c["status"]["competence_and_identity_contract"].__setitem__("broad_refutation_requires_independent_reproduction_and_two_transfer_settings", False))
    mutate("N3 invention", lambda c: c["status"]["negative_result_rehabilitation"].__setitem__("n3_count", 1))
    mutate("broad-negative inference laundering", lambda c: c["status"]["negative_result_rehabilitation"].__setitem__("broad_negative_inference_count", 1))
    mutate("surface language regression", lambda c: c["negative_surface_audit"]["summary"].__setitem__("forbidden_overbroad_phrase_count", 1))
    mutate("P2 selected-claim drift", lambda c: c["p2_selection"]["selected_claim"].__setitem__("claim_id", "posthoc.claim"))
    mutate("P2 premature heldout opening", lambda c: c["p2_selection"]["local_feasibility_snapshot"].__setitem__("final_denominator_opened", True))
    mutate("P2 development-final laundering", lambda c: c["status"]["p2_development_corpus_preflight"].__setitem__("final_pool_selected", True))
    mutate("P2 gold denominator shrink", lambda c: c["status"]["p2_gold_preflight_diagnosis"].__setitem__("replacement_slot_count", 0))
    mutate("P2 N0 mechanism laundering", lambda c: c["p2_gold"]["false_negative_findings"].__setitem__("idea_or_mechanism_negative_inference_count", 1))
    mutate("P2 outcome-aware replacement", lambda c: c["p2_policy"]["replacement_rule"].__setitem__("skipping_candidate_after_outcome_allowed", True))
    mutate("P2 replacement queue state erased", lambda c: c["p2_policy"]["replacement_rule"].__setitem__("replacement_draw_state", "not_started"))
    mutate("P2 replacement queue content leak", lambda c: c["p2_replacement_queue"].__setitem__("task_text_opened", True))
    mutate("P2 replacement queue repository reuse", lambda c: c["p2_replacement_queue"]["slots"][1]["candidates"][0].__setitem__("repo", c["p2_replacement_queue"]["slots"][0]["candidates"][0]["repo"]))
    mutate("P2 sequential execution rollback", lambda c: c["status"]["p2_replacement_execution"].__setitem__("current_setup_retry_rank", 1))
    mutate("P2 rank-six reopening", lambda c: c["status"]["p2_replacement_execution"].__setitem__("rank6_authorized", True))
    mutate("P2 resource premature pass", lambda c: c["p2_resource"]["qualification_state"].__setitem__("resource_gate_passed", True))
    mutate("P2 resource claim laundering", lambda c: c["p2_resource"]["campaign_ceilings"].__setitem__("resource_exhaustion_effect", "claim_failure"))
    mutate("P5 protected task opening", lambda c: c["p5_natural_campaign"]["population"].__setitem__("task_content_opened", 1))
    mutate("P5 heldout denominator shrink", lambda c: c["p5_natural_campaign"]["population"].__setitem__("heldout_task_count", 20))
    mutate("P5 strong baseline deletion", lambda c: c["p5_natural_campaign"]["arms"].pop(2))
    mutate("P5 public effect widening", lambda c: c["p5_natural_campaign"]["matching"].__setitem__("public_effects_during_trials", True))
    mutate("P5 institutional independence invention", lambda c: c["p5_natural_campaign"]["evaluator_and_monitor"].__setitem__("institutionally_independent", True))
    mutate("P5 T4 substitution laundering", lambda c: c["p5_natural_campaign"]["heldout"].__setitem__("t4_substitution_allowed", True))
    mutate("P5 qualification natural-task invention", lambda c: c["p5_natural_qualification"].__setitem__("natural_tasks_run", 1))
    mutate("P5 qualification elapsed-monitor invention", lambda c: c["p5_natural_qualification"].__setitem__("actual_twenty_four_hour_elapsed_monitor_evidence", True))
    mutate("P5 qualification heldout opening", lambda c: c["p5_natural_qualification"].__setitem__("heldout_opening_gate_passed", True))
    mutate("P5 qualification model-quality laundering", lambda c: c["p5_natural_qualification"]["model_runtime_canary"].__setitem__("model_quality_evaluated", True))
    mutate("false self-referential attestation", lambda c: c["status"]["attestation"].__setitem__("state", "commit_bound_clean"))
    mutate("attested build-run drift", lambda c: c["status"]["attestation"].__setitem__("build_run_id", 0))
    mutate("branch permission", lambda c: c["status"]["attestation"].__setitem__("branches_allowed_for_book_work", True))
    mutate("reader publication laundering", lambda c: c["reader_manifest"].__setitem__("release_state", "candidate"))
    mutate("N5 deletion", lambda c: c.__setitem__("competence", c["competence"].replace("N5 — Broad claim refutation", "N5 removed", 1)))
    mutate("false-negative rule deletion", lambda c: c.__setitem__("roadmap", c["roadmap"].replace("No false-negative laundering", "Deleted rule", 1)))
    mutate("missing successor continuity", lambda c: c["status"].__setitem__("closure_requires_active_successor", False))
    mutate("stale predecessor", lambda c: c["predecessor"].__setitem__("status", "active"))
    mutate("shared flagship identity drift", lambda c: c["status"]["quality_uplift_program"].__setitem__("shared_flagship_id", "drifted"))
    mutate("T0A source commit drift", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"].__setitem__("source_commit", "0" * 40))
    mutate("T0A origin publication erasure", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"].__setitem__("published_on_origin_main", False))
    mutate("T0A historical freeze denominator drift", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["historical_freeze"].__setitem__("artifact_count", 142))
    mutate("T1 anchor step drift", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["t1_lineage"].__setitem__("optimizer_steps", 9049))
    mutate("T1 checkpoint identity drift", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["t1_lineage"].__setitem__("checkpoint_sha256", "0" * 64))
    mutate("T1 pre-anchor chain invention", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["t1_lineage"].__setitem__("full_segment_predecessor_chain_available", True))
    mutate("T1 historical payload invention", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["t1_lineage"].__setitem__("t0a_payload_still_materialized_at_frozen_identity", True))
    mutate("T1 append-only lineage erasure", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["t1_lineage"].__setitem__("prospective_append_only_lineage_trigger_state", "MISSING"))
    mutate("T1 evaluator consumption invention", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["evaluation_boundary"].__setitem__("confirmation_surface_consumed", True))
    mutate("T1 capability invention", lambda c: c["status"]["quality_uplift_program"]["t0a_currentness"]["evaluation_boundary"].__setitem__("capability_claim", "SUPPORTED"))
    mutate("editorial meaning-preservation deletion", lambda c: c["status"]["quality_uplift_program"]["narrative_quality_gate"].__setitem__("requires_meaning_preservation_audit", False))
    mutate("post-review reference denominator rollback", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"].__setitem__("reference_chapter_count", 61))
    mutate("post-review narrative target rollback", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"].__setitem__("narrative_unit_target", 15))
    mutate("post-review calculus property deletion", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"]["governed_transition_calculus_properties"].pop())
    mutate("post-review bounded-liveness deletion", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"].__setitem__("bounded_liveness_required", False))
    mutate("post-review external-human gate", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"].__setitem__("prepublication_external_human_required", True))
    mutate("post-review proof-volume priority", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"].__setitem__("proof_work_priority", "maximize_theorem_count"))
    mutate("concept-first exit receipt deletion", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"].__setitem__("concept_first_exit_gate_state", "pending"))
    mutate("concept-first prose anchor deletion", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"]["concept_first_idea_audit"]["packets"][4]["anchors"].pop())
    mutate("concept-first roadmap-only remainder laundering", lambda c: c["status"]["quality_uplift_program"]["post_review_convergence"]["concept_first_idea_audit"].__setitem__("roadmap_only_idea_count", 1))
    mutate("post-review role omission", lambda c: c["current_role_map"]["roles"]["load-bearing-reference"].pop())
    mutate("communication candidate gate weakening", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("communication_requires_source_ethics_and_effect_gate", False))
    mutate("institutional candidate gate weakening", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("institutions_require_authority_legitimacy_and_update_gate", False))
    mutate("deployment-transition candidate gate weakening", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("deployment_transition_requires_realized_outcome_and_distribution_gate", False))
    mutate("physical-compute candidate gate weakening", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("physical_compute_requires_facility_environment_and_retirement_gate", False))
    mutate("objective-formation candidate gate weakening", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("objective_formation_requires_target_proxy_integrity_and_ontology_gate", False))
    mutate("embedded-agency foundations laundering", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("embedded_agency_remains_cross_book_foundations_program", False))
    mutate("societal-part premature creation", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("societal_part_requires_three_admitted_owner_gate", False))
    mutate("source-role gate weakening", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"]["source_roles_required_where_literature_permits"].pop())
    mutate("Q1 Q2 denominator overlap", lambda c: c["status"]["quality_uplift_program"]["empirical_lanes"].__setitem__("denominator_overlap_allowed", True))
    mutate("Q1 outcome tuning leakage", lambda c: c["status"]["quality_uplift_program"]["empirical_lanes"].__setitem__("q1_outcomes_may_tune_q2_or_student", True))
    mutate("P7.1a artificial T4 blocker", lambda c: c["status"]["quality_uplift_program"]["narrative_quality_gate"].__setitem__("case_independent_compression_state", "blocked_by_T4"))
    mutate("execution WIP expansion", lambda c: c["status"]["execution_readiness"].__setitem__("work_in_progress_limit", 9))
    mutate("blocked work consumes WIP", lambda c: c["status"]["execution_readiness"].__setitem__("blocked_lane_consumes_work_in_progress", True))
    mutate("protected outcome inspection", lambda c: c["status"]["execution_readiness"].__setitem__("protected_outcome_inspection_allowed", True))
    mutate("structural candidate concurrency", lambda c: c["status"]["execution_readiness"].__setitem__("maximum_concurrent_second_tranche_candidates", 13))
    mutate("obsolete structural freeze restoration", lambda c: c["status"]["execution_readiness"].__setitem__("structural_admission_freeze", True))
    mutate("A3 premature reactivation", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"].__setitem__("active_candidate_id", "perception-sensor-fusion-and-observation-trust"))
    mutate("historical atom denominator rewrite", lambda c: c["status"]["round_16_evidence_first_amendment"]["post_activation_atom_pack"].__setitem__("historical_3730_activation_atom_denominator_is_immutable", False))
    mutate("R16-A terminal atom denominator deletion", lambda c: c["status"]["round_16_evidence_first_amendment"]["post_activation_atom_pack"].__setitem__("atom_count", 29))
    mutate("W3 current scope rollback", lambda c: c["status"]["round_16_evidence_first_amendment"]["template_inheritance_guard"].__setitem__("current_live_chapter_scope", 66))
    mutate("historical reader laundering", lambda c: c["status"]["round_16_evidence_first_amendment"]["current_reader_freshness_packet"].__setitem__("published_reader_2026_07_18_is_immutable_historical_release", False))
    mutate("R16-B projection denominator rollback", lambda c: c["status"]["round_16_evidence_first_amendment"]["current_reader_freshness_packet"].__setitem__("chapter_projection_count", 83))
    mutate("R16-B unreviewed format laundering", lambda c: c["status"]["round_16_evidence_first_amendment"]["current_reader_freshness_packet"].__setitem__("unreviewed_format_count_deferred", 0))
    mutate("future atom-at-birth deletion", lambda c: c["status"]["round_16_evidence_first_amendment"]["future_admission_contract"].__setitem__("claim_atom_pack_required_at_birth", False))
    mutate("future reader-at-birth deletion", lambda c: c["status"]["round_16_evidence_first_amendment"]["future_admission_contract"].__setitem__("reader_projection_required_at_birth", False))
    mutate("future admission cadence expansion", lambda c: c["status"]["round_16_evidence_first_amendment"]["future_admission_contract"].__setitem__("maximum_new_chapters_per_empirical_checkpoint", 9))
    mutate("post-Round-18 P2 displacement", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"].__setitem__("p2_displacement_allowed", True))
    mutate("post-Round-18 obsolete freeze restoration", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"].__setitem__("structural_admission_freeze", True))
    mutate("post-Round-18 maturity gate deletion", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["maturity_gate_conditions"].pop())
    mutate("post-Round-18 chapter omission", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["depth_packet"]["chapter_ids"].pop())
    mutate("post-Round-18 candidate research premature activation", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"].__setitem__("candidate_research_active", True))
    mutate("post-Round-18 candidate premature admission", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["research_candidates"][0].__setitem__("admission_state", "manifest_admitted"))
    mutate("post-Round-18 word-count gate", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["depth_packet"].__setitem__("word_count_is_acceptance_gate", True))
    mutate("Round 20 chapter-count widening", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("manifest_chapter_count_freeze", 85))
    mutate("Round 20 terminal-state laundering", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("state", "active"))
    mutate("Round 20 word-count laundering", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("word_trigger_is_acceptance_or_evidence_gate", True))
    mutate("Round 20 atom coverage rollback", lambda c: c["round_20_chapter_substance"]["summary"].__setitem__("atom_covered_chapter_count", 83))
    mutate("Round 20 concept pass laundering", lambda c: c["round_20_chapter_substance"]["summary"].__setitem__("active_concepts_passing_count", 71))
    mutate("Round 21 semantic review denominator laundering", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("current_digest_bound_semantic_review_count", 8))
    mutate("Round 21 word-count completion laundering", lambda c: c["round_20_chapter_substance"]["summary"].__setitem__("word_trigger_is_completion_gate", True))
    mutate("Round 21 atom-count target laundering", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("atom_count_parity_is_acceptance_target", True))
    mutate("Round 21 next-batch false reopening", lambda c: c["status"]["round_20_chapter_substance_recovery"]["next_priority_batch"].append("false-owner"))
    mutate("Round 21 raw-scaffold audit bypass", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("raw_scaffold_audit_required", False))
    mutate("Round 21 raw-scaffold unjustified-block laundering", lambda c: c["p6_9_raw_scaffold_audit"]["summary"].__setitem__("unjustified_widest_block_count", 1))
    mutate("Round 21 evidence handoff truncation", lambda c: c["status"]["round_20_chapter_substance_recovery"]["evidence_handoff_requires"].pop())
    mutate("Round 21 evidence handoff identity laundering", lambda c: c["p6_9_proof_evidence_handoff"]["summary"].__setitem__("missing_handoff_identity_count", 1))
    mutate("Round 21 terminal flag deletion", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("p6_9_terminal", False))
    mutate("Round 20 manual review bypass", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("manual_semantic_review_required", False))
    mutate("Round 20 diagnostic thin list deletion", lambda c: c["status"]["round_20_chapter_substance_recovery"]["diagnostic_thin_chapters"].pop())
    mutate("Round 21 concept-completion queue false reopening", lambda c: c["status"]["round_20_chapter_substance_recovery"]["remaining_concept_completion_queue"].append("false-owner"))
    mutate("Round 20 support promotion", lambda c: c["status"]["round_20_chapter_substance_recovery"].__setitem__("support_state_effect", "promoted"))
    mutate("Precision Contract premature chapter authorization", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["precision_contract_source_amendment"].__setitem__("new_chapter_allowed_now", True))
    mutate("Precision Contract contingency activation", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["precision_contract_source_amendment"].__setitem__("contingency_is_active_candidate", True))
    mutate("Precision Contract P2 displacement", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["precision_contract_source_amendment"].__setitem__("p2_displacement_allowed", True))
    mutate("Precision Contract third WIP lane", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["precision_contract_source_amendment"].__setitem__("third_wip_lane_allowed", True))
    mutate("Precision Contract automatic Appendix H admission", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["precision_contract_source_amendment"].__setitem__("automatic_appendix_h_admission_allowed", True))
    mutate("Precision Contract support laundering", lambda c: c["status"]["post_round_18_depth_and_coverage_amendment"]["precision_contract_source_amendment"].__setitem__("support_state_effect", "supported"))
    mutate("roadmap manuscript prose deletion", lambda c: c["manuscript_completion"].__setitem__("precision_primary", c["manuscript_completion"]["precision_primary"].replace("### Functional precision: preserve behavior, not coordinates", "### Deleted precision prose", 1)))
    mutate("non-Docker deletion authorization", lambda c: c["status"]["round_16_evidence_first_amendment"]["p2_empirical_recovery"].__setitem__("non_docker_user_data_deletion_allowed", True))
    mutate("optimizer duplicate chapter authorization", lambda c: c["status"]["round_16_evidence_first_amendment"]["optimizer_landscape_depth_amendment"].__setitem__("new_chapter_allowed", True))
    mutate("optimizer coupled-policy deletion", lambda c: c["status"]["round_16_evidence_first_amendment"]["optimizer_landscape_depth_amendment"].__setitem__("optimizer_is_coupled_run_policy", False))
    mutate("optimizer unmatched tuning", lambda c: c["status"]["round_16_evidence_first_amendment"]["optimizer_landscape_depth_amendment"].__setitem__("matched_tuning_budget_required", False))
    mutate("optimizer rescue deletion", lambda c: c["status"]["round_16_evidence_first_amendment"]["optimizer_landscape_depth_amendment"].__setitem__("method_specific_rescue_required_before_negative_inference", False))
    mutate("optimizer Muon family deletion", lambda c: c["status"]["round_16_evidence_first_amendment"]["optimizer_landscape_depth_amendment"]["required_families"].pop(6))
    mutate("P2 pre-content rank skipping", lambda c: c["status"]["p2_sequential_materialization_contract"].__setitem__("pre_content_failure_may_skip_or_burn_rank", True))
    mutate("P2 post-content replay", lambda c: c["status"]["p2_sequential_materialization_contract"].__setitem__("post_content_replay_allowed", True))
    mutate("semantic proof cluster deletion", lambda c: c["status"]["semantic_proof_cluster_inventory"]["clusters"].pop())
    mutate("book organization reopening", lambda c: c["status"]["execution_readiness"].__setitem__("immediate_book_packet", "P7.2-T1-white-box-evidence-interpretability-and-activation-governance"))
    mutate("ManimGL substitution", lambda c: c["status"]["manim_visual_edition"]["toolchain"].__setitem__("manimgl_allowed", True))
    mutate("Manim global environment laundering", lambda c: c["status"]["manim_visual_edition"]["toolchain"].__setitem__("broken_global_environment_allowed", True))
    mutate("Manim chapter denominator shrink", lambda c: c["status"]["manim_visual_edition"].__setitem__("canonical_chapter_count", 83))
    mutate("Manim Git video-binary admission", lambda c: c["status"]["manim_visual_edition"]["repository_boundary"].__setitem__("rendered_video_binary_tracked_in_git", True))
    mutate("Manim Pages video-binary admission", lambda c: c["status"]["manim_visual_edition"]["repository_boundary"].__setitem__("rendered_video_binary_in_pages_artifact", True))
    mutate("Manim non-YouTube host drift", lambda c: c["status"]["manim_visual_edition"]["hosting"].__setitem__("canonical_binary_host", "GitHub Pages"))
    mutate("Manim premature publication authority", lambda c: c["status"]["manim_visual_edition"]["hosting"].__setitem__("external_publication_authorized_now", True))
    mutate("Manim upload-before-validation", lambda c: c["status"]["manim_visual_edition"]["hosting"].__setitem__("quarto_embed_only_after_published_current", False))
    mutate("Manim local-completion denominator drift", lambda c: c["status"]["manim_visual_edition"]["current_counts"].__setitem__("chapter_packets_validated", 83))
    mutate("Manim aesthetic floor weakening", lambda c: c["status"]["manim_visual_edition"]["pedagogical_and_aesthetic_ratchet"].__setitem__("minimum_score_each_dimension", 3))
    mutate("Manim average laundering", lambda c: c["status"]["manim_visual_edition"]["pedagogical_and_aesthetic_ratchet"].__setitem__("averaging_may_hide_failure", True))
    mutate("Manim external-human blocker", lambda c: c["status"]["manim_visual_edition"]["pedagogical_and_aesthetic_ratchet"].__setitem__("external_human_prepublication_gate_required", True))
    mutate("Manim mechanical-aesthetic laundering", lambda c: c["status"]["manim_visual_edition"]["pedagogical_and_aesthetic_ratchet"].__setitem__("mechanical_diagnostic_is_aesthetic_verdict", True))
    mutate("Manim support promotion", lambda c: c["status"]["manim_visual_edition"].__setitem__("support_state_effect", "promoted"))
    mutate("Manim roadmap section deletion", lambda c: c.__setitem__("roadmap", c["roadmap"].replace("### P7.3 — Governed Manim visual edition", "### Removed visual edition", 1)))
    mutate("P4 next packet rollback", lambda c: c["status"]["execution_readiness"].__setitem__("immediate_formal_packet", "P4-C3-authority-effect-rollback-and-corrigibility-semantic-audit"))
    mutate("first-tranche terminal count rollback", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"].__setitem__("completed_reader_chapter_count", 1))
    mutate("T1/T2/T3 terminal identity deletion", lambda c: c["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"].__setitem__("terminal_reader_chapter_ids", []))
    mutate("P4 C5 status reopening", lambda c: c["status"]["semantic_proof_cluster_inventory"]["clusters"][4].__setitem__("state", "strengthen"))
    mutate("reader format history laundering", lambda c: c["status"]["activation_truth"].__setitem__("current_published_reader_formats", ["html"]))

    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "Evidence-competence roadmap validation failed:\n - " + "\n - ".join(failures)
        )
    print(
        "Evidence-competence roadmap passed: P0 clean pushed/build/deploy ancestral custody checkpoint attested, P1/M1 complete, active P2/M2; 115 accepted transitions, "
        "25 direct and 90 indirect identities resolved with zero unmapped; N0-N5 competence contract active and historical rehabilitation complete; "
        "90 accepted historical negatives classified as 1 N0, 15 N1, 74 N2, and 0 N3-N5; "
        "the frozen 75-surface rehabilitation snapshot including the then-live 55 chapters reconciled with zero overbroad negative language; "
        "P2 selected prospectively from five candidates; natural development preflight covers 1,117 post-snapshot tasks, 12 repositories, seven languages, and 12 image manifests; the fixed gold denominator is fully dispositioned as eight qualified and four N0 replacements across 62 verified arm logs and eight attempts; the corrected infrastructure/content boundary reinstates rank five as setup-retry-pending and keeps rank six closed; the historical 2026-07-22 capacity entry condition was met, while the latest exact 2026-07-28 receipt confirms both a below-floor host and unreachable Docker daemon without opening protected content; the complete 30-candidate sequential materialization remains unpassed; Q1 D1 and Theseus Q2 D2 remain disjoint and sealed; remeasurement, qualification, construct, and heldout gates remain closed; "
        "all six semantic proof clusters are terminally adequate at bounded scope; the historical 66-chapter Round 18 freeze remains recorded, while the superseding no-deferral, taxonomy, and full-coverage transactions admit eighteen distinct manuscript owners into the current 84-chapter book at argument support, leave zero live candidate queue, add semantic review and current proof-triage custody, and remove structural freezing for manuscript ideas; the current 84-entry role partition is exact at 11 thesis, 54 load-bearing reference, 7 implementation, and 12 speculative chapters; the C0-C8 convergence amendment preserves three defended contributions, targets a 22-unit reader route, and adds shared calculus, developmental-loop, minimal-kernel, bounded-liveness, P0-P6 proof-depth, and natural-flagship work without an external-human prepublication gate; P7.3 is the active owner-directed book packet with five pilots, an all-84 ManimCE target, YouTube binary hosting, Git/Pages binary exclusion, exact captions/transcripts/receipts, and zero fabricated completion; optimizer manuscript depth is terminal while its empirical campaign remains a nonblocking evidence residual; current proof and main-attestation baselines exact; no support/release effect; "
        f"{len(mutations)}/{len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
