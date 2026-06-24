#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources" / "cache" / "cache_manifest.json"
REPORT = ROOT / "docs" / "source_readiness_report.md"


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing sources/cache/cache_manifest.json. Run scripts/cache_drive_sources.py first.")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = data.get("records", [])
    counts = Counter(record.get("status", "unknown") for record in records)
    rows = []
    for record in records:
        rows.append(
            "| `{id}` | {title} | `{status}` | {bytes} | {path} | {error} |".format(
                id=record.get("id", ""),
                title=str(record.get("title") or "").replace("|", "\\|"),
                status=record.get("status", ""),
                bytes=record.get("bytes") or "",
                path=record.get("raw_path") or "",
                error=str(record.get("error") or "").replace("|", "\\|"),
            )
        )
    summary = "\n".join(f"- `{status}`: {count}" for status, count in sorted(counts.items()))
    text = f"""# Source Readiness Report

Generated from `sources/cache/cache_manifest.json`.

Raw source exports are local-only and ignored by git. This report tracks readiness without publishing the raw source text.

## Summary

{summary}

## Records

| Source ID | Title | Cache status | Bytes | Local raw path | Error / note |
|---|---|---:|---:|---|---|
{chr(10).join(rows)}
"""
    REPORT.write_text(text, encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
