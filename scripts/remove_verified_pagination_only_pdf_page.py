#!/usr/bin/env python3
"""Remove one PDF page only when it contains pagination and no content assets.

This is a narrowly scoped reader-release repair for a renderer-inserted interior
page.  It refuses to edit a page that contains any extracted text other than the
expected printed page number, any image/form XObjects, annotations, or links.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--page", type=int, required=True, help="One-based page number")
    parser.add_argument(
        "--expected-pagination",
        required=True,
        help="The only extracted text permitted on the removed page",
    )
    args = parser.parse_args()

    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Input and output must differ")

    reader = PdfReader(args.input)
    page_index = args.page - 1
    if page_index < 0 or page_index >= len(reader.pages):
        raise SystemExit(f"Page {args.page} is outside 1..{len(reader.pages)}")

    page = reader.pages[page_index]
    extracted = " ".join((page.extract_text() or "").split())
    expected = " ".join(args.expected_pagination.split())
    resources = page.get("/Resources") or {}
    xobjects = resources.get("/XObject") or {}
    annotations = page.get("/Annots") or []

    if extracted != expected:
        raise SystemExit(
            f"Refusing removal: extracted text {extracted!r} != expected {expected!r}"
        )
    if len(xobjects):
        raise SystemExit(f"Refusing removal: page contains {len(xobjects)} XObject(s)")
    if len(annotations):
        raise SystemExit(f"Refusing removal: page contains {len(annotations)} annotation(s)")

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    del writer.pages[page_index]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as stream:
        writer.write(stream)

    output_reader = PdfReader(args.output)
    if len(output_reader.pages) != len(reader.pages) - 1:
        raise SystemExit("Output page-count verification failed")

    print(
        json.dumps(
            {
                "input": str(args.input),
                "input_pages": len(reader.pages),
                "input_sha256": sha256(args.input),
                "removed_page": args.page,
                "removed_text": extracted,
                "output": str(args.output),
                "output_pages": len(output_reader.pages),
                "output_sha256": sha256(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
