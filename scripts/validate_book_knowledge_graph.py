#!/usr/bin/env python3
"""Check reproducibility and evidence and navigation invariants of the graph."""

from __future__ import annotations

from collections import Counter, defaultdict
import json

import book_knowledge_graph as kg


RETRIEVAL_TASKS = "experiments/knowledge_graph_navigation/retrieval_tasks.json"


def check_published_packets(directory, graph, manifest):
    snapshot = graph["snapshot_id"]
    assert manifest["snapshot_id"] == snapshot, "Archive snapshot identity differs from the companion"
    catalog = json.loads((directory / manifest["search"]).read_bytes())
    assert catalog["snapshot_id"] == snapshot
    positions = [row[0] for row in catalog["records"]]
    assert positions == [node["id"] for node in graph["nodes"]]
    limits = manifest["limits"]
    files = {}
    packets = {}
    for path in manifest["files"]:
        if path.startswith("relationships/") or path.startswith("nodes/"):
            raw = (directory / path).read_bytes()
            data = json.loads(raw)
            assert data["snapshot_id"] == snapshot, path
            if "pages" in data:
                assert len(raw) <= limits["relationship_file_bytes"], path
                files[path] = data["pages"]
            else:
                packets.update(data["records"])
    assert set(packets) == set(positions)

    def page(address):
        file, position = address
        return files[f"relationships/{file}.json"][position]

    adjacent = defaultdict(Counter)
    for edge in graph["edges"]:
        for direction, head, tail in (("out", "from", "to"), ("in", "to", "from")):
            row = {"id": edge[tail], "origin": edge["origin"], "qualifiers": edge["qualifiers"]}
            adjacent[edge[head], edge["predicate"], direction][kg.json_bytes(row)] += 1
    for key, packet in packets.items():
        assert sum(len(group["neighbors"]) for group in packet["relations"]) <= limits["preview_edges_per_node"], key
        for group in packet["relations"]:
            preview = group["neighbors"]
            assert len(preview) <= limits["preview_per_relation"], key
            pages = [page(address) for address in group.get("pages", ())]
            assert all(0 < len(rows) <= limits["relationship_page_size"] for rows in pages), key
            assert all(len(rows) == limits["relationship_page_size"] for rows in pages[:-1]), key
            rows = [*preview, *(row for segment in pages for row in segment)]
            relation = key, group["predicate"], group["direction"]
            actual = Counter(kg.json_bytes({k: v for k, v in row.items() if k != "title"}) for row in rows)
            assert len(rows) == group["total"] and adjacent.pop(relation) == actual, relation
            if len(rows) > limits["relationship_page_size"]:
                members = [positions[index] for index in page(group["member_index"])]
                assert members == [row["id"] for row in rows], relation
    assert not adjacent, "Published pages omit relationships from the archive"
    omitted = defaultdict(list)
    for gap in graph["unresolved"]:
        omitted[gap["from"]].append(gap)
    for key, packet in packets.items():
        gaps = [row for address in packet.get("unresolved_pages", ()) for row in page(address)]
        assert gaps == omitted[key] and len(gaps) == packet["unresolved"], key


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
    for task in json.loads(read(RETRIEVAL_TASKS)):
        hits = kg.search(graph, task["query"], kind=task["kind"], limit=3)["matches"]
        assert task["target"] in {hit["id"] for hit in hits}, task["query"]
    assert not kg.search(graph, "zzzxxy unrelated nonexistent term")["matches"]

    start, end = "reader_unit:unit-09", "study_run:verifier-floor-cache"
    route = kg.connection(graph, start, end)
    assert route["status"] == "found" and route["authority"] == "navigation_only"
    assert [row["predicate"] for row in route["edges"]] == [
        "teaches_chapter", "owns_claim", "investigates", "retains_run",
    ]
    assert nodes[end]["limit"] and nodes[end]["result_sha256"]
    assert kg.connection(graph, end, start)["nodes"] == list(reversed(route["nodes"]))
    assert kg.connection(graph, start, end, depth=3)["status"] == "no_route_within_depth"
    assert not kg.connection(graph, start, end, predicates=("atom",))["edges"]

    def changed_bytes(path):
        return read(path) + (b"\n" if path == kg.STRUCTURE else b"")

    assert compile_snapshot(changed_bytes)["snapshot_id"] != graph["snapshot_id"]
    assert kg.json_bytes(graph) == kg.json_bytes(compile_snapshot())
    print(f"Knowledge graph validated: {len(nodes)} nodes, {len(graph['edges'])} edges, and "
          f"{len(graph['unresolved'])} recorded unresolved references.")


if __name__ == "__main__":
    main()
