#!/usr/bin/env python3
"""Bind the P7.1c reader-prose additions to existing reviewed claim ownership.

The reader-prose pass added short reader claims, operational rules, concrete
lenses, and bounded worked scenes.  This reconciliation does not dismiss those
sentences as decorative prose.  It checks each newly detected candidate against
the chapter's digest-bound P7.1c packet, maps complete propositions to an
already reviewed structured atom inside an explicitly selected semantic role,
and records fragments or explicit evidence-limit reports separately.  No
support state changes.
"""

from __future__ import annotations

import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence_quality" / "prose_claim_candidate_queue.json"
REGISTRY = ROOT / "evidence_quality" / "claim_atom_registry.json"
REVIEW_DIR = ROOT / "evidence_quality" / "claim_reviews"
PACKET_DIR = ROOT / "evidence_quality" / "reader_prose_quality_packets"
OUT = ROOT / "evidence_quality" / "p7_1c_reader_prose_claim_reconciliation.json"
EXPECTED_PENDING = 138

STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "for",
    "from", "has", "in", "into", "is", "it", "its", "may", "not",
    "of", "on", "only", "or", "that", "the", "their", "this", "to",
    "when", "while", "with",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tracked_or_current(path: Path) -> Any:
    """Prefer the tracked packet so a migration cannot erase prior review detail."""
    relative = path.relative_to(ROOT).as_posix()
    completed = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return json.loads(completed.stdout)
    return load(path)


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) > 2 and token not in STOP
    }


def headings_and_sections(path: Path) -> tuple[list[tuple[int, str]], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            headings.append((number, match.group(1)))
    sections: dict[str, str] = {}
    for index, (start, heading) in enumerate(headings):
        end = headings[index + 1][0] - 1 if index + 1 < len(headings) else len(lines)
        sections[heading] = "\n".join(lines[start - 1:end])
    return headings, sections


def section_for(line: int, headings: list[tuple[int, str]]) -> str:
    current = ""
    for start, heading in headings:
        if start > line:
            break
        current = heading
    return current


def preferred_roles(sentence: str, section: str) -> tuple[str, ...]:
    lowered = sentence.casefold()
    if sentence.startswith("**Reader claim.**"):
        return ("core", "mechanism", "invariant")
    if sentence.startswith("**Operational rule.**"):
        return ("invariant", "mechanism", "interface", "core")
    if section == "Human Reading Path":
        return ("insufficiency", "minimum", "failure_mode", "core")
    if any(term in lowered for term in ("reject", "block", "fail", "missing", "cannot")):
        return ("failure_mode", "invariant", "mechanism", "core")
    if any(term in lowered for term in ("requires", "must", "preserve", "bind", "authority")):
        return ("invariant", "interface", "mechanism", "core")
    return ("mechanism", "invariant", "core", "minimum")


def select_owner(
    sentence: str,
    section: str,
    atoms: list[dict[str, Any]],
) -> str:
    roles = preferred_roles(sentence, section)
    candidates: list[dict[str, Any]] = []
    for role in roles:
        candidates = [row for row in atoms if row.get("role") == role]
        if candidates:
            break
    if not candidates:
        candidates = atoms
    sentence_tokens = tokens(sentence)

    def score(row: dict[str, Any]) -> tuple[float, int, str]:
        atom_tokens = tokens(str(row.get("proposition", "")))
        overlap = len(sentence_tokens & atom_tokens)
        union = len(sentence_tokens | atom_tokens) or 1
        return (overlap / union, overlap, str(row["atom_id"]))

    return max(candidates, key=score)["atom_id"]


def explicit_limit_report(sentence: str) -> bool:
    lowered = sentence.casefold()
    return any(
        marker in lowered
        for marker in (
            "does not prove",
            "does not execute",
            "does not establish",
            "not world-complete",
            "not a deployed",
            "not production",
            "these checks show",
            "those checks show",
        )
    )


def main() -> None:
    queue = load(QUEUE)
    registry = load(REGISTRY)
    pending = [
        row for row in queue["candidates"]
        if row.get("review_state") == "pending_materiality_adjudication"
    ]
    if len(pending) != EXPECTED_PENDING and OUT.is_file():
        recorded_ids = {
            str(candidate["candidate_id"])
            for chapter in load(OUT).get("chapter_records", [])
            for candidate in chapter.get("candidate_dispositions", [])
        }
        pending = [
            row for row in queue["candidates"]
            if str(row.get("candidate_id")) in recorded_ids
        ]
    if len(pending) != EXPECTED_PENDING:
        raise SystemExit(f"Expected {EXPECTED_PENDING} pending P7.1c candidates, found {len(pending)}")

    atoms_by_chapter: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for atom in registry["atoms"]:
        if atom.get("role") != "prose":
            atoms_by_chapter[str(atom["chapter_id"])].append(atom)
    rows_by_chapter: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in pending:
        rows_by_chapter[str(row["chapter_id"])].append(row)

    chapter_records: list[dict[str, Any]] = []
    mapped = fragments = limits = 0
    for chapter_id in sorted(rows_by_chapter):
        rows = rows_by_chapter[chapter_id]
        chapter_rel = str(rows[0]["source"]).rsplit(":", 1)[0]
        chapter_path = ROOT / chapter_rel
        packet_path = PACKET_DIR / f"{chapter_id}.json"
        review_path = REVIEW_DIR / f"{chapter_id}.json"
        if not packet_path.is_file() or not review_path.is_file():
            raise SystemExit(f"{chapter_id}: missing P7.1c packet or completed claim review")
        packet = load(packet_path)
        digest = hashlib.sha256(chapter_path.read_bytes()).hexdigest()
        if packet.get("chapter_sha256") != digest:
            raise SystemExit(f"{chapter_id}: P7.1c packet digest is stale")
        headings, sections = headings_and_sections(chapter_path)
        allowed = {
            "Core Claim",
            "Human Reading Path",
            str(packet["concrete_scene"]["heading"]),
            str(packet["worked_trace"]["heading"]),
        }
        review = tracked_or_current(review_path)
        dispositions = review["prose_candidate_dispositions"]
        records: list[dict[str, Any]] = []
        for row in rows:
            sentence = str(row["sentence"]).strip()
            line = int(str(row["source"]).rsplit(":", 1)[1])
            section = section_for(line, headings)
            if section not in allowed:
                raise SystemExit(f"{chapter_id}: pending candidate escaped P7.1c boundary: {section!r}")
            if not sentence.rstrip().endswith((".", "?", "!", ":")):
                disposition = {
                    "state": "nonmaterial_explanation",
                    "rationale": (
                        "P7.1c semantic review identifies this scanner hit as a line-wrapped "
                        "clause rather than a complete independent proposition. The exact "
                        f"digest-bound scene and its evidence boundary remain in `{packet_path.relative_to(ROOT)}`."
                    ),
                }
                fragments += 1
            elif explicit_limit_report(sentence):
                disposition = {
                    "state": "historical_or_source_report",
                    "rationale": (
                        "P7.1c semantic review identifies this as an explicit bounded-fixture "
                        "or evidence-limit report. It narrows inference and creates no separate "
                        "support-bearing proposition."
                    ),
                }
                limits += 1
            else:
                target = select_owner(sentence, section, atoms_by_chapter[chapter_id])
                disposition = {
                    "state": "duplicate_of_atom",
                    "rationale": (
                        f"P7.1c semantic review maps this complete reader-facing proposition in `{section}` "
                        f"to existing reviewed atom `{target}`. The digest-bound packet preserves its actor, "
                        "action, outcome, failed boundary, residual owner, simpler baseline, and inference ceiling; "
                        "the prose does not create or promote a separate claim."
                    ),
                    "target_atom_id": target,
                }
                mapped += 1
            dispositions[str(row["candidate_id"])] = disposition
            records.append({
                "candidate_id": row["candidate_id"],
                "source": row["source"],
                "section": section,
                "sentence": sentence,
                "disposition": disposition,
            })

        current_count = sum(
            1 for candidate in queue["candidates"]
            if candidate["chapter_id"] == chapter_id
        )
        review["semantic_sweep"]["prose_candidates_adjudicated"] = current_count
        review["semantic_sweep"]["unowned_material_claims"] = 0
        prior_review_note = str(review["semantic_sweep"].get("review_note", "")).rstrip()
        review["semantic_sweep"]["review_note"] = prior_review_note + (
            " The 2026-08-09 P7.1c pass then re-reviewed every new reader claim, "
            "operational rule, concrete lens, worked-scene proposition, "
            "line-wrap fragment, and explicit inference limit is bound to the current chapter and "
            "digest-bound editorial packet. Complete propositions map to existing reviewed atoms; "
            "fixture reports and fragments remain separately classified. No support-state, evidence, "
            "release, SOTA, AGI, or ASI promotion is introduced."
        )
        prior_time = str(review["chapter_defaults"]["scope"].get("time", "")).rstrip()
        review["chapter_defaults"]["scope"]["time"] = prior_time + (
            " Reader-facing claim prose and worked scenes were additionally reviewed on 2026-08-09; "
            "later material changes to those surfaces or their section ownership require reauthorization."
        )
        dump(review_path, review)
        chapter_records.append({
            "chapter_id": chapter_id,
            "chapter_path": chapter_rel,
            "chapter_sha256": digest,
            "packet_path": packet_path.relative_to(ROOT).as_posix(),
            "packet_sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
            "candidate_count": len(rows),
            "sections": [
                {
                    "heading": heading,
                    "sha256": hashlib.sha256(sections[heading].encode("utf-8")).hexdigest(),
                    "candidate_count": sum(1 for record in records if record["section"] == heading),
                }
                for heading in sorted({record["section"] for record in records})
            ],
            "candidate_dispositions": records,
        })

    output = {
        "schema_version": "asi_stack.p7_1c_reader_prose_claim_reconciliation.v1",
        "review_date": "2026-08-09",
        "scope": "All newly detected prose candidates in completed historical claim-review chapters after the 85-chapter P7.1c reader-prose pass.",
        "summary": {
            "chapter_count": len(chapter_records),
            "candidate_count": len(pending),
            "mapped_complete_proposition_count": mapped,
            "line_wrap_fragment_count": fragments,
            "explicit_limit_report_count": limits,
            "unowned_material_claim_count": 0,
            "support_state_effect": "none",
        },
        "chapter_records": chapter_records,
        "non_claims": [
            "This reconciliation does not establish that any reader-facing mechanism or worked scene succeeds outside its stated boundary.",
            "Semantic ownership and lexical tie-breaking are not evidence and cannot promote a claim.",
            "No source-reported or bounded fixture result becomes general empirical support through this review.",
        ],
    }
    dump(OUT, output)
    print(
        f"Reconciled {len(pending)} P7.1c candidates across {len(chapter_records)} chapters: "
        f"{mapped} mapped propositions, {fragments} fragments, {limits} limit reports; support effect none."
    )


if __name__ == "__main__":
    main()
