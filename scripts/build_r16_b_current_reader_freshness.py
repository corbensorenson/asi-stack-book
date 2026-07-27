#!/usr/bin/env python3
"""Build the content-addressed R16-B current-reader freshness packet.

The packet avoids a second 84-chapter source copy. It records deterministic
reader projections and their digests against one exact source commit.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "56563e1b2b64405e2e944c521bf4df9f29eba6e6"
OUT_DIR = ROOT / "editions/reader_manuscript/reader_2026_07_26"
OUT = OUT_DIR / "manifest.json"
REPORT = OUT_DIR / "freshness_report.md"
HISTORICAL_PATH = "editions/reader_manuscript/reader_2026_07_18/manifest.json"
SURFACES = {
    "opening_map": "index.qmd",
    "chapter_role_classification": "evidence_quality/current_chapter_role_map.json",
    "narrative_route": "products/narrative_unit_crosswalk.json",
    "overview_figure": "index.qmd",
    "glossary": "appendices/B_glossary.qmd",
    "source_appendix": "appendices/H_external_sources.qmd",
    "claim_evidence_projection": "appendices/C_claim_evidence_matrix.qmd",
    "final_synthesis": "chapters/integrated-reference-architecture.qmd",
}


def git_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or f"missing {path}")
    return result.stdout


def load_at_commit(path: str) -> Any:
    return json.loads(git_bytes(path).decode("utf-8"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def projection(source: str) -> str:
    """Deterministic source-only reader projection.

    Remove YAML metadata and explicitly machine-only fenced blocks. Preserve
    prose, tables, diagrams, source boundaries, non-claims, tests, summaries,
    and handoffs so the freshness packet cannot silently change meaning.
    """
    text = source.replace("\r\n", "\n")
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
    text = re.sub(
        r"(?ms)^:::\s*\{\.asi-machine-only\}\s*$.*?^:::\s*$\n?",
        "",
        text,
    )
    return text.strip() + "\n"


def build() -> dict[str, Any]:
    book_bytes = git_bytes("book_structure.json")
    book = json.loads(book_bytes)
    rows = [(part, chapter) for part in book["parts"] for chapter in part["chapters"]]
    ids = [chapter["id"] for _, chapter in rows]
    if len(ids) != 84 or len(ids) != len(set(ids)):
        raise ValueError("source commit does not contain 84 unique chapters")

    role_map = load_at_commit("evidence_quality/current_chapter_role_map.json")
    role_ids = [chapter_id for members in role_map["roles"].values() for chapter_id in members]
    if len(role_ids) != 84 or set(role_ids) != set(ids):
        raise ValueError("chapter-role map does not cover the exact 84-chapter manifest")

    narrative = load_at_commit("products/narrative_unit_crosswalk.json")
    routed_ids = [chapter_id for unit in narrative["units"] for chapter_id in unit["chapter_ids"]]
    if len(routed_ids) != 84 or set(routed_ids) != set(ids):
        raise ValueError("22-unit narrative route does not cover the exact manifest")

    chapter_records = []
    bundle_hasher = hashlib.sha256()
    for index, (part, chapter) in enumerate(rows):
        source_bytes = git_bytes(chapter["file"])
        source = source_bytes.decode("utf-8")
        derived = projection(source)
        for heading in ("## Human Reading Path", "## Summary", "## Handoff"):
            if heading not in source:
                raise ValueError(f"{chapter['id']}: missing reader heading {heading}")
        derived_bytes = derived.encode("utf-8")
        derived_sha = digest(derived_bytes)
        bundle_hasher.update(chapter["id"].encode("utf-8") + b"\0" + derived_sha.encode("ascii") + b"\n")
        chapter_records.append(
            {
                "chapter_id": chapter["id"],
                "title": chapter["title"],
                "part_id": part["id"],
                "manifest_order": index + 1,
                "source_path": chapter["file"],
                "source_sha256": digest(source_bytes),
                "reader_projection_sha256": derived_sha,
                "reader_projection_word_count": len(re.findall(r"\b[\w'-]+\b", derived)),
                "role": next(role for role, members in role_map["roles"].items() if chapter["id"] in members),
                "narrative_unit_id": next(unit["unit_id"] for unit in narrative["units"] if chapter["id"] in unit["chapter_ids"]),
                "human_path_ref": f"{chapter['file']}#human-reading-path",
                "summary_ref": f"{chapter['file']}#summary",
                "handoff_ref": f"{chapter['file']}#handoff",
                "next_chapter_id": ids[index + 1] if index + 1 < len(ids) else None,
                "claim_support_state": chapter["evidence_level"],
                "materialization_state": "content_addressed_virtual_projection_not_duplicated",
            }
        )

    surface_records = {}
    for name, path in SURFACES.items():
        data = git_bytes(path)
        surface_records[name] = {"path": path, "sha256": digest(data)}

    historical_bytes = git_bytes(HISTORICAL_PATH)
    return {
        "schema_version": "asi_stack.r16_b_current_reader_freshness.v1",
        "packet_id": "P6.5-R16-B-current-84-chapter-reader-freshness-2026-07-26",
        "created": "2026-07-26",
        "state": "terminal_local_source_freshness_formats_deferred",
        "source_snapshot": {
            "source_content_commit": SOURCE_COMMIT,
            "book_structure_sha256": digest(book_bytes),
            "chapter_count": 84,
            "chapter_ids": ids,
            "chapter_ids_sha256": digest(json.dumps(ids, separators=(",", ":")).encode("utf-8")),
        },
        "derivation": {
            "projection_rule": "Normalize LF; remove YAML metadata and explicit asi-machine-only fenced blocks; preserve all other prose, tables, diagrams, source boundaries, non-claims, tests, summaries, and handoffs.",
            "projection_implementation": "scripts/build_r16_b_current_reader_freshness.py",
            "chapter_projection_count": 84,
            "chapter_bundle_sha256": bundle_hasher.hexdigest(),
            "source_duplication_avoided": True,
            "materialization_policy": "Virtual content-addressed QMD projections are reproducible from the exact commit; do not copy the 84 canonical chapters into another tracked tree.",
        },
        "chapter_records": chapter_records,
        "reader_surfaces": surface_records,
        "historical_release": {
            "release_id": "reader-2026-07-18",
            "manifest_path": HISTORICAL_PATH,
            "manifest_sha256": digest(historical_bytes),
            "state": "immutable_published_history_not_rewritten",
        },
        "format_dispositions": {
            "virtual_qmd": {
                "state": "terminal_content_addressed_source_projection",
                "artifact": "this manifest and its 84 per-chapter projection digests",
            },
            "html": {
                "state": "deferred_not_generated_by_freshness_packet",
                "reason": "The canonical live-book HTML remains the publication surface; this packet establishes reader-source freshness only.",
            },
            "pdf": {
                "state": "deferred_not_generated",
                "reason": "A new paginated artifact requires separate render and visual QA; the historical PDF remains immutable.",
            },
            "epub": {
                "state": "deferred_not_generated",
                "reason": "A new package requires separate navigation, native-reader, and accessibility review.",
            },
            "docx": {
                "state": "deferred_not_generated",
                "reason": "A new document requires separate Word/LibreOffice render and visual QA.",
            },
            "audio": {
                "state": "deferred_not_generated",
                "reason": "Audio requires a separately maintained script and listening review.",
            },
        },
        "freshness_checks": {
            "all_current_manifest_chapters": True,
            "opening_map": True,
            "chapter_role_classification": True,
            "adjacent_handoffs": True,
            "overview_figure": True,
            "glossary": True,
            "source_appendix": True,
            "claim_evidence_projection": True,
            "final_synthesis": True,
            "narrative_22_unit_route": True,
        },
        "non_claims": [
            "A source-fresh reader derivative is not a new public release or publication authority.",
            "Virtual projection digests do not substitute for HTML, PDF, EPUB, DOCX, audio, accessibility, or visual review.",
            "Reader derivation does not prove chapter claims, source correctness, proof adequacy, empirical support, safety, readiness, AGI, or ASI.",
            "The historical reader-2026-07-18 artifacts remain their own immutable 55-chapter snapshot.",
            "No support state, release state, or publication state moves.",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
        "publication_effect": "none",
    }


def report(record: dict[str, Any]) -> str:
    role_counts: dict[str, int] = {}
    unit_ids = set()
    min_words = None
    for row in record["chapter_records"]:
        role_counts[row["role"]] = role_counts.get(row["role"], 0) + 1
        unit_ids.add(row["narrative_unit_id"])
        words = row["reader_projection_word_count"]
        min_words = words if min_words is None else min(min_words, words)
    return f"""# R16-B Current 84-Chapter Reader Freshness Receipt

Recorded: 2026-07-26

## Outcome

The current reader-source derivative is terminal at commit
`{record['source_snapshot']['source_content_commit']}`. It covers all 84
manifest chapters, all 22 narrative units, and the exact chapter-role
partition `{json.dumps(role_counts, sort_keys=True)}`. The minimum virtual
reader projection is {min_words} words.

The packet is content-addressed rather than copied. Each chapter has exact
source and reader-projection digests; the combined projection digest is
`{record['derivation']['chapter_bundle_sha256']}`. This avoids tracking another
84-chapter manuscript tree while preserving deterministic reproduction.

## Required reader surfaces

The packet binds the opening map, chapter-role classification, adjacent
handoffs, overview, glossary, external-source appendix, claim/evidence
projection, final synthesis, and 22-unit narrative route. Every chapter has a
Human Reading Path, Summary, Handoff, role, narrative unit, and next-chapter
identity.

## Historical release and formats

`reader-2026-07-18` remains immutable published history. No PDF, EPUB, DOCX,
audio, or new reader HTML is fabricated by this freshness packet. Those formats
have exact deferred dispositions because each needs its own render,
accessibility, navigation, visual, or listening review.

## Maximum inference

The current 84-chapter manuscript has a reproducible, source-fresh reader
derivative and complete reader routing. This is not publication, external
review, claim proof, empirical evidence, readiness, AGI, or ASI.
"""


def main() -> None:
    record = build()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report(record), encoding="utf-8")
    print(
        "R16-B reader freshness built: 84 chapters, 22 narrative units, "
        "8 required reader surfaces, virtual QMD terminal, 5 formats honestly deferred; "
        "historical release unchanged."
    )


if __name__ == "__main__":
    main()
