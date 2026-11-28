"""Publish small, revision-bound entry points and exports of rendered book sections."""
from html.parser import HTMLParser
from hashlib import sha256
import json
import re
from pathlib import PurePosixPath
from urllib.parse import quote, unquote, urljoin, urlsplit

from research_dictionary import DIRECTORY

BOOK = "https://corbensorenson.github.io/asi-stack-book/"
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
SKIP = {"script", "style", "nav", "button", "svg", "iframe", "noscript", "template"}
HEADINGS = {"h2", "h3", "h4", "h5", "h6"}
BLOCKS = {"p", "li", "dt", "dd", "tr", "pre", "figcaption", "caption"} | HEADINGS
SCIFACT_LOOKUP = "agent/topics/scifact.json"
SCIFACT_STUDY_PAGES = {
    "products/evidence-registry/study-scientific-citation.html",
    "products/evidence-registry/study-citation-retrieval.html",
}
SCIFACT_CHAPTER_RECORDS = {"evidence_passage:scifact-scoring-ceiling"}


def artifact_anchor(anchor):
    """Keep human-readable filenames where the anchor is safe in an artifact."""
    if re.fullmatch(r"[A-Za-z0-9._-]{1,180}", anchor) and anchor not in {".", ".."}:
        return anchor
    return "~" + sha256(anchor.encode("utf-8")).hexdigest()


class PassageParser(HTMLParser):
    def __init__(self, targets=()):
        super().__init__()
        self.targets = set(targets)
        self.stack = []
        self.records = {}
        self.exact = {}
        self.footnotes = {}
        self.ancestors = {}
        self.tables = []
        self.main = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "main":
            self.main = True
        if not self.main:
            return
        blocked = (self.stack and self.stack[-1]["blocked"]) or tag in SKIP
        identity = attrs.get("id")
        frame = {"tag": tag, "id": identity, "blocked": blocked, "parts": [], "links": [],
                 "cells": [], "rows": [], "targets": [],
                 "case_listing": tag == "details" and "data-study-cases" in attrs}
        if identity and (tag == "section" or tag in HEADINGS):
            self.ancestors[identity] = [f["id"] for f in self.stack if f["tag"] == "section" and f["id"]]
        if tag not in VOID:
            self.stack.append(frame)
        if blocked:
            return
        if identity in self.targets:
            if tag in BLOCKS or tag in {"article", "section", "div", "table", "details", "dl", "ol", "ul"}:
                frame["targets"].append(identity)
            else:
                owner = next((part for part in reversed(self.stack) if part["tag"] in BLOCKS), frame)
                owner["targets"].append(identity)
        if tag == "a" and attrs.get("href") and "anchorjs-link" not in attrs.get("class", ""):
            for parent in reversed(self.stack):
                if parent["case_listing"]:
                    break
                parent["links"].append(attrs["href"])
        if tag in BLOCKS or tag == "br":
            self.handle_data("\n")
        if tag == "img" and attrs.get("alt"):
            self.handle_data(attrs["alt"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.stack and not self.stack[-1]["blocked"]:
            self.stack[-1]["parts"].append(data)

    def handle_endtag(self, tag):
        if tag in VOID or not self.main:
            return
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index]["tag"] == tag:
                break
        else:
            return
        frame = self.stack[index]
        del self.stack[index:]
        if frame["blocked"]:
            return
        text = "".join(frame["parts"])
        if tag in {"td", "th"}:
            cell = " ".join(text.split())
            row = next((part for part in reversed(self.stack) if part["tag"] == "tr"), None)
            if row is not None:
                row["cells"].append({"text": cell, "header": tag == "th"})
            text = (" | " if row and len(row["cells"]) > 1 else "") + cell
        if tag == "tr":
            if table := next((part for part in reversed(self.stack) if part["tag"] == "table"), None):
                if frame["cells"]:
                    table["rows"].append(frame["cells"])
                if frame["targets"]:
                    headers = [row for row in table["rows"][:-1] if all(cell["header"] for cell in row)]
                    frame["rows"] = headers + [frame["cells"]]
        if tag == "table" and frame["rows"]:
            listing = next((i for i in range(len(self.stack)-1, -1, -1) if self.stack[i]["case_listing"]), -1)
            owners = self.stack[listing+1:]
            section_ids = {part["id"] for part in owners if part["tag"] == "section"}
            section_ids.update(target for part in owners for target in part["targets"])
            if listing == -1 and "" in self.targets:
                section_ids.add("")
            self.tables.append((section_ids, frame["rows"]))
        if frame["id"]:
            item = (text, frame["links"])
            if tag == "section" or tag in HEADINGS:
                self.records[frame["id"]] = item
            if tag == "li" and frame["id"].startswith("fn"):
                self.footnotes[frame["id"]] = item
        if self.stack and not frame["case_listing"]:
            self.stack[-1]["parts"].append(text)
            if tag in BLOCKS:
                self.stack[-1]["parts"].append("\n")
        if tag == "main":
            self.main = False
            if "" in self.targets:
                frame["targets"].append("")
        for identity in frame["targets"]:
            tables = [rows for owners, rows in self.tables if identity in owners]
            if frame["rows"]:
                tables.append(frame["rows"])
            self.exact[identity] = text, frame["links"], tables


def section_exports(site, files, commit):
    directory = site / "agent"
    subject = json.loads(files.text(site / "terminology/subject-index.json"))
    entries = []
    routes = {}
    for volume in subject["volumes"]:
        path = volume["path"]
        parser = PassageParser()
        parser.feed(files.text(site / path))
        sections = []
        headings = dict(volume["headings"])
        for anchor, heading in volume["headings"]:
            body, links = parser.records[anchor]
            notes = {link[1:]: parser.footnotes[link[1:]][0].strip() for link in links
                     if link.startswith("#") and link[1:] in parser.footnotes}
            page_url = BOOK + path + "#" + anchor
            route = f'agent/sections/{volume["id"]}/{artifact_anchor(anchor)}.json'
            if "/" in anchor or "\\" in anchor or anchor in {".", ".."}:
                raise ValueError("Invalid agent passage anchor: " + anchor)
            value = dict(source_commit=commit, chapter=volume["title"], heading=heading, url=page_url,
                         heading_path=[headings[part] for part in parser.ancestors[anchor] if part in headings and part != anchor] + [heading],
                         tables=[rows for owners, rows in parser.tables if anchor in owners],
                         text=re.sub(r"\n[ \t]*\n(?:[ \t]*\n)*", "\n\n", body).strip(),
                         links=sorted({urljoin(page_url, link) for link in links
                                       if urljoin(page_url, link).startswith(("http://", "https://"))}),
                         footnotes=notes)
            files.write(site / route, serialize(value))
            sections.append(dict(anchor=anchor, heading=heading, file=route))
            routes[path, anchor] = route
        entries.append(dict(id=volume["id"], title=volume["title"], path=path, sections=sections))
    files.write(directory / "sections.json", serialize(dict(source_commit=commit, volumes=entries)))
    return routes


def section_target(url, *, study=False):
    """Resolve a publication URL while retaining the exact rendered fragment."""
    parts = urlsplit(url)
    path = PurePosixPath(parts.path)
    if parts.scheme or parts.netloc or path.is_absolute() or ".." in path.parts or path.suffix != ".html":
        raise ValueError("Invalid discovery destination: " + url)
    anchor = unquote(parts.fragment)
    if any(c in anchor for c in ("/", "\\")) or anchor in {".", ".."}:
        raise ValueError("Invalid discovery anchor: " + url)
    return path.as_posix(), anchor or ("current-decision" if study else "")


def attach_sections(site, files, commit, records, routes):
    """Bind primary and alternate discovery locators to rendered passages."""
    pending = {}
    evidence_paths = {}
    for row in records:
        for destination in [row, *row.get("locators", [])]:
            path, anchor = section_target(destination["url"], study=destination.get("kind") == "study")
            key = path, anchor
            if key not in routes:
                stem = PurePosixPath(path).with_suffix("")
                # Keep the root file distinct from every possible fragment name.
                route = (f"agent/passages/{stem}/anchors/{artifact_anchor(anchor)}.json"
                         if anchor else f"agent/passages/{stem}/page.json")
                routes[key] = route
                pending.setdefault(path, set()).add(anchor)
            destination["section_url"] = BOOK + quote(routes[key], safe="/")
            evidence_paths.setdefault(row["id"], site / routes[key])
    for path, anchors in pending.items():
        parser = PassageParser(anchors)
        parser.feed(files.text(site / path))
        for anchor in sorted(anchors):
            if anchor not in parser.exact:
                raise ValueError(f"Discovery passage is missing from main content: {path}#{anchor}")
            text, links, tables = parser.exact[anchor]
            url = BOOK + path + ("#" + quote(anchor, safe=".:_-") if anchor else "")
            notes = {link[1:]: parser.footnotes[link[1:]][0].strip() for link in links
                     if link.startswith("#") and link[1:] in parser.footnotes}
            value = dict(source_commit=commit, url=url, text=re.sub(r"\n\s*\n", "\n\n", text).strip(), tables=tables,
                         links=sorted({urljoin(url, link) for link in links if urljoin(url, link).startswith(("http://", "https://"))}),
                         footnotes=notes)
            if not value["text"]:
                raise ValueError("Empty discovery passage: " + url)
            files.write(site / routes[path, anchor], serialize(value))
    return evidence_paths


EVIDENCE_FIELDS = ("id", "kind", "title", "measurement", "summary", "disposition", "method", "limit",
                   "source_section", "outside_question", "unmeasured", "case_id", "case_sources",
                   "result_sha256", "protocol_sha256", "featured_run")


def attach_evidence(files, records, routes, commit, read):
    """Include the evidence and its provenance in the same fetch as the passage."""
    from book_knowledge_graph import declaration_cards

    declarations = {}
    for card in declaration_cards(read).values():
        lines = read(card["module_path"]).decode().splitlines()
        for row in card["declarations"]:
            path = row["origin"]["path"]
            line = int(row["origin"]["locator"].removeprefix("line:"))
            # These reviewed declarations all start at column one. Bound the
            # excerpt at the first proof delimiter, before any next declaration.
            excerpt = "\n".join(lines[line-1:line+20])
            statement, separator, _ = excerpt.partition(":= by")
            if not separator or re.search(r"\n(?:theorem|lemma|def|end)\s", statement):
                raise ValueError("Cannot isolate theorem signature: " + row["name"])
            declarations[row["name"]] = dict(statement=statement.rstrip(), premises=row["premises"],
                                              conclusion=row["conclusion"],
                                              url=f"https://github.com/corbensorenson/asi-stack-book/blob/{commit}/{path}#L{line}")
    by_file = {}
    for row in records:
        path = routes.get(row["id"])
        if path is None:
            continue
        packet = {field: row[field] for field in EVIDENCE_FIELDS if field in row}
        if row.get("source_commit"):
            packet["evidence_revision"] = row["source_commit"]
        if row.get("locators"):
            packet["locators"] = row["locators"]
        if row.get("measurement") == "Formal declaration":
            packet["declaration"] = declarations[row["title"]]
        by_file.setdefault(path, []).append(packet)
    for path, packets in by_file.items():
        passage = json.loads(files.text(path))
        passage["evidence"] = packets
        files.write(path, serialize(passage))


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"


def lookup_rows(records):
    """Keep one small record per determining route for batched reading."""
    rows = []
    for row in records:
        identity = row["id"]
        if identity.startswith("evidence_passage:bibliography-") or (
                identity.endswith("-download") and row["title"].endswith("-replay.zip")):
            continue
        rows.append({key: row[key] for key in ("id", "title", "aliases", "question", "section_url") if key in row})
    return rows


def scifact_lookup_rows(records):
    """Keep the two linked research studies and their deciding chapter passages together."""
    return lookup_rows(row for row in records if row["id"] in SCIFACT_CHAPTER_RECORDS or any(
        urlsplit(destination["url"]).path in SCIFACT_STUDY_PAGES
        for destination in (row, *row.get("locators", []))))


def publish(site, files, commit, read):
    routes = section_exports(site, files, commit)
    graph = site / DIRECTORY
    manifest = json.loads((graph / "manifest.json").read_bytes())
    catalog = json.loads((graph / manifest["evidence_catalog"]).read_bytes())
    if catalog["snapshot_id"] != manifest["snapshot_id"] or catalog["source_commit"] != commit:
        raise ValueError("Agent index differs from the graph revision")
    # Keep discovery distinct from exact case lookup and the downloadable bulk graph.
    fields = ("id", "kind", "title", "aliases", "question", "measurement", "url", "locators")
    records = []
    source_by_id = {}
    for row in catalog["records"]:
        if row.get("measurement") == "Case identifier":
            continue
        record = {key: row[key] for key in fields if key in row}
        if row.get("measurement") == "Formal declaration":
            record.update(premises=row["limit"], conclusion=row["summary"],
                          title=row["title"].replace("_", " "))
        elif row.get("record_version") or (row.get("disposition") and row.get("locators")):
            record.update(summary=row.get("summary"), disposition=row.get("disposition"), limit=row.get("limit"))
        if row.get("measurement") == "Worked sensitivity calculation":
            record.update(disposition=row["disposition"], limit=row["limit"])
        records.append(record)
        source_by_id[row["id"]] = row
    primary = attach_sections(site, files, commit, records, routes)
    # Alternate locators carry their own canonical URL and text. Add the
    # evidence only to each record's deciding passage.
    enriched = [dict(source_by_id[record["id"]], locators=record.get("locators", [])) for record in records]
    attach_evidence(files, enriched, primary, commit, read)
    files.write(site / "agent/discovery.json", serialize(dict(source_commit=commit, snapshot_id=manifest["snapshot_id"], records=records)))
    files.write(site / "agent/lookup.json", serialize(dict(source_commit=commit, snapshot_id=manifest["snapshot_id"], records=lookup_rows(records))))
    files.write(site / SCIFACT_LOOKUP, serialize(dict(source_commit=commit, snapshot_id=manifest["snapshot_id"],
                                                        records=scifact_lookup_rows(records))))
    index = dict(schema_version="asi-stack.agent-index.v1", book_url=BOOK, source_commit=commit,
                 snapshot_id=manifest["snapshot_id"], lookup=dict(algorithm="sha256", encoding="UTF-8",
                 prefix_length=manifest["shard_prefix_length"], template=DIRECTORY+manifest["shard_template"]),
                 evidence_lookup=dict(catalog="agent/lookup.json", match="id, title, aliases, or question",
                                      topics={"SciFact": SCIFACT_LOOKUP},
                                      read="Open section_url for the passage, evidence scope, and citation. Cite its url."),
                 evidence_discovery="agent/discovery.json", terms=DIRECTORY+"dictionary.json",
                 section_index="agent/sections.json", section_template="agent/sections/{volume_id}/{anchor}.json",
                 proof_declarations="products/evidence-registry/proof-declarations.html",
                 graph_manifest=DIRECTORY+"manifest.json",
                 citation_history="products/evidence-registry/citation-history.html",
                 reader_skill="products/evidence-registry/SKILL.md",
                 cli="products/evidence-registry/read_book.py",
                 example="agent/scifact-claim-7.md")
    files.write(site / "agent-index.json", serialize(index))
    files.write(site / "llms.txt", """# The ASI Stack

> Corben Sorenson’s living technical book on governed AI systems and the evidence behind its comparisons.

- [Agent index](agent-index.json) provides the revision, lookup rules, and routes below.
- [Look up several evidence topics in one read](agent/lookup.json). Keep the returned section URLs and open those passages together.
- [Look up SciFact studies and cases](agent/topics/scifact.json) when every clue concerns scientific citation. Use the same section links.
- [Discover evidence](agent/discovery.json) by title, alias, or question. Open a result’s `section_url` to read and cite its exact passage. Use the stable ID for graph relationships or case provenance.
- [Look up an AI term](products/evidence-registry/knowledge-graph/dictionary.json) by headword or alias.
- [Read one section](agent/sections.json) by chapter and anchor. Follow its canonical URL when citing.
- [Replay SciFact claim 7](agent/scifact-claim-7.md) from the observation and result pointers.
- [Reader instructions](products/evidence-registry/SKILL.md) explain how to cite scope and trace a correction.
""")
    files.write(site / "agent/scifact-claim-7.md", """# Replay SciFact claim 7

Use the identifier `evidence_case:three-paper-selection--7` with the [agent index](../agent-index.json). The book's shard rule is SHA-256 over the UTF-8 record ID. Use the first two lowercase hex characters in the shard template. Select the ID from `records` and match the shard and index snapshot IDs.

Download [read_book.py](../products/evidence-registry/read_book.py), then run `python3 read_book.py --scifact-example` with Python 3.10 or later. It verifies the pinned file digests, resolves the two published JSON Pointers, reproduces the first-paper and three-paper decisions from the retained model readings, and checks each against the reported result.

Both policies held this claim. The first used two readings and 157 input tokens on paper 10511066. The wider selector used six readings and 615 input tokens, then selected paper 25847842. A held claim supplies no justified verdict. Cite the case, the book and evidence revisions, and the scope of the paired study.

[Published case](../products/evidence-registry/study-citation-retrieval.html#run-three-paper-selection--case-7)
""")
