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


def narration_note(text: str) -> str:
    return f"> Narration note: {text}"


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


def generate(output_dir: Path) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="asi-reader-for-audio-") as temp_dir:
        reader_dir = Path(temp_dir) / DEFAULT_READER_TEMP_NAME
        reader_summary = build_reader_edition.generate(reader_dir, "reader_release")
        audio_profile = build_reader_edition.find_profile("audio_release")

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        script_files: list[str] = []
        for source_path in sorted(reader_dir.rglob("*.qmd")):
            relative = source_path.relative_to(reader_dir)
            target = output_dir / relative.with_suffix(".md")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(qmd_to_audio_markdown(source_path.read_text(encoding="utf-8")), encoding="utf-8")
            script_files.append(str(target.relative_to(output_dir)))

        write_pronunciation_glossary(output_dir)

        manifest = {
            "schema_version": "0.1",
            "source_profile": "reader_release",
            "audio_profile": audio_profile.get("id", "audio_release"),
            "content_layer_policy": audio_profile.get("content_layer_policy", {}),
            "source_reader_generation": reader_summary,
            "output_dir": str(output_dir),
            "script_files": script_files,
            "pronunciation_glossary": "pronunciation_glossary.md",
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
            if manifest["review_status"] != "review_required":
                raise SystemExit("Audio script check failed: generated manifest must require review.")
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
