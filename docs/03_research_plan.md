# Research plan: spatially multiplexed EM communication through tissue

## 1. Problem statement

Implanted and body-worn devices need far more uplink bandwidth than today's
body links provide. Neural interfaces need ~100–200+ Mb/s, while MedRadio and
BLE give ≲1–2 Mb/s, EQS-HBC gives ≲30 Mb/s and ultrasound gives ≲30 Mb/s
demonstrated. We will test whether **GHz EM links through tissue, using
multiple antennas to exploit the spatial (and polarisation) orthogonality of
the tissue channel**, can deliver several-fold higher throughput than SISO EM
and ultrasonic links. The comparison is at equal transmit power, SAR and
device size.

## 2. Hypotheses (falsifiable)

| ID | Hypothesis | Measured by | Pass threshold (initial; revise after Phase 1) |
|---|---|---|---|
| H1 | Between a ≤2 cm implant-side array and a ≤6 cm skin-side array, tissue supports ≥2 usable spatial/polarisation streams at depths ≤3–5 cm at 1–6 GHz | singular values of measured H(f); C_MIMO/C_BF | C_MIMO/C_BF ≥ 1.5 at 3 cm in ex vivo tissue |
| H2 | A real-time MIMO-OFDM link beats SISO and beamforming at the same Tx power | throughput, BER, EVM | ≥2× SISO throughput at 3 cm; ≥300 Mb/s at ≤0 dBm Tx (hardware permitting) |
| H3 | The through-tissue MIMO channel is stable enough for receiver-side MIMO without implant CSI | coherence time and Doppler under motion | coherence time ≥ 10× frame duration |
| H4 | The signal really propagates through tissue (not via cable, air or surface paths) | control experiments (§5.4) | <1 dB change with cable moves; air-path suppression ≥20 dB |
| H5 (exploratory) | Orthogonal guided modes and/or polarisations in a skin/fat/muscle stack add separable streams | mode-selective couplers; cross-mode isolation | ≥15 dB inter-mode isolation |

## 3. Scenario and requirements

* **Primary:** implant (1–2 cm package) at 1–5 cm depth in muscle or below fat
  → skin-worn patch array (≤6 cm). Uplink-heavy.
* **Secondary:** implant ↔ implant through the fat layer (Fat-IBC geometry),
  10–20 cm.
* **Constraints to respect from day one:** Tx power ≤ 0 dBm per implant, within
  local SAR (1.6 W/kg over 1 g, or 2 W/kg over 10 g) and ≤ 2 °C heating.
  External patch ≤ 10 dBm. Experiments run in a shielded enclosure.

## 4. Work packages and timeline (≈ 44 weeks, overlapping)

| WP | Weeks | 0–4 | 4–8 | 8–12 | 12–16 | 16–20 | 20–24 | 24–28 | 28–32 | 32–36 | 36–40 | 40–44 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WP0 scoping | 0–2 | ■ | | | | | | | | | | |
| WP1 modelling | 0–10 | ■ | ■ | ■ | | | | | | | | |
| WP2 phantoms & probe | 2–10 | ■ | ■ | ■ | | | | | | | | |
| WP3 channel sounding | 6–18 | | ■ | ■ | ■ | ■ | | | | | | |
| WP4 real-time MIMO link | 14–26 | | | | ■ | ■ | ■ | ■ | | | | |
| WP5 custom PCBs | 10–36 | | | ■ | ■ | ■ | ■ | ■ | ■ | ■ | | |
| WP6 demo & papers | 32–44 | | | | | | | | | ■ | ■ | ■ |

Milestones: **M1** (wk 10) design map plus go/no-go. **M2** (wk 18) measured
MIMO channel dataset. **M3** (wk 26) real-time 2×2 link through ex vivo tissue.
**M4** (wk 36) floating-Tx custom hardware. **M5** (wk 44) integrated demo and
paper submissions.

### WP0: Scoping (weeks 0–2)
* Bring the preliminary results into the repo (`data/prelim/`) and fit the
  screening model to them (see [02_critique.md §S8](02_critique.md)).
* Freeze the metric definitions (§6) and the primary scenario.
* Pin down the Cornell reference and the ultrasonic baseline numbers.

### WP1: Modelling (weeks 0–10)
1. **Analytic screening** (done, [`sim/`](../sim)): tissue model, SISO
   capacity vs distance for EM and ultrasound, scalar MIMO DoF.
2. **Layered analytic model:** planar skin/fat/muscle stack, using
   transfer-matrix or spectral-domain Green's functions. This captures guided
   fat-layer modes and the critical-angle trapping at the skin–air interface.
   Add a slab-waveguide eigenmode solver to assess S4 (mode multiplexing).
3. **Full-wave EM** (openEMS, free FDTD with Python; or CST/HFSS/Sim4Life if
   licensed): design implant-side and skin-side antenna elements *in* tissue
   with encapsulation. Extract S-parameters for N×M arrays, compute local SAR,
   and model the cable common-mode effect.
4. **Deliverable:** a design map of frequency × aperture × depth → expected
   streams, capacity and max Tx power under SAR. Pick 2 bands (e.g. 2.4 GHz ISM
   and 5.8 GHz ISM, plus a 1.0–1.5 GHz research band) and 2 antenna designs.
5. **Go/no-go:** if predicted C_MIMO/C_BF < 1.3 at 3 cm for every design,
   re-scope to polarisation-only MIMO or multi-implant MU-MIMO (S5).

### WP2: Phantoms and dielectric characterisation (weeks 2–10)
* Build an **open-ended coaxial probe** (or use a Keysight/SPEAG probe if
  available) and calibrate it with air, short and deionised water, then
  validate with saline or methanol.
* Make phantoms:
  * muscle: water + NaCl + sugar or polyethylene powder in agar/gelatin
  * fat: oil-in-gelatin (Lazebnik 2005)
  * skin layer
  * layered stacks with controllable fat thickness
* Target ε′ and σ within ±10 % of Gabriel values at the chosen bands.
* **Ex vivo tissue:** pork belly (skin/fat/muscle layering similar to human
  abdomen) and pork loin (muscle). Log temperature and measure dielectric
  properties at the start and end of every session.

### WP3: Channel sounding (weeks 6–18)
* **SISO first:** S21 vs frequency (0.4–8 GHz) and depth (1–10 cm), across
  phantom, ex vivo and air reference. Fit dB/cm and the antenna efficiency.
  This checks the model against your preliminary results.
* **MIMO:** a 2-port VNA plus a switch matrix (custom PCB-3 or Mini-Circuits
  USB switches) measures the full H(f) for 2×2 → 4×4 (→ 8×8 with
  polarisation). Calibrate through the switch paths. Check reciprocity
  (H_ij vs H_ji).
* **Analysis:** singular-value spectra, condition number, C_SISO / C_BF / C_MIMO
  at fixed absolute Tx power, coherence bandwidth and delay spread
  (time-domain), and spatial correlation.
* **Dynamic:** a motion rig (servo that flexes or compresses tissue, or a
  "breathing" balloon under the phantom) measures coherence time.
* **Deliverable:** open dataset (`data/channels/`, Touchstone `.sNp` files plus
  JSON metadata) and paper 1.

### WP4: Real-time link (weeks 14–26)
* An SDR-based **MIMO-OFDM** transceiver, built in steps:
  1×1 → 1×2 (MRC) → 2×2 (spatial multiplexing) → 4×4. Start from an 802.11n/ac
  style frame structure (known preambles, pilots, per-stream training), or a
  custom Python/GNU Radio OFDM for flexibility.
* Receivers: ZF and MMSE, then MMSE-SIC. Add rank adaptation so the link
  falls back to beamforming automatically when singular values collapse.
* **Measure:** throughput, BER/PER and per-stream EVM vs depth, Tx power and
  frequency. Compare at the *same* Tx power against SISO and transmit/receive
  beamforming.
* **Deliverable:** live demo v1 (cabled implant mimic) and paper 2 draft.

### WP5: Custom hardware (weeks 10–36)
See [04_hardware_and_demo.md](04_hardware_and_demo.md) for detail.
* **PCB-1:** skin-side tissue-coupled array (dual-polarised).
* **PCB-2:** implant-mimic array, encapsulated.
* **PCB-3:** RF switch matrix and calibration board.
* **PCB-4:** floating, battery-powered implant-mimic transmitter (removes cable
  artifacts).
* **PCB-5:** optional LNA/filter front-end.

### WP6: Demonstration and dissemination (weeks 32–44)
* An integrated demo: stream HD video or synthetic 1024-channel neural data
  through ex vivo tissue or a layered torso phantom, with a live dashboard
  (singular values, per-stream constellations, throughput vs SISO).
* Benchmark tables against Fat-IBC, EQS/Body-Resonance HBC and ultrasound at
  matched assumptions.
* **Stretch goals:** in vivo animal (IACUC) and on-body human tests of
  skin-side arrays only (IRB).

## 5. Methods in detail

### 5.1 Absolute link budget (no normalised SNR)
For every reported number, state Tx power (dBm, at the antenna port), measured
noise floor (dBm/Hz) and bandwidth. Compute capacity from measured H(f):

  C = Σ_k Δf · log2 det(I + (P/(N₀Δf·N_t)) H_k H_kᴴ)

with equal-power and water-filling variants, plus the C_BF and C_SISO
references on the same arrays.

### 5.2 Calibration and de-embedding
* Run SOLT or SOL calibration at the cable ends, and de-embed switch paths with
  through standards on PCB-3.
* Report antenna-to-antenna channels, with the antennas counted as part of the
  channel, and say so. Report antenna efficiency separately (from simulation,
  or measured in tissue with a Wheeler cap).

### 5.3 Phantom and tissue protocol
* Use fixed fixtures (3D-printed) so antenna positions are repeatable to
  ≤0.5 mm. Use a linear stage for depth sweeps.
* Record temperature, and measure the probe dielectric at 3 points before and
  after each session.
* Ex vivo: measure within N hours of slaughter, keep tissue wrapped and at
  controlled temperature, and use ≥3 samples per condition.

### 5.4 Artifact controls (mandatory for every dataset)
1. Cable-move test with chokes and a sleeve balun. Use RFoF or a floating Tx
   where possible.
2. Absorber over the air paths, plus a no-tissue reference.
3. Thickness sweep that is consistent with tissue dB/cm.
4. Time-gated impulse response to separate the direct path from reflections.
5. For on-body work, measure leakage at 0.3 m and 1 m.

### 5.5 Safety
SAR simulation for each antenna and Tx power, with a Tx power ceiling derived
from it. Measure temperature in phantoms with fibre-optic or thermocouple
probes at the maximum duty cycle.

### 5.6 Statistics
Use ≥3 tissue samples × ≥3 placements per condition, with confidence intervals
on capacity. Report outage capacity (10 %) under motion.

## 6. Metrics (report all, always)

| Metric | Unit | Notes |
|---|---|---|
| Path loss / |H| | dB | vs f, depth, tissue |
| Singular values, condition number | dB | per subcarrier |
| C_SISO, C_BF, C_MIMO (EP and WF) | Mb/s | fixed Tx power (dBm) and SAR |
| Real-time throughput, PER, per-stream EVM | Mb/s, %, dB | |
| Coherence bandwidth and time, delay spread | MHz, ms, ns | |
| Max Tx power at SAR limit | dBm | from simulation |
| Leakage off-body | dBm at 1 m | security / regulatory |
| Estimated energy per bit | pJ/b | from published IC numbers; flagged as estimate |

## 7. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Rank collapses beyond ~2–3 cm | High | High | use polarisation, MU-MIMO across implants, shallower scenarios; still publish the rank-vs-depth law |
| Cable artifacts dominate measurements | High | High | RFoF or floating Tx (PCB-4), controls §5.4 |
| Implant antennas too inefficient at small size | Medium | High | co-design with full-wave; higher-ε encapsulation; accept 1.5–2 cm package for demo |
| SDR bandwidth/EVM limits hide the channel's capacity | Medium | Medium | report channel capacity from VNA data separately from real-time throughput |
| Ex vivo variability | High | Medium | many samples, dielectric logging, phantoms as the controlled baseline |
| Regulatory (wideband GHz emissions) | Medium | Medium | shielded enclosure; ISM-band operation; experimental licence |
| Novelty challenged by Fat-IBC / ultrasound-MIMO work | Medium | High | position explicitly (C12); emphasise measured multi-stream EM and rank laws |

## 8. Expected outputs

1. **Paper 1 (channel):** "Spatial degrees of freedom of the through-tissue EM
   channel: measurements and models", targeting IEEE TAP, TBME or JERM, plus the
   open dataset.
2. **Paper 2 (system):** a real-time MIMO link through tissue with benchmarks,
   targeting e.g. MobiCom, SenSys, NSDI, IEEE JSAC or Nature Electronics if
   the results are strong.
3. **Paper 3 (exploratory):** polarisation and mode-division multiplexing in
   the skin/fat/muscle stack.
4. Open hardware: KiCad projects for PCB-1 to PCB-4.

## 9. Repository layout (proposed)

```
sim/            analytic models (this repo); later openEMS scripts
hw/             KiCad projects: pcb1_skin_array, pcb2_implant_array, ...
firmware/       switch-matrix MCU, floating-Tx control
sdr/            GNU Radio / Python MIMO-OFDM transceiver
data/           prelim/, channels/ (Touchstone + JSON metadata), runs/
analysis/       notebooks: capacity from measured H, rank vs depth
docs/           plans, protocols, figures
```
