---
draft: true
num: "008"
title: The PRNP balancing-selection signal
claim: The worldwide signal of balancing selection at the prion protein gene is real, not an artefact of how the variants were sampled.
subject: PRNP selection signal
domain: Life & Biological › Evolutionary & Population Genetics › Selection detection methods
cross_links: Cognitive, Neuroscience & Mind (Prion disease)
lifecycle: Active
stage: Under Investigation
stage_note: "2 of 5 chain sources verified at source (Mead 2008, Bitarello 2023); the reanalyses and the 2003 anchor are read at abstract only, full texts paywalled or rate-limited"
hypothesis: Under Test
peer_review: Unreviewed
contested: true
plain_status: "The original positive Tajima's D signal did not survive resequencing that captured rare variants. Reanalyses attribute it to ascertainment bias; the original authors partly conceded the statistics. A different signal (positive or purifying selection) may still be present."
summary: "Is the PRNP balancing-selection signal real? The high-frequency-variant signal did not survive rare-variant resequencing; attributed to ascertainment bias. Authors partly conceded. PRNP absent from current canonical lists."
kicker: Entry 008 · PRNP selection signal · Under investigation
lede: "Whether the statistical signature of balancing selection reported at the prion protein gene in 2003 is a genuine selection signal or an artefact of scoring only common variants. The specific signal did not survive resequencing designed to catch rare variants."
rests_on: []
cited_by: []
keywords:
  - prnp
  - balancing selection
  - tajima's d
  - ascertainment bias
  - neutrality test
  - resequencing
  - site frequency spectrum
  - population genetics
  - codon 129
  - prion
  - selection scan
added: 2026-10-09
updated: 2026-10-09
traced: October 2026
author: Priority Nexus LLC (AI-assisted research; sources checked at publisher 9 Oct 2026)
conflicts: None declared
---

## Claim as stated

The 2003 paper reported a statistical signature of balancing selection at PRNP in worldwide population samples — an excess of high-frequency (common) variants, read as the fingerprint of selection that had preserved two codon 129 variants for a long time. The claim under check here is narrower than the cannibalism hypothesis it was used to support ([[007-codon-129-balancing-selection|Entry 007]]): it is the methodological claim that **the signal itself is genuine balancing selection, not an artefact of which variants were counted.**

## Evidence base

The test at issue is Tajima's D, which compares two measures of genetic variation. Under neutral evolution they agree and D is near zero; an excess of common variants over rare ones drives D positive, the pattern long-maintained balancing selection produces. The 2003 analysis reported strongly positive D across populations.

There are two ways to find the variants a neutrality test scores. **Genotyping** checks a sample for variants already known to exist, which by construction are common — cheap, but it cannot see rare variants. **Resequencing** reads every base in every person, so it finds rare variants too. The central objection is that Tajima's D goes positive precisely when common variants outnumber rare ones, so a method that can only see common variants tends to produce a positive D whether or not selection is acting: the signature and the artefact look the same.

## Untested assumption

That the positive Tajima's D reported in 2003 reflected selection rather than the sampling method. The 2003 worldwide analysis scored variants above a frequency threshold rather than resequencing to capture rare ones, so the assumption that the test statistic was unbiased by ascertainment was not itself tested in that design.

## Evidence tiers

What T1–T4 mean for this claim.

- **T1** A positive neutrality-test statistic is **reported from genotype data**.
- **T2** The signal **survives resequencing** that ascertains rare variants in the same or other populations.
- **T3** The signal is **recovered by modern whole-genome selection scans** with demographic history modelled explicitly.
- **T4** PRNP appears as an **established balancing-selection locus** on the field's validated list, by current methods on large datasets.

The claim above is a **T3/T4** claim. The evidence reaches **T1** (the original positive D). At **T2**, resequencing did not recover a balancing-selection signal — it recovered negative D and a different (positive or purifying) selection signal. PRNP is absent from current **T4** lists.

## The chain

Oldest first. Verification reflects checks at the publisher on 9 October 2026.

### 2003 — The original positive signal
Tier: T1
Verification: Located, not read
Tags: Peer-reviewed; Load-bearing; Full text paywalled

Mead S, Stumpf MPH, Whitfield J, Beck JA, Poulter M, Campbell T, Uphill JB, Goldstein D, Alpers M, Fisher EMC, Collinge J. "Balancing Selection at the Prion Protein Gene Consistent with Prehistoric Kuru-like Epidemics." *Science* 2003;300(5619):640–643. [doi:10.1126/science.1083320](https://doi.org/10.1126/science.1083320) · PMID 12690204

> "Worldwide PRNP haplotype diversity and coding allele frequencies suggest that strong balancing selection at this locus occurred" *(abstract)*

- **What it shows (from the abstract):** A worldwide pattern of PRNP variation interpreted as balancing selection. The 2008 restatement by the same group describes the original finding as "two highly divergent clades, representing 129V and 129M, a bimodal distribution of pairwise mutational differences and a skew in the allele frequency distribution to high-frequency polymorphism."
- **What it does not show:** That the high-frequency skew was not produced by scoring only common variants.
- **Files:** Full text paywalled; abstract read at Europe PMC 9 Oct 2026. The specific per-population Tajima's D values are in the full text only and are not stated here as verified. Marked Located, not read.

> [!break] The break — resequencing that captures rare variants does not recover the signal

### 2004 — The ascertainment-bias charge
Tier: Methodological critique
Verification: Located, not read
Tags: Peer-reviewed; Full text paywalled

Kreitman M, Di Rienzo A. "Balancing claims for balancing selection." *Trends in Genetics* 2004;20(7):300–304. [doi:10.1016/j.tig.2004.05.002](https://doi.org/10.1016/j.tig.2004.05.002) · PMID 15219394

- **What it argues:** That scoring only variants above a frequency threshold introduces an ascertainment bias toward a positive Tajima's D, and that rejecting the neutral model is not the same as demonstrating balancing selection. The charge is recorded in the abstract of Zan et al. 2006 (below), which states that Kreitman and Di Rienzo "challenged this hypothesis by pointing out that the exclusion of polymorphisms with low frequency may introduce an ascertainment bias and, in turn, lead to a wrong conclusion."
- **Files:** Full text paywalled; no abstract text served by the publisher or Europe PMC. Citation confirmed at Crossref. No sentence is quoted directly from it here. Marked Located, not read.

### 2006 — Resequencing reanalysis
Tier: T2 (not recovered as balancing selection)
Verification: Located, not read
Tags: Peer-reviewed; Full text not retrieved

Soldevila M, Andrés AM, Ramírez-Soriano A, Marquès-Bonet T, Calafell F, Navarro A, Bertranpetit J. "The prion protein gene in humans revisited: Lessons from a worldwide resequencing study." *Genome Research* 2006;16(2):231–239. [doi:10.1101/gr.4345506](https://doi.org/10.1101/gr.4345506) · PMC1361719

> "The existence of an ancient, stable, balanced polymorphism that has been claimed in a previous study and related to cannibalism can be rejected and is shown to be due to ascertainment bias." *(abstract)*

- **What it shows (from the abstract):** Resequencing of PRNP exon 2 (2378 bp) in a worldwide sample of 174 humans found "an excess of low-frequency variants" — the opposite skew to the 2003 report. The abstract rejects the ancient balanced polymorphism as ascertainment bias, while noting that the data are consistent with "mainly positive selection" and that "short local periods of balancing selection (Kuru-like episodes)" are also consistent. So this is a rejection of the specific worldwide balancing-selection claim, not of all selection at PRNP.
- **What it does not show:** The per-population Tajima's D values and age estimates are in the full text, which was not retrieved (the journal page returned repeated rate-limit errors; the PMC record served the abstract only).
- **Files:** Abstract read at Europe PMC 9 Oct 2026; full text not retrieved. Marked Located, not read.

### 2006 — Independent resequencing, one population
Tier: T2 (not recovered)
Verification: Located, not read
Tags: Peer-reviewed; Full text paywalled

Zan Q, Wen B, He Y, Wang Y, Xu S, Qian J, Lu D, Jin L. "Complete sequence data support lack of balancing selection on PRNP in a natural Chinese population." *Journal of Human Genetics* 2006;51(5):451–454. [doi:10.1007/s10038-006-0383-8](https://doi.org/10.1007/s10038-006-0383-8) · PMID 16565881

> "We showed that the pattern of genetic variation in PRNP is not consistent with the presence of balancing selection in this gene." *(abstract)*

- **What it shows (from the abstract):** Full resequencing of the entire 15 kb PRNP genomic region in a Chinese population found no pattern consistent with balancing selection. The abstract also notes a caveat against the earlier reanalysis — that a Human Genome Diversity Project sample "may be substructured."
- **What it does not show:** A multi-population test; this is a single natural population.
- **Files:** Full text paywalled; abstract read at Europe PMC 9 Oct 2026. Marked Located, not read.

### 2008 — The authors' partial concession
Tier: T2
Verification: Verified at source
Tags: Peer-reviewed; Open access; Load-bearing

Mead S, Whitfield J, Poulter M, Shah P, Uphill J, Beck J, Campbell T, Al-Dujaily H, Hummerich H, Alpers MP, Collinge J. "Genetic susceptibility, evolution and the kuru epidemic." *Phil. Trans. R. Soc. B* 2008;363(1510):3741–3746. [doi:10.1098/rstb.2008.0087](https://doi.org/10.1098/rstb.2008.0087) · PMC2576515

> "We found a nucleotide diversity of 0.0011, 24 segregating sites excluding octapeptide-repeat polymorphism and a Tajima's D of +0.80 … Although this finding was not significant in the context of the standard neutral model of evolution … when compared with empirical data of Stephens et al. (2001), the finding was significant at the 95 per cent level."

- **What it shows:** The same group resequenced 4.7 kb across 94 CEPH individuals to catch rare variants. The redone Tajima's D was +0.80 — still positive, but not significant under the standard neutral model, and far below the original values. Of their original genotype-based statistics they wrote that these "should not, however, have been mentioned in comparison to the resequencing data of Stephens et al. 2001." They maintained that "the deepest genealogical split at PRNP is caused by the M129V polymorphism."
- **What it does not show:** A significant balancing-selection signal under the standard model; the retained claim is about the shape of the gene genealogy, not the strength of the original statistics.
- **Files:** Full text read at PMC 9 Oct 2026.

### 2023 — Where the field has settled
Tier: T4 (absence)
Verification: Verified at source
Tags: Peer-reviewed; Open access

Bitarello BD, Brandt DYC, Meyer D, Andrés AM. "Inferring Balancing Selection From Genome-Scale Data." *Genome Biology and Evolution* 2023;15(3):evad032. [doi:10.1093/gbe/evad032](https://doi.org/10.1093/gbe/evad032) · PMC10063222

> "Recent bottlenecks, admixture or substructure" *(listed among the demographic processes that mimic the allele-frequency skew of balancing selection; the review also lists "technical artifacts due to mapping errors in genomic regions with paralogy")*

- **What it shows:** A current methods review of balancing-selection detection. It sets out why the signal is hard to establish — demographic history and paralogy can produce false positives — and works through the canonical human examples (the MHC/HLA, ABO and sickle-cell loci). PRNP does not appear anywhere in the text or tables (confirmed: zero occurrences of "PRNP").
- **What it does not show:** A direct re-test of PRNP; the evidence here is the absence of PRNP from the field's standard list twenty years on, which is suggestive rather than a refutation.
- **Files:** Full text read at PMC 9 Oct 2026.

## What would settle it

- **If the claim holds:** a modern whole-genome selection scan — thousands of individuals across many populations, with demographic history modelled explicitly rather than assumed — would recover a balancing-selection signal at PRNP. The existing reanalyses are twenty years old and used hundreds of people.
- **If it doesn't:** such a scan would show PRNP sitting within the neutral/demographic background, with any residual signal attributable to positive or purifying selection rather than balancing selection.

## Current status

- The original high-frequency-variant signal did not survive resequencing that ascertained rare variants (Soldevila 2006; Zan 2006; and the authors' own redone analysis, Mead 2008).
- The authors partly conceded the statistics in 2008 while maintaining the gene-genealogy conclusion.
- Soldevila's resequencing reports a selection signal of a different kind (an excess of low-frequency variants, consistent with positive or purifying selection), so "no balancing selection" is not the same as "no selection."
- PRNP is absent from a 2023 review's treatment of the canonical human balancing-selection loci.
- No modern large-sample selection scan has been published to re-test it directly.

## Where it stands

- **Established.** The specific balancing-selection statistic reported in 2003 is not robust to a resequencing design that captures rare variants; the ascertainment-bias objection is accepted by the reanalyses and, on the original statistics, partly by the authors.
- **Still open.** Whether any genuine selection signal remains at PRNP once demography is modelled, and of what kind.
    - a modern whole-genome selection scan at PRNP with explicit demographic modelling
    - reconciliation of the differing resequenced regions and populations across the 2006 reanalyses

> [!summary]
> Original positive Tajima's D → attributed to ascertainment bias; not recovered by resequencing.
> Authors' 2008 redo → D +0.80, not significant under the standard neutral model.
> A different signal (positive/purifying selection) → may still be present.

> [!note] Provenance — read before citing
> Verified at source with the quoted sentence present: Mead et al. 2008 (*Phil. Trans. R. Soc. B*, open access, PMC2576515) and Bitarello et al. 2023 (*Genome Biology and Evolution*, open access, PMC10063222). Read at abstract only, full texts paywalled or not retrieved, and so marked Located, not read: Mead et al. 2003 (*Science*); Soldevila et al. 2006 (*Genome Research* — journal page rate-limited, PMC served the abstract only); Zan et al. 2006 (*Journal of Human Genetics*). Kreitman & Di Rienzo 2004 (*Trends in Genetics*) is cited by confirmed metadata only, with no quote taken from it. This entry is AI-assisted research and is marked so in the author field, per the Method page.
