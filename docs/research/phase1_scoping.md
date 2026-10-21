# ARS deep-research, full mode — Phase 1: Scoping

Run started 2026-10-16. Skill: ARS `deep-research` v2.12.1 (`full` mode).
Status: **awaiting author confirmation before Phase 2.**

---

## Research Question Brief

### Topic Area
High-data-rate electromagnetic (EM) communication through human tissue that uses
spatial and polarisation orthogonality (MIMO), positioned against ultrasonic,
Fat-IBC, EQS / Body-Resonance HBC and MedRadio/ISM implant links.

### Primary Research Question
What does the published literature (to October 2026) establish about the
achievable data rate and the spatial/polarisation degrees of freedom of
0.1–10 GHz EM links through human tissue, and does any prior work report a
**measured, multi-stream (MIMO) through-tissue EM link with an absolute link
budget**, compared at matched transmit power, SAR and depth with the best
ultrasonic, Fat-IBC, HBC and MedRadio/ISM links?

### FINER Assessment
| Criterion | Score | Justification |
|---|---|---|
| Feasible | 3/5 | Web search works; full-text fetch, arXiv and publisher APIs are blocked in this environment, so most verification is at abstract/snippet level. Scope is bounded to one modality family plus baselines. |
| Interesting | 5/5 | Decides whether the project's central novelty claim survives and sets the numbers every later paper must beat. |
| Novel | 4/5 | No existing review normalises EM-MIMO and ultrasonic through-tissue links to absolute power/depth; the repo's own scan flags this gap. |
| Ethical | 5/5 | Secondary literature only; no human or animal subjects. |
| Relevant | 5/5 | Directly feeds WP0 (baselines, Cornell reference) and the go/no-go at M1 in `docs/03_research_plan.md`. |
| **Average** | **4.4/5** | Meets the ≥3.0 threshold; no criterion below 2. |

### Scope Boundaries
**In scope:** peer-reviewed papers, theses and preprints, 2000 – Oct 2026, on
(a) in-body/through-tissue EM links (implant, ingestible/capsule, subcutaneous,
Fat-IBC, in-body↔on-body, in-body↔in-body), 0.1–10 GHz, with mm-wave/THz
in-body work noted where it reports rates; (b) implant / in-body MIMO and
polarisation-diversity antennas and channels; (c) baselines: ultrasonic
through-tissue communication (incl. spatial-DoF/MIMO ultrasound), EQS-HBC,
Body-Resonance HBC, galvanic coupling, MedRadio/ISM implant transceivers;
(d) theory of DoF / optimal frequency in lossy dispersive media; (e) SAR and
regulatory limits that bound transmit power.
**Out of scope:** wireless power transfer except as optimal-frequency theory;
optical/NIR transcutaneous links and molecular communication (noted only as
adjacent baselines); purely over-the-air on-body (wearable-to-wearable) MIMO
except as methodology references; commercial product claims without a
technical source.
**Domain:** biomedical telemetry, antennas & propagation, wireless comms.
**Timeframe:** 2000 – Oct 2026 (Gabriel 1996 kept as the dielectric anchor).
**Geography:** global. **Population:** human tissue, tissue phantoms, ex vivo
and in vivo animal tissue.
**Key assumptions:** a rate is only comparable when depth, medium,
transmit power and bandwidth are known; "capacity at normalised SNR" is not a
link budget.

### Sub-questions
1. **Baselines.** What are the verified best-reported data rates, depths,
   transmit powers, bandwidths and media for ultrasonic (SISO and MIMO),
   Fat-IBC, EQS / Body-Resonance HBC and MedRadio/ISM implant links, and which
   paper is the "Cornell ultrasound body channel" work?
2. **Spatial/polarisation DoF.** What modelling and measurement evidence exists
   for MIMO or polarisation-multiplexed EM channels in or through tissue
   (implant MIMO antennas, capsule/ingestible MIMO, Fat-IBC multi-antenna,
   near-field DoF theory in lossy media), and what does it show about rank
   versus depth, frequency and aperture?
3. **Novelty gap and reporting practice.** Has any work reported a measured
   (ideally real-time) spatially or polarisation-multiplexed through-tissue EM
   link, and how do existing EM works report link budgets and control for
   cable, air and surface-path artifacts?

### Sub-Question Bindings (#547)
1. inherits: timeframe=2000–2026; population=tissue/phantom/ex vivo/in vivo; deviations: includes ultrasound and HBC (baseline modalities) by design.
2. inherits: timeframe; population; band=0.1–10 GHz (+ mm-wave noted); deviations: none.
3. inherits: timeframe; population; band; deviations: none.

### Candidate Questions Considered
| # | Candidate | FINER Avg | Why not selected |
|---|---|---|---|
| 1 | Primary RQ above | 4.4 | Selected |
| 2 | "Is EM through tissue faster than ultrasound?" | 3.4 | Unanswerable without depth/power/aperture; the repo's own critique (C1) shows the answer flips at ~10 cm |
| 3 | Systematic review of implant MIMO antenna papers only | 3.6 | Too narrow; misses baselines and the novelty question |
| 4 | Full survey of all intra-body communication modalities | 3.0 | Too broad for abstract-level access; existing surveys cover it |

---

## Methodology Blueprint

### Research Paradigm
Post-positivist / pragmatist: the claims under test (data rates, depths,
existence of a measured MIMO link) are empirical and checkable against sources.

### Method
Structured **integrative literature review** with a **claim-verification
(fact-check) layer**. Integrative, because it combines measurement papers,
simulation papers, theory and theses, and documents its search.

### Data Strategy
Secondary data only. Sources: web search (the only working retrieval channel
here), with every reference checked for existence by title + venue + year +
DOI where available. Search log kept with the query strings used.
Planned query families (each run in standard mode, extended where thin):
in-body/implant MIMO; capsule endoscopy MIMO / high data rate; Fat-IBC rates
and MIMO; polarisation diversity implant; through-tissue ultrasound data rate
(SISO, MIMO, in vivo); EQS-HBC and Body-Resonance HBC rates; MedRadio/ISM
implant transceiver data rates; mm-wave/THz in-body communication; DoF of
lossy-medium channels; Cornell + ultrasound/implant/body communication.

### Analytical Framework
An **evidence matrix**, one row per link result, with columns: modality,
carrier, bandwidth, data rate (measured vs simulated vs projected), depth,
medium (phantom / ex vivo / in vivo), Tx power, streams/rank, real-time or
offline, link-budget reporting (absolute vs normalised SNR), artifact controls,
source tier. Thematic synthesis per sub-question, plus an explicit gap test
for sub-question 3 (search-bounded: states which queries were run).

### Validity Criteria
- Every baseline number traced to a named source; two independent sources
  where possible; otherwise flagged single-source.
- References that cannot be confirmed to exist are dropped (gray zone = FAIL).
- Absence claims (the novelty gap) are bounded by the documented search.
- Corrections to `docs/01_landscape.md` recorded explicitly.

### Limitations (By Design)
- **No full-text access** (arXiv, publisher and scholarly-API hosts are
  blocked by this environment's network policy). Numbers come from abstracts,
  snippets and secondary pages; method-level weaknesses will be marked
  `not assessed (read scope: abstract_only)` where applicable.
- Web search is US-region and may under-cover non-English literature.
- An absence of evidence for the novelty gap is not proof of absence.

### Ethical Considerations
Secondary research; no human-subjects involvement. AI-assistance disclosure
will be included in the report.

### Reporting Standard
APA 7.0 report (ARS default); no EQUATOR guideline applies to a
non-clinical integrative engineering review.

### Preregistration
Not applicable (no primary data collection).

---

## Devil's Advocate Report — Checkpoint 1

### Verdict: PASS (with major issues to carry forward)

### Critical Issues
None.

### Major Issues
1. **Feasibility of verification.** Abstract-level access means reported rates
   may lack their conditions (power, depth, bandwidth). Mitigation: record
   missing conditions as `not reported in accessible text`, never infer them.
2. **Absence claim risk.** The central question (sub-question 3) is a
   negative claim. It must be phrased as "not found in N documented searches",
   and must actively search for disconfirming work (capsule-endoscopy MIMO,
   Fat-IBC multi-antenna, polarisation-multiplexed implant links, in-body
   mm-wave), not only for supporting work.
3. **Possible misattribution already in the repo.** A first probe search
   associates arXiv:1702.05154 (ultrasound spatial DoF) with Stanford work,
   while `docs/01_landscape.md` groups it with UIUC. Phase 2 must verify
   affiliations rather than inherit them.

### Minor Issues
- "Thorough" is bounded by tool access; the report must say so up front.
- Commercial claims (e.g. Ixana Wi-R rates) are Tier 3 and must be labelled.

### Strongest Counter-Argument
The comparison against ultrasound may be ill-posed: modalities are optimised
for different depths and device volumes, so a single "who wins" answer is
not meaningful. The RQ handles this by requiring matched depth, power and
aperture rather than a single ranking.

### What's Missing
Downlink/power-delivery coupling (many implants get power and downlink over
the same modality), and energy per bit. Carried as secondary extraction
columns, not as separate sub-questions.

### Stress Test Results
RQ is answerable (yes, as a bounded evidence review); method fits (yes);
scope (appropriate after excluding WPT and optical).
