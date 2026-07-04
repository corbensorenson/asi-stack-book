#!/usr/bin/env python3
"""Repair known internal-link leakage in the curated-reader DOCX snapshot.

Pandoc leaves the forward Appendix G-to-H link as an external DOCX hyperlink
targeting ``H_external_sources.qmd``. That target is not useful in a Word
package, so this script removes the broken hyperlink wrapper while preserving
the visible linked text. It operates only on ignored build output and does not
approve the DOCX artifact.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCX = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "docx" / "_reader_site" / "The-ASI-Stack.docx"
DOCUMENT_XML = "word/document.xml"
DOCUMENT_RELS = "word/_rels/document.xml.rels"
QMD_REL_RE = re.compile(r"""<Relationship\b(?=[^>]*\bId=["']([^"']+)["'])(?=[^>]*\bTarget=["'][^"']+\.qmd(?:#[^"']*)?["'])[^>]*/>""")
RAW_QMD_HREF_RE = re.compile(r"""Target=["'][^"']+\.qmd(?:#[^"']*)?["']""")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader DOCX link repair failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def clone_info(info: ZipInfo) -> ZipInfo:
    cloned = ZipInfo(info.filename, date_time=info.date_time)
    cloned.comment = info.comment
    cloned.extra = info.extra
    cloned.internal_attr = info.internal_attr
    cloned.external_attr = info.external_attr
    cloned.create_system = info.create_system
    cloned.compress_type = info.compress_type
    return cloned


def unwrap_hyperlink(document_xml: str, relationship_id: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"""<w:hyperlink\b(?=[^>]*\br:id=["']{re.escape(relationship_id)}["'])[^>]*>(.*?)</w:hyperlink>""",
        re.DOTALL,
    )
    return pattern.subn(r"\1", document_xml)


def repair_docx(path: Path, check: bool = False) -> dict[str, object]:
    if not path.exists():
        fail([f"Missing DOCX artifact: {rel(path)}. Run `python3 scripts/render_curated_reader_formats.py --formats docx` first."])

    with ZipFile(path, "r") as source:
        infos = source.infolist()
        names = {info.filename for info in infos}
        for required in (DOCUMENT_XML, DOCUMENT_RELS):
            if required not in names:
                fail([f"DOCX package missing required entry: {required}"])
        document_xml = source.read(DOCUMENT_XML).decode("utf-8", errors="replace")
        rels_xml = source.read(DOCUMENT_RELS).decode("utf-8", errors="replace")

        relationship_ids = QMD_REL_RE.findall(rels_xml)
        already_repaired = not relationship_ids and not RAW_QMD_HREF_RE.search(rels_xml)
        unwrapped = 0
        for relationship_id in relationship_ids:
            document_xml, count = unwrap_hyperlink(document_xml, relationship_id)
            if count != 1:
                fail([f"expected to unwrap exactly one DOCX hyperlink for {relationship_id}, found {count}."])
            unwrapped += count

        rels_xml, removed = QMD_REL_RE.subn("", rels_xml)
        if RAW_QMD_HREF_RE.search(rels_xml):
            fail(["raw .qmd DOCX relationship target remains after repair."])
        if relationship_ids and removed != len(relationship_ids):
            fail([f"expected to remove {len(relationship_ids)} .qmd relationship(s), removed {removed}."])
        if not relationship_ids and not already_repaired:
            fail(["expected a .qmd relationship target or already-repaired DOCX package, but neither was found."])

        rewritten_entries: list[tuple[ZipInfo, bytes]] = []
        for info in infos:
            data = source.read(info.filename)
            if info.filename == DOCUMENT_XML:
                data = document_xml.encode("utf-8")
            elif info.filename == DOCUMENT_RELS:
                data = rels_xml.encode("utf-8")
            rewritten_entries.append((clone_info(info), data))

    if not check and relationship_ids:
        with NamedTemporaryFile("wb", delete=False, dir=str(path.parent), suffix=".docx") as handle:
            temp_path = Path(handle.name)
        try:
            with ZipFile(temp_path, "w") as target:
                for info, data in rewritten_entries:
                    target.writestr(info, data)
            shutil.move(str(temp_path), path)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    return {
        "docx": rel(path),
        "relationships_removed": len(relationship_ids),
        "hyperlinks_unwrapped": unwrapped,
        "already_repaired": already_repaired,
        "raw_qmd_relationship_targets_remaining": 0,
        "check_only": check,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx", default=str(DEFAULT_DOCX), help="curated-reader DOCX artifact to repair")
    parser.add_argument("--check", action="store_true", help="validate repairs without rewriting the DOCX")
    args = parser.parse_args()

    result = repair_docx(Path(args.docx), args.check)
    print(
        "Curated reader DOCX link repair passed: "
        f"{result['relationships_removed']} relationship(s) removed, "
        f"{result['hyperlinks_unwrapped']} hyperlink(s) unwrapped, "
        f"{result['raw_qmd_relationship_targets_remaining']} raw .qmd relationship targets remaining."
    )


if __name__ == "__main__":
    main()
