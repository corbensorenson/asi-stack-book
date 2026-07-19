#!/usr/bin/env python3
"""Register the maintained X Article synopsis validator."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_x_article_synopsis.py"
ARTIFACTS = [
    "docs/x_article_synopsis_contract.md",
    "scripts/build_x_article_manifest.py",
    "scripts/validate_x_article_synopsis.py",
    "scripts/register_x_article_synopsis.py",
    "schemas/x_article_manifest.schema.json",
    "editions/x_article/asi_stack_synopsis.md",
    "editions/x_article/claim_crosswalk.json",
    "editions/x_article/asi_stack_synopsis_header.png",
    "editions/x_article/header_provenance.json",
    "editions/x_article/composer_preflight.json",
    "editions/x_article/manifest.json",
    "editions/x_article/previews/desktop.png",
    "editions/x_article/previews/mobile.png",
    "editions/x_article/platform_derivatives/x_header_1200x480.jpg",
    "release_records/2026-07-16-x-article-synopsis-ready-not-published.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    registry["units"] = [u for u in registry["units"] if u.get("script") != SCRIPT]
    used = {u["order"] for u in registry["units"]}
    order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": "Canonical synopsis, 24-claim crosswalk, exact-ratio header/provenance, current official-help check, and real unpublished X desktop/mobile composer previews.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Preserve the <=9,999-word evidence boundary, first-line live-book link, exact 2000x800 header, platform residuals, staleness bindings, and ready-not-published decision.",
        "output_assertions": ["5,222 canonical visible words", "24 crosswalked claims", "exact 2000x800 RGB PNG", "desktop/mobile preview pass", "platform header alt-text limitation retained", "eight mutations reject", "not published"],
        "claim_scope": "Maintained public synopsis derivative and unpublished composer compatibility only.",
        "negative_controls": "validator_owned_eight_x_article_laundering_mutations",
        "negative_control_cases": ["word-limit inflation", "live-link rewrite", "header-ratio rewrite", "false publication", "support promotion", "article digest rewrite", "claim-count erasure", "platform alt-control laundering"],
        "prohibited_inference": "Article quality, composer acceptance, header generation, or preview coverage does not prove book claims, accessibility conformance, public publication, audience reach, platform permanence, safety, SOTA, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_claim_crosswalk_negative_results_header_provenance_composer_platform_residuals_and_publication_boundary",
    })
    required = list(registry["required_artifacts"])
    for path in ARTIFACTS:
        if path not in required: required.append(path)
    registry["units"].sort(key=lambda u: u["order"])
    registry["required_artifacts"] = required
    registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()
