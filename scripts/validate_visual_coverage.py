#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

MERMAID_BLOCK_RE = re.compile(r"```(?:\{mermaid\}|mermaid)\s*\n(.*?)\n```", re.DOTALL)
MERMAID_EDGE_RE = re.compile(r"(-->|---|-.->|==>|->>|-->>|-\)|--\)|-x|--x|--o)")
MERMAID_LABELED_EDGE_RE = re.compile(
    r"("
    r"[-.=]+\s*(?:\"[^\"]+\"|\|[^|]+\|)\s*[-.=]*>"
    r"|[-.=]+>\|[^|]+\|"
    r"|\b[A-Za-z][A-Za-z0-9_]*\s*[-]+>>\s*[A-Za-z][A-Za-z0-9_]*\s*:"
    r")"
)
MERMAID_NODE_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9_]*)\s*(?=[\[\(\{])")
MERMAID_DECL_RE = re.compile(r"^\s*(participant|actor|boundary|control|entity|database|collections|queue)\s+([A-Za-z][A-Za-z0-9_]*)\b", re.IGNORECASE)

MIN_DIAGRAM_LINES = 12
MIN_DIAGRAM_EDGES = 6
MIN_DIAGRAM_NODES = 7
MIN_LABELED_EDGES = 2


def fail(errors: list[str]) -> None:
    for error in errors:
        print(error)
    sys.exit(1)


def diagram_stats(block: str) -> tuple[int, int, int, int]:
    lines = [
        line.strip()
        for line in block.splitlines()
        if line.strip() and not line.strip().startswith("%%")
    ]
    edges = sum(len(MERMAID_EDGE_RE.findall(line)) for line in lines)
    labeled_edges = sum(len(MERMAID_LABELED_EDGE_RE.findall(line)) for line in lines)
    nodes: set[str] = set()
    for line in lines:
        nodes.update(MERMAID_NODE_RE.findall(line))
        declaration = MERMAID_DECL_RE.match(line)
        if declaration:
            nodes.add(declaration.group(2))
    return len(lines), edges, len(nodes), labeled_edges


def is_substantive_diagram(block: str) -> bool:
    line_count, edge_count, node_count, labeled_edge_count = diagram_stats(block)
    return (
        line_count >= MIN_DIAGRAM_LINES
        and edge_count >= MIN_DIAGRAM_EDGES
        and node_count >= MIN_DIAGRAM_NODES
        and labeled_edge_count >= MIN_LABELED_EDGES
    )


def main() -> None:
    errors: list[str] = []

    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    checked = 0
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            path = ROOT / chapter["file"]
            text = path.read_text(encoding="utf-8", errors="ignore")
            blocks = MERMAID_BLOCK_RE.findall(text)
            if not blocks:
                errors.append(f"Chapter lacks a Mermaid interface/lifecycle diagram: {chapter['file']}")
                continue
            checked += 1
            if not any(is_substantive_diagram(block) for block in blocks):
                best = max((diagram_stats(block) for block in blocks), default=(0, 0, 0))
                errors.append(
                    "Chapter Mermaid diagram is too thin: "
                    f"{chapter['file']} "
                    f"(best lines={best[0]}, edges={best[1]}, nodes={best[2]}, labeled_edges={best[3]}; "
                    f"minimum lines={MIN_DIAGRAM_LINES}, edges={MIN_DIAGRAM_EDGES}, "
                    f"nodes={MIN_DIAGRAM_NODES}, labeled_edges={MIN_LABELED_EDGES})"
                )

    index = (ROOT / "index.qmd").read_text(encoding="utf-8", errors="ignore")
    hero = ROOT / "assets" / "images" / "asi-stack-hero.png"
    if "assets/images/asi-stack-hero.png" not in index:
        errors.append("index.qmd does not reference the landing-page hero image.")
    if not hero.exists():
        errors.append("Landing-page hero image is missing: assets/images/asi-stack-hero.png")

    if errors:
        fail(errors)

    print(f"Visual coverage validation passed: {checked} chapter diagrams checked.")


if __name__ == "__main__":
    main()
