#!/usr/bin/env python3
"""Build concrete narrative, architecture-reference, and evidence-registry routes."""

from __future__ import annotations

import argparse
from html import escape
import hashlib
import json
from pathlib import Path
from typing import Any

import build_canonical_public_status as status_builder
from build_canonical_public_status import ROOT, build_status, load_json
from generated_directory import install as install_directory, ordinary, relative
from projection_files import ProjectionFiles


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
        for path in required:
            self.capture(path)
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


def page(title: str, subtitle: str, body: str, manifest_link: str) -> str:
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
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:1rem; }}
.card {{ border:1px solid var(--rule); border-radius:.6rem; padding:1rem; }} .card h3 {{ margin:.1rem 0 .55rem; }}
.meta {{ color:var(--muted); font-size:.92rem; }} nav {{ display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:2rem; }}
code {{ overflow-wrap:anywhere; }}
</style>
</head>
<body><main>
<nav><a href="../../index.html">Book home</a><a href="../index.html">Three products</a><a href="{escape(manifest_link)}">Machine manifest</a></nav>
<div class="eyebrow">Product projection</div>
<h1>{escape(title)}</h1>
<p class="lead">{escape(subtitle)}</p>
<p>Three proposed contributions organize all three products: <strong>governed-cognition interface contracts</strong>, <strong>public claim-state transition discipline</strong>, and <strong>record/reality reconciliation with residual honesty</strong>. The 89 technical chapters support composition and process proposals with bounded local implementation results. Selection establishes neither novelty nor chapter-core support. Read the <a href="../../docs/three_defended_contributions.md">contribution summary</a> and <a href="../../docs/defended_contribution_prior_art_positioning.md">competent conventional alternatives</a>.</p>
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
        'HTML is available; the manuscript remains ready for author review. '
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


def build_evidence(output: Path, status: dict[str, Any], *, inputs: ProductInputs | None = None,
                   payload: ProductPayload | None = None) -> dict[str, Any]:
    product_dir = output / "evidence-registry"
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
        "non_claims": [
            "Record availability, count, or schema validity does not establish claim truth.",
            "Internal validators are not independent review.",
            "The registry does not promote any chapter-core support state.",
        ],
    }
    write_json(product_dir / "manifest.json", manifest, payload)
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
        + "".join(sections)
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
    evidence = build_evidence(output, status, inputs=inputs, payload=payload)
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
