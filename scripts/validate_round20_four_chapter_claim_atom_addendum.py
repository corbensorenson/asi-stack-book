#!/usr/bin/env python3
"""Validate the additive Round 20 four-chapter atom packet."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from build_canonical_public_status import validate_against_schema
from build_round20_four_chapter_claim_atom_addendum import (
    CHAPTER_IDS,
    OUTPUT,
    ROOT,
    build,
)


SCHEMA = ROOT / "schemas/round20_four_chapter_claim_atom_addendum.schema.json"
ROLES = ["core", "boundary", "mechanism", "failure_boundary", "argument_exit"]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def errors(packet: dict) -> list[str]:
    out = validate_against_schema(packet, load(SCHEMA), str(OUTPUT.relative_to(ROOT)))
    if packet != build():
        out.append("tracked atom packet is stale against the manifest-derived build")
    atoms = packet.get("atoms", [])
    if [row.get("chapter_id") for row in packet.get("chapter_reviews", [])] != CHAPTER_IDS:
        out.append("chapter-review order does not match the frozen four-chapter denominator")
    if len({row.get("id") for row in atoms}) != 20:
        out.append("atom identities are not exactly unique")
    for chapter_id in CHAPTER_IDS:
        rows = [row for row in atoms if row.get("chapter_id") == chapter_id]
        if [row.get("role") for row in rows] != ROLES:
            out.append(f"{chapter_id}: five-role atom contract drifted")
        if any(row.get("owner") != chapter_id for row in rows):
            out.append(f"{chapter_id}: atom owner drifted")
        review = next(
            (row for row in packet.get("chapter_reviews", []) if row.get("chapter_id") == chapter_id),
            None,
        )
        if review is None or review.get("atom_ids") != [row.get("id") for row in rows]:
            out.append(f"{chapter_id}: review denominator does not match its atoms")
    return out


def main() -> None:
    packet = load(OUTPUT)
    out = errors(packet)
    mutations = []

    def reject(label, mutate):
        candidate = copy.deepcopy(packet)
        mutate(candidate)
        if not errors(candidate):
            out.append(f"negative control accepted: {label}")
        mutations.append(label)

    reject("chapter deletion", lambda p: p["chapter_ids"].pop())
    reject("atom deletion", lambda p: p["atoms"].pop())
    reject("owner drift", lambda p: p["atoms"][0].__setitem__("owner", "wrong-owner"))
    reject("support promotion", lambda p: p["atoms"][0].__setitem__("support_state", "source-derived"))
    reject("falsifier deletion", lambda p: p["atoms"][0].__setitem__("falsifier", ""))
    reject("evidence-lane deletion", lambda p: p["atoms"][0]["required_evidence_lanes"].pop())
    reject("review mismatch", lambda p: p["chapter_reviews"][0]["atom_ids"].pop())
    reject("historical rewrite", lambda p: p.__setitem__("historical_atom_sources_rewritten", True))

    if out:
        print("Round 20 atom addendum validation failed:")
        for item in out:
            print(f" - {item}")
        raise SystemExit(1)
    print(
        "Round 20 atom addendum passed: four manifest owners, twenty bounded atoms, "
        f"{len(mutations)}/{len(mutations)} rejecting mutations, and zero support movement."
    )


if __name__ == "__main__":
    main()
