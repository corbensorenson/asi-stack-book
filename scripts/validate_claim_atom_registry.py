#!/usr/bin/env python3
"""Validate P1 claim coverage without confusing generated candidates for review."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from build_claim_atom_registry import build


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "evidence_quality/claim_atom_registry.json"
QUEUE_PATH = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
REVIEWS_PATH = ROOT / "evidence_quality/claim_atom_reviews.json"
STATUS_PATH = ROOT / "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
STRUCTURE_PATH = ROOT / "book_structure.json"
REGISTRY_SCHEMA = ROOT / "schemas/claim_atom_registry.schema.json"
QUEUE_SCHEMA = ROOT / "schemas/prose_claim_candidate_queue.schema.json"
REVIEWS_SCHEMA = ROOT / "schemas/claim_atom_reviews.schema.json"
CHAPTER_REVIEW_SCHEMA = ROOT / "schemas/claim_chapter_review.schema.json"
POST_ACTIVATION_EXPANSION_IDS = {
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "human-factors-and-meaningful-control-in-oversight",
    "governed-world-models-and-reality-grounding",
    "white-box-evidence-interpretability-and-activation-governance",
    "governed-operations-incident-command-and-graceful-degradation",
    "governed-model-training-distributed-optimization-and-scaling",
}
POST_ACTIVATION_FORMAL_TARGETS = {"lean:corrigibility.agency.generic_countermodel_routes"}

def accepted_upward_states() -> dict[str, str]:
    states: dict[str, str] = {}
    for path in (ROOT / "evidence_transitions").rglob("*.json"):
        try:
            row = load(path)
        except Exception:
            continue
        if row.get("review_status") == "accepted" and row.get("transition_effect") == "upward":
            states[str(row.get("claim_id"))] = str(row.get("new_support_state"))
    return states


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter.get("id") not in POST_ACTIVATION_EXPANSION_IDS
    ]


def expected_role_counts(structure: dict[str, Any]) -> Counter[str]:
    result: Counter[str] = Counter()
    for chapter in chapters(structure):
        result.update({"core": 1, "problem": 1, "insufficiency": 1, "minimum": 1, "beyond_sota": 1})
        result["mechanism"] += len(chapter.get("mechanism", []))
        result["interface"] += len(chapter.get("interfaces", []))
        result["invariant"] += len(chapter.get("invariants", []))
        result["failure_mode"] += len(chapter.get("failure_modes", []))
        result["formal_target"] += sum(
            row.get("tag") not in POST_ACTIVATION_FORMAL_TARGETS
            for row in chapter.get("proof_targets", [])
        )
    return result


def errors(data: dict[str, Any], *, check_generation: bool = True) -> list[str]:
    out: list[str] = []
    registry = data["registry"]
    queue = data["queue"]
    reviews = data["reviews"]
    review_packets = data["review_packets"]
    status = data["status"]
    structure = data["structure"]
    for name, value, schema in (
        ("registry", registry, data["registry_schema"]),
        ("queue", queue, data["queue_schema"]),
        ("reviews", reviews, data["reviews_schema"]),
    ):
        try:
            jsonschema.Draft202012Validator(schema).validate(value)
        except jsonschema.ValidationError as exc:
            out.append(f"{name} schema: {exc.message}")
    for path, packet in review_packets.items():
        try:
            jsonschema.Draft202012Validator(data["chapter_review_schema"]).validate(packet)
        except jsonschema.ValidationError as exc:
            out.append(f"{path} schema: {exc.message}")

    chapter_rows = chapters(structure)
    chapter_ids = [row["id"] for row in chapter_rows]
    manifest = {row["id"]: row for row in chapter_rows}
    atoms = registry.get("atoms", [])
    candidates = queue.get("candidates", [])
    atom_ids = [row.get("atom_id") for row in atoms]
    candidate_ids = [row.get("candidate_id") for row in candidates]
    by_id = {row.get("atom_id"): row for row in atoms}
    if len(atom_ids) != len(set(atom_ids)):
        out.append("atom IDs are duplicated")
    if len(candidate_ids) != len(set(candidate_ids)):
        out.append("prose candidate IDs are duplicated")

    role_counts = Counter(row.get("role") for row in atoms if row.get("role") != "prose")
    expected = expected_role_counts(structure)
    if role_counts != expected:
        out.append(f"structured role coverage drifted: expected {dict(expected)}, got {dict(role_counts)}")
    if registry.get("summary", {}).get("atom_count") != len(atoms):
        out.append("registry atom summary does not match exact rows")
    if queue.get("summary", {}).get("candidate_count") != len(candidates):
        out.append("prose candidate summary does not match exact rows")
    if registry.get("summary", {}).get("prose_candidate_count") != len(candidates):
        out.append("registry and prose queue candidate counts disagree")
    if set(row.get("chapter_id") for row in atoms) != set(chapter_ids):
        out.append("atom registry does not cover exactly the manifest chapter set")
    if set(row.get("chapter_id") for row in candidates) != set(chapter_ids):
        out.append("prose queue does not cover exactly the manifest chapter set")

    packet_chapters = [packet.get("chapter_id") for packet in review_packets.values()]
    if len(packet_chapters) != len(set(packet_chapters)):
        out.append("chapter semantic-review packets duplicate ownership")
    unknown_packet_chapters = sorted(set(packet_chapters) - set(chapter_ids))
    if unknown_packet_chapters:
        out.append(f"chapter review packets name unknown chapters: {unknown_packet_chapters}")
    completed_sweeps = 0
    atoms_by_chapter: dict[str, list[dict[str, Any]]] = {chapter_id: [] for chapter_id in chapter_ids}
    candidates_by_chapter: dict[str, list[dict[str, Any]]] = {chapter_id: [] for chapter_id in chapter_ids}
    accepted_states = accepted_upward_states()
    for atom in atoms:
        atoms_by_chapter.setdefault(str(atom.get("chapter_id")), []).append(atom)
    for candidate in candidates:
        candidates_by_chapter.setdefault(str(candidate.get("chapter_id")), []).append(candidate)
    for path, packet in review_packets.items():
        chapter_id = packet.get("chapter_id")
        sweep = packet.get("semantic_sweep", {})
        if any(not str(atom_id).startswith(f"{chapter_id}.") for atom_id in packet.get("atom_reviews", {})):
            out.append(f"{path}: atom review escapes chapter ownership")
        if any(not str(candidate_id).startswith(f"{chapter_id}.prose.") for candidate_id in packet.get("prose_candidate_dispositions", {})):
            out.append(f"{path}: prose disposition escapes chapter ownership")
        current_candidate_ids = {
            str(row.get("candidate_id"))
            for row in candidates_by_chapter.get(chapter_id, [])
        }
        retired_ids: set[str] = set()
        for lineage in packet.get("prose_review_lineage", []):
            retired_id = str(lineage.get("retired_candidate_id", ""))
            if retired_id in retired_ids:
                out.append(f"{path}: prose review lineage duplicates retired ID {retired_id}")
            retired_ids.add(retired_id)
            if not retired_id.startswith(f"{chapter_id}.prose."):
                out.append(f"{path}: retired prose review escapes chapter ownership")
            normalized = re.sub(
                r"[^a-z0-9]+",
                " ",
                str(lineage.get("retired_sentence", "")).casefold(),
            ).strip()
            expected_id = f"{chapter_id}.prose.{hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:12]}"
            if retired_id != expected_id:
                out.append(f"{path}: retired prose ID does not match its preserved sentence: {retired_id}")
            if retired_id in current_candidate_ids:
                out.append(f"{path}: current prose candidate is incorrectly recorded as retired: {retired_id}")
            for replacement_id in lineage.get("replacement_candidate_ids", []):
                if replacement_id not in current_candidate_ids:
                    out.append(f"{path}: prose lineage replacement is not a current chapter candidate: {replacement_id}")
            preserved = lineage.get("preserved_disposition", {})
            if preserved.get("state") == "duplicate_of_atom":
                target = preserved.get("target_atom_id")
                if not target or target not in by_id:
                    out.append(f"{path}: retired duplicate prose review lacks a valid preserved target atom")
        if packet.get("review_state") == "completed":
            completed_sweeps += 1
            structured_count = sum(row.get("role") != "prose" for row in atoms_by_chapter.get(chapter_id, []))
            prose_count = len(candidates_by_chapter.get(chapter_id, []))
            if sweep.get("structured_atoms_reviewed") != structured_count:
                out.append(f"{path}: completed structured review count differs from registry")
            if sweep.get("prose_candidates_adjudicated") != prose_count:
                out.append(f"{path}: completed prose review count differs from queue")
            if sweep.get("unowned_material_claims") != 0:
                out.append(f"{path}: completed sweep retains unowned material claims")
            if any(row.get("review_state") == "machine_candidate" for row in atoms_by_chapter.get(chapter_id, [])):
                out.append(f"{path}: completed sweep retains machine candidate atoms")
            if any(row.get("review_state") == "pending_materiality_adjudication" for row in candidates_by_chapter.get(chapter_id, [])):
                out.append(f"{path}: completed sweep retains pending prose candidates")

    for chapter_id in chapter_ids:
        core_id = f"{chapter_id}.core"
        core = by_id.get(core_id)
        if not core:
            out.append(f"{core_id}: missing core atom")
            continue
        chapter = manifest[chapter_id]
        if core.get("proposition") != chapter.get("core_claim"):
            out.append(f"{core_id}: proposition differs from manifest")
        if core.get("owner") != chapter_id:
            out.append(f"{core_id}: owner differs from canonical chapter")
        if core.get("claim_label") != chapter.get("claim_label") or core.get("support_state") != chapter.get("evidence_level"):
            out.append(f"{core_id}: label/support differs from manifest")

    placeholders = ("semantic_review_required", "generated assumption placeholder", "semantic review must confirm")
    for atom in atoms:
        atom_id = str(atom.get("atom_id", ""))
        if atom.get("owner") != atom.get("chapter_id"):
            out.append(f"{atom_id}: duplicate or noncanonical owner")
        proposition = str(atom.get("proposition", "")).strip().casefold()
        falsifier = str(atom.get("falsifier", "")).strip().casefold()
        counter = str(atom.get("strongest_counterclaim", "")).strip().casefold()
        if not falsifier or falsifier == proposition or falsifier == counter:
            out.append(f"{atom_id}: falsifier is blank or tautological")
        lanes = [row.get("lane") for row in atom.get("required_lanes", [])]
        if len(lanes) != len(set(lanes)):
            out.append(f"{atom_id}: duplicate evidence lanes")
        if atom.get("support_state") not in {"unsupported", "argument", "deprecated", "refuted"} and accepted_states.get(atom_id) != atom.get("support_state"):
            out.append(f"{atom_id}: support promotion lacks an accepted transition in P1")
        if atom.get("review_state") != "machine_candidate":
            blob = json.dumps(atom, ensure_ascii=False).casefold()
            for placeholder in placeholders:
                if placeholder in blob:
                    out.append(f"{atom_id}: reviewed atom retains placeholder {placeholder!r}")
            if atom.get("proposition_type") == "untyped":
                out.append(f"{atom_id}: reviewed material claim remains untyped")

    allowed_candidate_states = {"pending_materiality_adjudication", "material_atom", "nonmaterial_explanation", "duplicate_of_atom", "editorial_or_question", "historical_or_source_report"}
    for row in candidates:
        if row.get("review_state") not in allowed_candidate_states:
            out.append(f"{row.get('candidate_id')}: invalid materiality disposition")
        if row.get("review_state") != "pending_materiality_adjudication" and not str(row.get("disposition_rationale") or "").strip():
            out.append(f"{row.get('candidate_id')}: adjudicated prose candidate lacks rationale")
        if row.get("review_state") == "material_atom" and row.get("candidate_id") not in by_id:
            out.append(f"{row.get('candidate_id')}: material prose claim has no atom")
        if row.get("review_state") == "duplicate_of_atom":
            target = row.get("target_atom_id")
            if not target or target not in by_id:
                out.append(f"{row.get('candidate_id')}: duplicate disposition lacks a valid target atom")

    atom_review_counts = Counter(row.get("review_state") for row in atoms)
    prose_review_counts = Counter(row.get("review_state") for row in candidates)
    summary = registry.get("summary", {})
    if summary.get("review_state_counts") != dict(sorted(atom_review_counts.items())):
        out.append("atom review-state summary drifted")
    if summary.get("prose_review_state_counts") != dict(sorted(prose_review_counts.items())):
        out.append("prose review-state summary drifted")
    program = status.get("p1_claim_atom_program", {})
    exact_status = {
        "structured_atom_count": len(atoms),
        "structured_machine_candidate_count": atom_review_counts.get("machine_candidate", 0),
        "prose_candidate_count": len(candidates),
        "pending_prose_candidate_count": prose_review_counts.get("pending_materiality_adjudication", 0),
        "chapter_dossier_count": len(review_packets),
        "semantic_chapter_sweep_completed_count": completed_sweeps,
    }
    for key, value in exact_status.items():
        if program.get(key) != value:
            out.append(f"P1 machine status drifted: {key} expected {value}, got {program.get(key)}")
    p1_state = next((row.get("state") for row in status.get("priorities", []) if row.get("id") == "P1"), None)
    m1_state = next((row.get("state") for row in status.get("milestones", []) if row.get("id") == "M1"), None)
    completed = p1_state == "completed" or m1_state == "completed" or program.get("state") == "completed"
    if completed:
        if atom_review_counts.get("machine_candidate", 0) or prose_review_counts.get("pending_materiality_adjudication", 0):
            out.append("P1 completion launders unreviewed structured atoms or prose candidates")
        if program.get("semantic_chapter_sweep_completed_count") != 54:
            out.append("P1 completion lacks 54 semantic chapter sweeps")
        if any(row.get("review_state") not in {"semantically_reviewed", "campaign_frozen", "terminally_adjudicated"} for row in atoms):
            out.append("P1 completion retains an unreviewed material atom")
    elif (p1_state, m1_state, program.get("state")) != ("in_progress", "in_progress", "in_progress"):
        out.append("P1/M1/program must move together while claim atomization is in progress")
    if program.get("support_state_effect") != "none" or summary.get("support_state_effect") != "none":
        out.append("P1 invented a support-state effect")

    if check_generation:
        try:
            expected_registry, expected_queue, expected_report, expected_dossiers = build()
        except Exception as exc:  # noqa: BLE001 - exact diagnostic belongs in validator output
            out.append(f"claim-atom regeneration failed: {exc}")
        else:
            if registry != expected_registry or queue != expected_queue:
                out.append("generated registry or queue is stale")
            report_path = ROOT / "docs/claim_atom_registry.md"
            if not report_path.exists() or report_path.read_text(encoding="utf-8") != expected_report:
                out.append("readable claim registry is stale")
            for chapter_id, body in expected_dossiers.items():
                path = ROOT / "evidence_quality/claim_dossiers" / f"{chapter_id}.md"
                if not path.exists() or path.read_text(encoding="utf-8") != body:
                    out.append(f"{chapter_id}: claim dossier is stale")
                    break
    return out


def snapshot() -> dict[str, Any]:
    return {
        "registry": load(REGISTRY_PATH),
        "queue": load(QUEUE_PATH),
        "reviews": load(REVIEWS_PATH),
        "status": load(STATUS_PATH),
        "structure": load(STRUCTURE_PATH),
        "registry_schema": load(REGISTRY_SCHEMA),
        "queue_schema": load(QUEUE_SCHEMA),
        "reviews_schema": load(REVIEWS_SCHEMA),
        "chapter_review_schema": load(CHAPTER_REVIEW_SCHEMA),
        "review_packets": {
            path: load(ROOT / path)
            for path in load(REVIEWS_PATH).get("review_files", [])
        },
    }


def main() -> None:
    base = snapshot()
    failures = errors(base)
    mutations: list[tuple[str, dict[str, Any]]] = []

    missing_core = copy.deepcopy(base)
    missing_core["registry"]["atoms"] = [row for row in missing_core["registry"]["atoms"] if row["atom_id"] != "asi-is-a-stack-not-a-model.core"]
    mutations.append(("missing core atom", missing_core))

    duplicate_owner = copy.deepcopy(base)
    duplicate_owner["registry"]["atoms"][0]["owner"] = "the-efficient-asi-hypothesis"
    mutations.append(("owner laundering", duplicate_owner))

    blank_falsifier = copy.deepcopy(base)
    blank_falsifier["registry"]["atoms"][0]["falsifier"] = ""
    mutations.append(("blank falsifier", blank_falsifier))

    tautology = copy.deepcopy(base)
    tautology["registry"]["atoms"][0]["falsifier"] = tautology["registry"]["atoms"][0]["proposition"]
    mutations.append(("tautological falsifier", tautology))

    lane = copy.deepcopy(base)
    lane["registry"]["atoms"][0]["required_lanes"].append(copy.deepcopy(lane["registry"]["atoms"][0]["required_lanes"][0]))
    mutations.append(("duplicate lane", lane))

    promotion = copy.deepcopy(base)
    promotion["registry"]["atoms"][0]["support_state"] = "empirical-test-backed"
    mutations.append(("unsupported P1 promotion", promotion))

    false_completion = copy.deepcopy(base)
    false_completion["registry"]["atoms"][0]["review_state"] = "machine_candidate"
    false_completion["registry"]["summary"]["review_state_counts"]["semantically_reviewed"] -= 1
    false_completion["registry"]["summary"]["review_state_counts"]["machine_candidate"] = 1
    false_completion["status"]["p1_claim_atom_program"]["structured_machine_candidate_count"] = 1
    mutations.append(("completion with candidates", false_completion))

    missing_prose = copy.deepcopy(base)
    missing_prose["queue"]["candidates"] = missing_prose["queue"]["candidates"][:-1]
    mutations.append(("missing prose candidate", missing_prose))

    scope = copy.deepcopy(base)
    scope_index = next(
        (
            index
            for index, row in enumerate(scope["registry"]["atoms"])
            if row.get("review_state") == "machine_candidate"
        ),
        0,
    )
    scope["registry"]["atoms"][scope_index]["review_state"] = "semantically_reviewed"
    scope["registry"]["atoms"][scope_index]["scope"]["population"] = "semantic_review_required"
    mutations.append(("reviewed scope placeholder", scope))

    summary = copy.deepcopy(base)
    summary["registry"]["summary"]["atom_count"] += 1
    mutations.append(("summary inflation", summary))

    support = copy.deepcopy(base)
    support["status"]["p1_claim_atom_program"]["support_state_effect"] = "promotion"
    mutations.append(("support-effect invention", support))

    lineage_path = "evidence_quality/claim_reviews/artifact-graphs-audit-logs-and-replay.json"
    lineage_hash = copy.deepcopy(base)
    lineage_hash["review_packets"][lineage_path]["prose_review_lineage"][0]["retired_sentence"] += " changed"
    mutations.append(("retired prose hash laundering", lineage_hash))

    lineage_replacement = copy.deepcopy(base)
    lineage_replacement["review_packets"][lineage_path]["prose_review_lineage"][0]["replacement_candidate_ids"] = [
        "artifact-graphs-audit-logs-and-replay.prose.000000000000"
    ]
    mutations.append(("noncurrent prose lineage replacement", lineage_replacement))

    for label, candidate in mutations:
        if not errors(candidate, check_generation=False):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Claim-atom registry validation failed:\n - " + "\n - ".join(failures))
    print(
        f"Claim-atom registry passed: {len(base['registry']['atoms'])} structured atoms, "
        f"{len(base['queue']['candidates'])} prose candidates, 54 generated dossiers, "
        "P1/M1 complete at the activation baseline, no support effect, and 13 rejecting mutations."
    )


if __name__ == "__main__":
    main()
