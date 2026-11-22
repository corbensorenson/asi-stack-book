#!/usr/bin/env python3
"""Run the retained Git comparison with its two archived baseline blobs."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import compare_repository_change_workflows as comparison
import run_p5_u1_governed_repository_change as runner


def baseline_bytes(commit, path):
    entry = LOCK["files"][path]
    data = (ROOT / entry["path"]).read_bytes()
    if commit != LOCK["origin_commit"] or sha256(data).hexdigest() != entry["sha256"]:
        raise ValueError(f"Baseline blob failed provenance check: {path}")
    return data


if __name__ == "__main__":
    LOCK = json.loads((Path(__file__).parent / "standalone_inputs/input_lock.json").read_bytes())
    with tempfile.TemporaryDirectory(prefix="asi-workflow-compare-") as directory:
        with patch.object(runner, "old_bytes", baseline_bytes):
            print(json.dumps(comparison.compare(Path(directory)), indent=2))
