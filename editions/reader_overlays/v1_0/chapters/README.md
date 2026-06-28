# v1.0 Chapter Overlays

Add one JSON file per reader-adapted chapter, usually named after the chapter slug.

Example shape:

```json
{
  "schema_version": "0.1",
  "target_file": "chapters/example-slug.qmd",
  "operations": [
    {
      "id": "example-slug.reader.problem-bridge.v1_0",
      "status": "active",
      "action": "prepend_to_section",
      "section": { "level": 2, "title": "Problem" },
      "content_lines": [
        "Reader-only prose goes here. It should preserve uncertainty and must not add source-derived claims that are not present in the live evidence state."
      ],
      "rationale": "Explain why this belongs in the reader edition rather than the canonical live chapter."
    }
  ]
}
```

Use `status: "planned"` for notes that should validate but not apply yet, and `status: "retired"` for old deltas kept for version history.
