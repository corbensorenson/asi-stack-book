#!/usr/bin/env python3
"""Validate activation-frozen P7 history and the separately governed live book."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
P7_RESULT = ROOT / "experiments/p7_book_evidence_reconciliation/result.json"
P7_SCHEMA = ROOT / "schemas/p7_book_evidence_reconciliation.schema.json"
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"
VECTORS = ROOT / "evidence_quality/core_claim_vectors.json"
HISTORICAL_STATUS = ROOT / "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
CURRENT_STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
TERMINAL = ROOT / "experiments/claim_family_terminal_coverage/results/result.json"
LINEAGE_LOCK = ROOT / "experiments/p7_book_evidence_reconciliation/lineage_lock.json"

ACTIVATION_COMMIT = "882b2a82c8e7af3c90265dd1ff23ecbfacf4b0db"
AMENDMENT_COMMIT = "295642f21a39e2d735553b3a51ef6ba2f5e76d2c"
RESULT_RELATIVE = "experiments/p7_book_evidence_reconciliation/result.json"
SCHEMA_RELATIVE = "schemas/p7_book_evidence_reconciliation.schema.json"
CURRENT_ROADMAP = "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md"

P7_START = "<!-- P7-EVIDENCE-RECONCILIATION:START -->"
P7_END = "<!-- P7-EVIDENCE-RECONCILIATION:END -->"
SOURCE_ROW_ID_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)
CORE_ROW_ID_RE = re.compile(r"^\|\s*`([^`]+\.core)`\s*\|", re.MULTILINE)

ACTIVATION_CHAPTER_COUNT = 55
ACTIVATION_SOURCE_COUNT = 316
AMENDMENT_SOURCE_COUNT = 326
CURRENT_COMPARATOR_SOURCE_ID = "ext_gated_deltanet2_2026"

# The completed roadmap's 2026-07-16 P7 authority.  It is loaded from its
# creation commit so later live files cannot silently redefine it.
ACTIVATION_RESULT_FILE_SHA256 = "a3093b4b17cd15ac2f59cdf9dbd9a5e2902f3d0dc52f2a1ed6a76258c5dc96fb"
ACTIVATION_RESULT_SEMANTIC_SHA256 = "f3cc1e0a80b657652a5a30dbfc11fc6334dcb14deb2e9955bf9d1b7597e510d7"
ACTIVATION_SCHEMA_FILE_SHA256 = "8b8420fd7a3fd4d41caff06589c01f2917c49a3becce1d9af42922d6f2290911"
ACTIVATION_APPENDIX_DIGESTS = {
    "appendices/C_claim_evidence_matrix.qmd": "d2c4bd33256eb27fc8afbd75d2ec0a8b16aa4eef4bdcae75568927cb9011801e",
    "appendices/E_codex_test_specs.qmd": "641578a68ac3c4394c0e3a82387c92a549d225d557781f9a8ceac5eea0d3b548",
    "appendices/F_changelog.qmd": "12e96c267769657ff82e1e4b922962db473bc0263ac43e0095045d8d60ce30bd",
    "appendices/H_external_sources.qmd": "ffe92dd8cd4ba405960c7fc0481972923a559e1980bb20694a78a9739dd6e218",
    "appendices/K_implementation_horizons.qmd": "2d7c20d4b372160444007841ed0cede8b74eb90be20d4ddb5c92846923487054",
}

# The unchanged tracked result is a later 326-source rebind.  Preserve its bytes
# and known difference scope, but never present it as contemporaneous P7 truth.
AMENDMENT_RESULT_FILE_SHA256 = "bc51dac1f127bd94fb17e919296ec1cef6f45f69fdad443a862297e10bd9e877"
AMENDMENT_RESULT_SEMANTIC_SHA256 = "009a8146d351a64ac3414e546dabbe9eb4e46c1d7df7ac11079ff9e308ae766f"
AMENDMENT_SCHEMA_FILE_SHA256 = "316be0e8aeb9b5a8124c2541700f2b3ae7998809be8398997a14dfb3aef6aa6e"
AMENDMENT_APPENDIX_DIGESTS = {
    "appendices/C_claim_evidence_matrix.qmd": "f003dafcd17b173f385ef3312e24f65187e867db00e8a969bff35d51f628183a",
    "appendices/E_codex_test_specs.qmd": "641578a68ac3c4394c0e3a82387c92a549d225d557781f9a8ceac5eea0d3b548",
    "appendices/F_changelog.qmd": "2c9ca71fe9704bbf5d7ccacf082eb1650aecb883811f2223d38c247e7d9c7610",
    "appendices/H_external_sources.qmd": "274705635fc6cbb0cbf2742ef3c8dee35333bc37e55938fc2ee2dabd44e74abb",
    "appendices/K_implementation_horizons.qmd": "2987dc5a2085a80a5eb5737aa98c89dfdb93b2a49ab94b8aa358236c2f086a78",
}

HISTORICAL_PACKET_DIGESTS_SHA256 = "83616012a3a9a9263f4a978ad1d5d2c7f3bca09b7ca9e7ce25621b7a64d72a68"
# P7.1a centralizes the invariant packet prose while preserving every
# activation-era chapter's data-bearing projection. Historical bytes remain
# pinned above; this digest governs the compact live projections only.
LIVE_COMPACT_PACKET_DIGESTS_SHA256 = "9ec4eea98ad28623458630a098ac6e0f67ebd622d532a58b79b02c1f4f8a68dd"
LINEAGE_LOCK_FILE_SHA256 = "8e2b683aea65c05f1cff216cf569343de2b6570ded40a2c74c7ee0fa4759b45b"
LINEAGE_LOCK_SEMANTIC_SHA256 = "7ce4f2c88b86488f78d4e0d4e7890cd89d3e76b4407984ba534dfb1f0b248618"
IMMUTABLE_ARTIFACT_DIGESTS = {
    "docs/p7_book_evidence_reconciliation.md": "012289e8deb94eb0dec1b72c74952340fb8e452ab872da7a953d0c0006957d24",
    "experiments/claim_family_terminal_coverage/results/result.json": "f8ef49c008ba303361235b8e5d2ff44fe907d03ba5a22cd41034acb2fee8ba27",
    "experiments/claim_family_bundle_coverage/result.json": "0fb2b4c51427ae6249311a58c6676725d643bc2aff42d092697cfad0caf5db25",
    "experiments/p6_external_reproduction/results/terminal_result.json": "aefde4bf4bb095de4af3e5b7a6411ee41f4998ab549f87792feef1b6e3a26e6b",
}

GOVERNED_APPENDICES = {
    "C": "appendices/C_claim_evidence_matrix.qmd",
    "E": "appendices/E_codex_test_specs.qmd",
    "F": "appendices/F_changelog.qmd",
    "G": "appendices/G_corben_source_corpus.qmd",
    "H": "appendices/H_external_sources.qmd",
    "K": "appendices/K_implementation_horizons.qmd",
}
LIVE_GOVERNANCE_CHECKS = (
    "scripts/validate_dynamic_spine.py",
    "scripts/validate_source_appendices.py",
    "scripts/validate_source_evidence_audit.py",
    "scripts/validate_implementation_horizons.py",
    "scripts/validate_book.py",
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def semantic_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha_bytes(payload)


def schema_error(value: Any, schema: dict[str, Any]) -> str | None:
    try:
        jsonschema.validate(value, schema)
    except jsonschema.ValidationError as error:
        return f"schema validation failed: {error.message}"
    return None


def normalized_result(value: dict[str, Any]) -> dict[str, Any]:
    """Remove only fields known to have been rebound after P7 activation."""
    normalized = copy.deepcopy(value)
    normalized["source_count"] = "<later-rebound>"
    normalized["appendix_digests"] = {
        relative: "<later-rebound>" for relative in normalized.get("appendix_digests", {})
    }
    for row in normalized.get("chapter_records", []):
        row["sha256"] = "<later-rebound>"
    return normalized


def reconstruct_activation_result(
    amendment: dict[str, Any], lineage: dict[str, Any]
) -> dict[str, Any]:
    """Recover the immutable activation record from the pinned lineage lock."""
    activation = copy.deepcopy(amendment)
    activation_lock = lineage.get("activation", {})
    activation["source_count"] = activation_lock.get("source_count")
    activation["appendix_digests"] = copy.deepcopy(activation_lock.get("appendix_digests", {}))
    chapter_digests = activation_lock.get("chapter_digests", {})
    for row in activation.get("chapter_records", []):
        row["sha256"] = chapter_digests.get(row.get("chapter_id"))
    return activation


def reconstruct_activation_schema(amendment_schema: dict[str, Any]) -> dict[str, Any]:
    activation_schema = copy.deepcopy(amendment_schema)
    activation_schema["properties"]["source_count"]["const"] = ACTIVATION_SOURCE_COUNT
    return activation_schema


def historical_errors(bundle: dict[str, Any]) -> list[str]:
    result = bundle["result"]
    contract = bundle["contract"]
    terminal = bundle["terminal"]
    schema = bundle["schema"]
    lineage = bundle["lineage"]
    out: list[str] = []
    validation_error = schema_error(result, schema)
    if validation_error:
        out.append(f"activation P7 {validation_error}")
    if semantic_sha(result) != ACTIVATION_RESULT_SEMANTIC_SHA256:
        out.append("activation-frozen P7 result facts or digests drifted")
    activation_lock = lineage.get("activation", {})
    later_lock = lineage.get("later_projection", {})
    if (
        semantic_sha(lineage) != LINEAGE_LOCK_SEMANTIC_SHA256
        or lineage.get("schema_version")
        != "asi_stack.p7_book_evidence_reconciliation.lineage_lock.v1"
        or activation_lock.get("commit") != ACTIVATION_COMMIT
        or activation_lock.get("result_file_sha256") != ACTIVATION_RESULT_FILE_SHA256
        or activation_lock.get("result_semantic_sha256") != ACTIVATION_RESULT_SEMANTIC_SHA256
        or activation_lock.get("schema_file_sha256") != ACTIVATION_SCHEMA_FILE_SHA256
        or activation_lock.get("chapter_count") != ACTIVATION_CHAPTER_COUNT
        or activation_lock.get("source_count") != ACTIVATION_SOURCE_COUNT
        or activation_lock.get("appendix_digests") != ACTIVATION_APPENDIX_DIGESTS
        or lineage.get("stable_packet_set_sha256") != HISTORICAL_PACKET_DIGESTS_SHA256
        or later_lock.get("commit") != AMENDMENT_COMMIT
        or later_lock.get("classification")
        != "later_historical_amendment_contaminated_current_projection_non_authoritative_for_p7_activation"
        or later_lock.get("result_file_sha256") != AMENDMENT_RESULT_FILE_SHA256
        or later_lock.get("result_semantic_sha256") != AMENDMENT_RESULT_SEMANTIC_SHA256
        or later_lock.get("schema_file_sha256") != AMENDMENT_SCHEMA_FILE_SHA256
        or later_lock.get("source_count") != AMENDMENT_SOURCE_COUNT
        or later_lock.get("changed_chapter_digest_count") != 37
        or later_lock.get("changed_appendix_digest_count") != 4
    ):
        out.append("P7 activation/amendment lineage lock drifted")

    records = result.get("chapter_records", [])
    chapter_ids = [row.get("chapter_id") for row in records]
    chapter_paths = [row.get("path") for row in records]
    if (
        result.get("chapter_count") != ACTIVATION_CHAPTER_COUNT
        or len(records) != ACTIVATION_CHAPTER_COUNT
        or len(set(chapter_ids)) != ACTIVATION_CHAPTER_COUNT
        or len(set(chapter_paths)) != ACTIVATION_CHAPTER_COUNT
    ):
        out.append("activation-frozen P7 chapter denominator or identity drifted")
    if any(row.get("path") != f"chapters/{row.get('chapter_id')}.qmd" for row in records):
        out.append("activation-frozen P7 chapter path binding drifted")
    if sum(row.get("atom_count", 0) for row in records) != 3745:
        out.append("activation-frozen P7 chapter atom coverage drifted")
    if Counter(row.get("core_disposition") for row in records) != {
        "blocked_after_full_attempt": 47,
        "narrowed_after_full_attempt": 8,
    }:
        out.append("activation-frozen P7 chapter-core dispositions drifted")
    if any(
        row.get(key) != 1
        for row in records
        for key in ("human_summary_count", "ai_packet_count", "argument_exit_table_count")
    ):
        out.append("activation-frozen P7 packet counts drifted")
    if result.get("source_count") != ACTIVATION_SOURCE_COUNT:
        out.append("activation-frozen P7 source denominator is not 316")
    if result.get("appendix_digests") != ACTIVATION_APPENDIX_DIGESTS:
        out.append("activation-frozen P7 appendix digest set drifted")

    scalar_keys = (
        "state",
        "chapter_count",
        "atom_count",
        "blocked_atom_count",
        "retained_atom_count",
        "narrowed_atom_count",
        "bounded_promotion_count",
        "source_count",
        "reader_projection_check_passed",
        "html_render_passed",
        "core_argument_count",
        "chapter_core_promotion_count",
        "support_state_effect",
        "publication_authority",
        "release_authority",
    )
    if any(result.get(key) != contract.get(key) for key in scalar_keys):
        out.append("activation result disagrees with the completed roadmap P7 contract")
    expected_paths = {
        "receipt_path": "docs/p7_book_evidence_reconciliation.md",
        "result_path": RESULT_RELATIVE,
        "schema_path": SCHEMA_RELATIVE,
        "validator_path": "scripts/validate_p7_book_evidence_reconciliation.py",
        "reconciliation_script_path": "scripts/reconcile_p7_chapter_evidence.py",
    }
    if any(contract.get(key) != value for key, value in expected_paths.items()):
        out.append("completed roadmap P7 artifact provenance drifted")
    if contract.get("appendix_digest_count") != len(ACTIVATION_APPENDIX_DIGESTS):
        out.append("completed roadmap P7 appendix denominator drifted")

    terminal_rows = terminal.get("dispositions", [])
    terminal_by_chapter: dict[str, list[dict[str, Any]]] = {}
    for row in terminal_rows:
        terminal_by_chapter.setdefault(str(row.get("chapter_id")), []).append(row)
    terminal_counts = Counter(row.get("terminal_disposition") for row in terminal_rows)
    expected_counts = {
        "blocked_after_full_attempt": result.get("blocked_atom_count"),
        "retained_after_full_attempt": result.get("retained_atom_count"),
        "narrowed_after_full_attempt": result.get("narrowed_atom_count"),
        "promoted_at_bounded_scope": result.get("bounded_promotion_count"),
    }
    if (
        terminal.get("atom_count") != 3745
        or len(terminal_rows) != 3745
        or terminal.get("all_atoms_terminal") is not True
        or dict(terminal_counts) != expected_counts
        or terminal.get("chapter_core_promotion_count") != 0
    ):
        out.append("frozen terminal ledger disagrees with the activation P7 totals")
    for record in records:
        chapter_id = str(record.get("chapter_id"))
        rows = terminal_by_chapter.get(chapter_id, [])
        cores = [row for row in rows if row.get("atom_id") == f"{chapter_id}.core"]
        if (
            len(rows) != record.get("atom_count")
            or len(cores) != 1
            or cores[0].get("terminal_disposition") != record.get("core_disposition")
        ):
            out.append(f"frozen terminal ledger crosswalk drifted: {chapter_id}")
    return out


def amendment_errors(bundle: dict[str, Any], activation: dict[str, Any]) -> list[str]:
    result = bundle["result"]
    schema = bundle["schema"]
    out: list[str] = []
    validation_error = schema_error(result, schema)
    if validation_error:
        out.append(f"later tracked P7 projection {validation_error}")
    if semantic_sha(result) != AMENDMENT_RESULT_SEMANTIC_SHA256:
        out.append("later tracked P7 projection facts or digests drifted")
    if result.get("source_count") != AMENDMENT_SOURCE_COUNT:
        out.append("later tracked P7 projection lost its recorded 326-source identity")
    if result.get("appendix_digests") != AMENDMENT_APPENDIX_DIGESTS:
        out.append("later tracked P7 projection appendix digests drifted")
    if normalized_result(result) != normalized_result(activation):
        out.append("later tracked P7 projection changed fields outside known source/digest rebinds")
    activation_chapter_digests = {
        row.get("chapter_id"): row.get("sha256") for row in activation.get("chapter_records", [])
    }
    amendment_chapter_digests = {
        row.get("chapter_id"): row.get("sha256") for row in result.get("chapter_records", [])
    }
    changed_chapter_digests = sum(
        activation_chapter_digests.get(chapter_id) != digest
        for chapter_id, digest in amendment_chapter_digests.items()
    )
    changed_appendix_digests = sum(
        ACTIVATION_APPENDIX_DIGESTS.get(relative) != digest
        for relative, digest in AMENDMENT_APPENDIX_DIGESTS.items()
    )
    if changed_chapter_digests != 37 or changed_appendix_digests != 4:
        out.append("later tracked P7 projection difference scope drifted")
    return out


def qmd_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def expected_test_rows(chapters: list[dict[str, Any]]) -> Counter[str]:
    rows: list[str] = []
    for chapter in chapters:
        tests = chapter.get("codex_tests") or []
        if not tests:
            rows.append(
                f"| `{chapter['id']}` | {qmd_escape(chapter.get('title'))} | "
                "No chapter-level test declared yet | planned | not run |"
            )
            continue
        for test in tests:
            if isinstance(test, dict):
                name = test.get("name", "Unnamed test")
                implementation = test.get("implementation_status", "planned")
                result = test.get("result_status", "not run")
            else:
                name, implementation, result = test, "planned", "not run"
            rows.append(
                f"| `{chapter['id']}` | {qmd_escape(chapter.get('title'))} | {qmd_escape(name)} | "
                f"{qmd_escape(implementation)} | {qmd_escape(result)} |"
            )
    return Counter(rows)


def expected_horizon_rows(chapters: list[dict[str, Any]]) -> Counter[str]:
    return Counter(
        f"| `{chapter['id']}` | {qmd_escape(chapter.get('title'))} | "
        f"{qmd_escape(chapter.get('minimal_implementation'))} | "
        f"{qmd_escape(chapter.get('beyond_state_of_art'))} | "
        f"`{qmd_escape(chapter.get('evidence_level'))}` |"
        for chapter in chapters
    )


def admitted_chapter_ids(status: dict[str, Any]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    tranche = status.get("quality_uplift_program", {}).get("structural_completeness_tranche", {})
    admitted: set[str] = set()
    for key in ("first_tranche", "second_tranche"):
        row = tranche.get(key, {})
        candidates = [str(value) for value in row.get("candidate_ids", [])]
        count = row.get("manifest_admitted_count")
        if count == 0:
            continue
        if count != len(candidates) or len(set(candidates)) != len(candidates):
            errors.append(f"{key} lacks an exact manifest-admitted identity set")
            continue
        admitted.update(candidates)
    return admitted, errors


def current_snapshot(
    activation: dict[str, Any],
) -> dict[str, Any]:
    structure = load(STRUCTURE)
    chapter_rows = [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    ]
    chapter_texts: dict[str, str] = {}
    missing_chapter_paths: list[str] = []
    for row in chapter_rows:
        relative = row.get("file", "") if isinstance(row, dict) else ""
        path = ROOT / relative
        if relative and path.is_file():
            chapter_texts[str(row.get("id"))] = path.read_text(encoding="utf-8", errors="ignore")
        else:
            missing_chapter_paths.append(str(relative))
    return {
        "structure": structure,
        "chapter_texts": chapter_texts,
        "missing_chapter_paths": missing_chapter_paths,
        "inventory": load(INVENTORY),
        "vectors": load(VECTORS),
        "current_status": load(CURRENT_STATUS),
        "historical_chapter_ids": {row.get("chapter_id") for row in activation.get("chapter_records", [])},
        "appendix_texts": {
            key: (ROOT / relative).read_text(encoding="utf-8", errors="ignore")
            for key, relative in GOVERNED_APPENDICES.items()
        },
    }


def current_errors(data: dict[str, Any]) -> list[str]:
    """Check current semantics without pinning mutable live counts or bytes."""
    out: list[str] = []
    raw_chapters = [
        chapter
        for part in data["structure"].get("parts", [])
        for chapter in part.get("chapters", [])
    ]
    chapters = [row for row in raw_chapters if isinstance(row, dict)]
    chapter_ids = [str(row.get("id")) for row in chapters]
    chapter_paths = [row.get("file") for row in chapters]
    live_ids = set(chapter_ids)
    historical_ids = set(data["historical_chapter_ids"])
    status = data["current_status"]
    admitted_ids, admission_errors = admitted_chapter_ids(status)
    out.extend(admission_errors)
    live_chapter_count = len(chapters)

    if (
        len(raw_chapters) != live_chapter_count
        or len(live_ids) != live_chapter_count
        or len(set(chapter_paths)) != live_chapter_count
        or data["missing_chapter_paths"]
    ):
        out.append("current live manifest lacks unique existing chapter identities and files")
    if live_ids != historical_ids | admitted_ids:
        out.append("current chapters escaped the activation P7 set plus manifest-admitted authority")

    packet_digests: dict[str, str] = {}
    for chapter_id in historical_ids & live_ids:
        text = data["chapter_texts"].get(str(chapter_id), "")
        if text.count(P7_START) != 1 or text.count(P7_END) != 1:
            out.append(f"current historical chapter lost its one P7 packet: {chapter_id}")
            continue
        packet = text[text.index(P7_START) : text.index(P7_END) + len(P7_END)]
        packet_digests[str(chapter_id)] = sha_bytes(packet.encode("utf-8"))
        required_live_fragments = (
            "## Evidence reconciliation (2026-07-16)",
            "living-book-methodology.qmd#chapter-evidence-packet-contract",
            "| Chapter-specific field | Value |",
            "| Family / atom denominator |",
            "| Terminal dispositions |",
            "| Core |",
            "| Core attempted / missing lanes |",
            "| Strongest family bundle |",
            "| Negative controls |",
            "| Accepted transitions |",
            "| Maximum inference |",
            "| Reproduction / next burden |",
        )
        if any(packet.count(fragment) != 1 for fragment in required_live_fragments):
            out.append(f"current historical chapter P7 packet shape drifted: {chapter_id}")
    if semantic_sha(packet_digests) != LIVE_COMPACT_PACKET_DIGESTS_SHA256:
        out.append("current historical P7 packet bytes drifted")
    for chapter_id in live_ids - historical_ids:
        text = data["chapter_texts"].get(str(chapter_id), "")
        if P7_START in text or P7_END in text:
            out.append(f"post-P7 chapter was laundered into the activation receipt: {chapter_id}")

    activation = status.get("activation_truth", {})
    tranche = status.get("quality_uplift_program", {}).get("structural_completeness_tranche", {})
    if (
        status.get("status") != "active"
        or status.get("roadmap_path") != CURRENT_ROADMAP
        or activation.get("live_working_chapter_count") != live_chapter_count
        or activation.get("chapter_core_argument_count") != live_chapter_count
        or activation.get("chapter_core_promotion_count") != 0
        or activation.get("total_structured_atom_count") != 3745
        or activation.get("blocked_after_full_attempt_atom_count") != 3698
        or tranche.get("current_manifest_chapter_count") != live_chapter_count
        or tranche.get("support_state_effect") != "none"
    ):
        out.append("current chapter authority or no-promotion boundary drifted")

    vectors = data["vectors"]
    vector_rows = vectors.get("vectors", [])
    vector_ids = [row.get("claim_id") for row in vector_rows]
    vector_summary = vectors.get("summary", {})
    if (
        len(vector_rows) != live_chapter_count
        or len(set(vector_ids)) != live_chapter_count
        or set(vector_ids) != {f"{chapter_id}.core" for chapter_id in live_ids}
        or any(row.get("summary_support_state") != "argument" for row in vector_rows)
        or vector_summary.get("vector_count") != live_chapter_count
        or vector_summary.get("summary_support_states") != {"argument": live_chapter_count}
        or vector_summary.get("automatic_support_state_changes") != 0
    ):
        out.append("current evidence vectors disagree with live argument-level chapter cores")

    inventory = data["inventory"]
    inventory_ids = [row.get("id") for row in inventory if isinstance(row, dict)]
    assigned_source_ids = {
        source_id for chapter in chapters for source_id in chapter.get("source_ids", [])
    }
    comparator_rows = [
        row for row in inventory if isinstance(row, dict) and row.get("id") == CURRENT_COMPARATOR_SOURCE_ID
    ]
    if (
        len(inventory_ids) != len(inventory)
        or len(set(inventory_ids)) != len(inventory)
        or len(inventory) < AMENDMENT_SOURCE_COUNT
        or not assigned_source_ids.issubset(set(inventory_ids))
        or len(comparator_rows) != 1
    ):
        out.append("current inventory lost uniqueness, the 326-source floor, assigned sources, or the P7 comparator")
    elif (
        comparator_rows[0].get("title")
        != "Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention"
        or comparator_rows[0].get("arxiv_id") != "2605.22791"
        or "not locally reproduced" not in str(comparator_rows[0].get("notes"))
    ):
        out.append("current P7 comparator metadata or reproduction boundary drifted")

    appendix = data["appendix_texts"]
    external_ids = {
        row.get("id")
        for row in inventory
        if isinstance(row, dict) and row.get("priority") == "external_literature"
    }
    corpus_ids = set(inventory_ids) - external_ids
    appendix_g_ids = set(SOURCE_ROW_ID_RE.findall(appendix["G"]))
    appendix_h_ids = set(SOURCE_ROW_ID_RE.findall(appendix["H"]))
    if appendix_g_ids != corpus_ids or appendix_h_ids != external_ids or appendix_g_ids & appendix_h_ids:
        out.append("current inventory and governed source appendices disagree")

    mapping_count = sum(len(row.get("claim_source_mappings", [])) for row in chapters)
    reviewed_mapping_count = sum(
        1
        for chapter in chapters
        for mapping in chapter.get("claim_source_mappings", [])
        if mapping.get("passage_refs")
        and str(mapping.get("passage_review_state", "")).lower() in {"reviewed", "accepted", "complete"}
    )
    appendix_c_ids = CORE_ROW_ID_RE.findall(appendix["C"])
    if (
        len(appendix_c_ids) != live_chapter_count
        or set(appendix_c_ids) != {f"{chapter_id}.core" for chapter_id in live_ids}
        or f"Current generated coverage: {live_chapter_count} chapter core claims, {mapping_count} exact claim-source mappings, {reviewed_mapping_count} passage-reviewed mappings" not in appendix["C"]
        or f"{live_chapter_count} chapter core claims remaining at `argument`" not in appendix["C"]
    ):
        out.append("current Appendix C disagrees with manifest claim/evidence coverage")

    appendix_e_table = appendix["E"].split("## Repository-Level Implemented Checks", 1)[0]
    actual_test_rows = Counter(
        line for line in appendix_e_table.splitlines() if line.startswith("| `")
    )
    if actual_test_rows != expected_test_rows(chapters):
        out.append("current Appendix E chapter test rows disagree with the manifest")

    actual_horizon_rows = Counter(line for line in appendix["K"].splitlines() if line.startswith("| `"))
    if (
        actual_horizon_rows != expected_horizon_rows(chapters)
        or f"Current generated coverage: {live_chapter_count} chapter implementation horizons." not in appendix["K"]
    ):
        out.append("current Appendix K implementation horizons disagree with the manifest")

    normalized_changelog = re.sub(r"\s+", " ", appendix["F"])
    if admitted_ids and (
        f"from {ACTIVATION_CHAPTER_COUNT} to {live_chapter_count} entries" not in normalized_changelog
        or any(
            str(row.get("title")) not in normalized_changelog
            for row in chapters
            if row.get("id") in admitted_ids
        )
    ):
        out.append("current Appendix F lacks the manifest-admission changelog boundary")

    substrate = data["chapter_texts"].get(
        "replaceable-cognitive-substrates-beyond-transformer-monoculture", ""
    )
    if "Gated DeltaNet-2" not in substrate or CURRENT_COMPARATOR_SOURCE_ID not in appendix["H"]:
        out.append("current comparator integration drifted")
    if (
        appendix["E"].count("candidate and strongest-comparator envelope unavailable") != 1
        or "P6 made a full access attempt and ended blocked" not in appendix["K"]
    ):
        out.append("current P6 appendix reconciliation drifted")
    return out


def run_check(command: list[str]) -> str | None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        return f"{' '.join(command)} failed: {detail}"
    return None


def run_mutation(
    base: dict[str, Any],
    errors: Callable[[dict[str, Any]], list[str]],
    label: str,
    mutation: Callable[[dict[str, Any]], None],
    failures: list[str],
    baseline_errors: set[str],
) -> None:
    candidate = copy.deepcopy(base)
    mutation(candidate)
    if not set(errors(candidate)) - baseline_errors:
        failures.append(f"negative mutation accepted: {label}")


def main() -> None:
    amendment_result = load(P7_RESULT)
    amendment_schema = load(P7_SCHEMA)
    lineage = load(LINEAGE_LOCK)
    activation_result = reconstruct_activation_result(amendment_result, lineage)
    activation_schema = reconstruct_activation_schema(amendment_schema)

    historical_bundle = {
        "result": activation_result,
        "schema": activation_schema,
        "contract": load(HISTORICAL_STATUS).get("p7_book_evidence_reconciliation_contract", {}),
        "terminal": load(TERMINAL),
        "lineage": lineage,
    }
    amendment_bundle = {"result": amendment_result, "schema": amendment_schema}
    current = current_snapshot(activation_result)

    failures = historical_errors(historical_bundle)
    failures.extend(amendment_errors(amendment_bundle, activation_result))
    failures.extend(current_errors(current))
    if sha(LINEAGE_LOCK) != LINEAGE_LOCK_FILE_SHA256:
        failures.append("P7 activation/amendment lineage lock file bytes drifted")
    if sha(P7_RESULT) != AMENDMENT_RESULT_FILE_SHA256:
        failures.append("later tracked P7 projection file bytes drifted")
    if sha(P7_SCHEMA) != AMENDMENT_SCHEMA_FILE_SHA256:
        failures.append("later tracked P7 projection schema bytes drifted")
    for relative, digest in IMMUTABLE_ARTIFACT_DIGESTS.items():
        path = ROOT / relative
        if not path.is_file() or sha(path) != digest:
            failures.append(f"immutable P7 dependency drifted: {relative}")

    for script in LIVE_GOVERNANCE_CHECKS:
        failure = run_check([sys.executable, script])
        if failure:
            failures.append(f"live governance check: {failure}")
    reader_failure = run_check([sys.executable, "scripts/build_reader_edition.py", "--check"])
    if reader_failure:
        failures.append(f"reader projection check: {reader_failure}")

    historical_mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("drop activation chapter", lambda value: value["result"]["chapter_records"].pop()),
        ("rewrite activation chapter digest", lambda value: value["result"]["chapter_records"][0].__setitem__("sha256", "0" * 64)),
        ("erase activation packet", lambda value: value["result"]["chapter_records"][0].__setitem__("ai_packet_count", 0)),
        ("erase activation gaps", lambda value: value["result"].__setitem__("blocked_atom_count", 0)),
        ("invent activation core movement", lambda value: value["result"].__setitem__("chapter_core_promotion_count", 1)),
        ("rewrite activation appendix digest", lambda value: value["result"]["appendix_digests"].__setitem__(next(iter(ACTIVATION_APPENDIX_DIGESTS)), "0" * 64)),
        ("forge activation atom count", lambda value: value["result"]["chapter_records"][0].__setitem__("atom_count", 1)),
        ("forge activation core disposition", lambda value: value["result"]["chapter_records"][0].__setitem__("core_disposition", "retained_after_full_attempt")),
        ("rebind activation chapter path", lambda value: value["result"]["chapter_records"][0].__setitem__("path", value["result"]["chapter_records"][1]["path"])),
        ("reorder activation chapters", lambda value: value["result"]["chapter_records"].reverse()),
        ("rewrite activation source count", lambda value: value["result"].__setitem__("source_count", AMENDMENT_SOURCE_COUNT)),
        ("rewrite completed P7 contract", lambda value: value["contract"].__setitem__("source_count", AMENDMENT_SOURCE_COUNT)),
        ("drop terminal atom", lambda value: value["terminal"]["dispositions"].pop()),
        ("rewrite terminal disposition", lambda value: value["terminal"]["dispositions"][0].__setitem__("terminal_disposition", "retained_after_full_attempt")),
        ("rewrite lineage lock", lambda value: value["lineage"]["activation"].__setitem__("source_count", AMENDMENT_SOURCE_COUNT)),
    ]
    historical_baseline_errors = set(historical_errors(historical_bundle))
    for label, mutation in historical_mutations:
        run_mutation(
            historical_bundle,
            historical_errors,
            label,
            mutation,
            failures,
            historical_baseline_errors,
        )

    amendment_mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("rebind amendment to live source count", lambda value: value["result"].__setitem__("source_count", len(current["inventory"]))),
        ("rewrite amendment invariant fact", lambda value: value["result"].__setitem__("atom_count", 1)),
        ("invent amendment appendix", lambda value: value["result"]["appendix_digests"].__setitem__("README.md", "0" * 64)),
    ]
    amendment_error_fn = lambda value: amendment_errors(value, activation_result)
    amendment_baseline_errors = set(amendment_error_fn(amendment_bundle))
    for label, mutation in amendment_mutations:
        run_mutation(
            amendment_bundle,
            amendment_error_fn,
            label,
            mutation,
            failures,
            amendment_baseline_errors,
        )

    historical_chapter_id = next(iter(current["historical_chapter_ids"]))
    admitted_ids, _ = admitted_chapter_ids(current["current_status"])
    admitted_chapter_id = next(iter(admitted_ids))
    current_mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("drop live chapter", lambda value: value["structure"]["parts"][0]["chapters"].pop()),
        ("duplicate live source", lambda value: value["inventory"].append(copy.deepcopy(value["inventory"][0]))),
        ("replace assigned comparator source", lambda value: next(row for row in value["inventory"] if row.get("id") == CURRENT_COMPARATOR_SOURCE_ID).__setitem__("id", "invented_source")),
        ("admitted chapter identity escape", lambda value: next(row for part in value["structure"]["parts"] for row in part["chapters"] if row.get("id") == admitted_chapter_id).__setitem__("id", "unadmitted-chapter")),
        ("erase live P7 packet marker", lambda value: value["chapter_texts"].__setitem__(historical_chapter_id, value["chapter_texts"][historical_chapter_id].replace(P7_START, "", 1))),
        ("rewrite live P7 packet bytes", lambda value: value["chapter_texts"].__setitem__(historical_chapter_id, value["chapter_texts"][historical_chapter_id].replace(P7_START, P7_START + "\nmutation", 1))),
        ("launder post-P7 chapter into receipt", lambda value: value["chapter_texts"].__setitem__(admitted_chapter_id, value["chapter_texts"][admitted_chapter_id] + f"\n{P7_START}\n{P7_END}\n")),
        ("erase Appendix C coverage", lambda value: value["appendix_texts"].__setitem__("C", value["appendix_texts"]["C"].replace("Current generated coverage:", "Erased coverage:", 1))),
        ("erase Appendix E test row", lambda value: value["appendix_texts"].__setitem__("E", value["appendix_texts"]["E"].replace(next(line for line in value["appendix_texts"]["E"].splitlines() if line.startswith("| `")), "", 1))),
        ("erase Appendix H source row", lambda value: value["appendix_texts"].__setitem__("H", value["appendix_texts"]["H"].replace(next(line for line in value["appendix_texts"]["H"].splitlines() if line.startswith("| `")), "", 1))),
        ("erase Appendix K horizon row", lambda value: value["appendix_texts"].__setitem__("K", value["appendix_texts"]["K"].replace(next(line for line in value["appendix_texts"]["K"].splitlines() if line.startswith("| `")), "", 1))),
        ("invent current core movement", lambda value: value["current_status"]["activation_truth"].__setitem__("chapter_core_promotion_count", 1)),
        ("promote current evidence vector", lambda value: value["vectors"]["vectors"][0].__setitem__("summary_support_state", "prototype-backed")),
        ("drift current chapter authority count", lambda value: value["current_status"]["activation_truth"].__setitem__("live_working_chapter_count", 1)),
    ]
    current_baseline_errors = set(current_errors(current))
    for label, mutation in current_mutations:
        run_mutation(
            current,
            current_errors,
            label,
            mutation,
            failures,
            current_baseline_errors,
        )

    if failures:
        raise SystemExit("P7 book reconciliation failed:\n - " + "\n - ".join(failures))
    live_chapter_count = sum(
        len(part.get("chapters", [])) for part in current["structure"].get("parts", [])
    )
    mutation_count = len(historical_mutations) + len(amendment_mutations) + len(current_mutations)
    print(
        "P7 book reconciliation passed: activation-frozen 55-chapter/316-source authority, 3,745 terminal "
        "atoms, 3,698 blocked gaps, and five historical appendix digests preserved; the unchanged later "
        f"contaminated-current 326-source projection is pinned as non-authoritative; current {live_chapter_count}-chapter/"
        f"{len(current['inventory'])}-source book, argument-level cores, governed appendices, and reader "
        f"projection validated dynamically; {mutation_count} mutations rejected and zero core movement."
    )


if __name__ == "__main__":
    main()
