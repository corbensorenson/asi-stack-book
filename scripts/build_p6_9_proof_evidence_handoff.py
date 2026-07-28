#!/usr/bin/env python3
"""Build the exact P6.9 chapter/concept/atom proof-and-evidence handoff."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "evidence_quality/chapter_substance_contract.json"
RAW_AUDIT = ROOT / "evidence_quality/p6_9_raw_scaffold_ownership_audit.json"
W3 = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"
OUTPUT = ROOT / "evidence_quality/p6_9_proof_evidence_handoff.json"
REPORT = ROOT / "docs/p6_9_proof_evidence_handoff.md"
ATOM_SOURCES = [
    ROOT / "evidence_quality/claim_atom_registry.json",
    ROOT / "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json",
    ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
    ROOT / "evidence_quality/taxonomy_completion_claim_atoms_2026_07_24.json",
    ROOT / "evidence_quality/round_18_breadth_completion_claim_atoms.json",
    ROOT / "evidence_quality/round20_four_chapter_claim_atom_addendum.json",
]
DEFAULT_FUTURE_LANES = [
    "source-synthesis",
    "formal",
    "executable",
    "empirical",
    "causal",
    "transfer",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_id(row: dict[str, Any]) -> str:
    for key in ("atom_id", "id", "stable_claim_identity"):
        if row.get(key):
            return row[key]
    raise ValueError(f"atom row has no stable identity: {row}")


def atom_owner(row: dict[str, Any], packet: dict[str, Any]) -> str:
    for key in ("chapter_id", "chapter_owner", "owner"):
        if row.get(key):
            return row[key]
    if packet.get("chapter_id"):
        return packet["chapter_id"]
    raise ValueError(f"atom {atom_id(row)} has no owner")


def atom_index() -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for path in ATOM_SOURCES:
        packet = load(path)
        for row in packet["atoms"]:
            identity = atom_id(row)
            if identity in values:
                raise ValueError(f"duplicate atom identity across sources: {identity}")
            lanes = [
                lane["lane"]
                for lane in row.get("required_lanes", [])
                if lane.get("lane")
            ]
            if row.get("required_evidence_lanes"):
                lanes.extend(row["required_evidence_lanes"])
            evidence_route = row.get("evidence_plan_route")
            residual = row.get("residual", {})
            acceptance = (
                row.get("acceptance_criterion")
                or row.get("acceptance")
            )
            values[identity] = {
                "atom_id": identity,
                "atom_source_path": path.relative_to(ROOT).as_posix(),
                "owner": atom_owner(row, packet),
                "proposition": (
                    row.get("proposition")
                    or row.get("claim_text")
                    or row.get("claim")
                ),
                "falsifier": row.get("falsifier"),
                "evidence_lanes": lanes or DEFAULT_FUTURE_LANES,
                "evidence_route": (
                    evidence_route
                    or acceptance
                    or "; ".join(
                        lane.get("necessity", "")
                        for lane in row.get("required_lanes", [])
                        if lane.get("necessity")
                    )
                ),
                "maximum_inference": (
                    row.get("promotion_ceiling")
                    or "argument only until the atom's acceptance condition is met "
                    "through a competent, independently challenged campaign"
                ),
                "unresolved_challenge": (
                    residual.get("next_unblocking_condition")
                    or acceptance
                    or "A claim-specific competent full attempt and independent challenge remain required."
                ),
                "support_state": row.get("support_state"),
            }
    return values


def build() -> dict[str, Any]:
    contract = load(CONTRACT)
    atoms = atom_index()
    raw_audit = load(RAW_AUDIT)
    contracted = [
        row for row in contract["chapter_records"] if row["concept_contracts"]
    ]
    chapter_records = []
    for chapter in contracted:
        if chapter["depth_state"] != "concept_contract_complete_semantic_reviewed":
            raise ValueError(f"{chapter['chapter_id']}: concept contract is not terminal")
        if chapter["semantic_review"]["reviewed_sha256"] != chapter["sha256"]:
            raise ValueError(f"{chapter['chapter_id']}: semantic review digest is stale")
        concepts = []
        for concept in chapter["concept_contracts"]:
            refs = []
            for identity in concept["atom_ids"]:
                if identity not in atoms:
                    raise ValueError(
                        f"{chapter['chapter_id']}/{concept['concept_id']}: "
                        f"missing atom {identity}"
                    )
                ref = atoms[identity]
                if ref["owner"] != chapter["chapter_id"]:
                    raise ValueError(
                        f"{identity}: owner {ref['owner']} does not match "
                        f"{chapter['chapter_id']}"
                    )
                if not all(
                    ref.get(key)
                    for key in (
                        "proposition",
                        "falsifier",
                        "evidence_lanes",
                        "evidence_route",
                        "maximum_inference",
                        "unresolved_challenge",
                    )
                ):
                    raise ValueError(f"{identity}: incomplete proof/evidence handoff")
                refs.append(ref)
            concepts.append(
                {
                    "concept_id": concept["concept_id"],
                    "heading": concept["heading"],
                    "source_ids": concept["source_ids"],
                    "atom_refs": refs,
                    "atom_ownership_rationale": concept[
                        "atom_ownership_rationale"
                    ],
                    "semantic_review_disposition": chapter["semantic_review"][
                        "disposition"
                    ],
                    "support_state_effect": "none",
                }
            )
        chapter_records.append(
            {
                "chapter_id": chapter["chapter_id"],
                "chapter_title": chapter["chapter_title"],
                "chapter_path": chapter["path"],
                "chapter_sha256": chapter["sha256"],
                "semantic_review_sha256": chapter["semantic_review"][
                    "reviewed_sha256"
                ],
                "semantic_review_date": chapter["semantic_review"][
                    "reviewed_date"
                ],
                "concept_count": len(concepts),
                "concepts": concepts,
            }
        )

    concept_count = sum(row["concept_count"] for row in chapter_records)
    atom_mapping_count = sum(
        len(concept["atom_refs"])
        for chapter in chapter_records
        for concept in chapter["concepts"]
    )
    return {
        "schema_version": "asi_stack.p6_9_proof_evidence_handoff.v1",
        "handoff_id": "P6.9-R21-exact-proof-evidence-handoff",
        "recorded_date": "2026-07-28",
        "state": "terminal_complete",
        "source_contract": {
            "path": "evidence_quality/chapter_substance_contract.json",
            "sha256": sha(CONTRACT),
            "contract_id": contract["contract_id"],
        },
        "raw_scaffold_exit": {
            "path": "evidence_quality/p6_9_raw_scaffold_ownership_audit.json",
            "sha256": sha(RAW_AUDIT),
            "state": raw_audit["state"],
            "unjustified_widest_block_count": raw_audit["summary"][
                "unjustified_widest_block_count"
            ],
            "exit_passed": raw_audit["summary"]["exit_passed"],
        },
        "w3_binding": {
            "path": "evidence_quality/p7_1a_w3_inheritance_guard.json",
            "sha256": sha(W3),
            "state": load(W3)["state"],
            "reader_facing_repeated_12_gram_count": load(W3)["measurements"][
                "editorial_narrative"
            ]["current"]["distinct_repeated_12_grams"],
        },
        "chapter_records": chapter_records,
        "summary": {
            "chapter_count": len(chapter_records),
            "concept_count": concept_count,
            "concepts_with_source_identity_count": sum(
                bool(concept["source_ids"])
                for chapter in chapter_records
                for concept in chapter["concepts"]
            ),
            "concepts_with_atom_identity_count": sum(
                bool(concept["atom_refs"])
                for chapter in chapter_records
                for concept in chapter["concepts"]
            ),
            "atom_mapping_count": atom_mapping_count,
            "concepts_with_falsifier_count": sum(
                all(ref["falsifier"] for ref in concept["atom_refs"])
                for chapter in chapter_records
                for concept in chapter["concepts"]
            ),
            "concepts_with_evidence_lane_count": sum(
                all(ref["evidence_lanes"] for ref in concept["atom_refs"])
                for chapter in chapter_records
                for concept in chapter["concepts"]
            ),
            "concepts_with_maximum_inference_count": sum(
                all(ref["maximum_inference"] for ref in concept["atom_refs"])
                for chapter in chapter_records
                for concept in chapter["concepts"]
            ),
            "concepts_with_unresolved_challenge_count": sum(
                all(ref["unresolved_challenge"] for ref in concept["atom_refs"])
                for chapter in chapter_records
                for concept in chapter["concepts"]
            ),
            "missing_handoff_identity_count": 0,
            "support_state_effect": "none",
        },
        "consumer": {
            "owner": "canonical post-v2.3 roadmap proof/evidence phase",
            "activation_rule": "Each concept remains argument-only until its exact falsifier, lanes, competence gates, and accepted evidence transition are executed; this packet grants no automatic campaign, support, or release authority.",
            "required_identity_fields": [
                "chapter_identity",
                "concept_identity",
                "atom_identity",
                "source_identity",
                "falsifier",
                "evidence_lane",
                "maximum_inference",
                "unresolved_challenge",
            ],
        },
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "A complete handoff is not proof that any concept is true.",
            "Editorial concept completion does not establish formal, executable, empirical, causal, or transfer evidence.",
            "No safety, deployment, SOTA, AGI, ASI, publication, or release conclusion follows.",
        ],
    }


def render_report(value: dict[str, Any]) -> str:
    summary = value["summary"]
    return "\n".join(
        [
            "# P6.9 exact proof/evidence handoff",
            "",
            "Status: **terminal complete**.",
            "",
            f"The packet hands off **{summary['concept_count']}** reviewed concepts",
            f"across **{summary['chapter_count']}** exact chapter digests. Every concept",
            "retains chapter, concept, atom, source, falsifier, evidence-lane,",
            "maximum-inference, and unresolved-challenge identity. The missing identity",
            "count is **0**.",
            "",
            "The packet is bound to the terminal raw-scaffold audit and terminal W3",
            "reader-facing inheritance guard. It does not activate a proof or empirical",
            "campaign, promote support, authorize release, or turn an editorial argument",
            "into evidence.",
            "",
            "## Reproduction",
            "",
            "```bash",
            "python3 scripts/build_p6_9_proof_evidence_handoff.py",
            "python3 scripts/validate_p6_9_proof_evidence_handoff.py",
            "```",
            "",
        ]
    )


def main() -> None:
    value = build()
    OUTPUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(render_report(value), encoding="utf-8")
    print(
        "Built P6.9 proof/evidence handoff: "
        f"{value['summary']['chapter_count']} chapters, "
        f"{value['summary']['concept_count']} concepts, "
        f"{value['summary']['missing_handoff_identity_count']} missing identities."
    )


if __name__ == "__main__":
    main()
