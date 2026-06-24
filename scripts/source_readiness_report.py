#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources" / "cache" / "cache_manifest.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
REPORT = ROOT / "docs" / "source_readiness_report.md"

AUTH_GATE_MARKERS = [
    "Google Drive: Sign-in",
    "Sign in to continue to Google Drive",
    "Email or phone",
    "accounts.google.com/v3/signin",
    "https://accounts.google.com",
]


def cache_note(record: dict) -> tuple[str, str]:
    """Return a display status and note without exposing raw source text."""
    status = str(record.get("status", ""))
    note = str(record.get("error") or "")
    raw_path = record.get("raw_path")
    if not raw_path:
        return status, note

    path = ROOT / raw_path
    if not path.exists():
        return status, note or "raw path missing"

    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError as exc:
        return status, note or f"could not inspect cache: {exc}"

    if any(marker in head for marker in AUTH_GATE_MARKERS):
        return "cached_auth_gate", "local cache is a Google sign-in/auth-gate page, not usable source text"
    return status, note


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing sources/cache/cache_manifest.json. Run scripts/cache_drive_sources.py first.")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cache_records = {record.get("id", ""): record for record in data.get("records", [])}
    inventory_records = json.loads(INVENTORY.read_text(encoding="utf-8"))
    rows = []
    counts = Counter()
    for source in inventory_records:
        source_id = source.get("id", "")
        record = cache_records.get(source_id)
        if record is None:
            url = str(source.get("url", ""))
            if "github.com/" in url:
                display_status = "not_cached_public_project"
                note = "public project source record; not part of Google Drive cache manifest"
            else:
                display_status = "not_cached"
                note = "source inventory record is not present in the cache manifest"
            counts[display_status] += 1
            rows.append(
                "| `{id}` | {title} | `{status}` | {bytes} | {path} | {error} |".format(
                    id=source_id,
                    title=str(source.get("title") or "").replace("|", "\\|"),
                    status=display_status,
                    bytes="",
                    path="",
                    error=note.replace("|", "\\|"),
                )
            )
            continue

        display_status, note = cache_note(record)
        counts[display_status] += 1
        rows.append(
            "| `{id}` | {title} | `{status}` | {bytes} | {path} | {error} |".format(
                id=record.get("id", ""),
                title=str(record.get("title") or "").replace("|", "\\|"),
                status=display_status,
                bytes=record.get("bytes") or "",
                path=record.get("raw_path") or "",
                error=note.replace("|", "\\|"),
            )
        )
    summary = "\n".join(f"- `{status}`: {count}" for status, count in sorted(counts.items()))
    text = f"""# Source Readiness Report

Generated from `sources/source_inventory.json` and `sources/cache/cache_manifest.json`.

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
