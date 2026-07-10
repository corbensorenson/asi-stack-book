#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
EVIDENCE_PLAN = ROOT / "docs" / "per_chapter_evidence_plan.md"
APPENDIX_C = ROOT / "appendices" / "C_claim_evidence_matrix.qmd"
TRANSITION_DIR = ROOT / "evidence_transitions"
NO_PROMOTION_LEDGER = ROOT / "claim_decisions" / "v1_0_core_claim_no_promotion.json"
DISPOSITION_LEDGER = ROOT / "claim_decisions" / "v1_x_core_claim_dispositions.json"
DISPOSITION_REPORT = ROOT / "docs" / "core_claim_disposition_ledger.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"

PLAN_ROW_RE = re.compile(r"^\|\s*([IVX]+)\s*\|\s*`([^`]+)`\s*\|")
APPENDIX_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|")

REQUIRED_ROADMAP_STRINGS = [
    "Every chapter core claim has an explicit disposition",
    "claim_decisions/v1_x_core_claim_dispositions.json",
    "core-claim dispositions are now recorded per chapter",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    print("v1.x core claim disposition validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(item) for item in value)


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for part_index, part in enumerate(structure.get("parts", []), start=1):
        if not isinstance(part, dict):
            continue
        part_id = str(part.get("id", ""))
        part_title = str(part.get("title", ""))
        for chapter_index, chapter in enumerate(part.get("chapters", []), start=1):
            if not isinstance(chapter, dict):
                continue
            enriched = dict(chapter)
            enriched["part_index"] = part_index
            enriched["part_id"] = part_id
            enriched["part_title"] = part_title
            enriched["chapter_index_in_part"] = chapter_index
            rows.append(enriched)
    return rows


def parse_plan_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    duplicates: set[str] = set()
    for line in EVIDENCE_PLAN.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not PLAN_ROW_RE.match(line.strip()):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            continue
        chapter_id = cells[1].strip("`")
        if chapter_id in rows:
            duplicates.add(chapter_id)
        rows[chapter_id] = {
            "part": cells[0],
            "primary_evidence_lane": cells[2],
            "formal_or_prototype_work": cells[3],
            "human_reader_focus": cells[4],
            "what_would_move_this": cells[5],
        }
    if duplicates:
        raise ValueError(f"duplicate per-chapter evidence-plan rows: {sorted(duplicates)}")
    return rows


def parse_appendix_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    duplicates: set[str] = set()
    for line_number, line in enumerate(APPENDIX_C.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        if not APPENDIX_ROW_RE.match(line.strip()):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 11:
            raise ValueError(f"{rel(APPENDIX_C)} line {line_number}: expected 11 cells, found {len(cells)}")
        claim_id = cells[0].strip("`")
        if claim_id in rows:
            duplicates.add(claim_id)
        rows[claim_id] = {
            "chapter_id": cells[1].strip("`"),
            "claim": cells[2],
            "claim_label": cells[3],
            "current_support_state": cells[4],
            "assigned_sources": cells[5],
            "current_evidence_summary": cells[6],
            "source_note_chapter_mapping": cells[7],
            "claim_source_mapping": cells[8],
            "open_gap": cells[9],
            "appendix_promotion_path": cells[10],
        }
    if duplicates:
        raise ValueError(f"duplicate Appendix C rows: {sorted(duplicates)}")
    return rows


def accepted_transitions(core_claim_ids: set[str]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    core: dict[str, dict[str, Any]] = {}
    non_core: list[dict[str, Any]] = []
    for path in sorted(TRANSITION_DIR.rglob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        if data.get("review_status") != "accepted" or data.get("transition_validity_state") != "review_accepted":
            continue
        claim_id = data.get("claim_id")
        if not isinstance(claim_id, str):
            continue
        row = dict(data)
        row["_path"] = rel(path)
        if claim_id in core_claim_ids:
            if claim_id in core:
                raise ValueError(f"duplicate accepted core transition for {claim_id}")
            core[claim_id] = row
        else:
            non_core.append(row)
    return core, non_core


def load_no_promotion_decisions() -> dict[str, dict[str, Any]]:
    ledger = load_json(NO_PROMOTION_LEDGER)
    if not isinstance(ledger, dict) or ledger.get("review_status") != "accepted":
        raise ValueError(f"{rel(NO_PROMOTION_LEDGER)} must be an accepted decision ledger")
    rows = ledger.get("decisions")
    if not isinstance(rows, list):
        raise ValueError(f"{rel(NO_PROMOTION_LEDGER)} decisions must be a list")
    decisions: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{rel(NO_PROMOTION_LEDGER)} decisions[{index}] must be an object")
        claim_id = row.get("claim_id")
        if not isinstance(claim_id, str):
            raise ValueError(f"{rel(NO_PROMOTION_LEDGER)} decisions[{index}] missing claim_id")
        if claim_id in decisions:
            raise ValueError(f"duplicate no-promotion decision for {claim_id}")
        decisions[claim_id] = row
    return decisions


def transition_refs_for_chapter(non_core_transitions: list[dict[str, Any]], chapter_file: str) -> list[str]:
    refs: list[str] = []
    for record in non_core_transitions:
        claim_id = str(record.get("claim_id", ""))
        transition_prefix = claim_id.split(".", 1)[0]
        surfaces = record.get("claim_surface_refs")
        if not isinstance(surfaces, list):
            surfaces = []
        evidence_packets = record.get("evidence_packet_refs")
        if not isinstance(evidence_packets, list):
            evidence_packets = []
        chapter_id = chapter_file.removeprefix("chapters/").removesuffix(".qmd")
        if transition_prefix and chapter_id.startswith(transition_prefix):
            refs.append(str(record.get("_path")))
        elif chapter_file in surfaces:
            refs.append(str(record.get("_path")))
        elif any(isinstance(item, str) and item == chapter_file for item in evidence_packets):
            refs.append(str(record.get("_path")))
    return sorted(set(refs))


def normalize_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if nonempty(str(item))]
    if nonempty(value):
        return [str(value)]
    return []


def build_expected() -> tuple[dict[str, Any], str, list[str]]:
    errors: list[str] = []
    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        fail([f"{rel(STRUCTURE)} must contain an object"])
    chapters = flatten_chapters(structure)
    core_claim_ids = {f"{chapter['id']}.core" for chapter in chapters}

    try:
        plan_rows = parse_plan_rows()
        appendix_rows = parse_appendix_rows()
        core_transitions, non_core_transitions = accepted_transitions(core_claim_ids)
        no_promotion = load_no_promotion_decisions()
    except ValueError as exc:
        fail([str(exc)])

    dispositions: list[dict[str, Any]] = []
    transition_count = 0
    decision_count = 0
    promoted_count = 0

    if set(plan_rows) != {str(chapter["id"]) for chapter in chapters}:
        errors.append(
            "per-chapter evidence plan must cover the active manifest chapter set exactly"
        )

    for chapter in chapters:
        chapter_id = str(chapter.get("id"))
        claim_id = f"{chapter_id}.core"
        chapter_file = str(chapter.get("file"))
        plan = plan_rows.get(chapter_id)
        appendix = appendix_rows.get(claim_id)
        if plan is None:
            errors.append(f"{chapter_id}: missing per-chapter evidence-plan row")
            continue
        if appendix is None:
            errors.append(f"{claim_id}: missing Appendix C row")
            continue
        if appendix.get("chapter_id") != chapter_id:
            errors.append(f"{claim_id}: Appendix C chapter mismatch")
        if appendix.get("claim") != chapter.get("core_claim"):
            errors.append(f"{claim_id}: Appendix C claim text mismatch")
        if appendix.get("claim_label") != chapter.get("claim_label"):
            errors.append(f"{claim_id}: Appendix C claim label mismatch")
        if appendix.get("current_support_state") != chapter.get("evidence_level"):
            errors.append(f"{claim_id}: Appendix C support state mismatch")

        transition = core_transitions.get(claim_id)
        decision = no_promotion.get(claim_id)
        if transition and decision:
            errors.append(f"{claim_id}: cannot have both accepted transition and no-promotion decision")
            continue
        if not transition and not decision:
            errors.append(f"{claim_id}: missing accepted transition or no-promotion decision")
            continue

        if transition:
            transition_count += 1
            new_state = str(transition.get("new_support_state", ""))
            if new_state != chapter.get("evidence_level"):
                errors.append(f"{claim_id}: transition support state does not match manifest")
            if new_state != "argument":
                promoted_count += 1
            disposition = {
                "disposition": "retained_at_argument_via_accepted_no_change_transition"
                if new_state == "argument"
                else "promoted_via_accepted_core_transition",
                "disposition_record_ref": str(transition.get("_path")),
                "coverage_type": "accepted_core_transition",
                "support_state_effect": str(transition.get("support_state_effect", "")),
                "required_evidence": normalize_list(transition.get("required_artifacts")),
                "blockers": normalize_list(transition.get("acceptance_blockers")),
                "promotion_burden": str(transition.get("promotion_burden", "")),
                "limitations": normalize_list(transition.get("limitations")),
                "non_claims": normalize_list(transition.get("non_claims")),
            }
        else:
            decision_count += 1
            if chapter.get("evidence_level") != "argument":
                errors.append(f"{claim_id}: no-promotion decision requires manifest support state argument")
            disposition = {
                "disposition": "retained_at_argument_via_accepted_no_promotion_decision",
                "disposition_record_ref": rel(NO_PROMOTION_LEDGER),
                "coverage_type": "accepted_no_promotion_decision",
                "support_state_effect": str(decision.get("support_state_effect", "")),
                "required_evidence": normalize_list(decision.get("required_evidence")),
                "blockers": normalize_list(decision.get("blockers")),
                "promotion_burden": str(decision.get("decision_reason", "")),
                "limitations": [],
                "non_claims": normalize_list(decision.get("non_claims")),
            }

        if not disposition["required_evidence"]:
            errors.append(f"{claim_id}: disposition lacks required_evidence")
        if not disposition["blockers"]:
            errors.append(f"{claim_id}: disposition lacks blockers")
        if not nonempty(disposition["promotion_burden"]):
            errors.append(f"{claim_id}: disposition lacks promotion burden or decision reason")
        if not nonempty(plan.get("what_would_move_this")):
            errors.append(f"{chapter_id}: evidence-plan promotion path is empty")
        if not nonempty(appendix.get("open_gap")):
            errors.append(f"{claim_id}: Appendix C open gap is empty")

        dispositions.append(
            {
                "claim_id": claim_id,
                "chapter_id": chapter_id,
                "chapter_title": str(chapter.get("title")),
                "part_id": str(chapter.get("part_id")),
                "part_title": str(chapter.get("part_title")),
                "chapter_file": chapter_file,
                "current_support_state": str(chapter.get("evidence_level")),
                "claim_label": str(chapter.get("claim_label")),
                "core_claim": str(chapter.get("core_claim")),
                **disposition,
                "current_evidence_summary": str(appendix.get("current_evidence_summary")),
                "open_gap": str(appendix.get("open_gap")),
                "primary_evidence_lane": str(plan.get("primary_evidence_lane")),
                "formal_or_prototype_work": str(plan.get("formal_or_prototype_work")),
                "human_reader_focus": str(plan.get("human_reader_focus")),
                "what_would_move_this": str(plan.get("what_would_move_this")),
                "relevant_non_core_transition_refs": transition_refs_for_chapter(non_core_transitions, chapter_file),
            }
        )

    ledger = {
        "disposition_set_id": "v1_x.per_chapter_core_claim_dispositions",
        "date": "2026-07-03",
        "scope_boundary": (
            f"Standing per-chapter disposition record for the {len(chapters)} active manifest "
            "chapter core claims. "
            "It consolidates accepted no-change transitions, accepted no-promotion decisions, Appendix C "
            "open gaps, and per-chapter evidence-plan promotion paths. It creates no support-state movement."
        ),
        "review_status": "active_validator_checked_record",
        "generated_from": [
            rel(STRUCTURE),
            rel(EVIDENCE_PLAN),
            rel(APPENDIX_C),
            rel(NO_PROMOTION_LEDGER),
            "evidence_transitions/**/*.json",
        ],
        "support_state_effect": "none",
        "summary": {
            "manifest_chapter_core_claims": len(chapters),
            "accepted_core_transition_dispositions": transition_count,
            "accepted_no_promotion_dispositions": decision_count,
            "promoted_core_claims": promoted_count,
            "chapter_core_claims_remaining_at_argument": sum(
                1 for row in dispositions if row["current_support_state"] == "argument"
            ),
        },
        "dispositions": dispositions,
        "non_claims": [
            "This ledger does not promote any chapter core claim above its manifest support state.",
            "This ledger does not prove ASI capability, deployed safety, runtime behavior, benchmark performance, source interpretation, novelty, model quality, or external review.",
            "This ledger does not replace accepted evidence-transition records for future support-state movement.",
            "This ledger does not make non-core transitions count as chapter-core support.",
        ],
    }
    report = build_report(ledger)
    return ledger, report, errors


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_report(ledger: dict[str, Any]) -> str:
    summary = ledger["summary"]
    lines = [
        "# Core Claim Disposition Ledger",
        "",
        "Last updated: 2026-07-03",
        "",
        "This report is generated by `python3 scripts/validate_v1_x_core_claim_dispositions.py --write`.",
        "It consolidates the per-chapter core-claim disposition state from the manifest, Appendix C, the evidence plan, accepted no-change transitions, and accepted no-promotion decisions.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Manifest chapter core claims | {summary['manifest_chapter_core_claims']} |",
        f"| Accepted core-transition dispositions | {summary['accepted_core_transition_dispositions']} |",
        f"| Accepted no-promotion dispositions | {summary['accepted_no_promotion_dispositions']} |",
        f"| Promoted core claims | {summary['promoted_core_claims']} |",
        f"| Core claims remaining at `argument` | {summary['chapter_core_claims_remaining_at_argument']} |",
        "",
        "## Dispositions",
        "",
        "| Claim ID | Current support | Disposition | Record | What would move it |",
        "|---|---|---|---|---|",
    ]
    for row in ledger["dispositions"]:
        lines.append(
            "| "
            f"`{row['claim_id']}` | "
            f"`{row['current_support_state']}` | "
            f"`{row['disposition']}` | "
            f"`{row['disposition_record_ref']}` | "
            f"{md_escape(row['what_would_move_this'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This ledger does not promote any chapter core claim above its manifest support state.",
            "- Non-core transitions remain visible only as relevant side-lane references; they do not count as chapter-core support.",
            "- Future support-state movement still requires a separate accepted evidence-transition record.",
            "",
        ]
    )
    return "\n".join(lines)


def validate_ledger_shape(ledger: Any, expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(ledger, dict):
        return [f"{rel(DISPOSITION_LEDGER)} must contain an object"]
    for key in ("disposition_set_id", "date", "scope_boundary", "review_status", "generated_from", "summary", "dispositions", "non_claims"):
        if key not in ledger:
            errors.append(f"{rel(DISPOSITION_LEDGER)} missing {key}")
    if ledger != expected:
        errors.append(
            f"{rel(DISPOSITION_LEDGER)} is stale; run "
            "`python3 scripts/validate_v1_x_core_claim_dispositions.py --write`."
        )
    summary = ledger.get("summary") if isinstance(ledger, dict) else {}
    if isinstance(summary, dict):
        expected_chapter_count = len(expected.get("dispositions", []))
        if summary.get("manifest_chapter_core_claims") != expected_chapter_count:
            errors.append(
                "disposition ledger must cover the current active manifest chapter core claims"
            )
        if summary.get("chapter_core_claims_remaining_at_argument") != expected_chapter_count:
            errors.append("all current chapter core claims must remain at argument")
        if summary.get("promoted_core_claims") != 0:
            errors.append("current v1.x disposition ledger must not record promoted core claims")
    dispositions = ledger.get("dispositions") if isinstance(ledger, dict) else None
    if isinstance(dispositions, list):
        for index, row in enumerate(dispositions):
            if not isinstance(row, dict):
                errors.append(f"dispositions[{index}] must be an object")
                continue
            for key in (
                "claim_id",
                "chapter_id",
                "current_support_state",
                "disposition",
                "disposition_record_ref",
                "required_evidence",
                "blockers",
                "open_gap",
                "what_would_move_this",
                "non_claims",
            ):
                if key not in row:
                    errors.append(f"dispositions[{index}] missing {key}")
            if row.get("current_support_state") != "argument":
                errors.append(f"{row.get('claim_id', index)} must remain at argument")
            if row.get("disposition") not in {
                "retained_at_argument_via_accepted_no_change_transition",
                "retained_at_argument_via_accepted_no_promotion_decision",
            }:
                errors.append(f"{row.get('claim_id', index)} has unexpected disposition {row.get('disposition')!r}")
            for key in ("required_evidence", "blockers", "non_claims"):
                if not nonempty_list(row.get(key)):
                    errors.append(f"{row.get('claim_id', index)} {key} must be a non-empty string list")
            for key in ("open_gap", "what_would_move_this"):
                if not nonempty(row.get(key)):
                    errors.append(f"{row.get('claim_id', index)} {key} must be non-empty")
    return errors


def main() -> None:
    write = "--write" in sys.argv
    expected, report, errors = build_expected()

    if write:
        DISPOSITION_LEDGER.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
        DISPOSITION_REPORT.write_text(report, encoding="utf-8")
    else:
        if DISPOSITION_LEDGER.exists():
            ledger = load_json(DISPOSITION_LEDGER)
            errors.extend(validate_ledger_shape(ledger, expected))
        else:
            errors.append(
                f"{rel(DISPOSITION_LEDGER)} is missing; run "
                "`python3 scripts/validate_v1_x_core_claim_dispositions.py --write`."
            )
        if DISPOSITION_REPORT.exists():
            current_report = DISPOSITION_REPORT.read_text(encoding="utf-8")
            if current_report != report:
                errors.append(
                    f"{rel(DISPOSITION_REPORT)} is stale; run "
                    "`python3 scripts/validate_v1_x_core_claim_dispositions.py --write`."
                )
        else:
            errors.append(
                f"{rel(DISPOSITION_REPORT)} is missing; run "
                "`python3 scripts/validate_v1_x_core_claim_dispositions.py --write`."
            )

    roadmap = ROADMAP.read_text(encoding="utf-8", errors="ignore")
    for required in REQUIRED_ROADMAP_STRINGS:
        if required not in roadmap:
            errors.append(f"{rel(ROADMAP)} missing required disposition text: {required}")

    if errors:
        fail(errors)

    summary = expected["summary"]
    print(
        "v1.x core claim disposition validation passed: "
        f"{summary['manifest_chapter_core_claims']} core claims, "
        f"{summary['accepted_core_transition_dispositions']} accepted transition dispositions, "
        f"{summary['accepted_no_promotion_dispositions']} no-promotion dispositions, "
        f"{summary['promoted_core_claims']} promoted core claims."
    )


if __name__ == "__main__":
    main()
