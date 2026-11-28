"""Build the book's shared terminology, chapter lookup and citation destinations."""
from collections import defaultdict
from html import escape
from html.parser import HTMLParser
import json
import re
from urllib.parse import quote

TERMS = "products/ai_dictionary.json"
EVIDENCE_LINKS = "products/dictionary_evidence_links.json"
EVIDENCE_LABELS = {"illustrated_by": "Worked example", "measured_in": "Measurement", "has_primary_source": "Primary source"}
DIRECTORY = "products/evidence-registry/knowledge-graph/"
PAGE = DIRECTORY+"dictionary.html"


def term_id(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace("+", " plus ")).strip("-")


def add_terms(graph):
    identities = set()
    for position, row in enumerate(graph.data(TERMS)):
        identity = term_id(row["term"])
        if identity in identities:
            raise ValueError(f"Repeated dictionary destination for {row['term']}: {identity}")
        identities.add(identity)
        key = "concept:"+identity
        dest = "chapters/"+row["chapter"]+".html"+("#"+row["anchor"] if row["anchor"] else "")
        if key not in graph.nodes:
            graph.node("concept", identity, TERMS, f"/{position}", title=row["term"],
                       definition=row["definition"], url=PAGE+"#term-"+identity)
        graph.nodes[key].update(aliases=row["aliases"], subject_url=dest)
        graph.edge(key, "explained_by", "chapter:"+row["chapter"], TERMS, f"/{position}", url=dest)
    for node in graph.nodes.values():
        if node["kind"] == "concept" and node.get("definition"):
            node["dictionary_url"] = PAGE+"#term-"+node["id"].partition(":")[2]


def link_evidence(graph):
    allowed = {"illustrated_by": {"evidence_passage", "evidence_case"},
               "measured_in": {"evidence_passage", "study_run"}, "has_primary_source": {"source"}}
    for position, row in enumerate(graph.data(EVIDENCE_LINKS)):
        term, relation, target = row["term"], row["relation"], row["target"]
        if not graph.nodes[term].get("dictionary_url") or graph.nodes[target]["kind"] not in allowed[relation]:
            raise ValueError(f"Invalid dictionary evidence link at {position}")
        graph.edge(term, relation, target, EVIDENCE_LINKS, f"/{position}", evidence_effect="none")


def shell(title, intro, body, *, rendered_index=False):
    book = "../" if rendered_index else "../../../"
    graph = book + DIRECTORY if rendered_index else ""
    indexes = "" if rendered_index else book + "terminology/"
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title} · The ASI Stack</title><style>body{{font:1.05rem/1.55 system-ui,sans-serif;max-width:65rem;margin:auto;padding:1.5rem}}'
            'a{color:#165687} input{font:inherit;padding:.45rem;width:min(96%,28rem)} nav a{margin-right:.65rem} article{border-top:1px solid #aaa;padding:.4rem 0}'
            'h3{margin-bottom:.3rem} p{margin:.3rem 0 .8rem} :target{scroll-margin:1.5rem} [hidden]{display:none}</style>'
            f'<main><nav><a href="{book}index.html">Book</a><a href="{graph}index.html">Knowledge graph</a><a href="{graph}dictionary.html">Dictionary</a>'
            f'<a href="{indexes}subject-index.html">Subject index</a><a href="{indexes}concordance.html">Term occurrences</a><a href="{graph}works.html">Sources</a></nav><h1>{title}</h1><p>{intro}</p><label for="filter">Filter entries</label><br>'
            '<input id="filter" type="search"><p role="status" id="count"></p>'+body+'</main>'
            '<script>const input=document.getElementById("filter"), rows=Array.from(document.querySelectorAll("[data-entry]"));'
            'function filter(){const q=input.value.trim().toLocaleLowerCase();let n=0;for(const r of rows){r.hidden=!!q&&!r.textContent.toLocaleLowerCase().includes(q);if(!r.hidden)n++}'
            'for(const s of document.querySelectorAll("[data-group]"))s.hidden=!s.querySelector("[data-entry]:not([hidden])");'
            'document.getElementById("count").textContent=n+" matching entries"}input.addEventListener("input",filter);filter();'
            'function openDestination(){const el=document.getElementById(location.hash.slice(1));if(!el)return;if(el.tagName==="DETAILS")el.open=true;el.scrollIntoView()}'
            'window.addEventListener("hashchange",()=>{input.value="";filter();openDestination()});openDestination();</script></html>')


def dictionary_files(graph):
    nodes = {n["id"]: n for n in graph["nodes"]}
    owners = defaultdict(list)
    examples = defaultdict(list)
    for edge in graph["edges"]:
        if edge["predicate"] in ("defined_by","explained_by") and edge["to"].startswith("chapter:"):
            owners[edge["from"]].append(edge["to"])
        if edge["predicate"] in EVIDENCE_LABELS:
            examples[edge["from"]].append(dict(id=edge["to"], role=edge["predicate"], url=nodes[edge["to"]]["url"],
                                                title=nodes[edge["to"]]["title"]))
    rows = []
    for node in nodes.values():
        if not node.get("dictionary_url"):
            continue
        rows.append(dict(term=node["title"], definition=node["definition"], aliases=node.get("aliases",[]),
                         id=node["id"], url=node["dictionary_url"], chapters=list(dict.fromkeys(owners[node["id"]])),
                         passage=node.get("subject_url",node["url"]), evidence=examples[node["id"]]))
    rows.sort(key=lambda row:row["term"].casefold())
    letters = defaultdict(list)
    for row in rows:
        label = escape(row["term"])
        links = [f'<a href="../../../{escape(row["passage"])}">Read the passage</a>',
                 f'<a href="index.html?node={quote(row["id"])}">Open graph record</a>']
        for owner in row["chapters"]:
            links.append(f'<a href="../../../{nodes[owner]["url"]}">{escape(nodes[owner]["title"])}</a>')
        links.append(f'<a href="../../../terminology/concordance.html#uses-{escape(row["id"].partition(":")[2])}">Find passages using this term</a>')
        for example in row["evidence"]:
            links.append(f'<a href="../../../{escape(example["url"])}">{EVIDENCE_LABELS[example["role"]]} · {escape(example["title"])}</a>')
        aliases = ', '.join(map(escape,row['aliases']))
        fragment = escape(row["url"].split("#")[1])
        letter = row['term'][0].upper()
        letters[letter].append(f'<article data-entry id="{fragment}"><h3><a href="#{fragment}">{label}</a></h3>'
                               + (f'<p>{aliases}</p>' if aliases else '')+f'<p>{escape(row["definition"])}</p><p>{" · ".join(links)}</p></article>')
    body = '<nav aria-label="Alphabet">'+''.join(f'<a href="#letter-{escape(k)}">{escape(k)}</a>' for k in letters)+'</nav>'
    body += ''.join(f'<section data-group id="letter-{escape(k)}"><h2>{escape(k)}</h2>{"".join(v)}</section>' for k,v in letters.items())
    html = shell("AI dictionary", f'{len(rows)} definitions from the book and its technical vocabulary. Search a term, abbreviation or definition. '
                 '<a href="dictionary.json" download>Download the dictionary</a>. The subject index also lists topics without a standalone definition.', body)
    works = works_index(graph, nodes)
    return {"dictionary.html":html.encode(), "dictionary.json":(json.dumps(dict(source_commit=graph["source_commit"],terms=rows),ensure_ascii=False)+"\n").encode(),
            **works}


def works_index(graph, nodes):
    chapter_ids = defaultdict(set)
    for edge in graph["edges"]:
        if edge["predicate"] == "assigned_to":
            chapter_ids[edge["from"]].add(edge["to"])
        elif edge["predicate"] == "lists_source":
            chapter_ids[edge["to"]].add(edge["from"])
    records, entries = [], []
    sources = sorted((n for n in nodes.values() if n["kind"] == "source"), key=lambda n: (n["title"].casefold(), n["id"]))
    for node in sources:
        key = node["id"]
        records.append({"id": key, "title": node["title"], "source_record": node["url"],
                        "primary_url": node.get("primary_url"), "chapters": sorted(chapter_ids[key])})
        links = [f'<a href="../../../{escape(node["url"])}">Book source record</a>',
                 f'<a href="index.html?node={quote(key)}">Graph record</a>']
        if node.get("primary_url"):
            links.append(f'<a href="{escape(node["primary_url"])}">Primary source</a>')
        chapters = [f'<a href="../../../{escape(nodes[c]["url"])}">{escape(nodes[c]["title"])}</a>'
                    for c in sorted(chapter_ids[key])]
        destinations = f'<p>Chapter assignments · {" · ".join(chapters)}</p>' if chapters else ''
        entries.append(f'<article data-entry id="{escape(key)}"><h3>{escape(node["title"])}</h3>'
                       f'<p>{escape(key)}</p><p>{" · ".join(links)}</p>{destinations}</article>')
    intro = (f'{len(records)} sources from the book’s inventory. Find a paper or project by title, identifier or assigned chapter. '
             'Chapter assignments describe editorial placement. Each chapter bibliography provides its citation context. '
             '<a href="works.json" download>Download the source index</a>.')
    return {"works.html": shell("Index of sources", intro, "".join(entries)).encode(),
            "works.json": (json.dumps(dict(source_commit=graph["source_commit"], works=records), ensure_ascii=False)+"\n").encode()}


class Headings(HTMLParser):
    """Read section destinations from Quarto's actual main content."""
    blocks = {"p", "li", "td", "th", "figcaption", "caption", "dt", "dd"}

    def __init__(self):
        super().__init__()
        self.main = False
        self.sections = []
        self.heading = None
        self.items = []
        self.passages = defaultdict(list)
        self.block = None

    def finish_block(self):
        if self.block:
            _, anchor, chunks = self.block
            self.passages[anchor].append("".join(chunks))
        self.block = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.main = True
        if not self.main:
            return
        if tag in self.blocks:
            self.finish_block()
            anchor = next((key for key in reversed(self.sections) if key), "")
            self.block = (tag, anchor, [])
        if tag == "section":
            self.sections.append(attrs.get("id"))
        if tag in ("h2","h3","h4","h5","h6"):
            self.heading = (tag, attrs.get("id") or (self.sections[-1] if self.sections else None), [])

    def handle_data(self, data):
        if self.heading:
            self.heading[2].append(data)
        elif self.block and self.main:
            self.block[2].append(data)

    def handle_endtag(self, tag):
        if self.block and self.block[0] == tag:
            self.finish_block()
        if self.heading and tag == self.heading[0]:
            _, anchor, words = self.heading
            if anchor:
                title = " ".join("".join(words).split())
                self.items.append((anchor, title))
                self.passages[anchor].append(title)
            self.heading = None
        if self.main and tag == "section" and self.sections:
            self.sections.pop()
        if tag == "main":
            self.main = False


CHAPTER_INDEX_DIRECTORY = "agent/chapter-index"


def subject_index(site, volumes, files, commit):
    sections, data = [], []
    terms = json.loads((site/DIRECTORY/"dictionary.json").read_bytes())["terms"]
    names = defaultdict(set)
    for term in terms:
        for word in (term["term"], *term["aliases"]):
            names[word].add(term["id"])
    # Short acronyms such as IR and RL must retain case in running prose.
    forms = sorted(names, key=lambda word:(-len(word),word))
    insensitive = {word.casefold(): ids for word,ids in names.items() if not word.isupper()}
    pattern = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(w) if w.isupper() else "(?i:"+re.escape(w)+")" for w in forms) + r")(?!\w)")
    occurrences = defaultdict(list)
    for identity,title,path in volumes:
        parser = Headings()
        page = site/path
        contents = page.read_text()
        parser.feed(contents)
        if not parser.items:
            raise ValueError("No citable headings in "+path)
        headings = dict(parser.items)
        for anchor, chunks in parser.passages.items():
            labels = {match[0] for block in chunks for match in pattern.finditer(block)}
            term_ids = set().union(*(names.get(word, set()) | insensitive.get(word.casefold(), set()) for word in labels))
            for key in sorted(term_ids):
                occurrences[key].append(dict(url=path+("#"+anchor if anchor else ""), chapter=title, section=headings.get(anchor, "Opening")))
        data.append(dict(id=identity,title=title,path=path,headings=parser.items))
        items = ''.join(f'<li data-entry><a href="../{path}#{escape(anchor)}">{escape(text)}</a></li>' for anchor,text in parser.items)
        sections.append(f'<section data-group id="{escape(identity)}"><h2>{escape(title)}</h2><ul>{items}</ul></section>')
        marker = '<nav aria-label="Terminology lookup">'
        prefix = '../' * (len(path.split('/'))-1)
        links = (marker+f'<a href="{prefix}{DIRECTORY}dictionary.html">AI dictionary</a> · '
                 f'<a href="{prefix}terminology/subject-index.html#{escape(identity)}">Index of this chapter</a> · '
                 f'<a href="{prefix}{CHAPTER_INDEX_DIRECTORY}/{escape(identity)}.json">Compact section index</a></nav>')
        if '</main>' not in contents:
            raise ValueError(path)
        projected = (re.sub(re.escape(marker)+r'.*?</nav>', lambda _: links, contents, count=1, flags=re.S)
                     if marker in contents else contents.replace('</main>', links+'</main>', 1))
        if projected != contents:
            files.write(page, projected)
    groups = []
    for term in terms:
        uses = occurrences.get(term["id"], [])
        slug = term["id"].partition(":")[2]
        links = "".join(f'<li><a href="../{escape(u["url"])}">{escape(u["chapter"])} · {escape(u["section"])}</a></li>' for u in uses)
        groups.append(f'<details data-entry id="uses-{escape(slug)}"><summary>{escape(term["term"])} ({len(uses)})</summary>'
                      f'<a href="../{DIRECTORY}dictionary.html#term-{escape(slug)}">Definition</a><ul>{links}</ul></details>')
    files.write(site/"terminology"/"concordance.html", shell("AI terminology in context",
                "Find terms and aliases in headings, paragraphs, lists, captions and table cells in both editions. Short acronyms retain case. Follow a mention to read it in context. "
                '<a href="concordance.json">Download occurrences</a>.', "".join(groups), rendered_index=True))
    files.write(site/"terminology"/"concordance.json",json.dumps(dict(source_commit=commit,occurrences=occurrences),ensure_ascii=False)+"\n")
    files.write(site/"terminology"/'subject-index.html' ,shell('Book subject index',
                f'Browse every addressable section heading in {len(data)} technical chapters and Reader units. '
                '<a href="subject-index.json">Download the section index</a>.',''.join(sections), rendered_index=True))
    files.write(site/"terminology"/'subject-index.json',json.dumps(dict(source_commit=commit,volumes=data),ensure_ascii=False)+'\n')
