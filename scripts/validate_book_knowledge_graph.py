#!/usr/bin/env python3
"""Check reproducibility and evidence and navigation invariants of the graph."""

from __future__ import annotations

from collections import Counter
import json

import book_knowledge_graph as kg


def main():
    def read(path):
        return (kg.ROOT / path).read_bytes()

    def compile_snapshot(reader=read):
        return kg.compile_graph(reader, source_commit="0" * 40, worktree=True)

    graph = compile_snapshot()
    nodes = {node["id"]: node for node in graph["nodes"]}
    coverage = Counter(node["kind"] for node in nodes.values())
    book = json.loads(read(kg.STRUCTURE))
    chapters = [chapter for part in book["parts"] for chapter in part["chapters"]]
    assert coverage["chapter"] == len(chapters)
    assert coverage["reader_unit"] == len(json.loads(read(kg.READER_MANIFEST))["units"])
    assert coverage["source"] == len(json.loads(read(kg.INVENTORY)))
    papers = json.loads(read(kg.PAPER_LIBRARY))["records"]
    for position, row in enumerate(papers):
        source = nodes[f"source:{row['source_id']}"]
        assert source["url"] == f"papers/{row['source_id']}.html"
        assert source["publication_origin"] == {"path": kg.PAPER_LIBRARY, "locator": f"/records/{position}"}
    assert coverage["proof_target"] == len(json.loads(read(kg.PROOFS))["records"])
    assert coverage["transition"] == len(json.loads(read(kg.IDENTITIES))["records"])
    assert coverage["study_run"] == len(json.loads(read(kg.STUDIES))["runs"])
    assert graph["authority"] == "navigation_only"
    assert len(nodes) == len(graph["nodes"])
    assert all(edge["from"] in nodes and edge["to"] in nodes for edge in graph["edges"])
    assert all(
        edge["qualifiers"]["parent_support_state_effect"] == "none"
        for edge in graph["edges"] if edge["predicate"] in {"proxy_for", "subclaim_of"}
    )

    sources_by_chapter = {chapter["id"]: set(chapter["source_ids"]) for chapter in chapters}
    for edge in graph["edges"]:
        if edge["predicate"] == "assigned_to" and edge["qualifiers"]["via_alias"]:
            slug = edge["to"].split(":", 1)[1]
            source = edge["from"].split(":", 1)[1]
            assert source in sources_by_chapter[slug]
    assert not any(row["from"].startswith("source:ext_") for row in graph["unresolved"])
    for query in ("e-means", "source:ext_emeans_2026"):
        match = kg.search(graph, query, kind="source", limit=2)["matches"][0]
        assert match["id"] == "source:ext_emeans_2026"
    replies = kg.neighborhood(graph, match["id"], depth=2, limit=10,
                              predicates=("assigned_to", "teaches_chapter"))
    assert {"reader_unit:unit-14", "reader_unit:unit-23"} <= {node["id"] for node in replies["nodes"]}
    assert replies["truncated"] and len(replies["edges"]) == 10
    rollout = kg.neighborhood(graph, "study:verifier-rollout", predicates=("retains_run", "investigates"))
    assert {edge["to"] for edge in rollout["edges"]} == {
        "claim:stable-capability-fields.core", "study_run:verifier-floor-cache", "study_run:verifier-paired",
    }
    assert nodes["claim:stable-capability-fields.core"]["state"] == "argument"

    def changed_bytes(path):
        return read(path) + (b"\n" if path == kg.STRUCTURE else b"")

    assert compile_snapshot(changed_bytes)["snapshot_id"] != graph["snapshot_id"]
    assert kg.json_bytes(graph) == kg.json_bytes(compile_snapshot())
    print(f"Knowledge graph validated: {len(nodes)} nodes, {len(graph['edges'])} edges, and "
          f"{len(graph['unresolved'])} recorded unresolved references.")


if __name__ == "__main__":
    main()
