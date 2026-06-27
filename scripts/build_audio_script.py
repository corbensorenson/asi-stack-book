#!/usr/bin/env python3
"""Generate a narration-script candidate from the reader edition source.

This script does not synthesize audio. It creates a review workspace for a
future audiobook release and flags tables, diagrams, images, and code blocks
that need human narration treatment before MP3, M4B, or audio-embedded EPUB
artifacts can be claimed.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "audio_script"
DEFAULT_READER_TEMP_NAME = "reader_source"
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\).*")
IMPLEMENTATION_HORIZON_HEADINGS = (
    "## Minimum Viable Implementation",
    "## Beyond the State of the Art",
)


def narration_note(text: str) -> str:
    return f"> Narration note: {text}"


def scan_audio_treatments(text: str) -> dict[str, int]:
    counts = {
        "tables": 0,
        "mermaid_diagrams": 0,
        "code_or_schema_blocks": 0,
        "images": 0,
    }
    in_code = False
    in_table = False

    for line in build_reader_edition.strip_frontmatter(text).splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                if "mermaid" in stripped.lower():
                    counts["mermaid_diagrams"] += 1
                else:
                    counts["code_or_schema_blocks"] += 1
            else:
                in_code = False
            in_table = False
            continue

        if in_code:
            continue

        if IMAGE_RE.match(stripped):
            counts["images"] += 1
            in_table = False
            continue

        if stripped.startswith("|"):
            if not in_table:
                counts["tables"] += 1
                in_table = True
            continue
        in_table = False

    return counts


def qmd_to_audio_markdown(text: str) -> str:
    lines = build_reader_edition.strip_frontmatter(text).splitlines()
    output: list[str] = []
    in_code = False
    skipping_table = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                if "mermaid" in stripped.lower():
                    output.append(narration_note("Diagram retained in companion text; write a concise spoken walkthrough before audio release."))
                else:
                    output.append(narration_note("Code or schema block retained in companion text; summarize only if it is essential to the argument."))
            else:
                in_code = False
            continue

        if in_code:
            continue

        if stripped.startswith("|"):
            if not skipping_table:
                output.append(narration_note("Table retained in companion text; replace with the key spoken takeaway before audio release."))
                skipping_table = True
            continue
        skipping_table = False

        if IMAGE_RE.match(stripped):
            output.append(narration_note("Image retained in companion text; add a short verbal description if it carries meaning."))
            continue

        output.append(line)

    header = [
        "---",
        "audio_script_status: review_required",
        "---",
        "",
        "> Release note: This is a generated narration-script candidate. It is not an audiobook transcript until reviewed.",
        "",
    ]
    return "\n".join(header + output).strip() + "\n"


def write_pronunciation_glossary(output_dir: Path) -> None:
    text = """# Pronunciation Glossary

Status: starter glossary for future audio review.

| Term | Spoken form | Review note |
|---|---|---|
| ASI | A-S-I | Spell the letters. |
| VCM | V-C-M | Spell the letters unless the final manuscript defines a spoken name. |
| MoECOT | moe-ee-cot | Confirm preferred pronunciation before recording. |
| PlanForge | plan forge | Treat as two clear words. |
| Codex | co-dex | Use the normal product pronunciation. |
| Quarto | quar-to | Confirm with narrator if needed. |
| SCF | S-C-F | Spell the letters. |
| RSI | R-S-I | Spell the letters. |
"""
    (output_dir / "pronunciation_glossary.md").write_text(text, encoding="utf-8")


def write_chapter_markers(output_dir: Path, script_files: list[str]) -> str:
    marker_path = "chapter_markers.md"
    lines = [
        "# Chapter Markers",
        "",
        "Status: generated starter markers for future audio packaging.",
        "",
        "Replace placeholder times with final timecodes only after the reviewed script is recorded and checked.",
        "",
        "| Marker | Script file | Start time | Review note |",
        "|---|---|---|---|",
    ]
    for index, script_file in enumerate(script_files, start=1):
        lines.append(f"| {index} | `{script_file}` | TBD | Verify after audio render. |")
    lines.append("")
    (output_dir / marker_path).write_text("\n".join(lines), encoding="utf-8")
    return marker_path


def load_structure() -> dict:
    value = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def implementation_horizon_script_records(output_dir: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for chapter in flatten_chapters(load_structure()):
        relative = str(chapter.get("file", ""))
        script_path = output_dir / Path(relative).with_suffix(".md")
        text = script_path.read_text(encoding="utf-8", errors="ignore") if script_path.exists() else ""
        missing = [
            heading
            for heading in IMPLEMENTATION_HORIZON_HEADINGS
            if heading not in text
        ]
        records.append(
            {
                "chapter_id": chapter.get("id", ""),
                "script_file": str(script_path.relative_to(output_dir)) if script_path.exists() else str(script_path),
                "missing_headings": missing,
            }
        )
    return records


def write_audio_checklist(
    output_dir: Path,
    audio_profile: dict,
    audio_policy: dict,
    companion_policy: dict,
    bundle_policy: dict,
    script_files: list[str],
) -> str:
    checklist_path = str(audio_policy.get("generated_checklist_path", "AUDIO_RELEASE_CHECKLIST.md"))
    companion_path = str(companion_policy.get("audio_companion_path", "companion_notes.md"))
    review_requirements = audio_policy.get("review_requirements", [])
    packaging_checks = audio_policy.get("audio_packaging_checks", [])
    spoken_rules = audio_policy.get("spoken_treatment_rules", [])
    release_gate = audio_profile.get("release_gate", [])
    artifact_formats = audio_policy.get("audio_artifact_formats", [])

    lines = [
        "# Audio Release Checklist",
        "",
        "Status: generated checklist for narration-script review.",
        "",
        "This workspace is a script-preparation artifact derived from the reader edition. It is not an audiobook, and it does not produce audio files.",
        "",
        "## Generated Script",
        "",
        f"- Profile: `{audio_profile.get('id', 'audio_release')}`",
        f"- Script files: {len(script_files)}",
        f"- Target audio artifacts: {', '.join(artifact_formats)}",
        f"- Companion notes: `{companion_path}`",
        "",
        "## Required Gate",
        "",
    ]
    for item in release_gate:
        lines.append(f"- [ ] {item}")

    lines.extend(["", "## Review Requirements", ""])
    for item in review_requirements:
        lines.append(f"- [ ] {item}")

    lines.extend(["", "## Spoken Treatment Rules", ""])
    for item in spoken_rules:
        lines.append(f"- [ ] {item}")

    if bundle_policy:
        lines.extend([
            "",
            "## Major-Version Audio Bundle",
            "",
            "- [ ] Confirm the reader manuscript for this major version was reviewed before this script is used.",
            "- [ ] Keep MP3/M4B packaging separate from EPUB/DOCX/PDF reader artifacts in the release record.",
            "- [ ] Treat audio embedded in EPUB as its own checked artifact, not as a side effect of EPUB generation.",
            "",
            "### Audio Quality Gates",
            "",
        ])
        for item in bundle_policy.get("audio_quality_gates", []):
            lines.append(f"- [ ] {item}")

    if packaging_checks:
        lines.extend(["", "## Audio Packaging Checks", ""])
        for item in packaging_checks:
            lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Packaging Checks",
        "",
        "- [ ] Replace generated narration notes for tables, diagrams, images, code, and schemas with reviewed spoken text or companion-note references.",
        f"- [ ] Review `{companion_path}` before claiming MP3, M4B, or audio-embedded EPUB artifacts.",
        "- [ ] Treat each audio format as `target_not_generated` until the exact audio artifact is produced and checked.",
        "- [ ] Fill chapter markers with final timecodes after audio generation.",
        "- [ ] Spot-check audio against the reviewed script before listing MP3, M4B, or audio-embedded EPUB as produced.",
        "- [ ] Verify an audio-embedded EPUB actually contains the reviewed audio files before naming it in a release record.",
        "",
        "## Non-Claims",
        "",
        "- This checklist does not claim any MP3, M4B, or audio-embedded EPUB exists.",
        "- This checklist does not claim narration quality, pronunciation quality, or accessibility quality.",
        "- The reviewed reader edition remains the source for audio adaptation.",
        "",
    ])
    (output_dir / checklist_path).write_text("\n".join(lines), encoding="utf-8")
    return checklist_path


def write_audio_companion_notes(
    output_dir: Path,
    companion_policy: dict,
    treatment_summary: dict[str, dict[str, int]],
) -> str:
    companion_path = str(companion_policy.get("audio_companion_path", "companion_notes.md"))
    totals = {
        "tables": 0,
        "mermaid_diagrams": 0,
        "code_or_schema_blocks": 0,
        "images": 0,
    }
    for counts in treatment_summary.values():
        for key in totals:
            totals[key] += int(counts.get(key, 0))

    lines = [
        "# Audio Companion Notes",
        "",
        "Status: generated starter notes for narration and audio-packaging review.",
        "",
        "These notes identify material that should be spoken, summarized, moved to companion material, or checked inside an audio-embedded EPUB. They are not an audiobook, not a transcript review, and not evidence that audio files exist.",
        "",
        "## Purpose",
        "",
        str(companion_policy.get("purpose", "Keep audio companion decisions explicit for human-listener releases.")),
        "",
        "## Treatment Summary",
        "",
        "| Script file | Tables | Mermaid diagrams | Code/schema blocks | Images |",
        "|---|---:|---:|---:|---:|",
    ]
    for script_file, counts in sorted(treatment_summary.items()):
        lines.append(
            "| "
            f"`{script_file}` | "
            f"{counts.get('tables', 0)} | "
            f"{counts.get('mermaid_diagrams', 0)} | "
            f"{counts.get('code_or_schema_blocks', 0)} | "
            f"{counts.get('images', 0)} |"
        )

    lines.extend([
        "| **Total** | "
        f"{totals['tables']} | "
        f"{totals['mermaid_diagrams']} | "
        f"{totals['code_or_schema_blocks']} | "
        f"{totals['images']} |",
        "",
        "## Companion Topics To Review",
        "",
    ])
    for item in companion_policy.get("required_topics", []):
        lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Review Requirements",
        "",
    ])
    for item in companion_policy.get("review_requirements", []):
        lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Audio Packaging Notes",
        "",
        "- [ ] Replace generated narration notes in chapter scripts with reviewed spoken summaries or explicit companion-note references.",
        "- [ ] Confirm chapter markers, metadata, and sample listening checks before listing MP3 or M4B artifacts.",
        "- [ ] Confirm an audio-embedded EPUB actually contains the reviewed audio files and usable navigation before listing it as produced.",
        "- [ ] Preserve uncertainty and evidence limits in the spoken script whenever omission would overstate a claim.",
        "",
        "## Non-Claims",
        "",
    ])
    for item in companion_policy.get("non_claims", []):
        lines.append(f"- {item}")
    lines.append("")

    (output_dir / companion_path).write_text("\n".join(lines), encoding="utf-8")
    return companion_path


def generate(output_dir: Path) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="asi-reader-for-audio-") as temp_dir:
        reader_dir = Path(temp_dir) / DEFAULT_READER_TEMP_NAME
        reader_summary = build_reader_edition.generate(reader_dir, "reader_release")
        profile_data = build_reader_edition.load_release_profiles()
        audio_profile = build_reader_edition.find_profile("audio_release")
        audio_policy = profile_data.get("audio_manuscript_policy", {})
        if not isinstance(audio_policy, dict):
            raise TypeError("audio_manuscript_policy must be an object")
        companion_policy = profile_data.get("companion_material_policy", {})
        if not isinstance(companion_policy, dict):
            raise TypeError("companion_material_policy must be an object")
        bundle_policy = profile_data.get("human_consumption_bundle_policy", {})
        if not isinstance(bundle_policy, dict):
            raise TypeError("human_consumption_bundle_policy must be an object")

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        script_files: list[str] = []
        treatment_summary: dict[str, dict[str, int]] = {}
        for source_path in sorted(reader_dir.rglob("*.qmd")):
            relative = source_path.relative_to(reader_dir)
            target = output_dir / relative.with_suffix(".md")
            target.parent.mkdir(parents=True, exist_ok=True)
            source_text = source_path.read_text(encoding="utf-8")
            target.write_text(qmd_to_audio_markdown(source_text), encoding="utf-8")
            script_files.append(str(target.relative_to(output_dir)))
            treatment_summary[str(target.relative_to(output_dir))] = scan_audio_treatments(source_text)

        write_pronunciation_glossary(output_dir)
        chapter_markers = write_chapter_markers(output_dir, script_files)
        companion_notes = write_audio_companion_notes(output_dir, companion_policy, treatment_summary)
        review_checklist = write_audio_checklist(
            output_dir,
            audio_profile,
            audio_policy,
            companion_policy,
            bundle_policy,
            script_files,
        )
        implementation_horizon_records = implementation_horizon_script_records(output_dir)
        implementation_horizon_status = (
            "pass"
            if all(not record["missing_headings"] for record in implementation_horizon_records)
            else "fail"
        )

        manifest = {
            "schema_version": "0.1",
            "source_profile": "reader_release",
            "audio_profile": audio_profile.get("id", "audio_release"),
            "content_layer_policy": audio_profile.get("content_layer_policy", {}),
            "source_reader_generation": reader_summary,
            "output_dir": str(output_dir),
            "human_consumption_bundle_policy": bundle_policy,
            "companion_material_policy": companion_policy,
            "script_files": script_files,
            "companion_notes": companion_notes,
            "companion_treatment_summary": treatment_summary,
            "implementation_horizon_script_status": implementation_horizon_status,
            "implementation_horizon_script_records": implementation_horizon_records,
            "pronunciation_glossary": "pronunciation_glossary.md",
            "chapter_markers": chapter_markers,
            "audio_review_checklist": review_checklist,
            "audio_artifact_formats": audio_policy.get("audio_artifact_formats", []),
            "target_artifact_status": {
                str(fmt): "target_not_generated"
                for fmt in audio_policy.get("audio_artifact_formats", [])
            },
            "audio_in_epub_rule": audio_policy.get("audio_in_epub_rule", ""),
            "reader_review_dependency": "Audio release work begins only after the reader manuscript for the same major version is reviewed.",
            "review_requirements": audio_policy.get("review_requirements", []),
            "audio_packaging_checks": audio_policy.get("audio_packaging_checks", []),
            "spoken_treatment_rules": audio_policy.get("spoken_treatment_rules", []),
            "review_status": "review_required",
            "non_claims": [
                "This generated workspace is not an audiobook.",
                "No MP3, M4B, or audio-embedded EPUB artifact is produced by this script.",
                "Tables, diagrams, images, code, and schemas require human narration treatment before release."
            ]
        }
        (output_dir / "audio_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="output directory for generated narration script")
    parser.add_argument("--check", action="store_true", help="generate into a temporary directory and verify the script workspace")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="asi-audio-script-") as temp_dir:
            manifest = generate(Path(temp_dir))
            if not manifest["script_files"]:
                raise SystemExit("Audio script check failed: no script files generated.")
            if not (Path(temp_dir) / "AUDIO_RELEASE_CHECKLIST.md").exists():
                raise SystemExit("Audio script check failed: missing AUDIO_RELEASE_CHECKLIST.md.")
            if not (Path(temp_dir) / "chapter_markers.md").exists():
                raise SystemExit("Audio script check failed: missing chapter_markers.md.")
            profile_data = build_reader_edition.load_release_profiles()
            companion_policy = profile_data.get("companion_material_policy", {})
            companion_path = str(
                companion_policy.get("audio_companion_path", "companion_notes.md")
                if isinstance(companion_policy, dict)
                else "companion_notes.md"
            )
            if not (Path(temp_dir) / companion_path).exists():
                raise SystemExit(f"Audio script check failed: missing {companion_path}.")
            if manifest["review_status"] != "review_required":
                raise SystemExit("Audio script check failed: generated manifest must require review.")
            if manifest.get("implementation_horizon_script_status") != "pass":
                missing = [
                    f"{record['script_file']}: {', '.join(record['missing_headings'])}"
                    for record in manifest.get("implementation_horizon_script_records", [])
                    if record.get("missing_headings")
                ]
                raise SystemExit(
                    "Audio script check failed: implementation horizon headings missing: "
                    + "; ".join(missing)
                )
            print(
                "Audio script check passed: "
                f"{len(manifest['script_files'])} script files generated for review."
            )
            return

    manifest = generate(Path(args.output))
    print(
        "Audio script generated: "
        f"{manifest['output_dir']} ({len(manifest['script_files'])} files)."
    )
    print("Review the script before producing or claiming audio artifacts.")


if __name__ == "__main__":
    main()
