"""First-order SISO capacity vs. distance: EM through muscle, EM in a fat
channel, and ultrasound through soft tissue, under the same transmit power and
receiver noise assumptions.

This is a *screening* model meant to show where each modality wins and which
assumptions dominate. It is not a substitute for full-wave simulation or
measurement. Every number that matters is in `Assumptions` so it can be swept.

Capacity is computed with water-filling over the usable band
[fc*(1 - fbw/2), fc*(1 + fbw/2)], maximised over the carrier fc. This bounds
what a link with a single antenna/transducer of that fractional bandwidth
could carry.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace

import numpy as np

from tissue import C0, propagation

K_B = 1.380649e-23


@dataclass(frozen=True)
class Assumptions:
    p_tx_dbm: float = 0.0        # 1 mW total transmit power (implant-class)
    nf_db: float = 6.0           # receiver noise figure
    t_k: float = 310.0           # body temperature
    # EM: antenna radiation efficiency in tissue (each end) and directivity.
    em_eff_db: float = -20.0     # at resonance; small implant antennas: -15..-30 dB
    em_size_m: float = 15e-3     # max antenna dimension (implant-scale)
    em_dir_dbi: float = 1.76     # short dipole
    em_fbw: float = 0.3          # usable fractional bandwidth of one antenna
    em_bw_cap_hz: float = 2e9    # instrument/RF chain limit
    # Fat channel: empirical guided-wave loss (Uppsala Fat-IBC measurements
    # report ~0.7 dB/cm in phantom, ~1.9 dB/cm ex vivo, at 1.7-2.6 GHz).
    fat_db_per_cm: float = 1.9
    fat_coupling_db: float = 20.0  # total launch + receive probe loss
    fat_fc_hz: float = 2.2e9
    fat_bw_hz: float = 0.9e9       # ~1.7-2.6 GHz band of those measurements
    # Ultrasound (piston transducer in soft tissue).
    us_alpha_db_cm_mhz: float = 0.75  # soft tissue ~0.5-1.0 dB/(cm MHz)
    us_c: float = 1540.0
    us_diam_m: float = 2e-3           # 2 mm implant-scale transducer
    us_eff_db: float = -6.0           # electro-acoustic efficiency per transducer
    us_fbw: float = 0.7
    # Implementation limit common to all modalities: EVM/phase-noise/ADC
    # bound the usable per-subcarrier SNR (~30 dB for good SDR hardware).
    snr_cap_db: float = 30.0


def noise_psd_w(a: Assumptions) -> float:
    return K_B * a.t_k * 10 ** (a.nf_db / 10)


def em_muscle_gain(f, d, a: Assumptions, tissue="muscle"):
    """Linear power gain Pr/Pt for EM in homogeneous tissue (Friis + absorption)."""
    p = propagation(tissue, f)
    lam = p["wavelength"]
    # Electrically small penalty: below half a tissue wavelength, radiation
    # resistance (and so efficiency) falls roughly as (L / (lam/2))^2.
    small = np.minimum(1.0, (a.em_size_m / (lam / 2)) ** 2)
    g_ant = (10 ** ((a.em_eff_db + a.em_dir_dbi) / 10) * small) ** 2
    return g_ant * (lam / (4 * np.pi * d)) ** 2 * np.exp(-2 * p["alpha"] * d)


def fat_channel_gain_db(d, a: Assumptions):
    return -(a.fat_coupling_db + a.fat_db_per_cm * d * 100)


def us_gain(f, d, a: Assumptions):
    lam = a.us_c / f
    ka = np.pi * a.us_diam_m / lam
    directivity = np.maximum(ka**2, 1.0)  # baffled piston, far field
    # Geometric capture cannot exceed 1 (near field of a collimated piston).
    geo = np.minimum(directivity**2 * (lam / (4 * np.pi * d)) ** 2, 1.0)
    g = 10 ** (2 * a.us_eff_db / 10) * geo
    atten_db = a.us_alpha_db_cm_mhz * (f / 1e6) * d * 100
    return g * 10 ** (-atten_db / 10)


def waterfill_capacity(gain, df, p_tot, n0, snr_cap=np.inf):
    """Rate [bit/s] of parallel Gaussian sub-channels of width df.

    Power is water-filled on the ideal channel; each sub-channel's SNR is then
    combined with the implementation cap as 1/(1/snr + 1/snr_cap).
    """
    inv = n0 / np.maximum(gain, 1e-200)  # noise-to-gain per Hz
    order = np.sort(inv)
    csum = np.cumsum(order)
    n = np.arange(1, len(order) + 1)
    # water level mu with p_tot = df * sum(mu - inv_i) over active channels
    mus = (p_tot / df + csum) / n
    ok = np.nonzero(mus > order)[0]
    if ok.size == 0:
        return 0.0
    mu = mus[ok[-1]]
    active = inv < mu
    snr = mu / inv[active] - 1
    snr = 1 / (1 / snr + 1 / snr_cap)
    return df * np.sum(np.log2(1 + snr))


def best_capacity(gain_fn, fcs, fbw, bw_cap, d, a: Assumptions, npts=256):
    p_tot = 1e-3 * 10 ** (a.p_tx_dbm / 10)
    n0 = noise_psd_w(a)
    best = (0.0, None)
    for fc in fcs:
        bw = min(fbw * fc, bw_cap)
        f = np.linspace(fc - bw / 2, fc + bw / 2, npts)
        c = waterfill_capacity(gain_fn(f, d, a), bw / npts, p_tot, n0,
                               10 ** (a.snr_cap_db / 10))
        if c > best[0]:
            best = (c, fc)
    return best


def scenarios(d, a: Assumptions):
    em_fcs = np.geomspace(100e6, 10e9, 80)
    us_fcs = np.geomspace(0.2e6, 40e6, 80)
    c_mus, f_mus = best_capacity(em_muscle_gain, em_fcs, a.em_fbw, a.em_bw_cap_hz, d, a)
    c_us, f_us = best_capacity(us_gain, us_fcs, a.us_fbw, np.inf, d, a)
    # Fat channel: flat empirical loss over its measured band.
    p_tot = 1e-3 * 10 ** (a.p_tx_dbm / 10)
    snr = p_tot * 10 ** (fat_channel_gain_db(d, a) / 10) / (noise_psd_w(a) * a.fat_bw_hz)
    snr = 1 / (1 / snr + 10 ** (-a.snr_cap_db / 10))
    c_fat = a.fat_bw_hz * np.log2(1 + snr)
    return {
        "EM, muscle (Friis+absorption)": (c_mus, f_mus),
        "EM, fat channel (empirical dB/cm)": (c_fat, a.fat_fc_hz),
        "Ultrasound, soft tissue": (c_us, f_us),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plot", default=None, help="write figure to this path")
    args = ap.parse_args()

    base = Assumptions()
    dists = np.array([1, 2, 3, 5, 7, 10, 15, 20]) * 1e-2

    print(f"{'d[cm]':>5s}  " + "  ".join(f"{k[:30]:>30s}" for k in scenarios(0.05, base)))
    rows = []
    for d in dists:
        s = scenarios(d, base)
        rows.append(s)
        cells = [f"{c/1e6:9.1f} Mb/s @{fc/1e9 if fc > 1e8 else fc/1e6:6.2f}{'G' if fc > 1e8 else 'M'}"
                 for c, fc in s.values()]
        print(f"{d*100:5.0f}  " + "  ".join(f"{x:>30s}" for x in cells))

    # Sensitivity: the assumptions that move the answer most.
    print("\nSensitivity at d = 5 cm (capacity in Mb/s):")
    sweeps = {
        "baseline": base,
        "EM antenna eff -10 dB": replace(base, em_eff_db=-10),
        "EM antenna eff -30 dB": replace(base, em_eff_db=-30),
        "EM antenna size 5 mm": replace(base, em_size_m=5e-3),
        "EM antenna size 30 mm": replace(base, em_size_m=30e-3),
        "Ptx 10 mW": replace(base, p_tx_dbm=10),
        "Ptx 0.1 mW": replace(base, p_tx_dbm=-10),
        "fat 0.7 dB/cm (phantom)": replace(base, fat_db_per_cm=0.7),
        "US 1.0 dB/cm/MHz, -10 dB eff": replace(base, us_alpha_db_cm_mhz=1.0, us_eff_db=-10),
        "no SNR cap (ideal hardware)": replace(base, snr_cap_db=200),
    }
    for name, a in sweeps.items():
        s = scenarios(0.05, a)
        print(f"  {name:32s} " + "  ".join(f"{c/1e6:8.1f}" for c, _ in s.values()))

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        dd = np.linspace(0.5, 20, 60) * 1e-2
        fig, ax = plt.subplots(figsize=(7, 4.5))
        curves = {k: [] for k in scenarios(0.05, base)}
        lo_c = {k: [] for k in curves}
        hi_c = {k: [] for k in curves}
        lo_a = replace(base, em_eff_db=-30, fat_db_per_cm=2.5, us_eff_db=-10, us_alpha_db_cm_mhz=1.0)
        hi_a = replace(base, em_eff_db=-10, fat_db_per_cm=0.7, us_eff_db=-3, us_alpha_db_cm_mhz=0.5)
        for d in dd:
            for store, a in ((curves, base), (lo_c, lo_a), (hi_c, hi_a)):
                for k, (c, _) in scenarios(d, a).items():
                    store[k].append(max(c, 1.0))
        for i, k in enumerate(curves):
            ax.semilogy(dd * 100, np.array(curves[k]) / 1e6, color=f"C{i}", label=k)
            ax.fill_between(dd * 100, np.array(lo_c[k]) / 1e6, np.array(hi_c[k]) / 1e6,
                            color=f"C{i}", alpha=0.15)
        ax.set_xlabel("distance through tissue [cm]")
        ax.set_ylabel("SISO capacity [Mb/s]  (Ptx = 1 mW)")
        ax.set_ylim(1e-2, 1e5)
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8)
        ax.set_title("Screening model: SISO capacity vs distance (bands = pessimistic/optimistic)")
        fig.tight_layout()
        fig.savefig(args.plot, dpi=150)
        print(f"\nwrote {args.plot}")


if __name__ == "__main__":
    main()
