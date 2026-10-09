# How to add or edit an entry

Every registry entry is one Markdown file in the [`entries/`](./entries) folder. You write it in Obsidian (or any text editor, or directly on github.com), push it to GitHub, and the website updates itself within a couple of minutes. You don't need a server, a database or a paid plan.

## One-time setup (about 10 minutes)

1. **Get the repository onto your computer.** Install [GitHub Desktop](https://desktop.github.com/) (free), sign in, and choose **File → Clone repository → PriorityNexusLLC/Assumption-Check-**.
2. **Open it in Obsidian.** In Obsidian, choose **Open folder as vault** and pick the folder GitHub Desktop just made. The whole repository becomes your vault.
3. **Turn on templates.** In Obsidian, go to **Settings → Core plugins** and switch on **Templates**. Then under **Settings → Templates**, set **Template folder location** to `templates`.

Optional: install the community plugin **Obsidian Git** if you'd rather commit and push from inside Obsidian instead of GitHub Desktop.

## Adding a new entry

1. In the `entries` folder, create a new note. Name it with the next number and a short slug, like `002-short-name-of-claim`.
2. Run **Templates: Insert template** (command palette, Ctrl/Cmd + P) and pick **Entry template**. The dates fill in automatically.
3. Fill in the properties at the top and the sections below. Delete any section you don't need. The template starts with `draft: true`, which keeps the entry off the site while you work on it.
4. When it's ready, change `draft` to `false` (or delete the line).
5. In GitHub Desktop, write a short summary (like "Add entry 002"), click **Commit to main**, then **Push origin**.

If GitHub Desktop asks you to **Pull origin** first, click it. That just means the site's robot rebuilt `entries.js` after your last push.

About two minutes later, the entry appears on the site's Registry, gets its own page, and shows up as a labeled star on the Map.

## Editing an existing entry

Open the file in Obsidian, make the change, update the `updated:` date, then commit and push as above. The Registry shows an **Updated** flag on the entry for 30 days. Every entry page links to its own change history on GitHub, so readers can see exactly what changed and when.

## The properties

| Property | What to put |
|---|---|
| `num` | The entry number, like `"003"`. Must be unique. |
| `title`, `claim` | The entry's title and the one-sentence claim being checked. |
| `subject`, `domain`, `cross_links` | Short subject tag; the `Core › Sub › Topic` path; other domains, separated by `·`. |
| `lifecycle` | `Active` or `Legacy`. |
| `stage`, `stage_note` | `Under Investigation` (trail mapped, sources not yet verified) or `Traced` (trace complete), plus a short note. |
| `hypothesis` | Leave empty until a testable form of the claim is found. Then use `Open Hypothesis`, `Under Test`, `Resolved — Supported`, `Resolved — Not supported` or `Resolved — Mixed`. A plain hyphen instead of the dash is fine. |
| `peer_review` | `Unreviewed`, `Open for review` or `Peer reviewed`. |
| `contested` | `true` or `false`. |
| `plain_status`, `summary` | One plain-language line for the entry page, and one for the Registry card. |
| `kicker`, `lede` | Optional small line above the title, and the intro paragraph under it. |
| `rests_on` | Numbers of other entries this one depends on, like `- "001"`. "Cited by" fills itself in on the other entry, and the Map draws the link. |
| `keywords` | Extra search words. |
| `added`, `updated`, `traced` | Dates. |
| `author`, `conflicts` | Who wrote the entry and any stake they hold. |

If a value contains a colon followed by a space (for example `The honest result: it holds`), put double quotes around the whole value. Otherwise Obsidian can't read the properties, and the build check flags it.

## Writing the body

Ordinary Markdown works: `**bold**`, `*italic*`, `[links](https://…)`, and lists. A few patterns get special styling on the site:

- **`## The chain`** (or **`## The trail`**): each `###` heading inside it is one source, written as `### 2004 — What it did`. Directly under the heading, put the `Tier:`, `Verification:` and `Tags:` lines (tags separated by `;`). Then add the citation, the quote as a `> "…"` line, and the details as `- **Label:** text` bullets. A tag of `Load-bearing` highlights the card. The verification counts in the scoreboard and footer are worked out for you. Verification can be `Verified at source`, `Located, not read`, `Unlocated`, `Unreadable` or `Identity unresolved`. `Tier:` is optional; leave it out for sources that aren't evidence tiers (like a folklore trail).
- **`> [!break] text`**: draws the orange "break" line in a chain. The next source is highlighted as where things go wrong.
- **`> [!note] Title`**: a dashed provenance-style note box.
- **`> [!callout] Headline`** placed before the first `##` section: replaces the standard "Peer-reviewed / Verified — not the same as true" box with your own (for example, "Under Investigation — this entry is a work in progress").
- **Tier lists**: bullets starting with `**T1**`, `**T2**`, and so on become the tier ladder.
- **Numbered lists starting with bold**: become the numbered findings cards.
- **`## Where it stands`** or **`## What would settle it`**: bullets starting with bold become the summary box. Indented bullets under one become the highlighted list of open tests. A `> [!summary]` block right after the bullets adds a highlighted box of one-line verdicts inside it.
- **`[[001-exosome-prion-chain|Entry 001]]`**: Obsidian-style links to other entries work on the site too.

Two worked examples: [`entries/001-exosome-prion-chain.md`](./entries/001-exosome-prion-chain.md), a finished trace, and [`entries/002-origin-of-santa-claus.md`](./entries/002-origin-of-santa-claus.md), an entry still Under Investigation.

## If something goes wrong

If an entry has a mistake the site can't read (a missing title, or an unrecognized `hypothesis` value), the **Build entries** check on GitHub turns red and the site keeps showing the last good version. Open the repository's **Actions** tab to see a plain message naming the file and the problem.

To preview on your own computer before pushing, run `python scripts/build_entries.py` in the repository folder, then open `index.html` in your browser.
