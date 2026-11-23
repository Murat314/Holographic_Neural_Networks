# Figures Directory

This directory hosts publication-grade TikZ/PGFPlots `.tex` figures and modular Python (`matplotlib`/`numpy`) simulation scripts generating vector `.pdf` assets.

## Planned Core Figures
1. `fig_genealogy.tex` — Historical & Architectural Genealogy (1990s Optical/Sutherland HNN $\rightarrow$ HRR/HDC $\rightarrow$ Modern CVNNs, FNet, SSMs).
2. `fig_algebra.tex` — Algebraic Operations in Complex Phase Space (Bundling, Binding via FFT/$\circledast$, and Unbinding via $\star$ with Crosstalk $\boldsymbol{\eta}$).
3. `fig_capacity.tex` — Theoretical Capacity & Scaling Trade-offs ($\mathrm{SNR} \propto D/N$ decay vs. $N/D$ ratio; Memory footprint $\mathcal{O}(1)$ vs. $\mathcal{O}(N)$ vs. $\mathcal{O}(N^2)$).
4. `fig_hybrid_arch.tex` — Future Hybrid Architecture integrating a Holographic $\mathcal{O}(1)$ Memory Module into a Transformer/SSM backbone.

## Visual Conventions
- Use the Okabe-Ito color definitions from `main.tex` (`okabeNavy`, `okabeTeal`, `okabeCoral`, `okabeAmber`, `okabeSky`, `okabePurple`, `okabeSlate`).
- Match mathematical notation strictly to macros defined in `main.tex` (`\vect{}`, `\mat{}`, `\cconv`, `\ccorr`, `\hadamard`, `\C`, `\R`, `\SNR`).
- Use relative positioning (`positioning` library) and uniform `\tikzset` styles in TikZ figures.
- Export Python figures as vector PDFs using `plt.savefig(..., format='pdf', bbox_inches='tight')`.
