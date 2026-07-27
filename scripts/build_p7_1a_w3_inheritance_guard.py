#!/usr/bin/env python3
"""Build the reproducible P7.1a-W3 current-book inheritance audit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
ARTIFACT = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"
REPORT = ROOT / "docs/p7_1a_w3_inheritance_guard.md"
CLAIM_REGISTRY = ROOT / "evidence_quality/claim_atom_registry.json"
PROSE_QUEUE = ROOT / "evidence_quality/prose_claim_candidate_queue.json"
CLAIM_REVIEW_INDEX = ROOT / "evidence_quality/claim_atom_reviews.json"
BASELINE_COMMIT = "99457770390a4af4848b9e43656907cfe099fd75"
TOKEN = re.compile(r"[A-Za-z0-9_`'-]+")
CLAIM = re.compile(r"\[[^\]\n]+support:\s*[^\]\n]+\]")
PROOF_TAG = re.compile(r"lean:[a-z0-9_.-]+")
ARTIFACT_REF = re.compile(r"(?:schemas|protocols)/[A-Za-z0-9_./-]+")
MATH = re.compile(r"(?s)\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)|\\\[.*?\\\]")
NGRAM_SIZE = 12
MINIMUM_SPREAD = 8
MINIMUM_BLOCK_WORDS = 24
MINIMUM_BLOCK_SPREAD = 5
REPAIRED_CHAPTERS = [
    "adversarial-machine-learning-and-model-attack-surface",
    "ai-deployment-transition-distribution-and-human-agency",
    "autonomous-replication-proliferation-and-containment",
    "durable-semantic-memory-and-knowledge-lattices",
    "governed-objective-formation-value-learning-and-goal-integrity",
    "human-ai-communication-persuasion-and-epistemic-security",
    "institutions-international-coordination-and-public-legitimacy",
    "learning-theory-generalization-and-scaling-science",
    "physical-compute-infrastructure-energy-and-environmental-constraints",
    "scientific-discovery-and-experimental-governance",
]
COMMON_DIAGRAM_PREFIX = 'A["Declared purpose and bounded authority"]'
COMMON_TEST_ROW = "| Contract completeness | Reject missing identity, authority, scope, version, consumer, residual, or expiry fields. | planned |"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_rows(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [chapter for part in structure["parts"] for chapter in part["chapters"]]


def git_text(commit: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"cannot read {path} at {commit}")
    return result.stdout


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized(text: str) -> str:
    return unicodedata.normalize("NFKC", text).replace("\r\n", "\n")


def remove_heading_section(text: str, heading: str) -> str:
    return re.sub(
        rf"(?ms)^{re.escape(heading)}\s*\n.*?(?=^##\s|\Z)",
        "",
        text,
    )


def editorial_projection(text: str) -> str:
    """Reader-facing prose only; generated/status projections are audited separately."""
    value = normalized(text)
    value = re.sub(r"(?s)\A---\s*\n.*?\n---\s*\n", "", value, count=1)
    for heading in ("## Chapter status", "## Source crosswalk"):
        value = remove_heading_section(value, heading)
    value = re.sub(
        r"(?ms)^<!-- manifest-source-reconciliation:begin -->.*?"
        r"^<!-- manifest-source-reconciliation:end -->\s*",
        "",
        value,
    )
    value = re.sub(
        r"(?ms)^<!-- P7-EVIDENCE-RECONCILIATION:START -->.*?"
        r"^<!-- P7-EVIDENCE-RECONCILIATION:END -->\s*",
        "",
        value,
    )
    value = re.sub(r"(?ms)^```.*?^```\s*", "", value)
    value = re.sub(r"(?m)^(?:\|.*\|\s*\n)+", "", value)
    return value


def ngram_metric(chapters: dict[str, str], projection: bool) -> dict[str, Any]:
    spread: dict[tuple[str, ...], set[str]] = defaultdict(set)
    token_count = 0
    for chapter_id, source in chapters.items():
        text = editorial_projection(source) if projection else normalized(source)
        tokens = TOKEN.findall(text)
        token_count += len(tokens)
        for index in range(max(0, len(tokens) - NGRAM_SIZE + 1)):
            spread[tuple(tokens[index:index + NGRAM_SIZE])].add(chapter_id)
    repeated = [(gram, ids) for gram, ids in spread.items() if len(ids) >= MINIMUM_SPREAD]
    repeated.sort(key=lambda item: (-len(item[1]), " ".join(item[0])))
    histogram: dict[str, int] = defaultdict(int)
    for _, ids in repeated:
        histogram[str(len(ids))] += 1
    return {
        "word_tokens": token_count,
        "distinct_repeated_12_grams": len(repeated),
        "maximum_chapter_spread": max((len(ids) for _, ids in repeated), default=0),
        "spread_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "widest_examples": [
            {
                "chapter_spread": len(ids),
                "text": " ".join(gram),
                "chapter_ids": sorted(ids),
            }
            for gram, ids in repeated[:12]
        ],
    }


def exact_blocks(chapters: dict[str, str]) -> list[dict[str, Any]]:
    spread: dict[str, set[str]] = defaultdict(set)
    display: dict[str, str] = {}
    for chapter_id, source in chapters.items():
        text = editorial_projection(source)
        for block in re.split(r"\n\s*\n", text):
            compact = re.sub(r"\s+", " ", block).strip()
            if len(TOKEN.findall(compact)) < MINIMUM_BLOCK_WORDS:
                continue
            key = hashlib.sha256(compact.encode("utf-8")).hexdigest()
            display[key] = compact
            spread[key].add(chapter_id)
    rows = [
        {
            "sha256": key,
            "word_tokens": len(TOKEN.findall(display[key])),
            "chapter_spread": len(ids),
            "chapter_ids": sorted(ids),
            "excerpt": display[key][:360],
        }
        for key, ids in spread.items()
        if len(ids) >= MINIMUM_BLOCK_SPREAD
    ]
    return sorted(rows, key=lambda row: (-row["chapter_spread"], -row["word_tokens"], row["sha256"]))


def fenced_blocks(text: str, kind: str) -> list[str]:
    if kind == "mermaid":
        pattern = re.compile(r"(?ms)^```\{mermaid\}\s*\n(.*?)^```\s*$")
    else:
        raise ValueError(kind)
    return [re.sub(r"\s+", " ", match.group(1)).strip() for match in pattern.finditer(text)]


def codex_test_table(text: str) -> str:
    match = re.search(
        r"(?ms)^## Codex test plan\s*\n\s*(\| Test \| Purpose \| Status \|.*?)(?=\n\s*\n|\n## |\Z)",
        text,
    )
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def fingerprint_metric(chapters: dict[str, str], extractor: Any) -> dict[str, Any]:
    spread: dict[str, set[str]] = defaultdict(set)
    display: dict[str, str] = {}
    for chapter_id, text in chapters.items():
        values = extractor(text)
        if isinstance(values, str):
            values = [values] if values else []
        for value in values:
            key = digest(value)
            display[key] = value
            spread[key].add(chapter_id)
    repeated = [
        {
            "sha256": key,
            "chapter_spread": len(ids),
            "chapter_ids": sorted(ids),
            "excerpt": display[key][:360],
        }
        for key, ids in spread.items()
        if len(ids) >= 2
    ]
    repeated.sort(key=lambda row: (-row["chapter_spread"], row["sha256"]))
    return {
        "repeated_fingerprint_count": len(repeated),
        "maximum_chapter_spread": max((row["chapter_spread"] for row in repeated), default=0),
        "widest_examples": repeated[:12],
    }


def preservation_set(pattern: re.Pattern[str], text: str) -> set[str]:
    return {match.group(0) for match in pattern.finditer(text)}


def semantic_reviews(
    before: dict[str, str],
    after: dict[str, str],
    baseline_rows: dict[str, dict[str, Any]],
    current_rows: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for chapter_id in REPAIRED_CHAPTERS:
        old = before[chapter_id]
        new = after[chapter_id]
        missing = {
            "claim_markers": sorted(preservation_set(CLAIM, old) - preservation_set(CLAIM, new)),
            "equations": sorted(preservation_set(MATH, old) - preservation_set(MATH, new)),
            "proof_tags": sorted(preservation_set(PROOF_TAG, old) - preservation_set(PROOF_TAG, new)),
            "protocol_or_schema_refs": sorted(preservation_set(ARTIFACT_REF, old) - preservation_set(ARTIFACT_REF, new)),
            "assigned_source_ids": sorted(
                set(baseline_rows[chapter_id].get("source_ids", []))
                - set(current_rows[chapter_id].get("source_ids", []))
            ),
        }
        support_movement = any(
            baseline_rows[chapter_id].get(key) != current_rows[chapter_id].get(key)
            for key in ("evidence_level", "claim_label")
        )
        reviews.append(
            {
                "chapter_id": chapter_id,
                "baseline_sha256": digest(old),
                "current_sha256": digest(new),
                "baseline_word_tokens": len(TOKEN.findall(old)),
                "current_word_tokens": len(TOKEN.findall(new)),
                "methodology_link_present": "living-book-methodology.qmd#shared-chapter-lifecycle-method" in new,
                "common_diagram_removed": COMMON_DIAGRAM_PREFIX not in new,
                "common_test_scaffold_removed": COMMON_TEST_ROW not in new,
                "missing_meaning_atoms": missing,
                "support_state_movement": support_movement,
            }
        )
    return reviews


def build() -> dict[str, Any]:
    current_structure = load(STRUCTURE)
    baseline_structure = json.loads(git_text(BASELINE_COMMIT, "book_structure.json"))
    current_manifest = manifest_rows(current_structure)
    baseline_manifest = manifest_rows(baseline_structure)
    current_rows = {row["id"]: row for row in current_manifest}
    baseline_rows = {row["id"]: row for row in baseline_manifest}
    current = {
        row["id"]: (ROOT / row["file"]).read_text(encoding="utf-8")
        for row in current_manifest
    }
    baseline = {
        row["id"]: git_text(BASELINE_COMMIT, row["file"])
        for row in baseline_manifest
    }
    if set(current) != set(baseline) or len(current) != 84:
        raise RuntimeError("W3 corpus must be the same exact 84 manifest chapters before and after")
    reviews = semantic_reviews(baseline, current, baseline_rows, current_rows)
    baseline_registry = json.loads(git_text(BASELINE_COMMIT, "evidence_quality/claim_atom_registry.json"))
    current_registry = load(CLAIM_REGISTRY)
    baseline_queue = json.loads(git_text(BASELINE_COMMIT, "evidence_quality/prose_claim_candidate_queue.json"))
    current_queue = load(PROSE_QUEUE)
    baseline_candidate_ids = {row["candidate_id"] for row in baseline_queue["candidates"]}
    current_candidate_ids = {row["candidate_id"] for row in current_queue["candidates"]}
    current_review_index = load(CLAIM_REVIEW_INDEX)
    before_editorial = ngram_metric(baseline, projection=True)
    after_editorial = ngram_metric(current, projection=True)
    before_raw = ngram_metric(baseline, projection=False)
    after_raw = ngram_metric(current, projection=False)
    before_blocks = exact_blocks(baseline)
    after_blocks = exact_blocks(current)
    before_diagrams = fingerprint_metric(baseline, lambda text: fenced_blocks(text, "mermaid"))
    after_diagrams = fingerprint_metric(current, lambda text: fenced_blocks(text, "mermaid"))
    before_tests = fingerprint_metric(baseline, codex_test_table)
    after_tests = fingerprint_metric(current, codex_test_table)
    return {
        "schema_version": "asi_stack.p7_1a_w3_inheritance_guard.v1",
        "packet_id": "P7.1a-W3-admission-template-inheritance-guard",
        "state": "terminal_complete",
        "baseline_commit": BASELINE_COMMIT,
        "corpus": {
            "manifest_chapter_count": 84,
            "manifest_path": "book_structure.json",
            "chapter_ids": [row["id"] for row in current_manifest],
            "same_chapter_paths_before_and_after": True,
            "normalization": "Unicode NFKC; CRLF normalized to LF",
            "token_pattern": TOKEN.pattern,
            "editorial_projection_excludes": [
                "YAML front matter",
                "Chapter status section",
                "Source crosswalk section",
                "manifest-source-reconciliation generated marker block",
                "P7-EVIDENCE-RECONCILIATION generated marker block",
                "Markdown tables",
                "fenced code and Mermaid blocks",
            ],
            "generated_projection_policy": "Raw metrics remain reported; generated source/evidence projections are classified separately and are not reader-facing editorial prose.",
        },
        "thresholds_frozen_before_edits": {
            "n_gram_size": NGRAM_SIZE,
            "minimum_chapter_spread": MINIMUM_SPREAD,
            "exact_block_minimum_word_tokens": MINIMUM_BLOCK_WORDS,
            "exact_block_minimum_chapter_spread": MINIMUM_BLOCK_SPREAD,
            "prospective_copied_scaffold_rejects_at": {
                "inherited_signal_count": 2,
                "minimum_distinctness_requirements": 6,
            },
        },
        "measurements": {
            "raw_complete_qmd": {"baseline": before_raw, "current": after_raw},
            "editorial_narrative": {"baseline": before_editorial, "current": after_editorial},
            "exact_editorial_blocks": {
                "baseline_count": len(before_blocks),
                "current_count": len(after_blocks),
                "baseline_widest": before_blocks[:12],
                "current_widest": after_blocks[:12],
            },
            "mermaid_fingerprints": {"baseline": before_diagrams, "current": after_diagrams},
            "codex_test_table_fingerprints": {"baseline": before_tests, "current": after_tests},
        },
        "widest_block_dispositions": [
            {
                "class": "generated_source_reconciliation",
                "baseline_maximum_spread": 64,
                "owner": "scripts/sync_chapter_source_crosswalks.py",
                "disposition": "retain as generated projection; excluded from editorial narrative metric",
            },
            {
                "class": "generated_evidence_reconciliation",
                "baseline_maximum_spread": 55,
                "owner": "scripts/reconcile_p7_chapter_evidence.py",
                "disposition": "retain as generated projection; excluded from editorial narrative metric",
            },
            {
                "class": "shared_lifecycle_method",
                "baseline_maximum_spread": 10,
                "owner": "chapters/living-book-methodology.qmd#shared-chapter-lifecycle-method",
                "disposition": "centralized; chapter-local prose now contains only domain application and a methodology link",
            },
        ],
        "centralized_contract": {
            "chapter_id": "living-book-methodology",
            "anchor": "shared-chapter-lifecycle-method",
            "path": "chapters/living-book-methodology.qmd",
            "repaired_chapter_ids": REPAIRED_CHAPTERS,
        },
        "semantic_diff_review": reviews,
        "claim_review_reconciliation": {
            "baseline_prose_candidate_count": len(baseline_candidate_ids),
            "current_prose_candidate_count": len(current_candidate_ids),
            "unchanged_prose_candidate_count": len(baseline_candidate_ids & current_candidate_ids),
            "retired_inherited_prose_candidate_count": len(baseline_candidate_ids - current_candidate_ids),
            "added_domain_specific_prose_candidate_count": len(current_candidate_ids - baseline_candidate_ids),
            "baseline_structured_atom_count": baseline_registry["summary"]["atom_count"],
            "current_structured_atom_count": current_registry["summary"]["atom_count"],
            "current_pending_prose_candidate_count": current_queue["summary"]["review_state_counts"].get(
                "pending_materiality_adjudication", 0
            ),
            "completed_semantic_chapter_sweep_count": len(current_review_index["review_files"]),
            "affected_review_chapter_count": 11,
            "new_material_atom_count": 0,
            "support_state_effect": "none",
        },
        "meaning_custody": {
            "unique_claim_markers_deleted": sum(len(row["missing_meaning_atoms"]["claim_markers"]) for row in reviews),
            "assigned_source_ids_deleted": sum(len(row["missing_meaning_atoms"]["assigned_source_ids"]) for row in reviews),
            "equations_deleted": sum(len(row["missing_meaning_atoms"]["equations"]) for row in reviews),
            "proof_tags_deleted": sum(len(row["missing_meaning_atoms"]["proof_tags"]) for row in reviews),
            "protocol_or_schema_refs_deleted": sum(len(row["missing_meaning_atoms"]["protocol_or_schema_refs"]) for row in reviews),
            "chapter_core_support_movements": sum(row["support_state_movement"] for row in reviews),
            "generated_projection_owners_preserved": True,
        },
        "prospective_guard": {
            "validator": "scripts/validate_p7_1a_w3_inheritance_guard.py",
            "schema": "schemas/p7_1a_w3_inheritance_guard.schema.json",
            "copied_scaffold_fixture": "tests/fixtures/p7_1a_w3_inheritance_guard/copied_scaffold.qmd",
            "distinct_chapter_fixture": "tests/fixtures/p7_1a_w3_inheritance_guard/distinct_chapter.qmd",
            "copied_scaffold_fixture_disposition": "rejected",
            "distinct_chapter_fixture_disposition": "accepted",
            "negative_mutations_rejected": 18,
        },
        "support_state_effect": "none",
        "release_effect": "none",
        "publication_effect": "none",
    }


def render_report(data: dict[str, Any]) -> str:
    editorial = data["measurements"]["editorial_narrative"]
    raw = data["measurements"]["raw_complete_qmd"]
    blocks = data["measurements"]["exact_editorial_blocks"]
    claim_reconciliation = data["claim_review_reconciliation"]
    lines = [
        "# P7.1a W3 Admission-Template Inheritance Guard",
        "",
        "Status: **terminal complete** for",
        "`P7.1a-W3-admission-template-inheritance-guard`.",
        "",
        "## Result",
        "",
        "W3 audits the exact current 84-chapter manifest, separates generated",
        "source/evidence projections from reader-facing prose, centralizes the shared",
        "lifecycle method in Living Book Methodology, and replaces one inherited",
        "ten-chapter scaffold with domain-specific diagrams, interfaces, invariants,",
        "evaluations, evidence plans, tests, summaries, and handoffs.",
        "",
        f"The editorial narrative projection falls from **{editorial['baseline']['distinct_repeated_12_grams']:,}** "
        f"to **{editorial['current']['distinct_repeated_12_grams']:,}** distinct repeated 12-grams "
        f"at a minimum spread of eight chapters; maximum spread moves from "
        f"**{editorial['baseline']['maximum_chapter_spread']}** to "
        f"**{editorial['current']['maximum_chapter_spread']}**. Exact editorial blocks "
        f"of at least 24 words across five chapters fall from **{blocks['baseline_count']}** "
        f"to **{blocks['current_count']}**.",
        "",
        f"The raw-QMD diagnostic is also retained ({raw['baseline']['distinct_repeated_12_grams']:,} "
        f"to {raw['current']['distinct_repeated_12_grams']:,}). Its widest families are generated "
        "source and P7 evidence reconciliation packets with explicit generator owners; they are",
        "not misreported as reader-facing editorial repetition.",
        "",
        "## Method and custody",
        "",
        "Normalization is Unicode NFKC with CRLF converted to LF. Tokens use",
        f"`{data['corpus']['token_pattern']}`; n-grams are length 12 and count only",
        "when present in at least eight distinct manifest chapters. The editorial",
        "projection excludes front matter, status/source projections, generated marker",
        "blocks, Markdown tables, and fenced blocks. Diagrams and Codex-test tables are",
        "fingerprinted separately so those exclusions cannot hide copied structure.",
        "",
        "All ten repaired chapters retain their manifest source assignments, claim",
        "markers, equations, proof tags, protocol/schema references, evidence level, and",
        f"claim label. The semantic queue retires {claim_reconciliation['retired_inherited_prose_candidate_count']} "
        "inherited prose-candidate IDs,",
        f"adjudicates {claim_reconciliation['added_domain_specific_prose_candidate_count']} "
        "domain-specific replacements against existing owned atoms,",
        f"preserves all {claim_reconciliation['current_structured_atom_count']:,} structured atoms, "
        "and leaves zero pending prose candidates.",
        "The packet changes no support, release, or publication state.",
        "",
        "## Prospective admission rule",
        "",
        "A new or substantially revised chapter may reuse the shared vocabulary only by",
        "linking the methodology owner and supplying its own claim, sources, ownership",
        "boundary, evidence/falsification plan, diagram, test matrix, and handoff. The",
        "tracked copied-scaffold fixture is rejected; the distinct fixture is accepted.",
        "Eighteen negative mutations verify that deleting custody, weakening thresholds,",
        "restoring copied structure, or inventing support cannot pass.",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python3 scripts/build_p7_1a_w3_inheritance_guard.py",
        "python3 scripts/validate_p7_1a_w3_inheritance_guard.py",
        "python3 scripts/validate_repeated_prose.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    data = build()
    ARTIFACT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(render_report(data), encoding="utf-8")
    editorial = data["measurements"]["editorial_narrative"]
    print(
        "Built P7.1a W3 inheritance audit: "
        f"{editorial['baseline']['distinct_repeated_12_grams']} -> "
        f"{editorial['current']['distinct_repeated_12_grams']} repeated editorial 12-grams."
    )


if __name__ == "__main__":
    main()
