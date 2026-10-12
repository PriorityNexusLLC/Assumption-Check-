#!/usr/bin/env python3
"""Find the connections between entries that nobody has written down yet.

Run it while drafting, before an entry is called finished. For each pair of
entries it reports what they actually have in common — the same source, the
same field, the same subject — and whether that connection is declared in
`rests_on` / `cited_by`. An overlap nobody declared is the thing to look at:

    does it belong here, or is it part of an existing entry?
    does it relate, and should the map draw an edge?
    does it answer a test another entry left open?
    does another entry rest on it?

The script never decides any of that. It surfaces the overlap and leaves the
judgement to a person, because "these two cite the same paper" is a fact and
"these two belong together" is an editorial call.

    python scripts/connections.py              # undeclared connections only
    python scripts/connections.py --all        # every connection, declared or not
    python scripts/connections.py --entry 004  # just one entry's neighbourhood
"""
import io
import re
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"

DOI = re.compile(r"10\.\d{4,9}/[^\s)\]|<>\"]+")
STOP = {"the", "and", "for", "that", "with", "from", "this", "not", "are", "was", "has"}


def read_entries():
    out = {}
    for path in sorted(ENTRIES.glob("*.md")):
        text = io.open(path, encoding="utf-8").read()
        m = re.search(r'(?m)^num:\s*"?(\d+)"?', text)
        if not m:
            continue
        num = m.group(1).zfill(3)

        def one(key):
            mm = re.search(r"(?m)^%s:\s*(.*)$" % key, text)
            return (mm.group(1).strip().strip("\"'") if mm else "")

        def many(key):
            mm = re.search(r"(?m)^%s:\s*\n((?:[ \t]+-[ \t]*.+\n)+)" % key, text)
            if not mm:
                inline = one(key)
                if inline and inline not in ("[]", ""):
                    return [x.strip() for x in re.split(r"[·,]", inline) if x.strip()]
                return []
            return [re.sub(r"^[ \t]+-[ \t]*", "", ln).strip().strip("\"'")
                    for ln in mm.group(1).splitlines() if ln.strip()]

        body = text.split("---", 2)[-1]
        out[num] = {
            "num": num,
            "file": path.name,
            "title": one("title"),
            "subject": one("subject"),
            "claim": one("claim"),
            "draft": one("draft").lower() == "true",
            "domain": one("domain"),
            "also_in": many("also_in"),
            "keywords": [k.lower() for k in many("keywords")],
            "rests_on": [x.zfill(3) for x in many("rests_on") if x.strip("[] ")],
            "cited_by": [x.zfill(3) for x in many("cited_by") if x.strip("[] ")],
            "dois": {d.rstrip(".").lower() for d in DOI.findall(text)},
            "settle": settle_text(body),
        }
    return out


def settle_text(body):
    """The 'What would settle it' section, where one entry's open test may be another's claim."""
    m = re.search(r"(?ms)^##\s*What would settle it\s*$(.*?)(?=^##\s|\Z)", body)
    return re.sub(r"\s+", " ", m.group(1)).strip().lower() if m else ""


def fields(entry):
    return {entry["domain"]} | set(entry["also_in"]) - {""}


def rarity(entries):
    """How many entries sit in each field. A field shared by most entries says
    little; a field shared by two says a lot. Same idea as weighting a word by
    how rare it is."""
    counts = {}
    for e in entries.values():
        for f in fields(e):
            if f:
                counts[f] = counts.get(f, 0) + 1
    return counts


def overlap(a, b):
    """What two entries genuinely share."""
    shared_fields = sorted(f for f in fields(a) & fields(b) if f)
    shared_dois = sorted(a["dois"] & b["dois"])
    shared_kw = sorted((set(a["keywords"]) & set(b["keywords"])) - STOP)
    same_subject = a["subject"] and a["subject"].lower() == b["subject"].lower()

    # does one entry's open test name the other's subject?
    answers = []
    for x, y in ((a, b), (b, a)):
        subj = (y["subject"] or "").lower()
        if subj and len(subj) > 4 and x["settle"] and subj in x["settle"]:
            answers.append("%s's open test names %s's subject" % (x["num"], y["num"]))
    return shared_fields, shared_dois, shared_kw, same_subject, answers


def declared(a, b):
    return b["num"] in a["rests_on"] + a["cited_by"] or a["num"] in b["rests_on"] + b["cited_by"]


def main(argv):
    show_all = "--all" in argv
    only = None
    if "--entry" in argv:
        only = argv[argv.index("--entry") + 1].zfill(3)

    entries = read_entries()
    if not entries:
        print("no entries found", file=sys.stderr)
        return 1
    counts = rarity(entries)

    rows, undeclared = [], 0
    for a, b in combinations(sorted(entries), 2):
        if only and only not in (a, b):
            continue
        ea, eb = entries[a], entries[b]
        f, d, k, same, answers = overlap(ea, eb)

        # Strength: a shared source or subject is hard evidence; a shared field
        # counts only as far as that field is specific to these two.
        narrow = [x for x in f if counts.get(x, 0) <= 3]
        broad = [x for x in f if counts.get(x, 0) > 3]
        score = 5 * len(d) + (6 if same else 0) + 3 * len(answers) + 2 * len(narrow) + len(k)
        if not show_all and score < 3:
            continue
        if not (f or d or same or answers or len(k) >= 2):
            continue
        is_declared = declared(ea, eb)
        if is_declared and not show_all:
            continue
        if not is_declared:
            undeclared += 1
        rows.append((score, a, b, narrow, broad, d, k, same, answers, is_declared))

    if not rows:
        print("No undeclared connections. Every overlap between entries is written down.")
        return 0

    rows.sort(key=lambda r: (-r[0], r[1], r[2]))
    print("Connections between entries%s, strongest first\n"
          % (" (all)" if show_all else " not yet declared"))
    for score, a, b, narrow, broad, d, k, same, answers, is_declared in rows:
        ea, eb = entries[a], entries[b]
        mark = "declared" if is_declared else "NOT DECLARED"
        print("%s  %s" % (a, ea["title"]))
        print("%s  %s      [%s]" % (b, eb["title"], mark))
        if same:
            print("    same subject: %s  — check these are not one entry" % ea["subject"])
        if d:
            print("    shares %d source%s: %s" % (len(d), "" if len(d) == 1 else "s", ", ".join(d)))
        if narrow:
            print("    shares %s — %s" % (
                ", ".join(narrow),
                "a field only these entries use" if all(counts[x] == 2 for x in narrow)
                else "a narrow field"))
        if broad:
            print("    also both in %s (%s)" % (
                ", ".join(broad),
                ", ".join("%d entries" % counts[x] for x in broad)))
        if k and len(k) >= 2:
            print("    shares keywords: %s" % ", ".join(k[:6]))
        for line in answers:
            print("    %s" % line)
        print()

    print("%d connection%s to decide on." % (undeclared, "" if undeclared == 1 else "s"))
    print("Record the real ones in `rests_on` (this entry depends on that one);")
    print("`cited_by` fills itself in on the other entry and the map draws the edge.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
