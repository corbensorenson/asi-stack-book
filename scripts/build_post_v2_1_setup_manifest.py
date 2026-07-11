#!/usr/bin/env python3
"""Build the outcome-unopened post-v2.1 executable setup manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/post_v2_1_evidence_program/setup_manifest.json"
FILES = [
    "scripts/post_v2_1_p1_observer.py",
    "scripts/run_post_v2_1_p1.py",
    "scripts/post_v2_1_p2_evaluator.py",
    "scripts/run_post_v2_1_p2.py",
    "scripts/post_v2_1_p3_observer.py",
    "scripts/run_post_v2_1_p3.py",
    "scripts/build_post_v2_1_setup_manifest.py",
    "scripts/validate_post_v2_1_evidence_setup.py",
    "schemas/post_v2_1_evidence_setup.schema.json",
]


def file_sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def build(state: str, setup_commit: str | None) -> dict:
    frozen = state == "frozen"
    return {
        "schema_version": "asi_stack.post_v2_1_evidence_setup.v0",
        "setup_id": "post-v2-1-three-program-executable-setup-2026-07-11",
        "state": "frozen_before_outcome_runs" if frozen else "implementations_installed_setup_commit_pending",
        "parent_input_commit": "52925c426",
        "setup_commit": setup_commit if frozen else None,
        "amendment_ref": "experiments/post_v2_1_evidence_program/amendments/preregistration_inputs_v1.json",
        "preregistration_ref": "experiments/post_v2_1_evidence_program/preregistration.json",
        "runtime_authority_ref": "experiments/post_v2_1_evidence_program/runtime_eligibility_disposition.json",
        "source_gap_scan_ref": "docs/post_v2_1_focused_source_gap_scan.md",
        "implementation_files": [{"path": path, "sha256": file_sha(path)} for path in FILES],
        "programs": [
            {
                "priority": "P1", "runner": "scripts/run_post_v2_1_p1.py", "observer": "scripts/post_v2_1_p1_observer.py",
                "execution_order": ["development", "calibration", "test"],
                "phase_calls": {"development": 12, "calibration": 24, "test": 36}, "model_calls": 72,
                "generated_token_ceiling": 18360, "seeds": [1701, 2903],
                "outcome_outputs": ["experiments/post_v2_1_evidence_program/p1/results/development.json", "experiments/post_v2_1_evidence_program/p1/results/calibration.json", "experiments/post_v2_1_evidence_program/p1/results/test.json"],
            },
            {
                "priority": "P2", "runner": "scripts/run_post_v2_1_p2.py", "evaluator": "scripts/post_v2_1_p2_evaluator.py",
                "execution_order": ["validation", "test"], "phase_calls": {"validation": 20, "test": 240},
                "model_calls": 260, "generated_token_ceiling": 41600, "seeds": [1701],
                "outcome_outputs": ["experiments/post_v2_1_evidence_program/p2/results/validation.json", "experiments/post_v2_1_evidence_program/p2/results/test.json"],
            },
            {
                "priority": "P3", "runner": "scripts/run_post_v2_1_p3.py", "observer": "scripts/post_v2_1_p3_observer.py",
                "execution_order": ["three_seed_five_arm_campaign"], "model_calls": 0, "generated_token_ceiling": 0,
                "seeds": [1701, 2903, 4307], "state_surfaces": 24,
                "outcome_outputs": ["experiments/post_v2_1_evidence_program/p3/results/result.json"],
            },
        ],
        "role_interfaces": {
            "P1_proposer": "pinned MLX model in run_post_v2_1_p1.py",
            "P1_effect_observer": "separate post_v2_1_p1_observer.py subprocess",
            "P2_candidate_generator": "pinned MLX model in run_post_v2_1_p2.py",
            "P2_evaluator": "separate post_v2_1_p2_evaluator.py subprocess with evaluator-only answer keys",
            "P3_trainer": "run_post_v2_1_p3.py",
            "P3_state_observer": "separate post_v2_1_p3_observer.py subprocess",
            "promotion_authority": "post-run disposition validator not present in any proposer/trainer",
        },
        "execution_guard": {
            "outcomes_must_be_absent_at_freeze": True,
            "runners_require_final_preregistration_state": True,
            "overwrite_or_retry_flag": False,
            "network_after_freeze": False,
            "model_snapshot_local_only": True,
            "hidden_chain_of_thought_retained": False,
            "external_service_spend_usd": 0,
        },
        "preflight_commands": [
            "python3 scripts/run_post_v2_1_p1.py --preflight",
            "python3 scripts/run_post_v2_1_p2.py --preflight",
            "python3 scripts/run_post_v2_1_p3.py --preflight",
        ],
        "combined_budget": {"model_calls": 332, "generated_tokens": 59960, "global_call_ceiling": 340, "global_token_ceiling": 60000},
        "support_state_effect": "none_before_accepted_post_run_dispositions",
        "non_claims": [
            "Installed runners and passing preflights are not empirical outcomes.",
            "Separate local processes are implementation separation, not external independence.",
            "The criterion evaluators are bounded to the synthetic registered tasks.",
            "No support state or residual closes through setup binding."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", choices=("installed", "frozen"), default="installed")
    parser.add_argument("--setup-commit")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.state == "frozen" and (not args.setup_commit or len(args.setup_commit) != 40):
        raise SystemExit("frozen state requires the exact 40-character setup commit")
    expected = build(args.state, args.setup_commit)
    if args.check:
        if not OUTPUT.exists() or json.loads(OUTPUT.read_text()) != expected:
            raise SystemExit("post-v2.1 setup manifest drifted")
        print("Post-v2.1 setup manifest is deterministic and current.")
        return
    OUTPUT.write_text(json.dumps(expected, indent=2) + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} state={expected['state']}")


if __name__ == "__main__":
    main()
