#!/usr/bin/env python3
"""Audit ASI Stack Manim narration, treatments, and audio-timed beat plans.

This is a structural preflight, not an aesthetic or truth judge. It rejects
known script, story, synchronization, continuity, accessibility, and claim
failures while keeping density and technique variety as diagnostics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA = "asi_stack.manim_beat_plan.v4"
TREATMENT_SCHEMA = "asi_stack.manim_treatment.v1"
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
}
REQUIRED_STORY_FUNCTIONS = {"mechanism", "evidence_boundary", "payoff"}
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
    "intentional hold",
    "display text",
    "show card",
    "fade in card",
}
TRANSFER_ACTION_RE = re.compile(
    r"\b(?:apply|choose|construct|decide|diagnose|distinguish|explain|identify|"
    r"predict|reason|recognize|test|trace)\b",
    re.I,
)
SCOPE_LIMIT_RE = re.compile(
    r"\b(?:can(?:not|'t)|do(?:es)? not|doesn't|is not evidence|not prove|"
    r"not establish|not guarantee|not demonstrate)\b",
    re.I,
)
CONTENT_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "but", "by",
    "can", "could", "for", "from", "has", "have", "how", "in", "into",
    "is", "it", "its", "may", "must", "not", "of", "on", "or", "should",
    "that", "the", "their", "then", "this", "to", "viewer", "when", "which",
    "will", "with",
}


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", text)


def normalized(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower()))


def collapsed(text: str) -> str:
    return " ".join(text.split())


def sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", text.strip()) if item.strip()]


def content_tokens(text: str) -> list[str]:
    return [token for token in normalized(text).split() if token not in CONTENT_STOPWORDS]


def token_jaccard(left: str, right: str) -> float:
    left_tokens = set(content_tokens(left))
    right_tokens = set(content_tokens(right))
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def near_duplicate_pairs(values: list[str], threshold: float = 0.72) -> list[dict]:
    pairs = []
    for left_index, right_index in combinations(range(len(values)), 2):
        score = token_jaccard(values[left_index], values[right_index])
        if score >= threshold:
            pairs.append({
                "left": left_index,
                "right": right_index,
                "content_token_jaccard": round(score, 3),
            })
    return pairs


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
    if not TRANSFER_ACTION_RE.search(value):
        warnings.append(
            "teaching_promise does not name an observable transfer action such as "
            "predict, explain, distinguish, apply, or diagnose"
        )
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

    script_sentences = sentences(clean)
    long_sentence_count = 0
    extreme_sentence_count = 0
    list_sentence_count = 0
    sentence_start_counts: Counter[str] = Counter()
    sentence_stem_counts: Counter[str] = Counter()
    for sentence in script_sentences:
        sentence_words = normalized(sentence).split()
        if sentence_words:
            sentence_start_counts[sentence_words[0]] += 1
            sentence_stem_counts[" ".join(sentence_words[:2])] += 1
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
    micro_blocks = 0
    for index, paragraph in enumerate(paragraphs, start=1):
        count = len(words(paragraph))
        if count < 8:
            micro_blocks += 1
        if count > 130:
            oversized_blocks += 1
            warnings.append(f"performance block {index} has {count} words; review prosody and scene load")
        if count > 180:
            errors.append(f"performance block {index} has {count} words; split it at a real thought boundary")

    if micro_blocks >= 2:
        warnings.append(
            f"narration has {micro_blocks} performance blocks below eight words; "
            "verify that emphasis justifies the likely prosody reset"
        )

    dominant_start = sentence_start_counts.most_common(1)
    if dominant_start and len(script_sentences) >= 12:
        start, count = dominant_start[0]
        share = count / len(script_sentences)
        if count >= 10 and share >= 0.30:
            warnings.append(
                f"{count} of {len(script_sentences)} sentences begin with {start!r}; "
                "listen for a mechanically repeated sentence shape"
            )
    repeated_stems = [
        (stem, count) for stem, count in sentence_stem_counts.most_common()
        if count >= 5 and count / max(len(script_sentences), 1) >= 0.12
    ]
    if repeated_stems:
        stem, count = repeated_stems[0]
        warnings.append(
            f"sentence stem {stem!r} appears {count} times; review cadence without "
            "replacing precise recurring terminology"
        )

    scope_limit_count = sum(bool(SCOPE_LIMIT_RE.search(item)) for item in script_sentences)
    tail_size = max(3, (len(script_sentences) + 3) // 4)
    tail_scope_limit_count = sum(
        bool(SCOPE_LIMIT_RE.search(item)) for item in script_sentences[-tail_size:]
    )
    if scope_limit_count >= 5 and scope_limit_count / max(len(script_sentences), 1) >= 0.15:
        warnings.append(
            f"{scope_limit_count} sentences use limitation language; keep distinct "
            "boundaries local and merge repeated disclaimers"
        )
    if tail_scope_limit_count >= 3:
        warnings.append(
            f"{tail_scope_limit_count} limitation sentences cluster in the final quarter; "
            "check whether late caveats are repairing earlier overbreadth"
        )

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
        "micro_performance_blocks": micro_blocks,
        "dominant_sentence_start": dominant_start[0][0] if dominant_start else None,
        "dominant_sentence_start_count": dominant_start[0][1] if dominant_start else 0,
        "repeated_sentence_stems": [
            {"stem": stem, "count": count} for stem, count in repeated_stems
        ],
        "scope_limit_sentence_count": scope_limit_count,
        "tail_scope_limit_sentence_count": tail_scope_limit_count,
        "question_count": question_count,
        "words_per_minute": round(wpm, 2) if wpm is not None else None,
    }


def opening_shape(narration: str) -> str:
    items = sentences(narration)
    if not items:
        return "empty"
    first = items[0].lstrip()
    tokens = normalized(first).split()
    if first.startswith(('"', "'", "“")):
        return "quoted_state"
    if first.endswith("?"):
        return "direct_question"
    if not tokens:
        return "other"
    if tokens[0] in {"imagine", "suppose", "consider", "watch", "picture"}:
        return "viewer_invitation"
    if tokens[0] in {
        "a", "an", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten",
    } or tokens[0].isdigit():
        return "counted_case_declaration"
    if tokens[0] in {"you", "your"}:
        return "direct_address"
    return "declaration"


def phrase_owners(rows: list[tuple[str, str]], size: int) -> dict[str, set[str]]:
    owners: dict[str, set[str]] = {}
    for chapter_id, narration in rows:
        tokens = normalized(narration).split()
        phrases = {
            " ".join(tokens[index:index + size])
            for index in range(max(0, len(tokens) - size + 1))
        }
        for phrase in phrases:
            if len(content_tokens(phrase)) >= 2:
                owners.setdefault(phrase, set()).add(chapter_id)
    return owners


def duplicate_edge_stems(
    rows: list[tuple[str, str]], *, opening: bool, size: int = 5
) -> list[dict]:
    owners: dict[str, set[str]] = {}
    for chapter_id, narration in rows:
        items = sentences(narration)
        if not items:
            continue
        tokens = normalized(items[0] if opening else items[-1]).split()
        if len(tokens) < size:
            continue
        stem = " ".join(tokens[:size] if opening else tokens[-size:])
        owners.setdefault(stem, set()).add(chapter_id)
    return [
        {"stem": stem, "chapters": sorted(chapters)}
        for stem, chapters in sorted(owners.items())
        if len(chapters) > 1
    ]


def audit_series_narrations(rows: list[tuple[str, str]]) -> dict:
    """Locate possible series templating without treating novelty as quality."""

    shape_counts = Counter(opening_shape(narration) for _, narration in rows)
    six_word_owners = phrase_owners(rows, 6)
    eight_word_owners = phrase_owners(rows, 8)
    shared_six_word_phrases = [
        {"phrase": phrase, "chapters": sorted(chapters)}
        for phrase, chapters in sorted(
            six_word_owners.items(), key=lambda item: (-len(item[1]), item[0])
        )
        if len(chapters) > 1
    ][:30]
    material_reuse_phrases = [
        {"phrase": phrase, "chapters": sorted(chapters)}
        for phrase, chapters in sorted(
            eight_word_owners.items(), key=lambda item: (-len(item[1]), item[0])
        )
        if len(chapters) > 1
    ][:20]
    duplicate_openings = duplicate_edge_stems(rows, opening=True)
    duplicate_closings = duplicate_edge_stems(rows, opening=False)
    word_counts = [len(words(narration)) for _, narration in rows]
    paragraph_counts = [
        len([item for item in re.split(r"\n\s*\n", narration.strip()) if item.strip()])
        for _, narration in rows
    ]

    warnings = []
    if rows:
        dominant_shape, dominant_count = shape_counts.most_common(1)[0]
        if len(rows) >= 8 and dominant_count / len(rows) >= 0.75:
            warnings.append(
                f"opening shape {dominant_shape!r} appears in {dominant_count} of "
                f"{len(rows)} scripts; compare openings for noun-swapped templating"
            )
    if material_reuse_phrases:
        warnings.append(
            f"{len(material_reuse_phrases)} exact eight-word phrase(s) recur across scripts; "
            "retain only intentional terminology or callbacks"
        )
    if duplicate_openings:
        warnings.append(
            f"{len(duplicate_openings)} exact five-word opening stem(s) recur across scripts"
        )
    if duplicate_closings:
        warnings.append(
            f"{len(duplicate_closings)} exact five-word closing stem(s) recur across scripts"
        )

    return {
        "scope": "diagnostic_not_quality_score",
        "narrations": len(rows),
        "review_triggers": warnings,
        "opening_shape_counts": dict(shape_counts),
        "word_count_range": [min(word_counts), max(word_counts)] if word_counts else None,
        "paragraph_count_range": (
            [min(paragraph_counts), max(paragraph_counts)] if paragraph_counts else None
        ),
        "shared_six_word_phrases": shared_six_word_phrases,
        "material_reuse_phrases": material_reuse_phrases,
        "duplicate_opening_stems": duplicate_openings,
        "duplicate_closing_stems": duplicate_closings,
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


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def schema_errors(value: dict, filename: str, label: str) -> list[str]:
    candidates = [Path.cwd() / "schemas" / filename]
    candidates.extend(parent / "schemas" / filename for parent in Path(__file__).resolve().parents)
    path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if path is None:
        return [f"{label} schema {filename} is unavailable; complete audit fails closed"]
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{label} schema is unreadable: {exc}"]
    return [
        f"{label}-schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(value)
    ]


def find_repository_root() -> Path | None:
    candidates = [Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents]
    return next((path for path in candidates if (path / "book_structure.json").is_file()), None)


def repository_treatment_errors(treatment: dict) -> list[str]:
    root = find_repository_root()
    if root is None:
        return ["ASI Stack repository truth surfaces are unavailable; treatment audit fails closed"]
    try:
        structure = json.loads((root / "book_structure.json").read_text(encoding="utf-8"))
        inventory = json.loads((root / "sources/source_inventory.json").read_text(encoding="utf-8"))
        substance = json.loads((root / "evidence_quality/chapter_substance_contract.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"repository truth surfaces are unreadable: {exc}"]
    chapter_id = treatment.get("chapter_id")
    chapter = next(
        (
            row for part in structure.get("parts", []) for row in part.get("chapters", [])
            if row.get("id") == chapter_id
        ),
        None,
    )
    if chapter is None:
        return [f"treatment chapter_id {chapter_id!r} is absent from canonical structure"]
    errors: list[str] = []
    chapter_path = root / chapter["file"]
    if not chapter_path.is_file() or hashlib.sha256(chapter_path.read_bytes()).hexdigest() != treatment.get("chapter_sha256"):
        errors.append("treatment chapter_sha256 does not bind the current canonical chapter")

    source_commit = treatment.get("source_commit")

    def committed_blob(relative: str) -> bytes | None:
        if not isinstance(source_commit, str) or len(source_commit) != 40:
            return None
        try:
            completed = subprocess.run(
                ["git", "show", f"{source_commit}:{relative}"],
                cwd=root,
                capture_output=True,
                check=False,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return None
        return completed.stdout if completed.returncode == 0 else None

    committed_chapter = committed_blob(chapter["file"])
    if committed_chapter is None:
        errors.append("treatment source_commit does not resolve to its canonical chapter")
    elif hashlib.sha256(committed_chapter).hexdigest() != treatment.get("chapter_sha256"):
        errors.append("treatment source_commit does not reproduce the canonical chapter")
    source_bindings = []
    inventory_by_id = {
        row["id"]: row for row in inventory
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    for source_id in chapter.get("source_ids", []):
        relative = f"sources/source_notes/{source_id}.md"
        path = root / relative
        if not path.is_file():
            errors.append(f"assigned source note is missing: {relative}")
            continue
        source_bindings.append({
            "source_id": source_id,
            "inventory_record": inventory_by_id.get(source_id),
            "note_path": relative,
            "note_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    source_body = json.dumps(
        source_bindings, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    expected_source_context = hashlib.sha256(source_body.encode("utf-8")).hexdigest()
    if treatment.get("source_context_sha256") != expected_source_context:
        errors.append("treatment source_context_sha256 does not bind the assigned source-note bundle")
    committed_inventory_blob = committed_blob("sources/source_inventory.json")
    committed_source_bindings = []
    if committed_inventory_blob is None:
        errors.append("treatment source_commit does not contain the source inventory")
    else:
        try:
            committed_inventory_rows = json.loads(committed_inventory_blob.decode("utf-8"))
            committed_inventory = {
                row["id"]: row for row in committed_inventory_rows
                if isinstance(row, dict) and isinstance(row.get("id"), str)
            }
        except (UnicodeDecodeError, json.JSONDecodeError):
            committed_inventory = {}
            errors.append("treatment source_commit contains an unreadable source inventory")
        for source_id in chapter.get("source_ids", []):
            relative = f"sources/source_notes/{source_id}.md"
            note = committed_blob(relative)
            if note is None:
                errors.append(f"treatment source_commit lacks assigned source note: {relative}")
                continue
            committed_source_bindings.append({
                "source_id": source_id,
                "inventory_record": committed_inventory.get(source_id),
                "note_path": relative,
                "note_sha256": hashlib.sha256(note).hexdigest(),
            })
        committed_body = json.dumps(
            committed_source_bindings,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        committed_context = hashlib.sha256(committed_body.encode("utf-8")).hexdigest()
        if committed_context != treatment.get("source_context_sha256"):
            errors.append("treatment source_commit does not reproduce the assigned source context")
    contract = treatment.get("content_contract", {})
    if not isinstance(contract, dict):
        return errors
    declared_sources = set(contract.get("source_ids", []))
    assigned_sources = set(chapter.get("source_ids", []))
    inventory_ids = {
        row.get("id") for row in inventory
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    unknown_sources = sorted(declared_sources - assigned_sources)
    if unknown_sources:
        errors.append("treatment cites sources not assigned to this chapter: " + ", ".join(unknown_sources))
    absent_sources = sorted(declared_sources - inventory_ids)
    if absent_sources:
        errors.append("treatment cites source IDs absent from inventory: " + ", ".join(absent_sources))
    chapter_record = next(
        (
            row for row in substance.get("chapter_records", [])
            if row.get("chapter_id") == chapter_id
        ),
        None,
    )
    allowed_claims = {
        row.get("atom_id") for row in (chapter_record or {}).get("atom_refs", [])
        if isinstance(row, dict) and isinstance(row.get("atom_id"), str)
    }
    if not allowed_claims:
        errors.append("canonical chapter substance contract supplies no claim atoms")
    unknown_claims = sorted(set(contract.get("chapter_claim_ids", [])) - allowed_claims)
    if unknown_claims:
        errors.append("treatment invents or cross-owns claim IDs: " + ", ".join(unknown_claims))
    art = treatment.get("art_direction", {})
    assets = art.get("asset_plan", []) if isinstance(art, dict) else []
    for index, asset in enumerate(assets if isinstance(assets, list) else []):
        if not isinstance(asset, dict) or asset.get("status") == "planned":
            continue
        relative = asset.get("path_or_source")
        path = (root / relative).resolve() if isinstance(relative, str) else None
        if path is None:
            errors.append(f"asset_plan[{index}] has no local cleared asset path")
            continue
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"asset_plan[{index}] cleared asset escapes the repository")
            continue
        if not path.is_file():
            errors.append(f"asset_plan[{index}] cleared asset is missing")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != asset.get("sha256"):
            errors.append(f"asset_plan[{index}] cleared asset digest drift")
    return errors


def audit_treatment(
    treatment: dict,
    narration: str | None,
    *,
    repository_check: bool = True,
) -> tuple[list[str], list[str], dict]:
    """Audit the source-bound editorial treatment and recorded script gate."""

    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(schema_errors(treatment, "manim_treatment.schema.json", "treatment"))
    if repository_check:
        errors.extend(repository_treatment_errors(treatment))
    if treatment.get("schema_version") != TREATMENT_SCHEMA:
        errors.append(f"treatment schema_version must be {TREATMENT_SCHEMA}")
    for field in ("chapter_id", "chapter_sha256", "source_commit", "selection_rationale"):
        require_text(treatment, field, "treatment", errors)
    digest = treatment.get("chapter_sha256", "")
    if digest and not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append("treatment.chapter_sha256 must be 64 lowercase hexadecimal characters")

    promise_errors, promise_warnings = audit_teaching_promise(treatment.get("teaching_promise"))
    errors.extend(promise_errors)
    warnings.extend(promise_warnings)
    selected_promise = normalized(str(treatment.get("teaching_promise", "")))

    candidates = treatment.get("promise_candidates")
    selected_candidates: list[str] = []
    candidate_promises: list[str] = []
    candidate_promise_texts: list[str] = []
    candidate_mechanisms: list[str] = []
    if not isinstance(candidates, list) or not 3 <= len(candidates) <= 5:
        errors.append("treatment.promise_candidates must contain three to five compared candidates")
    else:
        for index, candidate in enumerate(candidates):
            label = f"promise_candidates[{index}]"
            if not isinstance(candidate, dict):
                errors.append(f"{label} must be an object")
                continue
            for field in (
                "promise",
                "consequence",
                "visual_mechanism",
                "transfer_value",
                "evidence_fit",
                "rationale",
            ):
                require_text(candidate, field, label, errors)
            promise_text = str(candidate.get("promise", "")).strip()
            value = normalized(promise_text)
            candidate_promises.append(value)
            candidate_promise_texts.append(promise_text)
            candidate_mechanisms.append(str(candidate.get("visual_mechanism", "")).strip())
            if candidate.get("disposition") == "selected":
                selected_candidates.append(value)
            elif candidate.get("disposition") != "rejected":
                errors.append(f"{label}.disposition must be selected or rejected")
        if len(set(candidate_promises)) != len(candidate_promises):
            errors.append("treatment.promise_candidates must be meaningfully distinct")
        near_promises = near_duplicate_pairs(candidate_promise_texts)
        if near_promises:
            warnings.append(
                "promise candidates share most content words at pairs "
                + ", ".join(
                    f"{row['left'] + 1}/{row['right'] + 1}"
                    for row in near_promises
                )
                + "; compare genuinely different viewer outcomes"
            )
        near_mechanisms = near_duplicate_pairs(candidate_mechanisms)
        if near_mechanisms:
            warnings.append(
                "candidate visual mechanisms are near-duplicates at pairs "
                + ", ".join(
                    f"{row['left'] + 1}/{row['right'] + 1}"
                    for row in near_mechanisms
                )
                + "; sketch materially different explanatory mechanisms"
            )
        if selected_candidates != [selected_promise]:
            errors.append("exactly one candidate must select the exact teaching_promise")

    audience = treatment.get("audience")
    introduced_terms: set[str] = set()
    if not isinstance(audience, dict):
        errors.append("treatment.audience must be an object")
    else:
        for field in ("target_viewer", "standalone_context"):
            require_text(audience, field, "audience", errors)
        require_string_list(audience, "assumed_knowledge", "audience", errors, allow_empty=True)
        require_string_list(audience, "excluded_assumptions", "audience", errors)
        terms = require_string_list(audience, "introduced_terms", "audience", errors, allow_empty=True)
        introduced_terms = {normalized(item) for item in terms}
        if len(introduced_terms) > 3:
            errors.append("audience.introduced_terms exceeds the three-term budget")

    contract = treatment.get("content_contract")
    authority_refs: set[str] = set()
    truth_check_count = 0
    if not isinstance(contract, dict):
        errors.append("treatment.content_contract must be an object")
    else:
        claim_ids = require_string_list(contract, "chapter_claim_ids", "content_contract", errors)
        source_ids = require_string_list(contract, "source_ids", "content_contract", errors)
        authority_refs = set(claim_ids + source_ids)
        require_string_list(contract, "non_claims", "content_contract", errors)
        require_string_list(contract, "case_assumptions", "content_contract", errors)
        require_string_list(contract, "visual_simplifications", "content_contract", errors, allow_empty=True)
        notation = contract.get("notation_ledger")
        if not isinstance(notation, list):
            errors.append("content_contract.notation_ledger must be a list")
        elif len({normalized(str(row.get("token", ""))) for row in notation if isinstance(row, dict)}) != len(notation):
            errors.append("content_contract.notation_ledger tokens must be unique")
        truth_checks = contract.get("truth_checks")
        if not isinstance(truth_checks, list) or not truth_checks:
            errors.append("content_contract.truth_checks must contain at least one completed check")
        else:
            truth_check_count = len(truth_checks)
            for index, row in enumerate(truth_checks):
                label = f"truth_checks[{index}]"
                if not isinstance(row, dict):
                    errors.append(f"{label} must be an object")
                    continue
                require_text(row, "statement", label, errors)
                refs = require_string_list(row, "authority_refs", label, errors)
                unknown = sorted(set(refs) - authority_refs)
                if unknown:
                    errors.append(f"{label} cites refs outside the content contract: {', '.join(unknown)}")
                if row.get("result") != "pass":
                    errors.append(f"{label} must pass before its statement enters narration")

    story = treatment.get("story")
    macro_ids: list[str] = []
    if not isinstance(story, dict):
        errors.append("treatment.story must be an object")
    else:
        for field in (
            "concrete_case", "payoff", "comprehension_question", "transfer_question",
        ):
            require_text(story, field, "story", errors)
        opening_question = story.get("opening_question")
        if opening_question is not None:
            require_text(story, "opening_question", "story", errors)
        story_form = story.get("story_form")
        basis = story.get("story_basis")
        basis_required = story_form in {
            "failure_diagnosis", "comparison", "counterexample",
            "open_question", "hybrid",
        }
        if basis_required and not isinstance(basis, dict):
            errors.append("story.story_basis must bind the selected story form to authority")
        if isinstance(basis, dict):
            require_text(basis, "description", "story.story_basis", errors)
            basis_refs = require_string_list(
                basis, "authority_refs", "story.story_basis", errors
            )
            unknown = sorted(set(basis_refs) - authority_refs)
            if unknown:
                errors.append(
                    "story.story_basis cites refs outside the content contract: "
                    + ", ".join(unknown)
                )
        require_string_list(story, "comprehension_success_criteria", "story", errors)
        require_string_list(story, "transfer_success_criteria", "story", errors)
        moves = story.get("macro_moves")
        if not isinstance(moves, list) or not 3 <= len(moves) <= 7:
            errors.append("story.macro_moves must contain three to seven mental-model changes")
        else:
            for index, move in enumerate(moves):
                label = f"macro_moves[{index}]"
                if not isinstance(move, dict):
                    errors.append(f"{label} must be an object")
                    continue
                macro_id = move.get("id")
                if not isinstance(macro_id, str):
                    errors.append(f"{label}.id must be a string")
                    continue
                macro_ids.append(macro_id)
                require_text(move, "purpose", label, errors)
                before = require_text(move, "viewer_model_before", label, errors)
                require_text(move, "visible_event", label, errors)
                after = require_text(move, "viewer_model_after", label, errors)
                if before and after and normalized(before) == normalized(after):
                    errors.append(f"{label} does not change the viewer's model")
            expected = [f"m{index:02d}" for index in range(1, len(macro_ids) + 1)]
            if macro_ids != expected:
                errors.append("story.macro_moves must use unique ordered ids m01..mNN")

    for brief_name, fields in {
        "packaging": (
            "working_title",
            "thumbnail_concept",
            "thumbnail_alt_text",
            "promise_match",
            "first_fifteen_seconds_delivery",
            "source_delivery",
        ),
        "accessibility": (
            "color_redundancy",
            "motion_redundancy",
            "integrated_description",
            "caption_plan",
            "descriptive_transcript_plan",
            "reduced_motion_assessment",
            "caption_safe_composition",
        ),
    }.items():
        brief = treatment.get(brief_name)
        if not isinstance(brief, dict):
            errors.append(f"treatment.{brief_name} must be an object")
            continue
        for field in fields:
            require_text(brief, field, brief_name, errors)
        if brief_name == "packaging":
            refs = require_string_list(brief, "source_delivery_refs", "packaging", errors)
            unknown = sorted(set(refs) - authority_refs)
            if unknown:
                errors.append(
                    "packaging.source_delivery_refs are outside the content contract: "
                    + ", ".join(unknown)
                )

    art = treatment.get("art_direction")
    persistent: set[str] = set()
    keyframe_count = 0
    medium = None
    if not isinstance(art, dict):
        errors.append("treatment.art_direction must be an object")
    else:
        medium = art.get("medium")
        for field in (
            "medium_rationale",
            "visual_thesis",
            "signature_image",
            "visual_world",
            "composition_rule",
            "palette_rule",
            "typography_rule",
            "motion_character",
            "camera_rule",
            "surface_rule",
            "ending_image",
        ):
            require_text(art, field, "art_direction", errors)
        persistent_rows = require_string_list(art, "persistent_objects", "art_direction", errors)
        persistent = {normalized(item) for item in persistent_rows}
        require_string_list(art, "visual_invariants", "art_direction", errors)
        keyframes = art.get("semantic_keyframes")
        if not isinstance(keyframes, list) or not 3 <= len(keyframes) <= 9:
            errors.append("art_direction.semantic_keyframes must contain three to nine sparse states")
        else:
            keyframe_count = len(keyframes)
            seen_keyframes: set[str] = set()
            keyframe_id_sequence: list[str] = []
            after_moves: list[str] = []
            for index, keyframe in enumerate(keyframes):
                label = f"semantic_keyframes[{index}]"
                if not isinstance(keyframe, dict):
                    errors.append(f"{label} must be an object")
                    continue
                keyframe_id = keyframe.get("id")
                if keyframe_id in seen_keyframes:
                    errors.append(f"duplicate semantic keyframe id {keyframe_id!r}")
                seen_keyframes.add(str(keyframe_id))
                keyframe_id_sequence.append(str(keyframe_id))
                after = keyframe.get("after_macro_move_id")
                if after is not None and after not in macro_ids:
                    errors.append(f"{label} refers to unknown macro move {after!r}")
                elif after is not None:
                    after_moves.append(after)
                for field in ("focal_state", "visible_invariant"):
                    require_text(keyframe, field, label, errors)
            expected_keyframes = [f"k{index:02d}" for index in range(1, len(keyframes) + 1)]
            if keyframe_id_sequence != expected_keyframes:
                errors.append("semantic keyframes must use unique ordered ids k01..kNN")
            compact_after = [
                value for index, value in enumerate(after_moves)
                if index == 0 or value != after_moves[index - 1]
            ]
            if compact_after != macro_ids:
                errors.append("semantic keyframes must cover every macro move in story order")
        assets = art.get("asset_plan")
        if not isinstance(assets, list):
            errors.append("art_direction.asset_plan must be a list")
        else:
            asset_ids = [row.get("asset_id") for row in assets if isinstance(row, dict)]
            if len(set(asset_ids)) != len(asset_ids):
                errors.append("art_direction.asset_plan asset_id values must be unique")
            if art.get("medium") != "manim_primary" and not assets:
                errors.append("a non-Manim-primary treatment must identify every planned external asset")

    audio = treatment.get("audio_direction")
    performance_ids: list[str] = []
    performance_move_ids: list[str] = []
    if not isinstance(audio, dict):
        errors.append("treatment.audio_direction must be an object")
    else:
        for field in ("narration_style", "pacing_arc", "music_policy", "sound_effect_policy"):
            require_text(audio, field, "audio_direction", errors)
        require_string_list(audio, "review_devices", "audio_direction", errors)
        blocks = audio.get("performance_blocks")
        if not isinstance(blocks, list) or not blocks:
            errors.append("audio_direction.performance_blocks must be a non-empty list")
        else:
            for index, block in enumerate(blocks):
                label = f"performance_blocks[{index}]"
                if not isinstance(block, dict):
                    errors.append(f"{label} must be an object")
                    continue
                performance_ids.append(str(block.get("id", "")))
                performance_move_ids.extend(require_string_list(block, "macro_move_ids", label, errors))
                require_text(block, "performance_direction", label, errors)
                require_string_list(block, "pronunciation_items", label, errors, allow_empty=True)
            if len(set(performance_ids)) != len(performance_ids):
                errors.append("audio_direction.performance_blocks ids must be unique")
            if performance_move_ids != macro_ids:
                errors.append("performance blocks must cover each macro move exactly once and in story order")

    gate = treatment.get("script_gate")
    script_passed = False
    if not isinstance(gate, dict):
        errors.append("treatment.script_gate must be an object")
    else:
        require_text(gate, "narration_path", "script_gate", errors)
        if narration is not None:
            expected_digest = sha256_text(narration)
            if gate.get("narration_sha256") != expected_digest:
                errors.append("script_gate.narration_sha256 does not bind the supplied narration")
            expected_words = len(words(narration))
            if gate.get("narration_word_count") != expected_words:
                errors.append("script_gate.narration_word_count does not match the supplied narration")
            rationale = audio.get("duration_rationale") if isinstance(audio, dict) else None
            narration_errors, narration_warnings, _ = audit_narration(
                narration,
                duration_rationale=rationale,
            )
            errors.extend(f"narration:{error}" for error in narration_errors)
            warnings.extend(f"narration:{warning}" for warning in narration_warnings)
        if gate.get("verdict") == "pass":
            script_passed = True
            if medium not in {"manim_primary", "hybrid"}:
                errors.append(
                    "script_gate cannot pass with an unqualified final compositor; "
                    "the current accepted backend is ManimCE Cairo"
                )
            if narration is None:
                errors.append("script_gate cannot pass without the supplied narration")
            for field in ("read_aloud_review", "truth_review", "visualizability_review"):
                if gate.get(field) != "pass":
                    errors.append(f"script_gate passes before {field} passes")
            if not isinstance(gate.get("reviewer_id"), str) or len(gate["reviewer_id"].strip()) < 3:
                errors.append("script_gate passes without a reviewer_id")
            if gate.get("open_defects"):
                errors.append("script_gate passes with open defects")
        elif gate.get("verdict") == "revise" and not gate.get("open_defects"):
            errors.append("script_gate revise verdict must own at least one concrete defect")

    return errors, warnings, {
        "promise_candidates": len(candidates) if isinstance(candidates, list) else 0,
        "introduced_terms": len(introduced_terms),
        "authority_refs": len(authority_refs),
        "truth_checks": truth_check_count,
        "macro_moves": len(macro_ids),
        "persistent_objects": len(persistent),
        "semantic_keyframes": keyframe_count,
        "performance_blocks": len(performance_ids),
        "script_gate_passed": script_passed,
    }


def audit(
    plan: dict,
    narration: str | None,
    treatment: dict | None,
    *,
    treatment_text: str | None = None,
    repository_check: bool = True,
) -> tuple[list[str], list[str], dict]:
    """Audit a beat plan against the exact treatment and narration it implements."""

    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(schema_errors(plan, "manim_beat_plan.schema.json", "beat-plan"))
    if plan.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must be {SCHEMA}")
    for field in ("chapter_id", "chapter_sha256", "source_commit"):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            errors.append(f"missing non-empty {field}")
    digest = plan.get("chapter_sha256", "")
    if digest and not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append("chapter_sha256 must be 64 lowercase hexadecimal characters")

    treatment_summary: dict = {}
    macro_ids: list[str] = []
    performance_for_move: dict[str, str] = {}
    authority_refs: set[str] = set()
    permitted_terms: set[str] = set()
    persistent: set[str] = set()
    if not isinstance(treatment, dict):
        errors.append("a treatment is required for every v4 beat plan")
    else:
        treatment_errors, treatment_warnings, treatment_summary = audit_treatment(
            treatment, narration, repository_check=repository_check
        )
        errors.extend(f"treatment:{error}" for error in treatment_errors)
        warnings.extend(f"treatment:{warning}" for warning in treatment_warnings)
        for field in ("chapter_id", "chapter_sha256", "source_commit"):
            if plan.get(field) != treatment.get(field):
                errors.append(f"plan.{field} does not match treatment.{field}")
        if treatment.get("script_gate", {}).get("verdict") != "pass":
            errors.append("a beat plan cannot pass before the treatment script_gate passes")
        if treatment_text is not None and plan.get("treatment_sha256") != sha256_text(treatment_text):
            errors.append("treatment_sha256 does not bind the supplied treatment file")
        if narration is not None and plan.get("narration_sha256") != sha256_text(narration):
            errors.append("narration_sha256 does not bind the supplied narration file")
        story = treatment.get("story", {})
        macro_ids = [row.get("id") for row in story.get("macro_moves", []) if isinstance(row, dict)]
        for block in treatment.get("audio_direction", {}).get("performance_blocks", []):
            if isinstance(block, dict):
                for move in block.get("macro_move_ids", []):
                    performance_for_move[move] = block.get("id")
        contract = treatment.get("content_contract", {})
        authority_refs = set(contract.get("chapter_claim_ids", []) + contract.get("source_ids", []))
        permitted_terms = {normalized(item) for item in treatment.get("audience", {}).get("introduced_terms", [])}
        persistent = {normalized(item) for item in treatment.get("art_direction", {}).get("persistent_objects", [])}

    duration = plan.get("target_duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        errors.append("target_duration_seconds must be positive")
        duration = 1.0
    elif not 150 <= duration <= 270:
        warnings.append("target duration falls outside the preferred 2.5–4.5 minute visual-abstract range")
    if isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration > 270:
        audio_direction = treatment.get("audio_direction") if isinstance(treatment, dict) else None
        rationale = audio_direction.get("duration_rationale") if isinstance(audio_direction, dict) else None
        if not isinstance(rationale, str) or len(rationale.strip()) < 24:
            errors.append(
                "audio_direction.duration_rationale must explain why a video above the normal 4.5-minute target improves the teaching result"
            )

    timing = plan.get("timing")
    timing_state = None
    timing_contract = {
        "estimated": ("editorial_estimate", False, False),
        "block_timed": ("synthesis_receipt", True, False),
        "forced_aligned": ("forced_alignment_receipt", True, True),
    }
    if not isinstance(timing, dict) or timing.get("state") not in timing_contract:
        errors.append("timing.state must be estimated, block_timed, or forced_aligned")
    else:
        timing_state = timing["state"]
        expected_source, needs_receipt, needs_alignment = timing_contract[timing_state]
        if timing.get("source") != expected_source:
            errors.append(f"timing state {timing_state} requires source {expected_source}")
        receipt_fields = ("receipt_path", "receipt_sha256")
        narration_custody_fields = (
            "narration_receipt_path", "narration_receipt_sha256",
            "narration_verification_report_path",
            "narration_verification_report_sha256",
        )
        alignment_identity_fields = (
            "aligner_id", "manual_anchor_review_path", "manual_anchor_review_sha256",
            "manual_anchor_reviewer_id", "manual_anchor_count",
        )
        if needs_receipt and not all(timing.get(field) for field in receipt_fields):
            errors.append(f"timing state {timing_state} requires a bound timing receipt")
        if not needs_receipt and any(timing.get(field) is not None for field in receipt_fields):
            errors.append("estimated timing must not pretend to have a synthesis receipt")
        if needs_receipt and not all(timing.get(field) for field in narration_custody_fields):
            errors.append(f"timing state {timing_state} requires bound narration and verification receipts")
        if not needs_receipt and any(
            timing.get(field) is not None for field in narration_custody_fields
        ):
            errors.append("estimated timing must not pretend to have verified narration custody")
        if timing_state == "block_timed" and (
            timing.get("receipt_path") != timing.get("narration_receipt_path")
            or timing.get("receipt_sha256") != timing.get("narration_receipt_sha256")
        ):
            errors.append("block_timed timing receipt must be the bound narration render receipt")
        if needs_alignment and (
            not all(timing.get(field) for field in alignment_identity_fields)
            or timing.get("manual_anchor_failures") != 0
        ):
            errors.append(
                "forced_aligned timing requires an aligner and a zero-failure bound manual anchor review"
            )
        if not needs_alignment and any(
            timing.get(field) is not None
            for field in alignment_identity_fields + ("manual_anchor_failures",)
        ):
            errors.append(f"timing state {timing_state} must not claim forced-alignment review")

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
    introduced_terms: set[str] = set()
    macro_sequence: list[str] = []

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

        macro_move_id = beat.get("macro_move_id")
        if macro_move_id not in macro_ids:
            errors.append(f"{label}: unknown macro_move_id {macro_move_id!r}")
        else:
            macro_sequence.append(macro_move_id)
            expected_block = performance_for_move.get(macro_move_id)
            if beat.get("performance_block_id") != expected_block:
                errors.append(
                    f"{label}: performance_block_id must be {expected_block!r} for {macro_move_id}"
                )

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
            warnings.append(
                f"{label}: {beat_duration:.2f}s is an unusually long semantic beat; "
                "use mux-checked scene-internal cue windows for multiple pivotal events "
                "instead of whole-block interpolation, then inspect full-speed attention "
                "and learner control"
            )

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
        mode = beat.get("mode")
        same_state = normalized(str(beat.get("object_before", ""))) == normalized(
            str(beat.get("object_after", ""))
        )
        if mode == "change":
            if action in STATIC_ACTIONS:
                errors.append(f"{label}: change beat uses a static or text-only visual_action")
            if same_state:
                errors.append(f"{label}: change beat does not declare a state change")
        elif mode == "hold":
            if not same_state:
                errors.append(f"{label}: hold beat changes state; declare mode change instead")
            if not isinstance(hold_purpose, str) or len(hold_purpose.strip()) < 8:
                errors.append(f"{label}: intentional hold requires a specific hold_purpose")
        else:
            errors.append(f"{label}: mode must be change or hold")

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

        beat_techniques = require_string_list(
            beat, "animation_techniques", label, errors, allow_empty=(mode == "hold")
        )
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

        terms = require_string_list(beat, "introduced_terms", label, errors, allow_empty=True)
        term_keys = {normalized(item) for item in terms}
        introduced_terms.update(term_keys)
        unknown_terms = sorted(term_keys - permitted_terms)
        if unknown_terms:
            errors.append(f"{label}: introduces terms absent from treatment audience contract: {', '.join(unknown_terms)}")
        if mode == "hold" and terms:
            errors.append(f"{label}: a hold may consolidate but may not introduce terminology")

        if beat.get("claim_role") not in CLAIM_ROLES:
            errors.append(f"{label}: invalid claim_role {beat.get('claim_role')!r}")

        refs = require_string_list(beat, "source_refs", label, errors)
        unknown_refs = sorted(set(refs) - authority_refs)
        if unknown_refs:
            errors.append(f"{label}: source_refs are outside the treatment contract: {', '.join(unknown_refs)}")
        require_text(beat, "visual_inference", label, errors)

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
    if "mechanism" in story_positions and "payoff" in story_positions:
        if story_positions["payoff"][0] <= story_positions["mechanism"][0]:
            errors.append("the payoff must follow the first mechanism beat")
    if "mechanism" in story_positions and "evidence_boundary" in story_positions:
        if story_positions["evidence_boundary"][0] <= story_positions["mechanism"][0]:
            errors.append("the evidence boundary must follow the first mechanism beat")
    if len(story_positions.get("evidence_boundary", [])) > 2:
        errors.append("use one natural evidence boundary, or at most two when the mechanism genuinely needs separate limits")
    if len(introduced_terms) > 3:
        errors.append(
            f"beat plan introduces {len(introduced_terms)} distinct terms; the treatment budget is three"
        )

    compact_macro_sequence = [value for index, value in enumerate(macro_sequence) if index == 0 or value != macro_sequence[index - 1]]
    if compact_macro_sequence != macro_ids:
        errors.append("beats must cover each treatment macro move once, contiguously, and in story order")

    for question_id, position in question_positions.items():
        resolved_at = resolution_positions.get(question_id)
        if resolved_at is None:
            errors.append(f"question {question_id!r} is never resolved")
        elif resolved_at <= position:
            errors.append(f"question {question_id!r} resolves before or at its prompt")
    for question_id in resolution_positions.keys() - question_positions.keys():
        errors.append(f"resolution refers to unknown question {question_id!r}")
    if len(question_positions) > 2:
        errors.append("use at most two purposeful prediction or transfer prompts")

    if abs(previous_end - duration) > 0.25:
        errors.append(f"final beat ends at {previous_end:.3f}s, not target duration {duration:.3f}s")
    beat_rate = len(beats) / duration * 60
    if beat_rate < 8 or beat_rate > 14:
        warnings.append(
            f"semantic beat density is {beat_rate:.2f}/min; inspect pacing against the usual 8–14/min range"
        )
    if len(techniques) < 3:
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
    audio_direction = treatment.get("audio_direction") if isinstance(treatment, dict) else None
    duration_rationale = audio_direction.get("duration_rationale") if isinstance(audio_direction, dict) else None
    script_errors, script_warnings, script_summary = audit_narration(
        full_narration,
        duration_seconds=duration,
        duration_rationale=duration_rationale,
    )
    errors.extend(script_errors)
    warnings.extend(script_warnings)
    if narration is None:
        errors.append("a supplied narration file is required for a v4 beat plan")
    elif collapsed(narration) != collapsed(full_narration):
        errors.append("beat narration does not exactly cover the supplied narration after whitespace folding")

    summary = {
        "beats": len(beats),
        "timing_state": timing_state,
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
        "treatment": treatment_summary,
    }
    return errors, warnings, summary


def fixture() -> tuple[dict, dict, str, str]:
    """Return a compact but realistic passing treatment, plan, and narration."""

    functions = [
        "hook", "setup", "setup", "prediction", "construction", "mechanism",
        "mechanism", "worked_trace", "worked_trace", "counterexample",
        "failure", "consequence", "mechanism", "worked_trace", "comparison",
        "counterexample", "evidence_boundary", "payoff", "mechanism", "payoff",
    ]
    macro_for = ["m01"] * 5 + ["m02"] * 5 + ["m03"] * 5 + ["m04"] * 5
    performance_for = {"m01": "p01", "m02": "p01", "m03": "p02", "m04": "p02"}
    persistent = ["request token", "authority gate", "route graph"]
    techniques = ["TransformFromCopy", "MoveAlongPath", "ValueTracker", "Circumscribe"]
    beats: list[dict] = []
    for index, function in enumerate(functions):
        marker = f"decision marker {index:02d}"
        spoken = (
            f"At {marker}, the request reveals which relation changes and why the authority gate matters now."
        )
        mode = "hold" if index == 3 else "change"
        before = f"Request before governed relation {index:02d}."
        after = before if mode == "hold" else f"Request after governed relation {index:02d}."
        beats.append({
            "id": f"b{index + 1:02d}",
            "macro_move_id": macro_for[index],
            "performance_block_id": performance_for[macro_for[index]],
            "story_function": function,
            "mode": mode,
            "start_seconds": index * 9.0,
            "end_seconds": (index + 1) * 9.0,
            "narration": spoken,
            "sync_anchor": marker,
            "visual_purpose": "Make the active authority relation predictable from the visible state.",
            "visual_action": "Intentionally hold the route for prediction" if mode == "hold" else f"Move request through relation {index:02d}",
            "attention_target": "The active edge, request token, and authority gate.",
            "semantic_encodings": ["relation", "authority"],
            "object_before": before,
            "object_after": after,
            "continuity_objects": persistent[:2],
            "composition": "Keep the active edge centered while dimming non-causal context.",
            "motion_curve": "Use a fast departure, legible travel, and settled arrival.",
            "camera_action": "Keep the frame stable unless the compared route must enter.",
            "animation_techniques": [] if mode == "hold" else [techniques[index % len(techniques)]],
            "on_screen_text": [f"route {index:02d}"],
            "settle_seconds": 0.6,
            "hold_purpose": "Give the viewer two seconds to predict the permitted route." if mode == "hold" else None,
            "introduced_terms": ["authority gate"] if index == 0 else [],
            "claim_role": "mechanism" if function == "mechanism" else "transition",
            "source_refs": ["clm_fixture", "src_fixture"],
            "visual_inference": "Spatial crossing represents permission only within this declared toy case.",
            "evidence_boundary": "The route is a teaching model, not empirical evidence of deployment safety.",
            **({"question_id": "q1", "reasoning_pause_seconds": 2.0} if index == 3 else {}),
            **({"resolves_question_id": "q1"} if index == 5 else {}),
        })
    narration = "\n\n".join(beat["narration"] for beat in beats)
    treatment = {
        "schema_version": TREATMENT_SCHEMA,
        "chapter_id": "self-test",
        "chapter_sha256": "a" * 64,
        "source_context_sha256": "b" * 64,
        "source_commit": "a" * 40,
        "audience": {
            "target_viewer": "A curious adult interested in AI systems but not assumed to be a researcher.",
            "assumed_knowledge": ["AI systems can call tools"],
            "excluded_assumptions": ["No prior chapter or formal-methods knowledge is assumed"],
            "standalone_context": "Define authority before asking the viewer to reason about the route.",
            "introduced_terms": ["authority gate"],
        },
        "promise_candidates": [
            {"promise": "The viewer can predict when a route must stop.", "consequence": "Unsafe routes become visible.", "visual_mechanism": "A request meets a keyed gate.", "transfer_value": "The rule transfers to tool calls.", "evidence_fit": "The chapter claim directly supports it.", "disposition": "selected", "rationale": "It is consequential, visual, and testable."},
            {"promise": "The viewer can list every governance component.", "consequence": "The inventory becomes memorable.", "visual_mechanism": "A labeled architecture diagram grows.", "transfer_value": "The list transfers weakly.", "evidence_fit": "The chapter contains the inventory.", "disposition": "rejected", "rationale": "Recall is weaker than causal prediction."},
            {"promise": "The viewer can define authority in one sentence.", "consequence": "The term becomes available.", "visual_mechanism": "A definition replaces a prompt.", "transfer_value": "The definition transfers incompletely.", "evidence_fit": "The chapter defines the term.", "disposition": "rejected", "rationale": "Definition alone does not teach the mechanism."},
        ],
        "teaching_promise": "The viewer can predict when a route must stop.",
        "selection_rationale": "Prediction exposes the governing mechanism and supports a changed-case transfer check.",
        "content_contract": {
            "chapter_claim_ids": ["clm_fixture"],
            "source_ids": ["src_fixture"],
            "non_claims": ["The toy route does not establish real-world system safety."],
            "case_assumptions": ["Only a keyed authority gate permits external action."],
            "notation_ledger": [{"token": "K", "meaning": "authority key", "unit": None, "visual_form": "small gold key"}],
            "truth_checks": [{"statement": "Agreement does not itself grant authority in the toy model.", "authority_refs": ["clm_fixture", "src_fixture"], "method": "chapter_text", "result": "pass", "resolution": None}],
            "visual_simplifications": ["One gate represents the external policy enforcement layer."],
        },
        "story": {
            "story_form": "comparison",
            "story_basis": {
                "description": "The chapter distinguishes output agreement from delegated authority.",
                "authority_refs": ["clm_fixture", "src_fixture"],
            },
            "concrete_case": "Two equally plausible requests reach one authority-controlled route.",
            "opening_question": "Which request may cross the gate?",
            "macro_moves": [
                {"id": "m01", "purpose": "Pose the routing problem.", "viewer_model_before": "A plausible answer appears sufficient for action.", "visible_event": "Two equally plausible requests approach one locked route.", "viewer_model_after": "Answer quality alone may not permit the route."},
                {"id": "m02", "purpose": "Construct the gate.", "viewer_model_before": "The reason for the route difference remains unknown.", "visible_event": "One request receives a scoped key while content stays equal.", "viewer_model_after": "Authority is a separate mechanism from answer quality."},
                {"id": "m03", "purpose": "Run a failed route.", "viewer_model_before": "A plausible unkeyed request may still cross.", "visible_event": "The unkeyed request stops while the keyed request proceeds.", "viewer_model_after": "The viewer predicts refusal despite plausible output."},
                {"id": "m04", "purpose": "Transfer the rule.", "viewer_model_before": "The distinction may apply only to the first route.", "visible_event": "A different tool presents the same scoped-key boundary.", "viewer_model_after": "The viewer applies the distinction to a new tool."},
            ],
            "payoff": "A route stops when it lacks authority, even when its answer looks good.",
            "comprehension_question": "What mechanism determines whether the request may cross in the shown case?",
            "comprehension_success_criteria": ["Distinguish output quality from an authority grant."],
            "transfer_question": "What must change before the same request can operate a different external tool?",
            "transfer_success_criteria": ["Name a new authority grant rather than better answer agreement."],
        },
        "packaging": {
            "working_title": "A Good Answer Is Not Permission",
            "thumbnail_concept": "Two identical answers face one locked gate.",
            "thumbnail_alt_text": "Two matching answer cards stop before a locked authority gate.",
            "promise_match": "The title and thumbnail pose the exact permission distinction taught.",
            "first_fifteen_seconds_delivery": "Show the two answers and ask which one may act before defining the gate.",
            "source_delivery": "List chapter and external sources on the end card and in the description.",
            "source_delivery_refs": ["clm_fixture", "src_fixture"],
        },
        "art_direction": {
            "medium": "manim_primary",
            "medium_rationale": "State transitions and persistent identity are the teaching mechanism.",
            "visual_thesis": "Plausibility can travel farther than authority permits.",
            "signature_image": "Two equal paths meet one keyed gate and only one crosses.",
            "visual_world": "A stable route graph containing a token, edges, and one gate.",
            "persistent_objects": persistent,
            "visual_invariants": ["The request token retains identity across every route change."],
            "composition_rule": "Flow left to right on one stable decision axis.",
            "palette_rule": "Use teal for active flow and red plus shape for blocked flow.",
            "typography_rule": "Use short labels beside states rather than explanatory cards.",
            "motion_character": "Precise travel with firm stops and no decorative drift.",
            "camera_rule": "Reframe only when a comparison requires more space.",
            "surface_rule": "Use flat fields, stable strokes, and restrained emphasis.",
            "ending_image": "The authorized path crosses while the blocked answer remains visible.",
            "semantic_keyframes": [
                {"id": "k01", "after_macro_move_id": "m01", "focal_state": "Two requests approach an unexplained gate.", "visible_invariant": "Both request tokens remain identical.", "unresolved_question": "Which request may cross?"},
                {"id": "k02", "after_macro_move_id": "m02", "focal_state": "One request receives a visible key.", "visible_invariant": "Answer content remains unchanged.", "unresolved_question": "Does the key, rather than agreement, control action?"},
                {"id": "k03", "after_macro_move_id": "m03", "focal_state": "The unkeyed request stops at the boundary.", "visible_invariant": "The blocked answer remains plausible.", "unresolved_question": None},
                {"id": "k04", "after_macro_move_id": "m04", "focal_state": "A new tool repeats the same keyed boundary.", "visible_invariant": "Permission remains separate from answer quality.", "unresolved_question": None},
            ],
            "asset_plan": [],
        },
        "audio_direction": {
            "narration_style": "Warm, direct, and deliberate around the prediction pause.",
            "pacing_arc": "Quick concrete setup, slower mechanism, then a concise transfer.",
            "music_policy": "No music unless a later review proves it helps rather than masks speech.",
            "sound_effect_policy": "One restrained gate sound may reinforce the consequential stop.",
            "performance_blocks": [
                {"id": "p01", "macro_move_ids": ["m01", "m02"], "performance_direction": "Begin conversationally, then slow at the gate reveal.", "pronunciation_items": []},
                {"id": "p02", "macro_move_ids": ["m03", "m04"], "performance_direction": "State the failure plainly and finish with an open transfer prompt.", "pronunciation_items": []},
            ],
            "review_devices": ["headphones", "earbuds", "laptop speakers", "phone speakers"],
        },
        "accessibility": {
            "color_redundancy": "Blocked state also changes shape, position, and label.",
            "motion_redundancy": "Every movement ends in a distinct stable position.",
            "integrated_description": "Narration names the request, key, route, and blocked gate.",
            "caption_plan": "Create captions from qualified alignment and manually review line breaks.",
            "descriptive_transcript_plan": "Describe consequential visual states omitted from ordinary narration.",
            "reduced_motion_assessment": "No flash, spin, shake, parallax, or continuous camera motion.",
            "caption_safe_composition": "Keep the lower caption region free of the active gate and labels.",
        },
        "script_gate": {
            "narration_path": "visual_edition/self-test/generation-2/narration.txt",
            "narration_sha256": sha256_text(narration),
            "narration_word_count": len(words(narration)),
            "read_aloud_review": "pass",
            "truth_review": "pass",
            "visualizability_review": "pass",
            "reviewer_id": "self-test",
            "verdict": "pass",
            "open_defects": [],
        },
    }
    treatment_text = json.dumps(treatment, indent=2) + "\n"
    plan = {
        "schema_version": SCHEMA,
        "chapter_id": "self-test",
        "chapter_sha256": "a" * 64,
        "source_commit": "a" * 40,
        "treatment_path": "visual_edition/self-test/generation-2/treatment.json",
        "treatment_sha256": sha256_text(treatment_text),
        "narration_path": "visual_edition/self-test/generation-2/narration.txt",
        "narration_sha256": sha256_text(narration),
        "target_duration_seconds": 180.0,
        "timing": {"state": "estimated", "source": "editorial_estimate", "receipt_path": None, "receipt_sha256": None, "narration_receipt_path": None, "narration_receipt_sha256": None, "narration_verification_report_path": None, "narration_verification_report_sha256": None, "aligner_id": None, "manual_anchor_review_path": None, "manual_anchor_review_sha256": None, "manual_anchor_reviewer_id": None, "manual_anchor_count": None, "manual_anchor_failures": None},
        "beats": beats,
    }
    return treatment, plan, narration, treatment_text


def self_test() -> None:
    """Exercise a valid contract and failures that previously slipped through."""

    treatment, plan, narration, treatment_text = fixture()
    errors, _, summary = audit(
        plan, narration, treatment, treatment_text=treatment_text, repository_check=False
    )
    if errors:
        raise AssertionError("valid fixture failed:\n" + "\n".join(errors))
    if summary["beats"] != 20 or not summary["treatment"]["script_gate_passed"]:
        raise AssertionError(f"unexpected passing summary: {summary}")

    mutations = {
        "outside the treatment contract": lambda p, t: p["beats"][0].update(source_refs=["src_fake"]),
        "change beat does not declare": lambda p, t: p["beats"][0].update(object_after=p["beats"][0]["object_before"]),
        "hold beat changes state": lambda p, t: p["beats"][3].update(object_after="A different route state appears."),
        "absent from treatment audience": lambda p, t: p["beats"][1].update(introduced_terms=["mystery term"]),
        "requires source synthesis_receipt": lambda p, t: p["timing"].update(state="block_timed"),
        "cover each treatment macro move": lambda p, t: p["beats"][10].update(macro_move_id="m01", performance_block_id="p01"),
        "does not bind the supplied narration": lambda p, t: t["script_gate"].update(narration_sha256="0" * 64),
        "story.story_basis must bind": lambda p, t: t["story"].update(story_basis=None),
        "does not change the viewer's model": lambda p, t: t["story"]["macro_moves"][0].update(
            viewer_model_after=t["story"]["macro_moves"][0]["viewer_model_before"]
        ),
        "unqualified final compositor": lambda p, t: t["art_direction"].update(
            medium="conventional_edit_primary"
        ),
    }
    for fragment, mutate in mutations.items():
        broken_plan = json.loads(json.dumps(plan))
        broken_treatment = json.loads(json.dumps(treatment))
        mutate(broken_plan, broken_treatment)
        broken_errors, _, _ = audit(
            broken_plan,
            narration,
            broken_treatment,
            treatment_text=json.dumps(broken_treatment, indent=2) + "\n",
            repository_check=False,
        )
        if not any(fragment in error for error in broken_errors):
            raise AssertionError(f"invalid fixture did not trigger {fragment!r}: {broken_errors}")

    administrative = "This chapter records claim id clm_fixture and the current evidence state."
    narration_errors, _, _ = audit_narration(administrative)
    for fragment in ("templated or administrative", "repository identifier"):
        if not any(fragment in error for error in narration_errors):
            raise AssertionError(f"narration fixture did not trigger {fragment!r}")

    _, weak_promise_warnings = audit_teaching_promise(
        "The authority boundary remains visible throughout the example."
    )
    if not any("observable transfer action" in warning for warning in weak_promise_warnings):
        raise AssertionError("non-transfer teaching promise did not trigger a review warning")
    near_pairs = near_duplicate_pairs([
        "The viewer can predict when a route must stop.",
        "The viewer can predict exactly when this route must stop.",
        "The viewer can distinguish observation from a tool receipt.",
    ])
    if not near_pairs or near_pairs[0]["left"] != 0 or near_pairs[0]["right"] != 1:
        raise AssertionError(f"near-duplicate promises were not located: {near_pairs}")

    mechanical = "\n\n".join([
        "The system reveals one visible state.",
        "The system moves the request left.",
        "The system reveals the authority key.",
        "The system moves the request right.",
        "The system reveals a second state.",
        "The system moves the request again.",
        "The system reveals the final route.",
        "The system cannot establish deployment safety.",
        "The system does not prove general reliability.",
        "The system cannot guarantee outside behavior.",
        "The system does not establish human learning.",
        "The system cannot prove the wider claim.",
    ])
    _, mechanical_warnings, mechanical_summary = audit_narration(mechanical)
    for fragment in (
        "performance blocks below eight words",
        "mechanically repeated sentence shape",
        "limitation language",
        "final quarter",
    ):
        if not any(fragment in warning for warning in mechanical_warnings):
            raise AssertionError(
                f"mechanical narration did not trigger {fragment!r}: {mechanical_warnings}"
            )
    if mechanical_summary["micro_performance_blocks"] != 12:
        raise AssertionError(f"unexpected micro-block summary: {mechanical_summary}")

    repeated_phrase = "A retained request crosses the same narrow authority boundary today."
    series_summary = audit_series_narrations([
        ("one", repeated_phrase + " The observer records the result."),
        ("two", repeated_phrase + " The operator checks the result."),
    ])
    if not series_summary["material_reuse_phrases"]:
        raise AssertionError(f"cross-script phrase reuse was not located: {series_summary}")
    if series_summary["scope"] != "diagnostic_not_quality_score":
        raise AssertionError("series audit lost its inference boundary")

    root = find_repository_root()
    if root is not None and (root / ".git").exists():
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, timeout=30
        ).strip()
        structure = json.loads((root / "book_structure.json").read_text(encoding="utf-8"))
        inventory_rows = json.loads(
            (root / "sources/source_inventory.json").read_text(encoding="utf-8")
        )
        inventory = {
            row["id"]: row for row in inventory_rows
            if isinstance(row, dict) and isinstance(row.get("id"), str)
        }
        candidates = [
            chapter for part in structure.get("parts", [])
            for chapter in part.get("chapters", [])
        ]
        checked_commit = False
        for chapter in candidates:
            chapter_path = root / chapter["file"]
            committed = subprocess.run(
                ["git", "show", f"{commit}:{chapter['file']}"],
                cwd=root,
                capture_output=True,
                check=False,
                timeout=30,
            )
            if committed.returncode != 0 or committed.stdout != chapter_path.read_bytes():
                continue
            bindings = []
            context_is_committed = True
            for source_id in chapter.get("source_ids", []):
                note_relative = f"sources/source_notes/{source_id}.md"
                note_path = root / note_relative
                note_commit = subprocess.run(
                    ["git", "show", f"{commit}:{note_relative}"],
                    cwd=root,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
                if note_commit.returncode != 0 or note_commit.stdout != note_path.read_bytes():
                    context_is_committed = False
                    break
                bindings.append({
                    "source_id": source_id,
                    "inventory_record": inventory.get(source_id),
                    "note_path": note_relative,
                    "note_sha256": hashlib.sha256(note_path.read_bytes()).hexdigest(),
                })
            if not context_is_committed:
                continue
            context_body = json.dumps(
                bindings, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            )
            repository_fixture = {
                "chapter_id": chapter["id"],
                "chapter_sha256": hashlib.sha256(chapter_path.read_bytes()).hexdigest(),
                "source_context_sha256": hashlib.sha256(context_body.encode("utf-8")).hexdigest(),
                "source_commit": commit,
                "content_contract": {"chapter_claim_ids": [], "source_ids": []},
                "art_direction": {"asset_plan": []},
            }
            repository_errors = repository_treatment_errors(repository_fixture)
            if repository_errors:
                raise AssertionError(
                    "exact committed source fixture failed:\n" + "\n".join(repository_errors)
                )
            forged = json.loads(json.dumps(repository_fixture))
            forged["source_commit"] = "0" * 40
            forged_errors = repository_treatment_errors(forged)
            if not any("source_commit" in error or "source commit" in error for error in forged_errors):
                raise AssertionError("forged source commit was not rejected")
            checked_commit = True
            break
        if not checked_commit:
            raise AssertionError("no canonical chapter has a source context reproducible from HEAD")
    print("Self-test passed.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path, nargs="?")
    parser.add_argument("--treatment", type=Path)
    parser.add_argument("--narration", type=Path)
    parser.add_argument(
        "--treatment-only",
        action="store_true",
        help="audit a treatment and its optional narration before beat timing",
    )
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
        series_rows: list[tuple[str, str]] = []
        for path in paths:
            try:
                narration = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise SystemExit(f"Unable to read {path}: {exc}") from exc
            errors, warnings, summary = audit_narration(narration)
            failures += bool(errors)
            chapter_id = path.parents[1].name
            series_rows.append((chapter_id, narration))
            rows.append({
                "chapter_id": chapter_id,
                "path": str(path),
                "status": "revise" if errors else "structurally_clean",
                "errors": errors,
                "warnings": warnings,
                **summary,
            })
        series_diagnostics = audit_series_narrations(series_rows)
        print(json.dumps({
            "narrations": len(rows),
            "failures": failures,
            "series_diagnostics": series_diagnostics,
            "rows": rows,
        }, indent=2))
        if failures:
            sys.exit(1)
        print(
            f"Structural narration lint found no prohibited patterns in {len(rows)} drafts; "
            f"series diagnostics raised {len(series_diagnostics['review_triggers'])} "
            "manual review trigger(s). This does not approve truth, voice, "
            "visualizability, or distinctiveness."
        )
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
        print("Structural narration lint found no prohibited patterns; this does not approve the script.")
        return
    if args.treatment_only:
        if args.treatment is None:
            parser.error("--treatment is required with --treatment-only")
        try:
            treatment = load(args.treatment)
            narration = args.narration.read_text(encoding="utf-8") if args.narration else None
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise SystemExit(f"Unable to read inputs: {exc}") from exc
        errors, warnings, summary = audit_treatment(treatment, narration)
        print(json.dumps(summary, indent=2))
        for warning in warnings:
            print(f"WARNING: {warning}")
        if errors:
            print("Treatment audit failed:")
            for error in errors:
                print(f" - {error}")
            sys.exit(1)
        print("Treatment and recorded script gate passed.")
        return
    if args.plan is None:
        parser.error("plan is required unless a narration-only mode is used")
    if args.treatment is None or args.narration is None:
        parser.error("--treatment and --narration are required with a v4 beat plan")
    try:
        plan = load(args.plan)
        treatment_text = args.treatment.read_text(encoding="utf-8")
        treatment = json.loads(treatment_text)
        narration = args.narration.read_text(encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read inputs: {exc}") from exc
    errors, warnings, summary = audit(plan, narration, treatment, treatment_text=treatment_text)
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
