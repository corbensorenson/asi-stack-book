#!/usr/bin/env node
/*
Validate the rendered live-site reading-mode toggle in a real browser.

This script is intentionally post-render: run `quarto render --to html` first.
It uses Playwright when available. If Playwright or its browser executable is
not installed, the default behavior is an explicit skip so CI environments
without browser dependencies do not report a fabricated browser result. Pass
`--strict` to fail instead of skipping when browser automation is unavailable.
*/

const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_SITE = path.join(ROOT, "_site");
const DEFAULT_REPORT = path.join(ROOT, "build", "live_human_view_browser_report.json");
const VIEWPORTS = {
  desktop: { width: 1280, height: 900 },
  mobile: { width: 390, height: 844 },
};

function parseArgs(argv) {
  const args = {
    site: DEFAULT_SITE,
    report: DEFAULT_REPORT,
    strict: false,
    allChapters: false,
    allViewports: false,
  };
  for (let index = 2; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--strict") {
      args.strict = true;
    } else if (value === "--all-chapters") {
      args.allChapters = true;
    } else if (value === "--all-viewports") {
      args.allViewports = true;
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

function loadJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

function flattenChapters(structure) {
  return (structure.parts || []).flatMap((part) => part.chapters || []);
}

function renderedPath(siteDir, sourceFile) {
  return path.join(siteDir, sourceFile.replace(/\.qmd$/, ".html"));
}

function appendixTogglePages(structure) {
  const pages = [];
  for (const appendixId of ["corben-source-corpus", "external-sources-and-literature"]) {
    const appendix = (structure.appendices || []).find((record) => record.id === appendixId);
    if (appendix) {
      pages.push({ kind: "appendix", id: appendix.id, sourceFile: appendix.file });
    }
  }
  return pages;
}

function pagesForValidation(structure, allChapters) {
  const chapters = flattenChapters(structure);
  if (allChapters) {
    return chapters
      .map((chapter) => ({
        kind: "chapter",
        id: chapter.id,
        sourceFile: chapter.file,
      }))
      .concat(appendixTogglePages(structure));
  }

  const indexes = new Set([0, Math.floor(chapters.length / 2), chapters.length - 1]);
  return [...indexes]
    .filter((index) => chapters[index])
    .map((index) => ({
      kind: "chapter",
      id: chapters[index].id,
      sourceFile: chapters[index].file,
    }))
    .concat(appendixTogglePages(structure));
}

function viewportsForValidation(allViewports) {
  if (allViewports) {
    return [
      { name: "desktop", size: VIEWPORTS.desktop },
      { name: "mobile", size: VIEWPORTS.mobile },
    ];
  }
  return [{ name: "desktop", size: VIEWPORTS.desktop }];
}

function candidateModuleRoots() {
  const roots = [];
  for (const key of ["NODE_PATH", "CODEX_PLAYWRIGHT_NODE_MODULES", "CODEX_NODE_MODULES"]) {
    const value = process.env[key];
    if (!value) continue;
    roots.push(...value.split(path.delimiter).filter(Boolean));
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
    // Continue to known local/runtime module roots.
  }
  for (const root of candidateModuleRoots()) {
    const candidate = root.endsWith("playwright") ? root : path.join(root, "playwright");
    if (!fs.existsSync(candidate)) continue;
    try {
      return require(candidate);
    } catch (_) {
      // Keep trying candidates.
    }
  }
  return null;
}

function candidateBrowserExecutables() {
  const candidates = [];
  if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) {
    candidates.push(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE);
  }
  candidates.push(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
  );
  return [...new Set(candidates)].filter((candidate) => fs.existsSync(candidate));
}

async function launchChromium(playwright) {
  try {
    return await playwright.chromium.launch({ headless: true });
  } catch (managedError) {
    for (const executablePath of candidateBrowserExecutables()) {
      try {
        return await playwright.chromium.launch({
          headless: true,
          executablePath,
        });
      } catch (_) {
        // Keep trying candidates; preserve the managed-browser error if none work.
      }
    }
    throw managedError;
  }
}

async function visibleCount(page, selector) {
  return page.$$eval(selector, (elements) =>
    elements.filter((element) => {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    }).length
  );
}

async function waitForMode(page, mode) {
  await page.waitForFunction(
    (expected) => document.documentElement.getAttribute("data-asi-reading-mode") === expected,
    mode,
    { timeout: 5000 }
  );
}

async function validateResponsiveLayout(page, pageId, mode) {
  const metrics = await page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const scrollWidth = Math.max(doc.scrollWidth, body ? body.scrollWidth : 0);
    const clientWidth = doc.clientWidth;
    const toggle = document.querySelector(".asi-reading-mode");
    const toggleRect = toggle ? toggle.getBoundingClientRect() : null;
    const toggleStyle = toggle ? window.getComputedStyle(toggle) : null;
    const buttons = Array.from(document.querySelectorAll("[data-asi-reading-choice]")).map((button) => {
      const rect = button.getBoundingClientRect();
      const style = window.getComputedStyle(button);
      return {
        choice: button.getAttribute("data-asi-reading-choice") || "",
        text: button.textContent ? button.textContent.trim() : "",
        visible:
          style.display !== "none" &&
          style.visibility !== "hidden" &&
          rect.width > 0 &&
          rect.height > 0,
        rect: {
          left: rect.left,
          right: rect.right,
          top: rect.top,
          bottom: rect.bottom,
          width: rect.width,
          height: rect.height,
        },
        clipped_horizontally: rect.left < -1 || rect.right > viewportWidth + 1,
        text_overflow_px: Math.max(0, button.scrollWidth - button.clientWidth),
      };
    });
    return {
      viewport_width: viewportWidth,
      viewport_height: viewportHeight,
      client_width: clientWidth,
      scroll_width: scrollWidth,
      horizontal_overflow_px: Math.max(0, scrollWidth - clientWidth),
      toggle_visible:
        Boolean(toggle) &&
        toggleStyle.display !== "none" &&
        toggleStyle.visibility !== "hidden" &&
        toggleRect.width > 0 &&
        toggleRect.height > 0,
      toggle_rect: toggleRect
        ? {
            left: toggleRect.left,
            right: toggleRect.right,
            top: toggleRect.top,
            bottom: toggleRect.bottom,
            width: toggleRect.width,
            height: toggleRect.height,
          }
        : null,
      toggle_clipped_horizontally: toggleRect ? toggleRect.left < -1 || toggleRect.right > viewportWidth + 1 : true,
      buttons,
    };
  });

  if (metrics.horizontal_overflow_px > 2) {
    throw new Error(`${pageId}: ${mode} view has ${metrics.horizontal_overflow_px}px horizontal page overflow.`);
  }
  if (!metrics.toggle_visible) throw new Error(`${pageId}: ${mode} view reading-mode control is not visible.`);
  if (metrics.toggle_clipped_horizontally) throw new Error(`${pageId}: ${mode} view reading-mode control is clipped horizontally.`);
  if (metrics.buttons.length < 2) throw new Error(`${pageId}: ${mode} view did not render both reading-mode buttons.`);
  for (const button of metrics.buttons) {
    if (!button.visible) throw new Error(`${pageId}: ${mode} view reading-mode button ${button.choice} is not visible.`);
    if (button.clipped_horizontally) {
      throw new Error(`${pageId}: ${mode} view reading-mode button ${button.choice} is clipped horizontally.`);
    }
    if (button.text_overflow_px > 2) {
      throw new Error(`${pageId}: ${mode} view reading-mode button ${button.choice} has ${button.text_overflow_px}px text overflow.`);
    }
  }
  return metrics;
}

async function validateRenderedDiagrams(page, pageId, mode) {
  const collectMetrics = () =>
    page.evaluate(() => {
      const diagrams = Array.from(document.querySelectorAll('.cell-output-display svg[id^="mermaid"], svg[id^="mermaid"]')).map(
        (diagram) => {
          const rect = diagram.getBoundingClientRect();
          const style = window.getComputedStyle(diagram);
          const contentCount = diagram.querySelectorAll("path, rect, polygon, circle, ellipse, line, text, g.node, g.edgePath").length;
          const textCount = diagram.querySelectorAll("text").length;
          const visible =
            style.display !== "none" &&
            style.visibility !== "hidden" &&
            rect.width > 80 &&
            rect.height > 20 &&
            contentCount > 5;
          return {
            id: diagram.id || "",
            width: rect.width,
            height: rect.height,
            visible,
            content_count: contentCount,
            text_count: textCount,
          };
        }
      );
      return {
        diagram_count: diagrams.length,
        visible_diagram_count: diagrams.filter((diagram) => diagram.visible).length,
        diagrams,
      };
    });

  try {
    await page.waitForFunction(
      () =>
        Array.from(document.querySelectorAll('.cell-output-display svg[id^="mermaid"], svg[id^="mermaid"]')).some(
          (diagram) => {
            const rect = diagram.getBoundingClientRect();
            const style = window.getComputedStyle(diagram);
            const contentCount = diagram.querySelectorAll("path, rect, polygon, circle, ellipse, line, text, g.node, g.edgePath").length;
            return (
              style.display !== "none" &&
              style.visibility !== "hidden" &&
              rect.width > 80 &&
              rect.height > 20 &&
              contentCount > 5
            );
          }
        ),
      null,
      { timeout: 7000 }
    );
  } catch (error) {
    const metrics = await collectMetrics();
    throw new Error(`${pageId}: ${mode} view did not render a visible Mermaid diagram before timeout: ${JSON.stringify(metrics)}`);
  }

  const metrics = await collectMetrics();

  if (metrics.visible_diagram_count < 1) {
    throw new Error(`${pageId}: ${mode} view has no visible rendered Mermaid diagram.`);
  }
  return metrics;
}

async function validateChapterPage(page, fileUrl, pageId) {
  const record = { page_id: pageId, url: fileUrl, checks: {} };
  await page.goto(`${fileUrl}?view=human`, { waitUntil: "domcontentloaded" });
  await waitForMode(page, "human");
  await page.waitForSelector(".asi-reading-mode", { timeout: 5000 });
  await page.waitForSelector(".asi-core-claim-marker", { state: "attached", timeout: 5000 });
  await page.waitForSelector(".asi-support-boilerplate-ai", { state: "attached", timeout: 5000 });

  const liveSections = await page.locator('section[data-asi-live-section="true"]').count();
  const humanBlocks = await page.locator(".asi-human-only").count();
  const claimMarkers = await page.locator(".asi-core-claim-marker").count();
  const supportBoilerplate = await page.locator(".asi-support-boilerplate-ai").count();
  const liveVisibleHuman = await visibleCount(page, 'section[data-asi-live-section="true"]');
  const humanVisibleHuman = await visibleCount(page, ".asi-human-only");
  const claimMarkersVisibleHuman = await visibleCount(page, ".asi-core-claim-marker");
  const claimTextVisibleHuman = await visibleCount(page, ".asi-core-claim-text");
  const supportBoilerplateVisibleHuman = await visibleCount(page, ".asi-support-boilerplate-ai");
  const supportBoundaryVisibleHuman = await visibleCount(page, ".asi-support-boundary-human");
  const liveTocVisibleHuman = await visibleCount(page, '#TOC [data-asi-live-toc-link="true"]');
  const humanStatus = await page.locator("[data-asi-reading-mode-status]").textContent();
  const humanLayout = await validateResponsiveLayout(page, pageId, "human");
  const humanDiagrams = await validateRenderedDiagrams(page, pageId, "human");

  record.checks.human_url_mode = {
    live_sections: liveSections,
    human_blocks: humanBlocks,
    core_claim_markers: claimMarkers,
    support_boilerplate_phrases: supportBoilerplate,
    visible_live_sections: liveVisibleHuman,
    visible_human_blocks: humanVisibleHuman,
    visible_core_claim_markers: claimMarkersVisibleHuman,
    visible_core_claim_text: claimTextVisibleHuman,
    visible_support_boilerplate_phrases: supportBoilerplateVisibleHuman,
    visible_human_support_boundaries: supportBoundaryVisibleHuman,
    visible_live_toc_links: liveTocVisibleHuman,
    status_text: humanStatus || "",
    layout: humanLayout,
    diagrams: humanDiagrams,
  };

  if (liveSections <= 0) throw new Error(`${pageId}: no live-only sections were marked.`);
  if (humanBlocks <= 0) throw new Error(`${pageId}: no human-only bridge block rendered.`);
  if (claimMarkers <= 0) throw new Error(`${pageId}: no core claim markers were wrapped for reading-mode control.`);
  if (supportBoilerplate <= 0) throw new Error(`${pageId}: no support-boundary boilerplate was wrapped for reading-mode control.`);
  if (liveVisibleHuman !== 0) throw new Error(`${pageId}: Human view left ${liveVisibleHuman} live-only sections visible.`);
  if (liveTocVisibleHuman !== 0) throw new Error(`${pageId}: Human view left ${liveTocVisibleHuman} live-only TOC links visible.`);
  if (humanVisibleHuman <= 0) throw new Error(`${pageId}: Human view did not show the human-only bridge.`);
  if (claimMarkersVisibleHuman !== 0) throw new Error(`${pageId}: Human view left ${claimMarkersVisibleHuman} raw core claim markers visible.`);
  if (claimTextVisibleHuman <= 0) throw new Error(`${pageId}: Human view hid the core claim text with the marker.`);
  if (supportBoilerplateVisibleHuman !== 0) throw new Error(`${pageId}: Human view left ${supportBoilerplateVisibleHuman} repeated support boilerplate phrases visible.`);
  if (supportBoundaryVisibleHuman <= 0) throw new Error(`${pageId}: Human view did not show the compact evidence-boundary phrase.`);
  if (!(humanStatus || "").includes("Human view active.")) throw new Error(`${pageId}: Human view status text did not update.`);

  await page.locator('[data-asi-reading-choice="ai"]').click();
  await waitForMode(page, "ai");
  const liveVisibleAi = await visibleCount(page, 'section[data-asi-live-section="true"]');
  const humanVisibleAi = await visibleCount(page, ".asi-human-only");
  const claimMarkersVisibleAi = await visibleCount(page, ".asi-core-claim-marker");
  const supportBoilerplateVisibleAi = await visibleCount(page, ".asi-support-boilerplate-ai");
  const supportBoundaryVisibleAi = await visibleCount(page, ".asi-support-boundary-human");
  const aiStatus = await page.locator("[data-asi-reading-mode-status]").textContent();
  const aiLayout = await validateResponsiveLayout(page, pageId, "ai");
  const aiDiagrams = await validateRenderedDiagrams(page, pageId, "ai");
  record.checks.ai_click_mode = {
    visible_live_sections: liveVisibleAi,
    visible_human_blocks: humanVisibleAi,
    visible_core_claim_markers: claimMarkersVisibleAi,
    visible_support_boilerplate_phrases: supportBoilerplateVisibleAi,
    visible_human_support_boundaries: supportBoundaryVisibleAi,
    status_text: aiStatus || "",
    url: page.url(),
    layout: aiLayout,
    diagrams: aiDiagrams,
  };
  if (liveVisibleAi <= 0) throw new Error(`${pageId}: AI view did not restore live-only sections.`);
  if (humanVisibleAi !== 0) throw new Error(`${pageId}: AI view left ${humanVisibleAi} human-only bridge blocks visible.`);
  if (claimMarkersVisibleAi <= 0) throw new Error(`${pageId}: AI view did not restore raw core claim markers.`);
  if (supportBoilerplateVisibleAi <= 0) throw new Error(`${pageId}: AI view did not restore repeated support boilerplate phrases.`);
  if (supportBoundaryVisibleAi !== 0) throw new Error(`${pageId}: AI view left ${supportBoundaryVisibleAi} compact human evidence-boundary phrases visible.`);
  if (!page.url().includes("view=ai")) throw new Error(`${pageId}: AI click did not update the URL mode.`);
  if (!(aiStatus || "").includes("AI/research view active.")) throw new Error(`${pageId}: AI view status text did not update.`);

  await page.locator('[data-asi-reading-choice="human"]').click();
  await waitForMode(page, "human");
  record.checks.human_click_url = page.url();
  if (!page.url().includes("view=human")) throw new Error(`${pageId}: Human click did not update the URL mode.`);

  await page.goto(fileUrl, { waitUntil: "domcontentloaded" });
  await waitForMode(page, "human");
  record.checks.local_storage_persistence = "human";

  await page.goto(`${fileUrl}?view=ai`, { waitUntil: "domcontentloaded" });
  await waitForMode(page, "ai");
  record.checks.ai_url_mode = {
    visible_live_sections: await visibleCount(page, 'section[data-asi-live-section="true"]'),
    visible_human_blocks: await visibleCount(page, ".asi-human-only"),
    visible_core_claim_markers: await visibleCount(page, ".asi-core-claim-marker"),
    visible_support_boilerplate_phrases: await visibleCount(page, ".asi-support-boilerplate-ai"),
    visible_human_support_boundaries: await visibleCount(page, ".asi-support-boundary-human"),
    layout: await validateResponsiveLayout(page, pageId, "ai-url"),
    diagrams: await validateRenderedDiagrams(page, pageId, "ai-url"),
  };
  if (record.checks.ai_url_mode.visible_live_sections <= 0) throw new Error(`${pageId}: ?view=ai did not show live-only sections.`);
  if (record.checks.ai_url_mode.visible_human_blocks !== 0) throw new Error(`${pageId}: ?view=ai did not hide human bridge blocks.`);
  if (record.checks.ai_url_mode.visible_core_claim_markers <= 0) throw new Error(`${pageId}: ?view=ai did not show raw core claim markers.`);
  if (record.checks.ai_url_mode.visible_support_boilerplate_phrases <= 0) throw new Error(`${pageId}: ?view=ai did not show repeated support boilerplate phrases.`);
  if (record.checks.ai_url_mode.visible_human_support_boundaries !== 0) throw new Error(`${pageId}: ?view=ai did not hide compact human evidence-boundary phrases.`);

  return record;
}

async function validateAppendixPage(page, fileUrl, pageId) {
  const record = { page_id: pageId, url: fileUrl, checks: {} };
  await page.goto(`${fileUrl}?view=human`, { waitUntil: "domcontentloaded" });
  await waitForMode(page, "human");
  await page.waitForSelector(".asi-reading-mode", { timeout: 5000 });
  const status = await page.locator("[data-asi-reading-mode-status]").textContent();
  record.checks.human_url_mode = {
    status_text: status || "",
    layout: await validateResponsiveLayout(page, pageId, "human"),
  };
  if (!(status || "").includes("Human view active.")) throw new Error(`${pageId}: Human view status text did not update.`);
  await page.locator('[data-asi-reading-choice="ai"]').click();
  await waitForMode(page, "ai");
  record.checks.ai_click_url = page.url();
  record.checks.ai_click_layout = await validateResponsiveLayout(page, pageId, "ai");
  if (!page.url().includes("view=ai")) throw new Error(`${pageId}: AI click did not update appendix URL mode.`);
  return record;
}

async function runBrowserValidation(playwright, args) {
  const structure = loadJson("book_structure.json");
  const pageSelection = args.allChapters ? "all-chapters" : "sample";
  const pages = pagesForValidation(structure, args.allChapters);
  const viewports = viewportsForValidation(args.allViewports);
  const missing = pages
    .map((record) => renderedPath(args.site, record.sourceFile))
    .filter((htmlPath) => !fs.existsSync(htmlPath));
  if (missing.length) {
    throw new Error(`Rendered HTML is missing. Run quarto render --to html first. Missing: ${missing.join(", ")}`);
  }

  const browser = await launchChromium(playwright);
  const records = [];
  try {
    for (const viewport of viewports) {
      const page = await browser.newPage({ viewport: viewport.size });
      try {
        for (const sample of pages) {
          const htmlPath = renderedPath(args.site, sample.sourceFile);
          const fileUrl = pathToFileURL(htmlPath).href;
          const record =
            sample.kind === "chapter"
              ? await validateChapterPage(page, fileUrl, sample.id)
              : await validateAppendixPage(page, fileUrl, sample.id);
          record.viewport = viewport.name;
          record.viewport_size = viewport.size;
          records.push(record);
        }
      } finally {
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }

  return {
    schema_version: "0.1",
    status: "pass",
    page_selection: pageSelection,
    viewport_selection: args.allViewports ? "all-viewports" : "desktop",
    viewports: viewports.map((viewport) => ({ name: viewport.name, ...viewport.size })),
    site_dir: args.site,
    validated_pages: records,
    // Backward-compatible alias for consumers created before --all-chapters.
    sampled_pages: records,
    non_claims: [
      "This browser smoke test validates rendered reading-mode interaction, responsive layout fit, and rendered Mermaid visibility only.",
      "It does not claim a reviewed reader edition, ebook, PDF, DOCX, audiobook, or support-state promotion exists.",
    ],
  };
}

function writeReport(reportPath, report) {
  fs.mkdirSync(path.dirname(reportPath), { recursive: true });
  fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
}

(async () => {
  const args = parseArgs(process.argv);
  const playwright = loadPlaywright();
  if (!playwright) {
    const report = {
      schema_version: "0.1",
      status: "skipped",
      reason: "Playwright is not available in the current Node environment.",
    };
    writeReport(args.report, report);
    console.log("Live Human view browser validation skipped: Playwright is not available.");
    process.exit(args.strict ? 1 : 0);
  }

  try {
    const report = await runBrowserValidation(playwright, args);
    writeReport(args.report, report);
    console.log(
      `Live Human view browser validation passed: ${report.validated_pages.length} rendered page-view pairs exercised (${report.page_selection}, ${report.viewport_selection}).`
    );
  } catch (error) {
    const message = error && error.stack ? error.stack : String(error);
    writeReport(args.report, {
      schema_version: "0.1",
      status: "fail",
      error: message,
    });
    const unavailable = /Executable doesn't exist|browserType\.launch|Host system is missing dependencies|install-deps/i.test(message);
    if (unavailable && !args.strict) {
      console.log(`Live Human view browser validation skipped: ${message.split("\n")[0]}`);
      process.exit(0);
    }
    console.error("Live Human view browser validation failed:");
    console.error(message);
    process.exit(1);
  }
})();
