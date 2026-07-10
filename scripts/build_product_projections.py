#!/usr/bin/env python3
"""Build concrete narrative, architecture-reference, and evidence-registry routes."""

from __future__ import annotations

import argparse
from html import escape
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from build_canonical_public_status import ROOT, build_status, load_json


STRUCTURE = ROOT / "book_structure.json"
CONTRACTS = ROOT / "products" / "product_contracts.json"
SPINE = ROOT / "products" / "narrative_product_spine.json"
CONTRIBUTIONS = ROOT / "products" / "contribution_focus_contract.json"
DEFAULT_OUTPUT = ROOT / "build" / "product_projections"
MANIFEST_SCHEMA_VERSION = "asi_stack.product_projection_manifest.v0"

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


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
{body}
</main></body></html>
"""


def build_narrative(
    output: Path,
    canonical: list[dict[str, Any]],
    spine: dict[str, Any],
    contributions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    by_id = {row["chapter_id"]: row for row in canonical}
    selected: list[dict[str, Any]] = []
    for record in spine["chapters"]:
        row = dict(by_id[record["chapter_id"]])
        row.update(record)
        assignment = contributions.get(row["chapter_id"], {})
        row["contribution_id"] = assignment.get("contribution_id")
        selected.append(row)
    selected_ids = {row["chapter_id"] for row in selected}
    selected_orders = [row["order"] for row in selected]
    omitted: list[dict[str, Any]] = []
    for row in canonical:
        if row["chapter_id"] in selected_ids:
            continue
        nearest = min(selected, key=lambda owner: (abs(owner["order"] - row["order"]), owner["order"]))
        omitted.append({
            "chapter_id": row["chapter_id"],
            "title": row["title"],
            "canonical_order": row["order"],
            "architecture_reference_path": row["public_path"],
            "nearest_narrative_owner": nearest["chapter_id"],
        })
    manifest = {
        "schema_version": "asi_stack.narrative_product_projection.v0",
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
    write_json(product_dir / "manifest.json", manifest)
    cards = []
    for row in selected:
        link = safe_rel_link("products/narrative-book", row["public_path"]) + "?view=human"
        cards.append(
            f'<article class="card"><div class="meta">{row["order"]} · <code>{escape(row["core_claim_ref"])}</code></div>'
            f'<h3><a href="{escape(link)}">{escape(row["title"])}</a></h3>'
            f'<p><strong>Question:</strong> {escape(row["reader_question"])}</p>'
            f'<p class="meta"><strong>Running example:</strong> {escape(row["running_example"])}</p></article>'
        )
    body = (
        '<p class="status"><strong>Status:</strong> generated fifteen-chapter candidate route. '
        'It is not a reviewed reader release, and the other canonical chapters remain in the architecture reference.</p>'
        '<h2>Thesis-to-method route</h2><div class="grid">' + "".join(cards) + '</div>'
        f'<h2>Reference routing</h2><p>{len(omitted)} specialized chapters remain discoverable in the architecture reference; none was deleted or demoted.</p>'
    )
    (product_dir / "index.html").write_text(
        page("Narrative technical book", "A bounded thesis-to-method reading route with the live research scaffold hidden in Human view.", body, "manifest.json"),
        encoding="utf-8",
    )
    return manifest


def build_reference(
    output: Path,
    canonical: list[dict[str, Any]],
    contributions: dict[str, dict[str, Any]],
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
    write_json(product_dir / "manifest.json", manifest)
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
                f'<p class="meta"><code>{escape(row["core_claim_ref"])}</code><br>{escape(str(row.get("contribution_id") or ""))}</p></article>'
            )
        sections.append(f"<h2>{escape(part)}</h2><div class=\"grid\">{''.join(cards)}</div>")
    body = (
        '<p class="status"><strong>Status:</strong> complete generated lookup index over every canonical chapter. '
        'It is a specification route, not evidence of a deployed stack.</p>' + "".join(sections)
    )
    (product_dir / "index.html").write_text(
        page("Architecture reference specification", "All responsibilities, interfaces, invariants, failure routes, implementation horizons, and technical chapters in canonical order.", body, "manifest.json"),
        encoding="utf-8",
    )
    return manifest


def build_evidence(output: Path, status: dict[str, Any]) -> dict[str, Any]:
    product_dir = output / "evidence-registry"
    published_groups: list[dict[str, Any]] = []
    for group in EVIDENCE_GROUPS:
        published_entries: list[dict[str, Any]] = []
        for label, target in group["entries"]:
            source = ROOT / target
            if source.is_file():
                snapshot = product_dir / "artifacts" / target
                snapshot.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, snapshot)
                projection_path = (Path("artifacts") / target).as_posix()
                digest = sha256_file(source)
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
    write_json(product_dir / "manifest.json", manifest)
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
    (product_dir / "index.html").write_text(
        page("Evidence, proof, and release registry", "Structured routes to what is supported, by which artifacts, under which limits, and with which unresolved residuals.", body, "manifest.json"),
        encoding="utf-8",
    )
    manifest["entry_count"] = entry_count
    write_json(product_dir / "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status", type=Path, help="canonical status file; defaults to a fresh local status build")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    status_path = (
        args.status if args.status is not None and args.status.is_absolute()
        else ROOT / args.status if args.status is not None
        else None
    )
    required_inputs = [STRUCTURE, CONTRACTS, SPINE, CONTRIBUTIONS]
    if status_path is not None:
        required_inputs.append(status_path)
    for path in required_inputs:
        if not path.exists():
            raise SystemExit(f"missing product-projection input: {path}")
    structure = load_json(STRUCTURE)
    contracts = load_json(CONTRACTS)
    spine = load_json(SPINE)
    contribution_data = load_json(CONTRIBUTIONS)
    status = load_json(status_path) if status_path is not None else build_status()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    canonical = canonical_chapters(structure)
    assignments = {row["chapter_id"]: row for row in contribution_data["chapter_assignments"]}
    narrative = build_narrative(output, canonical, spine, assignments)
    reference = build_reference(output, canonical, assignments)
    evidence = build_evidence(output, status)
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
            "structure_sha256": sha256_file(STRUCTURE),
            "contract_sha256": sha256_file(CONTRACTS),
            "narrative_spine_sha256": sha256_file(SPINE),
        },
        "products": product_rows,
        "non_claims": [
            "Product projection is not product approval or publication review.",
            "Projection changes navigation and density, not canonical claim support.",
            "The canonical source tree and its evidence records remain authoritative.",
        ],
    }
    write_json(output / "product-projections.json", root_manifest)
    cards = "".join(
        f'<article class="card"><h3><a href="{escape(row["entry_path"])}">{escape(next(p["label"] for p in contracts["products"] if p["id"] == row["id"]))}</a></h3>'
        f'<p class="meta">{row["entry_count"]} indexed entries · {escape(row["status"])}</p></article>'
        for row in product_rows
    )
    root_body = '<p class="status">Three generated routes, one canonical source tree. Availability is separate from review and release approval.</p><div class="grid">' + cards + '</div>'
    # Root page needs one fewer parent traversal than the product-specific template.
    root_html = page("Choose the product you need", "Narrative reading, architecture lookup, and evidence audit are separate questions with separate density and review contracts.", root_body, "product-projections.json")
    root_html = root_html.replace('href="../../index.html"', 'href="../index.html"').replace('href="../index.html">Three products</a>', '')
    (output / "index.html").write_text(root_html, encoding="utf-8")
    print(
        f"Built product projections: {narrative['selected_chapter_count']} narrative chapters, "
        f"{reference['chapter_count']} reference chapters, {evidence['entry_count']} evidence routes."
    )


if __name__ == "__main__":
    main()
