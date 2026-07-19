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
READER_MANIFEST = ROOT / "editions/reader_manuscript/reader_2026_07_18/manifest.json"
READER_RELEASE_RECORD = ROOT / "release_records/2026-07-18-reader-2026-07-18-0921a924.json"
STRUCTURAL_RESEARCH = ROOT / "docs/structural_completeness_chapter_research_2026_07_19.md"
STRUCTURAL_GAP_AUDIT = ROOT / "docs/structural_completeness_gap_audit_2026_07_19.md"
SOURCE_INVENTORY = ROOT / "sources/source_inventory.json"
BOOK_MANIFEST = ROOT / "book_structure.json"
STRUCTURAL_CHAPTER_PATHS = {
    "white-box-evidence-interpretability-and-activation-governance": ROOT / "chapters/white-box-evidence-interpretability-and-activation-governance.qmd",
    "governed-world-models-and-reality-grounding": ROOT / "chapters/governed-world-models-and-reality-grounding.qmd",
    "human-factors-and-meaningful-control-in-oversight": ROOT / "chapters/human-factors-and-meaningful-control-in-oversight.qmd",
    "governed-operations-incident-command-and-graceful-degradation": ROOT / "chapters/governed-operations-incident-command-and-graceful-degradation.qmd",
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
    atom_ids = {row["atom_id"] for row in atom_registry["atoms"]}
    atom_ids.update(row["id"] for row in atom_addendum["atoms"])
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
        "identity_graph": load(IDENTITY_GRAPH),
        "negative_rehabilitation": load(NEGATIVE_REHABILITATION),
        "negative_surface_audit": load(NEGATIVE_SURFACE_AUDIT),
        "p2_selection": load(P2_SELECTION),
        "p2_corpus": load(P2_CORPUS),
        "p2_gold": load(P2_GOLD),
        "p2_policy": load(P2_POLICY),
        "p2_resource": load(P2_RESOURCE),
        "p2_replacement_queue": load(P2_REPLACEMENT_QUEUE),
        "reader_manifest": load(READER_MANIFEST),
        "reader_release_record": load(READER_RELEASE_RECORD),
        "structural_research": STRUCTURAL_RESEARCH.read_text(encoding="utf-8"),
        "structural_gap_audit": STRUCTURAL_GAP_AUDIT.read_text(encoding="utf-8"),
        "source_inventory": load(SOURCE_INVENTORY),
        "book_manifest": load(BOOK_MANIFEST),
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

    roadmap = data["roadmap"]
    required_sections = [
        "## Purpose",
        "## Strategic quality diagnosis",
        "## Execution-ready work board",
        "## Shared ASI Stack–Theseus flagship",
        "## Review adjudication and corrected baseline",
        "## Operating rules",
        "## P0 — Public truth, claim identity, and attestation continuity",
        "## P1 — Negative-result rehabilitation and false-negative defense",
        "## P2 — Competence-qualified natural empirical frontier",
        "## P3 — Independent reproduction, transfer, and SOTA challenge",
        "## P4 — Semantically meaningful formal evidence",
        "## P5 — Effect-complete governed reference system",
        "## P6 — Evidence, instrument, and source renewal",
        "## P7 — Reader remediation and owner-authorized publication",
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
        "59 to at most 72 chapters",
        "human-ai-communication-persuasion-and-epistemic-security",
        "institutions-international-coordination-and-public-legitimacy",
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
        "A blocked packet does not consume a slot",
    ]:
        if phrase.casefold() not in roadmap_normalized:
            out.append(f"roadmap governing boundary missing: {phrase}")

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
        "Status: **second-tranche coverage audit; roadmap admission does not imply manifest admission**",
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
    if len(manifest_chapters) != 59:
        out.append(f"working manifest chapter count is {len(manifest_chapters)}, expected 59")
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
    if second_ids.intersection(manifest_ids):
        out.append(f"manifest-gated second structural tranche admitted prematurely: {sorted(second_ids & manifest_ids)}")

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
    if surface_scope.get("surface_count") != rehabilitation_status.get("current_surface_count"):
        out.append("negative-inference current surface denominator drifted")
    if surface_scope.get("chapter_count") != rehabilitation_status.get("live_chapter_surface_count"):
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
    if execution_readiness.get("state") != "ready_with_parallel_unblocked_work_and_one_resource_blocked_lane":
        out.append("execution board is not in its ready-with-one-blocked-lane state")
    if execution_readiness.get("headline_priority") != "P2" or execution_readiness.get("headline_priority_state") != "blocked_below_frozen_host_free_space_floor":
        out.append("execution board obscures the P2 headline or its exact resource blocker")
    if execution_readiness.get("work_in_progress_limit") != 2 or execution_readiness.get("blocked_lane_consumes_work_in_progress") is not False:
        out.append("execution board lost its bounded WIP or blocked-lane rule")
    if execution_readiness.get("protected_outcome_inspection_allowed") is not False:
        out.append("execution board permits protected-outcome inspection")
    if execution_readiness.get("maximum_concurrent_second_tranche_candidates") != 1:
        out.append("execution board permits structural-candidate sprawl")
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
    if [row.get("id") for row in critical_path] != [f"T{i}" for i in range(7)]:
        out.append("shared quality critical path must be exactly T0 through T6")
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
    if narrative_gate.get("case_independent_compression_state") != "w1_terminal_w2_ready":
        out.append("P7.1a W1/W2 execution state drifted")
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

    p2_execution = status.get("p2_replacement_execution", {})
    execution_expected = {
        "state": "pool_materialization_blocked_rank5_setup_retry_pending_rank6_closed",
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

    if data["atom_registry"].get("summary", {}).get("atom_count") != 3730:
        out.append("activation atom registry denominator drifted")
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
    expected_proof = (306, 102, 1307, 901, 230, 176)
    if not proof_match or tuple(map(int, proof_match.groups())) != expected_proof:
        out.append("proof-depth baseline drifted without roadmap reconciliation")
    if data["proof_manifest"].get("proof_target_count") != expected_proof[0]:
        out.append("proof manifest target count disagrees with reconciled proof-depth baseline")

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
    if len(listed_modules) != 24 or len(set(listed_modules)) != 24:
        out.append("semantic proof cluster inventory must contain 24 unique modules")
    manifest_modules = {row.get("module") for row in data["proof_manifest"].get("records", [])}
    missing_modules = sorted(set(listed_modules) - manifest_modules)
    if missing_modules:
        out.append(f"semantic proof inventory names absent modules: {missing_modules}")
    if proof_inventory.get("state") != "cluster_1_terminal_5_pending":
        out.append("semantic proof inventory progress state drifted")
    if not proof_clusters or proof_clusters[0].get("state") != "adequate":
        out.append("P4-C1 lacks its terminal adequate bounded-scope disposition")
    if any(row.get("state") != "strengthen" for row in proof_clusters[1:]):
        out.append("unaudited semantic proof clusters lost their strengthen state")

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

    for path, text in data["public"].items():
        if "post_v2_3_maintenance_transfer_and_publication_roadmap.md" not in text:
            out.append(f"{path} lacks the active successor pointer")
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
    mutate("false self-referential attestation", lambda c: c["status"]["attestation"].__setitem__("state", "commit_bound_clean"))
    mutate("branch permission", lambda c: c["status"]["attestation"].__setitem__("branches_allowed_for_book_work", True))
    mutate("reader publication laundering", lambda c: c["reader_manifest"].__setitem__("release_state", "candidate"))
    mutate("N5 deletion", lambda c: c.__setitem__("competence", c["competence"].replace("N5 — Broad claim refutation", "N5 removed", 1)))
    mutate("false-negative rule deletion", lambda c: c.__setitem__("roadmap", c["roadmap"].replace("No false-negative laundering", "Deleted rule", 1)))
    mutate("missing successor continuity", lambda c: c["status"].__setitem__("closure_requires_active_successor", False))
    mutate("stale predecessor", lambda c: c["predecessor"].__setitem__("status", "active"))
    mutate("shared flagship identity drift", lambda c: c["status"]["quality_uplift_program"].__setitem__("shared_flagship_id", "drifted"))
    mutate("editorial meaning-preservation deletion", lambda c: c["status"]["quality_uplift_program"]["narrative_quality_gate"].__setitem__("requires_meaning_preservation_audit", False))
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
    mutate("P2 pre-content rank skipping", lambda c: c["status"]["p2_sequential_materialization_contract"].__setitem__("pre_content_failure_may_skip_or_burn_rank", True))
    mutate("P2 post-content replay", lambda c: c["status"]["p2_sequential_materialization_contract"].__setitem__("post_content_replay_allowed", True))
    mutate("semantic proof cluster deletion", lambda c: c["status"]["semantic_proof_cluster_inventory"]["clusters"].pop())
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
        "P2 selected prospectively from five candidates; natural development preflight covers 1,117 post-snapshot tasks, 12 repositories, seven languages, and 12 image manifests; the fixed gold denominator is fully dispositioned as eight qualified and four N0 replacements across 62 verified arm logs and eight attempts; the corrected infrastructure/content boundary reinstates rank five as setup-retry-pending, keeps rank six closed, and blocks the complete 30-image pool before any further protected content opens; Q1 D1 and Theseus Q2 D2 remain disjoint and sealed; remeasurement, qualification, construct, and heldout gates remain closed; "
        "six semantic proof clusters containing 24 unique modules are frozen for audit; current proof and main-attestation baselines exact; no support/release effect; "
        f"{len(mutations)}/{len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
