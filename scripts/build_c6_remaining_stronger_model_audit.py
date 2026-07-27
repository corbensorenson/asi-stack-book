#!/usr/bin/env python3
"""Build the terminal triage of C6's remaining stronger-model actions."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "proofs/proof_semantic_depth_overlay.json"
BASELINE_COMMIT = "9349d519130f37c86f319cd94147e57e3848b819"
OUT = ROOT / "proofs/c6_remaining_stronger_model_audit.json"
DOC = ROOT / "docs/c6_remaining_stronger_model_audit_2026_07_26.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_overlay_bytes() -> bytes:
    return subprocess.run(
        ["git", "show", f"{BASELINE_COMMIT}:proofs/proof_semantic_depth_overlay.json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def disposition(row: dict) -> tuple[str, str, str, int]:
    module = row["module_path"]
    name = row["name"]
    if module.endswith("/FailureModes.lean"):
        return (
            "rewrite_as_inverse_route_property",
            (
                "Replace the authored all-green witness with an input-general inverse: "
                "if FailureRecurrenceRouteFor returns closeFailureRecord, every earlier "
                "required field and non-claim boundary must have passed."
            ),
            "retain_target_after_proposition_rewrite_and_consumer_review",
            4,
        )
    if module.endswith("/LivingBook.lean"):
        return (
            "retire_redundant_fixture_witness",
            (
                "The exact blocked fixture is subsumed by the adjacent universal theorem "
                "that any locally complete candidate with incomplete accessibility review "
                "routes to accessibility review."
            ),
            "rebind_to_existing_universal_route_theorem",
            1,
        )
    if module.endswith("/TheseusReference.lean"):
        return (
            "retire_repository_fixture_mirror",
            (
                "The declaration proves a hand-authored sanitized import summary. Preserve "
                "the independent repository validator and immutable import result, but remove "
                "the copied Lean mirror and its formal-target status."
            ),
            "remove_lean_mirror_keep_executable_import_claim",
            2,
        )
    if module.endswith("/ProofCarryingContracts.lean"):
        return (
            "retire_redundant_fixture_witness",
            (
                "The accepted fixture is literal field construction. Retain the quantified "
                "overclaim and missing-control rejection theorems plus the independent replay "
                "validator; no replacement positive theorem is needed."
            ),
            "rebind_to_retained_rejection_family_and_executable_replay",
            1,
        )
    return (
        "retire_summary_fixture_mirror",
        (
            "The declaration normalizes a hand-authored Boolean/count summary. Preserve the "
            "independent executable result and any reachable route or counterexample family; "
            "do not replace the mirror with another copied summary theorem."
        ),
        "remove_lean_mirror_keep_executable_and_route_evidence_separate",
        3,
    )


def build() -> tuple[dict, str]:
    overlay_bytes = baseline_overlay_bytes()
    overlay = json.loads(overlay_bytes)
    pending = [
        row
        for row in overlay["records"]
        if row["disposition"] == "rewrite_with_stronger_model"
    ]
    if len(pending) != 54:
        raise SystemExit(f"expected 54 stronger-model actions, found {len(pending)}")
    records = []
    for row in pending:
        action, rationale, target_treatment, tranche = disposition(row)
        theorem_dependencies = row.get("theorem_dependency_refs", [])
        theorem_consumers = row.get("theorem_consumer_refs", [])
        if theorem_dependencies or theorem_consumers:
            raise SystemExit(f"action is no longer dependency-free: {row['theorem_id']}")
        executable_refs = sorted(
            {
                ref
                for ref in row.get("consumer_refs", [])
                if ref.startswith("scripts/") or ref.startswith("experiments/")
            }
        )
        records.append(
            {
                "theorem_id": row["theorem_id"],
                "module_path": row["module_path"],
                "name": row["name"],
                "semantic_owner_ids": row["semantic_owner_ids"],
                "current_semantic_level": row["semantic_level"],
                "current_syntax_depth_class": row["syntax_depth_class"],
                "theorem_dependency_refs": theorem_dependencies,
                "theorem_consumer_refs": theorem_consumers,
                "executable_or_result_refs": executable_refs,
                "current_maximum_inference": row["maximum_inference"],
                "recommended_action": action,
                "recommended_action_rationale": rationale,
                "target_treatment": target_treatment,
                "execution_tranche": tranche,
                "new_formal_claim_required": action == "rewrite_as_inverse_route_property",
                "support_state_effect": "none",
            }
        )
    records.sort(key=lambda row: (row["execution_tranche"], row["theorem_id"]))
    actions = Counter(row["recommended_action"] for row in records)
    modules = Counter(row["module_path"] for row in records)
    retire_count = sum(
        count for action, count in actions.items() if action.startswith("retire_")
    )
    rewrite_count = actions["rewrite_as_inverse_route_property"]
    record = {
        "schema_version": "asi_stack.c6_remaining_stronger_model_audit.v1",
        "as_of": "2026-07-26",
        "state": "terminal_triage_execution_pending",
        "roadmap_lane": "C6-P0-P6-semantic-proof-rationalization",
        "source_overlay": {
            "commit": BASELINE_COMMIT,
            "path": OVERLAY.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(overlay_bytes).hexdigest(),
            "live_theorem_count": overlay["summary"]["current_theorem_count"],
            "pending_stronger_model_count": len(pending),
        },
        "decision_policy": {
            "fixture_or_summary_literal_is_formal_evidence": False,
            "executable_validator_becomes_lean_proof": False,
            "retirement_requires_no_lean_dependency_or_theorem_consumer": True,
            "replacement_theorem_requires_reachable_consumer_or_smallest_shared_conclusion": True,
            "historical_results_remain_immutable": True,
            "support_moves_from_rationalization": False,
        },
        "summary": {
            "record_count": len(records),
            "retire_without_replacement_count": retire_count,
            "rewrite_as_inverse_route_property_count": rewrite_count,
            "module_count": len(modules),
            "action_counts": dict(sorted(actions.items())),
            "module_counts": dict(sorted(modules.items())),
            "theorem_dependency_count": 0,
            "theorem_consumer_count": 0,
            "new_formal_claim_count": rewrite_count,
        },
        "execution_order": [
            {
                "tranche": 1,
                "scope": "Unambiguously redundant Living Book and Circle fixture witnesses",
                "rule": "Retire only after rebinding to already retained universal/rejection theorems and independent consumers.",
            },
            {
                "tranche": 2,
                "scope": "Forty-three Theseus repository-import mirror declarations",
                "rule": "Remove copied Lean summaries and nine formal mirror targets while preserving immutable import results and executable validators.",
            },
            {
                "tranche": 3,
                "scope": "Benchmark, Runtime Adapter, Search Substrate, and Stable Capability Field summary mirrors",
                "rule": "Retain route theorems and executable results as separate evidence surfaces; add no replacement summary theorem.",
            },
            {
                "tranche": 4,
                "scope": "Failure Modes close-record witness",
                "rule": "Prove only the inverse route property consumed by the failure-record lifecycle; retire the authored all-green fixture.",
            },
        ],
        "records": records,
        "non_claims": [
            "This audit does not itself retire a theorem or change a proof target.",
            "An executable validator is not a Lean proof and a Lean theorem is not empirical evidence.",
            "Dependency-free means no current Lean dependency or theorem consumer, not that the surrounding idea is unimportant.",
            "Rationalization moves no chapter-core support, release state, empirical result, SOTA claim, AGI claim, or ASI claim.",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
    }
    lines = [
        "# C6 Remaining Stronger-Model Audit",
        "",
        "Date: 2026-07-26  ",
        "State: **terminal triage; dependency-safe execution pending**",
        "",
        "## Decision",
        "",
        (
            "All 54 remaining stronger-model actions were traced against the current "
            "semantic overlay. None has a Lean dependency or theorem consumer. Fifty-three "
            "are fixture or summary mirrors and should be retired without replacement; one "
            "Failure Modes witness should become a single input-general inverse route property."
        ),
        "",
        "This is proof reduction, not evidence destruction. Independent executable validators, "
        "immutable results, and retained reachable route or rejection families remain at their "
        "own scopes. They are not relabeled as Lean proofs.",
        "",
        "## Disposition totals",
        "",
        f"- Current live theorem estate: {overlay['summary']['current_theorem_count']}",
        f"- Pending stronger-model actions audited: {len(records)}",
        f"- Retire without replacement: {retire_count}",
        f"- Rewrite as one inverse route property: {rewrite_count}",
        f"- Lean dependencies: 0",
        f"- Theorem consumers: 0",
        f"- Support or release movement: none",
        "",
        "## Execution order",
        "",
    ]
    for item in record["execution_order"]:
        lines.append(
            f"{item['tranche']}. **{item['scope']}.** {item['rule']}"
        )
    lines.extend(
        [
            "",
            "## Module inventory",
            "",
            "| Module | Actions |",
            "|---|---:|",
        ]
    )
    for module, count in sorted(modules.items()):
        lines.append(f"| `{module}` | {count} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "The audit creates no formal or empirical result. Physical retirement must still "
            "update each public target, validator, chapter surface, manifest, overlay, and "
            "cumulative ledger together, pass Lean and mutation checks, and preserve historical "
            "artifacts unchanged.",
            "",
        ]
    )
    return record, "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record, doc = build()
    serialized = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        OUT.write_text(serialized, encoding="utf-8")
        DOC.write_text(doc, encoding="utf-8")
        print("Wrote C6 remaining stronger-model audit: 54 actions, 53 retire, 1 rewrite.")
        return
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != serialized:
        raise SystemExit("C6 stronger-model audit JSON is stale; run with --write")
    if not DOC.exists() or DOC.read_text(encoding="utf-8") != doc:
        raise SystemExit("C6 stronger-model audit report is stale; run with --write")
    print("C6 remaining stronger-model audit is current.")


if __name__ == "__main__":
    main()
