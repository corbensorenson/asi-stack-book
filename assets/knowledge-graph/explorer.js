"use strict";

const byId = (id) => document.getElementById(id);
const query = byId("query");
const kind = byId("kind");
const results = byId("results");
const resultsPanel = byId("results-panel");
const more = byId("more");
const record = byId("record");
const recordTitle = byId("record-title");
const status = byId("status");
const selectedClass = "aria-current";
const PAGE_SIZE = 10;
const bookRoot = new URL("../../../", document.baseURI);
const packets = new Map();
const stopWords = new Set(
  ("a an are about can did does find for how i in is it of on or paper show study the to used was were " +
   "what when where which with").split(" ")
);
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

function terms(normalized) {
  return new Set(normalized.split("-").filter(word => word && !stopWords.has(word))
    .map(word => word.length > 4 && word.endsWith("s") ? word.slice(0, -1) : word));
}

function grade(row, value, normalized, words) {
  if (row[0] === value) return 1000;
  const identity = slug(row[0].slice(row[0].indexOf(":") + 1));
  const title = slug(row[2]);
  const alias = row[4] || "";
  if (identity === normalized || title === normalized) return 900;
  if (alias === normalized) return 870;
  if (title.startsWith(normalized + "-")) return 830;
  if (("-" + title + "-").includes("-" + normalized + "-")) return 800;
  if (alias.length >= 3 && ("-" + normalized + "-").includes("-" + alias + "-")) return 780;
  const primary = terms([identity, title, alias].join("-"));
  const context = terms(row[5] || "");
  let direct = 0;
  let covered = 0;
  for (const word of words) {
    if (primary.has(word)) direct++;
    if (primary.has(word) || context.has(word)) covered++;
  }
  if (!covered || covered * 100 < words.size * 55) return 0;
  return Math.floor(200 * covered / words.size) + Math.floor(140 * direct / words.size);
}

function rankMatches(items, value, rowFor) {
  const normalized = slug(value);
  const words = terms(normalized);
  return items.map(item => {
    const row = rowFor(item);
    return {item, row, score: normalized ? grade(row, value, normalized, words) : 1};
  }).filter(({score}) => score)
    .sort((left, right) => right.score - left.score || left.row[2].length - right.row[2].length ||
      (left.row[0] < right.row[0] ? -1 : left.row[0] > right.row[0] ? 1 : 0))
    .map(({item}) => item);
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
  resultsPanel.hidden = !matches.length;
  more.hidden = shown >= matches.length;
  status.textContent = matches.length ? `Showing ${shown} of ${matches.length} results.` :
    "No matching records. Try a shorter phrase, a paper name, or a record ID.";
}

function lookup() {
  const value = query.value.trim();
  const normalized = slug(value);
  results.replaceChildren();
  resultsPanel.hidden = true;
  shown = 0;
  if (value && !normalized) {
    more.hidden = true;
    status.textContent = "Enter a title, term, or record ID.";
    return;
  }
  const candidates = catalog.records.filter(row => !kind.value || catalog.kinds[row[1]] === kind.value);
  matches = rankMatches(candidates, value, row => row);
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
    const line = /^line:(\d+)$/.exec(origin.locator);
    const fragment = line ? "#L" + line[1] : "";
    detail.append(link("Open source record", `https://github.com/corbensorenson/asi-stack-book/blob/${manifest.source_commit}/${origin.path}${fragment}`));
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

function renderRelation(item) {
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
  return row;
}

function pageAt([file, offset]) {
  return packetFile(`relationships/${file}.json`).then(data => {
    if (!Array.isArray(data.pages[offset])) throw new Error("This relationship page is unavailable");
    return data.pages[offset];
  });
}

function pager(list, render, addresses, total, label = "Show more links") {
  const controls = el("div", undefined, "relationship-pager");
  const state = el("p", `Showing ${list.children.length} of ${total}`, "metadata");
  state.setAttribute("role", "status");
  const button = el("button", label, "secondary");
  button.type = "button";
  controls.append(button, state);
  let position = 0;
  button.addEventListener("click", async event => {
    button.disabled = true;
    try {
      const rows = (await pageAt(addresses[position])).map(render);
      list.append(...rows);
      position++;
      state.textContent = `Showing ${list.children.length} of ${total}`;
      if (position === addresses.length) {
        button.hidden = true;
        if (!event.detail) {
          const destination = rows[0]?.querySelector("a") || state;
          if (destination === state) state.tabIndex = -1;
          destination.focus();
        }
      }
    } catch {
      state.textContent = "More links could not load. Try again or reload the graph.";
    } finally {
      button.disabled = false;
    }
  });
  return controls;
}

function groupFilter(group, label, rows, controls) {
  const form = el("form", undefined, "relationship-filter");
  const field = el("input");
  field.type = "search";
  field.maxLength = 180;
  field.setAttribute("aria-label", `Filter ${label.toLowerCase()}`);
  field.placeholder = "Title, name, or ID";
  const submit = el("button", "Filter links", "secondary");
  const reset = el("button", "Clear", "secondary");
  reset.type = "reset";
  reset.hidden = true;
  form.append(field, submit, reset);
  const state = el("p", undefined, "metadata");
  state.setAttribute("role", "status");
  const list = el("ul");
  let token = 0;

  function showPreview() {
    token++;
    list.replaceChildren();
    state.textContent = "";
    reset.hidden = true;
    rows.hidden = controls.hidden = false;
  }

  form.addEventListener("reset", () => {
    showPreview();
    field.focus();
  });
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const value = field.value.trim();
    if (!slug(value)) {
      showPreview();
      return;
    }
    const request = ++token;
    rows.hidden = controls.hidden = false;
    list.replaceChildren();
    reset.hidden = false;
    state.textContent = "Finding related records…";
    try {
      const members = await pageAt(group.member_index);
      const ranked = rankMatches(members.map((_, index) => index), value, index => catalog.records[members[index]]);
      const shown = ranked.slice(0, 6);
      const previews = group.neighbors.length;
      const pageSize = manifest.limits.relationship_page_size;
      const hits = await Promise.all(shown.map(async index => {
        if (index < previews) return group.neighbors[index];
        const offset = index - previews;
        const page = await pageAt(group.pages[Math.floor(offset / pageSize)]);
        return page[offset % pageSize];
      }));
      if (request !== token) return;
      list.append(...hits.map(renderRelation));
      rows.hidden = controls.hidden = true;
      state.textContent = ranked.length ? `Showing ${shown.length} of ${ranked.length} matching links.` :
        "No links in this group match. Try a shorter title or an exact ID.";
    } catch {
      if (request === token) state.textContent = "This filter could not load. Try again or reload the graph.";
    }
  });
  return [form, state, list];
}

function renderGroup(group, open) {
  const pane = el("details");
  pane.open = open;
  const labels = relations[group.predicate] || [group.predicate, group.predicate];
  const label = labels[group.direction === "out" ? 0 : 1];
  pane.append(el("summary", `${label} (${group.total})`));
  const list = el("ul");
  list.append(...group.neighbors.map(renderRelation));
  if (group.pages) {
    const controls = pager(list, renderRelation, group.pages, group.total);
    if (group.member_index) pane.append(...groupFilter(group, label, list, controls));
    pane.append(list, controls);
  } else {
    pane.append(list);
  }
  return pane;
}

function renderGap(gap) {
  const row = el("li");
  row.append(el("code", gap.target_ref), el("p", gap.reason), provenance(gap.origin, "Reference location"));
  return row;
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
  if (node.kind === "study") brief(record, "Current decision", node.disposition);
  brief(record, "Reported result", node.summary);
  brief(record, "Evidence limit", node.limit, "limit");
  if (node.kind === "study") brief(record, "What would change the decision", node.change);
  else brief(record, "Disposition", node.disposition);
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
  if (packet.unresolved_pages) {
    const unresolved = el("details", undefined, "unresolved");
    const list = el("ul");
    unresolved.append(el("summary", `Unresolved references (${packet.unresolved})`),
      el("p", "These references have no confirmed destination in this snapshot."), list,
      pager(list, renderGap, packet.unresolved_pages, packet.unresolved, "Load references"));
    record.append(unresolved);
  }
}

function packetFile(path) {
  if (!packets.has(path)) {
    const request = readJSON(path).then((data) => {
      if (data.snapshot_id !== manifest.snapshot_id) throw new Error("The graph changed during lookup");
      return data;
    }).catch((error) => {
      packets.delete(path);
      throw error;
    });
    packets.set(path, request);
    if (packets.size > 12) packets.delete(packets.keys().next().value);
  }
  return packets.get(path);
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
    const data = await packetFile(`nodes/${row[3]}.json`);
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
    resultsPanel.hidden = true;
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
      if (url.href !== location.href) history.pushState(null, "", url);
      lookup();
    });
    kind.addEventListener("change", () => byId("lookup").requestSubmit());
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
