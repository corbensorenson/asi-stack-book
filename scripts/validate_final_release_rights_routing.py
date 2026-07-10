#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "licensing/provenance_inventory.json"
ROUTING = ROOT / "licensing/final_release_rights_routing.json"


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().rstrip(b"\n")).hexdigest()


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    errors: list[str] = []
    inventory_paths = [item["path"] for item in inventory["files"]]
    rows = routing.get("files", [])
    routed_paths = [item.get("path") for item in rows]
    if routed_paths != inventory_paths or len(routed_paths) != len(set(routed_paths)):
        errors.append("rights routing must cover the current provenance inventory exactly once and in order")
    allowed = {"CC-BY-4.0", "Apache-2.0", "excluded-no-grant"}
    if any(item.get("license_route") not in allowed for item in rows):
        errors.append("rights routing contains an unresolved or unknown route")
    if routing.get("summary", {}).get("unresolved_count") != 0:
        errors.append("rights routing unresolved_count must be zero")
    counts = {key: sum(item.get("license_route") == key for item in rows) for key in allowed}
    if routing.get("summary", {}).get("by_license_route") != dict(sorted(counts.items())):
        errors.append("rights routing summary counts drifted")
    by_path = {item["path"]: item for item in rows}
    for path in ("LICENSE.md", "licenses/CC-BY-4.0.txt", "licenses/Apache-2.0.txt"):
        if by_path.get(path, {}).get("license_route") != "excluded-no-grant":
            errors.append(f"{path} must not be self-relicensed")
    for item in rows:
        path = item["path"]
        lane = item["license_route"]
        if path.startswith("sources/") and lane != "excluded-no-grant":
            errors.append(f"mixed/source path was improperly granted: {path}")
        if path.startswith(("experiments/", "editions/", "external_reviews/")) and lane != "excluded-no-grant":
            errors.append(f"import/derivative path was improperly granted: {path}")
        if lane == "Apache-2.0" and item.get("provenance_status") != "author_ownership_assertion_required":
            errors.append(f"Apache lane lacks author-ownership classification: {path}")
        if lane == "CC-BY-4.0" and item.get("provenance_status") not in {"author_ownership_assertion_required", "author_assertion_and_embedded_asset_review_required"}:
            errors.append(f"CC lane lacks author/asset classification: {path}")
    texts = routing.get("license_texts", {})
    for license_id, expected in {
        "CC-BY-4.0": "fe7b4ce83b8381cc5b216bbb4af73c570688d1b819c73bbaed8ca401f4677cd6",
        "Apache-2.0": "58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd",
    }.items():
        path = ROOT / texts.get(license_id, {}).get("path", "missing")
        if not path.is_file() or normalized_sha(path) != expected or texts[license_id].get("normalized_sha256") != expected:
            errors.append(f"{license_id} official legal text digest mismatch")
    license_md = (ROOT / "LICENSE.md").read_text(encoding="utf-8")
    notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
    scope = (ROOT / "docs/v2_0_release_scope.md").read_text(encoding="utf-8")
    for phrase in ("v2.0.0", "CC-BY-4.0", "Apache-2.0", "excluded-no-grant", "all rights are reserved"):
        if phrase not in license_md:
            errors.append(f"LICENSE.md missing routed boundary: {phrase}")
    if "v2.0.0" not in notice or "canonical live/research HTML book only" not in scope:
        errors.append("release notice or selected-format scope is incomplete")
    if errors:
        raise SystemExit("Final-release rights routing validation failed:\n - " + "\n - ".join(errors))
    print(f"Final-release rights routing passed: {len(rows)} paths, {counts}, HTML-only release scope.")


if __name__ == "__main__":
    main()
