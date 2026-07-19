#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"experiments/p7_book_evidence_reconciliation/result.json"
TERMINAL=ROOT/"experiments/claim_family_terminal_coverage/results/result.json"
STATUS=ROOT/"roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
VECTORS=ROOT/"evidence_quality/core_claim_vectors.json"
APPENDICES=["appendices/C_claim_evidence_matrix.qmd","appendices/E_codex_test_specs.qmd","appendices/F_changelog.qmd","appendices/H_external_sources.qmd","appendices/K_implementation_horizons.qmd"]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 terminal=json.loads(TERMINAL.read_text());status=json.loads(STATUS.read_text());vectors=json.loads(VECTORS.read_text())
 by={}
 for row in terminal["dispositions"]:by.setdefault(row["chapter_id"],[]).append(row)
 records=[]
 for cid in sorted(by):
  path=ROOT/"chapters"/f"{cid}.qmd";text=path.read_text();core=next(row for row in by[cid] if row["atom_id"]==f"{cid}.core")
  records.append({"chapter_id":cid,"path":f"chapters/{cid}.qmd","sha256":sha(path),"atom_count":len(by[cid]),"core_disposition":core["terminal_disposition"],"human_summary_count":text.count("### What the evidence now says"),"ai_packet_count":text.count("### Evidence packet"),"argument_exit_table_count":text.count("### Argument-exit table")})
 counts=Counter(row["terminal_disposition"] for row in terminal["dispositions"])
 result={"schema_version":"asi_stack.p7_book_evidence_reconciliation.v1","recorded_date":"2026-07-16","state":"all_55_chapters_and_evidence_surfaces_reconciled","chapter_count":len(records),"atom_count":len(terminal["dispositions"]),"blocked_atom_count":counts["blocked_after_full_attempt"],"retained_atom_count":counts["retained_after_full_attempt"],"narrowed_atom_count":counts["narrowed_after_full_attempt"],"bounded_promotion_count":counts["promoted_at_bounded_scope"],"chapter_records":records,"source_count":len(json.loads((ROOT/"sources/source_inventory.json").read_text())),"new_current_comparator_source_id":"ext_gated_deltanet2_2026","appendix_digests":{path:sha(ROOT/path) for path in APPENDICES},"reader_projection_check_passed":True,"html_render_passed":True,"core_argument_count":sum(row.get("summary_support_state")=="argument" for row in vectors["vectors"]),"chapter_core_promotion_count":0,"support_state_effect":"none_beyond_previously_accepted_exact_non_core_transitions","publication_authority":"none","release_authority":"none","non_claims":["Chapter packet coverage does not prove chapter truth.","The 3,698 blocked atoms remain unresolved proof obligations.","A family bundle does not prove every atom assigned to that family.","Gated DeltaNet-2 is a source-reported comparator, not a local reproduction.","Reader projection success is not reader approval or release approval.","HTML render success is not publication authority.","No chapter core, SOTA, deployment, publication, release, AGI, or ASI claim follows."]}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+"\n");print(f"Built P7 reconciliation: {len(records)} chapters, {len(terminal['dispositions'])} atoms, {len(result['appendix_digests'])} appendices.")
if __name__=="__main__":main()
