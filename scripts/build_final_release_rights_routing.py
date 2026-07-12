#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "licensing/provenance_inventory.json"
OUTPUT = ROOT / "licensing/final_release_rights_routing.json"
CC = "CC-BY-4.0"
APACHE = "Apache-2.0"
EXCLUDED = "excluded-no-grant"


def exact_release_paths() -> set[str] | None:
    """Return the tagged v2.2.0 tree once it exists, else prepublication mode."""
    check = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", "refs/tags/v2.2.0^{commit}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if check.returncode != 0:
        return None
    body = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "v2.2.0"],
        cwd=ROOT,
        text=True,
    )
    return {line for line in body.splitlines() if line}


def route(record: dict, release_paths: set[str] | None) -> tuple[str, str]:
    path = record["path"]
    lane = record["candidate_lane"]
    provenance = record["provenance_status"]
    if release_paths is not None and path not in release_paths:
        return EXCLUDED, "post-tag path; not present in the exact v2.2.0 release tree"
    if path == "LICENSE.md":
        return EXCLUDED, "operative routing document; not self-licensed"
    if path.startswith("licenses/"):
        return EXCLUDED, "verbatim third-party license text retained under its own terms"
    if lane == "prose_or_figures_candidate" and provenance in {
        "author_ownership_assertion_required", "author_assertion_and_embedded_asset_review_required"
    }:
        return CC, "author-created prose/figure lane cleared for the completed HTML/live-book release"
    if lane == "software_candidate" and provenance == "author_ownership_assertion_required":
        return APACHE, "author-created software/proof/schema/automation lane cleared for release"
    if lane == "metadata_candidate" and provenance == "author_ownership_assertion_required":
        return CC, "author-created public metadata/governance record cleared as documentation"
    return EXCLUDED, f"excluded from grant: {lane}; {provenance}"


def build() -> dict:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    release_paths = exact_release_paths()
    records = []
    for item in inventory["files"]:
        license_id, basis = route(item, release_paths)
        records.append({
            "path": item["path"],
            "artifact_class": item["artifact_class"],
            "provenance_status": item["provenance_status"],
            "license_route": license_id,
            "review_basis": basis,
        })
    counts = Counter(item["license_route"] for item in records)
    return {
        "schema_version": "asi_stack.final_release_rights_routing.v1",
        "release_candidate": "v2.2.0",
        "decision_date": "2026-07-11",
        "selected_formats": ["html-live-book"],
        "license_texts": {
            CC: {"path": "licenses/CC-BY-4.0.txt", "official_url": "https://creativecommons.org/licenses/by/4.0/legalcode.txt", "normalized_sha256": "fe7b4ce83b8381cc5b216bbb4af73c570688d1b819c73bbaed8ca401f4677cd6"},
            APACHE: {"path": "licenses/Apache-2.0.txt", "official_url": "https://www.apache.org/licenses/LICENSE-2.0.txt", "normalized_sha256": "58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd"},
        },
        "summary": {"path_count": len(records), "by_license_route": dict(sorted(counts.items())), "unresolved_count": 0},
        "files": records,
        "non_claims": [
            "Excluded paths receive no license grant from this release.",
            "The v2.2.0 routing review is an internal authorship/provenance decision, not legal advice or third-party clearance.",
            "Trademarks, endorsement, patents outside Apache-2.0, privacy, publicity, and third-party rights are not granted.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    value = build()
    body = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        OUTPUT.write_text(body, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(ROOT)}: {value['summary']}")
    elif not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != body:
        raise SystemExit("Final-release rights routing is stale; run with --write")
    else:
        print(f"Final-release rights routing passed: {value['summary']}")


if __name__ == "__main__":
    main()
