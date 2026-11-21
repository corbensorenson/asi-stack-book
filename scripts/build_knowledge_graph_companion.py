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


def input_paths(read):
    manifest = json.loads(read(kg.READER_MANIFEST))
    return (*COMPILER_INPUTS, *(kg.READER + row["source_file"] for row in manifest["units"]))


def shard_id(node_id):
    return sha256(node_id.encode()).hexdigest()[:SHARD_WIDTH]


def title_excerpt(value, cap=180):
    if len(value) <= cap:
        return value
    return value[:cap - 1] + "…"


def compressed(data):
    buffer = BytesIO()
    with GzipFile(fileobj=buffer, mode="wb", compresslevel=6, mtime=0, filename="") as archive:
        archive.write(data)
    return buffer.getvalue()


def prepare(read, *, source_commit, worktree):
    graph = kg.compile_graph(read, source_commit=source_commit, worktree=worktree)
    schema = read(GRAPH_SCHEMA)
    errors = validate_value(graph, json.loads(schema), "knowledge graph")
    if errors:
        raise ValueError("; ".join(errors[:5]))
    nodes = {node["id"]: node for node in graph["nodes"]}
    groups = defaultdict(list)
    omissions = defaultdict(int)
    for row in graph["unresolved"]:
        omissions[row["from"]] += 1
    for edge in graph["edges"]:
        groups[edge["from"]].append((edge["predicate"], "out", edge["to"], edge))
        groups[edge["to"]].append((edge["predicate"], "in", edge["from"], edge))

    kinds = sorted(graph["coverage"]["nodes"])
    catalog = []
    shards = defaultdict(dict)
    priorities = {predicate: i for i, predicate in enumerate(kg.NAVIGATION_PRIORITY)}
    for key, node in nodes.items():
        shard = shard_id(key)
        catalog.append([key, kinds.index(node["kind"]), title_excerpt(node["title"]), shard])
        relation_groups = defaultdict(list)
        for predicate, direction, neighbor, edge in groups[key]:
            relation_groups[(predicate, direction)].append((neighbor, edge))
        relations = []
        remaining = PACKET_EDGE_LIMIT
        ordered = sorted(relation_groups, key=lambda pair: (priorities.get(pair[0], len(priorities)), pair))
        for predicate, direction in ordered:
            items = relation_groups[(predicate, direction)]
            count = min(len(items), PREVIEWS_PER_RELATION, remaining)
            rows = []
            for neighbor, edge in items[:count]:
                adjacent = nodes[neighbor]
                rows.append({"id": neighbor, "title": title_excerpt(adjacent["title"]),
                             "origin": edge["origin"], "qualifiers": edge["qualifiers"]})
            remaining -= count
            relations.append({"predicate": predicate, "direction": direction, "total": len(items), "neighbors": rows})
        shards[shard][key] = {"node": node, "relations": relations, "unresolved": omissions[key]}

    snapshot = graph["snapshot_id"]
    files = {name: read(WEB + name) for name in ASSET_NAMES}
    files["graph.schema.json"] = schema
    files["search.json"] = kg.json_bytes({"snapshot_id": snapshot, "kinds": kinds, "records": catalog})
    files["graph.json.gz"] = compressed(kg.json_bytes(graph))
    for key, packets in shards.items():
        files[f"nodes/{key}.json"] = kg.json_bytes({"snapshot_id": snapshot, "records": packets})
    manifest = {
        "schema_version": "asi-stack.knowledge-graph-companion.v1",
        "graph_schema_version": graph["schema_version"], "snapshot_id": snapshot,
        "source_commit": source_commit, "worktree": worktree, "authority": graph["authority"],
        "search": "search.json", "archive": "graph.json.gz", "shard_template": "nodes/{shard}.json",
        "coverage": graph["coverage"],
        "limits": {"preview_per_relation": PREVIEWS_PER_RELATION, "preview_edges_per_node": PACKET_EDGE_LIMIT},
        "files": {path: {"sha256": sha256(raw).hexdigest(), "bytes": len(raw)}
                  for path, raw in sorted(files.items())},
    }
    files["manifest.json"] = kg.json_bytes(manifest)
    return files
