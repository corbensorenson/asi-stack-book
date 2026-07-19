#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    vertical = load("experiments/governed_repository_change_slice/results/2026-07-10-local.json")
    baseline = vertical.get("baseline_summary", {})
    governed = vertical.get("governed_summary", {})
    matched = vertical.get("matched_comparison", {})
    expected = {
        "scenario_count": (vertical.get("scenario_count"), 9),
        "baseline false accepts": (baseline.get("false_accepts"), 8),
        "governed false accepts": (governed.get("false_accepts"), 0),
        "baseline unsafe releases": (baseline.get("unsafe_releases"), 8),
        "governed unsafe releases": (governed.get("unsafe_releases"), 0),
        "additional cost": (matched.get("additional_cost_units"), 39),
        "additional latency": (matched.get("additional_latency_steps"), 62),
        "operator burden": (matched.get("additional_operator_review_steps"), 9),
        "rollback attempts": (governed.get("rollback_attempts"), 3),
        "exact rollbacks": (governed.get("exact_rollbacks"), 2),
        "quarantined failed rollback": (governed.get("failed_rollbacks"), 1),
        "residuals discovered": (governed.get("residuals_discovered"), 2),
    }
    for label, (actual, wanted) in expected.items():
        if actual != wanted:
            errors.append(f"Workstream D {label} drifted: {actual!r} != {wanted!r}")
    if vertical.get("support_state_effect") != "none" or vertical.get("evidence_transition_created") is not False:
        errors.append("Workstream D bounded rerun must not create or imply a support transition")
    invariants = load("experiments/governed_trace_invariants/results/2026-07-10-local.json")
    if not all(invariants.get("invariant_results", {}).values()):
        errors.append("Workstream D/E invariant suite is not fully passing")
    if not all(invariants.get("negative_controls", {}).values()) or len(invariants.get("negative_controls", {})) != 4:
        errors.append("Workstream D/E must reject four invariant mutations")
    if invariants.get("final_open_residuals") != 1 or invariants.get("support_state_effect") != "none":
        errors.append("Workstream D/E must preserve one open residual and no support effect")
    manifest = load("book_structure.json")
    live_chapter_ids = {
        str(chapter.get("id", ""))
        for part in manifest.get("parts", [])
        for chapter in part.get("chapters", [])
    }
    dispositions = load("claim_decisions/v1_x_core_claim_dispositions.json").get("summary", {})
    if (
        dispositions.get("manifest_chapter_core_claims") != len(live_chapter_ids)
        or dispositions.get("promoted_core_claims") != 0
        or dispositions.get("chapter_core_claims_remaining_at_argument") != len(live_chapter_ids)
    ):
        errors.append("Workstream D live core-claim dispositions are incomplete or promoted")
    active_status = load("roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json")
    activation = active_status.get("activation_baseline", {})
    if activation.get("core_claim_count") != 54 or activation.get("proof_target_count") != 298:
        errors.append("Workstream D/E historical 54-claim and 298-target closure baseline drifted")

    proof_manifest = load("proofs/proof_manifest.json")
    targets = proof_manifest.get("targets", proof_manifest.get("records", []))
    live_target_count = int(proof_manifest.get("proof_target_count", len(targets)))
    proof_chapter_ids = set(proof_manifest.get("chapter_counts", {}))
    if (
        len(targets) != live_target_count
        or live_target_count < int(activation.get("proof_target_count", 0))
        or proof_chapter_ids != live_chapter_ids
    ):
        errors.append(
            "Workstream E live proof manifest must preserve the historical 298-target inventory while covering every current manifest chapter"
        )
    adequacy = (ROOT / "docs/proof_adequacy_review.md").read_text(encoding="utf-8")
    for phrase in ("adequate finite-record invariant", "useful but too narrow", "needs richer state-machine or review semantics", "needs executable tests first", "needs empirical or baseline tests first"):
        if phrase not in adequacy:
            errors.append(f"Workstream E adequacy review missing class: {phrase}")
    proof_audit = (ROOT / "docs/proof_artifact_audit.md").read_text(encoding="utf-8")
    if f"Proof targets audited | {live_target_count}" not in proof_audit or "Validation errors | 0" not in proof_audit:
        errors.append("Workstream E proof artifact audit is incomplete")

    inventory = load("sources/source_inventory.json")
    source_ids = {record["id"] for record in inventory}
    for source_id in ("ext_mcp_protocol_2025_11_25", "ext_a2a_protocol_1_0_0", "ext_owasp_agentic_top_10_2026", "ext_nist_ai_rmf_1_0_2023"):
        if source_id not in source_ids:
            errors.append(f"Workstream F volatile refresh missing {source_id}")
    inter_stack = next(ch for part in manifest["parts"] for ch in part["chapters"] if ch["id"] == "inter-stack-protocols-identity-and-economic-exchange")
    for source_id in ("ext_mcp_protocol_2025_11_25", "ext_a2a_protocol_1_0_0"):
        if source_id not in inter_stack.get("source_ids", []):
            errors.append(f"Workstream F inter-stack chapter not routed to {source_id}")
    refresh = (ROOT / "docs/time_sensitive_source_refresh_2026_07_10.md").read_text(encoding="utf-8")
    for phrase in ("latest released specification", "release candidate", "latest released version", "AI RMF 1.0 is being revised"):
        if phrase not in refresh:
            errors.append(f"Workstream F refresh boundary missing: {phrase}")
    closure = (ROOT / "docs/workstreams_d_e_f_closure_audit.md").read_text(encoding="utf-8")
    for label in ("Workstream D", "Workstream E", "Workstream F", "proven locally"):
        if label not in closure:
            errors.append(f"Readable D–F closure audit missing {label}")
    if errors:
        raise SystemExit("Workstreams D–F closure validation failed:\n - " + "\n - ".join(errors))
    print("Workstreams D–F closure passed: bounded empirical slice, finite formal audit, source/terminology refresh, no support promotion.")


if __name__ == "__main__":
    main()
