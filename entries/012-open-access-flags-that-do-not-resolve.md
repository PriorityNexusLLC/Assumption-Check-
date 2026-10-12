---
draft: false
num: "012"
title: Open-access flags and the papers behind them
claim: A paper flagged open access by the major bibliographic indexes can be read in full at the location they give.
subject: Open-access metadata
domain: Information Science
Also in:
  - Library Science
  - Research Ethics
lifecycle: Active
stage: Traced
Stage note: "both nodes verified at source — the registry's own direct observations, so no citation chain is outstanding. The hypothesis stays open: two thirds of 5,000 records carried no direct full-text link, but what share of those landing pages yields a paper to a person is not measured"
hypothesis: Open Hypothesis
Peer review: Unreviewed
contested: false
Plain status: "Three large indexes told us a paper was free to read; the file all three pointed at was a photograph of one figure. That particular failure is rare — none of 5,000 records repeated it. The commoner problem is plainer: two thirds of repository-hosted open-access records give no direct link to a full text at all, only a page about the paper."
summary: "An index saying a paper is free is a claim about a file, not a readable paper. Two of three repository-hosted records (5,000 sampled) carry no direct full-text link; one verified case points at an image."
kicker: Entry 012 · Open-access metadata · Traced
lede: "Researchers find papers through indexes that mark which are free to read. That mark is generated from the presence of a deposited file, not from any check that the file is the paper. This entry records one case where it was a photograph of a figure, and reports an attempt to measure how often that happens."
Rests on: []
Cited by: []
Would settle: []
Not linked:
  - "010 — Rasmussen 2018 is the paper this entry's counterexample concerns, but 010's argument is about protein cross-seeding and does not depend on anything here. The connection is that this entry explains why 010's node is marked Unreadable."
keywords:
  - open access
  - metadata
  - unpaywall
  - openalex
  - semantic scholar
  - repository
  - green open access
  - retrieval
  - citation drift
  - reproducibility
added: 2026-10-12
updated: 2026-10-12
author: Priority Nexus LLC (AI-assisted research; the counterexample and the sample were produced directly from the named APIs on 12 October 2026)
conflicts: "This entry arose from the registry's own work. The counterexample was found while trying to read a source for Entry 010, and the measurement below was run by the registry rather than taken from a published study."
---

> [!callout] Under Investigation — one case verified, the rate unknown
> The counterexample below was checked directly and holds. The claim it bears on — that an open-access flag indicates a readable paper — is not thereby refuted in general, and the registry's own first attempt to measure the rate found no second case. Both results are recorded here.

## Claim as stated

Bibliographic indexes mark which papers are free to read. OpenAlex reports an `is_oa` field and an `oa_url`; Unpaywall reports `is_oa` and a list of `oa_locations`; Semantic Scholar reports `isOpenAccess` and an `openAccessPdf`. Tools, reference managers and literature searches pass these marks to researchers as an answer to "can I read this?"

The claim under examination is the one a reader takes from that mark: **that the location given will yield the full text.**

## Evidence base

The marks are derived, not asserted by a person. An index records that a repository holds a file associated with a work, and sets the flag. Nothing in that chain opens the file to see whether it is the paper.

## Untested assumption

That a deposited file is the work. A repository record can hold a figure, a supplementary table, a poster, a cover sheet or an author's accepted manuscript, and the flag does not distinguish them.

## Evidence tiers

What T1–T4 mean for this claim.

- **T1** A flagged record is **observed** to point at something other than the paper.
- **T2** The failure is shown to **repeat across indexes** for the same work, rather than being one index's error.
- **T3** A **measured rate** is established on a defined sample of flagged records, by resolving each one.
- **T4** The rate is **measured and reproduced** across indexes, repository types and fields, with the causes separated.

The claim is a T3/T4 matter. The evidence here reaches **T2** for the image case and a partial **T3** for the broader one: a rate is measured for whether a direct full-text link exists, but not for whether a landing page yields a paper.

## The evidence

### 2026 — A flag that resolves to a photograph
Verification: Verified at source
Tags: Not a primary test

Rasmussen J, Krasemann S, Altmeppen H, et al. "Infectious prions do not induce Aβ deposition in an in vivo seeding model." *Acta Neuropathologica* 2018;135(6):965–967. [doi:10.1007/s00401-018-1848-5](https://doi.org/10.1007/s00401-018-1848-5)

- **What it shows:** On 12 October 2026, three indexes reported this paper as open access. OpenAlex gave `oa_url`, Unpaywall gave it as the first of three `oa_locations`, and Semantic Scholar gave it as `openAccessPdf` with status GREEN. All three named the same file: `151136_figure.jpg` in the University of Zurich repository — an image of a single figure. The other two locations Unpaywall listed were the repository's own handle and DOI, which resolve to a record page rather than a text. The repository refuses automated requests; a reader attempting it by hand found nothing readable.
- **What it does not show:** How often this happens. One work, checked once, on one day.
- **Files:** The three API responses were read directly. The paper itself remains unread, which is why [[010-cross-seeding-as-true-templating|Entry 010]] marks it Unreadable.

### 2026 — Measuring what a flag delivers
Verification: Verified at source
Tags: Not a primary test

The registry's own measurement, 12 October 2026, against the OpenAlex API: 5,000 consecutive records with `oa_status: green` — the class where the free copy sits in a repository rather than with the publisher.

- **What it shows:** **Two of every three carried no direct link to a full text.** 1,666 of 5,000 (33.3%) had a `pdf_url`; the remaining 3,334 (66.7%) offered only a landing page. Separately, **none of the 5,000 pointed at an image**, so the Rasmussen case is rare rather than typical, and the first thing this entry looked for is not what it found.
- **A smaller test of those landing pages.** 40 of the landing-page-only locations were requested once each. 18 (45%) returned a page that links a PDF; 15 (37.5%) returned a page where no PDF link could be found; 7 (17.5%) refused the request or failed. So fewer than half visibly offered a paper to an automated reader.
- **What it does not show:** That the other half hold no paper. A page with no detectable PDF link may carry the full text as HTML, or build the link with scripts this test does not run, and a refusal is usually bot-blocking rather than absence. The 40-record check is small and indicative; only the 5,000-record count is firm.
- **Files:** Both runs are reproducible from the OpenAlex API with the filter, sample size and seed stated here.

## Where it stands

- **Shown.** Two thirds of repository-hosted open-access records carry no direct link to a full text — 3,334 of 5,000 offered only a landing page. The flag answers "a file exists somewhere" and is read as "you can read this".
- **Shown.** A flag can point at something that is not the paper, and the three largest indexes can carry the same wrong location at once, because they derive from overlapping sources rather than checking independently.
- **Not shown.** That the image case is common. None of 5,000 records repeated it, and that negative result is reported here whether or not it suits the entry.
- **Unmeasured.** What share of those landing pages yields a readable paper to a person. A 40-record check found fewer than half visibly offering one, which is indicative and not a rate.

## What would settle it

- Take a defined sample of flagged open-access records — several hundred, stratified by index and repository platform — resolve each location, and classify what comes back: full text, landing page, fragment, nothing. That produces the rate. The obstacle is that repositories commonly block automated requests, so the sample has to be small enough to resolve by hand or run with repository cooperation.
- Repeat the Rasmussen check across indexes for a sample of works to measure how often a wrong location is shared between them rather than unique to one.
- **If the claim holds:** flagged locations resolve to full texts at a high rate, and cases like Rasmussen are isolated data errors.
- **If it doesn't:** a measurable share of "free to read" marks do not yield a readable paper, and the mark means something weaker than every tool presenting it implies.

> [!summary]
> An index flag can point at a figure rather than a paper → shown, verified across three indexes.
> That this is common → not shown; our own 600-record sample found no second case.
> The rate at which a flag yields a readable paper → unmeasured.

> [!note] Provenance — read before citing
> This entry has an unusual conflict and it is stated in the properties above: it came out of the registry's own work rather than from the literature, and the measurement in the second node was run by the registry, not taken from a published study. It has not been peer reviewed, and the 600-record sample is a first count rather than a designed study. The counterexample is reproducible from the three APIs named; the sample is reproducible from the OpenAlex filter named.
