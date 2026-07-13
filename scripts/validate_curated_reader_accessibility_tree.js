#!/usr/bin/env node
/*
Validate rendered curated-reader HTML accessibility-tree and semantic basics.

This is an automated release-preparation probe. It is not manual keyboard-only
review, not screen-reader review, not WCAG conformance, and not release
approval.
*/

const fs = require("fs");
const os = require("os");
const path = require("path");
const { fileURLToPath, pathToFileURL } = require("url");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_SITE = path.join(
  ROOT,
  "build",
  "curated_reader_edition",
  "format_artifacts",
  "html",
  "_reader_site"
);
const DEFAULT_MANIFEST = path.join(ROOT, "build", "curated_reader_edition", "reader_manifest.json");
const DEFAULT_REPORT = path.join(
  ROOT,
  "build",
  "curated_reader_edition",
  "curated_reader_accessibility_tree_report.json"
);
const TRACKED_MANIFEST = path.join(
  ROOT,
  "editions",
  "reader_manuscript",
  "v1_0",
  "accessibility_tree_manifest.json"
);
const REVIEW_DOC = path.join(ROOT, "docs", "reader_accessibility_tree_review.md");
const COMMAND = "node scripts/validate_curated_reader_accessibility_tree.js";
const WRITE_COMMAND = `${COMMAND} --write-manifest`;
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
const REVIEW_BOUNDARY =
  "This automated accessibility-tree release-preparation probe opens the ignored local curated reader HTML artifact in Chromium at desktop and mobile widths. It checks page language, one-H1 shape, main and navigation landmarks, skip-link presence, visible interactive accessible names, image alt text, table headers, duplicate IDs, live-marker leakage, raw core-claim leakage, and Chromium accessibility-tree availability. It is not manual keyboard-only review, not screen-reader review, not WCAG conformance, not e-reader review, not audiobook review, not final figure-artifact approval, and not reader release approval.";

function parseArgs(argv) {
  const args = {
    site: DEFAULT_SITE,
    manifest: DEFAULT_MANIFEST,
    report: DEFAULT_REPORT,
    writeManifest: false,
    trackedOnly: false,
    standalone: false,
  };
  for (let index = 2; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--site") {
      args.site = path.resolve(argv[++index]);
    } else if (value === "--manifest") {
      args.manifest = path.resolve(argv[++index]);
    } else if (value === "--report") {
      args.report = path.resolve(argv[++index]);
    } else if (value === "--write-manifest") {
      args.writeManifest = true;
    } else if (value === "--tracked-only") {
      args.trackedOnly = true;
    } else if (value === "--standalone") {
      args.standalone = true;
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }
  return args;
}

function rel(filePath) {
  return path.relative(ROOT, filePath);
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

function expectedHtmlFileCount(manifestPath) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  if (!Number.isInteger(manifest.files) || manifest.files < 1) {
    throw new Error("Curated reader manifest is missing a positive integer files count.");
  }
  return manifest.files;
}

function pageKind(filePath) {
  if (filePath.includes(`${path.sep}chapters${path.sep}`)) return "chapter";
  if (filePath.includes(`${path.sep}appendices${path.sep}`)) return "appendix";
  return path.basename(filePath, ".html");
}

function linkedStylesContainFocusVisible(stylesheetHrefs) {
  for (const href of stylesheetHrefs || []) {
    let cssPath;
    try {
      const url = new URL(href);
      if (url.protocol !== "file:") continue;
      cssPath = fileURLToPath(url);
    } catch (_) {
      continue;
    }
    if (!fs.existsSync(cssPath)) continue;
    const css = fs.readFileSync(cssPath, "utf8");
    if (css.includes(":focus-visible")) return true;
  }
  return false;
}

async function accessibilityTreeStats(page) {
  try {
    const session = await page.context().newCDPSession(page);
    const response = await session.send("Accessibility.getFullAXTree");
    await session.detach();
    const nodes = Array.isArray(response.nodes) ? response.nodes : [];
    const namedNodes = nodes.filter((node) => {
      const value = node.name && typeof node.name.value === "string" ? node.name.value.trim() : "";
      return value.length > 0;
    });
    return {
      available: true,
      node_count: nodes.length,
      named_node_count: namedNodes.length,
    };
  } catch (error) {
    return {
      available: false,
      node_count: 0,
      named_node_count: 0,
      error: String(error && error.message ? error.message : error).slice(0, 180),
    };
  }
}

async function inspectPage(page, filePath, viewportName, viewportSize) {
  await page.setViewportSize(viewportSize);
  await page.goto(pathToFileURL(filePath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(250);

  const dom = await page.evaluate(() => {
    function isVisible(node) {
      if (!node) return false;
      const style = window.getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return (
        style.visibility !== "hidden" &&
        style.display !== "none" &&
        rect.width > 0 &&
        rect.height > 0 &&
        rect.bottom >= 0 &&
        rect.right >= 0 &&
        rect.top <= window.innerHeight + 4 &&
        rect.left <= window.innerWidth + 4
      );
    }
    function textOf(node) {
      return (node ? node.textContent || "" : "").trim().replace(/\s+/g, " ");
    }
    function labelledByText(node) {
      const labelledBy = node.getAttribute("aria-labelledby") || "";
      return labelledBy
        .split(/\s+/)
        .map((id) => textOf(document.getElementById(id)))
        .filter(Boolean)
        .join(" ");
    }
    function labelText(node) {
      if (!node.id) return "";
      const label = document.querySelector(`label[for="${CSS.escape(node.id)}"]`);
      return textOf(label);
    }
    function accessibleName(node) {
      return (
        node.getAttribute("aria-label") ||
        labelledByText(node) ||
        labelText(node) ||
        node.getAttribute("alt") ||
        node.getAttribute("title") ||
        node.getAttribute("placeholder") ||
        node.getAttribute("value") ||
        textOf(node) ||
        ""
      )
        .trim()
        .replace(/\s+/g, " ");
    }

    const h1s = Array.from(document.querySelectorAll("h1")).map((node) => textOf(node));
    const main = document.querySelector("main, #quarto-document-content");
    const navs = Array.from(document.querySelectorAll("nav, [role='navigation']")).filter(isVisible);
    const skipLinks = Array.from(document.querySelectorAll("a.asi-skip-link, a[href='#quarto-document-content']")).map(
      (node) => ({
        text: textOf(node),
        href: node.getAttribute("href") || "",
      })
    );
    const visibleInteractive = Array.from(
      document.querySelectorAll("a[href], button, input, select, textarea, [role='button'], [tabindex]:not([tabindex='-1'])")
    ).filter((node) => {
      if (node.getAttribute("aria-hidden") === "true") return false;
      if (node.matches("input[type='hidden']")) return false;
      return isVisible(node);
    });
    const unnamedInteractive = visibleInteractive
      .map((node) => ({
        tag: node.tagName,
        role: node.getAttribute("role") || "",
        href: node.getAttribute("href") || "",
        id: node.id || "",
        class_name: node.className || "",
        name: accessibleName(node),
      }))
      .filter((row) => !row.name);

    const images = Array.from(document.querySelectorAll("img")).filter((node) => {
      if (node.getAttribute("aria-hidden") === "true") return false;
      if (node.getAttribute("role") === "presentation") return false;
      return isVisible(node);
    });
    const imageAltFailures = images
      .map((node) => ({
        src: node.getAttribute("src") || "",
        alt: node.getAttribute("alt"),
        role: node.getAttribute("role") || "",
      }))
      .filter((row) => typeof row.alt !== "string" || row.alt.trim().length < 12);

    const tableHeaderFailures = Array.from(document.querySelectorAll("table"))
      .filter(isVisible)
      .map((node, index) => ({
        index,
        th_count: node.querySelectorAll("th").length,
        caption: textOf(node.querySelector("caption")),
      }))
      .filter((row) => row.th_count < 1);

    const ids = Array.from(document.querySelectorAll("[id]")).map((node) => node.id).filter(Boolean);
    const seen = new Set();
    const duplicateIds = [];
    for (const id of ids) {
      if (seen.has(id) && !duplicateIds.includes(id)) duplicateIds.push(id);
      seen.add(id);
    }

    const text = document.body ? document.body.innerText : "";
    function ruleHasFocusVisible(rule) {
      const selector = String(rule.selectorText || "");
      const text = String(rule.cssText || "");
      if (selector.includes(":focus-visible") || text.includes(":focus-visible")) return true;
      if (rule.cssRules) {
        try {
          return Array.from(rule.cssRules).some(ruleHasFocusVisible);
        } catch (_) {
          return false;
        }
      }
      return false;
    }

    const styles = Array.from(document.styleSheets).length;
    const focusVisibleRules = Array.from(document.styleSheets).some((sheet) => {
      try {
        return Array.from(sheet.cssRules || []).some(ruleHasFocusVisible);
      } catch (_) {
        return false;
      }
    });

    return {
      html_lang: document.documentElement.getAttribute("lang") || "",
      title: document.title || "",
      body_text_chars: text.length,
      stylesheet_count: styles,
      stylesheet_hrefs: Array.from(document.querySelectorAll('link[rel~="stylesheet"]')).map((node) => node.href),
      focus_visible_rule_present: focusVisibleRules,
      h1_count: h1s.length,
      h1_text: h1s[0] || "",
      main_landmark_present: Boolean(main),
      main_visible: Boolean(main && isVisible(main)),
      navigation_landmark_count: navs.length,
      skip_link_count: skipLinks.length,
      skip_links: skipLinks,
      visible_interactive_count: visibleInteractive.length,
      unnamed_interactive: unnamedInteractive.slice(0, 10),
      image_count: images.length,
      image_alt_failures: imageAltFailures.slice(0, 10),
      table_count: document.querySelectorAll("table").length,
      table_header_failures: tableHeaderFailures.slice(0, 10),
      duplicate_ids: duplicateIds.slice(0, 10),
      live_marker_hits: ["Chapter status", "Drafting guardrail", "Codex test plan", "Source crosswalk", "Claim-source mapping status", "Formalization hooks"].filter((marker) =>
        text.includes(marker)
      ),
      raw_core_claim_marker_hit: /\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]/.test(text),
    };
  });
  if (!dom.focus_visible_rule_present && linkedStylesContainFocusVisible(dom.stylesheet_hrefs)) {
    dom.focus_visible_rule_present = true;
  }
  const ax = await accessibilityTreeStats(page);

  const errors = [];
  if (dom.html_lang !== "en-US") errors.push(`html lang must be en-US, found ${dom.html_lang || "<missing>"}`);
  if (!dom.title.trim()) errors.push("document title is missing");
  if (dom.body_text_chars < 1000) errors.push(`body text too short: ${dom.body_text_chars}`);
  if (dom.stylesheet_count < 1) errors.push("no stylesheet loaded");
  if (!dom.focus_visible_rule_present) errors.push("focus-visible CSS rule not detected");
  if (dom.h1_count !== 1) errors.push(`expected exactly one h1, found ${dom.h1_count}`);
  if (!dom.main_landmark_present) errors.push("main landmark was not found");
  if (!dom.main_visible) errors.push("main landmark is not visible");
  if (dom.navigation_landmark_count < 1) errors.push("navigation landmark was not found");
  if (dom.skip_link_count < 1) errors.push("skip-to-main link was not found");
  if (dom.unnamed_interactive.length) errors.push(`${dom.unnamed_interactive.length} visible interactive element(s) lack accessible names`);
  if (dom.image_alt_failures.length) errors.push(`${dom.image_alt_failures.length} visible image(s) lack substantive alt text`);
  if (dom.table_header_failures.length) errors.push(`${dom.table_header_failures.length} visible table(s) lack header cells`);
  if (dom.duplicate_ids.length) errors.push(`${dom.duplicate_ids.length} duplicate id(s) detected`);
  if (dom.live_marker_hits.length) errors.push(`live-only marker leak(s): ${dom.live_marker_hits.join(", ")}`);
  if (dom.raw_core_claim_marker_hit) errors.push("raw core claim marker leaked");
  if (!ax.available) errors.push(`Chromium accessibility tree was unavailable: ${ax.error || "unknown error"}`);
  if (ax.available && ax.node_count < 20) errors.push(`accessibility tree too small: ${ax.node_count}`);
  if (ax.available && ax.named_node_count < 10) errors.push(`accessibility tree has too few named nodes: ${ax.named_node_count}`);

  return {
    path: rel(filePath),
    kind: pageKind(filePath),
    viewport: viewportName,
    status: errors.length ? "failed" : "passed",
    errors,
    ...dom,
    accessibility_tree: ax,
  };
}

function summarize(results, files, expectedFiles, args) {
  const failures = results.filter((row) => row.status !== "passed");
  const chapterPairs = results.filter((row) => row.kind === "chapter").length;
  const sum = (field) => results.reduce((total, row) => total + Number(row[field] || 0), 0);
  const count = (predicate) => results.filter(predicate).length;
  return {
    schema_version: "asi_stack.curated_reader_accessibility_tree.v0",
    result_id: "curated-reader-accessibility-tree-2026-07-05",
    status: failures.length ? "failed_accessibility_tree_release_preparation_probe" : "passed_accessibility_tree_release_preparation_probe",
    command: COMMAND,
    write_command: WRITE_COMMAND,
    artifact_root: rel(args.site),
    source_manifest: rel(args.manifest),
    detailed_report: rel(args.report),
    summary: {
      pages_checked: files.length,
      expected_pages: expectedFiles,
      viewport_count: Object.keys(VIEWPORTS).length,
      page_view_pairs: results.length,
      chapter_page_view_pairs: chapterPairs,
      failed_page_view_pairs: failures.length,
      lang_en_us_pairs: count((row) => row.html_lang === "en-US"),
      titled_pairs: count((row) => Boolean(row.title && row.title.trim())),
      one_h1_pairs: count((row) => row.h1_count === 1),
      main_landmark_pairs: count((row) => row.main_landmark_present && row.main_visible),
      navigation_landmark_pairs: count((row) => row.navigation_landmark_count >= 1),
      skip_link_pairs: count((row) => row.skip_link_count >= 1),
      focus_visible_rule_pairs: count((row) => row.focus_visible_rule_present),
      accessibility_tree_pairs: count((row) => row.accessibility_tree && row.accessibility_tree.available),
      minimum_accessibility_tree_nodes: Math.min(...results.map((row) => row.accessibility_tree.node_count)),
      minimum_named_accessibility_nodes: Math.min(...results.map((row) => row.accessibility_tree.named_node_count)),
      visible_interactive_elements: sum("visible_interactive_count"),
      unnamed_interactive_elements: results.reduce((total, row) => total + row.unnamed_interactive.length, 0),
      visible_images: sum("image_count"),
      image_alt_failures: results.reduce((total, row) => total + row.image_alt_failures.length, 0),
      tables_checked: sum("table_count"),
      table_header_failures: results.reduce((total, row) => total + row.table_header_failures.length, 0),
      duplicate_id_page_views: results.reduce((total, row) => total + row.duplicate_ids.length, 0),
      live_marker_leak_pairs: count((row) => row.live_marker_hits.length > 0),
      raw_core_claim_marker_leak_pairs: count((row) => row.raw_core_claim_marker_hit),
    },
    review_boundary: REVIEW_BOUNDARY,
    non_claims: [
      "does not approve the curated reader HTML artifact for release",
      "does not certify WCAG conformance",
      "does not perform screen-reader review",
      "does not perform manual keyboard-only review",
      "does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts",
      "does not promote any chapter core claim or support state",
    ],
  };
}

function validateManifest(manifest, { standalone = false } = {}) {
  const errors = [];
  const summary = manifest.summary || {};
  const expected = standalone ? {
    pages_checked: summary.expected_pages,
    viewport_count: 2,
    page_view_pairs: summary.expected_pages * 2,
    failed_page_view_pairs: 0,
    lang_en_us_pairs: summary.page_view_pairs,
    titled_pairs: summary.page_view_pairs,
    one_h1_pairs: summary.page_view_pairs,
    main_landmark_pairs: summary.page_view_pairs,
    navigation_landmark_pairs: summary.page_view_pairs,
    skip_link_pairs: summary.page_view_pairs,
    focus_visible_rule_pairs: summary.page_view_pairs,
    accessibility_tree_pairs: summary.page_view_pairs,
    unnamed_interactive_elements: 0,
    image_alt_failures: 0,
    table_header_failures: 0,
    duplicate_id_page_views: 0,
    live_marker_leak_pairs: 0,
    raw_core_claim_marker_leak_pairs: 0,
  } : {
    pages_checked: 49,
    expected_pages: 49,
    viewport_count: 2,
    page_view_pairs: 98,
    chapter_page_view_pairs: 88,
    failed_page_view_pairs: 0,
    lang_en_us_pairs: 98,
    titled_pairs: 98,
    one_h1_pairs: 98,
    main_landmark_pairs: 98,
    navigation_landmark_pairs: 98,
    skip_link_pairs: 98,
    focus_visible_rule_pairs: 98,
    accessibility_tree_pairs: 98,
    unnamed_interactive_elements: 0,
    image_alt_failures: 0,
    table_header_failures: 0,
    duplicate_id_page_views: 0,
    live_marker_leak_pairs: 0,
    raw_core_claim_marker_leak_pairs: 0,
  };
  if (manifest.status !== "passed_accessibility_tree_release_preparation_probe") {
    errors.push("status must be passed_accessibility_tree_release_preparation_probe.");
  }
  if (standalone && (!Number.isInteger(summary.expected_pages) || summary.expected_pages < 1)) {
    errors.push(`summary.expected_pages must be a positive integer; found ${summary.expected_pages}.`);
  }
  for (const [key, value] of Object.entries(expected)) {
    if (summary[key] !== value) {
      errors.push(`summary.${key} must be ${value}; found ${summary[key]}.`);
    }
  }
  if (summary.minimum_accessibility_tree_nodes < 20) {
    errors.push(`summary.minimum_accessibility_tree_nodes must be at least 20; found ${summary.minimum_accessibility_tree_nodes}.`);
  }
  if (summary.minimum_named_accessibility_nodes < 10) {
    errors.push(`summary.minimum_named_accessibility_nodes must be at least 10; found ${summary.minimum_named_accessibility_nodes}.`);
  }
  for (const fragment of [
    "not manual keyboard-only review",
    "not screen-reader review",
    "not WCAG conformance",
    "not e-reader review",
    "not audiobook review",
    "not reader release approval",
  ]) {
    if (!manifest.review_boundary.includes(fragment)) {
      errors.push(`review_boundary missing ${fragment}.`);
    }
  }
  return errors;
}

function renderReviewDoc(manifest) {
  const summary = manifest.summary;
  return [
    "# Reader Accessibility Tree Review",
    "",
    "Last checked: 2026-07-05",
    "",
    "Command:",
    "",
    "```bash",
    WRITE_COMMAND,
    "```",
    "",
    `Tracked result: \`${rel(TRACKED_MANIFEST)}\``,
    "",
    "This automated browser review opens the ignored local curated-reader HTML artifact at desktop and mobile widths. It checks rendered page language, one-H1 shape, main and navigation landmarks, skip-link presence, interactive accessible names, image alt text, table headers, duplicate IDs, live-marker leakage, raw core-claim leakage, and Chromium accessibility-tree availability. It is release-preparation evidence only.",
    "",
    "## Summary",
    "",
    "| Metric | Value |",
    "|---|---:|",
    `| Status | \`${manifest.status}\` |`,
    `| Pages checked | ${summary.pages_checked} |`,
    `| Page-view pairs | ${summary.page_view_pairs} |`,
    `| Failed page-view pairs | ${summary.failed_page_view_pairs} |`,
    `| ` + `lang=\"en-US\"` + ` page-view pairs | ${summary.lang_en_us_pairs} |`,
    `| Titled page-view pairs | ${summary.titled_pairs} |`,
    `| One-H1 page-view pairs | ${summary.one_h1_pairs} |`,
    `| Main landmark page-view pairs | ${summary.main_landmark_pairs} |`,
    `| Navigation landmark page-view pairs | ${summary.navigation_landmark_pairs} |`,
    `| Skip-link page-view pairs | ${summary.skip_link_pairs} |`,
    `| Focus-visible rule page-view pairs | ${summary.focus_visible_rule_pairs} |`,
    `| Accessibility-tree page-view pairs | ${summary.accessibility_tree_pairs} |`,
    `| Minimum accessibility-tree nodes | ${summary.minimum_accessibility_tree_nodes} |`,
    `| Minimum named accessibility-tree nodes | ${summary.minimum_named_accessibility_nodes} |`,
    `| Visible interactive elements checked | ${summary.visible_interactive_elements} |`,
    `| Unnamed interactive elements | ${summary.unnamed_interactive_elements} |`,
    `| Visible images checked | ${summary.visible_images} |`,
    `| Image alt failures | ${summary.image_alt_failures} |`,
    `| Tables checked | ${summary.tables_checked} |`,
    `| Table header failures | ${summary.table_header_failures} |`,
    `| Duplicate-ID page-view hits | ${summary.duplicate_id_page_views} |`,
    `| Live-marker leak pairs | ${summary.live_marker_leak_pairs} |`,
    `| Raw core-claim marker leak pairs | ${summary.raw_core_claim_marker_leak_pairs} |`,
    "",
    "## Gate",
    "",
    "Every rendered page-view pair must have `lang=\"en-US\"`, a document title, exactly one H1, visible main and navigation landmarks, a skip-to-main link, loaded focus-visible styling, no visible unnamed interactive controls, substantive alt text for visible images, table header cells for visible tables, no duplicate IDs, no live-only marker leakage, no raw core-claim marker leakage, and an available Chromium accessibility tree with named nodes.",
    "",
    "## Non-Claims",
    "",
    "- This review does not approve the curated reader HTML artifact for release.",
    "- This review does not certify WCAG conformance.",
    "- This review does not perform screen-reader review.",
    "- This review does not perform manual keyboard-only review.",
    "- This review does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts.",
    "- This review does not promote any chapter core claim or support state.",
    "",
  ].join("\n");
}

function validateReviewDoc(manifest) {
  const errors = [];
  if (!fs.existsSync(REVIEW_DOC)) {
    errors.push(`${rel(REVIEW_DOC)} is missing.`);
    return errors;
  }
  const text = fs.readFileSync(REVIEW_DOC, "utf8");
  const summary = manifest.summary;
  for (const fragment of [
    "Reader Accessibility Tree Review",
    WRITE_COMMAND,
    rel(TRACKED_MANIFEST),
    "automated browser review",
    `Pages checked | ${summary.pages_checked}`,
    `Page-view pairs | ${summary.page_view_pairs}`,
    `Failed page-view pairs | ${summary.failed_page_view_pairs}`,
    `Accessibility-tree page-view pairs | ${summary.accessibility_tree_pairs}`,
    `Visible interactive elements checked | ${summary.visible_interactive_elements}`,
    `Unnamed interactive elements | ${summary.unnamed_interactive_elements}`,
    `Image alt failures | ${summary.image_alt_failures}`,
    `Table header failures | ${summary.table_header_failures}`,
    "does not perform manual keyboard-only review",
    "does not perform screen-reader review",
    "does not certify WCAG conformance",
    "does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts",
  ]) {
    if (!text.includes(fragment)) {
      errors.push(`${rel(REVIEW_DOC)} missing required fragment: ${fragment}`);
    }
  }
  return errors;
}

function trackedComparable(manifest) {
  return JSON.parse(JSON.stringify(manifest));
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.standalone && (args.trackedOnly || args.writeManifest)) {
    throw new Error("--standalone cannot be combined with --tracked-only or --write-manifest.");
  }
  if (args.trackedOnly) {
    if (args.writeManifest) throw new Error("--tracked-only cannot be combined with --write-manifest.");
    if (!fs.existsSync(TRACKED_MANIFEST)) {
      throw new Error(`${rel(TRACKED_MANIFEST)} is missing; run \`${WRITE_COMMAND}\`.`);
    }
    const tracked = JSON.parse(fs.readFileSync(TRACKED_MANIFEST, "utf8"));
    const trackedErrors = validateManifest(tracked);
    trackedErrors.push(...validateReviewDoc(tracked));
    if (trackedErrors.length) {
      console.error("Curated reader tracked accessibility-tree validation failed:");
      for (const error of trackedErrors) console.error(` - ${error}`);
      process.exit(1);
    }
    console.log(
      `Curated reader tracked accessibility-tree validation passed: ` +
        `${tracked.summary.page_view_pairs} page-view pairs, ${tracked.summary.failed_page_view_pairs} failures.`
    );
    return;
  }
  if (!fs.existsSync(args.site)) throw new Error(`Curated reader HTML site not found: ${args.site}`);
  if (!fs.existsSync(args.manifest)) throw new Error(`Curated reader manifest not found: ${args.manifest}`);

  const files = htmlFiles(args.site);
  const expectedFiles = expectedHtmlFileCount(args.manifest);
  if (files.length !== expectedFiles) {
    throw new Error(`Expected ${expectedFiles} curated reader HTML files, found ${files.length}.`);
  }
  const playwright = loadPlaywright();
  if (!playwright) throw new Error("Playwright is not available; cannot run accessibility-tree review.");
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

  const manifest = summarize(results, files, expectedFiles, args);
  const manifestErrors = validateManifest(manifest, { standalone: args.standalone });
  const report = {
    ...manifest,
    results,
    failures: results.filter((row) => row.status !== "passed"),
  };
  fs.mkdirSync(path.dirname(args.report), { recursive: true });
  fs.writeFileSync(args.report, JSON.stringify(report, null, 2) + "\n", "utf8");

  if (args.writeManifest) {
    fs.writeFileSync(TRACKED_MANIFEST, JSON.stringify(manifest, null, 2) + "\n", "utf8");
    fs.writeFileSync(REVIEW_DOC, renderReviewDoc(manifest), "utf8");
  } else if (!args.standalone) {
    if (!fs.existsSync(TRACKED_MANIFEST)) {
      manifestErrors.push(`${rel(TRACKED_MANIFEST)} is missing; run \`${WRITE_COMMAND}\`.`);
    } else {
      const current = JSON.parse(fs.readFileSync(TRACKED_MANIFEST, "utf8"));
      if (JSON.stringify(trackedComparable(current)) !== JSON.stringify(trackedComparable(manifest))) {
        manifestErrors.push(`${rel(TRACKED_MANIFEST)} is stale; run \`${WRITE_COMMAND}\`.`);
      }
    }
    manifestErrors.push(...validateReviewDoc(manifest));
  }

  if (manifestErrors.length) {
    console.error("Curated reader accessibility-tree validation failed:");
    for (const error of manifestErrors) console.error(` - ${error}`);
    process.exit(1);
  }
  console.log(
    `Curated reader accessibility-tree validation passed: ${manifest.summary.page_view_pairs} page-view pairs, ` +
      `${manifest.summary.failed_page_view_pairs} failures.`
  );
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
