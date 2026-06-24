#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "sources" / "source_inventory.json"
RAW_DIR = ROOT / "sources" / "raw" / "google_docs"
MANIFEST = ROOT / "sources" / "cache" / "cache_manifest.json"


def load_inventory() -> list[dict]:
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def file_id_from_url(url: str) -> str | None:
    patterns = [
        r"/document/d/([^/]+)",
        r"/spreadsheets/d/([^/]+)",
        r"/presentation/d/([^/]+)",
        r"/file/d/([^/]+)",
        r"[?&]id=([^&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def source_kind(url: str) -> str:
    if "docs.google.com/document/" in url:
        return "google_doc"
    if "docs.google.com/spreadsheets/" in url:
        return "google_sheet"
    if "docs.google.com/presentation/" in url:
        return "google_slide"
    if "drive.google.com/file/" in url:
        return "drive_file"
    return "unknown"


def export_url(record: dict) -> tuple[str | None, str]:
    url = record["url"]
    file_id = file_id_from_url(url)
    if not file_id:
        return None, "missing_file_id"
    kind = source_kind(url)
    if kind == "google_doc":
        return f"https://docs.google.com/document/d/{quote(file_id)}/export?format=txt", "txt"
    if kind == "google_sheet":
        return f"https://docs.google.com/spreadsheets/d/{quote(file_id)}/export?format=csv", "csv"
    if kind == "google_slide":
        return f"https://docs.google.com/presentation/d/{quote(file_id)}/export/txt", "txt"
    if kind == "drive_file":
        return f"https://drive.google.com/uc?export=download&id={quote(file_id)}", "bin"
    return None, "unsupported_url"


def output_path(record: dict, extension: str) -> Path:
    safe_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", record["id"]).strip("-")
    return RAW_DIR / f"{safe_id}.{extension}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_curl(url: str, path: Path, timeout: int) -> tuple[bool, str]:
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--silent",
        "--show-error",
        "--max-time",
        str(timeout),
        "-o",
        str(path),
        url,
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return False, proc.stderr.strip() or proc.stdout.strip()
    return True, ""


def cache_record(record: dict, timeout: int, force: bool) -> dict:
    url, extension = export_url(record)
    now = datetime.now(timezone.utc).isoformat()
    result = {
        "id": record["id"],
        "title": record.get("title"),
        "url": record.get("url"),
        "attempted_at": now,
        "cache_mode": "public_url_export",
        "status": "not_attempted",
        "raw_path": None,
        "bytes": 0,
        "sha256": None,
        "error": None,
    }
    if not url:
        result["status"] = "unsupported"
        result["error"] = extension
        return result

    path = output_path(record, extension)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        result.update({
            "status": "cached_existing",
            "raw_path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
        return result

    tmp = path.with_suffix(path.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    ok, error = run_curl(url, tmp, timeout)
    if not ok:
        result["status"] = "connector_required" if "401" in error else "failed"
        result["error"] = error
        if tmp.exists():
            tmp.unlink()
        return result
    if tmp.stat().st_size == 0:
        result["status"] = "failed"
        result["error"] = "empty_export"
        tmp.unlink()
        return result
    tmp.replace(path)
    result.update({
        "status": "cached",
        "raw_path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Cache public Google Drive/Docs source exports locally.")
    parser.add_argument("--only", action="append", default=[], help="Source ID to cache. Repeatable.")
    parser.add_argument("--limit", type=int, help="Maximum records to attempt.")
    parser.add_argument("--force", action="store_true", help="Refresh existing cache files.")
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--sleep", type=float, default=0.25)
    args = parser.parse_args()

    records = load_inventory()
    if args.only:
        wanted = set(args.only)
        records = [record for record in records if record["id"] in wanted]
    if args.limit is not None:
        records = records[: args.limit]

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory_path": str(INVENTORY.relative_to(ROOT)),
        "raw_dir": str(RAW_DIR.relative_to(ROOT)),
        "note": "Raw files are intentionally ignored by git.",
        "records": [],
    }
    for record in records:
        status = cache_record(record, timeout=args.timeout, force=args.force)
        manifest["records"].append(status)
        print(f"{status['id']}: {status['status']} {status.get('bytes') or ''}")
        time.sleep(args.sleep)

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    failures = [item for item in manifest["records"] if item["status"] in {"failed", "unsupported"}]
    connector_required = [item for item in manifest["records"] if item["status"] == "connector_required"]
    if failures:
        print(f"Completed with {len(failures)} failed/unsupported records.", file=sys.stderr)
    if connector_required:
        print(f"{len(connector_required)} records require authenticated connector export.", file=sys.stderr)
    if not failures and not connector_required:
        print("All attempted records cached.")


if __name__ == "__main__":
    main()
