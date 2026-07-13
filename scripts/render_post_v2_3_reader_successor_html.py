#!/usr/bin/env python3
"""Render and deterministically archive the selected v2.0 curated HTML artifact."""
from __future__ import annotations
import hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
import build_reader_edition

ROOT=Path(__file__).resolve().parents[1];ED=ROOT/"editions/reader_manuscript/v2_0";BUILD=ROOT/"build/curated_reader_v2_0";SITE=BUILD/"_reader_site";ARCH=ED/"artifacts/asi-stack-curated-reader-v2.0-html.zip";AM=ED/"html_artifact_manifest.json"
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree_digest(root):
  h=hashlib.sha256()
  for p in sorted(x for x in root.rglob("*") if x.is_file()):h.update(p.relative_to(root).as_posix().encode()+b"\0"+p.read_bytes()+b"\0")
  return h.hexdigest()
def main():
  m=load(ED/"manifest.json")
  if m.get("selected_initial_format")!="canonical_curated_html" or m.get("release_state")!="not_yet_rendered":raise SystemExit("HTML format was not prospectively selected or source is not frozen")
  if BUILD.exists():shutil.rmtree(BUILD)
  build_reader_edition.generate(BUILD,"reader_release",None)
  for r in m["chapter_records"]:
    text=(ROOT/r["file"]).read_text();body=text.split("-->\n\n",1)[1]
    target=BUILD/"chapters"/(r["chapter_id"]+".qmd");target.write_text(body)
  subprocess.run(["quarto","render","--to","html"],cwd=BUILD,check=True)
  html=sorted(SITE.rglob("*.html"));chap=sorted((SITE/"chapters").glob("*.html"))
  if len(chap)!=54 or len(html)<59:raise SystemExit(f"unexpected HTML page count: {len(chap)} chapters, {len(html)} total")
  ARCH.parent.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(ARCH,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(x for x in SITE.rglob("*") if x.is_file()):
      info=zipfile.ZipInfo(p.relative_to(SITE).as_posix(),(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
  report={"schema_version":"asi_stack.curated_reader_html_artifact.v2","edition_id":m["edition_id"],"format":"canonical_curated_html","source_manifest":"editions/reader_manuscript/v2_0/manifest.json","source_tree_sha256":m["source_snapshot"]["source_tree_sha256"],"curated_chapter_bundle_sha256":hashlib.sha256(b"".join((ROOT/r["file"]).read_bytes() for r in m["chapter_records"])).hexdigest(),"format_profile_sha256":sha(BUILD/"_quarto.yml"),"local_site":"build/curated_reader_v2_0/_reader_site","archive":"editions/reader_manuscript/v2_0/artifacts/asi-stack-curated-reader-v2.0-html.zip","archive_sha256":sha(ARCH),"archive_bytes":ARCH.stat().st_size,"site_tree_sha256":tree_digest(SITE),"html_page_count":len(html),"chapter_entry_point_count":len(chap),"render_state":"rendered_pending_inspection","support_state_effect":"none","non_claims":["Rendering does not approve editorial quality or accessibility.","The archive is not the canonical evidence authority.","No independent external-human review is claimed.","No support state, safety, readiness, AGI, or ASI claim changes."]}
  AM.write_text(json.dumps(report,indent=2)+"\n")
  print(f"Rendered curated reader HTML: {len(html)} pages, 54 chapter entry points, archive {ARCH.stat().st_size} bytes, sha256 {report['archive_sha256']}.")
if __name__=="__main__":main()
