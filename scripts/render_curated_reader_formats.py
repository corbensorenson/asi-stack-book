#!/usr/bin/env python3
"""Render selected formats from the tracked curated reader manuscript.

This is the curated-reader counterpart to ``render_reader_formats.py``. It
builds the review workspace from tracked curated chapter files, renders the
requested Quarto formats, snapshots successful artifacts under ignored build
space, and writes a local report. It does not publish artifacts, clear release
blockers, or create an edition release record.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import posixpath
import re
import signal
import shutil
import subprocess
import tempfile
from typing import Iterator
import uuid
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile, ZipInfo

import build_curated_reader_edition


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "curated_reader_edition"
DEFAULT_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
DEFAULT_FORMATS = ("html", "epub", "docx")
FORMAT_EXTENSIONS = {
    "html": [".html"],
    "epub": [".epub"],
    "docx": [".docx"],
    "pdf": [".pdf"],
}
PRESERVED_ARTIFACT_DIR = "format_artifacts"
REPORT_NAME = "curated_reader_render_report.json"
TEXT_FORMAT_PROFILE_NAME = "text_format_profile.json"
DIAGRAM_SVG_REF_RE = re.compile(r"(\]\()(\.\./assets/diagrams/)([^)]+?)\.svg(\))")
MERMAID_BLOCK_RE = re.compile(r"```\{mermaid\}\s*\n([\s\S]*?)\n```")
MERMAID_SVG_RE = re.compile(r"""<svg\b(?=[^>]*\bid=["']mermaid-\d+["'])[\s\S]*?</svg>""")
VIEWBOX_RE = re.compile(r"""viewBox=["']\s*0\s+0\s+([0-9.]+)\s+([0-9.]+)\s*["']""")
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)


def render_environment() -> dict[str, str]:
    env = os.environ.copy()
    env["LANG"] = "en_US.UTF-8"
    env["LC_ALL"] = "en_US.UTF-8"
    return env


def find_artifacts(output_dir: Path, fmt: str) -> list[str]:
    suffixes = FORMAT_EXTENSIONS.get(fmt, [])
    search_root = output_dir / "_reader_site" if fmt == "html" and (output_dir / "_reader_site").exists() else output_dir
    artifacts: list[str] = []
    for path in search_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(output_dir)
        if PRESERVED_ARTIFACT_DIR in relative.parts:
            continue
        if any(path.name.endswith(suffix) for suffix in suffixes):
            artifacts.append(str(relative))
    return sorted(artifacts)


def apply_frozen_text_format_profile(output_dir: Path, manifest_path: Path) -> dict[str, object]:
    profile_path = manifest_path.resolve().parent / TEXT_FORMAT_PROFILE_NAME
    if not profile_path.is_file():
        return {"applied": False, "profile": "", "reference_doc": ""}
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    if profile.get("state") != "frozen_before_release_candidates":
        raise RuntimeError("text format profile exists but is not frozen")
    quarto_path = output_dir / "_quarto.yml"
    text = quarto_path.read_text(encoding="utf-8")
    docx_old = "  docx:\n    toc: true\n"
    docx_new = "  docx:\n    toc: true\n    reference-doc: assets/reader-v2-reference.docx\n"
    pdf_old = (
        "  pdf:\n    toc: true\n    number-sections: true\n"
        "    include-in-header:\n      - assets/pdf-long-inline-code.tex\n"
        "    filters:\n      - assets/pdf-break-inline-code.lua\n"
    )
    pdf_new = (
        "  pdf:\n    toc: true\n    number-sections: true\n"
        "    pdf-engine: typst\n    papersize: us-letter\n"
        "    mainfont: Libertinus Serif\n    monofont: DejaVu Sans Mono\n"
    )
    if docx_old not in text or pdf_old not in text:
        raise RuntimeError("generated Quarto format blocks drifted from frozen profile patch points")
    reference_rel = profile["formats"]["docx"]["reference_doc"]
    reference_src = ROOT / reference_rel
    reference_dst = output_dir / "assets" / "reader-v2-reference.docx"
    reference_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(reference_src, reference_dst)
    quarto_path.write_text(text.replace(docx_old, docx_new).replace(pdf_old, pdf_new), encoding="utf-8")
    return {
        "applied": True,
        "profile": str(profile_path.relative_to(ROOT)),
        "reference_doc": str(reference_src.relative_to(ROOT)),
    }


def preserve_artifacts(output_dir: Path, fmt: str, artifacts: list[str]) -> list[str]:
    snapshot_dir = output_dir / PRESERVED_ARTIFACT_DIR / fmt
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    if fmt == "html" and (output_dir / "_reader_site").is_dir():
        shutil.copytree(output_dir / "_reader_site", snapshot_dir / "_reader_site")
        return sorted(
            str(path.relative_to(output_dir))
            for path in snapshot_dir.rglob("*")
            if path.is_file()
        )

    preserved: list[str] = []
    for artifact in artifacts:
        src = output_dir / artifact
        if not src.is_file():
            continue
        dst = snapshot_dir / artifact
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        preserved.append(str(dst.relative_to(output_dir)))
    return sorted(preserved)


def canonicalize_epub(path: Path, manifest_path: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    profile_path = manifest_path.parent / TEXT_FORMAT_PROFILE_NAME
    profile = json.loads(profile_path.read_text(encoding="utf-8")) if profile_path.is_file() else {}
    edition_id = str(manifest.get("edition_id", "asi-stack-reader"))
    stable_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://asi-stack.org/editions/{edition_id}"))
    freeze_date = str(profile.get("freeze_date", "1980-01-01"))
    stable_timestamp = f"{freeze_date}T00:00:00Z"
    canonical = path.with_suffix(".canonical.epub")
    with ZipFile(path) as source:
        names = source.namelist()
        ordered = (["mimetype"] if "mimetype" in names else []) + sorted(
            name for name in names if name != "mimetype"
        )
        payloads = {name: source.read(name) for name in names}

        pinned_raster_replacements = 0
        pinned_rasters = (
            profile.get("shared_profile", {})
            .get("mermaid_policy", {})
            .get("epub_pinned_raster_members", [])
        )
        for record in pinned_rasters:
            member = record["member"]
            reference = ROOT / record["reference"]
            if member not in payloads:
                raise RuntimeError(f"pinned EPUB raster member is absent: {member}")
            if not reference.is_file():
                raise RuntimeError(f"pinned EPUB raster reference is absent: {reference}")
            reference_bytes = reference.read_bytes()
            observed = hashlib.sha256(reference_bytes).hexdigest()
            if observed != record["sha256"]:
                raise RuntimeError(
                    f"pinned EPUB raster reference drifted: {record['reference']} "
                    f"({observed} != {record['sha256']})"
                )
            payloads[member] = reference_bytes
            pinned_raster_replacements += 1

        identity_replacements = 0
        timestamp_replacements = 0
        for name in names:
            payload = payloads[name]
            replaced, count = re.subn(
                rb"urn:uuid:[0-9a-fA-F-]{36}",
                f"urn:uuid:{stable_uuid}".encode("ascii"),
                payload,
            )
            identity_replacements += count
            if name == "EPUB/content.opf":
                replaced, date_count = re.subn(
                    rb"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ",
                    stable_timestamp.encode("ascii"),
                    replaced,
                )
                timestamp_replacements += date_count
            payloads[name] = replaced

        appendix_target = ""
        first_chapter_target = ""
        nav_payload = payloads.get("EPUB/nav.xhtml", b"")
        if nav_payload:
            nav_tree = ET.fromstring(nav_payload)
            for node in nav_tree.iter():
                if node.tag.rsplit("}", 1)[-1] != "a":
                    continue
                node_text = " ".join(node.itertext())
                if manifest.get("chapter_records") and manifest["chapter_records"][0]["title"] in node_text:
                    first_chapter_target = node.attrib.get("href", "").split("#", 1)[0]
                if "External Sources by Other Authors" in node_text:
                    appendix_target = node.attrib.get("href", "").split("#", 1)[0]
        landmark_repairs = 0
        if nav_payload and first_chapter_target and b'epub:type="bodymatter"' not in nav_payload:
            landmark_pattern = re.compile(
                rb'(<nav\s+epub:type="landmarks"[\s\S]*?<ol>)([\s\S]*?)(</ol>\s*</nav>)'
            )
            bodymatter = (
                f'<li><a epub:type="bodymatter" href="{first_chapter_target}">Begin reading</a></li>'
            ).encode("utf-8")
            nav_payload, landmark_repairs = landmark_pattern.subn(
                lambda match: match.group(1) + match.group(2) + bodymatter + match.group(3),
                nav_payload,
                count=1,
            )
            payloads["EPUB/nav.xhtml"] = nav_payload
        link_repairs = 0
        if appendix_target:
            for name in names:
                if not name.endswith(".xhtml"):
                    continue
                owner_dir = Path(name).parent.as_posix()
                target = posixpath.relpath(posixpath.normpath(f"EPUB/{appendix_target}"), owner_dir)
                payloads[name], count = re.subn(
                    rb'href="H_external_sources\.qmd"',
                    f'href="{target}"'.encode("utf-8"),
                    payloads[name],
                )
                link_repairs += count

        with ZipFile(canonical, "w") as target:
            for name in ordered:
                info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_STORED if name == "mimetype" else ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                target.writestr(info, payloads[name], compresslevel=9)
    canonical.replace(path)
    return {
        "applied": True,
        "member_count": len(ordered),
        "mimetype_first_and_stored": ordered[:1] == ["mimetype"],
        "stable_edition_uuid": stable_uuid,
        "stable_metadata_timestamp": stable_timestamp,
        "identity_replacements": identity_replacements,
        "timestamp_replacements": timestamp_replacements,
        "internal_link_repairs": link_repairs,
        "landmark_repairs": landmark_repairs,
        "pinned_raster_replacements": pinned_raster_replacements,
    }


def convert_svg_to_png(svg_path: Path, png_path: Path) -> str:
    """Create a PNG fallback for non-HTML rendering without changing source assets."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("rsvg-convert"):
        subprocess.run(
            ["rsvg-convert", str(svg_path), "-o", str(png_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return "rsvg-convert"
    if shutil.which("sips"):
        subprocess.run(
            ["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return "sips"
    raise RuntimeError("no SVG-to-PNG converter found for raster fallback generation")


def find_chrome_binary() -> str:
    for candidate in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(candidate)
        if found:
            return found
    for candidate in CHROME_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return str(path)
    raise RuntimeError("no Chrome/Chromium binary found for PDF Mermaid fallback generation")


def html_path_for_qmd(output_dir: Path, qmd_path: Path) -> Path:
    relative = qmd_path.relative_to(output_dir).with_suffix(".html")
    return output_dir / "_reader_site" / relative


def ensure_html_for_mermaid(output_dir: Path, html_paths: list[Path]) -> bool:
    if all(path.exists() for path in html_paths):
        return False
    result = subprocess.run(
        ["quarto", "render", "--to", "html"],
        cwd=output_dir,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=render_environment(),
    )
    if result.returncode != 0:
        raise RuntimeError("HTML render for PDF Mermaid fallbacks failed:\n" + result.stdout[-2000:])
    missing = [str(path.relative_to(output_dir)) for path in html_paths if not path.exists()]
    if missing:
        raise RuntimeError("HTML render did not create expected Mermaid page(s): " + ", ".join(missing[:10]))
    return True


def rendered_mermaid_svgs(chrome_binary: str, html_path: Path) -> list[str]:
    node = shutil.which("node")
    if not node:
        raise RuntimeError("node executable is required for Mermaid SVG extraction")
    helper = ROOT / "scripts" / "extract_rendered_mermaid_svgs.js"
    env = os.environ.copy()
    env["PLAYWRIGHT_CHROMIUM_EXECUTABLE"] = chrome_binary
    try:
        result = subprocess.run(
            [node, str(helper), str(html_path.resolve())],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Playwright Mermaid SVG extraction timed out for {html_path.name}") from exc
    if result.returncode != 0:
        raise RuntimeError(
            f"Playwright Mermaid SVG extraction failed for {html_path.name} "
            f"({result.returncode}):\n{result.stderr[-2000:]}"
        )
    try:
        svgs = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Playwright Mermaid SVG extraction returned invalid JSON for {html_path.name}") from exc
    if not isinstance(svgs, list) or not all(isinstance(svg, str) for svg in svgs):
        raise RuntimeError(f"Playwright Mermaid SVG extraction returned an invalid SVG list for {html_path.name}")
    return [normalize_svg(svg) for svg in svgs]


def normalize_svg(svg: str) -> str:
    svg = svg.strip().replace("&nbsp;", "&#160;")
    svg = re.sub(r"<br([^>/]*?)>", r"<br\1/>", svg)
    svg = re.sub(r"animation\s*:[^;\"']*;", "animation:none;", svg)
    first_tag_end = svg.find(">")
    if first_tag_end != -1 and "xmlns=" not in svg[:first_tag_end]:
        svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg + "\n"


def mermaid_image_attrs(svg: str) -> str:
    width, height = svg_viewbox_size(svg)
    if height / max(width, 1.0) > 1.05:
        return 'height=5.85in fig-alt="Static rendered Mermaid diagram."'
    if width / max(height, 1.0) > 2.2:
        return 'width=95% fig-alt="Static rendered Mermaid diagram."'
    return 'width=90% fig-alt="Static rendered Mermaid diagram."'


def svg_viewbox_size(svg: str) -> tuple[float, float]:
    match = VIEWBOX_RE.search(svg)
    if not match:
        return (800.0, 500.0)
    return (float(match.group(1)), float(match.group(2)))


def render_svg_to_png_with_chrome(chrome_binary: str, svg: str, png_path: Path) -> str:
    width, height = svg_viewbox_size(svg)
    viewport_width = max(64, math.ceil(width))
    viewport_height = max(64, math.ceil(height))
    png_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="asi-mermaid-shot-") as temp_dir:
            html_path = Path(temp_dir) / "diagram.html"
            html_path.write_text(
                "\n".join(
                    [
                        "<!doctype html>",
                        "<html>",
                        "<head>",
                        "<meta charset=\"utf-8\">",
                        "<style>",
                        "html, body { margin: 0; padding: 0; background: #fff; overflow: hidden; }",
                        f"svg {{ width: {viewport_width}px !important; height: {viewport_height}px !important; max-width: none !important; }}",
                        "</style>",
                        "</head>",
                        "<body>",
                        svg,
                        "</body>",
                        "</html>",
                    ]
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    chrome_binary,
                    "--headless",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=10000",
                    "--timeout=60000",
                    f"--window-size={viewport_width},{viewport_height}",
                    f"--screenshot={png_path}",
                    html_path.resolve().as_uri(),
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
            )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Chrome SVG screenshot timed out for {png_path.name}") from exc
    if result.returncode != 0:
        raise RuntimeError(f"Chrome SVG screenshot failed for {png_path.name}: {result.stderr[-2000:]}")
    if not png_path.exists() or png_path.stat().st_size == 0:
        raise RuntimeError(f"Chrome SVG screenshot did not create {png_path}")
    return "chrome-screenshot"


def render_mermaid_svg_to_png(chrome_binary: str, svg_path: Path, svg: str, png_path: Path) -> str:
    """Render a browser-extracted Mermaid SVG into a static PNG fallback."""
    try:
        return convert_svg_to_png(svg_path, png_path)
    except (RuntimeError, subprocess.CalledProcessError):
        return render_svg_to_png_with_chrome(chrome_binary, svg, png_path)


@contextmanager
def pdf_mermaid_static_fallbacks(output_dir: Path) -> Iterator[dict[str, object]]:
    """Temporarily replace Mermaid fences with browser-rendered static PNGs."""
    qmd_paths = [
        path
        for path in sorted(output_dir.rglob("*.qmd"))
        if PRESERVED_ARTIFACT_DIR not in path.relative_to(output_dir).parts
    ]
    original_text: dict[Path, str] = {}
    matches_by_path: dict[Path, list[re.Match[str]]] = {}
    for path in qmd_paths:
        text = path.read_text(encoding="utf-8")
        matches = list(MERMAID_BLOCK_RE.finditer(text))
        if matches:
            original_text[path] = text
            matches_by_path[path] = matches

    fallback_info: dict[str, object] = {
        "applied": False,
        "chrome_binary": "",
        "converter": "",
        "fallback_count": 0,
        "rewritten_files": 0,
        "fallback_refs": [],
        "html_rendered_for_fallback": False,
        "error": "",
    }
    if not original_text:
        yield fallback_info
        return

    try:
        chrome_binary = find_chrome_binary()
        html_rendered = ensure_html_for_mermaid(
            output_dir,
            [html_path_for_qmd(output_dir, path) for path in original_text],
        )
        converter = ""
        fallback_refs: list[str] = []
        replacements_by_path: dict[Path, list[str]] = {}

        for qmd_path, matches in matches_by_path.items():
            html_path = html_path_for_qmd(output_dir, qmd_path)
            svgs = rendered_mermaid_svgs(chrome_binary, html_path)
            if len(svgs) < len(matches):
                raise RuntimeError(
                    f"expected at least {len(matches)} rendered Mermaid SVG(s) for "
                    f"{qmd_path.relative_to(output_dir)}, found {len(svgs)}"
                )

            replacements: list[str] = []
            file_stem = "-".join(qmd_path.relative_to(output_dir).with_suffix("").parts)
            for index, svg in enumerate(svgs[: len(matches)], start=1):
                svg_rel = Path("assets") / "diagrams" / "pdf-mermaid" / f"{file_stem}-mermaid-{index:02d}.svg"
                png_rel = svg_rel.with_suffix(".png")
                svg_path = output_dir / svg_rel
                png_path = output_dir / png_rel
                svg_path.parent.mkdir(parents=True, exist_ok=True)
                svg_path.write_text(svg, encoding="utf-8")
                converter = render_mermaid_svg_to_png(chrome_binary, svg_path, svg, png_path)
                fallback_refs.append(str(png_rel))
                image_ref = os.path.relpath(png_path, start=qmd_path.parent).replace(os.sep, "/")
                replacements.append(f"![]({image_ref}){{{mermaid_image_attrs(svg)}}}")
            replacements_by_path[qmd_path] = replacements

        for qmd_path, replacements in replacements_by_path.items():
            replacement_iter = iter(replacements)
            qmd_path.write_text(
                MERMAID_BLOCK_RE.sub(lambda _match: next(replacement_iter), original_text[qmd_path]),
                encoding="utf-8",
            )

        fallback_info = {
            "applied": True,
            "chrome_binary": chrome_binary,
            "converter": converter,
            "fallback_count": len(fallback_refs),
            "rewritten_files": len(original_text),
            "fallback_refs": fallback_refs,
            "html_rendered_for_fallback": html_rendered,
            "error": "",
        }
        yield fallback_info
    except Exception as exc:
        fallback_info["error"] = str(exc)
        raise
    finally:
        for path, text in original_text.items():
            path.write_text(text, encoding="utf-8")


@contextmanager
def raster_diagram_fallbacks(output_dir: Path) -> Iterator[dict[str, object]]:
    """Temporarily rewrite curated-reader diagram refs to PNG fallbacks."""
    qmd_paths = sorted(output_dir.rglob("*.qmd"))
    original_text: dict[Path, str] = {}
    refs: set[str] = set()
    for path in qmd_paths:
        text = path.read_text(encoding="utf-8")
        matches = list(DIAGRAM_SVG_REF_RE.finditer(text))
        if not matches:
            continue
        original_text[path] = text
        for match in matches:
            refs.add(match.group(3))

    fallback_info: dict[str, object] = {
        "applied": False,
        "converter": "",
        "fallback_count": 0,
        "rewritten_files": 0,
        "fallback_refs": [],
        "error": "",
    }
    if not refs:
        yield fallback_info
        return

    try:
        converter = ""
        fallback_refs: list[str] = []
        for ref in sorted(refs):
            svg_path = output_dir / "assets" / "diagrams" / f"{ref}.svg"
            png_rel = Path("assets") / "diagrams" / "format-png" / f"{ref}.png"
            png_path = output_dir / png_rel
            if not svg_path.exists():
                raise RuntimeError(f"missing SVG diagram for raster fallback: {svg_path}")
            converter = convert_svg_to_png(svg_path, png_path)
            fallback_refs.append(str(png_rel))

        for path, text in original_text.items():
            def replace(match: re.Match[str]) -> str:
                return f"{match.group(1)}{match.group(2)}format-png/{match.group(3)}.png{match.group(4)}"

            path.write_text(DIAGRAM_SVG_REF_RE.sub(replace, text), encoding="utf-8")

        fallback_info = {
            "applied": True,
            "converter": converter,
            "fallback_count": len(fallback_refs),
            "rewritten_files": len(original_text),
            "fallback_refs": fallback_refs,
            "error": "",
        }
        yield fallback_info
    except Exception as exc:  # pragma: no cover - recorded in render report.
        fallback_info["error"] = str(exc)
        raise
    finally:
        for path, text in original_text.items():
            path.write_text(text, encoding="utf-8")


def run_bounded_render(
    command: list[str], output_dir: Path, log_file: object, timeout_seconds: int
) -> tuple[int, bool]:
    process = subprocess.Popen(
        command,
        cwd=output_dir,
        text=True,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        env=render_environment(),
        start_new_session=True,
    )
    try:
        return process.wait(timeout=timeout_seconds), False
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        return 124, True


def run_render(
    output_dir: Path, fmt: str, timeout_seconds: int, manifest_path: Path
) -> dict[str, object]:
    command = ["quarto", "render", "--to", fmt]
    fallback_info: dict[str, object] = {
        "applied": False,
        "converter": "",
        "fallback_count": 0,
        "rewritten_files": 0,
        "fallback_refs": [],
        "error": "",
    }
    mermaid_fallback_info: dict[str, object] = {
        "applied": False,
        "chrome_binary": "",
        "converter": "",
        "fallback_count": 0,
        "rewritten_files": 0,
        "fallback_refs": [],
        "html_rendered_for_fallback": False,
        "error": "",
    }
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", errors="ignore") as log_file:
        if fmt == "pdf":
            with raster_diagram_fallbacks(output_dir) as fallback_info:
                with pdf_mermaid_static_fallbacks(output_dir) as mermaid_fallback_info:
                    returncode, timed_out = run_bounded_render(
                        command, output_dir, log_file, timeout_seconds
                    )
        elif fmt == "docx":
            with raster_diagram_fallbacks(output_dir) as fallback_info:
                with pdf_mermaid_static_fallbacks(output_dir) as mermaid_fallback_info:
                    returncode, timed_out = run_bounded_render(
                        command, output_dir, log_file, timeout_seconds
                    )
        elif fmt == "epub":
            with pdf_mermaid_static_fallbacks(output_dir) as mermaid_fallback_info:
                returncode, timed_out = run_bounded_render(
                    command, output_dir, log_file, timeout_seconds
                )
        else:
            returncode, timed_out = run_bounded_render(
                command, output_dir, log_file, timeout_seconds
            )
        log_file.seek(0)
        output = log_file.read()
    artifacts = find_artifacts(output_dir, fmt) if returncode == 0 else []
    epub_canonicalization: dict[str, object] = {"applied": False}
    if fmt == "epub" and artifacts:
        if len(artifacts) != 1:
            raise RuntimeError(f"expected one EPUB artifact before canonicalization, found {len(artifacts)}")
        epub_canonicalization = canonicalize_epub(output_dir / artifacts[0], manifest_path)
    preserved_artifacts = preserve_artifacts(output_dir, fmt, artifacts) if artifacts else []
    warning_lines = [line for line in output.splitlines() if "[WARNING]" in line]
    svg_conversion_warning_count = sum("Could not convert image" in line for line in warning_lines)
    return {
        "format": fmt,
        "status": "rendered" if returncode == 0 else "failed",
        "returncode": returncode,
        "timed_out": timed_out,
        "timeout_seconds": timeout_seconds,
        "command": " ".join(command),
        "artifacts": artifacts,
        "preserved_artifacts": preserved_artifacts,
        "warning_count": len(warning_lines),
        "svg_conversion_warning_count": svg_conversion_warning_count,
        "raster_diagram_fallbacks": fallback_info,
        "pdf_mermaid_static_fallbacks": mermaid_fallback_info,
        "epub_canonicalization": epub_canonicalization,
        "log_excerpt": output[-4000:],
    }


def write_report(
    output_dir: Path,
    generation_report: dict[str, object],
    render_records: list[dict[str, object]],
    manifest_path: Path,
) -> dict[str, object]:
    report = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_mode": "tracked_curated_reader_manuscript",
        "source_manifest": str(manifest_path.resolve().relative_to(ROOT)),
        "curated_generation": generation_report,
        "format_results": render_records,
        "review_status": "review_required",
        "release_blockers_preserved": [
            "format_artifact_not_reviewed",
            "reader_release_record_not_created",
            "full_format_artifact_review_not_completed",
            "app_or_ereader_review_not_completed",
        ],
        "non_claims": [
            "This report records local curated-reader render attempts only.",
            "A rendered curated-reader file is not a published major-version edition until reviewed and listed in an edition release record.",
            "Preserved artifacts are local snapshots in an ignored review workspace, not release artifacts.",
            "EPUB and DOCX renders are structural review inputs only until application-level review is complete.",
            "PDF renders are structural review inputs only until layout/page review and release approval are complete.",
            "Audio artifacts are not produced by this curated-reader format renderer.",
            "This report does not promote any claim support state.",
        ],
    }
    (output_dir / REPORT_NAME).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="reader profile id to use for scaffolding")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="tracked curated-reader manifest")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="generated curated reader workspace")
    parser.add_argument(
        "--formats",
        nargs="+",
        default=list(DEFAULT_FORMATS),
        help="Quarto formats to render, for example: html epub docx pdf",
    )
    parser.add_argument("--include-pdf", action="store_true", help="also attempt PDF if it is not already listed")
    parser.add_argument("--stop-on-fail", action="store_true", help="stop after the first failed format render")
    parser.add_argument("--timeout-seconds", type=int, default=300, help="per-format render timeout")
    parser.add_argument("--check", action="store_true", help="validate setup in a temporary workspace without rendering formats")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.timeout_seconds < 30:
        raise SystemExit("Curated reader format timeout must be at least 30 seconds.")
    manifest_path = Path(args.manifest)
    formats = list(dict.fromkeys(args.formats + (["pdf"] if args.include_pdf else [])))

    if args.check:
        if shutil.which("quarto") is None:
            raise SystemExit("Curated reader format render check failed: quarto is not on PATH.")
        with tempfile.TemporaryDirectory(prefix="asi-curated-reader-render-check-") as temp_dir:
            report = build_curated_reader_edition.generate(Path(temp_dir), args.profile, manifest_path)
            if not (Path(temp_dir) / "reader_manifest.json").exists():
                raise SystemExit("Curated reader format render check failed: missing reader_manifest.json.")
            print(
                "Curated reader format render check passed: "
                f"{report['chapter_count']} curated chapters ready for formats {', '.join(formats)}."
            )
            return

    if shutil.which("quarto") is None:
        raise SystemExit("Cannot render curated reader formats: quarto is not on PATH.")

    output_dir = Path(args.output)
    generation_report = build_curated_reader_edition.generate(output_dir, args.profile, manifest_path)
    generation_report["frozen_text_format_profile"] = apply_frozen_text_format_profile(
        output_dir, manifest_path
    )
    render_records: list[dict[str, object]] = []
    for fmt in formats:
        record = run_render(output_dir, fmt, args.timeout_seconds, manifest_path)
        render_records.append(record)
        print(f"{fmt}: {record['status']}")
        if args.stop_on_fail and record["status"] != "rendered":
            break

    report = write_report(output_dir, generation_report, render_records, manifest_path)
    failed = [record["format"] for record in render_records if record["status"] != "rendered"]
    print(f"Curated reader render report wrote: {output_dir / REPORT_NAME}")
    if failed:
        print(f"Failed formats: {', '.join(str(value) for value in failed)}")
        raise SystemExit(1)
    print(f"Rendered curated reader formats recorded: {len(report['format_results'])}")


if __name__ == "__main__":
    main()
