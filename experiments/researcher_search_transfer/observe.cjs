// NODE_PATH=ci/browser/node_modules node observe.cjs captures the public interface.
const fs = require("node:fs");
const path = require("node:path");
const {chromium} = require("playwright");
const root = "https://corbensorenson.github.io/asi-stack-book/";

(async () => {
  const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE});
  try {
    const page = await browser.newPage();
    const status = await (await page.request.get(root+"status/canonical-public-status.json?check="+Date.now())).json();
    const queries = JSON.parse(fs.readFileSync(path.join(__dirname,"queries.json")));
    const rows = [];
    for (const [query, target] of queries) {
      await page.goto(root);
      await page.locator("#quarto-search button").first().click();
      await page.locator("input.aa-Input:visible").fill(query);
      // Let the citable records merge with the full native search.
      await page.waitForFunction(() => typeof asiNativeReady !== "undefined" && asiNativeReady, {timeout:30000});
      await page.waitForTimeout(800);
      const links = await page.locator("li.aa-Item a.search-result-link").evaluateAll(items =>
        [...new Set(items.map(a=>{const url=new URL(a.href); return url.pathname+url.hash;}))].slice(0,3));
      rows.push({query,target,links,rank:links.findIndex(link=>link.endsWith("#"+target))+1});
    }
    console.log(JSON.stringify({revision:status.source_commit,rows},null,2));
  } finally {
    await browser.close();
  }
})().catch(err=>{console.error(err);process.exitCode=1;});
