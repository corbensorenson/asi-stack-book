#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "book_structure.json"
REPORT = ROOT / "docs/chapter_packet_contract_audit.md"
HEADINGS = [
    "Problem", "Why existing approaches are insufficient", "Core Claim",
    "Mechanism", "Interfaces", "Invariants", "Failure modes",
    "Minimum Viable Implementation", "Beyond the State of the Art",
    "Codex test plan", "Source crosswalk", "Summary", "Handoff",
]


def chapters(value: dict) -> list[dict]:
    return [chapter for part in value["parts"] for chapter in part["chapters"]]


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M | re.I)
    if not match:
        return ""
    tail = text[match.end():]
    stop = re.search(r"^## ", tail, re.M)
    return tail[:stop.start()] if stop else tail


def audit(chapter: dict) -> tuple[list[str], str]:
    path = ROOT / chapter["file"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for heading in HEADINGS:
        if not re.search(rf"^## {re.escape(heading)}\s*$", text, re.M | re.I):
            errors.append(f"missing heading {heading}")
    for field, minimum in (("mechanism", 3), ("interfaces", 3), ("invariants", 3), ("failure_modes", 3)):
        if not isinstance(chapter.get(field), list) or len(chapter[field]) < minimum:
            errors.append(f"manifest {field} needs at least {minimum} entries")
    for field in ("problem", "insufficient", "core_claim", "minimal_implementation", "beyond_state_of_art"):
        if not isinstance(chapter.get(field), str) or len(chapter[field].split()) < 5:
            errors.append(f"manifest {field} is missing or too thin")
    if not chapter.get("source_ids") or not chapter.get("claim_source_mappings"):
        errors.append("source route or exact claim mapping missing")
    if not chapter.get("codex_tests"):
        errors.append("test route missing")
    if not chapter.get("proof_targets") or not chapter.get("lean_module"):
        errors.append("proof route missing")
    if "```{mermaid}" not in text:
        errors.append("useful interface/lifecycle diagram missing")
    if len(section(text, "Handoff").split()) < 35:
        errors.append("handoff is too thin")
    why = section(text, "Why existing approaches are insufficient").lower()
    explicit = bool(re.search(r"^#{2,3} Strongest objection\s*$", text, re.M | re.I))
    bounded_challenge = any(token in why for token in (" objection", " but ", " however", " cannot ", " does not ", " risk"))
    if not explicit and not bounded_challenge:
        errors.append("strongest objection or bounded counterargument missing")
    objection_route = "explicit heading" if explicit else "bounded in insufficiency section"
    all_text = text.lower()
    if sum(token in all_text for token in ("authority", "lifecycle", "state", "scope", "boundary")) < 3:
        errors.append("authority/state/lifecycle boundary vocabulary too thin")
    if not chapter.get("open_evidence_gaps") and "open_evidence_gaps:" not in text:
        errors.append("weakening/evidence-change condition missing")
    return errors, objection_route


def render(rows: list[tuple[dict, list[str], str]]) -> str:
    lines = [
        "# Chapter Packet Contract Audit", "", "Last updated: 2026-07-10", "",
        "This generated audit checks every active chapter against the architecture-reference packet contract. An objection may be an explicit heading or a bounded counterargument in the insufficiency section; this classification does not claim independent review or argument quality.", "",
        "| Chapter ID | Result | Objection route | Notes |", "|---|---|---|---|",
    ]
    for chapter, errors, route in rows:
        notes = "; ".join(errors) if errors else "complete packet surface"
        lines.append(f"| `{chapter['id']}` | {'fail' if errors else 'pass'} | {route} | {notes} |")
    passed = sum(not errors for _, errors, _ in rows)
    lines += ["", f"Summary: {passed} of {len(rows)} active chapters pass; {len(rows) - passed} remain open.", "",
              "Non-claims: this is a structural and bounded semantic audit, not proof of prose quality, source interpretation, empirical validity, formal adequacy, deployment, safety, or independent review.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = []
    failures = []
    for chapter in chapters(value):
        errors, route = audit(chapter)
        rows.append((chapter, errors, route))
        if errors:
            failures.append(f"{chapter['id']}: {', '.join(errors)}")
    body = render(rows)
    if args.write:
        REPORT.write_text(body, encoding="utf-8")
    elif not REPORT.exists() or REPORT.read_text(encoding="utf-8") != body:
        failures.append("docs/chapter_packet_contract_audit.md is stale; run with --write")
    if failures:
        raise SystemExit("Chapter packet contract audit failed:\n - " + "\n - ".join(failures))
    print(f"Chapter packet contract audit passed: {len(rows)} active chapters, complete packet surfaces, report current.")


if __name__ == "__main__":
    main()
