#!/usr/bin/env python3
"""Allocate approved timed reviews and separate answers from treatment assignments."""

import argparse
from collections import Counter, defaultdict
import gzip
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from statistics import median
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
EVIDENCE = "products/evidence-registry/knowledge-graph/evidence-catalog.json"
FLAGS = ("details_correct", "contradiction_recognized", "citation_usable", "scope_retained")
ARMS = ("ordinary", "linked")


def load(path):
    return json.loads(path.read_bytes())


def write(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def identity(site):
    catalog = load(site / EVIDENCE)
    status = load(site / "status/canonical-public-status.json")
    if status["source_commit"] != catalog["source_commit"] or status["source_tree_state"] != "clean":
        raise ValueError("The catalog does not match a clean tested revision")
    return {"source_commit": catalog["source_commit"], "snapshot_id": catalog["snapshot_id"],
            "tasks_sha256": sha256((HERE / "tasks.json").read_bytes()).hexdigest()}


def code_for(*parts):
    return sha256(":".join(map(str, parts)).encode()).hexdigest()[:20]


def allocate(site, blocks, seed, output):
    assignments = []
    used = set()
    tasks = load(HERE / "tasks.json")
    for number, (label, a, b) in enumerate(blocks):
        if a == b or {a, b} & used or not all(re.fullmatch(r"[A-Za-z0-9_-]{3,36}", p) for p in (a, b)):
            raise ValueError("Each block needs two distinct opaque participant codes")
        used.update([a, b])
        order = sorted(tasks, key=lambda row: code_for(seed, number, row["id"]))
        for index, task in enumerate(order):
            parity = (index + number) % 2
            for participant, arm in zip((a, b), ARMS[parity:] + ARMS[:parity], strict=True):
                assignments.append({"participant_code": participant, "block": label, "task": task["id"],
                                    "arm": arm, "position": index + 1,
                                    "pair_id": code_for("pair", seed, number, task["id"]),
                                    "session_code": code_for("session", seed, number, participant, task["id"])})
    write(output, {**identity(site), "assignments": assignments})


class FragmentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        self.ids.update(value for name, value in attrs if name == "id")


def resolves(site, citation):
    if not citation:
        return False
    url = urlsplit(citation)
    target = (site / unquote(url.path)).resolve()
    if url.scheme or url.netloc or not target.is_relative_to(site) or not target.is_file():
        return False
    if not url.fragment:
        return True
    parser = FragmentParser()
    parser.feed(target.read_text(encoding="utf-8"))
    return unquote(url.fragment) in parser.ids


def blind(site, allocation_file, responses_dir, output, key_output):
    allocation = load(allocation_file)
    binding = identity(site)
    if any(allocation[key] != value for key, value in binding.items()):
        raise ValueError("Allocation and tested site disagree")
    planned = {row["session_code"]: row for row in allocation["assignments"]}
    tasks = {row["id"]: row for row in load(HERE / "tasks.json")}
    catalog = load(site / EVIDENCE)
    evidence_urls = {row["id"]: row.get("url") for row in catalog["records"]}
    companion = (site / EVIDENCE).parent
    manifest = load(companion / "manifest.json")
    archive = (companion / "graph.json.gz").read_bytes()
    if sha256(archive).hexdigest() != manifest["files"]["graph.json.gz"]["sha256"]:
        raise ValueError("The graph archive hash does not match the manifest")
    graph = json.loads(gzip.decompress(archive))
    if graph["snapshot_id"] != binding["snapshot_id"]:
        raise ValueError("The graph and evidence catalog disagree")
    urls = {row["id"]: row.get("url") for row in graph["nodes"]}
    urls.update(evidence_urls)
    responses = []
    key_rows = []
    completed = set()
    if not responses_dir.is_dir():
        raise ValueError("The response directory is missing")
    for path in sorted(responses_dir.glob("*.json")):
        answer = load(path)
        session = answer["session_code"]
        assignment = planned.get(session)
        if session in completed or not assignment or assignment["task"] != answer["task"]:
            raise ValueError(f"{path.name} is duplicate or unallocated")
        if any(answer.get(key) != value for key, value in binding.items()):
            raise ValueError(f"{path.name} uses a different tested site or task set")
        timed = answer["active_review_ms"]
        if type(timed) is not int or timed < 0:
            raise ValueError(f"{path.name} has invalid active time")
        task = tasks[assignment["task"]]
        opened = answer["opened_ids"]
        starts = task["initial"]
        allowed = {"accept", "revise", "hold"} if task["study"] == "claim" else {"locate", "hold"}
        if (not isinstance(opened, list) or opened[:len(starts)] != starts or len(set(opened)) != len(opened)
                or len(opened) > len(starts) + 2 or any(key not in evidence_urls for key in opened[len(starts):])
                or answer["disposition"] not in allowed):
            raise ValueError(f"{path.name} has invalid evidence opens or disposition")
        citations = []
        for key in dict.fromkeys(re.split(r"[\s,]+", answer["citations"].strip())):
            if key:
                uri = urls.get(key)
                citations.append({"id": key, "path": uri, "opened": key in opened, "resolves": resolves(site, uri)})
        blind_id = code_for("grade", session)
        responses.append({"id": blind_id, "task": task["id"], "question": task["question"],
                          "disposition": answer["disposition"], "reason": answer["reason"],
                          "scope": answer["scope"], "citations": citations})
        key_rows.append({"id": blind_id, "task": task["id"], "arm": assignment["arm"],
                         "pair_id": assignment["pair_id"],
                         "disposition": answer["disposition"], "active_review_ms": timed,
                         "has_opened_resolving_citation": any(row["opened"] and row["resolves"] for row in citations)})
        completed.add(session)
    missing = Counter((row["task"], row["arm"]) for row in planned.values()
                      if row["session_code"] not in completed)
    write(output, sorted(responses, key=lambda row: row["id"]))
    write(key_output, {**binding, "responses": key_rows, "missing": [
        {"task": task, "arm": arm, "count": count} for (task, arm), count in sorted(missing.items())
    ]})


def report(key_file, grades_file, output):
    key = load(key_file)
    rows = key["responses"]
    grades = load(grades_file)
    by_id = {row["id"]: row for row in grades}
    if len(by_id) != len(grades) or set(by_id) != {row["id"] for row in rows}:
        raise ValueError("Provide exactly one final grade per completed response")
    if key["tasks_sha256"] != sha256((HERE / "tasks.json").read_bytes()).hexdigest():
        raise ValueError("The rubric no longer matches the response set")
    tasks = {row["id"]: row for row in load(HERE / "tasks.json")}
    groups = defaultdict(list)
    pairs = defaultdict(dict)
    for row in rows:
        task = tasks[row["task"]]
        grade = by_id[row["id"]]
        if any(type(grade.get(field)) is not bool for field in FLAGS):
            raise ValueError(f"{row['id']} lacks a binary final grade")
        if grade["citation_usable"] and not row["has_opened_resolving_citation"]:
            raise ValueError(f"{row['id']} has no opened, resolving citation to credit")
        outcome = {
            **{field: grade[field] for field in FLAGS},
            "correct_disposition": row["disposition"] == task["decision"],
            "active_review_ms": row["active_review_ms"],
            "false_promotion": task["study"] == "claim" and row["disposition"] == "accept" and task["decision"] != "accept",
            "missed_contradiction": task["contradiction"] and not grade["contradiction_recognized"],
        }
        groups[(task["study"], row["arm"])].append(outcome)
        pair = pairs[(task["study"], row["pair_id"])]
        if row["arm"] in pair:
            raise ValueError(f"{row['pair_id']} has a duplicate treatment")
        pair[row["arm"]] = outcome
    matched = defaultdict(list)
    for (study, _), pair in pairs.items():
        if set(pair) == set(ARMS):
            ordinary, linked = (pair[arm] for arm in ARMS)
            matched[study].append({field: linked[field] - ordinary[field] for field in linked})
    write(output, {**{field: key[field] for field in ("source_commit", "snapshot_id", "tasks_sha256")}, "groups": [
        {"study": study, "arm": arm, "completed": len(group),
         **{metric: sum(row[metric] for row in group) for metric in
            (*FLAGS, "correct_disposition", "false_promotion", "missed_contradiction")},
         "median_active_review_ms": median(row["active_review_ms"] for row in group)}
        for (study, arm), group in sorted(groups.items())
    ], "matched": [
        {"study": study, "complete_pairs": len(group),
         **{metric + "_linked_minus_ordinary": sum(row[metric] for row in group) for metric in
            (*FLAGS, "correct_disposition", "false_promotion", "missed_contradiction")},
         "median_paired_active_review_ms_linked_minus_ordinary": median(row["active_review_ms"] for row in group)}
        for study, group in sorted(matched.items())
    ], "missing": key["missing"]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    assigning = modes.add_parser("assign")
    assigning.add_argument("site", type=Path)
    assigning.add_argument("output", type=Path)
    assigning.add_argument("--seed", required=True)
    assigning.add_argument("--block", nargs=3, action="append", required=True,
                           metavar=("FAMILIARITY", "CODE_A", "CODE_B"))
    blinding = modes.add_parser("blind")
    for arg in ("site", "allocation", "responses", "output", "key_output"):
        blinding.add_argument(arg, type=Path)
    reporting = modes.add_parser("report")
    for arg in ("key", "grades", "output"):
        reporting.add_argument(arg, type=Path)
    args = parser.parse_args()
    if args.mode == "assign":
        allocate(args.site, args.block, args.seed, args.output)
    elif args.mode == "blind":
        blind(args.site.resolve(), args.allocation, args.responses, args.output, args.key_output)
    else:
        report(args.key, args.grades, args.output)


if __name__ == "__main__":
    main()
