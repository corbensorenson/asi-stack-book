#!/usr/bin/env python3
"""Build public-safe custody receipts for the ignored Corben paper cache."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSURE = ROOT / "sources" / "corben_paper_corpus_closure.json"
OUTPUT = ROOT / "sources" / "corben_raw_source_receipts.json"


def canonical_sha(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    records: list[dict[str, object]] = []
    for row in closure["records"]:
        relative = row["raw_source"]
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"Cannot receipt missing private source: {relative}")
        content = path.read_bytes()
        records.append(
            {
                "source_id": row["source_id"],
                "raw_source": relative,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
                "custody_state": "locally_verified_private_cache",
            }
        )

    payload = {
        "schema_version": "asi_stack.corben_raw_source_receipts.v1",
        "as_of": closure["as_of"],
        "expected_record_count": len(records),
        "storage_policy": (
            "Raw paper bodies remain local and git-ignored. This tracked metadata binds "
            "the exact bytes used for section-family mining without publishing those bytes."
        ),
        "evidence_boundary": (
            "A digest proves byte identity only. It does not establish authorship, publication "
            "rights, truth, novelty, implementation quality, or empirical support."
        ),
        "records_sha256": canonical_sha(records),
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(records)} private-source receipts.")


if __name__ == "__main__":
    main()
