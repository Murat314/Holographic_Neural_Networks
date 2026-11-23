"""
Reproducible Monte Carlo simulation for Section 2 (Theorem 2.8: SNR Scaling Law)
and Figure 2(a) (figures/fig_capacity.tex).

Evaluates empirical vs. analytical discrimination Signal-to-Noise Ratio (SNR):
    SNR_disc = (E[S_q] - E[S'])^2 / Var(S_q - S')
for:
  1. Unitary Complex Phasors (FHRR on T^D), where Theorem 2.8 predicts
       SNR_FHRR^disc = 2D / (2N - 1) ~ (N / D)^(-1),
  2. Real-Valued Gaussian HRR (R^D, i.i.d. N(0, 1/D)), where Theorem 2.8 predicts
       SNR_HRR^disc  = D / (2N + 6 + 6/D) ~ (1/2) * (N / D)^(-1)  (for even D).

Outputs:
  - figures/capacity_snr.dat : whitespace-delimited table consumed by PGFPlots
                               in figures/fig_capacity.tex.
  - Optional vector PDF preview (figures/fig_capacity_preview.pdf) when invoked
    with --plot-pdf and matplotlib is installed.

Usage:
    python figures/simulate_capacity.py
    python figures/simulate_capacity.py --plot-pdf
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np


@dataclass(frozen=True)
class ExperimentConfig:
    """Simulation configuration for a fixed dimensionality D."""

    dim: int
    loads: Tuple[int, ...]
    trials: int
    batch_size: int
    chunk_size: int = 8


@dataclass(frozen=True)
class SNRResult:
    """Empirical and theoretical SNR metrics for a single (D, N) operating point."""

    dim: int
    load: int
    load_ratio: float
    snr_fhrr_emp: float
    snr_fhrr_theory: float
    snr_hrr_emp: float
    snr_hrr_theory: float


def theoretical_snr_fhrr(dim: int, load: int) -> float:
    """Exact discrimination SNR for unitary FHRR on T^D (Theorem 2.8, Part 1)."""
    return (2.0 * dim) / (2.0 * load - 1.0)


def theoretical_snr_hrr(dim: int, load: int) -> float:
    """Exact discrimination SNR for real Gaussian HRR on R^D (even D; Theorem 2.8, Part 2)."""
    var_sq = (load + 5.0) / dim + 4.0 / (dim ** 2)
    var_sp = (load + 1.0) / dim + 2.0 / (dim ** 2)
    return 1.0 / (var_sq + var_sp)


def _compute_disc_snr(sq: np.ndarray, sp: np.ndarray) -> float:
    """Compute empirical discrimination SNR = (E[S_q] - E[S'])^2 / Var(S_q - S')."""
    mean_gap = float(np.mean(sq) - np.mean(sp))
    var_diff = float(np.var(sq - sp, ddof=1))
    return (mean_gap ** 2) / var_diff


def simulate_fhrr_sweep(
    cfg: ExperimentConfig,
    rng: np.random.Generator,
) -> Dict[int, float]:
    """Incrementally accumulate unitary FHRR traces across sorted loads N."""
    sorted_loads = sorted(cfg.loads)
    dim = cfg.dim
    sq_by_load: Dict[int, np.ndarray] = {
        n: np.empty(cfg.trials, dtype=np.float64) for n in sorted_loads
    }
    sp_by_load: Dict[int, np.ndarray] = {
        n: np.empty(cfg.trials, dtype=np.float64) for n in sorted_loads
    }

    pi32 = np.float32(np.pi)
    for start in range(0, cfg.trials, cfg.batch_size):
        b = min(cfg.batch_size, cfg.trials - start)
        phi_q = rng.uniform(-pi32, pi32, size=(b, dim)).astype(np.float32)
        psi_q = rng.uniform(-pi32, pi32, size=(b, dim)).astype(np.float32)
        psi_p = rng.uniform(-pi32, pi32, size=(b, dim)).astype(np.float32)

        k_q = np.exp(1j * phi_q)
        v_q = np.exp(1j * psi_q)
        v_p = np.exp(1j * psi_p)

        # Start trace M with the target bound pair (load = 1)
        trace_m = (k_q * v_q).astype(np.complex64)
        current_load = 1

        for target_load in sorted_loads:
            remaining = target_load - current_load
            while remaining > 0:
                c = min(cfg.chunk_size, remaining)
                phi_c = rng.uniform(-pi32, pi32, size=(b, c, dim)).astype(np.float32)
                psi_c = rng.uniform(-pi32, pi32, size=(b, c, dim)).astype(np.float32)
                trace_m += np.sum(np.exp(1j * (phi_c + psi_c)), axis=1)
                remaining -= c
            current_load = target_load

            # Unbind via phase conjugation: V_hat_q = conj(K_q) odot M
            v_hat = np.conj(k_q) * trace_m
            sq_by_load[target_load][start : start + b] = (
                np.real(np.sum(np.conj(v_q) * v_hat, axis=1, dtype=np.complex128)) / dim
            )
            sp_by_load[target_load][start : start + b] = (
                np.real(np.sum(np.conj(v_p) * v_hat, axis=1, dtype=np.complex128)) / dim
            )

    return {
        n: _compute_disc_snr(sq_by_load[n], sp_by_load[n]) for n in sorted_loads
    }


def simulate_hrr_sweep(
    cfg: ExperimentConfig,
    rng: np.random.Generator,
) -> Dict[int, float]:
    """Incrementally accumulate real Gaussian HRR traces across sorted loads N."""
    sorted_loads = sorted(cfg.loads)
    dim = cfg.dim
    scale = float(1.0 / np.sqrt(dim))

    sq_by_load: Dict[int, np.ndarray] = {
        n: np.empty(cfg.trials, dtype=np.float64) for n in sorted_loads
    }
    sp_by_load: Dict[int, np.ndarray] = {
        n: np.empty(cfg.trials, dtype=np.float64) for n in sorted_loads
    }

    for start in range(0, cfg.trials, cfg.batch_size):
        b = min(cfg.batch_size, cfg.trials - start)
        k_q = rng.normal(0.0, scale, size=(b, dim)).astype(np.float32)
        v_q = rng.normal(0.0, scale, size=(b, dim)).astype(np.float32)
        v_p = rng.normal(0.0, scale, size=(b, dim)).astype(np.float32)

        kf_q = np.fft.rfft(k_q, axis=-1)
        vf_q = np.fft.rfft(v_q, axis=-1)
        trace_mf = kf_q * vf_q
        current_load = 1

        for target_load in sorted_loads:
            remaining = target_load - current_load
            while remaining > 0:
                c = min(cfg.chunk_size, remaining)
                k_c = rng.normal(0.0, scale, size=(b, c, dim)).astype(np.float32)
                v_c = rng.normal(0.0, scale, size=(b, c, dim)).astype(np.float32)
                trace_mf += np.sum(
                    np.fft.rfft(k_c, axis=-1) * np.fft.rfft(v_c, axis=-1), axis=1
                )
                remaining -= c
            current_load = target_load

            # Unbind via circular correlation: v_hat = IDFT(conj(DFT(k_q)) odot DFT(m))
            v_hat = np.fft.irfft(np.conj(kf_q) * trace_mf, n=dim, axis=-1)
            sq_by_load[target_load][start : start + b] = np.sum(
                v_q.astype(np.float64) * v_hat, axis=1
            )
            sp_by_load[target_load][start : start + b] = np.sum(
                v_p.astype(np.float64) * v_hat, axis=1
            )

    return {
        n: _compute_disc_snr(sq_by_load[n], sp_by_load[n]) for n in sorted_loads
    }


def run_benchmark(configs: Sequence[ExperimentConfig], seed: int = 2026) -> List[SNRResult]:
    """Run the full Monte Carlo suite across all configured (D, N) points."""
    rng = np.random.default_rng(seed)
    results: List[SNRResult] = []

    for cfg in configs:
        fhrr_map = simulate_fhrr_sweep(cfg, rng)
        hrr_map = simulate_hrr_sweep(cfg, rng)
        for load in sorted(cfg.loads):
            results.append(
                SNRResult(
                    dim=cfg.dim,
                    load=load,
                    load_ratio=load / cfg.dim,
                    snr_fhrr_emp=fhrr_map[load],
                    snr_fhrr_theory=theoretical_snr_fhrr(cfg.dim, load),
                    snr_hrr_emp=hrr_map[load],
                    snr_hrr_theory=theoretical_snr_hrr(cfg.dim, load),
                )
            )
    return results


def write_pgfplots_table(results: Sequence[SNRResult], output_path: Path) -> None:
    """Write whitespace-delimited table compatible with PGFPlots \\addplot table."""
    header = (
        "D N load_ratio snr_fhrr_emp snr_fhrr_theory snr_hrr_emp snr_hrr_theory\n"
    )
    lines = [header]
    for r in results:
        lines.append(
            f"{r.dim:d} {r.load:d} {r.load_ratio:.8f} "
            f"{r.snr_fhrr_emp:.6f} {r.snr_fhrr_theory:.6f} "
            f"{r.snr_hrr_emp:.6f} {r.snr_hrr_theory:.6f}\n"
        )
    output_path.write_text("".join(lines), encoding="utf-8")


def export_optional_pdf(results: Sequence[SNRResult], pdf_path: Path) -> None:
    """Optionally render a matplotlib vector PDF preview if matplotlib is available."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[info] matplotlib is not installed; skipping PDF preview export.")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0))
    markers: Dict[int, str] = {256: "o", 1024: "s", 4096: "^"}

    ratios = np.logspace(-2.5, -0.3, 200)
    ax1.loglog(ratios, 1.0 / ratios, color="#009988", lw=1.8, label=r"FHRR theory $(N/D)^{-1}$")
    ax1.loglog(ratios, 0.5 / ratios, color="#D55E00", ls="--", lw=1.8, label=r"HRR theory $\frac{1}{2}(N/D)^{-1}$")

    for dim in sorted({r.dim for r in results}):
        sub = [r for r in results if r.dim == dim]
        x = [r.load_ratio for r in sub]
        ax1.loglog(x, [r.snr_fhrr_emp for r in sub], markers[dim], color="#009988", mfc="white", ms=5, label=f"FHRR MC (D={dim})")
        ax1.loglog(x, [r.snr_hrr_emp for r in sub], markers[dim], color="#D55E00", ms=4.5, label=f"HRR MC (D={dim})")

    ax1.set_xlabel(r"Load Ratio $N / D$")
    ax1.set_ylabel(r"Discrimination $\mathrm{SNR}$")
    ax1.grid(True, which="both", alpha=0.25)
    ax1.legend(fontsize=7, ncol=2)

    d_ref = 4096
    n_vals = np.logspace(1, 6, 200)
    ax2.loglog(n_vals, n_vals ** 2, color="#D55E00", ls="--", lw=1.8, label=r"Attention matrix $N^2$")
    ax2.loglog(n_vals, 2.0 * n_vals * d_ref, color="#004488", ls="-.", lw=1.8, label=r"KV-cache $2ND$")
    ax2.loglog(n_vals, np.full_like(n_vals, 2.0 * d_ref ** 2), color="#E69F00", ls=":", lw=1.8, label=r"HNN matrix $2D^2$")
    ax2.loglog(n_vals, np.full_like(n_vals, 2.0 * d_ref), color="#009988", lw=2.0, label=r"Holographic trace $2D$")
    ax2.set_xlabel(r"Sequence Length / Stored Items $N$")
    ax2.set_ylabel(r"State Memory Footprint (Real Scalars, $D=4096$)")
    ax2.grid(True, which="both", alpha=0.25)
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    print(f"[ok] Saved vector PDF preview to {pdf_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate Theorem 2.8 SNR scaling.")
    parser.add_argument("--seed", type=int, default=2026, help="Random seed.")
    parser.add_argument(
        "--plot-pdf",
        action="store_true",
        help="Also export a matplotlib PDF preview if matplotlib is installed.",
    )
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent
    dat_path = out_dir / "capacity_snr.dat"
    pdf_path = out_dir / "fig_capacity_preview.pdf"

    configs = [
        ExperimentConfig(dim=256, loads=(2, 4, 8, 16, 32, 64, 128), trials=2000, batch_size=200, chunk_size=16),
        ExperimentConfig(dim=1024, loads=(4, 8, 16, 32, 64, 128), trials=1200, batch_size=100, chunk_size=8),
        ExperimentConfig(dim=4096, loads=(16, 32, 64, 128), trials=600, batch_size=50, chunk_size=4),
    ]

    results = run_benchmark(configs, seed=args.seed)
    write_pgfplots_table(results, dat_path)

    print(f"[ok] Wrote {len(results)} Monte Carlo data points to {dat_path}")
    print(f"{'D':>5} {'N':>4} {'N/D':>8} | {'FHRR_emp':>9} {'FHRR_th':>9} | {'HRR_emp':>9} {'HRR_th':>9}")
    print("-" * 66)
    for r in results:
        print(
            f"{r.dim:5d} {r.load:4d} {r.load_ratio:8.5f} | "
            f"{r.snr_fhrr_emp:9.3f} {r.snr_fhrr_theory:9.3f} | "
            f"{r.snr_hrr_emp:9.3f} {r.snr_hrr_theory:9.3f}"
        )

    if args.plot_pdf:
        export_optional_pdf(results, pdf_path)


if __name__ == "__main__":
    main()
