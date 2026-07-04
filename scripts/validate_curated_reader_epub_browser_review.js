#!/usr/bin/env node
/*
Render the curated reader EPUB spine XHTML in Chromium and record a bounded
application-level review manifest.

This is not a release approval tool and not a dedicated e-reader review. It
checks the ignored local EPUB artifact through a browser application renderer,
then stores only summary evidence in the tracked curated format probe manifest.
*/

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { pathToFileURL } = require("url");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_EPUB = path.join(
  ROOT,
  "build",
  "curated_reader_edition",
  "format_artifacts",
  "epub",
  "_reader_site",
  "The-ASI-Stack.epub"
);
const DEFAULT_REPORT = path.join(
  ROOT,
  "build",
  "curated_reader_edition",
  "curated_reader_epub_browser_review_report.json"
);
const DEFAULT_MANIFEST = path.join(
  ROOT,
  "editions",
  "reader_manuscript",
  "v1_0",
  "curated_format_probe_manifest.json"
);
const VIEWPORTS = {
  desktop: { width: 1120, height: 900 },
  ereader: { width: 600, height: 900 },
};
const REQUIRED_MARKERS = [
  "The ASI Stack",
  "Reader Edition Draft",
  "evidence boundary",
  "Reader Source List",
  "External Citation Policy",
];
const LIVE_ONLY_MARKERS = [
  "Chapter status",
  "Drafting guardrail",
  "Codex test plan",
  "Source crosswalk",
  "Claim-source mapping status",
  "Formalization hooks",
];
const RAW_CORE_CLAIM_RE = /\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]/;

function parseArgs(argv) {
  const args = {
    epub: DEFAULT_EPUB,
    report: DEFAULT_REPORT,
    manifest: DEFAULT_MANIFEST,
    writeManifest: false,
    strict: true,
  };
  for (let index = 2; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--epub") {
      args.epub = path.resolve(argv[++index]);
    } else if (value === "--report") {
      args.report = path.resolve(argv[++index]);
    } else if (value === "--manifest") {
      args.manifest = path.resolve(argv[++index]);
    } else if (value === "--write-manifest") {
      args.writeManifest = true;
    } else if (value === "--no-strict") {
      args.strict = false;
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }
  return args;
}

function candidateModuleRoots() {
  const roots = [];
  for (const key of ["NODE_PATH", "CODEX_PLAYWRIGHT_NODE_MODULES", "CODEX_NODE_MODULES"]) {
    const value = process.env[key];
    if (value) roots.push(...value.split(path.delimiter).filter(Boolean));
  }
  roots.push(path.join(ROOT, "node_modules"));
  roots.push(
    path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules"
    )
  );
  return [...new Set(roots)];
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (_) {
    // Continue to known module roots.
  }
  for (const root of candidateModuleRoots()) {
    const candidate = root.endsWith("playwright") ? root : path.join(root, "playwright");
    if (!fs.existsSync(candidate)) continue;
    try {
      return require(candidate);
    } catch (_) {
      // Continue trying candidates.
    }
  }
  return null;
}

function candidateBrowserExecutables() {
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

async function launchChromium(playwright) {
  try {
    return await playwright.chromium.launch({ headless: true });
  } catch (managedError) {
    for (const executablePath of candidateBrowserExecutables()) {
      try {
        return await playwright.chromium.launch({ headless: true, executablePath });
      } catch (_) {
        // Keep trying candidates.
      }
    }
    throw managedError;
  }
}

function relative(filePath) {
  return path.relative(ROOT, filePath);
}

function sha256File(filePath) {
  const hash = crypto.createHash("sha256");
  hash.update(fs.readFileSync(filePath));
  return hash.digest("hex");
}

function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function attr(tag, name) {
  const match = tag.match(new RegExp(`${name}=["']([^"']+)["']`));
  return match ? match[1] : "";
}

function resolveZipPath(base, href) {
  return path.posix.normalize(path.posix.join(path.posix.dirname(base), href));
}

function parseContainer(root) {
  const containerPath = path.join(root, "META-INF", "container.xml");
  const text = readText(containerPath);
  const match = text.match(/full-path=["']([^"']+)["']/);
  if (!match) throw new Error("Could not find EPUB rootfile full-path.");
  return match[1];
}

function parseOpf(root, opfZipPath) {
  const opfPath = path.join(root, ...opfZipPath.split("/"));
  const opfText = readText(opfPath);
  const manifest = new Map();
  for (const match of opfText.matchAll(/<item\b[^>]*>/g)) {
    const tag = match[0];
    const id = attr(tag, "id");
    const href = attr(tag, "href");
    const mediaType = attr(tag, "media-type");
    if (id && href) {
      manifest.set(id, {
        id,
        href,
        mediaType,
        zipPath: resolveZipPath(opfZipPath, href),
      });
    }
  }
  const spine = [];
  for (const match of opfText.matchAll(/<itemref\b[^>]*>/g)) {
    const idref = attr(match[0], "idref");
    const item = manifest.get(idref);
    if (item) spine.push(item);
  }
  return { opfText, manifest, spine };
}

function unpackEpub(epubPath) {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "asi-curated-epub-review-"));
  execFileSync("unzip", ["-q", epubPath, "-d", tempRoot], { stdio: "pipe" });
  return tempRoot;
}

function textMarkerCounts(results) {
  const markerCounts = Object.fromEntries(REQUIRED_MARKERS.map((marker) => [marker, 0]));
  for (const result of results) {
    for (const marker of REQUIRED_MARKERS) {
      if ((result.body_text || "").includes(marker)) markerCounts[marker] += 1;
    }
  }
  return markerCounts;
}

function isContentEntry(zipPath) {
  return /^EPUB\/text\/ch\d+\.xhtml$/.test(zipPath);
}

function isCoverEntry(zipPath) {
  return zipPath === "EPUB/text/cover.xhtml";
}

async function inspectPage(page, root, item, viewportName, viewportSize) {
  const filePath = path.join(root, ...item.zipPath.split("/"));
  await page.setViewportSize(viewportSize);
  await page.goto(pathToFileURL(filePath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(200);

  const text = await page.locator("body").innerText({ timeout: 5000 });
  const metrics = await page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    const main = document.querySelector("main") || document.body;
    const title = document.querySelector("h1, h2, title");
    const scrollWidth = Math.max(doc.scrollWidth, body ? body.scrollWidth : 0);
    const clientWidth = doc.clientWidth;
    const images = Array.from(document.querySelectorAll("img")).map((img) => {
      const rect = img.getBoundingClientRect();
      return {
        src: img.getAttribute("src") || "",
        complete: Boolean(img.complete),
        natural_width: img.naturalWidth || 0,
        natural_height: img.naturalHeight || 0,
        rendered_width: Math.round(rect.width),
        rendered_height: Math.round(rect.height),
      };
    });
    return {
      title: title ? title.textContent.trim() : "",
      body_text_chars: body ? body.innerText.length : 0,
      stylesheet_count: document.styleSheets.length,
      image_count: images.length,
      images,
      svg_count: document.querySelectorAll("svg").length,
      main_visible: Boolean(main && main.getBoundingClientRect().height > 0),
      scroll_width: scrollWidth,
      client_width: clientWidth,
      horizontal_overflow_px: Math.max(0, scrollWidth - clientWidth),
    };
  });

  const errors = [];
  const textMinimum = isContentEntry(item.zipPath) ? 500 : isCoverEntry(item.zipPath) ? 0 : 20;
  if (metrics.body_text_chars < textMinimum) {
    errors.push(`body text too short: ${metrics.body_text_chars}`);
  }
  if (!metrics.main_visible) errors.push("main content is not visible");
  if (metrics.stylesheet_count < 1) errors.push("no stylesheets loaded");
  if (metrics.horizontal_overflow_px > 24) {
    errors.push(`horizontal overflow ${metrics.horizontal_overflow_px}px`);
  }
  if (RAW_CORE_CLAIM_RE.test(text)) errors.push("raw core-claim marker leaked");
  for (const marker of LIVE_ONLY_MARKERS) {
    if (text.includes(marker)) errors.push(`live-only marker leaked: ${marker}`);
  }
  for (const image of metrics.images) {
    if (!image.complete) errors.push(`image did not finish loading: ${image.src}`);
    if (image.natural_width <= 0 || image.natural_height <= 0) {
      errors.push(`image has no natural dimensions: ${image.src}`);
    }
  }

  return {
    zip_path: item.zipPath,
    viewport: viewportName,
    body_text: text,
    ...metrics,
    status: errors.length ? "failed" : "passed",
    errors,
  };
}

function compactResult(result) {
  const { body_text: _bodyText, images, ...rest } = result;
  return {
    ...rest,
    image_failures: images.filter(
      (image) => !image.complete || image.natural_width <= 0 || image.natural_height <= 0
    ),
  };
}

function buildManifest(args, spine, results, failures) {
  const contentEntries = spine.filter((item) => isContentEntry(item.zipPath));
  const contentResults = results.filter((result) => isContentEntry(result.zip_path));
  const markerCounts = textMarkerCounts(results);
  const bodyCounts = results.map((result) => result.body_text_chars);
  const contentBodyCounts = contentResults.map((result) => result.body_text_chars);
  const overflowValues = results.map((result) => result.horizontal_overflow_px);
  const imageResults = results.flatMap((result) => result.images || []);
  return {
    status: failures.length ? "failed_browser_xhtml_application_review" : "passed_browser_xhtml_application_review",
    source_artifact: relative(args.epub),
    source_sha256: sha256File(args.epub),
    report_ref: relative(args.report),
    review_command:
      "node scripts/validate_curated_reader_epub_browser_review.js --write-manifest",
    renderer: "Chromium via Playwright over unpacked EPUB spine XHTML",
    spine_entries_checked: spine.length,
    content_xhtml_entries_checked: contentEntries.length,
    viewport_count: Object.keys(VIEWPORTS).length,
    page_view_pairs: results.length,
    failed_page_view_pairs: failures.length,
    rendered_image_count: imageResults.length,
    image_load_failures: imageResults.filter(
      (image) => !image.complete || image.natural_width <= 0 || image.natural_height <= 0
    ).length,
    max_horizontal_overflow_px: Math.max(...overflowValues),
    min_body_text_chars: Math.min(...bodyCounts),
    min_content_body_text_chars: Math.min(...contentBodyCounts),
    required_text_markers_present: REQUIRED_MARKERS.filter((marker) => markerCounts[marker] > 0),
    live_marker_hits: results.filter((result) =>
      LIVE_ONLY_MARKERS.some((marker) => (result.body_text || "").includes(marker))
    ).length,
    raw_core_claim_marker_hits: results.filter((result) =>
      RAW_CORE_CLAIM_RE.test(result.body_text || "")
    ).length,
    failure_samples: failures.slice(0, 12).map(compactResult),
    review_boundary:
      "This Chromium pass renders the unpacked EPUB spine XHTML as a local browser application review; it is stronger than package inspection, but it is not dedicated e-reader device/app approval, not a release record, and does not approve the EPUB artifact.",
    non_claims: [
      "does not approve the EPUB artifact for release",
      "does not replace dedicated e-reader device or application review",
      "does not publish or archive a reader artifact",
      "does not approve DOCX, PDF, audio, e-reader, or final figure artifacts",
      "does not promote any chapter core claim or support state",
    ],
  };
}

function validateManifestShape(manifest) {
  const errors = [];
  if (manifest.status !== "passed_browser_xhtml_application_review") {
    errors.push("epub_browser_review.status must be passed_browser_xhtml_application_review.");
  }
  if (manifest.source_artifact !== relative(DEFAULT_EPUB)) {
    errors.push("epub_browser_review.source_artifact must point to the curated reader EPUB.");
  }
  if (!/^[0-9a-f]{64}$/.test(String(manifest.source_sha256 || ""))) {
    errors.push("epub_browser_review.source_sha256 must be a SHA-256 digest.");
  }
  if (manifest.spine_entries_checked !== 52) errors.push("spine_entries_checked must be 52.");
  if (manifest.content_xhtml_entries_checked !== 49) errors.push("content_xhtml_entries_checked must be 49.");
  if (manifest.viewport_count !== 2) errors.push("viewport_count must be 2.");
  if (manifest.page_view_pairs !== 104) errors.push("page_view_pairs must be 104.");
  if (manifest.failed_page_view_pairs !== 0) errors.push("failed_page_view_pairs must be 0.");
  if (manifest.image_load_failures !== 0) errors.push("image_load_failures must be 0.");
  if (manifest.live_marker_hits !== 0) errors.push("live_marker_hits must be 0.");
  if (manifest.raw_core_claim_marker_hits !== 0) errors.push("raw_core_claim_marker_hits must be 0.");
  if (manifest.min_content_body_text_chars < 500) {
    errors.push("min_content_body_text_chars must be at least 500.");
  }
  for (const marker of REQUIRED_MARKERS) {
    if (!manifest.required_text_markers_present.includes(marker)) {
      errors.push(`required_text_markers_present missing ${marker}.`);
    }
  }
  const boundary = String(manifest.review_boundary || "");
  if (!boundary.includes("not dedicated e-reader") || !boundary.includes("does not approve the EPUB artifact")) {
    errors.push("review_boundary must preserve e-reader and release-approval boundaries.");
  }
  return errors;
}

async function main() {
  const args = parseArgs(process.argv);
  if (!fs.existsSync(args.epub)) {
    throw new Error(`Curated reader EPUB not found: ${args.epub}`);
  }
  if (!fs.existsSync(args.manifest)) {
    throw new Error(`Curated reader format probe manifest not found: ${args.manifest}`);
  }

  const playwright = loadPlaywright();
  if (!playwright) {
    const message = "Playwright is not available; curated reader EPUB browser review skipped.";
    if (args.strict) throw new Error(message);
    console.log(message);
    return;
  }

  const tempRoot = unpackEpub(args.epub);
  const rootfile = parseContainer(tempRoot);
  const { spine } = parseOpf(tempRoot, rootfile);
  if (spine.length < 1) {
    throw new Error("EPUB spine is empty.");
  }

  const browser = await launchChromium(playwright);
  const page = await browser.newPage();
  const results = [];
  try {
    for (const item of spine) {
      for (const [viewportName, viewportSize] of Object.entries(VIEWPORTS)) {
        results.push(await inspectPage(page, tempRoot, item, viewportName, viewportSize));
      }
    }
  } finally {
    await browser.close();
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }

  const failures = results.filter((result) => result.status !== "passed");
  const manifestRecord = buildManifest(args, spine, results, failures);

  const report = {
    schema_version: "0.1",
    review_type: "curated_reader_epub_browser_xhtml_application_review",
    rootfile,
    manifest: manifestRecord,
    spine_entries: spine.map((item) => item.zipPath),
    results: results.map(compactResult),
  };
  fs.mkdirSync(path.dirname(args.report), { recursive: true });
  fs.writeFileSync(args.report, JSON.stringify(report, null, 2) + "\n", "utf8");

  const shapeErrors = validateManifestShape(manifestRecord);
  if (shapeErrors.length) {
    throw new Error(`EPUB browser review manifest shape failed:\n - ${shapeErrors.join("\n - ")}`);
  }

  const trackedManifest = JSON.parse(fs.readFileSync(args.manifest, "utf8"));
  if (args.writeManifest) {
    trackedManifest.epub_browser_review = manifestRecord;
    fs.writeFileSync(args.manifest, JSON.stringify(trackedManifest, null, 2) + "\n", "utf8");
  } else if (JSON.stringify(trackedManifest.epub_browser_review) !== JSON.stringify(manifestRecord)) {
    throw new Error(
      "curated_format_probe_manifest.json epub_browser_review is stale; run " +
        "`node scripts/validate_curated_reader_epub_browser_review.js --write-manifest`."
    );
  }

  if (failures.length) {
    console.error(`Curated reader EPUB browser review failed: ${failures.length} page-view pair(s).`);
    for (const failure of failures.slice(0, 20)) {
      console.error(` - ${failure.zip_path} ${failure.viewport}: ${failure.errors.join("; ")}`);
    }
    process.exit(1);
  }
  console.log(
    `Curated reader EPUB browser review passed: ${results.length} page-view pairs across ${spine.length} spine entries.`
  );
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
