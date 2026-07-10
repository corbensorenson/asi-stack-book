#!/usr/bin/env python3
"""Build the moving latest mirror and honest immutable-release metadata index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tempfile
from typing import Any

from build_canonical_public_status import ROOT, load_json


POLICY = ROOT / "status" / "versioned_release_policy.json"
STATUS_REL = Path("status/canonical-public-status.json")
INDEX_REL = Path("versions/index.json")


def build_index(status: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.versioned_release_index.v0",
        "latest": {
            "url": policy["latest_channel"]["url"],
            "source_commit": status["source_commit"],
            "status_id": status["status_id"],
            "mutable": "yes",
        },
        "immutable_storage_authority": policy["immutable_channel"]["storage_authority"],
        "releases": policy["known_releases"],
        "non_claims": policy["non_claims"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--allow-local", action="store_true")
    args = parser.parse_args()
    site = args.site if args.site.is_absolute() else ROOT / args.site
    status_path = site / STATUS_REL
    if not status_path.exists():
        raise SystemExit(f"rendered site missing {STATUS_REL}")
    status = load_json(status_path)
    policy = load_json(POLICY)
    if not args.allow_local and (
        status.get("source_tree_state") != "clean" or status.get("build_context") != "tested_commit"
    ):
        raise SystemExit("release-channel build requires canonical status from a clean tested commit")

    for channel in (site / "latest", site / "versions"):
        if channel.exists():
            shutil.rmtree(channel)
    with tempfile.TemporaryDirectory(prefix="asi-stack-latest-") as temp:
        snapshot = Path(temp) / "site"
        shutil.copytree(site, snapshot)
        shutil.copytree(snapshot, site / "latest")
    index_path = site / INDEX_REL
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(build_index(status, policy), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Built moving latest mirror for {status['source_commit'][:12]} and "
        f"immutable release index with {len(policy['known_releases'])} release row(s)."
    )


if __name__ == "__main__":
    main()
