// Run with NODE_PATH=ci/browser/node_modules node evaluate.cjs BASELINE_SITE CANDIDATE_SITE.
const fs = require("node:fs");
const http = require("node:http");
const path = require("node:path");
const vm = require("node:vm");
const { chromium } = require("playwright");
const questions = [
  ["Does putting fallback behind an intermediary spare my client calls when the first endpoint is already known to be down?", ["receiver-live-transport", "receiver-placement-decision"]],
  ["Could cheaper partitions bury the sentence that overturns a release note?", ["emeans-retrieval-rebuild"]],
  ["Arrivals doubled and the reviewer is drowning in outstanding checks. Would a ledger clear the backlog?", ["verification-arrivals", "verification-load"]],
  ["Can I give finance a dollar figure for the reviewer hours freed by verifier handoff?", ["verifier-measurement-boundary"]],
  ["Is a short warm puzzle fit evidence of faster end-to-end maze solving?", ["cram-replacement-decision"]],
  ["What is the maintenance team's annual payroll saving?", ["verifier-measurement-boundary"]],
];
const probes = [
  ["When is the second hop worth it?", ["receiver-placement-decision", "receiver-live-transport"]],
  ["How do I know if my index lost the correction?", ["emeans-retrieval-rebuild"]],
  ["What if checking cannot keep up with new work?", ["verification-load", "verification-arrivals"]],
  ["e-means", ["emeans-retrieval-rebuild"]],
];
const extension = {".js":"application/javascript",".html":"text/html",".css":"text/css",".json":"application/json"};
async function serve(dir) {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, "http://localhost");
    let file = path.resolve(dir, "." + decodeURIComponent(url.pathname));
    if (file !== dir && !file.startsWith(dir + path.sep)) return res.writeHead(403).end();
    if (fs.statSync(file, {throwIfNoEntry:false})?.isDirectory()) file = path.join(file,"index.html");
    if (!fs.statSync(file, {throwIfNoEntry:false})?.isFile()) return res.writeHead(404).end();
    res.writeHead(200, {"Content-Type":extension[path.extname(file)] || "application/octet-stream","Content-Length":fs.statSync(file).size});
    fs.createReadStream(file).on("error", () => res.destroy()).pipe(res);
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  return server;
}
function ranks(dir, records) {
  const engine = vm.runInNewContext(fs.readFileSync(path.join(dir,"products/evidence-registry/knowledge-graph/evidence-search.js"),"utf8") + "\nasiEvidenceSearch");
  const index = engine.index(records);
  return questions.map(([query, keys], i) => {
    const hits = index(query);
    const at = hits.findIndex(hit => keys.includes(hit.record.id.split(":")[1]));
    const record = at < 0 ? null : hits[at].record;
    const target = record && new URL(record.url,"https://example.org/");
    const html = target && fs.readFileSync(path.join(dir, target.pathname), "utf8");
    return {query, top_three:hits.slice(0,3).map(hit => hit.record.id), determining_rank:at < 0 ? null : at + 1,
      destination:record?.url || null, anchor_exists:target ? Boolean(target.hash && html.includes('id="' + decodeURIComponent(target.hash.slice(1)) + '"')) : false,
      scoped_text:record?.limit || null, unsupported_quantity:i === 5};
  });
}
async function cold(browser, origin, query, keys, scope) {
  const ctx = await browser.newContext();
  try {
    await ctx.route(url => url.origin !== origin, route => route.abort());
    const page = await ctx.newPage();
    await page.goto(origin, {waitUntil:"load"});
    return await page.evaluate(async ({query, keys, scope}) => {
      const options = {isCaseSensitive:false, shouldSort:true, minMatchCharLength:2, limit:50};
      let first = null;
      const start = performance.now();
      const capture = items => {
        if (first === null && items.some(item => keys.includes(item.evidenceId?.split(":")[1]))) first = Math.round(performance.now() - start);
      };
      if (typeof asiLookup === "function") {
        capture(await asiLookup(query, scope, options, () => capture(asiSearchResults(query, scope, options))));
        if (asiBookSearchRequest) await asiBookSearchRequest;
      } else {
        await asiReadSearchData();
        capture(asiSearchResults(query, scope, options));
      }
      const resources = performance.getEntriesByType("resource").filter(e => /\/(evidence-search|search)\.json$/.test(e.name));
      return {query, scope:scope || "all", first_applicable_ms:first !== null && first <= 5000 ? first : null,
        indexes:resources.map(e => ({file:e.name.split("/").pop(), body_bytes:e.decodedBodySize}))};
    }, {query,keys,scope});
  } finally { await ctx.close(); }
}
async function main() {
  const browser = await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined});
  const result = {browser:browser.version(), cold_cutoff_ms:5000, sites:[]};
  try {
    for (const location of process.argv.slice(2)) {
      const dir = path.resolve(location);
      const catalog = JSON.parse(fs.readFileSync(path.join(dir, "products/evidence-registry/knowledge-graph/evidence-catalog.json")));
      const server = await serve(dir);
      try {
        const report = {revision:catalog.source_commit, heldout:ranks(dir, catalog.records), cold:[]};
        for (const [q, keys] of probes) for (const scope of ["", "evidence"]) {
          report.cold.push(await cold(browser, "http://127.0.0.1:" + server.address().port, q, keys, scope));
        }
        result.sites.push(report);
      } finally { server.closeAllConnections(); await new Promise(resolve => server.close(resolve)); }
    }
  } finally { await browser.close(); }
  console.log(JSON.stringify(result,null,2));
}
main().catch(error => {console.error(error);process.exitCode=1;});
