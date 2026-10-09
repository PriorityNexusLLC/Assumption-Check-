#!/usr/bin/env python3
"""Bundle entries/*.md into entries.js so the site can read them.

The page loads entries.js with a plain <script> tag, which keeps the site
working from GitHub Pages and when index.html is opened straight from disk.

    python scripts/build_entries.py          # rebuild entries.js
    python scripts/build_entries.py --check  # fail if entries.js is out of date

Each entry is checked for the fields the site needs; problems are reported by
file name so they are easy to find in Obsidian.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"
OUT = ROOT / "entries.js"

# hypothesis is optional: an entry Under Investigation gets one only once a testable form is found.
REQUIRED = ["num", "title", "claim", "peer_review", "lifecycle"]
HYPOTHESES = {"open hypothesis", "under test", "resolved supported", "resolved not supported", "resolved mixed"}
REVIEWS = {"unreviewed", "open for review", "peer reviewed"}
STAGES = {"traced", "under investigation"}


def norm(value):
    return re.sub(r"\s+", " ", re.sub(r"[—–,-]", " ", str(value).lower())).strip()


def frontmatter(text):
    """Read the flat key/value subset of YAML that Obsidian's Properties panel writes."""
    match = re.match(r"^﻿?---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not match:
        return None
    meta, list_key = {"_unquoted_colon": []}, None
    for line in match.group(1).splitlines():
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and list_key:
            meta[list_key].append(item.group(1).strip().strip("\"'"))
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip()
        list_key = None
        if value == "":
            meta[key], list_key = [], key
        else:
            if ": " in value and value[0] not in "\"'[":
                meta["_unquoted_colon"].append(key)
            meta[key] = value.strip("\"'")
    return meta


def body_after_frontmatter(text):
    m = re.match(r"^﻿?---\r?\n.*?\r?\n---[ \t]*(?:\r?\n|$)(.*)$", text, re.S)
    return m.group(1) if m else text


def node_verifications(body):
    """The 'Verification:' value under each '###' source node, lowercased."""
    return [norm(m.group(1)) for m in re.finditer(r"(?mi)^verification\s*:\s*(.+)$", body)]


def check(path, meta, body=""):
    problems = []
    if meta is None:
        return ["missing the --- properties block at the top"]
    if meta.get("draft") == "true":
        return []
    # Stage rule: an entry is "Traced" only when every chain node is verified at
    # source. Any node still needing original source data keeps it Under Investigation.
    if meta.get("stage") and norm(meta["stage"]) == "traced":
        unverified = [v for v in node_verifications(body) if v and v != "verified at source"]
        if unverified:
            problems.append(
                "stage is Traced but a chain node is not verified at source "
                f"({', '.join(sorted(set(unverified)))}); use Under Investigation until every "
                "node is Verified at source"
            )
    for key in REQUIRED:
        if not meta.get(key):
            problems.append(f"'{key}' is empty")
    if meta.get("num") and not re.fullmatch(r"\d+", str(meta["num"])):
        problems.append(f"'num' should be digits, like 002 (got {meta['num']!r})")
    if meta.get("hypothesis") and norm(meta["hypothesis"]) not in HYPOTHESES:
        problems.append(
            f"'hypothesis' is {meta['hypothesis']!r}; use one of: Open Hypothesis, Under Test, "
            "Resolved — Supported, Resolved — Not supported, Resolved — Mixed"
        )
    if meta.get("stage") and norm(meta["stage"]) not in STAGES:
        problems.append(f"'stage' is {meta['stage']!r}; use Traced or Under Investigation")
    for key in meta["_unquoted_colon"]:
        problems.append(f"'{key}' contains ': ' — put double quotes around the whole value")
    if meta.get("peer_review") and norm(meta["peer_review"]) not in REVIEWS:
        problems.append(
            f"'peer_review' is {meta['peer_review']!r}; use one of: Unreviewed, Open for review, Peer reviewed"
        )
    return problems


def build():
    sources, problems, nums = [], [], {}
    for path in sorted(ENTRIES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        problems += [f"{path.name}: {p}" for p in check(path, meta, body_after_frontmatter(text))]
        if meta and meta.get("draft") != "true" and meta.get("num"):
            num = str(meta["num"]).zfill(3)
            if num in nums:
                problems.append(f"{path.name}: entry number {num} is also used by {nums[num]}")
            nums[num] = path.name
        sources.append({"name": path.name, "text": text})
    body = json.dumps(sources, ensure_ascii=False, indent=1)
    js = (
        "// Generated by scripts/build_entries.py from entries/*.md. Do not edit by hand:\n"
        "// change the Markdown files and this file is rebuilt.\n"
        f"window.ENTRY_SOURCES = {body};\n"
    )
    return js, problems, len(sources)


def main():
    js, problems, count = build()
    if problems:
        print("Entries need fixing before they can be published:", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        sys.exit(1)
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != js:
            print("entries.js is out of date; run: python scripts/build_entries.py", file=sys.stderr)
            sys.exit(1)
        print("entries.js is up to date.")
        return
    OUT.write_text(js, encoding="utf-8")
    print(f"Wrote {OUT.name} from {count} file(s).")


if __name__ == "__main__":
    main()
