#!/usr/bin/env python3
"""Validate that stack language specifies logical contracts, not physical modularity."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "opener": ROOT / "chapters" / "asi-is-a-stack-not-a-model.qmd",
    "reference": ROOT / "chapters" / "integrated-reference-architecture.qmd",
    "outline": ROOT / "docs" / "book_outline.md",
    "glossary": ROOT / "appendices" / "B_glossary.qmd",
    "figure": ROOT / "assets" / "diagrams" / "asi-stack-control-plane.svg",
}

REQUIRED = {
    "opener": (
        "A layer is a logical responsibility and authority boundary",
        "One model may implement several roles",
        "Several models, tools, or people may also implement one role",
        "the stack claim itself is substrate-neutral",
    ),
    "reference": (
        "The participants in that trace are logical roles",
        "The reference architecture is therefore substrate-neutral",
    ),
    "outline": (
        "`layer` means a logical responsibility and authority boundary",
        "The architecture is substrate-neutral",
    ),
    "glossary": (
        "substrate-neutral governed architecture",
        "does not require one model or physical module per layer",
    ),
    "figure": ("Logical responsibility boundaries; one or many models may implement them.",),
}

FORBIDDEN = (
    "each layer requires its own model",
    "one model per layer is required",
    "each layer must run as a separate process",
    "the layers must be physically separate",
)


def semantic_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for owner, fragments in REQUIRED.items():
        for fragment in fragments:
            if fragment not in texts.get(owner, ""):
                errors.append(f"{owner} is missing substrate-neutral contract text: {fragment}")
    joined = "\n".join(texts.values()).lower()
    for phrase in FORBIDDEN:
        if phrase in joined:
            errors.append(f"physical-modularity overclaim found: {phrase}")
    return errors


def main() -> None:
    errors: list[str] = []
    texts: dict[str, str] = {}
    for owner, path in FILES.items():
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
        else:
            texts[owner] = path.read_text(encoding="utf-8", errors="ignore")
    errors.extend(semantic_errors(texts))
    mutated = dict(texts)
    mutated["opener"] = mutated.get("opener", "") + "\nEach layer requires its own model.\n"
    if not semantic_errors(mutated):
        errors.append("negative control was incorrectly accepted: one-model-per-layer claim")
    if errors:
        print("Substrate-neutral stack validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    print("Substrate-neutral stack validation passed: opener, reference trace, outline, glossary, figure, and rejecting negative control.")


if __name__ == "__main__":
    main()
