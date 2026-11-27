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


def export(read, emit, manifest, commit):
    metadata = {r["id"]:r for r in json.loads(read(METADATA))}
    inventory = {r["id"]:inventory_entry(r,metadata,commit) for r in json.loads(read("sources/source_inventory.json"))
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
    sections.append("<h2>By chapter</h2><ul>"+"".join(group(c["id"],c["title"],
                    [inventory[i] for i in c["source_ids"] if i in inventory]) for c in chapters)+"</ul>")
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
            'Study collections include the pinned experimental protocols and their direct inputs. Chapter collections contain assigned external sources.</p>'
            +"".join(sections))
