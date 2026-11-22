"use strict";

const drawers = [...document.querySelectorAll("[data-study-cases]")];

function showLinkedCase() {
  let id;
  try {
    id = decodeURIComponent(location.hash.slice(1));
  } catch {
    return;
  }
  const target = document.getElementById(id);
  const drawer = target?.closest("[data-study-cases]");
  if (!drawer) return;
  drawer.open = true;
  if (target.hidden) {
    const filter = drawer.querySelector("select");
    filter.value = "all";
    filter.dispatchEvent(new Event("change"));
  }
  requestAnimationFrame(() => target.scrollIntoView({block: "nearest"}));
}

for (const drawer of drawers) {
  const rows = [...drawer.querySelectorAll("tbody tr")];
  const filter = drawer.querySelector("select");
  const status = drawer.querySelector("[data-case-count]");
  drawer.open = false;
  filter.closest("label").hidden = false;
  function applyFilter() {
    let shown = 0;
    for (const row of rows) {
      row.hidden = filter.value !== "all" && !row.hasAttribute("data-" + filter.value);
      if (!row.hidden) shown++;
    }
    status.textContent = `Showing ${shown} of ${rows.length} paired cases.`;
  }
  filter.addEventListener("change", applyFilter);
}

window.addEventListener("hashchange", showLinkedCase);
showLinkedCase();
