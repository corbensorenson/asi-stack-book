#!/usr/bin/env node
/*
Validate automated keyboard traversal for the local curated reader HTML artifact.

This is a release-preparation review, not a release approval, manual
keyboard-only review, screen-reader review, or WCAG conformance check.
*/

const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

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
  "curated_reader_keyboard_navigation_report.json"
);
const TRACKED_MANIFEST = path.join(
  ROOT,
  "editions",
  "reader_manuscript",
  "v1_0",
  "keyboard_navigation_manifest.json"
);
const REVIEW_DOC = path.join(ROOT, "docs", "reader_keyboard_navigation_review.md");
const COMMAND = "node scripts/validate_curated_reader_keyboard_navigation.js";
const WRITE_COMMAND = `${COMMAND} --write-manifest`;
const TAB_STEPS = 80;
const VIEWPORTS = {
  desktop: { width: 1280, height: 900 },
  mobile: { width: 390, height: 844 },
};
const REVIEW_BOUNDARY =
  "This automated keyboard traversal review opens the ignored local curated reader HTML artifact in Chromium, verifies the skip-to-main route, tabs through each page at desktop and mobile widths, and checks focus reachability, search/nav reachability, main-content route availability, and trap absence. It records body-wrap and offscreen focus observations as residuals. It is not manual keyboard-only review, not screen-reader review, not WCAG conformance, not e-reader review, not audiobook review, not final figure-artifact approval, and not reader release approval.";

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

async function inspectPage(page, filePath, viewportName, viewportSize) {
  await page.setViewportSize(viewportSize);
  await page.goto(pathToFileURL(filePath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(250);

  let skipLink = {
    reached: false,
    activated: false,
    text: "",
    href: "",
    visible: false,
    tab_index: 0,
    main_visible_after_activation: false,
  };
  for (let tabIndex = 1; tabIndex <= 12; tabIndex += 1) {
    await page.keyboard.press("Tab");
    const candidate = await page.evaluate((currentTabIndex) => {
      const active = document.activeElement;
      if (!active) {
        return {
          reached: false,
          activated: false,
          text: "",
          href: "",
          visible: false,
          tab_index: currentTabIndex,
          main_visible_after_activation: false,
        };
      }
      const text = (active.innerText || active.textContent || "").trim();
      const href = active.getAttribute("href") || "";
      const rect = active.getBoundingClientRect();
      return {
        reached: active.classList.contains("asi-skip-link") && href === "#quarto-document-content",
        activated: false,
        text,
        href,
        visible: rect.width > 0 && rect.height > 0 && rect.top >= 0 && rect.left >= 0,
        tab_index: currentTabIndex,
        main_visible_after_activation: false,
      };
    }, tabIndex);
    if (candidate.reached) {
      skipLink = candidate;
      break;
    }
  }
  if (skipLink.reached) {
    await page.keyboard.press("Enter");
    await page.waitForTimeout(150);
    const activation = await page.evaluate(() => {
      const main = document.querySelector("#quarto-document-content, main");
      if (!main) return { activated: false, main_visible_after_activation: false, hash: window.location.hash };
      const rect = main.getBoundingClientRect();
      return {
        activated: window.location.hash === "#quarto-document-content" || rect.top <= 96,
        main_visible_after_activation: rect.bottom > 0 && rect.top < window.innerHeight,
        hash: window.location.hash,
      };
    });
    Object.assign(skipLink, activation);
  }

  await page.goto(pathToFileURL(filePath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(250);

  const setup = await page.evaluate(() => {
    const candidates = Array.from(
      document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])')
    ).filter((node) => {
      const style = window.getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return !node.disabled && style.visibility !== "hidden" && style.display !== "none" && rect.width > 0 && rect.height > 0;
    });
    const main = document.querySelector("main, #quarto-document-content");
    return {
      focusable_count: candidates.length,
      has_main: Boolean(main),
      title: (document.querySelector("h1") || document.querySelector("title") || {}).textContent || "",
    };
  });

  const sequence = [];
  for (let index = 0; index < TAB_STEPS; index += 1) {
    await page.keyboard.press("Tab");
    sequence.push(
      await page.evaluate(() => {
        const active = document.activeElement;
        if (!active) {
          return {
            tag: "",
            key: "none",
            visible: false,
            in_main: false,
            in_navigation: false,
            is_search: false,
            body_or_document: true,
          };
        }
        const rect = active.getBoundingClientRect();
        const style = window.getComputedStyle(active);
        const text = (
          active.innerText ||
          active.getAttribute("aria-label") ||
          active.getAttribute("title") ||
          active.getAttribute("href") ||
          active.id ||
          ""
        )
          .trim()
          .replace(/\s+/g, " ")
          .slice(0, 90);
        const key = [
          active.tagName,
          active.id || "",
          active.getAttribute("href") || "",
          active.getAttribute("aria-label") || "",
          text,
        ].join("|");
        const outline = `${style.outlineStyle} ${style.outlineWidth} ${style.outlineColor}`;
        const boxShadow = style.boxShadow || "";
        return {
          tag: active.tagName,
          key,
          text,
          href: active.getAttribute("href") || "",
          visible:
            style.visibility !== "hidden" &&
            style.display !== "none" &&
            rect.width > 0 &&
            rect.height > 0 &&
            rect.bottom >= 0 &&
            rect.right >= 0 &&
            rect.top <= window.innerHeight + 4 &&
            rect.left <= window.innerWidth + 4,
          in_main: Boolean(active.closest("main, #quarto-document-content")),
          in_navigation: Boolean(active.closest("nav, #quarto-header, #quarto-sidebar, .sidebar-navigation")),
          is_search: Boolean(
            active.matches(".quarto-search-button, .aa-Input, input[type='search'], #quarto-search input") ||
              /search/i.test(active.getAttribute("aria-label") || "") ||
              /search/i.test(text)
          ),
          body_or_document: active === document.body || active === document.documentElement,
          outline,
          box_shadow: boxShadow,
          rect: {
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          },
        };
      })
    );
  }

  const uniqueTargets = [...new Set(sequence.map((row) => row.key).filter(Boolean))];
  const bodyFocusEvents = sequence.filter((row) => row.body_or_document).length;
  const invisibleFocusEvents = sequence.filter((row) => !row.visible).length;
  const mainContentFocusReached = sequence.some((row) => row.in_main);
  const mainContentRouteAvailable =
    mainContentFocusReached || Boolean(skipLink.reached && skipLink.activated && skipLink.main_visible_after_activation);
  const navigationFocusReached = sequence.some((row) => row.in_navigation);
  const searchFocusReached = sequence.some((row) => row.is_search);
  const keyboardTrapCandidate = uniqueTargets.length < Math.min(6, setup.focusable_count);
  const errors = [];

  if (!setup.has_main) errors.push("main content landmark was not found");
  if (setup.focusable_count < 5) errors.push(`too few visible focusable elements: ${setup.focusable_count}`);
  if (!skipLink.reached) errors.push("skip-to-main link was not reachable in the early keyboard sequence");
  if (skipLink.reached && !skipLink.visible) errors.push("skip-to-main link was focused but not visibly positioned");
  if (skipLink.reached && !skipLink.activated) errors.push("skip-to-main link did not activate the main content route");
  if (!mainContentRouteAvailable) errors.push("main content route was not available by skip link or tab traversal");
  if (!navigationFocusReached) errors.push("navigation/header/sidebar was not reached by tab traversal");
  if (!searchFocusReached) errors.push("search control was not reached by tab traversal");
  if (keyboardTrapCandidate) errors.push(`possible focus trap: only ${uniqueTargets.length} unique target(s) reached`);

  return {
    path: rel(filePath),
    kind: pageKind(filePath),
    viewport: viewportName,
    title: setup.title.trim(),
    focusable_count: setup.focusable_count,
    tab_steps: TAB_STEPS,
    unique_focus_targets: uniqueTargets.length,
    body_or_document_focus_events: bodyFocusEvents,
    invisible_focus_events: invisibleFocusEvents,
    skip_link_reached: Boolean(skipLink.reached),
    skip_link_activated: Boolean(skipLink.activated),
    skip_link_main_visible_after_activation: Boolean(skipLink.main_visible_after_activation),
    main_content_focus_reached: mainContentFocusReached,
    main_content_route_available: mainContentRouteAvailable,
    navigation_focus_reached: navigationFocusReached,
    search_focus_reached: searchFocusReached,
    keyboard_trap_candidate: keyboardTrapCandidate,
    status: errors.length ? "failed" : "passed",
    errors,
    first_focus_targets: sequence.slice(0, 12),
    last_focus_targets: sequence.slice(-12),
  };
}

function summarize(results, files, expectedFiles, args) {
  const failures = results.filter((row) => row.status !== "passed");
  const focusableCounts = results.map((row) => row.focusable_count);
  const uniqueCounts = results.map((row) => row.unique_focus_targets);
  const bodyEvents = results.reduce((total, row) => total + row.body_or_document_focus_events, 0);
  const invisibleEvents = results.reduce((total, row) => total + row.invisible_focus_events, 0);
  const trapCandidates = results.filter((row) => row.keyboard_trap_candidate).length;
  const skipReached = results.filter((row) => row.skip_link_reached).length;
  const skipActivated = results.filter((row) => row.skip_link_activated).length;
  const mainReached = results.filter((row) => row.main_content_focus_reached).length;
  const mainRoute = results.filter((row) => row.main_content_route_available).length;
  const navReached = results.filter((row) => row.navigation_focus_reached).length;
  const searchReached = results.filter((row) => row.search_focus_reached).length;
  const chapterPairs = results.filter((row) => row.kind === "chapter").length;
  return {
    schema_version: "asi_stack.curated_reader_keyboard_navigation.v0",
    result_id: "curated-reader-keyboard-navigation-2026-07-04",
    status: failures.length ? "failed_automated_keyboard_traversal_review" : "passed_automated_keyboard_traversal_review",
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
      tab_steps_per_page_view: TAB_STEPS,
      failed_page_view_pairs: failures.length,
      minimum_focusable_elements: Math.min(...focusableCounts),
      minimum_unique_focus_targets: Math.min(...uniqueCounts),
      skip_link_reached_pairs: skipReached,
      skip_link_activated_pairs: skipActivated,
      main_content_focus_reached_pairs: mainReached,
      main_content_route_available_pairs: mainRoute,
      navigation_focus_reached_pairs: navReached,
      search_focus_reached_pairs: searchReached,
      body_or_document_focus_events: bodyEvents,
      invisible_focus_events: invisibleEvents,
      keyboard_trap_candidates: trapCandidates,
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
    tab_steps_per_page_view: TAB_STEPS,
    failed_page_view_pairs: 0,
    skip_link_reached_pairs: summary.page_view_pairs,
    skip_link_activated_pairs: summary.page_view_pairs,
    main_content_route_available_pairs: summary.page_view_pairs,
    navigation_focus_reached_pairs: summary.page_view_pairs,
    search_focus_reached_pairs: summary.page_view_pairs,
    keyboard_trap_candidates: 0,
  } : {
    pages_checked: 49,
    expected_pages: 49,
    viewport_count: 2,
    page_view_pairs: 98,
    chapter_page_view_pairs: 88,
    tab_steps_per_page_view: TAB_STEPS,
    failed_page_view_pairs: 0,
    skip_link_reached_pairs: 98,
    skip_link_activated_pairs: 98,
    main_content_route_available_pairs: 98,
    navigation_focus_reached_pairs: 98,
    search_focus_reached_pairs: 98,
    keyboard_trap_candidates: 0,
  };
  if (manifest.status !== "passed_automated_keyboard_traversal_review") {
    errors.push("status must be passed_automated_keyboard_traversal_review.");
  }
  if (standalone && (!Number.isInteger(summary.expected_pages) || summary.expected_pages < 1)) {
    errors.push(`summary.expected_pages must be a positive integer; found ${summary.expected_pages}.`);
  }
  for (const [key, value] of Object.entries(expected)) {
    if (summary[key] !== value) {
      errors.push(`summary.${key} must be ${value}; found ${summary[key]}.`);
    }
  }
  if (summary.minimum_focusable_elements < 5) {
    errors.push(`summary.minimum_focusable_elements must be at least 5; found ${summary.minimum_focusable_elements}.`);
  }
  if (summary.minimum_unique_focus_targets < 5) {
    errors.push(`summary.minimum_unique_focus_targets must be at least 5; found ${summary.minimum_unique_focus_targets}.`);
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
    "# Reader Keyboard Navigation Review",
    "",
    "Last checked: 2026-07-04",
    "",
    "Command:",
    "",
    "```bash",
    WRITE_COMMAND,
    "```",
    "",
    `Tracked result: \`${rel(TRACKED_MANIFEST)}\``,
    "",
    "This automated browser review tabs through the ignored local curated-reader HTML artifact at desktop and mobile widths. It checks keyboard traversal, focus reachability, focus visibility, search/navigation reachability, main-content reachability, and trap absence. It is release-preparation evidence only.",
    "",
    "## Summary",
    "",
    "| Metric | Value |",
    "|---|---:|",
    `| Status | \`${manifest.status}\` |`,
    `| Pages checked | ${summary.pages_checked} |`,
    `| Expected pages | ${summary.expected_pages} |`,
    `| Viewports | ${summary.viewport_count} |`,
    `| Page-view pairs | ${summary.page_view_pairs} |`,
    `| Chapter page-view pairs | ${summary.chapter_page_view_pairs} |`,
    `| Tab steps per page-view | ${summary.tab_steps_per_page_view} |`,
    `| Failed page-view pairs | ${summary.failed_page_view_pairs} |`,
    `| Minimum focusable elements | ${summary.minimum_focusable_elements} |`,
    `| Minimum unique focus targets | ${summary.minimum_unique_focus_targets} |`,
    `| Skip-link route reached | ${summary.skip_link_reached_pairs} |`,
    `| Skip-link route activated | ${summary.skip_link_activated_pairs} |`,
    `| Main-content focus reached by Tab | ${summary.main_content_focus_reached_pairs} |`,
    `| Main-content route available | ${summary.main_content_route_available_pairs} |`,
    `| Navigation/search focus reached | ${summary.navigation_focus_reached_pairs} / ${summary.search_focus_reached_pairs} |`,
    "| Body/document wrap observations | Recorded in ignored detailed report |",
    "| Offscreen focus observations | Recorded in ignored detailed report |",
    `| Keyboard trap candidates | ${summary.keyboard_trap_candidates} |`,
    "",
    "## Gate",
    "",
    "Each page-view pair must expose visible focusable elements, make the skip-to-main link reachable in the early keyboard sequence, activate the skip-to-main route, reach navigation and search through repeated `Tab` traversal, and avoid short repeated focus cycles that indicate a likely keyboard trap. Body/document wrap observations and offscreen focus observations are recorded as residuals because Quarto pages can wrap after the finite target list or move fixed mobile controls slightly outside the viewport after scrolling.",
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
    "Reader Keyboard Navigation Review",
    WRITE_COMMAND,
    rel(TRACKED_MANIFEST),
    "automated browser review",
    `Pages checked | ${summary.pages_checked}`,
    `Page-view pairs | ${summary.page_view_pairs}`,
    `Failed page-view pairs | ${summary.failed_page_view_pairs}`,
    `Skip-link route activated | ${summary.skip_link_activated_pairs}`,
    `Main-content route available | ${summary.main_content_route_available_pairs}`,
    `Keyboard trap candidates | ${summary.keyboard_trap_candidates}`,
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
  const comparable = JSON.parse(JSON.stringify(manifest));
  if (comparable.summary) {
    delete comparable.summary.body_or_document_focus_events;
    delete comparable.summary.invisible_focus_events;
  }
  return comparable;
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
      console.error("Curated reader tracked keyboard navigation validation failed:");
      for (const error of trackedErrors) console.error(` - ${error}`);
      process.exit(1);
    }
    console.log(
      `Curated reader tracked keyboard navigation validation passed: ` +
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
  if (!playwright) throw new Error("Playwright is not available; cannot run keyboard navigation review.");
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
    console.error("Curated reader keyboard navigation validation failed:");
    for (const error of manifestErrors) console.error(` - ${error}`);
    process.exit(1);
  }
  console.log(
    `Curated reader keyboard navigation validation passed: ${manifest.summary.page_view_pairs} page-view pairs, ` +
      `${manifest.summary.failed_page_view_pairs} failures.`
  );
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
