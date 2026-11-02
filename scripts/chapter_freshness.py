"""Chapter revision declarations and independent rendered-status checks.

Dates are author-maintained events, not source freshness or support evidence.
The renderer owns presentation; this module never changes manuscript bytes.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from html.parser import HTMLParser
import re

import yaml

REVISION_LABEL = 'Chapter revision'
REVIEW_LABEL = 'Source review'
SCOPE_LABEL = 'Source review scope'
UNRECORDED_REVIEW = 'Not recorded in chapter metadata; see source records'


class UniqueKeysLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        value = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in value
            except TypeError as error:
                raise ValueError('front matter requires scalar mapping keys') from error
            if duplicate:
                raise ValueError(f'duplicate front-matter key: {key!r}')
            value[key] = self.construct_object(value_node, deep=deep)
        return value


def declarations(text: str, *, as_of: date | None = None) -> dict:
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    if not match:
        raise ValueError('chapter requires a YAML front-matter mapping')
    try:
        metadata = yaml.load(match.group(1), Loader=UniqueKeysLoader)
    except yaml.YAMLError as error:
        raise ValueError(f'invalid chapter front matter: {error}') from error
    if not isinstance(metadata, dict):
        raise ValueError('chapter front matter must be a mapping')
    today = as_of or datetime.now(timezone.utc).date()

    def event(key):
        raw = metadata.get(key)
        # PyYAML accepts ISO date scalars as date objects; timestamps, bools,
        # compact/week dates and ambiguous strings are not revision dates.
        value = raw.isoformat() if type(raw) is date else raw
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError(f'{key} requires a canonical YYYY-MM-DD date')
        try:
            parsed = date.fromisoformat(value)
        except ValueError as error:
            raise ValueError(f'{key} is not a calendar date') from error
        if parsed > today:
            raise ValueError(f'{key} cannot declare a future event')
        return value

    result = {'last_updated': event('last_updated')}
    has_date = 'source_reviewed_on' in metadata
    has_scope = 'source_review_scope' in metadata
    if has_date != has_scope:
        raise ValueError('source_reviewed_on and source_review_scope must be supplied together')
    if has_date:
        scope = metadata['source_review_scope']
        if not isinstance(scope, str) or not scope.strip():
            raise ValueError('source_review_scope must name the bounded review')
        result.update(source_reviewed_on=event('source_reviewed_on'), source_review_scope=scope.strip())
    return result


class StatusTables(HTMLParser):
    """Read visible table cells only in the chapter-status section."""
    def __init__(self):
        super().__init__()
        self.sections = []
        self.in_status = False
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None
        self.hidden = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        # Quarto wraps h2 sections in <section id="chapter-status">.
        if tag == 'section':
            self.sections.append(self.in_status)
            self.in_status = self.in_status or attrs.get('id') == 'chapter-status'
        hidden = 'hidden' in attrs or attrs.get('aria-hidden') == 'true' or bool(
            re.search(r'(?:display\s*:\s*none|visibility\s*:\s*hidden)', attrs.get('style', ''), re.I))
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag, hidden))
            self.hidden += int(hidden)
        if not self.in_status or self.hidden:
            return
        if tag == 'table':
            if self.table is not None:
                raise ValueError('nested chapter-status tables are not supported')
            self.table = []
        elif tag == 'tr' and self.table is not None:
            self.row = []
        elif tag in ('td','th') and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.in_status and not self.hidden and self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.in_status and not self.hidden:
            if tag in ('td','th') and self.cell is not None:
                self.row.append(' '.join(''.join(self.cell).split()))
                self.cell = None
            elif tag == 'tr' and self.row is not None:
                self.table.append(self.row)
                self.row = None
            elif tag == 'table' and self.table is not None:
                self.tables.append(self.table)
                self.table = None
        if self.stack and self.stack[-1][0] == tag:
            self.hidden -= int(self.stack.pop()[1])
        if tag == 'section' and self.sections:
            self.in_status = self.sections.pop()


def rendered_errors(html: str, expected: dict) -> list[str]:
    parser = StatusTables()
    try:
        parser.feed(html)
    except ValueError as error:
        return [str(error)]
    if len(parser.tables) != 1:
        return ['chapter-status requires exactly one visible metadata table']
    rows = parser.tables[0]
    required = {REVISION_LABEL: expected['last_updated'],
                REVIEW_LABEL: expected.get('source_reviewed_on', UNRECORDED_REVIEW)}
    if 'source_review_scope' in expected:
        required[SCOPE_LABEL] = ' '.join(expected['source_review_scope'].split())
    errors = []
    for label, value in required.items():
        selected = [row for row in rows if row and row[0] == label]
        if selected != [[label, value]]:
            errors.append(f'{label}: expected exactly one visible value {value!r}, observed {selected!r}')
    if any(row and row[0] == 'Last updated' for row in rows):
        errors.append('legacy Last updated row survived the canonical projection')
    if SCOPE_LABEL not in required and any(row and row[0] == SCOPE_LABEL for row in rows):
        errors.append('rendered source-review scope has no declared review event')
    return errors
