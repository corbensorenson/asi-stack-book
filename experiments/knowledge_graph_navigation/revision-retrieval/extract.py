"""Emit the frozen evidence catalog and its induced graph from the tested HTML site."""
import gzip
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

site = Path(sys.argv[1])
graph_dir = site / "products/evidence-registry/knowledge-graph"
manifest = json.loads((graph_dir / "manifest.json").read_bytes())
status = json.loads((site / "status/canonical-public-status.json").read_bytes())
assert manifest["source_commit"] == status["source_commit"] == "e53063c0f54a442df9c58644ce82ef13e06f676a"
assert status["source_tree_state"] == "clean"


def checked(name):
    data = (graph_dir / name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == manifest["files"][name]["sha256"]
    return data


catalog = json.loads(checked("evidence-catalog.json"))
graph = json.loads(gzip.decompress(checked("graph.json.gz")))
assert graph["snapshot_id"] == catalog["snapshot_id"] == manifest["snapshot_id"]
records = catalog["records"]
for record in records:
    url = urlsplit(record["url"])
    target = site / url.path
    record["verified_fragment"] = bool(url.fragment and target.is_file()
                                       and ('id="' + url.fragment + '"') in target.read_text())
tasks = json.loads(Path(__file__).with_name("tasks.json").read_bytes())
included = {r["id"] for r in records} | {t["start"] for t in tasks}
edges = [[e["from"], e["predicate"], e["to"]] for e in graph["edges"]
         if e["from"] in included and e["to"] in included]
print(json.dumps(dict(source_commit=catalog["source_commit"], snapshot_id=catalog["snapshot_id"],
                      catalog_sha256=manifest["files"]["evidence-catalog.json"]["sha256"],
                      matcher_sha256=hashlib.sha256(checked("evidence-search.js")).hexdigest(),
                      records=records, edges=edges), indent=2))
