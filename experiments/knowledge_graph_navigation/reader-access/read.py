"""Budgeted text view of one rendered book. Usage: read.py SITE LOG URL [find text]."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

PUBLIC = "https://corbensorenson.github.io/asi-stack-book/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tree = ["root", {}, []]
        self.stack = [self.tree]

    def handle_starttag(self, tag, pairs):
        node = [tag, dict(pairs), []]
        self.stack[-1][2].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        self.stack[-1][2].append(text)


def find_node(node, test):
    if test(node):
        return node
    for item in node[2]:
        if isinstance(item, list):
            found = find_node(item, test)
            if found:
                return found
    return None


def render(node, url):
    tag, attrs, children = node
    if tag in {"script", "style", "svg", "nav", "header", "footer", "aside"}:
        return ""
    value = "".join(x if isinstance(x, str) else render(x, url) for x in children)
    if tag == "a" and attrs.get("href") and value.strip():
        value += " [" + urljoin(url, attrs["href"]).removeprefix(PUBLIC) + "]"
    if tag in {"h1", "h2", "h3", "h4", "li", "p", "tr", "section", "div"}:
        return "\n" + value.strip() + "\n"
    return value


def excerpt(lines, query):
    if not query:
        return "\n".join(lines)
    words = set(re.findall(r"\w+", query.lower()))
    ranked = sorted(range(len(lines)), key=lambda i: (
        query.lower() in lines[i].lower(),
        len(words.intersection(re.findall(r"\w+", lines[i].lower())))), reverse=True)
    return "\n".join(lines[i] for i in ranked if any(w in lines[i].lower() for w in words))


def main(site, log, requested, query=""):
    root, journal = Path(site).resolve(), Path(log)
    opens = json.loads(journal.read_text()) if journal.exists() else []
    remaining = 36000 - sum(row["returned_bytes"] for row in opens)
    if len(opens) >= 12 or remaining <= 0:
        raise SystemExit("Read budget exhausted.")
    url = urljoin(PUBLIC, requested)
    if not url.startswith(PUBLIC):
        raise SystemExit("Only public book routes are available in this session.")
    route = urlsplit(url)
    path = (root / unquote(route.path[len(urlsplit(PUBLIC).path):])).resolve()
    if path.is_dir():
        path /= "index.html"
    if not path.is_relative_to(root):
        raise SystemExit("Outside rendered book.")
    raw = path.read_bytes() if path.is_file() else b""
    if path.suffix == ".html" and raw:
        page = Page()
        page.feed(raw.decode())
        content = find_node(page.tree, lambda n: n[1].get("id") == unquote(route.fragment)) if route.fragment else None
        content = content or find_node(page.tree, lambda n: n[0] == "main") or page.tree
        lines = render(content, url).splitlines()
    elif path.suffix == ".json" and raw:
        data = json.loads(raw)
        rows = data.get("records", [data]) if isinstance(data, dict) else data
        lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    elif raw and path.suffix in {".md", ".txt", ".csv"}:
        lines = raw.decode().splitlines()
    else:
        lines = ["Route unavailable in text view."]
    lines = [re.sub(r"\s+", " ", line).strip() for line in lines if line.strip()]
    value = excerpt(lines, query).encode()[:min(5500, remaining)].decode(errors="ignore")
    opens.append(dict(url=url.removeprefix(PUBLIC), find=query, resource_bytes=len(raw),
                      returned_bytes=len(value.encode())))
    journal.write_text(json.dumps(opens, indent=2) + "\n")
    print(value)


if __name__ == "__main__":
    main(*sys.argv[1:])
