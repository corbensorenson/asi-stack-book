#!/usr/bin/env python3
"""Execute the final nine dependency-safe C6 proof-rationalization actions."""

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
AUDIT = ROOT / "proofs/c6_remaining_stronger_model_audit.json"
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)

TARGET_REWRITES = {
    "lean:benchmarks.ratchet.fixture_bridge": {
        "old": (
            "The benchmark anti-Goodhart fixture bridge mirrors 2 valid fixtures, 5 "
            "expected-invalid controls, promotion-ready, regression-floor, missing-checks, "
            "blocked-ratchet policy, reward-as-truth, saturated-promotion, release-approval, "
            "no-support-promotion, and non-claim-boundary facts."
        ),
        "new": (
            "An independent benchmark anti-Goodhart consumer computes two valid fixtures "
            "and five rejected controls; separately, retained quantified ratchet theorems "
            "require clean transfer-or-mutation checks, negative-evidence preservation, "
            "and regression records and reject contaminated promotion. Executable totals "
            "are not imported into Lean."
        ),
        "chapter_id": "benchmark-ratchets-and-anti-goodhart-evidence",
    },
    "lean:runtime.adapters.human_oversight_degradation_fixture_bridge": {
        "old": (
            "A modeled human-oversight degradation fixture accepts scoped low-fatigue "
            "approval, routes overloaded reviewers to delay or rotation, blocks "
            "automation-bias cases, and rejects missing qualifications, rubber-stamped "
            "approvals, alarm-fatigue acceptance, support-state promotion, and missing "
            "non-claim boundaries."
        ),
        "new": (
            "An independent human-oversight consumer computes low-fatigue, overload, "
            "automation-bias, and invalid-control outcomes; separately, retained "
            "runtime-adapter route theorems govern permission, approval, lease, sandbox, "
            "rollback, receipt, and revocation boundaries. Lean does not formalize "
            "reviewer cognition or copy the consumer summary."
        ),
        "chapter_id": "runtime-adapters-tool-permissions-and-human-approval",
    },
    "lean:scf.lifecycle.trace_fixture_bridge": {
        "old": (
            "The synthetic SCF lifecycle trace summary records two valid traces, six "
            "expected-invalid controls, forward lifecycle coverage, incident quarantine "
            "coverage, unsafe-transition rejection, and no deployed-route-validation, "
            "rollback-execution, or support-state-promotion claim."
        ),
        "new": (
            "An independent SCF lifecycle consumer computes two valid traces and six "
            "rejected controls; separately, retained quantified lifecycle theorems route "
            "identity, evidence, lease, evaluator, authority, incident, transition, and "
            "retirement failures. Executable totals and no-promotion flags are not copied "
            "into Lean."
        ),
        "chapter_id": "stable-capability-fields",
    },
    "lean:failure.recurrence.escalation_route": {
        "old": (
            "Modeled failure recurrence and receipt review routes missing failure class, "
            "boundary, receipt, owner, containment, residual, learning path, normalization "
            "guard, review escalation, quarantine, evidence-transition, and non-claim-"
            "boundary records to explicit outcomes."
        ),
        "new": (
            "If the finite failure-recurrence router returns closeFailureRecord, every "
            "required failure, class, boundary, receipt, owner, containment, residual, "
            "learning, normalization, and non-claim field is true and no earlier "
            "recurrence, severe-irreversible, unreviewed-promotion, unquarantined-escape, "
            "or missing-evidence-transition branch applies."
        ),
        "chapter_id": "failure-modes-of-ungoverned-intelligence",
    },
}

TARGET_BY_MODULE = {
    "lean/AsiStackProofs/BenchmarkRatchets.lean": "lean:benchmarks.ratchet.fixture_bridge",
    "lean/AsiStackProofs/RuntimeAdapters.lean": (
        "lean:runtime.adapters.human_oversight_degradation_fixture_bridge"
    ),
    "lean/AsiStackProofs/StableCapabilityFields.lean": (
        "lean:scf.lifecycle.trace_fixture_bridge"
    ),
}


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
    rows: dict[str, dict[str, str]] = {}
    for match in THEOREM_START.finditer(text):
        end = next(
            (candidate.start() for candidate in declarations if candidate.start() > match.start()),
            len(text),
        )
        block = text[match.start():end]
        signature = normalize(block.split(":= by", 1)[0])
        rows[match.group(1)] = {
            "block_sha256": sha256(block.encode()),
            "statement_sha256": sha256(statement_key(signature).encode()),
        }
    return rows


def update_targets() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    for tag, rewrite in TARGET_REWRITES.items():
        chapter = next(
            chapter
            for part in structure["parts"]
            for chapter in part["chapters"]
            if chapter["id"] == rewrite["chapter_id"]
        )
        target = next(row for row in chapter["proof_targets"] if row["tag"] == tag)
        if target["target"] not in {rewrite["old"], rewrite["new"]}:
            raise SystemExit(f"{tag}: target text drifted")
        target["target"] = rewrite["new"]
    STRUCTURE.write_text(json.dumps(structure, indent=2, ensure_ascii=False) + "\n")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for tag, rewrite in TARGET_REWRITES.items():
        row = next(row for row in triage["records"] if row["tag"] == tag)
        row["formal_target"] = rewrite["new"]
        row["rationale"] = (
            "C6 final rationalization keeps executable outcomes separate from formal route "
            "properties and replaces the authored close-state fixture with a quantified "
            "inverse; no copied summary is counted as formal evidence."
        )
    TRIAGE.write_text(json.dumps(triage, indent=2, ensure_ascii=False) + "\n")


def action_common(
    *,
    sequence: int,
    module: str,
    retired_name: str,
    replacement_name: str | None,
) -> dict:
    baseline_module = git_show(module)
    baseline_block = theorem_blocks(baseline_module.decode())[retired_name]
    replacement_block = None
    if replacement_name is not None:
        replacement_block = theorem_blocks(
            (ROOT / module).read_text(encoding="utf-8")
        )[replacement_name]
    return {
        "sequence": sequence,
        "module_path": module,
        "baseline_module_sha256": sha256(baseline_module),
        "retired_theorem_id": f"{module}::{retired_name}",
        "replacement_theorem_id": (
            f"{module}::{replacement_name}" if replacement_name is not None else None
        ),
        "retired_block_sha256": baseline_block["block_sha256"],
        "replacement_block_sha256": (
            replacement_block["block_sha256"] if replacement_block else None
        ),
        "retired_statement_sha256": baseline_block["statement_sha256"],
        "replacement_statement_sha256": (
            replacement_block["statement_sha256"] if replacement_block else None
        ),
        "dependency_check": {
            "same_module": True,
            "retired_theorem_dependency_refs": [],
            "retired_theorem_consumer_refs": [],
            "current_fully_qualified_consumer_refs": [],
        },
        "support_state_effect": "none",
    }


def update_ledger_and_reviews() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger["actions"] = [row for row in ledger["actions"] if row["sequence"] <= 151]
    if len(ledger["actions"]) != 151:
        raise SystemExit("expected 151 executed rationalization actions before final tranche")

    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    summary_records = [
        row
        for row in audit["records"]
        if row.get("recommended_action") == "retire_summary_fixture_mirror"
    ]
    migrated_targets: set[str] = set()
    for sequence, record in enumerate(summary_records, start=152):
        theorem_id = record["theorem_id"]
        module, name = theorem_id.split("::", 1)
        common = action_common(
            sequence=sequence,
            module=module,
            retired_name=name,
            replacement_name=None,
        )
        target_tag = TARGET_BY_MODULE.get(module)
        migrations = []
        if target_tag and target_tag not in migrated_targets:
            rewrite = TARGET_REWRITES[target_tag]
            migrations = [{
                "target_ref": f"proof-target:{target_tag}",
                "old_target_text": rewrite["old"],
                "new_target_text": rewrite["new"],
                "consumer_paths": [
                    "book_structure.json",
                    "docs/book_outline.md",
                    f"chapters/{rewrite['chapter_id']}.qmd",
                    "proofs/proof_manifest.json",
                    "proofs/proof_triage.json",
                ],
            }]
            migrated_targets.add(target_tag)
        ledger["actions"].append({
            "action_id": (
                f"C6-R{sequence}-retire-summary-fixture-mirror-"
                f"{name.replace('_', '-')}"
            ),
            "state": "executed",
            "action": "retire_summary_fixture_mirror",
            "semantic_relation": (
                "summary_fixture_mirror_retired_keep_executable_and_route_evidence_separate"
            ),
            **common,
            "semantic_basis": [
                record["recommended_action_rationale"],
                "The immutable semantic audit records no Lean dependency and no theorem consumer.",
                "The independent executable validator and result remain at their exact finite scope.",
                "Retained route or rejection theorems remain separate from executable counts and flags.",
                "No replacement summary theorem, support transition, or empirical inference is created.",
            ],
            "target_migrations": migrations,
            "maximum_inference_preserved": (
                "Only the retained formal route properties and separately labeled executable "
                "fixture results survive; neither evidence surface inherits the other."
            ),
            "validation_refs": list(dict.fromkeys([
                "scripts/validate_proof_semantic_rationalization_ledger.py",
                "scripts/validate_proof_semantic_depth_overlay.py",
                "scripts/validate_c6_remaining_stronger_model_audit.py",
                *record["executable_or_result_refs"],
                "lean:lake-build",
            ])),
        })
        review = reviews["theorem_reviews"][theorem_id]
        review["disposition"] = "retire_projection_or_assumption_restatement"
        review["review_rationale"] = (
            "Declaration physically retired: it copied a hand-authored executable summary "
            "into Lean despite having no dependency or theorem consumer. The executable "
            "validator and retained route model remain separate."
        )

    failure_record = next(
        row
        for row in audit["records"]
        if row.get("recommended_action") == "rewrite_as_inverse_route_property"
    )
    module, retired_name = failure_record["theorem_id"].split("::", 1)
    replacement_name = "failure_route_close_implies_complete_required_record"
    common = action_common(
        sequence=160,
        module=module,
        retired_name=retired_name,
        replacement_name=replacement_name,
    )
    failure_target = "lean:failure.recurrence.escalation_route"
    rewrite = TARGET_REWRITES[failure_target]
    ledger["actions"].append({
        "action_id": "C6-R160-rewrite-complete-failure-record-as-inverse-route-property",
        "state": "executed",
        "action": "rewrite_as_inverse_route_property",
        "semantic_relation": "authored_fixture_witness_replaced_by_quantified_inverse_route_property",
        **common,
        "semantic_basis": [
            failure_record["recommended_action_rationale"],
            "The authored all-green constant no longer supplies the positive proof witness.",
            "The replacement quantifies over every FailureRecurrenceReview input.",
            "A close result implies all required record fields and excludes every earlier route guard.",
            "The proposition establishes only the finite router inverse and creates no runtime bridge.",
        ],
        "target_migrations": [{
            "target_ref": f"proof-target:{failure_target}",
            "old_target_text": rewrite["old"],
            "new_target_text": rewrite["new"],
            "consumer_paths": [
                "book_structure.json",
                "docs/book_outline.md",
                f"chapters/{rewrite['chapter_id']}.qmd",
                "proofs/proof_manifest.json",
                "proofs/proof_triage.json",
            ],
        }],
        "maximum_inference_preserved": (
            "The finite router cannot report close unless its required record fields pass "
            "and no earlier modeled guard applies; this does not prove runtime detection, "
            "record truth, containment effectiveness, or deployment safety."
        ),
        "validation_refs": [
            "scripts/validate_proof_semantic_rationalization_ledger.py",
            "scripts/validate_proof_semantic_depth_overlay.py",
            "scripts/validate_c6_remaining_stronger_model_audit.py",
            "scripts/validate_architecture_red_team.py",
            "lean:lake-build",
        ],
    })
    failure_review = reviews["theorem_reviews"][failure_record["theorem_id"]]
    failure_review["disposition"] = "retire_projection_or_assumption_restatement"
    failure_review["replacement_refs"] = list(dict.fromkeys([
        *failure_review.get("replacement_refs", []),
        f"{module}::{replacement_name}",
    ]))
    failure_review["review_rationale"] = (
        "The authored all-green witness is physically retired and replaced by a quantified "
        "inverse theorem over arbitrary recurrence-review inputs."
    )

    for tag, rewrite in TARGET_REWRITES.items():
        target = reviews["target_reviews"][tag]
        target["replacement_refs"] = list(dict.fromkeys([
            *target.get("replacement_refs", []),
            *(
                [f"{module}::{replacement_name}"]
                if tag == failure_target
                else []
            ),
        ]))
        target["review_rationale"] = (
            "C6 final rationalization separates executable fixture results from formal "
            "route properties; the failure close branch is now supported by a quantified "
            "inverse rather than an authored positive fixture."
        )

    ledger["summary"].update({
        "executed_retirement_count": 157,
        "executed_scope_rewrite_count": 2,
        "current_live_theorem_count": 1219,
        "remaining_action_count": 0,
        "remaining_action_counts": {
            "retire_without_replacement": 0,
            "rewrite_as_inverse_route_property": 0,
        },
        "new_formal_claims": 1,
    })
    ledger["state"] = "dependency_safe_execution_complete"
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    REVIEWS.write_text(json.dumps(reviews, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    update_targets()
    update_ledger_and_reviews()
    print("Executed C6 actions 152-160: eight mirrors retired, one inverse theorem added.")


if __name__ == "__main__":
    main()
