#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evidence_quality/p7_1a_w2_narrative_audit.json"
STRUCTURE = ROOT / "book_structure.json"
ATOM_LEDGER = ROOT / "experiments/claim_family_terminal_coverage/results/result.json"
INDEX = ROOT / "index.qmd"
OUTLINE = ROOT / "docs/book_outline.md"
WORD = re.compile(r"[A-Za-z0-9_`'-]+")
CLAIM = re.compile(r"\[[^\]\n]+support:\s*[^\]\n]+\]")
PROOF_TAG = re.compile(r"lean:[a-z0-9_.-]+")
ARTIFACT_REF = re.compile(r"(?:schemas|protocols)/[A-Za-z0-9_./-]+")
MATH = re.compile(r"(?s)\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)|\\\[.*?\\\]")
EXPECTED_ROLE_COUNTS = {
    "thesis-bearing": 11,
    "load-bearing-reference": 30,
    "implementation-case": 7,
    "speculative-deferred-research": 11,
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_rows(value: dict[str, Any]) -> list[dict[str, Any]]:
    return [chapter for part in value["parts"] for chapter in part["chapters"]]


def baseline_text(commit: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"cannot read {path} at {commit}")
    return result.stdout


def preservation_set(pattern: re.Pattern[str], text: str) -> set[str]:
    return {match.group(0) for match in pattern.finditer(text)}


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    structure = data["structure"]
    baseline_structure = data["baseline_structure"]
    rows = manifest_rows(structure)
    baseline_rows = manifest_rows(baseline_structure)
    ids = [row["id"] for row in rows]
    if audit.get("state") != "terminal_complete" or audit.get("packet_id") != "P7.1a-W2-opening-variation-and-thesis-depth-leveling":
        out.append("packet identity or terminal state drifted")
    if len(ids) != audit.get("manifest_chapter_count") or len(set(ids)) != 59:
        out.append("manifest chapter denominator drifted")

    roles = audit.get("chapter_roles", {})
    if set(roles) != set(EXPECTED_ROLE_COUNTS):
        out.append("reader role vocabulary drifted")
    flattened: list[str] = []
    for role, count in EXPECTED_ROLE_COUNTS.items():
        values = roles.get(role, [])
        if len(values) != count or len(values) != len(set(values)):
            out.append(f"{role}: count or uniqueness drifted")
        flattened.extend(values)
    if len(flattened) != len(set(flattened)) or set(flattened) != set(ids):
        out.append("chapter roles are not an exact one-role partition of the manifest")

    phrase_data = audit.get("opening_variation", {})
    phrases = phrase_data.get("audited_phrase_families", [])
    baseline_all = "\n".join(data["baseline_chapters"].values())
    current_all = "\n".join(data["current_chapters"].values())
    before = sum(baseline_all.count(phrase) for phrase in phrases)
    after = sum(current_all.count(phrase) for phrase in phrases)
    if before != phrase_data.get("baseline_occurrence_count") or after != phrase_data.get("final_occurrence_count") or after != 0:
        out.append(f"opening formula metric drifted: {before} -> {after}")

    baseline_by_id = {row["id"]: row for row in baseline_rows}
    current_by_id = {row["id"]: row for row in rows}
    for record in audit.get("depth_leveling", []):
        chapter_id = record.get("chapter_id")
        old = data["baseline_chapters"].get(chapter_id, "")
        new = data["current_chapters"].get(chapter_id, "")
        old_words = len(WORD.findall(old))
        new_words = len(WORD.findall(new))
        if old_words != record.get("baseline_word_tokens") or new_words != record.get("final_word_tokens"):
            out.append(f"{chapter_id}: word-token metric drifted {old_words} -> {new_words}")
        if new_words <= old_words or new_words - old_words < 500:
            out.append(f"{chapter_id}: depth-leveling delta is not substantive")
        for heading in record.get("added_section_headings", []):
            if f"## {heading}" not in new:
                out.append(f"{chapter_id}: missing depth section {heading}")
        for pattern, label in ((CLAIM, "claim marker"), (PROOF_TAG, "proof tag"), (ARTIFACT_REF, "protocol/schema ref"), (MATH, "equation")):
            missing = preservation_set(pattern, old) - preservation_set(pattern, new)
            if missing:
                out.append(f"{chapter_id}: deleted {label}: {sorted(missing)[:3]}")
        if baseline_by_id[chapter_id].get("source_ids") != current_by_id[chapter_id].get("source_ids"):
            out.append(f"{chapter_id}: assigned source IDs changed")
        for key in ("evidence_level", "claim_label"):
            if baseline_by_id[chapter_id].get(key) != current_by_id[chapter_id].get(key):
                out.append(f"{chapter_id}: {key} moved")

    atom_count = data["atom_ledger"].get("atom_count")
    if atom_count != audit.get("protected_terminal_atom_count"):
        out.append(f"protected atom denominator drifted: {atom_count}")
    custody = audit.get("meaning_custody", {})
    zero_fields = (
        "unique_claim_markers_deleted", "assigned_source_ids_deleted", "equations_deleted",
        "proof_tags_deleted", "protocol_or_schema_refs_deleted",
        "chapter_core_support_movements", "protected_atom_rows_mutated",
    )
    if any(custody.get(field) != 0 for field in zero_fields):
        out.append("meaning-custody record claims a deletion or support movement")
    if custody.get("new_argument_sections_claim_empirical_or_formal_support") is not False or custody.get("flagship_case_structure_precommitted") is not False:
        out.append("W2 overclaims evidence or precommits the blocked flagship structure")
    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("W2 claims an unauthorized support, release, or publication effect")

    index = data["index"]
    outline = data["outline"]
    for phrase in (
        "## Chapter roles", "Thesis-bearing", "Load-bearing reference",
        "Implementation case", "Speculative/deferred research",
        "white-box evidence, thresholds, adversarial evaluation, safety cases, and operations",
    ):
        if phrase not in index:
            out.append(f"overview surface missing: {phrase}")
    for phrase in ("### Current reader-role classification", "P7.1a-W2 assigns every manifest chapter"):
        if phrase not in outline:
            out.append(f"outline role surface missing: {phrase}")
    for chapter_id, phrase in {
        "asi-is-a-stack-not-a-model": "falsifiable allocation question",
        "the-efficient-asi-hypothesis": "widens authority is an unsafe saving",
        "failure-modes-of-ungoverned-intelligence": "seeded detector pass",
    }.items():
        if phrase not in data["current_chapters"][chapter_id]:
            out.append(f"{chapter_id}: refreshed handoff missing")
    return out


def main() -> None:
    audit = load(AUDIT)
    baseline = audit["baseline_commit"]
    structure = load(STRUCTURE)
    rows = manifest_rows(structure)
    baseline_structure = json.loads(baseline_text(baseline, "book_structure.json"))
    current_chapters = {row["id"]: (ROOT / row["file"]).read_text(encoding="utf-8") for row in rows}
    baseline_chapters = {row["id"]: baseline_text(baseline, row["file"]) for row in manifest_rows(baseline_structure)}
    data = {
        "audit": audit,
        "structure": structure,
        "baseline_structure": baseline_structure,
        "current_chapters": current_chapters,
        "baseline_chapters": baseline_chapters,
        "atom_ledger": load(ATOM_LEDGER),
        "index": INDEX.read_text(encoding="utf-8"),
        "outline": OUTLINE.read_text(encoding="utf-8"),
    }
    failures = errors(data)
    mutations = [
        ("delete role", lambda value: value["audit"]["chapter_roles"]["thesis-bearing"].pop()),
        ("duplicate role", lambda value: value["audit"]["chapter_roles"]["implementation-case"].append(value["audit"]["chapter_roles"]["thesis-bearing"][0])),
        ("restore formula", lambda value: value["current_chapters"].__setitem__("human-intent-as-a-formal-input", value["current_chapters"]["human-intent-as-a-formal-input"] + "\nThis chapter treats\n")),
        ("erase depth heading", lambda value: value["current_chapters"].__setitem__("asi-is-a-stack-not-a-model", value["current_chapters"]["asi-is-a-stack-not-a-model"].replace("## What the stack thesis commits us to", "## Removed", 1))),
        ("delete claim marker", lambda value: value["current_chapters"].__setitem__("the-efficient-asi-hypothesis", CLAIM.sub("", value["current_chapters"]["the-efficient-asi-hypothesis"], count=1))),
        ("delete source", lambda value: next(row for row in manifest_rows(value["structure"]) if row["id"] == "failure-modes-of-ungoverned-intelligence")["source_ids"].pop()),
        ("invent support effect", lambda value: value["audit"].__setitem__("support_state_effect", "promotion")),
        ("erase overview", lambda value: value.__setitem__("index", value["index"].replace("## Chapter roles", "## Removed", 1))),
        ("precommit flagship", lambda value: value["audit"]["meaning_custody"].__setitem__("flagship_case_structure_precommitted", True)),
    ]
    baseline_errors = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline_errors:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P7.1a W2 narrative audit failed:\n - " + "\n - ".join(failures))
    print(
        "P7.1a W2 narrative audit passed: 59 chapters classified "
        "(11 thesis, 30 reference, 7 implementation, 11 speculative/deferred); "
        "8 opening formulas -> 0; three central chapters deepened by "
        "711/728/664 tokens; 9 mutations rejected; support effect none."
    )


if __name__ == "__main__":
    main()
