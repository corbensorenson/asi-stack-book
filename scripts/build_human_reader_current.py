#!/usr/bin/env python3
"""Build the maintained Human Reader draft manifest and generated surfaces."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shlex
from typing import Optional
from search_navigation import render_search_navigation


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "editions/reader_manuscript/current"
CHAPTERS = EDITION / "chapters"
GENERATED = EDITION / "generated"
MANIFEST = EDITION / "manifest.json"
CROSSWALK = EDITION / "conclusion_claim_crosswalk.json"
QUARTO = EDITION / "_quarto.yml"
INDEX = EDITION / "index.qmd"
UTILITY_ROUTE = EDITION / "quickstart.qmd"
EDITION_NAV = GENERATED / "edition-nav.html"
READER_STYLE = GENERATED / "reader.scss"
OUTLINE = ROOT / "docs/human_reader_26_unit_outline.md"
STRUCTURE = ROOT / "book_structure.json"
OWNER_OUTLINE = ROOT / "docs/book_outline.md"


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


# These are editorial entry points, not extra owner assignments. The current
# owner-to-unit crosswalk supplies filenames; the named heading supplies the
# existing anchor and is checked before a projection is written.
CONCEPT_ENTRY_POINTS = [
    ("Assurance", "What does a safety argument leave unresolved?", "safety-cases-and-structured-assurance", "Assurance Must Be Incremental and Revocable", "assurance"),
    ("Authority", "Whose permission admits this effect?", "system-boundaries-and-authority", "The Authority Tuple", "authority"),
    ("Compensation", "What can a new action repair without undoing history?", "governed-operations-incident-command-and-graceful-degradation", "Recovery, Compensation, and Closure", "compensation"),
    ("Contract", "How does an agreement preserve uncertainty?", "intent-to-execution-contracts", "A Contract Should Preserve Uncertainty", "contract"),
    ("Evidence", "What does a support state actually mean?", "evidence-states-and-claim-discipline", "Support States Are Not a Confidence Score", "evidence"),
    ("Layer", "When is a responsibility distinct without being a service?", "asi-is-a-stack-not-a-model", "Logical Layers, Not a Service Tax", "layer"),
    ("Lease", "How is an effect bounded while its grant remains current?", "runtime-adapters-tool-permissions-and-human-approval", "Effect Leases Bound Action in Time", "lease"),
    ("Observation", "Which state did an instrument actually inspect?", "perception-sensor-fusion-and-observation-trust", "Observation Is Task-Relative", "observation"),
    ("Qualification", "Why can compatible components still be ineligible?", "stable-capability-fields", "Compatibility Is Not Qualification", "qualification"),
    ("Receipt", "What does a recorded event claim establish?", "artifact-graphs-audit-logs-and-replay", "Audit Logs Are Event Claims", "receipt"),
    ("Residual", "Which obligation remains after a bounded decision?", "readiness-gates-residual-escrow-and-quarantine", "Residual Escrow", "residual"),
    ("Revocation", "What happens when a grant and an effect race?", "system-boundaries-and-authority", "Revocation Is a Race", "lease"),
    ("Rollback", "Which controllable state was actually restored?", "governed-operations-incident-command-and-graceful-degradation", "Rollback Is an Effect Claim", "rollback"),
]


def narrative_section_link(records: list[dict], owner_id: str, heading: str) -> str:
    unit = next(record for record in records if owner_id in record["owner_ids"])
    source = (EDITION / unit["source_file"]).read_text(encoding="utf-8")
    if not re.search(rf"^## {re.escape(heading)}(?: \{{[^\n]+\}})?$", source, re.MULTILINE):
        raise ValueError(f"Concept entry for {owner_id} needs heading {heading!r}")
    return f"{unit['source_file']}#{slugify(heading)}"


def concept_finder(records: list[dict], site_url: str) -> list[str]:
    glossary = f"{site_url.rstrip('/')}/appendices/B_glossary.html"
    lines = [
        "## Find a Concept {#find-a-concept}", "",
        "These entry points revisit a distinction in the narrative. The working glossary gives the definition and canonical technical owner; neither route adds evidence to the claim.", "",
    ]
    for term, question, owner_id, heading, glossary_term in CONCEPT_ENTRY_POINTS:
        target = narrative_section_link(records, owner_id, heading)
        lines.extend([
            f"- **[{term}]{{#concept-{slugify(term)}}}.** [{question}]({target}) · [{term} in the working glossary]({glossary}#term-{glossary_term}).", "",
        ])
    lines.extend([
        "### Return to the Repository Example {#repository-example}", "",
        "The story is a hypothetical teaching case. Jump to the stage you need; later stages retain their stated assumptions and unresolved effects.", "",
    ])
    for label, owner_id, heading in [
        ("Decompose the request", "asi-is-a-stack-not-a-model", "One Request, Many Commitments"),
        ("Follow revocation ordering", "system-boundaries-and-authority", "Revocation Is a Race"),
        ("Separate restoration from downstream remedy", "governed-operations-incident-command-and-graceful-degradation", "Recovery, Compensation, and Closure"),
        ("Decide whether a lesson becomes durable", "adjudicated-persistence-and-the-adaptive-commit-boundary", "The Adaptive Commit Boundary"),
        ("Follow the integrated request", "integrated-reference-architecture", "Following the Repository Change"),
    ]:
        lines.extend([f"- [{label}]({narrative_section_link(records, owner_id, heading)}).", ""])
    lines.extend([
        "Search in this edition covers the current narrative. For specialist contracts, sources, or papers, follow the glossary's technical-owner links or switch to the AI / researcher edition. Historical releases retain their own status; a matching term does not make an old result current.", "",
    ])
    return lines


def owner_guide(records: list[dict], owner_map: dict[str, dict], site_url: str) -> list[str]:
    """Expose maintained outline distinctions without inventing owner roles."""
    jobs = {}
    for entry in re.split(r"(?m)^### ", OWNER_OUTLINE.read_text(encoding="utf-8"))[1:]:
        identity = re.search(r"(?m)^Stable ID: `([^`]+)`", entry)
        if not identity:
            continue
        owner_id = identity.group(1)
        if owner_id not in owner_map or owner_id in jobs:
            raise ValueError(f"Unknown or duplicate outline owner {owner_id}")
        fields = {}
        for label in ("Chapter job", "Ownership boundary", "Nearest overlapping owners"):
            match = re.search(rf"(?ms)^{label}: (.*?)(?=\n\n|\Z)", entry)
            if not match:
                raise ValueError(f"Owner guide needs {label} for {owner_id}")
            fields[label] = " ".join(match.group(1).split())
        nearest = re.findall(r"\]\(\.\./chapters/([^/)]+)\.qmd\)", fields["Nearest overlapping owners"])
        if not nearest or any(n not in owner_map or n == owner_id for n in nearest):
            raise ValueError(f"Owner guide needs valid nearest owners for {owner_id}")
        jobs[owner_id] = (fields["Chapter job"], fields["Ownership boundary"], nearest)
    if list(jobs) != list(owner_map):
        raise ValueError("Owner guide must preserve exact canonical owner coverage and order")

    def technical_link(owner_id: str) -> str:
        owner = owner_map[owner_id]
        target = f"{site_url.rstrip('/')}/{Path(owner['file']).with_suffix('.html').as_posix()}"
        return f"[{owner['title']}]({target})"

    lines = [
        "## Find the Owner of a Source or Defect {#find-an-owner}", "",
        "Choose the responsibility where the first disputed meaning or decision arises. A misread request belongs to Human Intent; a plan that changes an accepted obligation belongs to conformance or Planning; an unknown external outcome belongs to Runtime. A source can inform several owners, and its volume does not create a chapter. A genuinely new responsibility still needs the established chapter-admission review.", "",
        "Expand a narrative unit below to see the distinct jobs of its technical owners, their inputs and outputs, and the closest neighboring responsibilities. These are authored architectural roles from the maintained book outline, not proof that an implementation or scientific claim is established. A logical owner need not be a separate service, model or institution.", "",
    ]
    for unit in records:
        label = html.escape(f"Unit {unit['order']} — {unit['title']}")
        lines.extend([f'<details class="owner-routes"><summary>{label}</summary>', "",
                      f"Read the [narrative explanation]({unit['source_file']}) or follow an exact technical owner:", ""])
        for owner_id in unit["owner_ids"]:
            job, boundary, nearest = jobs[owner_id]
            lines.extend([f"**{technical_link(owner_id)}**", "", job, "", boundary, "",
                          "**Nearest overlapping owners:** " + "; ".join(technical_link(n) for n in nearest) + ".", ""])
        lines.extend(["</details>", ""])
    return lines


def reading_routes(records: list[dict], owner_map: dict[str, dict], site_url: str) -> str:
    """Project reading links from canonical owners and their existing unit routes."""
    unit_for_owner = {
        owner_id: record
        for record in records
        for owner_id in record["owner_ids"]
    }
    contribution_owners = [
        "system-boundaries-and-authority", "intent-to-execution-contracts",
        "spinoza-verification-and-proof-carrying-claims",
        "artifact-graphs-audit-logs-and-replay", "integrated-reference-architecture",
    ]
    selected = list({unit_for_owner[owner_id]["unit_id"]: unit_for_owner[owner_id]
                     for owner_id in contribution_owners}.values())
    links = " → ".join(f"[{unit['title']}]({unit['source_file']})" for unit in selected)
    words = sum(unit["visible_word_count"] for unit in selected)
    total_words = sum(unit["visible_word_count"] for unit in records)
    lines = [
        "## Choose a Reading Depth", "",
        "The links below follow the current owner-to-unit map. Length describes pacing, not editorial approval or strength of evidence.", "",
        "| Route | Who it serves and prerequisites | Scope and commitment |", "|---|---|---|",
        "| Short: this repair | A reader familiar with a repository and an ordinary permission check; no formal-methods background required. | About fifteen minutes to orient. Executing recipes and inspecting failures takes additional time. |",
        f"| Intermediate: the three contributions | A practitioner who has read the thesis above and wants authority, claims, and observed effects in one argument. | {len(selected)} selected units, {words:,} current words; allow several reading sessions. |",
        f"| Full: [the narrative in order](index.qmd) | A technically curious reader willing to build the concepts cumulatively. | {len(records)} units, {total_words:,} current words; a book-length commitment, not a quick tutorial. |",
        "", "For the intermediate route, read:", "", links + ".", "",
        "Use the full route when a selected chapter assumes an earlier concept you want to develop. The selection is an entry path, not a replacement argument.", "",
        "### Practitioner and Research Reference Paths", "",
        "These paths leave the narrative for the live technical owners. The practitioner path assumes familiarity with a change workflow; the research path assumes comfort with experimental comparisons and formal assumptions. Each is selective reference work with variable depth, not a promised completion time.", "",
    ]
    paths = {
        "Practitioner — follow a proposed change to its effect and bill": [
            "intent-to-execution-contracts", "planning-as-a-control-layer",
            "artifact-graphs-audit-logs-and-replay", "resource-economics-and-token-budgets",
            "integrated-reference-architecture",
        ],
        "Research — challenge the efficiency, evidence, learning, and proof assumptions": [
            "the-efficient-asi-hypothesis", "evidence-states-and-claim-discipline",
            "learning-compute-topology-and-adaptive-process-architecture",
            "executable-specifications-and-lean-proof-envelope", "integrated-reference-architecture",
        ],
    }
    for label, owner_ids in paths.items():
        links = " → ".join(
            f"[{owner_map[owner_id]['title']}]({site_url.rstrip('/')}/{Path(owner_map[owner_id]['file']).with_suffix('.html').as_posix()})"
            for owner_id in owner_ids
        )
        lines.extend([f"**{label}.** {links}.", ""])
    lines.extend([
        "Every path preserves the same evidence boundary: core claims retain their canonical support states; finite proofs, authored fixtures, and source-reported results answer narrower questions. Following more links cannot combine those results into whole-stack validation. The technical owners retain exact assumptions, artifacts, and open obligations.", "",
        f"To revisit a term, use the [narrative concept finder](index.qmd#find-a-concept) or the [working glossary]({site_url.rstrip('/')}/appendices/B_glossary.html). It distinguishes permission from source precedence, reports from observations and evidence, and restored state from compensation. Each definition routes to its canonical technical owner.", "",
    ])
    return "\n".join(lines)


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
                "target_length_reached_ready_for_author_review"
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

    outputs[GENERATED / "reading-routes.qmd"] = reading_routes(records, owner_map, structure["site_url"])

    part_titles = {
        1: "Part I - Why Intelligence Needs a Governed Stack",
        2: "Part II - Building Governed Cognition",
        3: "Part III - Learning, Resources, and Recursive Improvement",
    }
    if not UTILITY_ROUTE.is_file():
        raise ValueError("Human Reader utility route is missing")
    chapter_lines = ["    - index.qmd", "    - quickstart.qmd"]
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
  const diagrams = Array.from(document.querySelectorAll('.asi-reader-diagram'));
  if (!diagrams.length) return;
  let observer;
  const positionDiagrams = () => {
    for (const diagram of diagrams) {
      if (diagram.dataset.positioned || !diagram.querySelector('svg')) continue;
      const excess = Math.max(0, diagram.scrollWidth - diagram.clientWidth);
      diagram.scrollLeft = diagram.dataset.initialScroll === 'end' ? excess : excess / 2;
      diagram.dataset.positioned = 'true';
    }
    if (diagrams.every(diagram => diagram.dataset.positioned)) observer.disconnect();
  };
  observer = new MutationObserver(() => requestAnimationFrame(positionDiagrams));
  observer.observe(document.body, {childList: true, subtree: true});
  requestAnimationFrame(positionDiagrams);
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
main.content { overflow-wrap: anywhere; }
main.content .anchored { position: relative; padding-right: 1em; }
main.content .anchorjs-link { position: absolute; left: auto !important; right: 0; margin-left: 0 !important; }

.asi-reader-table {
  max-width: 100%;
  overflow-x: auto;
  margin: 1.25rem 0;
  border: 1px solid #b8c4c9;
  border-radius: 6px;
}
.asi-reader-table:focus-visible { outline: 3px solid #245f73; outline-offset: 3px; }
.asi-reader-table table { min-width: 40rem; width: 100%; margin-bottom: 0; }
.asi-reader-table th, .asi-reader-table td { overflow-wrap: normal; word-break: normal; }

.asi-reader-diagram {
  max-width: 100%;
  overflow-x: auto;
  padding: 0.75rem 0.25rem;
  margin: 1.25rem 0 0.75rem;
  border: 1px solid #b8c4c9;
  border-radius: 6px;
}
.asi-reader-diagram:focus-visible { outline: 3px solid #245f73; outline-offset: 3px; }
.asi-reader-diagram .cell-output-display { overflow: visible; }
.asi-reader-diagram svg { width: var(--asi-diagram-width, 40rem); max-width: none !important; height: auto; }
.asi-reader-diagram svg .nodeLabel,
.asi-reader-diagram svg .edgeLabel { color: #162b33 !important; }

@media (max-width: 640px) {
  main.content { font-size: 1rem; line-height: 1.68; }
  main.content h1 { font-size: 2rem; }
  .asi-edition-switch {
    position: relative;
    top: auto;
    right: auto;
    left: auto;
    transform: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    width: calc(100% - 2rem);
    max-width: 100%;
    margin: 0.75rem auto 1rem;
    justify-content: flex-start;
  }
  .asi-edition-switch__label { flex: 1 1 auto; }
  .page-navigation { flex-direction: column; gap: 0.75rem; align-items: stretch; }
  .page-navigation .nav-page { width: 100%; max-width: 100%; margin: 0; }
  .page-navigation .pagination-link { min-width: 0; max-width: 100%; }
  .page-navigation .nav-page-text { min-width: 0; overflow-wrap: anywhere; }
  .page-navigation .chapter-title { white-space: normal; }
  .quarto-secondary-nav .container-fluid { align-items: center; }
  .quarto-secondary-nav .quarto-page-breadcrumbs { flex: 1 1 auto; min-width: 0; }
  .quarto-secondary-nav .breadcrumb { flex-wrap: nowrap; margin: 0; }
  .quarto-secondary-nav .breadcrumb-item:first-child:not(:last-child) { display: none; }
  .quarto-secondary-nav .breadcrumb-item:last-child { min-width: 0; max-width: 100%; padding-left: 0; }
  .quarto-secondary-nav .breadcrumb-item:last-child::before { display: none; }
  .quarto-secondary-nav .breadcrumb-item a { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
}

@media print { .asi-edition-switch, .asi-reader-skip { display: none !important; } }
"""
    outputs[EDITION_NAV] = edition_nav
    outputs[READER_STYLE] = reader_style
    search_kinds = {"index.html": "Reader guide", "quickstart.html": "Reader guide"}
    search_kinds.update({str(Path(row["source_file"]).with_suffix(".html")): "Human Reader" for row in records})
    outputs[GENERATED / "search-navigation.html"] = render_search_navigation(search_kinds)

    quarto = (
        "# Generated by scripts/build_human_reader_current.py\n"
        "project:\n  type: book\n  output-dir: _book\n\n"
        "book:\n  title: \"The ASI Stack\"\n"
        "  subtitle: \"Human Reader Edition\"\n"
        "  author: \"Corben Sorenson\"\n"
        "  site-url: \"https://corbensorenson.github.io/asi-stack-book/reader/\"\n"
        "  repo-url: \"https://github.com/corbensorenson/asi-stack-book\"\n"
        "  repo-subdir: \"editions/reader_manuscript/current\"\n"
        "  repo-actions: [source, issue]\n"
        "  page-navigation: true\n  search: true\n  chapters:\n"
        + "\n".join(chapter_lines)
        + "\n\nformat:\n  html:\n    toc: true\n    number-sections: true\n"
        "    theme:\n      - cosmo\n      - generated/reader.scss\n"
        "    include-before-body:\n      - generated/edition-nav.html\n"
        "    include-after-body:\n      - generated/search-navigation.html\n"
        "    link-external-newwindow: true\nlang: en-US\n"
    )
    outputs[QUARTO] = quarto

    index_lines = [
        "# Human Reader Edition {.unnumbered}",
        "",
        "This is the maintained draft of the independent 26-unit Human Reader edition. Every unit is drafted and inside its pacing range. Narrative completeness requires review of the mechanism, alternative, example, failure, and conclusion; target length alone does not establish it. Author approval and major-version release remain separate gates. The live technical book remains the claim, proof, evidence, and source authority.",
        "",
        "The narrative develops three proposed contributions: **governed-cognition interface contracts**, **public claim-state transition discipline**, and **record/reality reconciliation with residual honesty**. The 89 technical owners support these composition and process proposals; they are not independent discoveries. Bounded local implementation results do not establish general superiority, novelty, or chapter-core support. The [contribution summary](https://corbensorenson.github.io/asi-stack-book/docs/three_defended_contributions.md) and [conventional alternatives](https://corbensorenson.github.io/asi-stack-book/docs/defended_contribution_prior_art_positioning.md) give the scope and challengers.",
        "",
        "Start with [A Fifteen-Minute Route Through the Stack](quickstart.qmd) to run one bounded governed repository change and inspect what is implemented, what remains proposed, and how the three execution routes differ.",
        "",
    ]
    index_lines.extend(concept_finder(records, structure["site_url"]))
    index_lines.extend(["## Chapters in Order", "", "| Unit | Chapter | State | Words |", "|---:|---|---|---:|"])
    for record in records:
        title = record["title"]
        if record["state"] != "not_started":
            title = f"[{title}]({record['source_file']})"
        state_label = {
            "target_length_reached_ready_for_author_review": "Ready for author review",
            "drafting": "Drafting",
            "not_started": "Not started",
        }[record["state"]]
        index_lines.append(f"| {record['order']} | {title} | {state_label} | {record['visible_word_count']:,} |")
    index_lines.extend(["", *owner_guide(records, owner_map, structure["site_url"])])
    outputs[INDEX] = "\n".join(index_lines).rstrip() + "\n"

    crosswalk = build_crosswalk(records, owner_map)
    crosswalk_text = json.dumps(crosswalk, indent=2, ensure_ascii=False) + "\n"
    outputs[CROSSWALK] = crosswalk_text

    # A source builder observes draft bytes, not the remote publication target.
    manifest = {
        "schema_version": "asi_stack.human_reader_current.v1",
        "edition_id": "human-reader-current",
        "state": "complete_manuscript_ready_for_author_review",
        "source_graph": "book_structure.json",
        "source_outline": "docs/human_reader_26_unit_outline.md",
        "book_structure_sha256": digest(STRUCTURE),
        "outline_sha256": digest(OUTLINE),
        "owner_guide_source": "docs/book_outline.md",
        "owner_guide_source_sha256": digest(OWNER_OUTLINE),
        "conclusion_claim_crosswalk": "conclusion_claim_crosswalk.json",
        "conclusion_claim_crosswalk_sha256": digest_text(crosswalk_text),
        "utility_route": "quickstart.qmd",
        "utility_route_sha256": digest(UTILITY_ROUTE),
        "unit_count": len(records),
        "owner_route_count": sum(len(record["owner_ids"]) for record in records),
        "started_unit_count": sum(record["state"] != "not_started" for record in records),
        "target_length_unit_count": sum(record["state"] == "target_length_reached_ready_for_author_review" for record in records),
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
            if not path.is_file() or path.read_text(encoding='utf-8') != text:
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
