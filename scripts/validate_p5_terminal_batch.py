#!/usr/bin/env python3
import copy,json
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"experiments/p5_terminal_batch"
def load(p):return json.loads(p.read_text())
def errors(r):
 out=[]; rows=r.get("atom_results",[]); disp={x.get("atom_id"):x.get("disposition") for x in rows}
 expected={"circle-calculus-and-proof-carrying-ai-contracts.mechanism.003":"promoted_at_bounded_scope","system-boundaries-and-authority.invariant.001":"promoted_at_bounded_scope","capability-replacement-and-rollback.invariant.011":"narrowed_after_full_attempt"}
 if disp!=expected:out.append("dispositions")
 if not rows[0]["checks"]["all_commands_pass"] or rows[0]["checks"]["consumer_negative_controls"]!=4:out.append("circle")
 if rows[1]["checks"]["mutation_rejections"]!=38 or rows[1]["checks"]["unsafe_releases"]!=0:out.append("authority")
 if rows[2]["checks"]["service_restart_executed"] or rows[2]["checks"]["external_compensation_executed"] or rows[2]["new_support_state"]!="argument":out.append("rollback ceiling")
 if r.get("chapter_core_promotion_count")!=0 or r.get("terminal_batch_complete") is not True:out.append("boundary")
 return out
def main():
 r=load(BASE/"results/result.json");jsonschema.validate(r,load(ROOT/"schemas/p5_terminal_batch_result.schema.json"));fail=errors(r)
 for label,mut in [("core",lambda x:x.__setitem__("chapter_core_promotion_count",1)),("launder rollback",lambda x:x["atom_results"][2].__setitem__("disposition","promoted_at_bounded_scope")),("erase compensation",lambda x:x["atom_results"][2]["checks"].__setitem__("external_compensation_executed",True)),("erase mutation",lambda x:x["atom_results"][1]["checks"].__setitem__("mutation_rejections",37))]:
  c=copy.deepcopy(r);mut(c)
  if not errors(c):fail.append("mutation accepted:"+label)
 if fail:raise SystemExit("P5 terminal batch failed:\n - "+"\n - ".join(fail))
 print("P5 mandatory terminal batch passed: Circle and finite authority atoms promoted at bounded scope; rollback-outcome atom narrowed after full attempt; four mutations rejected; zero chapter-core movement.")
if __name__=="__main__":main()
