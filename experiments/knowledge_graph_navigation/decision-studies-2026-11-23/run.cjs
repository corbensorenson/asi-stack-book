"use strict";

const assert = require("node:assert/strict");
const {createHash} = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const {gunzipSync} = require("node:zlib");
const readline = require("node:readline/promises");

const session = process.argv[4] === "--session";
if ((!session && process.argv.length !== 4) || (session && process.argv.length !== 8)) {
  throw new Error("Use run.cjs TESTED_SITE OUTPUT [--session TASK ordinary|linked SESSION_CODE]");
}
const site = path.resolve(process.argv[2]);
const companion = path.join(site, "products/evidence-registry/knowledge-graph");
const tasksRaw = fs.readFileSync(path.join(__dirname, "tasks.json"));
const tasks = JSON.parse(tasksRaw);
const status = JSON.parse(fs.readFileSync(path.join(site, "status/canonical-public-status.json")));
const manifest = JSON.parse(fs.readFileSync(path.join(companion, "manifest.json")));
function checked(file) {
  const bytes = fs.readFileSync(path.join(companion, file));
  assert.equal(createHash("sha256").update(bytes).digest("hex"), manifest.files[file].sha256, file);
  return bytes;
}

const evidence = JSON.parse(checked(manifest.evidence_catalog));
const graph = JSON.parse(gunzipSync(checked(manifest.archive)));
assert.equal(graph.snapshot_id, manifest.snapshot_id);
assert.equal(evidence.snapshot_id, manifest.snapshot_id);
assert.equal(status.source_commit, manifest.source_commit);
assert.equal(status.source_tree_state, "clean");

const matcher = vm.runInNewContext(checked("evidence-search.js").toString() + "\nasiEvidenceSearch");
const records = new Map(graph.nodes.map(row => [row.id, row]));
for (const row of evidence.records) records.set(row.id, row);
const adjacency = new Map();
for (const edge of graph.edges) {
  for (const [from, to] of [[edge.from, edge.to], [edge.to, edge.from]]) {
    if (!adjacency.has(from)) adjacency.set(from, []);
    adjacency.get(from).push({id: to, predicate: edge.predicate});
  }
}
const rank = matcher.index(evidence.records);
const citable = new Set(evidence.records.map(row => row.id));
const tasksDigest = createHash("sha256").update(tasksRaw).digest("hex");

function packetText(row) {
  return [row.title, row.summary, row.definition, row.limit, row.disposition, ...(row.unmeasured || [])]
    .filter(Boolean).join(" ");
}

// Both instruments use the same conservative disposition rules on opened
// records. The score rubric, target IDs and gold decision are grader-only.
function decision(question, records) {
  if (question.startsWith("Find ") || /^(Which specific|Open the|Start from)/.test(question)) return "locate";
  const text = records.map(packetText).join(" ");
  if (/Atlas/.test(question) && /fell below|stop decision/i.test(text)) return "revise";
  if (/proof transport/.test(question) && /finite.{0,100}(gate|consumer)|one pinned Circle/i.test(text)) return "revise";
  if (/operator time/.test(question)) return "hold";
  if (/80 of 288/.test(question) && /of 288 paired cells.{0,130}each verified 80/i.test(text)) return "accept";
  if (/erased the original effect/.test(question) && /retained the original effect|kept the original effect/i.test(text)) return "revise";
  return "hold";
}

function typedChoices(seen, type) {
  return [...seen].flatMap(from => (adjacency.get(from) || [])
    .filter(edge => (!type || type.includes(edge.predicate)) && citable.has(edge.id) && !seen.has(edge.id))
    .map(edge => ({...edge, from})));
}

function openPacket({id, question, initial, lookup, type}, linked) {
  const start = performance.now();
  const ranked = rank(lookup);
  const scores = new Map(ranked.map(hit => [hit.record.id, hit.score]));
  const seen = new Set(initial);
  const visited = [];
  for (let action = 0; action < 2; action++) {
    const edges = linked ? typedChoices(seen, type) : [];
    edges.sort((a, b) => (scores.get(b.id) || 0) - (scores.get(a.id) || 0) ||
      (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    const candidate = edges[0] || ranked.map(hit => ({id: hit.record.id, predicate: "lookup"}))
      .find(row => !seen.has(row.id));
    if (!candidate) break;
    assert(records.has(candidate.id), candidate.id);
    seen.add(candidate.id);
    visited.push(candidate);
  }
  const observed = [...seen].map(key => records.get(key));
  const disposition = decision(question, observed);
  return {id, initial, records: observed, path: visited, disposition, elapsed_ms: performance.now() - start};
}

function cite(row) {
  if (!row.url) return false;
  const url = new URL(row.url, "https://candidate.invalid/");
  if (url.origin !== "https://candidate.invalid") return false;
  const target = path.resolve(site, "." + url.pathname);
  if (!target.startsWith(site + path.sep) || !fs.existsSync(target)) return false;
  if (!url.hash) return true;
  const html = fs.readFileSync(target, "utf8");
  return html.includes('id="' + decodeURIComponent(url.hash.slice(1)) + '"');
}

function grade(packet, rubric) {
  const choices = packet.records.filter(row => rubric.targets.includes(row.id));
  const claims = choices.map(packetText).join(" ").toLowerCase();
  const facts = rubric.facts.every(value => claims.includes(value.toLowerCase()));
  const scope = rubric.scope.some(value => claims.includes(value.toLowerCase()));
  return {
    exact_target: choices.length > 0,
    decision_ok: packet.disposition === rubric.decision && facts,
    false_promotion: packet.disposition === "accept" && rubric.decision !== "accept",
    missed_contradiction: rubric.contradiction && (packet.disposition !== "revise" || !facts),
    citation: facts && choices.some(cite),
    scoped: scope && facts,
    case_opened: packet.path.some(row => rubric.targets.includes(row.id)),
  };
}

async function manualSession(task, linked, code) {
  assert(/^[a-zA-Z0-9_-]{3,36}$/.test(code), "Use an opaque session code");
  assert(!fs.existsSync(process.argv[3]), "Choose a new output file");
  const consoleInput = readline.createInterface({input: process.stdin, output: process.stdout});
  try {
    await consoleInput.question("Ready to start the timed review? Press Enter. ");
    const start = performance.now();
    let paused = 0;
    let pauses = 0;
    const timedQuestion = async prompt => {
      for (;;) {
        const value = (await consoleInput.question(prompt)).trim();
        if (value.toLowerCase() !== "pause") return value;
        const waitStart = performance.now();
        await consoleInput.question("Press Enter to resume. ");
        paused += performance.now() - waitStart;
        pauses++;
      }
    };
    const seen = new Set(task.initial);
    const show = key => {
      const row = records.get(key);
      console.log("\n" + key + "\n" + packetText(row));
      if (row.url) console.log("Exact citation " + row.url);
    };
    console.log(task.question);
    for (const key of seen) show(key);
    while (seen.size - task.initial.length < 2) {
      const search = rank(task.lookup).filter(hit => !seen.has(hit.record.id)).slice(0, 10);
      const choices = new Map(search.map((hit, i) => [String(i + 1), hit.record.id]));
      console.log("\nRegister search");
      search.forEach((hit, i) => console.log(`${i + 1}. ${records.get(hit.record.id).title}`));
      if (linked) {
        const links = [...new Map(typedChoices(seen).map(edge => [edge.id, edge])).values()].slice(0, 10);
        console.log("\nRelated records");
        links.forEach((edge, i) => {
          const key = "l" + (i + 1);
          choices.set(key, edge.id);
          console.log(`${key}. ${records.get(edge.id).title} (${edge.predicate.replaceAll("_", " ")})`);
        });
      }
      if (!choices.size) break;
      const input = (await timedQuestion("Choose a record number, pause, or finish. ")).toLowerCase();
      if (input === "finish") break;
      const selected = choices.get(input);
      if (!selected) continue;
      seen.add(selected);
      show(selected);
    }
    let disposition;
    const allowed = task.study === "claim" ? ["accept", "revise", "hold"] : ["locate", "hold"];
    while (!allowed.includes(disposition)) {
      disposition = (await timedQuestion(`Disposition (${allowed.join(", ")}). `)).toLowerCase();
    }
    const reason = await timedQuestion("What evidence supports your decision or your abstention? ");
    const scope = await timedQuestion("What limit does the evidence retain? ");
    const citations = await timedQuestion("Cite the exact opened records by ID. ");
    fs.writeFileSync(process.argv[3], JSON.stringify({
      session_code: code, task: task.id, source_commit: status.source_commit, snapshot_id: evidence.snapshot_id,
      tasks_sha256: tasksDigest,
      opened_ids: [...seen], disposition, reason, scope, citations,
      active_review_ms: Math.round(performance.now() - start - paused),
      pauses,
    }, null, 2) + "\n", {flag: "wx"});
  } finally {
    consoleInput.close();
    process.stdin.unref?.();
  }
}

if (session) {
  const task = tasks.find(row => row.id === process.argv[5]);
  assert(task && ["ordinary", "linked"].includes(process.argv[6]), "Choose a known task and comparison");
  manualSession(task, process.argv[6] === "linked", process.argv[7]).catch(error => {
    console.error(error);
    process.exitCode = 1;
  });
} else {
  const packets = [];
  for (const [index, task] of tasks.entries()) {
    const order = index % 2 ? [true, false] : [false, true];
    for (const linked of order) {
      assert(task.initial.every(id => records.has(id)), task.id + " lacks a starting record");
      assert(task.targets.every(id => citable.has(id)), task.id + " lacks a citeable target");
      const packet = openPacket(task, linked);
      // Keep the grader input free of the lookup or relationship used to reach each record.
      const masked = {...packet, path: packet.path.map(row => ({id: row.id}))};
      const result = grade(masked, task);
      packets.push({...packet, comparison: linked ? "linked_register" : "ordinary_register", result});
    }
  }
  fs.writeFileSync(process.argv[3], JSON.stringify({
    source_commit: status.source_commit,
    snapshot_id: evidence.snapshot_id,
    tasks_sha256: tasksDigest,
    wall_time_units: "program milliseconds",
    human_review_time_ms: null,
    packets,
  }, null, 2) + "\n", {flag: "wx"});
}
