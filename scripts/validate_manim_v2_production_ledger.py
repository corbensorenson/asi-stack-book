#!/usr/bin/env python3
"""Validate Manim v2 production identity, ordering, gates, and custody."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from sync_manim_v2_production_ledger import build


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "visual_edition/manim_v2_production_ledger.json"
SCHEMA = ROOT / "schemas/manim_v2_production_ledger.schema.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_beat_auditor():
    path = ROOT / "skills/asi-stack-manim-videos/scripts/audit_video_plan.py"
    spec = importlib.util.spec_from_file_location("asi_stack_manim_beat_auditor", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the tracked Manim beat auditor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def semantic_errors(value: dict) -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(value)
    ]
    expected = build()
    expected["generated_at_utc"] = value.get("generated_at_utc")
    if value != expected:
        errors.append("ledger does not match its canonical manifest-driven derivation")
    beat_schema = json.loads((ROOT / "schemas/manim_beat_plan.schema.json").read_text(encoding="utf-8"))
    review_schema = json.loads((ROOT / "schemas/manim_experience_review.schema.json").read_text(encoding="utf-8"))
    narration_toolchain = json.loads(
        (ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8")
    )
    alignment_qualified = (
        narration_toolchain.get("alignment", {}).get("qualification_state")
        == "qualified"
    )
    beat_auditor = load_beat_auditor()
    for entry in value.get("entries", []):
        chapter_id = entry.get("chapter_id", "unknown")
        target = entry.get("target", {})
        gates = target.get("gates", {})
        stage = target.get("stage")
        gate_prerequisites = {
            "animatic": ("beat_plan",),
            "picture_and_sound_lock": ("beat_plan", "animatic"),
            "release_candidate": ("beat_plan", "animatic", "picture_and_sound_lock"),
            "independent_release_candidate": ("release_candidate",),
        }
        for gate_name, prerequisites in gate_prerequisites.items():
            if gates.get(gate_name) == "pass":
                missing = [name for name in prerequisites if gates.get(name) != "pass"]
                if missing:
                    errors.append(
                        f"{chapter_id}: {gate_name} passes before {', '.join(missing)}"
                    )
        if gates.get("picture_and_sound_lock") == "pass" and not alignment_qualified:
            errors.append(
                f"{chapter_id}: picture-and-sound lock passes before forced alignment is qualified"
            )
        if gates.get("accepted") == "pass":
            required = ("beat_plan", "animatic", "picture_and_sound_lock", "release_candidate", "independent_release_candidate", "technical", "claim_fidelity")
            missing = [name for name in required if gates.get(name) != "pass"]
            if missing:
                errors.append(f"{chapter_id}: accepted without passing {', '.join(missing)}")
        if target.get("youtube_state") != "not_ready" and gates.get("accepted") != "pass":
            errors.append(f"{chapter_id}: YouTube state advanced before generation-2 acceptance")
        if target.get("quarto_embed_state") == "generation_2_current" and target.get("youtube_state") != "public_current":
            errors.append(f"{chapter_id}: generation-2 embed is current before YouTube public-current reconciliation")
        if stage in {"accepted", "youtube_current", "quarto_current"} and gates.get("accepted") != "pass":
            errors.append(f"{chapter_id}: stage {stage} lacks the accepted gate")
        predecessor = entry.get("predecessor")
        if predecessor is not None:
            packet_path = ROOT / predecessor.get("packet_path", "")
            if not packet_path.is_file():
                errors.append(f"{chapter_id}: predecessor packet is missing")
            elif json.loads(packet_path.read_text(encoding="utf-8"))["render_receipt"]["output_sha256"] != predecessor.get("master_sha256"):
                errors.append(f"{chapter_id}: predecessor master identity drift")
        narration_path = ROOT / target.get("narration_path", "")
        narration = narration_path.read_text(encoding="utf-8") if narration_path.is_file() else None
        narration_sha256 = target.get("narration_sha256")
        if narration is None:
            if narration_sha256 is not None:
                errors.append(f"{chapter_id}: narration digest exists without its script")
            if stage not in {"planned", "briefed"}:
                errors.append(f"{chapter_id}: stage {stage} lacks its narration script")
        else:
            if narration_sha256 != digest(narration_path):
                errors.append(f"{chapter_id}: narration identity drift")
            if stage not in {"planned", "briefed"}:
                narration_errors, _, _ = beat_auditor.audit_narration(narration)
                errors.extend(
                    f"{chapter_id}:narration:{error}" for error in narration_errors
                )

        beat_path = ROOT / target.get("beat_plan_path", "")
        if gates.get("beat_plan") == "pass":
            if not beat_path.is_file():
                errors.append(f"{chapter_id}: beat-plan gate passes without its tracked plan")
            else:
                plan = json.loads(beat_path.read_text(encoding="utf-8"))
                errors.extend(
                    f"{chapter_id}:beat-plan-schema:{'.'.join(map(str, error.path))}: {error.message}"
                    for error in Draft202012Validator(beat_schema).iter_errors(plan)
                )
                audit_errors, _, _ = beat_auditor.audit(plan, narration)
                errors.extend(f"{chapter_id}:beat-plan:{error}" for error in audit_errors)
        for pass_name, review_path in target.get("experience_review_paths", {}).items():
            gate_name = pass_name
            gate_state = gates.get(gate_name)
            if gate_state in {"pass", "revise"}:
                path = ROOT / review_path
                if not path.is_file():
                    errors.append(f"{chapter_id}: {pass_name} is {gate_state} without its review record")
                else:
                    review = json.loads(path.read_text(encoding="utf-8"))
                    errors.extend(
                        f"{chapter_id}:{pass_name}-schema:{'.'.join(map(str, error.path))}: {error.message}"
                        for error in Draft202012Validator(review_schema).iter_errors(review)
                    )
                    expected_pass = "release_candidate" if pass_name == "independent_release_candidate" else pass_name
                    if review.get("chapter_id") != chapter_id or review.get("generation") != target.get("generation"):
                        errors.append(f"{chapter_id}: {pass_name} review identity or generation drift")
                    if review.get("pass") != expected_pass:
                        errors.append(f"{chapter_id}: {pass_name} review declares the wrong review pass")
                    if gate_state == "pass":
                        if review.get("verdict") != "pass" or review.get("open_defects"):
                            errors.append(f"{chapter_id}: {pass_name} gate passes with a revise verdict or open defects")
                        low = [name for name, row in review.get("dimensions", {}).items() if row.get("score", 0) < 4]
                        if low:
                            errors.append(f"{chapter_id}: {pass_name} averages cannot hide sub-4 dimensions: {', '.join(low)}")
                        if pass_name in {"release_candidate", "independent_release_candidate"}:
                            learning = review.get("learning_check", {})
                            if (
                                learning.get("reviewer_prior_exposure") != "cold"
                                or learning.get("comprehension_result") != "pass"
                                or learning.get("transfer_result") != "pass"
                            ):
                                errors.append(
                                    f"{chapter_id}: {pass_name} lacks a cold passing comprehension and transfer check"
                                )
                    elif review.get("verdict") != "revise" or not review.get("open_defects"):
                        errors.append(f"{chapter_id}: {pass_name} revise gate lacks a revise verdict and owned defects")
        if gates.get("accepted") == "pass":
            receipt_path = target.get("render_receipt_path")
            if not isinstance(target.get("master_sha256"), str) or len(target["master_sha256"]) != 64:
                errors.append(f"{chapter_id}: accepted generation lacks an exact master digest")
            if not receipt_path or not (ROOT / receipt_path).is_file():
                errors.append(f"{chapter_id}: accepted generation lacks a tracked render receipt")
    return errors


def negative_control_failures(value: dict) -> list[str]:
    """Require representative custody and lifecycle mutations to fail specifically."""

    controls: list[tuple[str, dict, str]] = []

    missing_entry = copy.deepcopy(value)
    missing_entry["entries"].pop()
    controls.append(("chapter deletion", missing_entry, "ledger does not match"))

    predecessor_drift = copy.deepcopy(value)
    predecessor_drift["entries"][0]["predecessor"]["master_sha256"] = "0" * 64
    controls.append(("predecessor identity drift", predecessor_drift, "predecessor master identity drift"))

    narration_drift = copy.deepcopy(value)
    scripted = next(
        entry for entry in narration_drift["entries"]
        if entry["target"].get("narration_sha256") is not None
    )
    scripted["target"]["narration_sha256"] = "0" * 64
    controls.append(("narration identity drift", narration_drift, "narration identity drift"))

    averaged_review = copy.deepcopy(value)
    averaged_review["entries"][0]["target"]["gates"]["animatic"] = "pass"
    averaged_review["entries"][0]["target"]["experience_review_paths"]["animatic"] = (
        "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/reviews/animatic-r2.json"
    )
    controls.append(("rejected review promotion", averaged_review, "averages cannot hide sub-4 dimensions"))

    unaligned_lock = copy.deepcopy(value)
    unaligned_lock["entries"][0]["target"]["gates"]["picture_and_sound_lock"] = "pass"
    controls.append(("unaligned picture lock", unaligned_lock, "forced alignment is qualified"))

    premature_acceptance = copy.deepcopy(value)
    premature_acceptance["entries"][0]["target"]["gates"]["accepted"] = "pass"
    controls.append(("premature acceptance", premature_acceptance, "accepted without passing"))

    premature_youtube = copy.deepcopy(value)
    premature_youtube["entries"][0]["target"]["youtube_state"] = "ready_for_authorized_supersession"
    controls.append(("premature YouTube advancement", premature_youtube, "YouTube state advanced"))

    premature_embed = copy.deepcopy(value)
    premature_embed["entries"][0]["target"]["quarto_embed_state"] = "generation_2_current"
    controls.append(("premature Quarto advancement", premature_embed, "embed is current before YouTube"))

    invented_support = copy.deepcopy(value)
    invented_support["support_state_effect"] = "promote"
    controls.append(("support invention", invented_support, "support_state_effect"))

    failures: list[str] = []
    for label, mutation, expected_fragment in controls:
        errors = semantic_errors(mutation)
        if not any(expected_fragment in error for error in errors):
            failures.append(f"negative control did not trigger its owned rejection: {label}")
    return failures


def main() -> None:
    value = json.loads(LEDGER.read_text(encoding="utf-8"))
    errors = semantic_errors(value)
    errors.extend(negative_control_failures(value))
    if errors:
        raise SystemExit("Manim v2 production ledger validation failed:\n - " + "\n - ".join(errors))
    print(
        f"Manim v2 production ledger validates: {len(value['entries'])} identities, four cohorts, "
        "preserved predecessors, fail-closed generation-2 gates, and nine rejecting mutations."
    )


if __name__ == "__main__":
    main()
