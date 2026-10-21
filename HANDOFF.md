# Handoff: body_channel → local Claude Code session

Written 2026-10-21 from a cloud session. Read this first, then continue where it
says **Next step**.

## 1. The project in one paragraph

Research on **high-data-rate EM communication through the human body** using
spatial (and polarisation) orthogonality with MIMO, aiming at a demonstrator
built from commercial SDRs plus custom PCBs. The primary scenario is a 1–2 cm
implant at 1–5 cm depth sending uplink to a skin-worn patch array. The claimed
novelty is a *measured, real-time, spatially multiplexed through-tissue EM link
with absolute link budgets*, which the first literature scan did not find.

## 2. What is in the repo

| Path | What it is |
|---|---|
| `README.md` | Overview and main findings of the screening models |
| `docs/01_landscape.md` | Prior work (HBC, Fat-IBC, ultrasound, implant MIMO), tissue constants. **Web-search only; numbers unverified** |
| `docs/02_critique.md` | Adversarial critique C1–C13, suggestions S1–S10 |
| `docs/03_research_plan.md` | Hypotheses H1–H5, work packages WP0–WP6, metrics, risks |
| `docs/04_hardware_and_demo.md` | Demo architecture, equipment tiers, PCB-1…PCB-5 |
| `docs/research/phase1_scoping.md` | ARS deep-research Phase 1 output (RQ brief, method, critic checkpoint) |
| `sim/` | `tissue.py` (Gabriel 1996), `link_budget.py` (SISO EM vs ultrasound), `mimo_dof.py` (stream count vs distance) |
| `.claude/` | Vendored ARS skills, commands and agents (see §4) |

Run the models: `pip install -r requirements.txt && cd sim && python tissue.py`
(see `README.md` for the plot commands).

## 3. Where the research run stopped

An ARS `deep-research` run in **full mode** was started:

- **Phase 1 (scoping): done**, in `docs/research/phase1_scoping.md`.
  Devil's-advocate checkpoint 1: PASS with three major issues (below).
- **Waiting on the author (you) for two answers before Phase 2:**
  1. Confirm or edit the primary research question and the 3 sub-questions.
  2. Answer the ARS review-form note: systematic / scoping / narrative-or-
     integrative / rapid / no formal review, or "skip". This note is shown
     once per project, so answering it in the local session closes it.
- **Phases 2–6 not started:** literature search and source verification,
  synthesis + checkpoint 2, APA report draft, editorial/ethics/checkpoint 3
  review, revision.

Primary RQ (as proposed): *What does the published literature (to Oct 2026)
establish about the achievable data rate and spatial/polarisation degrees of
freedom of 0.1–10 GHz EM links through human tissue, and does any prior work
report a measured, multi-stream (MIMO) through-tissue EM link with an absolute
link budget, compared at matched power, SAR and depth with the best
ultrasonic, Fat-IBC, HBC and MedRadio/ISM links?*

Issues to carry into Phase 2:
1. **Verification depth.** The cloud session could only use web search;
   arXiv, Crossref, OpenAlex, Semantic Scholar and publisher pages were
   blocked. A local session (especially with university library access)
   should verify numbers against full texts, which removes the main
   limitation recorded in the Phase 1 file. Update its "Limitations" section.
2. **The novelty gap is an absence claim.** State it as "not found in these
   documented searches" and actively search for disconfirming work:
   capsule-endoscopy MIMO, Fat-IBC multi-antenna, polarisation-multiplexed
   implant links, in-body mm-wave.
3. **Probable misattribution in `docs/01_landscape.md`.** arXiv:1702.05154
   (ultrasound spatial DoF, 2×2 link at double rate) appears to be **Stanford**
   work, not UIUC. Verify affiliations before citing.

Leads from the first probe search (unverified):
- No Cornell match yet for the "Cornell ultrasound body channel" paper.
  Closest: arXiv:1702.05154 (Stanford), MEAT-COMMS arXiv:1603.05269 (20–30
  Mb/s through pork/beef liver), DustNet arXiv:2511.14986 (8 ultrasonic
  neural-recording nodes, 400 kb/s at 2 MHz, 90 mm depth), Stanford thesis
  purl.stanford.edu/fn562zf5030, IEEE IUS 2019 abstract 1354.
- If you remember the Cornell paper's authors or title, give them to the
  session; that settles WP0's open item fastest.

## 4. ARS (Academic Research Skills) setup

ARS v3.23.1 (Imbad0202/academic-research-skills, CC-BY-NC-4.0, Cheng-I Wu)
is **vendored into this repo** so cloud sessions load it:
`.claude/skills/` (plugin root: 5 skills + `shared/`, `scripts/`, `docs/`),
`.claude/commands/ars-*.md` (16 commands), `.claude/agents/` (4 agents).
Details: `.claude/ARS_VENDORED.md`.

**On your local machine you already have ARS installed as a plugin.** Opening
this repo locally will then load ARS twice (plugin names are prefixed
`academic-research-skills:…`, the vendored ones are not). Both work. To avoid
confusion, prefer one:
- keep the plugin and ignore the vendored copy (the plugin also enables ARS's
  hooks and gets upstream updates), or
- disable the plugin for this project and use the vendored copy.

Python packages for ARS scripts (needed only for its verification/check
scripts):
`pip install -r .claude/skills/requirements-dev.txt -r .claude/skills/requirements-pdf-content-classifier.txt`
(installed in the cloud session; not persisted anywhere).

## 5. Next step (copy into the local session)

```
Read HANDOFF.md and docs/research/phase1_scoping.md. Resume the ARS
deep-research full-mode run at the Phase 1 → Phase 2 confirmation.
My answers: RQ = <confirm / edits>; review form = <choice or skip>.
Then run Phase 2 (bibliography + source verification) with full-text
access, writing outputs to docs/research/.
```

Other open items from `docs/03_research_plan.md` WP0: bring preliminary
measurements into `data/prelim/` and fit `sim/link_budget.py` to them
(critique §S8); freeze metric definitions and the primary scenario.

## 6. Git state at handoff

Branch `main`, pushed to `github.com/HarryZ4127/body_channel`. Nothing
uncommitted. `git pull` before starting locally.
