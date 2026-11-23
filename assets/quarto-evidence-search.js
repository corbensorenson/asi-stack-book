"use strict";

// This adapter runs with Quarto's pinned Fuse.js and autocomplete renderer.
let asiBookSearch;
let asiBookSearchRequest;
const asiScopes = [
  ["", "All"],
  ["evidence", "Research evidence"],
  ["reading", "Reading"],
  ["history", "History"],
];

function asiSearchScopes(createElement, state, setContext, refresh) {
  const scope = state.context.asiScope || "";
  const select = createElement("select", {
    value: scope,
    "aria-label": "Search scope",
    onChange(event) {
      setContext({ ...state.context, asiScope: event.currentTarget.value, expanded: [] });
      refresh();
    },
  }, asiScopes.map(([value, label]) => createElement("option", {value}, label)));
  const label = createElement("label", {class: "asi-search-scope"}, ["Search scope ", select]);
  if (state.query && state.collections.every(collection => !collection.items.length)) {
    return createElement("div", {}, [label,
      createElement("p", {}, "Try a shorter phrase, a paper name, or an exact evidence ID.")]);
  }
  return label;
}

function asiSetSearchRows(rows) {
  const research = new Map(rows.filter(row => row.evidence && row.evidence_primary)
    .map(row => [row.evidence.id, row]));
  const evidence = asiEvidenceSearch.index([...research.values()].map(row => row.evidence));
  const native = rows.filter(row => !row.evidence);
  const scopes = new Map();
  asiBookSearch = {research, evidence, native, scopes};
}

function asiReadSearchData() {
  if (!asiBookSearchRequest) {
    asiBookSearchRequest = fetch(offsetURL("search.json")).then(response => {
      if (!response.ok) throw new Error("Could not load the book search index");
      return response.json();
    }).then(asiSetSearchRows).catch(error => {
      asiBookSearchRequest = undefined;
      throw error;
    });
  }
  return asiBookSearchRequest;
}

function asiSearchResults(query, scope, options) {
  const {research, evidence, native, scopes} = asiBookSearch;
  let evidenceRows = [];
  if (!scope || scope === "evidence") {
    const floor = query.trim().split(/\s+/).length >= 7 ? 450 : 570;
    const ranked = evidence(query);
    evidenceRows = (scope ? ranked : ranked.filter(hit => hit.score >= floor).slice(0, 3))
      .map(hit => ({...research.get(hit.record.id), match: hit.reason}));
  }
  let bookRows = [];
  if (scope !== "evidence") {
    if (!scopes.has(scope)) {
      const collection = native.filter(row => !scope || row.asi_scope === scope);
      scopes.set(scope, new window.Fuse(collection, kFuseIndexOptions));
    }
    bookRows = scopes.get(scope).search(query, {...options, limit: options.limit * 2}).map(hit => hit.item);
    if (!scope) {
      bookRows = [...bookRows.filter(row => row.asi_scope !== "history"),
        ...bookRows.filter(row => row.asi_scope === "history")];
    }
  }
  const escape = value => value.replace(/[&<>"']/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]);
  return [...evidenceRows, ...bookRows].slice(0, options.limit).map(row => {
    const fragmentAt = row.href.indexOf("#");
    const fragment = fragmentAt < 0 ? "" : row.href.slice(fragmentAt);
    const base = fragmentAt < 0 ? row.href : row.href.slice(0, fragmentAt);
    const queryAt = base.indexOf("?");
    const params = new URLSearchParams(queryAt < 0 ? "" : base.slice(queryAt + 1));
    params.set(kQueryArg, query);
    const href = (queryAt < 0 ? base : base.slice(0, queryAt)) + "?" + params.toString() + fragment;
    const text = row.evidence
      ? '<span class="asi-evidence-result">' + escape(row.evidence.summary || "") + '</span>' +
        '<span class="asi-evidence-limit"><strong>Scope</strong> ' + escape(row.evidence.limit || "") + '</span>' +
        '<span class="asi-evidence-limit">' + escape(row.match) + '</span>'
      : highlightMatch(query, row.text);
    const section = [row.evidence_kind || row.section, row.evidence?.measurement].filter(Boolean).join(" · ");
    return {title: row.title, section, href, text, crumbs: row.crumbs};
  });
}
