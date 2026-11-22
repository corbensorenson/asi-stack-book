#!/usr/bin/env node
/* Browser coverage of the public search, paper and evidence paths. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const live = process.argv[2] === "--live";
const site = path.resolve(process.argv[2] || "_site");
const root = "https://corbensorenson.github.io/asi-stack-book/";
const inlineMathPaper = "papers/treellm.html";
const displayMathPaper = "papers/deterministic_capability_compilation.html";
const mathPapers = [
  inlineMathPaper,
  "papers/reflexive_router_whitepaper.html",
  "papers/learning_compute_topology.html",
  displayMathPaper,
];

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

async function checkEquationScroll(page, selector) {
  const equations = page.locator(selector);
  const index = await equations.evaluateAll(elements =>
    elements.findIndex(el => el.scrollWidth - el.clientWidth > 40));
  assert(index >= 0, `expected a wide equation for ${selector}`);
  const equation = equations.nth(index);
  await equation.focus();
  assert(await equation.evaluate(el => document.activeElement === el));
  await equation.press("ArrowRight");
  await page.waitForFunction(el => el.scrollLeft > 0, await equation.elementHandle(), { timeout: 5000 });
  const reachesBothEnds = await equation.evaluate(el => {
    const math = el.querySelector("mjx-math");
    el.scrollLeft = 0;
    const start = math.getBoundingClientRect().left >= el.getBoundingClientRect().left - 1;
    el.scrollLeft = el.scrollWidth;
    return start && math.getBoundingClientRect().right <= el.getBoundingClientRect().right + 1;
  });
  assert(reachesBothEnds, `equation clipped for ${selector}`);
}

async function addRenderedMathFixture(page) {
  // Reproduce the CHTML output structure without fetching third-party assets
  // during candidate validation. The live pass waits for MathJax itself.
  await page.evaluate(() => {
    for (const kind of ["inline", "display"]) {
      const paragraph = document.createElement("p");
      const wrapper = document.createElement("span");
      wrapper.className = "math " + kind;
      const container = document.createElement("mjx-container");
      container.className = "MathJax";
      container.setAttribute("jax", "CHTML");
      container.tabIndex = 0;
      if (kind === "display") container.setAttribute("display", "true");
      const math = document.createElement("mjx-math");
      math.style.cssText = "display:inline-block; inline-size:48em";
      math.textContent = "Equation";
      container.append(math);
      wrapper.append(container);
      paragraph.append(wrapper);
      document.querySelector("main.content").prepend(paragraph);
    }
  });
}

async function checkKnowledgeGraph(context, root) {
  const page = await context.newPage();
  const requests = [];
  const errors = [];
  page.on("request", request => requests.push(new URL(request.url()).pathname));
  page.on("pageerror", error => errors.push(error.message));
  try {
    const route = root + "products/evidence-registry/knowledge-graph/";
    await page.setViewportSize({ width: 390, height: 820 });
    await page.goto(route);
    await page.getByRole("heading", { name: "Receipt", exact: true }).waitFor();
    assert(await page.getByRole("heading", { name: "Evidence limit", exact: true }).isVisible());
    await page.getByRole("searchbox", { name: "Search the graph" }).fill("e-means");
    await page.getByRole("button", { name: "Search", exact: true }).click();
    await page.locator("#results a").first().click();
    await page.getByRole("heading", { name: /^e-means: outperforming k-means/i }).waitFor();
    assert(await page.getByText("Assigned chapters (2)", { exact: true }).isVisible());
    await page.getByRole("searchbox", { name: "Search the graph" }).fill("source:answerability_atlas_synthesis");
    await page.getByRole("button", { name: "Search", exact: true }).click();
    await page.locator("#results a").first().click();
    await page.getByRole("heading", { name: /^What an Answerability Atlas Can and Cannot Do/i }).waitFor();
    assert.equal(await page.getByRole("link", { name: "Open in the book" }).getAttribute("href"),
      root + "papers/answerability_atlas_synthesis.html");
    await page.getByRole("link", { name: "Verifier rollout", exact: true }).click();
    await page.getByRole("heading", { name: "Which scope earns a verifier rollout?" }).waitFor();
    assert.equal(await page.getByText("Study runs (2)", { exact: true }).count(), 1);
    await page.reload();
    await page.getByRole("heading", { name: "Which scope earns a verifier rollout?" }).waitFor();
    const tasks = JSON.parse(fs.readFileSync(path.join(__dirname, "../experiments/knowledge_graph_navigation/retrieval_tasks.json")));
    for (const task of tasks) {
      await page.getByRole("combobox", { name: "Record type" }).selectOption(task.kind);
      await page.getByRole("searchbox", { name: "Search the graph" }).fill(task.query);
      await page.getByRole("button", { name: "Search", exact: true }).click();
      const hits = await page.locator("#results a").evaluateAll(links => links.slice(0, 3).map(link => link.dataset.node));
      assert(hits.includes(task.target), `graph search missed ${task.query}`);
    }

    await page.goto(route + "?node=reader_unit%3Aunit-09");
    await page.getByRole("link", { name: "Stable Capability Fields", exact: true }).click();
    await page.getByRole("heading", { name: "Stable Capability Fields", exact: true }).waitFor();
    const claims = page.locator("#record .relations > details > summary").filter({ hasText: /^Claims \(\d+\)$/ });
    const core = claims.locator("..").locator("li > a").first();
    assert.equal(await core.getAttribute("data-node"), "claim:stable-capability-fields.core");
    await core.click();
    await page.getByRole("link", { name: "Which scope earns a verifier rollout?", exact: true }).click();
    await page.getByRole("link", { name: "Absolute floor and equal memoization", exact: true }).click();
    await page.getByRole("heading", { name: "Evidence limit", exact: true }).waitFor();

    await page.goto(route + "?node=chapter%3Avirtual-context-abi");
    const sources = page.locator("#record .relations > details > summary").filter({ hasText: /^Source mappings \(\d+\)$/ });
    const group = sources.locator("..");
    await sources.waitFor();
    if (!(await group.evaluate(node => node.open))) await sources.click();
    assert.equal(await group.locator(":scope > ul > li > a[data-node='source:ext_emeans_2026']").count(), 0);
    await group.getByRole("button", { name: "Show more links" }).click();
    await group.getByText(/^Showing 20 of \d+$/).waitFor();
    await group.getByRole("searchbox", { name: "Filter source mappings" }).fill("source:ext_emeans_2026");
    await group.getByRole("button", { name: "Filter links" }).click();
    await group.locator("a[data-node='source:ext_emeans_2026']:visible").first().waitFor();
    await group.getByText("Passage review · reviewed", { exact: true }).first().waitFor();
    await group.getByRole("button", { name: "Clear" }).click();
    await group.getByText(/^Showing 20 of \d+$/).waitFor();

    await page.goto(route + "?node=source%3Aviea");
    await page.getByText("Unresolved references (4)", { exact: true }).click();
    await page.getByRole("button", { name: "Load references" }).click();
    await page.getByText("no corroborated current chapter", { exact: true }).first().waitFor();
    assert(requests.some(pathname => /\/nodes\/[0-9a-f]{2}\.json$/.test(pathname)));
    assert(requests.some(pathname => /\/relationships\/\d+\.json$/.test(pathname)));
    assert(!requests.some(pathname => pathname.endsWith("/graph.json.gz")), "lookup downloaded the complete graph");
    assert.deepEqual(errors, []);
    console.log("Knowledge graph search, evidence trail, full relationships, unresolved references, and shareable links passed.");
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
    if (!live) await serveCandidate(context);
    await search(context, root, "ext_cram_2026", /H_external_sources\.html[^#]*#ext_cram_2026$/);
    await search(context, root, "virtual-context-abi.core", /C_claim_evidence_matrix\.html[^#]*#virtual-context-abi\.core$/);
    await search(context, root, "e-means", /virtual-context-abi\.html[^#]*#clustering-the-retrieval-index$/);
    if (!live) await checkKnowledgeGraph(context, root);

    const page = await context.newPage();
    await page.setViewportSize({ width: 1280, height: 860 });
    const chapter = root + "chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html";
    await page.goto(chapter);
    if (!live) {
      const graphLink = page.getByRole("link", { name: "Explore in graph", exact: true });
      await page.waitForFunction(link => {
        const url = new URL(link.href);
        return url.searchParams.get("node") === "chapter:replaceable-cognitive-substrates-beyond-transformer-monoculture";
      }, await graphLink.elementHandle());
      await graphLink.click();
      await page.getByRole("heading", { name: "Replaceable Cognitive Substrates: Beyond Transformer Monoculture", exact: true }).waitFor();
      await page.goto(root + "appendices/H_external_sources.html");
      assert.equal(await page.locator("[data-asi-reader-edition]").getAttribute("href"), root + "reader/");
      await page.goto(chapter);
    }
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
          ...(!live ? ["products/evidence-registry/knowledge-graph/"] : []),
          "papers/bugbrain.html", ...mathPapers]) {
        await page.goto(root + route);
        if (scale === 2) await page.addStyleTag({ content: "html {font-size:200% !important}" });
        if (live && mathPapers.includes(route)) {
          await page.locator("mjx-container").first().waitFor({ state: "attached" });
          await page.evaluate(async () => { await window.MathJax.startup.promise; });
        }
        if (scale === 2 && route === inlineMathPaper && live) {
          await checkEquationScroll(page, 'main mjx-container:not([display="true"])');
        }
        if (scale === 2 && route === displayMathPaper) {
          if (!live) {
            await addRenderedMathFixture(page);
            await checkEquationScroll(page, 'main mjx-container:not([display="true"])');
          }
          await checkEquationScroll(page, 'main mjx-container[display="true"]');
        }
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        assert(overflow <= 2, `${route || "book home"} at ${width}px and ${scale}× text overflows by ${overflow}px`);
      }
    }
    await page.goto(root + "papers/bugbrain.html");
    const table = page.locator(".paper-table").filter({ has: page.locator("table") }).first();
    await table.focus();
    assert(await table.evaluate(el => document.activeElement === el));
    console.log("Exact citation search, keyboard selection, copied links, paper contents, table focus, equation scrolling and reflow passed.");
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
