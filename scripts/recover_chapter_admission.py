#!/usr/bin/env python3
"""Inspect pending canonical admission or explicitly roll its file changes back."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from admission_guard import ACTIVE, canonical_access
from canonical_admission_transaction import control, rollback

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollback", action="store_true", help="Restore retained objects; later edits refuse before any restoration")
    args = parser.parse_args()
    if args.rollback:
        result = rollback(ROOT)
    else:
        with canonical_access(ROOT, recovery=True):
            result = control(ROOT / ACTIVE)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f"Canonical admission recovery refused; retained custody preserved: {error}")
