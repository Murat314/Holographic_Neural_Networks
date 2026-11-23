# From Optical Interference to Latent Superposition

**A Comprehensive Survey on Holographic Neural Networks, Vector Symbolic Architectures, and Their Potential in Modern AI**

**Author:** Murat Durmus  
**Manuscript date:** November 23, 2026  
**Status:** Research survey / preprint; independent verification and peer review remain outstanding.

## Overview

This research survey connects four related lines of work:

- Classical holographic neural networks and optical associative memory
- Holographic reduced representations (HRR/FHRR), vector symbolic architectures (VSA), and hyperdimensional computing (HDC)
- Complex-valued neural networks, spectral token mixing, linear attention, and state-space models
- Photonic, analog, and low-power hardware implementations

The paper develops a common complex-phasor framework for binding, bundling, and unbinding; examines crosstalk and retrieval-capacity trade-offs; and discusses potential hybrid holographic memory architectures for long-context systems.

**Important:** Proposed constant-size holographic memory modules are conceptual research directions, not experimentally established drop-in replacements for Transformer KV caches. The fixed-size trace trades storage growth for interference and finite retrieval capacity.

## Repository structure

```text
.
├── main.tex                  # Main LaTeX document
├── references.bib            # Bibliography
├── sections/                 # Seven manuscript sections
│   ├── 01_intro.tex
│   ├── 02_math.tex
│   ├── 03_history.tex
│   ├── 04_comparison.tex
│   ├── 05_applications.tex
│   ├── 06_potentials.tex
│   └── 07_conclusion.tex
├── figures/                  # TikZ figures, data, and simulation scripts
│   ├── fig_algebra.tex
│   ├── fig_capacity.tex
│   ├── fig_genealogy.tex
│   ├── fig_hybrid_arch.tex
│   ├── capacity_snr.dat
│   ├── simulate_capacity.py
│   ├── simulate_correlated_keys.py
│   └── README.md
├── BIB_VERIFICATION.md       # Bibliography review notes
└── REVISION_REPORT.md        # Revision and validation status
```

This is the intended **source-project layout**. See the repository file browser for the files currently published.

## Build the manuscript

Install a LaTeX distribution with `pdflatex`, `bibtex`, TikZ, and PGFPlots (for example, TeX Live). From the project root, run:

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Alternatively, if `latexmk` is installed:

```bash
latexmk -pdf main.tex
```

The compiled manuscript is `main.pdf`.

## Run simulations

Requires Python 3 with NumPy. Matplotlib is optional for PDF previews.

```bash
python -m pip install numpy matplotlib
python figures/simulate_capacity.py --help
python figures/simulate_correlated_keys.py
```

The first script examines Monte Carlo crosstalk and signal-to-noise behavior under the paper's random-code assumptions. The second explores retrieval under correlated keys as a stress test; its results should not be treated as broad language-model benchmarks.

## Reproducibility and limitations

The supplied revised manuscript contains embedded simulation code and a correlated-key experiment. The complete original Monte Carlo sweep was not fully reproduced during the previous review; smaller functionality checks were performed. In addition, not every bibliographic record or mathematical proof has been independently verified. Consult `REVISION_REPORT.md` and `BIB_VERIFICATION.md` before quoting validation status.

This is primarily a **survey and theoretical synthesis**, not a claim of measured end-to-end superiority over modern attention or state-space architectures.

## Citation

Until a formal publication record or DOI is available, cite the manuscript as:

> Durmus, M. (2026). *From Optical Interference to Latent Superposition: A Comprehensive Survey on Holographic Neural Networks, Vector Symbolic Architectures, and Their Potential in Modern AI*. Research manuscript.

## License

**No license has been specified.** All rights remain reserved unless the repository owner chooses to add a license. Please open an issue for questions about reuse or contributions.
