#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_PATH = ROOT / "book_structure.json"
INVENTORY_PATH = ROOT / "sources" / "source_inventory.json"
CACHE_MANIFEST_PATH = ROOT / "sources" / "cache" / "cache_manifest.json"
SOURCE_NOTES_DIR = ROOT / "sources" / "source_notes"
RAW_DIR = ROOT / "sources" / "raw" / "google_docs"


PART_FRAME = {
    "foundations-alignment-governance": {
        "role": "constitutional and boundary layer",
        "article": "a",
        "input": "human purposes, institutional constraints, safety requirements, and explicit authority grants",
        "output": "stable obligations, boundaries, evidence labels, and governance constraints for every downstream layer",
        "risk": "authority can leak from persuasive reasoning into action, replacement, or deployment before the stack has earned that authority",
    },
    "planning-memory-reasoning-execution": {
        "role": "operational cognition layer",
        "article": "an",
        "input": "governed goals, command contracts, memory packets, beliefs, work orders, and tool requests",
        "output": "typed plans, context selections, claims, jobs, artifacts, approvals, and replayable execution records",
        "risk": "a plausible plan can become unreplayable work if context, proof obligations, tool permissions, and artifact identity are not carried together",
    },
    "routing-compression-representation-substrates": {
        "role": "capability substrate layer",
        "article": "a",
        "input": "tasks, residuals, benchmarks, specialist capabilities, resource budgets, representation constraints, and mathematical contracts",
        "output": "routes, compressed artifacts, specialist modules, recurrence contracts, benchmark frontiers, and residual records",
        "risk": "capability growth can become a hidden monolith if routing, compression, representation, and residual accounting are not explicit",
    },
    "evidence-implementation-living-book": {
        "role": "implementation and evidence layer",
        "article": "an",
        "input": "the whole architecture, its proof targets, source notes, tests, prototypes, benchmarks, and publication workflow",
        "output": "executable specifications, implementation roadmaps, run records, changelog entries, and public living-book releases",
        "risk": "the book can read as finished before the architecture has been implemented, tested, or falsified at the right boundaries",
    },
}

ORDINALS = [
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fifth",
    "Sixth",
    "Seventh",
    "Eighth",
    "Ninth",
    "Tenth",
]


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def esc(value: str) -> str:
    return value.replace('"', '\\"')


def yaml_list(values: list[str], indent: int = 2) -> str:
    pad = " " * indent
    if not values:
        return f"{pad}[]"
    return "\n".join(f'{pad}- "{esc(value)}"' for value in values)


def inline_code_list(values: list[str]) -> str:
    if not values:
        return "none"
    return ", ".join(f"`{value}`" for value in values)


def plain_list(values: list[str]) -> str:
    if not values:
        return "none"
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def sanitize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).replace("|", "\\|").strip()


def bullet_lines(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def numbered_mechanism(values: list[str]) -> str:
    lines = []
    for index, item in enumerate(values):
        prefix = ORDINALS[index] if index < len(ORDINALS) else f"Step {index + 1}"
        lines.append(f"{prefix}, {item[0].lower() + item[1:] if item else item}")
    return " ".join(lines)


def load_cache_records() -> dict[str, dict]:
    if not CACHE_MANIFEST_PATH.exists():
        return {}
    data = load_json(CACHE_MANIFEST_PATH)
    if not isinstance(data, dict):
        return {}
    records = data.get("records", [])
    if not isinstance(records, list):
        return {}
    return {record["id"]: record for record in records if isinstance(record, dict) and "id" in record}


def source_maps() -> tuple[dict[str, dict], dict[str, dict]]:
    inventory = load_json(INVENTORY_PATH)
    if not isinstance(inventory, list):
        raise SystemExit("source_inventory.json must contain a list.")
    return {record["id"]: record for record in inventory}, load_cache_records()


def source_note_path(source_id: str) -> Path:
    return SOURCE_NOTES_DIR / f"{source_id}.md"


def local_raw_exists(source_id: str) -> bool:
    return any((RAW_DIR / f"{source_id}{suffix}").exists() for suffix in [".txt", ".md", ".bin"])


def source_readiness(source_id: str, cache_records: dict[str, dict]) -> str:
    note = source_note_path(source_id).exists()
    cache = cache_records.get(source_id)
    raw = local_raw_exists(source_id)
    labels = []
    if note:
        labels.append("source note available")
    if raw:
        labels.append("local raw cache available")
    if cache and cache.get("status") == "connector_required":
        labels.append("connector or recovery required")
    elif cache and cache.get("status") and not raw:
        labels.append(f"cache status: {cache['status']}")
    if not labels:
        labels.append("source note pending")
    return "; ".join(labels)


def source_summary(source_ids: list[str], cache_records: dict[str, dict]) -> str:
    note_ready = [sid for sid in source_ids if source_note_path(sid).exists()]
    raw_ready = [sid for sid in source_ids if local_raw_exists(sid)]
    pending_notes = [sid for sid in source_ids if not source_note_path(sid).exists()]
    recovery = [
        sid
        for sid in source_ids
        if cache_records.get(sid, {}).get("status") == "connector_required" and not local_raw_exists(sid)
    ]

    parts = []
    if note_ready:
        parts.append(f"source notes: {inline_code_list(note_ready)}")
    if raw_ready:
        parts.append(f"raw cache: {inline_code_list(raw_ready)}")
    if pending_notes:
        parts.append(f"pending source notes: {inline_code_list(pending_notes)}")
    if recovery:
        parts.append(f"connector/recovery: {inline_code_list(recovery)}")
    return "; ".join(parts) if parts else "No sources assigned."


def queue_summary(queue: dict | None) -> str:
    if not queue:
        return "No chapter-specific source queue is recorded."
    parts = []
    labels = [
        ("primary", "primary"),
        ("supporting", "supporting"),
        ("variants", "variant"),
        ("connector_or_recovery", "connector/recovery"),
        ("handoff_or_recovery_notes", "handoff/recovery note"),
    ]
    for key, label in labels:
        values = queue.get(key, [])
        if values:
            parts.append(f"{label}: {inline_code_list(values)}")
    return "; ".join(parts) if parts else "No chapter-specific source queue is recorded."


def proof_table(chapter: dict) -> str:
    targets = chapter.get("proof_targets", [])
    if not targets:
        return (
            "| Tag | Module | Target | Status |\n"
            "|---|---|---|---|\n"
            "| none recorded | none | No proof target is recorded for this chapter yet. | not applicable |"
        )
    rows = [
        "| Tag | Module | Target | Status |",
        "|---|---|---|---|",
    ]
    for target in targets:
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{sanitize_cell(target.get('tag', ''))}`",
                    f"`{sanitize_cell(target.get('module', chapter.get('lean_module', '')) )}`",
                    sanitize_cell(target.get("target", "")),
                    sanitize_cell(target.get("status", "planned")),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def source_crosswalk(chapter: dict, inventory: dict[str, dict], cache_records: dict[str, dict]) -> str:
    rows = [
        "| Source ID | Title | Layer | Planned use | Readiness |",
        "|---|---|---|---|---|",
    ]
    for source_id in chapter.get("source_ids", []):
        record = inventory.get(source_id, {})
        title = record.get("title", "Unknown source")
        layer = record.get("layer", "unclassified")
        notes = record.get("notes", "No inventory notes recorded.")
        readiness = source_readiness(source_id, cache_records)
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{sanitize_cell(source_id)}`",
                    sanitize_cell(title),
                    sanitize_cell(layer),
                    sanitize_cell(notes),
                    sanitize_cell(readiness),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def test_table(chapter: dict) -> str:
    rows = [
        "| Test | Purpose | Status |",
        "|---|---|---|",
    ]
    for test in chapter.get("codex_tests", []):
        purpose = test_purpose(test, chapter)
        rows.append(f"| {sanitize_cell(test)} | {sanitize_cell(purpose)} | planned; not run |")
    return "\n".join(rows)


def test_purpose(test: str, chapter: dict) -> str:
    name = test.lower()
    title = chapter["title"]
    if "validation" in name or "schema" in name or "fixture" in name:
        return f"Validate the declared {title} record shape without promoting the chapter claim."
    if "trace" in name:
        return "Check that every handoff keeps stable parent artifacts, authority refs, evidence refs, and residuals."
    if "audit" in name:
        return "Check that the required records are available, replayable, and explicit about missing evidence."
    if "authority" in name or "approval" in name or "permission" in name:
        return "Check that execution cannot exceed the declared authority, approval, or permission boundary."
    if "rollback" in name or "replacement" in name:
        return "Check that a failed or weakened transition preserves a recorded rollback path."
    if "residual" in name:
        return "Check that unresolved obligations remain attached instead of being hidden inside a success label."
    if "proof" in name or "theorem" in name:
        return "Check that formal references resolve to recorded proof artifacts before any proof-backed claim is promoted."
    if "benchmark" in name or "regression" in name or "quality" in name:
        return "Check the proposed capability against declared baselines, metrics, contamination notes, and negative-result handling."
    if "review" in name or "tribunal" in name or "dissent" in name:
        return "Check that contested claims preserve reviewer roles, evidence limits, dissent, and required actions."
    return f"Check the {title} boundary against the named acceptance condition and record any missing artifact or failed predicate."


def chapter_frontmatter(chapter: dict, part: dict, today: str, source_ids: list[str]) -> str:
    open_gaps = [
        "Source notes exist for all assigned sources, but claim-level source mapping remains incomplete.",
        "No chapter-level Codex tests have been implemented or run unless separately recorded in Appendix E.",
        "No support-state promotion is implied by this drafting pass.",
    ]
    return f"""---
title: "{esc(chapter['title'])}"
chapter_id: "{esc(chapter['id'])}"
part_id: "{esc(part['id'])}"
status: "{esc(chapter.get('status', 'conceptual'))}"
draft_maturity: "v0.2 manuscript draft"
last_updated: "{today}"
primary_sources:
{yaml_list(source_ids)}
evidence_level: "{esc(chapter.get('evidence_level', 'argument'))}"
claim_label: "{esc(chapter.get('claim_label', 'Design rationale'))}"
open_evidence_gaps:
{yaml_list(open_gaps)}
---
"""


def chapter_status_table(chapter: dict, part: dict, source_ids: list[str], cache_records: dict[str, dict], today: str) -> str:
    return f"""| Field | Value |
|---|---|
| Chapter ID | `{chapter['id']}` |
| Part | {part['title']} |
| Status | {chapter.get('status', 'conceptual')} |
| Manuscript maturity | v0.2 manuscript draft |
| Last updated | {today} |
| Primary source records | {inline_code_list(source_ids)} |
| Claim label | {chapter.get('claim_label', 'Design rationale')} |
| Evidence level | {chapter.get('evidence_level', 'argument')} |
| Source queue | {sanitize_cell(queue_summary(chapter.get('source_queue')))} |
| Source loading state | {sanitize_cell(source_summary(source_ids, cache_records))} |
| Test state | Chapter-level tests remain planned unless an implemented row below records the command and result. |"""


def build_chapter(chapter: dict, part: dict, part_index: int, chapter_index: int, prev_title: str | None, next_title: str | None, inventory: dict[str, dict], cache_records: dict[str, dict], today: str) -> str:
    source_ids = chapter.get("source_ids", [])
    frame = PART_FRAME.get(part["id"], PART_FRAME["foundations-alignment-governance"])
    claim_label = chapter.get("claim_label", "Design rationale")
    evidence_level = chapter.get("evidence_level", "argument")
    source_titles = [inventory.get(source_id, {}).get("title", source_id) for source_id in source_ids[:5]]
    source_phrase = plain_list(source_titles)
    mechanism_text = numbered_mechanism(chapter.get("mechanism", []))
    prev_sentence = f"It inherits pressure from the previous chapter, {prev_title}, and makes that pressure operational in a narrower boundary." if prev_title else "It opens this part by establishing the boundary conditions that later chapters depend on."
    next_sentence = f"It hands its output to {next_title}, where the next layer tightens or implements the same constraint." if next_title else "It closes this part by making the remaining handoff to the next part explicit."

    lines = [chapter_frontmatter(chapter, part, today, source_ids)]
    lines.append(f"# {chapter['title']}\n")
    lines.append("## Chapter status\n")
    lines.append(chapter_status_table(chapter, part, source_ids, cache_records, today))
    lines.append("\n## Drafting guardrail\n")
    lines.append(
        "This chapter is a v0.2 living-book draft. It synthesizes the architecture manifest, "
        "the current outline, the source inventory, available source notes, and local raw-source readiness. "
        "It does not by itself promote any claim beyond the support state shown in the chapter metadata and Appendix C. "
        "Where the chapter uses design reasoning, it is written as architecture argument rather than as reported empirical fact."
    )
    lines.append("\n## Problem\n")
    lines.append(chapter["problem"])
    lines.append(
        f"\nWithin the ASI Stack, this is {frame['article']} {frame['role']} problem. The layer receives {frame['input']} and must turn them into {frame['output']}. "
        f"The hard part is not naming the capability; it is making the boundary explicit enough that a later layer can test, replay, reject, or replace it without guessing what authority was assumed."
    )
    lines.append(
        f"\n{prev_sentence} {next_sentence} That is why the chapter is written as part of a single stack rather than as a standalone paper summary."
    )
    lines.append("\n## Why existing approaches are insufficient\n")
    lines.append(chapter["insufficient"])
    lines.append(
        f"\nThe common failure is to treat fluent output as if it already contained the missing system contract. In practice, {frame['risk']}. "
        "A living ASI architecture needs the opposite discipline: every layer should say what it may read, what it may decide, what it may cause, what evidence it owes, and what must happen when its conditions fail."
    )
    lines.append(
        "\nThis does not mean that every layer must be heavyweight. The stack is efficient precisely because small, typed artifacts can carry constraints forward while large models, tools, humans, or specialist modules are invoked only where the current boundary demands them."
    )
    lines.append("\n## Core Claim\n")
    lines.append(
        f"[{chapter['id']}.core, label: {claim_label}, support: {evidence_level}] {chapter['core_claim']}"
    )
    lines.append(
        f"\nThe claim is architectural: it says how this layer should be shaped if the whole system is expected to remain governed under growth. "
        f"The current support state is `{evidence_level}`, so the claim should be read as a design rationale unless a later evidence bundle promotes it. "
        f"The assigned source set - {source_phrase} - gives the chapter its vocabulary and comparison points, but the public manuscript keeps source-derived support separate from the draft itself."
    )
    lines.append("\n## Mechanism\n")
    lines.append(
        "The mechanism turns the core claim into a working contract. "
        f"{mechanism_text if mechanism_text else 'The detailed mechanism remains to be decomposed into implementation artifacts.'}"
    )
    lines.append("")
    lines.append(bullet_lines(chapter.get("mechanism", [])))
    lines.append(
        "\nOperationally, the layer should produce artifacts that can be inspected without rerunning the whole cognition path. "
        "A downstream reader or executor should be able to locate the relevant inputs, constraints, residuals, authority grants, and failure conditions. "
        "That artifact discipline is what lets the stack improve without making the improvement path opaque."
    )
    lines.append(
        "\nFor implementation, the mechanism should be kept small at first: a schema, a ledger entry, a route decision, a context packet, a proof obligation, or a replayable job record. "
        "Only after that minimal form is testable should the layer absorb richer heuristics, learned routing, larger memory, or autonomous repair."
    )
    lines.append("\n## Interfaces\n")
    lines.append(
        "Interfaces are the main protection against anthology drift. They force each idea to declare what it gives to the rest of the stack and what it refuses to decide."
    )
    lines.append("")
    lines.append(bullet_lines(chapter.get("interfaces", [])))
    lines.append(
        f"\nThe upstream interface accepts the part-level inputs: {frame['input']}. The downstream interface emits {frame['output']}. "
        "When either side is ambiguous, the layer should fail closed by producing a missing-contract, missing-evidence, or missing-authority record instead of silently continuing."
    )
    lines.append(
        "\nThis interface also makes chapter insertion and reordering safer. A new chapter can be added when it introduces a genuinely new contract, invariant, or artifact type; otherwise it should merge into the layer that already owns the boundary."
    )
    lines.append("\n## Invariants\n")
    lines.append(
        "The invariants are the conditions that must remain true even when the implementation changes, the source set grows, or later chapters introduce stronger mechanisms."
    )
    lines.append("")
    lines.append(bullet_lines(chapter.get("invariants", [])))
    lines.append(
        "\nIf an invariant cannot be checked directly, the living-book version of the stack should at least record a proxy check and a residual. "
        "A weak proxy is acceptable in v0.2 when it is visible; it becomes dangerous only when the manuscript treats it as a completed proof."
    )
    lines.append("\n## Failure modes\n")
    lines.append(
        "The failure model is part of the design, not an afterthought. This layer is expected to fail in ways that can be detected, quarantined, and used to improve the architecture."
    )
    lines.append("")
    lines.append(bullet_lines(chapter.get("failure_modes", [])))
    lines.append(
        "\nThe mitigation pattern is to convert each failure into an explicit artifact: a rejected handoff, a residual record, a stale-context marker, a failed proof obligation, a benchmark regression, or a human-review queue. "
        "The stack should prefer visible incompleteness over invisible confidence."
    )
    lines.append("\n## Minimal implementation\n")
    lines.append(chapter["minimal_implementation"])
    lines.append(
        "\nFor a first implementation, the goal is not to build a full agent around the chapter. The goal is to create the smallest public-safe artifact that can be validated in CI, rendered in the book, and inspected by a future writing or coding run. "
        "That artifact can be a JSON schema, a Lean predicate, a deterministic test fixture, a trace table, a source-note map, or a replayable command."
    )
    lines.append(
        "\nThe implementation should be promoted only when its evidence exists. A planned test remains planned; a proof target remains planned; a prototype claim remains unpromoted until the code, command, environment, and result are recorded."
    )
    lines.append("\n## Codex test plan\n")
    lines.append(test_table(chapter))
    lines.append(
        "\nThese tests are acceptance targets for later implementation work. They are not reported results. "
        "When a test is implemented, the chapter should link to the command, fixture, environment notes, and result summary, and Appendix E should be regenerated or updated accordingly."
    )
    lines.append("\n### Formalization hooks\n")
    lines.append(proof_table(chapter))
    lines.append(
        "\nThe table records proof and contract hooks for future work. Planned hooks should become Lean proofs only when the predicate is precise enough to mechanize; otherwise they should become schemas, process contracts, or research-agenda items."
    )
    lines.append("\n## Source crosswalk\n")
    lines.append(source_crosswalk(chapter, inventory, cache_records))
    lines.append(
        "\nThe crosswalk describes why each source is assigned to the chapter and what is currently available in the repo. "
        "A local raw cache or source note makes future mining easier, but this draft still keeps the support state conservative until the specific claim-to-source mapping is recorded."
    )
    lines.append("\n## Summary\n")
    lines.append(
        f"{chapter['title']} defines one boundary in the ASI Stack: {chapter['core_claim']} "
        "Its job is to make a capability more governable, not merely more impressive."
    )
    lines.append(
        "\nThe chapter's v0.2 contribution is a complete architectural pass: it names the problem, states the mechanism, exposes interfaces and invariants, records failure modes, identifies minimal implementation work, and keeps source and proof obligations visible. "
        "The v1.0 work is to mine the remaining sources, promote only the claims that earn promotion, and replace planned tests with executed artifacts."
    )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    structure = load_json(STRUCTURE_PATH)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    inventory, cache_records = source_maps()
    today = date.today().isoformat()

    for part_index, part in enumerate(structure.get("parts", []), start=1):
        chapters = part.get("chapters", [])
        for chapter_index, chapter in enumerate(chapters, start=1):
            prev_title = chapters[chapter_index - 2]["title"] if chapter_index > 1 else None
            next_title = chapters[chapter_index]["title"] if chapter_index < len(chapters) else None
            path = ROOT / chapter["file"]
            path.write_text(
                build_chapter(
                    chapter,
                    part,
                    part_index,
                    chapter_index,
                    prev_title,
                    next_title,
                    inventory,
                    cache_records,
                    today,
                ),
                encoding="utf-8",
            )

    print(
        "Drafted v0.2 manuscript chapters from book_structure.json: "
        f"{sum(len(part.get('chapters', [])) for part in structure.get('parts', []))} chapters."
    )


if __name__ == "__main__":
    main()
