#!/usr/bin/env python3
"""Freeze another comparison or preserve the assets needed to audit a completed run."""

import argparse
import json
from pathlib import Path
import re
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile, ZipInfo

from regression import (
    DEFAULT_SUITE, RAW, ROOT, archive_info, canonical_route, digest, file_digest,
    load, run_spec, site_member,
)


def identify(archive):
    with ZipFile(archive) as bundle:
        raw = bundle.read("tested-site-bundle.json")
        manifest = json.loads(raw)
        missing = {"site/" + row["path"] for row in manifest["site"]["files"]}.difference(bundle.namelist())
        if missing:
            raise ValueError(f"{archive} is missing {len(missing)} site assets; use the full tested bundle")
    return dict(revision=manifest["source_commit"], artifact_name=manifest["artifact_name"],
                archive_sha256=file_digest(archive), bundle_manifest_sha256=digest(raw))


def save(path, data):
    with path.open("x") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")


def archives(args):
    return {"baseline": args.baseline, "candidate": args.candidate}


def freeze(args):
    suite = load(args.template)
    frozen_paths = set(suite["inputs"])
    frozen_paths.difference_update(panel["path"] for panel in suite["panels"].values())
    if args.rubric:
        original = str(DEFAULT_SUITE.with_name("rubric.md").relative_to(ROOT))
        frozen_paths.discard(suite.get("rubric_path", original))
        suite["rubric_path"] = str(args.rubric.resolve().relative_to(ROOT))
        frozen_paths.add(suite["rubric_path"])
    if args.panels:
        suite["panels"] = {}
        for path in sorted(args.panels.glob("*.md")):
            name = str(path.resolve().relative_to(ROOT))
            ids = re.findall(r"^\*\*([A-Z]{2}\d+)\.\*\*", path.read_text(), re.MULTILINE)
            if not ids:
                raise ValueError(f"No question IDs found in {path}")
            suite["panels"][path.stem] = dict(path=name, ids=ids)
    panels = suite["panels"].values()
    ids = [identity for panel in panels for identity in panel["ids"]]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Question IDs must be nonempty and unique across the suite")
    frozen_paths.update(panel["path"] for panel in panels)
    suite["inputs"] = {name: file_digest(ROOT / name) for name in sorted(frozen_paths)}
    for arm, archive in archives(args).items():
        edition = identify(archive)
        old = suite["editions"][arm]
        if old["archive_sha256"] != edition["archive_sha256"]:
            suite["editions"][arm] = edition
    save(args.output, suite)


def write_replay_archive(source, target, members):
    with ZipFile(source) as full, ZipFile(target, "x") as replay:
        for name in sorted(members):
            row = ZipInfo(name)
            replay.writestr(row, full.read(name), compress_type=ZIP_DEFLATED, compresslevel=9)


def pack(args):
    suite = run_spec(args.suite)
    for arm, archive in archives(args).items():
        edition = suite["editions"][arm]
        if edition["archive_sha256"] != file_digest(archive):
            raise ValueError(f"Original archive SHA-256 differs for {arm}")
        manifest = archive_info(archive, arm, suite)
        files = {row["path"] for row in manifest["site"]["files"]}
        members = {"tested-site-bundle.json"}
        with ZipFile(archive) as bundle:
            for panel in suite["panels"]:
                log = load(args.results / f"{panel}-{arm}-opens.json")
                for row in log["reads"]:
                    try:
                        route = canonical_route(row["route"])
                        if route.startswith(RAW):
                            continue
                        name = site_member(bundle, route)
                    except (KeyError, ValueError):
                        if "bytes" in row:
                            raise
                        continue
                    if name.removeprefix("site/") not in files:
                        raise ValueError(f"Replay member is outside the tested manifest: {name}")
                    members.add(name)
        target = args.results / f"{arm}-replay.zip"
        write_replay_archive(archive, target, members)
        edition.update(original_archive_sha256=edition["archive_sha256"],
                       archive_sha256=file_digest(target), replay_archive=target.name)
    save(args.results / "replay-suite.json", suite)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)
    fresh = sub.add_parser("freeze")
    fresh.add_argument("--template", type=Path, default=DEFAULT_SUITE)
    fresh.add_argument("--panels", type=Path, help="Directory of Markdown panels inside the repository")
    fresh.add_argument("--rubric", type=Path, help="Alternative scoring rubric inside the repository")
    fresh.add_argument("--output", type=Path, required=True)
    fresh.set_defaults(action=freeze)
    replay = sub.add_parser("pack")
    replay.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    replay.add_argument("--results", type=Path, required=True)
    replay.set_defaults(action=pack)
    for command in (fresh, replay):
        command.add_argument("--baseline", type=Path, required=True)
        command.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        args.action(args)
    except (BadZipFile, KeyError, OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")


if __name__ == "__main__":
    main()
