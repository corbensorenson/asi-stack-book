#!/usr/bin/env python3
"""Build the maintained Human Reader draft manifest and generated surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "editions/reader_manuscript/current"
CHAPTERS = EDITION / "chapters"
GENERATED = EDITION / "generated"
MANIFEST = EDITION / "manifest.json"
CROSSWALK = EDITION / "conclusion_claim_crosswalk.json"
QUARTO = EDITION / "_quarto.yml"
INDEX = EDITION / "index.qmd"
EDITION_NAV = GENERATED / "edition-nav.html"
READER_STYLE = GENERATED / "reader.scss"
OUTLINE = ROOT / "docs/human_reader_26_unit_outline.md"
STRUCTURE = ROOT / "book_structure.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def visible_word_count(text: str) -> int:
    text = re.sub(r"^---.*?^---\s*", "", text, flags=re.MULTILINE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{<.*?>\}\}", "", text)
    return len(re.findall(r"\b[\w'-]+\b", text))


def outline_units() -> list[dict]:
    text = OUTLINE.read_text(encoding="utf-8")
    blocks = re.split(r"^## Unit ", text, flags=re.MULTILINE)[1:]
    units = []
    for block in blocks:
        heading, body = block.split("\n", 1)
        match = re.fullmatch(r"(\d+) - (.+)", heading.strip())
        if match is None:
            raise ValueError(f"Malformed unit heading: {heading!r}")

        def field(name: str, next_name: Optional[str] = None) -> str:
            end = rf"(?=\n\n\*\*{re.escape(next_name)}\.\*\*)" if next_name else r"(?=\n\n(?:\*\*|#)|\Z)"
            found = re.search(rf"\*\*{re.escape(name)}\.\*\*\s*(.*?){end}", body, flags=re.DOTALL)
            if found is None:
                raise ValueError(f"Unit {match.group(1)} missing {name}")
            return " ".join(found.group(1).split())

        target = field("Target length")
        length_match = re.fullmatch(r"([\d,]+)-([\d,]+) words\.", target)
        if length_match is None:
            raise ValueError(f"Unit {match.group(1)} has malformed target length")
        route_text = field("Canonical owner routes", "Narrative job")
        unit_id = f"unit-{int(match.group(1)):02d}"
        title = match.group(2).strip()
        units.append(
            {
                "unit_id": unit_id,
                "order": int(match.group(1)),
                "title": title,
                "owner_ids": re.findall(r"`([^`]+)`", route_text),
                "narrative_job": field("Narrative job", "Central question"),
                "central_question": field("Central question", "Argument moves"),
                "strongest_objection": field("Strongest objection", "Evidence that would change the conclusion"),
                "conclusion_change": field("Evidence that would change the conclusion", "Handoff"),
                "handoff": field("Handoff", "Target length"),
                "target_min_words": int(length_match.group(1).replace(",", "")),
                "target_max_words": int(length_match.group(2).replace(",", "")),
                "source_file": f"chapters/{unit_id}-{slugify(title)}.qmd",
            }
        )
    return units


def tracked_artifact_refs(owner: dict) -> list[dict]:
    """Return only repository paths already named by canonical owner metadata."""
    candidates = {owner["file"]}
    lean_module = owner.get("lean_module")
    if lean_module:
        candidates.add(f"lean/{lean_module.replace('.', '/')}.lean")
    encoded = json.dumps(
        {
            "proof_targets": owner.get("proof_targets", []),
            "codex_tests": owner.get("codex_tests", []),
        },
        ensure_ascii=False,
    )
    for quoted in re.findall(r"`([^`]+)`", encoded):
        try:
            tokens = shlex.split(quoted)
        except ValueError:
            tokens = quoted.split()
        for token in tokens:
            token = token.strip("'\"(),;:")
            if token and not token.startswith("-"):
                candidates.add(token)
    refs = []
    for candidate in sorted(candidates):
        path = ROOT / candidate
        if path.is_file():
            refs.append({"path": candidate, "sha256": digest(path)})
    return refs


def build_crosswalk(records: list[dict], owner_map: dict[str, dict]) -> dict:
    units = []
    for record in records:
        owners = []
        for owner_id in record["owner_ids"]:
            owner = owner_map[owner_id]
            source_note_refs = [
                f"sources/source_notes/{source_id}.md"
                for source_id in owner["source_ids"]
                if (ROOT / f"sources/source_notes/{source_id}.md").is_file()
            ]
            proof_edges = [
                {
                    "tag": target.get("tag"),
                    "module": target.get("module"),
                    "status": target.get("status"),
                    "target_sha256": digest_text(target.get("target", "")),
                }
                for target in owner.get("proof_targets", [])
            ]
            test_edges = []
            for test in owner.get("codex_tests", []):
                if isinstance(test, str):
                    test_edges.append(
                        {
                            "name": test,
                            "record_shape": "name_only",
                            "record_sha256": digest_text(json.dumps(test, ensure_ascii=False)),
                        }
                    )
                    continue
                test_edges.append(
                    {
                        "name": test.get("name"),
                        "record_shape": "structured",
                        "implementation_status": test.get("implementation_status"),
                        "record_sha256": digest_text(json.dumps(test, sort_keys=True, ensure_ascii=False)),
                    }
                )
            owners.append(
                {
                    "chapter_id": owner_id,
                    "title": owner["title"],
                    "technical_source_file": owner["file"],
                    "technical_source_sha256": digest(ROOT / owner["file"]),
                    "live_technical_path": f"chapters/{owner_id}.html",
                    "human_reader_unit_id": owner["human_reader_unit_id"],
                    "core_claim_id": f"{owner_id}.core",
                    "core_claim": owner["core_claim"],
                    "claim_label": owner["claim_label"],
                    "support_state": owner["evidence_level"],
                    "source_ids": owner["source_ids"],
                    "source_note_refs": source_note_refs,
                    "proof_edges": proof_edges,
                    "test_edges": test_edges,
                    "artifact_refs": tracked_artifact_refs(owner),
                    "publication": owner["publication"],
                }
            )
        units.append(
            {
                "unit_id": record["unit_id"],
                "order": record["order"],
                "title": record["title"],
                "human_reader_source_file": record["source_file"],
                "human_reader_source_sha256": record["source_sha256"],
                "public_path": f"reader/{Path(record['source_file']).with_suffix('.html').as_posix()}",
                "central_question": record["central_question"],
                "conclusion_change": record["conclusion_change"],
                "handoff": record["handoff"],
                "owner_count": len(owners),
                "owners": owners,
            }
        )
    owner_records = [owner for unit in units for owner in unit["owners"]]
    return {
        "schema_version": "asi_stack.human_reader_conclusion_claim_crosswalk.v1",
        "edition_id": "human-reader-current",
        "state": "canonical_current_editorial_crosswalk",
        "source_graph": "book_structure.json",
        "source_outline": "docs/human_reader_26_unit_outline.md",
        "book_structure_sha256": digest(STRUCTURE),
        "outline_sha256": digest(OUTLINE),
        "assignment_rule": "Every canonical technical owner routes to exactly one Human Reader unit while retaining its own claim, source, proof, test, artifact-reference, publication, support, and URL identity.",
        "unit_count": len(units),
        "owner_route_count": len(owner_records),
        "edge_counts": {
            "claim": len(owner_records),
            "source": sum(len(owner["source_ids"]) for owner in owner_records),
            "proof": sum(len(owner["proof_edges"]) for owner in owner_records),
            "test": sum(len(owner["test_edges"]) for owner in owner_records),
            "tracked_artifact_reference": sum(len(owner["artifact_refs"]) for owner in owner_records),
            "publication": len(owner_records),
        },
        "units": units,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "The crosswalk preserves identity and discoverability; it does not transfer or combine support among technical owners.",
            "An artifact reference means that canonical owner metadata names a tracked repository file; it does not independently validate that artifact's claims.",
            "Human Reader synthesis does not replace the live technical source for claims, sources, proofs, tests, evidence transitions, implementation status, or releases.",
            "Crosswalk completeness is not editorial approval, publication authority, safety, readiness, SOTA, AGI, or ASI evidence.",
        ],
    }


def build() -> tuple[dict, dict[Path, str]]:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    owner_map = {
        chapter["id"]: chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
    }
    units = outline_units()
    outputs: dict[Path, str] = {}
    records = []
    rendered_chapters = []
    for unit in units:
        source_path = EDITION / unit["source_file"]
        exists = source_path.is_file()
        words = visible_word_count(source_path.read_text(encoding="utf-8")) if exists else 0
        state = "not_started"
        if exists:
            state = (
                "target_length_reached_internal_review_pending"
                if unit["target_min_words"] <= words <= unit["target_max_words"]
                else "drafting"
            )
            rendered_chapters.append(unit["source_file"])
            panel_path = GENERATED / f"{unit['unit_id']}-status.qmd"
            support = sorted({owner_map[owner_id]["evidence_level"] for owner_id in unit["owner_ids"]})
            implemented_targets = sum(
                target.get("status") == "implemented"
                for owner_id in unit["owner_ids"]
                for target in owner_map[owner_id].get("proof_targets", [])
            )
            owner_links = ", ".join(
                f"[{owner_map[owner_id]['title']}](https://corbensorenson.github.io/asi-stack-book/chapters/{owner_id}.html)"
                for owner_id in unit["owner_ids"]
            )
            panel = (
                "::: {.callout-note collapse=\"true\"}\n"
                "## Research status\n\n"
                f"**Technical owners.** {len(unit['owner_ids'])} canonical routes.\n\n"
                f"**Owner routes.** {owner_links}.\n\n"
                f"**Core support states.** {', '.join(support)}.\n\n"
                f"**Implemented bounded proof targets.** {implemented_targets}.\n\n"
                "**Current boundary.** Editorial synthesis does not transfer support among owners and does not establish system-level efficiency, safety, deployment readiness, AGI, or ASI.\n\n"
                f"**What would change the conclusion.** {unit['conclusion_change']}\n\n"
                "**Technical evidence.** Follow the owner routes above and the live book's claim/evidence registry.\n"
                ":::\n"
            )
            outputs[panel_path] = panel
        records.append(
            {
                **unit,
                "state": state,
                "visible_word_count": words,
                "source_sha256": digest(source_path) if exists else None,
                "owner_support_states": sorted({owner_map[owner_id]["evidence_level"] for owner_id in unit["owner_ids"]}),
            }
        )

    part_titles = {
        1: "Part I - Why Intelligence Needs a Governed Stack",
        2: "Part II - Building Governed Cognition",
        3: "Part III - Learning, Resources, and Recursive Improvement",
    }
    chapter_lines = ["    - index.qmd"]
    for part_number, start, end in ((1, 1, 8), (2, 9, 18), (3, 19, 26)):
        part_files = [record["source_file"] for record in records if start <= record["order"] <= end and record["state"] != "not_started"]
        if part_files:
            chapter_lines.append(f"    - part: \"{part_titles[part_number]}\"")
            chapter_lines.append("      chapters:")
            chapter_lines.extend(f"        - {path}" for path in part_files)
    edition_nav = """<a class="asi-reader-skip" href="#quarto-document-content">Skip to chapter</a>
<nav class="asi-edition-switch" aria-label="Book edition">
  <span class="asi-edition-switch__label">Edition</span>
  <a data-asi-research-edition href="https://corbensorenson.github.io/asi-stack-book/">AI / researcher</a>
  <span aria-current="page">Human Reader</span>
</nav>
<script>
document.addEventListener("DOMContentLoaded", () => {
  const link = document.querySelector("[data-asi-research-edition]");
  if (!link) return;
  const marker = "/reader/";
  const index = window.location.pathname.indexOf(marker);
  if (index >= 0) {
    link.href = window.location.pathname.slice(0, index + 1);
  }
});
</script>
"""
    reader_style = """/* Generated Human Reader edition style. */
/*-- scss:defaults --*/
$body-bg: #fbfcfd;
$body-color: #20262c;
$link-color: #16677a;
$headings-color: #162b33;
$font-family-sans-serif: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
$font-family-serif: Georgia, "Times New Roman", serif;

/*-- scss:rules --*/
main.content {
  max-width: 52rem;
  font-family: $font-family-serif;
  font-size: 1.08rem;
  line-height: 1.74;
}

main.content h1,
main.content h2,
main.content h3,
main.content h4,
.sidebar-title,
.chapter-number {
  font-family: $font-family-sans-serif;
  letter-spacing: 0;
}

main.content h1 { font-size: 2.35rem; line-height: 1.12; }
main.content h2 { margin-top: 2.5rem; font-size: 1.55rem; line-height: 1.25; }
main.content h3 { margin-top: 2rem; font-size: 1.2rem; }
main.content p { margin-bottom: 1.05rem; }
main.content blockquote { border-left: 3px solid #b06b2b; color: #404a51; }
main.content table { display: block; width: 100%; max-width: 100%; overflow-x: auto; }

.asi-reader-skip {
  position: absolute;
  left: -10000px;
  top: auto;
}

.asi-reader-skip:focus {
  position: fixed;
  left: 1rem;
  top: 1rem;
  z-index: 1000;
  padding: 0.6rem 0.85rem;
  background: #ffffff;
  color: #162b33;
  border: 2px solid #16677a;
}

.asi-edition-switch {
  position: sticky;
  top: 0.5rem;
  z-index: 20;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  margin: 0.2rem 0 1.25rem;
  padding: 0.3rem;
  border: 1px solid #ccd5da;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 6px 18px rgba(22, 43, 51, 0.08);
  font-family: $font-family-sans-serif;
  font-size: 0.86rem;
}

.asi-edition-switch__label { padding: 0 0.45rem; color: #5d6970; font-weight: 650; }
.asi-edition-switch a,
.asi-edition-switch span[aria-current] {
  padding: 0.38rem 0.65rem;
  border: 1px solid transparent;
  border-radius: 6px;
  text-decoration: none;
  white-space: nowrap;
}
.asi-edition-switch a { color: #4f5d64; }
.asi-edition-switch a:hover,
.asi-edition-switch a:focus-visible { border-color: #9eacb3; color: #162b33; }
.asi-edition-switch span[aria-current] { border-color: #194d5c; background: #245f73; color: #ffffff; font-weight: 700; }

.callout-note { border-left-color: #b06b2b; background: #fffdf9; }
.sidebar-navigation a { line-height: 1.35; }

@media (max-width: 640px) {
  main.content { font-size: 1rem; line-height: 1.68; }
  main.content h1 { font-size: 2rem; }
  .asi-edition-switch { display: flex; width: 100%; justify-content: space-between; }
  .asi-edition-switch__label { flex: 1 1 auto; }
}

@media print { .asi-edition-switch, .asi-reader-skip { display: none !important; } }
"""
    outputs[EDITION_NAV] = edition_nav
    outputs[READER_STYLE] = reader_style

    quarto = (
        "# Generated by scripts/build_human_reader_current.py\n"
        "project:\n  type: book\n  output-dir: _book\n\n"
        "book:\n  title: \"The ASI Stack\"\n"
        "  subtitle: \"Human Reader Edition\"\n"
        "  author: \"Corben Sorenson\"\n"
        "  site-url: \"https://corbensorenson.github.io/asi-stack-book/reader/\"\n"
        "  repo-url: \"https://github.com/corbensorenson/asi-stack-book\"\n"
        "  repo-actions: [source, issue]\n"
        "  page-navigation: true\n  search: true\n  chapters:\n"
        + "\n".join(chapter_lines)
        + "\n\nformat:\n  html:\n    toc: true\n    number-sections: true\n"
        "    theme:\n      - cosmo\n      - generated/reader.scss\n"
        "    include-before-body:\n      - generated/edition-nav.html\n"
        "    link-external-newwindow: true\nlang: en-US\n"
    )
    outputs[QUARTO] = quarto

    index_lines = [
        "# Human Reader Edition {.unnumbered}",
        "",
        "This is the complete maintained draft of the independent 26-unit Human Reader edition. Every unit is inside its target range; editorial review and major-version release remain separate gates. The live technical book remains the claim, proof, evidence, and source authority.",
        "",
        "| Unit | Chapter | State | Words |",
        "|---:|---|---|---:|",
    ]
    for record in records:
        title = record["title"]
        if record["state"] != "not_started":
            title = f"[{title}]({record['source_file']})"
        index_lines.append(f"| {record['order']} | {title} | `{record['state']}` | {record['visible_word_count']:,} |")
    outputs[INDEX] = "\n".join(index_lines) + "\n"

    crosswalk = build_crosswalk(records, owner_map)
    crosswalk_text = json.dumps(crosswalk, indent=2, ensure_ascii=False) + "\n"
    outputs[CROSSWALK] = crosswalk_text

    manifest = {
        "schema_version": "asi_stack.human_reader_current.v1",
        "edition_id": "human-reader-current",
        "state": "complete_draft_public_html_candidate",
        "source_graph": "book_structure.json",
        "source_outline": "docs/human_reader_26_unit_outline.md",
        "book_structure_sha256": digest(STRUCTURE),
        "outline_sha256": digest(OUTLINE),
        "conclusion_claim_crosswalk": "conclusion_claim_crosswalk.json",
        "conclusion_claim_crosswalk_sha256": digest_text(crosswalk_text),
        "unit_count": len(records),
        "owner_route_count": sum(len(record["owner_ids"]) for record in records),
        "started_unit_count": sum(record["state"] != "not_started" for record in records),
        "target_length_unit_count": sum(record["state"] == "target_length_reached_internal_review_pending" for record in records),
        "visible_word_count": sum(record["visible_word_count"] for record in records),
        "units": records,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "This maintained draft is not a major-version release or a generated excerpt of the live technical chapters.",
            "A routed owner does not transfer claim, proof, source, evidence, or authority ownership to the Human Reader unit.",
            "Word-count or render completion is not editorial approval, evidence, safety, readiness, AGI, or ASI.",
            "EPUB, PDF, DOCX, audio, and full release work remain deferred until content freeze.",
        ],
    }
    outputs[MANIFEST] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    return manifest, outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    manifest, outputs = build()
    if args.write:
        CHAPTERS.mkdir(parents=True, exist_ok=True)
        GENERATED.mkdir(parents=True, exist_ok=True)
        for path, text in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(
            f"Wrote Human Reader current: {manifest['started_unit_count']}/26 started, "
            f"{manifest['visible_word_count']} visible words."
        )
        return
    stale = [path.relative_to(ROOT).as_posix() for path, text in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != text]
    if stale:
        raise SystemExit("Human Reader current derivatives are stale: " + ", ".join(stale))
    print(
        f"Human Reader current is synchronized: {manifest['started_unit_count']}/26 started, "
        f"{manifest['visible_word_count']} visible words."
    )


if __name__ == "__main__":
    main()
