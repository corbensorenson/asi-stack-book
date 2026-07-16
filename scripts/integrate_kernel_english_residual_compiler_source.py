#!/usr/bin/env python3
"""Assign the KERC source to its existing ASI Stack chapter owners."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "book_structure.json"
SOURCE_ID = "kernel_english_residual_compiler"
OWNERS = {
    "cognitive-compilation-and-semantic-ir",
    "compact-generative-systems-and-residual-honesty",
    "virtual-context-abi",
    "context-transactions-snapshots-mounts-and-taint",
    "verification-bandwidth-and-context-adequacy",
    "fast-generation-architectures",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "resource-economics-and-token-budgets",
    "security-kernel-and-digital-scifs",
    "procedural-memory-and-cognitive-loop-closure",
    "benchmark-ratchets-and-anti-goodhart-evidence",
    "integrated-reference-architecture",
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seen: set[str] = set()
    for part in manifest["parts"]:
        for chapter in part["chapters"]:
            if chapter["id"] in OWNERS:
                seen.add(chapter["id"])
                sources = chapter.setdefault("source_ids", [])
                if SOURCE_ID not in sources:
                    sources.append(SOURCE_ID)
                queue = chapter.setdefault("source_queue", {})
                supporting = queue.setdefault("supporting", [])
                if SOURCE_ID not in supporting:
                    supporting.append(SOURCE_ID)
    missing = sorted(OWNERS - seen)
    if missing:
        raise SystemExit("missing chapter owners: " + ", ".join(missing))
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Assigned {SOURCE_ID} to {len(seen)} existing chapters; no chapter added.")


if __name__ == "__main__":
    main()
