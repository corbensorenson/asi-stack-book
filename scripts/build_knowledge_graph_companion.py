#!/usr/bin/env python3
"""Prepare a static reader companion and bounded machine packets."""

from collections import defaultdict
from gzip import GzipFile
from hashlib import sha256
from io import BytesIO
import json

import book_knowledge_graph as kg
from schema_validation import validate_value


COMPANION_DIR = "evidence-registry/knowledge-graph"
WEB = "assets/knowledge-graph/"
ASSET_NAMES = ("index.html", "explorer.css", "explorer.js")
GRAPH_SCHEMA = "schemas/book_knowledge_graph.schema.json"
COMPILER_INPUTS = (
    kg.STRUCTURE, kg.INVENTORY, kg.PAPER_LIBRARY, kg.GLOSSARY, kg.READER_MANIFEST, kg.CROSSWALK,
    kg.CLAIMS, *kg.CLAIM_ADDENDA, kg.IDENTITIES, kg.PROOFS, kg.STUDIES,
    "scripts/book_knowledge_graph.py", "scripts/build_knowledge_graph_companion.py",
    "scripts/build_human_reader_current.py", "scripts/research_case_rows.py",
    "scripts/research_studies.py", GRAPH_SCHEMA, *(WEB + name for name in ASSET_NAMES),
)
SHARD_WIDTH = 2
PREVIEWS_PER_RELATION = 4
PACKET_EDGE_LIMIT = 28
RELATION_PAGE_SIZE = 16
RELATION_FILE_LIMIT = 96 * 1024


def input_paths(read):
    manifest = json.loads(read(kg.READER_MANIFEST))
    return (*COMPILER_INPUTS, *(kg.READER + row["source_file"] for row in manifest["units"]))


def shard_id(node_id):
    return sha256(node_id.encode()).hexdigest()[:SHARD_WIDTH]


def compressed(data):
    buffer = BytesIO()
    with GzipFile(fileobj=buffer, mode="wb", compresslevel=6, mtime=0, filename="") as archive:
        archive.write(data)
    return buffer.getvalue()


class RelationshipFiles:
    """Pack independently addressable pages into bounded static files."""

    def __init__(self, snapshot):
        self.prefix = b'{"snapshot_id":' + json.dumps(snapshot).encode() + b',"pages":['
        self.pending = []
        self.files = {}
        self.size = len(self.prefix) + 3

    def flush(self):
        if self.pending:
            self.files[f"relationships/{len(self.files)}.json"] = self.prefix + b",".join(self.pending) + b"]}\n"
            self.pending.clear()
            self.size = len(self.prefix) + 3

    def store(self, page):
        data = kg.json_bytes(page).rstrip(b"\n")
        if len(data) + len(self.prefix) + 4 > RELATION_FILE_LIMIT:
            raise ValueError("A knowledge graph relationship page exceeds its byte limit")
        if self.size + len(data) + 1 > RELATION_FILE_LIMIT:
            self.flush()
        address = [len(self.files), len(self.pending)]
        self.pending.append(data)
        self.size += len(data) + 1
        return address

    def paginate(self, items):
        return [self.store(items[start:start + RELATION_PAGE_SIZE])
                for start in range(0, len(items), RELATION_PAGE_SIZE)]


def prepare(read, *, source_commit, worktree):
    graph = kg.compile_graph(read, source_commit=source_commit, worktree=worktree)
    schema = read(GRAPH_SCHEMA)
    errors = validate_value(graph, json.loads(schema), "knowledge graph")
    if errors:
        raise ValueError("; ".join(errors[:5]))
    nodes = {node["id"]: node for node in graph["nodes"]}
    groups = defaultdict(list)
    omissions = defaultdict(list)
    for row in graph["unresolved"]:
        omissions[row["from"]].append(row)
    for edge in graph["edges"]:
        groups[edge["from"]].append((edge["predicate"], "out", edge["to"], edge))
        groups[edge["to"]].append((edge["predicate"], "in", edge["from"], edge))

    kinds = sorted(graph["coverage"]["nodes"])
    catalog = []
    record_positions = {key: i for i, key in enumerate(nodes)}
    shards = defaultdict(dict)
    overflow = RelationshipFiles(graph["snapshot_id"])
    priorities = {predicate: i for i, predicate in enumerate(kg.NAVIGATION_PRIORITY)}
    for key, node in nodes.items():
        shard = shard_id(key)
        title = kg.title_excerpt(node["title"])
        catalog.append([key, kinds.index(node["kind"]), title, shard, *kg.search_metadata(node, title)])
        relation_groups = defaultdict(list)
        for predicate, direction, neighbor, edge in groups[key]:
            relation_groups[(predicate, direction)].append((neighbor, edge))
        relations = []
        remaining = PACKET_EDGE_LIMIT
        ordered = sorted(relation_groups, key=lambda pair: (priorities.get(pair[0], len(priorities)), pair))
        for predicate, direction in ordered:
            items = relation_groups[(predicate, direction)]
            if predicate == "owns_claim" and direction == "out":
                items.sort(key=lambda item: nodes[item[0]].get("role") != "core")
            if predicate == "retains_run" and direction == "out":
                items.sort(key=lambda item: not item[1]["qualifiers"]["featured"])
            count = min(len(items), PREVIEWS_PER_RELATION, remaining)
            rows = []
            for neighbor, edge in items:
                adjacent = nodes[neighbor]
                rows.append({"id": neighbor, "title": kg.title_excerpt(adjacent["title"]),
                             "origin": edge["origin"], "qualifiers": edge["qualifiers"]})
            remaining -= count
            group = {"predicate": predicate, "direction": direction, "total": len(items), "neighbors": rows[:count]}
            if count < len(items):
                group["pages"] = overflow.paginate(rows[count:])
            if len(items) > RELATION_PAGE_SIZE:
                group["member_index"] = overflow.store([record_positions[row["id"]] for row in rows])
            relations.append(group)
        gaps = omissions[key]
        packet = {"node": node, "relations": relations, "unresolved": len(gaps)}
        if gaps:
            packet["unresolved_pages"] = overflow.paginate(gaps)
        shards[shard][key] = packet

    snapshot = graph["snapshot_id"]
    files = {name: read(WEB + name) for name in ASSET_NAMES}
    files["graph.schema.json"] = schema
    files["search.json"] = kg.json_bytes({"schema_version": "asi-stack.knowledge-graph-search.v2",
                                        "snapshot_id": snapshot, "kinds": kinds, "records": catalog})
    files["graph.json.gz"] = compressed(kg.json_bytes(graph))
    for key, packets in shards.items():
        files[f"nodes/{key}.json"] = kg.json_bytes({"snapshot_id": snapshot, "records": packets})
    overflow.flush()
    files.update(overflow.files)
    manifest = {
        "schema_version": "asi-stack.knowledge-graph-companion.v1",
        "graph_schema_version": graph["schema_version"], "snapshot_id": snapshot,
        "source_commit": source_commit, "worktree": worktree, "authority": graph["authority"],
        "search": "search.json", "archive": "graph.json.gz", "shard_template": "nodes/{shard}.json",
        "relationship_template": "relationships/{file}.json",
        "coverage": graph["coverage"],
        "limits": {"preview_per_relation": PREVIEWS_PER_RELATION, "preview_edges_per_node": PACKET_EDGE_LIMIT,
                   "relationship_page_size": RELATION_PAGE_SIZE, "relationship_file_bytes": RELATION_FILE_LIMIT},
        "files": {path: {"sha256": sha256(raw).hexdigest(), "bytes": len(raw)}
                  for path, raw in sorted(files.items())},
    }
    files["manifest.json"] = kg.json_bytes(manifest)
    return files
