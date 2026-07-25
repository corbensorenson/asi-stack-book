#!/usr/bin/env python3
"""Bind the maintenance-status schema to the superseding no-deferral snapshot."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
SCHEMA = ROOT / "schemas/post_v2_3_maintenance_transfer_and_publication_status.schema.json"


def main() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    properties = schema["properties"]
    required = schema["required"]
    if "no_deferral_manuscript_admission" not in required:
        required.append("no_deferral_manuscript_admission")
    properties["no_deferral_manuscript_admission"] = {
        "const": status["no_deferral_manuscript_admission"]
    }
    properties["round_16_evidence_first_amendment"] = {
        "const": status["round_16_evidence_first_amendment"]
    }
    properties["post_round_18_depth_and_coverage_amendment"] = {
        "const": status["post_round_18_depth_and_coverage_amendment"]
    }
    properties["activation_truth"] = {"const": status["activation_truth"]}
    properties["negative_result_rehabilitation"] = {
        "const": status["negative_result_rehabilitation"]
    }
    quality_schema = properties["quality_uplift_program"]
    quality_schema["properties"]["structural_completeness_tranche"] = {
        "const": status["quality_uplift_program"]["structural_completeness_tranche"]
    }
    readiness_schema = properties["execution_readiness"]
    readiness_schema["properties"]["structural_admission_freeze"] = {
        "const": status["execution_readiness"]["structural_admission_freeze"]
    }
    SCHEMA.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Bound maintenance schema to the current no-deferral status snapshot.")


if __name__ == "__main__":
    main()
