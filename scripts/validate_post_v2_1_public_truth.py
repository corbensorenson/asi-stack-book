#!/usr/bin/env python3
"""Validate the canonical post-v2.1 public release and roadmap identity."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "v2.2.0"
COMMIT = "e3d5348993cc5083604c85bd699bb0e36eb00de1"
DIGEST = "037563bc62792ecd968cf923b94e3082b02597f1b97f81b63fa59c6d083ee2db"
ROADMAP = "docs/post_v2_1_residual_and_transfer_roadmap.md"
SUCCESSOR = "docs/post_v2_2_implementation_completion_roadmap.md"
SUCCESSOR_STATUS = "roadmap_records/post_v2_2_implementation_completion_status.json"
PREDECESSOR = "docs/post_v2_evidence_roadmap.md"
RELEASE_RECORD = "release_records/2026-07-11-v2.2.0-residual-transfer-e3d53489.json"


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
        "completion": read_text("docs/v2_2_completion_declaration.md"),
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
    release = mapping(data["release"], "release record", errors)

    active_version = config.get("active_version")
    if active_version != VERSION:
        errors.append("canonical active_version is not the completed v2.2.0 release")
    if config.get("deployment_channel") != "latest":
        errors.append("canonical deployment channel is not latest")

    known = policy.get("known_releases", [])
    rows = [row for row in known if isinstance(row, dict) and row.get("version") == VERSION]
    if len(rows) != 1:
        errors.append("release policy must contain exactly one v2.2.0 row")
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
            errors.append(f"v2.2.0 policy {key} disagrees with canonical value")
    archive_url = str(row.get("site_artifact_url", ""))
    if VERSION not in archive_url or COMMIT not in archive_url:
        errors.append("v2.2.0 archive URL is not tag-and-commit bound")
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
        errors.append("optional formats are represented as approved by v2.2.0")

    if status.get("status") != "completed" or status.get("roadmap_path") != ROADMAP:
        errors.append("completed roadmap machine authority is stale or absent")
    predecessor = mapping(status.get("predecessor"), "roadmap predecessor", errors)
    if predecessor.get("path") != PREDECESSOR or predecessor.get("state") != "completed":
        errors.append("completed predecessor authority disagrees")
    baseline = mapping(status.get("baseline"), "roadmap baseline", errors)
    if baseline.get("latest_immutable_release") != VERSION:
        errors.append("roadmap baseline names a stale immutable release")
    if successor.get("status") != "active" or successor.get("roadmap_path") != SUCCESSOR:
        errors.append("active successor roadmap machine authority is stale or absent")
    if data.get("active_roadmap_headers") != [SUCCESSOR]:
        errors.append("there must be exactly one active canonical successor roadmap")

    structure = mapping(data["structure"], "book structure", errors)
    chapters = [c for p in structure.get("parts", []) if isinstance(p, dict) for c in p.get("chapters", [])]
    if len(chapters) != 54:
        errors.append("manifest chapter count is not 54")
    vectors_obj = data["vectors"]
    vectors = vectors_obj.get("vectors", []) if isinstance(vectors_obj, dict) else vectors_obj
    if not isinstance(vectors, list) or len(vectors) != 54:
        errors.append("evidence-vector count is not 54")
    elif any(row.get("summary_support_state") != "argument" for row in vectors if isinstance(row, dict)):
        errors.append("an evidence-vector core support state moved above argument")

    citation = str(data["citation"])
    citation_fragments = [
        'url: "https://corbensorenson.github.io/asi-stack-book/"',
        'repository-code: "https://github.com/corbensorenson/asi-stack-book"',
    ]
    citation_fragments.extend(['version: "2.2.0"', 'date-released: "2026-07-11"', COMMIT])
    for fragment in citation_fragments:
        if fragment not in citation:
            errors.append(f"CITATION.cff missing canonical fragment: {fragment}")
    if re.search(r"^doi\s*:", citation, re.MULTILINE | re.IGNORECASE):
        errors.append("CITATION.cff invents a DOI")

    required_by_surface = {
        "README.md": (str(data["readme"]), [VERSION, ROADMAP, SUCCESSOR, SUCCESSOR_STATUS, COMMIT, DIGEST, "all 54 chapter-core claims remain at `argument`", "root site and `/latest/` are mutable"]),
        "index.qmd": (str(data["index"]), [VERSION, ROADMAP, SUCCESSOR, SUCCESSOR_STATUS, COMMIT, DIGEST, "all 54 chapter-core claims remain at `argument`", "root site and `/latest/` are mutable"]),
        "docs/publication_readiness.md": (str(data["publication"]), [VERSION, ROADMAP, SUCCESSOR, SUCCESSOR_STATUS, COMMIT, DIGEST, "All 54 chapter-core claims remain at `argument`", "root site and `/latest/` are mutable"]),
        "docs/release_reproducibility.md": (str(data["reproducibility"]), [VERSION, COMMIT, DIGEST, "root and `/latest/` are mutable", "Historical v1.0.0 citation"]),
        "docs/public_status_contract.md": (str(data["public_contract"]), [f"`active_version` currently reports" , active_version, SUCCESSOR, SUCCESSOR_STATUS, "root or `/latest/` commits remain mutable"]),
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
    if f"At exact tag `{active_version}`" not in str(data["readme"]):
        errors.append("README rights summary does not name the active exact-tag boundary")
    if "At exact tag `v2.0.0`" in str(data["readme"]):
        errors.append("README rights summary still names v2.0.0 as current")

    completion_fragments = [VERSION, COMMIT, DIGEST, ROADMAP, SUCCESSOR, "Successor activated: 2026-07-13", "29177953198", "29178074691", "closes M5"]
    for fragment in completion_fragments:
        if fragment not in str(data["completion"]):
            errors.append(f"v2.2 completion declaration missing: {fragment}")
    return errors


def mutation_controls(base: dict[str, object]) -> list[str]:
    failures: list[str] = []
    mutations = []

    stale_version = copy.deepcopy(base)
    stale_version["config"]["active_version"] = "v2.0.0"
    mutations.append(("stale version", stale_version))

    stale_roadmap = copy.deepcopy(base)
    stale_roadmap["roadmap_status"]["status"] = "active"
    mutations.append(("stale roadmap", stale_roadmap))

    wrong_commit = copy.deepcopy(base)
    wrong_commit["release"]["source_commit"] = "0" * 40
    mutations.append(("wrong commit", wrong_commit))

    false_archive = copy.deepcopy(base)
    for row in false_archive["policy"]["known_releases"]:
        if row.get("version") == VERSION:
            row["site_artifact_state"] = "not_published"
    mutations.append(("false archive state", false_archive))

    wrong_rights = copy.deepcopy(base)
    active = str(wrong_rights["config"].get("active_version"))
    wrong_rights["readme"] = str(wrong_rights["readme"]).replace(f"At exact tag `{active}`", "At exact tag `v2.0.0`")
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
        "Post-v2.1 public-truth validation passed: v2.2.0 release/commit/archive, "
        "completed release roadmap plus one active successor, 54 argument-level core claims, tag-bound rights, "
        "mutable latest channel, optional-format boundary, and 6 rejecting mutations."
    )


if __name__ == "__main__":
    main()
