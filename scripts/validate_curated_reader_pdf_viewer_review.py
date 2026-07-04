#!/usr/bin/env python3
"""Record a bounded Chromium PDF-viewer review for the curated reader PDF.

The write path opens the ignored local PDF artifact in an isolated headed
Chromium/Chrome instance, captures two viewer screenshots, and records only
summary evidence in the tracked curated format probe manifest. The default path
validates the tracked manifest entry without requiring a local GUI or ignored
build artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
PDF = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "pdf" / "_reader_site" / "The-ASI-Stack.pdf"
REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_pdf_viewer_review_report.json"
SCREENSHOT_DIR = ROOT / "build" / "curated_reader_edition" / "pdf_viewer_review"
COMMAND = "python3 scripts/validate_curated_reader_pdf_viewer_review.py --write-manifest"
VIEWPORT = {"width": 1280, "height": 900}

NODE_CAPTURE = r"""
const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

function candidateModuleRoots(root) {
  const roots = [];
  for (const key of ["NODE_PATH", "CODEX_PLAYWRIGHT_NODE_MODULES", "CODEX_NODE_MODULES"]) {
    const value = process.env[key];
    if (value) roots.push(...value.split(path.delimiter).filter(Boolean));
  }
  roots.push(path.join(root, "node_modules"));
  roots.push(path.join(os.homedir(), ".cache", "codex-runtimes", "codex-primary-runtime", "dependencies", "node", "node_modules"));
  return [...new Set(roots)];
}

function loadPlaywright(root) {
  try { return require("playwright"); } catch (_) {}
  for (const moduleRoot of candidateModuleRoots(root)) {
    const candidate = moduleRoot.endsWith("playwright") ? moduleRoot : path.join(moduleRoot, "playwright");
    if (!fs.existsSync(candidate)) continue;
    try { return require(candidate); } catch (_) {}
  }
  return null;
}

function browserExecutables() {
  const candidates = [];
  if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) candidates.push(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE);
  candidates.push(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser"
  );
  return [...new Set(candidates)].filter((candidate) => fs.existsSync(candidate));
}

async function launch(playwright) {
  const errors = [];
  for (const executablePath of browserExecutables()) {
    try {
      return await playwright.chromium.launch({ headless: false, executablePath });
    } catch (error) {
      errors.push(`${executablePath}: ${error.message}`);
    }
  }
  try {
    return await playwright.chromium.launch({ headless: false });
  } catch (error) {
    errors.push(`managed chromium: ${error.message}`);
  }
  throw new Error(`Could not launch headed Chromium for PDF viewer review: ${errors.join(" | ")}`);
}

(async () => {
  const root = process.argv[1];
  const pdf = process.argv[2];
  const screenshotDir = process.argv[3];
  const width = Number(process.argv[4]);
  const height = Number(process.argv[5]);
  const playwright = loadPlaywright(root);
  if (!playwright) throw new Error("Playwright is not available.");
  fs.mkdirSync(screenshotDir, { recursive: true });
  const browser = await launch(playwright);
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto(pathToFileURL(pdf).href, { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.waitForTimeout(5000);
  const first = path.join(screenshotDir, "page-1-viewer.png");
  await page.screenshot({ path: first, fullPage: false });
  await page.mouse.move(Math.floor(width * 0.65), Math.floor(height * 0.5));
  await page.mouse.wheel(0, 900);
  await page.waitForTimeout(1000);
  const second = path.join(screenshotDir, "page-down-viewer.png");
  await page.screenshot({ path: second, fullPage: false });
  const info = await page.evaluate(() => ({
    url: location.href,
    title: document.title || "",
    body_text_characters: document.body && document.body.innerText ? document.body.innerText.length : 0,
    html_shell_characters: document.documentElement ? document.documentElement.outerHTML.length : 0,
    pdf_embedder_css_present: Boolean(document.querySelector('link[href*="pdf_embedder.css"]')),
  }));
  const userAgent = await page.evaluate(() => navigator.userAgent);
  await browser.close();
  console.log(JSON.stringify({ ...info, user_agent: userAgent, screenshots: [first, second] }));
})().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
"""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(errors: list[str]) -> None:
    print("Curated reader PDF viewer review validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def pdfinfo_pages(path: Path) -> int:
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    match = re.search(r"^Pages:\s+(\d+)", output, re.MULTILINE)
    if not match:
        fail(["pdfinfo output did not include a Pages row."])
    return int(match.group(1))


def screenshot_metrics(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    pixels = image.getdata()
    total = image.width * image.height
    dark = sum(1 for r, g, b in pixels if r < 80 and g < 80 and b < 80)
    white = sum(1 for r, g, b in pixels if r > 245 and g > 245 and b > 245)
    stat = ImageStat.Stat(image)
    channel_stds = [float(value) for value in stat.stddev]
    return {
        "path": rel(path),
        "bytes": path.stat().st_size,
        "width": image.width,
        "height": image.height,
        "dark_pixel_percent": round(dark / total * 100, 3),
        "white_pixel_percent": round(white / total * 100, 3),
        "luminance_variation_proxy": round(sum(channel_stds) / len(channel_stds), 3),
    }


def screenshot_difference_percent(first: Path, second: Path) -> float:
    a = Image.open(first).convert("RGB")
    b = Image.open(second).convert("RGB")
    if a.size != b.size:
        return 100.0
    diff = ImageChops.difference(a, b)
    changed = 0
    for pixel in diff.getdata():
        if pixel != (0, 0, 0):
            changed += 1
    return round(changed / (a.width * a.height) * 100, 3)


def run_browser_capture() -> dict[str, Any]:
    if not PDF.exists():
        fail([f"Missing curated reader PDF artifact: {rel(PDF)}. Run render_curated_reader_formats first."])
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for existing in SCREENSHOT_DIR.glob("*.png"):
        existing.unlink()
    completed = subprocess.run(
        [
            "node",
            "-e",
            NODE_CAPTURE,
            str(ROOT),
            str(PDF),
            str(SCREENSHOT_DIR),
            str(VIEWPORT["width"]),
            str(VIEWPORT["height"]),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"},
    )
    if completed.returncode != 0:
        fail([f"Headed Chromium PDF viewer capture failed: {completed.stderr[-2000:]}"])
    try:
        capture = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail([f"Headed Chromium PDF viewer capture did not emit JSON: {exc}; stdout={completed.stdout[-1000:]!r}"])
    screenshots = [Path(item) for item in capture.get("screenshots", [])]
    if len(screenshots) != 2:
        fail(["Headed Chromium PDF viewer capture must produce two screenshots."])
    return {
        "status": "passed_chromium_pdf_viewer_smoke_review",
        "source_artifact": rel(PDF),
        "source_sha256": sha256_file(PDF),
        "report_ref": rel(REPORT),
        "review_command": COMMAND,
        "renderer": "Google Chrome PDF viewer through headed Playwright",
        "viewport_width": VIEWPORT["width"],
        "viewport_height": VIEWPORT["height"],
        "pdfinfo_pages": pdfinfo_pages(PDF),
        "viewer_url_scheme": "file",
        "viewer_shell_detected": bool(capture.get("pdf_embedder_css_present")),
        "viewer_dom_body_text_characters": int(capture.get("body_text_characters", 0)),
        "viewer_html_shell_characters": int(capture.get("html_shell_characters", 0)),
        "user_agent": str(capture.get("user_agent", "")),
        "screenshots": [screenshot_metrics(path) for path in screenshots],
        "page_down_changed_pixel_percent": screenshot_difference_percent(screenshots[0], screenshots[1]),
        "review_boundary": (
            "This headed Chromium PDF viewer smoke review verifies that the ignored local PDF opens in a real "
            "PDF viewer surface and produces nonblank viewer screenshots before and after navigation. It is not "
            "manual page-by-page PDF review, not PDF content approval, and does not approve the PDF artifact."
        ),
        "non_claims": [
            "does not approve the PDF artifact for release",
            "does not replace manual PDF page-by-page reading-flow or layout review",
            "does not replace final figure-artifact review",
            "does not publish or archive a reader artifact",
            "does not approve EPUB, DOCX, e-reader, audio, or final figure artifacts",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_observed(observed: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if observed.get("status") != "passed_chromium_pdf_viewer_smoke_review":
        errors.append("pdf_viewer_review.status must be passed_chromium_pdf_viewer_smoke_review.")
    if observed.get("source_artifact") != rel(PDF):
        errors.append("pdf_viewer_review.source_artifact must point to the curated reader PDF.")
    if not re.fullmatch(r"[0-9a-f]{64}", str(observed.get("source_sha256", ""))):
        errors.append("pdf_viewer_review.source_sha256 must be a SHA-256 digest.")
    pdf_summary = manifest.get("inspection_summary", {}).get("pdf", {})
    if isinstance(pdf_summary, dict):
        if observed.get("source_sha256") != pdf_summary.get("sha256"):
            errors.append("pdf_viewer_review.source_sha256 must match inspection_summary.pdf.sha256.")
        if observed.get("pdfinfo_pages") != pdf_summary.get("pages"):
            errors.append("pdf_viewer_review.pdfinfo_pages must match inspection_summary.pdf.pages.")
    expected_exact = {
        "renderer": "Google Chrome PDF viewer through headed Playwright",
        "viewport_width": VIEWPORT["width"],
        "viewport_height": VIEWPORT["height"],
        "viewer_url_scheme": "file",
        "viewer_shell_detected": True,
        "viewer_dom_body_text_characters": 0,
    }
    for key, expected in expected_exact.items():
        if observed.get(key) != expected:
            errors.append(f"pdf_viewer_review.{key} must be {expected!r}; found {observed.get(key)!r}.")
    if observed.get("viewer_html_shell_characters", 0) < 100:
        errors.append("pdf_viewer_review.viewer_html_shell_characters is unexpectedly small.")
    screenshots = observed.get("screenshots")
    if not isinstance(screenshots, list) or len(screenshots) != 2:
        errors.append("pdf_viewer_review.screenshots must contain two rows.")
        screenshots = []
    for index, row in enumerate(screenshots):
        if not isinstance(row, dict):
            errors.append("pdf_viewer_review screenshot rows must be objects.")
            continue
        if row.get("width") != VIEWPORT["width"] or row.get("height") != VIEWPORT["height"]:
            errors.append(f"pdf_viewer_review screenshot {index} dimensions must be 1280 x 900.")
        if row.get("bytes", 0) < 20_000:
            errors.append(f"pdf_viewer_review screenshot {index} file size is too small for a rendered viewer.")
        if row.get("dark_pixel_percent", 0) < 10:
            errors.append(f"pdf_viewer_review screenshot {index} must include dark PDF viewer chrome.")
        if row.get("white_pixel_percent", 0) < 20:
            errors.append(f"pdf_viewer_review screenshot {index} must include a visible white PDF page region.")
        if row.get("luminance_variation_proxy", 0) < 40:
            errors.append(f"pdf_viewer_review screenshot {index} luminance variation is too low.")
    if observed.get("page_down_changed_pixel_percent", 0) < 1:
        errors.append("pdf_viewer_review page_down_changed_pixel_percent must show visible navigation change.")
    boundary = str(observed.get("review_boundary", ""))
    if "not manual page-by-page PDF review" not in boundary or "does not approve the PDF artifact" not in boundary:
        errors.append("pdf_viewer_review.review_boundary must preserve manual-review and approval boundaries.")
    non_claim_text = " ".join(str(item) for item in observed.get("non_claims", [])).lower()
    for phrase in (
        "does not approve the pdf artifact",
        "does not replace manual pdf page-by-page",
        "does not replace final figure-artifact review",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"pdf_viewer_review.non_claims missing boundary phrase: {phrase}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="run headed Chromium and write the manifest entry")
    args = parser.parse_args()

    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain a JSON object."])

    if args.write_manifest:
        observed = run_browser_capture()
        report = {
            "schema_version": "0.1",
            "review_type": "curated_reader_pdf_chromium_viewer_smoke_review",
            "manifest": observed,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        errors = validate_observed(observed, manifest)
        if errors:
            fail(errors)
        commands = manifest.setdefault("source_commands", [])
        if COMMAND not in commands:
            commands.append(COMMAND)
        refs = manifest.setdefault("local_report_refs", [])
        if rel(REPORT) not in refs:
            refs.append(rel(REPORT))
        manifest["pdf_viewer_review"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        observed = manifest.get("pdf_viewer_review")
        if not isinstance(observed, dict):
            fail(["curated_format_probe_manifest.json is missing pdf_viewer_review; run with --write-manifest."])
        errors = validate_observed(observed, manifest)
        if errors:
            fail(errors)

    print(
        "Curated reader PDF viewer review passed: "
        f"{manifest.get('pdf_viewer_review', observed)['pdfinfo_pages']} pages, "
        f"{len(manifest.get('pdf_viewer_review', observed)['screenshots'])} viewer screenshots."
    )


if __name__ == "__main__":
    main()
