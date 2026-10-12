# Assumption Check — build & conventions

Public registry of scientific claims. Entries are Markdown; the site is a single
`index.html` that renders a generated `entries.js`. A Priority Nexus LLC project.

## Where things live
- `entries/NNN-slug.md` — one entry per file (YAML frontmatter + body).
- `scripts/build_entries.py` — bundles `entries/*.md` into `entries.js`. Run it
  after any entry change.
- `index.html` — the whole site (renderer, registry, filters, Method, Map, About).
- `templates/Entry template.md`, `HOW-TO-ADD-AN-ENTRY.md` — the entry format.

## Build & verify (always, before committing an entry change)
```
python3 scripts/build_entries.py
```
It validates frontmatter and enforces the stage rule (below). A failed build is
the check working — fix the entry, don't bypass it. `entries.js` is generated;
never hand-edit it.

## Entry essentials
- Frontmatter keys: num, title, claim, subject, domain, cross_links, lifecycle,
  stage, stage_note, hypothesis, peer_review, contested, plain_status, summary,
  kicker, lede, rests_on, cited_by, keywords, added, updated, traced, author,
  conflicts. `draft: true` hides an entry from the live registry.
- **Title is a statement, never a question.**
- Each evidence node carries `Tier:`, `Verification:`, `Tags:` and, where possible,
  a verbatim source quote plus a link/file.

## Stage rule (enforced by the build)
- **Under Investigation** until every evidence node is `Verification: Verified at
  source`. Only when all nodes are verified at source may `stage: Traced`.
- Verification ladder: Unlocated → Located, not read → Verified at source
  (+ Unreadable, Identity unresolved). An abstract is **Located, not read**, never
  Verified at source — only the original full document counts.

## Registry behaviour
- The default registry list shows **Traced** entries only. Under Investigation
  entries appear only via the "Under Investigation" stage filter (an explicit
  search also surfaces one). This is a permanent rule in `index.html`.

## Language — "strict syntax"
Minimal, plain, unbiased, blunt; facts only; jargon only inside quotes; headings
name the study, never argue the conclusion. The only non-neutral text allowed is a
direct source quote in quotation marks with attribution.

## Privacy
The research method, the claim pipeline, priorities, and the private notes live in
the separate **private** repo and must not be copied into this public repo. Keep
this file to build/schema/style only.
