#!/usr/bin/env python3
"""Report exact raw and content-normalized narration/ASR edit blocks."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from types import ModuleType
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_root() -> Path:
    configured = os.environ.get("ASI_STACK_BOOK_ROOT")
    root = Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()
    if not (root / "scripts/validate_visual_narration.py").is_file():
        raise ValueError(
            "run from the ASI Stack book root or set ASI_STACK_BOOK_ROOT"
        )
    return root


def load_validator(root: Path) -> ModuleType:
    path = root / "scripts/validate_visual_narration.py"
    spec = importlib.util.spec_from_file_location("asi_stack_narration_validator", path)
    if spec is None or spec.loader is None:
        raise ValueError("could not load the canonical narration validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def checked_input(root: Path, value: str, suffix: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        raise ValueError("diagnostic inputs must be repository-relative")
    path = (root / candidate).resolve()
    audio_root = (root / "build/visual_edition/audio").resolve()
    try:
        path.relative_to(audio_root)
    except ValueError as exc:
        raise ValueError("diagnostic input escapes build/visual_edition/audio") from exc
    if path.suffix != suffix or not path.is_file():
        raise ValueError(f"diagnostic input is not an existing {suffix} file: {value}")
    return path


def edit_blocks(expected: list[str], recognized: list[str]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    matcher = difflib.SequenceMatcher(a=expected, b=recognized, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        blocks.append(
            {
                "operation": tag,
                "expected_range": [i1, i2],
                "recognized_range": [j1, j2],
                "expected_tokens": expected[i1:i2],
                "recognized_tokens": recognized[j1:j2],
                "expected_context": expected[max(0, i1 - 4):min(len(expected), i2 + 4)],
                "recognized_context": recognized[
                    max(0, j1 - 4):min(len(recognized), j2 + 4)
                ],
            }
        )
    return blocks


def build_report(
    expected_text: str,
    recognized_text: str,
    validator: ModuleType,
) -> dict[str, Any]:
    raw_expected = validator.tokens(expected_text)
    raw_recognized = validator.tokens(recognized_text)
    normalized_expected = validator.normalize_content_tokens(raw_expected)
    normalized_recognized = validator.normalize_content_tokens(raw_recognized)
    raw_blocks = edit_blocks(raw_expected, raw_recognized)
    normalized_blocks = edit_blocks(normalized_expected, normalized_recognized)
    return {
        "schema_version": "asi_stack.narration_asr_diagnostic.v1",
        "gate_effect": "diagnostic_only",
        "raw": {
            "expected_token_count": len(raw_expected),
            "recognized_token_count": len(raw_recognized),
            "exact_match": not raw_blocks,
            "edit_block_count": len(raw_blocks),
            "edit_blocks": raw_blocks,
        },
        "content_normalized": {
            "expected_token_count": len(normalized_expected),
            "recognized_token_count": len(normalized_recognized),
            "exact_match": not normalized_blocks,
            "edit_block_count": len(normalized_blocks),
            "edit_blocks": normalized_blocks,
        },
        "interpretation": (
            "Use these blocks to localize a speech or recognition defect. This report "
            "does not change the canonical validator, pass a gate, or assess acoustic quality."
        ),
    }


def self_test(validator: ModuleType) -> None:
    equivalent = build_report(
        "Check out route two hundred forty.",
        "Checkout root 240.",
        validator,
    )
    if equivalent["content_normalized"]["edit_blocks"]:
        raise AssertionError("content-equivalent forms did not normalize")
    defect = build_report("Keep the private outlet.", "Keep the public outlet.", validator)
    blocks = defect["content_normalized"]["edit_blocks"]
    if len(blocks) != 1 or blocks[0]["operation"] != "replace":
        raise AssertionError("one-token substitution was not localized")
    print("Narration ASR diagnostic self-test passed: equivalence and defect controls checked.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", help="repository-relative synthesis receipt JSON")
    parser.add_argument("--asr", help="repository-relative ASR transcript JSON")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    root = repository_root()
    validator = load_validator(root)
    if args.self_test:
        self_test(validator)
        return
    if not args.receipt or not args.asr:
        parser.error("--receipt and --asr are required unless --self-test is used")

    receipt_path = checked_input(root, args.receipt, ".json")
    asr_path = checked_input(root, args.asr, ".json")
    expected_stem = receipt_path.name.removesuffix(".receipt.json")
    if receipt_path.name != f"{expected_stem}.receipt.json":
        raise ValueError("receipt filename must end in .receipt.json")
    if asr_path.parent != receipt_path.parent or asr_path.name != f"{expected_stem}.json":
        raise ValueError("ASR transcript and receipt must share one canonical audio identity")

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    asr = json.loads(asr_path.read_text(encoding="utf-8"))
    segments = receipt.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("synthesis receipt has no segments")
    expected_text = " ".join(item["spoken_text"] for item in segments)
    recognized_text = asr.get("text")
    if not isinstance(recognized_text, str):
        raise ValueError("ASR transcript has no text")

    report = build_report(expected_text, recognized_text, validator)
    diagnostic_path = Path(__file__).resolve()
    validator_path = root / "scripts/validate_visual_narration.py"
    report["custody"] = {
        "diagnostic_path": diagnostic_path.relative_to(root).as_posix(),
        "diagnostic_sha256": sha256(diagnostic_path),
        "canonical_validator_path": validator_path.relative_to(root).as_posix(),
        "canonical_validator_sha256": sha256(validator_path),
        "receipt_path": receipt_path.relative_to(root).as_posix(),
        "receipt_sha256": sha256(receipt_path),
        "asr_path": asr_path.relative_to(root).as_posix(),
        "asr_sha256": sha256(asr_path),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
