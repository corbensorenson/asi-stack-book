#!/usr/bin/env python3
"""Validate generation-two visual-production identity, review, and custody."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from sync_manim_v2_production_ledger import build


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "visual_edition/manim_v2_production_ledger.json"
SCHEMA = ROOT / "schemas/manim_v2_production_ledger.schema.json"
REVIEW_DIMENSIONS = (
    "teaching_clarity", "composition", "motion_quality", "synchronization",
    "continuity", "pacing", "voice", "sound_mix", "engagement",
    "accessibility", "claim_fidelity",
)
REVIEW_OWNED_DIMENSIONS = {
    "animatic": {
        "teaching_clarity", "composition", "motion_quality", "synchronization",
        "continuity", "pacing", "voice", "engagement",
    },
    "picture_and_sound_lock": set(REVIEW_DIMENSIONS) - {"claim_fidelity"},
    "release_candidate": set(REVIEW_DIMENSIONS),
    "independent_release_candidate": set(REVIEW_DIMENSIONS) - {"claim_fidelity"},
}
ALL_VIEWING_PASSES = (
    "normal_speed", "muted", "audio_only", "captions_on", "phone",
    "large_screen", "headphones", "speakers", "random_frames",
)
EXPECTED_REJECTING_CONTROL_COUNT = 96


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(commit: str, relative_path: str) -> bytes | None:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=30,
    )
    return completed.stdout if completed.returncode == 0 else None


def committed_source_context_digest(commit: str, chapter: dict) -> str | None:
    inventory_blob = git_blob(commit, "sources/source_inventory.json")
    if inventory_blob is None:
        return None
    try:
        inventory_rows = json.loads(inventory_blob.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    inventory = {
        row["id"]: row for row in inventory_rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    bindings = []
    for source_id in chapter.get("source_ids", []):
        relative = f"sources/source_notes/{source_id}.md"
        note = git_blob(commit, relative)
        if note is None:
            return None
        bindings.append({
            "source_id": source_id,
            "inventory_record": inventory.get(source_id),
            "note_path": relative,
            "note_sha256": hashlib.sha256(note).hexdigest(),
        })
    body = json.dumps(bindings, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def safe_repo_path(value: str) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return path


def load_skill_script(filename: str, module_name: str):
    path = ROOT / f"skills/asi-stack-manim-videos/scripts/{filename}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load tracked skill script {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_beat_auditor():
    return load_skill_script("audit_video_plan.py", "asi_stack_manim_beat_auditor")


def canonical_claim_ids() -> dict[str, set[str]]:
    substance = json.loads(
        (ROOT / "evidence_quality/chapter_substance_contract.json").read_text(encoding="utf-8")
    )
    return {
        row["chapter_id"]: {
            ref["atom_id"] for ref in row.get("atom_refs", [])
            if isinstance(ref, dict) and isinstance(ref.get("atom_id"), str)
        }
        for row in substance.get("chapter_records", [])
        if isinstance(row, dict) and isinstance(row.get("chapter_id"), str)
    }


def chapter_source_ids() -> dict[str, set[str]]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    return {
        chapter["id"]: set(chapter.get("source_ids", []))
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    }


def binding_errors(binding: dict, label: str, expected: dict | None = None) -> list[str]:
    errors: list[str] = []
    path_value = binding.get("path") if isinstance(binding, dict) else None
    sha_value = binding.get("sha256") if isinstance(binding, dict) else None
    if bool(path_value) != bool(sha_value):
        return [f"{label} path and digest must either both exist or both be null"]
    if expected is not None and binding != expected:
        errors.append(f"{label} does not bind the ledger-owned artifact identity")
    if path_value:
        path = safe_repo_path(path_value)
        if path is None:
            errors.append(f"{label} escapes the repository")
        elif not path.is_file():
            errors.append(f"{label} points to a missing artifact")
        elif digest(path) != sha_value:
            errors.append(f"{label} artifact digest drift")
    return errors


def expected_binding(path_value: str | None, sha_value: str | None) -> dict:
    return {"path": path_value, "sha256": sha_value}


def current_file_binding(path_value: str) -> dict:
    path = safe_repo_path(path_value)
    return expected_binding(
        path_value,
        digest(path) if path is not None and path.is_file() else None,
    )


def tracked_identity_errors(target: dict, path_field: str, digest_field: str, label: str) -> list[str]:
    path = safe_repo_path(target.get(path_field, ""))
    expected = target.get(digest_field)
    if path is None:
        return [f"{label} path escapes the repository or is absent"]
    if not path.is_file():
        return [] if expected is None else [f"{label} digest exists without its file"]
    return [] if expected == digest(path) else [f"{label} identity drift"]


def narration_custody_document_errors(
    receipt: dict,
    report: dict,
    plan: dict,
    treatment: dict | None,
    narration_toolchain: dict,
    target: dict,
    *,
    audio_relative: str,
    audio_sha256: str,
    narration_receipt_sha256: str,
    asr_sha256: str,
    narration_text: str,
) -> list[str]:
    errors: list[str] = []
    synthesis = narration_toolchain.get("synthesis", {})
    verification = narration_toolchain.get("verification", {})
    tracked = narration_toolchain.get("tracked_inputs", {})
    expected_model_files = {
        "build/visual_edition/models/Kokoro-82M-bf16/config.json": synthesis.get("config_sha256"),
        "build/visual_edition/models/Kokoro-82M-bf16/kokoro-v1_0.safetensors": synthesis.get("weights_sha256"),
        f"build/visual_edition/models/Kokoro-82M-bf16/voices/{synthesis.get('voice')}.safetensors": synthesis.get("voice_sha256"),
    }
    expected_receipt = {
        "schema_version": "asi_stack.local_narration_render.v1",
        "renderer_sha256": tracked.get("renderer_sha256"),
        "toolchain_id": narration_toolchain.get("toolchain_id"),
        "implementation": synthesis.get("implementation"),
        "implementation_version": synthesis.get("version"),
        "model_repository": synthesis.get("model_repository"),
        "model_revision": synthesis.get("model_revision"),
        "input_path": target.get("narration_path"),
        "input_sha256": target.get("narration_sha256"),
        "lexicon_path": tracked.get("pronunciation_lexicon"),
        "lexicon_sha256": tracked.get("pronunciation_lexicon_sha256"),
        "model_file_sha256": expected_model_files,
        "voice": synthesis.get("voice"),
        "speed": synthesis.get("speed"),
        "sample_rate": synthesis.get("sample_rate"),
        "output_path": audio_relative,
        "output_sha256": audio_sha256,
    }
    for field, expected in expected_receipt.items():
        if receipt.get(field) != expected:
            errors.append(f"narration render receipt {field} differs from the pinned toolchain or artifact")
    expected_segmentation = {
        "maximum_characters": synthesis.get("maximum_segment_characters"),
        "sentence_pause_seconds": synthesis.get("sentence_pause_seconds"),
        "paragraph_pause_seconds": synthesis.get("paragraph_pause_seconds"),
    }
    segmentation = receipt.get("segmentation", {})
    for field, expected in expected_segmentation.items():
        if segmentation.get(field) != expected:
            errors.append(f"narration render receipt segmentation {field} drift")
    expected_normalization = {
        "filter": synthesis.get("normalizer_implementation"),
        "ffmpeg_path": synthesis.get("normalizer_path"),
        "ffmpeg_version": synthesis.get("normalizer_version"),
        "ffmpeg_sha256": synthesis.get("normalizer_sha256"),
        "integrated_lufs_target": synthesis.get("integrated_lufs_target"),
        "true_peak_dbtp_target": synthesis.get("true_peak_dbtp_target"),
        "loudness_range_target": synthesis.get("loudness_range_target"),
    }
    normalization = receipt.get("normalization", {})
    for field, expected in expected_normalization.items():
        if normalization.get(field) != expected:
            errors.append(f"narration render receipt normalization {field} drift")
    if abs(float(receipt.get("duration_seconds") or 0) - float(plan.get("target_duration_seconds") or 0)) > 0.25:
        errors.append("narration render duration differs from the beat-plan duration")
    segments = receipt.get("segments", [])
    rendered_text = " ".join(
        row.get("written_text", "") for row in segments if isinstance(row, dict)
    )
    if " ".join(rendered_text.split()) != " ".join(narration_text.split()):
        errors.append("narration render segments do not reproduce the exact narration")
    paragraph_count = len([
        paragraph for paragraph in re.split(r"\n\s*\n", narration_text.strip())
        if paragraph.strip()
    ])
    block_count = len(
        treatment.get("audio_direction", {}).get("performance_blocks", [])
        if isinstance(treatment, dict) else []
    )
    receipt_paragraph_count = sum(
        row.get("paragraph_end") is True for row in segments if isinstance(row, dict)
    )
    if paragraph_count != receipt_paragraph_count or paragraph_count != block_count:
        errors.append("narration paragraphs, synthesis blocks, and treatment performance blocks do not align")
    expected_report = {
        "schema_version": "asi_stack.local_narration_validation.v1",
        "validation_state": "pass",
        "validator_sha256": tracked.get("narration_validator_sha256"),
        "receipt_sha256": narration_receipt_sha256,
        "asr_sha256": asr_sha256,
        "audio_path": audio_relative,
        "audio_sha256": audio_sha256,
    }
    for field, expected in expected_report.items():
        if report.get(field) != expected:
            errors.append(f"narration verification report {field} identity drift")
    checks = report.get("checks", {})
    if not isinstance(checks, dict) or not checks or not all(checks.values()):
        errors.append("narration verification report retains a failing check")
    if report.get("content_word_error_rate", 1) > verification.get(
        "maximum_content_normalized_word_error_rate", 0
    ):
        errors.append("narration verification exceeds the pinned content WER ceiling")
    return errors


def narration_custody_errors(
    entry: dict,
    plan: dict,
    treatment: dict | None,
    narration_toolchain: dict,
) -> list[str]:
    errors: list[str] = []
    timing = plan.get("timing", {})
    if timing.get("state") == "estimated":
        return errors
    chapter_id = entry.get("chapter_id")
    target = entry.get("target", {})
    audio_relative = f"build/visual_edition/audio/{chapter_id}-narration-master.wav"
    narration_receipt_relative = (
        f"build/visual_edition/audio/{chapter_id}-narration-master.receipt.json"
    )
    verification_relative = (
        f"build/visual_edition/audio/{chapter_id}-narration-master.validation.json"
    )
    asr_relative = f"build/visual_edition/audio/{chapter_id}-narration-master.json"
    narration_binding = {
        "path": timing.get("narration_receipt_path"),
        "sha256": timing.get("narration_receipt_sha256"),
    }
    verification_binding = {
        "path": timing.get("narration_verification_report_path"),
        "sha256": timing.get("narration_verification_report_sha256"),
    }
    errors.extend(binding_errors(narration_binding, "timing.narration_receipt"))
    errors.extend(binding_errors(verification_binding, "timing.narration_verification_report"))
    if narration_binding.get("path") != narration_receipt_relative:
        errors.append("timed beat plan uses a noncanonical narration render receipt")
    if verification_binding.get("path") != verification_relative:
        errors.append("timed beat plan uses a noncanonical narration verification report")
    if timing.get("state") == "block_timed" and (
        timing.get("receipt_path") != narration_binding.get("path")
        or timing.get("receipt_sha256") != narration_binding.get("sha256")
    ):
        errors.append("block-timed plan does not use its narration render receipt as timing authority")
    narration_receipt_path = safe_repo_path(narration_binding.get("path", ""))
    verification_path = safe_repo_path(verification_binding.get("path", ""))
    audio_path = safe_repo_path(audio_relative)
    asr_path = safe_repo_path(asr_relative)
    narration_path = safe_repo_path(target.get("narration_path", ""))
    if not all(
        path is not None and path.is_file()
        for path in (
            narration_receipt_path, verification_path, audio_path, asr_path,
            narration_path,
        )
    ):
        return errors + ["timed beat plan lacks complete narration, audio, ASR, or verification custody"]
    try:
        receipt = json.loads(narration_receipt_path.read_text(encoding="utf-8"))
        report = json.loads(verification_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return errors + [f"narration custody artifact is unreadable JSON: {exc}"]

    narration_text = narration_path.read_text(encoding="utf-8")
    errors.extend(
        narration_custody_document_errors(
            receipt, report, plan, treatment, narration_toolchain, target,
            audio_relative=audio_relative,
            audio_sha256=digest(audio_path),
            narration_receipt_sha256=digest(narration_receipt_path),
            asr_sha256=digest(asr_path),
            narration_text=narration_text,
        )
    )
    return errors


def sandbox_policy_receipt_errors(
    policy_receipt: dict,
    policy_schema: dict,
    ledger: dict,
    entry: dict,
    treatment: dict | None,
    render_receipt: dict | None,
    runner_module,
    *,
    check_files: bool,
    expected_profile: str = "release",
    reviewed_master: dict | None = None,
) -> list[str]:
    errors = [
        f"sandbox-policy-receipt-schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(policy_schema).iter_errors(policy_receipt)
    ]
    target = entry.get("target", {})
    if policy_receipt.get("chapter_id") != entry.get("chapter_id"):
        errors.append("sandbox policy receipt chapter identity drift")
    if policy_receipt.get("profile") != expected_profile:
        errors.append(
            f"{expected_profile} review requires a {expected_profile}-profile sandbox receipt"
        )
    if expected_profile == "release":
        if not isinstance(render_receipt, dict):
            errors.append("release sandbox receipt lacks its final render receipt")
            render_receipt = {}
        if policy_receipt.get("isolation_mode") != render_receipt.get("execution_security", {}).get("isolation_mode"):
            errors.append("render and sandbox receipts name different isolation modes")
    expected = {
        "runner": expected_binding(
            ledger.get("isolated_render_runner_path"),
            ledger.get("isolated_render_runner_sha256"),
        ),
        "scene": expected_binding(target.get("scene_path"), target.get("scene_sha256")),
        "treatment": expected_binding(target.get("treatment_path"), target.get("treatment_sha256")),
    }
    for name, binding in expected.items():
        actual = policy_receipt.get(name, {})
        if actual != binding:
            errors.append(f"sandbox policy receipt {name} does not bind the canonical identity")
        if check_files:
            errors.extend(binding_errors(actual, f"sandbox_policy_receipt.{name}"))
    if expected_profile == "release":
        if policy_receipt.get("toolchain_id") != render_receipt.get("render", {}).get("toolchain_id"):
            errors.append("sandbox policy receipt names a different visual toolchain")
        if policy_receipt.get("audio_master") != render_receipt.get("input_bindings", {}).get("audio_master"):
            errors.append("sandbox policy receipt audio master differs from the final render receipt")
    else:
        toolchain_path = safe_repo_path(ledger.get("visual_toolchain_path", ""))
        toolchain_id = None
        if toolchain_path is not None and toolchain_path.is_file():
            toolchain_id = json.loads(toolchain_path.read_text(encoding="utf-8")).get("toolchain_id")
        if policy_receipt.get("toolchain_id") != toolchain_id:
            errors.append("draft sandbox receipt names a different visual toolchain")
        expected_audio_path = (
            f"build/visual_edition/audio/{entry.get('chapter_id')}-narration-master.wav"
        )
        audio_binding = policy_receipt.get("audio_master")
        if not isinstance(audio_binding, dict) or audio_binding.get("path") != expected_audio_path:
            errors.append(
                "animatic draft sandbox receipt lacks the canonical narration audio master"
            )
        elif check_files:
            errors.extend(
                binding_errors(audio_binding, "sandbox_policy_receipt.audio_master")
            )
    visual_toolchain_path = safe_repo_path(ledger.get("visual_toolchain_path", ""))
    visual_toolchain = (
        json.loads(visual_toolchain_path.read_text(encoding="utf-8"))
        if visual_toolchain_path is not None and visual_toolchain_path.is_file()
        else {}
    )
    if policy_receipt.get("media_tools") != visual_toolchain.get("media_tools"):
        errors.append("sandbox policy receipt does not bind the pinned media-tool identities")
    expected_read_scope = {
        "global_metadata_lookup": True,
        "unlisted_repository_content_access": False,
        "repository_content_mode": "explicit_inputs_plus_build",
        "system_content_roots": [
            str(path) for path in runner_module.SYSTEM_READ_ROOTS
        ],
        "rationale": (
            "The macOS Python launcher and native dependencies require the "
            "listed system content roots plus global metadata; unlisted "
            "repository file contents remain denied."
        ),
    }
    if policy_receipt.get("filesystem_read_scope") != expected_read_scope:
        errors.append("sandbox policy receipt filesystem read scope differs from the tracked runner")
    resource_limits = policy_receipt.get("resource_limits", {})
    expected_static_limits = {
        "max_open_files": 256,
        "max_processes": runner_module.MAX_PROCESSES,
        "max_resident_memory_bytes": None,
        "memory_limit_status": runner_module.MEMORY_LIMIT_STATUS,
        "core_dump_bytes": 0,
    }
    if any(
        resource_limits.get(name) != expected
        for name, expected in expected_static_limits.items()
    ):
        errors.append(
            "sandbox policy receipt resource limits differ from the tracked runner"
        )
    expected_resource_checks = {
        "memory_bound",
        "core_dump_bytes",
        "cpu_seconds",
        "max_file_size_bytes",
        "max_open_files",
        "max_processes",
    }
    resource_checks = policy_receipt.get("resource_limit_self_test", {})
    if (
        set(resource_checks) != expected_resource_checks
        or any(
            value != (
                runner_module.MEMORY_LIMIT_STATUS
                if name == "memory_bound" else "pass"
            )
            for name, value in resource_checks.items()
        )
    ):
        errors.append("sandbox policy receipt resource-limit self-test did not pass")
    preflight = policy_receipt.get("source_preflight", {})
    if preflight.get("scene_sha256") != target.get("scene_sha256"):
        errors.append("sandbox policy receipt source preflight binds a different scene")
    expected_auditor = expected_binding(
        ledger.get("scene_source_auditor_path"), ledger.get("scene_source_auditor_sha256")
    )
    if preflight.get("auditor") != expected_auditor:
        errors.append("sandbox policy receipt does not bind the current source auditor")

    outputs = {
        row.get("role"): row for row in policy_receipt.get("outputs", [])
        if isinstance(row, dict)
    }
    runner_steps = policy_receipt.get("render_steps", [])
    normalized_steps = [
        {
            "phase": row.get("phase"),
            "command_argv": row.get("command_argv"),
            "exit_code": row.get("exit_code"),
        }
        for row in runner_steps if isinstance(row, dict)
    ]
    if expected_profile == "release":
        final_steps = render_receipt.get("render", {}).get("render_steps", [])
        if normalized_steps != final_steps:
            errors.append("render receipt command sequence does not reproduce the isolated runner receipt")
    expected_step_count = 2
    if len(runner_steps) == expected_step_count:
        scene_argv = runner_steps[0].get("command_argv", [])
        try:
            seed_value = int(scene_argv[scene_argv.index("--seed") + 1])
        except (ValueError, IndexError):
            errors.append("isolated scene command lacks a parseable deterministic seed")
        else:
            if expected_profile == "release" and seed_value != render_receipt.get("render", {}).get("random_seed"):
                errors.append("isolated scene seed differs from the final render receipt")
            scene_class = scene_argv[-1] if scene_argv else ""
            scene_path = safe_repo_path(target.get("scene_path", ""))
            media_root = (
                ROOT / f"build/visual_edition/isolated-renders/{entry.get('chapter_id')}/{expected_profile}/media"
            ).resolve()
            if scene_path is None or not isinstance(scene_class, str) or not scene_class.isidentifier():
                errors.append("isolated scene command lacks a valid canonical scene and class")
            else:
                expected_scene_argv = runner_module.manim_command(
                    scene_path, scene_class, entry.get("chapter_id"), expected_profile,
                    seed_value, media_root,
                )
                if scene_argv != expected_scene_argv:
                    errors.append(
                        f"isolated scene command does not exactly reproduce the tracked runner {expected_profile} command"
                    )
                if check_files and scene_path.is_file():
                    classes = {
                        node.name for node in ast.parse(scene_path.read_text(encoding="utf-8")).body
                        if isinstance(node, ast.ClassDef)
                    }
                    if scene_class not in classes:
                        errors.append("isolated scene command names a class absent from the bound scene")
        if expected_profile in {"draft", "release"}:
            mux_argv = runner_steps[1].get("command_argv", [])
            visual_path = safe_repo_path(outputs.get("visual_track", {}).get("path", ""))
            audio_binding = policy_receipt.get("audio_master")
            audio_path = (
                safe_repo_path(audio_binding.get("path", ""))
                if isinstance(audio_binding, dict) else None
            )
            master_path = (
                safe_repo_path(target.get("master_path", ""))
                if expected_profile == "release"
                else (
                    ROOT
                    / f"build/visual_edition/isolated-renders/{entry.get('chapter_id')}/draft/{entry.get('chapter_id')}-animatic.mp4"
                ).resolve()
            )
            ffmpeg = mux_argv[0] if mux_argv else ""
            expected_ffmpeg = visual_toolchain.get("media_tools", {}).get(
                "ffmpeg", {}
            ).get("path")
            if (
                visual_path is None
                or audio_path is None
                or master_path is None
                or not isinstance(ffmpeg, str)
                or ffmpeg != expected_ffmpeg
            ):
                errors.append("isolated mux command lacks canonical executable or artifact paths")
            else:
                pending_output = runner_module.pending_mux_output(
                    master_path, expected_profile
                )
                expected_mux_argv = runner_module.mux_command(
                    ffmpeg,
                    visual_path,
                    audio_path,
                    pending_output,
                    expected_profile,
                )
                if mux_argv != expected_mux_argv:
                    errors.append("isolated mux command does not exactly reproduce the tracked runner release command")
    elif not any("render_steps" in error for error in errors):
        errors.append(
            f"{expected_profile} sandbox receipt must contain exactly {expected_step_count} render step(s)"
        )

    if expected_profile == "release":
        master = outputs.get("muxed_master", {})
        if (
            master.get("path") != target.get("master_path")
            or master.get("sha256") != target.get("master_sha256")
        ):
            errors.append("sandbox policy receipt does not bind the ledger master")
    else:
        visual = outputs.get("muxed_master", {})
        if reviewed_master is None or {
            "path": visual.get("path"), "sha256": visual.get("sha256")
        } != reviewed_master:
            errors.append("draft sandbox receipt does not bind the reviewed audio animatic")
        visual_path = safe_repo_path(visual.get("path", ""))
        expected_root = (
            ROOT / f"build/visual_edition/isolated-renders/{entry.get('chapter_id')}/draft"
        ).resolve()
        if visual_path is None:
            errors.append("draft sandbox receipt visual track path is invalid")
        else:
            try:
                visual_path.relative_to(expected_root)
            except ValueError:
                errors.append("draft sandbox receipt audio animatic escapes its canonical output root")
    if check_files:
        for role, output in outputs.items():
            errors.extend(binding_errors(output, f"sandbox_policy_receipt.output.{role}"))
            output_path = safe_repo_path(output.get("path", ""))
            if output_path and output_path.is_file() and output.get("size_bytes") != output_path.stat().st_size:
                errors.append(f"sandbox policy receipt output {role} size drift")
        policy_binding = policy_receipt.get("policy", {})
        errors.extend(binding_errors(policy_binding, "sandbox_policy_receipt.policy"))
        policy_path = safe_repo_path(policy_binding.get("path", "")) if isinstance(policy_binding, dict) else None
        if policy_path and policy_path.is_file() and isinstance(treatment, dict):
            scene_path = safe_repo_path(target.get("scene_path", ""))
            treatment_path = safe_repo_path(target.get("treatment_path", ""))
            audio_binding = policy_receipt.get("audio_master", {})
            audio_path = safe_repo_path(audio_binding.get("path", "")) if isinstance(audio_binding, dict) else None
            asset_paths = []
            for row in treatment.get("art_direction", {}).get("asset_plan", []):
                if (
                    isinstance(row, dict)
                    and row.get("status") in {"original", "rights_cleared"}
                    and row.get("security_review") in {"pass", "not_applicable"}
                ):
                    path = safe_repo_path(row.get("path_or_source", ""))
                    if path:
                        asset_paths.append(path)
            read_paths = [
                scene_path,
                treatment_path,
                ROOT / "visual_edition/manim.cfg",
                ROOT / "visual_edition/toolchain.json",
                ROOT / "visual_edition/__init__.py",
                ROOT / "visual_edition/lib/__init__.py",
                ROOT / "visual_edition/lib/asi_visuals.py",
                *asset_paths,
            ]
            if audio_path:
                read_paths.append(audio_path)
            expected_policy = runner_module.build_policy([path for path in read_paths if path])
            if policy_path.read_text(encoding="utf-8") != expected_policy:
                errors.append(
                    "sandbox policy text does not match the tracked runner's "
                    "repository-read contract"
                )
    return errors


def render_receipt_errors(
    receipt: dict,
    receipt_schema: dict,
    ledger: dict,
    entry: dict,
    plan: dict | None,
    treatment: dict | None,
    sandbox_schema: dict,
    runner_module,
    *,
    check_files: bool,
) -> list[str]:
    errors = [
        f"render-receipt-schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(receipt_schema).iter_errors(receipt)
    ]
    target = entry.get("target", {})
    if receipt.get("chapter_id") != entry.get("chapter_id"):
        errors.append("render receipt chapter identity drift")
    if isinstance(treatment, dict) and receipt.get("source_commit") != treatment.get("source_commit"):
        errors.append("render receipt source commit differs from the treatment")
    visual_toolchain = json.loads((ROOT / ledger["visual_toolchain_path"]).read_text(encoding="utf-8"))
    if receipt.get("render", {}).get("toolchain_id") != visual_toolchain.get("toolchain_id"):
        errors.append("render receipt names a different visual toolchain")
    timing = plan.get("timing", {}) if isinstance(plan, dict) else {}
    expected_inputs = {
        "chapter": expected_binding(entry.get("chapter_path"), entry.get("chapter_sha256")),
        "treatment": expected_binding(target.get("treatment_path"), target.get("treatment_sha256")),
        "beat_plan": expected_binding(target.get("beat_plan_path"), target.get("beat_plan_sha256")),
        "scene": expected_binding(target.get("scene_path"), target.get("scene_sha256")),
        "narration": expected_binding(target.get("narration_path"), target.get("narration_sha256")),
        "visual_grammar": expected_binding(ledger.get("visual_grammar_path"), ledger.get("visual_grammar_sha256")),
        "visual_toolchain": expected_binding(ledger.get("visual_toolchain_path"), ledger.get("visual_toolchain_sha256")),
        "primitive_library": expected_binding(ledger.get("primitive_library_path"), ledger.get("primitive_library_sha256")),
        "scene_source_auditor": expected_binding(ledger.get("scene_source_auditor_path"), ledger.get("scene_source_auditor_sha256")),
        "isolated_render_runner": expected_binding(ledger.get("isolated_render_runner_path"), ledger.get("isolated_render_runner_sha256")),
        "final_receipt_compiler": expected_binding(
            "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py",
            ledger.get("authoring_component_sha256", {}).get(
                "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py"
            ),
        ),
        "av_auditor": expected_binding(
            "skills/asi-stack-manim-videos/scripts/audit_av_experience.py",
            ledger.get("authoring_component_sha256", {}).get(
                "skills/asi-stack-manim-videos/scripts/audit_av_experience.py"
            ),
        ),
        "av_diagnostics_schema": expected_binding(
            ledger.get("av_diagnostics_schema_path"),
            ledger.get("av_diagnostics_schema_sha256"),
        ),
        "sandbox_policy_receipt_schema": expected_binding(ledger.get("sandbox_policy_receipt_schema_path"), ledger.get("sandbox_policy_receipt_schema_sha256")),
        "primitive_regression_manifest": expected_binding(ledger.get("primitive_regression_manifest_path"), ledger.get("primitive_regression_manifest_sha256")),
        "narration_toolchain": expected_binding(ledger.get("narration_toolchain_path"), ledger.get("narration_toolchain_sha256")),
        "timing_receipt": expected_binding(timing.get("receipt_path"), timing.get("receipt_sha256")),
        "narration_render_receipt": expected_binding(
            timing.get("narration_receipt_path"),
            timing.get("narration_receipt_sha256"),
        ),
        "narration_verification_report": expected_binding(
            timing.get("narration_verification_report_path"),
            timing.get("narration_verification_report_sha256"),
        ),
    }
    bindings = receipt.get("input_bindings", {})
    if not isinstance(bindings, dict):
        bindings = {}
    for name, expected in expected_inputs.items():
        actual = bindings.get(name, {})
        if actual != expected:
            errors.append(f"render receipt {name} does not bind the canonical input")
        if check_files:
            errors.extend(binding_errors(actual, f"render_receipt.{name}"))
    audio_binding = bindings.get("audio_master", {})
    if check_files:
        errors.extend(binding_errors(audio_binding, "render_receipt.audio_master"))
        if isinstance(plan, dict):
            narration_toolchain = json.loads(
                (ROOT / ledger["narration_toolchain_path"]).read_text(encoding="utf-8")
            )
            errors.extend(
                narration_custody_errors(
                    entry, plan, treatment, narration_toolchain
                )
            )
            narration_receipt_path = safe_repo_path(
                plan.get("timing", {}).get("narration_receipt_path", "")
            )
            if narration_receipt_path and narration_receipt_path.is_file():
                narration_receipt = json.loads(
                    narration_receipt_path.read_text(encoding="utf-8")
                )
                expected_audio = {
                    "path": narration_receipt.get("output_path"),
                    "sha256": narration_receipt.get("output_sha256"),
                }
                if audio_binding != expected_audio:
                    errors.append("render receipt audio master differs from verified narration output")

    security = receipt.get("execution_security", {})
    if security.get("source_preflight_scene_sha256") != target.get("scene_sha256"):
        errors.append("render receipt source preflight binds a different scene")
    if security.get("network_access") is not False:
        errors.append("render receipt does not prove network-denied execution")
    if security.get("credential_environment_inherited") is not False:
        errors.append("render receipt inherited credential environment variables")
    if check_files:
        policy_binding = security.get("sandbox_policy_receipt", {})
        errors.extend(binding_errors(policy_binding, "render_receipt.sandbox_policy_receipt"))
        policy_path = safe_repo_path(policy_binding.get("path", "")) if isinstance(policy_binding, dict) else None
        if policy_path and policy_path.is_file():
            try:
                policy_receipt = json.loads(policy_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"sandbox policy receipt is not readable JSON: {exc}")
            else:
                errors.extend(
                    sandbox_policy_receipt_errors(
                        policy_receipt, sandbox_schema, ledger, entry, treatment,
                        receipt, runner_module, check_files=True,
                    )
                )

    output = receipt.get("output", {})
    if output.get("path") != target.get("master_path") or output.get("sha256") != target.get("master_sha256"):
        errors.append("render receipt output does not bind the ledger master")
    if isinstance(plan, dict):
        planned_duration = plan.get("target_duration_seconds")
        actual_duration = output.get("duration_seconds")
        if isinstance(planned_duration, (int, float)) and isinstance(actual_duration, (int, float)):
            if abs(float(planned_duration) - float(actual_duration)) > 0.25:
                errors.append("render receipt duration differs from the audio-timed beat plan")
    if check_files:
        errors.extend(binding_errors(output, "render_receipt.output"))
        diagnostics = receipt.get("av_diagnostics", {})
        errors.extend(binding_errors(diagnostics, "render_receipt.av_diagnostics"))
        diagnostics_path = safe_repo_path(diagnostics.get("path", "")) if isinstance(diagnostics, dict) else None
        if diagnostics_path and diagnostics_path.is_file():
            report = json.loads(diagnostics_path.read_text(encoding="utf-8"))
            diagnostics_schema_path = safe_repo_path(
                ledger.get("av_diagnostics_schema_path", "")
            )
            if diagnostics_schema_path is None or not diagnostics_schema_path.is_file():
                errors.append("A/V diagnostics schema is missing")
            else:
                diagnostics_schema = json.loads(
                    diagnostics_schema_path.read_text(encoding="utf-8")
                )
                errors.extend(
                    "av-diagnostics-schema:"
                    f"{'.'.join(map(str, error.path))}: {error.message}"
                    for error in Draft202012Validator(diagnostics_schema).iter_errors(
                        report
                    )
                )
            if report.get("video_sha256") != target.get("master_sha256"):
                errors.append("A/V diagnostics were run against a different master")
            if report.get("beat_plan_sha256") != target.get("beat_plan_sha256"):
                errors.append("A/V diagnostics were run against a different beat plan")
            if report.get("video") != target.get("master_path"):
                errors.append("A/V diagnostics name a noncanonical master path")
            if report.get("beat_plan") != target.get("beat_plan_path"):
                errors.append("A/V diagnostics name a noncanonical beat-plan path")
            visual_toolchain = json.loads(
                (ROOT / ledger["visual_toolchain_path"]).read_text(encoding="utf-8")
            )
            if report.get("media_tools") != visual_toolchain.get("media_tools"):
                errors.append("A/V diagnostics do not bind the pinned media tools")
            av_path = "skills/asi-stack-manim-videos/scripts/audit_av_experience.py"
            expected_av_auditor = {
                "path": av_path,
                "sha256": digest(ROOT / av_path),
            }
            if report.get("auditor") != expected_av_auditor:
                errors.append("A/V diagnostics do not bind the current tracked auditor")
            if ledger.get("authoring_component_sha256", {}).get(av_path) != expected_av_auditor["sha256"]:
                errors.append("production ledger does not bind the current A/V auditor")
            if isinstance(plan, dict):
                av_module = load_skill_script(
                    "audit_av_experience.py", "asi_stack_manim_av_validator"
                )
                if report.get("detection_contract") != av_module.DETECTION_CONTRACT:
                    errors.append(
                        "A/V diagnostics weaken or alter the governed detection contract"
                    )
                try:
                    declared_freezes, undeclared_freezes = av_module.classify_declared_intervals(
                        report.get("freezes", []), plan.get("beats", []), kind="freeze"
                    )
                    declared_silences, undeclared_silences = av_module.classify_declared_intervals(
                        report.get("silences", []), plan.get("beats", []), kind="silence"
                    )
                except (KeyError, TypeError, ValueError):
                    errors.append("A/V diagnostics contain malformed interval custody")
                else:
                    if (
                        report.get("declared_freezes") != declared_freezes
                        or report.get("undeclared_freezes") != undeclared_freezes
                        or report.get("declared_silences") != declared_silences
                        or report.get("undeclared_silences") != undeclared_silences
                    ):
                        errors.append(
                            "A/V diagnostic interval classifications do not reproduce from the beat plan"
                        )
            if report.get("errors"):
                errors.append("A/V diagnostics retain mechanical errors")
            if report.get("warnings"):
                errors.append("A/V diagnostics retain unresolved warnings")
            if report.get("validation_state") != "pass":
                errors.append("A/V diagnostics have not reached a warning-free pass state")
    assets = (
        treatment.get("art_direction", {}).get("asset_plan", [])
        if isinstance(treatment, dict) else []
    )
    expected_rights = "no_external_assets" if not assets else "cleared"
    if receipt.get("asset_rights_state") != expected_rights:
        errors.append("render receipt asset-rights state does not match the treatment")
    unresolved_assets = [
        row for row in assets
        if not isinstance(row, dict)
        or row.get("status") not in {"original", "rights_cleared"}
        or row.get("security_review") not in {"pass", "not_applicable"}
        or not row.get("sha256")
    ]
    if unresolved_assets:
        errors.append("render receipt cannot close custody over planned or unreviewed assets")
    return errors


def review_context_manifest_errors(
    review: dict,
    pass_name: str,
    expected_bindings: dict[str, dict],
    treatment: dict | None,
) -> list[str]:
    errors: list[str] = []
    context = review.get("review_context", {})
    if not isinstance(context, dict):
        return ["review context must be an object"]
    manifest_binding = {
        "path": context.get("context_manifest_path"),
        "sha256": context.get("context_manifest_sha256"),
    }
    raw_binding = {
        "path": context.get("raw_review_path"),
        "sha256": context.get("raw_review_sha256"),
    }
    errors.extend(binding_errors(manifest_binding, f"{pass_name}.context_manifest"))
    errors.extend(binding_errors(raw_binding, f"{pass_name}.raw_review"))
    manifest_path = safe_repo_path(context.get("context_manifest_path", ""))
    if manifest_path is None or not manifest_path.is_file():
        return errors
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "schemas/manim_review_context_manifest.schema.json").read_text(encoding="utf-8")
    )
    errors.extend(
        f"context-manifest-schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(manifest)
    )
    if (
        manifest.get("chapter_id") != review.get("chapter_id")
        or manifest.get("generation") != review.get("generation")
        or manifest.get("review_pass") != pass_name
        or manifest.get("review_session_id") != context.get("review_session_id")
    ):
        errors.append("review context manifest identity drift")

    kind_to_binding = {
        "rendered_video": expected_bindings.get("reviewed_master"),
        "captions": expected_bindings.get("captions"),
        "descriptive_transcript": expected_bindings.get("transcript"),
        "chapter": expected_bindings.get("chapter"),
        "narration_script": expected_bindings.get("narration"),
        "treatment": expected_bindings.get("treatment"),
        "beat_plan": expected_bindings.get("beat_plan"),
        "scene_code": expected_bindings.get("scene"),
        "render_receipt": expected_bindings.get("render_receipt"),
        "sandbox_policy_receipt": expected_bindings.get("sandbox_policy_receipt"),
        "av_diagnostics": expected_bindings.get("av_diagnostics"),
        "sample_manifest": {
            "path": review.get("frame_sampling", {}).get("sample_manifest_path"),
            "sha256": review.get("frame_sampling", {}).get("sample_manifest_sha256"),
        },
    }
    expected_materials: list[dict] = []
    for kind in context.get("allowed_materials", []):
        if kind == "answer_key":
            continue
        if kind == "source_notes":
            source_ids = (
                treatment.get("content_contract", {}).get("source_ids", [])
                if isinstance(treatment, dict) else []
            )
            for source_id in source_ids:
                path = ROOT / f"sources/source_notes/{source_id}.md"
                if path.is_file():
                    expected_materials.append({
                        "kind": "source_notes",
                        "path": str(path.relative_to(ROOT)),
                        "sha256": digest(path),
                    })
            continue
        binding = kind_to_binding.get(kind)
        if isinstance(binding, dict) and binding.get("path") and binding.get("sha256"):
            expected_materials.append({"kind": kind, **binding})
    actual_materials = manifest.get("material_bindings", [])

    def normalized_materials(rows: list) -> list[tuple]:
        return sorted(
            (row.get("kind"), row.get("path"), row.get("sha256"))
            for row in rows if isinstance(row, dict)
        )

    if normalized_materials(actual_materials) != normalized_materials(expected_materials):
        errors.append("review context manifest does not exactly match allowed artifact bindings")
    for row in actual_materials if isinstance(actual_materials, list) else []:
        errors.extend(binding_errors(row, f"{pass_name}.context_material"))
    errors.extend(binding_errors(manifest.get("prompt_binding", {}), f"{pass_name}.review_prompt"))

    environment = manifest.get("environment_class")
    if pass_name in {"release_candidate", "independent_release_candidate"}:
        if environment not in {"fresh_isolated_ai_task", "independent_human_session"}:
            errors.append(f"{pass_name} was not run in an independent review environment")
        if not manifest.get("isolated_from_prior_artifact_context"):
            errors.append(f"{pass_name} context inherited prior artifact context")
        if manifest.get("prior_review_included"):
            errors.append(f"{pass_name} context included a prior review")
    if pass_name == "independent_release_candidate":
        if not manifest.get("isolated_from_prior_artifact_context"):
            errors.append("cold audience proxy context was not isolated from prior artifact context")
        if manifest.get("prior_review_included"):
            errors.append("cold audience proxy received a prior review")
        prompt_path = safe_repo_path(manifest.get("prompt_binding", {}).get("path", ""))
        raw_path = safe_repo_path(context.get("raw_review_path", ""))
        if prompt_path and prompt_path.is_file() and raw_path and raw_path.is_file():
            prompt_text = " ".join(prompt_path.read_text(encoding="utf-8").split()).casefold()
            raw_text = " ".join(raw_path.read_text(encoding="utf-8").split()).casefold()
            learning = review.get("learning_check", {})
            for field in ("comprehension_prompt", "transfer_prompt"):
                value = learning.get(field)
                if isinstance(value, str) and " ".join(value.split()).casefold() not in prompt_text:
                    errors.append(f"cold audience proxy prompt omits the frozen {field}")
            for field in ("comprehension_raw_response", "transfer_raw_response"):
                value = learning.get(field)
                if isinstance(value, str) and " ".join(value.split()).casefold() not in raw_text:
                    errors.append(f"cold audience proxy raw artifact omits {field}")
            for field in ("comprehension_success_criteria", "transfer_success_criteria"):
                for criterion in learning.get(field, []):
                    normalized = " ".join(criterion.split()).casefold()
                    if normalized and (normalized in prompt_text or normalized in raw_text):
                        errors.append("cold audience proxy received success criteria before assessment")
    return errors


def sample_manifest_errors(
    manifest_path: Path,
    review: dict,
    expected_bindings: dict[str, dict],
    plan: dict,
) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"sample manifest is unreadable: {exc}"]
    schema_path = ROOT / "schemas/manim_frame_sample_manifest.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors.extend(
        "sample-manifest-schema:"
        f"{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(manifest)
    )
    expected_sampler = {
        "path": "skills/asi-stack-manim-videos/scripts/sample_video_beats.py",
        "sha256": digest(
            ROOT / "skills/asi-stack-manim-videos/scripts/sample_video_beats.py"
        ),
    }
    if manifest.get("sampler") != expected_sampler:
        errors.append("sample manifest does not bind the current tracked sampler")
    expected_sample_set = (
        "animatic" if review.get("pass") == "animatic" else "final"
    )
    if manifest.get("sample_set") != expected_sample_set:
        errors.append("sample manifest names the wrong governed sample set")
    expected_manifest_path = (
        ROOT
        / f"visual_edition/chapters/{review.get('chapter_id')}/generation-2/receipts/{expected_sample_set}-sample-manifest.json"
    ).resolve()
    if manifest_path.resolve() != expected_manifest_path:
        errors.append("sample manifest does not use its canonical tracked path")
    visual_toolchain = json.loads(
        (ROOT / "visual_edition/toolchain.json").read_text(encoding="utf-8")
    )
    if manifest.get("media_tools") != {
        "ffmpeg": visual_toolchain.get("media_tools", {}).get("ffmpeg")
    }:
        errors.append("sample manifest does not bind the pinned FFmpeg identity")
    if manifest.get("chapter_id") != review.get("chapter_id"):
        errors.append("sample manifest chapter identity drift")
    if manifest.get("video_sha256") != expected_bindings.get("reviewed_master", {}).get("sha256"):
        errors.append("sample manifest was extracted from a different reviewed master")
    if manifest.get("beat_plan_sha256") != expected_bindings.get("beat_plan", {}).get("sha256"):
        errors.append("sample manifest was extracted from a different beat plan")
    if manifest.get("video_path") != expected_bindings.get("reviewed_master", {}).get("path"):
        errors.append("sample manifest names a different reviewed master")
    if manifest.get("beat_plan_path") != expected_bindings.get("beat_plan", {}).get("path"):
        errors.append("sample manifest names a different beat plan")

    beats = plan.get("beats", []) if isinstance(plan, dict) else []
    expected = {
        beat.get("id"): beat for beat in beats
        if isinstance(beat, dict) and isinstance(beat.get("id"), str)
    }
    rows = manifest.get("beats", [])
    if not isinstance(rows, list):
        return errors + ["sample manifest beats must be a list"]
    row_ids = [row.get("beat_id") for row in rows if isinstance(row, dict)]
    if row_ids != list(expected):
        errors.append("sample manifest does not cover every beat exactly once and in plan order")
    if (
        manifest.get("expected_beat_count") != len(expected)
        or manifest.get("sampled_beat_count") != len(rows)
    ):
        errors.append("sample manifest beat-count fields do not reproduce from its rows")
    frame_sampling = review.get("frame_sampling", {})
    if not isinstance(frame_sampling, dict):
        frame_sampling = {}
    required_samples = frame_sampling.get("samples_per_beat", 5)
    for row in rows:
        if not isinstance(row, dict):
            errors.append("sample manifest contains a non-object beat row")
            continue
        beat_id = row.get("beat_id")
        plan_beat = expected.get(beat_id)
        samples = row.get("samples", [])
        if not isinstance(samples, list) or len(samples) < required_samples:
            errors.append(f"sample manifest beat {beat_id!r} has fewer than {required_samples} samples")
            continue
        timestamps = [sample.get("timestamp_seconds") for sample in samples if isinstance(sample, dict)]
        if len(timestamps) != len(samples) or len(set(timestamps)) != len(timestamps):
            errors.append(f"sample manifest beat {beat_id!r} has missing or duplicated timestamps")
        if plan_beat:
            start = plan_beat.get("start_seconds")
            end = plan_beat.get("end_seconds")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                errors.append(f"sample manifest beat {beat_id!r} has an invalid plan interval")
            elif any(
                not isinstance(value, (int, float)) or value < start or value > end
                for value in timestamps
            ):
                errors.append(f"sample manifest beat {beat_id!r} samples outside its plan interval")
        for sample in samples:
            if not isinstance(sample, dict):
                continue
            relative = sample.get("path")
            sample_path = (ROOT / relative).resolve() if isinstance(relative, str) else None
            if sample_path is None:
                errors.append(f"sample manifest beat {beat_id!r} has no sample path")
                continue
            try:
                sample_path.relative_to(
                    (
                        ROOT
                        / f"build/visual_edition/review-samples/{review.get('chapter_id')}/{expected_sample_set}"
                    ).resolve()
                )
            except ValueError:
                errors.append(f"sample manifest beat {beat_id!r} sample escapes its canonical build root")
                continue
            if not sample_path.is_file() or digest(sample_path) != sample.get("sha256"):
                errors.append(f"sample manifest beat {beat_id!r} sample identity drift")
    targeted = manifest.get("targeted_transition_samples", [])
    if not isinstance(targeted, list):
        errors.append("sample manifest targeted_transition_samples must be a list")
    elif len(targeted) != frame_sampling.get("targeted_transition_samples"):
        errors.append("sample manifest targeted-transition count does not match the review")
    else:
        for sample in targeted:
            if not isinstance(sample, dict):
                errors.append("sample manifest contains a non-object targeted sample")
                continue
            beat_id = sample.get("beat_id")
            plan_beat = expected.get(beat_id)
            timestamp = sample.get("timestamp_seconds")
            if plan_beat is None:
                errors.append(
                    f"sample manifest targeted sample names unknown beat {beat_id!r}"
                )
            elif (
                not isinstance(timestamp, (int, float))
                or timestamp < plan_beat.get("start_seconds", float("inf"))
                or timestamp > plan_beat.get("end_seconds", float("-inf"))
            ):
                errors.append(
                    f"sample manifest targeted sample lies outside beat {beat_id!r}"
                )
            relative = sample.get("path")
            sample_path = (
                (ROOT / relative).resolve()
                if isinstance(relative, str)
                else None
            )
            if sample_path is None:
                errors.append("sample manifest targeted sample has no path")
                continue
            try:
                sample_path.relative_to(
                    (
                        ROOT
                        / f"build/visual_edition/review-samples/{review.get('chapter_id')}/{expected_sample_set}"
                    ).resolve()
                )
            except ValueError:
                errors.append("sample manifest targeted sample escapes its canonical build root")
                continue
            if not sample_path.is_file() or digest(sample_path) != sample.get("sha256"):
                errors.append("sample manifest targeted sample identity drift")
    return errors


def review_contract_errors(
    review: dict,
    pass_name: str,
    expected_bindings: dict[str, dict],
    plan_or_beat_count: dict | int,
    treatment: dict | None,
    *,
    check_files: bool,
) -> list[str]:
    """Apply review semantics that JSON Schema cannot express."""

    errors: list[str] = []
    if review.get("pass") != pass_name:
        errors.append(f"{pass_name} review declares the wrong pass")
    role = review.get("review_role")
    expected_role = {
        "animatic": "implementation_diagnostic",
        "picture_and_sound_lock": "implementation_diagnostic",
        "release_candidate": "source_aware_critic",
        "independent_release_candidate": "cold_audience_proxy",
    }[pass_name]
    if role != expected_role:
        errors.append(f"{pass_name} requires review_role {expected_role}")

    bindings = review.get("artifact_bindings", {})
    if not isinstance(bindings, dict):
        bindings = {}
    for name, expected in expected_bindings.items():
        actual = bindings.get(name)
        if expected is None:
            if actual is not None:
                errors.append(f"{pass_name}.{name} must be null at this review stage")
            continue
        if check_files:
            errors.extend(binding_errors(actual, f"{pass_name}.{name}", expected))
        elif actual != expected:
            errors.append(f"{pass_name}.{name} does not bind the ledger-owned artifact identity")

    context = review.get("review_context", {})
    if not isinstance(context, dict):
        context = {}
    allowed = set(context.get("allowed_materials", []))
    if context.get("review_session_id") is None:
        errors.append(f"{pass_name} lacks a review session identity")
    if pass_name == "release_candidate":
        if context.get("script_author") or context.get("scene_implementer"):
            errors.append("source-aware release critic must be independent of script and scene authorship")
        source_aware_materials = {
            "rendered_video", "captions", "descriptive_transcript", "chapter",
            "source_notes", "narration_script", "treatment", "beat_plan",
            "scene_code", "render_receipt", "sandbox_policy_receipt",
            "av_diagnostics", "sample_manifest",
        }
        if not source_aware_materials.issubset(allowed) or "answer_key" in allowed:
            errors.append("source-aware release critic lacks the materials needed for claim-fidelity review")
    if pass_name == "independent_release_candidate":
        prohibited = {
            "chapter", "source_notes", "narration_script", "treatment", "beat_plan",
            "scene_code", "answer_key",
        }
        if context.get("prior_exposure") != "cold":
            errors.append("cold audience proxy has prior exposure")
        if context.get("script_author") or context.get("scene_implementer"):
            errors.append("cold audience proxy participated in authorship or implementation")
        if allowed - {"rendered_video", "captions", "descriptive_transcript"} or allowed & prohibited:
            errors.append("cold audience proxy context leaks source, script, implementation, or answer-key material")
    if check_files:
        errors.extend(
            review_context_manifest_errors(
                review, pass_name, expected_bindings, treatment
            )
        )

    beat_count = (
        len(plan_or_beat_count.get("beats", []))
        if isinstance(plan_or_beat_count, dict)
        else plan_or_beat_count
    )
    samples = review.get("frame_sampling", {})
    if not isinstance(samples, dict):
        samples = {}
    if samples.get("expected_beat_count") != beat_count:
        errors.append("frame sample manifest expects the wrong beat count")
    if samples.get("sampled_beat_count") != beat_count:
        errors.append("frame sampling does not cover every beat")
    if samples.get("unresolved_interpolation_defects") != 0:
        errors.append("frame sampling leaves unresolved interpolation defects")
    manifest_binding = {
        "path": samples.get("sample_manifest_path"),
        "sha256": samples.get("sample_manifest_sha256"),
    }
    if check_files:
        errors.extend(binding_errors(manifest_binding, f"{pass_name}.sample_manifest"))
        manifest_path = safe_repo_path(samples.get("sample_manifest_path", ""))
        if manifest_path and manifest_path.is_file() and isinstance(plan_or_beat_count, dict):
            errors.extend(
                sample_manifest_errors(
                    manifest_path, review, expected_bindings, plan_or_beat_count
                )
            )

    required_viewing = set(ALL_VIEWING_PASSES)
    if pass_name == "animatic":
        required_viewing = {
            "normal_speed", "muted", "audio_only", "phone", "random_frames"
        }
    elif pass_name == "independent_release_candidate":
        required_viewing = {"normal_speed", "captions_on", "phone", "random_frames"}
    for name in required_viewing:
        viewing = review.get("viewing_passes", {})
        row = viewing.get(name, {}) if isinstance(viewing, dict) else {}
        result = row.get("result") if isinstance(row, dict) else row
        if result != "pass":
            errors.append(f"{pass_name} required viewing pass {name} did not pass")
    if pass_name == "animatic":
        captions_result = review.get("viewing_passes", {}).get(
            "captions_on", {}
        ).get("result")
        if captions_result != "not_applicable":
            errors.append(
                "animatic captions-on viewing must remain not_applicable before captions exist"
            )
    phone = review.get("phone_review", {})
    if not isinstance(phone, dict):
        phone = {}
    if phone.get("complete_playback") is not True:
        errors.append(f"{pass_name} phone review did not cover the complete candidate")
    if phone.get("zoom_used") is not False:
        errors.append(f"{pass_name} phone review used zoom")
    if phone.get("audio_enabled") is not True:
        errors.append(f"{pass_name} phone review did not include audio")
    method_is_physical = phone.get("method") == "physical_device"
    if phone.get("physical_device") is not method_is_physical:
        errors.append(f"{pass_name} phone review method and physical-device flag disagree")
    width = phone.get("viewport_css_width_px")
    if pass_name == "animatic":
        if not isinstance(width, int) or isinstance(width, bool) or width > 360:
            errors.append("animatic phone viewport exceeds 360 CSS pixels")
        if phone.get("captions_enabled") is not False:
            errors.append("animatic phone review claims captions before captions exist")
    else:
        if phone.get("method") != "physical_device" or phone.get("physical_device") is not True:
            errors.append(f"{pass_name} requires complete playback on a physical phone")
        if phone.get("captions_enabled") is not True:
            errors.append(f"{pass_name} physical-phone review did not include captions")

    dimensions = review.get("dimensions", {})
    if not isinstance(dimensions, dict):
        dimensions = {}
    owned_dimensions = REVIEW_OWNED_DIMENSIONS[pass_name]
    for name in REVIEW_DIMENSIONS:
        row = dimensions.get(name, {})
        if not isinstance(row, dict):
            row = {"score": row, "evidence_timestamps": []}
        score = row.get("score")
        timestamps = row.get("evidence_timestamps", [])
        if name not in owned_dimensions:
            if score is not None or timestamps:
                errors.append(
                    f"{pass_name} must not score non-owned {name} dimension"
                )
            continue
        if not isinstance(score, int) or score < 4:
            errors.append(f"{pass_name} cannot average away a sub-4 or unscored {name} dimension")
        if not timestamps:
            errors.append(f"{pass_name} {name} score lacks timestamped evidence")

    learning = review.get("learning_check", {})
    if not isinstance(learning, dict):
        learning = {}
    if pass_name == "independent_release_candidate":
        if learning.get("reviewer_received_answer_key"):
            errors.append("cold learning proxy received the answer key")
        if (
            learning.get("status") != "pass"
            or learning.get("comprehension_result") != "pass"
            or learning.get("transfer_result") != "pass"
        ):
            errors.append("cold audience proxy lacks passing comprehension and changed-condition transfer")
        for field in (
            "comprehension_prompt", "comprehension_raw_response", "transfer_prompt",
            "transfer_raw_response", "assessor_id",
        ):
            if not learning.get(field):
                errors.append(f"cold audience proxy lacks {field}")
        for field in ("comprehension_success_criteria", "transfer_success_criteria"):
            if not learning.get(field):
                errors.append(f"cold audience proxy lacks predeclared {field}")
        if learning.get("artifact_grounding_result") != "pass" or not learning.get(
            "artifact_grounding"
        ):
            errors.append("cold audience proxy lacks artifact-specific response grounding")
        raw_response = " ".join(
            str(learning.get(field) or "")
            for field in ("comprehension_raw_response", "transfer_raw_response")
        )
        normalized_raw_response = " ".join(raw_response.split()).casefold()
        for row in learning.get("artifact_grounding", []):
            excerpt = row.get("response_excerpt") if isinstance(row, dict) else None
            if not isinstance(excerpt, str) or (
                " ".join(excerpt.split()).casefold() not in normalized_raw_response
            ):
                errors.append(
                    "cold audience proxy artifact grounding excerpt is not present in the raw response"
                )
        story = treatment.get("story", {}) if isinstance(treatment, dict) else {}
        frozen_fields = {
            "comprehension_prompt": "comprehension_question",
            "comprehension_success_criteria": "comprehension_success_criteria",
            "transfer_prompt": "transfer_question",
            "transfer_success_criteria": "transfer_success_criteria",
        }
        for review_field, treatment_field in frozen_fields.items():
            if learning.get(review_field) != story.get(treatment_field):
                errors.append(
                    f"cold audience proxy {review_field} does not match the predeclared treatment contract"
                )
    else:
        expected_not_run = {
            "status": "not_run",
            "comprehension_prompt": None,
            "comprehension_raw_response": None,
            "comprehension_success_criteria": [],
            "comprehension_result": "not_run",
            "transfer_prompt": None,
            "transfer_raw_response": None,
            "transfer_success_criteria": [],
            "transfer_result": "not_run",
            "artifact_grounding": [],
            "artifact_grounding_result": "not_run",
            "assessor_id": None,
            "misconception_or_failure_action": None,
        }
        if any(learning.get(key) != expected for key, expected in expected_not_run.items()):
            errors.append(
                f"{pass_name} must not manufacture a cold-proxy learning result"
            )

    defects = review.get("open_defects", [])
    if not isinstance(defects, list):
        defects = []
    unresolved = [
        defect for defect in defects
        if isinstance(defect, dict) and (
            defect.get("disposition") == "open"
        or (
            defect.get("disposition") == "accepted_with_rationale"
            and (defect.get("severity") != "minor" or not defect.get("rationale"))
        )
        )
    ]
    if review.get("verdict") == "pass" and unresolved:
        errors.append("passing review retains unresolved material defects")
    if review.get("verdict") == "revise" and not unresolved:
        errors.append("revise review does not own an unresolved defect")
    return errors


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

    treatment_schema = json.loads((ROOT / "schemas/manim_treatment.schema.json").read_text(encoding="utf-8"))
    beat_schema = json.loads((ROOT / "schemas/manim_beat_plan.schema.json").read_text(encoding="utf-8"))
    review_schema = json.loads((ROOT / "schemas/manim_experience_review.schema.json").read_text(encoding="utf-8"))
    receipt_schema = json.loads((ROOT / "schemas/manim_render_receipt.schema.json").read_text(encoding="utf-8"))
    sandbox_schema = json.loads((ROOT / "schemas/manim_sandbox_policy_receipt.schema.json").read_text(encoding="utf-8"))
    narration_toolchain = json.loads((ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8"))
    alignment_qualified = narration_toolchain.get("alignment", {}).get("qualification_state") == "qualified"
    beat_auditor = load_beat_auditor()
    scene_auditor = load_skill_script(
        "audit_scene_source.py", "asi_stack_manim_scene_source_auditor"
    )
    sys.modules["audit_scene_source"] = scene_auditor
    isolated_runner = load_skill_script(
        "render_scene_isolated.py", "asi_stack_manim_isolated_runner"
    )
    primitive_auditor = load_skill_script(
        "audit_primitive_regression.py", "asi_stack_manim_primitive_auditor"
    )
    try:
        errors.extend(
            f"primitive-regression:{error}"
            for error in primitive_auditor.static_audit_errors()
        )
    except Exception as exc:
        errors.append(f"primitive-regression audit could not run: {exc}")
    claims_by_chapter = canonical_claim_ids()
    sources_by_chapter = chapter_source_ids()
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    chapter_records = {
        chapter["id"]: chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    }
    inventory_source_ids = {
        row.get("id")
        for row in json.loads((ROOT / "sources/source_inventory.json").read_text(encoding="utf-8"))
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }

    for entry in value.get("entries", []):
        chapter_id = entry.get("chapter_id", "unknown")
        target = entry.get("target", {})
        gates = target.get("gates", {})
        stage = target.get("stage")
        gate_prerequisites = {
            "script": ("treatment",),
            "beat_plan": ("treatment", "script"),
            "animatic": ("treatment", "script", "beat_plan"),
            "picture_and_sound_lock": ("treatment", "script", "beat_plan", "animatic"),
            "release_candidate": ("treatment", "script", "beat_plan", "animatic", "picture_and_sound_lock"),
            "independent_release_candidate": ("release_candidate",),
        }
        for gate_name, prerequisites in gate_prerequisites.items():
            if gates.get(gate_name) == "pass":
                missing = [name for name in prerequisites if gates.get(name) != "pass"]
                if missing:
                    errors.append(f"{chapter_id}: {gate_name} passes before {', '.join(missing)}")

        if gates.get("accepted") == "pass":
            required = (
                "treatment", "script", "beat_plan", "animatic", "picture_and_sound_lock",
                "release_candidate", "independent_release_candidate", "technical", "claim_fidelity",
            )
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
            packet_path = safe_repo_path(predecessor.get("packet_path", ""))
            if packet_path is None or not packet_path.is_file():
                errors.append(f"{chapter_id}: predecessor packet is missing")
            elif json.loads(packet_path.read_text(encoding="utf-8"))["render_receipt"]["output_sha256"] != predecessor.get("master_sha256"):
                errors.append(f"{chapter_id}: predecessor master identity drift")

        narration_path = safe_repo_path(target.get("narration_path", ""))
        narration = narration_path.read_text(encoding="utf-8") if narration_path and narration_path.is_file() else None
        if narration is None:
            if target.get("narration_sha256") is not None:
                errors.append(f"{chapter_id}: narration digest exists without its draft")
            if stage not in {"planned"}:
                errors.append(f"{chapter_id}: stage {stage} lacks its narration draft")
        else:
            if target.get("narration_sha256") != digest(narration_path):
                errors.append(f"{chapter_id}: narration identity drift")
            narration_errors, _, _ = beat_auditor.audit_narration(narration)
            errors.extend(f"{chapter_id}:narration:{error}" for error in narration_errors)

        treatment_path = safe_repo_path(target.get("treatment_path", ""))
        treatment = None
        treatment_text = None
        if treatment_path and treatment_path.is_file():
            treatment_text = treatment_path.read_text(encoding="utf-8")
            treatment = json.loads(treatment_text)
            if target.get("treatment_sha256") != digest(treatment_path):
                errors.append(f"{chapter_id}: treatment identity drift")
            errors.extend(
                f"{chapter_id}:treatment-schema:{'.'.join(map(str, error.path))}: {error.message}"
                for error in Draft202012Validator(treatment_schema).iter_errors(treatment)
            )
            if (
                treatment.get("chapter_id") != chapter_id
                or treatment.get("chapter_sha256") != entry.get("chapter_sha256")
                or treatment.get("source_context_sha256") != entry.get("source_context_sha256")
            ):
                errors.append(f"{chapter_id}: treatment chapter or source-context identity drift")
            source_commit = treatment.get("source_commit")
            chapter_record = chapter_records.get(chapter_id, {})
            if isinstance(source_commit, str) and len(source_commit) == 40:
                committed_chapter = git_blob(source_commit, entry.get("chapter_path", ""))
                if committed_chapter is None:
                    errors.append(f"{chapter_id}: treatment source commit or chapter blob is unavailable")
                elif hashlib.sha256(committed_chapter).hexdigest() != entry.get("chapter_sha256"):
                    errors.append(f"{chapter_id}: treatment source commit does not reproduce the chapter")
                committed_context = committed_source_context_digest(source_commit, chapter_record)
                if committed_context is None:
                    errors.append(f"{chapter_id}: treatment source commit cannot reproduce its source context")
                elif committed_context != entry.get("source_context_sha256"):
                    errors.append(f"{chapter_id}: treatment source commit does not reproduce its source context")
            contract = treatment.get("content_contract", {})
            declared_claims = set(contract.get("chapter_claim_ids", [])) if isinstance(contract, dict) else set()
            declared_sources = set(contract.get("source_ids", [])) if isinstance(contract, dict) else set()
            allowed_claims = set(claims_by_chapter.get(chapter_id, set()))
            unknown_claims = sorted(declared_claims - allowed_claims)
            if unknown_claims:
                errors.append(
                    f"{chapter_id}: treatment invents or cross-owns claim IDs: {', '.join(unknown_claims)}"
                )
            unknown_sources = sorted(
                declared_sources - sources_by_chapter.get(chapter_id, set())
            )
            if unknown_sources:
                errors.append(
                    f"{chapter_id}: treatment cites sources not assigned to the chapter: {', '.join(unknown_sources)}"
                )
            absent_sources = sorted(declared_sources - inventory_source_ids)
            if absent_sources:
                errors.append(
                    f"{chapter_id}: treatment cites source IDs absent from inventory: {', '.join(absent_sources)}"
                )
        elif target.get("treatment_sha256") is not None:
            errors.append(f"{chapter_id}: treatment digest exists without its file")
        if gates.get("treatment") == "pass":
            if treatment is None:
                errors.append(f"{chapter_id}: treatment gate passes without its treatment")
            else:
                treatment_errors, _, _ = beat_auditor.audit_treatment(treatment, narration)
                errors.extend(f"{chapter_id}:treatment:{error}" for error in treatment_errors)
        if gates.get("script") == "pass":
            if treatment is None or narration is None:
                errors.append(f"{chapter_id}: script gate passes without treatment and narration")
            elif treatment.get("script_gate", {}).get("verdict") != "pass":
                errors.append(f"{chapter_id}: script gate passes without a recorded treatment script verdict")

        beat_path = safe_repo_path(target.get("beat_plan_path", ""))
        plan = None
        if beat_path and beat_path.is_file():
            plan = json.loads(beat_path.read_text(encoding="utf-8"))
            if target.get("beat_plan_sha256") != digest(beat_path):
                errors.append(f"{chapter_id}: beat-plan identity drift")
        elif target.get("beat_plan_sha256") is not None:
            errors.append(f"{chapter_id}: beat-plan digest exists without its file")
        if gates.get("beat_plan") == "pass":
            if plan is None:
                errors.append(f"{chapter_id}: beat-plan gate passes without its tracked plan")
            else:
                errors.extend(
                    f"{chapter_id}:beat-plan-schema:{'.'.join(map(str, error.path))}: {error.message}"
                    for error in Draft202012Validator(beat_schema).iter_errors(plan)
                )
                audit_errors, _, _ = beat_auditor.audit(
                    plan, narration, treatment, treatment_text=treatment_text
                )
                errors.extend(f"{chapter_id}:beat-plan:{error}" for error in audit_errors)
                timing = plan.get("timing", {})
                if timing.get("state") == "estimated":
                    errors.append(f"{chapter_id}: beat-plan gate passes on editorial timing estimates")
                if timing.get("state") in {"block_timed", "forced_aligned"}:
                    receipt_path = safe_repo_path(timing.get("receipt_path", ""))
                    if (
                        receipt_path is None
                        or not receipt_path.is_file()
                        or digest(receipt_path) != timing.get("receipt_sha256")
                    ):
                        errors.append(f"{chapter_id}: timing receipt is missing or has identity drift")
                    errors.extend(
                        f"{chapter_id}:narration-custody:{error}"
                        for error in narration_custody_errors(
                            entry, plan, treatment, narration_toolchain
                        )
                    )
                if timing.get("state") == "forced_aligned":
                    if not alignment_qualified:
                        errors.append(f"{chapter_id}: forced-aligned plan uses an unqualified alignment toolchain")
                    anchor_path = safe_repo_path(timing.get("manual_anchor_review_path", ""))
                    if (
                        anchor_path is None
                        or not anchor_path.is_file()
                        or digest(anchor_path) != timing.get("manual_anchor_review_sha256")
                    ):
                        errors.append(f"{chapter_id}: manual anchor review is missing or has identity drift")
        if gates.get("picture_and_sound_lock") == "pass":
            if not alignment_qualified:
                errors.append(f"{chapter_id}: picture-and-sound lock passes before forced alignment is qualified")
            if not plan or plan.get("timing", {}).get("state") != "forced_aligned":
                errors.append(f"{chapter_id}: picture-and-sound lock lacks a forced-aligned beat plan")
            assets = (
                treatment.get("art_direction", {}).get("asset_plan", [])
                if isinstance(treatment, dict) else []
            )
            unresolved_assets = [
                row for row in assets
                if not isinstance(row, dict)
                or row.get("status") == "planned"
                or row.get("security_review") == "planned"
                or not row.get("sha256")
            ]
            if unresolved_assets:
                errors.append(f"{chapter_id}: picture-and-sound lock retains planned or unbound assets")

        for path_field, digest_field, label in (
            ("scene_path", "scene_sha256", "scene"),
            ("caption_path", "caption_sha256", "captions"),
            ("transcript_path", "transcript_sha256", "transcript"),
            ("thumbnail_path", "thumbnail_sha256", "thumbnail"),
            ("render_receipt_path", "render_receipt_sha256", "render receipt"),
        ):
            errors.extend(
                f"{chapter_id}: {error}"
                for error in tracked_identity_errors(target, path_field, digest_field, label)
            )

        scene_path = safe_repo_path(target.get("scene_path", ""))
        if scene_path and scene_path.is_file():
            report = scene_auditor.audit_scene(
                scene_path,
                root=ROOT,
                treatment_path=(
                    treatment_path
                    if treatment_path and treatment_path.is_file()
                    else None
                ),
            )
            errors.extend(
                f"{chapter_id}:scene-source:{finding['code']}:{finding['line']}: {finding['message']}"
                for finding in report.get("findings", [])
            )

        receipt_path = safe_repo_path(target.get("render_receipt_path", ""))
        receipt = None
        if receipt_path and receipt_path.is_file():
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            errors.extend(
                f"{chapter_id}:{error}"
                for error in render_receipt_errors(
                    receipt, receipt_schema, value, entry, plan, treatment,
                    sandbox_schema, isolated_runner,
                    check_files=True,
                )
            )

        expected_bindings = {
            "chapter": expected_binding(entry.get("chapter_path"), entry.get("chapter_sha256")),
            "treatment": expected_binding(target.get("treatment_path"), target.get("treatment_sha256")),
            "beat_plan": expected_binding(target.get("beat_plan_path"), target.get("beat_plan_sha256")),
            "scene": expected_binding(target.get("scene_path"), target.get("scene_sha256")),
            "narration": expected_binding(target.get("narration_path"), target.get("narration_sha256")),
            "visual_grammar": expected_binding(value.get("visual_grammar_path"), value.get("visual_grammar_sha256")),
            "visual_toolchain": expected_binding(value.get("visual_toolchain_path"), value.get("visual_toolchain_sha256")),
            "primitive_library": expected_binding(value.get("primitive_library_path"), value.get("primitive_library_sha256")),
            "scene_source_auditor": expected_binding(value.get("scene_source_auditor_path"), value.get("scene_source_auditor_sha256")),
            "isolated_render_runner": expected_binding(value.get("isolated_render_runner_path"), value.get("isolated_render_runner_sha256")),
            "sandbox_policy_receipt_schema": expected_binding(value.get("sandbox_policy_receipt_schema_path"), value.get("sandbox_policy_receipt_schema_sha256")),
            "primitive_regression_manifest": expected_binding(value.get("primitive_regression_manifest_path"), value.get("primitive_regression_manifest_sha256")),
            "narration_toolchain": expected_binding(value.get("narration_toolchain_path"), value.get("narration_toolchain_sha256")),
        }
        for pass_name, review_path_value in target.get("experience_review_paths", {}).items():
            gate_state = gates.get(pass_name)
            if gate_state not in {"pass", "revise"}:
                continue
            review_path = safe_repo_path(review_path_value)
            if review_path is None or not review_path.is_file():
                errors.append(f"{chapter_id}: {pass_name} is {gate_state} without its review record")
                continue
            review = json.loads(review_path.read_text(encoding="utf-8"))
            errors.extend(
                f"{chapter_id}:{pass_name}-schema:{'.'.join(map(str, error.path))}: {error.message}"
                for error in Draft202012Validator(review_schema).iter_errors(review)
            )
            if review.get("chapter_id") != chapter_id or review.get("generation") != target.get("generation"):
                errors.append(f"{chapter_id}: {pass_name} review identity or generation drift")
            review_expected = dict(expected_bindings)
            sandbox_name = (
                "animatic-sandbox.json"
                if pass_name == "animatic"
                else "release-sandbox.json"
            )
            sandbox_relative = (
                f"visual_edition/chapters/{chapter_id}/generation-2/receipts/{sandbox_name}"
            )
            sandbox_binding = current_file_binding(sandbox_relative)
            review_expected["sandbox_policy_receipt"] = sandbox_binding
            sandbox_value = None
            if pass_name == "animatic":
                reviewed_master = expected_binding(None, None)
                sandbox_path = safe_repo_path(sandbox_relative)
                if sandbox_path is not None and sandbox_path.is_file():
                    try:
                        sandbox_value = json.loads(sandbox_path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError as exc:
                        errors.append(
                            f"{chapter_id}: animatic sandbox receipt is unreadable JSON: {exc}"
                        )
                    else:
                        reviewed_master = next(
                            (
                                {"path": row.get("path"), "sha256": row.get("sha256")}
                                for row in sandbox_value.get("outputs", [])
                                if isinstance(row, dict) and row.get("role") == "muxed_master"
                            ),
                            reviewed_master,
                        )
                review_expected.update({
                    "reviewed_master": reviewed_master,
                    "captions": None,
                    "transcript": None,
                    "thumbnail": None,
                    "render_receipt": None,
                    "av_diagnostics": None,
                })
                if isinstance(sandbox_value, dict):
                    errors.extend(
                        f"{chapter_id}:{error}"
                        for error in sandbox_policy_receipt_errors(
                            sandbox_value, sandbox_schema, value, entry,
                            treatment, None, isolated_runner, check_files=True,
                            expected_profile="draft",
                            reviewed_master=reviewed_master,
                        )
                    )
            else:
                review_expected["reviewed_master"] = expected_binding(target.get("master_path"), target.get("master_sha256"))
                review_expected.update({
                    "captions": expected_binding(target.get("caption_path"), target.get("caption_sha256")),
                    "transcript": expected_binding(target.get("transcript_path"), target.get("transcript_sha256")),
                    "thumbnail": (
                        expected_binding(target.get("thumbnail_path"), target.get("thumbnail_sha256"))
                        if pass_name in {"release_candidate", "independent_release_candidate"}
                        else None
                    ),
                    "render_receipt": expected_binding(
                        target.get("render_receipt_path"), target.get("render_receipt_sha256")
                    ),
                    "av_diagnostics": current_file_binding(
                        f"visual_edition/chapters/{chapter_id}/generation-2/av_diagnostics.json"
                    ),
                })
            errors.extend(
                f"{chapter_id}:{error}"
                for error in review_contract_errors(
                    review, pass_name, review_expected, plan if plan else {}, treatment,
                    check_files=True,
                )
            )
            if gate_state == "pass" and review.get("verdict") != "pass":
                errors.append(f"{chapter_id}: {pass_name} gate passes with a revise verdict")
            if gate_state == "revise" and review.get("verdict") != "revise":
                errors.append(f"{chapter_id}: {pass_name} revise gate lacks a revise verdict")

        if gates.get("accepted") == "pass":
            receipt_path = safe_repo_path(target.get("render_receipt_path", ""))
            master_path = safe_repo_path(target.get("master_path", ""))
            if not isinstance(target.get("master_sha256"), str):
                errors.append(f"{chapter_id}: accepted generation lacks an exact master digest")
            elif master_path is None or not master_path.is_file() or digest(master_path) != target["master_sha256"]:
                errors.append(f"{chapter_id}: accepted master identity drift")
            if receipt_path is None or not receipt_path.is_file() or receipt is None:
                errors.append(f"{chapter_id}: accepted generation lacks a tracked render receipt")
    return errors


def synthetic_review(pass_name: str) -> tuple[dict, dict, dict]:
    digests = {name: hashlib.sha256(name.encode("utf-8")).hexdigest() for name in
        (
            "reviewed_master", "chapter", "treatment", "beat_plan", "scene",
            "narration", "captions", "transcript", "thumbnail", "visual_grammar",
            "visual_toolchain", "primitive_library", "scene_source_auditor",
            "isolated_render_runner", "sandbox_policy_receipt_schema",
            "primitive_regression_manifest", "narration_toolchain",
            "sandbox_policy_receipt", "render_receipt", "av_diagnostics",
        )}
    bindings = {name: {"path": f"fixture/{name}.bin", "sha256": value} for name, value in digests.items()}
    if pass_name == "animatic":
        for name in ("captions", "transcript", "thumbnail", "render_receipt", "av_diagnostics"):
            bindings[name] = None
    elif pass_name == "picture_and_sound_lock":
        bindings["thumbnail"] = None
    viewing = {
        name: {"result": "pass", "notes": "The complete viewing mode passed review."}
        for name in ALL_VIEWING_PASSES
    }
    if pass_name == "animatic":
        viewing["captions_on"] = {
            "result": "not_applicable",
            "notes": "Captions do not exist at the animatic stage and were not reviewed.",
        }
    owned_dimensions = REVIEW_OWNED_DIMENSIONS[pass_name]
    dimensions = {
        name: {
            "score": 4 if name in owned_dimensions else None,
            "rationale": (
                "Timestamped evidence meets the dimension acceptance anchor."
                if name in owned_dimensions
                else "This review lane does not own this dimension; the later qualified lane does."
            ),
            "evidence_timestamps": [1.0] if name in owned_dimensions else [],
        }
        for name in REVIEW_DIMENSIONS
    }
    independent = pass_name == "independent_release_candidate"
    role = {
        "animatic": "implementation_diagnostic",
        "picture_and_sound_lock": "implementation_diagnostic",
        "release_candidate": "source_aware_critic",
        "independent_release_candidate": "cold_audience_proxy",
    }[pass_name]
    allowed_materials = {
        "animatic": [
            "rendered_video", "narration_script", "treatment", "beat_plan",
            "scene_code", "sandbox_policy_receipt", "sample_manifest",
        ],
        "picture_and_sound_lock": [
            "rendered_video", "captions", "descriptive_transcript",
            "narration_script", "treatment", "beat_plan", "scene_code",
            "render_receipt", "sandbox_policy_receipt", "av_diagnostics",
            "sample_manifest",
        ],
        "release_candidate": [
            "rendered_video", "captions", "descriptive_transcript", "chapter",
            "source_notes", "narration_script", "treatment", "beat_plan",
            "scene_code", "render_receipt", "sandbox_policy_receipt",
            "av_diagnostics", "sample_manifest",
        ],
        "independent_release_candidate": [
            "rendered_video", "captions", "descriptive_transcript",
        ],
    }[pass_name]
    review = {
        "schema_version": "asi_stack.manim_experience_review.v4",
        "chapter_id": "fixture",
        "generation": 2,
        "pass": pass_name,
        "review_role": role,
        "reviewed_at_utc": "2026-08-08T00:00:00Z",
        "artifact_bindings": bindings,
        "review_context": {
            "reviewer_id": "fixture-reviewer", "review_session_id": "fixture-session",
            "reviewer_type": "ai_proxy",
            "prior_exposure": "cold" if independent else "familiar",
            "script_author": False, "scene_implementer": False,
            "allowed_materials": allowed_materials,
            "context_manifest_path": "fixture/context_manifest.json",
            "context_manifest_sha256": "e" * 64,
            "raw_review_path": "fixture/raw_review.txt",
            "raw_review_sha256": "d" * 64,
            "independence_notes": "The reviewer did not author or implement the candidate artifacts."
        },
        "frame_sampling": {"samples_per_beat": 5, "expected_beat_count": 6, "sampled_beat_count": 6, "targeted_transition_samples": 2, "sample_manifest_path": "fixture/samples.json", "sample_manifest_sha256": "f" * 64, "unresolved_interpolation_defects": 0},
        "learning_check": {
            "status": "pass" if independent else "not_run", "reviewer_received_answer_key": False,
            "comprehension_prompt": "Explain the mechanism shown in the worked case." if independent else None,
            "comprehension_raw_response": "The gate separates plausible output from permission to act." if independent else None,
            "comprehension_success_criteria": ["Distinguish output quality from authority"] if independent else [],
            "comprehension_result": "pass" if independent else "not_run",
            "transfer_prompt": "Predict what changes when the request reaches a different tool." if independent else None,
            "transfer_raw_response": "The request needs a grant scoped to the different tool." if independent else None,
            "transfer_success_criteria": ["Require a changed authority grant"] if independent else [],
            "transfer_result": "pass" if independent else "not_run",
            "artifact_grounding": [{
                "timestamp_seconds": 12.0,
                "observed_cue": "The visible key changes scope at the second tool.",
                "response_excerpt": "grant scoped to the different tool",
                "causal_relevance": "The response uses the video's changed key scope to justify its prediction.",
            }] if independent else [],
            "artifact_grounding_result": "pass" if independent else "not_run",
            "assessor_id": "fixture-assessor" if independent else None,
            "misconception_or_failure_action": None,
            "proxy_limit": "An AI proxy diagnoses the artifact but is not evidence of human learning."
        },
        "viewing_passes": viewing,
        "phone_review": {
            "method": "browser_viewport" if pass_name == "animatic" else "physical_device",
            "complete_playback": True,
            "viewport_css_width_px": 360 if pass_name == "animatic" else 390,
            "zoom_used": False,
            "physical_device": pass_name != "animatic",
            "device_description": (
                "360px browser viewport preflight"
                if pass_name == "animatic"
                else "fixture physical phone"
            ),
            "captions_enabled": pass_name != "animatic",
            "audio_enabled": True,
        },
        "dimensions": dimensions,
        "open_defects": [], "verdict": "pass", "support_state_effect": "none",
        "non_claim": "This review diagnoses one derivative and does not prove learning or chapter truth."
    }
    treatment = {
        "story": {
            "comprehension_question": "Explain the mechanism shown in the worked case.",
            "comprehension_success_criteria": ["Distinguish output quality from authority"],
            "transfer_question": "Predict what changes when the request reaches a different tool.",
            "transfer_success_criteria": ["Require a changed authority grant"],
        }
    }
    return review, copy.deepcopy(bindings), treatment


def review_negative_control_failures() -> tuple[list[str], int]:
    controls = []
    base, bindings, treatment = synthetic_review("independent_release_candidate")
    controls.append(("failed viewing pass", lambda r: r["viewing_passes"]["phone"].update(result="fail"), "required viewing pass phone"))
    controls.append(("desktop substituted for phone", lambda r: r["phone_review"].update(method="browser_viewport", physical_device=False), "physical phone"))
    controls.append(("phone captions omitted", lambda r: r["phone_review"].update(captions_enabled=False), "did not include captions"))
    controls.append(("phone custody contradiction", lambda r: r["phone_review"].update(method="browser_viewport"), "flag disagree"))
    controls.append(("cold context leak", lambda r: r["review_context"]["allowed_materials"].append("answer_key"), "context leaks"))
    controls.append(("artifact digest drift", lambda r: r["artifact_bindings"]["narration"].update(sha256="0" * 64), "does not bind"))
    controls.append(("fake sample coverage", lambda r: r["frame_sampling"].update(sampled_beat_count=5), "does not cover every beat"))
    controls.append(("interpolation defect", lambda r: r["frame_sampling"].update(unresolved_interpolation_defects=1), "unresolved interpolation"))
    controls.append(("author reviews self", lambda r: r["review_context"].update(script_author=True), "participated in authorship"))
    controls.append(("answer key leaked", lambda r: r["learning_check"].update(reviewer_received_answer_key=True), "received the answer key"))
    controls.append(("cold claim score", lambda r: r["dimensions"]["claim_fidelity"].update(score=4, evidence_timestamps=[1.0]), "must not score"))
    controls.append(("post-hoc criteria", lambda r: r["learning_check"].update(comprehension_success_criteria=["Accept any response"]), "does not match the predeclared"))
    controls.append(("ungrounded cold pass", lambda r: r["learning_check"].update(artifact_grounding=[]), "lacks artifact-specific"))
    controls.append(("fabricated grounding excerpt", lambda r: r["learning_check"]["artifact_grounding"][0].update(response_excerpt="This sentence never appeared in either raw response."), "not present in the raw response"))
    failures: list[str] = []
    for label, mutate, expected in controls:
        review = copy.deepcopy(base)
        mutate(review)
        errors = review_contract_errors(
            review, "independent_release_candidate", bindings, 6, treatment,
            check_files=False,
        )
        if not any(expected in error for error in errors):
            failures.append(f"review negative control did not trigger: {label}")
    source_review, source_bindings, source_treatment = synthetic_review("release_candidate")
    source_review["review_context"]["scene_implementer"] = True
    source_errors = review_contract_errors(
        source_review, "release_candidate", source_bindings, 6, source_treatment,
        check_files=False,
    )
    if not any("independent of script and scene" in error for error in source_errors):
        failures.append("review negative control did not trigger: source-aware self-review")
    schema = json.loads(
        (ROOT / "schemas/manim_experience_review.schema.json").read_text(encoding="utf-8")
    )
    for pass_name in (
        "animatic", "picture_and_sound_lock", "release_candidate",
        "independent_release_candidate",
    ):
        review, pass_bindings, pass_treatment = synthetic_review(pass_name)
        schema_failures = list(Draft202012Validator(schema).iter_errors(review))
        semantic_failures = review_contract_errors(
            review, pass_name, pass_bindings, 6, pass_treatment,
            check_files=False,
        )
        if schema_failures or semantic_failures:
            details = [error.message for error in schema_failures] + semantic_failures
            failures.append(
                f"valid {pass_name} review fixture failed: {'; '.join(details)}"
            )
    animatic, animatic_bindings, animatic_treatment = synthetic_review("animatic")
    animatic["artifact_bindings"]["render_receipt"] = {
        "path": "fixture/render_receipt.bin", "sha256": "0" * 64,
    }
    animatic_errors = review_contract_errors(
        animatic, "animatic", animatic_bindings, 6, animatic_treatment,
        check_files=False,
    )
    if not any("must be null at this review stage" in error for error in animatic_errors):
        failures.append("review negative control did not trigger: future artifact in animatic")
    animatic, animatic_bindings, animatic_treatment = synthetic_review("animatic")
    animatic["dimensions"]["sound_mix"].update(score=4, evidence_timestamps=[1.0])
    animatic_errors = review_contract_errors(
        animatic, "animatic", animatic_bindings, 6, animatic_treatment,
        check_files=False,
    )
    if not any("must not score non-owned sound_mix" in error for error in animatic_errors):
        failures.append("review negative control did not trigger: animatic final-mix score")
    source_review, source_bindings, source_treatment = synthetic_review("release_candidate")
    source_review["learning_check"].update(
        status="pass", comprehension_result="pass", transfer_result="pass"
    )
    source_errors = review_contract_errors(
        source_review, "release_candidate", source_bindings, 6,
        source_treatment, check_files=False,
    )
    if not any("must not manufacture" in error for error in source_errors):
        failures.append("review negative control did not trigger: non-cold learning claim")
    animatic, animatic_bindings, animatic_treatment = synthetic_review("animatic")
    animatic["phone_review"]["viewport_css_width_px"] = 420
    animatic_errors = review_contract_errors(
        animatic, "animatic", animatic_bindings, 6,
        animatic_treatment, check_files=False,
    )
    if not any("exceeds 360 CSS pixels" in error for error in animatic_errors):
        failures.append("review negative control did not trigger: wide animatic phone viewport")
    return failures, len(controls) + 5


def narration_custody_negative_control_failures() -> tuple[list[str], int]:
    toolchain = json.loads(
        (ROOT / "visual_edition/narration_toolchain.json").read_text(encoding="utf-8")
    )
    synthesis = toolchain["synthesis"]
    tracked = toolchain["tracked_inputs"]
    narration_text = "A gate preserves authority."
    audio_relative = "build/visual_edition/audio/fixture-narration-master.wav"
    audio_sha = "a" * 64
    receipt_sha = "b" * 64
    asr_sha = "c" * 64
    target = {
        "narration_path": "visual_edition/chapters/fixture/generation-2/narration.txt",
        "narration_sha256": "d" * 64,
    }
    plan = {"target_duration_seconds": 120.0}
    treatment = {"audio_direction": {"performance_blocks": [{"id": "p01"}]}}
    receipt = {
        "schema_version": "asi_stack.local_narration_render.v1",
        "renderer_sha256": tracked["renderer_sha256"],
        "toolchain_id": toolchain["toolchain_id"],
        "implementation": synthesis["implementation"],
        "implementation_version": synthesis["version"],
        "model_repository": synthesis["model_repository"],
        "model_revision": synthesis["model_revision"],
        "input_path": target["narration_path"],
        "input_sha256": target["narration_sha256"],
        "lexicon_path": tracked["pronunciation_lexicon"],
        "lexicon_sha256": tracked["pronunciation_lexicon_sha256"],
        "model_file_sha256": {
            "build/visual_edition/models/Kokoro-82M-bf16/config.json": synthesis["config_sha256"],
            "build/visual_edition/models/Kokoro-82M-bf16/kokoro-v1_0.safetensors": synthesis["weights_sha256"],
            f"build/visual_edition/models/Kokoro-82M-bf16/voices/{synthesis['voice']}.safetensors": synthesis["voice_sha256"],
        },
        "voice": synthesis["voice"],
        "speed": synthesis["speed"],
        "sample_rate": synthesis["sample_rate"],
        "segmentation": {
            "maximum_characters": synthesis["maximum_segment_characters"],
            "maximum_observed_characters": len(narration_text),
            "sentence_pause_seconds": synthesis["sentence_pause_seconds"],
            "paragraph_pause_seconds": synthesis["paragraph_pause_seconds"],
        },
        "duration_seconds": 120.0,
        "normalization": {
            "filter": synthesis["normalizer_implementation"],
            "ffmpeg_path": synthesis["normalizer_path"],
            "ffmpeg_version": synthesis["normalizer_version"],
            "ffmpeg_sha256": synthesis["normalizer_sha256"],
            "integrated_lufs_target": synthesis["integrated_lufs_target"],
            "true_peak_dbtp_target": synthesis["true_peak_dbtp_target"],
            "loudness_range_target": synthesis["loudness_range_target"],
        },
        "output_path": audio_relative,
        "output_sha256": audio_sha,
        "segments": [{
            "written_text": narration_text,
            "spoken_text": narration_text,
            "paragraph_end": True,
        }],
    }
    report = {
        "schema_version": "asi_stack.local_narration_validation.v1",
        "validation_state": "pass",
        "validator_sha256": tracked["narration_validator_sha256"],
        "receipt_sha256": receipt_sha,
        "asr_sha256": asr_sha,
        "audio_path": audio_relative,
        "audio_sha256": audio_sha,
        "content_word_error_rate": 0.0,
        "checks": {"all_fixture_checks": True},
    }
    baseline = narration_custody_document_errors(
        receipt, report, plan, treatment, toolchain, target,
        audio_relative=audio_relative,
        audio_sha256=audio_sha,
        narration_receipt_sha256=receipt_sha,
        asr_sha256=asr_sha,
        narration_text=narration_text,
    )
    if baseline:
        return ["valid narration custody fixture failed: " + "; ".join(baseline)], 11
    controls = (
        ("renderer drift", "receipt", lambda row: row.update(renderer_sha256="0" * 64), "renderer_sha256"),
        ("toolchain drift", "receipt", lambda row: row.update(toolchain_id="stale"), "toolchain_id"),
        ("model revision drift", "receipt", lambda row: row.update(model_revision="0" * 40), "model_revision"),
        ("normalizer drift", "receipt", lambda row: row["normalization"].update(ffmpeg_sha256="0" * 64), "normalization ffmpeg_sha256 drift"),
        ("audio drift", "receipt", lambda row: row.update(output_sha256="0" * 64), "output_sha256"),
        ("duration drift", "receipt", lambda row: row.update(duration_seconds=121.0), "duration differs"),
        ("text drift", "receipt", lambda row: row["segments"][0].update(written_text="Different words."), "do not reproduce"),
        ("block mismatch", "treatment", lambda row: row["audio_direction"].update(performance_blocks=[]), "do not align"),
        ("failed report", "report", lambda row: row.update(validation_state="fail"), "validation_state identity drift"),
        ("failed check", "report", lambda row: row["checks"].update(all_fixture_checks=False), "retains a failing check"),
        ("WER ceiling", "report", lambda row: row.update(content_word_error_rate=1.0), "WER ceiling"),
    )
    failures: list[str] = []
    for label, owner, mutate, expected in controls:
        candidate_receipt = copy.deepcopy(receipt)
        candidate_report = copy.deepcopy(report)
        candidate_treatment = copy.deepcopy(treatment)
        mutate({
            "receipt": candidate_receipt,
            "report": candidate_report,
            "treatment": candidate_treatment,
        }[owner])
        errors = narration_custody_document_errors(
            candidate_receipt, candidate_report, plan, candidate_treatment,
            toolchain, target, audio_relative=audio_relative,
            audio_sha256=audio_sha,
            narration_receipt_sha256=receipt_sha, asr_sha256=asr_sha,
            narration_text=narration_text,
        )
        if not any(expected in error for error in errors):
            failures.append(f"narration custody negative control did not trigger: {label}")
    return failures, len(controls)


def render_receipt_negative_control_failures() -> tuple[list[str], int]:
    receipt_schema = json.loads(
        (ROOT / "schemas/manim_render_receipt.schema.json").read_text(encoding="utf-8")
    )
    sandbox_schema = json.loads(
        (ROOT / "schemas/manim_sandbox_policy_receipt.schema.json").read_text(encoding="utf-8")
    )
    toolchain = json.loads(
        (ROOT / "visual_edition/toolchain.json").read_text(encoding="utf-8")
    )
    binding_names = (
        "chapter", "treatment", "beat_plan", "scene", "narration",
        "visual_grammar", "visual_toolchain", "primitive_library",
        "scene_source_auditor", "isolated_render_runner", "final_receipt_compiler",
        "av_auditor", "av_diagnostics_schema",
        "sandbox_policy_receipt_schema", "primitive_regression_manifest",
        "narration_toolchain", "timing_receipt", "narration_render_receipt",
        "narration_verification_report", "audio_master",
    )
    bindings = {
        name: {"path": f"fixture/{name}.artifact", "sha256": "1" * 64}
        for name in binding_names
    }
    bindings["visual_toolchain"]["path"] = "visual_edition/toolchain.json"
    bindings["final_receipt_compiler"]["path"] = (
        "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py"
    )
    bindings["av_auditor"]["path"] = (
        "skills/asi-stack-manim-videos/scripts/audit_av_experience.py"
    )
    bindings["av_diagnostics_schema"]["path"] = (
        "schemas/manim_av_diagnostics.schema.json"
    )
    source_commit = "a" * 40
    scene_path = "visual_edition/chapters/fixture/generation-2/scene.py"
    treatment_path = "visual_edition/chapters/fixture/generation-2/treatment.json"
    master_path = "build/visual_edition/generation-2/final/fixture.mp4"
    bindings["scene"]["path"] = scene_path
    bindings["treatment"]["path"] = treatment_path
    scene_argv = [
        str((ROOT / toolchain["python"]["canonical_relative_path"]).resolve()),
        "-m", "manim", "render", "--renderer", "cairo", "--format", "mp4",
        "--resolution", "1920,1080", "--fps", "30", "--seed", "0",
        "--disable_caching", str((ROOT / scene_path).resolve()), "FixtureScene",
    ]
    mux_argv = [
        "/opt/homebrew/bin/ffmpeg", "-nostdin", "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000",
        "-movflags", "+faststart", str((ROOT / master_path).resolve()),
    ]
    value = {
        "schema_version": "asi_stack.manim_render_receipt.v1",
        "chapter_id": "fixture",
        "generation": 2,
        "rendered_at_utc": "2026-08-09T00:00:00Z",
        "source_commit": source_commit,
        "render": {
            "render_steps": [
                {"phase": "scene_render", "command_argv": scene_argv, "exit_code": 0},
                {"phase": "audio_mux", "command_argv": mux_argv, "exit_code": 0},
            ],
            "toolchain_id": toolchain["toolchain_id"],
            "random_seed": 0,
            "timezone": "UTC",
            "cache_policy": "clean",
        },
        "execution_security": {
            "isolation_mode": "macos_sandbox_exec",
            "network_access": False,
            "credential_environment_inherited": False,
            "repository_writable_roots": ["build/visual_edition"],
            "sandbox_policy_receipt": {
                "path": "visual_edition/chapters/fixture/generation-2/receipts/release-sandbox.json",
                "sha256": "f" * 64,
            },
            "source_preflight_scene_sha256": bindings["scene"]["sha256"],
            "source_preflight_verdict": "pass",
            "source_preflight_finding_count": 0,
        },
        "input_bindings": bindings,
        "output": {
            "path": master_path,
            "sha256": "b" * 64,
            "duration_seconds": 120.0,
            "pixel_width": 1920,
            "pixel_height": 1080,
            "frame_rate": 30,
            "video_codec": "h264",
            "pixel_format": "yuv420p",
            "audio_codec": "aac",
            "audio_channels": 2,
            "audio_sample_rate_hz": 48000,
        },
        "av_diagnostics": {
            "path": "visual_edition/chapters/fixture/generation-2/av_diagnostics.json",
            "sha256": "c" * 64,
        },
        "unresolved_material_warnings": 0,
        "asset_rights_state": "no_external_assets",
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": "This synthetic receipt tests custody only and proves no chapter truth or learning.",
    }
    ledger = {
        "visual_toolchain_path": "visual_edition/toolchain.json",
        "visual_grammar_path": bindings["visual_grammar"]["path"],
        "visual_grammar_sha256": bindings["visual_grammar"]["sha256"],
        "visual_toolchain_sha256": bindings["visual_toolchain"]["sha256"],
        "primitive_library_path": bindings["primitive_library"]["path"],
        "primitive_library_sha256": bindings["primitive_library"]["sha256"],
        "scene_source_auditor_path": bindings["scene_source_auditor"]["path"],
        "scene_source_auditor_sha256": bindings["scene_source_auditor"]["sha256"],
        "isolated_render_runner_path": bindings["isolated_render_runner"]["path"],
        "isolated_render_runner_sha256": bindings["isolated_render_runner"]["sha256"],
        "authoring_component_sha256": {
            "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py":
                bindings["final_receipt_compiler"]["sha256"],
            "skills/asi-stack-manim-videos/scripts/audit_av_experience.py":
                bindings["av_auditor"]["sha256"],
        },
        "sandbox_policy_receipt_schema_path": bindings["sandbox_policy_receipt_schema"]["path"],
        "sandbox_policy_receipt_schema_sha256": bindings["sandbox_policy_receipt_schema"]["sha256"],
        "av_diagnostics_schema_path": bindings["av_diagnostics_schema"]["path"],
        "av_diagnostics_schema_sha256": bindings["av_diagnostics_schema"]["sha256"],
        "primitive_regression_manifest_path": bindings["primitive_regression_manifest"]["path"],
        "primitive_regression_manifest_sha256": bindings["primitive_regression_manifest"]["sha256"],
        "narration_toolchain_path": bindings["narration_toolchain"]["path"],
        "narration_toolchain_sha256": bindings["narration_toolchain"]["sha256"],
    }
    entry = {
        "chapter_id": "fixture",
        "chapter_path": bindings["chapter"]["path"],
        "chapter_sha256": bindings["chapter"]["sha256"],
        "target": {
            "treatment_path": treatment_path,
            "treatment_sha256": bindings["treatment"]["sha256"],
            "beat_plan_path": bindings["beat_plan"]["path"],
            "beat_plan_sha256": bindings["beat_plan"]["sha256"],
            "scene_path": scene_path,
            "scene_sha256": bindings["scene"]["sha256"],
            "narration_path": bindings["narration"]["path"],
            "narration_sha256": bindings["narration"]["sha256"],
            "master_path": master_path,
            "master_sha256": value["output"]["sha256"],
            "gates": {"picture_and_sound_lock": "pass"},
        },
    }
    plan = {
        "target_duration_seconds": 120.0,
        "timing": {
            "receipt_path": bindings["timing_receipt"]["path"],
            "receipt_sha256": bindings["timing_receipt"]["sha256"],
            "narration_receipt_path": bindings["narration_render_receipt"]["path"],
            "narration_receipt_sha256": bindings["narration_render_receipt"]["sha256"],
            "narration_verification_report_path": bindings["narration_verification_report"]["path"],
            "narration_verification_report_sha256": bindings["narration_verification_report"]["sha256"],
        },
    }
    treatment = {"source_commit": source_commit, "art_direction": {"asset_plan": []}}
    scene_auditor = load_skill_script(
        "audit_scene_source.py", "asi_stack_manim_scene_source_render_fixture"
    )
    sys.modules["audit_scene_source"] = scene_auditor
    runner = load_skill_script(
        "render_scene_isolated.py", "asi_stack_manim_isolated_runner_render_fixture"
    )
    baseline = render_receipt_errors(
        value, receipt_schema, ledger, entry, plan, treatment, sandbox_schema,
        runner, check_files=False,
    )
    if baseline:
        return ["valid render receipt fixture failed: " + "; ".join(baseline)], 8
    controls = (
        ("source commit drift", lambda row: row.__setitem__("source_commit", "0" * 40), "source commit differs"),
        ("runner binding drift", lambda row: row["input_bindings"]["isolated_render_runner"].update(sha256="0" * 64), "isolated_render_runner does not bind"),
        ("compiler binding drift", lambda row: row["input_bindings"]["final_receipt_compiler"].update(sha256="0" * 64), "final_receipt_compiler does not bind"),
        ("A/V auditor binding drift", lambda row: row["input_bindings"]["av_auditor"].update(sha256="0" * 64), "av_auditor does not bind"),
        ("A/V schema binding drift", lambda row: row["input_bindings"]["av_diagnostics_schema"].update(sha256="0" * 64), "av_diagnostics_schema does not bind"),
        ("network declaration", lambda row: row["execution_security"].__setitem__("network_access", True), "does not prove network-denied"),
        ("master identity drift", lambda row: row["output"].update(sha256="0" * 64), "does not bind the ledger master"),
        ("duration drift", lambda row: row["output"].update(duration_seconds=121.0), "duration differs"),
    )
    failures: list[str] = []
    for label, mutate, expected in controls:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        errors = render_receipt_errors(
            candidate, receipt_schema, ledger, entry, plan, treatment,
            sandbox_schema, runner, check_files=False,
        )
        if not any(expected in error for error in errors):
            failures.append(f"render receipt negative control did not trigger: {label}")
    unresolved_treatment = copy.deepcopy(treatment)
    unresolved_treatment["art_direction"]["asset_plan"] = [{
        "status": "planned", "security_review": "planned", "sha256": None,
    }]
    asset_errors = render_receipt_errors(
        value, receipt_schema, ledger, entry, plan, unresolved_treatment,
        sandbox_schema, runner, check_files=False,
    )
    if not any("planned or unreviewed assets" in error for error in asset_errors):
        failures.append("render receipt negative control did not trigger: unresolved asset custody")
    return failures, len(controls) + 1


def sandbox_receipt_negative_control_failures() -> tuple[list[str], int]:
    schema = json.loads(
        (ROOT / "schemas/manim_sandbox_policy_receipt.schema.json").read_text(encoding="utf-8")
    )
    scene_path = "visual_edition/chapters/fixture/generation-2/scene.py"
    treatment_path = "visual_edition/chapters/fixture/generation-2/treatment.json"
    master_path = "build/visual_edition/generation-2/final/fixture.mp4"
    visual_path = "build/visual_edition/isolated-renders/fixture/release/media/fixture-visual.mp4"
    audio_path = "build/visual_edition/audio/fixture-narration-master.wav"
    scene_sha = "a" * 64
    treatment_sha = "b" * 64
    master_sha = "c" * 64
    runner_sha = "d" * 64
    auditor_sha = "e" * 64
    scene_argv = [
        str(ROOT / "build/visual_edition/venv/bin/python"),
        "-m", "manim", "render",
        "--config_file", str((ROOT / "visual_edition/manim.cfg").resolve()),
        "--renderer", "cairo", "--format", "mp4", "--resolution", "1920,1080",
        "--fps", "30", "--seed", "0", "--disable_caching", "--progress_bar", "none",
        "--media_dir", str((ROOT / "build/visual_edition/isolated-renders/fixture/release/media").resolve()),
        "--output_file", "fixture-visual.mp4",
        str((ROOT / scene_path).resolve()), "FixtureScene",
    ]
    release_pending_path = (
        ROOT / "build/visual_edition/generation-2/final/.fixture.release.pending.mp4"
    ).resolve()
    mux_argv = [
        "/opt/homebrew/bin/ffmpeg", "-hide_banner", "-nostdin", "-y",
        "-i", str((ROOT / visual_path).resolve()), "-i", str((ROOT / audio_path).resolve()),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000",
        "-b:a", "192k", "-movflags", "+faststart", str(release_pending_path),
    ]
    value = {
        "schema_version": "asi_stack.manim_sandbox_policy_receipt.v1",
        "created_at_utc": "2026-08-09T00:00:00Z",
        "chapter_id": "fixture",
        "profile": "release",
        "isolation_mode": "macos_sandbox_exec",
        "runner": {
            "path": "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py",
            "sha256": runner_sha,
        },
        "policy": {
            "path": "visual_edition/chapters/fixture/generation-2/receipts/release.sb",
            "sha256": "f" * 64,
        },
        "scene": {"path": scene_path, "sha256": scene_sha},
        "treatment": {"path": treatment_path, "sha256": treatment_sha},
        "audio_master": {"path": audio_path, "sha256": "1" * 64},
        "toolchain_id": "fixture-manim-toolchain",
        "media_tools": json.loads(
            (ROOT / "visual_edition/toolchain.json").read_text(encoding="utf-8")
        )["media_tools"],
        "network_access": False,
        "credential_environment_inherited": False,
        "repository_writable_roots": ["build/visual_edition"],
        "filesystem_read_scope": {
            "global_metadata_lookup": True,
            "unlisted_repository_content_access": False,
            "repository_content_mode": "explicit_inputs_plus_build",
            "system_content_roots": [
                "/System", "/Library/ColorSync", "/Library/Fonts",
                "/Library/Frameworks", "/usr", "/bin", "/sbin", "/opt/homebrew",
            ],
            "rationale": (
                "The macOS Python launcher and native dependencies require the "
                "listed system content roots plus global metadata; unlisted "
                "repository file contents remain denied."
            ),
        },
        "resource_limits": {
            "wall_seconds": 1800,
            "cpu_seconds": 1800,
            "max_file_size_bytes": 4294967296,
            "max_open_files": 256,
            "max_processes": 256,
            "max_resident_memory_bytes": None,
            "memory_limit_status": "not_enforced_macos",
            "core_dump_bytes": 0,
        },
        "policy_self_test": {
            "allowed_write": "pass",
            "denied_write": "pass",
            "denied_read": "pass",
            "symlink_escape_denied": "pass",
            "symlink_read_escape_denied": "pass",
            "hardlink_escape_denied": "pass",
            "unlisted_exec_denied": "pass",
            "network_denied": "pass",
            "credentials_stripped": "pass",
        },
        "resource_limit_self_test": {
            "memory_bound": "not_enforced_macos",
            "core_dump_bytes": "pass",
            "cpu_seconds": "pass",
            "max_file_size_bytes": "pass",
            "max_open_files": "pass",
            "max_processes": "pass",
        },
        "source_preflight": {
            "verdict": "pass",
            "finding_count": 0,
            "scene_sha256": scene_sha,
            "auditor": {
                "path": "skills/asi-stack-manim-videos/scripts/audit_scene_source.py",
                "sha256": auditor_sha,
            },
        },
        "render_steps": [
            {"phase": "scene_render", "command_argv": scene_argv, "exit_code": 0, "wall_seconds": 1.0},
            {"phase": "audio_mux", "command_argv": mux_argv, "exit_code": 0, "wall_seconds": 1.0},
        ],
        "outputs": [
            {
                "role": "visual_track",
                "path": visual_path,
                "sha256": "2" * 64,
                "size_bytes": 100,
            },
            {"role": "muxed_master", "path": master_path, "sha256": master_sha, "size_bytes": 100},
        ],
        "support_state_effect": "none",
        "publication_effect": "none",
        "non_claim": "This constrained fixture does not establish scene safety, teaching, chapter truth, or publication authority.",
    }
    ledger = {
        "isolated_render_runner_path": value["runner"]["path"],
        "isolated_render_runner_sha256": runner_sha,
        "scene_source_auditor_path": value["source_preflight"]["auditor"]["path"],
        "scene_source_auditor_sha256": auditor_sha,
        "visual_toolchain_path": "visual_edition/toolchain.json",
    }
    entry = {
        "chapter_id": "fixture",
        "target": {
            "scene_path": scene_path,
            "scene_sha256": scene_sha,
            "treatment_path": treatment_path,
            "treatment_sha256": treatment_sha,
            "master_path": master_path,
            "master_sha256": master_sha,
        },
    }
    final_receipt = {
        "execution_security": {"isolation_mode": "macos_sandbox_exec"},
        "input_bindings": {"audio_master": value["audio_master"]},
        "render": {
            "toolchain_id": value["toolchain_id"],
            "random_seed": 0,
            "render_steps": [
                {key: row[key] for key in ("phase", "command_argv", "exit_code")}
                for row in value["render_steps"]
            ],
        },
    }
    scene_auditor = load_skill_script(
        "audit_scene_source.py", "asi_stack_manim_scene_source_sandbox_fixture"
    )
    sys.modules["audit_scene_source"] = scene_auditor
    runner = load_skill_script(
        "render_scene_isolated.py", "asi_stack_manim_isolated_runner_fixture"
    )
    baseline = sandbox_policy_receipt_errors(
        value, schema, ledger, entry, {}, final_receipt, runner, check_files=False
    )
    if baseline:
        return ["valid sandbox receipt fixture failed: " + "; ".join(baseline)], 22
    controls = (
        ("network declaration", lambda row: row.__setitem__("network_access", True), "network_access"),
        ("credential inheritance", lambda row: row.__setitem__("credential_environment_inherited", True), "credential_environment_inherited"),
        ("content read-scope widening", lambda row: row["filesystem_read_scope"]["system_content_roots"].append("/Library"), "filesystem read scope"),
        ("symlink escape probe", lambda row: row["policy_self_test"].__setitem__("symlink_escape_denied", "fail"), "symlink_escape_denied"),
        ("symlink read escape probe", lambda row: row["policy_self_test"].__setitem__("symlink_read_escape_denied", "fail"), "symlink_read_escape_denied"),
        ("hardlink escape probe", lambda row: row["policy_self_test"].__setitem__("hardlink_escape_denied", "fail"), "hardlink_escape_denied"),
        ("unlisted executable probe", lambda row: row["policy_self_test"].__setitem__("unlisted_exec_denied", "fail"), "unlisted_exec_denied"),
        ("memory-limit laundering", lambda row: row["resource_limits"].__setitem__("memory_limit_status", "enforced"), "resource limits differ"),
        ("process limit weakening", lambda row: row["resource_limits"].__setitem__("max_processes", 257), "resource limits differ"),
        ("resource self-test laundering", lambda row: row["resource_limit_self_test"].__setitem__("max_open_files", "fail"), "resource-limit self-test"),
        ("write-root widening", lambda row: row["repository_writable_roots"].append("."), "repository_writable_roots"),
        ("runner drift", lambda row: row["runner"].update(sha256="0" * 64), "runner does not bind"),
        ("source preflight laundering", lambda row: row["source_preflight"].update(finding_count=1), "finding_count"),
        ("release command weakening", lambda row: row["render_steps"][0]["command_argv"].remove("--disable_caching"), "does not exactly reproduce"),
        ("mux command widening", lambda row: row["render_steps"][1]["command_argv"].insert(-1, "-shortest"), "does not exactly reproduce"),
        ("media-tool identity drift", lambda row: row["media_tools"]["ffmpeg"].update(sha256="0" * 64), "media-tool identities"),
        ("seed receipt drift", lambda row: row["render_steps"][0]["command_argv"].__setitem__(row["render_steps"][0]["command_argv"].index("0"), "1"), "seed differs"),
        ("master identity drift", lambda row: row["outputs"][1].update(sha256="0" * 64), "does not bind the ledger master"),
    )
    failures: list[str] = []
    for label, mutate, expected in controls:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        errors = sandbox_policy_receipt_errors(
            candidate, schema, ledger, entry, {}, final_receipt, runner,
            check_files=False,
        )
        if not any(expected in error for error in errors):
            failures.append(f"sandbox receipt negative control did not trigger: {label}")
    draft = copy.deepcopy(value)
    draft_visual_path = (
        "build/visual_edition/isolated-renders/fixture/draft/media/fixture-visual.mp4"
    )
    draft_scene_argv = runner.manim_command(
        ROOT / scene_path, "FixtureScene", "fixture", "draft", 0,
        (ROOT / "build/visual_edition/isolated-renders/fixture/draft/media").resolve(),
    )
    draft_master_path = (
        "build/visual_edition/isolated-renders/fixture/draft/fixture-animatic.mp4"
    )
    draft_pending_path = (
        ROOT
        / "build/visual_edition/isolated-renders/fixture/draft/.fixture-animatic.draft.pending.mp4"
    ).resolve()
    draft_mux_argv = [
        value["media_tools"]["ffmpeg"]["path"],
        "-hide_banner", "-nostdin", "-y",
        "-i", str((ROOT / draft_visual_path).resolve()),
        "-i", str((ROOT / audio_path).resolve()),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-r", "15", "-c:a", "aac", "-ar", "48000",
        "-b:a", "192k", "-movflags", "+faststart", str(draft_pending_path),
    ]
    draft.update({
        "profile": "draft",
        "policy": {
            "path": "visual_edition/chapters/fixture/generation-2/receipts/animatic-sandbox.sb",
            "sha256": "f" * 64,
        },
        "audio_master": {"path": audio_path, "sha256": "1" * 64},
        "toolchain_id": json.loads(
            (ROOT / "visual_edition/toolchain.json").read_text(encoding="utf-8")
        )["toolchain_id"],
        "render_steps": [
            {
                "phase": "scene_render", "command_argv": draft_scene_argv,
                "exit_code": 0, "wall_seconds": 1.0,
            },
            {
                "phase": "audio_mux", "command_argv": draft_mux_argv,
                "exit_code": 0, "wall_seconds": 1.0,
            },
        ],
        "outputs": [
            {
                "role": "visual_track", "path": draft_visual_path,
                "sha256": "2" * 64, "size_bytes": 100,
            },
            {
                "role": "muxed_master", "path": draft_master_path,
                "sha256": "3" * 64, "size_bytes": 100,
            },
        ],
    })
    draft_ledger = {
        **ledger,
        "visual_toolchain_path": "visual_edition/toolchain.json",
    }
    reviewed_master = {"path": draft_master_path, "sha256": "3" * 64}
    draft_baseline = sandbox_policy_receipt_errors(
        draft, schema, draft_ledger, entry, {}, None, runner,
        check_files=False, expected_profile="draft",
        reviewed_master=reviewed_master,
    )
    if draft_baseline:
        failures.append(
            "valid draft sandbox receipt fixture failed: "
            + "; ".join(draft_baseline)
        )
    draft_controls = (
        (
            "draft audio omission",
            lambda row: row.__setitem__("audio_master", None),
            "canonical narration audio master",
        ),
        (
            "draft profile laundering",
            lambda row: row.__setitem__("profile", "release"),
            "draft review requires a draft-profile",
        ),
        (
            "draft command weakening",
            lambda row: row["render_steps"][0]["command_argv"].remove("--disable_caching"),
            "does not exactly reproduce",
        ),
        (
            "draft reviewed-media drift",
            lambda row: row["outputs"][1].update(sha256="0" * 64),
            "does not bind the reviewed audio animatic",
        ),
    )
    for label, mutate, expected in draft_controls:
        candidate = copy.deepcopy(draft)
        mutate(candidate)
        errors = sandbox_policy_receipt_errors(
            candidate, schema, draft_ledger, entry, {}, None, runner,
            check_files=False, expected_profile="draft",
            reviewed_master=reviewed_master,
        )
        if not any(expected in error for error in errors):
            failures.append(f"sandbox receipt negative control did not trigger: {label}")
    return failures, len(controls) + len(draft_controls)


def negative_control_failures(value: dict) -> tuple[list[str], int]:
    controls: list[tuple[str, dict, str]] = []
    missing_entry = copy.deepcopy(value)
    missing_entry["entries"].pop()
    controls.append(("chapter deletion", missing_entry, "ledger does not match"))
    predecessor_drift = copy.deepcopy(value)
    predecessor_drift["entries"][0]["predecessor"]["master_sha256"] = "0" * 64
    controls.append(("predecessor identity drift", predecessor_drift, "predecessor master identity drift"))
    narration_drift = copy.deepcopy(value)
    drafted = next(entry for entry in narration_drift["entries"] if entry["target"].get("narration_sha256"))
    drafted["target"]["narration_sha256"] = "0" * 64
    controls.append(("narration identity drift", narration_drift, "narration identity drift"))
    scene_drift = copy.deepcopy(value)
    implemented = next(entry for entry in scene_drift["entries"] if entry["target"].get("scene_sha256"))
    implemented["target"]["scene_sha256"] = "0" * 64
    controls.append(("scene identity drift", scene_drift, "scene identity drift"))
    fake_treatment = copy.deepcopy(value)
    untreated = next(
        entry for entry in fake_treatment["entries"]
        if not entry["target"].get("treatment_sha256")
    )
    untreated["target"]["gates"]["treatment"] = "pass"
    controls.append(("missing treatment promotion", fake_treatment, "treatment gate passes without"))
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
            failures.append(f"ledger negative control did not trigger: {label}")
    rejecting_count = len(controls)
    for check in (
        review_negative_control_failures,
        narration_custody_negative_control_failures,
        render_receipt_negative_control_failures,
        sandbox_receipt_negative_control_failures,
    ):
        check_failures, check_count = check()
        failures.extend(check_failures)
        rejecting_count += check_count
    av_auditor = load_skill_script(
        "audit_av_experience.py", "audit_av_experience"
    )
    sys.modules["audit_av_experience"] = av_auditor
    failures.extend(
        f"A/V diagnostics negative control failed: {failure}"
        for failure in av_auditor.negative_control_failures()
    )
    rejecting_count += av_auditor.NEGATIVE_CONTROL_COUNT
    receipt_compiler = load_skill_script(
        "build_final_render_receipt.py", "asi_stack_manim_final_receipt_compiler_controls"
    )
    failures.extend(
        f"final-receipt compiler negative control failed: {failure}"
        for failure in receipt_compiler.self_test()
    )
    rejecting_count += receipt_compiler.NEGATIVE_CONTROL_COUNT
    scene_auditor = load_skill_script(
        "audit_scene_source.py", "asi_stack_manim_scene_source_negative_controls"
    )
    failures.extend(
        f"scene-source negative control failed: {failure}"
        for failure in scene_auditor.self_test()
    )
    rejecting_count += scene_auditor.NEGATIVE_CONTROL_COUNT
    primitive_auditor = load_skill_script(
        "audit_primitive_regression.py", "asi_stack_manim_primitive_negative_controls"
    )
    failures.extend(
        f"primitive-regression negative control failed: {failure}"
        for failure in primitive_auditor.self_test()
    )
    rejecting_count += primitive_auditor.NEGATIVE_CONTROL_COUNT
    sample_auditor = load_skill_script(
        "sample_video_beats.py", "asi_stack_manim_frame_sample_controls"
    )
    failures.extend(
        f"frame-sample negative control failed: {failure}"
        for failure in sample_auditor.schema_negative_control_failures()
    )
    rejecting_count += sample_auditor.NEGATIVE_CONTROL_COUNT
    return failures, rejecting_count


def main() -> None:
    value = json.loads(LEDGER.read_text(encoding="utf-8"))
    errors = semantic_errors(value)
    negative_errors, rejecting_count = negative_control_failures(value)
    errors.extend(negative_errors)
    if rejecting_count != EXPECTED_REJECTING_CONTROL_COUNT:
        errors.append(
            "rejecting-control inventory drift: "
            f"expected {EXPECTED_REJECTING_CONTROL_COUNT}, counted {rejecting_count}"
        )
    if errors:
        raise SystemExit("Manim generation-two production ledger validation failed:\n - " + "\n - ".join(errors))
    print(
        f"Manim generation-two ledger validates: {len(value['entries'])} identities, "
        "fail-closed treatment/timing/render/review gates, "
        f"{rejecting_count} rejecting controls, and no inferred learning claim."
    )


if __name__ == "__main__":
    main()
