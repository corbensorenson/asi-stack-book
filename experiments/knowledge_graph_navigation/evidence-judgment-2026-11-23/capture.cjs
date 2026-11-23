"use strict";

const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

if (process.argv.length !== 4) throw new Error("Use capture.cjs SITE OUTPUT");
const site = path.resolve(process.argv[2]);
const root = "https://corbensorenson.github.io/asi-stack-book/";
const registry = "products/evidence-registry/knowledge-graph/";
const catalog = JSON.parse(fs.readFileSync(path.join(site, registry, "evidence-catalog.json"), "utf8"));
const tasksBytes = fs.readFileSync(path.join(__dirname, "tasks.json"));
const tasks = JSON.parse(tasksBytes);
const entries = {technical: "", reader: "reader/", paper: "papers/"};
const firstFour = 4;
const followed = 2;

function limited(value) {
  return Buffer.from(value.replace(/\s+/g, " ").trim()).subarray(0, 1400).toString().replace(/\uFFFD$/, "");
}

function canonical(href) {
  const url = new URL(href, root);
  url.searchParams.delete("q");
  return decodeURIComponent(url.href);
}

async function ordinary(page, task) {
  await page.goto(root + entries[task.entry]);
  await page.locator("#quarto-search button").first().click();
  const input = page.locator("input.aa-Input:visible").first();
  const facet = page.getByRole("combobox", { name: "Search scope" });
  const links = page.locator("li.aa-Item a.search-result-link");
  await input.fill("e-means");
  await facet.selectOption("evidence");
  await page.waitForFunction(() => document.querySelector(".asi-evidence-limit"));
  await input.fill(task.query);
  await page.waitForFunction(query => {
    const link = document.querySelector("li.aa-Item a.search-result-link");
    return link ? new URL(link.href).searchParams.get("q") === query
      : /no results/i.test(document.querySelector(".aa-Panel")?.innerText || "");
  }, task.query, { timeout: 8000 });
  return (await links.evaluateAll(rows => rows.slice(0, 4).map(link => ({
    href: link.href, excerpt: link.innerText,
  })))).map(row => ({...row, excerpt: limited(row.excerpt)}));
}

async function graph(page, task) {
  const params = new URLSearchParams({kind: "evidence", q: task.query});
  await page.goto(root + registry + "?" + params);
  await page.waitForFunction(() => /^(Showing|No matching)/.test(document.getElementById("status")?.textContent));
  return (await page.locator("#results li").evaluateAll(rows => rows.slice(0, 4).map(row => ({
    href: row.querySelector("a").href, id: row.querySelector("a").dataset.node, excerpt: row.innerText,
  })))).map(row => ({...row, excerpt: limited(row.excerpt)}));
}

async function checkFragment(page, href) {
  const response = await page.goto(href);
  const hash = decodeURIComponent(new URL(href).hash.slice(1));
  const opened = await page.evaluate(fragment => {
    const exact = fragment ? document.getElementById(fragment) : document.querySelector("main h1");
    if (!exact) return {visible: false, text: ""};
    const container = exact.closest("tr, section, aside") || exact;
    return {visible: !!exact.getClientRects().length, text: container.innerText};
  }, hash);
  return {url: canonical(href), status: response?.status() || 0, visible: opened.visible,
    excerpt: limited(opened.text)};
}

async function assess(context, task, arm) {
  const page = await context.newPage();
  try {
    const items = await (arm === "graph" ? graph(page, task) : ordinary(page, task));
    assert(items.length <= firstFour);
    const target = catalog.records.find(record => record.id === task.target);
    assert(target, task.target);
    const rank = items.findIndex(row => arm === "graph" ? row.id === target.id :
      canonical(row.href) === canonical(target.url));
    const routes = [];
    for (const row of items.slice(0, followed)) {
      let href = row.href;
      let preview;
      if (arm === "graph") {
        await page.goto(href);
        const record = page.locator("#record");
        const link = record.getByRole("link", {name: "Open in the book", exact: true});
        await link.waitFor();
        href = await link.evaluate(link => link.href);
        preview = limited(await record.evaluate(element =>
          [...element.children].slice(0, [...element.children].findIndex(child => child.classList.contains("relations")))
            .map(child => child.innerText).join(" ")));
      }
      routes.push({...(await checkFragment(page, href)), ...(preview ? {preview} : {})});
    }
    return {rank: rank < 0 ? null : rank + 1, items, routes};
  } finally {
    await page.close();
  }
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined,
  });
  try {
    const context = await browser.newContext({viewport: {width: 1280, height: 860}});
    await context.route("**/*", async request => {
      const url = request.request().url();
      if (!url.startsWith(root)) return request.abort();
      const target = path.resolve(site, decodeURIComponent(new URL(url).pathname.slice(new URL(root).pathname.length)));
      if (!target.startsWith(site + path.sep) && target !== site) return request.fulfill({status: 404});
      const selected = fs.statSync(target, {throwIfNoEntry: false})?.isDirectory() ? path.join(target, "index.html") : target;
      if (!fs.statSync(selected, {throwIfNoEntry: false})?.isFile()) return request.fulfill({status: 404});
      await request.fulfill({path: selected});
    });
    const results = [];
    for (const [index, task] of tasks.entries()) {
      const order = index % 2 ? ["graph", "ordinary"] : ["ordinary", "graph"];
      const result = {id: task.id, order};
      for (const arm of order) result[arm] = await assess(context, task, arm);
      results.push(result);
    }
    fs.writeFileSync(process.argv[3], JSON.stringify({source_commit: catalog.source_commit,
      snapshot_id: catalog.snapshot_id, tasks_sha256: crypto.createHash("sha256").update(tasksBytes).digest("hex"),
      chromium: browser.version(), results}, null, 2) + "\n");
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
