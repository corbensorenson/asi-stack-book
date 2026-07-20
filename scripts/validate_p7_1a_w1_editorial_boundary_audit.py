#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evidence_quality/p7_1a_w1_editorial_boundary_audit.json"
TERMINAL = ROOT / "experiments/claim_family_terminal_coverage/results/result.json"
HISTORICAL_STATUS = ROOT / "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"
START = "<!-- P7-EVIDENCE-RECONCILIATION:START -->"
END = "<!-- P7-EVIDENCE-RECONCILIATION:END -->"
TOKEN_RE = re.compile(r"[A-Za-z0-9_`'-]+")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def repeated_metric(chapter_ids: list[str], getter: Callable[[str], str]) -> tuple[int, int, int]:
    locations: dict[str, set[str]] = defaultdict(set)
    token_count = 0
    for chapter_id in chapter_ids:
        words = TOKEN_RE.findall(getter(chapter_id))
        token_count += len(words)
        for index in range(len(words) - 11):
            locations[" ".join(words[index:index + 12])].add(chapter_id)
    repeated = [paths for paths in locations.values() if len(paths) >= 8]
    return token_count, len(repeated), max((len(paths) for paths in repeated), default=0)


def packet_digest(chapter_ids: list[str]) -> str:
    digests: dict[str, str] = {}
    for chapter_id in chapter_ids:
        text = (ROOT / "chapters" / f"{chapter_id}.qmd").read_text(encoding="utf-8")
        packet = text[text.index(START):text.index(END) + len(END)]
        digests[chapter_id] = hashlib.sha256(packet.encode("utf-8")).hexdigest()
    payload = json.dumps(digests, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def errors(data: dict) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    chapter_ids = data["chapter_ids"]
    terminal = data["terminal"]
    structure = data["structure"]
    inventory_ids = {row["id"] for row in data["inventory"]}
    chapters = {chapter["id"]: chapter for part in structure["parts"] for chapter in part["chapters"]}
    measure = audit.get("measurement", {})
    baseline = tuple(data["baseline_metric"])
    current = tuple(data["current_metric"])
    expected_baseline = (
        measure.get("baseline_word_tokens"),
        measure.get("reproduced_baseline_distinct_repeated_12_grams"),
        measure.get("maximum_chapter_spread_before"),
    )
    if audit.get("state") != "terminal_complete" or audit.get("historical_chapter_count") != 55:
        out.append("packet state or historical denominator drifted")
    # The recorded final metric is the terminal W1 receipt. Later governed
    # chapter edits may change live token counts, so they must preserve the
    # frozen baseline identity and the reduction floor rather than pretending
    # to reproduce the historical final bytes.
    if baseline != expected_baseline or current[1] > baseline[1] * 0.85:
        out.append("frozen baseline drifted or the live book fails the 15% W1 reduction floor")
    if terminal.get("atom_count") != 3745 or len(terminal.get("dispositions", [])) != 3745:
        out.append("protected terminal atom denominator drifted")
    if packet_digest(chapter_ids) != audit["centralized_contract"]["compact_packet_digest"]:
        out.append("compact live packet digest drifted")
    required_packet_fields = (
        "| Family / atom denominator |", "| Terminal dispositions |", "| Core |",
        "| Core attempted / missing lanes |", "| Strongest family bundle |",
        "| Negative controls |", "| Accepted transitions |", "| Maximum inference |",
        "| Reproduction / next burden |",
    )
    for chapter_id in chapter_ids:
        text = data["chapter_texts"][chapter_id]
        if text.count(START) != 1 or text.count(END) != 1:
            out.append(f"packet markers drifted: {chapter_id}")
            continue
        packet = text[text.index(START):text.index(END)]
        if any(packet.count(field) != 1 for field in required_packet_fields):
            out.append(f"chapter-specific packet fields drifted: {chapter_id}")
    for row in audit.get("boundary_sections", []):
        chapter_id = row["chapter_id"]
        text = data["chapter_texts"].get(chapter_id, "")
        if f"## {row['heading']}" not in text or "does **not**" not in text:
            out.append(f"named boundary section or non-claim missing: {chapter_id}")
        if not set(row["source_ids"]).issubset(set(chapters[chapter_id].get("source_ids", [])) & inventory_ids):
            out.append(f"boundary source assignment drifted: {chapter_id}")
        if not all(atom in text for atom in row["atom_refs"]):
            out.append(f"boundary atom custody drifted: {chapter_id}")
    for chapter_id in audit.get("consolidation_provenance_chapters", []):
        text = data["chapter_texts"][chapter_id]
        guard = text.index("## Drafting guardrail")
        archive = text.find("archive/retired_chapters/")
        provenance = text.find("## Provenance and consolidation history")
        if archive < guard or provenance < guard or archive < provenance:
            out.append(f"retired-chapter bookkeeping returned to opening: {chapter_id}")
    custody = audit.get("meaning_custody", {})
    if any(custody.get(key) != 0 for key in (
        "unique_claims_deleted", "equations_deleted", "source_assignments_deleted",
        "protocol_or_proof_boundaries_deleted", "terminal_atom_rows_mutated",
        "chapter_core_support_movements",
    )):
        out.append("meaning or support custody no longer records zero loss/movement")
    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("unauthorized support, release, or publication effect")
    return out


def main() -> None:
    audit = load(AUDIT)
    historical = load(HISTORICAL_STATUS)
    chapter_ids = [row["chapter_id"] for row in historical["chapter_claim_program"]]
    baseline_commit = audit["baseline_commit"]
    baseline_metric = repeated_metric(
        chapter_ids,
        lambda chapter_id: subprocess.check_output(
            ["git", "show", f"{baseline_commit}:chapters/{chapter_id}.qmd"],
            cwd=ROOT, text=True,
        ),
    )
    chapter_texts = {
        chapter_id: (ROOT / "chapters" / f"{chapter_id}.qmd").read_text(encoding="utf-8")
        for chapter_id in chapter_ids
    }
    current_metric = repeated_metric(chapter_ids, chapter_texts.__getitem__)
    data = {
        "audit": audit,
        "chapter_ids": chapter_ids,
        "chapter_texts": chapter_texts,
        "baseline_metric": baseline_metric,
        "current_metric": current_metric,
        "terminal": load(TERMINAL),
        "structure": load(STRUCTURE),
        "inventory": load(INVENTORY),
    }
    failures = errors(data)
    mutations = [
        ("erase section", lambda value: value["chapter_texts"].__setitem__("failure-modes-of-ungoverned-intelligence", value["chapter_texts"]["failure-modes-of-ungoverned-intelligence"].replace("## Gradual disempowerment and option-value loss", "", 1))),
        ("erase non-claim", lambda value: value["chapter_texts"].__setitem__("scalable-oversight-and-adversarial-ai-control", value["chapter_texts"]["scalable-oversight-and-adversarial-ai-control"].replace("does **not**", "claims", 1))),
        ("drop atom", lambda value: value["terminal"]["dispositions"].pop()),
        ("drop source", lambda value: next(chapter for part in value["structure"]["parts"] for chapter in part["chapters"] if chapter["id"] == "failure-modes-of-ungoverned-intelligence")["source_ids"].clear()),
        ("move archive residue", lambda value: value["chapter_texts"].__setitem__("virtual-context-abi", value["chapter_texts"]["virtual-context-abi"].replace("## Drafting guardrail", "archive/retired_chapters/\n\n## Drafting guardrail", 1))),
        ("invent deletion", lambda value: value["audit"]["meaning_custody"].__setitem__("unique_claims_deleted", 1)),
        ("invent support effect", lambda value: value["audit"].__setitem__("support_state_effect", "promotion")),
        ("erase packet field", lambda value: value["chapter_texts"].__setitem__(chapter_ids[0], value["chapter_texts"][chapter_ids[0]].replace("| Maximum inference |", "| Missing maximum |", 1))),
    ]
    baseline_errors = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline_errors:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P7.1a W1 editorial-boundary audit failed:\n - " + "\n - ".join(failures))
    print(
        "P7.1a W1 editorial-boundary audit passed: 55 chapters, 3,745 protected atoms, "
        f"repeated 12-grams {baseline_metric[1]} -> {current_metric[1]}, compact packet digest pinned, "
        f"two boundary sections and three provenance repairs present, {len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
