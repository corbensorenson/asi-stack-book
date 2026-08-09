#!/usr/bin/env python3
"""Audit ASI Stack Manim narration and v2 beat plans.

This is a structural preflight, not an aesthetic or truth judge. It rejects
known script, story, synchronization, continuity, accessibility, and claim
failures while keeping density and technique variety as diagnostics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCHEMA = "asi_stack.manim_beat_plan.v2"
ALLOWED_STORY_FUNCTIONS = {
    "hook",
    "setup",
    "prediction",
    "construction",
    "mechanism",
    "worked_trace",
    "comparison",
    "counterexample",
    "failure",
    "consequence",
    "evidence_boundary",
    "payoff",
    "handoff",
}
REQUIRED_STORY_FUNCTIONS = {"hook", "mechanism", "evidence_boundary", "payoff"}
SEMANTIC_ENCODINGS = {
    "identity",
    "relation",
    "causality",
    "sequence",
    "quantity",
    "uncertainty",
    "contrast",
    "containment",
    "authority",
    "rollback",
    "attention",
}
CLAIM_ROLES = {
    "question",
    "concrete_example",
    "mechanism",
    "transition",
    "counterexample",
    "evidence",
    "boundary",
    "connective",
}
BRIEF_FIELDS = {
    "story": ("concrete_case", "opening_question", "payoff", "transfer"),
    "art_direction": (
        "visual_thesis",
        "signature_image",
        "visual_world",
        "persistent_objects",
        "composition_rule",
        "palette_rule",
        "typography_rule",
        "motion_character",
        "camera_rule",
        "surface_rule",
        "ending_image",
    ),
    "audio_direction": (
        "narration_style",
        "pacing_arc",
        "music_policy",
        "sound_effect_policy",
        "review_devices",
    ),
    "accessibility": (
        "color_redundancy",
        "motion_redundancy",
        "integrated_description",
        "caption_plan",
        "reduced_motion_assessment",
    ),
}
TEMPLATE_PHRASES = (
    "this chapter",
    "the tempting shortcut is insufficient",
    "the chapter's core claim is",
    "the chapters core claim is",
    "current evidence state",
    "read the live chapter",
    "read the live book",
    "the next chapter",
    "chapter digest",
    "source commit",
)
INTERNAL_METADATA_PATTERNS = (
    (re.compile(r"\b(?:claim|proof|fixture|validator|theorem)\s+(?:id|count|counts)\b", re.I), "internal identifier or count"),
    (re.compile(r"\b(?:argument|formal|measured|reproduced|operational)\s+support\b", re.I), "support-state vocabulary"),
    (re.compile(r"\b(?:chapters?|sources?|scripts?|visual_edition)/[^\s]+", re.I), "repository path"),
    (re.compile(r"\b(?:ext|src|clm|prf)_[a-z0-9_-]+\b", re.I), "repository identifier"),
)
STATIC_ACTIONS = {
    "hold",
    "wait",
    "display text",
    "show card",
    "fade in card",
}


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", text)


def normalized(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower()))


def sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", text.strip()) if item.strip()]


def audit_teaching_promise(value: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(value, str) or not value.strip():
        return ["missing non-empty teaching_promise"], warnings
    count = len(words(value))
    if count > 34:
        errors.append(f"teaching_promise has {count} words; select one transferable outcome")
    elif count > 26:
        warnings.append(f"teaching_promise has {count} words; review for chapter-summary scope")
    joins = len(re.findall(r"\band\b", value, flags=re.I))
    if joins > 2 or value.count(";") or value.count(",") > 2:
        errors.append("teaching_promise reads as a coverage list rather than one outcome")
    return errors, warnings


def audit_narration(
    narration: str,
    *,
    duration_seconds: float | None = None,
    duration_rationale: str | None = None,
) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    clean = narration.strip()
    word_count = len(words(clean))
    if word_count < 220:
        warnings.append(f"narration has {word_count} words; verify that the mechanism and transfer test are complete")
    if word_count > 520:
        warnings.append(f"narration has {word_count} words; the normal visual-abstract ceiling is 520")
    if word_count > 600 and not (isinstance(duration_rationale, str) and len(duration_rationale.strip()) >= 24):
        errors.append("narration above 600 words requires a specific duration rationale")
    if word_count > 650:
        errors.append(f"narration has {word_count} words; scripts above 650 must be split or reselected")

    long_sentence_count = 0
    extreme_sentence_count = 0
    list_sentence_count = 0
    for sentence in sentences(clean):
        count = len(words(sentence))
        if count > 24:
            long_sentence_count += 1
            warnings.append(f"review {count}-word sentence for multiple spoken ideas: {sentence[:72]!r}")
        if count > 32:
            extreme_sentence_count += 1
            errors.append(f"{count}-word sentence exceeds the spoken-language ceiling: {sentence[:72]!r}")
        if sentence.count(",") >= 5 or sentence.count(";") >= 3:
            list_sentence_count += 1
            errors.append(f"sentence reads as an inventory rather than a causal explanation: {sentence[:72]!r}")

    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", clean) if item.strip()]
    oversized_blocks = 0
    for index, paragraph in enumerate(paragraphs, start=1):
        count = len(words(paragraph))
        if count > 130:
            oversized_blocks += 1
            warnings.append(f"performance block {index} has {count} words; review prosody and scene load")
        if count > 180:
            errors.append(f"performance block {index} has {count} words; split it at a real thought boundary")

    normalized_narration = normalized(clean)
    for phrase in TEMPLATE_PHRASES:
        if phrase in normalized_narration:
            errors.append(f"templated or administrative narration phrase is prohibited: {phrase!r}")
    for pattern, label in INTERNAL_METADATA_PATTERNS:
        if pattern.search(clean):
            errors.append(f"spoken narration contains {label}; express the boundary in ordinary language")

    question_count = clean.count("?")
    if question_count > 3:
        warnings.append(f"narration asks {question_count} questions; keep only questions with evidence and thinking time")

    wpm = None
    if isinstance(duration_seconds, (int, float)) and duration_seconds > 0:
        wpm = word_count / duration_seconds * 60
        if wpm < 100 or wpm > 155:
            warnings.append(f"narration rate is {wpm:.1f} WPM; inspect delivery against the usual 100–155 WPM range")
        if wpm < 80 or wpm > 170:
            errors.append(f"narration rate of {wpm:.1f} WPM is an extreme delivery outlier")

    return errors, warnings, {
        "narration_words": word_count,
        "paragraphs": len(paragraphs),
        "long_sentence_warning_count": long_sentence_count,
        "extreme_sentence_count": extreme_sentence_count,
        "inventory_sentence_count": list_sentence_count,
        "oversized_performance_blocks": oversized_blocks,
        "question_count": question_count,
        "words_per_minute": round(wpm, 2) if wpm is not None else None,
    }


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("beat plan must contain a JSON object")
    return value


def require_text(container: dict, field: str, label: str, errors: list[str]) -> str:
    value = container.get(field)
    if not isinstance(value, str) or len(value.strip()) < 8:
        errors.append(f"{label}.{field} must be a specific non-empty description")
        return ""
    return value.strip()


def require_string_list(
    container: dict,
    field: str,
    label: str,
    errors: list[str],
    *,
    allow_empty: bool = False,
) -> list[str]:
    value = container.get(field)
    if (
        not isinstance(value, list)
        or (not value and not allow_empty)
        or not all(isinstance(item, str) and item.strip() for item in value)
    ):
        qualifier = "a string list" if allow_empty else "a non-empty string list"
        errors.append(f"{label}.{field} must be {qualifier}")
        return []
    return [item.strip() for item in value]


def self_test() -> None:
    """Exercise a passing plan and deliberate synchronization/design failures."""
    functions = (
        ["hook"]
        + ["setup"] * 3
        + ["prediction"] * 2
        + ["construction"] * 4
        + ["mechanism"] * 7
        + ["worked_trace"] * 5
        + ["failure"] * 3
        + ["consequence"] * 2
        + ["evidence_boundary"]
        + ["payoff"]
        + ["handoff"]
    )
    techniques = [
        "TransformFromCopy",
        "MoveAlongPath",
        "LaggedStart",
        "ValueTracker",
        "ReplacementTransform",
        "Circumscribe",
    ]
    persistent = ["request token", "authority gate", "route graph"]
    beats = []
    for index, function in enumerate(functions):
        marker = f"marker {index:02d}"
        spoken = f"At {marker}, the token changes one relation and reveals the next governed state."
        beats.append(
            {
                "id": f"b{index + 1:02d}",
                "story_function": function,
                "start_seconds": index * 6.0,
                "end_seconds": (index + 1) * 6.0,
                "narration": spoken,
                "sync_anchor": marker,
                "visual_purpose": "Show one causal relation changing at the spoken anchor.",
                "visual_action": f"move token through relation {index:02d}",
                "attention_target": "The active edge and token endpoint.",
                "semantic_encodings": ["relation", "causality"],
                "object_before": f"Token before relation {index:02d}.",
                "object_after": f"Token after relation {index:02d}.",
                "continuity_objects": persistent[:2],
                "composition": "The active edge occupies the center while context remains dimmed.",
                "motion_curve": "Ease-out arrival followed by a short settled hold.",
                "camera_action": "Static frame because the complete relation is already legible.",
                "animation_techniques": [techniques[index % len(techniques)]],
                "on_screen_text": [f"state {index:02d}"],
                "settle_seconds": 0.5,
                "hold_purpose": "Let the changed endpoint register before the next relation.",
                "new_concepts": ["authority boundary"] if index == 0 else [],
                "claim_role": "mechanism" if function == "mechanism" else "transition",
                "evidence_boundary": "Synthetic validator fixture; it makes no book claim.",
            }
        )
    plan = {
        "schema_version": SCHEMA,
        "chapter_id": "self-test",
        "teaching_promise": "The viewer can predict when a route must stop.",
        "chapter_sha256": "a" * 64,
        "source_commit": "self-test",
        "target_duration_seconds": 180.0,
        "story": {
            "concrete_case": "A request reaches two routes and one authority gate.",
            "opening_question": "Which route may allow the request to act?",
            "payoff": "The authority key, not answer agreement, controls action.",
            "transfer": "Apply the same distinction to tools and updates.",
        },
        "art_direction": {
            "visual_thesis": "The request moves farther than its authority permits.",
            "signature_image": "Two equal paths meet one gate, with one visibly blocked.",
            "visual_world": "A persistent route graph with token and authority gate.",
            "persistent_objects": persistent,
            "composition_rule": "Flow left to right along one stable decision axis.",
            "palette_rule": "Accent marks active flow and warning marks blocked flow.",
            "typography_rule": "Use short labels adjacent to states and boundaries.",
            "motion_character": "Precise routing with firm, legible stopping motion.",
            "camera_rule": "Reframe only to compare paths or isolate the authority gate.",
            "surface_rule": "Flat field, stable strokes, and restrained emphasis glow.",
            "ending_image": "Only the keyed path crosses while both answers remain visible.",
        },
        "audio_direction": {
            "narration_style": "Warm and deliberate with contrastive emphasis.",
            "pacing_arc": "Fast setup, slow prediction, crisp reveal, quiet boundary.",
            "music_policy": "Rights-cleared bed ducked under all dense explanation.",
            "sound_effect_policy": "One restrained gate sound; no decorative effects.",
            "review_devices": ["headphones", "earbuds", "laptop speakers", "phone speakers"],
        },
        "accessibility": {
            "color_redundancy": "Route state also uses shape, position, and a label.",
            "motion_redundancy": "Each movement ends in a distinct stable position.",
            "integrated_description": "Narration names the token, route, and blocked gate.",
            "caption_plan": "Exact final narration plus the meaningful gate sound.",
            "reduced_motion_assessment": "No flash, spin, parallax, shake, or continuous zoom.",
        },
        "beats": beats,
    }
    narration = "\n\n".join(beat["narration"] for beat in beats)
    errors, _, summary = audit(plan, narration)
    if errors:
        raise AssertionError("valid fixture failed:\n" + "\n".join(errors))
    if summary["beats"] != 30 or summary["animation_technique_count"] != 6:
        raise AssertionError(f"unexpected passing summary: {summary}")

    broken = json.loads(json.dumps(plan))
    broken["beats"][0]["sync_anchor"] = "missing spoken anchor"
    broken["beats"][0]["visual_action"] = "hold"
    broken["beats"][0]["object_after"] = broken["beats"][0]["object_before"]
    broken["beats"][0]["semantic_encodings"] = ["sparkle"]
    broken["art_direction"]["signature_image"] = ""
    broken_errors, _, _ = audit(broken, narration)
    expected_fragments = (
        "sync_anchor",
        "static or text-only",
        "do not declare a state change",
        "unknown semantic_encodings",
        "art_direction.signature_image",
    )
    for fragment in expected_fragments:
        if not any(fragment in error for error in broken_errors):
            raise AssertionError(f"invalid fixture did not trigger {fragment!r}")

    duplicate = json.loads(json.dumps(plan))
    duplicate["beats"][1]["sync_anchor"] = duplicate["beats"][0]["sync_anchor"]
    duplicate["beats"][1]["narration"] += " The marker 00 phrase is repeated here."
    duplicate_narration = " ".join(beat["narration"] for beat in duplicate["beats"])
    duplicate_errors, _, _ = audit(duplicate, duplicate_narration)
    if not any("duplicates another beat" in error for error in duplicate_errors):
        raise AssertionError("duplicate sync-anchor fixture did not fail")

    administrative = (
        "This chapter asks a specific question. "
        "The chapter's core claim is recorded as claim id clm_fixture."
    )
    narration_errors, _, _ = audit_narration(administrative)
    for fragment in ("templated or administrative", "repository identifier"):
        if not any(fragment in error for error in narration_errors):
            raise AssertionError(f"narration fixture did not trigger {fragment!r}")
    print("Self-test passed.")


def audit(plan: dict, narration: str | None) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    if plan.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must be {SCHEMA}")
    for field in ("chapter_id", "chapter_sha256", "source_commit"):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            errors.append(f"missing non-empty {field}")
    promise_errors, promise_warnings = audit_teaching_promise(plan.get("teaching_promise"))
    errors.extend(promise_errors)
    warnings.extend(promise_warnings)
    digest = plan.get("chapter_sha256", "")
    if digest and not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append("chapter_sha256 must be 64 lowercase hexadecimal characters")

    duration = plan.get("target_duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        errors.append("target_duration_seconds must be positive")
        duration = 1.0
    elif not 150 <= duration <= 270:
        warnings.append("target duration falls outside the preferred 2.5–4.5 minute visual-abstract range")
    if isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration > 270:
        audio_direction = plan.get("audio_direction")
        rationale = audio_direction.get("duration_rationale") if isinstance(audio_direction, dict) else None
        if not isinstance(rationale, str) or len(rationale.strip()) < 24:
            errors.append(
                "audio_direction.duration_rationale must explain why a video above the normal 4.5-minute target improves the teaching result"
            )

    for brief_name, fields in BRIEF_FIELDS.items():
        brief = plan.get(brief_name)
        if not isinstance(brief, dict):
            errors.append(f"{brief_name} must be an object")
            continue
        for field in fields:
            if field in {"persistent_objects", "review_devices"}:
                require_string_list(brief, field, brief_name, errors)
            else:
                require_text(brief, field, brief_name, errors)

    persistent = set()
    art_direction = plan.get("art_direction")
    if isinstance(art_direction, dict):
        value = art_direction.get("persistent_objects")
        if isinstance(value, list):
            persistent = {normalized(item) for item in value if isinstance(item, str)}
        if len(persistent) > 7:
            warnings.append("art_direction.persistent_objects names more than seven objects; review visual load")

    beats = plan.get("beats")
    if not isinstance(beats, list) or not beats:
        errors.append("beats must be a non-empty list")
        return errors, warnings, {}

    seen_ids: set[str] = set()
    seen_anchors: set[str] = set()
    story_positions: dict[str, list[int]] = {}
    narration_parts: list[str] = []
    techniques: set[str] = set()
    continuity_counts: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    composition_counts: Counter[str] = Counter()
    previous_end = 0.0
    long_sentences = 0
    settle_total = 0.0
    question_positions: dict[str, int] = {}
    resolution_positions: dict[str, int] = {}
    introduced_concepts: set[str] = set()

    for index, beat in enumerate(beats):
        label = f"beat[{index}]"
        if not isinstance(beat, dict):
            errors.append(f"{label} must be an object")
            continue
        beat_id = beat.get("id")
        if not isinstance(beat_id, str) or not beat_id:
            errors.append(f"{label} has no id")
        elif beat_id in seen_ids:
            errors.append(f"duplicate beat id {beat_id}")
        else:
            seen_ids.add(beat_id)
            label = beat_id

        function = beat.get("story_function")
        if function not in ALLOWED_STORY_FUNCTIONS:
            errors.append(f"{label}: invalid story_function {function!r}")
        else:
            story_positions.setdefault(function, []).append(index)

        start = beat.get("start_seconds")
        end = beat.get("end_seconds")
        if not isinstance(start, (int, float)) or isinstance(start, bool):
            errors.append(f"{label}: start_seconds must be numeric")
            start = previous_end
        if not isinstance(end, (int, float)) or isinstance(end, bool) or end <= start:
            errors.append(f"{label}: end_seconds must be greater than start_seconds")
            end = start
        if abs(start - previous_end) > 0.25:
            errors.append(f"{label}: timing gap/overlap from prior beat is {start - previous_end:+.3f}s")
        beat_duration = end - start
        previous_end = end

        hold_purpose = beat.get("hold_purpose")
        if beat_duration > 12 and not (isinstance(hold_purpose, str) and len(hold_purpose.strip()) >= 8):
            errors.append(f"{label}: {beat_duration:.2f}s beat exceeds 12s without a recorded viewing purpose")
        if beat_duration > 20:
            errors.append(f"{label}: {beat_duration:.2f}s exceeds the 20s maximum semantic beat span")

        spoken = beat.get("narration")
        if not isinstance(spoken, str) or not spoken.strip():
            errors.append(f"{label}: narration must be non-empty")
            spoken = ""
        narration_parts.append(spoken)
        anchor = beat.get("sync_anchor")
        if not isinstance(anchor, str) or len(words(anchor)) < 2 or normalized(anchor) not in normalized(spoken):
            errors.append(f"{label}: sync_anchor must be a distinctive phrase inside its narration")
        else:
            anchor_key = normalized(anchor)
            if anchor_key in seen_anchors:
                errors.append(f"{label}: sync_anchor duplicates another beat: {anchor!r}")
            seen_anchors.add(anchor_key)

        for sentence in sentences(spoken):
            count = len(words(sentence))
            if count > 24:
                long_sentences += 1

        for field in (
            "visual_purpose",
            "visual_action",
            "attention_target",
            "object_before",
            "object_after",
            "composition",
            "motion_curve",
            "camera_action",
            "evidence_boundary",
        ):
            require_text(beat, field, label, errors)
        action = normalized(str(beat.get("visual_action", "")))
        action_counts[action] += 1
        composition_counts[normalized(str(beat.get("composition", "")))] += 1
        if action in STATIC_ACTIONS:
            errors.append(f"{label}: visual_action is static or text-only")
        if normalized(str(beat.get("object_before", ""))) == normalized(str(beat.get("object_after", ""))):
            errors.append(f"{label}: object_before and object_after do not declare a state change")

        encodings = require_string_list(beat, "semantic_encodings", label, errors)
        unknown_encodings = sorted(set(encodings) - SEMANTIC_ENCODINGS)
        if unknown_encodings:
            errors.append(f"{label}: unknown semantic_encodings: {', '.join(unknown_encodings)}")

        continuity = require_string_list(beat, "continuity_objects", label, errors)
        for item in continuity:
            key = normalized(item)
            continuity_counts[key] += 1
            if persistent and key not in persistent:
                errors.append(f"{label}: continuity object {item!r} is absent from art_direction.persistent_objects")

        beat_techniques = require_string_list(beat, "animation_techniques", label, errors)
        techniques.update(beat_techniques)

        screen = require_string_list(beat, "on_screen_text", label, errors, allow_empty=True)
        screen_words = sum(len(words(item)) for item in screen)
        if screen_words > 16:
            errors.append(f"{label}: {screen_words} on-screen words exceed the 16-word beat ceiling")
        if screen and normalized(" ".join(screen)) == normalized(spoken):
            errors.append(f"{label}: on-screen text duplicates narration")

        settle = beat.get("settle_seconds", 0)
        if not isinstance(settle, (int, float)) or isinstance(settle, bool) or settle < 0:
            errors.append(f"{label}: settle_seconds must be non-negative")
            settle = 0
        if settle > beat_duration:
            errors.append(f"{label}: settle_seconds exceeds beat duration")
        if settle > 6 and not (isinstance(hold_purpose, str) and len(hold_purpose.strip()) >= 8):
            errors.append(f"{label}: settle longer than 6s requires hold_purpose")
        settle_total += settle

        concepts = require_string_list(beat, "new_concepts", label, errors, allow_empty=True)
        introduced_concepts.update(normalized(item) for item in concepts)
        if len(concepts) > 2:
            warnings.append(f"{label}: introduces {len(concepts)} concepts; consider splitting the beat")
        if len(concepts) > 4:
            errors.append(f"{label}: more than four new concepts cannot be reviewed as one semantic beat")

        if beat.get("claim_role") not in CLAIM_ROLES:
            errors.append(f"{label}: invalid claim_role {beat.get('claim_role')!r}")

        question_id = beat.get("question_id")
        if question_id is not None:
            if not isinstance(question_id, str) or not question_id.strip():
                errors.append(f"{label}: question_id must be a non-empty string")
            elif question_id in question_positions:
                errors.append(f"{label}: duplicate question_id {question_id!r}")
            else:
                question_positions[question_id] = index
                pause = beat.get("reasoning_pause_seconds", 0)
                if not isinstance(pause, (int, float)) or isinstance(pause, bool) or pause < 0:
                    errors.append(f"{label}: reasoning_pause_seconds must be non-negative")
                elif pause < 1:
                    warnings.append(f"{label}: prediction prompt allows less than one second to think")
        resolves = beat.get("resolves_question_id")
        if resolves is not None:
            if not isinstance(resolves, str) or not resolves.strip():
                errors.append(f"{label}: resolves_question_id must be a non-empty string")
            elif resolves in resolution_positions:
                errors.append(f"{label}: question {resolves!r} is resolved more than once")
            else:
                resolution_positions[resolves] = index

    present_functions = set(story_positions)
    missing_functions = sorted(REQUIRED_STORY_FUNCTIONS - present_functions)
    if missing_functions:
        errors.append("missing required story functions: " + ", ".join(missing_functions))
    if beats and isinstance(beats[0], dict) and beats[0].get("story_function") != "hook":
        errors.append("the first beat must use story_function 'hook'")
    if "mechanism" in story_positions and "payoff" in story_positions:
        if story_positions["payoff"][0] <= story_positions["mechanism"][0]:
            errors.append("the payoff must follow the first mechanism beat")
    if "mechanism" in story_positions and "evidence_boundary" in story_positions:
        if story_positions["evidence_boundary"][0] <= story_positions["mechanism"][0]:
            errors.append("the evidence boundary must follow the first mechanism beat")
    if len(story_positions.get("evidence_boundary", [])) > 2:
        errors.append("use one natural evidence boundary, or at most two when the mechanism genuinely needs separate limits")
    if len(introduced_concepts) > 3:
        errors.append(
            f"beat plan introduces {len(introduced_concepts)} distinct concepts; the visual-abstract budget is three"
        )
    if story_positions.get("handoff"):
        warnings.append("handoff beat is optional; remove chapter navigation or publication language from narration")

    for question_id, position in question_positions.items():
        resolved_at = resolution_positions.get(question_id)
        if resolved_at is None:
            errors.append(f"question {question_id!r} is never resolved")
        elif resolved_at <= position:
            errors.append(f"question {question_id!r} resolves before or at its prompt")
    for question_id in resolution_positions.keys() - question_positions.keys():
        errors.append(f"resolution refers to unknown question {question_id!r}")

    if abs(previous_end - duration) > 0.25:
        errors.append(f"final beat ends at {previous_end:.3f}s, not target duration {duration:.3f}s")
    beat_rate = len(beats) / duration * 60
    if beat_rate < 8 or beat_rate > 14:
        warnings.append(
            f"semantic beat density is {beat_rate:.2f}/min; inspect pacing against the usual 8–14/min range"
        )
    if beat_rate < 3 or beat_rate > 20:
        errors.append(f"semantic beat density of {beat_rate:.2f}/min is an extreme pacing outlier")
    if len(techniques) < 4:
        warnings.append(
            f"only {len(techniques)} animation techniques declared; review visual variety, "
            "but do not add a technique without semantic purpose"
        )
    if settle_total / duration > 0.35:
        warnings.append(f"declared settling occupies {settle_total / duration:.1%} of duration; review momentum")

    if beats:
        dominant_action = action_counts.most_common(1)[0]
        dominant_composition = composition_counts.most_common(1)[0]
        if dominant_action[1] / len(beats) > 0.35:
            warnings.append(f"one visual_action repeats across {dominant_action[1] / len(beats):.1%} of beats")
        if dominant_composition[1] / len(beats) > 0.35:
            warnings.append(f"one composition description repeats across {dominant_composition[1] / len(beats):.1%} of beats")
        if continuity_counts:
            dominant_object, count = continuity_counts.most_common(1)[0]
            if count / len(beats) < 0.5:
                warnings.append(
                    f"no persistent object spans half the beats; strongest is {dominant_object!r} at {count / len(beats):.1%}"
                )

    full_narration = "\n\n".join(narration_parts)
    audio_direction = plan.get("audio_direction")
    duration_rationale = audio_direction.get("duration_rationale") if isinstance(audio_direction, dict) else None
    script_errors, script_warnings, script_summary = audit_narration(
        full_narration,
        duration_seconds=duration,
        duration_rationale=duration_rationale,
    )
    errors.extend(script_errors)
    warnings.extend(script_warnings)
    if narration is not None and normalized(narration) != normalized(full_narration):
        errors.append("beat narration does not exactly cover the supplied narration file after normalization")

    summary = {
        "beats": len(beats),
        "duration_seconds": round(duration, 3),
        "beats_per_minute": round(beat_rate, 2),
        **script_summary,
        "animation_technique_count": len(techniques),
        "declared_settle_fraction": round(settle_total / duration, 4),
        "beat_long_sentence_warning_count": long_sentences,
        "story_function_counts": dict(
            Counter(beat.get("story_function") for beat in beats if isinstance(beat, dict))
        ),
        "persistent_object_coverage": {
            key: round(count / len(beats), 3) for key, count in continuity_counts.most_common()
        },
    }
    return errors, warnings, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path, nargs="?")
    parser.add_argument("--narration", type=Path)
    parser.add_argument(
        "--narration-only",
        action="store_true",
        help="audit a narration file before a timed beat plan exists",
    )
    parser.add_argument(
        "--all-narrations",
        type=Path,
        metavar="ROOT",
        help="audit every generation-2/narration.txt below ROOT",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.all_narrations is not None:
        paths = sorted(args.all_narrations.glob("*/generation-2/narration.txt"))
        if not paths:
            raise SystemExit(f"No generation-2 narrations found below {args.all_narrations}")
        failures = 0
        rows = []
        for path in paths:
            try:
                narration = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise SystemExit(f"Unable to read {path}: {exc}") from exc
            errors, warnings, summary = audit_narration(narration)
            failures += bool(errors)
            rows.append({
                "chapter_id": path.parents[1].name,
                "path": str(path),
                "status": "revise" if errors else "pass",
                "errors": errors,
                "warnings": warnings,
                **summary,
            })
        print(json.dumps({"narrations": len(rows), "failures": failures, "rows": rows}, indent=2))
        if failures:
            sys.exit(1)
        print(f"Narration audit passed for {len(rows)} generation-two scripts.")
        return
    if args.narration_only:
        if args.narration is None:
            parser.error("--narration is required with --narration-only")
        try:
            narration = args.narration.read_text(encoding="utf-8")
        except OSError as exc:
            raise SystemExit(f"Unable to read narration: {exc}") from exc
        errors, warnings, summary = audit_narration(narration)
        print(json.dumps(summary, indent=2))
        for warning in warnings:
            print(f"WARNING: {warning}")
        if errors:
            print("Narration audit failed:")
            for error in errors:
                print(f" - {error}")
            sys.exit(1)
        print("Narration audit passed.")
        return
    if args.plan is None:
        parser.error("plan is required unless a narration-only mode is used")
    try:
        plan = load(args.plan)
        narration = args.narration.read_text(encoding="utf-8") if args.narration else None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read inputs: {exc}") from exc
    errors, warnings, summary = audit(plan, narration)
    print(json.dumps(summary, indent=2))
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print("Beat-plan audit failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Beat-plan audit passed.")


if __name__ == "__main__":
    main()
