#!/usr/bin/env python3
"""Record the first C6 residual tranche: two redundant fixture witnesses."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from build_proof_rationalization_registry import normalize
from build_proof_semantic_depth_overlay import statement_key


ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = "d0f9bda14f1253999f2c40d556d925d31e4b36a4"
LEDGER = ROOT / "proofs/proof_semantic_rationalization_ledger.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
CHAPTER = ROOT / "chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd"
OUTLINE = ROOT / "docs/book_outline.md"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)

RETIREMENTS = [
    {
        "sequence": 107,
        "module": "lean/AsiStackProofs/LivingBook.lean",
        "name": "curated_reader_blocked_candidate_fixture_routes_to_accessibility_review",
        "replacement_refs": [
            "lean/AsiStackProofs/LivingBook.lean::local_reader_artifacts_do_not_clear_missing_accessibility_review",
            "scripts/validate_reader_release_candidate_bridge.py",
            "experiments/reader_release_candidate_bridge/results/2026-07-05-local.json",
        ],
        "target_ref": "proof-target:lean:living_book.methodology.reader_release_candidate_bridge",
        "semantic_basis": [
            "The retired theorem reduces one authored blocked-candidate constant by reflexivity.",
            "The adjacent retained theorem proves the same route for every locally complete candidate whose accessibility review is incomplete.",
            "Nine further retained route theorems cover missing screen-reader, WCAG, audio, approval, and support-promotion cases.",
            "The deterministic reader-release consumer preserves the historical fixture result and eleven invalid controls without becoming a Lean proof.",
            "The public target remains implemented by the retained universal route family and independent consumer.",
        ],
        "maximum_inference": (
            "The retained family establishes only finite reader-candidate routing under "
            "declared predicates; it does not approve, publish, or validate any reader format."
        ),
    },
    {
        "sequence": 108,
        "module": "lean/AsiStackProofs/ProofCarryingContracts.lean",
        "name": "circle_public_consumer_gate_fixture_accepted",
        "replacement_refs": [
            "lean/AsiStackProofs/ProofCarryingContracts.lean::circle_public_consumer_gate_promotion_overclaim_rejected",
            "lean/AsiStackProofs/ProofCarryingContracts.lean::circle_public_consumer_gate_missing_mutation_control_rejected",
            "scripts/validate_circle_public_replay.py",
        ],
        "target_ref": "proof-target:lean:circle_contracts.public_consumer_gate.fixture_bridge",
        "semantic_basis": [
            "The retired theorem proves acceptance of a hand-authored all-green fixture by field reflexivity.",
            "The two retained quantified theorems reject promotion, chapter-core, deployed-transport, and missing-control overclaims for any allegedly accepted fixture.",
            "The independent consumer computes the one valid receipt and four invalid controls from public replay inputs.",
            "Keeping executable counts and quantified rejection facts separate is stronger evidence hygiene than copying the consumer summary into Lean.",
            "The public target is narrowed to the retained quantified rejection consequences and separately labeled replay result.",
        ],
        "maximum_inference": (
            "The retained split surface establishes finite rejection consequences and an "
            "independent deterministic replay; it does not prove Circle transport, external "
            "theorem truth, workload benefit, deployment, or support movement."
        ),
    },
]

OLD_CIRCLE_TARGET = (
    "The public Circle consumer-gate fixture records one valid receipt, four rejected "
    "mutation controls, seven required theorem IDs, pinned digest fields, blocked support "
    "movement, no chapter-core promotion, and no deployed-transport claim."
)
NEW_CIRCLE_TARGET = (
    "Any record satisfying the finite Circle public-consumer acceptance contract loses "
    "acceptance when promotion/deployed-transport overclaims or required mutation-control "
    "rejections are present; an independent replay validator separately computes one valid "
    "receipt and four invalid controls."
)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_show(path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{BASELINE_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def theorem_blocks(text: str) -> dict[str, dict[str, str]]:
    declarations = list(DECL_START.finditer(text))
    result = {}
    for match in THEOREM_START.finditer(text):
        end = next(
            (candidate.start() for candidate in declarations if candidate.start() > match.start()),
            len(text),
        )
        block = text[match.start():end]
        signature = normalize(block.split(":= by", 1)[0])
        result[match.group(1)] = {
            "block_sha256": sha256(block.encode()),
            "statement_sha256": sha256(statement_key(signature).encode()),
        }
    return result


def update_circle_target() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] == "circle-calculus-and-proof-carrying-ai-contracts"
    )
    target = next(
        row
        for row in chapter["proof_targets"]
        if row["tag"] == "lean:circle_contracts.public_consumer_gate.fixture_bridge"
    )
    target["target"] = NEW_CIRCLE_TARGET
    STRUCTURE.write_text(json.dumps(structure, indent=2, ensure_ascii=False) + "\n")

    for path in [CHAPTER, OUTLINE]:
        text = path.read_text(encoding="utf-8")
        if NEW_CIRCLE_TARGET in text:
            continue
        if OLD_CIRCLE_TARGET not in text:
            raise SystemExit(f"old Circle target text missing from {path}")
        path.write_text(text.replace(OLD_CIRCLE_TARGET, NEW_CIRCLE_TARGET), encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    row = next(
        row
        for row in triage["records"]
        if row["tag"] == "lean:circle_contracts.public_consumer_gate.fixture_bridge"
    )
    row["formal_target"] = NEW_CIRCLE_TARGET
    row["rationale"] = (
        "Quantified Lean rejection consequences and the independent executable replay are "
        "kept as distinct evidence surfaces; the authored positive fixture witness is retired."
    )
    TRIAGE.write_text(json.dumps(triage, indent=2, ensure_ascii=False) + "\n")


def update_ledger_and_reviews() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger["actions"] = [
        action for action in ledger["actions"] if action["sequence"] <= 106
    ]
    if len(ledger["actions"]) != 106:
        raise SystemExit("expected 106 executed rationalization actions before tranche")
    overlay = json.loads(git_show("proofs/proof_semantic_depth_overlay.json"))
    overlay_rows = {row["theorem_id"]: row for row in overlay["records"]}
    for item in RETIREMENTS:
        module_bytes = git_show(item["module"])
        blocks = theorem_blocks(module_bytes.decode())
        theorem_id = f"{item['module']}::{item['name']}"
        baseline = overlay_rows[theorem_id]
        if baseline.get("theorem_dependency_refs") or baseline.get("theorem_consumer_refs"):
            raise SystemExit(f"retirement is no longer dependency-safe: {theorem_id}")
        source = blocks[item["name"]]
        ledger["actions"].append(
            {
                "action_id": f"C6-R{item['sequence']}-retire-{item['name'].replace('_', '-')}",
                "sequence": item["sequence"],
                "state": "executed",
                "action": "retire_redundant_authored_fixture_witness",
                "semantic_relation": "fixture_witness_subsumed_or_rebound_to_quantified_results_and_independent_consumer",
                "module_path": item["module"],
                "baseline_module_sha256": sha256(module_bytes),
                "retired_theorem_id": theorem_id,
                "replacement_theorem_id": None,
                "retired_block_sha256": source["block_sha256"],
                "replacement_block_sha256": None,
                "retired_statement_sha256": source["statement_sha256"],
                "replacement_statement_sha256": None,
                "semantic_basis": item["semantic_basis"],
                "dependency_check": {
                    "same_module": True,
                    "retired_theorem_dependency_refs": [],
                    "retired_theorem_consumer_refs": [],
                    "current_fully_qualified_consumer_refs": [],
                },
                "target_migrations": [],
                "maximum_inference_preserved": item["maximum_inference"],
                "validation_refs": [
                    "scripts/validate_proof_semantic_rationalization_ledger.py",
                    "scripts/validate_proof_semantic_depth_overlay.py",
                    *item["replacement_refs"],
                    "lean:lake-build",
                ],
                "support_state_effect": "none",
            }
        )
    ledger["summary"].update(
        {
            "executed_retirement_count": 106,
            "executed_scope_rewrite_count": 2,
            "current_live_theorem_count": 1270,
            "remaining_action_count": 52,
            "remaining_action_counts": {
                "retire_without_replacement": 51,
                "rewrite_as_inverse_route_property": 1,
            },
        }
    )
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")

    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    for item in RETIREMENTS:
        theorem_id = f"{item['module']}::{item['name']}"
        row = reviews["theorem_reviews"][theorem_id]
        row["review_state"] = "terminally_dispositioned"
        row["disposition"] = "retire_projection_or_assumption_restatement"
        row["replacement_refs"] = list(
            dict.fromkeys([*row.get("replacement_refs", []), *item["replacement_refs"]])
        )
        row["runtime_consumer_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("runtime_consumer_refs", []),
                    *[ref for ref in item["replacement_refs"] if ref.startswith("scripts/")],
                ]
            )
        )
        row["review_rationale"] = (
            "Declaration physically retired: the authored fixture witness had no Lean "
            "dependency or theorem consumer and is subsumed or honestly split between "
            "retained quantified consequences and an independent executable consumer."
        )
        target = reviews["target_reviews"][item["target_ref"].removeprefix("proof-target:")]
        target["replacement_refs"] = list(
            dict.fromkeys([*target.get("replacement_refs", []), *item["replacement_refs"]])
        )
        target["review_rationale"] = (
            "Public target remains implemented by retained quantified route/rejection "
            "theorems plus an independent executable consumer; the literal fixture witness "
            "is no longer counted as formal evidence."
        )
    REVIEWS.write_text(json.dumps(reviews, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    update_circle_target()
    update_ledger_and_reviews()
    print("Recorded C6 actions 107-108 and retired two authored fixture witnesses.")


if __name__ == "__main__":
    main()
