#!/usr/bin/env python3
"""Record remote container-manifest availability for the P2 development pool."""

from __future__ import annotations

import base64
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / "experiments/p2_governed_repository_admission/corpus/development_pool.json"
OUT = ROOT / "experiments/p2_governed_repository_admission/corpus/image_manifest_receipts.json"


def main() -> None:
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    receipts = []
    for row in pool["rows"]:
        proc = subprocess.run(
            ["docker", "manifest", "inspect", "--verbose", row["image_name"]],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode:
            raise SystemExit(f"manifest unavailable for {row['instance_id']}: {proc.stderr.strip()}")
        manifest = json.loads(proc.stdout)
        descriptor = manifest["Descriptor"]
        raw = json.loads(base64.b64decode(manifest["Raw"]))
        receipts.append({
            "instance_id": row["instance_id"],
            "image_name": row["image_name"],
            "manifest_digest": descriptor["digest"],
            "manifest_size_bytes": descriptor["size"],
            "platform": descriptor["platform"],
            "compressed_layer_bytes": sum(layer["size"] for layer in raw.get("layers", [])),
            "layer_count": len(raw.get("layers", [])),
            "raw_manifest_sha256": hashlib.sha256(base64.b64decode(manifest["Raw"])).hexdigest(),
            "observed_date": "2026-07-17",
            "manifest_available": True,
        })
    value = {
        "schema_version": "asi_stack.p2_image_manifest_receipts.v1",
        "recorded_date": "2026-07-17",
        "state": "all_development_manifests_resolve_gold_execution_pending",
        "image_count": len(receipts),
        "all_available": all(row["manifest_available"] for row in receipts),
        "platforms": sorted({f"{row['platform']['os']}/{row['platform']['architecture']}" for row in receipts}),
        "total_unshared_compressed_layer_bytes": sum(row["compressed_layer_bytes"] for row in receipts),
        "resource_boundary": "unshared layer sum is a conservative upper bound; actual pulls may share layers; manifest resolution does not measure expanded disk, emulation, runtime, cleanup, or gold-test success",
        "final_pool_selected": False,
        "final_pool_opened": False,
        "support_state_effect": "none",
        "receipts": receipts,
    }
    OUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"P2 image preflight recorded {len(receipts)} resolvable manifests; gold execution remains pending.")


if __name__ == "__main__":
    main()
