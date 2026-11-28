#!/usr/bin/env python3
"""Run and replay the ASI Stack matched agent reading check."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import file_digest as hash_file, sha256
import importlib.util
import json
from pathlib import Path, PurePosixPath
import random
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from zipfile import BadZipFile, ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BOOK = "https://corbensorenson.github.io/asi-stack-book/"
RAW = "https://raw.githubusercontent.com/corbensorenson/asi-stack-book/"
INPUT_REPO = "https://github.com/corbensorenson/asi-stack-book/blob/"
LIMITS = dict(opens=18, display=52000, per_open=5500)
CRITERIA = ("decision", "citation", "scope")
DEFAULT_SUITE = HERE / "suite.json"


def load(path):
    return json.loads(path.read_bytes())


def digest(raw):
    return sha256(raw).hexdigest()


def file_digest(path):
    with path.open("rb") as stream:
        return hash_file(stream, "sha256").hexdigest()


def load_reader():
    spec = importlib.util.spec_from_file_location("matched_agent_reader", HERE.parent / "agent-batch-lookup/read.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_spec(path):
    spec = load(path)
    for path, expected in spec["inputs"].items():
        if file_digest(ROOT / path) != expected:
            raise ValueError("Frozen input changed: " + path)
    return spec


def archive_info(archive, arm, spec):
    with ZipFile(archive) as bundle:
        raw = bundle.read("tested-site-bundle.json")
        if digest(raw) != spec["editions"][arm]["bundle_manifest_sha256"]:
            raise ValueError("Tested bundle manifest differs from the frozen edition")
        manifest = json.loads(raw)
        if manifest["source_commit"] != spec["editions"][arm]["revision"]:
            raise ValueError("Corpus revision changed")
    return manifest


def canonical_route(route):
    if route.startswith(INPUT_REPO):
        route = RAW + route.removeprefix(INPUT_REPO)
    parts = urlsplit(route)
    if route.startswith(RAW):
        revision, _, name = route.removeprefix(RAW).split("#", 1)[0].partition("/")
        if not name or not re.fullmatch("[a-f0-9]{40}", revision) or ".." in PurePosixPath(unquote(name)).parts:
            raise ValueError("Source links need a pinned public revision")
        return route
    if parts.netloc and not route.startswith(BOOK):
        raise ValueError("Use the assigned book or a pinned public source in its repository")
    if parts.scheme and not route.startswith(BOOK):
        raise ValueError("Invalid book route")
    relative = urlsplit(route.removeprefix(BOOK))
    path = unquote(relative.path).lstrip("/")
    if ".." in PurePosixPath(path).parts or "\\" in path:
        raise ValueError("Unsafe book path")
    return (path or "index.html") + ("#" + relative.fragment if relative.fragment else "")


def site_member(bundle, route):
    path = "site/" + urlsplit(route).path
    if path.endswith("/"):
        path += "index.html"
    try:
        bundle.getinfo(path)
    except KeyError:
        path = path.rstrip("/") + "/index.html"
        bundle.getinfo(path)
    return path


def fetch(archive, route):
    if route.startswith(RAW):
        prefix = urlsplit(RAW).path
        revision, name = urlsplit(route).path.removeprefix(prefix).split("/", 1)
        result = subprocess.run(
            ["git", "show", f"{revision}:{unquote(name)}"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if result.returncode:
            raise KeyError("Pinned source is unavailable")
        return result.stdout
    with ZipFile(archive) as bundle:
        return bundle.read(site_member(bundle, route))


def get_display(raw, route, focus):
    reader = load_reader()
    if focus[:1] == ["--batch"]:
        if len(focus) < 2:
            raise ValueError("Supply at least one clue")
        return reader.batch(raw, focus[1:])
    return reader.reader.display(raw, route, " ".join(focus))


def read_session(args):
    spec = run_spec(args.suite)
    manifest = archive_info(args.archive, args.arm, spec)
    if args.panel not in spec["panels"]:
        raise ValueError("Unknown panel")
    if args.journal.exists():
        session = load(args.journal)
        if (session["arm"], session["panel"], session["revision"]) != (args.arm, args.panel, manifest["source_commit"]):
            raise ValueError("Journal belongs to another session")
    else:
        session = dict(arm=args.arm, panel=args.panel, revision=manifest["source_commit"], reads=[])
    reads = session["reads"]
    if not reads and args.route not in ("index.html", BOOK, BOOK+"index.html"):
        raise ValueError("Open the homepage first")
    remaining = LIMITS["display"] - sum(row.get("displayed_bytes", 0) for row in reads)
    if len(reads) >= LIMITS["opens"] or remaining <= 0:
        raise ValueError("Reading allowance exhausted")
    entry = dict(route=args.route, focus=args.focus)
    try:
        route = canonical_route(args.route)
        raw = fetch(args.archive, route)
        entry.update(canonical_route=route, bytes=len(raw), sha256=digest(raw))
        displayed = get_display(raw, route, args.focus)
        shown = displayed.encode()[:min(remaining, LIMITS["per_open"])].decode(errors="ignore")
        entry.update(displayed_bytes=len(shown.encode()), displayed_sha256=digest(shown.encode()))
        print(shown)
    except (KeyError, ValueError, OSError) as exc:
        entry["error"] = type(exc).__name__
        print("Resource unavailable")
    reads.append(entry)
    temporary = args.journal.with_suffix(".tmp")
    temporary.write_text(json.dumps(session, indent=2, ensure_ascii=False)+"\n")
    temporary.replace(args.journal)


def audit_log(archive, spec, session):
    arm = session["arm"]
    manifest = archive_info(archive, arm, spec)
    reads = session["reads"]
    if not reads or canonical_route(reads[0]["route"]) != "index.html":
        raise ValueError("Session did not open the homepage first")
    if session["revision"] != manifest["source_commit"] or len(reads) > LIMITS["opens"]:
        raise ValueError("Session revision or open count is invalid")
    files = {row["path"]: row for row in manifest["site"]["files"]}
    displayed = cumulative = 0
    unique = {}
    by_document = Counter()
    for row in reads:
        if displayed >= LIMITS["display"]:
            raise ValueError("Read after displayed allowance expired")
        if "bytes" not in row:
            if not row.get("error") or "sha256" in row:
                raise ValueError("Incomplete read journal entry")
            # Verify that the recorded failure really had no retrievable data.
            try:
                route = canonical_route(row["route"])
                fetch(archive, route)
            except (KeyError, ValueError, OSError):
                continue
            raise ValueError("Journal marked a readable resource unavailable")
        route = canonical_route(row["route"])
        if row["canonical_route"] != route:
            raise ValueError("Journal route mismatch")
        raw = fetch(archive, route)
        if not route.startswith(RAW):
            with ZipFile(archive) as bundle:
                relative = site_member(bundle, route).removeprefix("site/")
            asset = files[relative]
            if asset["sha256"] != digest(raw) or asset["size"] != len(raw):
                raise ValueError("Asset differs from tested manifest: " + route)
        if len(raw) != row["bytes"] or digest(raw) != row["sha256"]:
            raise ValueError("Read bytes differ from the journal")
        cumulative += len(raw)
        unique[row["sha256"]] = len(raw)
        by_document[urlsplit(route).path] += 1
        try:
            shown = get_display(raw, route, row["focus"])
        except (KeyError, ValueError, OSError) as exc:
            if row.get("error") != type(exc).__name__:
                raise ValueError("Read error differs from recorded error")
            continue
        visible = shown.encode()[:min(LIMITS["display"]-displayed, LIMITS["per_open"])].decode(errors="ignore").encode()
        if len(visible) != row["displayed_bytes"] or digest(visible) != row["displayed_sha256"]:
            raise ValueError("Displayed evidence differs from journal")
        displayed += len(visible)
    return dict(opens=len(reads), cumulative_bytes=cumulative, deduplicated_bytes=sum(unique.values()),
                displayed_bytes=displayed, discovery_opens=sum(n for key,n in by_document.items()
                if key in ("agent/discovery.json", "agent/lookup.json",
                           "products/evidence-registry/knowledge-graph/evidence-catalog.json")))


def grade_session(path, panel):
    answers = path.with_name(path.name.replace("-grades.json", "-answers.md"))
    raw = load(path)
    if raw["answer_sha256"] != file_digest(answers) or set(raw["questions"]) != set(panel["ids"]):
        raise ValueError("Grade does not match the answer file or panel")
    totals = Counter()
    for question, grade in raw["questions"].items():
        if any(type(grade[key]) is not bool for key in CRITERIA):
            raise ValueError("Every grade needs three boolean judgments")
        if not all(grade[key] for key in CRITERIA) and not grade.get("note"):
            raise ValueError("Record a rationale for every partial grade: " + question)
        totals.update({key: int(grade[key]) for key in CRITERIA})
    if type(raw["unsupported_numbers"]) is not int or raw["unsupported_numbers"] < 0:
        raise ValueError("Unsupported-number count must be nonnegative")
    return dict(totals, quality=sum(totals.values()), available=3*len(panel["ids"]),
                unsupported_numbers=raw["unsupported_numbers"])


def paired_interval(pairs, metric):
    rng = random.Random(20261128)
    differences = [candidate[metric]-baseline[metric] for baseline, candidate in pairs]
    bounds = sorted(sum(rng.choices(differences, k=len(pairs)))/len(pairs) for _ in range(5000))
    return [bounds[124], bounds[4874]]


def score(args):
    spec = run_spec(args.suite)
    archives = {"baseline":args.baseline, "candidate":args.candidate}
    for arm, archive in archives.items():
        if file_digest(archive) != spec["editions"][arm]["archive_sha256"]:
            raise ValueError("Corpus archive SHA-256 differs: " + arm)
    panels = {}
    for panel_id, panel in spec["panels"].items():
        arm_results = {}
        for arm, archive in archives.items():
            prefix = args.results / f"{panel_id}-{arm}"
            session = load(prefix.with_name(prefix.name+"-opens.json"))
            if (session["arm"], session["panel"]) != (arm, panel_id):
                raise ValueError("Session label differs from placement")
            reads = audit_log(archive, spec, session)
            grades = grade_session(prefix.with_name(prefix.name+"-grades.json"), panel)
            arm_results[arm] = {**reads, **grades}
        panels[panel_id] = arm_results
    totals = {arm: {key:sum(pair[arm][key] for pair in panels.values())
                   for key in next(iter(panels.values()))[arm]} for arm in archives}
    a, b = totals["baseline"], totals["candidate"]
    gates = dict(quality=b["quality"] >= a["quality"],
                 scope=b["scope"] >= a["scope"],
                 unsupported_numbers=b["unsupported_numbers"] <= a["unsupported_numbers"],
                 deduplicated_bytes=b["deduplicated_bytes"] < a["deduplicated_bytes"])
    pairs = [(value["baseline"], value["candidate"]) for value in panels.values()]
    result = dict(suite_revision=file_digest(args.suite), panels=panels, totals=totals,
                  gates=gates, regression_passed=all(gates.values()),
                  paired_intervals=dict(quality_points_per_panel=paired_interval(pairs,"quality"),
                                        deduplicated_bytes_per_panel=paired_interval(pairs,"deduplicated_bytes")))
    print(json.dumps(result, indent=2))
    return int(args.require_pass and not result["regression_passed"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action",required=True)
    read = sub.add_parser("read")
    read.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    read.add_argument("arm", choices=("baseline","candidate"))
    read.add_argument("panel")
    read.add_argument("archive", type=Path)
    read.add_argument("journal", type=Path)
    read.add_argument("route")
    read.add_argument("focus", nargs=argparse.REMAINDER)
    check = sub.add_parser("score")
    check.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    check.add_argument("--baseline", required=True,type=Path)
    check.add_argument("--candidate", required=True,type=Path)
    check.add_argument("--results", required=True,type=Path)
    check.add_argument("--require-pass",action="store_true")
    args = parser.parse_args()
    try:
        if args.action == "read":
            read_session(args)
            return 0
        return score(args)
    except (BadZipFile, KeyError, ValueError, OSError) as exc:
        parser.exit(2, f"{exc}\n")


if __name__ == "__main__":
    sys.exit(main())
