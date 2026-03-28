# The Diamond Advantage — AI Data Center Impact Calculator

## Project Overview
An interactive Streamlit web application built to demonstrate Diamond Foundry's value proposition for an interview with DF's CEO for a marketing role. The app shows how Diamond Foundry's single-crystal diamond (SCD) technology can reduce heat, power consumption, carbon emissions, and water usage in AI data centers.

## How to Run
```bash
pip install -r requirements.txt
streamlit run diamond_advantage.py
```
Opens at http://localhost:8501

## Tech Stack
- **Python 3.10+**
- **Streamlit** (>=1.30.0) — app framework
- **Plotly** (>=5.18.0) — interactive charts
- All in a single file: `diamond_advantage.py`

## App Structure (sections in order)
1. **Hero** — Headline "What if we could cool AI with diamonds?" + 4 key stats
2. **The AI Power Crisis** — 3 problem cards + thermal conductivity bar chart
3. **Interactive Calculator** — 3 sliders (GPU count, power/GPU, PUE) driving a side-by-side comparison of Traditional Silicon vs Diamond Foundry SCD (temp, power, CO₂, water) with savings banner + 2 charts
4. **From Greenhouse Gas to Diamond** — 5-step process flow + carbon sequestration callout
5. **Global Impact at Scale** — Global stats cards + projected energy chart through 2030
6. **Master Plan Timeline** — DF's 3-decade vision (2013 → 2023 → 2033)
7. **Footer**

## Diamond Foundry Brand Guidelines
- **DF Black:** #221E1E (primary background)
- **DF Orange:** #FF5532 (accent, CTAs, highlights — derived from plasma reactor color)
- **DF Grey:** #C9C9C9 (secondary text)
- **DF White:** #FFFFFF (headings, emphasis)
- **Supporting darks:** #2A2626 (dark grey, cards), #3A3636 (mid grey, borders)
- **Font:** Inter (Google Fonts)
- **Tone:** "Visionary Transformer" — forward-looking, wisdom-driven, inspirational
- **Core values:** Embrace change, build for eternity, make things happen, win together, transparency

## Key DF Data Points (from master deck)
- Diamond semiconductor figure of merit: **17,200×** better than silicon
- Thermal conductivity: Diamond **>2,200 W/mK** vs Silicon 150 vs Copper 380
- Chip temperature reduction: **52°C**
- Power density improvement: **3.7×** (34 W/mm²)
- AI chip packages: **15kW** enabled (vs 1.3kW without diamond)
- DF global SCD capacity market share: **97%**
- Reactor generation: **10th gen**, proprietary
- Revenue 2023: ~$200M, 26% net profit margin
- 3 application verticals: AI chips (Si-on-SCD), Power electronics (SiC-on-SCD), GaN RF (GaN-on-SCD)
- Manufacturing: Wenatchee WA ($200M), Spain Trujillo ($2.77B), Spain Zaragoza (wafer fab)
- Green energy powered (hydroelectric + solar)
- Process: Methane (CH₄) → Plasma → Atomic Carbon → Single-Crystal Diamond

## Calculator Assumptions
- Carbon intensity: 0.385 kg CO₂/kWh (US grid average)
- Water usage: 1.8 m³/MWh (evaporative cooling average)
- Cooling reduction with SCD: 42% (derived from thermal conductivity advantage)
- Energy cost: $65/MWh wholesale
- Peak chip temp baseline: 95°C
- Global data center energy (2024): ~460 TWh, ~40% AI workloads

## Design Conventions
- All custom HTML uses classes prefixed with `df-` (e.g., `df-card`, `df-hero-stat`)
- Plotly charts use transparent backgrounds with DF color palette
- Streamlit native components (metrics, sliders, tabs) are restyled via CSS
- Dark theme throughout — no light mode

## Reference Materials
- `Diamond Foundry – Brandbook .pdf` — Visual identity, typography, color palette, brand values
- `Diamond Foundry Master Deck Feb 18.pdf` — Technology details, financials, scaling data, competitive positioning
