#!/usr/bin/env node
/*
Validate the generated reader HTML artifact in a real browser.

This is an artifact-review helper, not a release approval tool. Run
`python3 scripts/render_reader_formats.py --formats html epub docx` first so
the ignored reader HTML snapshot exists under build/reader_edition.
*/

const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_SITE = path.join(ROOT, "build", "reader_edition", "format_artifacts", "html", "_reader_site");
const DEFAULT_MANIFEST = path.join(ROOT, "build", "reader_edition", "reader_manifest.json");
const DEFAULT_REPORT = path.join(ROOT, "build", "reader_html_artifact_browser_report.json");
const VIEWPORTS = {
  desktop: { width: 1280, height: 900 },
  mobile: { width: 390, height: 844 },
};
const RAW_CORE_CLAIM_RE = /\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]/;
const LIVE_ONLY_MARKERS = [
  "Chapter status",
  "Drafting guardrail",
  "Codex test plan",
  "Source crosswalk",
  "Claim-source mapping status",
  "Formalization hooks",
];

function parseArgs(argv) {
  const args = {
    site: DEFAULT_SITE,
    report: DEFAULT_REPORT,
    strict: false,
  };
  for (let index = 2; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--strict") {
      args.strict = true;
    } else if (value === "--site") {
      args.site = path.resolve(argv[++index]);
    } else if (value === "--report") {
      args.report = path.resolve(argv[++index]);
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

function htmlFiles(site) {
  const results = [];
  function visit(dir) {
    for (const name of fs.readdirSync(dir)) {
      const item = path.join(dir, name);
      const stat = fs.statSync(item);
      if (stat.isDirectory()) {
        visit(item);
      } else if (name.endsWith(".html")) {
        results.push(item);
      }
    }
  }
  visit(site);
  return results.sort();
}

function relative(filePath) {
  return path.relative(ROOT, filePath);
}

function expectedHtmlFileCount() {
  if (!fs.existsSync(DEFAULT_MANIFEST)) {
    throw new Error(`Reader manifest not found: ${DEFAULT_MANIFEST}`);
  }
  const manifest = JSON.parse(fs.readFileSync(DEFAULT_MANIFEST, "utf8"));
  if (!Number.isInteger(manifest.files) || manifest.files < 1) {
    throw new Error("Reader manifest is missing a positive integer files count.");
  }
  return manifest.files;
}

async function inspectPage(page, filePath, viewportName, viewportSize) {
  await page.setViewportSize(viewportSize);
  await page.goto(pathToFileURL(filePath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(300);

  const text = await page.locator("body").innerText({ timeout: 5000 });
  const metrics = await page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    const main = document.querySelector("main") || document.body;
    const title = document.querySelector("h1");
    const scrollWidth = Math.max(doc.scrollWidth, body ? body.scrollWidth : 0);
    const clientWidth = doc.clientWidth;
    return {
      title: title ? title.textContent.trim() : "",
      body_text_chars: body ? body.innerText.length : 0,
      stylesheet_count: document.styleSheets.length,
      link_count: document.querySelectorAll("a[href]").length,
      image_count: document.querySelectorAll("img").length,
      svg_count: document.querySelectorAll("svg").length,
      main_visible: Boolean(main && main.getBoundingClientRect().height > 0),
      scroll_width: scrollWidth,
      client_width: clientWidth,
      horizontal_overflow_px: Math.max(0, scrollWidth - clientWidth),
    };
  });

  const errors = [];
  if (!metrics.title) errors.push("missing visible h1 title");
  if (metrics.body_text_chars < 1000) errors.push(`body text too short: ${metrics.body_text_chars}`);
  if (metrics.stylesheet_count < 1) errors.push("no stylesheets loaded");
  if (!metrics.main_visible) errors.push("main content is not visible");
  if (metrics.horizontal_overflow_px > 2) errors.push(`horizontal overflow ${metrics.horizontal_overflow_px}px`);
  if (RAW_CORE_CLAIM_RE.test(text)) errors.push("raw core-claim marker leaked");
  for (const marker of LIVE_ONLY_MARKERS) {
    if (text.includes(marker)) errors.push(`live-only marker leaked: ${marker}`);
  }
  if (filePath.includes(`${path.sep}chapters${path.sep}`) && metrics.svg_count < 1) {
    errors.push("chapter page has no rendered SVG diagram");
  }

  return {
    path: relative(filePath),
    viewport: viewportName,
    ...metrics,
    status: errors.length ? "failed" : "passed",
    errors,
  };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!fs.existsSync(args.site)) {
    throw new Error(`Reader HTML site snapshot not found: ${args.site}`);
  }

  const files = htmlFiles(args.site);
  const expectedFiles = expectedHtmlFileCount();
  if (files.length < expectedFiles) {
    throw new Error(`Expected at least ${expectedFiles} reader HTML files, found ${files.length}.`);
  }

  const playwright = loadPlaywright();
  if (!playwright) {
    const message = "Playwright is not available; reader HTML browser validation skipped.";
    if (args.strict) throw new Error(message);
    console.log(message);
    return;
  }

  const browser = await launchChromium(playwright);
  const page = await browser.newPage();
  const results = [];
  try {
    for (const filePath of files) {
      for (const [viewportName, viewportSize] of Object.entries(VIEWPORTS)) {
        results.push(await inspectPage(page, filePath, viewportName, viewportSize));
      }
    }
  } finally {
    await browser.close();
  }

  const failures = results.filter((result) => result.status !== "passed");
  const report = {
    schema_version: "0.1",
    artifact_root: relative(args.site),
    expected_page_count: expectedFiles,
    page_count: files.length,
    viewport_count: Object.keys(VIEWPORTS).length,
    page_view_pairs: results.length,
    status: failures.length ? "failed" : "passed",
    failures,
    results,
    non_claims: [
      "This is a browser review of a local ignored reader HTML snapshot only.",
      "Passing this check does not create an edition release record or publish an artifact.",
      "Passing this check does not approve EPUB, DOCX, PDF, e-reader, or audio artifacts.",
      "Passing this check does not promote any claim support state.",
    ],
  };

  fs.mkdirSync(path.dirname(args.report), { recursive: true });
  fs.writeFileSync(args.report, JSON.stringify(report, null, 2) + "\n", "utf8");

  if (failures.length) {
    console.error(`Reader HTML browser validation failed: ${failures.length} failing page-view pair(s).`);
    for (const failure of failures.slice(0, 20)) {
      console.error(` - ${failure.path} ${failure.viewport}: ${failure.errors.join("; ")}`);
    }
    process.exit(1);
  }
  console.log(`Reader HTML browser validation passed: ${results.length} page-view pairs across ${files.length} pages.`);
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
