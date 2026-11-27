"""Export citation-manager records from the public inventory and verified publisher metadata."""
from html import escape
import json
import re

BOOK = "https://corbensorenson.github.io/asi-stack-book/"
REPO = "https://github.com/corbensorenson/asi-stack-book/blob/"
METADATA = "sources/bibliographic_metadata.json"


def issued(value):
    match = re.match(r"(\d{4})(?:[-/](\d{1,2}))?(?:[-/](\d{1,2}))?", value or "")
    return {"date-parts": [[int(v) for v in match.groups() if v]]} if match else None


def inventory_entry(source, metadata, commit):
    key = source["id"]
    meta = metadata.get(key, {})
    kind = source.get("source_type", "")
    venue = meta.get("venue") or ""
    if kind in ("book", "arxiv_book"):
        csl_type = "book"
    elif venue == "arXiv":
        csl_type = "article"
    elif "journal" in kind or venue == "Proceedings of the VLDB Endowment":
        csl_type = "article-journal"
    elif kind in ("conference_paper", "conference_paper_pdf", "workshop_paper", "arxiv_and_conference") or venue.startswith(("Proceedings of the", "Findings of the")):
        csl_type = "paper-conference"
    elif "report" in kind:
        csl_type = "report"
    elif "standard" in kind or "specification" in kind or kind == "informational_rfc":
        csl_type = "standard"
    elif "preprint" in kind or "paper" in kind or kind in ("arxiv", "research_article"):
        csl_type = "article"
    elif kind == "software_repository":
        csl_type = "software"
    else:
        csl_type = "webpage"
    note = f'Source note: {REPO}{commit}/sources/source_notes/{key}.md. Source used: {meta.get("version_used",source["url"])}.'
    if meta:
        note += " Bibliographic metadata: "+meta["metadata_url"]
    else:
        note += " Inventory record. Authorship has not been verified for this export."
    record = dict(id=key, type=csl_type, title=meta.get("title",source["title"]),
                  URL=meta.get("metadata_url",source["url"]), note=note)
    if authors := meta.get("authors"):
        # Publisher bylines may use different name order and corporate authors.
        # Literal names preserve the original byline without guessing family names.
        record["author"] = []
        for name in authors:
            if name.count(", ") == 1:
                family, given = name.split(", ", 1)
                record["author"].append({"family":family, "given":given})
            else:
                record["author"].append({"literal":name})
    for field, value in [("container-title",meta.get("venue")), ("DOI",re.sub(r"^https?://(?:dx\.)?doi\.org/", "", meta.get("doi") or source.get("doi") or "", flags=re.I)),
                         ("issued",issued(meta.get("date") or source.get("published")))]:
        if value:
            record[field] = value
    return record


def tex(value):
    return "".join({"\\":r"\textbackslash{}", "{":r"\{", "}":r"\}", "&":r"\&", "%":r"\%",
                    "#":r"\#", "_":r"\_", "$":r"\$"}.get(c,c) for c in value)


def bibtex(record):
    kind = {"paper-conference": "inproceedings", "article-journal": "article", "book": "book", "report": "techreport"}.get(record["type"],"misc")
    fields = {"title":"{"+tex(record["title"])+"}", "url":record["URL"]}
    if record.get("author"):
        fields["author"] = " and ".join(("{"+tex(a["literal"])+"}" if "literal" in a else tex(a["family"])+", "+tex(a["given"])) for a in record["author"])
    if record.get("issued"):
        fields["year"] = str(record["issued"]["date-parts"][0][0])
    if record.get("container-title"):
        field = {"inproceedings":"booktitle","article":"journal"}.get(kind,"howpublished")
        fields[field] = tex(record["container-title"])
    if record.get("DOI"):
        fields["doi"] = record["DOI"]
    fields["note"] = tex(record["note"])
    return "@"+kind+"{"+record["id"]+",\n"+",\n".join(f"  {k} = {{{v}}}" for k,v in fields.items())+"\n}\n"


def normalize_url(value):
    value = value.rstrip(".,")
    match = re.search(r"arxiv\.org/(?:abs|pdf|html)/([0-9]+\.[0-9]+)", value)
    return "arxiv:" + match[1] if match else value.split("#")[0].rstrip("/")


def heading_anchor(title):
    explicit = re.search(r"\{#([^}\s]+)[^}]*\}\s*$", title)
    if explicit:
        return explicit[1]
    plain = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
    cleaned = re.sub(r"[^\w. -]", "", plain.lower()).strip()
    return re.sub(r"^[^a-z]+", "", cleaned).replace(" ", "-")


def chapter_entries(chapter, text, sources, records, urls, originals, reviewed):
    anchors = {}
    coverage = {}
    heading, anchor, fence = "Opening decision", "", ""
    lines = text.split("---\n", 2)[-1].splitlines()
    for line in lines:
        if re.match(r"^\s*(?:```|~~~)", line):
            fence = "" if fence else line.strip()[:3]
            continue
        if fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+)$", line)
        if match:
            heading = re.sub(r"\s*\{[^}]*\}\s*$", "", match[1])
            slug = heading_anchor(match[1])
            count = anchors.get(slug, 0)
            anchors[slug] = count + 1
            anchor = slug if not count else f"{slug}-{count}"
        ids = set(re.findall(r"\bext_[a-zA-Z0-9_]+\b", line))
        ids.update(re.findall(r"`([a-z][a-z0-9_]+)`", line))
        for link in re.findall(r"\]\(([^ )]+)", line):
            if (sid := urls.get(normalize_url(link))):
                ids.add(sid)
            paper = re.search(r"(?:^|/)papers/([\w-]+)\.(?:html|qmd)", link)
            if paper and paper[1] in originals:
                ids.add(paper[1])
        for sid in sorted(ids & sources.keys()):
            context = (heading + " " + line).lower()
            mapping = anchor in {"chapter-status","source-crosswalk","external-literature-queue","manifest-source-assignment-reconciliation","claim-source-mapping-status"}
            if mapping:
                role = "Source mapping"
            elif (sid, anchor) in reviewed:
                role = "Reported evidence"
            elif any(term in context for term in ("research lead", "unreviewed", "pending review", "recovery only")):
                role = "Research lead"
            elif "comparator" in context or "why existing approaches" in heading.lower() or "baseline" in heading.lower():
                role = "Comparator"
            elif sid in originals:
                role = "Original work"
            elif any(term in context for term in ("reported", "authors", "measured", "evaluated", "scored")):
                role = "Reported evidence"
            else:
                role = "Passage reference"
            coverage.setdefault(sid, {}).setdefault((anchor, role), heading)
    for (sid, slug), items in reviewed.items():
        if slug not in anchors:
            raise ValueError(f"Missing reviewed bibliography passage: {chapter['id']}#{slug}")
        places = coverage.setdefault(sid,{})
        if (slug,"Reported evidence") not in places:
            places[slug,"Reported evidence"] = slug.replace("-"," ")
    ordered = dict.fromkeys([*chapter["source_ids"], *coverage])
    entries, items = [], []
    for sid in ordered:
        source = sources[sid]
        external = source["priority"] == "external_literature"
        if external:
            record = records[sid].copy()
        else:
            url = BOOK + ("papers/" + sid + ".html" if sid in originals else
                          "products/evidence-registry/knowledge-graph/?node=source:" + sid)
            record = dict(id=sid, title=source["title"], type="report" if sid in originals else "document",
                          URL=url, note="Book project paper or artifact.")
        places = coverage.get(sid, {})
        substantive = any(role != "Source mapping" for _, role in places)
        kind = ("Book paper or artifact" if not external else
                "Cited in passage" if substantive else "Assigned background" if sid in chapter["source_ids"] else "Source mapping")
        label = f'<a href="{escape(record["URL"])}">{escape(record["title"])}</a>'
        links, notes = [], []
        for (slug, role), title in places.items():
            dest = BOOK + chapter["file"].replace(".qmd",".html") + ("#" + slug if slug else "")
            links.append(f'<a href="{escape(dest)}">{escape(title)}</a> ({role})')
            notes.append(f"{role}: {title} {dest}")
        for (source, slug), details in reviewed.items():
            if source != sid:
                continue
            for d in details:
                explanation = " · ".join(d[k] for k in ("comparison","quantity","scope"))
                links.append(f'<a href="{escape(d["url"])}">{escape(d["locator"])}</a> · {escape(explanation)}')
                notes.append(d["locator"]+" "+d["url"]+" · "+explanation)
        record["note"] += " Chapter use: " + kind + ". " + " | ".join(notes)
        entries.append(record)
        items.append(f'<li>{label} · {kind}' + ('<ul><li>'+'</li><li>'.join(links)+'</li></ul>' if links else '')+'</li>')
    return entries, items


def export(read, emit, manifest, commit):
    metadata = {r["id"]:r for r in json.loads(read(METADATA))}
    sources = {r["id"]:r for r in json.loads(read("sources/source_inventory.json"))}
    inventory = {r["id"]:inventory_entry(r,metadata,commit) for r in sources.values()
                 if r["priority"]=="external_literature"}
    sections = []
    def group(key, title, entries):
        records = list({r["id"]:r for r in entries}.values())
        emit(key+".json",json.dumps(records,indent=2,ensure_ascii=False)+"\n")
        emit(key+".bib","\n".join(bibtex(r) for r in records))
        return (f'<li id="{escape(key)}">{escape(title)} ({len(records)}) · '
                f'<a download href="{key}.bib">BibTeX</a> · <a download href="{key}.json">CSL-JSON</a></li>')
    sections.append("<h2>External sources</h2><ul>"+group("external","Complete external source inventory",inventory.values())+"</ul>")
    chapters = [c for p in json.loads(read("book_structure.json"))["parts"] for c in p["chapters"]]
    originals = {r["source_id"] for r in json.loads(read("papers/paper_library.json"))["records"]}
    urls = {normalize_url(url):sid for sid, source in sources.items()
            for url in (source.get("url"), metadata.get(sid,{}).get("metadata_url")) if url}
    evidence = {}
    for row in json.loads(read("products/worked_source_locators.json")):
        if row["source"] not in sources:
            raise ValueError("Unknown source "+row["source"])
        evidence.setdefault(row["chapter"],{}).setdefault((row["source"],row["anchor"]),[]).append(row)
    chapter_links = []
    for c in chapters:
        entries, items = chapter_entries(c, read(c["file"]).decode(), sources, inventory, urls, originals, evidence.get(c["id"],{}))
        details = c["id"]+".html"
        title = escape(c["title"])
        chapter_links.append(group(c["id"], c["title"], entries).replace("</li>", f' · <a href="{details}">Passages and roles</a></li>'))
        emit(details, '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
             f'<title>{title} · References</title><main><p><a href="index.html">Bibliographies</a></p><h1>{title}</h1>'
             f'<p><a href="{c["id"]}.bib">BibTeX</a> · <a href="{c["id"]}.json">CSL-JSON</a></p><ol>'
             + "".join(items) + "</ol></main></html>")
    sections.append("<h2>By chapter</h2><ul>"+"".join(chapter_links)+"</ul>")
    study_links = []
    for s in manifest["studies"]:
        sid = s["id"]
        entries = []
        def add(key,title,url,kind,description,author=None):
            record = dict(id=key,title=title,URL=url,type=kind,note=description)
            if author:
                record["author"] = [{"literal":author}]
            entries.append(record)
        for run in manifest["runs"]:
            if run["study"] == sid:
                add("run-"+run["id"],run["title"],REPO+run["source_commit"]+"/"+run["protocol"],"report",
                    "Protocol for the retained run. Result SHA-256 "+run["result_sha256"])
                entries[-1]["issued"] = issued(run["date"])
        if sid in ("scientific-citation","citation-retrieval"):
            entries.append(inventory["ext_scifact_2020"])
            add("minilm-nli-release","NLI MiniLM2 L6 H768","https://huggingface.co/cross-encoder/nli-MiniLM2-L6-H768/tree/b95119ce93d3e065de6214e38cd4a97b0f2f2c6d","software","Pinned model release used for inference.")
        if sid=="citation-retrieval":
            entries.append(inventory["ext_scifact_open_2022"])
            entries.append(dict(id="lukens-nlrp12-2015", type="article-journal",
                title="The NLRP12 Sensor Negatively Regulates Autoinflammatory Disease by Modulating Interleukin-4 Production in T Cells",
                author=[{"family":family,"given":given} for family,given in [
                    ("Lukens","JR"),("Gurung","P"),("Shaw","PJ"),("Barr","MJ"),("Zaki","MH"),
                    ("Brown","SA"),("Vogel","P"),("Chi","H"),("Kanneganti","TD")]],
                DOI="10.1016/j.immuni.2015.03.006", URL="https://pubmed.ncbi.nlm.nih.gov/25888258/",
                issued=issued("2015"), note="Claim 833 deciding paper. Author list from PubMed record 25888258.",
                **{"container-title":"Immunity"}))
            add("scifact-open-data","SciFact-Open archive","https://scifact.s3.us-west-2.amazonaws.com/scifact-open/latest/scifact_open.tar.gz","dataset","Archive SHA-256 8f4dc238b2eff422bab5c7918fcbddb6996b29d37cb887942ef6ee1a16fb3415.")
        if sid=="forward-transfer":
            upstream = json.loads(read("experiments/sygus_forward_transfer/inputs.json"))
            add("sygus-2017-general-hd", "SyGuS 2017 General Track Hacker’s Delight benchmarks",
                upstream["repository"]+"/tree/"+upstream["revision"]+"/comp/2017/General_Track",
                "dataset", "Pinned upstream tasks. The external protocol freezes the selected files and their SHA-256 digests.", "SyGuS-Org")
            add("forward_transfer_program_synthesis","From Compression to Forward Transfer: Evaluating Reusable Knowledge in Program Synthesis",BOOK+s["paper"],"report","Original August 2026 manuscript with collaborator credits preserved.","Corben Sorenson")
        if sid=="claim-review":
            add("answerability_atlas_synthesis","What an Answerability Atlas Can and Cannot Do",BOOK+"papers/answerability_atlas_synthesis.html","report","Audited synthesis, October 2026. The study protocol identifies the superseded and corrected comparisons.","Answerability Atlas Project")
        if sid=="crossed-receiver":
            for key,url,title in [
                ("npm-lock","https://github.com/npm/cli/blob/977fd5784f875fdc2e3436ed15c444ddca63e3d7/package-lock.json","npm CLI pinned dependency lock"),
                ("npm-lock-format","https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json/","npm CLI v10 package-lock format"),
                ("jsdelivr","https://www.jsdelivr.com/documentation","jsDelivr documentation"),("unpkg","https://unpkg.com/","UNPKG package delivery")]:
                add(key,title,url,"webpage","Primary source recorded in the package-observation protocol.")
        if sid=="matched-release":
            for task in json.loads(read("experiments/matched_publication_boundary/cohort.json")):
                add("release-"+task["repo"].replace("/","-"),task["repo"]+" README",task["url"],"software",
                    "Release input at "+task["revision"]+". SHA-256 "+task["sha256"])
        study_links.append(group("study-"+sid,s["title"],entries))
    sections.insert(1,"<h2>By study</h2><ul>"+"".join(study_links)+"</ul>")
    return (f'<p>{len(metadata)} external records have publisher bylines checked against the work title. '
            'Other records retain available inventory fields. Source notes identify which edition or data release informed the chapter. '
            'Study collections include the pinned experimental protocols and their direct inputs. Chapter collections distinguish cited passages, assigned background, and project papers or artifacts. Each passage link identifies how the chapter uses the work.</p>'
            +"".join(sections))
