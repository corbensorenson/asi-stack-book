#!/usr/bin/env python3
"""Repair known internal-link leakage in the curated-reader EPUB snapshot.

Quarto resolves the Appendix H link in HTML, but the EPUB writer currently
leaves the forward Appendix G-to-H link as ``H_external_sources.qmd``. This
script rewrites that packaged XHTML href to the spine target Quarto generated
for the external-sources appendix. It operates only on ignored build output and
does not approve the EPUB artifact.
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
    raw_after: list[str] = []
    repaired_target_hits = 0
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
                data = text.encode("utf-8")
            rewritten_entries.append((clone_info(info), data))

    if raw_after:
        fail(["unmapped raw .qmd href(s) remain after repair: " + "; ".join(raw_after[:10])])
    if not replacements and repaired_target_hits == 0:
        fail(["expected a repair target or already-repaired href, but neither was found."])

    if not check and replacements:
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
        "already_repaired_href_hits": repaired_target_hits,
        "raw_qmd_hrefs_remaining": 0,
        "check_only": check,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epub", default=str(DEFAULT_EPUB), help="curated-reader EPUB artifact to repair")
    parser.add_argument("--check", action="store_true", help="validate repairs without rewriting the EPUB")
    args = parser.parse_args()

    result = repair_epub(Path(args.epub), args.check)
    print(
        "Curated reader EPUB link repair passed: "
        f"{len(result['repairs'])} href repair(s), "
        f"{result['already_repaired_href_hits']} already-repaired href hit(s), "
        f"{result['raw_qmd_hrefs_remaining']} raw .qmd hrefs remaining."
    )


if __name__ == "__main__":
    main()
