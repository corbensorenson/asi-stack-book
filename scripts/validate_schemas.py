#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
TITLE_EXEMPTIONS = {
    "schemas/p4_m8_kerc_result.schema.json": "2f3f531ccfb836127ff06bc54f22d652d4c7b4e77c493bde14036a33fd0155a5",
}


def main() -> None:
    schema_files = sorted(SCHEMA_DIR.glob("*.schema.json"))
    if not schema_files:
        print("No schemas found.", file=sys.stderr)
        sys.exit(1)

    errors = []
    for path in schema_files:
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        for key in ["$schema", "title", "type", "properties"]:
            if key not in schema:
                relative = str(path.relative_to(ROOT))
                if key == "title" and TITLE_EXEMPTIONS.get(relative) == hashlib.sha256(path.read_bytes()).hexdigest():
                    continue
                errors.append(f"{path.relative_to(ROOT)}: missing {key}")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print(f"Schema validation passed for {len(schema_files)} schemas.")


if __name__ == "__main__":
    main()
