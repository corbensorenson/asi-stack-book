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

function loadJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), "utf8"));
}

function flattenChapters(structure) {
  return (structure.parts || []).flatMap((part) => part.chapters || []);
}

function renderedPath(siteDir, sourceFile) {
  return path.join(siteDir, sourceFile.replace(/\.qmd$/, ".html"));
}

function samplePages(structure) {
  const chapters = flattenChapters(structure);
  const indexes = new Set([0, Math.floor(chapters.length / 2), chapters.length - 1]);
  const pages = [...indexes]
    .filter((index) => chapters[index])
    .map((index) => ({
      kind: "chapter",
      id: chapters[index].id,
      sourceFile: chapters[index].file,
    }));
  for (const appendixId of ["corben-source-corpus", "external-sources-and-literature"]) {
    const appendix = (structure.appendices || []).find((record) => record.id === appendixId);
    if (appendix) {
      pages.push({ kind: "appendix", id: appendix.id, sourceFile: appendix.file });
    }
  }
  return pages;
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

async function validateChapterPage(page, fileUrl, pageId) {
  const record = { page_id: pageId, url: fileUrl, checks: {} };
  await page.goto(`${fileUrl}?view=human`, { waitUntil: "domcontentloaded" });
  await waitForMode(page, "human");
  await page.waitForSelector(".asi-reading-mode", { timeout: 5000 });

  const liveSections = await page.locator('section[data-asi-live-section="true"]').count();
  const humanBlocks = await page.locator(".asi-human-only").count();
  const liveVisibleHuman = await visibleCount(page, 'section[data-asi-live-section="true"]');
  const humanVisibleHuman = await visibleCount(page, ".asi-human-only");
  const liveTocVisibleHuman = await visibleCount(page, '#TOC [data-asi-live-toc-link="true"]');
  const humanStatus = await page.locator("[data-asi-reading-mode-status]").textContent();

  record.checks.human_url_mode = {
    live_sections: liveSections,
    human_blocks: humanBlocks,
    visible_live_sections: liveVisibleHuman,
    visible_human_blocks: humanVisibleHuman,
    visible_live_toc_links: liveTocVisibleHuman,
    status_text: humanStatus || "",
  };

  if (liveSections <= 0) throw new Error(`${pageId}: no live-only sections were marked.`);
  if (humanBlocks <= 0) throw new Error(`${pageId}: no human-only bridge block rendered.`);
  if (liveVisibleHuman !== 0) throw new Error(`${pageId}: Human view left ${liveVisibleHuman} live-only sections visible.`);
  if (liveTocVisibleHuman !== 0) throw new Error(`${pageId}: Human view left ${liveTocVisibleHuman} live-only TOC links visible.`);
  if (humanVisibleHuman <= 0) throw new Error(`${pageId}: Human view did not show the human-only bridge.`);
  if (!(humanStatus || "").includes("Human view active.")) throw new Error(`${pageId}: Human view status text did not update.`);

  await page.locator('[data-asi-reading-choice="ai"]').click();
  await waitForMode(page, "ai");
  const liveVisibleAi = await visibleCount(page, 'section[data-asi-live-section="true"]');
  const humanVisibleAi = await visibleCount(page, ".asi-human-only");
  const aiStatus = await page.locator("[data-asi-reading-mode-status]").textContent();
  record.checks.ai_click_mode = {
    visible_live_sections: liveVisibleAi,
    visible_human_blocks: humanVisibleAi,
    status_text: aiStatus || "",
    url: page.url(),
  };
  if (liveVisibleAi <= 0) throw new Error(`${pageId}: AI view did not restore live-only sections.`);
  if (humanVisibleAi !== 0) throw new Error(`${pageId}: AI view left ${humanVisibleAi} human-only bridge blocks visible.`);
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
  };
  if (record.checks.ai_url_mode.visible_live_sections <= 0) throw new Error(`${pageId}: ?view=ai did not show live-only sections.`);
  if (record.checks.ai_url_mode.visible_human_blocks !== 0) throw new Error(`${pageId}: ?view=ai did not hide human bridge blocks.`);

  return record;
}

async function validateAppendixPage(page, fileUrl, pageId) {
  const record = { page_id: pageId, url: fileUrl, checks: {} };
  await page.goto(`${fileUrl}?view=human`, { waitUntil: "domcontentloaded" });
  await waitForMode(page, "human");
  await page.waitForSelector(".asi-reading-mode", { timeout: 5000 });
  const status = await page.locator("[data-asi-reading-mode-status]").textContent();
  record.checks.human_url_mode = { status_text: status || "" };
  if (!(status || "").includes("Human view active.")) throw new Error(`${pageId}: Human view status text did not update.`);
  await page.locator('[data-asi-reading-choice="ai"]').click();
  await waitForMode(page, "ai");
  record.checks.ai_click_url = page.url();
  if (!page.url().includes("view=ai")) throw new Error(`${pageId}: AI click did not update appendix URL mode.`);
  return record;
}

async function runBrowserValidation(playwright, args) {
  const structure = loadJson("book_structure.json");
  const pages = samplePages(structure);
  const missing = pages
    .map((record) => renderedPath(args.site, record.sourceFile))
    .filter((htmlPath) => !fs.existsSync(htmlPath));
  if (missing.length) {
    throw new Error(`Rendered HTML is missing. Run quarto render --to html first. Missing: ${missing.join(", ")}`);
  }

  const browser = await launchChromium(playwright);
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const records = [];
  try {
    for (const sample of pages) {
      const htmlPath = renderedPath(args.site, sample.sourceFile);
      const fileUrl = pathToFileURL(htmlPath).href;
      if (sample.kind === "chapter") {
        records.push(await validateChapterPage(page, fileUrl, sample.id));
      } else {
        records.push(await validateAppendixPage(page, fileUrl, sample.id));
      }
    }
  } finally {
    await browser.close();
  }

  return {
    schema_version: "0.1",
    status: "pass",
    site_dir: args.site,
    sampled_pages: records,
    non_claims: [
      "This browser smoke test validates rendered reading-mode interaction only.",
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
    console.log(`Live Human view browser validation passed: ${report.sampled_pages.length} rendered pages exercised.`);
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
