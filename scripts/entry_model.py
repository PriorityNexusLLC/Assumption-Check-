#!/usr/bin/env python3
"""Parse entries/*.md into the structured form the site and the JSON API share.

This is the single place an entry's Markdown is understood. The build renders
HTML from this model and writes the same model to api/*.json, so a later
server-backed version can serve those shapes without the front end changing.

Nothing here reaches the network or the clock: parsing an entry twice gives the
same bytes, which is what lets the build check itself in CI.
"""
import re
import unicodedata

# Frontmatter keys the site needs; `hypothesis` stays optional because an entry
# Under Investigation earns one only once a testable form of the claim is found.
REQUIRED = ["num", "title", "claim", "peer_review", "lifecycle"]
HYPOTHESES = {
    "open hypothesis",
    "under test",
    "resolved supported",
    "resolved not supported",
    "resolved mixed",
}
REVIEWS = {"unreviewed", "open for review", "peer reviewed"}
STAGES = {"traced", "under investigation"}
VERIFICATIONS = {
    "verified at source",
    "located not read",
    "unlocated",
    "unreadable",
    "identity unresolved",
}
LIST_KEYS = {"rests_on", "cited_by", "keywords", "cross_links"}


def norm(value):
    """Lowercase and flatten dashes/commas, so 'Resolved — Mixed' == 'resolved mixed'."""
    return re.sub(r"\s+", " ", re.sub(r"[—–,-]", " ", str(value).lower())).strip()


def slugify(text):
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)


# ---------------------------------------------------------------- frontmatter

def split_frontmatter(text):
    """Return (meta, body). Mirrors the flat YAML subset Obsidian's Properties panel writes."""
    match = re.match(r"^﻿?---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)(.*)$", text, re.S)
    if not match:
        return None, text
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
        elif value in ("[]", "''", '""'):
            meta[key] = []
        else:
            if ": " in value and value[0] not in "\"'[":
                meta["_unquoted_colon"].append(key)
            meta[key] = value.strip("\"'")
    return meta, match.group(2)


# ------------------------------------------------------------------- inline md

def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def inline(text, entry_urls=None):
    """Bold, italic, code, links and [[wikilinks]] — the subset entries actually use."""
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)

    def wiki(m):
        target, label = m.group(1), m.group(2) or m.group(1)
        num = re.match(r"\s*(\d{3})", target)
        href = (entry_urls or {}).get(num.group(1)) if num else None
        if href:
            return f'<a href="{href}">{label.strip()}</a>'
        return label.strip()

    out = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", wiki, out)
    out = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: '<a href="%s"%s>%s</a>'
        % (
            esc(m.group(2)),
            ' target="_blank" rel="noopener"' if m.group(2).startswith("http") else "",
            m.group(1),
        ),
        out,
    )
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    return out


def plain(text):
    """Strip markup for meta descriptions and the search index."""
    out = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), str(text))
    out = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", out)
    out = re.sub(r"[*`>#]", "", out)
    return re.sub(r"\s+", " ", out).strip()


# -------------------------------------------------------------------- blocks

CALLOUT = re.compile(r"^>\s*\[!(\w+)\]\s*(.*)$")


def parse_blocks(lines, entry_urls=None):
    """Group body lines into blocks: paragraph, bullets, ordered, quote, callout, code."""
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        m = CALLOUT.match(line)
        if m:
            kind, title, body = m.group(1).lower(), m.group(2).strip(), []
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            blocks.append({"type": "callout", "kind": kind, "title": title,
                           "blocks": parse_blocks(body, entry_urls)})
            continue

        if line.startswith(">"):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            blocks.append({"type": "quote", "text": " ".join(x.strip() for x in body).strip()})
            continue

        if line.startswith("```"):
            fence, body = line[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            blocks.append({"type": "code", "lang": fence, "text": "\n".join(body)})
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                indent = len(lines[i]) - len(lines[i].lstrip())
                items.append({"depth": 1 if indent >= 2 else 0,
                              "text": re.sub(r"^\s*[-*]\s+", "", lines[i]).rstrip()})
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).rstrip())
                i += 1
            blocks.append({"type": "ordered", "items": items})
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{2,3}\s|>|```|\s*[-*]\s+|\s*\d+\.\s+)", lines[i]
        ):
            para.append(lines[i].strip())
            i += 1
        if para:
            blocks.append({"type": "paragraph", "text": " ".join(para)})
        else:
            i += 1
    return blocks


NODE_META = re.compile(r"^(Tier|Verification|Tags)\s*:\s*(.*)$", re.I)


def parse_node(heading, lines, entry_urls=None):
    """One '###' source inside a chain: its badges, citation, quote and detail bullets."""
    node = {"heading": heading, "year": None, "tier": None, "verification": None,
            "tags": [], "citation": "", "quote": None, "details": [], "blocks": []}
    m = re.match(r"^\s*(\d{4})\s*[—–-]\s*(.*)$", heading)
    if m:
        node["year"], node["heading"] = m.group(1), m.group(2).strip()

    rest = []
    for line in lines:
        mm = NODE_META.match(line.strip())
        if mm and not rest:
            key, value = mm.group(1).lower(), mm.group(2).strip()
            if key == "tags":
                node["tags"] = [t.strip() for t in value.split(";") if t.strip()]
            else:
                node[key] = value
            continue
        rest.append(line)

    blocks = parse_blocks(rest, entry_urls)
    for b in blocks:
        if b["type"] == "quote" and node["quote"] is None:
            node["quote"] = b["text"]
        elif b["type"] == "bullets":
            for item in b["items"]:
                dm = re.match(r"^\*\*(.+?):?\*\*:?\s*(.*)$", item["text"])
                if dm:
                    node["details"].append({"label": dm.group(1).rstrip(":"), "text": dm.group(2)})
                else:
                    node["details"].append({"label": None, "text": item["text"]})
        elif b["type"] == "paragraph" and not node["citation"]:
            node["citation"] = b["text"]
        else:
            node["blocks"].append(b)
    return node


def parse_body(body, entry_urls=None):
    """Body -> ordered sections; a section holding '###' headings becomes a chain."""
    sections, current, lines = [], None, body.splitlines()
    i, preamble = 0, []
    while i < len(lines):
        line = lines[i]
        h2 = re.match(r"^##\s+(.*)$", line)
        h3 = re.match(r"^###\s+(.*)$", line)
        if h2:
            current = {"heading": h2.group(1).strip(), "id": slugify(h2.group(1)),
                       "blocks": [], "nodes": []}
            sections.append(current)
            i += 1
            continue
        if h3 and current is not None:
            body_lines, i = [], i + 1
            while i < len(lines) and not re.match(r"^#{2,3}\s", lines[i]):
                body_lines.append(lines[i])
                i += 1
            # a [!break] callout belongs to the node that follows it
            brk = None
            for b in parse_blocks(body_lines, entry_urls):
                if b["type"] == "callout" and b["kind"] == "break":
                    brk = b["title"]
            node = parse_node(h3.group(1).strip(), body_lines, entry_urls)
            node["break_before"] = brk
            current["nodes"].append(node)
            continue
        chunk, i = [line], i + 1
        while i < len(lines) and not re.match(r"^#{2,3}\s", lines[i]):
            chunk.append(lines[i])
            i += 1
        target = current["blocks"] if current is not None else preamble
        target.extend(parse_blocks(chunk, entry_urls))
    return preamble, sections


# --------------------------------------------------------------------- entry

def build_entry(name, text, entry_urls=None):
    meta, body = split_frontmatter(text)
    if meta is None:
        return None, [f"{name}: no frontmatter block"]

    problems = []
    for key in REQUIRED:
        if not meta.get(key):
            problems.append(f"{name}: '{key}' is missing")
    for key in meta.get("_unquoted_colon", []):
        problems.append(f"{name}: '{key}' contains ': ' — put double quotes around the whole value")
    if meta.get("stage") and norm(meta["stage"]) not in STAGES:
        problems.append(f"{name}: 'stage' is {meta['stage']!r}; use Traced or Under Investigation")
    if meta.get("hypothesis") and norm(meta["hypothesis"]) not in HYPOTHESES:
        problems.append(f"{name}: 'hypothesis' is {meta['hypothesis']!r}")
    if meta.get("peer_review") and norm(meta["peer_review"]) not in REVIEWS:
        problems.append(
            f"{name}: 'peer_review' is {meta['peer_review']!r}; "
            "use one of: Unreviewed, Open for review, Peer reviewed"
        )
    if re.search(r"\?\s*$", str(meta.get("title", ""))):
        problems.append(f"{name}: 'title' is a question; a title states the claim's subject")

    preamble, sections = parse_body(body, entry_urls)
    nodes = [n for s in sections for n in s["nodes"]]

    counts = {}
    for n in nodes:
        key = norm(n.get("verification") or "")
        if key and key not in VERIFICATIONS:
            problems.append(f"{name}: 'Verification: {n.get('verification')}' is not a known state")
        counts[key or "unstated"] = counts.get(key or "unstated", 0) + 1

    stage = meta.get("stage", "")
    if norm(stage) == "traced":
        unverified = sorted({k for k in counts if k != "verified at source"})
        if unverified:
            problems.append(
                f"{name}: stage is Traced but a chain node is not verified at source "
                f"({', '.join(unverified)}); use Under Investigation until every node is "
                "Verified at source"
            )

    num = str(meta.get("num", "")).zfill(3) if meta.get("num") else ""
    slug = re.sub(r"\.md$", "", name)
    entry = {
        "num": num,
        "slug": slug,
        "file": name,
        "draft": str(meta.get("draft", "")).lower() == "true",
        "title": meta.get("title", ""),
        "claim": meta.get("claim", ""),
        "subject": meta.get("subject", ""),
        "domain": meta.get("domain", ""),
        "cross_links": meta.get("cross_links", []) if isinstance(meta.get("cross_links"), list)
        else [x.strip() for x in str(meta.get("cross_links", "")).split("·") if x.strip()],
        "lifecycle": meta.get("lifecycle", ""),
        "stage": stage,
        "stage_note": meta.get("stage_note", ""),
        "hypothesis": meta.get("hypothesis", ""),
        "peer_review": meta.get("peer_review", ""),
        "contested": str(meta.get("contested", "")).lower() == "true",
        "plain_status": meta.get("plain_status", ""),
        "summary": meta.get("summary", ""),
        "kicker": meta.get("kicker", ""),
        "lede": meta.get("lede", ""),
        "rests_on": [str(x).zfill(3) for x in meta.get("rests_on", []) or []],
        "cited_by": [str(x).zfill(3) for x in meta.get("cited_by", []) or []],
        "keywords": meta.get("keywords", []) or [],
        "added": meta.get("added", ""),
        "updated": meta.get("updated", ""),
        "traced": meta.get("traced", ""),
        "author": meta.get("author", ""),
        "conflicts": meta.get("conflicts", ""),
        "preamble": preamble,
        "sections": sections,
        "verification_counts": counts,
        "node_count": len(nodes),
        "verified_count": counts.get("verified at source", 0),
    }
    return entry, problems
