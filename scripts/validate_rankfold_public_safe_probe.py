#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any

from run_rankfold_public_safe_probe import NON_CLAIMS, PROBE_ID, RESULT, RESULT_COMMAND, ROOT, build_corpus, sha256_bytes


DOC = ROOT / "docs" / "rankfold_public_safe_probe.md"
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
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
DECISION = ROOT / "evidence_transitions" / "v1_x_measured" / "rankfold_public_safe_replay_probe_no_change.json"

REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove RankFold codec correctness",
    "NeuralFold compression",
    "compression advantage",
    "downstream utility",
    "fallback execution",
    "does not copy dataset bytes",
)

SURFACE_FRAGMENTS = (
    "RankFold public-safe replay probe",
    "evidence_transitions/v1_x_measured/rankfold_public_safe_replay_probe_no_change.json",
    "RAW0",
    "roundtrip-exact",
    "single-byte archive mutation",
    "NeuralFold",
    "compression advantage",
    "support-state",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def validate_no_promotion_decision(errors: list[str]) -> None:
    if not DECISION.exists():
        errors.append(f"Missing {rel(DECISION)}.")
        return
    decision = load_json(DECISION)
    expected = {
        "transition_id": "v1_x_measured.rankfold_public_safe_replay_probe.no_change",
        "claim_id": "rankfold-neuralfold.public_safe_replay_probe",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "blocks_promotion",
    }
    for key, expected_value in expected.items():
        if decision.get(key) != expected_value:
            errors.append(f"{rel(DECISION)}: {key} must be {expected_value!r}.")
    for ref in (
        rel(DOC),
        rel(RESULT),
        "scripts/run_rankfold_public_safe_probe.py",
        "scripts/validate_rankfold_public_safe_probe.py",
    ):
        refs = (
            decision.get("claim_surface_refs", [])
            + decision.get("claim_record_refs", [])
            + decision.get("artifact_refs", [])
            + decision.get("evidence_packet_refs", [])
        )
        if ref not in refs:
            errors.append(f"{rel(DECISION)} must reference {ref}.")
    require_fragments(
        rel(DECISION),
        text_blob(decision),
        (
            "single-byte archive mutation is rejected",
            "NeuralFold disabled-by-license boundary",
            "compression_advantage_observed remains false",
            "no enabled NeuralFold compression path",
            "does not promote the RankFold chapter core claim",
        ),
        errors,
    )


def fail(errors: list[str]) -> None:
    print("RankFold public-safe replay probe validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    errors: list[str] = []
    paths = (RESULT, DOC, STRUCTURE, OUTLINE, ROADMAP, LIVE_CHAPTER, READER_CHAPTER, README, PUBLICATION, DECISION)
    for path in paths:
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    result = load_json(RESULT)
    structure = load_json(STRUCTURE)
    blob = text_blob(result)
    if "/Users/" in blob or "/var/folders/" in blob:
        errors.append(f"{rel(RESULT)} must not publish local absolute paths.")

    expected_input = build_corpus()
    expected_hash = sha256_bytes(expected_input)
    expected_bytes = len(expected_input)

    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "rankfold_public_safe_replay_probe",
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, expected in expected_scalars.items():
        if result.get(key) != expected:
            errors.append(f"{rel(RESULT)}: {key} must be {expected!r}.")
    if not isinstance(result.get("recorded_at_utc"), str) or not result["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must end with Z.")
    if result.get("source_project_dirty_at_probe") is not True:
        errors.append(f"{rel(RESULT)}: dirty source-project boundary must remain explicit.")
    if not re.fullmatch(r"[0-9a-f]{64}", str(result.get("rfa_binary_sha256", ""))):
        errors.append(f"{rel(RESULT)}: rfa_binary_sha256 must be a SHA-256 hex digest.")

    input_record = result.get("input", {})
    if input_record.get("bytes") != expected_bytes:
        errors.append(f"{rel(RESULT)}: synthetic input byte count changed.")
    if input_record.get("sha256") != expected_hash:
        errors.append(f"{rel(RESULT)}: synthetic input digest changed.")
    if input_record.get("public_safe") is not True:
        errors.append(f"{rel(RESULT)}: input must remain public_safe=true.")

    roundtrip = result.get("roundtrip", {})
    archive_bytes = roundtrip.get("archive_file_bytes")
    if not isinstance(archive_bytes, int) or archive_bytes <= expected_bytes:
        errors.append(f"{rel(RESULT)}: RAW0 archive should be larger than the tiny synthetic input in this result.")
        archive_bytes = 0
    if roundtrip.get("codec_observed") != "RAW0":
        errors.append(f"{rel(RESULT)}: codec_observed must remain RAW0 for the recorded local result.")
    if roundtrip.get("pack_engine_observed") != "Raw (stored)":
        errors.append(f"{rel(RESULT)}: pack_engine_observed must remain Raw (stored).")
    if roundtrip.get("neuralfold_disabled_by_license") is not True:
        errors.append(f"{rel(RESULT)}: NeuralFold license-disabled boundary must remain explicit.")
    if roundtrip.get("compression_advantage_observed") is not False:
        errors.append(f"{rel(RESULT)}: this tiny RAW0 replay must not claim compression advantage.")
    if roundtrip.get("roundtrip_exact") is not True:
        errors.append(f"{rel(RESULT)}: roundtrip_exact must be true.")
    if roundtrip.get("unpacked_file_bytes") != expected_bytes:
        errors.append(f"{rel(RESULT)}: unpacked byte count must match input.")
    if roundtrip.get("unpacked_sha256") != expected_hash:
        errors.append(f"{rel(RESULT)}: unpacked digest must match input.")
    verify = roundtrip.get("verify", {})
    if verify.get("ok") != 1 or verify.get("failed") != 0 or verify.get("skipped") != 0:
        errors.append(f"{rel(RESULT)}: verify must record 1 OK, 0 FAILED, 0 skipped.")
    if archive_bytes:
        if not math.isclose(roundtrip.get("archive_to_input_ratio", -1), round(archive_bytes / expected_bytes, 8), abs_tol=1e-8):
            errors.append(f"{rel(RESULT)}: archive_to_input_ratio mismatch.")
        if not math.isclose(roundtrip.get("input_to_archive_ratio", -1), round(expected_bytes / archive_bytes, 8), abs_tol=1e-8):
            errors.append(f"{rel(RESULT)}: input_to_archive_ratio mismatch.")

    negative = result.get("negative_control", {})
    if negative.get("kind") != "single_byte_archive_mutation":
        errors.append(f"{rel(RESULT)}: negative control must be single_byte_archive_mutation.")
    if negative.get("rejected") is not True or negative.get("verify_exit_code") == 0:
        errors.append(f"{rel(RESULT)}: corrupt archive negative control must be rejected.")

    commands = result.get("commands")
    if not isinstance(commands, list) or len(commands) != 5:
        errors.append(f"{rel(RESULT)}: expected five command records.")
    else:
        ids = [command.get("id") for command in commands if isinstance(command, dict)]
        if ids != ["pack", "verify", "list", "unpack", "verify_corrupt"]:
            errors.append(f"{rel(RESULT)}: unexpected command record order {ids!r}.")

    if result.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match runner boundaries.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), REQUIRED_NON_CLAIM_TERMS, errors)

    for owner, path in (
        (rel(DOC), DOC),
        (rel(OUTLINE), OUTLINE),
        (rel(ROADMAP), ROADMAP),
        (rel(LIVE_CHAPTER), LIVE_CHAPTER),
        (rel(READER_CHAPTER), READER_CHAPTER),
        (rel(README), README),
        (rel(PUBLICATION), PUBLICATION),
    ):
        require_fragments(owner, path.read_text(encoding="utf-8"), SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "rankfold-neuralfold-and-artifact-compression")
    if record.get("evidence_level") != "argument":
        errors.append("rankfold-neuralfold-and-artifact-compression: evidence_level must remain argument.")
    require_fragments(
        "book_structure rankfold tests",
        text_blob(record.get("codex_tests", [])),
        (
            "RankFold public-safe replay probe",
            "RAW0",
            "single-byte archive mutation",
            "no NeuralFold-compression, compression-advantage, codec-correctness, downstream-utility, fallback-execution, deployed-compression, or support-state-promotion claim",
        ),
        errors,
    )
    validate_no_promotion_decision(errors)

    if errors:
        fail(errors)
    print(
        "RankFold public-safe replay probe validation passed: "
        "synthetic RAW0 pack/verify/list/unpack roundtrip and corrupt-archive negative control checked."
    )


if __name__ == "__main__":
    main()
