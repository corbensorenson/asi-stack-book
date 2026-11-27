"use strict";

// Use the authored records at each revision. Their dispositions are plain text;
// the rendered study summaries can also contain metrics computed from a pinned run.
function describeCitation(id, passages, studies) {
  const [kind, key] = id.split(":");
  if (kind === "evidence_passage") {
    const p = passages.find(row => row.id === key);
    if (!p) return null;
    const successor = passages.find(row => row.links.some(link => link.predicate === "supersedes_decision" && link.target === id));
    return {id, decision:p.disposition || p.summary, scope:p.limit, detail:p.summary, title:p.title, url:p.url,
      method:p.method, links:p.links, locators:p.locators, aliases:p.aliases, outside:p.outside_question, successor:successor?.id,
      source:"products/evidence_passages.json"};
  }
  const study = studies.studies.find(row => row.id === key);
  const run = studies.runs.find(row => row.id === (kind === "study" ? study?.featured_run : key));
  if (!run) return null;
  return {id, title:kind === "study" ? study.title : run.title, decision:run.disposition, scope:run.limit,
    detail:run.method, digest:run.result_sha256, protocol:run.protocol_sha256, run:run.id, source:run.result,
    followups:studies.runs.filter(row => row.follow_up_to === run.id).map(row => row.id).sort(),
    aliases:run.aliases, outside:run.outside_question,
    url:"products/evidence-registry/study-" + run.study + ".html#run-" + run.id};
}

function compareCitation(id, prior, current) {
  const before = describeCitation(id, prior.passages, prior.studies);
  const after = describeCitation(id, current.passages, current.studies);
  const result = {before, after};
  if (!before) return {...result, meaning:"Record absent from saved revision"};
  if (!after) return {...result, meaning:"Record absent from current revision"};
  if (after.successor) {
    const successor = describeCitation("evidence_passage:" + after.successor, current.passages, current.studies);
    return {...result, successor, meaning:before.successor === after.successor
      ? "Correction already recorded at the saved revision" : "A correction superseded the saved decision"};
  }
  if (after.run !== before.run) {
    // A change in which run is featured alone does not prove a correction or a follow-up.
    const seen = new Set();
    let predecessor = after.run;
    while (predecessor && !seen.has(predecessor)) {
      seen.add(predecessor);
      predecessor = current.studies.runs.find(row => row.id === predecessor)?.follow_up_to;
      if (predecessor === before.run) return {...result, meaning:"Follow-up under different or additional conditions"};
    }
    return {...result, meaning:"Featured comparison changed; inspect both studies"};
  }
  const substantive = ["decision","scope","detail","digest","protocol","method"];
  if (substantive.some(key => before[key] !== after[key])) {
    return {...result, meaning:"Evidence or claim text changed; inspect the two versions"};
  }
  const added = (after.followups || []).filter(key => !before.followups.includes(key));
  if (added.length) return {...result, followups:added.map(key =>
    describeCitation("study_run:" + key, current.passages, current.studies)),
    meaning:"A later run followed up the saved result"};
  if (JSON.stringify(after.links) !== JSON.stringify(before.links)) {
    return {...result, meaning:"Evidence relationships changed; inspect the linked records"};
  }
  const same = JSON.stringify(before) === JSON.stringify(after);
  return {...result, meaning:same ? "Same recorded decision and presentation" : "Editorial or navigation change; decision and evidence fields match"};
}

if (typeof document !== "undefined") {
  const form = document.getElementById("history-form");
  const output = document.getElementById("history-output");
  const root = "https://github.com/corbensorenson/asi-stack-book/blob/";
  const initial = new URLSearchParams(location.search);
  const get = async url => {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Could not read revision evidence (" + response.status + ").");
    return response.json();
  };
  let generation = 0;
  async function show() {
    const request = ++generation;
    const id = form.elements.record.value.trim(), revision = form.elements.revision.value.trim().toLowerCase();
    output.textContent = "Loading revision…";
    try {
      if (!/^(study|study_run|evidence_passage):[a-z0-9-]+$/.test(id) || !/^[a-f0-9]{40}$/.test(revision))
        throw new Error("Enter a passage, study or run ID and a full 40-character book revision.");
      const current = await get("citation-current.json");
      let prior = current;
      if (current.revision !== revision) {
        if (current.archived.includes(revision)) prior = await get("citation-history/" + revision + ".json");
        else {
          const relation = await get("https://api.github.com/repos/corbensorenson/asi-stack-book/compare/" + revision + "..." + current.revision);
          if (!["ahead", "identical"].includes(relation.status)) throw new Error("The saved revision is outside this book revision’s ancestry.");
          const base = "https://raw.githubusercontent.com/corbensorenson/asi-stack-book/" + revision + "/products/";
          prior = id.startsWith("evidence_passage:") ? {passages:await get(base + "evidence_passages.json")} : {studies:await get(base + "research_studies.json")};
        }
      }
      if (request !== generation) return;
      const change = compareCitation(id, prior, current);
      output.replaceChildren();
      const heading = document.createElement("h2"); heading.textContent = change.meaning; output.append(heading);
      for (const [label, row, sha] of [["Saved record", change.before, revision], ["Current record", change.after, current.revision], ["Governing correction", change.successor, current.revision], ...(change.followups || []).map(row => ["Later run", row, current.revision])]) {
        if (!row) continue;
        const h = document.createElement("h3"); h.textContent = label + " · " + row.title; output.append(h);
        for (const value of [row.decision, row.scope, row.detail === row.decision ? null : row.detail, sha]) {
          if (value) {const p = document.createElement("p"); p.textContent = value; output.append(p);}
        }
        const link = document.createElement("a"); link.href = root + sha + "/" + row.source; link.textContent = "Revision-pinned source"; output.append(link);
        if (label !== "Saved record") {
          const live = document.createElement("a"); live.href = "../../" + row.url; live.textContent = "Open the cited passage"; output.append(" · ",live);
        }
      }
      const url = new URL(location.href); url.search = new URLSearchParams({record:id,revision}).toString(); history.replaceState(null,"",url);
    } catch (error) { if (generation === request) output.textContent = error.message; }
  }
  form.elements.record.value = initial.get("record") || "study:crossed-receiver";
  form.elements.revision.value = initial.get("revision") || form.elements.revision.defaultValue;
  form.addEventListener("submit", event => {event.preventDefault(); show();});
  if (initial.has("record") && initial.has("revision")) show();
}
