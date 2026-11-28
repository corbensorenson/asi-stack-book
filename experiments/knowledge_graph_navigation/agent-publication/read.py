"""Read one public resource under the shared agent comparison budget."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("reader", HERE.parent / "reader-access/read.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
RAW = "https://raw.githubusercontent.com/corbensorenson/asi-stack-book/"


def resource(site, route):
    if route.startswith(RAW):
        revision, name = route.removeprefix(RAW).split("/", 1)
        if not re.fullmatch("[a-f0-9]{40}", revision):
            raise ValueError("Repository references need a full revision")
        return subprocess.check_output(["git", "show", revision + ":" + name])
    route = route.removeprefix(reader.PUBLIC)
    url = urlsplit(route)
    path = (site / unquote(url.path.lstrip("/"))).resolve()
    if url.scheme or url.netloc or not path.is_relative_to(site):
        raise ValueError("Use a path from the book")
    if path.is_dir():
        path /= "index.html"
    return path.read_bytes()


def display(raw, route, query):
    text = raw.decode()
    url = urlsplit(route)
    if not url.path or url.path.endswith((".html", "/")):
        parser = reader.Page()
        parser.feed(text)
        node = reader.find_node(parser.tree, lambda row: row[1].get("id") == unquote(url.fragment)) if url.fragment else None
        if node is None:
            node = reader.find_node(parser.tree, lambda row: row[0] == "main") or parser.tree
        from urllib.parse import urljoin
        text = reader.render(node, urljoin(reader.PUBLIC, route))
    if query:
        text = reader.excerpt(text.splitlines(), query)
        if url.path.endswith(".json"):
            value = json.loads(raw)
            terms = {q for q in re.findall(r"[\w-]+", query.casefold()) if len(q) > 2}
            iterable = value.get("records", value.get("terms", value.get("volumes", value.get("cases", [])))) if isinstance(value, dict) else value
            if isinstance(iterable, dict):
                iterable = iterable.values()
            rows = [(json.dumps(row, ensure_ascii=False), row) for row in iterable]
            rows.sort(key=lambda item: (query.casefold() in item[0].casefold(), len(terms & set(re.findall(r"[\w-]+", item[0].casefold())))), reverse=True)
            if rows:
                text = "\n".join(raw_row for raw_row, _ in rows[:10])
    return text


def main():
    site, journal, route, *query = sys.argv[1:]
    journal = Path(journal)
    opens = json.loads(journal.read_text()) if journal.is_file() else []
    remaining = 52000 - sum(row.get("displayed_bytes", 0) for row in opens)
    if len(opens) >= 18 or remaining <= 0:
        raise SystemExit("Reading allowance exhausted")
    entry = {"route": route}
    try:
        raw = resource(Path(site).resolve(), route)
        entry.update(bytes=len(raw), sha256=sha256(raw).hexdigest())
        value = display(raw, route, " ".join(query))
        value = value.encode()[:min(remaining, 5500)].decode(errors="ignore")
        entry["displayed_bytes"] = len(value.encode())
        print(value)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        entry["error"] = type(error).__name__
        print("Resource unavailable")
    finally:
        journal.write_text(json.dumps(opens+[entry], indent=2)+"\n")


if __name__ == "__main__":
    main()
