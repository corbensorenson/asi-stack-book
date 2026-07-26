#!/usr/bin/env python3
"""Record and project the C6 Evidence States semantic consolidation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from build_proof_rationalization_registry import normalize
from build_proof_semantic_depth_overlay import statement_key


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "proofs/proof_semantic_rationalization_ledger.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MANIFEST = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs/book_outline.md"
TRIAGE = ROOT / "proofs/proof_triage.json"
MODULE = "lean/AsiStackProofs/EvidenceStates.lean"
REFINEMENT = "lean/AsiStackProofs/EvidenceTransitionRefinement.lean"
VALIDATOR = "scripts/validate_evidence_transition_refinement.py"
RESULT = "experiments/evidence_transition_refinement/results/2026-07-26-local.json"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)

NAMES = [
    "no_requested_transition_allows_no_change",
    "missing_claim_record_rejects_evidence_transition",
    "missing_scope_boundary_requests_scope_boundary",
    "missing_support_state_effect_requests_effect_record",
    "mismatched_support_state_effect_blocks_transition",
    "upward_transition_without_review_requests_review",
    "source_derived_without_source_note_requests_required_evidence",
    "synthetic_test_backed_without_test_run_requests_required_evidence",
    "downward_transition_without_negative_evidence_requests_negative_evidence",
    "downward_transition_without_trigger_requests_downgrade_trigger",
    "terminal_refutation_with_wrong_effect_requests_terminal_effect",
    "terminal_refutation_without_negative_evidence_requests_negative_evidence",
    "terminal_refutation_without_changelog_requests_changelog",
    "transition_without_nonclaims_preserves_nonclaim_boundary",
    "complete_synthetic_test_backed_transition_accepts",
    "claim_state_transition_bridge_fixture_valid",
]

NEW_TARGETS = [
    {
        "tag": "lean:evidence.support_state.operational_invariant",
        "module": "AsiStackProofs.EvidenceTransitionRefinement",
        "target": (
            "A reachable lifecycle freezes exact atom and proposition/obligation/predicate "
            "projections, derives non-aggregating target evidence, preserves negative "
            "evidence and non-claims, and cannot assign support, move related claims, or "
            "create external effects."
        ),
        "status": "implemented",
    },
    {
        "tag": "lean:evidence.support_state.failure_blocks_promotion",
        "module": "AsiStackProofs.EvidenceStates",
        "target": "A claim cannot be promoted when required evidence is absent.",
        "status": "implemented",
    },
    {
        "tag": "lean:evidence.support_state.transition_lifecycle_route",
        "module": "AsiStackProofs.EvidenceTransitionRefinement",
        "target": (
            "Six reachable stages preserve three claim projections and route "
            "state-specific evidence, adverse-transition, review, decision, handoff, "
            "replay, substitution, and authority failures to explicit outcomes; an "
            "independent consumer reaches every declared route."
        ),
        "status": "implemented",
    },
]

OLD_TARGET_TEXTS = {
    "lean:evidence.support_state.operational_invariant": (
        "A reachable evidence-admission model derives state-specific artifact requirements "
        "from the requested support state and inspected evidence bundle rather than "
        "assuming the RequiredEvidence predicate."
    ),
    "lean:evidence.support_state.transition_lifecycle_route": (
        "A modeled support-state transition routes no-change requests, missing records, "
        "scope gaps, support-effect gaps, missing review, missing required evidence, "
        "terminal/downgrade gaps, changelog gaps, and missing non-claim boundaries to "
        "explicit outcomes."
    ),
    "lean:evidence.bundle.completeness_probe_bridge": (
        "An independently implemented formal bridge derives the evidence-bundle probe's "
        "accepted and rejected outcomes from exact bundle inputs and audit logic rather "
        "than assuming a valid summary predicate."
    ),
    "lean:evidence.claim_ledger.completeness_audit_bridge": (
        "An independently implemented formal bridge derives claim-ledger completeness and "
        "rejection outcomes from exact manifest and Appendix C inputs rather than assuming "
        "a valid summary predicate."
    ),
    "lean:evidence.accepted_transition.review_audit_bridge": (
        "An independently implemented formal bridge derives accepted-transition audit "
        "outcomes from exact transition, no-promotion, changelog, and evidence inputs "
        "rather than assuming a valid summary predicate."
    ),
    "lean:evidence.claim_state.transition_bridge": (
        "A reachable claim-state lifecycle model derives negative-evidence, no-live-movement, "
        "and non-claim conclusions from narrowing, downgrade, and refutation cases rather "
        "than projecting fields from a hand-authored summary predicate."
    ),
}


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def blocks(text: str) -> dict[str, dict[str, str]]:
    declarations = list(DECL_START.finditer(text))
    result: dict[str, dict[str, str]] = {}
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


def git_show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def update_manifest() -> None:
    data = json.loads(MANIFEST.read_text())
    chapter = next(
        chapter
        for part in data["parts"]
        for chapter in part["chapters"]
        if chapter["id"] == "evidence-states-and-claim-discipline"
    )
    chapter["proof_targets"] = NEW_TARGETS
    for test in chapter["codex_tests"]:
        if test["name"] == "Evidence transition lifecycle route":
            test.update(
                {
                    "name": "Projection-aware evidence-transition refinement",
                    "purpose": (
                        "Check a six-stage reachable lifecycle for exact atom and three "
                        "claim-projection bindings, non-aggregating target evidence, "
                        "adverse-transition burden, review, decision, ledger handoff, "
                        "acknowledgment, replay, substitution, and authority boundaries."
                    ),
                    "implementation_status": "implemented",
                    "result_status": (
                        f"validated locally at {RESULT}; all 35 declared routes reached "
                        "by an independent consumer; support, inheritance, and external "
                        "effect none"
                    ),
                    "status": (
                        "implemented by reachable Lean refinement and independent Python "
                        "consumer; no evidence truth, live support movement, inherited "
                        "movement, release decision, or external effect"
                    ),
                }
            )
        elif test["name"] in {
            "Evidence bundle completeness and changelog-consistency probe",
            "Claim ledger completeness audit",
            "Accepted live transition review audit",
            "Claim-state transition bridge",
        }:
            test["result_status"] = re.sub(
                r"; (?:executable|three historical).*",
                "",
                test["result_status"],
            )
            test["result_status"] += (
                "; bounded executable consumer retained at its recorded scope; no generic "
                "Lean mirror or support-state movement claim"
            )
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    triage = json.loads(TRIAGE.read_text())
    kept = [
        row
        for row in triage["records"]
        if row["chapter_id"] != "evidence-states-and-claim-discipline"
    ]
    prior = {
        row["tag"]: row
        for row in triage["records"]
        if row["chapter_id"] == "evidence-states-and-claim-discipline"
    }
    replacements = []
    for target in NEW_TARGETS:
        row = prior[target["tag"]]
        row.update(
            {
                "module": target["module"],
                "formal_target": target["target"],
                "target_status": target["status"],
                "triage": "formal-invariant",
                "recommended_route": "lean-candidate",
                "rationale": (
                    "Implemented by the projection-aware reachable lifecycle and "
                    "independent all-route consumer; the foundational blocker remains "
                    "a narrow deductive fact. No evidence truth or support movement follows."
                ),
            }
        )
        replacements.append(row)
    insertion = next(
        index
        for index, row in enumerate(triage["records"])
        if row["chapter_id"] == "evidence-states-and-claim-discipline"
    )
    triage["records"] = kept[:insertion] + replacements + kept[insertion:]
    triage["record_count"] = len(triage["records"])
    TRIAGE.write_text(json.dumps(triage, indent=2, ensure_ascii=False) + "\n")


def update_outline() -> None:
    text = OUTLINE.read_text()
    start = text.index("### Evidence States and Claim Discipline")
    end = text.index("\n### Scalable Oversight and Adversarial AI Control", start)
    section = text[start:end]
    proof_start = section.index("Lean proof targets:")
    table_start = section.index("| Tag | Lean module | Formal target | Status |", proof_start)
    table_end = section.find("\n\n", table_start)
    if table_end == -1:
        table_end = len(section)
    table = "\n".join(
        [
            "| Tag | Lean module | Formal target | Status |",
            "|---|---|---|---|",
            *[
                f"| `{row['tag']}` | `{row['module']}` | {row['target']} | {row['status']} |"
                for row in NEW_TARGETS
            ],
        ]
    )
    section = section[:table_start] + table + section[table_end:]
    section = section.replace(
        "Implemented Lean proof target: finite evidence-transition lifecycle routing sends "
        "no-change requests, missing claim records, scope-boundary gaps, support-effect gaps, "
        "support-effect mismatches, review gaps, missing required evidence, missing negative "
        "evidence, downgrade-trigger gaps, terminal-effect mismatches, missing changelog refs, "
        "and missing non-claim boundaries to explicit modeled outcomes.",
        "Implemented Lean and executable refinement: six reachable stages freeze exact atom "
        "and proposition/obligation/predicate projections, derive target-specific evidence, "
        "carry adverse-transition and review duties, and hand a bounded recommendation to the "
        "claim ledger; all 35 routes are independently exercised with no support, inherited-"
        "movement, release, or external-effect authority.",
    )
    text = text[:start] + section + text[end:]
    OUTLINE.write_text(text)


def update_ledger_and_reviews() -> None:
    ledger = json.loads(LEDGER.read_text())
    ledger["actions"] = [row for row in ledger["actions"] if row["sequence"] < 91]
    baseline_commit = ledger["classification_baseline"]["commit"]
    module_bytes = git_show(baseline_commit, MODULE)
    baseline_blocks = blocks(module_bytes.decode())
    overlay = json.loads(
        git_show(baseline_commit, ledger["classification_baseline"]["overlay_path"])
    )
    overlay_rows = {row["theorem_id"]: row for row in overlay["records"]}
    module_sha = sha256(module_bytes)
    consumer_paths = [
        "book_structure.json",
        "docs/book_outline.md",
        "chapters/evidence-states-and-claim-discipline.qmd",
        "proofs/proof_manifest.json",
        "proofs/proof_triage.json",
    ]
    migrations = []
    new_text = {
        row["tag"]: row["target"]
        for row in NEW_TARGETS
    }
    for tag, old in OLD_TARGET_TEXTS.items():
        destination = (
            "lean:evidence.support_state.operational_invariant"
            if tag == "lean:evidence.support_state.operational_invariant"
            else "lean:evidence.support_state.transition_lifecycle_route"
        )
        migrations.append(
            {
                "target_ref": f"proof-target:{tag}",
                "old_target_text": old,
                "new_target_text": new_text[destination],
                "consumer_paths": consumer_paths,
            }
        )
    for sequence, name in enumerate(NAMES, start=91):
        theorem_id = f"{MODULE}::{name}"
        source = baseline_blocks[name]
        baseline_row = overlay_rows[theorem_id]
        ledger["actions"].append(
            {
                "action_id": f"C6-R{sequence}-evidence-{name.replace('_', '-')}",
                "sequence": sequence,
                "state": "executed",
                "action": "retire_legacy_fixture_theorem_after_reachable_refinement_rebinding",
                "semantic_relation": (
                    "legacy_fixture_statement_replaced_by_reachable_refinement_and_independent_consumer"
                ),
                "module_path": MODULE,
                "baseline_module_sha256": module_sha,
                "retired_theorem_id": theorem_id,
                "replacement_theorem_id": None,
                "retired_block_sha256": source["block_sha256"],
                "replacement_block_sha256": None,
                "retired_statement_sha256": source["statement_sha256"],
                "replacement_statement_sha256": None,
                "semantic_basis": [
                    "The retired theorem normalizes one hand-authored review mutation or literal summary projection.",
                    "The immutable semantic overlay records no theorem dependency or exercised consumer for the declaration.",
                    "The replacement lifecycle is reachable across six stages and preserves exact atom, proposition, obligation, and predicate identities.",
                    "Target evidence is selected by category without treating heterogeneous support states as a scalar ladder.",
                    "Adverse transitions preserve negative evidence, triggers, supersession, dissent, limitations, residuals, and changelog duties.",
                    "An independent executable consumer reaches all declared routes and mutation outcomes without trusting a copied valid summary.",
                    "The lifecycle emits only a bounded ledger handoff and has no support, parent, descendant, release, or external-effect authority.",
                ],
                "dependency_check": {
                    "same_module": True,
                    "retired_theorem_dependency_refs": baseline_row.get("theorem_dependency_refs", []),
                    "retired_theorem_consumer_refs": baseline_row.get("theorem_consumer_refs", []),
                    "current_fully_qualified_consumer_refs": [],
                },
                "target_migrations": migrations if sequence == 91 else [],
                "maximum_inference_preserved": (
                    "The replacement establishes the finite identity-bound transition-control "
                    "boundary and independent route coverage; it does not establish evidence "
                    "truth, semantic projection equivalence, reviewer independence, a correct "
                    "live decision, support movement, inheritance, release, or external effect."
                ),
                "validation_refs": [
                    "scripts/validate_proof_semantic_rationalization_ledger.py",
                    "scripts/validate_proof_semantic_depth_overlay.py",
                    VALIDATOR,
                    RESULT,
                    "lean:lake-build",
                ],
                "support_state_effect": "none",
            }
        )
    current_migration_text = {
        f"proof-target:{tag}": (
            new_text["lean:evidence.support_state.operational_invariant"]
            if tag == "lean:evidence.support_state.operational_invariant"
            else new_text["lean:evidence.support_state.transition_lifecycle_route"]
        )
        for tag in OLD_TARGET_TEXTS
    }
    for action in ledger["actions"]:
        for migration in action["target_migrations"]:
            if migration["target_ref"] in current_migration_text:
                migration["new_target_text"] = current_migration_text[migration["target_ref"]]
    ledger["summary"].update(
        {
            "executed_retirement_count": 104,
            "executed_scope_rewrite_count": 2,
            "current_live_theorem_count": 1272,
            "remaining_action_count": 54,
            "remaining_action_counts": {"rewrite_with_stronger_model": 54},
        }
    )
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")

    reviews = json.loads(REVIEWS.read_text())
    for name in NAMES:
        row = reviews["theorem_reviews"][f"{MODULE}::{name}"]
        row["review_state"] = "terminally_dispositioned"
        row["disposition"] = "replace_with_stronger_model"
        row["replacement_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("replacement_refs", []),
                    "proof-model:evidence-states.projection-aware-transition-refinement.v1",
                    REFINEMENT,
                    VALIDATOR,
                    RESULT,
                ]
            )
        )
        row["runtime_consumer_refs"] = list(
            dict.fromkeys([*row.get("runtime_consumer_refs", []), VALIDATOR])
        )
        row["review_rationale"] = (
            "Declaration physically retired: literal checklist normalization is superseded "
            "by the projection-aware reachable lifecycle and independently computed route cases."
        )
    for tag in OLD_TARGET_TEXTS:
        row = reviews["target_reviews"][tag]
        row["replacement_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("replacement_refs", []),
                    "proof-model:evidence-states.projection-aware-transition-refinement.v1",
                    REFINEMENT,
                    VALIDATOR,
                    RESULT,
                    "lean/AsiStackProofs/ClaimLedgerRefinement.lean",
                ]
            )
        )
        row["runtime_consumer_refs"] = list(
            dict.fromkeys([*row.get("runtime_consumer_refs", []), VALIDATOR])
        )
        row["semantic_role"] = (
            "Projection-aware reachable transition control plus bounded repository consumers; "
            "copied audit-summary normalization is excluded."
        )
        row["review_rationale"] = (
            "Rebound to the reachable lifecycle, independent route consumer, and existing "
            "claim-ledger lifecycle; repository-specific audits retain their executable scope."
        )
    REVIEWS.write_text(json.dumps(reviews, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    update_manifest()
    update_outline()
    update_ledger_and_reviews()
    print("Recorded 16 Evidence States retirements and consolidated seven targets to three.")


if __name__ == "__main__":
    main()
