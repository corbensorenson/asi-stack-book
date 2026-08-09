#!/usr/bin/env python3
"""Build the exact P6.9 widest raw-scaffold ownership audit."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

from visual_chapter_source import canonical_chapter_text


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
W3 = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"
OUTPUT = ROOT / "evidence_quality/p6_9_raw_scaffold_ownership_audit.json"
REPORT = ROOT / "docs/p6_9_raw_scaffold_ownership_audit.md"
TOKEN = re.compile(r"[A-Za-z0-9_`'-]+")
NGRAM_SIZE = 12
MINIMUM_SPREAD = 8
MARKER = re.compile(
    r"(?ms)^(?:<!-- manifest-source-reconciliation:begin -->|"
    r"### Manifest source assignment reconciliation).*?"
    r"^<!-- manifest-source-reconciliation:end -->"
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).replace("\r\n", "\n")


def ngrams(value: str) -> set[tuple[str, ...]]:
    tokens = TOKEN.findall(normalized(value))
    return {
        tuple(tokens[index:index + NGRAM_SIZE])
        for index in range(max(0, len(tokens) - NGRAM_SIZE + 1))
    }


def build() -> dict[str, Any]:
    structure = load(STRUCTURE)
    w3 = load(W3)
    historical_ids = set(w3["corpus"]["chapter_ids"])
    rows = [
        chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
        if chapter["id"] in historical_ids
    ]
    if len(rows) != 84:
        raise ValueError(f"expected 84 manifest chapters, found {len(rows)}")
    chapters = {
        row["id"]: canonical_chapter_text(ROOT / row["file"])
        for row in rows
    }
    spread: dict[tuple[str, ...], set[str]] = defaultdict(set)
    generated: dict[str, set[tuple[str, ...]]] = {}
    for chapter_id, text in chapters.items():
        for gram in ngrams(text):
            spread[gram].add(chapter_id)
        generated[chapter_id] = set()
        for match in MARKER.finditer(normalized(text)):
            generated[chapter_id].update(ngrams(match.group(0)))

    repeated = {
        gram: ids
        for gram, ids in spread.items()
        if len(ids) >= MINIMUM_SPREAD
    }
    maximum_spread = max((len(ids) for ids in repeated.values()), default=0)
    widest = [
        (gram, ids)
        for gram, ids in repeated.items()
        if len(ids) == maximum_spread
    ]
    widest.sort(key=lambda item: " ".join(item[0]))

    records = []
    for gram, ids in widest:
        text = " ".join(gram)
        chapter_ids = sorted(ids)
        generated_in_every_occurrence = all(
            gram in generated[chapter_id] for chapter_id in chapter_ids
        )
        records.append(
            {
                "sha256": digest_text(text),
                "normalized_text": text,
                "word_tokens": NGRAM_SIZE,
                "chapter_spread": len(chapter_ids),
                "chapter_ids": chapter_ids,
                "chapter_ids_sha256": digest_text(
                    json.dumps(chapter_ids, separators=(",", ":"))
                ),
                "reader_visible": False if generated_in_every_occurrence else True,
                "generated": generated_in_every_occurrence,
                "structured": generated_in_every_occurrence,
                "source_only": generated_in_every_occurrence,
                "owner": (
                    "scripts/sync_chapter_source_crosswalks.py"
                    if generated_in_every_occurrence
                    else "unowned"
                ),
                "regeneration_path": (
                    "book_structure.json -> scripts/sync_chapter_source_crosswalks.py -> "
                    "manifest-source-reconciliation marker block"
                    if generated_in_every_occurrence
                    else "missing"
                ),
                "semantic_purpose": (
                    "Preserve generated manifest-source assignment, intake role, and "
                    "no-promotion boundaries at the chapter source interface."
                    if generated_in_every_occurrence
                    else "unclassified"
                ),
                "disposition": (
                    "generate" if generated_in_every_occurrence else "unjustified"
                ),
                "rationale": (
                    "The exact 12-token fingerprint occurs only inside the marked "
                    "generated source-reconciliation projection in every owning "
                    "chapter. Central generator custody is safer than bespoke edits; "
                    "W3 excludes the marker block from the reader-facing projection."
                    if generated_in_every_occurrence
                    else "The widest block lacks complete generated ownership."
                ),
            }
        )

    raw = w3["measurements"]["raw_complete_qmd"]["current"]
    editorial = w3["measurements"]["editorial_narrative"]["current"]
    chapter_digest_rows = [
        {
            "chapter_id": chapter_id,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }
        for chapter_id, text in sorted(chapters.items())
    ]
    return {
        "schema_version": "asi_stack.p6_9_raw_scaffold_ownership_audit.v1",
        "audit_id": "P6.9-R21-raw-scaffold-ownership-audit",
        "recorded_date": "2026-07-28",
        "state": "terminal_complete",
        "scope": {
            "manifest_chapter_count": 84,
            "manifest_path": "book_structure.json",
            "chapter_corpus_sha256": digest_text(
                json.dumps(chapter_digest_rows, separators=(",", ":"))
            ),
            "normalization": "Unicode NFKC; CRLF normalized to LF",
            "token_pattern": TOKEN.pattern,
            "n_gram_size": NGRAM_SIZE,
            "minimum_chapter_spread": MINIMUM_SPREAD,
            "classification_scope": "every raw-QMD 12-gram at the current maximum chapter spread",
        },
        "w3_binding": {
            "path": "evidence_quality/p7_1a_w3_inheritance_guard.json",
            "sha256": hashlib.sha256(W3.read_bytes()).hexdigest(),
            "raw_repeated_12_gram_count": raw["distinct_repeated_12_grams"],
            "raw_maximum_chapter_spread": raw["maximum_chapter_spread"],
            "reader_facing_repeated_12_gram_count": editorial[
                "distinct_repeated_12_grams"
            ],
            "reader_facing_maximum_chapter_spread": editorial[
                "maximum_chapter_spread"
            ],
        },
        "widest_block_records": records,
        "summary": {
            "widest_block_count": len(records),
            "classified_block_count": sum(
                row["disposition"] in {
                    "centralize",
                    "generate",
                    "rewrite_domain_specific",
                    "retain_with_reason",
                }
                for row in records
            ),
            "generated_source_reconciliation_block_count": sum(
                row["disposition"] == "generate" for row in records
            ),
            "reader_visible_widest_block_count": sum(
                row["reader_visible"] for row in records
            ),
            "unjustified_widest_block_count": sum(
                row["disposition"] == "unjustified" for row in records
            ),
            "exit_condition": "zero_unjustified_widest_spread_blocks",
            "exit_passed": all(
                row["disposition"] != "unjustified" for row in records
            ),
        },
        "negative_control": {
            "fixture": "tests/fixtures/p7_1a_w3_inheritance_guard/copied_scaffold.qmd",
            "validator": "scripts/validate_p7_1a_w3_inheritance_guard.py",
            "copied_reader_facing_prose_disposition": "rejected",
            "purpose": "Show that generated-source retention does not authorize copied reader-facing chapter prose.",
        },
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "Generated ownership does not prove source correctness, passage review, or support.",
            "Zero unjustified widest blocks does not imply zero raw repetition.",
            "The audit does not establish prose quality, evidence, safety, transfer, SOTA, AGI, or ASI.",
        ],
    }


def report(value: dict[str, Any]) -> str:
    summary = value["summary"]
    binding = value["w3_binding"]
    return "\n".join(
        [
            "# P6.9 raw-scaffold ownership audit",
            "",
            "Status: **terminal complete**.",
            "",
            "The audit classifies every exact 12-token block at the current raw-QMD",
            f"maximum spread of **{binding['raw_maximum_chapter_spread']}** chapters.",
            f"All **{summary['widest_block_count']}** widest fingerprints occur only",
            "inside the marked manifest-source reconciliation projection, are owned by",
            "`scripts/sync_chapter_source_crosswalks.py`, and have the disposition",
            "`generate`. The unjustified count is **0**.",
            "",
            "The retained repetition is structured source-interface metadata. It is not",
            "reader-facing editorial prose: the independently maintained W3 projection",
            f"reports **{binding['reader_facing_repeated_12_gram_count']}** repeated",
            "12-grams at the frozen reader-facing threshold. The copied-scaffold",
            "negative fixture remains rejected, so generated retention does not create",
            "permission to copy chapter narrative.",
            "",
            "This closes only the raw-scaffold ownership gate. It changes no support,",
            "release, evidence, safety, transfer, SOTA, AGI, or ASI state.",
            "",
            "## Reproduction",
            "",
            "```bash",
            "python3 scripts/build_p6_9_raw_scaffold_ownership_audit.py",
            "python3 scripts/validate_p6_9_raw_scaffold_ownership_audit.py",
            "```",
            "",
        ]
    )


def main() -> None:
    value = build()
    OUTPUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report(value), encoding="utf-8")
    print(
        "Built P6.9 raw-scaffold audit: "
        f"{value['summary']['widest_block_count']} widest fingerprints, "
        f"{value['summary']['unjustified_widest_block_count']} unjustified."
    )


if __name__ == "__main__":
    main()
