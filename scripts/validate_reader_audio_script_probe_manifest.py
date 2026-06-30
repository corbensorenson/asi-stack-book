#!/usr/bin/env python3
"""Validate the tracked reader audio-script probe manifest and summary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "audio_script_probe_manifest.json"
SUMMARY = ROOT / "docs" / "reader_audio_script_probe_manifest.md"
SCRIPT = ROOT / "scripts" / "build_audio_script.py"
REQUIRED_COMMAND_FRAGMENTS = (
    "python3 scripts/build_audio_script.py --check",
    "python3 scripts/build_audio_script.py",
    "inspect audio_manifest.json in a temporary workspace",
)
REQUIRED_REVIEW_FILES = {
    "audio_manifest.json",
    "AUDIO_RELEASE_CHECKLIST.md",
    "companion_notes.md",
    "chapter_markers.md",
    "pronunciation_glossary.md",
    "proof_equation_reading_rules.md",
}
EXPECTED_TARGET_STATUS = {
    "mp3": "target_not_generated",
    "m4b": "target_not_generated",
    "audio-embedded-epub": "target_not_generated",
}
COMPANION_TOTAL_KEYS = (
    "tables",
    "mermaid_diagrams",
    "code_or_schema_blocks",
    "images",
)
REQUIRED_BLOCKERS = {
    "reviewed_reader_release_record_not_created_for_audio",
    "narration_script_not_reviewed",
    "audio_files_not_generated",
    "audio_spot_check_not_performed",
    "chapter_markers_not_timecoded",
    "audio_metadata_not_reviewed",
    "audio_embedded_epub_not_packaged_or_checked",
    "audio_edition_release_record_not_created",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader audio-script probe manifest validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_string(owner: str, key: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}: {key} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner}: {key} must contain at least {min_words} words.")
    return value


def require_string_list(owner: str, key: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner}: {key} entries must be non-empty strings.")
        else:
            result.append(item)
    return result


def require_int(owner: str, key: str, value: Any, errors: list[str], *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{owner}: {key} must be an integer.")
        return 0
    if value < minimum:
        errors.append(f"{owner}: {key} must be at least {minimum}.")
    return value


def validate_ref(owner: str, ref: str, errors: list[str]) -> None:
    path_part = ref.split("#", 1)[0]
    if not path_part:
        errors.append(f"{owner}: ref must include a path before any anchor: {ref!r}.")
        return
    if not (ROOT / path_part).exists():
        errors.append(f"{owner}: referenced tracked path does not exist: {path_part}.")


def load_audio_module() -> Any:
    sys.path.insert(0, str((ROOT / "scripts").resolve()))
    spec = importlib.util.spec_from_file_location("build_audio_script", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {rel(SCRIPT)}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generated_audio_manifest(errors: list[str]) -> tuple[dict[str, Any], Path | None, tempfile.TemporaryDirectory[str] | None]:
    check = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check.returncode != 0:
        errors.append(f"`python3 scripts/build_audio_script.py --check` failed:\n{check.stdout}{check.stderr}")
        return {}, None, None

    module = load_audio_module()
    temp_context = tempfile.TemporaryDirectory(prefix="asi-audio-probe-")
    temp_path = Path(temp_context.name)
    manifest = module.generate(temp_path)
    if not isinstance(manifest, dict):
        errors.append("Generated audio manifest must be an object.")
        return {}, temp_path, temp_context
    return manifest, temp_path, temp_context


def validate_generated_workspace(
    generated: dict[str, Any],
    workspace: Path | None,
    tracked: dict[str, Any],
    errors: list[str],
) -> None:
    if workspace is None:
        return
    script_files = generated.get("script_files")
    if not isinstance(script_files, list):
        errors.append("Generated audio manifest script_files must be a list.")
        script_files = []
    summary = tracked.get("script_workspace_summary")
    if not isinstance(summary, dict):
        errors.append("script_workspace_summary must be an object.")
        summary = {}

    if len(script_files) != summary.get("script_files"):
        errors.append(
            f"tracked script file count {summary.get('script_files')} does not match generated {len(script_files)}."
        )
    if generated.get("source_profile") != summary.get("source_profile"):
        errors.append("Generated source_profile does not match tracked source_profile.")
    if generated.get("audio_profile") != summary.get("audio_profile"):
        errors.append("Generated audio_profile does not match tracked audio_profile.")
    if generated.get("implementation_horizon_script_status") != "pass":
        errors.append("Generated implementation_horizon_script_status must be pass.")
    if generated.get("review_status") != "review_required":
        errors.append("Generated review_status must be review_required.")
    if generated.get("target_artifact_status") != EXPECTED_TARGET_STATUS:
        errors.append("Generated target_artifact_status must keep all audio targets not generated.")

    treatment = generated.get("companion_treatment_summary")
    if not isinstance(treatment, dict):
        errors.append("Generated companion_treatment_summary must be an object.")
        treatment = {}
    totals = {
        key: sum(int(value.get(key, 0)) for value in treatment.values() if isinstance(value, dict))
        for key in COMPANION_TOTAL_KEYS
    }
    if totals != tracked.get("companion_treatment_totals"):
        errors.append(f"tracked companion treatment totals {tracked.get('companion_treatment_totals')} do not match generated {totals}.")

    for required in REQUIRED_REVIEW_FILES:
        if not (workspace / required).exists():
            errors.append(f"Generated audio workspace missing required review file: {required}")

    proof_rules = (workspace / "proof_equation_reading_rules.md").read_text(
        encoding="utf-8",
        errors="ignore",
    ).lower()
    for phrase in (
        "theorem ids",
        "lean predicates",
        "support states",
        "equations",
        "negative controls",
        "these rules do not claim mp3",
        "these rules do not promote any chapter core claim",
    ):
        if phrase not in proof_rules:
            errors.append(f"proof_equation_reading_rules.md missing phrase: {phrase}")

    glossary = (workspace / "pronunciation_glossary.md").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    for term in ("ASI", "MoECOT", "Lean", "EPUB", "DOCX", "MP3", "M4B"):
        if term not in glossary:
            errors.append(f"pronunciation_glossary.md missing term: {term}")


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if manifest.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if manifest.get("status") != "local_audio_script_probe_record":
        errors.append("status must be local_audio_script_probe_record.")
    require_string("manifest", "purpose", manifest.get("purpose"), errors, min_words=18)

    commands = "\n".join(require_string_list("manifest", "source_commands", manifest.get("source_commands"), errors))
    for fragment in REQUIRED_COMMAND_FRAGMENTS:
        if fragment not in commands:
            errors.append(f"source_commands missing required fragment: {fragment}")

    for ref in require_string_list("manifest", "local_artifact_refs", manifest.get("local_artifact_refs"), errors):
        if not ref.startswith("build/"):
            errors.append(f"local_artifact_refs should point to ignored build outputs: {ref}")
    for ref in require_string_list("manifest", "tracked_evidence_refs", manifest.get("tracked_evidence_refs"), errors):
        validate_ref("tracked_evidence_refs", ref, errors)

    summary = manifest.get("script_workspace_summary")
    if not isinstance(summary, dict):
        errors.append("script_workspace_summary must be an object.")
        summary = {}
    if summary.get("status") != "generated_in_temp_and_checked":
        errors.append("script_workspace_summary.status must be generated_in_temp_and_checked.")
    if summary.get("source_profile") != "reader_release":
        errors.append("script_workspace_summary.source_profile must be reader_release.")
    if summary.get("audio_profile") != "audio_release":
        errors.append("script_workspace_summary.audio_profile must be audio_release.")
    require_int("script_workspace_summary", "script_files", summary.get("script_files"), errors, minimum=1)
    if summary.get("implementation_horizon_script_status") != "pass":
        errors.append("script_workspace_summary.implementation_horizon_script_status must be pass.")
    if summary.get("review_status") != "review_required":
        errors.append("script_workspace_summary.review_status must be review_required.")
    review_files = set(
        require_string_list(
            "script_workspace_summary",
            "required_review_files",
            summary.get("required_review_files"),
            errors,
        )
    )
    missing_review_files = REQUIRED_REVIEW_FILES - review_files
    if missing_review_files:
        errors.append(f"script_workspace_summary.required_review_files missing {sorted(missing_review_files)}.")

    totals = manifest.get("companion_treatment_totals")
    if not isinstance(totals, dict):
        errors.append("companion_treatment_totals must be an object.")
        totals = {}
    for key in COMPANION_TOTAL_KEYS:
        require_int("companion_treatment_totals", key, totals.get(key), errors, minimum=0)

    if manifest.get("target_artifact_status") != EXPECTED_TARGET_STATUS:
        errors.append("target_artifact_status must keep MP3, M4B, and audio-embedded EPUB at target_not_generated.")

    blockers = set(require_string_list("manifest", "release_blockers_preserved", manifest.get("release_blockers_preserved"), errors))
    missing_blockers = REQUIRED_BLOCKERS - blockers
    if missing_blockers:
        errors.append(f"release_blockers_preserved missing {sorted(missing_blockers)}.")

    non_claims = require_string_list("manifest", "non_claims", manifest.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in (
        "not an audiobook",
        "does not approve",
        "does not check narration quality",
        "does not promote any chapter core claim",
        "does not promote any claim support state",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims must include boundary phrase: {phrase}")

    generated, workspace, temp_context = generated_audio_manifest(errors)
    if generated:
        validate_generated_workspace(generated, workspace, manifest, errors)
    if temp_context is not None:
        temp_context.cleanup()

    return errors


def validate_summary(manifest: dict[str, Any], errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    summary = manifest.get("script_workspace_summary", {})
    totals = manifest.get("companion_treatment_totals", {})
    script_files = summary.get("script_files") if isinstance(summary, dict) else None
    mermaid_diagrams = totals.get("mermaid_diagrams") if isinstance(totals, dict) else None
    required_fragments = [
        "Reader Audio-Script Probe Manifest",
        "python3 scripts/build_audio_script.py --check",
        f"| Script files | {script_files} |",
        "| Implementation-horizon script status | pass |",
        f"| Mermaid diagrams | {mermaid_diagrams} |",
        "| MP3 | `target_not_generated` |",
        "audio_edition_release_record_not_created",
        "This manifest is not an audiobook",
        "does not promote any chapter core claim",
        "does not promote any claim support state",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def main() -> None:
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain an object."])
    errors = validate_manifest(manifest)
    validate_summary(manifest, errors)
    if errors:
        fail(errors)
    summary = manifest.get("script_workspace_summary", {})
    totals = manifest.get("companion_treatment_totals", {})
    print(
        "Reader audio-script probe manifest validation passed: "
        f"{summary.get('script_files')} script files, "
        f"{totals.get('mermaid_diagrams')} diagram notes, and no audio artifacts generated."
    )


if __name__ == "__main__":
    main()
