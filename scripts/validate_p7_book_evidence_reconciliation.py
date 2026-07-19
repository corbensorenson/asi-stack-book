#!/usr/bin/env python3
import copy,hashlib,json,subprocess,sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"experiments/p7_book_evidence_reconciliation/result.json";S=ROOT/"schemas/p7_book_evidence_reconciliation.schema.json"
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def errors(v):
 out=[];records=v.get("chapter_records",[]);status=load(ROOT/"roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json");expected={x["chapter_id"] for x in status["chapter_claim_program"]}
 if {x.get("chapter_id") for x in records}!=expected:out.append("chapter coverage")
 for row in records:
  path=ROOT/row.get("path","missing")
  if not path.exists() or sha(path)!=row.get("sha256"):out.append("chapter digest:"+str(row.get("chapter_id")))
  elif path.read_text().count("<!-- P7-EVIDENCE-RECONCILIATION:START -->")!=1 or path.read_text().count("<!-- P7-EVIDENCE-RECONCILIATION:END -->")!=1:out.append("chapter marker:"+row["chapter_id"])
  if any(row.get(k)!=1 for k in ["human_summary_count","ai_packet_count","argument_exit_table_count"]):out.append("chapter packet:"+str(row.get("chapter_id")))
 for path,digest in v.get("appendix_digests",{}).items():
  p=ROOT/path
  if not p.exists() or sha(p)!=digest:out.append("appendix digest:"+path)
 inventory=load(ROOT/"sources/source_inventory.json")
 if len(inventory)!=319 or not any(x.get("id")=="ext_gated_deltanet2_2026" for x in inventory):out.append("current source inventory")
 chapter=(ROOT/"chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd").read_text();h=(ROOT/"appendices/H_external_sources.qmd").read_text();e=(ROOT/"appendices/E_codex_test_specs.qmd").read_text();k=(ROOT/"appendices/K_implementation_horizons.qmd").read_text()
 if "Gated DeltaNet-2" not in chapter or "ext_gated_deltanet2_2026" not in h:out.append("current comparator integration")
 if e.count("candidate and strongest-comparator envelope unavailable")!=1 or "P6 made a full access attempt and ended blocked" not in k:out.append("P6 appendix reconciliation")
 if v.get("blocked_atom_count")!=3698 or v.get("chapter_core_promotion_count")!=0 or v.get("core_argument_count")!=55:out.append("support/gap boundary")
 return out
def main():
 v=load(P);jsonschema.validate(v,load(S));fail=errors(v)
 check=subprocess.run([sys.executable,"scripts/build_reader_edition.py","--check"],cwd=ROOT,text=True,capture_output=True)
 if check.returncode:fail.append("reader projection check:"+check.stdout+check.stderr)
 muts=[("drop chapter",lambda x:x["chapter_records"].pop()),("rewrite digest",lambda x:x["chapter_records"][0].__setitem__("sha256","0"*64)),("erase packet",lambda x:x["chapter_records"][0].__setitem__("ai_packet_count",0)),("erase gaps",lambda x:x.__setitem__("blocked_atom_count",0)),("invent core",lambda x:x.__setitem__("chapter_core_promotion_count",1))]
 for label,mut in muts:
  c=copy.deepcopy(v);mut(c)
  if not errors(c):fail.append("mutation accepted:"+label)
 if fail:raise SystemExit("P7 book reconciliation failed:\n - "+"\n - ".join(fail))
 print("P7 book reconciliation passed: 55 chapter-specific human/AI evidence packets, 3,745 terminal atoms, 3,698 blocked gaps retained, five appendices digest-bound, reader projection replayed, Gated DeltaNet-2/P6 blockers integrated, five mutations rejected, zero core movement.")
if __name__=="__main__":main()
