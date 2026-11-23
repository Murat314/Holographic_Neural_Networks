# Bibliographic audit status (2026-11-23)

This document replaces an outdated placeholder checklist. `references.bib` contains structured bibliographic entries; **structured does not mean externally verified**. A source-by-source verification against publisher pages, Crossref, DBLP, or arXiv is still required before submission.

## Verification procedure

For each cited BibTeX entry: (1) resolve the DOI at the publisher or Crossref, (2) compare title, authors, year, venue, volume, pages and publication type, (3) correct discrepancies in `references.bib`, (4) verify that the cited source actually supports the manuscript claim. Preserve a record of checked entries and their source URLs.

## Reproducibility and manuscript checks

- Run `python figures/simulate_capacity.py --seed 2026` to regenerate `figures/capacity_snr.dat` (can be computationally expensive).
- The LaTeX appendix now imports the exact source script using `\lstinputlisting`, so code and printed listing cannot silently diverge.
- The associated mathematical result is Theorem 2.8 and the simulation plot is Figure 2(a).
- The research-methodology text records databases and selection rules but does not specify individual query dates, result counts or screening log. Do not claim PRISMA-style systematic reproducibility without such records.
