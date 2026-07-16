#!/usr/bin/env python3
"""Validate the canonical post-v2.1 public release and roadmap identity."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "v2.3.0"
COMMIT = "e27661166e9105f37cb36d63b15795f80715ca24"
DIGEST = "ebb3cccb0841a15a49d7d20ee8d5c7f7dce97dac562ca05068025951274ee28c"
HISTORICAL_VERSION = "v2.2.0"
HISTORICAL_COMMIT = "e3d5348993cc5083604c85bd699bb0e36eb00de1"
HISTORICAL_DIGEST = "037563bc62792ecd968cf923b94e3082b02597f1b97f81b63fa59c6d083ee2db"
ROADMAP = "docs/post_v2_1_residual_and_transfer_roadmap.md"
SUCCESSOR = "docs/post_v2_2_implementation_completion_roadmap.md"
SUCCESSOR_STATUS = "roadmap_records/post_v2_2_implementation_completion_status.json"
ACTIVE_SUCCESSOR = "docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md"
ACTIVE_SUCCESSOR_STATUS = "roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json"
POST_V2_3_COMPLETION = "docs/post_v2_3_quality_floor_reader_completion_declaration.md"
POST_V2_3_NO_RELEASE = "release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json"
CURRENT_SUCCESSOR = "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
CURRENT_SUCCESSOR_STATUS = "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
NEXT_SUCCESSOR = "docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md"
NEXT_SUCCESSOR_STATUS = "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
PREDECESSOR = "docs/post_v2_evidence_roadmap.md"
RELEASE_RECORD = "release_records/2026-07-13-v2.3.0-qcsa-e2766116.json"
RIGHTS_TAG = "v2.3.0"


def read_json(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def snapshot() -> dict[str, object]:
    return {
        "config": read_json("status/public_status_config.json"),
        "policy": read_json("status/versioned_release_policy.json"),
        "roadmap_status": read_json("roadmap_records/post_v2_1_residual_and_transfer_status.json"),
        "successor_status": read_json(SUCCESSOR_STATUS),
        "active_successor_status": read_json(ACTIVE_SUCCESSOR_STATUS),
        "current_successor_status": read_json(CURRENT_SUCCESSOR_STATUS),
        "next_successor_status": read_json(NEXT_SUCCESSOR_STATUS),
        "release": read_json(RELEASE_RECORD),
        "structure": read_json("book_structure.json"),
        "vectors": read_json("evidence_quality/core_claim_vectors.json"),
        "citation": read_text("CITATION.cff"),
        "readme": read_text("README.md"),
        "index": read_text("index.qmd"),
        "publication": read_text("docs/publication_readiness.md"),
        "reproducibility": read_text("docs/release_reproducibility.md"),
        "public_contract": read_text("docs/public_status_contract.md"),
        "license": read_text("LICENSE.md"),
        "notice": read_text("NOTICE.md"),
        "predecessor": read_text(PREDECESSOR),
        "completion": read_text("docs/v2_3_completion_declaration.md"),
        "audit": read_text("docs/post_v2_1_public_truth_audit.md"),
        "active_roadmap_headers": [
            str(path.relative_to(ROOT))
            for path in sorted((ROOT / "docs").glob("*roadmap*.md"))
            if "Status: active canonical successor roadmap; unfinished work only"
            in path.read_text(encoding="utf-8", errors="ignore")[:1000]
        ],
    }


def mapping(value: object, label: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def validate(data: dict[str, object]) -> list[str]:
    errors: list[str] = []
    config = mapping(data["config"], "status config", errors)
    policy = mapping(data["policy"], "release policy", errors)
    status = mapping(data["roadmap_status"], "roadmap status", errors)
    successor = mapping(data["successor_status"], "successor roadmap status", errors)
    active_successor = mapping(data["active_successor_status"], "active successor roadmap status", errors)
    current_successor = mapping(data["current_successor_status"], "current successor roadmap status", errors)
    next_successor = mapping(data["next_successor_status"], "next successor roadmap status", errors)
    release = mapping(data["release"], "release record", errors)

    active_version = config.get("active_version")
    if active_version != VERSION:
        errors.append("canonical active_version is not the completed v2.3.0 release")
    if config.get("deployment_channel") != "latest":
        errors.append("canonical deployment channel is not latest")

    known = policy.get("known_releases", [])
    rows = [row for row in known if isinstance(row, dict) and row.get("version") == VERSION]
    if len(rows) != 1:
        errors.append("release policy must contain exactly one v2.3.0 row")
        row = {}
    else:
        row = rows[0]
    expected_policy = {
        "source_commit": COMMIT,
        "release_record": RELEASE_RECORD,
        "site_artifact_state": "published",
        "site_artifact_sha256": DIGEST,
    }
    for key, expected in expected_policy.items():
        if row.get(key) != expected:
            errors.append(f"v2.3.0 policy {key} disagrees with canonical value")
    archive_url = str(row.get("site_artifact_url", ""))
    if VERSION not in archive_url or COMMIT not in archive_url:
        errors.append("v2.3.0 archive URL is not tag-and-commit bound")
    historical_rows = [row for row in known if isinstance(row, dict) and row.get("version") == HISTORICAL_VERSION]
    if len(historical_rows) != 1:
        errors.append("historical v2.2.0 policy row is absent or duplicated")
    else:
        historical = historical_rows[0]
        if historical.get("source_commit") != HISTORICAL_COMMIT or historical.get("site_artifact_sha256") != HISTORICAL_DIGEST or historical.get("site_artifact_state") != "published":
            errors.append("historical v2.2.0 policy identity drifted")
    latest = mapping(policy.get("latest_channel"), "latest channel", errors)
    if latest.get("mutable") != "yes":
        errors.append("/latest/ must remain explicitly mutable")

    if release.get("source_tag") != VERSION or release.get("source_commit") != COMMIT:
        errors.append("exact release record tag or commit disagrees")
    formats = release.get("artifact_formats", [])
    if not isinstance(formats, list):
        errors.append("release artifact_formats must be a list")
        formats = []
    format_rows = {row.get("format"): row for row in formats if isinstance(row, dict)}
    for name in ["canonical_live_html", "immutable_html_site_archive"]:
        if format_rows.get(name, {}).get("status") != "published":
            errors.append(f"released HTML format {name} is not published")
    optional = format_rows.get("epub_docx_pdf_audio_and_curated_reader", {})
    if optional.get("status") != "not_applicable":
        errors.append("optional formats are represented as approved by v2.3.0")

    if status.get("status") != "completed" or status.get("roadmap_path") != ROADMAP:
        errors.append("completed roadmap machine authority is stale or absent")
    predecessor = mapping(status.get("predecessor"), "roadmap predecessor", errors)
    if predecessor.get("path") != PREDECESSOR or predecessor.get("state") != "completed":
        errors.append("completed predecessor authority disagrees")
    baseline = mapping(status.get("baseline"), "roadmap baseline", errors)
    if baseline.get("latest_immutable_release") != HISTORICAL_VERSION:
        errors.append("historical roadmap baseline no longer names v2.2.0")
    if successor.get("status") != "completed" or successor.get("roadmap_path") != SUCCESSOR:
        errors.append("completed successor roadmap machine authority is stale or absent")
    if active_successor.get("status") != "completed" or active_successor.get("roadmap_path") != ACTIVE_SUCCESSOR:
        errors.append("later completed successor roadmap machine authority is stale or absent")
    if current_successor.get("status") != "completed" or current_successor.get("roadmap_path") != CURRENT_SUCCESSOR:
        errors.append("terminal clean-handoff successor roadmap machine authority is stale or absent")
    if next_successor.get("status") != "active" or next_successor.get("roadmap_path") != NEXT_SUCCESSOR:
        errors.append("claim-proof/SOTA active successor roadmap machine authority is stale or absent")
    if data.get("active_roadmap_headers") != [NEXT_SUCCESSOR]:
        errors.append("public truth must expose exactly the claim-proof/SOTA active successor")

    structure = mapping(data["structure"], "book structure", errors)
    chapters = [c for p in structure.get("parts", []) if isinstance(p, dict) for c in p.get("chapters", [])]
    if len(chapters) != 55:
        errors.append("live manifest chapter count is not 55")
    vectors_obj = data["vectors"]
    vectors = vectors_obj.get("vectors", []) if isinstance(vectors_obj, dict) else vectors_obj
    if not isinstance(vectors, list) or len(vectors) != 55:
        errors.append("live evidence-vector count is not 55")
    elif any(row.get("summary_support_state") != "argument" for row in vectors if isinstance(row, dict)):
        errors.append("an evidence-vector core support state moved above argument")
    activation = mapping(next_successor.get("activation_baseline"), "claim-proof activation baseline", errors)
    expansion = mapping(next_successor.get("structural_expansion_contract"), "claim-proof structural expansion", errors)
    if activation.get("active_chapter_count") != 54 or activation.get("core_claim_count") != 54:
        errors.append("frozen 54-chapter claim-proof activation baseline drifted")
    if expansion.get("live_chapter_count") != 55 or expansion.get("support_state_effect") != "none":
        errors.append("authorized 55th-chapter expansion is absent or invented a support effect")

    citation = str(data["citation"])
    citation_fragments = [
        'url: "https://corbensorenson.github.io/asi-stack-book/"',
        'repository-code: "https://github.com/corbensorenson/asi-stack-book"',
    ]
    citation_fragments.extend(['version: "2.3.0"', 'date-released: "2026-07-13"', COMMIT, DIGEST])
    for fragment in citation_fragments:
        if fragment not in citation:
            errors.append(f"CITATION.cff missing canonical fragment: {fragment}")
    if re.search(r"^doi\s*:", citation, re.MULTILINE | re.IGNORECASE):
        errors.append("CITATION.cff invents a DOI")

    required_by_surface = {
        "README.md": (str(data["readme"]), [VERSION, ROADMAP, SUCCESSOR, SUCCESSOR_STATUS, ACTIVE_SUCCESSOR, ACTIVE_SUCCESSOR_STATUS, CURRENT_SUCCESSOR, CURRENT_SUCCESSOR_STATUS, NEXT_SUCCESSOR, NEXT_SUCCESSOR_STATUS, POST_V2_3_COMPLETION, POST_V2_3_NO_RELEASE, COMMIT, DIGEST, "all 54 chapter-core claims remain at `argument`", "root site and `/latest/` are mutable", "active canonical successor roadmap"]),
        "index.qmd": (str(data["index"]), [VERSION, ROADMAP, SUCCESSOR, SUCCESSOR_STATUS, ACTIVE_SUCCESSOR, ACTIVE_SUCCESSOR_STATUS, CURRENT_SUCCESSOR, CURRENT_SUCCESSOR_STATUS, NEXT_SUCCESSOR, NEXT_SUCCESSOR_STATUS, POST_V2_3_COMPLETION, POST_V2_3_NO_RELEASE, COMMIT, DIGEST, "all 54 chapter-core claims remain at `argument`", "root site and `/latest/` are mutable", "active canonical successor roadmap"]),
        "docs/publication_readiness.md": (str(data["publication"]), [VERSION, ROADMAP, SUCCESSOR, SUCCESSOR_STATUS, ACTIVE_SUCCESSOR, ACTIVE_SUCCESSOR_STATUS, CURRENT_SUCCESSOR, CURRENT_SUCCESSOR_STATUS, NEXT_SUCCESSOR, NEXT_SUCCESSOR_STATUS, POST_V2_3_NO_RELEASE, COMMIT, DIGEST, "all 54 chapter-core claims remain at `argument`", "root site and `/latest/` are mutable", "active canonical successor roadmap"]),
        "docs/release_reproducibility.md": (str(data["reproducibility"]), [VERSION, COMMIT, DIGEST, "root and `/latest/` are mutable", "Historical v1.0.0 citation"]),
        "docs/public_status_contract.md": (str(data["public_contract"]), [f"`active_version` currently reports" , active_version, SUCCESSOR, SUCCESSOR_STATUS, ACTIVE_SUCCESSOR, ACTIVE_SUCCESSOR_STATUS, CURRENT_SUCCESSOR, CURRENT_SUCCESSOR_STATUS, NEXT_SUCCESSOR, NEXT_SUCCESSOR_STATUS, POST_V2_3_NO_RELEASE, "active canonical successor roadmap", "root or `/latest/` commits remain mutable"]),
    }
    for name, (text, fragments) in required_by_surface.items():
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{name} missing current identity fragment: {fragment}")

    forbidden_current = {
        "index.qmd": ["v1.0.0 living-book release; v1.x evidence", "This release is a tagged v1.0.0 living-book baseline"],
        "docs/publication_readiness.md": ["ready for continued public\nv1.x work", "`CITATION.cff` is v1.0.0 metadata"],
        "docs/public_status_contract.md": ["`active_version` currently reports `v1.x-development`"],
    }
    lookup = {"index.qmd": str(data["index"]), "docs/publication_readiness.md": str(data["publication"]), "docs/public_status_contract.md": str(data["public_contract"])}
    for name, phrases in forbidden_current.items():
        for phrase in phrases:
            if phrase in lookup[name]:
                errors.append(f"{name} retains obsolete active identity: {phrase}")

    for name, text in {
        "LICENSE.md": str(data["license"]),
        "NOTICE.md": str(data["notice"]),
        "README.md": str(data["readme"]),
    }.items():
        if VERSION not in text:
            errors.append(f"{name} does not preserve the v2.2.0 rights boundary")
    if f"At exact tag `{RIGHTS_TAG}`" not in str(data["readme"]):
        errors.append("README rights summary does not name the current exact-tag boundary")
    if "At exact tag `v2.0.0`" in str(data["readme"]):
        errors.append("README rights summary still names v2.0.0 as current")

    completion_fragments = [VERSION, COMMIT, DIGEST, SUCCESSOR, ACTIVE_SUCCESSOR, ACTIVE_SUCCESSOR_STATUS, CURRENT_SUCCESSOR, CURRENT_SUCCESSOR_STATUS, RELEASE_RECORD, "29234323320", "29234640734", "closes P5, M7, and the roadmap", "Successor activated: 2026-07-13"]
    for fragment in completion_fragments:
        if fragment not in str(data["completion"]):
            errors.append(f"v2.3 completion declaration missing: {fragment}")
    return errors


def mutation_controls(base: dict[str, object]) -> list[str]:
    failures: list[str] = []
    mutations = []

    stale_version = copy.deepcopy(base)
    stale_version["config"]["active_version"] = HISTORICAL_VERSION
    mutations.append(("stale version", stale_version))

    stale_roadmap = copy.deepcopy(base)
    stale_roadmap["roadmap_status"]["status"] = "active"
    mutations.append(("stale roadmap", stale_roadmap))

    duplicate_successor = copy.deepcopy(base)
    duplicate_successor["active_roadmap_headers"] = [NEXT_SUCCESSOR, "docs/fake_roadmap.md"]
    mutations.append(("duplicate active successor", duplicate_successor))

    wrong_commit = copy.deepcopy(base)
    wrong_commit["release"]["source_commit"] = "0" * 40
    mutations.append(("wrong commit", wrong_commit))

    false_archive = copy.deepcopy(base)
    for row in false_archive["policy"]["known_releases"]:
        if row.get("version") == VERSION:
            row["site_artifact_state"] = "not_published"
    mutations.append(("false archive state", false_archive))

    wrong_rights = copy.deepcopy(base)
    wrong_rights["readme"] = str(wrong_rights["readme"]).replace(f"At exact tag `{RIGHTS_TAG}`", "At exact tag `v2.0.0`")
    mutations.append(("wrong rights tag", wrong_rights))

    invented_format = copy.deepcopy(base)
    for row in invented_format["release"]["artifact_formats"]:
        if row.get("format") == "epub_docx_pdf_audio_and_curated_reader":
            row["status"] = "published"
    mutations.append(("invented format approval", invented_format))

    for name, mutated in mutations:
        if not validate(mutated):
            failures.append(f"mutation was accepted: {name}")
    return failures


def main() -> None:
    data = snapshot()
    errors = validate(data)
    errors.extend(mutation_controls(data))
    if errors:
        print("Post-v2.1 public-truth validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Post-v2.1 public-truth validation passed: v2.3.0 release/commit/archive, "
        "completed predecessor/release/post-v2.3 roadmaps with the exact claim-proof/SOTA successor active, a frozen 54-claim activation baseline plus 55 live argument-level core claims, tag-bound rights, "
        "mutable latest channel, optional-format boundary, and 7 rejecting mutations."
    )


if __name__ == "__main__":
    main()
