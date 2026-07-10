#!/usr/bin/env python3
"""Synchronize dynamic public trust counts from canonical book records.

The live chapter count, source count, and core-claim disposition counts are
authoritative in JSON. Public prose surfaces retain explanatory prose, but the
counted fragments below are regenerated so ordinary manifest additions do not
require hand-edited counters.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from build_canonical_public_status import build_status, public_status_summary_block


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
DISPOSITIONS = ROOT / "claim_decisions" / "v1_x_core_claim_dispositions.json"
EVIDENCE_PLAN = ROOT / "docs" / "per_chapter_evidence_plan.md"
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
NON_CORE_LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
EVIDENCE_TRANSITIONS = ROOT / "evidence_transitions" / "v1_x_measured"


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def replace_once(text: str, pattern: str, replacement: str, path: Path) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise ValueError(f"{path.relative_to(ROOT)}: expected one match for {pattern!r}, found {count}")
    return updated


def chapter_count() -> int:
    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    return sum(len(part.get("chapters", [])) for part in structure.get("parts", []))


def chapter_ids() -> list[str]:
    structure = read_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    return [
        str(chapter["id"])
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict) and isinstance(chapter.get("id"), str)
    ]


def source_count() -> int:
    inventory = read_json(INVENTORY)
    if not isinstance(inventory, list):
        raise TypeError("sources/source_inventory.json must contain a list")
    return len(inventory)


def disposition_counts() -> tuple[int, int, int]:
    data = read_json(DISPOSITIONS)
    if not isinstance(data, dict) or not isinstance(data.get("summary"), dict):
        raise TypeError("v1_x core-claim disposition data is missing a summary")
    summary = data["summary"]
    values = (
        summary.get("manifest_chapter_core_claims"),
        summary.get("accepted_core_transition_dispositions"),
        summary.get("accepted_no_promotion_dispositions"),
    )
    if not all(isinstance(value, int) for value in values):
        raise TypeError("v1_x core-claim disposition summary has non-integer counts")
    return values  # type: ignore[return-value]


def no_promotion_side_lane_count() -> int:
    """Count accepted, non-promoting side-lane decisions from their records."""
    total = 0
    for path in EVIDENCE_TRANSITIONS.glob("*.json"):
        record = read_json(path)
        if not isinstance(record, dict):
            raise TypeError(f"{path.relative_to(ROOT)} must contain an object")
        if (
            record.get("transition_effect") == "no_change"
            and record.get("support_state_effect") == "blocks_promotion"
        ):
            total += 1
    return total


def sync_evidence_lane_counts(ids: list[str]) -> None:
    plan = EVIDENCE_PLAN.read_text(encoding="utf-8")
    plan = replace_once(
        plan,
        r"active \d+-chapter evidence-lane backlog",
        f"active {len(ids)}-chapter evidence-lane backlog",
        EVIDENCE_PLAN,
    )
    plan = replace_once(
        plan,
        r"the other (?:[a-z-]+|\d+) remain planned-only",
        f"the other {len(ids) - 3} remain planned-only",
        EVIDENCE_PLAN,
    )
    EVIDENCE_PLAN.write_text(plan, encoding="utf-8")

    cycle = ACTIVE_CYCLE.read_text(encoding="utf-8")
    selected_section_match = re.search(
        r"## Selected Lanes\n(.*?)\n## Planned-Only Lanes",
        cycle,
        flags=re.DOTALL,
    )
    if selected_section_match is None:
        raise ValueError(f"{ACTIVE_CYCLE.relative_to(ROOT)}: missing selected-lanes section")
    selected_ids = re.findall(
        r"^\|\s*`([^`]+)`\s*\|",
        selected_section_match.group(1),
        flags=re.MULTILINE,
    )
    selected = set(selected_ids)
    if not selected or any(chapter_id not in ids for chapter_id in selected):
        raise ValueError(f"{ACTIVE_CYCLE.relative_to(ROOT)}: selected-lane IDs are invalid")
    planned_ids = [chapter_id for chapter_id in ids if chapter_id not in selected]
    cycle = replace_once(
        cycle,
        r"leaves the other (?:[a-z-]+|\d+) chapter lanes planned-only",
        f"leaves the other {len(planned_ids)} chapter lanes planned-only",
        ACTIVE_CYCLE,
    )
    cycle = replace_once(
        cycle,
        r"\| Planned-only chapter lanes \| \d+ \|",
        f"| Planned-only chapter lanes | {len(planned_ids)} |",
        ACTIVE_CYCLE,
    )
    cycle = replace_once(
        cycle,
        r"all \d+ chapter core claims remain `argument`",
        f"all {len(ids)} chapter core claims remain `argument`",
        ACTIVE_CYCLE,
    )
    cycle = replace_once(
        cycle,
        r"No \d+-lane fixture sweep is claimed or implied",
        f"No {len(ids)}-lane fixture sweep is claimed or implied",
        ACTIVE_CYCLE,
    )
    planned_section_match = re.search(
        r"## Planned-Only Lanes\n(.*?)\n## Non-Claims",
        cycle,
        flags=re.DOTALL,
    )
    if planned_section_match is None:
        raise ValueError(f"{ACTIVE_CYCLE.relative_to(ROOT)}: missing planned-only section")
    bullets = list(re.finditer(r"^-\s*`([^`]+)`\s*$", planned_section_match.group(1), re.MULTILINE))
    if not bullets:
        raise ValueError(f"{ACTIVE_CYCLE.relative_to(ROOT)}: missing planned-only chapter list")
    first = planned_section_match.start(1) + bullets[0].start()
    last = planned_section_match.start(1) + bullets[-1].end()
    cycle = cycle[:first] + "\n".join(f"- `{chapter_id}`" for chapter_id in planned_ids) + cycle[last:]
    ACTIVE_CYCLE.write_text(cycle, encoding="utf-8")


def sync_public_trust_metrics() -> None:
    if (ROOT / ".git").exists():
        status = build_status()
    else:
        # Dynamic-spine fixtures copy the source tree without Git metadata.
        # The generated prose block consumes content metrics only; a zero SHA
        # and dirty state cannot be mistaken for release/deployment identity.
        status = build_status(
            source_commit_override="0" * 40,
            source_tree_state_override="dirty",
        )
    ids = chapter_ids()
    chapters = int(status["counts"]["chapters"])
    sources = int(status["counts"]["sources"])
    externally_positioned = int(status["counts"]["externally_positioned_chapters"])
    disposition_chapters = chapters
    transitions = int(status["transition_counts"]["core_no_change_dispositions"])
    no_promotions = int(status["transition_counts"]["core_no_promotion_dispositions"])
    side_lane_no_promotions = no_promotion_side_lane_count()
    if disposition_chapters != chapters:
        raise ValueError(
            "core-claim disposition count does not match manifest chapter count; "
            "write dispositions before synchronizing public metrics"
        )

    sync_evidence_lane_counts(ids)

    ledger = NON_CORE_LEDGER.read_text(encoding="utf-8")
    ledger = replace_once(
        ledger,
        r"\| Chapter core claims \| All \d+ remain at `argument`\. \|",
        f"| Chapter core claims | All {chapters} remain at `argument`. |",
        NON_CORE_LEDGER,
    )
    ledger = replace_once(
        ledger,
        r"\| Accepted no-promotion side-lane decisions \| \d+ accepted `blocks_promotion` decisions; no support-state movement\. \|",
        f"| Accepted no-promotion side-lane decisions | {side_lane_no_promotions} accepted `blocks_promotion` decisions; no support-state movement. |",
        NON_CORE_LEDGER,
    )
    ledger = replace_once(
        ledger,
        r"the active manifest now has \d+ core claims, all at `argument`",
        f"the active manifest now has {chapters} core claims, all at `argument`",
        NON_CORE_LEDGER,
    )
    NON_CORE_LEDGER.write_text(ledger, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_once(
        readme,
        r"the inventory has \d+ public-safe records; \d+/\d+ chapters are externally positioned",
        f"the inventory has {sources} public-safe records; {externally_positioned}/{chapters} chapters are externally positioned",
        readme_path,
    )
    readme = replace_once(
        readme,
        r"All \d+ chapter core claims remain at `argument`; \[the core-claim disposition ledger\]\(docs/core_claim_disposition_ledger\.md\) records \d+ per-chapter core-claim dispositions, \d+ accepted no-change transition dispositions, \d+ accepted no-promotion dispositions",
        f"All {chapters} chapter core claims remain at `argument`; [the core-claim disposition ledger](docs/core_claim_disposition_ledger.md) records {disposition_chapters} per-chapter core-claim dispositions, {transitions} accepted no-change transition dispositions, {no_promotions} accepted no-promotion dispositions",
        readme_path,
    )
    readme = replace_once(
        readme,
        r"all \d+ chapter core claims, derived from `docs/per_chapter_evidence_plan\.md`",
        f"all {chapters} chapter core claims, derived from `docs/per_chapter_evidence_plan.md`",
        readme_path,
    )
    readme = replace_once(
        readme,
        r"\d+ of \d+ chapters currently have in-prose `ext_\*` positioning",
        f"{externally_positioned} of {chapters} chapters currently have in-prose `ext_*` positioning",
        readme_path,
    )
    readme = replace_once(
        readme,
        r"turn that placement audit into a \d+-chapter grounding ledger: all \d+ chapters have source-noted external positioning records",
        f"turn that placement audit into a {chapters}-chapter grounding ledger: all {externally_positioned} chapters have source-noted external positioning records",
        readme_path,
    )
    readme = replace_once(
        readme,
        r"All \d+ chapters now carry a `\.asi-human-only` Human Reading Path bridge",
        f"All {chapters} chapters now carry a `.asi-human-only` Human Reading Path bridge",
        readme_path,
    )
    readme_path.write_text(readme, encoding="utf-8")

    index_path = ROOT / "index.qmd"
    index = index_path.read_text(encoding="utf-8")
    index = replace_once(
        index,
        r"\d+ public-safe records; \d+/\d+ chapters externally positioned",
        f"{sources} public-safe records; {externally_positioned}/{chapters} chapters externally positioned",
        index_path,
    )
    index = replace_once(
        index,
        r"The inventory has \d+ public-safe records; \d+/\d+ chapters are externally positioned",
        f"The inventory has {sources} public-safe records; {externally_positioned}/{chapters} chapters are externally positioned",
        index_path,
    )
    index = replace_once(
        index,
        r"All \d+ chapter core claims remain at `argument`; \[`the core-claim disposition ledger`\]\(docs/core_claim_disposition_ledger\.md\) records \d+ per-chapter core-claim dispositions, \d+ accepted no-change transition dispositions, \d+ accepted no-promotion dispositions",
        f"All {chapters} chapter core claims remain at `argument`; [`the core-claim disposition ledger`](docs/core_claim_disposition_ledger.md) records {disposition_chapters} per-chapter core-claim dispositions, {transitions} accepted no-change transition dispositions, {no_promotions} accepted no-promotion dispositions",
        index_path,
    )
    index_path.write_text(index, encoding="utf-8")

    publication_path = ROOT / "docs" / "publication_readiness.md"
    publication = publication_path.read_text(encoding="utf-8")
    publication = replace_once(
        publication,
        r"\d+ of \d+ chapters currently have in-prose `ext_\*` positioning",
        f"{externally_positioned} of {chapters} chapters currently have in-prose `ext_*` positioning",
        publication_path,
    )
    publication = replace_once(
        publication,
        r"currently has \d+ source-noted chapters, 0 explicit exceptions",
        f"currently has {chapters} source-noted chapters, 0 explicit exceptions",
        publication_path,
    )
    publication_path.write_text(publication, encoding="utf-8")

    block = public_status_summary_block(status)
    for surface in (
        ROOT / "README.md",
        ROOT / "index.qmd",
        ROOT / "docs" / "v1_0_candidate_status.md",
        ROOT / "docs" / "publication_readiness.md",
    ):
        text = surface.read_text(encoding="utf-8")
        pattern = r"<!-- canonical-status:generated-begin -->.*?<!-- canonical-status:generated-end -->"
        updated, count = re.subn(pattern, lambda _: block, text, flags=re.DOTALL)
        if count != 1:
            raise ValueError(
                f"{surface.relative_to(ROOT)}: expected one canonical generated-status block, found {count}"
            )
        surface.write_text(updated, encoding="utf-8")

    print(
        "Synchronized public trust metrics: "
        f"{chapters} chapters, {sources} sources, {transitions} core transitions, "
        f"{no_promotions} core no-promotion decisions."
    )


if __name__ == "__main__":
    sync_public_trust_metrics()
