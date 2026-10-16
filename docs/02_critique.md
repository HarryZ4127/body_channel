# Critique, rebuttals, and suggestions

This is a deliberately adversarial review of the idea *"use the body as an EM
channel, exploit spatial orthogonality with MIMO, and beat ultrasound on data
rate."* Each point states the objection a reviewer is likely to raise, what our
screening models say ([`sim/`](../sim)), and what to do about it.

Numbers below come from the first-order models in this repo (1 mW Tx, 6 dB NF,
30 dB implementation SNR cap, −20 dB implant-antenna efficiency, 1.5 cm antenna).
They are for *steering the research*, not for publication. See
[`figures/siso_table.txt`](figures/siso_table.txt) and
[`figures/mimo_table.txt`](figures/mimo_table.txt).

> **Interpretation note.** We read "special orthogonality" as **spatial
> orthogonality**, i.e. separating streams through the eigenmodes of the
> multi-antenna channel. If you meant something else (waveguide-mode
> orthogonality in the fat layer, polarisation, OAM), §S3–S4 cover those.

---

## What is strong about the idea (steelman)

1. **The bandwidth argument is real.** At GHz carriers an EM link can use
   hundreds of MHz. Ultrasound transducers sit at 1–40 MHz with tens of percent
   fractional bandwidth, and attenuation grows linearly with frequency
   (~0.5–1 dB/cm/MHz). At 1–5 cm our model gives EM through muscle ~0.9–5 Gb/s
   vs ultrasound ~80–280 Mb/s (SISO, same power).
2. **Tissue shrinks the wavelength.** Muscle has ε′≈53 at 2.45 GHz, so
   λ drops from 12.2 cm in air to 1.7 cm. Arrays fit into implant-scale
   apertures that would be useless in air. This is the physical basis for
   "spatial orthogonality in the body".
3. **There is a measurable gap.** We found antenna papers that report MIMO
   implant capacity from simulation or at a *normalised* SNR. We found no
   published measured, real-time, spatially multiplexed through-tissue EM link
   with absolute link budgets. That's the publishable opening (see
   [01_landscape.md](01_landscape.md)).
4. **There is a killer application.** High-channel-count neural interfaces need
   ~100–200+ Mb/s uplinks (e.g. 1024 ch × 20 kS/s × 10 b ≈ 205 Mb/s raw).
   Today's MedRadio and BLE links run at ~1 Mb/s or less, so BCIs compress
   heavily or use wires.

---

## Major critiques

### C1. "EM gives a *way* higher data rate than ultrasound" is only true inside a distance/geometry envelope

* EM absorption in muscle is **3.9 dB/cm at 2.45 GHz** and **11.5 dB/cm at
  5.8 GHz** (plane wave). Ultrasound at 5 MHz is ~3.75 dB/cm.
* In our SISO model (muscle, 1 mW), **EM wins below ~10 cm and ultrasound wins
  beyond ~10–12 cm**
  ([figure](figures/siso_capacity_vs_distance.png)). At 15 cm EM is ~2 Mb/s
  vs ultrasound ~19 Mb/s.
* The EM curve depends heavily on the implant antenna. At 5 cm, ±10 dB of
  antenna efficiency swings capacity from **24 Mb/s to 3.5 Gb/s**. Shrinking
  the antenna from 15 mm to 5 mm drops it from 914 to **31 Mb/s**. Ultrasound
  is far less sensitive to transducer size.
* The fair comparison also needs **equal device volume**. A 2 mm ultrasound
  crystal is practical. An efficient 2.45 GHz in-muscle antenna is ~1–2 cm.

**Rebuttal to prepare:** Don't claim "EM > ultrasound" in general. Claim
"for depths ≤ *X* cm and implant apertures ≥ *Y* mm, EM-MIMO achieves *N*×
the rate of the best reported ultrasonic links at the same power and safety
limits." Then measure *X* and *Y*.

### C2. Spatial degrees of freedom are set by aperture, tissue wavelength and distance, not by antenna count

* The usable streams scale roughly like the Fresnel number
  N ≈ (A_tx·A_rx)/(λ_t·d)². Loss in tissue adds a spatial low-pass effect.
  High-angle (high spatial frequency) components travel farther through lossy
  tissue, so they die first.
* **Fat at 2.45 GHz has λ_t ≈ 5.3 cm.** A 2 cm implant fits *one* λ/2-spaced
  element, so in our model there is **zero spatial multiplexing in the fat
  channel at 2.45 GHz**. You need ~5.8 GHz (λ_t ≈ 2.3 cm) to get ~4 streams.
* **Muscle at 2.45 GHz:** with a 2 cm → 4 cm aperture we get ~9 streams at
  1 cm, ~4 at 5 cm, and 1 at 8 cm. The multiplexing gain over beamforming on
  the same arrays (C_MIMO/C_BF) is **7.7× at 1 cm, 1.9× at 5 cm, 1.0× at
  8 cm** ([figure](figures/mimo_streams_vs_distance.png)).
* **The tension:** the high-SNR channel (fat) has few spatial modes. The
  many-mode channels (muscle, higher frequency) have low SNR. The sweet spot is
  narrow and has to be found by measurement.

**Rebuttal to prepare:** Show measured singular-value spectra vs depth and
frequency, and state the depth at which rank collapses. That curve is
publishable on its own, and our model predicts its shape.

### C3. MIMO is not a unique EM advantage. Ultrasound has *more* spatial DoF per aperture

* Ultrasound at 5 MHz has λ ≈ 0.3 mm, so a 2 mm transducer already holds a
  6×6 array. UIUC has published work on exploiting spatial DoF for ultrasound
  implant links (arXiv 1702.05154).
* So "MIMO" is not the differentiator vs ultrasound. **Bandwidth × multiple
  streams** is. Make the argument as *spectral efficiency × bandwidth*, and
  compare against the ultrasonic MIMO number too, not just ultrasonic SISO.

### C4. At low SNR, MIMO gives array gain, not multiplexing

Spatial multiplexing pays off only when each eigenchannel has decent SNR.
Through-tissue links are power-limited, so the dominant benefit at depth will
be **beamforming gain** (up to N_t·N_r). That's useful, but it's a different
claim. **Always report C_MIMO alongside C_BF and C_SISO on the same hardware**,
and say which regime each measurement is in.

### C5. "bps/Hz at 20 dB SNR" style results are misleading. Don't report them

Several implant-MIMO antenna papers compute capacity at a *fixed normalised
SNR*. That hides the path loss, which is the whole problem. Reviewers in
comms will reject this. **Report capacity at a fixed absolute Tx power that is
SAR-compliant, with measured noise floor and bandwidth.**

### C6. Implant-side cost: N RF chains, N× power, N× area

A 4×4 MIMO implant needs 4 transmit chains, coherent LO distribution and
4 antennas in ~1–2 cm. At pJ/bit levels the RF chains, not the channel, may
set the limit. Options that keep the implant simple:

* **Asymmetric SIMO/MIMO:** few implant antennas, a large external array on a
  skin patch, and all the heavy processing outside.
* **Multi-implant (distributed) MU-MIMO:** several mm-scale single-antenna
  implants, separated by the external array. Spatial orthogonality *between
  devices* matches implant power budgets well (see S5).
* **Receiver-side processing only** (MMSE-SIC, V-BLAST), so the implant needs
  no channel knowledge.
* Estimate **energy/bit** from published transceiver ICs, because a USRP-based
  demo says nothing about implant power. Be explicit about this in the paper.

### C7. Is the signal actually going *through* the body? (The #1 artifact)

At GHz the received signal can arrive by paths that bypass the tissue:

* **Cable radiation.** Coax feeds to an "implant" antenna carry common-mode
  currents and radiate. They can dominate the measured S21 by 10–30 dB.
* **Air and surface paths** around a phantom tank or along the skin (creeping
  and surface waves).
* **Tank-wall guiding** in plastic phantom containers.

Controls every dataset should include:

1. Feed the implant-side antennas with **RF-over-fibre** or a **battery-powered,
   floating transmitter**. At minimum, use ferrite chokes and a sleeve balun,
   and show that S21 doesn't change when you move the cable.
2. Repeat the measurement with **absorber** blocking the air paths, plus a
   no-tissue air reference.
3. Sweep **tissue thickness** and check that loss scales with the tissue's
   dB/cm, not with free-space spreading.
4. Use **time gating** (VNA time domain) to separate the direct path from
   reflections.

### C8. Phantom ≠ ex vivo ≠ in vivo

* Ex vivo tissue dehydrates and cools, and ε and σ drift by a few percent per °C
  and over hours. There's also no perfusion or blood vessels. The Uppsala
  group found vessels matter for Fat-IBC.
* Fat thickness varies between people by more than 10× (a few mm to >5 cm). A
  fat-channel link that works for one body may fail for another.
* **Plan:** measure dielectric properties every session (open-ended coax probe),
  control temperature, report across tissue samples, and move to in vivo
  animal tests before claiming clinical relevance.

### C9. Safety and regulation limit power *and* bandwidth

* **SAR:** FCC limits 1.6 W/kg averaged over 1 g. ICNIRP (2020, general
  public) limits 2 W/kg over 10 g for head/trunk and 4 W/kg for limbs. Implant
  standards (ISO 14708 family) limit surface temperature rise to ~2 °C. A small
  implant antenna puts its power into a tiny volume, so local SAR, not total
  power, sets the cap. **Simulate SAR for every antenna design.**
* **Spectrum:** MedRadio (401–406 MHz) caps EIRP at 25 µW. Wide-bandwidth GHz
  emissions that leak off-body count as radiated emissions (ISM band rules,
  UWB mask −41.3 dBm/MHz). Run wideband experiments in a **shielded enclosure**,
  or get an experimental licence. Leakage also undercuts any
  "private/secure body channel" claim (C10).

### C10. Confinement and security claims don't hold at GHz

Electro-quasistatic HBC (<30 MHz) can credibly claim the signal stays on the
body. A 2.45 GHz link cannot claim that without measurements. If security
matters, measure leakage vs distance off the body and report it. Otherwise
drop the claim.

### C11. Why the body and not over-the-air?

For wearable-to-wearable links, Wi-Fi and UWB already give Gb/s over the air.
A through-body EM link needs a reason: implants (no air path exists), power,
interference immunity or confinement. **Pick implants (or implant to skin
patch) as the primary scenario.** That's where the case is strongest.

### C12. Prior art you must position against

* **Fat-IBC (Uppsala):** 1.7–2.6 GHz and 5.8 GHz, ~0.7 dB/cm in phantom and
  ~1.9 dB/cm ex vivo. A 2026 thesis reports up to **120 Mb/s in phantoms**.
* **Body-Resonance HBC (Purdue, Sen group):** a transmission-line-like
  near/intermediate-field regime, projected at 100s of Mb/s.
* **Ultrasound:** 20–30 Mb/s through ~5 cm of ex vivo tissue, also in vivo
  (Singer/Oelze, UIUC). Ultrasonic spatial-DoF work also exists.

The novelty has to be **measured multi-stream (MIMO) through-tissue EM links
with absolute link budgets, plus a real-time demonstrator.** Being "EM in the
body" isn't novel by itself.

### C13. Channel dynamics

Breathing, heartbeat, posture and muscle contraction change the channel.
Measure coherence time and Doppler with motion phantoms and, later, in vivo.
If coherence is long (likely ≫10 ms), receiver-side MIMO with periodic
pilots works. If it isn't, rank adaptation becomes part of the system design.

---

## Suggestions and opportunities

**S1. Sharpen the scenario.** A primary target could be: *a 1–2 cm implant
at 1–5 cm depth (subcutaneous or intramuscular) sending uplink to a skin-worn
patch array of ≤6 cm.* This is where the model says EM-MIMO has both SNR and
DoF. A secondary target is implant-to-implant through the fat layer.

**S2. Treat frequency as a research result, not a choice.** The optimal carrier
moves with depth and antenna size (our model: ~3 GHz at 1 cm, ~1.3 GHz at
5 cm for a 1.5 cm antenna). This matches the "GHz optimum" result for
power transfer into dispersive tissue (Poon, O'Driscoll & Meng, IEEE TAP 2010).
Sweep 0.4–8 GHz in measurements.

**S3. Use polarisation as the cheapest extra DoF.** Two (and in the reactive
near field, up to three) orthogonal polarisations can roughly double streams
without enlarging the aperture. This is especially valuable in fat at
2.45 GHz, where spatial DoF ≈ 1. Dual- or tri-polarised compact antennas
should be an early design target.

**S4. Mode-division multiplexing in the fat layer (high-risk, high-novelty).**
The skin/fat/muscle stack is a lossy dielectric slab waveguide. Exciting
orthogonal guided modes (TE/TM, different orders), as in multimode fibre, is
another form of "orthogonality". Our search found no prior work on this. The
catch is that a 1–3 cm fat layer at 2.45 GHz supports very few modes, so this
needs higher frequency or thicker fat. Run a quick modal analysis (slab
waveguide eigenmodes with Gabriel parameters) before committing.

**S5. Multi-user spatial multiplexing across implants.** Several single-antenna
mm-scale implants plus one external array give spatial orthogonality between
devices. The implants stay simple, and the result maps directly onto
distributed neural recording systems.

**S6. Hybrid modalities.** Use ultrasound for deep links or power and EM-MIMO
for high-rate shallow links. Or use an EM uplink with an ultrasound or
inductive downlink and power. It's a stronger system story than "EM vs
ultrasound".

**S7. Standardise the metrics.** For every experiment, report: throughput and
capacity at fixed Tx power (dBm) and SAR; C_SISO / C_BF / C_MIMO; singular
values and condition number; coherence bandwidth and time; leakage at 1 m;
and estimated pJ/bit.

**S8. Plug in your preliminary results.** Fit `em_eff_db`, `em_size_m` and
the dB/cm terms in `sim/link_budget.py` to your measured S21. That tells you
immediately whether your setup is in the multiplexing regime or the
beamforming regime (C4), and whether cable artifacts (C7) might be present
(e.g. loss that grows more slowly with depth than the tissue's dB/cm).

**S9. Release an open dataset.** Measured through-tissue MIMO channel matrices
across frequency, depth and tissue type would be a citable contribution on
their own. They're also a hedge if the real-time demo slips.

**S10. On the Cornell ultrasound paper.** We couldn't find a Cornell
paper matching the description. The closest high-rate ultrasonic work we found
is from UIUC (Singer, Oelze and co-authors). Please share the exact citation so
we can position against the right baseline.
