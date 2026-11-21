"use strict";

const byId = (id) => document.getElementById(id);
const query = byId("query");
const kind = byId("kind");
const results = byId("results");
const more = byId("more");
const record = byId("record");
const recordTitle = byId("record-title");
const status = byId("status");
const selectedClass = "aria-current";
const PAGE_SIZE = 10;
const bookRoot = new URL("../../../", document.baseURI);
const shards = new Map();
const recordKinds = {
  chapter: "Technical chapter", claim: "Claim", claim_record: "Retained claim record",
  concept: "Concept", part: "Part", proof_target: "Proof target", reader_unit: "Reader unit",
  source: "Source", study: "Study", study_run: "Study run", transition: "Evidence transition",
};
const relations = {
  assigned_to: ["Assigned chapters", "Assigned sources"],
  atom: ["Exact claim", "Exact evidence records"],
  contains: ["Chapters", "Part"],
  declares_dependency: ["Declared dependencies", "Records that reference this dependency"],
  declares_proof_target: ["Proof targets", "Declaring chapter"],
  defined_by: ["Defining chapter", "Defined concepts"],
  explained_by: ["Technical explanations", "Concepts explained here"],
  has_concept_claim: ["Concept claims", "Concept"],
  investigates: ["Claim investigated", "Studies"],
  lists_source: ["Listed sources", "Chapters listing this source"],
  maps_source_passage: ["Source mappings", "Chapter mappings"],
  owns_claim: ["Claims", "Owning chapter"],
  proxy_for: ["Claim measured by proxy", "Proxy results"],
  reader_example: ["Reader examples", "Concepts illustrated"],
  related_term: ["Related terms", "Related terms"],
  retained_record_for: ["Claim identity", "Retained records"],
  retains_run: ["Study runs", "Study"],
  subclaim_of: ["Broader claim", "Evidence for bounded subclaims"],
  teaches_chapter: ["Technical owners", "Reader unit"],
};

let manifest;
let catalog;
let catalogById;
let matches = [];
let shown = 0;
let selection;
let requestToken = 0;

function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function localLink(path) {
  if (!path || !/^(appendices|chapters|papers|products|reader)\//.test(path)) return null;
  const url = new URL(path, bookRoot);
  return url.origin === bookRoot.origin && url.pathname.startsWith(bookRoot.pathname) ? url.href : null;
}

function link(text, url) {
  const a = el("a", text);
  a.href = url;
  return a;
}

function nodeLink(id, title) {
  const url = new URL(location.href);
  url.searchParams.set("node", id);
  const a = link(title, url);
  a.dataset.node = id;
  if (id === selection) a.setAttribute(selectedClass, "true");
  return a;
}

function slug(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function label(kindId) {
  return recordKinds[kindId] || kindId.replaceAll("_", " ");
}

function grade(row, value, normalized, tokens) {
  if (row[0] === value) return 5;
  const identity = slug(row[0].slice(row[0].indexOf(":") + 1));
  const title = slug(row[2]);
  if (identity === normalized || title === normalized) return 4;
  if (title.startsWith(normalized + "-")) return 3;
  if (("-" + title + "-").includes("-" + normalized + "-")) return 2;
  const fields = new Set([...(identity.split("-")), ...(title.split("-"))]);
  return tokens.every((token) => fields.has(token)) ? 1 : 0;
}

function showMatches() {
  for (const row of matches.slice(shown, shown + PAGE_SIZE)) {
    const option = el("li");
    const a = nodeLink(row[0], row[2]);
    a.append(el("span", label(catalog.kinds[row[1]]), "result-kind"));
    option.append(a);
    results.append(option);
  }
  shown = Math.min(matches.length, shown + PAGE_SIZE);
  more.hidden = shown >= matches.length;
  status.textContent = matches.length ? `Showing ${shown} of ${matches.length} results.` :
    "No matching records. Try the term alone or choose another record type.";
}

function lookup() {
  const value = query.value.trim();
  const normalized = slug(value);
  results.replaceChildren();
  shown = 0;
  if (value && !normalized) {
    more.hidden = true;
    status.textContent = "Enter a title, term, or record ID.";
    return;
  }
  const tokens = normalized.split("-");
  matches = catalog.records.filter((row) => !kind.value || catalog.kinds[row[1]] === kind.value)
    .map((row) => ({row, score: normalized ? grade(row, value, normalized, tokens) : 1}))
    .filter(({score}) => score)
    .sort((left, right) => right.score - left.score || left.row[2].length - right.row[2].length ||
      left.row[2].localeCompare(right.row[2]) ||
      left.row[0].localeCompare(right.row[0]))
    .map(({row}) => row);
  showMatches();
}

async function readJSON(path) {
  const response = await fetch(path, {credentials: "same-origin"});
  if (!response.ok) throw new Error(`Could not load ${path}`);
  return response.json();
}

function brief(parent, heading, value, className) {
  if (!value || typeof value !== "string") return;
  parent.append(el("h3", heading), el("p", value, className));
}

function provenance(origin, heading = "Record location") {
  const detail = el("details");
  const cite = el("p");
  cite.append(el("code", origin.path), document.createTextNode(" · "), el("code", origin.locator));
  detail.append(el("summary", heading), cite);
  if (!manifest.worktree && /^[0-9a-f]{40}$/.test(manifest.source_commit) &&
      /^[a-zA-Z0-9_.\/-]+$/.test(origin.path) && !origin.path.startsWith("/") && !origin.path.includes("..")) {
    detail.append(link("Open source record", `https://github.com/corbensorenson/asi-stack-book/blob/${manifest.source_commit}/${origin.path}`));
  }
  return detail;
}

function passageList(parent, passages) {
  if (!passages || !passages.length) return;
  const detail = el("details");
  const list = el("ul");
  for (const path of passages) {
    const row = el("li");
    if (/^https:\/\//i.test(path)) {
      row.append(link(path, path));
    } else if (!manifest.worktree && /^[0-9a-f]{40}$/.test(manifest.source_commit) &&
               /^sources\/source_notes\/[a-zA-Z0-9_-]+\.md(?:#[^\s]+)?$/.test(path)) {
      row.append(link(path, `https://github.com/corbensorenson/asi-stack-book/blob/${manifest.source_commit}/${path}`));
    } else {
      row.append(el("code", path));
    }
    list.append(row);
  }
  detail.append(el("summary", "Reviewed passage references"), list);
  parent.append(detail);
}

function scopeDetails(scope) {
  const details = el("details");
  const list = el("dl");
  for (const [key, value] of Object.entries(scope)) {
    if (typeof value === "string" || Array.isArray(value)) {
      list.append(el("dt", key.replaceAll("_", " ")), el("dd", Array.isArray(value) ? value.join(", ") : value));
    }
  }
  details.append(el("summary", "Scope and maximum inference"), list);
  return details;
}

function renderGroup(group, open) {
  const pane = el("details");
  pane.open = open;
  const labels = relations[group.predicate] || [group.predicate, group.predicate];
  pane.append(el("summary", `${labels[group.direction === "out" ? 0 : 1]} (${group.total})`));
  const list = el("ul");
  for (const item of group.neighbors) {
    const row = el("li");
    row.append(nodeLink(item.id, item.title));
    const q = item.qualifiers;
    if (q.mapped_support) row.append(el("p", q.mapped_support));
    if (q.limit) row.append(el("p", q.limit, "limit"));
    if (typeof q.scope === "string") row.append(el("p", q.scope));
    if (q.parent_support_state_effect) {
      row.append(el("p", `Parent support effect · ${q.parent_support_state_effect}`, "metadata"));
    }
    if (q.scope && typeof q.scope === "object") row.append(scopeDetails(q.scope));
    if (q.url && localLink(q.url)) row.append(link("Open the reader example", localLink(q.url)));
    if (q.review_state) row.append(el("p", `Passage review · ${q.review_state}`, "metadata"));
    passageList(row, q.passages);
    row.append(provenance(item.origin, "Relationship source"));
    list.append(row);
  }
  pane.append(list);
  const omitted = group.total - group.neighbors.length;
  if (omitted) {
    pane.append(el("p", `${omitted} more in the `, "metadata"));
    pane.lastChild.append(link("complete graph", "graph.json.gz"), document.createTextNode("."));
  }
  return pane;
}

function renderRecord(packet) {
  const {node, relations: groups} = packet;
  recordTitle.textContent = node.title;
  record.replaceChildren();
  const values = [label(node.kind), node.record_version === "retained" ? "Retained record" : null,
    node.state || null, node.status || null].filter(Boolean);
  record.append(el("p", values.join(" · "), "metadata"));
  const id = el("p");
  id.append(el("code", node.id));
  record.append(id);
  if (localLink(node.url)) record.append(link("Open in the book", localLink(node.url)));
  if (node.primary_url && /^https?:\/\//i.test(node.primary_url)) {
    const source = el("p");
    source.append(link("Open the primary source", node.primary_url));
    record.append(source);
  }
  brief(record, "Definition", node.definition);
  brief(record, "Citation", node.citation_label);
  if (node.kind === "study") brief(record, "Research question", node.question);
  brief(record, "Reported result", node.summary);
  brief(record, "Evidence limit", node.limit, "limit");
  brief(record, "Disposition", node.disposition);
  brief(record, "Lean module", node.module);
  if (typeof node.scope === "string") brief(record, "Scope", node.scope);
  else if (node.scope) record.append(scopeDetails(node.scope));
  record.append(provenance(node.origin));
  if (node.publication_origin) record.append(provenance(node.publication_origin, "Paper library record"));
  if (node.implementation_origin) record.append(provenance(node.implementation_origin, "Lean implementation"));
  if (node.transition_origin) record.append(provenance(node.transition_origin, "Transition record"));
  if (node.result_sha256 || node.record_sha256) {
    const pinned = el("details");
    pinned.append(el("summary", node.result_sha256 ? "Pinned study artifacts" : "Transition record digest"));
    for (const [label, value] of [["Source commit", node.source_commit], ["Protocol SHA-256", node.protocol_sha256],
                                  ["Result SHA-256", node.result_sha256], ["Record SHA-256", node.record_sha256]]) {
      if (!value) continue;
      const line = el("p", label + " ");
      line.append(el("code", value));
      pinned.append(line);
    }
    record.append(pinned);
  }
  if (groups.length) {
    const region = el("section", undefined, "relations");
    region.append(el("h3", "Relationships"));
    for (const [index, group] of groups.entries()) region.append(renderGroup(group, index < 2));
    record.append(region);
  }
  if (packet.unresolved) record.append(el("p", `${packet.unresolved} unresolved references in the source record.`, "metadata"));
}

function loadShard(key) {
  if (!shards.has(key)) {
    const request = readJSON(`nodes/${key}.json`).then((data) => {
      if (data.snapshot_id !== manifest.snapshot_id) throw new Error("The graph changed during lookup");
      return data;
    }).catch((error) => {
      shards.delete(key);
      throw error;
    });
    shards.set(key, request);
    if (shards.size > 12) shards.delete(shards.keys().next().value);
  }
  return shards.get(key);
}

async function openRecord(id, focus) {
  const token = ++requestToken;
  selection = id;
  const row = catalogById.get(id);
  if (!row) {
    recordTitle.textContent = "Record unavailable";
    record.replaceChildren(el("p", "Search for a title or try an example starting point."));
    return;
  }
  for (const a of results.querySelectorAll("a")) {
    if (a.dataset.node === id) a.setAttribute(selectedClass, "true");
    else a.removeAttribute(selectedClass);
  }
  recordTitle.textContent = "Loading record…";
  record.replaceChildren();
  try {
    const data = await loadShard(row[3]);
    if (token !== requestToken) return;
    renderRecord(data.records[id]);
  } catch (error) {
    if (token !== requestToken) return;
    recordTitle.textContent = "Record could not load";
    record.replaceChildren(el("p", `${error.message}. Reload the companion or download the complete graph.`));
  }
  if (focus) recordTitle.focus();
}

function applyLocation() {
  const params = new URL(location.href).searchParams;
  query.value = params.get("q") || "";
  kind.value = params.get("kind") || "";
  if (params.has("q") || kind.value) lookup();
  else {
    results.replaceChildren();
    more.hidden = true;
    status.textContent = "Choose an example or search for a record.";
  }
  openRecord(params.get("node") || "concept:receipt", false);
}

async function start() {
  try {
    [manifest, catalog] = await Promise.all([readJSON("manifest.json"), readJSON("search.json")]);
    if (catalog.snapshot_id !== manifest.snapshot_id) throw new Error("The search index and graph have different revisions");
    catalogById = new Map(catalog.records.map((row) => [row[0], row]));
    for (const name of catalog.kinds) {
      const option = el("option", label(name));
      option.value = name;
      kind.append(option);
    }
    byId("snapshot").textContent = `${catalog.records.length.toLocaleString()} records · ${manifest.worktree ? "Local snapshot" : "Source commit"} ${manifest.source_commit.slice(0, 8)}`;
    byId("lookup").addEventListener("submit", (event) => {
      event.preventDefault();
      const url = new URL(location.href);
      url.searchParams.set("q", query.value.trim());
      if (kind.value) url.searchParams.set("kind", kind.value);
      else url.searchParams.delete("kind");
      history.pushState(null, "", url);
      lookup();
    });
    more.addEventListener("click", showMatches);
    window.addEventListener("popstate", applyLocation);
    document.addEventListener("click", (event) => {
      const target = event.target.closest("a[data-node], a[data-example]");
      if (!target || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const id = target.dataset.node || target.dataset.example;
      const url = new URL(location.href);
      url.searchParams.set("node", id);
      history.pushState(null, "", url);
      openRecord(id, true);
    });
    applyLocation();
  } catch (error) {
    status.textContent = `${error.message}. Reload this page or use the glossary and full graph download.`;
  }
}

start();
