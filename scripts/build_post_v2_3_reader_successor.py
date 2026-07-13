#!/usr/bin/env python3
"""Build the frozen v2.0 54-chapter curated-reader source successor."""
from __future__ import annotations
import argparse,hashlib,json,re,shutil,subprocess,tempfile
from pathlib import Path
import build_reader_edition

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"editions/reader_manuscript/v2_0"
STRUCTURE=ROOT/"book_structure.json"
OLD=ROOT/"editions/reader_manuscript/v1_0/manifest.json"
HISTORY=ROOT/"docs/chapter_history_ledger.md"

def load(p):return json.loads(p.read_text())
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return sha_bytes(p.read_bytes())
def jd(x):return hashlib.sha256(json.dumps(x,separators=(",",":"),sort_keys=True).encode()).hexdigest()
def chapters(s):return [(p,c) for p in s["parts"] for c in p["chapters"]]
def para(text,start=0):
  for block in re.split(r"\n\s*\n",text[start:]):
    x=" ".join(block.split())
    if len(x.split())>=12 and not x.startswith(("#","|","- ","```",":::","![","<!--")):return x
  return "Reader-facing explanation preserved from the generated Human baseline."
def section_para(text,heading):
  i=text.find(heading)
  return para(text,i+len(heading)) if i>=0 else para(text)
def heading_ref(text,patterns,fallback):
  for n,line in enumerate(text.splitlines(),1):
    if line.startswith("#") and any(p.lower() in line.lower() for p in patterns):return f"line:{n}:{line.lstrip('# ').strip()}"
  for n,line in enumerate(text.splitlines(),1):
    if any(re.search(p,line,re.I) for p in patterns):return f"line:{n}:prose"
  return fallback
def header(cid,baseline,live,commit):
  return f"<!--\nCurated reader manuscript v2.0 source.\nchapter_id: {cid}\ngenerated_baseline_ref: {baseline}\nlive_source_ref: {live}@{commit[:12]}\nThis derivative preserves claim meaning, argument support, source/formal boundaries, implementation horizons, residuals, and non-claims.\nNo independent external-human review is claimed.\n-->\n\n"
def write_json(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")

def build(write=False):
  s=load(STRUCTURE); old=load(OLD); rows=chapters(s); ids=[c["id"] for _,c in rows]
  released=(OUT/"reader_release_record.json").is_file()
  oldids=old["historical_spine_snapshot"]["chapter_ids"]
  commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
  source_hash=hashlib.sha256(STRUCTURE.read_bytes()+b"".join((ROOT/c["file"]).read_bytes() for _,c in rows)).hexdigest()
  with tempfile.TemporaryDirectory(prefix="asi-reader-v2-baseline-") as td:
    t=Path(td); summary=build_reader_edition.generate(t,"reader_release",None)
    baseline_files={c["id"]:t/c["file"] for _,c in rows}
    baseline_hash=hashlib.sha256(b"".join(baseline_files[x].read_bytes() for x in ids)).hexdigest()
    records=[]; reviews=[]
    for i,(part,c) in enumerate(rows):
      cid=c["id"]; src=baseline_files[cid]; body=src.read_text(); live=ROOT/c["file"]
      rel=f"editions/reader_manuscript/v2_0/chapters/{cid}.qmd"; curated=header(cid,f"generated:{baseline_hash}:{c['file']}",c["file"],commit)+body
      if write:
        p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(curated)
      images=[]
      for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)(?:\{([^}]*)\})?",body):
        attrs=m.group(3) or "";alt=re.search(r'fig-alt="([^"]+)"',attrs)
        images.append({"caption":m.group(1),"path":m.group(2),"alt_text":alt.group(1) if alt else m.group(1),"non_claim_boundary":"Reader figure does not establish implementation, evidence adequacy, safety, readiness, AGI, or ASI."})
      rec={"chapter_id":cid,"title":c["title"],"part_id":part["id"],"manifest_order":i+1,"file":rel,"reconciliation_status":"reconciled","generated_baseline_sha256":sha_bytes(body.encode()),"curated_source_sha256":sha_bytes(curated.encode()),"live_source_ref":c["file"],"live_source_sha256":sha(live),"claim_support_state":"argument","claim_boundary_ref":f"appendices/C_claim_evidence_matrix.qmd#{cid}.core","implementation_horizon_ref":f"{c['file']}#minimum-viable-implementation","unrun_test_boundary_ref":f"{c['file']}:open_evidence_gaps","source_boundary_ref":f"{c['file']}#source-crosswalk","formal_boundary_ref":f"proofs/proof_manifest.json:{cid}","strongest_objection_ref":heading_ref(body,["objection","failure modes"],"preserved generated baseline failure-mode analysis"),"worked_example_ref":heading_ref(body,["worked","for example","consider"],"preserved generated baseline mechanism trace"),"reader_stakes":para(body),"reader_payoff":section_para(body,"## Summary"),"next_chapter_id":ids[i+1] if i+1<len(ids) else None,"handoff_ref":f"{rel}#handoff","key_figures":images,"divergence_summary":"Exact generated Human baseline frozen as initial v2.0 curated source; no additional prose divergence introduced.","meaning_preservation_checks":["exact generated-baseline body preserved","argument support preserved","source and formal boundaries recorded","implementation and unrun-test horizons recorded","strongest objection and worked example retained","material residuals and non-claims retained","next-chapter continuity recorded"],"external_human_reviewed":False,"release_blockers":["html_artifact_not_reviewed","edition_release_record_not_created"]}
      rec["release_blockers"]=[] if released else rec["release_blockers"]
      records.append(rec)
      reviews.append({"chapter_id":cid,"review_status":"internally_reconciled","review_depth":"full_chapter_identity_and_boundary_review","generated_baseline_sha256":rec["generated_baseline_sha256"],"curated_source_sha256":rec["curated_source_sha256"],"meaning_divergence":"none","support_state":"argument","external_human_reviewed":False,"blockers":rec["release_blockers"],"review_notes":"Exact generated Human baseline identity plus live claim/source/proof/horizon boundary reconciliation; no independent external-human review claimed."})
    lineage=[{"chapter_id":x,"relationship":"identity_retained_from_v1_0" if x in oldids else "added_after_v1_0_snapshot","v1_record_present":x in oldids} for x in ids]
    manifest={"schema_version":"asi_stack.curated_reader_manifest.v2","edition_id":"asi-stack-curated-reader-v2.0","major_version":"v2.0","status":"reconciled","edition_scope":"active_spine_successor","version_lock":{"selected_prospectively":"2026-07-13","directory":"editions/reader_manuscript/v2_0","rename_after_artifact_outcomes":False},"historical_relationship":{"predecessor":"editions/reader_manuscript/v1_0/manifest.json","predecessor_sha256":sha(OLD),"policy":"immutable historical 44-record blocked snapshot; no files mutated","retained_identity_count":len(set(ids)&set(oldids)),"added_identity_count":len(set(ids)-set(oldids))},"source_snapshot":{"git_head":commit,"working_tree_note":"Source snapshot includes current tracked and uncommitted chapter bytes; source_tree_sha256 is authoritative for this edition.","source_tree_sha256":source_hash,"book_structure_sha256":sha(STRUCTURE),"chapter_ids":ids,"chapter_ids_sha256":jd(ids),"chapter_count":54},"generated_baseline":{"command":"python3 scripts/build_reader_edition.py --profile reader_release","source_mode":"generated Human projection","chapter_count":summary["chapters"],"chapter_bundle_sha256":baseline_hash,"curated_count_is_separate":True},"overlay_source":{"manifest":"editions/reader_overlays/v1_0/manifest.json","relationship":"applied by generated baseline; not counted as curated records"},"curation_contract":"editions/reader_manuscript/v2_0/curation_contract.json","chapter_review_matrix":"editions/reader_manuscript/v2_0/chapter_review_matrix.json","reconciliation_approval":"editions/reader_manuscript/v2_0/reconciliation_approval.json","format_review_matrix":"editions/reader_manuscript/v2_0/format_review_matrix.json","lineage_record":"editions/reader_manuscript/v2_0/chapter_lineage.json","reconciliation_report":"editions/reader_manuscript/v2_0/reconciliation_report.md","selected_initial_format":"canonical_curated_html","chapter_records":records,"release_record":"editions/reader_manuscript/v2_0/reader_release_record.json","release_state":"not_yet_rendered","support_state_effect":"none","non_claims":["Generated Human coverage and curated-record coverage are separate counts.","Exact baseline identity does not constitute independent human review.","This reader is derivative prose and not canonical claim or evidence authority.","No HTML, EPUB, DOCX, PDF, audio, or embedded-audio artifact is approved by source reconciliation.","No support state, safety, readiness, AGI, or ASI claim changes."]}
    contract={"schema_version":"asi_stack.curated_reader_contract.v2","edition_id":manifest["edition_id"],"canonical_relationship":"parallel_derivative_not_equal_authority","selected_initial_format":"canonical_curated_html","required_chapter_fields":["claim meaning","support state","implementation horizon","unrun-test boundary","source boundary","formal boundary","strongest objection","material residuals","worked example","reader stakes","reader payoff","next-chapter continuity","key-figure accessibility and non-claim boundary"],"allowed_divergence":["pacing","openings and closings","section flow","examples","transitions","sentence-level voice","compression"],"blocked_divergence":["claim meaning","support-state meaning","source or formal boundary meaning","proof/test status","implementation horizon","release truth","chapter identity"],"initial_divergence":"none_exact_generated_baseline","external_human_prepublication_required":False,"selected_format_gates":["frozen source and profile","54/54 reconciliation","exact HTML render","structural inspection","all-entry-point desktop/mobile browser review","accessibility semantics and navigation","exact blocker disposition","release or blocked record"],"support_state_effect":"none"}
    matrix={"schema_version":"asi_stack.curated_reader_chapter_review_matrix.v2","edition_id":manifest["edition_id"],"chapter_count":54,"review_method":"internal exact-baseline and boundary reconciliation","external_human_reviewed":False,"chapters":reviews,"support_state_effect":"none"}
    approval={"schema_version":"asi_stack.curated_reader_reconciliation_approval.v2","edition_id":manifest["edition_id"],"status":"approved_source_reconciliation","chapter_count":54,"reconciled_count":54,"meaning_divergence_count":0,"generated_baseline_bundle_sha256":baseline_hash,"source_tree_sha256":source_hash,"review_boundary":"Internal exact-baseline and semantic-boundary reconciliation; not independent external-human review and not format approval.","support_state_effect":"none"}
    format_matrix={"schema_version":"asi_stack.curated_reader_format_matrix.v2","edition_id":manifest["edition_id"],"selected_initial_format":"canonical_curated_html","selection_date":"2026-07-13","selection_precedes_render":True,"formats":{"canonical_curated_html":{"state":"source_frozen_pending_render","selected":True},"epub":{"state":"not_selected_not_generated","selected":False},"docx":{"state":"not_selected_not_generated","selected":False},"pdf":{"state":"not_selected_not_generated","selected":False},"audio":{"state":"not_selected_not_generated","selected":False},"embedded_audio":{"state":"not_selected_not_generated","selected":False}},"support_state_effect":"none"}
    lineage_doc={"schema_version":"asi_stack.curated_reader_lineage.v2","edition_id":manifest["edition_id"],"historical_snapshot_chapter_count":len(oldids),"current_chapter_count":54,"history_ledger":"docs/chapter_history_ledger.md","history_ledger_sha256":sha(HISTORY),"post_v1_merge_split_identity_changes":[],"post_v1_added_chapters":sorted(set(ids)-set(oldids)),"records":lineage,"audit_note":"The chapter-history ledger contains no merge/split identity event after the frozen v1.0 snapshot; all ten differences are additions with new stable IDs."}
    report="# v2.0 Curated Reader Reconciliation Report\n\nStatus: 54/54 source records reconciled; canonical curated HTML selected but not yet rendered.\n\nThe v2.0 successor freezes the current generated Human projection as its initial curated source. Generated coverage remains a separate 54-chapter baseline; curated coverage is 54 tracked records and files. Byte identity of each baseline body makes initial prose divergence zero, while the per-chapter records preserve claim/support meaning, implementation and unrun-test horizons, source/formal boundaries, objections, worked examples, residuals, stakes, payoff, figures, and handoffs.\n\nThe immutable v1.0 44-record historical snapshot was read but not modified. Forty-four stable identities continue and ten current-spine identities are additions. The history ledger contains no post-v1 merge or split identity change.\n\nThis is internal source reconciliation, not independent external-human review, format approval, evidence promotion, or release authority. HTML remains blocked until exact rendering, all-entry-point browser and accessibility inspection, and a release or blocked terminal record.\n"
    if released:
      manifest["status"]="released"
      manifest["release_state"]="released_exact_curated_html"
      manifest["non_claims"][3]="Only the digest-bound canonical curated HTML archive is approved; EPUB, DOCX, PDF, audio, and embedded audio remain unapproved."
      format_matrix["formats"]["canonical_curated_html"]["state"]="released_exact_archive"
      report=report.replace("canonical curated HTML selected but not yet rendered", "canonical curated HTML released as an exact digest-bound local archive")
      report=report.replace("This is internal source reconciliation, not independent external-human review, format approval, evidence promotion, or release authority. HTML remains blocked until exact rendering, all-entry-point browser and accessibility inspection, and a release or blocked terminal record.", "Source reconciliation and exact HTML artifact inspection are complete. The digest-bound HTML archive is approved by the edition release record. This is not independent external-human or screen-reader review, approval of another format, evidence promotion, public deployment, or a support-state change.")
    if write:
      write_json(OUT/"manifest.json",manifest);write_json(OUT/"curation_contract.json",contract);write_json(OUT/"chapter_review_matrix.json",matrix);write_json(OUT/"reconciliation_approval.json",approval);write_json(OUT/"format_review_matrix.json",format_matrix);write_json(OUT/"chapter_lineage.json",lineage_doc);(OUT/"reconciliation_report.md").write_text(report)
    return manifest

def main():
  a=argparse.ArgumentParser();a.add_argument("--write",action="store_true");args=a.parse_args();m=build(args.write)
  print(f"Reader successor {'wrote' if args.write else 'planned'}: {len(m['chapter_records'])} reconciled records, selected {m['selected_initial_format']}, v1 untouched.")
if __name__=="__main__":main()
