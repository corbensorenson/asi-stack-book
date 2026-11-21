#!/usr/bin/env node
/* Compare the two actual browser interfaces on a fixed local publication. */
const assert = require("node:assert/strict");
const { createHash } = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { gunzipSync } = require("node:zlib");
const { chromium } = require("../../ci/browser/node_modules/playwright");

const [siteArgument, output] = process.argv.slice(2);
assert(siteArgument && output, "usage: node compare.cjs SITE OUTPUT.json");
const site = path.resolve(siteArgument);
const root = "https://corbensorenson.github.io/asi-stack-book/";
const graphBase = root + "products/evidence-registry/knowledge-graph/";
const registry = root + "products/evidence-registry/";
const taskBytes = fs.readFileSync(path.join(__dirname, "tasks.json"));
const tasks = JSON.parse(taskBytes);
const hash = data => createHash("sha256").update(data).digest("hex");
const readSite = name => fs.readFileSync(path.join(site, name));
const graph = JSON.parse(gunzipSync(readSite("products/evidence-registry/knowledge-graph/graph.json.gz")));
const nodes = new Map(graph.nodes.map(node => [node.id, node]));
const catalog = "products/evidence-registry/knowledge-graph/search.json";
const budget = {primary: 4, follow: 4, excerpt_bytes: 1000};
const entries = {technical: root, reader: root + "reader/", registry};

const slug = text => text.normalize("NFKD").toLowerCase().match(/[a-z0-9]+/g)?.join(" ") || "";
const clean = text => text.replace(/\s+/g, " ").trim();
const bytes = text => Buffer.byteLength(text || "");
function excerpt(text) {
  let result = clean(text);
  while (bytes(result) > budget.excerpt_bytes) result = result.slice(0, -1);
  return result;
}
function relative(href) {
  if (!href?.startsWith(root)) return null;
  const url = new URL(href);
  let name = decodeURIComponent(url.pathname.slice(new URL(root).pathname.length));
  if (!name || name.endsWith("/")) name += "index.html";
  return name + decodeURIComponent(url.hash);
}
function graphID(href) {
  return href?.startsWith(graphBase) ? new URL(href).searchParams.get("node") : null;
}
const stop = new Set(["a", "and", "as", "in", "is", "of", "on", "the", "to", "with"]);
function linkScore(query, label) {
  const phrase = slug(query);
  const name = slug(label);
  if (!name) return 0;
  if (phrase === name) return 100;
  if ((" " + name + " ").includes(" " + phrase + " ")) return 50;
  const terms = new Set(phrase.split(" ").filter(term => !stop.has(term)));
  const words = new Set(name.split(" "));
  return [...terms].filter(term => words.has(term)).length;
}
function editionMatch(href, edition) {
  const id = graphID(href);
  if (id) return id.startsWith(edition === "reader" ? "reader_unit:" : "chapter:");
  return relative(href)?.startsWith(edition === "reader" ? "reader/chapters/" : "chapters/");
}
function rankLinks(query, links, edition) {
  return links.map(link => ({...link, rank: linkScore(query, link.label) +
    (edition && editionMatch(link.href, edition) ? 200 : 0)}))
    .sort((a, b) => b.rank - a.rank);
}
function uniqueLinks(links, seen = new Set()) {
  return links.filter(link => {
    const key = graphID(link.href) || relative(link.href);
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

async function candidate(context) {
  await context.route("**/*", async route => {
    const name = relative(route.request().url())?.split("#")[0];
    if (!name) return route.abort();
    const target = path.resolve(site, name);
    if (!target.startsWith(site + path.sep) || !fs.statSync(target, {throwIfNoEntry: false})?.isFile()) {
      return route.fulfill({status: 404, contentType: "text/plain", body: "Missing candidate route"});
    }
    return route.fulfill({path: target});
  });
}
async function labels(locator) {
  return locator.evaluateAll(anchors => anchors.map(a => ({
    href: a.href, label: (a.innerText || a.textContent || "").trim(),
  })));
}
async function startSearch(page, task, method) {
  let links;
  if (method === "graph") {
    await page.goto(graphBase);
    await page.locator("#record h3").first().waitFor();
    await page.getByRole("searchbox", {name: "Search the graph"}).fill(task.query);
    await page.getByRole("button", {name: "Search", exact: true}).click();
    links = await labels(page.locator("#results a"));
  } else if (task.entry === "registry") {
    await page.goto(registry);
    links = rankLinks(task.query, await labels(page.locator('main a[href*="study-"][href$=".html"]')));
  } else {
    await page.goto(entries[task.entry]);
    await page.locator("#quarto-search button").first().click();
    await page.locator("input.aa-Input:visible").first().fill(task.query);
    const result = page.locator("li.aa-Item a.search-result-link");
    const empty = page.locator(".quarto-search-no-results:not(.no-query)");
    await result.first().or(empty).first().waitFor({state: "attached"});
    links = await labels(result);
  }
  return uniqueLinks(links).slice(0, budget.primary);
}

async function inspect(page, link) {
  const id = graphID(link.href);
  const route = relative(link.href);
  const response = await page.goto(link.href, {waitUntil: "domcontentloaded"});
  const status = response?.status() ?? (page.url() === link.href ? 200 : null);
  if (status !== 200) return {route, id, label: excerpt(link.label), status, text: "", links: []};
  if (id) {
    await page.waitForFunction(expected => document.querySelector("#record > p > code")?.textContent === expected, id);
  } else if (route.startsWith("chapters/")) {
    // The standard Reader link resolves the chapter's crosswalk asynchronously.
    await page.waitForLoadState("networkidle");
  }
  const detail = await page.evaluate(id => {
    const record = id ? document.querySelector("#record") : document.querySelector("main");
    const fragment = decodeURIComponent(location.hash.slice(1));
    const anchor = fragment ? document.getElementById(fragment) : null;
    const scope = id ? record : anchor?.closest("section,tr") || anchor || record;
    const headings = id ? "h3" : "h4";
    const evidenceLimit = [...(scope?.querySelectorAll(headings) || [])]
      .find(heading => /^(Evidence limit|Scope and limits)$/.test(heading.textContent));
    const core = [...(scope?.children || [])].filter(el => /^(P|H[1-4]|TD)$/.test(el.tagName))
      .slice(0, 7).map(el => el.innerText);
    const sourceLinks = [...(record?.querySelectorAll("a[href]") || [])];
    const links = sourceLinks.map(a => ({href: a.href, label: (a.innerText || a.textContent || "").trim()}));
    return {anchor: !!anchor, text: [evidenceLimit?.nextElementSibling?.innerText, ...core].filter(Boolean).join(" "), links};
  }, id);
  return {route, id, label: excerpt(link.label), status, anchor: detail.anchor,
    text: excerpt(detail.text), links: detail.links};
}
function matches(record, node) {
  if (!node || record.status !== 200) return false;
  if (record.id) return record.id === node.id;
  if (!node.url) return false;
  return node.url.includes("#") ? record.anchor && record.route === node.url :
    record.route.split("#")[0] === node.url;
}
async function compare(context, task, method) {
  const page = await context.newPage();
  try {
    await page.setViewportSize({width: 1300, height: 820});
    const links = await startSearch(page, task, method);
    const primary = [];
    for (const link of links) primary.push(await inspect(page, link));
    const seen = new Set();
    uniqueLinks(links, seen);
    const edition = task.kind === "cross-edition" ? (task.entry === "reader" ? "technical" : "reader") : null;
    const reachable = primary.flatMap(record => record.links)
      .filter(link => {
        const destination = relative(link.href);
        return destination && (graphID(link.href) ||
          /^(chapters|appendices|papers|reader\/chapters|products\/evidence-registry)\/.+\.html(?:#.*)?$/.test(destination));
      });
    const next = uniqueLinks(rankLinks(task.query, reachable, edition), seen).slice(0, budget.follow);
    const followed = [];
    for (const link of next) followed.push(await inspect(page, link));
    const records = [...primary, ...followed];
    const target = nodes.get(task.target);
    const owner = nodes.get(task.owner);
    const exactAt = records.findIndex(record => matches(record, target));
    return {
      primary_exact: exactAt >= 0 && exactAt < primary.length, exact: exactAt >= 0, first_exact_rank: exactAt < 0 ? null : exactAt + 1,
      owner: records.some(record => matches(record, owner || target)),
      same_record_limit: task.limit ? records.some(record => matches(record, target) &&
        slug(record.text).includes(slug(task.limit))) : null,
      excerpt_bytes: records.reduce((total, record) => total + bytes(record.text), 0),
      primary: primary.map(({links, ...record}) => record),
      followed: followed.map(({links, ...record}) => record),
    };
  } catch (error) {
    return {error: String(error)};
  } finally {
    await page.close();
  }
}

async function main() {
  assert(new Set(tasks.map(task => task.id)).size === tasks.length);
  for (const task of tasks) {
    assert(nodes.get(task.target)?.url, task.id);
    if (task.owner) assert(nodes.get(task.owner)?.url, task.id);
    if (task.limit) assert(slug(nodes.get(task.target).limit).includes(slug(task.limit)), task.id);
  }
  const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined});
  try {
    const context = await browser.newContext();
    context.setDefaultTimeout(5000);
    await candidate(context);
    const results = [];
    for (const [index, task] of tasks.entries()) {
      const row = {task: task.id, kind: task.kind};
      for (const method of (index % 2 ? ["graph", "baseline"] : ["baseline", "graph"])) {
        row[method] = await compare(context, task, method);
      }
      results.push(row);
      console.log(task.id, row.baseline.error || row.baseline.first_exact_rank, row.graph.error || row.graph.first_exact_rank);
    }
    const report = {
      schema: "asi-stack.graph-navigation-comparison.v1", snapshot_id: graph.snapshot_id,
      source_commit: graph.source_commit, worktree: graph.worktree, graph_input_sha256: graph.inputs_sha256,
      reader_search_sha256: hash(readSite("reader/search.json")), search_sha256: hash(readSite("search.json")),
      graph_search_sha256: hash(readSite(catalog)), registry_sha256: hash(readSite("products/evidence-registry/index.html")),
      tasks_sha256: hash(taskBytes), runner_sha256: hash(fs.readFileSync(__filename)),
      protocol_sha256: hash(fs.readFileSync(path.join(__dirname, "protocol.md"))),
      browser: browser.version(), budget, results,
    };
    fs.writeFileSync(output, JSON.stringify(report, null, 2) + "\n");
    if (results.some(row => row.baseline.error || row.graph.error)) process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
