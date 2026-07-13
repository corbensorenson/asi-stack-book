#!/usr/bin/env python3
"""Generate path-level licensing provenance classifications without granting rights."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any

from build_canonical_public_status import ROOT, load_json


POLICY = ROOT / "licensing" / "provenance_policy.json"
OUTPUT = ROOT / "licensing" / "provenance_inventory.json"
DECISION = ROOT / "governance" / "licensing_decision.json"
RELEASE = "v2.3.0"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_paths() -> list[str]:
    tag = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{RELEASE}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if tag.returncode == 0:
        body = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "-z", RELEASE],
            cwd=ROOT,
        )
        return sorted(item.decode("utf-8") for item in body.split(b"\0") if item)
    body = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    paths = {
        item.decode("utf-8")
        for item in body.split(b"\0")
        if item and (ROOT / item.decode("utf-8")).exists()
    }
    paths.add(OUTPUT.relative_to(ROOT).as_posix())
    return sorted(paths)


def compile_rules(policy: dict[str, Any]) -> list[tuple[dict[str, Any], re.Pattern[str]]]:
    compiled = []
    for rule in policy.get("rules", []):
        compiled.append((rule, re.compile(str(rule["path_regex"]))))
    return compiled


def classify(path: str, compiled: list[tuple[dict[str, Any], re.Pattern[str]]], default: dict[str, Any]) -> dict[str, Any]:
    rule = next((record for record, pattern in compiled if pattern.search(path)), default)
    return {
        "path": path,
        "rule_id": rule["id"],
        "artifact_class": rule["artifact_class"],
        "provenance_status": rule["provenance_status"],
        "candidate_lane": rule["candidate_lane"],
        "current_effect": "all_rights_reserved_no_permission_granted",
        "blocking_reason": rule["blocking_reason"],
    }


def build_inventory() -> dict[str, Any]:
    policy = load_json(POLICY)
    decision = load_json(DECISION)
    paths = source_paths()
    compiled = compile_rules(policy)
    rows = [classify(path, compiled, policy["default_rule"]) for path in paths]
    by_class = Counter(row["artifact_class"] for row in rows)
    by_status = Counter(row["provenance_status"] for row in rows)
    by_lane = Counter(row["candidate_lane"] for row in rows)
    path_set_digest = hashlib.sha256(("\n".join(paths) + "\n").encode("utf-8")).hexdigest()
    return {
        "schema_version": "asi_stack.licensing_provenance_inventory.v0",
        "decision_state": decision["status"],
        "operative_license": policy["operative_license"],
        "generated_from": {
            "policy": POLICY.relative_to(ROOT).as_posix(),
            "policy_sha256": sha256_file(POLICY),
            "file_set_command": policy["file_set_command"],
            "path_set_sha256": path_set_digest,
        },
        "summary": {
            "file_count": len(rows),
            "by_artifact_class": dict(sorted(by_class.items())),
            "by_provenance_status": dict(sorted(by_status.items())),
            "by_candidate_lane": dict(sorted(by_lane.items())),
            "unknown_quarantine_count": by_status.get("unknown_quarantine", 0),
        },
        "files": rows,
        "non_claims": [
            "This inventory grants no license and makes no legal ownership determination.",
            "Candidate lanes are implementation-planning categories only; every path remains governed by LICENSE.md.",
            "No path is cleared until author assertions, third-party review, contribution terms, and any qualified legal review are recorded."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    inventory = build_inventory()
    body = json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != body:
            raise SystemExit(f"{OUTPUT.relative_to(ROOT)} is stale; run builder without --check")
        print(
            f"Licensing provenance inventory current: {inventory['summary']['file_count']} paths, "
            f"{inventory['summary']['unknown_quarantine_count']} unknown-quarantine path(s)."
        )
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(body, encoding="utf-8")
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)}: {inventory['summary']['file_count']} paths, "
        f"{inventory['summary']['unknown_quarantine_count']} unknown-quarantine path(s)."
    )


if __name__ == "__main__":
    main()
