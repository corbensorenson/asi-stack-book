#!/usr/bin/env python3
"""Validate the public-safe RankFold artifact import record.

This is a record-consistency and evidence-boundary guard. It does not rerun
RankFold compression, copy source data, or promote the chapter core claim.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "rankfold_artifact_import" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "rankfold_artifact_import.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LIVE_CHAPTER = ROOT / "chapters" / "rankfold-neuralfold-and-artifact-compression.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "rankfold-neuralfold-and-artifact-compression.qmd"
)

EXPECTED_DECODED_SHA = "2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8"
EXPECTED_BINARY_SHA = "f03e3175742411b4310187cf48c5e735813c4a411a93dc53b68a3364ed75f438"
EXPECTED_ARCHIVES = {
    "enwik8_out2_1771038259": {
        "archive_file_bytes": 36169618,
        "archive_file_sha256": "9b0b5b1f91d8d7a05d5d51fcd83b7a46f18eac6e7bd5d55f367366bc71f80816",
        "pack0_stream_blake3": "2d2b78f65cf604628243540675c230a6867844c871b1ae4ae856bdd7b52d0cba",
    },
    "enwik8_out3_1771047103": {
        "archive_file_bytes": 36155111,
        "archive_file_sha256": "0b78b195c80714d2f1ef1e044e0ee9f28ec92444e09b6ef9372656c573462352",
        "pack0_stream_blake3": "64cf51d37f7649df05dd835d52dbda430b95ee6240e851ebea02849b60e1d482",
    },
    "enwik8_out4_1771047630": {
        "archive_file_bytes": 36148844,
        "archive_file_sha256": "12fc0fc45d56408ea734d2408658fff57e9786376d5b31d87f24acb112666651",
        "pack0_stream_blake3": "0b830cd6b1d99554e8519df8427e7b50abccf3e399bcb6f6501a1c4796d7cfe4",
    },
}

NON_CLAIM_FRAGMENTS = (
    "does not copy dataset bytes",
    "does not prove RankFold codec correctness",
    "does not prove deterministic decoder correctness",
    "does not rerun compression",
    "does not prove benchmark performance",
    "does not prove downstream utility",
    "does not prove fallback execution",
    "does not promote the RankFold chapter core claim",
    "does not create a support-state transition",
    "does not prove deployed compression behavior",
)

SURFACE_FRAGMENTS = (
    "RankFold artifact import",
    "100,000,000-byte decoded artifact",
    EXPECTED_DECODED_SHA,
    "2.76634019",
    "1 OK, 0 failed",
    "NEURAL0",
    "does not prove RankFold codec correctness",
    "does not promote the RankFold chapter core claim",
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


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    normalized = normalize(text)
    for fragment in fragments:
        if normalize(fragment) not in normalized:
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
    for path in (RESULT, DOC, STRUCTURE, OUTLINE, ROADMAP, LIVE_CHAPTER, READER_CHAPTER):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    result = load_json(RESULT)
    structure = load_json(STRUCTURE)
    doc_text = DOC.read_text(encoding="utf-8")
    outline_text = OUTLINE.read_text(encoding="utf-8")
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    live_text = LIVE_CHAPTER.read_text(encoding="utf-8")
    reader_text = READER_CHAPTER.read_text(encoding="utf-8")

    if result.get("record_id") != "rankfold-artifact-import-2026-07-02-enwik8-local":
        errors.append(f"{rel(RESULT)}: unexpected record_id.")
    if result.get("rfa_binary_sha256") != EXPECTED_BINARY_SHA:
        errors.append(f"{rel(RESULT)}: rfa binary digest changed.")
    if result.get("source_project_dirty_at_import") is not True:
        errors.append(f"{rel(RESULT)}: dirty source-project boundary must stay explicit.")
    if "/Users/" in text_blob(result):
        errors.append(f"{rel(RESULT)} must not publish local absolute paths.")

    reference = result.get("reference_decoded_artifact", {})
    if reference.get("decoded_file_bytes") != 100000000:
        errors.append(f"{rel(RESULT)}: reference decoded size must remain 100000000 bytes.")
    if reference.get("decoded_sha256") != EXPECTED_DECODED_SHA:
        errors.append(f"{rel(RESULT)}: reference decoded digest mismatch.")

    observations = result.get("observations", [])
    if not isinstance(observations, list) or len(observations) != 3:
        errors.append(f"{rel(RESULT)}: expected exactly 3 archive observations.")
        observations = []

    labels_seen: set[str] = set()
    best_ratio = 0.0
    for observation in observations:
        if not isinstance(observation, dict):
            errors.append(f"{rel(RESULT)}: observation entries must be objects.")
            continue
        label = str(observation.get("artifact_label", ""))
        labels_seen.add(label)
        expected = EXPECTED_ARCHIVES.get(label)
        if expected is None:
            errors.append(f"{rel(RESULT)}: unexpected archive label {label!r}.")
            continue
        if observation.get("archive_file_bytes") != expected["archive_file_bytes"]:
            errors.append(f"{label}: archive_file_bytes mismatch.")
        if observation.get("archive_file_sha256") != expected["archive_file_sha256"]:
            errors.append(f"{label}: archive_file_sha256 mismatch.")
        if observation.get("decoded_file_bytes") != 100000000:
            errors.append(f"{label}: decoded_file_bytes must remain 100000000.")
        if observation.get("decoded_sha256") != EXPECTED_DECODED_SHA:
            errors.append(f"{label}: decoded_sha256 mismatch.")
        archive_bytes = observation.get("archive_file_bytes")
        if isinstance(archive_bytes, int):
            archive_to_decoded = round(archive_bytes / 100000000, 8)
            decoded_to_archive = round(100000000 / archive_bytes, 8)
            if not math.isclose(observation.get("archive_to_decoded_ratio", -1), archive_to_decoded, abs_tol=1e-8):
                errors.append(f"{label}: archive_to_decoded_ratio mismatch.")
            if not math.isclose(observation.get("decoded_to_archive_ratio", -1), decoded_to_archive, abs_tol=1e-8):
                errors.append(f"{label}: decoded_to_archive_ratio mismatch.")
            best_ratio = max(best_ratio, decoded_to_archive)
        verify = observation.get("rfa_verify", {})
        if verify.get("ok") != 1 or verify.get("failed") != 0 or verify.get("skipped") != 0:
            errors.append(f"{label}: rfa_verify must remain 1 OK, 0 failed, 0 skipped.")
        inspect = observation.get("rfa_inspect", {})
        if inspect.get("streams") != 1 or inspect.get("pages") != 1 or inspect.get("entries") != 1:
            errors.append(f"{label}: inspect stream/page/entry counts must remain 1.")
        if inspect.get("encrypted") is not False:
            errors.append(f"{label}: encrypted must remain false for this public-safe record.")
        if inspect.get("pack0_stream_name") != "__pack0__":
            errors.append(f"{label}: expected __pack0__ stream.")
        if inspect.get("pack0_stream_blake3") != expected["pack0_stream_blake3"]:
            errors.append(f"{label}: pack0 stream BLAKE3 mismatch.")
        if inspect.get("codec_mix", {}).get("NEURAL0") != 1:
            errors.append(f"{label}: codec mix must include NEURAL0: 1.")

    missing_labels = set(EXPECTED_ARCHIVES) - labels_seen
    if missing_labels:
        errors.append(f"{rel(RESULT)}: missing archive observations {sorted(missing_labels)}.")

    summary = result.get("summary", {})
    if summary.get("observed_archives") != 3:
        errors.append(f"{rel(RESULT)}: observed_archives summary must be 3.")
    if summary.get("decoded_digest_consensus") is not True:
        errors.append(f"{rel(RESULT)}: decoded_digest_consensus must be true.")
    if not math.isclose(summary.get("best_observed_decoded_to_archive_ratio", -1), best_ratio, abs_tol=1e-8):
        errors.append(f"{rel(RESULT)}: best ratio summary mismatch.")
    if summary.get("support_state_effect") != "none" or summary.get("chapter_core_support_effect") != "none":
        errors.append(f"{rel(RESULT)}: support-state effects must remain none.")
    if summary.get("evidence_transition_created") is not False:
        errors.append(f"{rel(RESULT)}: evidence_transition_created must remain false.")

    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIM_FRAGMENTS, errors)
    for owner, text in (
        (rel(DOC), doc_text),
        (rel(OUTLINE), outline_text),
        (rel(ROADMAP), roadmap_text),
        (rel(LIVE_CHAPTER), live_text),
        (rel(READER_CHAPTER), reader_text),
    ):
        require_fragments(owner, text, SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "rankfold-neuralfold-and-artifact-compression")
    if record.get("evidence_level") != "argument":
        errors.append("rankfold-neuralfold-and-artifact-compression: evidence_level must remain argument.")
    tests_text = text_blob(record.get("codex_tests", []))
    require_fragments(
        "book_structure rankfold tests",
        tests_text,
        (
            "RankFold artifact import validation",
            "100,000,000-byte decoded artifact",
            "no codec-correctness, benchmark-performance, downstream-utility, fallback-execution, deployed-compression, or support-state-promotion claim",
        ),
        errors,
    )

    if errors:
        fail(errors)

    print("RankFold artifact import validation passed: 3 local archive observations checked.")


def fail(errors: list[str]) -> None:
    print("RankFold artifact import validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
