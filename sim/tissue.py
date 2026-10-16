"""Tissue dielectric properties (Gabriel et al. 1996, 4-pole Cole-Cole) and
plane-wave propagation constants in lossy tissue.

Reference:
    S. Gabriel, R. W. Lau, C. Gabriel, "The dielectric properties of biological
    tissues: III. Parametric models for the dielectric spectrum of tissues",
    Phys. Med. Biol. 41 (1996) 2271-2293.

    eps(w) = ef + sum_n del_n / (1 + (j w tau_n)^(1 - alf_n)) + sig / (j w eps0)

The parameter table below was transcribed from the paper; `_self_check()`
compares it against tabulated single-frequency values (IT'IS / IFAC database)
so a transcription error shows up immediately. Re-verify against the IFAC
database (niremf.ifac.cnr.it) before using numbers in a publication.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

EPS0 = 8.8541878128e-12
MU0 = 4e-7 * np.pi
C0 = 299_792_458.0
ETA0 = np.sqrt(MU0 / EPS0)


@dataclass(frozen=True)
class ColeCole:
    ef: float
    poles: tuple[tuple[float, float, float], ...]  # (del, tau [s], alf)
    sig: float  # static ionic conductivity [S/m]

    def eps_complex(self, f):
        """Complex relative permittivity eps' - j eps'' (includes conductivity)."""
        w = 2 * np.pi * np.asarray(f, dtype=float)
        eps = np.full_like(w, self.ef, dtype=complex)
        for d, tau, a in self.poles:
            if d:
                eps += d / (1 + (1j * w * tau) ** (1 - a))
        return eps + self.sig / (1j * w * EPS0)


def _cc(ef, d1, t1ps, a1, d2, t2ns, a2, sig, d3=0, t3us=1, a3=0, d4=0, t4ms=1, a4=0):
    return ColeCole(
        ef,
        (
            (d1, t1ps * 1e-12, a1),
            (d2, t2ns * 1e-9, a2),
            (d3, t3us * 1e-6, a3),
            (d4, t4ms * 1e-3, a4),
        ),
        sig,
    )


TISSUES: dict[str, ColeCole] = {
    "muscle": _cc(4.0, 50.0, 7.234, 0.10, 7000, 353.678, 0.10, 0.200, 1.2e6, 318.310, 0.10, 2.5e7, 2.274, 0.00),
    "fat": _cc(2.5, 3.0, 7.958, 0.20, 15, 15.915, 0.10, 0.010, 3.3e4, 159.155, 0.05, 1e7, 7.958, 0.01),
    "fat_infiltrated": _cc(2.5, 9.0, 7.958, 0.20, 35, 15.915, 0.10, 0.035, 3.3e4, 159.155, 0.05, 1e7, 15.915, 0.01),
    "skin_dry": _cc(4.0, 32.0, 7.234, 0.00, 1100, 32.481, 0.20, 0.0002),
    "skin_wet": _cc(4.0, 39.0, 7.958, 0.10, 280, 79.577, 0.00, 0.0004, 3e4, 1.592, 0.16, 3e4, 1.592, 0.20),
    "blood": _cc(4.0, 56.0, 8.377, 0.10, 5200, 132.629, 0.10, 0.700),
    "bone_cortical": _cc(2.5, 10.0, 13.263, 0.20, 180, 79.577, 0.20, 0.020, 5000, 159.155, 0.20, 1e5, 15.915, 0.00),
    "brain_grey": _cc(4.0, 45.0, 7.958, 0.10, 400, 15.915, 0.15, 0.020, 2e5, 106.103, 0.22, 4.5e7, 5.305, 0.00),
}


def props(tissue: str, f):
    """Return (eps_r', sigma_eff [S/m]) at frequency f."""
    eps = TISSUES[tissue].eps_complex(f)
    w = 2 * np.pi * np.asarray(f, dtype=float)
    return eps.real, -eps.imag * w * EPS0


def propagation(tissue: str, f):
    """Plane-wave constants in tissue.

    Returns dict with alpha [Np/m], beta [rad/m], wavelength [m],
    penetration (skin) depth [m], loss [dB/cm], intrinsic impedance [ohm].
    """
    eps = TISSUES[tissue].eps_complex(f)
    k0 = 2 * np.pi * np.asarray(f, dtype=float) / C0
    k = k0 * np.sqrt(eps)  # eps has negative imag part -> k = beta - j alpha
    alpha = -k.imag
    beta = k.real
    return {
        "alpha": alpha,
        "beta": beta,
        "wavelength": 2 * np.pi / beta,
        "depth": 1 / alpha,
        "db_per_cm": 8.686 * alpha / 100,
        "eta": ETA0 / np.sqrt(eps),
    }


def _self_check():
    # (tissue, f [Hz], eps_r, sigma [S/m]) from the IT'IS/IFAC tabulated values.
    ref = [
        ("muscle", 403e6, 57.1, 0.797),
        ("muscle", 915e6, 55.0, 0.948),
        ("muscle", 2.45e9, 52.7, 1.74),
        ("muscle", 5.8e9, 48.5, 4.96),
        ("fat", 2.45e9, 5.28, 0.105),
        ("skin_dry", 2.45e9, 38.0, 1.46),
        ("blood", 2.45e9, 58.3, 2.54),
    ]
    worst = 0.0
    for t, f, er, sg in ref:
        e, s = props(t, f)
        err = max(abs(e / er - 1), abs(s / sg - 1))
        worst = max(worst, err)
        print(f"{t:10s} {f/1e9:5.3f} GHz  eps'={e:6.2f} (ref {er:5.2f})  "
              f"sigma={s:5.3f} (ref {sg:5.3f})  err={100*err:4.1f}%")
    return worst


def plot(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    f = np.geomspace(10e6, 10e9, 400)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for t in ("muscle", "skin_wet", "fat", "blood", "bone_cortical"):
        p = propagation(t, f)
        axs[0].loglog(f / 1e9, p["db_per_cm"], label=t)
        axs[1].loglog(f / 1e9, 1e3 * p["wavelength"], label=t)
    axs[0].set_ylabel("plane-wave loss [dB/cm]")
    axs[1].set_ylabel("wavelength in tissue [mm]")
    for ax in axs:
        ax.set_xlabel("frequency [GHz]")
        ax.grid(True, which="both", alpha=0.3)
    axs[0].legend(fontsize=8)
    fig.suptitle("Gabriel 1996 tissue model: absorption and in-tissue wavelength")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"wrote {path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2 and sys.argv[1] == "--plot":
        plot(sys.argv[2])
    worst = _self_check()
    print(f"worst relative error vs reference: {100*worst:.1f}%")
    print()
    print(f"{'tissue':16s} {'f[GHz]':>7s} {'eps_r':>6s} {'sig':>6s} {'lam[mm]':>8s} "
          f"{'depth[mm]':>9s} {'dB/cm':>6s}")
    for t in ("muscle", "fat", "skin_wet", "blood"):
        for f in (0.403e9, 0.915e9, 2.45e9, 5.8e9, 8e9):
            e, s = props(t, f)
            p = propagation(t, f)
            print(f"{t:16s} {f/1e9:7.3f} {e:6.1f} {s:6.2f} {1e3*p['wavelength']:8.1f} "
                  f"{1e3*p['depth']:9.1f} {p['db_per_cm']:6.2f}")
