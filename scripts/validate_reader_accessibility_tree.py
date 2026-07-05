#!/usr/bin/env python3
"""Run the curated reader HTML accessibility-tree release-preparation probe."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NODE_SCRIPT = ROOT / "scripts" / "validate_curated_reader_accessibility_tree.js"


def main() -> None:
    result = subprocess.run(
        ["node", str(NODE_SCRIPT), *sys.argv[1:]],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
