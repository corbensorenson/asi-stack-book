#!/usr/bin/env python3
"""Validate the active post-v2.2 implementation-completion authority."""

from __future__ import annotations

import copy
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema


ROADMAP = ROOT / "docs/post_v2_2_implementation_completion_roadmap.md"
STATUS = ROOT / "roadmap_records/post_v2_2_implementation_completion_status.json"
SCHEMA = ROOT / "schemas/post_v2_2_implementation_completion_status.schema.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCES = ROOT / "sources/source_inventory.json"
VECTORS = ROOT / "evidence_quality/core_claim_vectors.json"
README = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
PREDECESSOR = ROOT / "docs/post_v2_1_residual_and_transfer_roadmap.md"
PREDECESSOR_COMPLETION = ROOT / "docs/v2_2_completion_declaration.md"
CYCLE_COMPLETION = ROOT / "docs/v2_3_completion_declaration.md"

ROADMAP_PATH = "docs/post_v2_2_implementation_completion_roadmap.md"
STATUS_PATH = "roadmap_records/post_v2_2_implementation_completion_status.json"
ACTIVE_SUCCESSOR_PATH = "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md"
ACTIVE_SUCCESSOR_STATUS_PATH = "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json"
CURRENT_SUCCESSOR_PATH = "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
CURRENT_SUCCESSOR_STATUS_PATH = "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
EXPECTED_PRIORITIES = [f"P{i}" for i in range(6)]
EXPECTED_MILESTONES = [f"M{i}" for i in range(8)]
EXPECTED_LANES = [f"QI-{i:02d}" for i in range(1, 13)]
QCSA_OWNERS = {
    "cognitive-compilation-and-semantic-ir",
    "virtual-context-abi",
    "claim-ledgers-and-belief-revision",
    "runtime-adapters-tool-permissions-and-human-approval",
    "inter-stack-protocols-identity-and-economic-exchange",
    "routing-heads-and-specialist-cores",
    "compact-generative-systems-and-residual-honesty",
    "data-engines-continual-learning-and-unlearning",
    "integrated-reference-architecture",
}
REQUIRED_ROADMAP_SECTIONS = [
    "## Goal to point at",
    "## What “completed” means",
    "## P1 — Implement the QCSA artifact stack",
    "## P2 — Evaluate QCSA and its ablations",
    "## P3 — Governed vertical reference path",
    "## P4 — Evidence and book completion",
    "## P5 — Release or honest no-release closure",
    "## Definition of done",
    "## Canonical execution prompt",
]


def active_roadmaps() -> list[str]:
    marker = "Status: active canonical successor roadmap; unfinished work only"
    return [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "docs").glob("*roadmap*.md"))
        if marker in path.read_text(encoding="utf-8", errors="ignore")[:1200]
    ]


def semantic_errors(data: dict) -> list[str]:
    errors: list[str] = []
    status = data["status"]
    roadmap = data["roadmap"]
    structure = data["structure"]
    sources = data["sources"]
    vectors_obj = data["vectors"]
    vectors = vectors_obj.get("vectors", []) if isinstance(vectors_obj, dict) else vectors_obj
    chapters = [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]
    chapter_ids = {chapter.get("id") for chapter in chapters}
    source_rows = sources if isinstance(sources, list) else sources.get("sources", [])

    if status.get("status") not in {"active", "completed"}:
        errors.append("roadmap status is neither active nor completed")
    if status.get("roadmap_path") != ROADMAP_PATH:
        errors.append("machine roadmap path drifted")
    if status.get("status") == "active" and data["active_roadmaps"] != [ROADMAP_PATH]:
        errors.append("there must be exactly one active canonical roadmap")
    if status.get("status") == "completed" and data["active_roadmaps"] != [CURRENT_SUCCESSOR_PATH]:
        errors.append("completed roadmap history must coexist with exactly the declared current successor")

    baseline = status.get("baseline", {})
    expected_baseline = {
        "latest_immutable_release": "v2.2.0",
        "active_chapter_count": 54,
        "public_safe_source_count": 280,
        "core_claim_count": 54,
        "core_argument_count": 54,
        "promoted_core_claim_count": 0,
        "qcsa_chapter_owner_count": 9,
        "qcsa_implementation_lane_count": 12,
        "qcsa_implemented_lane_count": 0,
    }
    if baseline != expected_baseline:
        errors.append("activation baseline drifted")
    if len(chapters) != 54:
        errors.append("active chapter count is not 54")
    if len(source_rows) != 280:
        errors.append("public-safe source count is not 280")
    if not isinstance(vectors, list) or len(vectors) != 54:
        errors.append("core evidence-vector count is not 54")
    elif any(row.get("summary_support_state") != "argument" for row in vectors):
        errors.append("roadmap activation moved a core support state")

    qowners = {chapter.get("id") for chapter in chapters if "qcsa_whitepaper" in chapter.get("source_ids", [])}
    if qowners != QCSA_OWNERS:
        errors.append("QCSA chapter ownership differs from the nine existing owners")
    if chapter_ids & {"qcsa", "question-compiled-semantic-addressing"}:
        errors.append("roadmap activation unexpectedly created a QCSA chapter")

    priorities = status.get("priorities", [])
    if [row.get("id") for row in priorities] != EXPECTED_PRIORITIES:
        errors.append("priority order must be P0 through P5")
    milestones = status.get("milestones", [])
    if [row.get("id") for row in milestones] != EXPECTED_MILESTONES:
        errors.append("milestone order must be M0 through M7")
    lanes = status.get("qcsa_lanes", [])
    if [row.get("id") for row in lanes] != EXPECTED_LANES:
        errors.append("QCSA lane identity/order must be QI-01 through QI-12")
    for row in lanes:
        owners = set(row.get("owner_chapters", []))
        if not owners or not owners <= QCSA_OWNERS:
            errors.append(f"{row.get('id')}: owner is absent or outside QCSA chapter owners")
    if status.get("status") == "completed":
        if any(row.get("state") != "completed" for row in priorities):
            errors.append("terminal roadmap retains incomplete priorities")
        if any(row.get("state") != "completed" for row in milestones):
            errors.append("terminal roadmap retains incomplete milestones")
        if any(row.get("state") not in {"completed", "rejected"} for row in lanes):
            errors.append("terminal roadmap retains an undispositioned QCSA lane")

    for section in REQUIRED_ROADMAP_SECTIONS:
        if roadmap.count(section) != 1:
            errors.append(f"roadmap must contain exactly one section: {section}")
    for phrase in [
        "all twelve QCSA normative lanes",
        "external-human prepublication review",
        "Identity, address, truth, and authority remain separate",
        "Existing owners before new chapters",
        "No outcome-driven scope expansion",
        "matched-resource Pareto improvement",
        "deployment without rebuilding",
    ]:
        if phrase not in roadmap:
            errors.append(f"roadmap missing governing boundary: {phrase}")
    for lane_id in EXPECTED_LANES:
        if roadmap.count(f"`{lane_id}`") < 1:
            errors.append(f"roadmap does not define {lane_id}")

    for name, text in [("README.md", data["readme"]), ("index.qmd", data["index"])]:
        for phrase in [ROADMAP_PATH, STATUS_PATH, ACTIVE_SUCCESSOR_PATH, ACTIVE_SUCCESSOR_STATUS_PATH, CURRENT_SUCCESSOR_PATH, CURRENT_SUCCESSOR_STATUS_PATH, "v2.2.0", "v2.3.0", "e27661166e9105f37cb36d63b15795f80715ca24", "all 54 chapter-core claims remain at `argument`"]:
            if phrase not in text:
                errors.append(f"{name} missing roadmap/release truth: {phrase}")
    predecessor = data["predecessor"]
    if "Status: completed 2026-07-11" not in predecessor:
        errors.append("predecessor roadmap lost completed status")
    if ROADMAP_PATH not in data["predecessor_completion"] or "Successor activated: 2026-07-13" not in data["predecessor_completion"]:
        errors.append("v2.2 completion declaration lacks the dated successor pointer")
    for phrase in ["v2.3.0", "e27661166e9105f37cb36d63b15795f80715ca24", "29234323320", "29234640734", "closes P5, M7, and the roadmap", "No successor roadmap is", ACTIVE_SUCCESSOR_PATH, "Successor activated: 2026-07-13"]:
        if phrase not in data["cycle_completion"]:
            errors.append(f"v2.3 completion declaration lacks: {phrase}")
    if status.get("support_state_effect") != "none" or status.get("new_chapter_effect") != "none" or status.get("optional_format_effect") != "none":
        errors.append("roadmap activation changed claim, chapter, or optional-format state")
    return errors


def negative_controls(base: dict) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict]] = []

    stale_release = copy.deepcopy(base)
    stale_release["status"]["baseline"]["latest_immutable_release"] = "v2.1.0"
    mutations.append(("stale immutable release", stale_release))

    missing_lane = copy.deepcopy(base)
    missing_lane["status"]["qcsa_lanes"] = missing_lane["status"]["qcsa_lanes"][:-1]
    mutations.append(("missing QCSA lane", missing_lane))

    wrong_owner = copy.deepcopy(base)
    wrong_owner["status"]["qcsa_lanes"][0]["owner_chapters"] = ["prototype-roadmap"]
    mutations.append(("wrong chapter owner", wrong_owner))

    support_promotion = copy.deepcopy(base)
    support_promotion["vectors"]["vectors"][0]["summary_support_state"] = "prototype-backed"
    mutations.append(("support promotion", support_promotion))

    chapter_invention = copy.deepcopy(base)
    chapter_invention["structure"]["parts"][0]["chapters"].append({"id": "qcsa", "source_ids": []})
    mutations.append(("standalone chapter invention", chapter_invention))

    duplicate_active = copy.deepcopy(base)
    duplicate_active["active_roadmaps"] = [CURRENT_SUCCESSOR_PATH, "docs/fake_roadmap.md"]
    mutations.append(("duplicate active roadmap", duplicate_active))

    stale_pointer = copy.deepcopy(base)
    stale_pointer["readme"] = stale_pointer["readme"].replace(ROADMAP_PATH, "docs/post_v2_1_residual_and_transfer_roadmap.md")
    mutations.append(("stale README pointer", stale_pointer))

    terminal_regression = copy.deepcopy(base)
    terminal_regression["status"]["priorities"][-1]["state"] = "running"
    mutations.append(("terminal priority regression", terminal_regression))

    for label, mutated in mutations:
        if not semantic_errors(mutated):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = [ROADMAP, STATUS, SCHEMA, STRUCTURE, SOURCES, VECTORS, README, INDEX, PREDECESSOR, PREDECESSOR_COMPLETION, CYCLE_COMPLETION]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing post-v2.2 roadmap artifacts: " + ", ".join(missing))
    status = load_json(STATUS)
    data = {
        "status": status,
        "roadmap": ROADMAP.read_text(encoding="utf-8"),
        "structure": load_json(STRUCTURE),
        "sources": load_json(SOURCES),
        "vectors": load_json(VECTORS),
        "readme": README.read_text(encoding="utf-8"),
        "index": INDEX.read_text(encoding="utf-8"),
        "predecessor": PREDECESSOR.read_text(encoding="utf-8"),
        "predecessor_completion": PREDECESSOR_COMPLETION.read_text(encoding="utf-8"),
        "cycle_completion": CYCLE_COMPLETION.read_text(encoding="utf-8"),
        "active_roadmaps": active_roadmaps(),
    }
    errors = validate_against_schema(status, load_json(SCHEMA), STATUS.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(data))
    errors.extend(negative_controls(data))
    if errors:
        raise SystemExit("Post-v2.2 implementation roadmap validation failed:\n - " + "\n - ".join(errors))
    print(
        "Post-v2.2 implementation roadmap passed: completed terminal roadmap, 6 priorities, "
        "8 milestones, 12 QCSA implementation lanes, 9 existing chapter owners, "
        "54 argument-state core claims, one declared current successor, no new chapter/format effect, and 8 rejecting mutations."
    )


if __name__ == "__main__":
    main()
