"use strict";

document.addEventListener("click", async event => {
  const button = event.target.closest("button[data-copy-citation]");
  if (!button) return;
  const citation = button.dataset.copyCitation;
  const feedback = button.nextElementSibling;
  try {
    await navigator.clipboard.writeText(citation);
    feedback.textContent = "Citation copied.";
  } catch {
    let field = feedback.nextElementSibling;
    if (!field) {
      field = document.createElement("textarea");
      field.readOnly = true;
      field.rows = 5;
      field.setAttribute("aria-label", "Citation text");
      feedback.after(field);
    }
    field.value = citation;
    field.focus();
    field.select();
    feedback.textContent = "Citation selected for copying.";
  }
});
