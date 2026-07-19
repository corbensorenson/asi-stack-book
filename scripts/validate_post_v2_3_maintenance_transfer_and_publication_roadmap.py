#!/usr/bin/env python3
"""Validate the active evidence-competence, transfer, and publication roadmap."""

from __future__ import annotations

import copy
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
        "transition_snapshot": transition_snapshot(atom_ids),
        "proof_review": PROOF_REVIEW.read_text(encoding="utf-8"),
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
        "## Initial owned queue",
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
        "90 non-direct claim IDs",
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
    ]:
        if phrase.casefold() not in roadmap_normalized:
            out.append(f"roadmap governing boundary missing: {phrase}")

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
    if surface_scope.get("surface_count") != 75 or surface_scope.get("chapter_count") != 55:
        out.append("negative-inference surface audit denominator drifted")
    for field, expected in {
        "current_surface_count": 75,
        "live_chapter_surface_count": 55,
        "forbidden_overbroad_phrase_count": 0,
        "missing_rehabilitation_boundary_count": 0,
        "blocked_chapter_boundary_failure_count": 0,
    }.items():
        if rehabilitation_status.get(field) != expected:
            out.append(f"roadmap surface-rehabilitation status drift: {field}")

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

    p2_execution = status.get("p2_replacement_execution", {})
    execution_expected = {
        "state": "slot1_rank5_terminal_rank6_next_other_slots_rank1_unexecuted",
        "independent_evaluator_calibration_case_count": 32,
        "rank_one_task_spec_opened_count": 4,
        "unique_candidate_task_spec_opened_count": 5,
        "slot1_terminal_candidate_count": 5,
        "slot1_next_rank": 6,
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
    expected_proof = (298, 98, 1307, 901, 230, 176)
    if not proof_match or tuple(map(int, proof_match.groups())) != expected_proof:
        out.append("proof-depth baseline drifted without roadmap reconciliation")

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
    if attestation.get("state") != "pushed_ancestral_custody_checkpoint":
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
    mutate("P2 sequential execution rollback", lambda c: c["status"]["p2_replacement_execution"].__setitem__("slot1_next_rank", 1))
    mutate("P2 resource premature pass", lambda c: c["p2_resource"]["qualification_state"].__setitem__("resource_gate_passed", True))
    mutate("P2 resource claim laundering", lambda c: c["p2_resource"]["campaign_ceilings"].__setitem__("resource_exhaustion_effect", "claim_failure"))
    mutate("false self-referential attestation", lambda c: c["status"]["attestation"].__setitem__("state", "commit_bound_clean"))
    mutate("branch permission", lambda c: c["status"]["attestation"].__setitem__("branches_allowed_for_book_work", True))
    mutate("reader publication laundering", lambda c: c["reader_manifest"].__setitem__("release_state", "candidate"))
    mutate("N5 deletion", lambda c: c.__setitem__("competence", c["competence"].replace("N5 — Broad claim refutation", "N5 removed", 1)))
    mutate("false-negative rule deletion", lambda c: c.__setitem__("roadmap", c["roadmap"].replace("No false-negative laundering", "Deleted rule", 1)))
    mutate("missing successor continuity", lambda c: c["status"].__setitem__("closure_requires_active_successor", False))
    mutate("stale predecessor", lambda c: c["predecessor"].__setitem__("status", "active"))

    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "Evidence-competence roadmap validation failed:\n - " + "\n - ".join(failures)
        )
    print(
        "Evidence-competence roadmap passed: P0 ancestral custody checkpoint pushed, P1/M1 complete, active P2/M2; 115 accepted transitions, "
        "25 direct and 90 indirect identities resolved with zero unmapped; N0-N5 competence contract active and historical rehabilitation complete; "
        "90 accepted historical negatives classified as 1 N0, 15 N1, 74 N2, and 0 N3-N5; "
        "75 current surfaces including 55 chapters reconciled with zero overbroad negative language; "
        "P2 selected prospectively from five candidates; natural development preflight covers 1,117 post-snapshot tasks, 12 repositories, seven languages, and 12 image manifests; the fixed gold denominator is fully dispositioned as eight qualified and four N0 replacements across 62 verified arm logs and eight attempts; the corrected infrastructure/content boundary now reinstates rank five as pending and blocks the complete 30-image pool before any further protected content opens; remeasurement, qualification, construct, and heldout gates remain closed; "
        "current proof and main-attestation baselines exact; no support/release effect; "
        f"{len(mutations)}/{len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
