#!/usr/bin/env python3
"""Generate the embedded live-site reader overlay asset.

The reader edition generator applies overlays to derived Quarto source. The
live Human view needs the same semantic overlay source without fetching files at
runtime, especially under local file:// validation. This script embeds the
active overlay operations as JSON in a small after-body include.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "assets" / "reader-overlays.html"


def active_overlay_payload(profile_id: str) -> dict[str, object]:
    profile = build_reader_edition.find_profile(profile_id)
    context = build_reader_edition.load_reader_overlay_context(profile)
    summary = build_reader_edition.reader_overlay_summary(context)
    operations = [
        {
            "id": operation["id"],
            "target_file": operation["target_file"],
            "action": operation["action"],
            "section": operation["section"],
            "content": operation["content"],
            "rationale": operation.get("rationale", ""),
        }
        for operation in context.get("operations", [])
        if isinstance(operation, dict) and operation.get("status") == "active"
    ]
    return {
        "schema_version": "0.1",
        "profile": profile_id,
        "manifest_path": summary.get("manifest_path"),
        "manifest_id": summary.get("manifest_id"),
        "operation_count": len(operations),
        "operations": operations,
        "non_claims": [
            "This embedded payload supports the live Human view only.",
            "It does not claim a reviewed reader edition, ebook, audio artifact, or support-state promotion.",
        ],
    }


def render_asset(payload: dict[str, object]) -> str:
    raw_json = json.dumps(payload, indent=2, ensure_ascii=False)
    safe_json = raw_json.replace("</script", "<\\/script")
    return (
        '<script type="application/json" id="asi-reader-overlays">\n'
        f"{safe_json}\n"
        "</script>\n"
    )


def sync_asset(output: Path, profile_id: str, check: bool) -> dict[str, object]:
    payload = active_overlay_payload(profile_id)
    expected = render_asset(payload)
    if check:
        if not output.exists():
            raise FileNotFoundError(f"Missing reader overlay asset: {output.relative_to(ROOT)}")
        actual = output.read_text(encoding="utf-8")
        if actual != expected:
            raise ValueError(
                f"{output.relative_to(ROOT)} is out of date; "
                "run scripts/sync_reader_overlay_asset.py"
            )
        return payload
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="release profile to embed")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="asset path to write")
    parser.add_argument("--check", action="store_true", help="check without writing")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        payload = sync_asset(Path(args.output), args.profile, args.check)
    except Exception as exc:
        print(f"Reader overlay asset sync failed: {exc}")
        sys.exit(1)
    action = "validated" if args.check else "wrote"
    print(
        "Reader overlay asset "
        f"{action}: {Path(args.output).relative_to(ROOT)} "
        f"({payload['operation_count']} active operations)."
    )


if __name__ == "__main__":
    main()
