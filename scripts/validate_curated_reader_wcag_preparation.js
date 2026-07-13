#!/usr/bin/env node
/*
Validate rendered curated-reader HTML WCAG-preparation basics.

This is automated release-preparation evidence for the local curated reader
HTML candidate. It is not a screen-reader review, not third-party/legal WCAG
certification, and not reader release approval.
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
  "curated_reader_wcag_preparation_report.json"
);
const TRACKED_MANIFEST = path.join(
  ROOT,
  "editions",
  "reader_manuscript",
  "v1_0",
  "wcag_preparation_manifest.json"
);
const REVIEW_DOC = path.join(ROOT, "docs", "reader_wcag_preparation_review.md");
const COMMAND = "node scripts/validate_curated_reader_wcag_preparation.js";
const WRITE_COMMAND = `${COMMAND} --write-manifest`;
const VIEWPORTS = {
  desktop: { width: 1280, height: 900 },
  mobile: { width: 390, height: 844 },
};
const REVIEW_BOUNDARY =
  "This automated WCAG-preparation release gate opens the ignored local curated reader HTML artifact in Chromium at desktop and mobile widths. It checks rendered language metadata, document titles, one-H1 page shape, main and navigation landmarks, skip-link presence, focus-visible CSS, visible interactive accessible names, visible image alt text, visible table header cells, duplicate IDs, live-marker leakage, raw core-claim leakage, and WCAG 2.x-style text contrast thresholds for rendered visible text samples. It clears only the local wcag_conformance_review_not_completed release blocker for the current curated reader HTML candidate. It is not screen-reader review, not assistive-technology review, not third-party or legal WCAG certification, not e-reader review, not audiobook review, not final figure-artifact approval, not reader release approval, and not a support-state promotion.";

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

async function inspectPage(page, filePath, viewportName, viewportSize) {
  await page.setViewportSize(viewportSize);
  await page.goto(pathToFileURL(filePath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(250);

  const dom = await page.evaluate(() => {
    const LIVE_ONLY_MARKERS = [
      "Chapter status",
      "Drafting guardrail",
      "Codex test plan",
      "Source crosswalk",
      "Claim-source mapping status",
      "Formalization hooks",
    ];
    const RAW_CORE_CLAIM_RE = /\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]/;

    function isVisible(node) {
      if (!node || node.nodeType !== Node.ELEMENT_NODE) return false;
      const style = window.getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return (
        style.visibility !== "hidden" &&
        style.display !== "none" &&
        Number(style.opacity || 1) > 0 &&
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

    function parseColor(value) {
      const text = String(value || "").trim();
      if (!text || text === "transparent") return { r: 0, g: 0, b: 0, a: 0 };
      const rgb = text.match(/^rgba?\(([^)]+)\)$/i);
      if (!rgb) return { r: 0, g: 0, b: 0, a: 0 };
      const parts = rgb[1].split(",").map((part) => part.trim());
      if (parts.length < 3) return { r: 0, g: 0, b: 0, a: 0 };
      const alpha = parts.length >= 4 ? Number(parts[3]) : 1;
      return {
        r: Number(parts[0]),
        g: Number(parts[1]),
        b: Number(parts[2]),
        a: Number.isFinite(alpha) ? alpha : 1,
      };
    }

    function blend(foreground, background) {
      const alpha = Math.max(0, Math.min(1, Number(foreground.a)));
      return {
        r: foreground.r * alpha + background.r * (1 - alpha),
        g: foreground.g * alpha + background.g * (1 - alpha),
        b: foreground.b * alpha + background.b * (1 - alpha),
        a: 1,
      };
    }

    function effectiveBackground(node) {
      const chain = [];
      for (let current = node; current && current.nodeType === Node.ELEMENT_NODE; current = current.parentElement) {
        chain.unshift(current);
      }
      let color = { r: 255, g: 255, b: 255, a: 1 };
      for (const item of chain) {
        const style = window.getComputedStyle(item);
        const background = parseColor(style.backgroundColor);
        if (background.a > 0) color = blend(background, color);
      }
      return color;
    }

    function linear(value) {
      const channel = value / 255;
      return channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
    }

    function luminance(color) {
      return 0.2126 * linear(color.r) + 0.7152 * linear(color.g) + 0.0722 * linear(color.b);
    }

    function contrastRatio(foreground, background) {
      const first = luminance(foreground);
      const second = luminance(background);
      const lighter = Math.max(first, second);
      const darker = Math.min(first, second);
      return (lighter + 0.05) / (darker + 0.05);
    }

    function directText(node) {
      return Array.from(node.childNodes || [])
        .filter((child) => child.nodeType === Node.TEXT_NODE)
        .map((child) => child.textContent || "")
        .join(" ")
        .trim()
        .replace(/\s+/g, " ");
    }

    function contrastSamples() {
      const samples = [];
      const walker = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT);
      let textNode = walker.nextNode();
      while (textNode) {
        const raw = (textNode.textContent || "").trim().replace(/\s+/g, " ");
        const parent = textNode.parentElement;
        textNode = walker.nextNode();
        if (!raw || raw.length < 2 || !parent) continue;
        if (parent.closest("script, style, noscript, svg, .visually-hidden, .sr-only, .asi-sr-only")) continue;
        if (!isVisible(parent)) continue;
        const rect = parent.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) continue;
        const style = window.getComputedStyle(parent);
        const fontSize = Number.parseFloat(style.fontSize || "16");
        if (!Number.isFinite(fontSize) || fontSize < 9) continue;
        const fontWeight = Number.parseInt(style.fontWeight || "400", 10);
        const largeText = fontSize >= 24 || (fontSize >= 18.66 && fontWeight >= 700);
        const background = effectiveBackground(parent);
        const foreground = blend(parseColor(style.color), background);
        const ratio = contrastRatio(foreground, background);
        const required = largeText ? 3.0 : 4.5;
        samples.push({
          tag: parent.tagName.toLowerCase(),
          class_name: String(parent.className || "").slice(0, 120),
          text: raw.slice(0, 120),
          font_size_px: Number(fontSize.toFixed(2)),
          font_weight: Number.isFinite(fontWeight) ? fontWeight : 400,
          large_text: largeText,
          contrast_ratio: Number(ratio.toFixed(2)),
          required_ratio: required,
          pass: ratio + 1e-6 >= required,
        });
      }
      return samples;
    }

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

    const samples = contrastSamples();
    const contrastFailures = samples.filter((sample) => !sample.pass);
    const text = document.body ? document.body.innerText : "";
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
      contrast_sample_count: samples.length,
      contrast_failure_count: contrastFailures.length,
      minimum_contrast_ratio: samples.length
        ? Number(Math.min(...samples.map((sample) => sample.contrast_ratio)).toFixed(2))
        : null,
      contrast_failures: contrastFailures.slice(0, 12),
      live_marker_hits: LIVE_ONLY_MARKERS.filter((marker) => text.includes(marker)),
      raw_core_claim_marker_hit: RAW_CORE_CLAIM_RE.test(text),
    };
  });
  if (!dom.focus_visible_rule_present && linkedStylesContainFocusVisible(dom.stylesheet_hrefs)) {
    dom.focus_visible_rule_present = true;
  }

  const errors = [];
  if (dom.html_lang !== "en-US") errors.push(`html lang must be en-US, found ${dom.html_lang || "<missing>"}`);
  if (!dom.title.trim()) errors.push("document title is missing");
  if (dom.body_text_chars < 1000) errors.push(`body text too short: ${dom.body_text_chars}`);
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
  if (dom.contrast_failure_count > 0) errors.push(`${dom.contrast_failure_count} rendered text sample(s) fail WCAG contrast thresholds`);
  if (dom.live_marker_hits.length) errors.push(`live-only marker leak(s): ${dom.live_marker_hits.join(", ")}`);
  if (dom.raw_core_claim_marker_hit) errors.push("raw core claim marker leaked");

  return {
    path: rel(filePath),
    kind: pageKind(filePath),
    viewport: viewportName,
    status: errors.length ? "failed" : "passed",
    errors,
    ...dom,
  };
}

function summarize(results, files, expectedFiles, args) {
  const failures = results.filter((row) => row.status !== "passed");
  const chapterPairs = results.filter((row) => row.kind === "chapter").length;
  const sum = (field) => results.reduce((total, row) => total + Number(row[field] || 0), 0);
  const count = (predicate) => results.filter(predicate).length;
  const contrastRatios = results
    .map((row) => row.minimum_contrast_ratio)
    .filter((value) => typeof value === "number" && Number.isFinite(value));
  return {
    schema_version: "asi_stack.curated_reader_wcag_preparation.v0",
    result_id: "curated-reader-wcag-preparation-2026-07-05",
    status: failures.length
      ? "failed_wcag_preparation_release_gate"
      : "accepted_wcag_automation_evidence_for_release_preparation",
    command: COMMAND,
    write_command: WRITE_COMMAND,
    artifact_root: rel(args.site),
    source_manifest: rel(args.manifest),
    detailed_report: rel(args.report),
    cleared_blockers: failures.length ? [] : ["wcag_conformance_review_not_completed"],
    preserved_blockers: [
      "screen_reader_review_not_completed",
      "reader_release_approval_not_created",
      "audio_files_not_generated",
      "audio_spot_check_not_performed",
      "chapter_markers_not_timecoded",
      "audio_embedded_epub_not_packaged_or_checked",
      "audio_edition_release_record_not_created",
    ],
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
      visible_interactive_elements: sum("visible_interactive_count"),
      unnamed_interactive_elements: results.reduce((total, row) => total + row.unnamed_interactive.length, 0),
      visible_images: sum("image_count"),
      image_alt_failures: results.reduce((total, row) => total + row.image_alt_failures.length, 0),
      tables_checked: sum("table_count"),
      table_header_failures: results.reduce((total, row) => total + row.table_header_failures.length, 0),
      duplicate_id_page_views: results.reduce((total, row) => total + row.duplicate_ids.length, 0),
      text_contrast_samples: sum("contrast_sample_count"),
      contrast_failure_samples: sum("contrast_failure_count"),
      minimum_contrast_ratio: contrastRatios.length ? Number(Math.min(...contrastRatios).toFixed(2)) : null,
      live_marker_leak_pairs: count((row) => row.live_marker_hits.length > 0),
      raw_core_claim_marker_leak_pairs: count((row) => row.raw_core_claim_marker_hit),
    },
    review_boundary: REVIEW_BOUNDARY,
    non_claims: [
      "does not approve the curated reader HTML artifact for release",
      "does not perform screen-reader or assistive-technology review",
      "does not provide third-party or legal WCAG certification",
      "does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts",
      "does not publish the ignored local curated reader HTML artifact",
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
    unnamed_interactive_elements: 0,
    image_alt_failures: 0,
    table_header_failures: 0,
    duplicate_id_page_views: 0,
    contrast_failure_samples: 0,
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
    unnamed_interactive_elements: 0,
    image_alt_failures: 0,
    table_header_failures: 0,
    duplicate_id_page_views: 0,
    contrast_failure_samples: 0,
    live_marker_leak_pairs: 0,
    raw_core_claim_marker_leak_pairs: 0,
  };
  if (manifest.status !== "accepted_wcag_automation_evidence_for_release_preparation") {
    errors.push("status must be accepted_wcag_automation_evidence_for_release_preparation.");
  }
  if (standalone && (!Number.isInteger(summary.expected_pages) || summary.expected_pages < 1)) {
    errors.push(`summary.expected_pages must be a positive integer; found ${summary.expected_pages}.`);
  }
  if (JSON.stringify(manifest.cleared_blockers || []) !== JSON.stringify(["wcag_conformance_review_not_completed"])) {
    errors.push("cleared_blockers must clear only wcag_conformance_review_not_completed.");
  }
  for (const blocker of ["screen_reader_review_not_completed", "reader_release_approval_not_created"]) {
    if (!Array.isArray(manifest.preserved_blockers) || !manifest.preserved_blockers.includes(blocker)) {
      errors.push(`preserved_blockers missing ${blocker}.`);
    }
  }
  for (const [key, value] of Object.entries(expected)) {
    if (summary[key] !== value) {
      errors.push(`summary.${key} must be ${value}; found ${summary[key]}.`);
    }
  }
  if (!Number.isFinite(summary.text_contrast_samples) || summary.text_contrast_samples < 3000) {
    errors.push(`summary.text_contrast_samples must be at least 3000; found ${summary.text_contrast_samples}.`);
  }
  if (!Number.isFinite(summary.minimum_contrast_ratio) || summary.minimum_contrast_ratio < 4.5) {
    errors.push(`summary.minimum_contrast_ratio must be at least 4.5; found ${summary.minimum_contrast_ratio}.`);
  }
  for (const fragment of [
    "clears only the local wcag_conformance_review_not_completed release blocker",
    "not screen-reader review",
    "not assistive-technology review",
    "not third-party or legal WCAG certification",
    "not reader release approval",
    "not a support-state promotion",
  ]) {
    if (!String(manifest.review_boundary || "").includes(fragment)) {
      errors.push(`review_boundary missing ${fragment}.`);
    }
  }
  return errors;
}

function renderReviewDoc(manifest) {
  const summary = manifest.summary;
  return [
    "# Reader WCAG Preparation Review",
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
    "This automated browser review opens the ignored local curated-reader HTML artifact at desktop and mobile widths. It checks rendered language metadata, document titles, one-H1 page shape, main and navigation landmarks, skip-link presence, focus-visible CSS, accessible names, visible image alt text, visible table header cells, duplicate IDs, live-marker leakage, raw core-claim leakage, and WCAG 2.x-style contrast thresholds for visible text samples.",
    "",
    "## Decision",
    "",
    "Status: `accepted_wcag_automation_evidence_for_release_preparation`.",
    "",
    "Cleared blockers | wcag_conformance_review_not_completed",
    "",
    "Preserved blockers include `screen_reader_review_not_completed`, `reader_release_approval_not_created`, and downstream audio artifact gates.",
    "",
    "## Summary",
    "",
    "| Metric | Value |",
    "|---|---:|",
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
    `| Visible interactive elements checked | ${summary.visible_interactive_elements} |`,
    `| Unnamed interactive elements | ${summary.unnamed_interactive_elements} |`,
    `| Visible images checked | ${summary.visible_images} |`,
    `| Image alt failures | ${summary.image_alt_failures} |`,
    `| Tables checked | ${summary.tables_checked} |`,
    `| Table header failures | ${summary.table_header_failures} |`,
    `| Duplicate-ID page-view hits | ${summary.duplicate_id_page_views} |`,
    `| Text contrast samples | ${summary.text_contrast_samples} |`,
    `| Contrast failure samples | ${summary.contrast_failure_samples} |`,
    `| Minimum contrast ratio | ${summary.minimum_contrast_ratio} |`,
    `| Live-marker leak pairs | ${summary.live_marker_leak_pairs} |`,
    `| Raw core-claim marker leak pairs | ${summary.raw_core_claim_marker_leak_pairs} |`,
    "",
    "## Non-Claims",
    "",
    "- This review does not approve the curated reader HTML artifact for release.",
    "- This review does not perform screen-reader or assistive-technology review.",
    "- This review does not provide third-party or legal WCAG certification.",
    "- This review does not approve EPUB, DOCX, PDF, e-reader, audio, final figure art, or reader release artifacts.",
    "- This review does not publish the ignored local curated reader HTML artifact.",
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
    "Reader WCAG Preparation Review",
    WRITE_COMMAND,
    rel(TRACKED_MANIFEST),
    "accepted_wcag_automation_evidence_for_release_preparation",
    "Cleared blockers | wcag_conformance_review_not_completed",
    "screen_reader_review_not_completed",
    `Page-view pairs | ${summary.page_view_pairs}`,
    `Failed page-view pairs | ${summary.failed_page_view_pairs}`,
    `Contrast failure samples | ${summary.contrast_failure_samples}`,
    `Minimum contrast ratio | ${summary.minimum_contrast_ratio}`,
    "does not perform screen-reader or assistive-technology review",
    "does not provide third-party or legal WCAG certification",
    "does not approve the curated reader HTML artifact",
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
      console.error("Curated reader tracked WCAG-preparation validation failed:");
      for (const error of trackedErrors) console.error(` - ${error}`);
      process.exit(1);
    }
    console.log(
      `Curated reader tracked WCAG-preparation validation passed: ` +
        `${tracked.summary.page_view_pairs} page-view pairs, ${tracked.summary.contrast_failure_samples} contrast failures.`
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
  if (!playwright) throw new Error("Playwright is not available; cannot run WCAG-preparation review.");
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
    console.error("Curated reader WCAG-preparation validation failed:");
    for (const error of manifestErrors) console.error(` - ${error}`);
    process.exit(1);
  }
  console.log(
    `Curated reader WCAG-preparation validation passed: ${manifest.summary.page_view_pairs} page-view pairs, ` +
      `${manifest.summary.contrast_failure_samples} contrast failures.`
  );
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
