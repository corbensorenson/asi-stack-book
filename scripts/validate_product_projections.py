#!/usr/bin/env python3
"""Validate the executable three-product projections and their negative controls."""

from __future__ import annotations

import argparse
from collections import defaultdict
import copy
import gzip
import hashlib
from html import escape, unescape
import json
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlsplit

import research_studies as research
import book_knowledge_graph as graph
import build_knowledge_graph_companion as knowledge
import validate_book_knowledge_graph as graph_checks
from research_case_rows import anchor as research_anchor, export_csv, rows_for
from build_canonical_public_status import ROOT, build_status, validate_against_schema
from build_product_projections import (
    CONTRACTS,
    CONTRIBUTIONS,
    MANIFEST_SCHEMA_VERSION,
    SPINE,
    STRUCTURE,
    UNIT_CROSSWALK,
    build_evidence,
    build_narrative,
    build_reference,
    canonical_chapters,
    sha256_file,
    write_json,
    build_products,
)
from build_reader_edition import (
    filter_structure_for_narrative_spine,
    generate as generate_reader,
    load_narrative_spine,
)


SPINE_SCHEMA = ROOT / "schemas" / "narrative_product_spine.schema.json"
PROJECTION_SCHEMA = ROOT / "schemas" / "product_projection_manifest.schema.json"
DOC = ROOT / "docs" / "product_projection_artifacts.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_into(output: Path, status: dict) -> None:
    structure = load(STRUCTURE)
    spine = load(SPINE)
    contribution_data = load(CONTRIBUTIONS)
    canonical = canonical_chapters(structure)
    assignments = {row["chapter_id"]: row for row in contribution_data["chapter_assignments"]}
    narrative = build_narrative(output, canonical, spine, assignments)
    reference = build_reference(output, canonical, assignments)
    evidence = build_evidence(output, status)
    root = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_from": {
            "canonical_status_id": status["status_id"],
            "source_commit": status["source_commit"],
            "chapter_count": status["counts"]["chapters"],
            "source_count": status["counts"]["sources"],
            "structure_sha256": sha256_file(STRUCTURE),
            "contract_sha256": sha256_file(CONTRACTS),
            "narrative_spine_sha256": sha256_file(SPINE),
            "narrative_unit_crosswalk_sha256": sha256_file(UNIT_CROSSWALK),
        },
        "products": [
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
        ],
        "non_claims": [
            "Product projection is not product approval or publication review.",
            "Projection changes navigation and density, not canonical claim support.",
            "The canonical source tree and its evidence records remain authoritative.",
        ],
    }
    write_json(output / "product-projections.json", root)


def snapshot_errors(output: Path, evidence: dict) -> list[str]:
    errors: list[str] = []
    for group in evidence.get("groups", []):
        for entry in group.get("entries", []):
            if entry.get("publication_mode") != "content_addressed_snapshot":
                continue
            path = output / "evidence-registry" / entry["projection_path"]
            if not path.is_file():
                errors.append(f"missing evidence snapshot {entry['projection_path']}")
            elif sha256(path) != entry.get("sha256"):
                errors.append(f"evidence snapshot digest mismatch {entry['projection_path']}")
            canonical = ROOT / str(entry.get("canonical_path", ""))
            if canonical.is_file() and sha256(canonical) != entry.get("sha256"):
                errors.append(f"evidence snapshot is stale against canonical source {entry['canonical_path']}")
    return errors


def research_projection_errors(output: Path, source_commit: str, site: Path | None = None) -> list[str]:
    def read(path):
        return (ROOT / path).read_bytes()

    registry = output / "evidence-registry"
    manifest = json.loads(read(research.RECORDS))
    studies = research.studies_from(manifest, read)
    paths = {
        "research-studies.json": json.dumps({
            "schema_version": manifest["schema_version"], "source_commit": source_commit,
            "studies": studies, "agenda": manifest["agenda"], "independent_reports": manifest["independent_reports"],
        }, indent=2, ensure_ascii=False).encode() + b"\n",
        "verifier-replay.zip": research.verifier_archive(read),
        "study-case-browser.js": read(Path("assets/study-case-browser.js")),
        research.AUDIT_PACKAGE: research.audit_replay_archive(manifest, read),
        research.RECEIVER_PACKAGE: research.receiver_replay_archive(manifest, read),
        research.GIT_PACKAGE: research.git_replay_archive(manifest, read),
    }
    case_rows = {
        run["id"]: rows_for(run["format"], json.loads(read(Path(run["result"]))))
        for study in studies for run in study["runs"]
    }
    paths.update({f"cases-{run_id}.csv": export_csv(run_id, rows) for run_id, rows in case_rows.items()})
    errors = [
        f"research projection is missing or stale: {name}" for name, expected in paths.items()
        if not (registry / name).is_file() or (registry / name).read_bytes() != expected
    ]
    citations = list(graph.claim_citations(read))
    citation_page = registry / "claim-citations.html"
    citation_data = registry / "claim-citations.json"
    if not citation_page.is_file() or not citation_data.is_file() or load(citation_data) != citations:
        errors.append("non-core citation data differs from the retained evidence decisions")
    else:
        html = citation_page.read_text()
        for citation in citations:
            identity = citation["id"]
            record = html.partition(f'<section id="{identity}">')[2].partition("</section>")[0]
            if (escape(citation["proposition"]) not in record
                    or any(escape(limit) not in record for limit in citation["limits"])
                    or f'#{citation["parent"]}' not in record):
                errors.append(f"non-core citation lost proposition, parent, or scope: {identity}")
            for name in (citation["run"], citation["transition"]):
                snapshot = registry / "artifacts" / name
                if (f'href="artifacts/{name}"' not in record or not snapshot.is_file()
                        or snapshot.read_bytes() != read(name)):
                    errors.append(f"non-core citation target differs from its retained bytes: {name}")
    first = research.excerpt(studies, research.SITE_REGISTRY, home=True)
    reader = research.excerpt(studies, research.PUBLIC_REGISTRY, home=False)
    for name, data in [(research.HOME_EXCERPT, first), (research.READER_EXCERPT, reader)]:
        if read(name) != data.encode():
            errors.append(f"shared research excerpt is stale: {name}")

    index = (registry / "index.html").read_text()
    agenda = registry / "research-agenda.html"
    if "is the open comparison" in index or not agenda.is_file() or 'href="research-agenda.html"' not in index:
        errors.append("research registry lost its current agenda or retained a stale baseline")
    elif any(escape(row["question"]) not in agenda.read_text() for row in manifest["agenda"]):
        errors.append("active agenda lost a research question")
    for study in studies:
        name = research.study_page(study["id"])
        page = registry / name
        page_html = page.read_text() if page.is_file() else ""
        if (f'href="{name}"' not in index or escape(study["summary"]) not in index
                or escape(study["summary"]) not in page_html or study["result_sha256"] not in page_html):
            errors.append(f"study page or registry summary is missing or stale: {name}")
        if ('src="study-case-browser.js"' not in page_html
                or page_html.count("<details data-study-cases open>") != len(study["runs"])):
            errors.append(f"case view lost its disclosure or filter: {name}")
        decision = page_html.partition('<section id="current-decision">')[2].partition("</section>")[0]
        featured = research_anchor(study["featured_run"])
        if (any(escape(study[key]) not in decision for key in ("disposition", "summary", "limit"))
                or f'href="#{featured}"' not in decision
                or not (0 <= page_html.find('id="current-decision"') < page_html.find('id="run-history"'))):
            errors.append(f"featured decision, evidence limit, or run link is stale: {name}")
        claim = study["claim"]["id"]
        claim_route = f"appendices/C_claim_evidence_matrix.html#{claim}"
        if f'href="../../{claim_route}"' not in page_html:
            errors.append(f"missing scoped claim route: {name}")
        for run in study["runs"]:
            run_fragment = research_anchor(run["id"])
            run_text = f'id="{run_fragment}"'
            amount = page_html.count(run_text)
            if amount != 1 or run["result_sha256"] not in page_html:
                errors.append(f"missing or duplicate pinned run: {run['id']}")
            starts = [
                page_html.find(f'id="{research_anchor(run["id"], row["id"])}"')
                for row in case_rows[run["id"]]
            ]
            if any(start < 0 for start in starts) or starts != sorted(set(starts)):
                errors.append(f"missing or unordered paired cases: {run['id']}")
            for position, row in zip(starts, case_rows[run["id"]], strict=True):
                opening = page_html[position:page_html.find(">", position)]
                if any((f" data-{key}" in opening) != row[key] for key in ("disagrees", "exhausted", "adverse")):
                    errors.append(f"case filter tags differ from retained outcomes: {run['id']} {row['id']}")
            if f'href="cases-{run["id"]}.csv"' not in page_html:
                errors.append(f"study page lacks its paired export: {run['id']}")
            kit = (research.AUDIT_PACKAGE if run["id"] in research.AUDIT_REPLAYS
                   else research.RECEIVER_PACKAGE if run["id"] == research.RECEIVER_REPLAY_ID else None)
            fragment_html = page_html.partition(f'<section {run_text}>')[2].partition("</section>")[0]
            if kit and (f'href="{kit}"' not in fragment_html or f'python3 replay.py {run["id"]}' not in fragment_html):
                errors.append(f"standalone replay kit or command is missing: {run['id']}")
        if study["id"] == "verifier-rollout":
            if ('id="independent-checks"' not in page_html
                    or f'/{source_commit}/{research.REPORT_TEMPLATE.as_posix()}' not in page_html):
                errors.append("verifier page lost its independent review route")
        if site is not None:
            matrix = site / "appendices/C_claim_evidence_matrix.html"
            if not matrix.is_file() or f'id="{claim}"' not in matrix.read_text():
                errors.append(f"scoped claim anchor is absent from Appendix C: {claim}")
            surfaces = [(site / "reader/quickstart.html", research.PUBLIC_REGISTRY)]
            if study["id"] != "forward-transfer":
                surfaces.append((site / "index.html", research.SITE_REGISTRY))
            for target, prefix in surfaces:
                if not target.is_file():
                    errors.append(f"rendered research surface missing: {target.relative_to(site)}")
                    continue
                html = " ".join(target.read_text().split())
                if f'href="{prefix}/{name}"' not in html or escape(study["summary"]) not in html:
                    errors.append(f"rendered research summary missing or stale: {target.relative_to(site)} for {name}")
            if study.get("paper"):
                paper = site / study["paper"]
                if not paper.is_file() or f'href="{research.PUBLIC_REGISTRY}/{name}"' not in paper.read_text():
                    errors.append(f"rendered paper lost its study link: {study['paper']}")
    return errors


def run_history_controls() -> list[str]:
    manifest = load(ROOT / research.RECORDS)
    earlier = next(row for row in manifest["runs"] if row["format"] == "transfer_pilot_v1")
    original = (ROOT / earlier["result"]).read_bytes()
    result = json.loads(original)
    for row in result["tasks"]:
        outcomes = row["outcomes"]
        if outcomes["ordinary_retrieval"]["terminal"] == "verified":
            outcomes["reusable_routines"] = copy.deepcopy(outcomes["ordinary_retrieval"])
    routine = result["totals"]["reusable_routines"]
    won = sum(row["outcomes"]["reusable_routines"]["terminal"] == "verified" for row in result["tasks"])
    routine["verified"] = won
    routine["budget_exhausted"] = len(result["tasks"]) - won
    test_result = json.dumps(result).encode()
    added = {
        **earlier, "id": "control-later-run", "result": "control-later.json",
        "result_sha256": hashlib.sha256(test_result).hexdigest(), "result_summary": "Routines verified {routines}.",
    }
    manifest["runs"].append(added)
    study = next(row for row in manifest["studies"] if row["id"] == earlier["study"])
    study["featured_run"] = added["id"]

    def read(path):
        return test_result if path.name == added["result"] else (ROOT / path).read_bytes()

    candidate = next(row for row in research.studies_from(manifest, read) if row["id"] == study["id"])
    errors = []
    if (candidate["metrics"]["routines"] <= candidate["metrics"]["retrieval"]
            or not any(row["result_sha256"] == earlier["result_sha256"] for row in candidate["runs"])):
        errors.append("run history cannot accept changed results while preserving the earlier citation")
    try:
        research.studies_from(manifest, lambda path: original + b" " if path.as_posix() == earlier["result"] else read(path))
    except ValueError as exc:
        if "pinned run bytes changed" not in str(exc):
            errors.append(f"run history rejected a mutation for the wrong reason: {exc}")
    else:
        errors.append("run history accepted changed bytes under an earlier citation")
    return errors


def narrative_projection_errors(spine: dict) -> list[str]:
    errors: list[str] = []
    projection_fields = (
        "plain_language_thesis",
        "normative_engineering_rule",
        "machine_contract",
    )
    for record in spine.get("chapters", []):
        for field in projection_fields:
            if len(str(record.get(field, "")).strip()) < (64 if field == "machine_contract" else 48):
                errors.append(f"{record.get('chapter_id')}: missing bounded narrative projection {field}")
        machine_contract = str(record.get("machine_contract", "")).lower()
        if "does not" not in machine_contract and "no " not in machine_contract:
            errors.append(f"{record.get('chapter_id')}: machine contract lacks an explicit noninheritance boundary")
    return errors


def narrative_routing_errors(
    narrative: dict,
    units: list[dict],
    canonical: list[dict],
    html_text: str,
) -> list[str]:
    """Require every specialist owner to be visible under its narrative unit."""
    errors: list[str] = []
    canonical_by_id = {row["chapter_id"]: row for row in canonical}
    unit_by_representative = {
        unit["representative_chapter_id"]: unit
        for unit in units
    }
    unit_by_chapter = {
        chapter_id: unit
        for unit in units
        for chapter_id in unit.get("chapter_ids", [])
    }
    selected = narrative.get("chapters", [])
    routed_ids: list[str] = []
    for row in selected:
        chapter_id = row.get("chapter_id")
        unit = unit_by_representative.get(chapter_id)
        if unit is None:
            errors.append(f"{chapter_id}: narrative representative has no unit")
            continue
        if row.get("unit_id") != unit.get("unit_id") or row.get("unit_label") != unit.get("label"):
            errors.append(f"{chapter_id}: narrative unit metadata does not match the crosswalk")
        expected_ids = [
            owner_id
            for owner_id in unit.get("chapter_ids", [])
            if owner_id != chapter_id
        ]
        owners = row.get("reference_owners", [])
        owner_ids = [owner.get("chapter_id") for owner in owners]
        if row.get("reference_owner_count") != len(expected_ids):
            errors.append(f"{chapter_id}: specialist-owner count does not match the crosswalk")
        if owner_ids != expected_ids:
            errors.append(f"{chapter_id}: specialist-owner routes do not match crosswalk order")
        routed_ids.extend(owner_ids)
        for owner in owners:
            owner_id = owner.get("chapter_id")
            canonical_owner = canonical_by_id.get(owner_id)
            if canonical_owner is None:
                errors.append(f"{chapter_id}: unknown specialist owner {owner_id!r}")
                continue
            expected_record = {
                "chapter_id": owner_id,
                "title": canonical_owner["title"],
                "canonical_order": canonical_owner["order"],
                "core_claim_ref": canonical_owner["core_claim_ref"],
                "distinct_responsibility": canonical_owner["core_claim"],
                "claim_label": canonical_owner["claim_label"],
                "support_state": canonical_owner["support_state"],
                "architecture_reference_path": canonical_owner["public_path"],
            }
            if owner != expected_record:
                errors.append(f"{chapter_id}: specialist owner {owner_id} is stale against canonical metadata")
            if canonical_owner["title"] not in html_text:
                errors.append(f"{chapter_id}: specialist owner {owner_id} is hidden from the narrative page")
            if escape(canonical_owner["core_claim"]) not in html_text:
                errors.append(f"{chapter_id}: specialist owner {owner_id} lacks a visible distinct responsibility")
            if f'{canonical_owner["public_path"]}?view=human' not in html_text:
                errors.append(f"{chapter_id}: specialist owner {owner_id} lacks a direct Human-view route")

    expected_routed_ids = [
        chapter_id
        for unit in units
        for chapter_id in unit.get("chapter_ids", [])
        if chapter_id != unit.get("representative_chapter_id")
    ]
    if routed_ids != expected_routed_ids:
        errors.append("narrative product does not visibly route every specialist owner exactly once")
    if len(routed_ids) != len(set(routed_ids)):
        errors.append("narrative product visibly routes a specialist owner more than once")

    omitted = narrative.get("reference_only_chapters", [])
    omitted_by_id = {row.get("chapter_id"): row for row in omitted}
    if set(omitted_by_id) != set(expected_routed_ids):
        errors.append("reference-only chapter index does not match visible specialist-owner routing")
    for chapter_id in expected_routed_ids:
        row = omitted_by_id.get(chapter_id)
        unit = unit_by_chapter.get(chapter_id)
        if row is None or unit is None:
            continue
        representative = unit.get("representative_chapter_id")
        if (
            row.get("nearest_narrative_owner") != representative
            or row.get("unit_id") != unit.get("unit_id")
            or row.get("unit_label") != unit.get("label")
        ):
            errors.append(f"{chapter_id}: reference-only unit route does not match the crosswalk")
    return errors


def reference_responsibility_errors(
    reference: dict,
    canonical: list[dict],
    html_text: str,
) -> list[str]:
    """Require the complete reference to expose canonical responsibility and support."""
    errors: list[str] = []
    rows = reference.get("chapters", [])
    if len(rows) != len(canonical):
        return ["architecture reference responsibility denominator does not match canonical chapters"]
    fields = ("chapter_id", "title", "core_claim_ref", "core_claim", "claim_label", "support_state")
    for row, expected in zip(rows, canonical):
        for field in fields:
            if row.get(field) != expected.get(field):
                errors.append(f"{expected['chapter_id']}: architecture reference has stale {field}")
        if escape(expected["core_claim"]) not in html_text:
            errors.append(f"{expected['chapter_id']}: architecture reference hides its distinct responsibility")
        if expected["support_state"] not in html_text:
            errors.append(f"{expected['chapter_id']}: architecture reference hides its support state")
    return errors


def validate_rendered_site(site: Path, projection_schema: dict) -> list[str]:
    errors: list[str] = []
    products = site / "products"
    status_path = site / "status" / "canonical-public-status.json"
    root_path = products / "product-projections.json"
    if not status_path.is_file() or not root_path.is_file():
        return ["rendered site is missing canonical status or product-projections manifest"]
    try:
        build_products(products, status_path, check=True)
    except (ValueError, OSError, KeyError, TypeError) as error:
        errors.append(f"installed product byte/input integrity failed: {error}")
    status = load(status_path)
    root_manifest = load(root_path)
    errors.extend(validate_against_schema(root_manifest, projection_schema, "rendered product-projections.json"))
    generated = root_manifest.get("generated_from", {})
    expected_binding = {
        "canonical_status_id": status.get("status_id"),
        "source_commit": status.get("source_commit"),
        "chapter_count": status.get("counts", {}).get("chapters"),
        "source_count": status.get("counts", {}).get("sources"),
        "structure_sha256": sha256_file(STRUCTURE),
        "contract_sha256": sha256_file(CONTRACTS),
        "narrative_spine_sha256": sha256_file(SPINE),
        "narrative_unit_crosswalk_sha256": sha256_file(UNIT_CROSSWALK),
    }
    if generated != expected_binding:
        errors.append("rendered product projection is not bound to canonical status and current source digests")
    for row in root_manifest.get("products", []):
        for field in ("entry_path", "manifest_path"):
            target = products / str(row.get(field, ""))
            if not target.is_file():
                errors.append(f"rendered product projection missing {field}: {row.get(field)!r}")
    narrative_path = products / "narrative-book" / "manifest.json"
    reference_path = products / "architecture-reference" / "manifest.json"
    evidence_path = products / "evidence-registry" / "manifest.json"
    if not all(path.is_file() for path in (narrative_path, reference_path, evidence_path)):
        return errors
    narrative = load(narrative_path)
    reference = load(reference_path)
    evidence = load(evidence_path)
    graph_manifest = products / knowledge.COMPANION_DIR / "manifest.json"
    graph_home = products / knowledge.COMPANION_DIR / "index.html"
    if not graph_manifest.is_file() or not graph_home.is_file():
        errors.append("rendered evidence registry is missing the knowledge graph companion")
    else:
        graph = load(graph_manifest)
        expected = {"entry_path": "knowledge-graph/index.html", "manifest_path": "knowledge-graph/manifest.json",
                    "snapshot_id": graph.get("snapshot_id")}
        if (evidence.get("knowledge_graph") != expected or graph.get("source_commit") != status.get("source_commit")
                or graph.get("authority") != "navigation_only"):
            errors.append("knowledge graph identity or navigation authority differs from the rendered registry")
        registry = evidence_path.with_name("index.html").read_text(encoding="utf-8")
        home = (site / "index.html").read_text(encoding="utf-8")
        if 'href="knowledge-graph/index.html"' not in registry or knowledge.COMPANION_DIR + "/index.html" not in home:
            errors.append("knowledge graph is missing from the book home or Evidence Registry")
        archive_path = graph_manifest.with_name("graph.json.gz")
        if archive_path.is_file():
            with gzip.open(archive_path, "rt", encoding="utf-8") as stream:
                archive = json.load(stream)
            errors.extend(graph_route_errors(site, archive))
            try:
                graph_checks.check_published_packets(graph_manifest.parent, archive, graph)
            except (AssertionError, KeyError, IndexError, OSError, ValueError) as error:
                errors.append(f"Knowledge graph packet integrity failed: {error}")
    narrative_html = (products / "narrative-book" / "index.html").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    current_reader = load(ROOT / "editions/reader_manuscript/current/manifest.json")
    current_projection = narrative.get("current_reader", {})
    if (
        current_projection.get("unit_count") != current_reader.get("unit_count")
        or current_projection.get("owner_route_count") != current_reader.get("owner_route_count")
        or current_projection.get("manifest_sha256") != sha256_file(ROOT / "editions/reader_manuscript/current/manifest.json")
        or narrative.get("custody_mode") != "historical_candidate_navigation"
        or 'href="../../reader/"' not in narrative_html
        or "Historical candidate navigation" not in narrative_html
    ):
        errors.append("narrative entry lost the current-reader route or historical-candidate boundary")
    reference_html = (products / "architecture-reference" / "index.html").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    errors.extend(
        narrative_routing_errors(
            narrative,
            load(UNIT_CROSSWALK).get("units", []),
            canonical_chapters(load(STRUCTURE)),
            narrative_html,
        )
    )
    errors.extend(
        reference_responsibility_errors(
            reference,
            canonical_chapters(load(STRUCTURE)),
            reference_html,
        )
    )
    errors.extend(snapshot_errors(products, evidence))
    errors.extend(research_projection_errors(products, status["source_commit"], site))
    for row in narrative.get("chapters", []):
        if not (site / row.get("public_path", "")).is_file():
            errors.append(f"rendered narrative route target missing: {row.get('public_path')!r}")
    for row in reference.get("chapters", []):
        if not (site / row.get("public_path", "")).is_file():
            errors.append(f"rendered architecture route target missing: {row.get('public_path')!r}")
    for group in evidence.get("groups", []):
        for entry in group.get("entries", []):
            if entry.get("publication_mode") != "rendered_site_route":
                continue
            canonical_path = str(entry.get("canonical_path", ""))
            if not (site / canonical_path).is_file():
                errors.append(f"rendered evidence route target missing: {canonical_path!r}")
    latest_products = site / "latest" / "products"
    if (site / "latest").is_dir() and not (latest_products / "product-projections.json").is_file():
        errors.append("moving latest mirror is missing the product-projection manifest")
    return errors


def graph_route_errors(site: Path, graph: dict) -> list[str]:
    routes = defaultdict(set)
    errors = []
    urls = (row.get("url") for row in (
        *graph["nodes"], *(edge["qualifiers"] for edge in graph["edges"])
    ))
    for url in filter(None, urls):
        parts = urlsplit(url)
        path = Path(parts.path)
        if parts.scheme or parts.netloc or path.is_absolute() or ".." in path.parts:
            errors.append(f"unsafe internal knowledge graph route: {url}")
            continue
        routes[path].add(unquote(parts.fragment))
    for path, fragments in routes.items():
        page = site / path
        if not page.is_file():
            errors.append(f"missing knowledge graph destination: {path}")
            continue
        if fragments - {""}:
            ids = set(map(unescape, re.findall(r'\sid=["\']([^"\']+)', page.read_text(encoding="utf-8"))))
            errors.extend(f"missing knowledge graph anchor: {path}#{fragment}"
                          for fragment in sorted(fragments - ids - {""}))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="also validate generated product pages inside a rendered site")
    args = parser.parse_args()
    errors: list[str] = []
    graph_checks.main()
    errors.extend(run_history_controls())
    required = [STRUCTURE, CONTRACTS, SPINE, UNIT_CROSSWALK, CONTRIBUTIONS, SPINE_SCHEMA, PROJECTION_SCHEMA, DOC]
    for path in required:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        fail(errors)
    structure = load(STRUCTURE)
    spine = load(SPINE)
    status = build_status()
    spine_schema = load(SPINE_SCHEMA)
    projection_schema = load(PROJECTION_SCHEMA)
    errors.extend(validate_against_schema(spine, spine_schema, str(SPINE.relative_to(ROOT))))
    canonical = canonical_chapters(structure)
    canonical_ids = [row["chapter_id"] for row in canonical]
    selected_ids = [row["chapter_id"] for row in spine["chapters"]]
    unit_crosswalk = load(UNIT_CROSSWALK)
    units = unit_crosswalk.get("units", [])
    if len(units) != 22 or [row.get("order") for row in units] != list(range(1, 23)):
        errors.append("narrative unit crosswalk must contain 22 ordered units")
    if [row.get("representative_chapter_id") for row in units] != selected_ids:
        errors.append("narrative unit representatives do not match the narrative spine")
    assigned_ids = [
        chapter_id
        for unit in units
        for chapter_id in unit.get("chapter_ids", [])
    ]
    if len(assigned_ids) != len(set(assigned_ids)):
        errors.append("narrative unit crosswalk assigns at least one chapter more than once")
    if set(assigned_ids) != set(canonical_ids) or len(assigned_ids) != len(canonical_ids):
        errors.append(f"narrative unit crosswalk does not assign all {len(canonical_ids)} canonical chapters exactly once")
    for unit in units:
        if unit.get("representative_chapter_id") not in unit.get("chapter_ids", []):
            errors.append(f"{unit.get('unit_id')}: representative chapter is absent from its unit")
    errors.extend(narrative_projection_errors(spine))
    if len(selected_ids) != 22:
        errors.append("narrative product must contain exactly 22 representative chapters")
    if selected_ids != [chapter_id for chapter_id in canonical_ids if chapter_id in set(selected_ids)]:
        errors.append("narrative product spine does not preserve canonical manifest order")
    if status["claim_state_distribution"]["support_states"] != {"argument": len(canonical)}:
        errors.append("product projection must preserve all chapter-core support states at argument")

    with tempfile.TemporaryDirectory(prefix="asi-products-") as temp:
        temp = str(Path(temp).resolve())  # Resolve the owned macOS /var temp alias.
        output = Path(temp) / "products"
        output.mkdir(parents=True)
        build_into(output, status)
        root_manifest = load(output / "product-projections.json")
        errors.extend(validate_against_schema(root_manifest, projection_schema, "product-projections.json"))
        if {row["id"] for row in root_manifest["products"]} != {"narrative_book", "architecture_reference", "evidence_registry"}:
            errors.append("projection manifest must contain exactly the three product IDs")
        narrative = load(output / "narrative-book" / "manifest.json")
        reference = load(output / "architecture-reference" / "manifest.json")
        evidence = load(output / "evidence-registry" / "manifest.json")
        narrative_html = (output / "narrative-book" / "index.html").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        reference_html = (output / "architecture-reference" / "index.html").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        errors.extend(narrative_routing_errors(narrative, units, canonical, narrative_html))
        errors.extend(reference_responsibility_errors(reference, canonical, reference_html))
        if narrative.get("selected_chapter_count") != len(selected_ids):
            errors.append("narrative projection selected count mismatch")
        if narrative.get("canonical_chapter_count") != len(canonical):
            errors.append("narrative projection canonical count mismatch")
        if len(narrative.get("reference_only_chapters", [])) != len(canonical) - len(selected_ids):
            errors.append("narrative projection does not route every omitted chapter")
        if [row["chapter_id"] for row in reference.get("chapters", [])] != canonical_ids:
            errors.append("architecture-reference projection is not the complete canonical chapter order")
        if reference.get("chapter_count") != len(canonical):
            errors.append("architecture-reference chapter count mismatch")
        errors.extend(snapshot_errors(output, evidence))
        errors.extend(research_projection_errors(output, status["source_commit"]))
        if evidence.get("chapter_count") != len(canonical) or evidence.get("source_count") != status["counts"]["sources"]:
            errors.append("evidence-registry projection does not match canonical counts")
        for relative in (
            "index.html",
            "narrative-book/index.html",
            "architecture-reference/index.html",
            "evidence-registry/index.html",
        ):
            if not (output / relative).is_file() and relative != "index.html":
                errors.append(f"missing generated product page {relative}")

        reader_output = Path(temp) / "narrative-reader"
        summary = generate_reader(reader_output, "reader_release", SPINE)
        if summary.get("chapters") != len(selected_ids) or summary.get("omitted_canonical_chapter_count") != len(canonical) - len(selected_ids):
            errors.append("bounded narrative reader summary count mismatch")
        if summary.get("selected_chapter_ids") != selected_ids:
            errors.append("bounded narrative reader selected ID mismatch")
        for record in spine["chapters"]:
            chapter_file = next(row["source_file"] for row in canonical if row["chapter_id"] == record["chapter_id"])
            generated = reader_output / chapter_file
            text = generated.read_text(encoding="utf-8") if generated.exists() else ""
            for phrase in (
                "Narrative orientation",
                "**Plain-language thesis.**",
                "**Engineering rule.**",
                "**Machine contract.**",
                "**Question.**",
                "**Running example.**",
                "**Strongest objection.**",
                "**Failure story.**",
                "**What would change the conclusion.**",
                record["core_claim_ref"],
                "adds no evidence and changes no support state",
            ):
                if phrase not in text:
                    errors.append(f"{record['chapter_id']}: generated orientation missing {phrase!r}")
        omitted_files = {
            row["source_file"]
            for row in canonical
            if row["chapter_id"] not in set(selected_ids)
        }
        leaked = sorted(path for path in omitted_files if (reader_output / path).exists())
        if leaked:
            errors.append(f"bounded narrative reader copied omitted chapter files: {leaked[:3]}")

        # Reject a too-wide narrative product.
        too_wide = copy.deepcopy(spine)
        extra_id = next(chapter_id for chapter_id in canonical_ids if chapter_id not in set(selected_ids))
        extra = copy.deepcopy(too_wide["chapters"][-1])
        extra["order"] = 23
        extra["chapter_id"] = extra_id
        extra["core_claim_ref"] = f"{extra_id}.core"
        too_wide["chapters"].append(extra)
        too_wide_path = Path(temp) / "too-wide.json"
        write_json(too_wide_path, too_wide)
        try:
            load_narrative_spine(too_wide_path)
        except ValueError:
            pass
        else:
            errors.append("negative control failed: 23-unit narrative spine was accepted")

        # Reject a missing editorial field.
        missing_field = copy.deepcopy(spine)
        del missing_field["chapters"][0]["machine_contract"]
        if not validate_against_schema(missing_field, spine_schema, "negative.missing_field"):
            errors.append("negative control failed: missing machine contract was accepted")

        # Reject a substantial-looking machine contract that omits the
        # noninheritance boundary.
        unbounded_contract = copy.deepcopy(spine)
        unbounded_contract["chapters"][0]["machine_contract"] = (
            "The transition record binds source identity, target identity, authority, "
            "obligations, evidence, residuals, consumers, expiry, and recovery state."
        )
        if not narrative_projection_errors(unbounded_contract):
            errors.append("negative control failed: machine contract without noninheritance was accepted")

        # Reject selection order that disagrees with the canonical manifest.
        wrong_order = copy.deepcopy(spine)
        wrong_order["chapters"][0], wrong_order["chapters"][1] = wrong_order["chapters"][1], wrong_order["chapters"][0]
        wrong_order["chapters"][0]["order"] = 1
        wrong_order["chapters"][1]["order"] = 2
        try:
            filter_structure_for_narrative_spine(structure, wrong_order)
        except ValueError:
            pass
        else:
            errors.append("negative control failed: out-of-order narrative spine was accepted")

        # Reject a changed evidence snapshot against its content digest.
        snapshot = next(
            output / "evidence-registry" / entry["projection_path"]
            for group in evidence["groups"]
            for entry in group["entries"]
            if entry["publication_mode"] == "content_addressed_snapshot"
        )
        snapshot.write_bytes(snapshot.read_bytes() + b"\nmutation")
        if not snapshot_errors(output, evidence):
            errors.append("negative control failed: changed evidence snapshot was accepted")

        # Reject a specialist owner that exists in the crosswalk but is hidden
        # from the narrative unit's visible route.
        hidden_owner = copy.deepcopy(narrative)
        unit_with_specialists = next(
            row for row in hidden_owner["chapters"]
            if row.get("reference_owners")
        )
        unit_with_specialists["reference_owners"].pop()
        unit_with_specialists["reference_owner_count"] -= 1
        if not narrative_routing_errors(hidden_owner, units, canonical, narrative_html):
            errors.append("negative control failed: hidden specialist owner was accepted")

        # Reject a responsibility summary that drifts from its canonical
        # chapter owner even when the link and claim identity remain present.
        stale_responsibility = copy.deepcopy(narrative)
        stale_responsibility["chapters"][2]["reference_owners"][0]["distinct_responsibility"] = (
            "A generic chapter responsibility that no longer matches the canonical owner."
        )
        if not narrative_routing_errors(stale_responsibility, units, canonical, narrative_html):
            errors.append("negative control failed: stale specialist responsibility was accepted")

        # Reject support inflation in a reader-facing specialist route.
        inflated_support = copy.deepcopy(narrative)
        inflated_support["chapters"][2]["reference_owners"][0]["support_state"] = "empirical-test-backed"
        if not narrative_routing_errors(inflated_support, units, canonical, narrative_html):
            errors.append("negative control failed: inflated specialist support state was accepted")

    doc = DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        f"{len(selected_ids)}-unit",
        f"{len(canonical)}-chapter",
        "content-addressed",
        "not a reviewed reader release",
    ):
        if phrase not in doc:
            errors.append(f"{DOC.relative_to(ROOT)} missing {phrase!r}")
    if args.site is not None:
        site = args.site if args.site.is_absolute() else ROOT / args.site
        errors.extend(validate_rendered_site(site, projection_schema))
    fail(errors)
    print(
        f"Product-projection validation passed: {len(selected_ids)} narrative chapters, "
        f"{len(selected_ids) * 3} explicit unit projections, "
        f"{len(canonical) - len(selected_ids)} reference-routed omissions, "
        f"{len(canonical) - len(selected_ids)} visible specialist-owner routes, "
        f"{len(canonical)} reference chapters, {evidence['entry_count']} evidence routes, "
        "and research-history mutation controls."
    )


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Product-projection validation failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
