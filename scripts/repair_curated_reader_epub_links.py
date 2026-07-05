#!/usr/bin/env python3
"""Repair known EPUB XHTML leakage in the curated-reader EPUB snapshot.

Quarto resolves the Appendix H link in HTML, but the EPUB writer currently
leaves the forward Appendix G-to-H link as ``H_external_sources.qmd``. This
script rewrites that packaged XHTML href to the spine target Quarto generated
for the external-sources appendix.

The EPUB writer can also emit Mermaid figure wrappers as ``<figure class>``.
That is tolerated by Chromium's HTML parser, but Apple Books treats the XHTML
as XML and stops at the invalid bare attribute. This repair removes only that
invalid empty attribute. It operates only on ignored build output and does not
approve the EPUB artifact.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPUB = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "epub" / "_reader_site" / "The-ASI-Stack.epub"
RAW_QMD_HREF_RE = re.compile(r"""href=(["'])([^"']+\.qmd(?:#[^"']*)?)\1""")
BARE_CLASS_ATTR_RE = re.compile(r"""<([A-Za-z][\w:.-]*)([^<>]*?)\sclass(?=(?:\s|/|>))([^<>]*?)>""")
OPEN_FIGURE_PARAGRAPH_RE = re.compile(r"""<p>\s*<figure>\s*</p>""")
CLOSE_FIGURE_PARAGRAPH_RE = re.compile(r"""<p>\s*</figure>\s*</p>""")
EPUB_OVERFLOW_CSS_MARKER = "ASI reader EPUB overflow repair v2"
EPUB_OVERFLOW_CSS = f"""

/* {EPUB_OVERFLOW_CSS_MARKER}: keep Quarto-generated figures inside narrow e-reader page boxes. */
html,
body {{
  max-width: 100% !important;
  overflow-x: hidden !important;
}}
body,
body * {{
  box-sizing: border-box;
}}
figure,
.cell,
.cell-output-display {{
  max-width: 100% !important;
  overflow-x: hidden !important;
}}
img,
svg {{
  max-width: 100% !important;
  height: auto !important;
}}
pre,
table {{
  max-width: 100% !important;
  overflow-x: auto !important;
}}
p code,
li code,
td code {{
  overflow-wrap: anywhere !important;
  word-break: break-word !important;
  white-space: normal !important;
}}
pre code {{
  white-space: pre-wrap !important;
}}
"""
REPAIR_MAP = {
    "H_external_sources.qmd": "ch049.xhtml#external-sources-by-other-authors",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader EPUB link repair failed:")
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
    cloned.compress_type = ZIP_STORED if info.filename == "mimetype" else info.compress_type
    return cloned


def repair_epub(path: Path, check: bool = False) -> dict[str, object]:
    if not path.exists():
        fail([f"Missing EPUB artifact: {rel(path)}. Run `python3 scripts/render_curated_reader_formats.py --formats epub` first."])

    replacements: list[str] = []
    bare_class_repairs: list[str] = []
    figure_paragraph_repairs: list[str] = []
    stylesheet_repairs: list[str] = []
    raw_after: list[str] = []
    repaired_target_hits = 0
    bare_class_after = 0
    overflow_css_hits = 0
    with ZipFile(path, "r") as source:
        infos = source.infolist()
        if not infos or infos[0].filename != "mimetype":
            fail(["EPUB mimetype entry must be first before link repair."])
        rewritten_entries: list[tuple[ZipInfo, bytes]] = []
        for info in infos:
            data = source.read(info.filename)
            if info.filename.endswith(".xhtml"):
                text = data.decode("utf-8", errors="replace")
                repaired_target_hits += sum(text.count(target) for target in REPAIR_MAP.values())

                def replace_href(match: re.Match[str]) -> str:
                    quote = match.group(1)
                    target = match.group(2)
                    replacement = REPAIR_MAP.get(target)
                    if replacement is None:
                        raw_after.append(f"{info.filename} -> {target}")
                        return match.group(0)
                    replacements.append(f"{info.filename}: {target} -> {replacement}")
                    return f"href={quote}{replacement}{quote}"

                text = RAW_QMD_HREF_RE.sub(replace_href, text)

                def remove_bare_class(match: re.Match[str]) -> str:
                    bare_class_repairs.append(f"{info.filename}: <{match.group(1)} class>")
                    return f"<{match.group(1)}{match.group(2)}{match.group(3)}>"

                text = BARE_CLASS_ATTR_RE.sub(remove_bare_class, text)
                bare_class_after += len(BARE_CLASS_ATTR_RE.findall(text))
                open_wrappers = len(OPEN_FIGURE_PARAGRAPH_RE.findall(text))
                close_wrappers = len(CLOSE_FIGURE_PARAGRAPH_RE.findall(text))
                if open_wrappers or close_wrappers:
                    text = OPEN_FIGURE_PARAGRAPH_RE.sub("<figure>", text)
                    text = CLOSE_FIGURE_PARAGRAPH_RE.sub("</figure>", text)
                    figure_paragraph_repairs.append(
                        f"{info.filename}: {open_wrappers} opening wrapper(s), {close_wrappers} closing wrapper(s)"
                    )
                data = text.encode("utf-8")
            elif info.filename.endswith(".css"):
                text = data.decode("utf-8", errors="replace")
                if EPUB_OVERFLOW_CSS_MARKER in text:
                    overflow_css_hits += 1
                elif info.filename == "EPUB/styles/stylesheet1.css":
                    text = text.rstrip() + EPUB_OVERFLOW_CSS + "\n"
                    stylesheet_repairs.append(info.filename)
                    overflow_css_hits += 1
                    data = text.encode("utf-8")
            rewritten_entries.append((clone_info(info), data))

    if raw_after:
        fail(["unmapped raw .qmd href(s) remain after repair: " + "; ".join(raw_after[:10])])
    if bare_class_after:
        fail([f"bare class attribute(s) remain after repair: {bare_class_after}"])
    if overflow_css_hits == 0:
        fail(["EPUB overflow CSS repair marker was not present or added."])
    if not replacements and repaired_target_hits == 0 and not bare_class_repairs and not figure_paragraph_repairs and not stylesheet_repairs:
        fail(["expected a link repair target, already-repaired href, bare class repair, figure wrapper repair, or stylesheet repair, but none was found."])

    if not check and (replacements or bare_class_repairs or figure_paragraph_repairs or stylesheet_repairs):
        with NamedTemporaryFile("wb", delete=False, dir=str(path.parent), suffix=".epub") as handle:
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
        "epub": rel(path),
        "repairs": replacements,
        "bare_class_attribute_repairs": bare_class_repairs,
        "figure_paragraph_repairs": figure_paragraph_repairs,
        "stylesheet_overflow_repairs": stylesheet_repairs,
        "already_repaired_href_hits": repaired_target_hits,
        "raw_qmd_hrefs_remaining": 0,
        "bare_class_attributes_remaining": 0,
        "overflow_css_marker_hits": overflow_css_hits,
        "check_only": check,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epub", default=str(DEFAULT_EPUB), help="curated-reader EPUB artifact to repair")
    parser.add_argument("--check", action="store_true", help="validate repairs without rewriting the EPUB")
    args = parser.parse_args()

    result = repair_epub(Path(args.epub), args.check)
    print(
        "Curated reader EPUB repair passed: "
        f"{len(result['repairs'])} href repair(s), "
        f"{len(result['bare_class_attribute_repairs'])} bare class repair(s), "
        f"{len(result['figure_paragraph_repairs'])} figure wrapper repair(s), "
        f"{len(result['stylesheet_overflow_repairs'])} stylesheet repair(s), "
        f"{result['already_repaired_href_hits']} already-repaired href hit(s), "
        f"{result['raw_qmd_hrefs_remaining']} raw .qmd hrefs remaining, "
        f"{result['bare_class_attributes_remaining']} bare class attributes remaining, "
        f"{result['overflow_css_marker_hits']} overflow CSS marker hit(s)."
    )


if __name__ == "__main__":
    main()
