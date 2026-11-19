#!/usr/bin/env node
/* Browser coverage of the public search, paper and evidence paths. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const site = path.resolve(process.argv[2] || "_site");
const root = "https://corbensorenson.github.io/asi-stack-book/";

async function serveCandidate(context) {
  // Keep Quarto's canonical origin so same-page links keep their normal
  // navigation behavior. The browser receives only bytes from the candidate.
  await context.route("**/*", async route => {
    const url = route.request().url();
    if (!url.startsWith(root)) return route.abort();
    const relative = decodeURIComponent(new URL(url).pathname.slice(new URL(root).pathname.length));
    let target = path.resolve(site, relative);
    if (!target.startsWith(site + path.sep) && target !== site) return route.fulfill({ status: 404 });
    if (fs.statSync(target, { throwIfNoEntry: false })?.isDirectory()) target = path.join(target, "index.html");
    if (!fs.statSync(target, { throwIfNoEntry: false })?.isFile()) return route.fulfill({ status: 404 });
    return route.fulfill({ path: target });
  });
}

async function search(browser, root, query, expected) {
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 860 });
  try {
    await page.goto(root);
    await page.locator("#quarto-search button").first().click();
    const input = page.locator("input.aa-Input:visible").first();
    const start = performance.now();
    await input.fill(query);
    const result = page.locator("li.aa-Item a.search-result-link").first();
    await result.waitFor();
    assert.match(await result.getAttribute("href"), expected, query);
    const firstUseful = performance.now() - start;
    const timing = await page.evaluate(async () => {
      const resource = performance.getEntriesByType("resource").find(entry => entry.name.endsWith("/search.json"));
      const bytes = await (await fetch("search.json")).text();
      const start = performance.now();
      JSON.parse(bytes);
      return { fetch_ms: resource?.duration, standalone_parse_ms: performance.now() - start };
    });
    await input.focus();
    if (!(await page.locator('li.aa-Item[aria-selected="true"]').count())) await page.keyboard.press("ArrowDown");
    await page.keyboard.press("Enter");
    await page.waitForURL(expected);
    const target = decodeURIComponent(new URL(page.url()).hash.slice(1));
    assert(await page.locator("#" + target.replace(".", "\\.")).first().isVisible(), query);
    console.log(JSON.stringify({ query, first_useful_ms: Math.round(firstUseful), ...timing }));
  } finally {
    await page.close();
  }
}

async function main() {
  const browser = await chromium.launch({
    executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined,
  });
  try {
    const context = await browser.newContext();
    await serveCandidate(context);
    await search(context, root, "ext_cram_2026", /H_external_sources\.html[^#]*#ext_cram_2026$/);
    await search(context, root, "virtual-context-abi.core", /C_claim_evidence_matrix\.html[^#]*#virtual-context-abi\.core$/);
    await search(context, root, "e-means", /virtual-context-abi\.html[^#]*#clustering-the-retrieval-index$/);

    const page = await context.newPage();
    await page.setViewportSize({ width: 1280, height: 860 });
    const chapter = root + "chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html";
    await page.goto(chapter);
    await page.locator('[data-asi-reading-choice="human"]').click();
    await page.goto(chapter + "#source-crosswalk");
    assert(await page.locator("#source-crosswalk").isVisible(), "copied citation is hidden");
    await page.goto(chapter + "?test=reading-preference", { waitUntil: "load" });
    assert.equal(await page.locator("html").getAttribute("data-asi-reading-mode"), "human");

    for (const [paper, fragment] of [["bugbrain", "#introduction"], ["treellm", "#introduction"]]) {
      await page.goto(root + "papers/" + paper + ".html");
      const link = page.locator(`main a[href$="${fragment}"]`).filter({ hasText: /^Introduction$/ }).first();
      await link.click();
      await page.waitForURL(url => url.hash === fragment, { timeout: 5000 }).catch(error => {
        throw new Error(`${paper}: ${page.url()} after clicking ${fragment}. ${error.message}`);
      });
      assert(await page.locator(fragment).isVisible());
    }

    for (const [width, scale] of [[1280, 1], [390, 1], [320, 1], [320, 2]]) {
      await page.setViewportSize({ width, height: 820 });
      for (const route of ["", "reader/", "reader/quickstart.html", "products/evidence-registry/",
          "papers/bugbrain.html", "papers/treellm.html", "papers/reflexive_router_whitepaper.html",
          "papers/learning_compute_topology.html", "papers/deterministic_capability_compilation.html"]) {
        await page.goto(root + route);
        if (scale === 2) await page.addStyleTag({ content: "html {font-size:200% !important}" });
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        assert(overflow <= 2, `${route || "book home"} at ${width}px and ${scale}× text overflows by ${overflow}px`);
      }
    }
    await page.goto(root + "papers/bugbrain.html");
    const table = page.locator(".paper-table").filter({ has: page.locator("table") }).first();
    await table.focus();
    assert(await table.evaluate(el => document.activeElement === el));
    console.log("Exact citation search, keyboard selection, copied links, paper contents, table focus and reflow passed.");
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
