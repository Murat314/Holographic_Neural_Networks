# Revision and verification report — 23 November 2026

## Changes actually made

1. Corrected stale Theorem 2.6 / Figure 3 annotations in `figures/simulate_capacity.py` to Theorem 2.8 / Figure 2(a).
2. Replaced the manually duplicated Appendix A Python source with `\lstinputlisting` from the exact file used to compute the figure, preventing future divergence between code and PDF.
3. Added a clear narrative-survey methodological limitation in Section 1.3; did not fabricate search dates, hit counts or screening logs.
4. Replaced an obsolete 41-placeholder BibTeX checklist with an honest audit protocol for the 48 structured entries. External verification of all 48 records is not claimed.
5. Added `figures/simulate_correlated_keys.py` and an exploratory correlated-key benchmark in Appendix B, including the observed results and caveats.
6. Updated the AI-assistance disclosure to mention additional ChatGPT editing and simulation assistance.

## Tests performed

- `python -m py_compile figures/simulate_capacity.py`: passed.
- Small Monte Carlo smoke test (D=32,64; loads 2,4,8): executed with positive finite discrimination SNRs.
- `python figures/simulate_correlated_keys.py`: executed; results reported in Appendix B (D=256, 500 trials per setting, nine settings).
- Full original 17-point Monte Carlo rerun was attempted but did not finish within the tool execution time limit. Therefore the original `figures/capacity_snr.dat` remains the project-provided data and is NOT certified as independently reproduced.
- Direct `pdflatex` compilation uses the included pre-existing `main.bbl`; `bibtex` executable is unavailable in this environment. Do not interpret this as a fresh successful BibTeX build.
- Spot-checked bibliographic details of Schlegel et al. (Springer DOI 10.1007/s10462-021-10110-3) and Frady et al. (PubMed/DBLP). The remaining records require authoritative individual validation.

## Remaining work before journal submission

- Verify each of the 48 bibliographic records against primary publisher metadata and verify every substantive claim-to-citation mapping.
- Complete a full fresh run of the original Monte Carlo benchmark on a machine with adequate runtime, and compare regenerated data against the included table.
- Review exact finite-D formulae and conditional assumptions independently, especially the Gaussian HRR comparison.
- Consider adding performance comparisons against implemented linear-attention/state-space baselines. The current paper remains a survey with an exploratory architectural blueprint, not a validated foundation-model implementation.
- Obtain author review of all edits and satisfy the target venue's AI-assistance policy.
