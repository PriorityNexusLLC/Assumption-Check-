#!/usr/bin/env python3
"""Create or refresh the domain notes in domains/ from the science list.

The notes are the database: once written they are ordinary Obsidian notes you
can edit, link and write in. This script only ever rewrites the frontmatter
block that records where a field sits in the taxonomy — anything you write in
the body is left alone, so it is safe to re-run.

    python scripts/make_domains.py            # create or refresh notes
    python scripts/make_domains.py --check    # fail if any note is missing or stale

Source: scripts/science-list.json, extracted from "Science List.docx"
(14 cores, 117 sub-groups, 1198 field entries / 1195 unique names).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / "science-list.json"
DOMAINS = ROOT / "domains"
INDEX = ROOT / "Domains.md"

ILLEGAL = re.compile(r'[\\/:*?"<>|]')


def filename_for(field):
    """A field name that is safe on every filesystem; the true name stays in frontmatter."""
    return ILLEGAL.sub(" - ", field).strip()


def yaml_value(text):
    text = str(text)
    return '"%s"' % text.replace('"', '\\"') if re.search(r'[:#\[\]{}&*!|>%@`"\']', text) else text


def load():
    """field name -> {name, placements:[(core_n, core_name, sub)]} in list order."""
    cores = json.loads(SOURCE.read_text(encoding="utf-8"))
    fields = {}
    for core in cores:
        for sub in core["subs"]:
            for name in sub["fields"]:
                rec = fields.setdefault(name, {"name": name, "placements": []})
                place = (core["n"], core["name"], sub["name"])
                if place not in rec["placements"]:
                    rec["placements"].append(place)
    return cores, fields


def frontmatter_for(rec):
    (core_n, core_name, sub) = rec["placements"][0]
    lines = [
        "---",
        "type: domain",
        "field: %s" % yaml_value(rec["name"]),
        "core: %s" % str(core_n).zfill(2),
        "core_name: %s" % yaml_value(core_name),
        "sub: %s" % yaml_value(sub),
    ]
    extra = rec["placements"][1:]
    if extra:
        lines.append("also_in:")
        for (n, cname, s) in extra:
            lines.append("  - %s" % yaml_value("%s › %s" % (str(n).zfill(2) + " " + cname, s)))
    fname = filename_for(rec["name"])
    if fname != rec["name"]:
        lines.append("aliases:")
        lines.append("  - %s" % yaml_value(rec["name"]))
    lines.append("entries: []")
    lines.append("---")
    return "\n".join(lines)


def body_for(rec):
    (core_n, core_name, sub) = rec["placements"][0]
    trail = "%s. %s › %s" % (str(core_n).zfill(2), core_name, sub)
    out = ["", "# %s" % rec["name"], "", "*%s*" % trail, ""]
    for (n, cname, s) in rec["placements"][1:]:
        out += ["*Also listed under %s. %s › %s*" % (str(n).zfill(2), cname, s), ""]
    out += [
        "Registry entries filed under this field appear here on the site, and in this",
        "note's backlinks once an entry links to it.",
        "",
        "## Notes",
        "",
        "",
    ]
    return "\n".join(out)


def split_existing(text):
    """(frontmatter, body) for a note already on disk."""
    m = re.match(r"^﻿?(---\r?\n.*?\r?\n---)[ \t]*\r?\n?(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else (None, text)


def run(check_only=False):
    if not SOURCE.exists():
        print("missing %s" % SOURCE, file=sys.stderr)
        return 1
    cores, fields = load()
    DOMAINS.mkdir(exist_ok=True)

    written, stale, created = 0, [], 0
    for rec in fields.values():
        path = DOMAINS / (filename_for(rec["name"]) + ".md")
        want_fm = frontmatter_for(rec)
        if path.exists():
            have_fm, body = split_existing(path.read_text(encoding="utf-8"))
            if have_fm == want_fm:
                continue
            new = want_fm + "\n" + body
            stale.append(path.name)
        else:
            new = want_fm + body_for(rec)
            created += 1
            stale.append(path.name)
        if not check_only:
            path.write_text(new, encoding="utf-8", newline="\n")
            written += 1

    index = index_text(cores)
    have_index = INDEX.read_text(encoding="utf-8") if INDEX.exists() else None
    if have_index != index:
        stale.append(INDEX.name)
        if not check_only:
            INDEX.write_text(index, encoding="utf-8", newline="\n")

    if check_only:
        if stale:
            print("domain notes are out of date (%d); run: python scripts/make_domains.py"
                  % len(stale), file=sys.stderr)
            for name in stale[:10]:
                print("  - " + name, file=sys.stderr)
            return 1
        print("domain notes are up to date (%d fields)." % len(fields))
        return 0

    print("Domains: %d fields (%d notes written, %d new)." % (len(fields), written, created))
    return 0


def index_text(cores):
    out = [
        "# Domains",
        "",
        "The 14 core categories of science, their sub-groups, and every field beneath them.",
        "One note per field lives in `domains/`. An entry's `domain:` property names one of",
        "these fields; its core and sub-group follow from this list, so they cannot drift.",
        "",
        "Generated by `scripts/make_domains.py` from `scripts/science-list.json`.",
        "",
    ]
    total = 0
    for core in cores:
        n = str(core["n"]).zfill(2)
        count = sum(len(s["fields"]) for s in core["subs"])
        total += count
        out.append("## %s. %s" % (n, core["name"]))
        out.append("")
        if core.get("desc"):
            out.append("%s" % core["desc"])
            out.append("")
        for sub in core["subs"]:
            out.append("**%s**" % sub["name"])
            out.append("")
            for field in sub["fields"]:
                fname = filename_for(field)
                label = "" if fname == field else "|%s" % field
                out.append("- [[%s%s]]" % (fname, label))
            out.append("")
    out.insert(6, "%d fields across %d sub-groups." % (total, sum(len(c["subs"]) for c in cores)))
    out.insert(7, "")
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(run("--check" in sys.argv))
