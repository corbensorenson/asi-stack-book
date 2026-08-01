#!/usr/bin/env python3
"""Validate R16-A as a complete, reviewed, non-promoting organization packet."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from build_post_activation_six_chapter_claim_atom_addendum import CHAPTERS, build
from visual_chapter_source import canonical_chapter_sha256


ROOT = Path(__file__).resolve().parents[1]
ADDENDUM = ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json"
SCHEMA = ROOT / "schemas/post_activation_six_chapter_claim_atom_addendum.schema.json"
EVIDENCE_PLAN = ROOT / "docs/per_chapter_evidence_plan.md"
REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
HISTORICAL_ADDENDUM = ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return canonical_chapter_sha256(path)


def manifest_chapters() -> dict[str, dict]:
    manifest = load(ROOT / "book_structure.json")
    return {
        chapter["id"]: chapter
        for part in manifest["parts"]
        for chapter in part["chapters"]
    }


def errors(packet: dict) -> list[str]:
    out: list[str] = []
    schema = load(SCHEMA)
    for error in sorted(Draft202012Validator(schema).iter_errors(packet), key=lambda e: list(e.path)):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")

    if packet != build():
        out.append("packet is not the exact deterministic reviewed R16-A projection")

    expected_ids = [chapter["chapter_id"] for chapter in CHAPTERS]
    manifest = manifest_chapters()
    reviews = packet.get("chapter_reviews", [])
    atoms = packet.get("atoms", [])
    review_by_chapter = {row.get("chapter_id"): row for row in reviews}
    atom_ids = [row.get("id") for row in atoms]
    if len(atom_ids) != len(set(atom_ids)):
        out.append("atom identities are not unique")
    if [row.get("chapter_id") for row in reviews] != expected_ids:
        out.append("chapter review denominator or order drifted")
    if packet.get("chapter_count") != 6 or packet.get("atom_count") != 30:
        out.append("declared six-chapter or thirty-atom denominator drifted")
    if packet.get("historical_activation_atom_denominator") != 3730:
        out.append("historical 3,730-atom activation denominator was rewritten")
    if packet.get("historical_single_chapter_addendum_atom_count") != 15:
        out.append("historical 15-atom addendum denominator was rewritten")
    if packet.get("historical_denominators_rewritten") is not False:
        out.append("packet claims permission to rewrite historical denominators")
    if len(load(REGISTRY).get("atoms", [])) != 4059:
        out.append("current 4,059-atom registry was rewritten")
    if len(load(HISTORICAL_ADDENDUM).get("atoms", [])) != 15:
        out.append("historical replaceable-substrates addendum was rewritten")

    evidence_plan = EVIDENCE_PLAN.read_text(encoding="utf-8")
    expected_roles = ["core", "boundary", "mechanism", "failure_boundary", "argument_exit"]
    for chapter_id in expected_ids:
        chapter = manifest.get(chapter_id)
        if chapter is None:
            out.append(f"manifest chapter missing: {chapter_id}")
            continue
        chapter_atoms = [row for row in atoms if row.get("chapter_id") == chapter_id]
        if len(chapter_atoms) != 5:
            out.append(f"{chapter_id}: does not have exactly five atoms")
            continue
        if [row.get("role") for row in chapter_atoms] != expected_roles:
            out.append(f"{chapter_id}: role sequence drifted")
        if [row.get("ordinal") for row in chapter_atoms] != [1, 2, 3, 4, 5]:
            out.append(f"{chapter_id}: ordinal sequence drifted")
        core = chapter_atoms[0]
        if core.get("id") != f"{chapter_id}.core":
            out.append(f"{chapter_id}: stable core identity drifted")
        if core.get("claim") != chapter.get("core_claim"):
            out.append(f"{chapter_id}: core claim is not the exact manifest proposition")
        if any(row.get("owner") != chapter_id for row in chapter_atoms):
            out.append(f"{chapter_id}: chapter owner drifted")
        if any(row.get("support_state") != "argument" or row.get("support_state_effect") != "none" for row in chapter_atoms):
            out.append(f"{chapter_id}: atom support was promoted or moved")
        if any(row.get("promotion_ceiling") != "argument_until_claim_specific_campaign_and_accepted_evidence_transition" for row in chapter_atoms):
            out.append(f"{chapter_id}: promotion ceiling drifted")
        if any(not row.get("falsifier") or not row.get("acceptance_criterion") for row in chapter_atoms):
            out.append(f"{chapter_id}: falsifier or acceptance criterion missing")
        if any(not row.get("non_claims") or len(row["non_claims"]) < 2 for row in chapter_atoms):
            out.append(f"{chapter_id}: non-claim boundary missing")
        if chapter_id not in evidence_plan:
            out.append(f"{chapter_id}: evidence-plan owner row missing")
        review = review_by_chapter.get(chapter_id)
        if review is None:
            out.append(f"{chapter_id}: review receipt missing")
            continue
        path = ROOT / review.get("chapter_path", "")
        if not path.exists() or review.get("chapter_sha256") != sha256(path):
            out.append(f"{chapter_id}: chapter review digest is stale")
        if review.get("atom_ids") != [row.get("id") for row in chapter_atoms]:
            out.append(f"{chapter_id}: review receipt atom denominator drifted")
        if review.get("decision") != "retain_at_argument_no_promotion":
            out.append(f"{chapter_id}: review disposition promoted or drifted")

    if packet.get("summary", {}).get("promoted_atom_count") != 0:
        out.append("summary reports a promoted atom")
    if packet.get("support_state_effect") != "none" or packet.get("release_effect") != "none":
        out.append("packet changes support or release state")
    return out


def main() -> None:
    packet = load(ADDENDUM)
    failures = errors(packet)
    mutations: list[tuple[str, dict]] = []

    def mutate(label: str, edit) -> None:
        candidate = copy.deepcopy(packet)
        edit(candidate)
        mutations.append((label, candidate))

    mutate("chapter receipt deletion", lambda p: p["chapter_reviews"].pop())
    mutate("atom deletion", lambda p: p["atoms"].pop())
    mutate("duplicate atom identity", lambda p: p["atoms"][1].__setitem__("id", p["atoms"][0]["id"]))
    mutate("wrong owner", lambda p: p["atoms"][0].__setitem__("owner", "wrong-owner"))
    mutate("core proposition rewrite", lambda p: p["atoms"][0].__setitem__("claim", "A rewritten core proposition that is intentionally long enough to pass only superficial length checks."))
    mutate("chapter digest rewrite", lambda p: p["chapter_reviews"][0].__setitem__("chapter_sha256", "0" * 64))
    mutate("support promotion", lambda p: p["atoms"][0].__setitem__("support_state", "prototype-backed"))
    mutate("support movement", lambda p: p["atoms"][0].__setitem__("support_state_effect", "promote"))
    mutate("falsifier deletion", lambda p: p["atoms"][0].__setitem__("falsifier", ""))
    mutate("acceptance deletion", lambda p: p["atoms"][0].__setitem__("acceptance_criterion", ""))
    mutate("evidence route deletion", lambda p: p["atoms"][0].__setitem__("evidence_plan_route", ""))
    mutate("nonclaim deletion", lambda p: p["atoms"][0].__setitem__("non_claims", []))
    mutate("historical denominator rewrite", lambda p: p.__setitem__("historical_activation_atom_denominator", 4067))
    mutate("review atom mismatch", lambda p: p["chapter_reviews"][0]["atom_ids"].pop())

    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("R16-A six-chapter addendum validation failed:\n - " + "\n - ".join(failures))
    print(
        "R16-A six-chapter claim organization passed: 6/6 chapter reviews, "
        "30/30 reviewed atoms, 0 promotions, historical denominators preserved, "
        f"and {len(mutations)}/{len(mutations)} mutations rejected."
    )


if __name__ == "__main__":
    main()
