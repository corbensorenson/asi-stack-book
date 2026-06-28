#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_WORDS = 18
FORMULAIC_BEYOND_OPENERS = (
    "The mature version of",
    "The mature version is",
    "The logical end state is",
    "At full build-out,",
    "At maturity,",
)
FORMULAIC_BEYOND_PHRASES = (
    "The mature version of",
    "The mature product surface would include:",
    "The final product surface would include:",
    "would expose:",
    "The operational contract is",
    "Support should stay at",
    "At that mature boundary",
    "In that final product",
    "Failure closure:",
    "detect and route failure modes such as",
    "This is a target architecture, not a current-result claim",
    "It remains beyond the chapter's present support state",
)
FORMULAIC_MVI_PHRASES = (
    "The next useful implementation step is",
    "The next useful fixture set is",
    "The next useful fixture is",
    "The fixture validates",
    "The fixture is not",
    "The fixture is only",
    "Passing the fixture",
    "Passing schema validation only",
    "That would",
    "without claiming",
    "does not prove",
    "do not prove",
    "proves only",
    "prove only",
    "cannot prove",
    "The accompanying Lean module is",
    "The Lean predicates do not",
    "These proofs do not implement",
    "The Lean coverage stays at",
)
FORMULAIC_GENERAL_PHRASES = (
    "The book needs a place",
    "The book needs",
    "The stack needs",
    "The ASI Stack needs",
    "The public schema now records",
    "The insufficiency is",
    "The problem is",
    "The interface is the",
    "The interface is a",
    "The interface is an",
    "The interface should",
    "The interface should also record",
    "The interface should distinguish",
    "The interface should expose",
    "The interface should carry",
    "The interface should also",
    "The minimum should",
    "The contract should also",
    "None of those passages show",
    "The reviewed passages sharpen the",
    "The passage-reviewed mappings support discussion",
    "The evidence map is narrower now",
    "The support state remains `argument`",
    "The practical point is",
    "The practical test is",
    "The practical rule is",
    "The practical purpose is",
    "The practical problem is",
    "The record should",
    "The response is",
    "The stack should",
    "This is why",
    "The subtle failure is",
    "The subtle failure mode is",
    "Another failure is",
    "Each failure should",
    "Another invariant is",
    "A second invariant is",
    "The strongest invariant is",
    "The key invariant is",
    "The invariant is",
    "**Diagram reading note:**",
)


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return "\n".join(lines[index + 1 :])
    return text


def paragraph_words(paragraph: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", paragraph)


def normalized_paragraphs(path: Path) -> list[str]:
    text = strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    paragraphs: list[str] = []
    in_code = False
    current: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            if current:
                paragraphs.append(" ".join(" ".join(current).split()))
                current = []
            continue
        current.append(stripped)

    if current:
        paragraphs.append(" ".join(" ".join(current).split()))

    filtered = []
    for paragraph in paragraphs:
        if paragraph.startswith("|"):
            continue
        if paragraph.startswith("#"):
            continue
        if len(paragraph_words(paragraph)) < MIN_WORDS:
            continue
        filtered.append(paragraph)
    return filtered


def beyond_state_body(path: Path) -> str:
    text = strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    match = re.search(r"^## Beyond the State of the Art\s*$\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return ""
    return match.group("body").strip()


def minimum_viable_body(path: Path) -> str:
    text = strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    match = re.search(r"^## Minimum Viable Implementation\s*$\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return ""
    return match.group("body").strip()


def beyond_state_openers(body: str) -> list[str]:
    if not body:
        return []
    first_paragraph = body.split("\n\n", 1)[0]
    return [" ".join(first_paragraph.split())]


def main() -> None:
    locations: dict[str, list[str]] = defaultdict(list)
    formulaic_openers: list[tuple[str, str]] = []
    formulaic_phrases: list[tuple[str, str]] = []
    formulaic_mvi_phrases: list[tuple[str, str]] = []
    formulaic_general_phrases: list[tuple[str, str]] = []
    for path in sorted((ROOT / "chapters").glob("*.qmd")):
        chapter_text = strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
        for paragraph in normalized_paragraphs(path):
            locations[paragraph].append(str(path.relative_to(ROOT)))
        for phrase in FORMULAIC_GENERAL_PHRASES:
            if phrase in chapter_text:
                formulaic_general_phrases.append((str(path.relative_to(ROOT)), phrase))
        beyond_body = beyond_state_body(path)
        for opener in beyond_state_openers(beyond_body):
            if opener.startswith(FORMULAIC_BEYOND_OPENERS):
                formulaic_openers.append((str(path.relative_to(ROOT)), opener))
        for phrase in FORMULAIC_BEYOND_PHRASES:
            if phrase in beyond_body:
                formulaic_phrases.append((str(path.relative_to(ROOT)), phrase))
        mvi_body = minimum_viable_body(path)
        for phrase in FORMULAIC_MVI_PHRASES:
            if phrase in mvi_body:
                formulaic_mvi_phrases.append((str(path.relative_to(ROOT)), phrase))

    repeats = {paragraph: paths for paragraph, paths in locations.items() if len(paths) > 1}
    if repeats or formulaic_openers or formulaic_phrases or formulaic_mvi_phrases or formulaic_general_phrases:
        if repeats:
            print(f"Repeated long prose paragraphs found: {len(repeats)}")
        for paragraph, paths in sorted(repeats.items(), key=lambda item: (-len(item[1]), item[0])):
            print(f" - {len(paths)}x {paths}: {paragraph[:220]}")
        if formulaic_openers:
            print(f"Formulaic Beyond the State of the Art openers found: {len(formulaic_openers)}")
            for path, opener in formulaic_openers:
                print(f" - {path}: {opener[:220]}")
        if formulaic_phrases:
            print(f"Formulaic Beyond the State of the Art phrases found: {len(formulaic_phrases)}")
            for path, phrase in formulaic_phrases:
                print(f" - {path}: {phrase}")
        if formulaic_mvi_phrases:
            print(f"Formulaic Minimum Viable Implementation phrases found: {len(formulaic_mvi_phrases)}")
            for path, phrase in formulaic_mvi_phrases:
                print(f" - {path}: {phrase}")
        if formulaic_general_phrases:
            print(f"Formulaic chapter prose phrases found: {len(formulaic_general_phrases)}")
            for path, phrase in formulaic_general_phrases:
                print(f" - {path}: {phrase}")
        sys.exit(1)

    print("Repeated prose validation passed.")


if __name__ == "__main__":
    main()
