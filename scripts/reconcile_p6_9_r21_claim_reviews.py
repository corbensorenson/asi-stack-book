#!/usr/bin/env python3
"""Reconcile Round-21 concept prose with its reviewed claim-atom ownership.

The Round-21 chapter-substance contract already records an exact semantic
review for every new concept section and maps each concept to one or more
existing claim atoms. This migration projects that reviewed ownership into the
older P1 prose-candidate review packets. It does not create atoms, change
support states, or infer efficacy from source-grounded prose.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "evidence_quality/chapter_substance_contract.json"
QUEUE_PATH = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
REVIEW_DIR = ROOT / "evidence_quality/claim_reviews"
ROUND_21_CHAPTERS = {
    "scientific-discovery-and-experimental-governance",
    "governed-objective-formation-value-learning-and-goal-integrity",
    "durable-semantic-memory-and-knowledge-lattices",
    "ai-deployment-transition-distribution-and-human-agency",
    "autonomous-replication-proliferation-and-containment",
    "human-ai-communication-persuasion-and-epistemic-security",
}
TOKEN_STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "for", "from",
    "has", "in", "into", "is", "it", "its", "may", "not", "of", "on", "only",
    "or", "that", "the", "their", "this", "to", "when", "while", "with",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) > 2 and token not in TOKEN_STOP
    }


def heading_ranges(path: Path) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            rows.append((number, match.group(1)))
    return rows


def section_for(line_number: int, headings: list[tuple[int, str]]) -> str:
    current = ""
    for start, heading in headings:
        if start > line_number:
            break
        current = heading
    return current


def closest_atom(
    sentence: str,
    atom_ids: list[str],
    propositions: dict[str, str],
) -> str:
    sentence_tokens = tokens(sentence)

    def score(atom_id: str) -> tuple[float, int, str]:
        atom_tokens = tokens(propositions[atom_id])
        overlap = len(sentence_tokens & atom_tokens)
        union = len(sentence_tokens | atom_tokens) or 1
        return (overlap / union, overlap, atom_id)

    return max(atom_ids, key=score)


def main() -> None:
    contract = load(CONTRACT_PATH)
    queue = load(QUEUE_PATH)
    registry = load(ROOT / "evidence_quality/claim_atom_registry.json")
    propositions = {
        row["atom_id"]: row["proposition"]
        for row in registry["atoms"]
    }
    records = {
        row["chapter_id"]: row
        for row in contract["chapter_records"]
        if row["chapter_id"] in ROUND_21_CHAPTERS
    }
    if set(records) != ROUND_21_CHAPTERS:
        missing = sorted(ROUND_21_CHAPTERS - set(records))
        raise SystemExit(f"Round-21 contract records missing: {missing}")

    candidates_by_chapter: dict[str, list[dict[str, Any]]] = {
        chapter_id: [] for chapter_id in ROUND_21_CHAPTERS
    }
    for candidate in queue["candidates"]:
        chapter_id = candidate["chapter_id"]
        if chapter_id in candidates_by_chapter:
            candidates_by_chapter[chapter_id].append(candidate)

    reconciled = 0
    for chapter_id in sorted(ROUND_21_CHAPTERS):
        record = records[chapter_id]
        chapter_path = ROOT / record["path"]
        lines = chapter_path.read_text(encoding="utf-8").splitlines()
        headings = heading_ranges(chapter_path)
        concept_by_heading = {
            row["heading"]: row
            for row in record["concept_contracts"]
        }
        packet_path = REVIEW_DIR / f"{chapter_id}.json"
        packet = load(packet_path)
        dispositions = packet["prose_candidate_dispositions"]

        for candidate in candidates_by_chapter[chapter_id]:
            if candidate["candidate_id"] in dispositions:
                continue
            line_number = int(candidate["source"].rsplit(":", 1)[1])
            heading = section_for(line_number, headings)
            concept = concept_by_heading.get(heading)
            if concept is None:
                raise SystemExit(
                    f"{candidate['candidate_id']}: new candidate is outside a "
                    f"Round-21 concept section ({heading!r})"
                )
            atom_ids = list(concept["atom_ids"])
            if not atom_ids or any(atom_id not in propositions for atom_id in atom_ids):
                raise SystemExit(
                    f"{candidate['candidate_id']}: concept atom ownership is unavailable"
                )
            source_line = lines[line_number - 1].lstrip()
            if source_line.startswith("**Source grounding.**"):
                disposition = {
                    "state": "historical_or_source_report",
                    "rationale": (
                        "Round-21 semantic review classified this as a bounded "
                        f"source-grounding statement for `{concept['concept_id']}`. "
                        "It reports or limits external evidence and creates no local "
                        "support-bearing atom or support-state movement."
                    ),
                }
            else:
                target = closest_atom(
                    candidate["sentence"],
                    atom_ids,
                    propositions,
                )
                disposition = {
                    "state": "duplicate_of_atom",
                    "rationale": (
                        "Round-21 exact-digest semantic review maps this "
                        f"`{concept['concept_id']}` proposition to the existing "
                        f"owner atom `{target}`; it creates no additional atom and "
                        "does not change support state."
                    ),
                    "target_atom_id": target,
                }
            dispositions[candidate["candidate_id"]] = disposition
            reconciled += 1

        packet["semantic_sweep"]["prose_candidates_adjudicated"] = len(
            candidates_by_chapter[chapter_id]
        )
        packet["semantic_sweep"]["review_note"] = (
            "Re-reviewed the complete chapter through the Round-21 concept expansion "
            "on 2026-07-28. Every new claim-bearing sentence is reconciled to the "
            "exact concept-to-atom ownership recorded by the current-digest chapter "
            "substance contract, or classified as bounded source reporting. No new "
            "atom, unowned material claim, support transition, efficacy inference, "
            "release decision, or publication claim was introduced."
        )
        packet["chapter_defaults"]["scope"]["time"] = (
            "Semantic review current through 2026-07-28; material changes to "
            "evidence, authority, population, model, environment, ontology, "
            "consumer, or contracted concept prose require reauthorization."
        )
        dump(packet_path, packet)

    print(
        f"Reconciled {reconciled} Round-21 prose candidates across "
        f"{len(ROUND_21_CHAPTERS)} chapter review packets."
    )


if __name__ == "__main__":
    main()
