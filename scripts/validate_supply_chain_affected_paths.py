#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "supply_chain_affected_path_record.schema.json"
VALID = ROOT / "tests" / "fixtures" / "protocol_records" / "supply_chain_affected_path_record.valid.json"
MUTATIONS = ROOT / "experiments" / "supply_chain_affected_paths" / "fixtures"
EXPECTED_SOURCES = {"cca_project", "moecot_manifest_project", "corbens_trainer_project"}
LEAN = ROOT / "lean" / "AsiStackProofs" / "SupplyChainIntegrity.lean"
LIFECYCLE_THEOREMS = {
    "accepted_supply_chain_step_is_valid",
    "accepted_supply_chain_step_applies_event",
    "apply_supply_chain_event_preserves_identity",
    "accepted_supply_chain_step_preserves_non_authority",
    "accepted_supply_chain_step_respects_authority_ceiling",
    "successful_supply_chain_run_preserves_identity",
    "successful_supply_chain_run_preserves_non_authority",
    "successful_supply_chain_run_respects_authority_ceiling",
    "successful_supply_chain_run_has_valid_trace",
    "supply_chain_run_composes",
    "quarantined_artifact_cannot_be_admitted",
    "accepted_admission_requires_clean_review",
    "accepted_admission_records_authority_and_receipt",
    "accepted_revocation_zeros_authority_and_records_invalidation",
    "admitted_then_revoked_run_reaches_zero_authority",
    "critical_advisory_run_reaches_quarantine",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def reachable(subject: str, edges: list[dict[str, Any]]) -> set[str]:
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        adjacency.setdefault(edge.get("from_node", ""), set()).add(edge.get("to_node", ""))
    closure = {subject}
    frontier = [subject]
    while frontier:
        node = frontier.pop()
        for descendant in adjacency.get(node, set()):
            if descendant not in closure:
                closure.add(descendant)
                frontier.append(descendant)
    return closure


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(record.get("source_ids", [])) != EXPECTED_SOURCES:
        errors.append("supply-chain lineage must name the three historical-project sources exactly")

    nodes = record.get("nodes", [])
    node_ids = [row.get("node_id") for row in nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("supply-chain node identities must be unique")
    node_map = {row.get("node_id"): row for row in nodes}
    requested = record.get("requested_artifact", {})
    requested_node = node_map.get(requested.get("node_id"))
    if not requested_node or requested_node.get("digest") != requested.get("digest") or requested_node.get("declared_name") != requested.get("declared_name"):
        errors.append("requested artifact name and digest must bind to one graph node")

    for edge in record.get("edges", []):
        if edge.get("from_node") not in node_map or edge.get("to_node") not in node_map:
            errors.append("every supply-chain edge must bind two declared nodes")
    for reference in record.get("assurance_references", []):
        if reference.get("subject_node") not in node_map:
            errors.append("every assurance reference must bind a declared node")
        if instant(reference["expires_at"]) <= instant(reference["observed_at"]):
            errors.append("assurance references must expire after observation")
        if not reference.get("limitations"):
            errors.append("assurance references must preserve bounded limitations")

    event = record.get("invalidation_event", {})
    if event.get("event_id") == event.get("prior_event_ref"):
        errors.append("invalidation must append a distinct event rather than overwrite history")
    subject = event.get("subject_node")
    if subject not in node_map:
        errors.append("invalidation subject must bind a declared node")
    expected_closure = reachable(subject, record.get("edges", [])) if subject in node_map else set()
    declared_closure = set(record.get("declared_affected_closure", []))
    if declared_closure != expected_closure:
        errors.append("declared affected closure must equal the full reachable downstream path")

    routes = record.get("response_routes", [])
    route_ids = [row.get("node_id") for row in routes]
    if len(route_ids) != len(set(route_ids)) or set(route_ids) != declared_closure:
        errors.append("every affected node must have exactly one owned response route")
    if any(row.get("ordinary_use_allowed") for row in routes):
        errors.append("invalidated affected paths cannot retain ordinary use")

    admission = record.get("admission", {})
    if event.get("invalidates_admission"):
        if admission.get("decision") not in {"repair", "review", "quarantined", "blocked"}:
            errors.append("an invalidating event cannot remain eligible for custody review")
        if admission.get("custody_review_allowed") or admission.get("readiness_review_allowed"):
            errors.append("invalidating affected paths must block custody and readiness review")
    bad_refs = [ref for ref in record.get("assurance_references", []) if ref.get("state") in {"unverified", "stale", "revoked", "unresolved"}]
    if bad_refs and (admission.get("custody_review_allowed") or admission.get("decision") == "eligible_for_custody_review"):
        errors.append("stale, unverified, revoked, or unresolved assurances cannot pass admission")
    if node_map.get(subject, {}).get("state") in {"invalidated", "revoked"} and admission.get("decision") != "quarantined":
        errors.append("a revoked or invalidated subject must quarantine the requested path")
    if admission.get("support_state_effect") == "eligible_for_bounded_evidence_review":
        errors.append("hand-authored supply-chain fixtures cannot promote support")

    closure = record.get("lifecycle_closure", {})
    if not all(closure.get(field) for field in ("residual_owner_ref", "retention_until", "disposal_or_retirement_ref", "next_review_trigger")):
        errors.append("lifecycle closure requires residual owner, retention, disposal, and re-review trigger")
    if instant(closure["retention_until"]) <= instant(event["observed_at"]):
        errors.append("retention must extend beyond the invalidation observation")
    if not record.get("promotion_blockers") or not record.get("non_claims"):
        errors.append("supply-chain record must preserve blockers and non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    if mutation["operation"] == "batch_set":
        for change in mutation["changes"]:
            target: Any = value
            for segment in change["path"][:-1]:
                target = target[segment]
            target[change["path"][-1]] = change["value"]
        return value
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    leaf = mutation["path"][-1]
    operation = mutation["operation"]
    if operation == "set":
        target[leaf] = mutation["value"]
    elif operation == "delete":
        del target[leaf]
    elif operation == "append":
        target[leaf].append(mutation["value"])
    else:
        raise ValueError(f"unsupported mutation operation {operation!r}")
    return value


def validate_lean_surface() -> None:
    text = LEAN.read_text(encoding="utf-8")
    theorems = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", text, re.MULTILINE))
    if len(theorems) != 23:
        raise SystemExit(f"Supply-chain Lean surface must contain exactly 23 theorems, found {len(theorems)}.")
    missing = sorted(LIFECYCLE_THEOREMS - theorems)
    if missing:
        raise SystemExit(f"Supply-chain Lean lifecycle theorem(s) missing: {missing}")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/SupplyChainIntegrity.lean"],
        cwd=ROOT / "lean",
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise SystemExit(
            "Supply-chain Lean recompilation failed:\n"
            + completed.stdout
            + completed.stderr
        )


def lifecycle_step(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any] | None:
    identity_fields = ("artifact_id", "artifact_digest", "lineage_id", "supplier_id", "build_id")
    if any(event[field] != state[field] for field in identity_fields):
        return None
    if event["requested_authority"] > state["authority_ceiling"]:
        return None
    if event["support_requested"] or event["external_effect_authority_requested"]:
        return None
    if not event["revocation_path"] or not event["residual_owner"] or not event["non_claim_boundary"]:
        return None
    transition = (state["stage"], event["kind"])
    if transition == ("received", "bind_provenance"):
        if not event["signature_verified"] or not event["inventory_complete"]:
            return None
        next_stage = "provenance_bound"
    elif transition == ("provenance_bound", "review_clean"):
        if not event["independent_review"] or event["critical_advisory"]:
            return None
        next_stage = "reviewed_clean"
    elif transition == ("provenance_bound", "review_critical"):
        if not event["independent_review"] or not event["critical_advisory"]:
            return None
        next_stage = "quarantined"
    elif transition == ("reviewed_clean", "admit"):
        next_stage = "admitted"
    elif transition == ("admitted", "revoke"):
        next_stage = "revoked"
    else:
        return None
    next_state = deepcopy(state)
    next_state["stage"] = next_stage
    if event["kind"] == "admit":
        next_state["active_authority"] = event["requested_authority"]
        next_state["admission_receipts"] += 1
    if event["kind"] == "revoke":
        next_state["active_authority"] = 0
        next_state["invalidation_receipts"] += 1
    return next_state


def validate_lifecycle_consumer() -> int:
    initial = {
        "stage": "received",
        "artifact_id": 10,
        "artifact_digest": 20,
        "lineage_id": 30,
        "supplier_id": 40,
        "build_id": 50,
        "authority_ceiling": 3,
        "active_authority": 0,
        "admission_receipts": 0,
        "invalidation_receipts": 0,
        "support_count": 0,
        "external_effect_authority_count": 0,
    }

    def event(kind: str, **changes: Any) -> dict[str, Any]:
        value = {
            "kind": kind,
            "artifact_id": 10,
            "artifact_digest": 20,
            "lineage_id": 30,
            "supplier_id": 40,
            "build_id": 50,
            "requested_authority": 2,
            "signature_verified": True,
            "inventory_complete": True,
            "independent_review": True,
            "critical_advisory": False,
            "revocation_path": True,
            "residual_owner": True,
            "non_claim_boundary": True,
            "support_requested": False,
            "external_effect_authority_requested": False,
        }
        value.update(changes)
        return value

    state = deepcopy(initial)
    for item in (
        event("bind_provenance"),
        event("review_clean"),
        event("admit"),
        event("revoke"),
    ):
        state = lifecycle_step(state, item)
        if state is None:
            raise SystemExit("Independent supply-chain clean lifecycle did not close.")
    identity_fields = ("artifact_id", "artifact_digest", "lineage_id", "supplier_id", "build_id", "authority_ceiling")
    if any(state[field] != initial[field] for field in identity_fields):
        raise SystemExit("Independent supply-chain lifecycle changed artifact or provenance identity.")
    if state["stage"] != "revoked" or state["active_authority"] != 0:
        raise SystemExit("Independent supply-chain lifecycle did not revoke authority.")
    if state["admission_receipts"] != 1 or state["invalidation_receipts"] != 1:
        raise SystemExit("Independent supply-chain lifecycle lost admission or invalidation receipt accounting.")
    if state["support_count"] != 0 or state["external_effect_authority_count"] != 0:
        raise SystemExit("Independent supply-chain lifecycle assigned support or external-effect authority.")

    critical = lifecycle_step(initial, event("bind_provenance"))
    critical = lifecycle_step(critical, event("review_critical", critical_advisory=True)) if critical else None
    if critical is None or critical["stage"] != "quarantined":
        raise SystemExit("Independent critical-advisory lifecycle did not quarantine.")

    reviewed = lifecycle_step(initial, event("bind_provenance"))
    reviewed = lifecycle_step(reviewed, event("review_clean")) if reviewed else None
    controls = [
        (initial, event("bind_provenance", artifact_digest=21)),
        (initial, event("bind_provenance", requested_authority=4)),
        (initial, event("bind_provenance", support_requested=True)),
        (initial, event("bind_provenance", external_effect_authority_requested=True)),
        (initial, event("bind_provenance", signature_verified=False)),
        (reviewed, event("review_critical", critical_advisory=False)),
        (critical, event("admit")),
        (reviewed, event("admit", revocation_path=False)),
    ]
    if any(candidate is not None and lifecycle_step(candidate, item) is not None for candidate, item in controls):
        raise SystemExit("Independent supply-chain lifecycle accepted a rejecting control.")
    return len(controls)


def main() -> None:
    validate_lean_surface()
    lifecycle_controls = validate_lifecycle_consumer()
    schema = load(SCHEMA)
    valid = load(VALID)
    errors = validate_value(valid, schema, str(VALID.relative_to(ROOT))) + semantic_errors(valid)
    if errors:
        raise SystemExit("Valid supply-chain affected-path record failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No supply-chain affected-path mutations found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(valid, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(
        "Supply-chain affected-path harness passed: exact 23-theorem Lean surface recompiled; "
        f"1 quarantined three-project record, {len(mutations)} fixture mutations, and "
        f"{lifecycle_controls} lifecycle controls rejected."
    )


if __name__ == "__main__":
    main()
