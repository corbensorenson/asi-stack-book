#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,re
from pathlib import Path
from build_canonical_public_status import ROOT
import build_post_v2_3_reader_successor as builder

M=ROOT/"editions/reader_manuscript/v2_0/manifest.json";OLD=ROOT/"editions/reader_manuscript/v1_0/manifest.json"
FILES=["curation_contract.json","chapter_review_matrix.json","reconciliation_approval.json","format_review_matrix.json","chapter_lineage.json","reconciliation_report.md"]
LIVE_ONLY=["## Chapter status","## Drafting guardrail","## Codex test plan","## Source crosswalk","## Formalization hooks"]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def errs(d,expected):
  e=[];records=d.get("chapter_records",[]);ids=d.get("source_snapshot",{}).get("chapter_ids",[])
  state=(d.get("status"),d.get("release_state"))
  if state not in {("reconciled","not_yet_rendered"),("released","released_exact_curated_html")}:e.append("source/terminal state drift")
  if len(records)!=54 or [x.get("chapter_id") for x in records]!=ids:e.append("54-record identity/order drift")
  if d.get("historical_relationship",{}).get("predecessor_sha256")!=sha(OLD):e.append("v1 historical digest drift")
  if d.get("selected_initial_format")!="canonical_curated_html":e.append("prospective format selection drift")
  if d.get("support_state_effect")!="none":e.append("support promotion")
  if d.get("generated_baseline",{}).get("chapter_count")!=54:e.append("generated denominator drift")
  if d.get("historical_relationship",{}).get("retained_identity_count")!=44 or d.get("historical_relationship",{}).get("added_identity_count")!=10:e.append("historical/current denominator drift")
  if expected is not None and d!=expected:e.append("unreleased manifest no longer matches regenerated current baseline")
  for r in records:
    p=ROOT/r.get("file","")
    if not p.is_file():e.append(r.get("chapter_id","")+": missing curated file");continue
    text=p.read_text();body=text.split("-->\n\n",1)[1] if "-->\n\n" in text else ""
    if f"chapter_id: {r['chapter_id']}" not in text[:900]:e.append(r["chapter_id"]+": header identity missing")
    if hashlib.sha256(text.encode()).hexdigest()!=r.get("curated_source_sha256"):e.append(r["chapter_id"]+": curated digest drift")
    if hashlib.sha256(body.encode()).hexdigest()!=r.get("generated_baseline_sha256"):e.append(r["chapter_id"]+": generated baseline divergence")
    if r.get("claim_support_state")!="argument" or r.get("external_human_reviewed") is not False:e.append(r["chapter_id"]+": claim/review boundary drift")
    if not r.get("strongest_objection_ref") or not r.get("worked_example_ref") or not r.get("reader_stakes") or not r.get("reader_payoff"):e.append(r["chapter_id"]+": semantic packet missing")
    if text.count("\n## Handoff")!=1:e.append(r["chapter_id"]+": handoff count drift")
    for marker in LIVE_ONLY:
      if marker in body:e.append(r["chapter_id"]+": live-only marker leaked")
  for f in FILES:
    if not (M.parent/f).is_file():e.append("missing successor surface "+f)
  if state==("released","released_exact_curated_html"):
    if not (M.parent/"reader_release_record.json").is_file():e.append("released source lacks exact edition release record")
    else:
      rr=load(M.parent/"reader_release_record.json")
      if rr.get("source_authority",{}).get("source_tree_sha256")!=d.get("source_snapshot",{}).get("source_tree_sha256"):e.append("released source snapshot is not bound by release record")
    if any(r.get("release_blockers") for r in records):e.append("released source retains selected-format chapter blockers")
    if (M.parent/"format_review_matrix.json").is_file():
      fm=load(M.parent/"format_review_matrix.json")
      if fm.get("formats",{}).get("canonical_curated_html",{}).get("state")!="released_exact_archive":e.append("selected format matrix is not terminally released")
  if (M.parent/"reconciliation_approval.json").is_file():
    a=load(M.parent/"reconciliation_approval.json")
    if a.get("reconciled_count")!=54 or a.get("meaning_divergence_count")!=0 or a.get("support_state_effect")!="none":e.append("reconciliation approval drift")
  if (M.parent/"chapter_lineage.json").is_file():
    l=load(M.parent/"chapter_lineage.json")
    if len(l.get("records",[]))!=54 or len(l.get("post_v1_added_chapters",[]))!=10 or l.get("post_v1_merge_split_identity_changes")!=[]:e.append("lineage drift")
  return e
def main():
  if not M.is_file():raise SystemExit("Reader successor validation failed: manifest absent")
  d=load(M);expected=None if d.get("release_state")=="released_exact_curated_html" else builder.build(False);e=errs(d,expected)
  for mut in [lambda x:x.__setitem__("chapter_records",x["chapter_records"][:-1]),lambda x:x["historical_relationship"].__setitem__("predecessor_sha256","0"*64),lambda x:x.__setitem__("selected_initial_format","epub"),lambda x:x.__setitem__("support_state_effect","prototype-backed"),lambda x:x["chapter_records"][0].__setitem__("curated_source_sha256","0"*64),lambda x:x["chapter_records"][0].__setitem__("external_human_reviewed",True)]:
    q=copy.deepcopy(d);mut(q)
    if not errs(q,expected):e.append("negative mutation accepted")
  if e:raise SystemExit("Reader successor validation failed:\n - "+"\n - ".join(e[:40]))
  print("Reader successor passed: 54/54 exact-baseline curated records, 44 retained plus 10 added identities, zero meaning divergence, v1 preserved, canonical HTML selected, and 6 rejecting mutations.")
if __name__=="__main__":main()
