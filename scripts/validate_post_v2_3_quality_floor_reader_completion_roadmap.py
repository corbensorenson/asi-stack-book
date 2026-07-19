#!/usr/bin/env python3
"""Validate the active post-v2.3 quality-floor and reader authority."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import statistics
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema
from validate_chapter_source_hygiene import hygiene_errors


ROADMAP_PATH = "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md"
STATUS_PATH = "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json"
SCHEMA_PATH = "schemas/post_v2_3_quality_floor_reader_completion_status.schema.json"
PREDECESSOR_PATH = "docs/post_v2_2_implementation_completion_roadmap.md"
HISTORICAL_READER_PATH = "editions/reader_manuscript/v1_0/manifest.json"
PROVISIONAL_READER_PATH = "editions/reader_manuscript/v2_0/manifest.json"
QUALITY_PACKETS_PATH = "docs/post_v2_3_chapter_quality_packets.md"
COMPLETION_PATH = "docs/post_v2_3_quality_floor_reader_completion_declaration.md"
NO_RELEASE_PATH = "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json"
SUCCESSOR_ROADMAP_PATH = "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
SUCCESSOR_STATUS_PATH = "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
SUCCESSOR_SCHEMA_PATH = "schemas/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.schema.json"
SUCCESSOR_P0_RECEIPT_PATH = "docs/post_v2_3_clean_handoff_receipt.md"
SUCCESSOR_TEXT_FORMAT_PROFILE_PATH = "editions/reader_manuscript/v2_0/text_format_profile.json"
SUCCESSOR_DOCX_REFERENCE_PATH = "editions/reader_manuscript/v2_0/profiles/reader-v2-reference.docx"
SUCCESSOR_FORMAT_MATRIX_PATH = "editions/reader_manuscript/v2_0/format_review_matrix.json"
SUCCESSOR_EPUB_DISPOSITION_PATH = "editions/reader_manuscript/v2_0/epub_disposition.json"
NEXT_SUCCESSOR_ROADMAP_PATH = "docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md"
NEXT_SUCCESSOR_STATUS_PATH = "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
ACTIVE_CURRENT_ROADMAP_PATH = "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"
ACTIVE_CURRENT_STATUS_PATH = "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
ACTIVE_MARKER = "Status: **active canonical successor**"
TARGET_IDS = [
    "scalable-oversight-and-adversarial-ai-control",
    "model-weight-custody-and-hardware-roots-of-trust",
    "ai-supply-chain-integrity-and-lifecycle-provenance",
    "open-ended-improvement-engines",
    "inter-stack-protocols-identity-and-economic-exchange",
    "governed-deliberation-and-test-time-scaling",
    "capability-thresholds-and-deployment-commitments",
    "adversarial-evaluation-sandbagging-and-training-time-deception",
    "safety-cases-and-structured-assurance",
    "data-engines-continual-learning-and-unlearning",
]
EXPECTED_BASELINE_WORDS = [2663, 2583, 3608, 2745, 3680, 2832, 2631, 2333, 2681, 3890]
REQUIRED_SECTIONS = [
    "## Goal to point at",
    "## Completion contract",
    "## P1 — Ten-chapter semantic depth",
    "## P2 — Owned formal and executable depth",
    "## P3 — Current-spine curated reader",
    "## P4 — Evidence adjudication and next campaigns",
    "## P5 — Coherent release and closure",
    "## Definition of done",
    "## Canonical execution prompt",
]


def chapter_rows(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def word_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return len(re.findall(r"\b[\w’'-]+\b", text))


def active_roadmaps() -> list[str]:
    return [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "docs").glob("*roadmap*.md"))
        if ACTIVE_MARKER in path.read_text(encoding="utf-8", errors="ignore")[:1200]
    ]


def snapshot() -> dict:
    return {
        "status": load_json(ROOT / STATUS_PATH),
        "roadmap": (ROOT / ROADMAP_PATH).read_text(encoding="utf-8"),
        "schema": load_json(ROOT / SCHEMA_PATH),
        "structure": load_json(ROOT / "book_structure.json"),
        "sources": load_json(ROOT / "sources/source_inventory.json"),
        "vectors": load_json(ROOT / "evidence_quality/core_claim_vectors.json"),
        "historical_reader": load_json(ROOT / HISTORICAL_READER_PATH),
        "readme": (ROOT / "README.md").read_text(encoding="utf-8"),
        "index": (ROOT / "index.qmd").read_text(encoding="utf-8"),
        "publication": (ROOT / "docs/publication_readiness.md").read_text(encoding="utf-8"),
        "public_contract": (ROOT / "docs/public_status_contract.md").read_text(encoding="utf-8"),
        "completion": (ROOT / "docs/v2_3_completion_declaration.md").read_text(encoding="utf-8"),
        "cycle_completion": (ROOT / COMPLETION_PATH).read_text(encoding="utf-8"),
        "no_release": load_json(ROOT / NO_RELEASE_PATH),
        "quality_packets": (ROOT / QUALITY_PACKETS_PATH).read_text(encoding="utf-8"),
        "predecessor": (ROOT / PREDECESSOR_PATH).read_text(encoding="utf-8"),
        "successor_roadmap": (ROOT / SUCCESSOR_ROADMAP_PATH).read_text(encoding="utf-8"),
        "successor_status": load_json(ROOT / SUCCESSOR_STATUS_PATH),
        "successor_schema": load_json(ROOT / SUCCESSOR_SCHEMA_PATH),
        "successor_p0_receipt": (ROOT / SUCCESSOR_P0_RECEIPT_PATH).read_text(encoding="utf-8"),
        "successor_text_format_profile": load_json(ROOT / SUCCESSOR_TEXT_FORMAT_PROFILE_PATH),
        "successor_format_matrix": load_json(ROOT / SUCCESSOR_FORMAT_MATRIX_PATH),
        "successor_epub_disposition": load_json(ROOT / SUCCESSOR_EPUB_DISPOSITION_PATH),
        "next_successor_status": load_json(ROOT / NEXT_SUCCESSOR_STATUS_PATH),
        "active_current_status": load_json(ROOT / ACTIVE_CURRENT_STATUS_PATH),
        "active_roadmaps": active_roadmaps(),
        "hygiene_errors": hygiene_errors(),
    }


def semantic_errors(data: dict) -> list[str]:
    errors: list[str] = []
    status = data["status"]
    roadmap = data["roadmap"]
    rows = chapter_rows(data["structure"])
    ids = [row.get("id") for row in rows]
    activation_ids = [
        row.get("chapter_id")
        for row in load_json(ROOT / PROVISIONAL_READER_PATH).get("chapter_records", [])
    ]
    by_id = {row.get("id"): row for row in rows}
    sources_obj = data["sources"]
    source_rows = sources_obj if isinstance(sources_obj, list) else sources_obj.get("sources", [])
    vectors_obj = data["vectors"]
    vectors = vectors_obj.get("vectors", []) if isinstance(vectors_obj, dict) else vectors_obj
    active_current = data["active_current_status"]
    current_truth = active_current.get("activation_truth", {})
    live_chapter_count = current_truth.get("live_working_chapter_count")
    live_argument_count = current_truth.get("chapter_core_argument_count")

    if status.get("status") != "completed":
        errors.append("post-v2.3 roadmap must be completed after every terminal gate closes")
    if data["active_roadmaps"] != [ACTIVE_CURRENT_ROADMAP_PATH]:
        errors.append("terminal roadmap history must expose the exact active evidence-competence successor")
    if "Status: completed 2026-07-13" not in data["predecessor"]:
        errors.append("predecessor roadmap lost completed status")
    if (
        not isinstance(live_chapter_count, int)
        or live_chapter_count < 55
        or len(rows) != live_chapter_count
        or len(source_rows) < 280
    ):
        errors.append(
            "current manifest disagrees with active-roadmap chapter truth or the historical public-safe source floor was violated"
        )
    digest = hashlib.sha256("\n".join(activation_ids).encode()).hexdigest()
    if status["activation_baseline"].get("activation_chapter_ids_sha256") != digest:
        errors.append("historical 54-chapter activation identity/order drifted")
    if (
        live_argument_count != live_chapter_count
        or not isinstance(vectors, list)
        or len(vectors) != live_chapter_count
        or [row.get("chapter_id") for row in vectors] != ids
        or any(row.get("summary_support_state") != "argument" for row in vectors)
    ):
        errors.append("current chapter-core vector identity, count, or argument-only state drifted")
    next_status = data["next_successor_status"]
    if next_status.get("activation_baseline", {}).get("active_chapter_count") != 54:
        errors.append("claim-proof successor lost the frozen 54-chapter activation baseline")
    if next_status.get("structural_expansion_contract", {}).get("live_chapter_count") != 55:
        errors.append("claim-proof successor lost the authorized 55th chapter")
    if next_status.get("status") != "completed" or next_status.get("roadmap_path") != NEXT_SUCCESSOR_ROADMAP_PATH:
        errors.append("claim-proof successor is not preserved as completed history")
    if active_current.get("status") != "active" or active_current.get("roadmap_path") != ACTIVE_CURRENT_ROADMAP_PATH:
        errors.append("current evidence-competence roadmap machine authority is stale")

    cohort = status.get("chapter_cohort", [])
    if [row.get("id") for row in cohort] != TARGET_IDS:
        errors.append("ten-chapter cohort identity or order drifted")
    if [row.get("baseline_word_count") for row in cohort] != EXPECTED_BASELINE_WORDS:
        errors.append("ten-chapter activation word baseline drifted")
    if [row.get("id") for row in status.get("priorities", [])] != [f"P{i}" for i in range(6)]:
        errors.append("priority order must be P0 through P5")
    if [row.get("id") for row in status.get("milestones", [])] != [f"M{i}" for i in range(10)]:
        errors.append("milestone order must be M0 through M9")
    if any(row.get("state") != "completed" for row in status.get("priorities", [])):
        errors.append("completed roadmap has a non-completed priority")
    if any(row.get("state") != "completed" for row in status.get("milestones", [])):
        errors.append("completed roadmap has a non-completed milestone")
    if status.get("breadth_freeze") is not True:
        errors.append("chapter breadth freeze is not active")
    if status.get("support_state_effect") != "none" or status.get("release_effect") != "none":
        errors.append("roadmap activation invented support or release effect")

    semantic_done = []
    formal_done = []
    for record in cohort:
        chapter_id = record["id"]
        chapter = by_id.get(chapter_id)
        if chapter is None or chapter.get("file") != record.get("file"):
            errors.append(f"{chapter_id}: missing or file mapping drifted")
            continue
        if record.get("semantic_packet_state") == "completed":
            semantic_done.append(word_count(ROOT / record["file"]))
            if semantic_done[-1] < 4487:
                errors.append(f"{chapter_id}: semantic packet marked complete below the prose floor")
            if f"| `{chapter_id}` | complete |" not in data["quality_packets"]:
                errors.append(f"{chapter_id}: semantic packet complete without a complete quality-ledger row")
        if record.get("formal_packet_state") == "completed":
            formal_done.append(chapter_id)
            current_modules = [
                value.strip()
                for value in str(chapter.get("lean_module", "")).split(";")
                if value.strip()
            ]
            if record.get("required_lean_module") not in current_modules:
                errors.append(f"{chapter_id}: formal packet complete without its required owned module")
            module_files = [
                ROOT / "lean" / (module.replace(".", "/") + ".lean")
                for module in current_modules
            ]
            required_file = ROOT / "lean" / (record["required_lean_module"].replace(".", "/") + ".lean")
            if not required_file.is_file():
                errors.append(f"{chapter_id}: required owned Lean module file is absent")
            else:
                theorem_count = sum(
                    len(re.findall(r"^theorem\s+", module_file.read_text(encoding="utf-8"), re.M))
                    for module_file in module_files
                    if module_file.is_file()
                )
                if theorem_count < 5:
                    errors.append(f"{chapter_id}: formal packet complete with fewer than five theorem declarations")
    p1 = next(row for row in status["priorities"] if row["id"] == "P1")
    p2 = next(row for row in status["priorities"] if row["id"] == "P2")
    if p1["state"] == "completed":
        if len(semantic_done) != 10 or statistics.median(semantic_done) < 4944:
            errors.append("P1 completed without ten semantic packets and the cohort median floor")
    if p2["state"] == "completed" and len(formal_done) != 10:
        errors.append("P2 completed without ten owned formal packets")

    historical = data["historical_reader"]
    if historical.get("edition_scope") != "historical_release_snapshot" or len(historical.get("chapter_records", [])) != 44:
        errors.append("frozen v1.0 curated-reader identity or 44-record history drifted")
    regen = historical.get("historical_spine_snapshot", {}).get("regeneration_policy", "")
    if "Create a later reader-edition directory" not in regen:
        errors.append("historical reader lost its later-edition requirement")
    reader = status.get("reader_successor", {})
    reader_state = reader.get("state")
    if reader_state == "absent" and (ROOT / PROVISIONAL_READER_PATH).exists():
        errors.append("reader successor exists while machine state says absent")
    if reader_state in {"initialized", "reconciling", "reconciled", "released", "blocked"}:
        if not (ROOT / PROVISIONAL_READER_PATH).is_file():
            errors.append("reader successor state is active but provisional manifest is absent")
        else:
            successor = load_json(ROOT / PROVISIONAL_READER_PATH)
            records = successor.get("chapter_records", [])
            if reader_state in {"reconciled", "released"} and [row.get("chapter_id") for row in records] != activation_ids:
                errors.append("reader successor claims reconciliation without exact 54-chapter identity/order")
    p3 = next(row for row in status["priorities"] if row["id"] == "P3")
    if p3["state"] == "completed" and reader_state not in {"released", "blocked"}:
        errors.append("P3 completed without an exact reader release or blocked disposition")

    no_release = data["no_release"]
    if no_release.get("decision") != "no_public_living_book_release":
        errors.append("terminal no-public-release decision is absent or changed")
    if no_release.get("latest_public_living_book_release", {}).get("version") != "v2.3.0":
        errors.append("terminal record does not preserve v2.3.0 as latest public release")
    if no_release.get("publication_effect") != {
        "source_tag_created": False,
        "public_deployment_performed": False,
        "immutable_site_archive_created": False,
        "rights_grant_created": False,
        "source_commit_claimed": False,
    }:
        errors.append("terminal no-release record invents a publication effect")
    for phrase in ["P0–P5", "M0–M9", NO_RELEASE_PATH, SUCCESSOR_ROADMAP_PATH, SUCCESSOR_STATUS_PATH, "Successor activated: 2026-07-13"]:
        if phrase not in data["cycle_completion"]:
            errors.append(f"cycle completion declaration missing terminal boundary: {phrase}")

    successor = data["successor_status"]
    errors.extend(validate_against_schema(successor, data["successor_schema"], SUCCESSOR_STATUS_PATH))
    if successor.get("status") != "completed" or successor.get("roadmap_path") != SUCCESSOR_ROADMAP_PATH:
        errors.append("declared clean-handoff successor machine authority is absent or not terminal")
    if [row.get("id") for row in successor.get("priorities", [])] != [f"P{i}" for i in range(5)]:
        errors.append("successor priority order must be P0 through P4")
    if [row.get("id") for row in successor.get("milestones", [])] != [f"M{i}" for i in range(9)]:
        errors.append("successor milestone order must be M0 through M8")
    if successor.get("external_human_prepublication_required") is not False:
        errors.append("successor silently requires external-human prepublication review")
    if successor.get("maximum_new_outcome_campaigns") != 1 or successor.get("breadth_freeze") is not True:
        errors.append("successor campaign ceiling or chapter breadth freeze drifted")
    if successor.get("activation_baseline", {}).get("public_safe_source_count") != 280:
        errors.append("successor lost the exact historical 280-source activation baseline")
    p0 = next((row for row in successor.get("priorities", []) if row.get("id") == "P0"), {})
    m1 = next((row for row in successor.get("milestones", []) if row.get("id") == "M1"), {})
    handoff = successor.get("p0_handoff", {})
    if p0.get("state") == "completed" or m1.get("state") == "completed":
        if p0.get("state") != "completed" or m1.get("state") != "completed":
            errors.append("successor P0 and M1 completion states disagree")
        if handoff.get("state") != "completed" or handoff.get("receipt_path") != SUCCESSOR_P0_RECEIPT_PATH:
            errors.append("successor clean-handoff completion lacks its machine receipt binding")
        for value in [
            handoff.get("source_commit"),
            str(handoff.get("build_run_id", "")),
            str(handoff.get("deploy_run_id", "")),
            handoff.get("deployed_url"),
        ]:
            if not value or value not in data["successor_p0_receipt"]:
                errors.append(f"successor clean-handoff receipt missing machine-bound value: {value}")
        if handoff.get("support_state_effect") != "none" or handoff.get("release_effect") != "none":
            errors.append("successor clean-handoff receipt invented a support or release effect")
    m2 = next((row for row in successor.get("milestones", []) if row.get("id") == "M2"), {})
    if m2.get("state") == "completed":
        profile = data["successor_text_format_profile"]
        source_lock = profile.get("source_lock", {})
        if profile.get("state") != "frozen_before_release_candidates" or source_lock.get("chapter_count") != 54:
            errors.append("successor M2 completed without a frozen 54-chapter text-format profile")
        for path, expected in [
            (SUCCESSOR_TEXT_FORMAT_PROFILE_PATH, None),
            (PROVISIONAL_READER_PATH, source_lock.get("manifest_sha256")),
            (SUCCESSOR_DOCX_REFERENCE_PATH, profile.get("formats", {}).get("docx", {}).get("reference_doc_sha256")),
        ]:
            if not (ROOT / path).is_file():
                errors.append(f"successor M2 artifact is missing: {path}")
            elif expected and hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                errors.append(f"successor M2 artifact digest drifted: {path}")
        milestone_states = {
            row.get("id"): row.get("state") for row in successor.get("milestones", [])
        }
        expected_terminal_prefix = {
            "epub": ("M3", ("approved_", "blocked_")),
            "pdf": ("M4", ("approved_", "blocked_")),
            "docx": ("M5", ("approved_", "blocked_")),
        }
        for name, (milestone_id, terminal_prefixes) in expected_terminal_prefix.items():
            format_state = profile.get("formats", {}).get(name, {}).get("state", "")
            if milestone_states.get(milestone_id) == "completed":
                if not format_state.startswith(terminal_prefixes):
                    errors.append(f"successor {milestone_id} completed without terminal {name} profile state")
            elif format_state != "profile_frozen_candidate_not_generated":
                errors.append(f"successor {name} profile advanced before {milestone_id} completion")
        if any(profile.get("formats", {}).get(name, {}).get("state") != "deferred_not_authorized" for name in ["audio", "embedded_audio"]):
            errors.append("successor M2 silently authorized an audio format")
        if profile.get("support_state_effect") != "none" or profile.get("release_effect") != "none":
            errors.append("successor M2 profile invented support or release effect")
    m3 = next((row for row in successor.get("milestones", []) if row.get("id") == "M3"), {})
    if m3.get("state") == "completed":
        disposition = data["successor_epub_disposition"]
        epub_status = next(
            (row for row in successor.get("reader_formats", []) if row.get("format") == "epub"), {}
        )
        matrix_epub = data["successor_format_matrix"].get("formats", {}).get("epub", {})
        if disposition.get("decision") not in {"approved_exact_local_artifact", "approved_public_artifact", "blocked"}:
            errors.append("successor M3 completed without a terminal EPUB disposition")
        if epub_status.get("state") != disposition.get("decision") or matrix_epub.get("state") != disposition.get("decision"):
            errors.append("successor EPUB status, format matrix, and disposition disagree")
        artifact = disposition.get("artifact", {})
        artifact_path = ROOT / artifact.get("path", "")
        if not artifact_path.is_file():
            errors.append("successor M3 exact EPUB artifact is absent")
        elif hashlib.sha256(artifact_path.read_bytes()).hexdigest() != artifact.get("sha256"):
            errors.append("successor M3 exact EPUB artifact digest drifted")
    successor_roadmap_normalized = " ".join(data["successor_roadmap"].split())
    for phrase in [
        "Critique adjudication",
        "P0 — Authority, truth repair, and clean handoff",
        "P1 — 54-chapter multi-format reader",
        "P2 — Selective external anchoring and completeness residuals",
        "P3 — Evidence protocol repair and current implementation transfer",
        "P4 — Product reconciliation, release decision, and closure",
        "Do not repeat the already accepted accelerator-parity manifest import",
        "does not assume that the next public living-book version is `v2.4`",
        "No external-human prepublication gate",
    ]:
        if phrase not in successor_roadmap_normalized:
            errors.append(f"successor roadmap missing governing boundary: {phrase}")

    if data["hygiene_errors"]:
        errors.extend(data["hygiene_errors"])
    for section in REQUIRED_SECTIONS:
        if roadmap.count(section) != 1:
            errors.append(f"roadmap must contain exactly one section: {section}")
    for phrase in [
        "No new chapter is added",
        "Semantic adequacy before proxy counts",
        "frozen 44-chapter historical snapshot",
        "External-human prepublication review is not required",
        "Governance tax on useful natural work",
        "Residual honesty under pressure",
        "promote`, `narrow`, `no_change`, or `refute",
    ]:
        if phrase not in roadmap:
            errors.append(f"roadmap missing governing boundary: {phrase}")
    for name in TARGET_IDS:
        if roadmap.count(f"`{name}`") < 1:
            errors.append(f"roadmap does not identify target chapter: {name}")

    current_claim_ratio = f"{live_argument_count}/{live_chapter_count} chapter-core claims at `argument`"
    surface_requirements = {
        "README.md": (data["readme"], current_claim_ratio),
        "index.qmd": (data["index"], current_claim_ratio),
        "docs/publication_readiness.md": (
            data["publication"],
            f"All {live_chapter_count} live chapter-core claims remain at `argument`",
        ),
        "docs/public_status_contract.md": (data["public_contract"], current_claim_ratio),
    }
    for name, (text, live_claim_phrase) in surface_requirements.items():
        normalized = " ".join(text.split())
        for phrase in [NEXT_SUCCESSOR_ROADMAP_PATH, NEXT_SUCCESSOR_STATUS_PATH, ACTIVE_CURRENT_ROADMAP_PATH, ACTIVE_CURRENT_STATUS_PATH, "v2.3.0", live_claim_phrase]:
            if phrase not in text and phrase not in normalized:
                errors.append(f"{name} missing active roadmap truth: {phrase}")
    for phrase in [ROADMAP_PATH, "Successor activated: 2026-07-13"]:
        if phrase not in data["completion"]:
            errors.append(f"v2.3 completion declaration missing successor pointer: {phrase}")
    return errors


def mutation_controls(base: dict) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict]] = []

    duplicate = copy.deepcopy(base)
    duplicate["active_roadmaps"] = [ACTIVE_CURRENT_ROADMAP_PATH, "docs/fake_roadmap.md"]
    mutations.append(("duplicate active roadmap", duplicate))

    missing_chapter = copy.deepcopy(base)
    missing_chapter["status"]["chapter_cohort"] = missing_chapter["status"]["chapter_cohort"][:-1]
    mutations.append(("missing target chapter", missing_chapter))

    padded_completion = copy.deepcopy(base)
    padded_completion["quality_packets"] = padded_completion["quality_packets"].replace(
        "| `scalable-oversight-and-adversarial-ai-control` | complete |",
        "| `scalable-oversight-and-adversarial-ai-control` | pending |",
    )
    mutations.append(("premature semantic completion", padded_completion))

    borrowed_completion = copy.deepcopy(base)
    borrowed_completion["status"]["chapter_cohort"][0]["required_lean_module"] = "AsiStackProofs.SelfImprovement"
    mutations.append(("borrowed module completion", borrowed_completion))

    reader_laundering = copy.deepcopy(base)
    reader_laundering["status"]["reader_successor"]["state"] = "reconciled"
    mutations.append(("reader denominator laundering", reader_laundering))

    support = copy.deepcopy(base)
    support["vectors"]["vectors"][0]["summary_support_state"] = "prototype-backed"
    mutations.append(("support promotion", support))

    breadth = copy.deepcopy(base)
    breadth["structure"]["parts"][0]["chapters"].append({"id": "new-breadth", "file": "chapters/new-breadth.qmd"})
    mutations.append(("breadth expansion", breadth))

    orphan = copy.deepcopy(base)
    orphan["hygiene_errors"] = ["chapters/accidental.html: undeclared"]
    mutations.append(("undeclared chapter HTML", orphan))

    stale_pointer = copy.deepcopy(base)
    stale_pointer["readme"] = stale_pointer["readme"].replace(ACTIVE_CURRENT_ROADMAP_PATH, PREDECESSOR_PATH)
    mutations.append(("stale public pointer", stale_pointer))

    external_review = copy.deepcopy(base)
    external_review["roadmap"] = external_review["roadmap"].replace("External-human prepublication review is not required", "External-human prepublication review is required")
    mutations.append(("external review requirement", external_review))

    for label, mutated in mutations:
        if not semantic_errors(mutated):
            failures.append(f"negative control was accepted: {label}")
    return failures


def main() -> None:
    required = [ROADMAP_PATH, STATUS_PATH, SCHEMA_PATH, PREDECESSOR_PATH, HISTORICAL_READER_PATH, PROVISIONAL_READER_PATH, QUALITY_PACKETS_PATH, COMPLETION_PATH, NO_RELEASE_PATH, SUCCESSOR_ROADMAP_PATH, SUCCESSOR_STATUS_PATH, SUCCESSOR_SCHEMA_PATH, SUCCESSOR_P0_RECEIPT_PATH, SUCCESSOR_TEXT_FORMAT_PROFILE_PATH, SUCCESSOR_DOCX_REFERENCE_PATH, NEXT_SUCCESSOR_STATUS_PATH, ACTIVE_CURRENT_STATUS_PATH]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("missing post-v2.3 roadmap artifacts: " + ", ".join(missing))
    data = snapshot()
    errors = validate_against_schema(data["status"], data["schema"], STATUS_PATH)
    errors.extend(semantic_errors(data))
    errors.extend(mutation_controls(data))
    if errors:
        raise SystemExit("Post-v2.3 quality-floor roadmap validation failed:\n - " + "\n - ".join(errors))
    print(
        "Post-v2.3 quality-floor roadmap passed: completed authority with one declared clean-handoff successor, frozen 54-chapter activation spine and historical 55-chapter expansion preserved, "
        f"current {data['active_current_status']['activation_truth']['live_working_chapter_count']} live chapters, "
        f"10 exact depth targets, 44-record historical reader preserved, 54-record successor {data['status']['reader_successor']['state']}, "
        f"10 declared redirects, {data['active_current_status']['activation_truth']['chapter_core_argument_count']} live argument-state core claims, and 10 rejecting mutations."
    )


if __name__ == "__main__":
    main()
