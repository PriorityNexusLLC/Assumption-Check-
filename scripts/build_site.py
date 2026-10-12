#!/usr/bin/env python3
"""Generate a real page for every entry, plus the JSON a future API would serve.

Why this exists: the site renders entries in the browser from Markdown shipped
in entries.js, so until JavaScript runs there is no page — nothing to link to,
nothing to cite, nothing for a search engine to read, and one URL for the whole
registry. This writes each entry out as its own HTML page with its content
already in it.

    python scripts/build_site.py           # write entry/ and api/
    python scripts/build_site.py --check    # fail if either is out of date

Output:
    entry/<num>-<slug>/index.html   the readable, citable page
    entry/<num>/index.html          a short stable URL that redirects to it
    api/entries.json                every entry in summary
    api/entries/<num>.json          one entry, in full, as structured data
    api/domains.json                the fields, and which entries sit in them
    sitemap.xml, robots.txt

The styling is taken from index.html at build time, so the design stays in one
place and these pages cannot drift from it.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import entry_model as em  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"
DOMAINS = ROOT / "domains"
SITE = ROOT / "site.json"

DEFAULTS = {
    "base_url": "https://prioritynexusllc.github.io/Assumption-Check-",
    "name": "Assumption Check",
    "tagline": "What's been tested, and what would settle it.",
    "operator": "Priority Nexus LLC",
}


def config():
    cfg = dict(DEFAULTS)
    if SITE.exists():
        cfg.update(json.loads(SITE.read_text(encoding="utf-8")))
    cfg["base_url"] = cfg["base_url"].rstrip("/")
    return cfg


def site_css():
    """The <style> block from index.html, so one stylesheet serves both."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    blocks = re.findall(r"<style>(.*?)</style>", html, re.S)
    return "\n".join(blocks)


def fonts_link():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    return "\n".join(re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*>', html))


# ------------------------------------------------------------------ rendering

def render_blocks(blocks, urls):
    out = []
    for b in blocks:
        t = b["type"]
        if t == "paragraph":
            out.append("<p>%s</p>" % em.inline(b["text"], urls))
        elif t == "bullets":
            out.append("<ul class='prose-list'>%s</ul>" % "".join(
                "<li>%s</li>" % em.inline(i["text"], urls) for i in b["items"]))
        elif t == "ordered":
            out.append("<ol class='numlist'>%s</ol>" % "".join(
                "<li><div>%s</div></li>" % em.inline(i, urls) for i in b["items"]))
        elif t == "quote":
            out.append("<blockquote class='quote'>%s</blockquote>" % em.inline(b["text"], urls))
        elif t == "code":
            out.append("<pre class='cite'><code>%s</code></pre>" % em.esc(b["text"]))
        elif t == "callout":
            kind = {"note": "note", "summary": "selfcheck", "callout": "callout"}.get(
                b["kind"], "note")
            inner = render_blocks(b["blocks"], urls)
            title = "<p class='k'>%s</p>" % em.esc(b["title"]) if b["title"] else ""
            out.append("<div class='%s'>%s%s</div>" % (kind, title, inner))
    return "\n".join(out)


def render_node(node, urls):
    pills = []
    if node.get("tier"):
        pills.append("<span class='pill tier'>%s</span>" % em.esc(node["tier"]))
    v = node.get("verification")
    if v:
        cls = {"verified at source": "v", "located not read": "u", "unlocated": "x",
               "unreadable": "u", "identity unresolved": "c"}.get(em.norm(v), "u")
        pills.append("<span class='pill %s'>%s</span>" % (cls, em.esc(v)))
    for tag in node.get("tags", []):
        cls = "pubtag pre" if "preprint" in tag.lower() else "pubtag"
        pills.append("<span class='%s'>%s</span>" % (cls, em.esc(tag)))

    details = "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (
            em.esc(d["label"] or ""), em.inline(d["text"], urls))
        for d in node.get("details", []))

    quote = ""
    if node.get("quote"):
        quote = "<div class='quote'>%s</div>" % em.inline(node["quote"], urls)

    brk = ""
    if node.get("break_before"):
        brk = "<p class='breakmark'>%s</p>" % em.esc(node["break_before"])

    classes = "node" + (" brk" if node.get("break_before") else "")
    return (
        "%s<div class='%s'><div class='yr'><span class='dot'></span>%s</div>"
        "<div class='ncard'><h3>%s</h3><div class='pills'>%s</div>"
        "<div class='cite'>%s</div>%s<dl class='meta'>%s</dl>%s</div></div>"
    ) % (
        brk, classes, em.esc(node.get("year") or ""), em.inline(node["heading"], urls),
        "".join(pills), em.inline(node.get("citation", ""), urls), quote, details,
        render_blocks(node.get("blocks", []), urls),
    )


def render_entry_body(e, urls, by_num):
    parts = []
    if e["kicker"]:
        parts.append("<p class='kicker'>%s</p>" % em.inline(e["kicker"], urls))
    parts.append("<h1>%s</h1>" % em.esc(e["title"]))
    if e["lede"]:
        parts.append("<p class='lede'>%s</p>" % em.inline(e["lede"], urls))

    parts.append("<div class='claimbox'><p class='k'>Claim as stated</p><p>%s</p></div>"
                 % em.inline(e["claim"], urls))

    pills = []
    if e["stage"]:
        cls = "pill stage" + ("" if em.norm(e["stage"]) == "traced" else " inv")
        pills.append("<span class='%s'>%s</span>" % (cls, em.esc(e["stage"])))
    if e["hypothesis"]:
        pills.append("<span class='pill a'>%s</span>" % em.esc(e["hypothesis"]))
    if e["peer_review"]:
        pills.append("<span class='pill c'>%s</span>" % em.esc(e["peer_review"]))
    if e["contested"]:
        pills.append("<span class='pill c'>Contested</span>")
    pills.append("<span class='pill %s'>%d of %d verified at source</span>" % (
        "v" if e["verified_count"] == e["node_count"] and e["node_count"] else "u",
        e["verified_count"], e["node_count"]))
    parts.append("<div class='scoreboard'>%s</div>" % "".join(pills))
    if e["stage_note"]:
        parts.append("<p class='block-note'>%s</p>" % em.inline(e["stage_note"], urls))

    # the facts strip
    def link_field(name):
        if (DOMAINS / (name + ".md")).exists():
            return "<a href='../../domain/%s/'>%s</a>" % (em.slugify(name), em.esc(name))
        return em.esc(name)

    rows = [("Subject", em.esc(e["subject"])),
            ("Field", link_field(e["domain"]) if e["domain"] else "—")]
    if e["also_in"]:
        rows.append(("Also in", " · ".join(link_field(x) for x in e["also_in"])))
    if e["rests_on"]:
        rows.append(("Rests on", " · ".join(
            "<a href='../%s-%s/'>Entry %s</a>" % (n, em.slugify(by_num[n]["title"]), n)
            if n in by_num else "Entry " + n for n in e["rests_on"])))
    if e.get("would_settle"):
        rows.append(("Would help settle", " · ".join(
            "<a href='../%s-%s/'>Entry %s</a>" % (n, em.slugify(by_num[n]["title"]), n)
            if n in by_num else "Entry " + n for n in e["would_settle"])))
    if e.get("cited_by"):
        rows.append(("Cited by", " · ".join(
            "<a href='../%s-%s/'>Entry %s</a>" % (n, em.slugify(by_num[n]["title"]), n)
            if n in by_num else "Entry " + n for n in e["cited_by"])))
    rows += [("Added", em.esc(e["added"])), ("Updated", em.esc(e["updated"]))]
    if e["author"]:
        rows.append(("Entry author", em.esc(e["author"])))
    if e["conflicts"]:
        rows.append(("Conflicts", em.esc(e["conflicts"])))
    parts.append("<dl class='metastrip'>%s</dl>" % "".join(
        "<div class='m'><dt>%s</dt><dd>%s</dd></div>" % (k, v) for k, v in rows if v))

    parts.append(render_blocks(e["preamble"], urls))
    for section in e["sections"]:
        parts.append("<h2 class='block' id='%s'>%s</h2>" % (section["id"], em.esc(section["heading"])))
        parts.append(render_blocks(section["blocks"], urls))
        if section["nodes"]:
            parts.append("<div class='chain'>%s</div>" % "".join(
                render_node(n, urls) for n in section["nodes"]))
    return "\n".join(parts)


def page(cfg, title, description, canonical, body, css, fonts, jsonld=None, depth=2):
    up = "../" * depth
    ld = "<script type='application/ld+json'>%s</script>" % json.dumps(jsonld) if jsonld else ""
    return """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%(title)s — %(site)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<meta property="og:type" content="article">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:site_name" content="%(site)s">
<meta name="twitter:card" content="summary">
%(fonts)s
<style>%(css)s</style>
%(ld)s
</head><body>
<div class="bar"><div class="bar-inner">
  <a class="wordmark" href="%(up)sindex.html"><b>%(site)s</b></a>
  <div class="bar-spacer"></div>
  <a class="navlink" href="%(up)sindex.html#registry">Registry</a>
  <a class="navlink" href="%(up)sindex.html#method">Method</a>
  <a class="navlink" href="%(up)sDomains.html">Domains</a>
  <a class="navlink" href="%(up)sindex.html#about">About</a>
</div></div>
<main class="wrap">
%(body)s
<footer>
  <span class="mono">%(site)s · %(operator)s</span>
  <span class="mono"><a href="%(canonical)s">%(canonical)s</a></span>
</footer>
</main>
</body></html>
""" % {
        "title": em.esc(title), "site": em.esc(cfg["name"]), "desc": em.esc(description),
        "canonical": em.esc(canonical), "fonts": fonts, "css": css, "ld": ld, "up": up,
        "body": body, "operator": em.esc(cfg["operator"]),
    }


# --------------------------------------------------------------------- build

def collect():
    entries, problems = {}, []
    for path in sorted(ENTRIES.glob("*.md")):
        e, probs = em.build_entry(path.name, path.read_text(encoding="utf-8"))
        problems += [p for p in probs if "domain" not in p]
        if e and not e["draft"]:
            entries[e["num"]] = e
    # cited_by is the reverse of rests_on, so each link is written once
    for e in entries.values():
        e.setdefault("cited_by_derived", [])
    for e in entries.values():
        for n in e["rests_on"]:
            if n in entries and e["num"] not in entries[n]["cited_by_derived"]:
                entries[n]["cited_by_derived"].append(e["num"])
    for e in entries.values():
        e["cited_by"] = sorted(e["cited_by_derived"])
        del e["cited_by_derived"]
    return entries, problems


def summary_of(e):
    keep = ("num", "title", "claim", "subject", "domain", "also_in", "stage", "stage_note",
            "hypothesis", "peer_review", "contested", "lifecycle", "summary", "plain_status",
            "rests_on", "cited_by", "would_settle", "not_linked", "keywords", "added", "updated",
            "author", "conflicts",
            "node_count", "verified_count", "url")
    return {k: e[k] for k in keep if k in e}


def run(check_only=False):
    cfg = config()
    entries, problems = collect()
    if problems:
        print("entries need fixing first:", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        return 1
    if not entries:
        print("no publishable entries", file=sys.stderr)
        return 1

    css, fonts = site_css(), fonts_link()
    by_num = entries
    urls = {n: "../%s-%s/" % (n, em.slugify(e["title"])) for n, e in entries.items()}
    files = {}

    for num, e in sorted(entries.items()):
        slug = "%s-%s" % (num, em.slugify(e["title"]))
        e["url"] = "%s/entry/%s/" % (cfg["base_url"], slug)
        desc = em.plain(e["summary"] or e["claim"])[:300]
        jsonld = {
            "@context": "https://schema.org",
            "@type": "ScholarlyArticle",
            "headline": e["title"],
            "about": e["subject"],
            "abstract": desc,
            "url": e["url"],
            "dateModified": e["updated"] or e["added"],
            "datePublished": e["added"],
            "publisher": {"@type": "Organization", "name": cfg["operator"]},
            "isPartOf": {"@type": "Dataset", "name": cfg["name"], "url": cfg["base_url"] + "/"},
        }
        body = render_entry_body(e, urls, by_num)
        files["entry/%s/index.html" % slug] = page(
            cfg, e["title"], desc, e["url"], body, css, fonts, jsonld, depth=2)
        # short, stable URL that survives a title change
        files["entry/%s/index.html" % num] = (
            '<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="canonical" href="%s">'
            '<meta http-equiv="refresh" content="0; url=../%s/">'
            '<title>Entry %s</title></head><body>'
            '<p>Entry %s has moved to <a href="../%s/">%s</a>.</p></body></html>\n'
            % (e["url"], slug, num, num, slug, e["title"]))
        files["api/entries/%s.json" % num] = json.dumps(e, ensure_ascii=False, indent=1) + "\n"

    files["api/entries.json"] = json.dumps(
        {"name": cfg["name"], "count": len(entries),
         "entries": [summary_of(e) for _, e in sorted(entries.items())]},
        ensure_ascii=False, indent=1) + "\n"

    fields = {}
    for e in entries.values():
        for f in [e["domain"]] + e["also_in"]:
            if f:
                fields.setdefault(f, {"field": f, "entries": []})["entries"].append(e["num"])
    files["api/domains.json"] = json.dumps(
        {"count": len(fields), "fields": [fields[k] for k in sorted(fields)]},
        ensure_ascii=False, indent=1) + "\n"

    # A page for every field an entry actually uses, so the links above resolve,
    # and an index of all 1,195 so the empty corners are visible.
    all_fields = {}
    for path in sorted(DOMAINS.glob("*.md")):
        head = path.read_text(encoding="utf-8")[:800]
        def prop(key, default=""):
            m = re.search(r"(?m)^%s:\s*(.+)$" % key, head)
            return m.group(1).strip().strip("\"'") if m else default
        all_fields[path.stem] = {
            "field": prop("field", path.stem), "core": prop("core"),
            "core_name": prop("core_name"), "sub": prop("sub"),
            "entries": fields.get(prop("field", path.stem), {}).get("entries", []),
        }

    for name, info in all_fields.items():
        if not info["entries"]:
            continue
        slug = em.slugify(info["field"])
        url = "%s/domain/%s/" % (cfg["base_url"], slug)
        rows = []
        for num in sorted(info["entries"]):
            e = entries[num]
            rows.append(
                "<button class='entry-card' onclick=\"location.href='../../entry/%s-%s/'\">"
                "<div class='top'><span class='tag domain'>%s</span>"
                "<span class='pill stage%s'>%s</span></div>"
                "<h3>%s</h3><p class='claim-line'>%s</p></button>"
                % (num, em.slugify(e["title"]), em.esc(e["subject"]),
                   "" if em.norm(e["stage"]) == "traced" else " inv", em.esc(e["stage"]),
                   em.esc(e["title"]), em.inline(e["claim"], {})))
        body = (
            "<p class='kicker'>%s. %s › %s</p><h1>%s</h1>"
            "<p class='lede'>%d registry %s filed under this field.</p>"
            "<div class='list' style='margin-top:2rem'>%s</div>"
            "<p class='herolink'><a href='../../Domains.html'>All fields →</a></p>"
            % (em.esc(info["core"]), em.esc(info["core_name"]), em.esc(info["sub"]),
               em.esc(info["field"]), len(info["entries"]),
               "entry" if len(info["entries"]) == 1 else "entries", "".join(rows)))
        files["domain/%s/index.html" % slug] = page(
            cfg, info["field"],
            "Registry entries in %s — %s." % (info["field"], cfg["tagline"]),
            url, body, css, fonts, depth=2)

    by_core = {}
    for name, info in sorted(all_fields.items(), key=lambda kv: kv[1]["field"]):
        by_core.setdefault((info["core"], info["core_name"]), []).append(info)
    sections = []
    for (core, core_name), infos in sorted(by_core.items()):
        used = [i for i in infos if i["entries"]]
        items = []
        for i in infos:
            if i["entries"]:
                items.append("<li><a href='domain/%s/'>%s</a> <span class='sub'>%d</span></li>"
                             % (em.slugify(i["field"]), em.esc(i["field"]), len(i["entries"])))
            else:
                items.append("<li><span class='fnone'>%s</span></li>" % em.esc(i["field"]))
        sections.append(
            "<h2 class='block'>%s. %s</h2><p class='block-note'>%d fields, %d with entries.</p>"
            "<ul class='prose-list' style='columns:2;'>%s</ul>"
            % (em.esc(core), em.esc(core_name), len(infos), len(used), "".join(items)))
    files["Domains.html"] = page(
        cfg, "Domains",
        "The 14 core categories of science and the %d fields beneath them." % len(all_fields),
        "%s/Domains.html" % cfg["base_url"],
        "<p class='kicker'>The map of fields</p><h1>Domains</h1>"
        "<p class='lede'>%d fields across 14 cores. A field in grey has no entry yet — "
        "which is itself worth seeing.</p>%s" % (len(all_fields), "".join(sections)),
        css, fonts, depth=0)

    urlset = (["%s/" % cfg["base_url"], "%s/Domains.html" % cfg["base_url"]]
              + [e["url"] for _, e in sorted(entries.items())]
              + ["%s/domain/%s/" % (cfg["base_url"], em.slugify(i["field"]))
                 for i in all_fields.values() if i["entries"]])
    files["sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join("  <url><loc>%s</loc></url>\n" % u for u in urlset)
        + "</urlset>\n")
    files["robots.txt"] = "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % cfg["base_url"]

    stale = []
    for rel, text in files.items():
        path = ROOT / rel
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == text:
            continue
        stale.append(rel)
        if not check_only:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")

    if check_only:
        if stale:
            print("generated pages are out of date (%d); run: python scripts/build_site.py"
                  % len(stale), file=sys.stderr)
            for rel in stale[:8]:
                print("  - " + rel, file=sys.stderr)
            return 1
        print("generated pages are up to date (%d entries)." % len(entries))
        return 0

    print("Wrote %d files for %d entries." % (len(files), len(entries)))
    return 0


if __name__ == "__main__":
    sys.exit(run("--check" in sys.argv))
