#!/usr/bin/env python3
"""Build the single public status record for a source tree or tested commit.

The tracked config contains policy only. Counts, order, state distributions,
digests, commit identity, tree state, and build time are derived at execution.
Release automation writes the complete record into the rendered site so the
uploaded artifact carries the exact status envelope used by downstream checks.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from validate_external_sota_positioning import chapter_rows as external_positioning_rows


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "status" / "public_status_config.json"
SCHEMA = ROOT / "schemas" / "canonical_public_status.schema.json"
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
DISPOSITIONS = ROOT / "claim_decisions" / "v1_x_core_claim_dispositions.json"
RELEASE_PROFILES = ROOT / "editions" / "release_profiles.json"
CLAIM_IDENTITY_GRAPH = ROOT / "evidence_quality" / "claim_identity_graph.json"
TRANSITION_DIRS = (
    ROOT / "evidence_transitions" / "v1_0_measured",
    ROOT / "evidence_transitions" / "v1_x_measured",
)
GENERATED_STATUS_BEGIN = "<!-- canonical-status:generated-begin -->"
GENERATED_STATUS_END = "<!-- canonical-status:generated-end -->"


def public_status_summary_block(status: dict[str, Any]) -> str:
    counts = status["counts"]
    promoted = status["transition_counts"]["promoted_core_claims"]
    identity = status["claim_identity"]
    return (
        f"{GENERATED_STATUS_BEGIN}\n"
        "_Current canonical metrics (generated from machine records): "
        f"**{counts['chapters']} manifest chapters; {counts['sources']} public-safe records; "
        f"{counts['chapters']} chapter-core claims; "
        f"{counts['externally_positioned_chapters']}/{counts['chapters']} chapters externally positioned; "
        f"{promoted} promoted core claims; "
        f"{identity['resolved_transition_count']}/{identity['review_accepted_transition_count']} accepted transitions identity-resolved "
        f"({identity['direct_atom_relation_count']} direct, {identity['subclaim_relation_count']} subclaim, "
        f"{identity['proxy_relation_count']} proxy; {identity['parent_support_movements']} parent movements).**_\n"
        f"{GENERATED_STATUS_END}"
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def validate_against_schema(value: Any, schema: dict[str, Any], path: str = "status") -> list[str]:
    """Validate the JSON Schema keywords used by the canonical-status contract."""
    errors: list[str] = []
    expected = schema.get("type")
    type_ok = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
    }.get(expected, True)
    if not type_ok:
        return [f"{path}: expected {expected}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in {schema['enum']!r}")
    if isinstance(value, str):
        if len(value) < int(schema.get("minLength", 0)):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and not re.search(str(schema["pattern"]), value):
            errors.append(f"{path}: string does not match {schema['pattern']!r}")
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in schema:
        if value < int(schema["minimum"]):
            errors.append(f"{path}: value is below minimum {schema['minimum']}")
    if isinstance(value, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{index}]"))
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required if isinstance(required, list) else []:
            if key not in value:
                errors.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        properties = properties if isinstance(properties, dict) else {}
        additional = schema.get("additionalProperties", True)
        for key, child in value.items():
            if key in properties and isinstance(properties[key], dict):
                errors.extend(validate_against_schema(child, properties[key], f"{path}.{key}"))
            elif additional is False:
                errors.append(f"{path}: unexpected key {key!r}")
            elif isinstance(additional, dict):
                errors.extend(validate_against_schema(child, additional, f"{path}.{key}"))
    return errors


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def source_commit() -> str:
    candidate = os.environ.get("GITHUB_SHA") or run_git("rev-parse", "HEAD")
    value = candidate.strip().lower()
    if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError(f"source commit must be a full 40-character SHA: {candidate!r}")
    return value


def source_tree_state() -> str:
    return "dirty" if run_git("status", "--porcelain", "--untracked-files=all") else "clean"


def build_timestamp() -> str:
    configured = os.environ.get("CANONICAL_STATUS_BUILD_TIMESTAMP") or os.environ.get("GITHUB_RUN_STARTED_AT")
    if configured:
        value = configured.strip()
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def public_path(source_path: str) -> str:
    path = Path(source_path)
    return str(path.with_suffix(".html"))


def accepted_transition_counts() -> tuple[int, int]:
    upward = 0
    blocks = 0
    seen: set[str] = set()
    for directory in TRANSITION_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            record = load_json(path)
            if not isinstance(record, dict):
                raise TypeError(f"{path.relative_to(ROOT)} must contain an object")
            identity = str(record.get("transition_id") or path.resolve())
            if identity in seen:
                continue
            seen.add(identity)
            accepted = (
                record.get("transition_validity_state") == "review_accepted"
                and record.get("review_status") == "accepted"
            )
            if not accepted:
                continue
            if record.get("transition_effect") == "upward":
                upward += 1
            if (
                record.get("transition_effect") == "no_change"
                and record.get("support_state_effect") == "blocks_promotion"
            ):
                blocks += 1
    return upward, blocks


def build_status(
    *,
    timestamp: str | None = None,
    source_commit_override: str | None = None,
    source_tree_state_override: str | None = None,
) -> dict[str, Any]:
    config = load_json(CONFIG)
    structure = load_json(STRUCTURE)
    inventory = load_json(INVENTORY)
    dispositions = load_json(DISPOSITIONS)
    identity_graph = load_json(CLAIM_IDENTITY_GRAPH)
    if not isinstance(config, dict) or not isinstance(structure, dict):
        raise TypeError("public status config and book structure must contain objects")
    if not isinstance(inventory, list):
        raise TypeError("source inventory must contain a list")
    if not isinstance(dispositions, dict) or not isinstance(dispositions.get("summary"), dict):
        raise TypeError("core claim dispositions must contain a summary object")
    if not isinstance(identity_graph, dict) or not isinstance(identity_graph.get("summary"), dict):
        raise TypeError("claim identity graph must contain a summary object")

    chapters = [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]
    appendices = [row for row in structure.get("appendices", []) if isinstance(row, dict)]
    chapter_order = [
        {
            "position": index,
            "id": str(chapter["id"]),
            "title": str(chapter["title"]),
            "source_path": str(chapter["file"]),
            "public_path": public_path(str(chapter["file"])),
        }
        for index, chapter in enumerate(chapters, start=1)
    ]
    appendix_order = [
        {
            "position": index,
            "id": str(row.get("id") or Path(str(row["file"])).stem),
            "title": str(row["title"]),
            "source_path": str(row["file"]),
            "public_path": public_path(str(row["file"])),
        }
        for index, row in enumerate(appendices, start=1)
    ]
    positioning_rows = external_positioning_rows()
    if len(positioning_rows) != len(chapters):
        raise ValueError("external-positioning audit row count does not match manifest chapter count")
    externally_positioned = sum(1 for row in positioning_rows if row["status"] == "positioned")
    upward, blocks = accepted_transition_counts()
    summary = dispositions["summary"]
    identity_summary = identity_graph["summary"]
    commit = source_commit_override or source_commit()
    tree_state = source_tree_state_override or source_tree_state()
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise ValueError("source_commit_override must be a full lowercase SHA")
    if tree_state not in {"clean", "dirty"}:
        raise ValueError("source_tree_state_override must be clean or dirty")
    built_at = timestamp or build_timestamp()
    order_bytes = json.dumps(chapter_order, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    status = {
        "schema_version": str(config["schema_version"]),
        "status_id": f"{config['active_version']}:{commit[:12]}:{sha256_bytes(order_bytes)[:12]}",
        "active_version": str(config["active_version"]),
        "baseline_release": str(config["baseline_release"]),
        "release_profile": str(config["release_profile"]),
        "deployment_channel": str(config["deployment_channel"]),
        "site_url": str(config["site_url"]),
        "source_commit": commit,
        "source_tree_state": tree_state,
        "build_context": "tested_commit" if tree_state == "clean" else "local_worktree",
        "build_timestamp": built_at,
        "counts": {
            "parts": len(structure.get("parts", [])),
            "chapters": len(chapters),
            "sources": len(inventory),
            "appendices": len(appendices),
            "expected_book_pages": len(structure.get("front_matter", [])) + len(chapters) + len(appendices),
            "externally_positioned_chapters": externally_positioned,
        },
        "claim_state_distribution": {
            "claim_labels": dict(sorted(Counter(str(chapter.get("claim_label")) for chapter in chapters).items())),
            "support_states": dict(sorted(Counter(str(chapter.get("evidence_level")) for chapter in chapters).items())),
        },
        "transition_counts": {
            "core_no_change_dispositions": int(summary["accepted_core_transition_dispositions"]),
            "core_no_promotion_dispositions": int(summary["accepted_no_promotion_dispositions"]),
            "promoted_core_claims": int(summary["promoted_core_claims"]),
            "accepted_non_core_upward_transitions": upward,
            "accepted_blocks_promotion_decisions": blocks,
        },
        "claim_identity": {
            "review_accepted_transition_count": int(identity_summary["review_accepted_transition_count"]),
            "resolved_transition_count": int(identity_summary["resolved_transition_count"]),
            "unresolved_transition_count": int(identity_summary["unresolved_transition_count"]),
            "canonical_atom_count": int(identity_summary["canonical_atom_count"]),
            "direct_atom_relation_count": int(identity_summary["relation_counts"]["atom"]),
            "subclaim_relation_count": int(identity_summary["relation_counts"]["subclaim_of"]),
            "proxy_relation_count": int(identity_summary["relation_counts"]["proxy_for"]),
            "parent_support_movements": 0,
        },
        "digests": {
            "book_structure_sha256": sha256_file(STRUCTURE),
            "source_inventory_sha256": sha256_file(INVENTORY),
            "claim_dispositions_sha256": sha256_file(DISPOSITIONS),
            "release_profiles_sha256": sha256_file(RELEASE_PROFILES),
            "chapter_order_sha256": sha256_bytes(order_bytes),
            "claim_identity_graph_sha256": sha256_file(CLAIM_IDENTITY_GRAPH),
        },
        "chapter_order": chapter_order,
        "appendix_order": appendix_order,
        "non_claims": [
            "This status record reports repository and release metadata, not a validated ASI implementation.",
            "A clean tested commit and successful render do not prove model quality, safety, security, or chapter-core claims.",
            "A dirty local-worktree record is not a release or deployment attestation.",
            "External positioning and source counts do not imply exhaustive literature coverage or reproduced results."
        ],
    }
    validate_status_shape(status)
    schema = load_json(SCHEMA)
    if not isinstance(schema, dict):
        raise TypeError("canonical public status schema must contain an object")
    schema_errors = validate_against_schema(status, schema)
    if schema_errors:
        raise ValueError("canonical public status schema validation failed:\n - " + "\n - ".join(schema_errors))
    return status


def validate_status_shape(status: dict[str, Any]) -> None:
    required = {
        "schema_version", "status_id", "active_version", "baseline_release", "release_profile",
        "deployment_channel", "site_url", "source_commit", "source_tree_state", "build_context",
        "build_timestamp", "counts", "claim_state_distribution", "transition_counts", "claim_identity", "digests",
        "chapter_order", "appendix_order", "non_claims",
    }
    missing = sorted(required - set(status))
    if missing:
        raise ValueError("canonical status missing fields: " + ", ".join(missing))
    chapters = int(status["counts"]["chapters"])
    sources = int(status["counts"]["sources"])
    if chapters != len(status["chapter_order"]):
        raise ValueError("chapter count does not match chapter order length")
    if sum(status["claim_state_distribution"]["support_states"].values()) != chapters:
        raise ValueError("support-state distribution does not match chapter count")
    if sum(status["claim_state_distribution"]["claim_labels"].values()) != chapters:
        raise ValueError("claim-label distribution does not match chapter count")
    if chapters <= 0 or sources <= 0:
        raise ValueError("chapter and source counts must be positive")
    if not 0 <= int(status["counts"]["externally_positioned_chapters"]) <= chapters:
        raise ValueError("externally positioned chapter count must be within manifest chapter bounds")
    identity = status["claim_identity"]
    if identity["resolved_transition_count"] != identity["review_accepted_transition_count"]:
        raise ValueError("accepted transition identity graph is not fully resolved")
    if identity["unresolved_transition_count"] != 0 or identity["parent_support_movements"] != 0:
        raise ValueError("claim identity graph permits unresolved identity or parent support movement")
    relation_total = (
        identity["direct_atom_relation_count"]
        + identity["subclaim_relation_count"]
        + identity["proxy_relation_count"]
    )
    if relation_total != identity["resolved_transition_count"]:
        raise ValueError("claim identity relation counts do not equal resolved transitions")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Write the complete status record to this path; otherwise print JSON.")
    parser.add_argument("--timestamp", help="Explicit ISO-8601 build timestamp for deterministic tests.")
    args = parser.parse_args()
    status = build_status(timestamp=args.timestamp)
    body = json.dumps(status, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(body, encoding="utf-8")
        print(
            f"Canonical public status wrote {output.relative_to(ROOT)}: "
            f"{status['counts']['chapters']} chapters, {status['counts']['sources']} sources, "
            f"tree={status['source_tree_state']}."
        )
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
