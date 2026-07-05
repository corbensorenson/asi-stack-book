#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

const ROOT = path.resolve(__dirname, "..");

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
    // Continue to known runtime module roots.
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

async function main() {
  const htmlPath = process.argv[2];
  if (!htmlPath) throw new Error("usage: extract_rendered_mermaid_svgs.js <html-path>");
  const playwright = loadPlaywright();
  if (!playwright) throw new Error("Playwright is not available in known module roots.");

  const browser = await launchChromium(playwright);
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1200 } });
    await page.goto(pathToFileURL(path.resolve(htmlPath)).href, {
      waitUntil: "networkidle",
      timeout: 60000,
    });
    await page.waitForFunction(
      () => document.querySelectorAll('svg[id^="mermaid-"], pre.mermaid svg, .mermaid svg').length > 0,
      { timeout: 60000 }
    );
    const svgs = await page.evaluate(() =>
      Array.from(document.querySelectorAll('svg[id^="mermaid-"], pre.mermaid svg, .mermaid svg')).map((svg) =>
        svg.outerHTML
      )
    );
    process.stdout.write(JSON.stringify(svgs));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
