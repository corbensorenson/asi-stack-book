#!/usr/bin/env python3
"""Read ASI Stack records and verify the SciFact example with Python's standard library."""
import argparse
from hashlib import sha256
import json
import re
from urllib.parse import urljoin
from urllib.request import urlopen

BOOK = "https://corbensorenson.github.io/asi-stack-book/"
EXAMPLE = "evidence_case:three-paper-selection--7"
STOP_WORDS = set("a an and are at be by can did do does for from how i in is it of on or should that the to was what when which who why with would you".split())


def fetch(url, expected=None):
    with urlopen(url, timeout=30) as response:
        data = response.read()
    if expected and sha256(data).hexdigest() != expected:
        raise ValueError("SHA-256 mismatch at " + url)
    return data


def pointer(document, location):
    if location == "":
        return document
    if not location.startswith("/"):
        raise ValueError("Invalid JSON pointer: " + location)
    for part in location[1:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def record(base, identity):
    index = json.loads(fetch(urljoin(base, "agent-index.json")))
    shard = sha256(identity.encode("utf-8")).hexdigest()[:index["lookup"]["prefix_length"]]
    url = urljoin(base, index["lookup"]["template"].format(shard=shard))
    packet = json.loads(fetch(url))
    if packet["snapshot_id"] != index["snapshot_id"]:
        raise ValueError("Publication changed during lookup. Retry from the agent index.")
    return index, packet["records"][identity]


def search_key(text):
    return " ".join(re.findall(r"\d+(?:\.\d+)?|[^\W\d_]+", text.casefold()))


def search_tokens(key):
    return set(key.split()) - STOP_WORDS


def find_records(records, queries, *, limit=2):
    """Rank stable IDs and exact clues before matching title and question words."""
    documents = []
    for row in records:
        titles = [row.get("id", ""), row.get("title", ""), *row.get("aliases", [])]
        named = [search_key(x) for x in titles if x]
        question = search_key(row.get("question", ""))
        terms = set().union(*(search_tokens(key) for key in [*named, question]))
        documents.append((row, named + [question], terms))
    results = []
    for query in queries:
        key = search_key(query)
        words = search_tokens(key)
        def score(entry):
            _, names, terms = entry
            named = max((len(search_tokens(name)) for name in names
                         if len(search_tokens(name)) >= 2 and f" {name} " in f" {key} "), default=0)
            return key in names, named, len(words & terms), -len(terms)
        ordered = sorted(documents, key=score, reverse=True) if words else []
        matches = [row for row, _, terms in ordered if words & terms][:limit]
        results.append(dict(query=query, matches=matches))
    return results


def find_passages(base, queries):
    index = json.loads(fetch(urljoin(base, "agent-index.json")))
    catalog = json.loads(fetch(urljoin(base, index["evidence_lookup"]["catalog"])))
    if (catalog["snapshot_id"], catalog["source_commit"]) != (index["snapshot_id"], index["source_commit"]):
        raise ValueError("Publication changed during lookup. Retry from the agent index.")
    matches = find_records(catalog["records"], queries)
    return dict(book_revision=index["source_commit"], queries=matches)


def read_inputs(references):
    documents = {}
    for ref in references:
        if ref["url"] not in documents:
            documents[ref["url"]] = json.loads(fetch(ref["url"], ref["sha256"]))
        yield pointer(documents[ref["url"]], ref["pointer"])


def replay_example(index, node):
    by_role = dict(zip((ref["role"] for ref in node["case_sources"]), read_inputs(node["case_sources"]), strict=True))
    case, observed = by_role["reported_result"], by_role["model_readings"]
    if case["id"] != 7 or observed["id"] != 7 or len(observed["candidates"]) != 3:
        raise ValueError("Citation does not identify the frozen claim 7 comparison")
    labels = ("CONTRADICT", "SUPPORT", "NEUTRAL")
    outcomes = {}
    for arm, size in (("first", 1), ("three", 3)):
        candidates = observed["candidates"][:size]
        scores = [list(map(sum, zip(*row["scores"], strict=True))) for row in candidates]
        rank = max(range(size), key=lambda i: max(scores[i][:2]) - scores[i][2])
        candidate = candidates[rank]
        verdict = labels[max(range(3), key=scores[rank].__getitem__)]
        annotation = candidate["annotation"] or {}
        justified = (annotation.get("provenance") == "citation" and bool(annotation["sentences"])
                     and set(annotation["sentences"]) <= set(candidate["cited"]) and verdict == annotation["label"])
        outcome = "held" if verdict == "NEUTRAL" else "justified" if justified else "unsupported"
        outcomes[arm] = dict(outcome=outcome, verdict=verdict, rank=rank+1, doc=candidate["doc"],
                             cited=candidate["cited"], readings=2*size,
                             tokens=sum(sum(row["tokens"]) for row in candidates))
    if outcomes != case["arms"]:
        raise ValueError("Replayed outcomes differ from the pinned report")
    return dict(case_id=7, arms=outcomes, limit=node["limit"], record_id=node["id"],
                passage_url=urljoin(index["book_url"], node["url"]), book_revision=index["source_commit"],
                evidence_revision=node["source_commit"], result_sha256=node["result_sha256"], inputs=node["case_sources"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=BOOK, help="Book root, with trailing slash")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--record", metavar="ID", help="Read a graph record and typed links")
    action.add_argument("--case-inputs", metavar="ID", help="Verify hashes and resolve the exact case pointers")
    action.add_argument("--scifact-example", action="store_true", help="Recompute both outcomes for SciFact claim 7")
    action.add_argument("--find", action="append", metavar="CLUE", help="Find up to two passage links per clue. Repeat for several clues in one request.")
    args = parser.parse_args()
    try:
        if args.find:
            answer = find_passages(args.base, args.find)
        else:
            index, packet = record(args.base, args.record or args.case_inputs or EXAMPLE)
            answer = {"book_revision": index["source_commit"], **packet}
            if args.case_inputs:
                answer["inputs"] = list(read_inputs(packet["node"]["case_sources"]))
            if args.scifact_example:
                answer = replay_example(index, packet["node"])
    except (OSError, KeyError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(answer, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
