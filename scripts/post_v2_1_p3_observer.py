#!/usr/bin/env python3
"""Separate full-state surface observer for the post-v2.1 P3 program."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def path_identity(path: Path) -> dict:
    if not path.exists() and not path.is_symlink():
        return {"state": "absent"}
    if path.is_file():
        return {"state": "file", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "size": path.stat().st_size}
    rows = []
    for member in sorted(path.rglob("*"), key=lambda value: value.relative_to(path).as_posix()):
        if member.is_file():
            rows.append({"path": member.relative_to(path).as_posix(), "sha256": hashlib.sha256(member.read_bytes()).hexdigest(), "size": member.stat().st_size})
    return {"state": "tree", "tree_sha256": canonical_sha(rows), "members": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--surface-map", type=Path, required=True)
    parser.add_argument("--state-root", type=Path, required=True)
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text())
    surface_map = json.loads(args.surface_map.read_text())
    expected = [row["surface_id"] for row in inventory["surfaces"]]
    records = []
    for surface_id in expected:
        relative = surface_map["surfaces"].get(surface_id)
        records.append({
            "surface_id": surface_id,
            "relative_path": relative,
            "identity": {"state": "unmapped"} if relative is None else path_identity(args.state_root / relative),
        })
    payload = {
        "observer_id": "post-v2-1-p3-separate-state-observer-v0",
        "inventory_content_sha256": inventory["content_sha256"],
        "surface_count": len(records),
        "complete_mapping": len(records) == 24 and all(row["identity"]["state"] != "unmapped" for row in records),
        "records": records,
    }
    payload["observation_sha256"] = canonical_sha(records)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
