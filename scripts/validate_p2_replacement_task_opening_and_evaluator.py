#!/usr/bin/env python3
"""Validate P2 rank-one task opening and independent evaluator calibration."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
OPENING = ROOT / "evidence_quality/p2_replacement_task_opening.json"
OPENING_SCHEMA = ROOT / "schemas/p2_replacement_task_opening.schema.json"
CAL = ROOT / "evidence_quality/p2_independent_test_log_evaluator_calibration.json"
CAL_SCHEMA = ROOT / "schemas/p2_independent_test_log_evaluator_calibration.schema.json"
QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
DOC = ROOT / "docs/p2_replacement_task_opening_and_evaluator_calibration.md"

def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def failures(data: dict, *, inspect_files: bool = True) -> list[str]:
    out = []; opening = data["opening"]; cal = data["cal"]
    for record, schema_path, label in [(opening, OPENING_SCHEMA, "opening"), (cal, CAL_SCHEMA, "calibration")]:
        schema = json.loads(schema_path.read_text())
        for error in Draft202012Validator(schema).iter_errors(record): out.append(f"{label}-schema:{'.'.join(map(str,error.path))}:{error.message}")
    rows = opening.get("candidates", []); custody = opening.get("custody", {})
    expected_counts = [(71, 156, 227), (2, 6207, 6209), (60, 0, 60), (1, 350, 351)]
    if [r.get("slot") for r in rows] != [1,2,3,4]: out.append("opening slot order drifted")
    for row, counts in zip(rows, expected_counts):
        if (row.get("fail_to_pass_count"), row.get("pass_to_pass_count"), row.get("expected_test_count")) != counts: out.append(f"expected-test denominator drift: {row.get('instance_id')}")
        if row.get("expected_test_count") != row.get("fail_to_pass_count",0) + row.get("pass_to_pass_count",0): out.append(f"expected-test arithmetic drift: {row.get('instance_id')}")
        if row.get("solution_test_path_overlap") != []: out.append(f"path collision admitted: {row.get('instance_id')}")
    if custody.get("candidate_execution_started") or custody.get("candidate_baseline_outcome_opened") or custody.get("candidate_gold_outcome_opened") or custody.get("rank_greater_than_one_task_content_opened"): out.append("opening custody breached")
    if cal.get("exact_agreement_count") != cal.get("total_case_count") or not all(r.get("exact_agreement") for r in cal.get("fixtures",[]) + cal.get("historical_logs",[])): out.append("calibration disagreement remains")
    if cal.get("candidate_execution_started") or cal.get("candidate_outcome_opened") or cal.get("final_pool_opened"): out.append("calibration custody breached")
    if opening.get("support_state_effect") != "none" or cal.get("support_state_effect") != "none": out.append("opening/calibration promoted support")
    if inspect_files:
        queue = json.loads(QUEUE.read_text()); expected = [s["candidates"][0] for s in queue["slots"]]
        for row, source in zip(rows, expected):
            for key in ["instance_id","repo","base_commit","language","license","image_name","problem_statement_sha256","solution_patch_sha256","test_patch_sha256","test_command_sha256"]:
                if row.get(key) != source.get(key): out.append(f"queue/opening drift {key}: {row.get('instance_id')}")
        if sha(ROOT / cal["independent_evaluator_path"]) != cal.get("independent_evaluator_sha256"): out.append("independent evaluator code digest drifted")
        for row in cal.get("historical_logs",[]):
            path=ROOT/row["path"]
            if not path.is_file() or sha(path)!=row["sha256"]: out.append(f"historical calibration log drift: {row['path']}")
        attempts = [
            ("p2_independent_test_log_evaluator_calibration_attempt_001.json", "instrument_failure_before_candidate_execution"),
            ("p2_independent_test_log_evaluator_calibration_attempt_002_failed_30_of_32.json", "failed"),
            ("p2_independent_test_log_evaluator_calibration_attempt_003_failed_31_of_32.json", "failed")]
        for name,state in attempts:
            attempt=json.loads((ROOT/"evidence_quality"/name).read_text())
            if attempt.get("state")!=state: out.append(f"failed calibration attempt drift: {name}")
        doc=DOC.read_text()
        for phrase in ["32/32 exact", "Two parsers can share a", "Candidate execution outcomes", "held-out pool remain unopened"]:
            if phrase not in doc: out.append(f"opening/calibration receipt missing boundary: {phrase}")
    return out

def main() -> None:
    base={"opening":json.loads(OPENING.read_text()),"cal":json.loads(CAL.read_text())}; out=failures(base); mutations=[]
    def add(label,edit): c=copy.deepcopy(base);edit(c);mutations.append((label,c))
    add("path collision",lambda c:c["opening"]["candidates"][0].__setitem__("solution_test_path_overlap",["x"]))
    add("denominator drift",lambda c:c["opening"]["candidates"][0].__setitem__("expected_test_count",1))
    add("execution started",lambda c:c["opening"]["custody"].__setitem__("candidate_execution_started",True))
    add("next rank opened",lambda c:c["opening"]["custody"].__setitem__("rank_greater_than_one_task_content_opened",True))
    add("agreement loss",lambda c:c["cal"]["fixtures"][0].__setitem__("exact_agreement",False))
    add("case shrink",lambda c:c["cal"].__setitem__("total_case_count",31))
    add("outcome opened",lambda c:c["cal"].__setitem__("candidate_outcome_opened",True))
    add("final opened",lambda c:c["cal"].__setitem__("final_pool_opened",True))
    add("support promotion",lambda c:c["cal"].__setitem__("support_state_effect","promotion"))
    for label,c in mutations:
        if not failures(c,inspect_files=False): out.append(f"negative mutation accepted: {label}")
    if out: raise SystemExit("P2 task opening/evaluator calibration failed:\n - "+"\n - ".join(out))
    print("P2 task opening/evaluator calibration passed: four rank-one specs, 6,847 expected identities, 32/32 dual-parser controls, three failed attempts retained, outcomes/final pool closed; 9/9 mutations rejected.")

if __name__=="__main__":main()
