#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "appendices/B_glossary.qmd"
MANIFEST = ROOT / "book_structure.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    chapters = {chapter["id"]: chapter for part in manifest["parts"] for chapter in part["chapters"]}
    lines = GLOSSARY.read_text(encoding="utf-8").splitlines()
    rows = [line for line in lines if line.startswith("| ") and not line.startswith("| Term ") and not line.startswith("|---")]
    errors: list[str] = []
    terms: list[str] = []
    owners: dict[str, int] = {}
    for line in rows:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4:
            errors.append(f"glossary row must have term, definition, owner, status: {line[:80]}")
            continue
        term, definition, owner_cell, status = cells
        owner = owner_cell.strip("`")
        terms.append(term.casefold())
        owners[owner] = owners.get(owner, 0) + 1
        if owner not in chapters:
            errors.append(f"{term}: owner {owner!r} is not an active chapter")
        if len(definition.split()) < 8:
            errors.append(f"{term}: definition is too thin")
        if "initial" in status.lower() or "refine after" in status.lower():
            errors.append(f"{term}: provisional status was not resolved")
        if "lineage label" in status.lower() and "lineage" not in definition.lower():
            errors.append(f"{term}: lineage-only status must be explicit in the definition")
    if len(terms) != len(set(terms)):
        errors.append("glossary terms must be unique")
    if len(rows) < 20:
        errors.append("terminology audit unexpectedly lost glossary coverage")
    if errors:
        raise SystemExit("Terminology ownership validation failed:\n - " + "\n - ".join(errors))
    print(f"Terminology ownership passed: {len(rows)} unique terms, {len(owners)} active chapter owners, no provisional definitions.")


if __name__ == "__main__":
    main()
