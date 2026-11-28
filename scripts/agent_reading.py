"""Publish small, revision-bound entry points and exports of rendered book sections."""
from html.parser import HTMLParser
import json
import re
from urllib.parse import urljoin

from research_dictionary import DIRECTORY

BOOK = "https://corbensorenson.github.io/asi-stack-book/"
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
SKIP = {"script", "style", "nav", "button", "svg", "iframe", "noscript", "template"}
HEADINGS = {"h2", "h3", "h4", "h5", "h6"}


class PassageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.records = {}
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
        frame = {"tag": tag, "id": identity, "blocked": blocked, "parts": [], "links": [], "cells": [], "rows": []}
        if identity and (tag == "section" or tag in HEADINGS):
            self.ancestors[identity] = [f["id"] for f in self.stack if f["tag"] == "section" and f["id"]]
        if tag not in VOID:
            self.stack.append(frame)
        if blocked:
            return
        if tag == "a" and attrs.get("href") and "anchorjs-link" not in attrs.get("class", ""):
            for parent in self.stack:
                parent["links"].append(attrs["href"])
        if tag in {"p", "li", "dt", "dd", "tr", "pre", "figcaption", "caption"} | HEADINGS:
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
            table = next((part for part in reversed(self.stack) if part["tag"] == "table"), None)
            if table is not None and frame["cells"]:
                table["rows"].append(frame["cells"])
        if tag == "table" and frame["rows"]:
            section_ids = {part["id"] for part in self.stack if part["tag"] == "section"}
            self.tables.append((section_ids, frame["rows"]))
        if frame["id"]:
            item = (text, frame["links"])
            if tag == "section" or tag in HEADINGS:
                self.records[frame["id"]] = item
            if tag == "li" and frame["id"].startswith("fn"):
                self.footnotes[frame["id"]] = item
        if self.stack:
            self.stack[-1]["parts"].append(text)
            if tag in {"p", "li", "dt", "dd", "tr", "pre", "figcaption", "caption"} | HEADINGS:
                self.stack[-1]["parts"].append("\n")
        if tag == "main":
            self.main = False


def section_exports(site, files, commit):
    directory = site / "agent"
    subject = json.loads(files.text(site / "terminology/subject-index.json"))
    entries = []
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
            route = f'agent/sections/{volume["id"]}/{anchor}.json'
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
        entries.append(dict(id=volume["id"], title=volume["title"], path=path, sections=sections))
    files.write(directory / "sections.json", serialize(dict(source_commit=commit, volumes=entries)))


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"


def publish(site, files, commit):
    section_exports(site, files, commit)
    graph = site / DIRECTORY
    manifest = json.loads((graph / "manifest.json").read_bytes())
    catalog = json.loads((graph / manifest["evidence_catalog"]).read_bytes())
    if catalog["snapshot_id"] != manifest["snapshot_id"] or catalog["source_commit"] != commit:
        raise ValueError("Agent index differs from the graph revision")
    # Keep discovery distinct from exact case lookup and the downloadable bulk graph.
    fields = ("id", "kind", "title", "aliases", "question", "measurement", "url")
    records = [{key: row[key] for key in fields if key in row} for row in catalog["records"]
               if row.get("measurement") != "Case identifier"]
    files.write(site / "agent/discovery.json", serialize(dict(source_commit=commit, snapshot_id=manifest["snapshot_id"], records=records)))
    index = dict(schema_version="asi-stack.agent-index.v1", book_url=BOOK, source_commit=commit,
                 snapshot_id=manifest["snapshot_id"], lookup=dict(algorithm="sha256", encoding="UTF-8",
                 prefix_length=manifest["shard_prefix_length"], template=DIRECTORY+manifest["shard_template"]),
                 evidence_discovery="agent/discovery.json", terms=DIRECTORY+"dictionary.json",
                 section_index="agent/sections.json", graph_manifest=DIRECTORY+"manifest.json",
                 citation_history="products/evidence-registry/citation-history.html",
                 reader_skill="products/evidence-registry/SKILL.md",
                 cli="products/evidence-registry/read_book.py",
                 example="agent/scifact-claim-7.md")
    files.write(site / "agent-index.json", serialize(index))
    files.write(site / "llms.txt", """# The ASI Stack

> Corben Sorenson’s living technical book on governed AI systems and the evidence behind its comparisons.

- [Agent index](agent-index.json) provides the revision, lookup rules, and routes below.
- [Discover evidence](agent/discovery.json) by title, alias, or question. Use the returned stable ID to fetch the record and its limits.
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
