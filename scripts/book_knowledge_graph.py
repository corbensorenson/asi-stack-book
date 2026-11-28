#!/usr/bin/env python3
"""Compile the book's public records into a reproducible navigation graph."""

from __future__ import annotations

import argparse
import research_dictionary
from collections import Counter, deque
import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

from build_human_reader_current import CONCEPT_ENTRY_POINTS, slugify
from research_case_rows import anchor as run_anchor, location, rows_for, study_arm_label
import research_studies


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = "book_structure.json"
INVENTORY = "sources/source_inventory.json"
PAPER_LIBRARY = "papers/paper_library.json"
GLOSSARY = "appendices/B_glossary.qmd"
READER = "editions/reader_manuscript/current/"
READER_MANIFEST = READER + "manifest.json"
CROSSWALK = READER + "conclusion_claim_crosswalk.json"
CLAIMS = "evidence_quality/claim_atom_registry.json"
IDENTITIES = "evidence_quality/claim_identity_graph.json"
CITATIONS = "products/claim_citations.json"
CITATION_PAGE = "products/evidence-registry/claim-citations.html"
PASSAGES = "products/evidence_passages.json"
CASES = "products/evidence_cases.json"
CHAPTER_HISTORY = "docs/chapter_history_ledger.md"
PROOFS = "proofs/proof_manifest.json"
STUDIES = "products/research_studies.json"
CLAIM_ADDENDA = (
    "evidence_quality/replaceable_cognitive_substrates_claim_atom_addendum.json",
    "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json",
    "evidence_quality/round_18_breadth_completion_claim_atoms.json",
    "evidence_quality/taxonomy_completion_claim_atoms_2026_07_24.json",
    "evidence_quality/round20_four_chapter_claim_atom_addendum.json",
    "evidence_quality/round22_concept_linked_claim_atom_addendum.json",
)
SOURCE_TARGET_ALIASES = {
    "fast-generation": "fast-generation-architectures",
    "resource-economics": "resource-economics-and-token-budgets",
    "math-substrates": "mathematical-and-search-substrates",
}
SCHEMA_VERSION = "asi-stack.knowledge-graph.v1"
LINK = re.compile(r"\]\(\.\./chapters/([a-z0-9-]+)\.qmd(?:#[^)]+)?\)")
NAVIGATION_PRIORITY = ("supersedes_decision", "qualifies_study", "teaches_chapter", "reader_example", "owns_claim", "retains_run", "investigates",
                       "examines_run", "case_of_run", "related_proof", "discusses_claim", "cites_source", "follows_up",
                       "maps_source_passage", "atom", "subclaim_of", "proxy_for", "declares_proof_target",
                       "defined_by", "explained_by", "illustrated_by", "measured_in", "has_primary_source", "contains", "assigned_to")
PATH_PREDICATES = frozenset(NAVIGATION_PRIORITY) - {"contains", "assigned_to"}
PATH_VISIT_LIMIT = 1000
SEARCH_STOP_WORDS = frozenset(
    "a an are about can did does find for how i in is it of on or paper show study the to used was were "
    "what when where which with".split()
)


class Graph:
    def __init__(self, read):
        self.read = read
        self.inputs = {}
        self.nodes = {}
        self.edges = []
        self.unresolved = []

    def text(self, path):
        raw = self.read(path)
        self.inputs[path] = sha256(raw).hexdigest()
        return raw.decode("utf-8")

    def data(self, path):
        return json.loads(self.text(path))

    def node(self, kind, identity, path, locator, **fields):
        key = f"{kind}:{identity}"
        if key in self.nodes:
            raise ValueError(f"duplicate graph identity: {key}")
        self.nodes[key] = {"id": key, "kind": kind, "origin": source(path, locator), **fields}
        return key

    def edge(self, head, relation, tail, path, locator, **qualifiers):
        self.edges.append({"from": head, "predicate": relation, "to": tail,
                           "origin": source(path, locator), "qualifiers": qualifiers})

    def gap(self, source_id, relation, target, path, locator, reason):
        self.unresolved.append({"from": source_id, "predicate": relation, "target_ref": target,
                                "origin": source(path, locator), "reason": reason})


def source(path, locator):
    return {"path": path, "locator": locator}


def html_path(path):
    return str(Path(path).with_suffix(".html"))


def passage_refs(values):
    result = []
    for ref in values:
        url = urlsplit(ref)
        if url.scheme == "https" and url.hostname and not url.username and not url.password:
            result.append(ref)
        elif re.fullmatch(r"sources/source_notes/[a-zA-Z0-9_-]+\.md(?:#[^\s]+)?", ref):
            result.append(ref)
    return result


def chapter_records(graph):
    by_id = {}
    for part_i, part in enumerate(graph.data(STRUCTURE)["parts"]):
        pointer = f"/parts/{part_i}"
        parent = graph.node("part", part["id"], STRUCTURE, pointer, title=part["title"])
        for i, chapter in enumerate(part["chapters"]):
            locator = f"{pointer}/chapters/{i}"
            slug = chapter["id"]
            url = html_path(chapter["file"])
            owner = graph.node("chapter", slug, STRUCTURE, locator, title=chapter["title"], url=url)
            claim_id = slug + ".core"
            claim = graph.node("claim", claim_id, STRUCTURE, locator + "/core_claim",
                               title=chapter["core_claim"], role="core", state=chapter["evidence_level"],
                               label=chapter["claim_label"], record_version="current",
                               url="appendices/C_claim_evidence_matrix.html#" + claim_id)
            graph.edge(parent, "contains", owner, STRUCTURE, locator, order=i + 1)
            graph.edge(owner, "owns_claim", claim, STRUCTURE, locator + "/core_claim")
            by_id[slug] = (chapter, locator)
    return by_id


def reader_records(graph):
    manifest = graph.data(READER_MANIFEST)
    crosswalk = graph.data(CROSSWALK)
    by_id = {entry["unit_id"]: entry for entry in manifest["units"]}
    owners = {}
    seen = set()
    for i, unit in enumerate(crosswalk["units"]):
        unit_id = unit["unit_id"]
        locator = f"/units/{i}"
        row = by_id[unit_id]
        ids = [owner["chapter_id"] for owner in unit["owners"]]
        if unit_id in seen or ids != row["owner_ids"]:
            raise ValueError(f"reader crosswalk differs from the current manifest: {unit_id}")
        seen.add(unit_id)
        key = graph.node("reader_unit", unit_id, CROSSWALK, locator,
                         title=unit["title"], url=unit["public_path"], order=row["order"])
        for j, slug in enumerate(ids):
            if slug in owners:
                raise ValueError(f"duplicate reader owner: {slug}")
            owners[slug] = (key, row, unit["public_path"])
            graph.edge(key, "teaches_chapter", f"chapter:{slug}", CROSSWALK, f"{locator}/owners/{j}")
    if seen != set(by_id):
        raise ValueError("reader crosswalk omits a current unit")
    return owners


def source_records(graph, chapters):
    papers = {row["source_id"]: i for i, row in enumerate(graph.data(PAPER_LIBRARY)["records"])}
    for i, row in enumerate(graph.data(INVENTORY)):
        locator = f"/{i}"
        external = row["priority"] == "external_literature"
        fields = {"title": row["title"], "category": row["priority"],
                  "url": ("appendices/H_external_sources.html#" + row["id"] if external
                          else "appendices/G_corben_source_corpus.html")}
        if row["id"] in papers:
            fields.update(url=f"papers/{row['id']}.html",
                          publication_origin=source(PAPER_LIBRARY, f"/records/{papers[row['id']]}"))
        for key in ("source_type", "published", "citation_label"):
            if row.get(key):
                fields[key] = row[key]
        if row.get("passage_review_limits"):
            fields["limit"] = row["passage_review_limits"]
        url = urlsplit(row.get("url") or "")
        if external and url.scheme in {"http", "https"} and url.hostname and not url.username and not url.password:
            fields["primary_url"] = row["url"]
        key = graph.node("source", row["id"], INVENTORY, locator, **fields)
        for j, token in enumerate(row.get("chapter_targets", [])):
            pointer = f"{locator}/chapter_targets/{j}"
            slug = SOURCE_TARGET_ALIASES.get(token, token)
            # Alias use is corroborated by the destination's current source list.
            corroborated = slug in chapters and (
                slug == token or row["id"] in chapters[slug][0]["source_ids"]
            )
            if not corroborated:
                graph.gap(key, "assigned_to", token, INVENTORY, pointer, "no corroborated current chapter")
                continue
            graph.edge(key, "assigned_to", f"chapter:{slug}", INVENTORY, pointer,
                       recorded_target=token, via_alias=token != slug)

    for slug, (chapter, locator) in chapters.items():
        owner = f"chapter:{slug}"
        for i, identity in enumerate(chapter["source_ids"]):
            graph.edge(owner, "lists_source", f"source:{identity}", STRUCTURE, f"{locator}/source_ids/{i}")
        for i, mapping in enumerate(chapter.get("claim_source_mappings", [])):
            graph.edge(owner, "maps_source_passage", f"source:{mapping['source_id']}", STRUCTURE,
                       f"{locator}/claim_source_mappings/{i}",
                       review_state=mapping.get("passage_review_state", "unspecified"),
                       mapped_support=mapping["mapped_support"], limit=mapping["limits"],
                       passages=passage_refs(mapping.get("passage_refs", ())),
                       evidence_effect="none")


def concept_records(graph, owners):
    for number, line in enumerate(graph.text(GLOSSARY).splitlines(), start=1):
        if not line.startswith("| ") or line.startswith(("| Term |", "|---")):
            continue
        cells = re.split(r"(?<!\\)\|", line)[1:-1]
        if len(cells) != 4:
            raise ValueError(f"unexpected glossary row at line {number}")
        name, meaning, third, fourth = (cell.strip() for cell in cells)
        anchored = re.fullmatch(r"\[(.+)\]\{#term-([a-z0-9-]+)\}", name)
        if anchored:
            name, identity = anchored.groups()
            url = "appendices/B_glossary.html#term-" + identity
            chapter_links, limit = fourth, third
        else:
            identity = slugify(name)
            url = "appendices/B_glossary.html#architecture-and-source-terms"
            chapter_links, limit = third, fourth
        pointer = f"line:{number}"
        key = graph.node("concept", identity, GLOSSARY, pointer, title=name, definition=meaning,
                         limit=limit, url=url)
        for slug in dict.fromkeys(LINK.findall(chapter_links)):
            graph.edge(key, "defined_by" if not anchored else "explained_by", f"chapter:{slug}", GLOSSARY, pointer)

    for title, question, owner, heading, glossary_id in CONCEPT_ENTRY_POINTS:
        unit, row, url = owners[owner]
        path = READER + row["source_file"]
        match = re.search(rf"^## {re.escape(heading)}(?: \{{([^\n]+)\}})?$", graph.text(path), re.MULTILINE)
        if not match:
            raise ValueError(f"reader concept heading is missing: {heading}")
        explicit = re.search(r"(?:^|\s)#([\w-]+)", match[1] or "")
        fragment = explicit[1] if explicit else slugify(heading)
        slug = slugify(title)
        if f"concept:{slug}" not in graph.nodes:
            graph.node("concept", slug, "scripts/build_human_reader_current.py", "CONCEPT_ENTRY_POINTS:" + slug,
                       title=title, url="reader/index.html#concept-" + slug)
        graph.edge(f"concept:{slug}", "reader_example", unit, path, "#" + fragment,
                   url=url + "#" + fragment, question=question)
        if slug != glossary_id:
            graph.edge(f"concept:{slug}", "related_term", f"concept:{glossary_id}",
                       "scripts/build_human_reader_current.py", "CONCEPT_ENTRY_POINTS:" + slug)

def retired_chapter_routes(graph, chapters):
    candidates = {}
    for number, line in enumerate(graph.text(CHAPTER_HISTORY).splitlines(), 1):
        columns = [column.strip() for column in line.strip("|").split("|")]
        if len(columns) < 5 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", columns[0]):
            continue
        former, current = columns[1].strip("`"), columns[4].strip("`")
        if former not in chapters and current in chapters:
            candidates.setdefault(former, []).append((current, source(CHAPTER_HISTORY, f"line:{number}")))
    return {former: entries[0] for former, entries in candidates.items() if len(entries) == 1}


def claim_records(graph, chapters):
    staged = []
    for path in (CLAIMS, *CLAIM_ADDENDA):
        for i, row in enumerate(graph.data(path)["atoms"]):
            identity = row.get("atom_id") or row.get("id") or row["stable_claim_identity"]
            owner = row.get("chapter_id") or row.get("chapter_owner")
            statement = row.get("proposition") or row.get("claim") or row["claim_text"]
            pointer = f"/atoms/{i}"
            existing = "claim:" + identity in graph.nodes
            kind = "claim_record" if existing else "claim"
            key = graph.node(kind, f"{Path(path).stem}:{identity}" if existing else identity,
                             path, pointer, title=statement, label=row.get("claim_label"),
                             state=row.get("support_state"), role=row.get("role"), scope=row.get("scope"),
                             record_version="retained", owner_ref=owner)
            if existing:
                graph.edge(key, "retained_record_for", "claim:" + identity, path, pointer,
                           evidence_effect="none")
            elif owner in chapters:
                graph.edge(f"chapter:{owner}", "owns_claim", key, path, pointer)
            elif owner:
                graph.gap(key, "owned_by", owner, path, pointer, "retained chapter ID outside the current manifest")
            if row.get("concept_id") and owner in chapters:
                identity = f"{owner}.{row['concept_id']}"
                concept = graph.node("concept", identity, path, pointer + "/concept_id",
                                     title=row["heading"], record_version="retained",
                                     url=html_path(chapters[owner][0]["file"]))
                graph.edge(concept, "has_concept_claim", key, path, pointer)
                graph.edge(concept, "explained_by", f"chapter:{owner}", path, pointer)
            staged.append((key, path, pointer, row))
    retired_routes = retired_chapter_routes(graph, chapters)
    for key, path, pointer, row in staged:
        for i, dependency in enumerate(row.get("dependencies", [])):
            locator = f"{pointer}/dependencies/{i}"
            candidates = [f"{kind}:{dependency}" for kind in ("claim", "chapter", "source", "proof_target")
                          if f"{kind}:{dependency}" in graph.nodes]
            if len(candidates) == 1:
                graph.edge(key, "declares_dependency", candidates[0], path, locator,
                           target_kind=graph.nodes[candidates[0]]["kind"], evidence_effect="none")
            elif not candidates and dependency in retired_routes:
                target, origin = retired_routes[dependency]
                graph.edge(key, "declares_dependency", "chapter:" + target, path, locator,
                           target_kind="chapter", via_alias=True, recorded_target=dependency,
                           alias_origin=origin, evidence_effect="none")
            else:
                reason = "ambiguous retained reference" if candidates else "unresolved retained reference"
                graph.gap(key, "declares_dependency", dependency, path, locator, reason)


def citation_inputs(read):
    selections = json.loads(read(CITATIONS))
    selected = {row["id"]: row for row in selections}
    if len(selected) != len(selections):
        raise ValueError("duplicate claim citation")
    identities = {}
    for row in json.loads(read(IDENTITIES))["records"]:
        identity = row["claim_id"]
        if identity in selected:
            if identity in identities:
                raise ValueError(f"ambiguous citation transition: {identity}")
            if selected[identity]["run"] not in row["identity_scope"]["artifact"]:
                raise ValueError(f"citation run is outside the retained identity scope: {identity}")
            identities[identity] = row
    if selected.keys() != identities.keys():
        raise ValueError("claim citation lacks a retained transition")
    return [(selection, identities[identity]) for identity, selection in selected.items()]


def claim_citations(read):
    proofs = {row["tag"]: row for row in json.loads(read(PROOFS))["records"]}
    for selection, identity in citation_inputs(read):
        record = read(identity["transition_path"])
        if sha256(record).hexdigest() != identity["transition_sha256"]:
            raise ValueError(f"citation transition digest changed: {selection['id']}")
        transition = json.loads(record)
        citation = {**selection, "transition": identity["transition_path"],
               "transition_id": identity["transition_id"], "relation": identity["primary_relation"],
               "url": f"{CITATION_PAGE}#{selection['id']}", "parent": identity["canonical_parent_id"],
               "parent_effect": identity["parent_support_state_effect"],
               "proposition": transition["scope_boundary"], "state": transition["new_support_state"],
               "decision": transition["transition_effect"], "limits": transition["limitations"],
               "run_sha256": sha256(read(selection["run"])).hexdigest()}
        if tag := selection.get("related_proof"):
            proof = proofs[tag]
            if proof["status"] != "implemented" or proof["chapter_id"] != identity["owner_chapter_id"]:
                raise ValueError(f"citation proof belongs to another scope: {tag}")
            citation["proof"] = {
                "tag": tag,
                "url": f'{CITATION_PAGE}#proof-{selection["id"]}',
                "proposition": proof["formal_target"],
                "limit": selection["proof_scope"],
                "module_path": proof["module_path"],
            }
        yield citation


DECLARATIONS = "products/proof_declarations.json"


def declaration_cards(read):
    cards = {}
    for item in json.loads(read(DECLARATIONS)):
        path = item["module_path"]
        lines = read(path).decode().splitlines()
        declarations = []
        for row in item["declarations"]:
            pattern = re.compile(r"^(?:theorem|lemma) " + re.escape(row["name"]) + r"\b")
            matches = [i for i, line in enumerate(lines, 1) if pattern.match(line)]
            if len(matches) != 1:
                raise ValueError(f"Missing or ambiguous Lean declaration: {row['name']}")
            declarations.append({**row, "origin": source(path, f"line:{matches[0]}")})
        cards[item["tag"]] = {**item, "declarations": declarations}
    return cards


def evidence_records(graph):
    cards = declaration_cards(lambda path: graph.text(path).encode())
    for i, row in enumerate(graph.data(PROOFS)["records"]):
        locator = f"/records/{i}"
        key = graph.node("proof_target", row["tag"], PROOFS, locator, title=row["formal_target"],
                         status=row["status"], module=row["module"])
        if row["status"] == "implemented":
            graph.nodes[key]["implementation_origin"] = source(row["module_path"], "/")
        if card := cards.get(row["tag"]):
            if row.get("module_path") != card["module_path"]:
                raise ValueError(f"Proof citation module mismatch: {row['tag']}")
            node = graph.nodes[key]
            node["implementation_origin"] = card["declarations"][0]["origin"]
            node["declarations"] = card["declarations"]
            node["locators"] = [{"label": "Passage using this formal result", "url": card["passage"]},
                                {"label": "Declaration names and premises", "url": "products/evidence-registry/proof-declarations.html#" + row["tag"]}]
        graph.edge(f"chapter:{row['chapter_id']}", "declares_proof_target", key, PROOFS, locator)

    for i, row in enumerate(graph.data(IDENTITIES)["records"]):
        locator = f"/records/{i}"
        key = graph.node("transition", row["transition_id"], IDENTITIES, locator,
                         title=row["claim_id"], record_sha256=row["transition_sha256"],
                         transition_origin=source(row["transition_path"], "/"))
        relation = row["primary_relation"]
        effect = row["parent_support_state_effect"]
        if relation in {"proxy_for", "subclaim_of"} and effect != "none":
            raise ValueError(f"{row['transition_id']}: non-exact relation carries a parent support effect")
        graph.edge(key, relation, "claim:" + row["canonical_parent_id"], IDENTITIES, locator,
                   parent_support_state_effect=effect, scope=row["identity_scope"])

    def citation_bytes(path):
        return graph.text(path).encode("utf-8")

    for citation in claim_citations(citation_bytes):
        transition_id = "transition:" + citation["transition_id"]
        transition = graph.nodes[transition_id]
        transition["url"] = citation["url"]
        transition["summary"] = citation["proposition"]
        transition["limit"] = ". ".join(item.rstrip(".") for item in citation["limits"]) + "."
        transition["citation_title"] = citation["title"]
        transition["state"] = citation["state"]
        claim = graph.nodes.get("claim:" + citation["id"])
        if claim is not None and claim["role"] != "core":
            claim["url"] = citation["url"]
        if proof := citation.get("proof"):
            proof_key = "proof_target:" + proof["tag"]
            graph.nodes[proof_key].update(url=proof["url"], summary=proof["proposition"], limit=proof["limit"],
                                          citation_title="Circle finite public-consumer gate",
                                          measurement="Finite formal target", method=graph.nodes[proof_key]["module"])
            position = next(i for i, row in enumerate(graph.data(CITATIONS)) if row["id"] == citation["id"])
            graph.edge(transition_id, "related_proof", proof_key, CITATIONS, f"/{position}/related_proof",
                       scope=proof["limit"], evidence_effect="none")

    manifest = graph.data(STUDIES)
    for i, study in enumerate(research_studies.studies_from(manifest, lambda p: graph.text(str(p)).encode("utf-8"))):
        locator = f"/studies/{i}"
        url = f"products/evidence-registry/study-{study['id']}.html"
        key = graph.node(
            "study", study["id"], STUDIES, locator, title=study["title"], question=study["question"], url=url,
            featured_run="study_run:" + study["featured_run"], summary=study["summary"],
            limit=study["limit"], disposition=study["disposition"], change=study["change"], date=study["date"],
        )
        if study.get("claim"):
            graph.edge(key,"investigates","claim:"+study["claim"]["id"],STUDIES,locator+"/claim",
                       scope=study["claim"]["scope"],evidence_effect="none")
        for run in study["runs"]:
            record_index = next(i for i, declared in enumerate(manifest["runs"]) if declared["id"] == run["id"])
            run_locator = f"/runs/{record_index}"
            identity = graph.node("study_run",run["id"],STUDIES,run_locator,title=run["title"],
                                  url=url+"#"+run_anchor(run["id"]),limit=run["limit"],summary=run["summary"],
                                  result_sha256=run["result_sha256"], protocol_sha256=run["protocol_sha256"],
                                  source_commit=run["source_commit"], disposition=run["disposition"],
                                  unmeasured=run.get("unmeasured", []), date=run["date"],
                                  method=run["method"], protocol=run["protocol"], result=run["result"],
                                  question=study["question"], featured=study["featured_run"] == run["id"],
                                  format=run["format"], aliases=run.get("aliases", []), outside_question=run.get("outside_question", ""))
            graph.edge(key,"retains_run",identity,STUDIES,run_locator,featured=study["featured_run"]==run["id"])
            if run.get("follow_up_to"):
                graph.edge(identity, "follows_up", "study_run:" + run["follow_up_to"], STUDIES,
                           run_locator + "/follow_up_to", evidence_effect="none")


def evidence_passages(graph):
    rows = graph.data(PASSAGES)
    passages = {f"evidence_passage:{row['id']}": row for row in rows}
    for i, passage in enumerate(rows):
        locator = f"/{i}"
        fields = {name: value for name, value in passage.items() if name not in {"id", "links"}}
        key = graph.node("evidence_passage", passage["id"], PASSAGES, locator, **fields)
        for j, link in enumerate(passage["links"]):
            if link["predicate"] not in {"cites_source", "discusses_claim", "examines_run", "explained_by",
                                         "qualifies_study", "supersedes_decision"}:
                raise ValueError(f"invalid evidence passage relation: {link['predicate']}")
            if link["predicate"] == "supersedes_decision":
                older = passages.get(link["target"], {})
                if passage.get("record_version") == "superseded" or older.get("record_version") != "superseded":
                    raise ValueError("Decision supersession must point from a current passage to a superseded passage")
            graph.edge(key, link["predicate"], link["target"], PASSAGES, f"{locator}/links/{j}",
                       evidence_effect="none")


def evidence_cases(graph):
    normalized = {}
    for i, selection in enumerate(graph.data(CASES)):
        run_id = selection["run"]
        run_key = "study_run:" + run_id
        run = graph.nodes[run_key]
        if run_id not in normalized:
            result = graph.data(run["result"])
            normalized[run_id] = {row["id"]: row for row in rows_for(run["format"], result)}
        row = normalized[run_id][selection["case"]]
        arms = [f'{study_arm_label(name)}: {row["arms"][name]["outcome"]}'
                for name in selection.get("arms", row["arms"])]
        locator = f"/{i}"
        anchor = run_anchor(run_id, row["id"])
        key = graph.node("evidence_case", f'{run_id}--{row["id"]}', CASES, locator,
                         title=selection["title"], question=selection["question"],
                         summary=". ".join(arms) + ".", limit=selection["limit"], method=row["condition"],
                         aliases=selection["aliases"], source_commit=run["source_commit"],
                         study_run=run_key,
                         measurement="Authored paired case",
                         result_sha256=run["result_sha256"], date=run["date"],
                         url=run["url"].split("#", 1)[0] + "#" + anchor)
        graph.edge(key, "case_of_run", run_key, CASES, locator + "/case", evidence_effect="none")


def collection_routes(graph):
    registry = "products/evidence-registry/"
    for ri, run in enumerate(graph.data(STUDIES)["runs"]):
        run_key = "study_run:" + run["id"]
        node = graph.nodes[run_key]
        result = graph.data(run["result"])
        readings = {}
        if run["format"] == "three_papers":
            path = "experiments/scifact_three_papers/observations.json"
            readings = {str(case["id"]): location("cases", index)
                        for index, case in enumerate(graph.data(path)["cases"])}
        for row in rows_for(run["format"], result):
            identity = run["id"] + "--" + row["id"]
            key = "evidence_case:" + identity
            if key not in graph.nodes:
                outcomes = ". ".join(f'{study_arm_label(k)}: {v["outcome"]} ({v["work"]})' for k, v in row["arms"].items())
                graph.node("evidence_case", identity, run["result"], row["pointers"][0], title=row["id"],
                           aliases=[row["id"]], question=row["condition"], summary=outcomes,
                           limit=node["limit"], measurement="Case identifier", source_commit=run["source_commit"],
                           result_sha256=run["result_sha256"], url=node["url"].split("#")[0]+"#"+run_anchor(run["id"],row["id"]))
                graph.edge(key, "case_of_run", run_key, STUDIES, f"/runs/{ri}", evidence_effect="none")
            prefix = f'https://raw.githubusercontent.com/corbensorenson/asi-stack-book/{run["source_commit"]}/'
            sources = [dict(role="reported_result", url=prefix+run["result"], pointer=pointer,
                            sha256=run["result_sha256"]) for pointer in row["pointers"]]
            if readings:
                sources.append(dict(role="model_readings", url=prefix+path, pointer=readings[row["id"]],
                                    sha256=graph.inputs[path]))
            graph.nodes[key].update(case_id=row["id"], case_sources=sources)
        if run["format"] == "sygus_external":
            for task in sorted({r["task"] for r in graph.data(run["result"])["cases"]}):
                key = graph.node("evidence_passage", task+"-schedules", run["result"], "/cases",
                                 title=task+" under both schedules", aliases=[task], limit=node["limit"],
                                 summary="Compare the same task across two schedules and three libraries.",
                                 source_commit=run["source_commit"], result_sha256=run["result_sha256"],
                                 url=node["url"].split("#")[0]+"#task-"+task)
                if task == "hd-17":
                    graph.nodes[key].update(question="Which task changed the whole-program result?",
                                            aliases=[task,"proposals to first solution"],
                                            summary="Only whole-program handles solved hd-17, at 8,142 proposals. The other five cells exhausted 12,000.")
                graph.edge(key,"examines_run",run_key,STUDIES,f"/runs/{ri}",evidence_effect="none")
                for schedule in ("handles","expanded"):
                    graph.edge(key,"compares_case","evidence_case:"+run["id"]+"--"+task+"-"+schedule,
                               STUDIES,f"/runs/{ri}",evidence_effect="none")
        if run["format"] in research_studies.PORTABLE_RUN_FORMATS:
            key = graph.node("evidence_passage", run["id"]+"-download", STUDIES, f"/runs/{ri}",
                             title=run["id"]+"-replay.zip", aliases=[run["title"]+" replay download"],
                             url=node["url"], limit=node["limit"], summary="Download the offline replay from this run.")
            graph.edge(key,"examines_run",run_key,STUDIES,f"/runs/{ri}",evidence_effect="none")
    for ci, card in enumerate(graph.data(DECLARATIONS)):
        for di, decl in enumerate(card["declarations"]):
            name = decl["name"]
            locator = f"/{ci}/declarations/{di}"
            clues = {field: decl[field] for field in ("aliases", "question") if field in decl}
            key = graph.node("evidence_passage",name,DECLARATIONS,locator,title=name,**clues,
                             summary=decl["conclusion"],limit=decl["premises"],measurement="Formal declaration",
                             url=registry+"proof-declarations.html#"+name)
            graph.edge(key,"specifies_declaration_of","proof_target:"+card["tag"],DECLARATIONS,locator,evidence_effect="none")
    def bibliography(identity, title, target, path, locator):
        key = graph.node("evidence_passage", "bibliography-"+identity,path,locator,
                         title=title+" bibliography",aliases=[identity+".bib",identity+".json",title+" CSL-JSON"],
                         url=registry+"bibliographies/index.html#"+identity,summary="Download BibTeX or CSL-JSON.",
                         limit="Reference membership describes the works used or assigned. Claim support is recorded separately.")
        graph.edge(key,"bibliography_for",target,path,locator,evidence_effect="none")
    for pi, part in enumerate(graph.data(STRUCTURE)["parts"]):
        for ci, chapter in enumerate(part["chapters"]):
            bibliography(chapter["id"],chapter["title"],"chapter:"+chapter["id"],STRUCTURE,f"/parts/{pi}/chapters/{ci}")
    for si, study in enumerate(graph.data(STUDIES)["studies"]):
        bibliography("study-"+study["id"],study["title"],"study:"+study["id"],STUDIES,f"/studies/{si}")


def compile_graph(read, *, source_commit, worktree):
    graph = Graph(read)
    for path in ("scripts/book_knowledge_graph.py", "scripts/build_human_reader_current.py",
                 "scripts/research_studies.py", "scripts/research_case_rows.py"):
        graph.text(path)
    graph.text("scripts/research_dictionary.py")
    chapters = chapter_records(graph)
    owners = reader_records(graph)
    if set(owners) != set(chapters):
        raise ValueError("current reader owners differ from canonical chapters")
    source_records(graph, chapters)
    concept_records(graph, owners)
    claim_records(graph, chapters)
    research_dictionary.add_terms(graph)
    evidence_records(graph)
    evidence_passages(graph)
    evidence_cases(graph)
    collection_routes(graph)
    research_dictionary.link_evidence(graph)
    for edge in graph.edges:
        if edge["from"] not in graph.nodes or edge["to"] not in graph.nodes:
            raise ValueError(f"graph edge has an unknown endpoint: {edge}")
    payload = {
        "schema_version": SCHEMA_VERSION, "source_commit": source_commit, "worktree": worktree,
        "authority": "navigation_only", "inputs_sha256": graph.inputs,
        "coverage": {"nodes": dict(Counter(n["kind"] for n in graph.nodes.values())),
                     "edges": dict(Counter(e["predicate"] for e in graph.edges)),
                     "unresolved": len(graph.unresolved)},
        "nodes": sorted(graph.nodes.values(), key=lambda n: n["id"]),
        "edges": sorted(graph.edges, key=lambda e: (e["from"], e["predicate"], e["to"], e["origin"]["locator"])),
        "unresolved": graph.unresolved,
    }
    return {**payload, "snapshot_id": sha256(json_bytes(payload)).hexdigest()}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def search_metadata(node, display_title):
    citation = node.get("citation_label", "")
    alias = re.split(r"\([0-9]{4}[a-z]?\)[,.:]?\s*", citation, maxsplit=1)[-1] if citation else ""
    context = [node.get(field, "") for field in ("definition", "question", "summary", "citation_title",
                                                  "disposition", "limit")]
    context.extend(node.get("aliases", []))
    context.extend(node.get("unmeasured", []))
    context.extend((citation, node["title"][len(display_title) - 1:] if display_title != node["title"] else ""))
    names = node.get("aliases", []) if node.get("dictionary_url") else []
    return slugify(alias), slugify(" ".join(context)), names


def evidence_catalog(graph):
    """Expose the same bounded records used to build the graph's search index."""
    kinds = {"study", "study_run", "evidence_passage", "evidence_case", "transition", "proof_target"}
    records = []
    for node in graph["nodes"]:
        if node["kind"] not in kinds or not node.get("url"):
            continue
        measurement = node.get("measurement") or {
            "study_run": "Measured under stated conditions",
            "transition": "Retained evidence decision",
        }.get(node["kind"], "")
        fields = [
            node.get("citation_title", node["title"]),
            f'https://corbensorenson.github.io/asi-stack-book/{node["url"]}',
            f'Evidence record {node["id"]}',
            f'Book revision {graph["source_commit"]}',
        ]
        for label, key in (("Evidence revision", "source_commit"), ("Result SHA-256", "result_sha256"),
                           ("Method", "method"), ("Source locator", "source_section"), ("Scope", "limit")):
            if key in node:
                fields.append(f"{label} — {node[key]}")
        fields.extend(f'Case input — {ref["url"]} · JSON Pointer {ref["pointer"]} · SHA-256 {ref["sha256"]}'
                      for ref in node.get("case_sources", []))
        records.append({**node, "measurement": measurement, "citation_text": "\n".join(fields)})
    return {
        "schema_version": "asi-stack.evidence-catalog.v1",
        "source_commit": graph["source_commit"],
        "snapshot_id": graph["snapshot_id"],
        "authority": graph["authority"],
        "records": records,
    }


def search_terms(text):
    return {word[:-1] if len(word) > 4 and word.endswith("s") else word
            for word in text.split("-") if word and word not in SEARCH_STOP_WORDS}


def search_score(typed_query, query, words, key, title, alias, context, names):
    identity = slugify(key.split(":", 1)[1])
    if typed_query == key:
        return 1000
    if typed_query.casefold() == title.casefold():
        return 910
    if any(typed_query.casefold() == name.casefold() for name in names):
        return 905
    title = slugify(title)
    if query in {identity, title}:
        return 900
    if query == alias:
        return 870
    if title.startswith(query + "-"):
        return 830
    if f"-{query}-" in f"-{title}-":
        return 800
    if len(alias) >= 3 and f"-{alias}-" in f"-{query}-":
        return 780
    primary = words & search_terms("-".join((identity, title, alias)))
    covered = primary | (words & search_terms(context))
    if not covered or len(covered) * 100 < len(words) * 55:
        return 0
    return 200 * len(covered) // len(words) + 140 * len(primary) // len(words)


def search(graph, query, *, kind=None, limit=8):
    typed_query = query.strip()
    query = slugify(query)
    if not query:
        raise ValueError("search needs at least one letter or digit")
    words = search_terms(query)
    hits = []
    for entry in graph["nodes"]:
        if kind and entry["kind"] != kind:
            continue
        title = title_excerpt(entry["title"])
        score = search_score(typed_query, query, words, entry["id"], title, *search_metadata(entry, title))
        if score:
            hits.append((-score, len(title), entry["id"], entry))
    hits.sort()
    return {"snapshot": graph["snapshot_id"], "matches": [hit[-1] for hit in hits[:limit]],
            "total_matches": len(hits)}


def title_excerpt(value, cap=180):
    if len(value) <= cap:
        return value
    return value[:cap - 1] + "…"


def neighborhood(graph, node_id, *, depth=1, limit=24, predicates=()):
    nodes = {row["id"]: row for row in graph["nodes"]}
    seed = nodes[node_id]
    adjacent = {}
    for edge in graph["edges"]:
        if not predicates or edge["predicate"] in predicates:
            adjacent.setdefault(edge["from"], []).append((edge, edge["to"]))
            adjacent.setdefault(edge["to"], []).append((edge, edge["from"]))
    priority = {predicate: i for i, predicate in enumerate(NAVIGATION_PRIORITY)}
    frontier = [node_id]
    visited = {node_id}
    selected = {}
    truncated = False
    for _ in range(depth):
        next_frontier = []
        # Give each vertex in a layer one turn before returning to its neighbors.
        # A heavily linked chapter should not exhaust the whole budget alone.
        pending = deque(iter(sorted(adjacent.get(vertex, ()), key=lambda pair: (
            priority.get(pair[0]["predicate"], len(priority)), pair[1]
        ))) for vertex in frontier)
        while pending:
            iterator = pending.popleft()
            pair = next(iterator, None)
            if pair is None:
                continue
            pending.append(iterator)
            edge, target = pair
            key = (edge["from"], edge["predicate"], edge["to"], edge["origin"]["path"], edge["origin"]["locator"])
            if key in selected:
                continue
            if len(selected) == limit:
                truncated = True
                break
            selected[key] = edge
            if target not in visited:
                visited.add(target)
                next_frontier.append(target)
        frontier = next_frontier
        if not frontier or truncated:
            break
    return {"snapshot": graph["snapshot_id"], "seed": seed, "nodes": [nodes[key] for key in sorted(visited)],
            "edges": list(selected.values()), "depth": depth, "truncated": truncated}


def connection(graph, start, end, *, predicates=(), depth=4):
    nodes = {node["id"]: node for node in graph["nodes"]}
    for key in (start, end):
        if key not in nodes:
            raise KeyError(key)
    eligible = frozenset(predicates) if predicates else PATH_PREDICATES
    adjacent = {}
    for edge in graph["edges"]:
        if edge["predicate"] in eligible:
            adjacent.setdefault(edge["from"], []).append((edge["to"], edge))
            adjacent.setdefault(edge["to"], []).append((edge["from"], edge))
    priority = {predicate: i for i, predicate in enumerate(NAVIGATION_PRIORITY)}
    parents = [{start: None}, {end: None}]
    frontiers = [[start], [end]]
    meeting = start if start == end else None
    capped = False
    for _ in range(depth):
        if meeting or capped or not all(frontiers):
            break
        side = int(len(frontiers[1]) < len(frontiers[0]))
        next_frontier = []
        for vertex in frontiers[side]:
            ordered = sorted(adjacent.get(vertex, ()), key=lambda item: (
                priority.get(item[1]["predicate"], len(priority)), item[0]
            ))
            for neighbor, edge in ordered:
                if neighbor in parents[side]:
                    continue
                if neighbor in parents[1 - side]:
                    parents[side][neighbor] = vertex, edge
                    meeting = neighbor
                    break
                if sum(map(len, parents)) >= PATH_VISIT_LIMIT:
                    capped = True
                    break
                parents[side][neighbor] = vertex, edge
                next_frontier.append(neighbor)
            if meeting or capped:
                break
        frontiers[side] = next_frontier

    path_nodes, path_edges = [], []
    if meeting:
        cursor = meeting
        while cursor != start:
            path_nodes.append(nodes[cursor])
            cursor, edge = parents[0][cursor]
            path_edges.append(edge)
        path_nodes.append(nodes[start])
        path_nodes.reverse()
        path_edges.reverse()
        cursor = meeting
        while cursor != end:
            cursor, edge = parents[1][cursor]
            path_nodes.append(nodes[cursor])
            path_edges.append(edge)
    return {
        "snapshot": graph["snapshot_id"], "authority": "navigation_only", "start": start, "end": end,
        "status": "found" if meeting else "visit_limit_reached" if capped else "no_route_within_depth",
        "depth_limit": depth, "visit_limit": PATH_VISIT_LIMIT,
        "predicates": sorted(eligible), "nodes": path_nodes, "edges": path_edges,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    option = parser.add_mutually_exclusive_group()
    option.add_argument("--find", metavar="TEXT", help="Find nodes by title or stable ID")
    option.add_argument("--node", metavar="ID", help="Read a bounded neighborhood")
    option.add_argument("--path", nargs=2, metavar=("FROM", "TO"), help="Find a short citation or reading route")
    parser.add_argument("--kind", help="Limit search to one node kind")
    parser.add_argument("--predicate", action="append", default=[], help="Permit a relation during traversal")
    parser.add_argument("--depth", type=int, choices=(1, 2, 3, 4),
                        help="Default depth is 1 for --node and 4 for --path")
    parser.add_argument("--limit", type=int, default=24, help="Maximum matches or edges (1–100)")
    parser.add_argument("--snapshot", type=Path, help="Query a previously compiled JSON snapshot")
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    if args.node and args.depth and args.depth > 2:
        parser.error("--node supports depth 1 or 2. Use --path for longer routes.")
    if args.snapshot:
        raw = args.snapshot.read_bytes()
        if raw.startswith(b"\x1f\x8b"):
            raw = gzip.decompress(raw)
        graph = json.loads(raw)
        if graph.get("schema_version") != SCHEMA_VERSION:
            parser.error("unsupported snapshot format")
    else:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        graph = compile_graph(lambda p: (ROOT / p).read_bytes(), source_commit=commit, worktree=True)
    if args.find is not None:
        try:
            graph = search(graph, args.find, kind=args.kind, limit=args.limit)
        except ValueError as error:
            parser.error(str(error))
    elif args.node is not None or args.path is not None:
        try:
            if args.path:
                graph = connection(graph, *args.path, depth=args.depth or 4, predicates=args.predicate)
            else:
                graph = neighborhood(graph, args.node, depth=args.depth or 1, limit=args.limit, predicates=args.predicate)
        except KeyError:
            parser.error(f"unknown node: {args.node}")
    sys.stdout.buffer.write(json_bytes(graph))


if __name__ == "__main__":
    main()
