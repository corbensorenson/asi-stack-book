#!/usr/bin/env python3
"""Validate Round 22 concept-linked atom custody and rejecting controls."""

from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path

from visual_chapter_source import canonical_chapter_sha256


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "evidence_quality/round22_concept_linked_claim_atom_addendum.json"
CONTRACT = ROOT / "evidence_quality/chapter_substance_contract.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return canonical_chapter_sha256(path)


def errors(packet: dict, contract: dict) -> list[str]:
    out: list[str] = []
    atoms = packet.get("atoms", [])
    reviews = packet.get("chapter_reviews", [])
    chapter_ids = packet.get("chapter_ids", [])
    if packet.get("chapter_count") != 13 or len(chapter_ids) != 13:
        out.append("thirteen-chapter denominator drifted")
    if packet.get("atom_count") != 104 or len(atoms) != 104:
        out.append("104-concept denominator drifted")
    if len({row.get("id") for row in atoms}) != 104:
        out.append("atom identities are not unique")
    if Counter(row.get("chapter_id") for row in atoms) != Counter({key: 8 for key in chapter_ids}):
        out.append("one-atom-per-reviewed-concept chapter distribution drifted")
    if packet.get("atom_count_is_acceptance_target") is not False:
        out.append("atom count became an acceptance target")
    if packet.get("support_state_effect") != "none":
        out.append("packet moved support")

    contract_by_id = {row["chapter_id"]: row for row in contract.get("chapter_records", [])}
    for chapter_id in chapter_ids:
        record = contract_by_id.get(chapter_id, {})
        concepts = record.get("concept_contracts", [])
        rows = [row for row in atoms if row.get("chapter_id") == chapter_id]
        review = next((row for row in reviews if row.get("chapter_id") == chapter_id), None)
        expected_concepts = [row.get("concept_id") for row in concepts]
        if len(concepts) != 8:
            out.append(f"{chapter_id}: no eight-concept current contract")
            continue
        if [row.get("concept_id") for row in rows] != expected_concepts:
            out.append(f"{chapter_id}: atom concepts drifted from contract")
        if any(row.get("owner") != chapter_id for row in rows):
            out.append(f"{chapter_id}: owner drifted")
        if any(row.get("support_state") != "argument" for row in rows):
            out.append(f"{chapter_id}: atom support promoted")
        if any(not row.get("falsifier") or not row.get("source_grounding") for row in rows):
            out.append(f"{chapter_id}: falsifier or source boundary missing")
        if review is None:
            out.append(f"{chapter_id}: review missing")
            continue
        chapter_path = ROOT / record["path"]
        if review.get("chapter_sha256") != digest(chapter_path):
            out.append(f"{chapter_id}: chapter digest stale")
        if review.get("concept_ids") != expected_concepts:
            out.append(f"{chapter_id}: review concept denominator drifted")
        if review.get("atom_ids") != [row.get("id") for row in rows]:
            out.append(f"{chapter_id}: review atom denominator drifted")
    return out


def main() -> None:
    packet = load(PACKET)
    contract = load(CONTRACT)
    out = errors(packet, contract)
    mutations = []

    def reject(label, mutate):
        candidate = copy.deepcopy(packet)
        mutate(candidate)
        if not errors(candidate, contract):
            out.append(f"negative control accepted: {label}")
        mutations.append(label)

    reject("atom deletion", lambda p: p["atoms"].pop())
    reject("owner drift", lambda p: p["atoms"][0].__setitem__("owner", "wrong-owner"))
    reject("support promotion", lambda p: p["atoms"][0].__setitem__("support_state", "bounded"))
    reject("falsifier deletion", lambda p: p["atoms"][0].__setitem__("falsifier", ""))
    reject("source boundary deletion", lambda p: p["atoms"][0].__setitem__("source_grounding", ""))
    reject("review mismatch", lambda p: p["chapter_reviews"][0]["atom_ids"].pop())
    reject("digest drift", lambda p: p["chapter_reviews"][0].__setitem__("chapter_sha256", "0" * 64))
    reject("count target activation", lambda p: p.__setitem__("atom_count_is_acceptance_target", True))

    if out:
        print("Round 22 concept-linked atom validation failed:")
        for item in out:
            print(f" - {item}")
        raise SystemExit(1)
    print(
        "Round 22 concept-linked atom validation passed: 13 chapters, "
        f"104 reviewed concepts, {len(mutations)}/{len(mutations)} rejecting mutations, "
        "and zero support movement."
    )


if __name__ == "__main__":
    main()
