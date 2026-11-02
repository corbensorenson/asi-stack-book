"""Build search-result page labels from each publication's existing owners."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets/search-labels.html"


def render_search_navigation(page_kinds: dict[str, str]) -> str:
    for route, label in page_kinds.items():
        path = PurePosixPath(route)
        if (path.is_absolute() or ".." in path.parts or "\\" in route
                or path.as_posix() != route or path.suffix != ".html"
                or not isinstance(label, str) or not label.strip()):
            raise ValueError(f"invalid search page label: {route!r}")
    # The map is embedded, so labels need no network request. Escape the script
    # delimiter even if a future owner introduces markup in a label.
    data = json.dumps(page_kinds, ensure_ascii=False, sort_keys=True).replace("<", "\\u003c")
    return ('<!-- Generated page-role labels; not claim support or release status. -->\n'
            '<script type="application/json" id="asi-search-page-kinds">'
            + data + '</script>\n' + TEMPLATE.read_text(encoding="utf-8"))
