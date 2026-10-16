"""How many spatial streams does tissue support? Scalar-Green's-function MIMO
model between two parallel square arrays in a homogeneous lossy medium.

    H_ij = a_el * lam / (4 pi r_ij) * exp(-j k r_ij),   k = beta - j alpha

Elements sit on a lambda_tissue/2 grid that fits inside each aperture, which is
the usual no-superdirectivity limit. Reported per configuration:

  * n_tx x n_rx element counts,
  * usable eigenchannels (those that receive power under water-filling),
  * C_MIMO / C_BF: spatial-multiplexing gain over beamforming on the *same*
    arrays. This isolates what "spatial orthogonality" adds beyond array gain.

Limitations (deliberate, first-order): scalar field (polarisation could add up
to x2-x3 in the reactive near field), no mutual coupling, no layered tissue or
reflections, element pattern ignored. Use full-wave EM (openEMS/Sim4Life) to
confirm any configuration before building it.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np

from link_budget import K_B
from tissue import propagation


@dataclass(frozen=True)
class Link:
    medium: str          # tissue name, or "ultrasound"
    f_hz: float
    l_tx_m: float        # implant aperture (side of square)
    l_rx_m: float        # external aperture
    bw_hz: float = 100e6
    p_tx_dbm: float = 0.0
    nf_db: float = 6.0
    el_gain_db: float = -18.2   # -20 dB efficiency + 1.76 dBi, per element
    snr_cap_db: float = 30.0
    max_side: int = 8           # cap elements per side (RF-chain realism)


def k_and_lam(link: Link):
    if link.medium == "ultrasound":
        lam = 1540.0 / link.f_hz
        alpha = 0.75 / 8.686 * 100 * (link.f_hz / 1e6)  # Np/m
        return 2 * np.pi / lam - 1j * alpha, lam
    p = propagation(link.medium, link.f_hz)
    return p["beta"] - 1j * p["alpha"], p["wavelength"]


def grid(side_m, lam, max_side):
    n = int(min(max_side, max(1, np.floor(side_m / (lam / 2)) + 1)))
    if n == 1:
        x = np.zeros(1)
    else:
        x = (np.arange(n) - (n - 1) / 2) * (lam / 2)
    xx, yy = np.meshgrid(x, x)
    return np.column_stack([xx.ravel(), yy.ravel()])


def channel(link: Link, d):
    k, lam = k_and_lam(link)
    tx = grid(link.l_tx_m, lam, link.max_side)
    rx = grid(link.l_rx_m, lam, link.max_side)
    dx = rx[:, None, :] - tx[None, :, :]
    r = np.sqrt(np.sum(dx**2, axis=-1) + d**2)
    a_el = 10 ** (link.el_gain_db / 20)
    h = a_el**2 * lam / (4 * np.pi * r) * np.exp(-1j * k * r)
    centre = (np.argmin(np.hypot(*rx.T)), np.argmin(np.hypot(*tx.T)))
    return h, len(tx), len(rx), centre


def capacities(link: Link, d):
    h, nt, nr, centre = channel(link, d)
    s2 = np.linalg.svd(h, compute_uv=False) ** 2
    p = 1e-3 * 10 ** (link.p_tx_dbm / 10)
    n = K_B * 310 * 10 ** (link.nf_db / 10) * link.bw_hz
    cap = 10 ** (link.snr_cap_db / 10)
    # water-fill over eigenchannels
    inv = np.sort(n / np.maximum(s2, 1e-300))
    best = None
    for m in range(len(inv), 0, -1):
        mu = (p + inv[:m].sum()) / m
        if mu > inv[m - 1]:
            best = (mu, m)
            break
    mu, m = best
    snr = mu / inv[:m] - 1
    eff = 1 / (1 / snr + 1 / cap)
    # Optimal MIMO is never worse than beamforming; the SNR cap applied after
    # water-filling can make the two-step estimate dip below it.
    c_mimo = link.bw_hz * np.sum(np.log2(1 + eff))
    snr_bf = p * s2.max() / n
    c_bf = link.bw_hz * np.log2(1 + 1 / (1 / snr_bf + 1 / cap))
    c_mimo = max(c_mimo, c_bf)
    # SISO: centre element to centre element
    snr_siso = p * abs(h[centre]) ** 2 / n
    c_siso = link.bw_hz * np.log2(1 + 1 / (1 / snr_siso + 1 / cap))
    return dict(nt=nt, nr=nr, streams=m, c_mimo=c_mimo, c_bf=c_bf, c_siso=c_siso,
                snr_bf_db=10 * np.log10(snr_bf))


CONFIGS = {
    "muscle 1.3 GHz, 2 cm -> 4 cm": Link("muscle", 1.3e9, 0.02, 0.04),
    "muscle 2.45 GHz, 1 cm -> 4 cm": Link("muscle", 2.45e9, 0.01, 0.04),
    "muscle 2.45 GHz, 2 cm -> 4 cm": Link("muscle", 2.45e9, 0.02, 0.04),
    "muscle 5.8 GHz, 1 cm -> 4 cm": Link("muscle", 5.8e9, 0.01, 0.04),
    "fat 2.45 GHz, 2 cm -> 4 cm": Link("fat", 2.45e9, 0.02, 0.04),
    "fat 5.8 GHz, 2 cm -> 4 cm": Link("fat", 5.8e9, 0.02, 0.04),
    "ultrasound 5 MHz, 2 mm -> 1 cm (BW 3 MHz)": Link("ultrasound", 5e6, 0.002, 0.01, bw_hz=3e6,
                                                     el_gain_db=-6.0, max_side=6),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plot", default=None)
    args = ap.parse_args()
    dists = [0.01, 0.02, 0.03, 0.05, 0.08]
    print(f"{'configuration':44s} {'d':>4s} {'Nt x Nr':>8s} {'strm':>4s} {'SNR_BF':>7s} "
          f"{'SISO':>9s} {'BF':>9s} {'MIMO':>9s} {'MIMO/BF':>7s}")
    results = {}
    for name, link in CONFIGS.items():
        results[name] = []
        for d in dists:
            r = capacities(link, d)
            results[name].append(r)
            print(f"{name:44s} {d*100:3.0f}cm {r['nt']:3d}x{r['nr']:<4d} {r['streams']:4d} "
                  f"{r['snr_bf_db']:6.1f}dB {r['c_siso']/1e6:8.1f}M {r['c_bf']/1e6:8.1f}M "
                  f"{r['c_mimo']/1e6:8.1f}M {r['c_mimo']/max(r['c_bf'],1):7.2f}")
        print()

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        dd = np.linspace(0.005, 0.10, 40)
        fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
        for i, (name, link) in enumerate(CONFIGS.items()):
            rr = [capacities(link, d) for d in dd]
            axs[0].plot(dd * 100, [r["streams"] for r in rr], color=f"C{i}", label=name)
            axs[1].plot(dd * 100, [r["c_mimo"] / max(r["c_bf"], 1) for r in rr], color=f"C{i}")
        axs[0].set_ylabel("eigenchannels used (water-filling)")
        axs[1].set_ylabel("C_MIMO / C_beamforming (same arrays)")
        for ax in axs:
            ax.set_xlabel("implant-to-array distance [cm]")
            ax.grid(alpha=0.3)
        axs[0].set_yscale("log", base=2)
        axs[0].legend(fontsize=7)
        fig.suptitle("Spatial multiplexing in tissue: scalar lossy-medium model, Ptx = 1 mW")
        fig.tight_layout()
        fig.savefig(args.plot, dpi=150)
        print(f"wrote {args.plot}")


if __name__ == "__main__":
    main()
