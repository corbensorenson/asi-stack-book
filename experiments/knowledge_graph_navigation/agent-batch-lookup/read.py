"""Read one book resource or resolve several clues in a single catalog read."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reader = load("comparison_reader", HERE.parent / "agent-publication/read.py")
lookup = load("book_client", HERE.parents[2] / "skills/asi-stack-reader/scripts/read_book.py")


def batch(raw, clues):
    data = json.loads(raw)
    records = data["records"]
    if isinstance(records, dict) or not records or any(not isinstance(row, dict) for row in records):
        raise ValueError("Batch lookup expects a JSON array of evidence records")
    results = lookup.find_records(records, clues)
    for result in results:
        result["matches"] = [
            {field: row[field] for field in ("id", "title", "url", "section_url") if field in row}
            for row in result["matches"]
        ]
    return json.dumps(results, indent=2, ensure_ascii=False)


def main():
    site, journal, route, *queries = sys.argv[1:]
    journal = Path(journal)
    opens = json.loads(journal.read_text()) if journal.is_file() else []
    remaining = 52000 - sum(row.get("displayed_bytes", 0) for row in opens)
    if len(opens) >= 18 or remaining <= 0:
        raise SystemExit("Reading allowance exhausted")
    entry = {"route": route}
    try:
        raw = reader.resource(Path(site).resolve(), route)
        entry.update(bytes=len(raw), sha256=sha256(raw).hexdigest())
        if queries[:1] == ["--batch"]:
            entry["clues"] = queries[1:]
            result = batch(raw, queries[1:])
        else:
            result = reader.display(raw, route, " ".join(queries))
        result = result.encode()[:min(remaining, 5500)].decode(errors="ignore")
        entry["displayed_bytes"] = len(result.encode())
        print(result)
    except (OSError, KeyError, ValueError, subprocess.CalledProcessError) as error:
        entry["error"] = type(error).__name__
        print("Resource unavailable")
    finally:
        journal.write_text(json.dumps(opens+[entry], indent=2)+"\n")


if __name__ == "__main__":
    main()
