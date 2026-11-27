"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const {createHash} = require("node:crypto");
const assert = require("node:assert/strict");
const load = name => JSON.parse(fs.readFileSync(path.join(__dirname, name)));
const corpus = load("corpus.json");
const scorer = fs.readFileSync(path.join(__dirname, "../../../assets/evidence-search.js"));
assert.equal(createHash("sha256").update(scorer).digest("hex"), corpus.matcher_sha256,
  "Replay from the pinned book revision to recover the published matcher");
const search = vm.runInNewContext(scorer.toString() + "\nasiEvidenceSearch").index(corpus.records);
const byId = new Map(corpus.records.map(record => [record.id, record]));
function retrieve(question, start, method) {
  const hits = search(question).map(hit => hit.record.id);
  if (method === "identifier") {
    return question.split(/\s+/).filter(id => byId.has(id)).slice(0, 2);
  }
  if (method === "text") return hits.filter(id => id !== start).slice(0, 2);
  const seen = new Set([start]);
  const opened = [];
  for (let i = 0; i < 2; i++) {
    const adjacent = new Set();
    for (const [from, , to] of corpus.edges) {
      if (seen.has(from)) adjacent.add(to);
      if (seen.has(to)) adjacent.add(from);
    }
    const candidates = [...adjacent].filter(id => !seen.has(id) && byId.has(id)).sort();
    const next = hits.find(id => candidates.includes(id)) || candidates[0];
    if (!next) break;
    opened.push(next);
    seen.add(next);
  }
  return opened;
}
const trials = [];
for (const task of load("tasks.json")) {
  for (const identified of [false, true]) {
    const question = task.question + (identified ? " " + task.target : "");
    for (const method of identified ? ["text","graph","identifier"] : ["text","graph"]) {
      const opened = retrieve(question, task.start, method);
      const packet = opened.map(id => {
        const {summary, disposition, limit, url} = byId.get(id);
        return {id, summary, disposition, limit, url};
      });
      const includes = (r, phrases) => phrases.every(phrase => [r.summary,r.disposition,r.limit]
        .join(" ").toLowerCase().includes(phrase.toLowerCase()));
      trials.push({subject:task.subject, question, identified, method, packet,
        decision:packet.some(r => includes(r, task.decision)),
        citation:packet.some(r => r.id===task.target && r.url===task.url && byId.get(r.id).verified_fragment),
        scope:packet.some(r => includes(r, [...task.decision, ...task.scope]))});
    }
  }
}
process.stdout.write(JSON.stringify({snapshot:corpus.snapshot_id,trials}, null, 2) + "\n");
