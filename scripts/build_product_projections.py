#!/usr/bin/env python3
"""Build concrete narrative, architecture-reference, and evidence-registry routes."""

from __future__ import annotations

import argparse
from html import escape
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import build_knowledge_graph_companion as knowledge
import book_knowledge_graph as graph
import build_canonical_public_status as status_builder
from build_canonical_public_status import ROOT, build_status, load_json
from generated_directory import install as install_directory, ordinary, relative
from projection_files import ProjectionFiles
import research_studies as research
from research_case_rows import ARM_LABELS, anchor as research_anchor, export_csv, rows_for, study_arm_label


STRUCTURE = ROOT / "book_structure.json"
CONTRACTS = ROOT / "products" / "product_contracts.json"
SPINE = ROOT / "products" / "narrative_product_spine.json"
UNIT_CROSSWALK = ROOT / "products" / "narrative_unit_crosswalk.json"
CONTRIBUTIONS = ROOT / "products" / "contribution_focus_contract.json"
DEFAULT_OUTPUT = ROOT / "build" / "product_projections"
CURRENT_READER = ROOT / "editions/reader_manuscript/current/manifest.json"
MANIFEST_SCHEMA_VERSION = "asi_stack.product_projection_manifest.v1"
PROJECTION_SCHEMA = ROOT / "schemas/product_projection_manifest.schema.json"
STATUS_SCHEMA = ROOT / "schemas/canonical_public_status.schema.json"
SPINE_SCHEMA = ROOT / "schemas/narrative_product_spine.schema.json"
INVENTORY = ROOT / "sources/source_inventory.json"
P5_U1_RESULT = "experiments/p5_u1_governed_repository_change/results/2026-08-13-local.json"

READER_SKILL = Path("skills/asi-stack-reader/SKILL.md")
READER_UI = READER_SKILL.parent / "agents/openai.yaml"
CITATION_ARCHIVE = Path("products/citation_history/a3e9a06203978c6c3b9c5bbeb8d1f1acd640762f.json")
CITATION_SCRIPT = Path("assets/knowledge-graph/citation-history.js")

EVIDENCE_GROUPS = [
    {
        "id": "public_status",
        "label": "Canonical public status",
        "purpose": "Current commit, release profile, chapter/source totals, and claim-state distribution.",
        "entries": [
            ["Canonical status", "status/canonical-public-status.json"],
            ["Version channels", "versions/index.json"],
        ],
    },
    {
        "id": "claims_and_quality",
        "label": "Claims and evidence quality",
        "purpose": "Claim support, non-aggregating quality dimensions, and transition boundaries.",
        "entries": [
            ["Claim/evidence matrix", "appendices/C_claim_evidence_matrix.html"],
            ["Core-claim quality vectors", "evidence_quality/core_claim_vectors.json"],
            ["Core-claim dispositions", "claim_decisions/v1_x_core_claim_dispositions.json"],
        ],
    },
    {
        "id": "sources",
        "label": "Source ownership and limits",
        "purpose": "Public-safe inventory and separate local/author versus external-literature routes.",
        "entries": [
            ["Source matrix", "appendices/A_source_matrix.html"],
            ["Corben source corpus", "appendices/G_corben_source_corpus.html"],
            ["External sources", "appendices/H_external_sources.html"],
            ["Machine inventory", "sources/source_inventory.json"],
        ],
    },
    {
        "id": "proofs_tests_and_replay",
        "label": "Proofs, tests, and replay",
        "purpose": "Exact finite targets, validators, executed probes, and their non-claims.",
        "entries": [
            ["Test specification ledger", "appendices/E_codex_test_specs.html"],
            ["Proof manifest", "proofs/proof_manifest.json"],
            ["Governed workflow result", "experiments/governed_repository_change_slice/results/2026-07-10-local.json"],
            ["Trace-invariant result", "experiments/governed_trace_invariants/results/2026-07-10-local.json"],
            ["P5-U1 recorded source-link repair", P5_U1_RESULT],
        ],
    },
    {
        "id": "release_and_residuals",
        "label": "Release, review, and residual state",
        "purpose": "What is published or blocked, which reviews exist, and which decisions remain open.",
        "entries": [
            ["Publication readiness", "docs/publication_readiness.md"],
            ["External review status", "docs/external_review_status.md"],
            ["Remediation program", "docs/external_ai_review_remediation_program.md"],
            ["Changelog", "appendices/F_changelog.html"],
        ],
    },
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ProductPayload:
    """Pure byte preparation: --check does not create even a temporary tree."""
    def __init__(self, root: Path):
        self.root = root
        self.files: dict[str, bytes] = {}

    def write(self, path: Path, data: bytes) -> None:
        name = relative(path.relative_to(self.root).as_posix())
        self.files[name] = data


def write_text(path: Path, text: str, payload: ProductPayload | None = None) -> None:
    if payload is None:
        ProjectionFiles().write(path, text)
    else:
        payload.write(path, text.encode("utf-8"))


def write_json(path: Path, value: Any, payload: ProductPayload | None = None) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n", payload)


class ProductInputs:
    """Bind the bytes actually read, including optional snapshot presence."""
    def __init__(self, status_path: Path | None):
        self.status_path = status_path
        self.data: dict[Path, bytes | None] = {}
        required = [STRUCTURE, CONTRACTS, SPINE, UNIT_CROSSWALK, CONTRIBUTIONS, CURRENT_READER,
                    PROJECTION_SCHEMA, STATUS_SCHEMA, SPINE_SCHEMA, INVENTORY]
        required.extend(ROOT / name for name in ("scripts/build_product_projections.py", "scripts/generated_directory.py",
                                                "scripts/build_tested_site_bundle.py",
                                                "scripts/build_canonical_public_status.py", "scripts/projection_files.py",
                                                "scripts/validate_product_projections.py", "scripts/schema_validation.py", "scripts/admission_guard.py"))
        required.extend(ROOT / name for name in (READER_SKILL, READER_UI, CITATION_ARCHIVE, CITATION_SCRIPT, "LICENSE.md"))
        for path in required:
            self.capture(path)
        self.capture(ROOT / research.RECORDS)
        self.capture(ROOT / "assets/study-case-browser.js")
        self.research_manifest = self.json(ROOT / research.RECORDS)
        for name in sorted(research.input_paths(self.research_manifest)):
            self.capture(ROOT / relative(name.as_posix()))
        self.capture(ROOT / research.AUDIT_LOCK)
        for name in sorted(research.audit_replay_paths(lambda path: self.data[ROOT / path])):
            self.capture(ROOT / relative(name.as_posix()))
        self.capture(ROOT / research.GIT_LOCK)
        for name in sorted(research.git_replay_paths(lambda path: self.data[ROOT / path])):
            self.capture(ROOT / relative(name.as_posix()))
        for name in (graph.CITATIONS, graph.IDENTITIES):
            self.capture(ROOT / name)
        for name in knowledge.input_paths(lambda path: self.data[ROOT / relative(path)]):
            self.capture(ROOT / relative(name))
        for group in EVIDENCE_GROUPS:
            for _, target in group["entries"]:
                self.capture(ROOT / relative(target), optional=True)
        if status_path is not None:
            self.capture(status_path)
            self.status = self.json(status_path)
        else:
            self.auto_notes = self.note_presence()
            self.auto_paths = self.status_inputs()
            for path in self.auto_paths:
                self.capture(path)
            self.status = build_status()
        # Retain the existing status schema/domain owners, without granting a
        # supplied status record authority to change the manuscript's counts.
        status_builder.validate_status_shape(self.status)
        errors = status_builder.validate_against_schema(self.status, self.json(STATUS_SCHEMA), "product status")
        if errors:
            raise ValueError("; ".join(errors[:8]))
        canonical = canonical_chapters(self.json(STRUCTURE))
        if (self.status["counts"]["chapters"] != len(canonical)
                or self.status["counts"]["sources"] != len(self.json(INVENTORY))
                or self.status["digests"]["book_structure_sha256"] != self.digest(STRUCTURE)
                or self.status["digests"]["source_inventory_sha256"] != self.digest(INVENTORY)
                or self.status["claim_state_distribution"]["support_states"] != {"argument": len(canonical)}):
            raise ValueError("product status does not match canonical chapter/support counts")
        self.status_consumed = self.consumed_status(self.status)
        self.identity = {}
        for path, data in self.data.items():
            name = "inputs/supplied-status.json" if path == status_path else path.relative_to(ROOT).as_posix()
            self.identity[name] = hashlib.sha256(data).hexdigest() if data is not None else None
        self.identity["inputs/derived-status-consumed.json"] = hashlib.sha256(self.status_consumed).hexdigest()
        if status_path is None:
            self.identity["inputs/external-note-presence.json"] = hashlib.sha256(json.dumps(self.auto_notes).encode()).hexdigest()
        self.guard()

    def capture(self, path: Path, *, optional: bool = False) -> None:
        ordinary(path)
        if path in self.data:
            if self.data[path] is None and not optional:
                raise ValueError(f"missing product input: {path}")
            return
        if path.exists() and not path.is_file():
            raise ValueError(f"product input is not a regular file: {path}")
        if not path.is_file() and not optional:
            raise ValueError(f"missing product input: {path}")
        self.data[path] = path.read_bytes() if path.is_file() else None

    def status_inputs(self) -> list[Path]:
        paths = [ROOT / path.relative_to(status_builder.ROOT) for path in
                 (status_builder.CONFIG, status_builder.INVENTORY, status_builder.DISPOSITIONS,
                  status_builder.RELEASE_PROFILES, status_builder.CLAIM_IDENTITY_GRAPH)]
        paths += [ROOT / relative(chapter["file"]) for part in self.json(STRUCTURE)["parts"] for chapter in part["chapters"]]
        for pattern in ("evidence_transitions/v1_0_measured/*.json", "evidence_transitions/v1_x_measured/*.json"):
            paths += sorted(ROOT.glob(pattern))
        return paths

    def note_presence(self) -> list[str]:
        # The status owner consumes filenames only, not note bodies.
        names = []
        for path in sorted(ROOT.glob("sources/source_notes/ext_*.md")):
            ordinary(path)
            if not path.is_file():
                raise ValueError(f"external note presence is not a regular file: {path}")
            names.append(path.relative_to(ROOT).as_posix())
        return names

    @staticmethod
    def consumed_status(status: dict) -> bytes:
        # build_timestamp is deliberately not consumed by a product page.
        # Explicit --status bytes still retain their full source identity.
        value = {key: status[key] for key in ("status_id", "source_commit", "counts", "claim_state_distribution")}
        return json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")

    def json(self, path: Path) -> Any:
        return json.loads(self.data[path])

    def digest(self, path: Path) -> str:
        return hashlib.sha256(self.data[path]).hexdigest()

    def guard(self) -> None:
        for path, data in self.data.items():
            ordinary(path)
            if path.exists() and not path.is_file():
                raise ValueError(f"product input became a special object: {path}")
            if (path.read_bytes() if path.is_file() else None) != data:
                raise ValueError(f"product input changed while preparing: {path}")
        if self.status_path is None:
            if (self.status_inputs() != self.auto_paths or self.note_presence() != self.auto_notes
                    or self.consumed_status(build_status()) != self.status_consumed):
                raise ValueError("derived product status/input set changed while preparing")


def canonical_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    order = 0
    for part_index, part in enumerate(structure.get("parts", []), start=1):
        for chapter in part.get("chapters", []):
            order += 1
            chapter_id = str(chapter.get("chapter_id") or chapter.get("id") or "")
            source_file = str(chapter.get("file", ""))
            rows.append({
                "order": order,
                "part_order": part_index,
                "part_title": str(part.get("title", "")),
                "chapter_id": chapter_id,
                "title": str(chapter.get("title", "")),
                "source_file": source_file,
                "public_path": str(Path(source_file).with_suffix(".html")),
                "core_claim_ref": f"{chapter_id}.core",
                "core_claim": str(chapter.get("core_claim", "")),
                "claim_label": str(chapter.get("claim_label", "")),
                "support_state": str(chapter.get("evidence_level", "")),
            })
    return rows


def safe_rel_link(from_product_dir: str, target: str) -> str:
    depth = len(Path(from_product_dir).parts)
    return "../" * depth + target


def page(title: str, subtitle: str, body: str, manifest_link: str, *, show_portfolio: bool = True) -> str:
    portfolio = (
        '<p>Three proposed contributions organize all three products: <strong>governed-cognition interface contracts</strong>, '
        '<strong>public claim-state transition discipline</strong>, and <strong>record/reality reconciliation with residual honesty</strong>. '
        'The 89 technical chapters support composition and process proposals with bounded local implementation results. '
        'Selection establishes neither novelty nor chapter-core support. Read the <a href="../../docs/three_defended_contributions.md">contribution summary</a> '
        'and <a href="../../docs/defended_contribution_prior_art_positioning.md">competent conventional alternatives</a>.</p>'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · The ASI Stack</title>
<style>
:root {{ color-scheme: light dark; --ink:#17212b; --paper:#fff; --muted:#52606d; --rule:#d8e0e8; --accent:#175b8c; }}
@media (prefers-color-scheme:dark) {{ :root {{ --ink:#edf3f8; --paper:#10161c; --muted:#b3c0cb; --rule:#34424e; --accent:#7fc7ff; }} }}
* {{ box-sizing:border-box; }} body {{ margin:0; background:var(--paper); color:var(--ink); font:17px/1.58 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ width:min(980px,calc(100% - 2rem)); margin:0 auto; padding:3rem 0 5rem; }}
h1 {{ font-size:clamp(2rem,6vw,4rem); line-height:1.02; margin:.3rem 0 1rem; }} h2 {{ margin-top:2.4rem; }}
a {{ color:var(--accent); }} .eyebrow {{ color:var(--muted); text-transform:uppercase; letter-spacing:.09em; font-weight:700; font-size:.78rem; }}
.lead {{ color:var(--muted); font-size:1.15rem; max-width:72ch; }} .status {{ border-left:.3rem solid var(--accent); padding:.65rem 1rem; background:color-mix(in srgb,var(--accent) 8%,transparent); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr)); gap:1rem; }}
.card {{ border:1px solid var(--rule); border-radius:.6rem; padding:1rem; }} .card h3 {{ margin:.1rem 0 .55rem; }}
.meta {{ color:var(--muted); font-size:.92rem; }} nav {{ display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:2rem; }}
pre, .table-scroll {{ overflow:auto; }} table {{ border-collapse:collapse; }} th, td {{ padding:.35rem .6rem; border:1px solid var(--rule); }}
details[data-study-cases] {{ border-block:1px solid var(--rule); padding:.55rem 0; }}
details[data-study-cases] summary {{ cursor:pointer; font-weight:600; }}
details[data-study-cases] select {{ font:inherit; max-width:100%; }}
tr:target {{ outline:2px solid var(--accent); outline-offset:-2px; }}
main {{ overflow-wrap:anywhere; }}
</style>
</head>
<body><main>
<nav><a href="../../index.html">Book home</a><a href="../index.html">Three products</a><a href="{escape(manifest_link)}">Machine manifest</a></nav>
<div class="eyebrow">Product projection</div>
<h1>{escape(title)}</h1>
<p class="lead">{escape(subtitle)}</p>
{portfolio if show_portfolio else ""}
{body}
</main></body></html>
"""


def build_narrative(
    output: Path,
    canonical: list[dict[str, Any]],
    spine: dict[str, Any],
    contributions: dict[str, dict[str, Any]],
    *, inputs: ProductInputs | None = None, payload: ProductPayload | None = None,
) -> dict[str, Any]:
    by_id = {row["chapter_id"]: row for row in canonical}
    unit_crosswalk = inputs.json(UNIT_CROSSWALK) if inputs else load_json(UNIT_CROSSWALK)
    current_reader = inputs.json(CURRENT_READER) if inputs else load_json(CURRENT_READER)
    unit_by_representative = {
        unit["representative_chapter_id"]: unit
        for unit in unit_crosswalk["units"]
    }
    unit_by_chapter = {
        chapter_id: unit
        for unit in unit_crosswalk["units"]
        for chapter_id in unit["chapter_ids"]
    }
    unit_owner_by_chapter = {
        chapter_id: unit["representative_chapter_id"]
        for unit in unit_crosswalk["units"]
        for chapter_id in unit["chapter_ids"]
    }
    selected: list[dict[str, Any]] = []
    for record in spine["chapters"]:
        row = dict(by_id[record["chapter_id"]])
        row.update(record)
        unit = unit_by_representative[row["chapter_id"]]
        reference_owners = []
        for chapter_id in unit["chapter_ids"]:
            if chapter_id == row["chapter_id"]:
                continue
            owner = by_id[chapter_id]
            reference_owners.append({
                "chapter_id": chapter_id,
                "title": owner["title"],
                "canonical_order": owner["order"],
                "core_claim_ref": owner["core_claim_ref"],
                "distinct_responsibility": owner["core_claim"],
                "claim_label": owner["claim_label"],
                "support_state": owner["support_state"],
                "architecture_reference_path": owner["public_path"],
            })
        row["unit_id"] = unit["unit_id"]
        row["unit_label"] = unit["label"]
        row["reference_owner_count"] = len(reference_owners)
        row["reference_owners"] = reference_owners
        assignment = contributions.get(row["chapter_id"], {})
        row["contribution_id"] = assignment.get("contribution_id")
        selected.append(row)
    selected_ids = {row["chapter_id"] for row in selected}
    selected_orders = [row["order"] for row in selected]
    omitted: list[dict[str, Any]] = []
    for row in canonical:
        if row["chapter_id"] in selected_ids:
            continue
        owner_id = unit_owner_by_chapter[row["chapter_id"]]
        omitted.append({
            "chapter_id": row["chapter_id"],
            "title": row["title"],
            "canonical_order": row["order"],
            "architecture_reference_path": row["public_path"],
            "nearest_narrative_owner": owner_id,
            "unit_id": unit_by_chapter[row["chapter_id"]]["unit_id"],
            "unit_label": unit_by_chapter[row["chapter_id"]]["label"],
            "distinct_responsibility": row["core_claim"],
            "claim_label": row["claim_label"],
            "support_state": row["support_state"],
        })
    manifest = {
        "schema_version": "asi_stack.narrative_product_projection.v1",
        "custody_mode": "historical_candidate_navigation",
        "current_reader": {
            "entry_path": "reader/index.html",
            "unit_count": current_reader["unit_count"],
            "owner_route_count": current_reader["owner_route_count"],
            "manifest_sha256": inputs.digest(CURRENT_READER) if inputs else sha256_file(CURRENT_READER),
            "review_state": "ready_for_author_review_not_an_approved_multiformat_release",
        },
        "status": spine["status"],
        "selected_chapter_count": len(selected),
        "canonical_chapter_count": len(canonical),
        "selected_canonical_orders": selected_orders,
        "chapters": selected,
        "reference_only_chapters": omitted,
        "review_gate": spine["review_gate"],
        "non_claims": spine["non_claims"],
    }
    product_dir = output / "narrative-book"
    write_json(product_dir / "manifest.json", manifest, payload)
    cards = []
    for row in selected:
        link = safe_rel_link("products/narrative-book", row["public_path"]) + "?view=human"
        reference_owner_items = "".join(
            '<li><a href="'
            + escape(
                safe_rel_link(
                    "products/narrative-book",
                    owner["architecture_reference_path"],
                )
                + "?view=human"
            )
            + '">'
            + escape(owner["title"])
            + '</a><br><span class="meta"><strong>Distinct responsibility:</strong> '
            + escape(owner["distinct_responsibility"])
            + '<br><code>'
            + escape(owner["core_claim_ref"])
            + "</code> · "
            + escape(owner["claim_label"])
            + " at <code>"
            + escape(owner["support_state"])
            + "</code> support</span></li>"
            for owner in row["reference_owners"]
        )
        if reference_owner_items:
            reference_owner_block = (
                f'<details><summary><strong>Specialist reference owners '
                f'({row["reference_owner_count"]})</strong></summary>'
                f'<p class="meta">These chapters retain their own claims, sources, evidence '
                f'ceilings, and implementation responsibilities.</p><ul>{reference_owner_items}</ul></details>'
            )
        else:
            reference_owner_block = (
                '<p class="meta"><strong>Specialist reference owners:</strong> '
                'none; this representative is the unit’s sole canonical owner.</p>'
            )
        cards.append(
            f'<article class="card"><div class="meta">{row["order"]} · {escape(row["unit_label"])} · '
            f'<code>{escape(row["core_claim_ref"])}</code></div>'
            f'<h3><a href="{escape(link)}">{escape(row["title"])}</a></h3>'
            f'<p><strong>Plain-language thesis:</strong> {escape(row["plain_language_thesis"])}</p>'
            f'<p><strong>Engineering rule:</strong> {escape(row["normative_engineering_rule"])}</p>'
            f'<p class="meta"><strong>Machine contract:</strong> {escape(row["machine_contract"])}</p>'
            f'<p><strong>Question:</strong> {escape(row["reader_question"])}</p>'
            f'<p class="meta"><strong>Running example:</strong> {escape(row["running_example"])}</p>'
            f'{reference_owner_block}</article>'
        )
    body = (
        '<p class="status"><strong>Current Human Reader:</strong> '
        f'<a href="../../reader/">Read the independently authored {manifest["current_reader"]["unit_count"]}-unit book</a>, '
        f'routed to all {manifest["current_reader"]["owner_route_count"]} technical owners. '
        'HTML is available and editorial review remains open. '
        'This does not approve EPUB, PDF or audio.</p>'
        '<h2>Historical candidate navigation</h2>'
        '<p class="status"><strong>Status:</strong> historical generated twenty-two-unit candidate route. '
        'It is not a reviewed reader release, and the other canonical chapters remain in the architecture reference.</p>'
        '<h2>Thesis-to-method route</h2><div class="grid">' + "".join(cards) + '</div>'
        f'<h2>Reference routing</h2><p>{len(omitted)} specialized chapters remain discoverable in the architecture reference; none was deleted or demoted.</p>'
    )
    write_text(product_dir / "index.html",
        page("Narrative technical book", "A bounded thesis-to-method reading route with the live research scaffold hidden in Human view.", body, "manifest.json"),
        payload,
    )
    return manifest


def build_reference(
    output: Path,
    canonical: list[dict[str, Any]],
    contributions: dict[str, dict[str, Any]],
    *, payload: ProductPayload | None = None,
) -> dict[str, Any]:
    chapters = []
    for row in canonical:
        record = dict(row)
        assignment = contributions.get(row["chapter_id"], {})
        record["contribution_id"] = assignment.get("contribution_id")
        record["contribution_role"] = assignment.get("contribution_role")
        chapters.append(record)
    manifest = {
        "schema_version": "asi_stack.architecture_reference_projection.v0",
        "status": "generated_complete_reference_index_not_a_deployed_system",
        "chapter_count": len(chapters),
        "chapters": chapters,
        "supporting_routes": [
            "appendices/D_protocol_schemas.html",
            "appendices/K_implementation_horizons.html",
            "appendices/B_glossary.html",
        ],
        "non_claims": [
            "A complete reference index does not establish deployed enforcement or architecture quality.",
            "Chapter inclusion does not promote a support state.",
            "The canonical Quarto source remains authoritative.",
        ],
    }
    product_dir = output / "architecture-reference"
    write_json(product_dir / "manifest.json", manifest, payload)
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in chapters:
        groups.setdefault(row["part_title"], []).append(row)
    sections = []
    for part, rows in groups.items():
        cards = []
        for row in rows:
            link = safe_rel_link("products/architecture-reference", row["public_path"]) + "?view=ai"
            cards.append(
                f'<article class="card"><div class="meta">{row["order"]} · {escape(str(row.get("contribution_role") or ""))}</div>'
                f'<h3><a href="{escape(link)}">{escape(row["title"])}</a></h3>'
                f'<details><summary>Distinct responsibility</summary><p>{escape(row["core_claim"])}</p></details>'
                f'<p class="meta"><code>{escape(row["core_claim_ref"])}</code> · '
                f'{escape(row["claim_label"])} at <code>{escape(row["support_state"])}</code> support'
                f'<br>{escape(str(row.get("contribution_id") or ""))}</p></article>'
            )
        sections.append(f"<h2>{escape(part)}</h2><div class=\"grid\">{''.join(cards)}</div>")
    body = (
        '<p class="status"><strong>Status:</strong> complete generated lookup index over every canonical chapter. '
        'It is a specification route, not evidence of a deployed stack.</p>' + "".join(sections)
    )
    write_text(product_dir / "index.html",
        page("Architecture reference specification", "All responsibilities, interfaces, invariants, failure routes, implementation horizons, and technical chapters in canonical order.", body, "manifest.json"),
        payload,
    )
    return manifest


def study_table(label: str, headings: list[str], rows: str) -> str:
    header = "".join(f'<th scope="col">{escape(heading)}</th>' for heading in headings)
    return (
        f'<div class="table-scroll" role="region" aria-label="{escape(label)}" tabindex="0"><table>'
        f'<caption>{escape(label)}</caption><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table></div>'
    )


def graph_link(record_id: str, label: str = "Open in the graph") -> str:
    target = "knowledge-graph/?" + urlencode({"node": record_id})
    return f'<a href="{escape(target)}">{escape(label)}</a>'


def paired_case_table(run: dict, cases: list[dict], featured: set[str]) -> str:
    rows = []
    methods = list(dict.fromkeys(method for row in cases for method in row["arms"]))
    for row in cases:
        fragment = research_anchor(run["id"], row["id"])
        cells = []
        for method in methods:
            if method in row["arms"]:
                value = row["arms"][method]
                cells.append(f'<td>{escape(value["outcome"])}<br><small>{escape(value["work"])}</small></td>')
            else:
                cells.append('<td>Ineligible without an identifier</td>')
        outcomes = "".join(cells)
        attributes = "".join(f" data-{name}" for name in ("disagrees", "exhausted", "adverse") if row[name])
        graph_id = f'evidence_case:{run["id"]}--{row["id"]}'
        graph_route = f'<br><small>{graph_link(graph_id)}</small>' if graph_id in featured else ""
        rows.append(
            f'<tr id="{fragment}"{attributes}><th scope="row"><a href="#{fragment}">{escape(row["id"])}</a>{graph_route}</th>'
            f'<td>{escape(row["condition"])}</td>{outcomes}</tr>'
        )
    differences = sum(row["disagrees"] for row in cases)
    options = [("all", "All cases")]
    options.extend((key, label) for key, label in (
        ("disagrees", "Different outcomes"), ("exhausted", "Budget exhausted"), ("adverse", "Adverse cases")
    ) if any(row[key] for row in cases))
    selectors = "".join(f'<option value="{key}">{label}</option>' for key, label in options)
    return (
        f'<h4>Paired cases</h4><p>{differences} of {len(cases)} cases have differing outcomes. '
        f'<a href="cases-{run["id"]}.csv" download>Download paired-case CSV</a>.</p>'
        f'<details data-study-cases open><summary>Inspect {len(cases)} paired cases</summary>'
        f'<p><label hidden>Filter paired cases <select>{selectors}</select></label> '
        f'<span role="status" data-case-count></span></p>'
        + study_table(f'{run["title"]} cases', ["Case", "Conditions", *(study_arm_label(key) for key in methods)],
                      "".join(rows))
        + "</details>"
    )


def study_outcomes(format_id: str, result: dict) -> str:
    if format_id == "transfer_pilot_v1":
        totals = result["totals"]
        fields = ("verified", "budget_exhausted", "attempts", "screening_primitive_steps", "checker_primitive_steps")
        rows = "".join(
            f'<tr><th scope="row">{ARM_LABELS[arm]}</th>'
            + "".join(f'<td>{record[key]:,}</td>' for key in fields) + '</tr>'
            for arm, record in totals.items()
        )
        return study_table("Search and verification work across the twelve later tasks",
                           ["Arm", "Verified", "Exhausted", "Proposals", "Screening steps", "Verification steps"], rows)
    if format_id == "transfer_factorial_v1":
        arms = result["summary"]["all"]["arms"]
        rows = "".join(
            f'<tr><th scope="row">{escape(name)}</th><td>{stratum["cells"]}</td>'
            + "".join(f'<td>{stratum["arms"][arm]["verified"]}</td>' for arm in arms) + '</tr>'
            for name, stratum in result["summary"].items() if name != "all"
        )
        order = ", ".join(f"{ARM_LABELS[arm]} {count}" for arm, count in result["ordering_success_changes"].items())
        return (
            study_table("Verified design cells by resource and query",
                        ["Resource and query", "Cells", *(ARM_LABELS[arm] for arm in arms)], rows)
            + f"<p>Outcome changed with operator ordering in these counts of task, query and budget combinations: {order}.</p>"
            + '<p>Neutral queries contain no matching terms. Their residual differences reflect the fixed tie-break and task-ID control. '
              'The raw result separates screening, verification, queue and indexing work. The timing artifact reports CPU diagnostics.</p>'
        )
    if format_id == "transfer_scheduler_v1":
        keys = tuple(arm + "__" + order for arm in ("no_library", "aware_whole", "aware_routine")
                     for order in ("handle-depth", "expanded-length"))
        rows = "".join(
            f'<tr><th scope="row">{escape(label)}</th><td>{item["cells"]}</td>'
            + "".join(f'<td>{item["arms"][key]}</td>' for key in keys) + '</tr>'
            for label, item in result["summary"].items()
        )
        return study_table("Verified cells under each scheduler", ["Resource and query", "Cells",
                            *(study_arm_label(key) for key in keys)], rows)
    if format_id == "verifier_policy_audit_v2":
        arms = result["totals"]
        measures = {
            "documents_constructed": "Documents constructed",
            "document_bytes_serialized": "Document bytes serialized",
            "document_bytes_hashed": "Document bytes hashed",
            "index_hashes": "Index hashes",
            "index_bytes_hashed": "Index bytes hashed",
            "index_reads": "Index reads",
            "document_reads": "Evidence document reads",
            "policy_evaluations": "Policy evaluations",
            "notification_invalidations": "Delivered invalidations",
            "expiry_invalidations": "Expiry invalidations",
            "missed_update_recoveries": "Missed updates recovered",
            "cache_writes": "Cache writes",
            "handoff_bytes_serialized": "Handoff bytes serialized",
        }
        rows = "".join(
            f'<tr><th scope="row">{label}</th>'
            + "".join(f'<td>{values.get(key, 0):,}</td>' for values in arms.values()) + '</tr>'
            for key, label in measures.items()
        )
        return study_table("Recorded work across all eleven profiles", ["Work", *(study_arm_label(key) for key in arms)], rows)
    if format_id == "verifier_freshness_v1":
        arms = research.freshness_work(result)
        measures = [
            ("routes", "specialist", "Specialist decisions"),
            ("work", "document_reads", "Evidence documents read"),
            ("work", "handoff_bytes", "Local cache serialization bytes"),
        ]
        if any(values["wire"] for values in arms.values()):
            measures += [
                ("wire", "messages", "Authority and worker pipe messages"),
                ("wire", "payload_bytes", "Authority and worker pipe payload bytes"),
            ]
        rows = "".join(
            f'<tr><th scope="row">{label}</th>'
            + "".join(f'<td>{values[group].get(key, 0):,}</td>' for values in arms.values()) + '</tr>'
            for group, key, label in measures
        )
        return study_table("Paired decisions and recorded work", ["Measure", *(study_arm_label(key) for key in arms)], rows)
    if format_id == "receiver_effect_audit_v2":
        rows = "".join(
            f'<tr id="receiver-control-{escape(c["id"])}"><th scope="row">{escape(c["id"])}</th>'
            f'<td>{escape(c["observed_effect"].replace("_", " "))}</td>'
            f'<td>{"Yes" if c["safe_hold"] else "No"}</td>'
            f'<td>{"Yes" if c["false_closure"] else "No"}</td></tr>'
            for c in result["controls"]
        )
        return study_table("Receiver score controls", ["Control", "Observed effect", "Safe hold", "False closure"], rows)
    return ""


def render_run(study: dict, row: dict, result: dict, cases: list[dict], featured: set[str], replay: str = "") -> str:
    source = f'{research.REPO}/blob/{row["source_commit"]}'
    artifacts = [("Raw paired result", row["result"]), ("Pinned protocol", row["protocol"]), *(
        (Path(target).name, target) for target in row["inputs"] if target != row["protocol"]
    )]
    artifact_links = "".join(
        f'<li><a href="{escape(source + "/" + target)}">{escape(label)}</a></li>'
        for label, target in artifacts
    )
    fragment = research_anchor(row["id"])
    predecessor = row.get("follow_up_to")
    follows = (f'<p>Follow-up to <a href="#{research_anchor(predecessor)}">{escape(next(run["title"] for run in study["runs"] if run["id"] == predecessor))}</a>.</p>'
               if predecessor else "")
    replay_note = (" The Git repair also needs its pre-fix history." if row["format"] == "scoped_git_v1" else "")
    if row["format"] == "review_packet":
        replay_note = (f' Replace TESTED_SITE with the rendered site at {escape(result["source_commit"])}. '
                       'The retained packets also contain every opened excerpt and score.')
    elif row["format"] in {"package_transport", "package_observation"}:
        replay_note = ' This command collects a new network observation. Use the raw result below for the original snapshot.'
    return (
        f'<section id="{fragment}"><h3>{escape(row["title"])} <a href="#{fragment}" aria-label="Link to this run">#</a></h3>'
        f'{follows}<p>{escape(row["method"])}</p><h4>Result</h4><p>{escape(row["summary"])}</p>'
        f'{study_outcomes(row["format"], result)}'
        f'<h4>Scope and limits</h4><p>{escape(row["limit"])}</p>'
        f'<p>{graph_link("study_run:" + row["id"])}</p>'
        f'<h4>Disposition</h4><p>{escape(row["disposition"])}</p>'
        f'<h4>Replay</h4><p>Run from a checkout at this evidence revision.{replay_note}</p>'
        f'<pre><code>{escape(row["command"])}</code></pre><ul>{artifact_links}</ul>'
        + replay +
        f'<h4>Cite this run</h4><p>Corben Sorenson. “{escape(study["title"])}.” '
        f'<em>The ASI Stack</em>, {escape(row["date"])}. Run <code>{row["id"]}</code>, evidence revision '
        f'<a href="{escape(source + "/" + row["result"])}"><code>{row["source_commit"]}</code></a>. '
        f'Result SHA-256 <code>{row["result_sha256"]}</code>.</p>'
        + paired_case_table(row, cases, featured) + "</section>"
    )


def current_study_decision(study: dict) -> str:
    run = research_anchor(study["featured_run"])
    return (
        '<section id="current-decision"><h2>Current decision</h2>'
        f'<p class="status"><strong>{escape(study["disposition"])}</strong></p>'
        f'<p>{escape(study["summary"])}</p>'
        f'<p><strong>Scope and limits.</strong> {escape(study["limit"])}</p>'
        f'<p><a href="#{run}">Inspect the featured run and its conditions</a>.</p></section>'
    )


def receiver_cost_exercise(study: dict) -> str:
    history = {run["id"]: run["metrics"] for run in study["runs"]}
    local = history["receiver-availability"]
    requests = local["additional_calls"] - local["matched_calls"]
    payload = local["matched_bytes"] - local["additional_bytes"]
    return (
        '<section id="price-an-avoided-request"><h2>What is an avoided request worth?</h2>'
        f'<p>In the <a href="#run-receiver-availability">local replay</a>, the gateway saved {requests} caller requests '
        f'and added {payload:,} payload bytes. Break-even on those two prices was {payload/requests:g} bytes per '
        'request avoided. Price a request like 100 bytes and caller fallback wins. Price it like 500 and '
        'the gateway wins.</p><p>The <a href="#run-receiver-distribution">first delivery follow-up</a> '
        'modeled a fallback after an unavailable primary. In the <a href="#run-receiver-live-transport">'
        'measured transport follow-up</a> the caller knew to skip the primary. No caller requests were saved, '
        'so there is no per-request break-even. The services shared an npm origin. '
        '<a href="../../chapters/resource-economics-and-token-budgets.html#receiver-break-even">'
        'Reprice the two workloads</a>.</p></section>'
    )


def forward_transfer_choices(study: dict) -> str:
    by_format = {run["format"]: run for run in study["runs"]}
    factorial = by_format["transfer_factorial_v1"]["metrics"]
    scheduler = by_format["transfer_scheduler_v1"]["metrics"]
    conditions = (
        ("Handle depth, proposal cap", factorial["stratum_cells"],
         factorial["proposal_whole"], factorial["proposal_routine"], by_format["transfer_factorial_v1"]),
        ("Handle depth, expanded-work cap", factorial["stratum_cells"],
         factorial["expanded_whole"], factorial["expanded_routine"], by_format["transfer_factorial_v1"]),
        ("Expanded-length priority, proposal cap", scheduler["stratum"],
         scheduler["whole_reordered"], scheduler["routines_reordered"], by_format["transfer_scheduler_v1"]),
    )
    rows = "".join(
        f'<tr><th scope="row"><a href="#{research_anchor(run["id"])}">{escape(label)}</a></th>'
        f'<td>{whole} / {cells}</td><td>{routine} / {cells}</td></tr>'
        for label, cells, whole, routine, run in conditions
    )
    return (
        '<h3>Which representation wins under a different budget?</h3>'
        '<p>These comparisons use descriptive queries and the same five-bit task lineages. '
        'Each denominator counts design cells and repeated conditions.</p>'
        + study_table("Verified cells under three search conditions",
                      ["Scheduler and cap", "Query-aware whole programs", "Query-aware routines"], rows)
    )


def independent_reports(reports: list[dict], study: dict, status: dict) -> str:
    runs = {row["id"] for row in study["runs"]}
    relevant = [row for row in reports if row["run"] in runs]
    if study["id"] != "verifier-rollout" and not relevant:
        return ""
    template = f'{research.REPO}/blob/{status["source_commit"]}/{research.REPORT_TEMPLATE.as_posix()}'
    body = (
        '<h2 id="independent-checks">Independent checks</h2>'
        f'<p>Use the <a href="{escape(template)}">independent check report template</a> for an exact rerun, '
        'independent reanalysis or changed assumption. Each published revision preserves the report and its disposition.</p>'
    )
    if not relevant:
        return body + '<p>No independent check reports have been published for this study.</p>'
    for row in relevant:
        source = f'{research.REPO}/blob/{row["source_commit"]}/{row["artifact"]}'
        report_id = f'{row["id"]}-revision-{row["revision"]}'
        body += (
            f'<section id="report-{report_id}"><h3>{escape(report_id)}</h3>'
            f'<p>{escape(row["kind"])} · <a href="#{research_anchor(row["run"])}">{escape(row["run"])}</a> · '
            f'<a href="{escape(source)}">Pinned report</a> · SHA-256 <code>{row["artifact_sha256"]}</code></p>'
            f'<p>{escape(row["reported_result"])}</p>'
            f'<p><strong>{escape(row["disposition"])}</strong> {escape(row["decision"])}</p></section>'
        )
    return body


def build_research(product_dir: Path, status: dict, inputs: ProductInputs | None,
                   payload: ProductPayload | None, featured: set[str]) -> tuple[list[dict], str]:
    def read(name):
        return inputs.data[ROOT / name] if inputs else (ROOT / name).read_bytes()

    manifest = inputs.research_manifest if inputs else json.loads(read(research.RECORDS))
    case_browser = product_dir / "study-case-browser.js"
    case_browser_source = read(Path("assets/study-case-browser.js"))
    if payload is None:
        case_browser.write_bytes(case_browser_source)
    else:
        payload.write(case_browser, case_browser_source)
    studies = research.studies_from(manifest, read)
    reports = manifest["independent_reports"]
    write_json(product_dir / "research-studies.json", {
        "schema_version": manifest["schema_version"], "source_commit": status["source_commit"],
        "studies": studies, "agenda": manifest["agenda"], "independent_reports": reports,
    }, payload)
    archive = research.verifier_archive(read)
    archive_path = product_dir / "verifier-replay.zip"
    if payload is None:
        archive_path.write_bytes(archive)
    else:
        payload.write(archive_path, archive)
    audit = research.audit_replay_archive(manifest, read)
    receiver = research.receiver_replay_archive(manifest, read)
    scoped_git = research.git_replay_archive(manifest, read)
    for name, content in ((research.AUDIT_PACKAGE, audit), (research.RECEIVER_PACKAGE, receiver),
                          (research.GIT_PACKAGE, scoped_git)):
        if payload is None:
            (product_dir / name).write_bytes(content)
        else:
            payload.write(product_dir / name, content)
    replay_links = {}
    for run, package, content in (
        *((identity, research.AUDIT_PACKAGE, audit) for identity in research.AUDIT_REPLAYS),
        (research.RECEIVER_REPLAY_ID, research.RECEIVER_PACKAGE, receiver),
        (research.GIT_REPLAY_ID, research.GIT_PACKAGE, scoped_git),
    ):
        replay_links[run] = (
            f'<p><a href="{package}" download>Download the standalone replay kit</a>. '
            f'Run <code>python3 replay.py {run}</code>. '
            f'Kit SHA-256 <code>{hashlib.sha256(content).hexdigest()}</code>.</p>'
        )

    for run in manifest["runs"]:
        if run["format"] not in {"verification_arrivals", "revision_retrieval"}:
            continue
        members = {name: read(Path(name)) for name in (run["protocol"], run["result"], *run["inputs"])}
        command = run["command"]
        members["README.md"] = (
            f'# {run["title"]}\n\nExtract the archive and run from its root:\n\n'
            f'```sh\n{command} > observation.json\ncmp observation.json {run["result"]}\n```\n\n'
            f'The pinned protocol is {run["protocol"]}. The replay uses local data.\n'
        ).encode()
        package = run["id"] + "-replay.zip"
        content = research.replay_zip(members)
        if payload is None:
            (product_dir / package).write_bytes(content)
        else:
            payload.write(product_dir / package, content)
        replay_links[run["id"]] = (
            f'<p><a href="{package}" download>Download the offline protocol, inputs, replay and results</a>. '
            f'Kit SHA-256 <code>{hashlib.sha256(content).hexdigest()}</code>.</p>'
        )

    for study in studies:
        sections = []
        run_index = []
        for row in study["runs"]:
            result = json.loads(read(Path(row["result"])))
            cases = rows_for(row["format"], result)
            csv_path = product_dir / f'cases-{row["id"]}.csv'
            export = export_csv(row["id"], cases)
            if payload is None:
                csv_path.write_bytes(export)
            else:
                payload.write(csv_path, export)
            sections.append(render_run(study, row, result, cases, featured, replay_links.get(row["id"], "")))
            label = " · featured" if row["id"] == study["featured_run"] else ""
            run_index.append(f'<li><a href="#{research_anchor(row["id"])}">{escape(row["title"])}</a>{label}</li>')
        links = ""
        if study.get("reader_anchor"):
            links += f'<p><a href="../../reader/quickstart.html#{escape(study["reader_anchor"])}">Worked reader comparison</a></p>'
        if study.get("paper"):
            links += f'<p><a href="../../{escape(study["paper"])}">Original paper</a>.</p>'
        if study["id"] == "scoped-git":
            links += (
                '<p><a href="#run-authority-commit-ordering">Inspect the separate authority-ordering check</a>. '
                'Its <a href="../../chapters/system-boundaries-and-authority.html#grant-to-effect-authority">'
                'shared trace</a> follows a grant, an effect and a later observation.</p>'
            )
        if study["id"] == "claim-review":
            links += (
                '<p>On <a href="#run-claim-review-matched--case-c3">the labor question</a> both policies held the claim, '
                'but only the ordinary register supplied the determining citation. Follow the '
                '<a href="knowledge-graph/?node=study%3Averifier-rollout">repaired measurement-boundary route</a> '
                'or inspect the <a href="../../chapters/virtual-context-abi.html#revision-retrieval-study">'
                'reserved-history retrieval comparison</a>.</p>'
            )
        if study.get("spotlight"):
            spot = study["spotlight"]
            target = research_anchor(spot["run"], spot["case"])
            if not any(f'id="{target}"' in section for section in sections):
                raise ValueError(f"study spotlight does not name a case: {target}")
            links += f'<p><a href="#{target}">{escape(spot["label"])}</a>.</p>'
        if study["id"] == "verifier-rollout":
            links += (
                '<p><a href="verifier-replay.zip">Download the original verifier replay</a>. '
                f'Package SHA-256 <code>{hashlib.sha256(archive).hexdigest()}</code>. '
                'The follow-up below supplies the absolute floor and shared-source controls. '
                '<a href="#independent-checks">Report an independent check</a>.</p>'
            )
        links += replay_links.get(study["featured_run"], "")
        claim = study["claim"]
        comparison = forward_transfer_choices(study) if study["id"] == "forward-transfer" else ""
        if study["id"] == "crossed-receiver":
            comparison = receiver_cost_exercise(study)
        body = (
            '<p><a href="index.html">Return to the Evidence Registry</a></p>'
            + current_study_decision(study) + comparison +
            f'<h2>Question</h2><p>{escape(study["question"])}</p>{links}'
            '<h2 id="related-claim">What this evidence bears on</h2>'
            f'<p>{escape(claim["scope"])} '
            f'<a href="../../appendices/C_claim_evidence_matrix.html#{escape(claim["id"])}">Related book claim and support state</a>.</p>'
            f'<h2>What would change the decision</h2><p>{escape(study["change"])}</p>'
            f'<h2 id="run-history">Run history</h2><ul>{"".join(run_index)}</ul>'
            + "".join(sections) + independent_reports(reports, study, status)
            + '<script src="study-case-browser.js" defer></script>'
        )
        write_text(product_dir / research.study_page(study["id"]),
                   page(study["title"], "Run history, case evidence, and citations.", body,
                        "research-studies.json", show_portfolio=False), payload)

    questions = []
    for row in manifest["agenda"]:
        questions.append(
            f'<h2>{escape(row["question"])}</h2><p><strong>Strongest rival.</strong> {escape(row["rival"])}</p>'
            f'<p><strong>Cheapest discriminating test.</strong> {escape(row["test"])}</p>'
            f'<p><strong>Decisions.</strong> {escape(row["decisions"])}</p>'
            f'<p><a href="{research.study_page(row["study"])}">Current study</a> · '
            f'<a href="{research.REPO}/blob/main/{escape(row["backlog"])}">Related backlog record</a></p>'
        )
    write_text(product_dir / "research-agenda.html", page(
        "Active research agenda", "Three questions that can change what the book recommends.",
        '<p><a href="index.html">Return to the Evidence Registry</a></p>' + "".join(questions),
        "research-studies.json", show_portfolio=False,
    ), payload)
    cards = "".join(
        f'<article class="card"><h3><a href="{research.study_page(row["id"])}">{escape(row["title"])}</a></h3>'
        f'<p>{escape(row["disposition"])}</p><p>{escape(row["summary"])}</p>'
        f'<p><a href="{research.study_page(row["id"])}#current-decision">Read the decision and its limits</a></p></article>'
        for row in studies
    )
    return studies, cards


def build_claim_citations(product_dir, inputs, payload):
    def read(name):
        path = ROOT / relative(name)
        return inputs.data[path] if inputs else path.read_bytes()

    citations = list(graph.claim_citations(read))
    sections = []
    for citation in citations:
        for source in (citation["transition"], citation["run"]):
            target = product_dir / "artifacts" / source
            data = read(source)
            if payload is None:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            else:
                payload.write(target, data)
        limits = "".join(f"<li>{escape(limit)}</li>" for limit in citation["limits"])
        related = ""
        if proof := citation.get("proof"):
            anchor = proof["url"].split("#", 1)[1]
            related = (
                f'<aside id="{escape(anchor)}"><h3>Related formal target</h3>'
                f'<p><code>{escape(proof["tag"])}</code> · {escape(proof["proposition"])}</p>'
                f'<p>{escape(proof["limit"])}</p>'
                f'<p>{graph_link("proof_target:" + proof["tag"], "Open the formal target in the graph")}</p></aside>'
            )
        sections.append(
            f'<section id="{escape(citation["id"])}"><h2>{escape(citation["title"])}</h2>'
            f'<p>{escape(citation["proposition"])}</p>'
            f'<p>Recorded support <strong>{escape(citation["state"])}</strong>. '
            f'Relation to the <a href="../../appendices/C_claim_evidence_matrix.html#{escape(citation["parent"])}">'
            f'chapter claim</a> is <code>{escape(citation["relation"])}</code>. '
            f'Effect on parent support <strong>{escape(citation["parent_effect"])}</strong>.</p>'
            f'<p><a href="artifacts/{escape(citation["run"])}">Exact result</a> · '
            f'<a href="artifacts/{escape(citation["transition"])}">Recorded evidence decision</a> · '
            f'{graph_link("transition:" + citation["transition_id"])}</p>'
            f'<h3>Scope and limits</h3><ul>{limits}</ul>'
            f'<p>Result SHA-256 <code>{citation["run_sha256"]}</code></p>{related}</section>'
        )
    write_text(product_dir / "claim-citations.html",
               page("Selected non-core claims", "Cite a bounded proposition, its exact run, and the recorded limits.",
                    "".join(sections), "claim-citations.json"), payload)
    write_json(product_dir / "claim-citations.json", citations, payload)
    return len(citations)


def research_comparisons(product_dir: Path, catalog: dict, payload: ProductPayload | None) -> None:
    records = {row["id"]: row for row in catalog["records"]}
    comparisons = (
        ("receiver-placement", "Choose where a second status lookup runs",
         ("study_run:receiver-availability", "evidence_case:receiver-availability--pair-024",
          "evidence_case:receiver-availability--pair-064", "study_run:receiver-distribution",
          "study_run:receiver-live-transport")),
        ("verifier-freshness", "Separate verifier freshness from cache format",
         ("study_run:verifier-floor-cache", "study_run:verifier-revision-freshness",
          "study_run:verifier-process-boundary")),
        ("scheduler-and-budget", "Choose a reuse representation under the actual work cap",
         ("study_run:transfer-factorial", "study_run:transfer-scheduler-audit",
          "evidence_case:transfer-scheduler-audit--b24-descriptive-proposals-both-reversed")),
        ("baseline-admission", "Check the strongest feasible comparator",
         ("evidence_passage:atlas-corrected-decision", "study_run:git-retrospective")),
    )
    sections = []
    for identity, title, keys in comparisons:
        snippets = []
        for key in keys:
            row = records[key]
            href = safe_rel_link("products/evidence-registry", row["url"])
            snippets.append(f'<h3><a href="{escape(href)}">{escape(row["title"])}</a></h3>'
                            f'<p>{escape(row["summary"])}</p>'
                            f'<p><strong>Scope</strong> {escape(row["limit"])}</p>'
                            f'<p>{graph_link(key)} · <button type="button" data-copy-citation="'
                            f'{escape(row["citation_text"])}">Copy citation</button> <span role="status"></span></p>')
        sections.append(f'<section id="{identity}"><h2>{escape(title)}</h2>{"".join(snippets)}</section>')
    body = ('<p><a href="index.html">Return to the Evidence Registry</a></p>' + "".join(sections)
            + '<script src="knowledge-graph/evidence-citation.js" defer></script>')
    write_text(product_dir / "research-comparisons.html",
               page("Research comparisons", "Read the conditions that changed each decision and open the exact records.",
                    body, "knowledge-graph/evidence-catalog.json", show_portfolio=False), payload)


def reader_resources(directory, status, inputs, payload):
    def read(name):
        path = ROOT / name
        return inputs.data[path] if inputs else path.read_bytes()

    def install(name, data):
        if payload is None:
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        else:
            payload.write(directory / name, data)

    skill = read(READER_SKILL)
    kit = research.replay_zip({"asi-stack-reader/SKILL.md": skill,
                               "asi-stack-reader/agents/openai.yaml": read(READER_UI),
                               "asi-stack-reader/RIGHTS.md": read("LICENSE.md")})
    install("asi-stack-reader.zip", kit)
    install("SKILL.md", skill)
    # This skill uses paragraphs, numbered instructions and Markdown links. Render
    # those directly from the installable source so the two guides stay in sync.
    body = skill.decode().split("---\n", 2)[2].strip().split("\n\n")
    def inline(text):
        return re.sub(r"\[([^\]]+)\]\((https://[^\s)]+)\)", r'<a href="\2">\1</a>', escape(text))
    paragraphs = []
    for block in body[1:]:
        if block.startswith("1. "):
            paragraphs.append("<ol>" + "".join("<li>" + inline(line.partition(". ")[2]) + "</li>"
                                                for line in block.splitlines()) + "</ol>")
        else:
            paragraphs.append("<p>" + inline(block) + "</p>")
    guide = ('<p><a href="asi-stack-reader.zip" download>Download the reader skill</a> · '
             '<a href="SKILL.md">Plain Markdown instructions</a> · '
             '<a href="citation-history.html">Check a saved citation</a></p>'
             '<p>To install, extract the asi-stack-reader folder into the skills directory used by your agent. '
             'A web reader can use the instructions below directly.</p>' + "".join(paragraphs))
    write_text(directory / "reader-skill.html", page("Read The ASI Stack with an agent",
               "Find the deciding passage and cite its limits.", guide, "knowledge-graph/manifest.json",
               show_portfolio=False), payload)

    archive = json.loads(read(CITATION_ARCHIVE))
    install("saved-revisions/" + archive["revision"] + ".json", read(CITATION_ARCHIVE))
    write_json(directory / "citation-current.json", {
        "revision": status["source_commit"], "archived": [archive["revision"]],
        "passages": json.loads(read(graph.PASSAGES)), "studies": json.loads(read(research.RECORDS))}, payload)
    install("citation-history.js", read(CITATION_SCRIPT))
    form = ('<p>Paste the evidence record ID and full book revision from a saved citation. '
            'This comparison covers studies, individual runs and citable passages. The book includes one earlier '
            'snapshot locally and reads other historical revisions from its GitHub repository.</p>'
            '<form id="history-form"><p><label>Record ID <input name="record" required size="38"></label></p>'
            f'<p><label>Saved book revision <input name="revision" value="{archive["revision"]}" required size="44"></label></p>'
            '<button>Compare revisions</button></form><div id="history-output" aria-live="polite"></div>'
            '<noscript>Use the versioned source links in the evidence catalog to compare records manually.</noscript>'
            '<script src="citation-history.js" defer></script>')
    write_text(directory / "citation-history.html", page("What changed since I cited this?",
               "Compare a saved record with the current book.", form, "citation-current.json", show_portfolio=False), payload)


def build_evidence(output: Path, status: dict[str, Any], *, inputs: ProductInputs | None = None,
                   payload: ProductPayload | None = None, companion: dict | None = None,
                   catalog: dict | None = None) -> dict[str, Any]:
    product_dir = output / "evidence-registry"
    if payload is None:
        product_dir.mkdir(parents=True, exist_ok=True)
    reader_resources(product_dir, status, inputs, payload)
    featured_cases = {row["id"] for row in (catalog or {}).get("records", []) if row["kind"] == "evidence_case"}
    studies, study_cards = build_research(product_dir, status, inputs, payload, featured_cases)
    citation_count = build_claim_citations(product_dir, inputs, payload)
    published_groups: list[dict[str, Any]] = []
    for group in EVIDENCE_GROUPS:
        published_entries: list[dict[str, Any]] = []
        for label, target in group["entries"]:
            source = ROOT / relative(target)
            ordinary(source)
            data = inputs.data[source] if inputs else source.read_bytes() if source.is_file() else None
            if data is not None:
                snapshot = product_dir / "artifacts" / target
                if payload is None:
                    snapshot.parent.mkdir(parents=True, exist_ok=True)
                    ordinary(snapshot)
                    snapshot.write_bytes(data)
                else:
                    payload.write(snapshot, data)
                projection_path = (Path("artifacts") / target).as_posix()
                digest = hashlib.sha256(data).hexdigest()
                mode = "content_addressed_snapshot"
            else:
                projection_path = safe_rel_link("products/evidence-registry", target)
                digest = None
                mode = "rendered_site_route"
            published_entries.append({
                "label": label,
                "canonical_path": target,
                "projection_path": projection_path,
                "publication_mode": mode,
                "sha256": digest,
            })
        published_groups.append({
            "id": group["id"],
            "label": group["label"],
            "purpose": group["purpose"],
            "entries": published_entries,
        })
    entry_count = sum(len(group["entries"]) for group in published_groups)
    manifest = {
        "schema_version": "asi_stack.evidence_registry_projection.v0",
        "status": "generated_registry_route_not_independent_evidence",
        "canonical_status_id": status["status_id"],
        "chapter_count": status["counts"]["chapters"],
        "source_count": status["counts"]["sources"],
        "core_claim_distribution": status["claim_state_distribution"]["support_states"],
        "groups": published_groups,
        "studies": [research.study_page(row["id"]) for row in studies],
        "active_research_agenda": "research-agenda.html",
        "claim_citations": {"page": "claim-citations.html", "data": "claim-citations.json", "count": citation_count},
        "non_claims": [
            "Record availability, count, or schema validity does not establish claim truth.",
            "Internal validators are not independent review.",
            "The registry does not promote any chapter-core support state.",
        ],
    }
    companion_intro = ""
    if companion is not None:
        manifest["knowledge_graph"] = {
            "entry_path": "knowledge-graph/index.html",
            "manifest_path": "knowledge-graph/manifest.json",
            "snapshot_id": companion["snapshot_id"],
        }
        companion_intro = (
            '<h2>Browse the book as a knowledge graph</h2>'
            '<p><a href="knowledge-graph/index.html">Open the knowledge graph</a> to follow concepts, claims, and evidence. '
            '<a href="knowledge-graph/manifest.json">Agent manifest</a> · <a href="reader-skill.html">Reader skill</a> · <a href="citation-history.html">Check a saved citation</a>.</p>'
        )
    comparison_link = ""
    if catalog is not None:
        research_comparisons(product_dir, catalog, payload)
        manifest["research_comparisons"] = "research-comparisons.html"
        comparison_link = ' · <a href="research-comparisons.html">Research comparisons</a>'
    sections = []
    for group in published_groups:
        cards = []
        for entry in group["entries"]:
            cards.append(
                f'<article class="card"><h3><a href="{escape(entry["projection_path"])}">{escape(entry["label"])}</a></h3>'
                f'<p class="meta"><code>{escape(entry["canonical_path"])}</code><br>{escape(entry["publication_mode"])}</p></article>'
            )
        sections.append(
            f'<h2>{escape(group["label"])}</h2><p>{escape(group["purpose"])}</p><div class="grid">{"".join(cards)}</div>'
        )
    body = (
        f'<p class="status"><strong>Current status:</strong> {status["counts"]["chapters"]} chapters; '
        f'{status["counts"]["sources"]} public-safe sources; all chapter-core support remains explicitly bounded.</p>'
        '<h2>Research studies and replays</h2>'
        '<p><a href="research-agenda.html">Active research agenda</a> · '
        f'<a href="research-studies.json">Study data and citations</a>{comparison_link}</p>'
        f'<div class="grid">{study_cards}</div>'
        '<h2>Follow a claim into its evidence</h2>'
        '<p><a href="claim-citations.html">Cite a selected non-core claim</a> with its recorded scope and exact result.</p>'
        '<ul><li><strong>Authority at a write.</strong> Read the '
        '<a href="../../appendices/C_claim_evidence_matrix.html#system-boundaries-and-authority.core">authority claim</a>, '
        f'then open the <a href="artifacts/{P5_U1_RESULT}">twelve replay records</a>. '
        'The direct and record-only routes pass the configuration check while admitting an out-of-scope edit. '
        'The governed denial answers a mechanism question. The '
        '<a href="study-scoped-git.html">matched scoped Git run</a> checks the stronger alternative.</li>'
        '<li><strong>Claim custody.</strong> Compare the '
        '<a href="../../appendices/C_claim_evidence_matrix.html#evidence-states-and-claim-discipline.core">support discipline claim</a> '
        'with the <a href="artifacts/claim_decisions/v1_x_core_claim_dispositions.json">recorded core dispositions</a>. '
        'The ledger identifies what was decided. Whether those joins improve independent review remains open.</li>'
        '<li><strong>Observed effect and recovery.</strong> Start with '
        '<a href="../../appendices/C_claim_evidence_matrix.html#artifact-graphs-audit-logs-and-replay.core">the artifact claim</a>. '
        'Follow the <a href="../../chapters/integrated-reference-architecture.html#p5-stateful-service-successor">local service trial</a> '
        'and the <a href="../../reader/quickstart.html#read-the-twelve-outcomes">three compensation paths</a>. '
        'A read of the named target and the retained Git history answer different questions. '
        'Recovery across other services remains open.</li></ul>'
        + companion_intro + "".join(sections)
    )
    write_text(product_dir / "index.html",
        page("Evidence, proof, and release registry", "Structured routes to what is supported, by which artifacts, under which limits, and with which unresolved residuals.", body, "manifest.json"),
        payload,
    )
    manifest["entry_count"] = entry_count
    write_json(product_dir / "manifest.json", manifest, payload)
    return manifest


def prepare_payload(output: Path, inputs: ProductInputs) -> ProductPayload:
    structure = inputs.json(STRUCTURE)
    contracts = inputs.json(CONTRACTS)
    spine = inputs.json(SPINE)
    contribution_data = inputs.json(CONTRIBUTIONS)
    status = inputs.status
    payload = ProductPayload(output)
    canonical = canonical_chapters(structure)
    assignments = {row["chapter_id"]: row for row in contribution_data["chapter_assignments"]}
    narrative = build_narrative(output, canonical, spine, assignments, inputs=inputs, payload=payload)
    reference = build_reference(output, canonical, assignments, payload=payload)
    graph_files = knowledge.prepare(lambda p: inputs.data[ROOT / relative(p)],
                                    source_commit=status["source_commit"],
                                    worktree=status["source_tree_state"] != "clean")
    for name, data in graph_files.items():
        payload.write(output / knowledge.COMPANION_DIR / name, data)
    evidence = build_evidence(output, status, inputs=inputs, payload=payload,
                              companion=json.loads(graph_files["manifest.json"]),
                              catalog=json.loads(graph_files["evidence-catalog.json"]))
    product_rows = [
        {
            "id": "narrative_book",
            "status": narrative["status"],
            "entry_path": "narrative-book/index.html",
            "manifest_path": "narrative-book/manifest.json",
            "entry_count": narrative["selected_chapter_count"],
        },
        {
            "id": "architecture_reference",
            "status": reference["status"],
            "entry_path": "architecture-reference/index.html",
            "manifest_path": "architecture-reference/manifest.json",
            "entry_count": reference["chapter_count"],
        },
        {
            "id": "evidence_registry",
            "status": evidence["status"],
            "entry_path": "evidence-registry/index.html",
            "manifest_path": "evidence-registry/manifest.json",
            "entry_count": evidence["entry_count"],
        },
    ]
    root_manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_from": {
            "canonical_status_id": status["status_id"],
            "source_commit": status["source_commit"],
            "chapter_count": status["counts"]["chapters"],
            "source_count": status["counts"]["sources"],
            "structure_sha256": inputs.digest(STRUCTURE),
            "contract_sha256": inputs.digest(CONTRACTS),
            "narrative_spine_sha256": inputs.digest(SPINE),
            "narrative_unit_crosswalk_sha256": inputs.digest(UNIT_CROSSWALK),
        },
        "products": product_rows,
        "non_claims": [
            "Product projection is not product approval or publication review.",
            "Projection changes navigation and density, not canonical claim support.",
            "The canonical source tree and its evidence records remain authoritative.",
        ],
    }
    write_json(output / "product-projections.json", root_manifest, payload)
    cards = "".join(
        f'<article class="card"><h3><a href="{escape(row["entry_path"])}">{escape(next(p["label"] for p in contracts["products"] if p["id"] == row["id"]))}</a></h3>'
        f'<p class="meta">{row["entry_count"]} indexed entries · {escape(row["status"])}</p></article>'
        for row in product_rows
    )
    root_body = '<p class="status">Three generated routes, one canonical source tree. Availability is separate from review and release approval.</p><div class="grid">' + cards + '</div>'
    # Root page needs one fewer parent traversal than the product-specific template.
    root_html = page("Choose the product you need", "Narrative reading, architecture lookup, and evidence audit are separate questions with separate density and review contracts.", root_body, "product-projections.json")
    root_html = root_html.replace('href="../../index.html"', 'href="../index.html"').replace('href="../index.html">Three products</a>', '').replace('href="../../docs/', 'href="../docs/')
    write_text(output / "index.html", root_html, payload)
    validate_payload(payload, inputs)
    return payload


def validate_payload(payload: ProductPayload, inputs: ProductInputs) -> None:
    # Keep the existing domain consumers; byte preparation is not acceptance.
    from validate_product_projections import narrative_projection_errors, narrative_routing_errors, reference_responsibility_errors
    def load(name):
        return json.loads(payload.files[name])
    root = load("product-projections.json")
    narrative = load("narrative-book/manifest.json")
    reference = load("architecture-reference/manifest.json")
    evidence = load("evidence-registry/manifest.json")
    canonical = canonical_chapters(inputs.json(STRUCTURE))
    errors = status_builder.validate_against_schema(root, inputs.json(PROJECTION_SCHEMA), "product projection")
    errors += status_builder.validate_against_schema(inputs.json(SPINE), inputs.json(SPINE_SCHEMA), "narrative spine")
    errors += narrative_projection_errors(inputs.json(SPINE))
    errors += narrative_routing_errors(narrative, inputs.json(UNIT_CROSSWALK)["units"], canonical,
                                       payload.files["narrative-book/index.html"].decode())
    errors += reference_responsibility_errors(reference, canonical, payload.files["architecture-reference/index.html"].decode())
    expected_binding = {"canonical_status_id": inputs.status["status_id"], "source_commit": inputs.status["source_commit"],
                        "chapter_count": len(canonical), "source_count": inputs.status["counts"]["sources"],
                        "structure_sha256": inputs.digest(STRUCTURE), "contract_sha256": inputs.digest(CONTRACTS),
                        "narrative_spine_sha256": inputs.digest(SPINE), "narrative_unit_crosswalk_sha256": inputs.digest(UNIT_CROSSWALK)}
    if root["generated_from"] != expected_binding:
        errors.append("prepared product binding differs from inspected status/source bytes")
    expected_products = {"narrative_book": ("narrative-book", narrative, narrative["selected_chapter_count"]),
                         "architecture_reference": ("architecture-reference", reference, reference["chapter_count"]),
                         "evidence_registry": ("evidence-registry", evidence, evidence["entry_count"])}
    if len(root["products"]) != 3 or {row["id"] for row in root["products"]} != set(expected_products):
        errors.append("prepared product IDs are incomplete or duplicated")
    for row in root["products"]:
        if row["id"] in expected_products:
            directory, manifest, count = expected_products[row["id"]]
            if row != {"id": row["id"], "status": manifest["status"], "entry_path": directory + "/index.html",
                       "manifest_path": directory + "/manifest.json", "entry_count": count}:
                errors.append("prepared product route/count disagrees with its owning manifest")
    current = inputs.json(CURRENT_READER)
    if (narrative["current_reader"]["unit_count"] != current["unit_count"]
            or narrative["current_reader"]["owner_route_count"] != current["owner_route_count"]
            or narrative["current_reader"]["manifest_sha256"] != inputs.digest(CURRENT_READER)
            or narrative["custody_mode"] != "historical_candidate_navigation"):
        errors.append("prepared narrative lost current-reader or historical-candidate custody")
    if (len(narrative["chapters"]) != narrative["selected_chapter_count"] or narrative["canonical_chapter_count"] != len(canonical)
            or evidence["chapter_count"] != len(canonical) or evidence["source_count"] != inputs.status["counts"]["sources"]
            or reference["chapter_count"] != len(canonical)):
        errors.append("prepared product counts contradict canonical ownership/status")
    if evidence["entry_count"] != sum(len(group["entries"]) for group in evidence["groups"]):
        errors.append("prepared evidence denominator differs from its entries")
    for group in evidence["groups"]:
        for entry in group["entries"]:
            if entry["publication_mode"] == "content_addressed_snapshot":
                data = payload.files["evidence-registry/" + relative(entry["projection_path"])]
                if hashlib.sha256(data).hexdigest() != entry["sha256"] or data != inputs.data[ROOT / entry["canonical_path"]]:
                    errors.append("prepared evidence snapshot differs from inspected source")
    for row in root["products"]:
        if row["entry_path"] not in payload.files or row["manifest_path"] not in payload.files:
            errors.append("prepared product route is missing")
    if errors:
        raise ValueError("; ".join(errors[:8]))


def build_products(output: Path, status_path: Path | None = None, *, check: bool = False) -> dict:
    ordinary(output)
    output = output.resolve()
    if not check and output != (ROOT / "_site/products").resolve() and not output.is_relative_to((ROOT / "build").resolve()):
        raise ValueError("product installation requires _site/products or an ignored build output")
    inputs = ProductInputs(status_path)
    for path in inputs.data:
        source = path.resolve()
        if source == output or output in source.parents or source in output.parents:
            raise ValueError("product output and inspected inputs must not overlap")
    payload = prepare_payload(output, inputs)
    # Products inside a rendered site share the reader/channel writer's lock.
    lock_root = output.parent if output.name == "products" and (output.parent / "status/canonical-public-status.json").is_file() else output
    return install_directory(output, family="product_projections", payload=payload.files, inputs=inputs.identity,
                             guard=inputs.guard, check=check, lock_root=lock_root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status", type=Path, help="canonical status file; defaults to a fresh local status build")
    parser.add_argument("--check", action="store_true", help="Check complete current bytes without writing or staging")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    status_path = args.status if args.status is None or args.status.is_absolute() else ROOT / args.status
    try:
        print(f"{'Checking' if args.check else 'Preparing complete replacement for'} product output: {output}", flush=True)
        record = build_products(output, status_path, check=args.check)
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise SystemExit(f"Product projection refused: {error}") from error
    print(f"{'Checked' if args.check else 'Installed'} complete product projection: {len(record['files'])} files; support/release effects none.")


if __name__ == "__main__":
    from admission_guard import canonical_access
    try:
        with canonical_access(ROOT):
            main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Product projection refused: {error}")
