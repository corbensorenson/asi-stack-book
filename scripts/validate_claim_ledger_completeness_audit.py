#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "claim_ledger_completeness" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "claim_ledger_completeness_audit.md"
APPENDIX_C = ROOT / "appendices" / "C_claim_evidence_matrix.qmd"
CHAPTER = ROOT / "chapters" / "evidence-states-and-claim-discipline.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "evidence-states-and-claim-discipline.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "EvidenceStates.lean"

COMMAND = "python3 scripts/validate_claim_ledger_completeness_audit.py"
PROOF_TAG = "lean:evidence.claim_ledger.completeness_audit_bridge"
CODEX_TEST_NAME = "Claim ledger completeness audit"
REQUIRED_THEOREMS = ["claim_ledger_completeness_audit_bridge"]
REQUIRED_NON_CLAIMS = [
    "does not prove claim truth",
    "does not prove source interpretation",
    "does not prove promotion readiness",
    "does not create a support-state transition",
    "does not promote chapter core claims",
    "does not prove external review quality",
]

ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|")
FORBIDDEN_APPENDIX_PHRASES = [
    "automatically promotes",
    "promotion is guaranteed",
    "now source-derived",
    "now prototype-backed",
    "now synthetic-test-backed",
    "now empirical-test-backed",
    "now external-literature-backed",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Claim ledger completeness audit validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def strip_ticks(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def parse_appendix_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(APPENDIX_C.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        if not ROW_RE.match(line.strip()):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 11:
            rows.append(
                {
                    "line_number": line_number,
                    "parse_error": f"expected 11 cells, found {len(cells)}",
                    "raw": line,
                }
            )
            continue
        rows.append(
            {
                "line_number": line_number,
                "claim_id": strip_ticks(cells[0]),
                "chapter_id": strip_ticks(cells[1]),
                "claim": cells[2],
                "claim_label": cells[3],
                "support_state": cells[4],
                "assigned_sources": cells[5],
                "current_evidence": cells[6],
                "source_note_chapter_mapping": cells[7],
                "claim_source_mapping": cells[8],
                "open_gap": cells[9],
                "promotion_path": cells[10],
            }
        )
    return rows


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_rows(
    chapters: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    appendix_text: str,
) -> list[str]:
    errors: list[str] = []
    chapters_by_id = {str(chapter.get("id")): chapter for chapter in chapters}
    rows_by_claim: dict[str, dict[str, Any]] = {}
    claim_counts = Counter(str(row.get("claim_id", "")) for row in rows if "claim_id" in row)

    for row in rows:
        if "parse_error" in row:
            errors.append(f"Appendix C line {row['line_number']}: {row['parse_error']}")
            continue
        claim_id = str(row.get("claim_id", ""))
        chapter_id = str(row.get("chapter_id", ""))
        if claim_counts[claim_id] > 1:
            errors.append(f"{claim_id}: duplicate Appendix C claim row.")
        rows_by_claim[claim_id] = row
        if chapter_id not in chapters_by_id:
            errors.append(f"{claim_id}: unknown chapter_id {chapter_id!r}.")
            continue
        expected_claim_id = f"{chapter_id}.core"
        if claim_id != expected_claim_id:
            errors.append(f"{claim_id}: expected claim_id {expected_claim_id!r}.")

    expected_claim_ids = {f"{chapter_id}.core" for chapter_id in chapters_by_id}
    present_claim_ids = set(rows_by_claim)
    for claim_id in sorted(expected_claim_ids - present_claim_ids):
        errors.append(f"{claim_id}: missing Appendix C core claim row.")
    for claim_id in sorted(present_claim_ids - expected_claim_ids):
        errors.append(f"{claim_id}: stale or unknown Appendix C claim row.")

    for chapter in chapters:
        chapter_id = str(chapter.get("id"))
        claim_id = f"{chapter_id}.core"
        row = rows_by_claim.get(claim_id)
        if row is None:
            continue
        if row.get("claim") != chapter.get("core_claim"):
            errors.append(f"{claim_id}: claim text does not match book_structure.json.")
        if row.get("claim_label") != chapter.get("claim_label"):
            errors.append(f"{claim_id}: claim label does not match book_structure.json.")
        if row.get("support_state") != chapter.get("evidence_level"):
            errors.append(f"{claim_id}: support state does not match book_structure.json.")
        if row.get("support_state") != "argument":
            errors.append(f"{claim_id}: chapter core support state must remain argument for this audit.")

        assigned_sources = str(row.get("assigned_sources", ""))
        for source_id in chapter.get("source_ids", []):
            if f"`{source_id}`" not in assigned_sources:
                errors.append(f"{claim_id}: assigned source {source_id!r} missing from Appendix C.")

        for key in (
            "current_evidence",
            "source_note_chapter_mapping",
            "claim_source_mapping",
            "open_gap",
            "promotion_path",
        ):
            if not nonempty(row.get(key)):
                errors.append(f"{claim_id}: {key} is empty.")
    required_fragments = [
        f"Current generated coverage: {len(chapters)} chapter core claims",
        f"{len(chapters)} reviewer-facing promotion-path rows",
        "They do not promote any chapter core claim above `argument`.",
    ]
    for fragment in required_fragments:
        if fragment not in appendix_text:
            errors.append(f"Appendix C missing coverage fragment: {fragment}")
    lowered = appendix_text.lower()
    for forbidden in FORBIDDEN_APPENDIX_PHRASES:
        if forbidden in lowered:
            errors.append(f"Appendix C contains forbidden promotion overclaim: {forbidden}")

    return errors


def mutation_controls(chapters: list[dict[str, Any]], rows: list[dict[str, Any]], appendix_text: str) -> dict[str, bool]:
    controls: dict[str, bool] = {}
    if not rows:
        return {
            "missing_row_rejected": False,
            "duplicate_row_rejected": False,
            "unknown_row_rejected": False,
            "claim_label_mismatch_rejected": False,
            "support_state_mismatch_rejected": False,
            "missing_open_gap_rejected": False,
            "missing_promotion_path_rejected": False,
        }

    first = deepcopy(rows[0])
    rows_without_first = deepcopy(rows[1:])
    controls["missing_row_rejected"] = bool(validate_rows(chapters, rows_without_first, appendix_text))

    duplicate_rows = deepcopy(rows)
    duplicate_rows.append(deepcopy(first))
    controls["duplicate_row_rejected"] = bool(validate_rows(chapters, duplicate_rows, appendix_text))

    unknown_rows = deepcopy(rows)
    unknown = deepcopy(first)
    unknown["claim_id"] = "unknown-chapter.core"
    unknown["chapter_id"] = "unknown-chapter"
    unknown_rows.append(unknown)
    controls["unknown_row_rejected"] = bool(validate_rows(chapters, unknown_rows, appendix_text))

    label_rows = deepcopy(rows)
    label_rows[0]["claim_label"] = "Demonstrated"
    controls["claim_label_mismatch_rejected"] = bool(validate_rows(chapters, label_rows, appendix_text))

    support_rows = deepcopy(rows)
    support_rows[0]["support_state"] = "synthetic-test-backed"
    controls["support_state_mismatch_rejected"] = bool(validate_rows(chapters, support_rows, appendix_text))

    open_gap_rows = deepcopy(rows)
    open_gap_rows[0]["open_gap"] = ""
    controls["missing_open_gap_rejected"] = bool(validate_rows(chapters, open_gap_rows, appendix_text))

    promotion_rows = deepcopy(rows)
    promotion_rows[0]["promotion_path"] = ""
    controls["missing_promotion_path_rejected"] = bool(validate_rows(chapters, promotion_rows, appendix_text))

    return controls


def build_expected_result(
    chapters: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    controls: dict[str, bool],
) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.claim_ledger_completeness_audit.v0",
        "result_id": "2026-07-02-claim-ledger-completeness-audit",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "real_appendix_c_claim_ledger_completeness_audit",
        "manifest_chapter_core_claim_count": len(chapters),
        "appendix_c_core_claim_row_count": len(rows),
        "expected_invalid_mutation_control_count": len(controls),
        "negative_controls": controls,
        "coverage": {
            "manifest_claims_covered": len(rows) == len(chapters),
            "appendix_rows_unique": len({row.get("claim_id") for row in rows}) == len(rows),
            "claim_labels_match_manifest": True,
            "support_states_match_manifest": True,
            "open_gaps_present": True,
            "promotion_paths_present": True,
            "assigned_sources_present": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.EvidenceStates",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "manifest_claims_covered": True,
                "appendix_rows_unique": True,
                "label_support_matched": True,
                "open_gap_present": True,
                "promotion_path_present": True,
                "negative_controls_rejected": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Appendix C completeness audit only; claim truth, source interpretation, promotion readiness, and external review quality remain outside this result.",
            "Every chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "evidence-states-and-claim-discipline":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Evidence States chapter.")
        return
    if CODEX_TEST_NAME.lower() not in text_blob(chapter.get("codex_tests", [])):
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "manifestClaimsCovered",
        "appendixRowsUnique",
        "labelSupportMatched",
        "openGapPresent",
        "promotionPathPresent",
        "negativeControlsRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Claim Ledger Completeness Audit",
            rel(RESULT),
            "44 manifest chapter core claims",
            "seven expected-invalid mutation controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Claim ledger completeness audit",
            rel(RESULT),
            "44 manifest chapter core claims",
            "seven expected-invalid mutation controls",
        ],
        READER: [
            "claim ledger completeness audit",
            "44 core claim rows",
            "not a truth audit",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Claim ledger completeness audit",
            "real Appendix C audit",
            "no support-state promotion",
        ],
        CHANGELOG: ["Claim ledger completeness audit", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_claim_ledger_completeness_audit.py",
            "docs/claim_ledger_completeness_audit.md",
            "experiments/claim_ledger_completeness/results/2026-07-02-local.json",
            'run_validator("validate_claim_ledger_completeness_audit.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required claim ledger completeness surface {rel(path)}.")
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
        for phrase in phrases:
            if re.sub(r"\s+", " ", phrase).lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    structure = load_json(MANIFEST)
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    appendix_text = APPENDIX_C.read_text(encoding="utf-8", errors="ignore")
    rows = parse_appendix_rows()
    errors.extend(validate_rows(chapters, rows, appendix_text))
    controls = mutation_controls(chapters, rows, appendix_text)
    if len(controls) != 7:
        errors.append("Expected exactly seven expected-invalid mutation controls.")
    for name, rejected in controls.items():
        if not rejected:
            errors.append(f"{name}: expected-invalid mutation control unexpectedly passed.")

    expected = build_expected_result(chapters, rows, controls)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Claim ledger completeness audit validation passed.")


if __name__ == "__main__":
    main()
