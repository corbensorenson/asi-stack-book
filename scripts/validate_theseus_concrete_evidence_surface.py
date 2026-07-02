#!/usr/bin/env python3
"""Validate concrete Project Theseus facts surfaced in the book.

The Project Theseus lane is useful only if its public-safe facts stay visible
without becoming broader prototype, benchmark, deployment, or support-state
claims. This check guards the chapter, reader chapter, outline, roadmap, and
manifest against drifting back into abstract prototype narration.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ARCH_SUMMARY = ROOT / "docs" / "theseus_report_import_slice.md"
GEN_SUMMARY = ROOT / "docs" / "theseus_generation_mode_import_slice.md"
SUPPORT_SUMMARY = ROOT / "docs" / "theseus_support_replay_probe.md"
BUNDLE_SUMMARY = ROOT / "docs" / "theseus_report_bundle_audit.md"
ARCH_RESULT = ROOT / "experiments" / "theseus_import" / "results" / "2026-06-29-local.json"
GEN_RESULT = ROOT / "experiments" / "theseus_generation_mode_import" / "results" / "2026-07-01-local.json"
SUPPORT_RESULT = ROOT / "experiments" / "theseus_support_replay_probe" / "results" / "2026-07-01-local.json"
BUNDLE_RESULT = ROOT / "experiments" / "theseus_report_bundle_audit" / "results" / "2026-07-02-local.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LIVE_CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "project-theseus-as-report-first-implementation-reference.qmd"
)

ARCH_FACTS = (
    "theseus.architecture_gate.20260618T192303Z.public_static_import",
    "1ad88a22",
    "dirty_at_import_review",
    "ready_for_heavy_training",
    "14/14",
    "external_inference_calls",
    "7994e2909029644d6073289d8c9c59f774473f366a1c8cbda5943326f28518b2",
    "c33ea5d8d466e394ac556eebd623fb0eb43f601d79ea5f66021ec57762751923",
)

GEN_FACTS = (
    "theseus.generation_mode_gate.20260701.public_static_import",
    "YELLOW",
    "18 modes",
    "13 comparisons",
    "zero hard gaps",
    "zero promotable comparisons",
    "mean_useful_solution_per_second",
    "a711d0dbca9779f26d4b0a63db18ce1fc574ade47a262f5140a9a7b6d325e90b",
    "eebf96a7cf0a6c30c9203d2f11377c953973694a34dec8f095c8b76e378114c7",
    "e99477a1b9546c14c60dc8e2b442f1437274d7ba367e717c23b608fb41fd290b",
    "0a101d427d51029ba7a0aaaaf4329cb47e96400cd21fc284123e366fb309d709",
)

GEN_DOC_FACTS = (
    "theseus.generation_mode_gate.20260701.public_static_import",
    "YELLOW",
    "18 modes",
    "13 comparisons",
    "zero hard gaps",
    "zero promotable comparisons",
    "mean useful solution per second",
    "0a101d427d51029ba7a0aaaaf4329cb47e96400cd21fc284123e366fb309d709",
)

PROBE_FACTS = (
    "theseus-support-replay-probe-2026-07-01-local",
    "Replay commands | 2",
    "Tracked artifacts | 10",
    "Support-state effect | `none`",
    "Chapter-core support effect | `none`",
    "Evidence transition created | `false`",
)

RESULT_DIGESTS = (
    "cbf3d334f79e535c2b6c07a455a84985af774a801ee2b3f084dbfe28a4f7623d",
    "50d1c01397082194f45b916165c582570653073b56a7de934cf9222e80d7486c",
)

BUNDLE_FACTS = (
    "theseus-report-bundle-audit-2026-07-02-local",
    "Expected-invalid controls | 7",
    "Replay-ready rows | 2",
    "Blocked replay rows | 1",
    "Crosswalk rows | 8",
    "Architecture/gate mapping rows | 5",
    "Visible artifact gaps | 6",
    "Intervention ladder levels | 6",
    "Support-state effect | `none`",
    "Evidence transition created | `false`",
)

NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not rerun Project Theseus",
    "does not prove deployed Theseus runtime behavior",
    "does not prove generation speed",
    "does not prove useful-solution-per-second improvement",
    "does not prove model quality",
    "does not create a support-state transition",
)

ARCH_NON_CLAIMS = (
    "does not rerun Project Theseus",
    "Does not promote any chapter core claim",
    "Does not prove deployed Theseus runtime behavior",
    "model quality",
    "benchmark quality",
    "ASI",
)

GEN_NON_CLAIMS = (
    "does not rerun Project Theseus",
    "Does not promote any chapter core claim",
    "Does not prove generation speed",
    "useful-solution-per-second improvement",
    "model quality",
    "ASI",
)

PROBE_NON_CLAIMS = (
    "core claim",
    "support-state transition",
    "rerun Project Theseus",
    "deployed Theseus runtime behavior",
    "generation speed",
    "useful-solution-per-second improvement",
    "model quality",
)

CHAPTER_FACTS = (
    "Concrete Theseus Evidence Surface",
    "architecture-gate import",
    "14/14",
    "generation-mode import",
    "18 modes",
    "13 comparisons",
    "zero hard gaps",
    "zero promotable comparisons",
    "useful-solution-per-second",
    "0.0",
    "support replay probe",
    "2 replay commands",
    "10 tracked artifacts",
    "report-bundle audit",
    "7 expected-invalid controls",
    "8 crosswalk rows",
    "6 visible artifact gaps",
    "support-state effect `none`",
    "do not promote the Theseus core claim",
)

READER_FACTS = (
    "What The Static Imports Mean",
    "14 of 14",
    "zero external inference calls",
    "18 modes",
    "13 comparisons",
    "zero hard gaps",
    "zero promotable comparisons",
    "useful solution per second at `0.0`",
    "two ASI-side validators",
    "ten tracked artifacts",
    "report-bundle audit",
    "seven expected-invalid controls",
    "eight stack-layer crosswalk rows",
    "six visible artifact gaps",
    "does not move the Project Theseus core claim above `argument`",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    lower_text = normalize_text(text)
    for fragment in fragments:
        if normalize_text(fragment) not in lower_text:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def main() -> None:
    errors: list[str] = []

    paths = (
        ARCH_SUMMARY,
        GEN_SUMMARY,
        SUPPORT_SUMMARY,
        BUNDLE_SUMMARY,
        ARCH_RESULT,
        GEN_RESULT,
        SUPPORT_RESULT,
        BUNDLE_RESULT,
        STRUCTURE,
        OUTLINE,
        ROADMAP,
        LIVE_CHAPTER,
        READER_CHAPTER,
    )
    for path in paths:
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    arch_summary_text = ARCH_SUMMARY.read_text(encoding="utf-8")
    gen_summary_text = GEN_SUMMARY.read_text(encoding="utf-8")
    support_summary_text = SUPPORT_SUMMARY.read_text(encoding="utf-8")
    bundle_summary_text = BUNDLE_SUMMARY.read_text(encoding="utf-8")
    arch_result = load_json(ARCH_RESULT)
    gen_result = load_json(GEN_RESULT)
    support_result = load_json(SUPPORT_RESULT)
    bundle_result = load_json(BUNDLE_RESULT)
    structure = load_json(STRUCTURE)
    outline_text = OUTLINE.read_text(encoding="utf-8")
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    live_text = LIVE_CHAPTER.read_text(encoding="utf-8")
    reader_text = READER_CHAPTER.read_text(encoding="utf-8")

    require_fragments(rel(ARCH_SUMMARY), arch_summary_text, ARCH_FACTS + ARCH_NON_CLAIMS, errors)
    require_fragments(rel(GEN_SUMMARY), gen_summary_text, GEN_DOC_FACTS + GEN_NON_CLAIMS, errors)
    require_fragments(rel(SUPPORT_SUMMARY), support_summary_text, PROBE_FACTS + PROBE_NON_CLAIMS, errors)
    require_fragments(rel(BUNDLE_SUMMARY), bundle_summary_text, BUNDLE_FACTS + PROBE_NON_CLAIMS, errors)
    require_fragments(rel(ARCH_RESULT), text_blob(arch_result), (ARCH_FACTS[0], ARCH_FACTS[6], ARCH_FACTS[7]) + ARCH_NON_CLAIMS[1:], errors)
    require_fragments(rel(GEN_RESULT), text_blob(gen_result), (GEN_FACTS[0], GEN_FACTS[7], GEN_FACTS[10]) + GEN_NON_CLAIMS[1:], errors)
    require_fragments(rel(SUPPORT_RESULT), text_blob(support_result), RESULT_DIGESTS + PROBE_NON_CLAIMS, errors)
    require_fragments(
        rel(BUNDLE_RESULT),
        text_blob(bundle_result),
        (
            "theseus-report-bundle-audit-2026-07-02-local",
            "expected_invalid_count",
            "replay_ready_row_count",
            "crosswalk_layer_count",
            "visible_artifact_gap_count",
            "intervention_ladder_level_count",
            "support_state_effect",
            "none",
        )
        + PROBE_NON_CLAIMS,
        errors,
    )

    if arch_result.get("accepted_gate_count") != 14 or arch_result.get("accepted_passed_count") != 14:
        errors.append(f"{rel(ARCH_RESULT)} must preserve the 14/14 imported architecture-gate summary.")
    if gen_result.get("accepted_mode_count") != 18 or gen_result.get("accepted_comparison_count") != 13:
        errors.append(f"{rel(GEN_RESULT)} must preserve the 18-mode/13-comparison summary.")
    if gen_result.get("accepted_hard_gap_count") != 0:
        errors.append(f"{rel(GEN_RESULT)} must preserve zero hard gaps.")
    if gen_result.get("accepted_promotable_comparison_count") != 0:
        errors.append(f"{rel(GEN_RESULT)} must preserve zero promotable comparisons.")
    if float(gen_result.get("accepted_useful_solution_per_second", -1)) != 0.0:
        errors.append(f"{rel(GEN_RESULT)} must preserve useful-solution-per-second 0.0.")

    if arch_result.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append(f"{rel(ARCH_RESULT)} must keep support_state_effect no_chapter_core_claim_promotion.")
    if gen_result.get("support_state_effect") != "no_chapter_core_claim_promotion":
        errors.append(f"{rel(GEN_RESULT)} must keep support_state_effect no_chapter_core_claim_promotion.")
    if support_result.get("support_state_effect") != "none":
        errors.append(f"{rel(SUPPORT_RESULT)} must keep support_state_effect none.")
    if support_result.get("chapter_core_support_effect") != "none":
        errors.append(f"{rel(SUPPORT_RESULT)} must keep chapter_core_support_effect none.")
    if support_result.get("evidence_transition_created") is not False:
        errors.append(f"{rel(SUPPORT_RESULT)} must not create an evidence transition.")
    if bundle_result.get("support_state_effect") != "none":
        errors.append(f"{rel(BUNDLE_RESULT)} must keep support_state_effect none.")
    if bundle_result.get("chapter_core_support_effect") != "none":
        errors.append(f"{rel(BUNDLE_RESULT)} must keep chapter_core_support_effect none.")
    if bundle_result.get("evidence_transition_created") is not False:
        errors.append(f"{rel(BUNDLE_RESULT)} must not create an evidence transition.")
    expected_bundle_counts = {
        "expected_invalid_count": 7,
        "replay_ready_row_count": 2,
        "blocked_replay_row_count": 1,
        "crosswalk_layer_count": 8,
        "mapped_gate_decision_count": 5,
        "visible_artifact_gap_count": 6,
        "intervention_ladder_level_count": 6,
    }
    for key, expected in expected_bundle_counts.items():
        if bundle_result.get(key) != expected:
            errors.append(f"{rel(BUNDLE_RESULT)} must keep {key} {expected}.")

    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
    else:
        record = chapter_record(structure, "project-theseus-as-report-first-implementation-reference")
        if record.get("evidence_level") != "argument":
            errors.append("Project Theseus chapter evidence_level must remain argument.")
        tests = text_blob(record.get("codex_tests", []))
        require_fragments(
            "book_structure Project Theseus tests",
            tests,
            (
                "Theseus support replay probe",
                "Theseus concrete evidence-surface validation",
                "Theseus report-bundle audit validation",
                "python3 scripts/validate_theseus_concrete_evidence_surface.py",
                "python3 scripts/validate_theseus_report_bundle_audit.py",
                "no live Theseus replay",
                "support-state promotion",
            ),
            errors,
        )

    require_fragments(rel(LIVE_CHAPTER), live_text, CHAPTER_FACTS + PROBE_NON_CLAIMS, errors)
    require_fragments(rel(READER_CHAPTER), reader_text, READER_FACTS + PROBE_NON_CLAIMS, errors)
    for path, text in ((LIVE_CHAPTER, live_text), (READER_CHAPTER, reader_text)):
        if "support: argument" not in text and path == LIVE_CHAPTER:
            errors.append(f"{rel(path)} must keep core claim support at argument.")
        if "Evidence level | argument" not in text and path == LIVE_CHAPTER:
            errors.append(f"{rel(path)} must keep the status table at argument evidence.")

    require_fragments(
        rel(OUTLINE),
        outline_text,
        (
            "Theseus concrete evidence-surface validation",
            "Theseus report-bundle audit validation",
            "14/14",
            "18 modes",
            "13 comparisons",
            "zero promotable comparisons",
            "7 expected-invalid controls",
            "8 crosswalk rows",
            "6 visible artifact gaps",
            "support-state effect `none`",
            "does not promote chapter-core support",
        ),
        errors,
    )
    require_fragments(
        rel(ROADMAP),
        roadmap_text,
        (
            "project-theseus-as-report-first-implementation-reference",
            "validate_theseus_concrete_evidence_surface.py",
            "validate_theseus_report_bundle_audit.py",
            "14/14",
            "18",
            "13 comparisons",
            "zero promotable comparisons",
            "report-bundle audit",
            "support-state effect `none`",
            "two ASI-side",
            "support-state effect `none`",
        ),
        errors,
    )

    if errors:
        fail(errors)

    print("Theseus concrete evidence-surface validation passed.")


def fail(errors: list[str]) -> None:
    print("Theseus concrete evidence-surface validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
