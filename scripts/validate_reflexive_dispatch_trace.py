#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "protocol_records" / "reflexive_dispatch_trace_record.valid.json"
MANIFEST = ROOT / "book_structure.json"
SOURCE_ID = "reflexive_router_whitepaper"
CHAPTERS = {
    "routing-heads-and-specialist-cores",
    "intent-to-execution-contracts",
    "planning-as-a-control-layer",
    "stable-capability-fields",
    "virtual-context-abi",
    "context-transactions-snapshots-mounts-and-taint",
    "claim-ledgers-and-belief-revision",
    "runtime-adapters-tool-permissions-and-human-approval",
    "procedural-memory-and-cognitive-loop-closure",
    "resource-economics-and-token-budgets",
    "benchmark-ratchets-and-anti-goodhart-evidence",
    "integrated-reference-architecture",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if row.get("source_id") != SOURCE_ID:
        errors.append("source identity drift")
    event = row.get("event", {})
    ingress = row.get("ingress", {})
    if event.get("authenticated") is not True or not event.get("authority_ref"):
        errors.append("event is unauthenticated or lacks an authority reference")
    if ingress.get("mode") in {"forced_route", "direct_command", "compiled_workflow"} and ingress.get("command_authenticated") is not True:
        errors.append("command-like ingress is unauthenticated")
    if ingress.get("inference_bypassed") is True and ingress.get("mode") == "automatic":
        errors.append("automatic ingress silently bypasses routing inference")

    proposals = {item.get("proposal_id"): item for item in row.get("proposals", [])}
    if len(proposals) != len(row.get("proposals", [])) or not proposals:
        errors.append("proposal identities are empty or duplicated")
    qualifications = {item.get("proposal_id"): item for item in row.get("qualification", [])}
    if set(qualifications) != set(proposals):
        errors.append("qualification does not exactly cover route proposals")
    for proposal_id, qualification in qualifications.items():
        if qualification.get("capability_id") != proposals[proposal_id].get("capability_id"):
            errors.append("qualification changes the proposed capability identity")
        if qualification.get("qualified") is True and qualification.get("failures"):
            errors.append("qualified proposal retains blocking failures")

    selection = row.get("selection", {})
    selected = selection.get("selected_proposal_ids", [])
    if any(item not in proposals or qualifications.get(item, {}).get("qualified") is not True or proposals.get(item, {}).get("ood") is True for item in selected):
        errors.append("selection contains absent, unqualified, or OOD proposals")
    if selection.get("fallback_used") is True and ingress.get("fallback_policy") == "no_fallback":
        errors.append("silent fallback violates the ingress contract")
    nodes = row.get("plan_nodes", [])
    if selection.get("kind") == "atomic" and (len(selected) != 1 or len(nodes) != 1):
        errors.append("atomic selection is not one proposal and one node")
    if selection.get("kind") == "dag" and (len(selected) < 2 or len(nodes) < 2):
        errors.append("DAG selection lacks multiple qualified proposals and nodes")
    if selection.get("kind") == "none" and (selected or nodes):
        errors.append("no-route selection still contains dispatched work")

    effect = row.get("effect", {})
    result = row.get("result", {})
    material_states = {"committed", "observed", "verified", "partial", "rolled_back", "compensated", "quarantined", "unknown"}
    if effect.get("required") is True:
        if effect.get("state") == "not_required" or not effect.get("authority_ref") or not effect.get("receipt_ref"):
            errors.append("required effect bypasses authority or receipt custody")
        if result.get("effect_receipt_ref") != effect.get("receipt_ref"):
            errors.append("typed result loses the effect receipt")
    elif effect.get("state") != "not_required":
        errors.append("non-effect path claims a material effect state")
    if effect.get("state") in material_states and not effect.get("receipt_ref"):
        errors.append("material or indeterminate effect lacks a receipt")
    if not result.get("dispatch_provenance_ref") or not result.get("authoritative_artifact_ref"):
        errors.append("typed result loses dispatch or artifact provenance")

    chronicle = row.get("chronicle", {})
    if not chronicle.get("transaction_time") or not chronicle.get("valid_time") or not chronicle.get("record_refs"):
        errors.append("Chronicle update loses bitemporal or record identity")
    compilation = row.get("compilation", {})
    if compilation.get("state") in {"candidate", "shadow", "qualified"}:
        if len(compilation.get("source_trace_refs", [])) < 2 or not compilation.get("negative_case_refs") or not compilation.get("differential_test_ref"):
            errors.append("reflex compilation lacks repeated traces, negative space, or differential evidence")
    if not compilation.get("expiry") or not compilation.get("decompilation_route"):
        errors.append("reflex lifecycle lacks expiry or decompilation")
    if row.get("support_state_effect") != "none" or len(row.get("non_claims", [])) < 5:
        errors.append("fixture launders support or omits non-claims")
    return errors


def main() -> None:
    failures: list[str] = []
    value = load(FIXTURE)
    failures.extend(semantic_errors(value))

    manifest = load(MANIFEST)
    assigned = {
        chapter["id"]
        for part in manifest["parts"]
        for chapter in part["chapters"]
        if SOURCE_ID in chapter.get("source_ids", [])
    }
    if assigned != CHAPTERS:
        failures.append(f"manifest source assignment drift: {sorted(assigned)}")
    for chapter_id in CHAPTERS:
        chapter = next(chapter for part in manifest["parts"] for chapter in part["chapters"] if chapter["id"] == chapter_id)
        prose = (ROOT / chapter["file"]).read_text(encoding="utf-8")
        if prose.count(SOURCE_ID) < 2 or "The Reflexive Router" not in prose:
            failures.append(f"chapter lacks source metadata and prose integration: {chapter_id}")

    mutations: list[tuple[str, Any]] = [
        ("unauthenticated event", lambda row: row["event"].__setitem__("authenticated", False)),
        ("unauthenticated forced route", lambda row: row["ingress"].__setitem__("command_authenticated", False)),
        ("selected unqualified route", lambda row: row["qualification"][0].__setitem__("qualified", False)),
        ("silent fallback", lambda row: row["selection"].__setitem__("fallback_used", True)),
        ("effect authority bypass", lambda row: row["effect"].__setitem__("authority_ref", "")),
        ("effect receipt loss", lambda row: row["result"].__setitem__("effect_receipt_ref", "effect://other")),
        ("dispatch provenance loss", lambda row: row["result"].__setitem__("dispatch_provenance_ref", "")),
        ("premature reflex qualification", lambda row: row["compilation"].__setitem__("state", "qualified")),
        ("support laundering", lambda row: row.__setitem__("support_state_effect", "promotion")),
        ("source substitution", lambda row: row.__setitem__("source_id", "other")),
        ("one-node DAG", lambda row: row["selection"].__setitem__("kind", "dag")),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        if not semantic_errors(candidate):
            failures.append(f"negative mutation accepted: {label}")

    if failures:
        raise SystemExit("Reflexive dispatch trace validation failed:\n - " + "\n - ".join(failures))
    print(
        "Reflexive dispatch trace passed: one schema-bound non-evidentiary trace, "
        "twelve chapter integrations, proposal/admission and inference/enforcement separation, "
        "typed effect/result/Chronicle custody, guarded compilation, eleven rejecting mutations, "
        "and no support-state effect."
    )


if __name__ == "__main__":
    main()
