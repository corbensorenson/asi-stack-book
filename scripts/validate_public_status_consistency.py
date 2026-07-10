#!/usr/bin/env python3
"""Reject contradictory active status claims and optionally audit rendered navigation."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from build_canonical_public_status import (
    CONFIG,
    GENERATED_STATUS_BEGIN,
    GENERATED_STATUS_END,
    ROOT,
    build_status,
    load_json,
    public_status_summary_block,
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_depth = 0
        self.anchor_depth = 0
        self.h1_text: list[str] = []
        self.h1_values: list[str] = []
        self.sidebar_links: list[tuple[str, str]] = []
        self._anchor_href = ""
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "h1":
            self.h1_depth += 1
            self.h1_text = []
        if tag == "a" and "sidebar-item-text" in attr.get("class", "").split():
            self.anchor_depth += 1
            self._anchor_href = attr.get("href", "")
            self._anchor_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1" and self.h1_depth:
            self.h1_depth -= 1
            self.h1_values.append(" ".join("".join(self.h1_text).split()))
        if tag == "a" and self.anchor_depth:
            self.anchor_depth -= 1
            self.sidebar_links.append((" ".join("".join(self._anchor_text).split()), self._anchor_href))

    def handle_data(self, data: str) -> None:
        if self.h1_depth:
            self.h1_text.append(data)
        if self.anchor_depth:
            self._anchor_text.append(data)


PATTERNS: tuple[tuple[str, re.Pattern[str], tuple[str, ...]], ...] = (
    ("source_count", re.compile(r"\b(?P<value>\d+)\s+public-safe\s+(?:source\s+)?records?\b", re.I), ("sources",)),
    ("core_claim_count", re.compile(r"\b(?P<value>\d+)\s+(?:chapter[- ]core|core\s+chapter)\s+claims?\b", re.I), ("chapters",)),
    ("chapter_count", re.compile(r"\b(?P<value>\d+)\s+manifest\s+chapters?\b", re.I), ("chapters",)),
    ("chapter_count", re.compile(r"\bAll\s+(?P<value>\d+)\s+chapters?\b", re.I), ("chapters",)),
    ("chapter_count", re.compile(r"\b(?P<value>\d+)\s+source-noted\s+chapters?\b", re.I), ("chapters",)),
    ("chapter_count", re.compile(r"\b(?P<value>\d+)-chapter\s+(?:grounding|evidence-lane)\b", re.I), ("chapters",)),
    ("chapter_count", re.compile(r"\bcurrent\s+(?P<value>\d+)-chapter\s+manifest\b", re.I), ("chapters",)),
    ("core_claim_count", re.compile(r"\b(?P<value>\d+)\s+per-chapter\s+core-claim\s+dispositions\b", re.I), ("chapters",)),
    ("core_claim_count", re.compile(r"\ball\s+(?P<value>\d+)\s+(?:chapter\s+core\s+claims\s+)?remain\s+at\s+`?argument`?\b", re.I), ("chapters",)),
    (
        "external_positioning_count",
        re.compile(r"\b(?P<left>\d+)\s*(?:/|of)\s*(?P<right>\d+)\s+chapters?\s+(?:externally\s+positioned|currently\s+have\s+in-prose|have\s+`?ext_)", re.I),
        ("externally_positioned_chapters", "chapters"),
    ),
)


def expected_metric(status: dict[str, Any], metric: str) -> int:
    if metric == "source_count":
        return int(status["counts"]["sources"])
    if metric in {"chapter_count", "core_claim_count"}:
        return int(status["counts"]["chapters"])
    if metric == "external_positioning_count":
        return int(status["counts"]["externally_positioned_chapters"])
    raise KeyError(metric)


def active_lines(text: str, config: dict[str, Any]) -> list[tuple[int, str]]:
    markers = config["historical_scope_markers"]
    historical = False
    rows: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if markers["begin"] in line:
            historical = True
            continue
        if markers["end"] in line:
            historical = False
            continue
        if historical or markers["line"] in line:
            continue
        rows.append((number, line))
    if historical:
        raise ValueError("unterminated canonical-status historical block")
    return rows


def scan_surface(path: Path, status: dict[str, Any], config: dict[str, Any]) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    observed: set[str] = set()
    for line_number, line in active_lines(path.read_text(encoding="utf-8", errors="ignore"), config):
        for metric, pattern, keys in PATTERNS:
            for match in pattern.finditer(line):
                observed.add(metric)
                expected = expected_metric(status, metric)
                if "value" in match.groupdict():
                    values = [int(match.group("value"))]
                else:
                    values = [int(match.group("left")), int(match.group("right"))]
                for value, key in zip(values, keys):
                    key_expected = int(status["counts"][key])
                    if value != key_expected:
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_number}: active {metric} value {value} "
                            f"does not match canonical {key}={key_expected}: {match.group(0)!r}"
                        )
                if metric == "external_positioning_count" and expected != int(status["counts"]["chapters"]):
                    errors.append("not every active chapter is externally positioned in the canonical status")
    return errors, observed


def validate_generated_block(path: Path, status: dict[str, Any]) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        re.escape(GENERATED_STATUS_BEGIN) + r".*?" + re.escape(GENERATED_STATUS_END),
        re.DOTALL,
    )
    blocks = pattern.findall(text)
    if len(blocks) != 1:
        return [
            f"{path.relative_to(ROOT)}: expected exactly one generated canonical-status block, "
            f"found {len(blocks)}"
        ]
    if blocks[0] != public_status_summary_block(status):
        return [f"{path.relative_to(ROOT)}: generated canonical-status block is stale or hand-edited"]
    return []


def validate_chapter_header_count_boundary(status: dict[str, Any]) -> list[str]:
    """Forbid independent active global counts in per-chapter header scaffolding."""
    errors: list[str] = []
    for row in status["chapter_order"]:
        path = ROOT / row["source_path"]
        text = path.read_text(encoding="utf-8", errors="ignore")
        header = text.split("\n## Problem", 1)[0]
        for line_number, line in enumerate(header.splitlines(), start=1):
            for metric, pattern, _ in PATTERNS:
                if pattern.search(line):
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: chapter header carries independent active "
                        f"{metric}; global status belongs to the canonical object"
                    )
    return errors


def run_negative_controls(status: dict[str, Any], config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    chapters = int(status["counts"]["chapters"])
    wrong = chapters - 1
    fixtures = [
        (f"All {wrong} manifest chapters exist.", True, "stale manifest count"),
        (f"{wrong}/{chapters} chapters externally positioned", True, "mismatched ratio"),
        (f"{config['historical_scope_markers']['line']} Historical: all {wrong} chapters.", False, "historical line marker"),
    ]
    for text, should_fail, label in fixtures:
        path = ROOT / "build" / "status" / f"negative-control-{label.replace(' ', '-')}.md"
        # Exercise the same line scanner without writing a fixture artifact.
        found = False
        for _, line in active_lines(text, config):
            for metric, pattern, keys in PATTERNS:
                for match in pattern.finditer(line):
                    values = [int(match.group("value"))] if "value" in match.groupdict() else [int(match.group("left")), int(match.group("right"))]
                    expected_values = [int(status["counts"][key]) for key in keys]
                    if values != expected_values:
                        found = True
        if found != should_fail:
            errors.append(f"negative control {label!r} expected failure={should_fail}, observed failure={found} ({path})")
    return errors


def normalize_href(href: str) -> str:
    value = href.split("?", 1)[0].split("#", 1)[0]
    while value.startswith("../"):
        value = value[3:]
    return value.lstrip("/")


def validate_rendered_site(site: Path, status: dict[str, Any], *, require_clean: bool) -> list[str]:
    errors: list[str] = []
    status_path = site / "status" / "canonical-public-status.json"
    if not status_path.exists():
        return [f"rendered site missing {status_path}"]
    rendered_status = json.loads(status_path.read_text(encoding="utf-8"))
    for key in ["active_version", "release_profile", "deployment_channel", "source_commit"]:
        if rendered_status.get(key) != status.get(key):
            errors.append(f"rendered status {key} does not match current build status")
    for key in ["chapters", "sources", "expected_book_pages", "externally_positioned_chapters"]:
        if rendered_status.get("counts", {}).get(key) != status["counts"][key]:
            errors.append(f"rendered status count {key} does not match current canonical count")
    if require_clean and rendered_status.get("source_tree_state") != "clean":
        errors.append("release site status must report a clean source tree")

    expected_paths = [row["public_path"] for row in status["chapter_order"]]
    for path in expected_paths:
        page = site / path
        if not page.exists():
            errors.append(f"rendered site missing chapter page: {path}")
            continue
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8", errors="ignore"))
        if len(parser.h1_values) != 1:
            errors.append(f"{path}: expected one H1, found {len(parser.h1_values)}")

    first_page = site / expected_paths[0]
    if first_page.exists():
        parser = PageParser()
        parser.feed(first_page.read_text(encoding="utf-8", errors="ignore"))
        chapter_links = [(title, normalize_href(href)) for title, href in parser.sidebar_links if "chapters/" in normalize_href(href)]
        actual_paths = [href for _, href in chapter_links]
        if actual_paths != expected_paths:
            errors.append(
                "rendered sidebar chapter order differs from canonical manifest order: "
                f"expected {len(expected_paths)} paths, observed {len(actual_paths)}"
            )
        titles = [re.sub(r"^\d+\s+", "", title) for title, _ in chapter_links]
        expected_titles = [row["title"] for row in status["chapter_order"]]
        if titles != expected_titles:
            errors.append("rendered sidebar chapter titles differ from canonical manifest titles")
        if len(set(actual_paths)) != len(actual_paths):
            errors.append("rendered sidebar contains duplicate chapter URLs")
        if len(set(titles)) != len(titles):
            errors.append("rendered sidebar contains duplicate chapter titles")
    return errors


def fetch_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": "asi-stack-public-status-validator/0.1"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise HTTPError(url, response.status, response.reason, response.headers, None)
        return response.read().decode("utf-8", errors="replace")


def remote_chapter_links(html: str, base_url: str) -> list[tuple[str, str]]:
    parser = PageParser()
    parser.feed(html)
    base_path = urlparse(base_url).path.rstrip("/") + "/"
    rows: list[tuple[str, str]] = []
    for title, href in parser.sidebar_links:
        absolute = urljoin(base_url, href)
        path = urlparse(absolute).path
        if path.startswith(base_path):
            path = path[len(base_path):]
        else:
            path = path.lstrip("/")
        if path.startswith("chapters/"):
            rows.append((title, path))
    return rows


def remote_status_errors(base_url: str, status: dict[str, Any], *, require_clean: bool) -> tuple[list[str], dict[str, Any] | None]:
    errors: list[str] = []
    status_url = urljoin(base_url.rstrip("/") + "/", "status/canonical-public-status.json")
    try:
        deployed = json.loads(fetch_url(status_url))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return [f"could not read deployed canonical status at {status_url}: {exc}"], None
    for key in ["active_version", "baseline_release", "release_profile", "deployment_channel", "source_commit"]:
        if deployed.get(key) != status.get(key):
            errors.append(
                f"deployed status {key}={deployed.get(key)!r} does not match expected {status.get(key)!r}"
            )
    for key, expected in status["counts"].items():
        if deployed.get("counts", {}).get(key) != expected:
            errors.append(
                f"deployed status count {key}={deployed.get('counts', {}).get(key)!r} does not match expected {expected}"
            )
    for key, expected in status["digests"].items():
        if deployed.get("digests", {}).get(key) != expected:
            errors.append(f"deployed status digest {key} does not match expected source digest")
    if require_clean:
        if deployed.get("source_tree_state") != "clean":
            errors.append("deployed status must report a clean source tree")
        if deployed.get("build_context") != "tested_commit":
            errors.append("deployed status must report tested_commit build context")
    return errors, deployed


def validate_remote_site(base_url: str, status: dict[str, Any], *, require_clean: bool) -> list[str]:
    errors, deployed = remote_status_errors(base_url, status, require_clean=require_clean)
    if errors or deployed is None:
        return errors
    base = base_url.rstrip("/") + "/"
    expected_paths = [row["public_path"] for row in status["chapter_order"]]
    try:
        landing = fetch_url(base)
    except (HTTPError, URLError, TimeoutError) as exc:
        return [f"could not read deployed landing page {base}: {exc}"]
    links = remote_chapter_links(landing, base)
    actual_paths = [path for _, path in links]
    if actual_paths != expected_paths:
        errors.append(
            "deployed sidebar chapter order differs from canonical manifest order: "
            f"expected {len(expected_paths)} paths, observed {len(actual_paths)}"
        )
    titles = [re.sub(r"^\d+\s+", "", title) for title, _ in links]
    expected_titles = [row["title"] for row in status["chapter_order"]]
    if titles != expected_titles:
        errors.append("deployed sidebar chapter titles differ from canonical manifest titles")
    if len(set(actual_paths)) != len(actual_paths):
        errors.append("deployed sidebar contains duplicate chapter URLs")
    if len(set(titles)) != len(titles):
        errors.append("deployed sidebar contains duplicate chapter titles")
    for path in expected_paths:
        url = urljoin(base, path)
        try:
            html = fetch_url(url)
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f"could not read deployed chapter {url}: {exc}")
            continue
        parser = PageParser()
        parser.feed(html)
        if len(parser.h1_values) != 1:
            errors.append(f"{url}: expected one H1, found {len(parser.h1_values)}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="Also validate a rendered Quarto site directory.")
    parser.add_argument("--url", help="Also crawl and attest a deployed site URL.")
    parser.add_argument("--require-clean", action="store_true", help="Require the rendered status record to identify a clean tested commit.")
    parser.add_argument("--attempts", type=int, default=1, help="Remote-status attempts for deployment propagation.")
    parser.add_argument("--retry-delay", type=int, default=0, help="Seconds between remote-status attempts.")
    args = parser.parse_args()
    config = load_json(CONFIG)
    status = build_status(timestamp="2000-01-01T00:00:00Z")
    errors: list[str] = []
    observed_by_surface: dict[str, set[str]] = {}
    for surface in config["active_source_surfaces"]:
        path = ROOT / surface["path"]
        if not path.exists():
            errors.append(f"missing active public status surface: {surface['path']}")
            continue
        errors.extend(validate_generated_block(path, status))
        surface_errors, observed = scan_surface(path, status, config)
        errors.extend(surface_errors)
        observed_by_surface[surface["path"]] = observed
        missing = sorted(set(surface["required_metrics"]) - observed)
        if missing:
            errors.append(f"{surface['path']}: missing active canonical metrics: {', '.join(missing)}")
    errors.extend(validate_chapter_header_count_boundary(status))
    errors.extend(run_negative_controls(status, config))
    if args.site:
        site = args.site if args.site.is_absolute() else ROOT / args.site
        errors.extend(validate_rendered_site(site, status, require_clean=args.require_clean))
    if args.url:
        if args.attempts < 1 or args.retry_delay < 0:
            errors.append("--attempts must be positive and --retry-delay must be nonnegative")
        else:
            remote_errors: list[str] = []
            for attempt in range(1, args.attempts + 1):
                remote_errors = validate_remote_site(args.url, status, require_clean=args.require_clean)
                if not remote_errors:
                    break
                if attempt < args.attempts:
                    print(f"Remote status attempt {attempt}/{args.attempts} not current; retrying in {args.retry_delay}s.")
                    time.sleep(args.retry_delay)
            errors.extend(remote_errors)
    if errors:
        print("Public status consistency validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print(
        "Public status consistency validation passed: "
        f"{len(config['active_source_surfaces'])} source surfaces, "
        f"{status['counts']['chapters']} chapters, {status['counts']['sources']} sources, "
        f"negative controls passed"
        + (f", rendered site {args.site} checked" if args.site else "")
        + (f", deployed site {args.url} attested" if args.url else "")
        + "."
    )


if __name__ == "__main__":
    main()
