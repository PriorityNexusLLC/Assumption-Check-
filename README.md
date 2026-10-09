# Assumption Check

**A public registry of scientific claims — the evidence under each one, and the exact test that would settle it.**

Built and operated by **Priority Nexus LLC** · *Prioritizing Boundaries*

> ⭐ **Live prototype:** open [`index.html`](./index.html) in any browser, or view it hosted (see **Running it** below).
> *Alternate link (private — only opens if shared with you): https://claude.ai/artifact/NCjZzeVbiqGDRxFaaPrABC*

---

## What this is

Most confusion about science isn't a shortage of information — it's an excess of noise. Claims pile up faster than anyone can check them, and the original finding gets buried under layers of citation that drift further from the source with each repetition.

**Assumption Check** traces a claim back to what was actually measured, marks how far the checking has gone, and names the test that would settle it. Nothing is called true for being popular, peer-reviewed, or often repeated — only when the evidence holds.

It is **not** a debunking list and **not** a forum. The one rule that sets it apart: **every claim — including every competing hypothesis — goes through the same schema and the same standard of proof.**

## Core values

- **Identity** — every claim, source, and reviewer is named.
- **Transparency** — the method, the wording rules, and each entry's confidence level are public.
- **Integrity** — findings follow the evidence, not funding, popularity, or pressure. Paid review never changes a public rating.

---

## How an entry works

Each registry entry uses a **six-field schema**:

1. **Claim as stated** — quoted from the paper, with how it's reported publicly if that differs.
2. **Evidence base** — design, sample, what was measured.
3. **Untested assumption / unaddressed alternative** — the specific gap, stated neutrally.
4. **What would settle it** — the concrete test, with the predicted result either way.
5. **Current status** — replications, critiques, author responses, whether the test has been run.
6. **Entry author and conflicts** — who wrote it and any stake they hold.

### Evidence tiers (universal)

| Tier | Meaning |
|------|---------|
| **T1** | Observed or associated |
| **T2** | Shown under controlled or model conditions |
| **T3** | Shown in the real system, partially |
| **T4** | Established in the real system, measured |

Each entry then defines what the tiers mean for its own field.

### How an entry is scored (three separate questions)

- **Hypothesis** — is the science settled? *(Open → Under Test → Resolved: Supported / Not supported / Mixed)*
- **Peer review** — has a domain expert vetted this entry? *(Unreviewed → Open for review → Peer reviewed)*
- **Source verification** — per source: was the quote confirmed against the publisher? *(Verified at source / Located / Unreadable / Identity confirmed)*

Per-source tags also record **Peer-reviewed vs Preprint**, **Replication** status, and attached **source files**.

> **Peer-reviewed / Verified — not the same as true.** Every tag describes how far the checking has gone, not whether the claim is correct.

### Domains

Entries file under a `Core › Sub › Topic` path across **14 core science categories** (Physical, Chemical, Life & Biological, Earth/Environmental/Planetary, Space & Astronomical, Mathematics/Logic/Formal, Computer/Information/Data, Engineering & Technology, Medical & Health, Social/Behavioral/Economic, Cognitive/Neuroscience/Mind, Philosophy/Ethics/Foundational, Systems/Complexity/Interdisciplinary, Cross-Disciplinary Bridge). A claim is placed under its best-fit primary category and cross-linked to the others it spans.

---

## Flagship entry: the exosome prion chain (Entry 001)

A single claim — *"prion-bearing extracellular vesicles transmit disease to animals"* — traced link by link through its citation chain, with **all 8 nodes verified at source** (full text read for each).

**Honest result:** the core claim holds. Two independent primary studies (Février et al. 2004, PNAS; Vella et al. 2007, *J. Pathol.*) each show exosome-associated prions cause disease by intracerebral injection into PrP-overexpressing mice (both 5/5; clean controls). The real caveats are narrower than the downstream language suggests:

- **Scope** — both use the most permissive assay (intracerebral injection, PrP-overexpressing mice); natural routes and normal-PrP animals untested.
- **One miscitation** — a 2017 review cites a cell-culture-only paper (Guo et al. 2016) for the in-vivo claim; the claim is true, but the citation points to the wrong source.

The entry corrected its own framing twice as sources were read — a demonstration that the method can exonerate a claim, not just challenge one.

---

## Running it

The site is a single page with no server and no database. Entries are Markdown files in `entries/`, which a GitHub Action bundles into `entries.js` whenever they change.

- **Locally:** download the repo and open `index.html` in any browser. Keep `pn-logo.png` and `entries.js` in the same folder.
- **Hosted (anyone can view), via GitHub Pages:** in the repo, go to **Settings → Pages**, set **Source** to `Deploy from a branch`, pick your `main` branch and the `/ (root)` folder, and save. After a minute the site is live at `https://<your-username>.github.io/<repo-name>/`. Put that URL at the top of this README so visitors land straight on it.

## Adding entries

Entries are written in Obsidian (or any editor) as Markdown, one file per claim. See **[HOW-TO-ADD-AN-ENTRY.md](./HOW-TO-ADD-AN-ENTRY.md)** for the one-time setup and the format. Anyone can propose a claim through the [suggestion form](https://github.com/PriorityNexusLLC/Assumption-Check-/issues/new?template=suggest-a-claim.yml).

## Files

- `index.html` — the site (Home, Registry, Entry pages, Method, Map, About).
- `entries/` — one Markdown file per registry entry. This is where the content lives.
- `entries.js` — generated from `entries/` by `scripts/build_entries.py`; don't edit it by hand.
- `templates/Entry template.md` — the Obsidian template for a new entry.
- `.github/workflows/build-entries.yml` — rebuilds `entries.js` when entries change, and checks each entry for mistakes.
- `.github/ISSUE_TEMPLATE/suggest-a-claim.yml` — the public "Suggest a claim" form.
- `pn-logo.png` — Priority Nexus LLC logo, used on the About page.
- `README.md` — this file.

## Status & roadmap

This repository accompanies a **working prototype**, built as a self-contained page.

**Prototype (now):** Home · Registry (search + badge filters) · Entry pages built from Markdown · Method · Map (real entries drawn and linked; the rest illustrative) · About · public claim suggestions via GitHub issues.

**Full build (planned):** custom domain · reviewer accounts and moderation · persistent source-file uploads · the full node map (global "night sky" + per-claim constellation) computed from stored connections.

---

## Contact

**Priority Nexus LLC** — theaistherapist@gmail.com
For collaboration, review, or funding enquiries.

---

*Last updated: 9 October 2026*
