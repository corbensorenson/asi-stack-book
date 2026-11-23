"use strict";

// Match the same citable records in ordinary search and the graph. Document
// frequency comes from the evidence corpus rather than the surrounding book.
const asiEvidenceSearch = (() => {
  const stop = new Set(("a an and are at be by can could did do does for from has have how i if in is it many " +
    "of on or should that the their this to under versus was were what when where which who why will with would " +
    "about any based been being both different given new same than these they those using").split(" "));
  const normalize = value => (value || "").toLowerCase().normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  const terms = value => new Set(normalize(value).split(" ").filter(word => word && !stop.has(word))
    .map(word => word.length > 4 && word.endsWith("s") && !word.endsWith("ss") ? word.slice(0, -1) : word));
  const phrase = (text, query) => (" " + text + " ").includes(" " + query + " ");

  function index(records) {
    const frequency = new Map();
    const documents = records.map(record => {
      const identity = normalize(record.id.split(":").slice(1).join(":"));
      const title = normalize(record.citation_title || record.title);
      const aliases = (record.aliases || []).map(normalize);
      const question = normalize(record.question);
      const primary = terms([identity, title, ...aliases].join(" "));
      const decision = terms([question, record.summary, record.disposition, record.method].join(" "));
      const scope = terms([record.limit, record.measurement, ...(record.unmeasured || [])].join(" "));
      for (const word of new Set([...primary, ...decision, ...scope])) {
        frequency.set(word, (frequency.get(word) || 0) + 1);
      }
      return {record, identity, title, aliases, question, primary, decision, scope};
    });
    const weight = word => 1 + Math.log((documents.length + 1) / ((frequency.get(word) || 0) + 1));

    return function search(query) {
      const normalized = normalize(query);
      const requested = [...terms(normalized)];
      if (!requested.length) return [];
      // Out-of-vocabulary prose cannot discriminate among these records.
      const words = requested.filter(word => frequency.has(word));
      const weights = words.map(weight);
      const total = weights.reduce((sum, value) => sum + value, 0);
      const question = requested.length >= 5;
      return documents.flatMap(document => {
        const {record, identity, title, aliases, primary, decision, scope} = document;
        let score;
        let reason;
        if (query.trim().toLowerCase() === record.id || normalized === identity) {
          score = 1000;
          reason = "Exact evidence ID";
        } else if ([title, document.question, ...aliases].includes(normalized)) {
          score = 900;
          reason = "Exact title, question or alias";
        } else if ([title, ...aliases].some(field => phrase(field, normalized))) {
          score = 800;
          reason = "Phrase in title or alias";
        } else {
          let covered = 0;
          let ranked = 0;
          const matched = [];
          for (const [i, word] of words.entries()) {
            const strength = primary.has(word) ? 1 : decision.has(word) ? 0.8 : scope.has(word) ? 0.65 : 0;
            if (strength) {
              covered += weights[i];
              matched.push(word);
            }
            ranked += weights[i] * strength;
          }
          if (matched.length < Math.min(requested.length, 2)) return [];
          if (covered / total < (question ? 0.30 : 0.56)) return [];
          score = Math.round(650 * ranked / total);
          reason = "Matched terms: " + matched.slice(0, 6).join(", ");
        }
        return [{record, score, reason}];
      }).sort((a, b) => b.score - a.score || Number(Boolean(b.record.featured)) - Number(Boolean(a.record.featured)) ||
        (a.record.id < b.record.id ? -1 : a.record.id > b.record.id ? 1 : 0));
    };
  }
  return Object.freeze({index});
})();
