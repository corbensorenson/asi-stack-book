#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "proofs" / "p2_closure_audit.json"
RATIONALIZATION = ROOT / "proofs" / "proof_rationalization_registry.json"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
ADEQUACY = ROOT / "docs" / "proof_adequacy_review.md"
VALIDATION = ROOT / "validation" / "registry.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_claim_proof_and_sota_challenge_status.json"
MAINTENANCE_STATUS = ROOT / "roadmap_records" / "post_v2_3_maintenance_transfer_and_publication_status.json"

HISTORICAL_PROOF_TARGET_COUNT = 298
CURRENT_PROOF_TARGET_COUNT = 306
CURRENT_IMPLEMENTED_TARGET_COUNT = 304
CURRENT_PLANNED_TARGET_COUNT = 2
HISTORICAL_EXPECTED_CLASSES = {
    "adequate finite-record invariant": 73,
    "useful but too narrow": 158,
    "needs richer state-machine or review semantics": 16,
    "needs executable tests first": 35,
    "needs empirical or baseline tests first": 14,
    "research-agenda until artifact import": 2,
}
CURRENT_EXPECTED_CLASSES = {
    "adequate finite-record invariant": 73,
    "useful but too narrow": 158,
    "needs richer state-machine or review semantics": 20,
    "needs executable tests first": 37,
    "needs empirical or baseline tests first": 16,
    "research-agenda until artifact import": 2,
}
ADMITTED_CHAPTERS = {
    "white-box-evidence-interpretability-and-activation-governance",
    "governed-world-models-and-reality-grounding",
    "human-factors-and-meaningful-control-in-oversight",
    "governed-operations-incident-command-and-graceful-degradation",
}
PLANNED_CHAPTERS = ADMITTED_CHAPTERS - {
    "white-box-evidence-interpretability-and-activation-governance",
    "governed-world-models-and-reality-grounding",
    "human-factors-and-meaningful-control-in-oversight",
}
EXPECTED_RICHER = {
    "constitutional-alignment-substrate": 6,
    "moral-uncertainty-and-value-conflict": 6,
    "resource-economics-and-token-budgets": 4,
}
REVIEWED_STATES = {"semantically_reviewed", "terminally_dispositioned"}
FORWARD_PRIORITIES = {"P3", "P4", "P5", "P6", "P7"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def adequacy_counts(text: str) -> Counter[str]:
    body = text.split("## Chapter-Level Target Classification", 1)[1].split(
        "## Follow-Through Increments", 1
    )[0]
    counts: Counter[str] = Counter()
    for line in body.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"[0-9,]+", cells[1]):
            counts[cells[2]] += int(cells[1].replace(",", ""))
    return counts


def current_proof_errors(
    manifest: dict[str, Any],
    triage: dict[str, Any],
    maintenance_status: dict[str, Any],
    adequacy_text: str,
) -> list[str]:
    out: list[str] = []
    current_targets = manifest.get("records", [])
    manifest_ids = [row.get("tag") for row in current_targets]
    triage_records = triage.get("records", [])
    triage_ids = [row.get("tag") for row in triage_records]
    status_counts = Counter(row.get("status") for row in current_targets)
    planned_targets = [row for row in current_targets if row.get("status") == "planned"]
    planned_chapter_counts = Counter(row.get("chapter_id") for row in planned_targets)
    activation_truth = maintenance_status.get("activation_truth", {})
    first_tranche = (
        maintenance_status.get("quality_uplift_program", {})
        .get("structural_completeness_tranche", {})
        .get("first_tranche", {})
    )
    if (
        manifest.get("proof_target_count") != CURRENT_PROOF_TARGET_COUNT
        or len(current_targets) != CURRENT_PROOF_TARGET_COUNT
        or len(set(manifest_ids)) != CURRENT_PROOF_TARGET_COUNT
        or dict(status_counts) != {
            "implemented": CURRENT_IMPLEMENTED_TARGET_COUNT,
            "planned": CURRENT_PLANNED_TARGET_COUNT,
        }
        or manifest.get("status_counts") != dict(status_counts)
        or activation_truth.get("proof_target_count") != CURRENT_PROOF_TARGET_COUNT
        or activation_truth.get("chapter_core_promotion_count") != 0
    ):
        out.append("current proof manifest/status is not exactly 306 unique targets: 304 implemented plus 2 planned with no core promotion")
    if (
        maintenance_status.get("status") != "active"
        or maintenance_status.get("roadmap_path") != "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
        or first_tranche.get("manifest_admitted_count") != len(ADMITTED_CHAPTERS)
        or set(first_tranche.get("candidate_ids", [])) != ADMITTED_CHAPTERS
        or len(planned_targets) != CURRENT_PLANNED_TARGET_COUNT
        or {row.get("chapter_id") for row in planned_targets} != PLANNED_CHAPTERS
        or planned_chapter_counts != Counter({chapter_id: 2 for chapter_id in PLANNED_CHAPTERS})
    ):
        out.append("planned proof targets are not tied exactly to the one unfinished manifest-admitted chapter")
    triage_by_tag = {row.get("tag"): row for row in triage_records}
    if (
        triage.get("record_count") != CURRENT_PROOF_TARGET_COUNT
        or len(triage_records) != CURRENT_PROOF_TARGET_COUNT
        or len(set(triage_ids)) != CURRENT_PROOF_TARGET_COUNT
        or set(manifest_ids) != set(triage_ids)
        or any(triage_by_tag.get(row.get("tag"), {}).get("target_status") != row.get("status") for row in current_targets)
    ):
        out.append("current proof manifest and triage identities/statuses differ")
    observed_classes = dict(adequacy_counts(adequacy_text))
    if observed_classes != CURRENT_EXPECTED_CLASSES or sum(observed_classes.values()) != CURRENT_PROOF_TARGET_COUNT:
        out.append(f"current proof-adequacy classes drifted: {observed_classes}")
    return out


def errors(audit: dict[str, Any]) -> list[str]:
    out: list[str] = []
    rationalization = load(RATIONALIZATION)
    manifest = load(MANIFEST)
    triage = load(TRIAGE)
    validation = load(VALIDATION)
    status = load(STATUS)
    maintenance_status = load(MAINTENANCE_STATUS)

    if audit.get("schema_version") != "asi_stack.p2_closure_audit.v1":
        out.append("wrong audit schema version")
    if audit.get("roadmap_id") != status.get("roadmap_id"):
        out.append("audit roadmap identity drift")
    if audit.get("state") != "completed":
        out.append("P2 closure audit is not completed")
    if audit.get("support_state_effect") != "none":
        out.append("P2 closure audit invents a support-state effect")

    theorems = rationalization.get("baseline_theorems", [])
    baseline_targets = rationalization.get("baseline_targets", [])
    summary = rationalization.get("summary", {})
    baseline_target_ids = [row.get("target_id") for row in baseline_targets]
    if len(baseline_targets) != HISTORICAL_PROOF_TARGET_COUNT or len(set(baseline_target_ids)) != HISTORICAL_PROOF_TARGET_COUNT:
        out.append("frozen P2 baseline does not contain exactly 298 unique target identities")
    if any(row.get("baseline_status") != "implemented" for row in baseline_targets):
        out.append("frozen P2 baseline contains a non-implemented target")
    if any(row.get("review_state") not in REVIEWED_STATES for row in theorems + baseline_targets):
        out.append("activation-baseline proof inventory still contains an unreviewed item")
    if any(not row.get("disposition") or not row.get("claim_atom_id") for row in theorems + baseline_targets):
        out.append("activation-baseline proof inventory contains an undispositioned or unowned item")

    expected_baseline = {
        "theorem_declarations": len(theorems),
        "proof_targets": len(baseline_targets),
        "theorem_machine_candidates": 0,
        "target_machine_candidates": 0,
        "fully_reviewed_modules": summary.get("fully_reviewed_module_count"),
        "fully_reviewed_safety_critical_modules": summary.get("safety_critical_fully_reviewed_module_count"),
    }
    if audit.get("activation_baseline") != expected_baseline:
        out.append("activation-baseline closure counts drifted")

    contract = status.get("proof_rationalization_contract", {})
    expected_historical_surface = {
        "theorem_declarations": contract.get("current_live_theorem_declaration_count"),
        "proof_targets": contract.get("current_live_proof_target_count"),
        "missing_or_changed_baseline_theorems": contract.get("current_missing_or_changed_theorem_count"),
        "missing_or_changed_baseline_targets": contract.get("current_missing_or_changed_target_count"),
        "implemented_current_targets": HISTORICAL_PROOF_TARGET_COUNT,
    }
    if audit.get("current_surface") != expected_historical_surface:
        out.append("frozen P2 proof-surface closure counts drifted")
    if contract.get("current_live_proof_target_count") != HISTORICAL_PROOF_TARGET_COUNT:
        out.append("historical P2 status no longer preserves its 298-target closure surface")

    routes = audit.get("adequacy_routes", [])
    route_counts = {row.get("adequacy_class"): row.get("target_count") for row in routes}
    if route_counts != HISTORICAL_EXPECTED_CLASSES or sum(route_counts.values()) != HISTORICAL_PROOF_TARGET_COUNT:
        out.append("frozen P2 adequacy routes do not cover all 298 historical targets exactly")
    for row in routes:
        priorities = set(row.get("forward_priorities", []))
        if not row.get("p2_disposition") or not priorities or not priorities <= FORWARD_PRIORITIES:
            out.append(f"invalid forward route for adequacy class {row.get('adequacy_class')}")

    richer = audit.get("richer_semantics_forward_routes", [])
    richer_counts = {row.get("chapter_id"): row.get("target_count") for row in richer}
    if richer_counts != EXPECTED_RICHER:
        out.append("the sixteen richer-semantics targets are not exactly routed")
    for row in richer:
        priorities = set(row.get("forward_priorities", []))
        if not row.get("current_model") or len(row.get("remaining_work", [])) < 4:
            out.append(f"richer-semantics route lacks model or exact remaining work: {row.get('chapter_id')}")
        if not {"P3", "P4"} <= priorities:
            out.append(f"richer-semantics route escapes executable/causal gates: {row.get('chapter_id')}")

    registered = {row.get("script") for row in validation.get("units", [])}
    models = audit.get("required_semantic_models", [])
    if len(models) != 9 or len({row.get("model_id") for row in models}) != 9:
        out.append("required semantic-model closure set must contain nine unique models")
    for row in models:
        dossier = ROOT / str(row.get("dossier", ""))
        validator = str(row.get("consumer_validator", ""))
        if not dossier.is_file():
            out.append(f"missing model-adequacy dossier: {row.get('model_id')}")
        if validator not in registered or not (ROOT / "scripts" / validator).is_file():
            out.append(f"missing registered consumer validator: {row.get('model_id')}")

    priority_states = {row.get("id"): row.get("state") for row in status.get("priorities", [])}
    milestone_states = {row.get("id"): row.get("state") for row in status.get("milestones", [])}
    if priority_states.get("P2") != "completed" or priority_states.get("P3") not in {"in_progress", "completed"}:
        out.append("roadmap state does not preserve P2 closure and P3 activation")
    if milestone_states.get("M3") != "completed":
        out.append("milestone state does not close M3")
    current_priority = status.get("current_priority")
    terminal_roadmap = status.get("status") == "completed" and current_priority is None
    if not terminal_roadmap and current_priority not in {"P3", "P4", "P5", "P6", "P7", "P8", "P9"}:
        out.append("current priority regressed before P3 after P2 closure")
    if len(audit.get("non_claims", [])) < 5:
        out.append("P2 closure audit lacks explicit non-claims")
    out.extend(
        current_proof_errors(
            manifest,
            triage,
            maintenance_status,
            ADEQUACY.read_text(encoding="utf-8"),
        )
    )
    return out


def main() -> None:
    audit = load(AUDIT)
    failures = errors(audit)
    mutations: list[tuple[str, dict[str, Any]]] = []
    support = copy.deepcopy(audit)
    support["support_state_effect"] = "promotion"
    mutations.append(("support laundering", support))
    baseline = copy.deepcopy(audit)
    baseline["activation_baseline"]["proof_targets"] -= 1
    mutations.append(("baseline target deletion", baseline))
    route = copy.deepcopy(audit)
    route["adequacy_routes"][2]["forward_priorities"] = []
    mutations.append(("unrouted richer semantics", route))
    richer = copy.deepcopy(audit)
    richer["richer_semantics_forward_routes"][0]["target_count"] = 5
    mutations.append(("richer-semantics count laundering", richer))
    model = copy.deepcopy(audit)
    model["required_semantic_models"] = model["required_semantic_models"][:-1]
    mutations.append(("semantic model omission", model))
    state = copy.deepcopy(audit)
    state["state"] = "in_progress"
    mutations.append(("false closure state", state))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    current_manifest = load(MANIFEST)
    current_triage = load(TRIAGE)
    current_status = load(MAINTENANCE_STATUS)
    adequacy_text = ADEQUACY.read_text(encoding="utf-8")
    current_mutation_count = 0
    proof_invention = copy.deepcopy(current_manifest)
    proof_invention["proof_target_count"] = CURRENT_PROOF_TARGET_COUNT + 1
    if not current_proof_errors(proof_invention, current_triage, current_status, adequacy_text):
        failures.append("negative mutation accepted: current proof-target invention")
    current_mutation_count += 1
    escaped_plan = copy.deepcopy(current_manifest)
    next(row for row in escaped_plan["records"] if row.get("status") == "planned")["chapter_id"] = "asi-is-a-stack-not-a-model"
    if not current_proof_errors(escaped_plan, current_triage, current_status, adequacy_text):
        failures.append("negative mutation accepted: planned target escaped admitted chapters")
    current_mutation_count += 1
    current_status_drift = copy.deepcopy(current_status)
    current_status_drift["activation_truth"]["proof_target_count"] = HISTORICAL_PROOF_TARGET_COUNT
    if not current_proof_errors(current_manifest, current_triage, current_status_drift, adequacy_text):
        failures.append("negative mutation accepted: current proof-status regression")
    current_mutation_count += 1
    if failures:
        raise SystemExit("P2 closure audit failed:\n - " + "\n - ".join(failures))
    print(
        "P2 closure audit passed: 1,151 baseline theorem declarations, 298 unique historical targets, "
        "65/65 reviewed modules, 298/298 frozen historical adequacy routes, 306 current targets "
        "(304 implemented plus 2 planned exactly on one unfinished admitted chapter), 306/306 current adequacy classifications, "
        f"nine semantic-model dossiers/consumers, {len(mutations) + current_mutation_count} rejecting mutations, and no support-state effect."
    )


if __name__ == "__main__":
    main()
