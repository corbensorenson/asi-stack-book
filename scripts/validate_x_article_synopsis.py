#!/usr/bin/env python3
"""Validate X synopsis evidence fidelity, staleness bindings, header, and publication state."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "editions/x_article"
MANIFEST_PATH = BASE / "manifest.json"
SCHEMA_PATH = ROOT / "schemas/x_article_manifest.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_words(text: str) -> list[str]:
    return re.findall(r"\b[\w’'-]+\b", re.sub(r"<!--.*?-->", "", text, flags=re.S))


def errors(manifest: dict) -> list[str]:
    out: list[str] = []
    schema = load(SCHEMA_PATH)
    for err in sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path)):
        out.append(f"schema:{'.'.join(map(str, err.path))}: {err.message}")
    article_path = BASE / "asi_stack_synopsis.md"
    crosswalk_path = BASE / "claim_crosswalk.json"
    header_path = BASE / "asi_stack_synopsis_header.png"
    provenance_path = BASE / "header_provenance.json"
    preflight_path = BASE / "composer_preflight.json"
    article = article_path.read_text(encoding="utf-8")
    lines = article.splitlines()
    if len(lines) < 3 or lines[2] != "https://corbensorenson.github.io/asi-stack-book/":
        out.append("exact live-book URL is not the first visible body line after the title")
    count = len(visible_words(article))
    if count != manifest.get("article", {}).get("visible_word_count") or count > 9999:
        out.append(f"visible word count mismatch or overflow: {count}")
    markers = re.findall(r"<!-- claim: (XA-\d{2}) -->", article)
    if markers != [f"XA-{i:02d}" for i in range(1, 25)]:
        out.append("article claim markers must be exactly XA-01 through XA-24 in order")
    crosswalk = load(crosswalk_path)
    claims = crosswalk.get("claims", [])
    if [row.get("id") for row in claims] != markers:
        out.append("crosswalk IDs do not exactly match article markers")
    for row in claims:
        if not str(row.get("claim_atom_id", "")).endswith(".core"):
            out.append(f"{row.get('id')} lacks a stable chapter-core atom")
        for artifact in row.get("artifacts", []):
            if not (ROOT / artifact).exists():
                out.append(f"{row.get('id')} cites missing artifact: {artifact}")
        if not row.get("boundary") or "boundary" in row.get("boundary", "").casefold() and len(row["boundary"]) < 25:
            out.append(f"{row.get('id')} lacks a substantive claim boundary")
    with Image.open(header_path) as im:
        if im.size != (2000, 800) or im.mode != "RGB" or im.format != "PNG":
            out.append(f"header must be exact 2000x800 RGB PNG; found {im.size} {im.mode} {im.format}")
    provenance = load(provenance_path)
    if provenance.get("master", {}).get("sha256") != sha(header_path):
        out.append("header provenance digest mismatch")
    if provenance.get("alt_text_characters", 0) > 1000 or len(provenance.get("alt_text", "")) < 80:
        out.append("header alt text is missing, too short, or above the X limit")
    derivative = BASE / "platform_derivatives/x_header_1200x480.jpg"
    with Image.open(derivative) as im:
        if im.size != (1200, 480):
            out.append("X platform header derivative is not exact observed 1200x480")
    preflight = load(preflight_path)
    if preflight.get("article", {}).get("composer_reported_word_count") != 5196:
        out.append("composer word-count receipt drifted")
    if preflight.get("article", {}).get("top_link_passed") is not True:
        out.append("composer top-link check did not pass")
    if preflight.get("header", {}).get("upload") != "passed" or "passed" not in preflight.get("header", {}).get("desktop_preview", "") or "passed" not in preflight.get("header", {}).get("mobile_preview", ""):
        out.append("header upload/preview evidence is incomplete")
    if preflight.get("header", {}).get("header_alt_text_control") != "not_exposed_by_live_article_header_editor":
        out.append("platform header alt-text limitation was erased")
    if preflight.get("publication", {}).get("publish_button_clicked") is not False or preflight.get("publication", {}).get("decision") != "ready_not_published":
        out.append("unpublished draft was laundered into publication")
    if manifest.get("composer", {}).get("state") != "historical_draft_stale_after_source_refresh":
        out.append("historical composer draft is not marked stale after source refresh")
    if manifest.get("staleness", {}).get("state") != "source_current_platform_draft_stale":
        out.append("source/platform derivative split is not explicit")
    for key, rec in manifest.get("bound_inputs", {}).items():
        path = ROOT / rec.get("path", "missing")
        if not path.is_file() or path.stat().st_size != rec.get("bytes") or sha(path) != rec.get("sha256"):
            out.append(f"stale or missing bound input: {key}")
    for key, rec in manifest.get("artifacts", {}).items():
        path = ROOT / rec.get("path", "missing")
        if not path.is_file() or path.stat().st_size != rec.get("bytes") or sha(path) != rec.get("sha256"):
            out.append(f"stale or missing X Article artifact: {key}")
    if manifest.get("publication", {}).get("external_publication_authorized") is not False or manifest.get("publication", {}).get("article_url") is not None:
        out.append("manifest invented external-publication authority or URL")
    if manifest.get("support_state_effect") != "none":
        out.append("synopsis work cannot move claim support")
    return out


def mutations(base: dict) -> tuple[int, list[str]]:
    cases = []
    def add(label, fn):
        obj = copy.deepcopy(base); fn(obj); cases.append((label, obj))
    add("word_limit_inflation", lambda d: d["article"].__setitem__("maximum_visible_word_count", 10000))
    add("link_rewrite", lambda d: d.__setitem__("canonical_live_book_url", "https://example.com/"))
    add("header_ratio_rewrite", lambda d: d["header"].__setitem__("aspect_ratio", "16:9"))
    add("false_publication", lambda d: d["publication"].__setitem__("external_publication_authorized", True))
    add("support_promotion", lambda d: d.__setitem__("support_state_effect", "promotion"))
    add("article_digest_rewrite", lambda d: d["artifacts"]["article"].__setitem__("sha256", "0" * 64))
    add("claim_count_erasure", lambda d: d["article"].__setitem__("claim_marker_count", 23))
    add("platform_alt_laundering", lambda d: d["header"].__setitem__("platform_alt_text_control", "passed"))
    rejected, escaped = 0, []
    for label, candidate in cases:
        if errors(candidate): rejected += 1
        else: escaped.append(label)
    return rejected, escaped


def main() -> int:
    manifest = load(MANIFEST_PATH)
    failures = errors(manifest)
    rejected, escaped = mutations(manifest)
    if rejected != 8:
        failures.append(f"must reject 8/8 mutations; found {rejected}; escaped={escaped}")
    if failures:
        print("X Article synopsis validation failed:", file=sys.stderr)
        for failure in failures: print(f" - {failure}", file=sys.stderr)
        return 1
    print(f"X Article synopsis passed: {manifest['article']['visible_word_count']} canonical words, 24 crosswalked claims, exact 2000x800 header, 8/8 mutations rejected; local source current, historical platform draft stale, publication not authorized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
