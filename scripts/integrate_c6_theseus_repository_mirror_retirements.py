#!/usr/bin/env python3
"""Execute C6 tranche two: retire 43 copied Project Theseus proof mirrors."""

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
AUDIT = ROOT / "proofs" / "c6_remaining_stronger_model_audit.json"
LEDGER = ROOT / "proofs" / "proof_semantic_rationalization_ledger.json"
REVIEWS = ROOT / "proofs" / "proof_rationalization_reviews.json"
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
LEAN = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
BEYOND_ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
FAST_CHAPTER = ROOT / "chapters" / "fast-generation-architectures.qmd"
FAST_READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "fast-generation-architectures.qmd"
THESEUS_READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)
MIRROR_START = "structure TheseusPublicTaskBundleImportSummary where"

TARGETS = {
    "public_task_bundle_import": "lean:theseus.reference.public_task_bundle_import.fixture_bridge",
    "fast_support_aggregate": "lean:theseus.reference.fast_support_aggregate.fixture_bridge",
    "artifact_retention_replay_import": "lean:theseus.reference.artifact_retention_replay_import.fixture_bridge",
    "module_definition_of_done_import": "lean:theseus.reference.module_definition_of_done_import.fixture_bridge",
    "project_registry_import": "lean:theseus.reference.project_registry_import.fixture_bridge",
    "assistant_reference_trace_import": "lean:theseus.reference.assistant_reference_trace_import.fixture_bridge",
    "accelerator_parity_manifest_import": "lean:theseus.reference.accelerator_parity_manifest_import.fixture_bridge",
    "book_crosswalk_import": "lean:theseus.reference.book_crosswalk.pointer_boundary",
    "work_board_import": "lean:theseus.reference.work_board_import.metadata_boundary",
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


def target_for(name: str) -> str:
    for prefix, target in TARGETS.items():
        if name.startswith(f"theseus_{prefix}"):
            return target
    raise SystemExit(f"no target mapping for {name}")


def executable_refs(records: list[dict], target: str) -> list[str]:
    refs: list[str] = []
    for record in records:
        if target_for(record["name"]) == target:
            refs.extend(record.get("executable_or_result_refs", []))
    return list(dict.fromkeys(refs))


def remove_formal_mirror_source() -> None:
    text = LEAN.read_text(encoding="utf-8")
    start = text.find(MIRROR_START)
    if start < 0:
        if any(record["name"] in text for record in retirement_records()):
            raise SystemExit("partial Theseus mirror retirement detected")
        return
    tail = text[start:]
    names = set(THEOREM_START.findall(tail))
    expected = {record["name"] for record in retirement_records()}
    if names != expected:
        raise SystemExit(f"unexpected theorem set in Theseus mirror tail: {sorted(names ^ expected)}")
    LEAN.write_text(text[:start].rstrip() + "\n\nend AsiStackProofs.TheseusReference\n", encoding="utf-8")


def retirement_records() -> list[dict]:
    value = json.loads(AUDIT.read_text(encoding="utf-8"))
    return [
        row
        for row in value["records"]
        if row.get("recommended_action") == "retire_repository_fixture_mirror"
    ]


def remove_formal_targets(records: list[dict]) -> dict[str, str]:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] == "project-theseus-as-report-first-implementation-reference"
    )
    old_targets = {
        row["tag"]: row["target"]
        for row in chapter["proof_targets"]
        if row["tag"] in set(TARGETS.values())
    }
    if not old_targets:
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        old_targets = {
            migration["target_ref"].removeprefix("proof-target:"): migration["old_target_text"]
            for action in ledger["actions"]
            for migration in action.get("target_migrations", [])
            if migration["target_ref"].removeprefix("proof-target:") in set(TARGETS.values())
        }
    if set(old_targets) != set(TARGETS.values()):
        raise SystemExit("expected all nine Theseus mirror targets or their prior ledger records")
    chapter["proof_targets"] = [
        row for row in chapter["proof_targets"] if row["tag"] not in old_targets
    ]
    STRUCTURE.write_text(json.dumps(structure, indent=2, ensure_ascii=False) + "\n")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    triage["records"] = [
        row for row in triage["records"] if row["tag"] not in old_targets
    ]
    triage["record_count"] = len(triage["records"])
    TRIAGE.write_text(json.dumps(triage, indent=2, ensure_ascii=False) + "\n")

    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    for target, old_text in old_targets.items():
        row = reviews["target_reviews"][target]
        row["review_state"] = "terminally_dispositioned"
        row["disposition"] = "retire_projection_or_assumption_restatement"
        row["semantic_role"] = "Historical copied repository-import summary; executable validator remains authoritative."
        row["replacement_refs"] = list(
            dict.fromkeys(
                [
                    *row.get("replacement_refs", []),
                    *executable_refs(records, target),
                    "proofs/c6_remaining_stronger_model_audit.json",
                    "proofs/proof_semantic_rationalization_ledger.json",
                ]
            )
        )
        row["review_rationale"] = (
            "Formal target physically retired after the dependency audit found no Lean "
            "dependency or theorem consumer. The immutable result and independent executable "
            "validator preserve the bounded import claim without counting a copied summary as proof."
        )
    REVIEWS.write_text(json.dumps(reviews, indent=2, ensure_ascii=False) + "\n")
    return old_targets


def update_ledger_and_theorem_reviews(records: list[dict], old_targets: dict[str, str]) -> None:
    baseline_module = git_show("lean/AsiStackProofs/TheseusReference.lean")
    blocks = theorem_blocks(baseline_module.decode())
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger["actions"] = [row for row in ledger["actions"] if row["sequence"] <= 108]
    if len(ledger["actions"]) != 108:
        raise SystemExit("expected 108 prior C6 actions")
    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    for offset, record in enumerate(records, start=109):
        name = record["name"]
        theorem_id = record["theorem_id"]
        if record.get("theorem_dependency_refs") or record.get("theorem_consumer_refs"):
            raise SystemExit(f"retirement is no longer dependency-safe: {theorem_id}")
        source = blocks[name]
        target = target_for(name)
        refs = list(
            dict.fromkeys(
                [
                    *record.get("executable_or_result_refs", []),
                    "proofs/c6_remaining_stronger_model_audit.json",
                ]
            )
        )
        ledger["actions"].append(
            {
                "action_id": f"C6-R{offset}-retire-theseus-repository-mirror-{name.replace('_', '-')}",
                "sequence": offset,
                "state": "executed",
                "action": "retire_repository_import_fixture_mirror",
                "semantic_relation": "copied_repository_summary_rebound_to_executable_validator_and_immutable_result",
                "module_path": record["module_path"],
                "baseline_module_sha256": sha256(baseline_module),
                "retired_theorem_id": theorem_id,
                "replacement_theorem_id": None,
                "retired_block_sha256": source["block_sha256"],
                "replacement_block_sha256": None,
                "retired_statement_sha256": source["statement_sha256"],
                "replacement_statement_sha256": None,
                "semantic_basis": [
                    record["recommended_action_rationale"],
                    "The frozen audit reports zero Lean dependencies and zero theorem consumers.",
                    "The repository validator checks the source artifact, deterministic result, controls, and claim boundary directly.",
                    "The associated formal target is removed rather than pretending executable evidence is a theorem.",
                    "The historical result remains unchanged and no support-state or release transition is created.",
                ],
                "dependency_check": {
                    "same_module": True,
                    "retired_theorem_dependency_refs": [],
                    "retired_theorem_consumer_refs": [],
                    "current_fully_qualified_consumer_refs": [],
                },
                "target_migrations": [
                    {
                        "target_ref": f"proof-target:{target}",
                        "old_target_text": old_targets[target],
                        "new_target_text": (
                            "Executable-only bounded import claim; the copied formal mirror is retired."
                        ),
                        "consumer_paths": [],
                    }
                ],
                "maximum_inference_preserved": record["current_maximum_inference"],
                "validation_refs": [
                    *refs,
                    "scripts/validate_retired_theseus_formal_mirrors.py",
                    "scripts/validate_proof_semantic_rationalization_ledger.py",
                    "scripts/validate_proof_semantic_depth_overlay.py",
                    "lean:lake-build",
                ],
                "support_state_effect": "none",
            }
        )
        review = reviews["theorem_reviews"][theorem_id]
        review["review_state"] = "terminally_dispositioned"
        review["disposition"] = "retire_projection_or_assumption_restatement"
        review["replacement_refs"] = list(
            dict.fromkeys(
                [
                    *review.get("replacement_refs", []),
                    *refs,
                    "proofs/proof_semantic_rationalization_ledger.json",
                ]
            )
        )
        review["runtime_consumer_refs"] = list(
            dict.fromkeys(
                [
                    *review.get("runtime_consumer_refs", []),
                    *[ref for ref in refs if ref.startswith("scripts/")],
                ]
            )
        )
        review["review_rationale"] = (
            "Declaration physically retired: it copied a repository-import summary, had no "
            "Lean dependency or theorem consumer, and is more honestly represented by its "
            "independent executable validator plus immutable import result."
        )

    ledger["summary"].update(
        {
            "executed_retirement_count": 149,
            "executed_scope_rewrite_count": 2,
            "current_live_theorem_count": 1227,
            "remaining_action_count": 9,
            "remaining_action_counts": {
                "retire_without_replacement": 8,
                "rewrite_as_inverse_route_property": 1,
            },
        }
    )
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    REVIEWS.write_text(json.dumps(reviews, indent=2, ensure_ascii=False) + "\n")


def update_public_prose() -> None:
    retired_tags = set(TARGETS.values())
    for path in (CHAPTER, OUTLINE):
        text = path.read_text(encoding="utf-8")
        lines = [
            line
            for line in text.splitlines()
            if not any(tag in line for tag in retired_tags)
        ]
        text = "\n".join(lines) + "\n"
        text = text.replace(
            "seven expected-invalid controls, and a finite Lean bridge.",
            "seven expected-invalid controls, and an immutable executable receipt.",
        )
        text = text.replace(
            "14 expected-invalid or rejected controls, two accepted no-promotion decisions, and the aggregate Lean fixture.",
            "14 expected-invalid or rejected controls, two accepted no-promotion decisions, and an immutable aggregate receipt.",
        )
        text = text.replace(
            "; checks `theseusFastSupportAggregateFixture`;",
            "; the copied formal mirror is retired after semantic audit;",
        )
        start = text.find("These Lean hooks are implemented as finite-record predicates")
        end = text.find("### Formal-proof audit boundary", start)
        if start >= 0 and end >= 0:
            replacement = (
                "The remaining formal hooks cover three reusable boundaries: implementation-reference "
                "claims need an artifact surface, promotion needs passing gate reports, and the retained "
                "report-bundle audit enforces a bounded public bundle contract. Nine repository-import "
                "lanes remain executable evidence, not formal targets. Their validators continue to check "
                "digests, counts, redaction, negative controls, and non-promotion boundaries against "
                "immutable results. The 43 copied Lean summary theorems and their supporting mirror-only "
                "definitions were retired because they had no Lean dependencies or theorem consumers and "
                "added no fact beyond those validators.\n\n"
            )
            text = text[:start] + replacement + text[end:]
        audit_start = text.find("### Formal-proof audit boundary")
        source_start = text.find("## Source crosswalk", audit_start)
        if audit_start >= 0 and source_start >= 0:
            replacement = (
                "### Formal-proof audit boundary\n\n"
                "The module now contains eleven theorem declarations: reusable finite policy consequences "
                "for implementation-reference surfaces, gate-before-promotion, bundle completeness, replay "
                "boundaries, public-safety boundaries, and the retained report-bundle audit. The 43 "
                "repository-import summary mirrors were physically retired with nine formal targets. Their "
                "executable validators and immutable results remain available as bounded implementation "
                "evidence. This change reduces proof ceremony; it does not weaken a claimed theorem, promote "
                "support, or establish live Theseus behavior, capability, quality, safety, deployment, "
                "transfer, AGI, ASI, or SOTA.\n\n"
            )
            text = text[:audit_start] + replacement + text[source_start:]
        path.write_text(text, encoding="utf-8")

    replacements = {
        "`theseusFastSupportAggregateFixture`": "the executable aggregate receipt (copied formal mirror retired)",
        "Lean fixture the executable aggregate receipt (copied formal mirror retired)": "executable aggregate receipt (copied formal mirror retired)",
        "`lean:theseus.reference.public_task_bundle_import.fixture_bridge`": "the executable-only public-task-bundle receipt (formal mirror retired)",
        "`lean:theseus.reference.fast_support_aggregate.fixture_bridge`": "the executable-only support-aggregate receipt (formal mirror retired)",
        "`lean:theseus.reference.artifact_retention_replay_import.fixture_bridge`": "the executable-only artifact-retention receipt (formal mirror retired)",
        "`lean:theseus.reference.module_definition_of_done_import.fixture_bridge`": "the executable-only module-definition-of-done receipt (formal mirror retired)",
        "`lean:theseus.reference.project_registry_import.fixture_bridge`": "the executable-only project-registry receipt (formal mirror retired)",
        "`lean:theseus.reference.assistant_reference_trace_import.fixture_bridge`": "the executable-only assistant-reference-trace receipt (formal mirror retired)",
        "`lean:theseus.reference.accelerator_parity_manifest_import.fixture_bridge`": "the executable-only accelerator-parity receipt (formal mirror retired)",
        "`lean:theseus.reference.book_crosswalk.pointer_boundary`": "the executable-only book-crosswalk receipt (formal mirror retired)",
        "`lean:theseus.reference.work_board_import.metadata_boundary`": "the executable-only work-board receipt (formal mirror retired)",
    }
    for path in (ACTIVE_CYCLE, BEYOND_ROADMAP, FAST_CHAPTER, FAST_READER, THESEUS_READER):
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    outline = OUTLINE.read_text(encoding="utf-8")
    stale_start = outline.find(
        "Implemented negative-case theorems now cover dashboard-only implementation-reference rejection"
    )
    stale_end = outline.find("\n\n### Prototype Roadmap", stale_start)
    if stale_start >= 0 and stale_end >= 0:
        outline = (
            outline[:stale_start]
            + "The remaining formal hooks cover three reusable boundaries: implementation-reference "
            "claims need an artifact surface, promotion needs passing gate reports, and the retained "
            "report-bundle audit enforces a bounded public bundle contract. Nine repository-import "
            "lanes remain executable evidence, not formal targets. Their validators continue to check "
            "digests, counts, redaction, negative controls, and non-promotion boundaries against "
            "immutable results. The 43 copied Lean summary theorems and their supporting mirror-only "
            "definitions were retired because they had no Lean dependencies or theorem consumers and "
            "added no fact beyond those validators.\n\n"
            "These formal hooks do not prove report truth, clean live replay, current runtime state, "
            "model quality, benchmark superiority, capability, safety, deployment, transfer, AGI, "
            "ASI, or chapter-core support. They establish only the declared finite record and "
            "rejection consequences."
            + outline[stale_end:]
        )
        OUTLINE.write_text(outline, encoding="utf-8")


def main() -> None:
    records = retirement_records()
    if len(records) != 43:
        raise SystemExit(f"expected 43 repository-mirror retirements, got {len(records)}")
    old_targets = remove_formal_targets(records)
    update_ledger_and_theorem_reviews(records, old_targets)
    remove_formal_mirror_source()
    update_public_prose()
    print("Executed C6 actions 109-151: retired 43 Theseus mirrors and nine formal targets.")


if __name__ == "__main__":
    main()
