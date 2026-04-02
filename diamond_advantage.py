"""
The Diamond Advantage — AI Data Center Impact Calculator
Built for Diamond Foundry | Interactive Streamlit Application
"""

import streamlit as st
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Diamond Advantage | Diamond Foundry",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────
# DF BRAND PALETTE
# ──────────────────────────────────────────────────────────────
DF_BLACK = "#221E1E"
DF_ORANGE = "#FF5532"
DF_GREY = "#C9C9C9"
DF_WHITE = "#FFFFFF"
DF_DARK_GREY = "#2A2626"
DF_MID_GREY = "#3A3636"
DF_LIGHT_ORANGE = "#FF7A5C"

# ──────────────────────────────────────────────────────────────
# DF LOGOS — Matching df.com: compact D◇F for header, full wordmark for footer
# ──────────────────────────────────────────────────────────────

# Compact D◇F mark (as seen in df.com header nav)
DF_LOGO_COMPACT = """
<svg viewBox="0 0 80 28" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="21" style="font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 600; letter-spacing: 0.15em; fill: {color};">D</text>
  <polygon points="38,3 48,14 38,25 28,14" fill="none" stroke="{color}" stroke-width="1.6"/>
  <text x="56" y="21" style="font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 600; letter-spacing: 0.15em; fill: {color};">F</text>
</svg>
"""

# Full DIAMOND ◇ FOUNDRY wordmark (as seen in df.com footer)
DF_LOGO_FULL = """
<svg viewBox="0 0 420 28" xmlns="http://www.w3.org/2000/svg">
  <style>
    .df-wm {{ font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500; letter-spacing: 0.28em; fill: {color}; }}
  </style>
  <text x="0" y="18" class="df-wm">DIAMOND</text>
  <polygon points="218,2 228,14 218,26 208,14" fill="none" stroke="{color}" stroke-width="1.5"/>
  <text x="245" y="18" class="df-wm">FOUNDRY</text>
</svg>
"""

def df_logo_compact(color=DF_WHITE, width="70px"):
    """Render the compact D◇F header mark."""
    svg = DF_LOGO_COMPACT.replace("{color}", color)
    return f'<div style="width: {width}; display: inline-block;">{svg}</div>'

def df_logo_full(color=DF_WHITE, width="320px"):
    """Render the full DIAMOND ◇ FOUNDRY wordmark."""
    svg = DF_LOGO_FULL.replace("{color}", color)
    return f'<div style="width: {width};">{svg}</div>'


# ──────────────────────────────────────────────────────────────
# CONSTANTS — Calculator assumptions
# ──────────────────────────────────────────────────────────────
CARBON_INTENSITY_KG_PER_KWH = 0.385   # US grid average 2024
WATER_M3_PER_MWH = 1.8                 # Evaporative cooling average
COOLING_REDUCTION_FACTOR = 0.42         # Diamond thermal conductivity advantage
ENERGY_COST_PER_MWH = 65               # $/MWh wholesale
PEAK_CHIP_TEMP_C = 95                   # Typical junction temp under load
TEMP_REDUCTION_C = 52                   # From DF deck
HOURS_PER_YEAR = 8760
GLOBAL_DC_ENERGY_TWH_2024 = 460
AI_WORKLOAD_FRACTION = 0.40
COOLING_FRACTION = 0.35

# ──────────────────────────────────────────────────────────────
# CUSTOM CSS — Full DF Branding
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* ── df.com fonts: Inter + IBM Plex Mono ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {{
        --df-black: {DF_BLACK};
        --df-orange: {DF_ORANGE};
        --df-body: rgba(34,30,30,0.4);
        --df-text: {DF_BLACK};
    }}

    /* ── Global: white bg, dark text (matches df.com body) ── */
    .stApp {{
        background-color: #FFFFFF;
        color: {DF_BLACK};
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        line-height: 24px;
    }}

    .main .block-container {{
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}

    /* ── Headings: df.com uses weight 400 (light), negative tracking ── */
    h1, h2, h3, h4 {{
        font-family: 'Inter', sans-serif !important;
        color: {DF_BLACK} !important;
        font-weight: 400 !important;
    }}
    h1 {{
        font-size: 3.5rem !important;
        line-height: 1 !important;
        letter-spacing: -0.05em !important;
    }}
    h2 {{
        font-size: 2.4rem !important;
        letter-spacing: -0.03em !important;
        margin-top: 3rem !important;
    }}
    h3 {{
        font-size: 1.3rem !important;
        color: rgba(34,30,30,0.4) !important;
        font-weight: 400 !important;
    }}

    p, li, span, div {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* ── Dividers: thin, light (df.com style) ── */
    hr {{
        border: none;
        border-top: 1px solid #E5E5E5;
        margin: 3rem 0;
    }}

    [data-testid="stSidebar"] {{ display: none; }}

    /* ── Slider: DF orange thumb ── */
    .stSlider > div > div > div > div {{
        background-color: {DF_ORANGE} !important;
    }}
    .stSlider [data-baseweb="slider"] div[role="slider"] {{
        background-color: {DF_ORANGE} !important;
        border-color: {DF_ORANGE} !important;
    }}
    .stSlider label {{
        color: {DF_BLACK} !important;
        font-weight: 500 !important;
    }}

    /* ── Metric cards (dark cards in the calculator section) ── */
    [data-testid="stMetric"] {{
        background-color: {DF_DARK_GREY};
        border: 1px solid {DF_MID_GREY};
        border-radius: 12px;
        padding: 20px 24px;
    }}
    [data-testid="stMetricValue"] {{
        color: {DF_WHITE} !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 0.95rem !important;
    }}

    /* ── Diamond side metric: orange left border ── */
    .df-diamond-col [data-testid="stMetric"] {{
        border-left: 3px solid {DF_ORANGE};
    }}

    /* ── Selectbox ── */
    .stSelectbox label {{
        color: {DF_BLACK} !important;
        font-weight: 500 !important;
    }}

    /* ── DARK cards (calculator, sequestration — like df.com's dark photo cards) ── */
    .df-card {{
        background: {DF_BLACK};
        border: none;
        border-radius: 12px;
        padding: 32px;
        margin: 12px 0;
        color: {DF_WHITE};
    }}
    .df-card-orange {{
        background: linear-gradient(135deg, #3D1A10, #2D1510);
        border: 1px solid rgba(255,85,50,0.2);
        border-radius: 12px;
        padding: 32px;
        margin: 12px 0;
    }}

    /* ── LIGHT cards (used for the "AI Crisis" section on white bg) ── */
    .df-card-light {{
        background: #F8F8F8;
        border: 1px solid #E5E5E5;
        border-radius: 12px;
        padding: 32px;
        margin: 12px 0;
    }}

    /* ── Hero stats ── */
    .df-hero-stat {{
        font-size: 3.5rem;
        font-weight: 800;
        color: {DF_ORANGE};
        line-height: 1;
        margin-bottom: 4px;
    }}
    .df-hero-label {{
        font-size: 0.85rem;
        color: rgba(34,30,30,0.4);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 500;
    }}

    .df-accent {{
        color: {DF_ORANGE};
        font-weight: 600;
    }}

    .df-big-number {{
        font-size: 4.5rem;
        font-weight: 800;
        color: {DF_ORANGE};
        line-height: 1;
        letter-spacing: -0.03em;
    }}

    /* ── Section labels: IBM Plex Mono uppercase (matches df.com nav/labels) ── */
    .df-section-label {{
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: normal;
        color: rgba(34,30,30,0.4);
        font-weight: 400;
        font-family: 'IBM Plex Mono', monospace !important;
        margin-bottom: 8px;
    }}

    .df-divider {{
        width: 60px;
        height: 3px;
        background-color: {DF_ORANGE};
        margin: 16px 0 24px 0;
        border-radius: 2px;
    }}

    /* ── Impact numbers ── */
    .df-impact-number {{
        font-size: 2.8rem;
        font-weight: 800;
        color: {DF_ORANGE};
        line-height: 1.1;
    }}

    /* ── Process steps (dark cards) ── */
    .df-process-step {{
        background: {DF_BLACK};
        border: none;
        border-radius: 12px;
        padding: 24px 16px;
        text-align: center;
    }}
    .df-process-icon {{
        font-size: 2.5rem;
        margin-bottom: 12px;
    }}
    .df-process-title {{
        font-size: 1rem;
        font-weight: 600;
        color: {DF_WHITE};
        margin-bottom: 8px;
    }}
    .df-process-desc {{
        font-size: 0.82rem;
        color: rgba(255,255,255,0.5);
        line-height: 1.5;
    }}
    .df-arrow {{
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        color: {DF_ORANGE};
        padding-top: 40px;
    }}

    /* ── Footer: dark bg (matches df.com footer) ── */
    .df-footer {{
        background-color: {DF_BLACK};
        text-align: center;
        padding: 48px 32px 24px 32px;
        margin: 48px -5rem 0 -5rem;
        border-radius: 0;
    }}

    /* ── Comparison headers ── */
    .comparison-header {{
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding-bottom: 12px;
        margin-bottom: 16px;
        border-bottom: 2px solid;
    }}
    .comparison-traditional {{
        color: rgba(34,30,30,0.4);
        border-color: rgba(34,30,30,0.1);
    }}
    .comparison-diamond {{
        color: {DF_ORANGE};
        border-color: {DF_ORANGE};
    }}

    /* ── Timeline ── */
    .df-timeline-item {{
        position: relative;
        padding-left: 32px;
        padding-bottom: 32px;
        border-left: 2px solid #E5E5E5;
        margin-left: 16px;
    }}
    .df-timeline-item::before {{
        content: '';
        position: absolute;
        left: -7px;
        top: 4px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: {DF_ORANGE};
    }}
    .df-timeline-year {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {DF_ORANGE};
    }}
    .df-timeline-text {{
        font-size: 0.95rem;
        color: rgba(34,30,30,0.4);
        margin-top: 4px;
        line-height: 1.6;
    }}

    /* ── Muted column (traditional silicon) ── */
    .df-muted-col [data-testid="stMetric"] {{
        opacity: 0.55;
    }}

    /* ── CTA links: IBM Plex Mono, orange, uppercase (matches df.com READ MORE →) ── */
    .df-cta-link {{
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 15px;
        font-weight: 400;
        text-transform: uppercase;
        color: {DF_ORANGE};
        text-decoration: none;
    }}

    /* ── Pill buttons (matches df.com "Learn more" / "DF Tech Stack" buttons) ── */
    .df-pill-btn {{
        display: inline-block;
        font-family: 'Inter', sans-serif !important;
        font-size: 17px;
        color: {DF_BLACK};
        border: 1px solid #E5E5E5;
        border-radius: 999px;
        padding: 12px 28px;
        text-decoration: none;
        letter-spacing: -0.03em;
        transition: border-color 0.2s;
    }}
    .df-pill-btn:hover {{
        border-color: {DF_BLACK};
    }}

    /* ── Hide streamlit chrome ── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PASSWORD GATE (optional — only active if secrets are set)
# ══════════════════════════════════════════════════════════════
def check_password():
    """Returns True if no password is configured or if correct password is entered."""
    try:
        correct = st.secrets["password"]
    except (KeyError, FileNotFoundError):
        return True  # No password configured — run freely

    if st.session_state.get("authenticated"):
        return True

    st.markdown(f"""
    <div style="max-width: 400px; margin: 120px auto 0 auto; text-align: center;">
        <div style="display: flex; justify-content: center; margin-bottom: 24px;">
            {df_logo_compact(DF_BLACK, "80px")}
        </div>
        <h2 style="margin-top: 16px; font-size: 1.6rem;">The Diamond Advantage</h2>
        <p style="color: rgba(34,30,30,0.4); font-size: 0.9rem;">Enter password to continue</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("Password", type="password", label_visibility="collapsed")
        if password:
            if password == correct:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
    return False


if not check_password():
    st.stop()


# ══════════════════════════════════════════════════════════════
#  SECTION 0 — HERO
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="margin-bottom: 24px;">
    {df_logo_compact(DF_BLACK, "80px")}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<h1 style="margin-bottom: 0;">What if we could cool AI<br>
<span style="color: {DF_ORANGE};">with diamonds?</span></h1>
""", unsafe_allow_html=True)

st.markdown(f"""
<p style="font-size: 1.15rem; color: rgba(34,30,30,0.4); max-width: 680px; line-height: 1.7; margin-top: 16px;">
AI is hitting a wall — not of intelligence, but of <strong style="color:{DF_BLACK}">heat</strong>.
Every generation of chips runs hotter, drinks more power, and demands more cooling.
Diamond Foundry is solving this by replacing traditional substrates with
<strong style="color:{DF_BLACK}">single-crystal diamond</strong> — the most thermally conductive material on Earth —
grown from captured methane greenhouse gas.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="df-divider"></div>', unsafe_allow_html=True)

# Hero stats row
hero_cols = st.columns(4)
hero_data = [
    ("17,200×", "Semiconductor merit vs. silicon"),
    ("2,200+", "W/mK thermal conductivity"),
    ("52°C", "Chip temperature reduction"),
    ("3.7×", "Higher power density"),
]
for col, (val, label) in zip(hero_cols, hero_data):
    with col:
        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0;">
            <div class="df-hero-stat">{val}</div>
            <div class="df-hero-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  SECTION 1 — THE AI POWER CRISIS
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-section-label">The Problem</div>', unsafe_allow_html=True)
st.markdown("## The AI Infrastructure Crisis")

crisis_cols = st.columns(3)
crisis_cards = [
    ("⚡", "Power Hungry",
     "Global data centers consumed <strong style='color:#FF5532'>~460 TWh</strong> in 2024 — "
     "roughly 2% of global electricity. AI workloads are projected to push this past "
     "<strong style='color:#FF5532'>1,000 TWh by 2028</strong>."),
    ("🌡️", "Heat Wall",
     "Modern AI chips like NVIDIA's B200 push <strong style='color:#FF5532'>1,000W per GPU</strong>. "
     "Traditional silicon substrates can't dissipate this heat fast enough, "
     "forcing chips to throttle and waste energy on cooling."),
    ("💧", "Water & Carbon Cost",
     "A single large AI data center can consume <strong style='color:#FF5532'>5+ million gallons "
     "of water daily</strong> for cooling. The carbon footprint of training one large AI model "
     "can exceed <strong style='color:#FF5532'>300 tons of CO₂</strong>."),
]
for col, (icon, title, desc) in zip(crisis_cols, crisis_cards):
    with col:
        st.markdown(f"""
        <div class="df-card-light">
            <div style="font-size: 2rem; margin-bottom: 12px;">{icon}</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: {DF_BLACK}; margin-bottom: 12px;">{title}</div>
            <div style="font-size: 0.9rem; color: rgba(34,30,30,0.5); line-height: 1.65;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# Thermal conductivity chart
st.markdown(f"""
<div style="margin-top: 32px;">
    <div class="df-section-label">Why Diamond?</div>
    <h3 style="color: {DF_WHITE} !important; font-weight: 700 !important;">
        Thermal Conductivity Comparison
    </h3>
</div>
""", unsafe_allow_html=True)

materials = ["Silicon", "Gallium Nitride", "Copper", "Silicon Carbide", "Diamond (SCD)"]
conductivity = [150, 200, 380, 490, 2200]
bar_colors = [DF_GREY, DF_GREY, DF_GREY, DF_GREY, DF_ORANGE]

fig_thermal = go.Figure()
fig_thermal.add_trace(go.Bar(
    x=conductivity, y=materials, orientation='h',
    marker=dict(color=bar_colors, line=dict(width=0), cornerradius=6),
    text=[f"  {v:,} W/mK" for v in conductivity],
    textposition='outside',
    textfont=dict(color=DF_BLACK, size=14, family="Inter"),
    hovertemplate='%{y}: %{x:,} W/mK<extra></extra>',
))
fig_thermal.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", color="rgba(34,30,30,0.4)", size=13),
    height=280, margin=dict(l=0, r=80, t=10, b=10),
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 2800]),
    yaxis=dict(showgrid=False, tickfont=dict(size=13, color=DF_GREY), autorange="reversed"),
    bargap=0.35,
)
st.plotly_chart(fig_thermal, use_container_width=True, config={'displayModeBar': False})

st.markdown(f"""
<p style="text-align: center; font-size: 1rem; color: rgba(34,30,30,0.4); margin-top: -16px;">
    Diamond conducts heat <span class="df-accent">14.7× better than silicon</span> and
    <span class="df-accent">5.8× better than copper</span>.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  SECTION 2 — INTERACTIVE CALCULATOR (uses st.fragment)
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-section-label">Interactive Calculator</div>', unsafe_allow_html=True)
st.markdown("## The Diamond Advantage Calculator")
st.markdown(f"""
<p style="font-size: 1rem; color: rgba(34,30,30,0.4); max-width: 700px; line-height: 1.6; margin-bottom: 24px;">
Configure a hypothetical AI data center and see the impact of switching from
traditional silicon substrates to Diamond Foundry's single-crystal diamond (SCD) technology.
</p>
""", unsafe_allow_html=True)


@st.fragment
def calculator_fragment():
    """Calculator section wrapped in st.fragment for real-time slider updates."""

    # ── Controls ──
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    with calc_col1:
        num_gpus = st.slider(
            "Number of AI GPUs",
            min_value=1000, max_value=100000, value=20000, step=1000,
            format="%d",
            help="Typical large AI cluster: 10,000–50,000 GPUs"
        )
    with calc_col2:
        power_per_gpu = st.slider(
            "Power per GPU (Watts)",
            min_value=300, max_value=1500, value=700, step=50,
            format="%dW",
            help="NVIDIA A100: ~400W, H100: ~700W, B200: ~1000W"
        )
    with calc_col3:
        pue = st.selectbox(
            "Cooling Efficiency (PUE)",
            options=[
                ("Air-cooled (PUE 1.6)", 1.6),
                ("Efficient air (PUE 1.3)", 1.3),
                ("Liquid-cooled (PUE 1.15)", 1.15),
            ],
            format_func=lambda x: x[0],
            index=0,
            help="Power Usage Effectiveness — how much overhead goes to cooling"
        )
        pue_value = pue[1]

    # ── Calculations ──
    total_it_power_kw = (num_gpus * power_per_gpu) / 1000
    total_facility_power_kw = total_it_power_kw * pue_value
    cooling_overhead_kw = total_facility_power_kw - total_it_power_kw
    annual_energy_mwh = total_facility_power_kw * HOURS_PER_YEAR / 1000
    annual_co2_tons = annual_energy_mwh * CARBON_INTENSITY_KG_PER_KWH
    annual_water_m3 = cooling_overhead_kw * HOURS_PER_YEAR / 1000 * WATER_M3_PER_MWH

    diamond_chip_temp = PEAK_CHIP_TEMP_C - TEMP_REDUCTION_C
    diamond_cooling_kw = cooling_overhead_kw * (1 - COOLING_REDUCTION_FACTOR)
    diamond_facility_kw = total_it_power_kw + diamond_cooling_kw
    diamond_annual_mwh = diamond_facility_kw * HOURS_PER_YEAR / 1000
    diamond_co2_tons = diamond_annual_mwh * CARBON_INTENSITY_KG_PER_KWH
    diamond_water_m3 = diamond_cooling_kw * HOURS_PER_YEAR / 1000 * WATER_M3_PER_MWH

    energy_saved_mwh = annual_energy_mwh - diamond_annual_mwh
    co2_saved_tons = annual_co2_tons - diamond_co2_tons
    water_saved_m3 = annual_water_m3 - diamond_water_m3
    water_saved_gallons = water_saved_m3 * 264.172
    cost_saved = energy_saved_mwh * ENERGY_COST_PER_MWH

    # ── Results: side-by-side comparison ──
    st.markdown(f"""
    <div style="display: flex; gap: 12px; margin: 24px 0 8px 0;">
        <div class="comparison-header comparison-traditional" style="flex: 1; text-align: center;">
            Traditional Silicon
        </div>
        <div class="comparison-header comparison-diamond" style="flex: 1; text-align: center;">
            Diamond Foundry SCD
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Temperature
    r1_left, r1_right = st.columns(2)
    with r1_left:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Peak Chip Temperature", f"{PEAK_CHIP_TEMP_C}°C")
        st.markdown('</div>', unsafe_allow_html=True)
    with r1_right:
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Peak Chip Temperature", f"{diamond_chip_temp}°C",
                  delta=f"-{TEMP_REDUCTION_C}°C cooler", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # Power
    r2_left, r2_right = st.columns(2)
    with r2_left:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Total Facility Power", f"{total_facility_power_kw:,.0f} kW")
        st.markdown('</div>', unsafe_allow_html=True)
    with r2_right:
        pct_power = (1 - diamond_facility_kw / total_facility_power_kw) * 100
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Total Facility Power", f"{diamond_facility_kw:,.0f} kW",
                  delta=f"-{pct_power:.0f}% power draw", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # CO₂
    r3_left, r3_right = st.columns(2)
    with r3_left:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Annual CO₂ Emissions", f"{annual_co2_tons:,.0f} tons")
        st.markdown('</div>', unsafe_allow_html=True)
    with r3_right:
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Annual CO₂ Emissions", f"{diamond_co2_tons:,.0f} tons",
                  delta=f"-{co2_saved_tons:,.0f} tons/year", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # Water
    r4_left, r4_right = st.columns(2)
    with r4_left:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Annual Water Usage", f"{annual_water_m3:,.0f} m³")
        st.markdown('</div>', unsafe_allow_html=True)
    with r4_right:
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Annual Water Usage", f"{diamond_water_m3:,.0f} m³",
                  delta=f"-{water_saved_m3:,.0f} m³/year", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Savings banner ──
    st.markdown(f"""
    <div class="df-card-orange" style="margin-top: 24px;">
        <div class="df-section-label" style="text-align: center;">Annual Savings with Diamond Foundry</div>
        <div style="display: flex; justify-content: space-around; text-align: center; margin-top: 16px; flex-wrap: wrap;">
            <div style="padding: 8px 16px;">
                <div class="df-impact-number">{energy_saved_mwh:,.0f}</div>
                <div class="df-hero-label" style="margin-top: 4px;">MWh Energy Saved</div>
            </div>
            <div style="padding: 8px 16px;">
                <div class="df-impact-number">{co2_saved_tons:,.0f}</div>
                <div class="df-hero-label" style="margin-top: 4px;">Tons CO₂ Avoided</div>
            </div>
            <div style="padding: 8px 16px;">
                <div class="df-impact-number">{water_saved_gallons / 1e6:,.1f}M</div>
                <div class="df-hero-label" style="margin-top: 4px;">Gallons Water Saved</div>
            </div>
            <div style="padding: 8px 16px;">
                <div class="df-impact-number">${cost_saved / 1e6:,.1f}M</div>
                <div class="df-hero-label" style="margin-top: 4px;">Annual Cost Savings</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts ──
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_power = go.Figure()
        fig_power.add_trace(go.Bar(
            name='IT Load (GPUs)',
            x=['Traditional<br>Silicon', 'Diamond<br>Foundry SCD'],
            y=[total_it_power_kw, total_it_power_kw],
            marker_color=DF_GREY, marker_cornerradius=4,
            text=[f'{total_it_power_kw:,.0f} kW'] * 2,
            textposition='inside',
            textfont=dict(color=DF_BLACK, size=12, family="Inter"),
            hovertemplate='IT Load: %{y:,.0f} kW<extra></extra>',
        ))
        fig_power.add_trace(go.Bar(
            name='Cooling Overhead',
            x=['Traditional<br>Silicon', 'Diamond<br>Foundry SCD'],
            y=[cooling_overhead_kw, diamond_cooling_kw],
            marker_color=[DF_LIGHT_ORANGE, DF_ORANGE], marker_cornerradius=4,
            text=[f'{cooling_overhead_kw:,.0f} kW', f'{diamond_cooling_kw:,.0f} kW'],
            textposition='inside',
            textfont=dict(color=DF_WHITE, size=12, family="Inter"),
            hovertemplate='Cooling: %{y:,.0f} kW<extra></extra>',
        ))
        fig_power.update_layout(
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="rgba(34,30,30,0.4)", size=12),
            height=350, margin=dict(l=20, r=20, t=40, b=20),
            title=dict(text="Power Breakdown (kW)", font=dict(size=14, color=DF_BLACK)),
            yaxis=dict(showgrid=True, gridcolor="rgba(34,30,30,0.08)", zeroline=False,
                       tickfont=dict(color="rgba(34,30,30,0.4)")),
            xaxis=dict(tickfont=dict(color=DF_BLACK, size=12)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
                        font=dict(color=DF_GREY, size=11)),
            bargap=0.4,
        )
        st.plotly_chart(fig_power, use_container_width=True, config={'displayModeBar': False})

    with chart_col2:
        pct_reduction = (co2_saved_tons / annual_co2_tons) * 100 if annual_co2_tons > 0 else 0
        fig_donut = go.Figure()
        fig_donut.add_trace(go.Pie(
            labels=['CO₂ Avoided', 'Remaining Emissions'],
            values=[co2_saved_tons, diamond_co2_tons],
            hole=0.65,
            marker=dict(colors=[DF_ORANGE, DF_MID_GREY], line=dict(width=0)),
            textinfo='none',
            hovertemplate='%{label}: %{value:,.0f} tons<extra></extra>',
        ))
        fig_donut.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color=DF_GREY),
            height=350, margin=dict(l=20, r=20, t=40, b=20),
            title=dict(text="CO₂ Reduction Impact", font=dict(size=14, color=DF_BLACK)),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                        font=dict(color=DF_GREY, size=11)),
            annotations=[dict(
                text=f"<b>{pct_reduction:.0f}%</b><br><span style='font-size:12px'>reduction</span>",
                x=0.5, y=0.5, font=dict(size=28, color=DF_ORANGE, family="Inter"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})


# Run the fragment
calculator_fragment()

st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  SECTION 3 — FROM METHANE TO DIAMOND
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-section-label">The Process</div>', unsafe_allow_html=True)
st.markdown("## From Greenhouse Gas to Diamond")
st.markdown(f"""
<p style="font-size: 1rem; color: rgba(34,30,30,0.4); max-width: 700px; line-height: 1.6; margin-bottom: 32px;">
Diamond Foundry doesn't mine diamonds — it <strong style="color:{DF_BLACK}">crystallizes them from methane</strong>,
a potent greenhouse gas. Using proprietary plasma reactors powered by green energy,
DF literally transforms a climate problem into the world's most advanced thermal substrate.
</p>
""", unsafe_allow_html=True)

# Process steps — responsive 5-column layout
process_steps = [
    ("🏭", "Methane Capture",
     "CH₄ greenhouse gas is sourced as the carbon feedstock — turning a climate liability into raw material."),
    ("⚡", "Plasma Reactor",
     "DF's proprietary 10th-gen reactors achieve 150× higher productivity, breaking methane into atomic carbon."),
    ("💎", "Crystal Growth",
     "Carbon atoms self-assemble into perfect single-crystal diamond via DF's patented heteroepitaxy."),
    ("🔬", "Wafer Finishing",
     "Diamond ingots are polished to angstrom-level flatness, then atomically bonded to silicon or SiC."),
    ("🧠", "AI-Ready Substrate",
     "The SCD wafer conducts heat 14.7× better than silicon — enabling the next generation of AI."),
]

p_cols = st.columns(9)
col_idx = 0
for i, (icon, title, desc) in enumerate(process_steps):
    with p_cols[col_idx]:
        st.markdown(f"""
        <div class="df-process-step">
            <div class="df-process-icon">{icon}</div>
            <div class="df-process-title">{title}</div>
            <div class="df-process-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    col_idx += 1
    if i < len(process_steps) - 1:
        with p_cols[col_idx]:
            st.markdown('<div class="df-arrow">→</div>', unsafe_allow_html=True)
        col_idx += 1

# Carbon sequestration callout
st.markdown(f"""
<div class="df-card-orange" style="margin-top: 32px; text-align: center;">
    <div style="font-size: 1.5rem; font-weight: 600; color: {DF_WHITE}; margin-bottom: 8px;">
        Crystallizing Greenhouse Gas into Single-Crystal Diamond
    </div>
    <div style="font-size: 1rem; color: rgba(255,255,255,0.5); max-width: 600px; margin: 0 auto; line-height: 1.6;">
        Every diamond wafer Diamond Foundry produces permanently locks carbon atoms
        into the hardest, most thermally conductive material known to science —
        powered by hydroelectric and solar energy.
    </div>
    <div style="display: flex; justify-content: center; gap: 48px; margin-top: 24px;">
        <div>
            <div style="font-size: 2rem; font-weight: 800; color: {DF_ORANGE};">97%</div>
            <div class="df-hero-label">of global SCD capacity</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: 800; color: {DF_ORANGE};">10th Gen</div>
            <div class="df-hero-label">proprietary reactors</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: 800; color: {DF_ORANGE};">100%</div>
            <div class="df-hero-label">green energy powered</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  SECTION 4 — GLOBAL IMPACT AT SCALE
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-section-label">The Big Picture</div>', unsafe_allow_html=True)
st.markdown("## If Every AI Data Center Used Diamond")
st.markdown(f"""
<p style="font-size: 1rem; color: rgba(34,30,30,0.4); max-width: 700px; line-height: 1.6; margin-bottom: 32px;">
The world is building AI infrastructure at an unprecedented pace. Here's what it would mean
if Diamond Foundry's SCD technology were deployed across the global AI data center fleet.
</p>
""", unsafe_allow_html=True)

# Global scale estimates
global_ai_energy_twh = GLOBAL_DC_ENERGY_TWH_2024 * AI_WORKLOAD_FRACTION
global_cooling_twh = global_ai_energy_twh * COOLING_FRACTION
global_savings_twh = global_cooling_twh * COOLING_REDUCTION_FACTOR
global_co2_saved_mt = global_savings_twh * 1e6 * CARBON_INTENSITY_KG_PER_KWH / 1e6
global_water_saved_billion_gal = global_cooling_twh * 1e6 * WATER_M3_PER_MWH * 264.172 / 1e9
homes_equivalent = global_savings_twh * 1e6 / 10.5
cars_equivalent = global_co2_saved_mt * 1e6 / 4.6

g_cols = st.columns(4)
global_stats = [
    (f"{global_savings_twh:.1f}", "TWh", "Energy saved annually",
     "Equivalent to powering a small country"),
    (f"{global_co2_saved_mt:.1f}M", "tons", "CO₂ emissions avoided",
     f"Like removing {cars_equivalent/1e6:.1f}M cars from roads"),
    (f"{global_water_saved_billion_gal:.0f}B", "gallons", "Water conserved",
     "Enough to supply a major city for a year"),
    (f"{homes_equivalent/1e6:.1f}M", "homes", "Equivalent energy freed",
     "Redirected from cooling to useful compute"),
]
for col, (num, unit, label, sublabel) in zip(g_cols, global_stats):
    with col:
        st.markdown(f"""
        <div class="df-card" style="text-align: center; min-height: 200px;">
            <div class="df-big-number" style="font-size: 3rem;">{num}</div>
            <div style="font-size: 1rem; color: {DF_ORANGE}; font-weight: 600; margin-bottom: 8px;">{unit}</div>
            <div style="font-size: 0.95rem; color: {DF_WHITE}; font-weight: 600;">{label}</div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.4); margin-top: 6px; line-height: 1.4;">{sublabel}</div>
        </div>
        """, unsafe_allow_html=True)

# Growth projection chart
st.markdown("<br>", unsafe_allow_html=True)

years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
dc_energy_baseline = [460, 550, 660, 790, 950, 1100, 1280]
dc_energy_diamond = [460, 530, 610, 700, 790, 880, 980]

fig_proj = go.Figure()
fig_proj.add_trace(go.Scatter(
    x=years, y=dc_energy_baseline,
    name='Without Diamond (Baseline)',
    line=dict(color=DF_GREY, width=3, dash='dot'),
    mode='lines+markers', marker=dict(size=8, color=DF_GREY),
    hovertemplate='%{x}: %{y:,.0f} TWh<extra>Baseline</extra>',
))
fig_proj.add_trace(go.Scatter(
    x=years, y=dc_energy_diamond,
    name='With Diamond Foundry SCD',
    line=dict(color=DF_ORANGE, width=3),
    mode='lines+markers', marker=dict(size=8, color=DF_ORANGE),
    fill='tonexty', fillcolor="rgba(255,85,50,0.08)",
    hovertemplate='%{x}: %{y:,.0f} TWh<extra>With Diamond</extra>',
))
fig_proj.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", color="rgba(34,30,30,0.4)", size=12),
    height=380, margin=dict(l=20, r=20, t=50, b=20),
    title=dict(text="Projected Global Data Center Energy Consumption (TWh)",
               font=dict(size=14, color=DF_BLACK)),
    xaxis=dict(showgrid=False, tickfont=dict(color=DF_GREY, size=12), dtick=1),
    yaxis=dict(showgrid=True, gridcolor="rgba(34,30,30,0.08)", zeroline=False,
               tickfont=dict(color="rgba(34,30,30,0.4)"), ticksuffix=" TWh"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,
                font=dict(color=DF_GREY, size=12)),
)
fig_proj.add_annotation(
    x=2029, y=(dc_energy_baseline[5] + dc_energy_diamond[5]) / 2,
    text=f"<b>{dc_energy_baseline[5] - dc_energy_diamond[5]} TWh saved</b>",
    showarrow=True, arrowhead=0, arrowcolor=DF_ORANGE,
    font=dict(color=DF_ORANGE, size=13, family="Inter"),
    ax=80, ay=0,
    bordercolor=DF_ORANGE, borderwidth=1, borderpad=6,
    bgcolor="rgba(255,255,255,0.9)",
)
st.plotly_chart(fig_proj, use_container_width=True, config={'displayModeBar': False})

st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  SECTION 5 — MASTER PLAN TIMELINE
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-section-label">The Vision</div>', unsafe_allow_html=True)
st.markdown("## Diamond Foundry's Three-Decade Master Plan")

timeline_data = [
    ("2013", "Introduce sustainably created diamond wherever mined diamond has been able to go",
     "Diamond Foundry launched with lab-grown gems — proving that diamonds could be created "
     "from methane using green energy, with zero mining. Today: 26% market share of rough diamonds."),
    ("2023", "Introduce single-crystal diamond wafers and put a diamond behind every chip",
     "World's first SCD wafers created. $200M+ revenue with 26% net profit margin. "
     "Partnerships with Infineon. Global manufacturing across USA, Spain, and Germany."),
    ("2033", "Introduce diamond as a semiconductor and deliver on its 17,200× merit over silicon",
     "The ultimate vision: diamond-based semiconductor devices. Not just thermal substrates, "
     "but active diamond electronics — unlocking the full 17,200× semiconductor figure of merit."),
]
for year, headline, desc in timeline_data:
    st.markdown(f"""
    <div class="df-timeline-item">
        <div class="df-timeline-year">{year}</div>
        <div style="font-size: 1.05rem; font-weight: 600; color: {DF_BLACK}; margin: 4px 0 8px 0;">{headline}</div>
        <div class="df-timeline-text">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="df-footer">
    <div style="margin-bottom: 16px; display: flex; justify-content: center;">
        {df_logo_full(DF_GREY, "280px")}
    </div>
    <div style="font-size: 0.85rem; color: rgba(255,255,255,0.5); line-height: 1.6;">
        Empowering mega-tech industry to shape the future.<br>
        <a href="https://www.df.com" target="_blank"
           style="color: {DF_ORANGE}; text-decoration: none;">df.com</a>
    </div>
    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.25); margin-top: 16px;">
        Interactive demo built for illustrative purposes. Data sourced from Diamond Foundry
        public materials, IEA, and industry estimates.<br>
        Projections are modeled estimates and do not represent guaranteed outcomes.
    </div>
</div>
""", unsafe_allow_html=True)
