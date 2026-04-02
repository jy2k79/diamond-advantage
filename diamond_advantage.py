"""
The Diamond Advantage — AI Data Center Impact Calculator
Built for Diamond Foundry | Interactive Streamlit Application

Design language: Faithful to df.com — typography-driven, generous whitespace,
minimal decoration, photography-style dark cards only where needed.
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
# DF BRAND PALETTE  (extracted from df.com computed styles)
# ──────────────────────────────────────────────────────────────
DF_BLACK   = "#221E1E"
DF_ORANGE  = "#FF5532"
DF_WHITE   = "#FFFFFF"
DF_BODY    = "rgba(34,30,30,0.4)"   # body text on df.com
DF_BORDER  = "rgba(226,226,226,0.5)" # pill borders, dividers
DF_BG_CARD = "#221E1E"               # dark cards (calculator, footer)

# ──────────────────────────────────────────────────────────────
# DF LOGOS — SVG marks matching df.com
# ──────────────────────────────────────────────────────────────

# Real DF logo image files (provided by DF)
import os, base64
LOGO_SHORT = os.path.join(os.path.dirname(__file__), "DF short logo.png")
LOGO_FULL  = os.path.join(os.path.dirname(__file__), "DF Logo on White.png")

def logo_b64(path):
    """Return base64 data URI for embedding logo in HTML (needed for footer on dark bg)."""
    with open(path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"


# ──────────────────────────────────────────────────────────────
# THIN-LINE SVG ICONS  (replace emojis — monoline, DF-style)
# ──────────────────────────────────────────────────────────────

def svg_icon(name, size=32, color=DF_BLACK):
    """Minimal single-stroke SVG icons matching df.com's clean aesthetic."""
    icons = {
        "bolt": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "thermometer": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
        "droplet": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
        "diamond": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 12 12 22 2 12"/></svg>',
        "zap": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "factory": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20h20"/><path d="M5 20V8l5 4V8l5 4V4h3v16"/></svg>',
        "atom": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(0 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/></svg>',
        "layers": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        "cpu": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        "arrow-right": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    }
    return icons.get(name, "")


# ──────────────────────────────────────────────────────────────
# CONSTANTS — Calculator assumptions
# ──────────────────────────────────────────────────────────────
CARBON_INTENSITY  = 0.385   # kg CO₂/kWh (US grid 2024)
WATER_M3_PER_MWH  = 1.8     # evaporative cooling avg
COOLING_REDUCTION  = 0.42    # diamond thermal advantage
ENERGY_COST_MWH   = 65      # $/MWh wholesale
PEAK_TEMP_C        = 95      # typical junction temp
TEMP_REDUCTION_C   = 52      # from DF deck
HOURS_PER_YEAR     = 8760
GLOBAL_DC_TWH      = 460     # 2024 estimate
AI_FRACTION        = 0.40
COOLING_FRACTION   = 0.35


# ──────────────────────────────────────────────────────────────
# CSS — Faithful df.com design system
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ── Global: white bg, muted body text (df.com) ── */
    .stApp {{
        background-color: {DF_WHITE} !important;
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

    /* ── Headings: df.com → weight 400, tight tracking ── */
    h1, h2, h3, h4 {{
        font-family: 'Inter', sans-serif !important;
        color: {DF_BLACK} !important;
        font-weight: 400 !important;
    }}
    h1 {{
        font-size: 64px !important;
        line-height: 64px !important;
        letter-spacing: -0.05em !important;
    }}
    h2 {{
        font-size: 32px !important;
        line-height: 40px !important;
        letter-spacing: -0.05em !important;
        margin-top: 0 !important;
    }}
    h3 {{
        font-size: 24px !important;
        letter-spacing: -0.05em !important;
    }}

    p, li, span, div {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* ── Dividers: df.com thin grey ── */
    hr {{
        border: none;
        border-top: 1px solid rgba(226,226,226,0.5);
        margin: 3.5rem 0;
    }}

    /* ── Hide Streamlit chrome ── */
    [data-testid="stSidebar"] {{ display: none; }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* ── Sliders: DF orange ── */
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
        font-size: 14px !important;
    }}

    /* ── Selectbox ── */
    .stSelectbox label {{
        color: {DF_BLACK} !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }}

    /* ── Metric cards: dark bg (calculator area only) ── */
    [data-testid="stMetric"] {{
        background-color: {DF_BG_CARD};
        border: none;
        border-radius: 16px;
        padding: 24px 28px;
        min-height: 130px;
    }}
    [data-testid="stMetricValue"] {{
        color: {DF_WHITE} !important;
        font-weight: 400 !important;
        font-size: 2rem !important;
        letter-spacing: -0.03em !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: rgba(255,255,255,0.4) !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 0.9rem !important;
    }}

    /* ── Diamond-side accent border ── */
    .df-diamond-col [data-testid="stMetric"] {{
        border-left: 3px solid {DF_ORANGE};
    }}

    /* ── Muted column (traditional silicon side) ── */
    .df-muted-col [data-testid="stMetric"] {{
        opacity: 0.5;
    }}

    /* ── Section labels: IBM Plex Mono (df.com category markers) ── */
    .df-label {{
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 14px;
        font-weight: 400;
        color: {DF_BODY};
        text-transform: none;
        margin-bottom: 12px;
    }}

    /* ── Body text (df.com muted) ── */
    .df-body {{
        font-size: 17px;
        color: {DF_BODY};
        line-height: 1.7;
        max-width: 680px;
    }}

    /* ── Stat number (large, tight tracking like df.com h1) ── */
    .df-stat-num {{
        font-family: 'Inter', sans-serif;
        font-size: 56px;
        font-weight: 400;
        color: {DF_BLACK};
        letter-spacing: -0.05em;
        line-height: 1;
    }}
    .df-stat-label {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 13px;
        font-weight: 400;
        color: {DF_BODY};
        margin-top: 8px;
    }}

    /* ── Dark card (calculator results, global impact) ── */
    .df-dark-card {{
        background: {DF_BG_CARD};
        border-radius: 16px;
        padding: 36px 32px;
        color: {DF_WHITE};
    }}

    /* ── Savings banner (white bg, thin border — df.com style) ── */
    .df-savings-card {{
        background: {DF_WHITE};
        border: 1px solid {DF_BORDER};
        border-radius: 16px;
        padding: 36px 32px;
    }}

    /* ── Pill button (df.com style) ── */
    .df-pill {{
        display: inline-flex;
        align-items: center;
        font-family: 'Inter', sans-serif;
        font-size: 17px;
        font-weight: 400;
        color: {DF_BLACK};
        border: 1px solid {DF_BORDER};
        border-radius: 999px;
        padding: 12px 24px;
        text-decoration: none;
        letter-spacing: -0.03em;
        background: rgba(226,226,226,0.5);
    }}

    /* ── CTA link (df.com "Learn more →" style) ── */
    .df-cta {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 15px;
        font-weight: 400;
        color: {DF_ORANGE};
        text-decoration: none;
    }}

    /* ── Process step (dark cards) ── */
    .df-step {{
        background: {DF_BG_CARD};
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        height: 100%;
        box-sizing: border-box;
    }}
    .df-step-title {{
        font-size: 15px;
        font-weight: 600;
        color: {DF_WHITE};
        margin: 16px 0 8px 0;
    }}
    .df-step-desc {{
        font-size: 13px;
        color: rgba(255,255,255,0.4);
        line-height: 1.6;
    }}
    .df-step-arrow {{
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(34,30,30,0.15);
        font-size: 24px;
        padding-top: 40px;
    }}

    /* ── Comparison headers ── */
    .df-comp-header {{
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 13px;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        padding-bottom: 12px;
        margin-bottom: 16px;
        border-bottom: 1px solid;
    }}
    .df-comp-trad {{
        color: {DF_BODY};
        border-color: rgba(226,226,226,0.5);
    }}
    .df-comp-diamond {{
        color: {DF_ORANGE};
        border-color: {DF_ORANGE};
    }}

    /* ── Timeline ── */
    .df-tl-item {{
        position: relative;
        padding-left: 32px;
        padding-bottom: 36px;
        border-left: 1px solid rgba(226,226,226,0.5);
        margin-left: 16px;
    }}
    .df-tl-item::before {{
        content: '';
        position: absolute;
        left: -5px;
        top: 6px;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: {DF_ORANGE};
    }}
    .df-tl-year {{
        font-size: 32px;
        font-weight: 400;
        color: {DF_BLACK};
        letter-spacing: -0.05em;
    }}
    .df-tl-headline {{
        font-size: 16px;
        font-weight: 500;
        color: {DF_BLACK};
        margin: 4px 0 8px 0;
    }}
    .df-tl-text {{
        font-size: 15px;
        color: {DF_BODY};
        line-height: 1.7;
    }}

    /* ── Footer ── */
    .df-footer {{
        background-color: {DF_BG_CARD};
        text-align: center;
        padding: 56px 32px 28px 32px;
        margin: 56px -5rem 0 -5rem;
    }}

    /* ── Chart area subtitle ── */
    .df-chart-label {{
        font-size: 14px;
        color: {DF_BODY};
        text-align: center;
        margin-top: -12px;
    }}

    /* ── Impact numbers (savings banner — on white) ── */
    .df-impact-num {{
        font-family: 'Inter', sans-serif;
        font-size: 36px;
        font-weight: 400;
        color: {DF_BLACK};
        letter-spacing: -0.05em;
        line-height: 1;
    }}
    .df-impact-label {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        color: {DF_BODY};
        margin-top: 6px;
        text-transform: uppercase;
    }}

    /* ── Global stat card (dark, for section 4) ── */
    .df-global-card {{
        background: {DF_BG_CARD};
        border-radius: 16px;
        padding: 32px 24px;
        text-align: center;
        height: 100%;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .df-global-num {{
        font-size: 44px;
        font-weight: 400;
        color: {DF_WHITE};
        letter-spacing: -0.05em;
        line-height: 1.1;
    }}
    .df-global-unit {{
        font-size: 14px;
        color: {DF_ORANGE};
        font-weight: 500;
        margin-bottom: 8px;
    }}
    .df-global-label {{
        font-size: 14px;
        color: rgba(255,255,255,0.6);
        font-weight: 400;
    }}
    .df-global-sub {{
        font-size: 12px;
        color: rgba(255,255,255,0.3);
        margin-top: 8px;
        line-height: 1.4;
    }}

    /* ══════════════════════════════════════════════════════
       TABLET  (≤960px) — process step arrows hide early
       ══════════════════════════════════════════════════════ */
    @media (max-width: 960px) {{
        .df-step-arrow-sep {{
            display: none !important;
        }}
    }}

    /* ══════════════════════════════════════════════════════
       MOBILE RESPONSIVE  (≤768px)
       ══════════════════════════════════════════════════════ */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        /* Headings scale down */
        h1 {{
            font-size: 36px !important;
            line-height: 38px !important;
            letter-spacing: -0.03em !important;
        }}
        h2 {{
            font-size: 24px !important;
            line-height: 30px !important;
        }}
        h3 {{
            font-size: 20px !important;
        }}

        /* Hero stats: 2×2 grid */
        .df-stat-num {{
            font-size: 36px !important;
        }}
        .df-stat-label {{
            font-size: 12px !important;
        }}

        /* Metric cards: slightly less padding */
        [data-testid="stMetric"] {{
            padding: 18px 20px;
            min-height: 110px;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 1.6rem !important;
        }}

        /* Process steps: vertical stack */
        .df-step {{
            padding: 20px 16px;
        }}
        .df-step-title {{
            font-size: 14px;
        }}
        .df-step-desc {{
            font-size: 12px;
        }}

        /* Savings banner numbers */
        .df-impact-num {{
            font-size: 28px !important;
        }}

        /* Global cards */
        .df-global-card {{
            padding: 24px 16px;
            min-height: 140px;
        }}
        .df-global-num {{
            font-size: 32px !important;
        }}

        /* Timeline */
        .df-tl-year {{
            font-size: 24px;
        }}

        /* Footer: less negative margin */
        .df-footer {{
            margin-left: -1rem;
            margin-right: -1rem;
            padding: 36px 16px 20px 16px;
        }}

        /* Dividers: less vertical margin */
        hr {{
            margin: 2rem 0;
        }}
    }}

    /* ══════════════════════════════════════════════════════
       SMALL MOBILE  (≤480px)
       ══════════════════════════════════════════════════════ */
    @media (max-width: 480px) {{
        h1 {{
            font-size: 28px !important;
            line-height: 32px !important;
        }}
        .df-stat-num {{
            font-size: 28px !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 1.3rem !important;
        }}
        .df-impact-num {{
            font-size: 24px !important;
        }}
        .df-global-num {{
            font-size: 28px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PASSWORD GATE  (optional — only if secrets configured)
# ══════════════════════════════════════════════════════════════
def check_password():
    try:
        correct = st.secrets["password"]
    except (KeyError, FileNotFoundError):
        return True
    if st.session_state.get("authenticated"):
        return True
    col_pw_l, col_pw_c, col_pw_r = st.columns([1, 1, 1])
    with col_pw_c:
        st.image(LOGO_SHORT, width=80)
        st.markdown('<h2 style="font-size:24px;text-align:center;">The Diamond Advantage</h2>',
                    unsafe_allow_html=True)
        st.markdown('<p class="df-body" style="text-align:center;">Enter password to continue</p>',
                    unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        pw = st.text_input("Password", type="password", label_visibility="collapsed")
        if pw:
            if pw == correct:
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

st.image(LOGO_SHORT, width=70)

st.markdown("""
<h1>What if we could cool AI<br>
<span style="color:#FF5532;">with diamonds?</span></h1>
""", unsafe_allow_html=True)

st.markdown(f"""
<p class="df-body" style="margin-top:24px;">
AI is hitting a wall. Not of intelligence, but of heat.
Every generation of chips runs hotter, drinks more power, demands more cooling.
Diamond Foundry replaces traditional substrates with single-crystal diamond,
the most thermally conductive material on Earth. Grown from captured methane greenhouse gas.
</p>
""", unsafe_allow_html=True)

# Hero stats — clean, typography-driven (like df.com)
st.markdown("<br>", unsafe_allow_html=True)
hero_cols = st.columns(4)
hero_data = [
    ("17,200×", "Semiconductor figure of merit vs silicon"),
    ("2,200+", "W/mK thermal conductivity"),
    ("52°C", "Chip temperature reduction"),
    ("3.7×", "Higher power density"),
]
for col, (val, label) in zip(hero_cols, hero_data):
    with col:
        st.markdown(f"""
        <div style="padding:12px 0;">
            <div class="df-stat-num">{val}</div>
            <div class="df-stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════
#  SECTION 1 — THE AI POWER CRISIS
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-label">The Problem</div>', unsafe_allow_html=True)
st.markdown("## The AI Infrastructure Crisis")

crisis_cols = st.columns(3)
crisis_data = [
    ("bolt", "Power Hungry",
     "Global data centers consumed ~460 TWh in 2024. "
     "Roughly 2% of global electricity. AI workloads are projected to push this past "
     "1,000 TWh by 2028."),
    ("thermometer", "Heat Wall",
     "Modern AI chips like NVIDIA's B200 push 1,000W per GPU. "
     "Traditional silicon substrates can't dissipate this heat fast enough. "
     "Chips throttle. Energy is wasted on cooling."),
    ("droplet", "Water & Carbon Cost",
     "A single large AI data center can consume 5+ million gallons "
     "of water daily for cooling. Training one large AI model "
     "can exceed 300 tons of CO₂."),
]
for col, (icon, title, desc) in zip(crisis_cols, crisis_data):
    with col:
        st.markdown(f"""
        <div style="padding:24px 0;">
            <div style="margin-bottom:16px;">{svg_icon(icon, 28, "rgba(34,30,30,0.3)")}</div>
            <div style="font-size:18px;font-weight:500;color:{DF_BLACK};margin-bottom:12px;">{title}</div>
            <div style="font-size:16px;color:{DF_BODY};line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# Thermal conductivity chart
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="df-label">Why Diamond?</div>', unsafe_allow_html=True)
st.markdown("### Thermal Conductivity Comparison")

materials = ["Silicon", "Gallium Nitride", "Copper", "Silicon Carbide", "Diamond (SCD)"]
conductivity = [150, 200, 380, 490, 2200]
bar_colors = ["rgba(34,30,30,0.15)"] * 4 + [DF_ORANGE]

fig_thermal = go.Figure()
fig_thermal.add_trace(go.Bar(
    x=conductivity, y=materials, orientation='h',
    marker=dict(color=bar_colors, line=dict(width=0), cornerradius=6),
    text=[f"  {v:,} W/mK" for v in conductivity],
    textposition='outside',
    textfont=dict(color=DF_BLACK, size=13, family="Inter"),
    hovertemplate='%{y}: %{x:,} W/mK<extra></extra>',
))
fig_thermal.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", color="rgba(34,30,30,0.4)", size=13),
    height=260, margin=dict(l=0, r=80, t=10, b=10),
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 2800]),
    yaxis=dict(showgrid=False, tickfont=dict(size=13, color="rgba(34,30,30,0.4)"), autorange="reversed"),
    bargap=0.35,
)
st.plotly_chart(fig_thermal, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
<p class="df-chart-label">
    Diamond conducts heat 14.7× better than silicon and 5.8× better than copper.
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════
#  SECTION 2 — INTERACTIVE CALCULATOR  (@st.fragment)
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-label">Interactive Calculator</div>', unsafe_allow_html=True)
st.markdown("## The Diamond Advantage Calculator")
st.markdown(f"""
<p class="df-body" style="margin-bottom:28px;">
Configure a hypothetical AI data center and see the impact of switching from
traditional silicon substrates to Diamond Foundry's single-crystal diamond technology.
</p>
""", unsafe_allow_html=True)


# Inject JS to make sliders fire updates during drag (works on desktop + mobile touch)
st.markdown("""
<script>
(function() {
    const DEBOUNCE_MS = 150;
    let timers = {};

    function attachLiveDrag() {
        const sliders = document.querySelectorAll('[data-baseweb="slider"] div[role="slider"]');
        sliders.forEach((thumb, idx) => {
            if (thumb.dataset.liveDrag) return;
            thumb.dataset.liveDrag = "true";

            const observer = new MutationObserver(() => {
                clearTimeout(timers[idx]);
                timers[idx] = setTimeout(() => {
                    // Dispatch both mouse and touch end events for cross-device support
                    thumb.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
                    thumb.dispatchEvent(new TouchEvent('touchend', {bubbles: true}));
                }, DEBOUNCE_MS);
            });
            observer.observe(thumb, {attributes: true, attributeFilter: ['aria-valuenow']});
        });
    }

    const bodyObserver = new MutationObserver(() => { setTimeout(attachLiveDrag, 300); });
    bodyObserver.observe(document.body, {childList: true, subtree: true});
    setTimeout(attachLiveDrag, 800);
})();
</script>
""", unsafe_allow_html=True)


@st.fragment
def calculator_fragment():
    """Calculator wrapped in st.fragment for real-time slider updates."""

    # ── Controls ──
    c1, c2, c3 = st.columns(3)
    with c1:
        num_gpus = st.slider("Number of AI GPUs", 1000, 100000, 20000, 1000,
                             format="%d", help="Typical large cluster: 10,000–50,000 GPUs")
    with c2:
        power_per_gpu = st.slider("Power per GPU (Watts)", 300, 1500, 700, 50,
                                  format="%dW", help="A100: ~400W, H100: ~700W, B200: ~1000W")
    with c3:
        pue = st.selectbox("Cooling Efficiency (PUE)", [
            ("Air-cooled (PUE 1.6)", 1.6),
            ("Efficient air (PUE 1.3)", 1.3),
            ("Liquid-cooled (PUE 1.15)", 1.15),
        ], format_func=lambda x: x[0], index=0,
           help="Power Usage Effectiveness. How much overhead goes to cooling.")
        pue_val = pue[1]

    # ── Calculations ──
    it_kw = (num_gpus * power_per_gpu) / 1000
    facility_kw = it_kw * pue_val
    cooling_kw = facility_kw - it_kw
    annual_mwh = facility_kw * HOURS_PER_YEAR / 1000
    annual_co2 = annual_mwh * CARBON_INTENSITY
    annual_water = cooling_kw * HOURS_PER_YEAR / 1000 * WATER_M3_PER_MWH

    d_temp = PEAK_TEMP_C - TEMP_REDUCTION_C
    d_cooling_kw = cooling_kw * (1 - COOLING_REDUCTION)
    d_facility_kw = it_kw + d_cooling_kw
    d_annual_mwh = d_facility_kw * HOURS_PER_YEAR / 1000
    d_co2 = d_annual_mwh * CARBON_INTENSITY
    d_water = d_cooling_kw * HOURS_PER_YEAR / 1000 * WATER_M3_PER_MWH

    saved_mwh = annual_mwh - d_annual_mwh
    saved_co2 = annual_co2 - d_co2
    saved_water = annual_water - d_water
    saved_gal = saved_water * 264.172
    saved_cost = saved_mwh * ENERGY_COST_MWH

    # ── Comparison headers ──
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin:28px 0 8px 0;">
        <div class="df-comp-header df-comp-trad" style="flex:1;text-align:center;">Traditional Silicon</div>
        <div class="df-comp-header df-comp-diamond" style="flex:1;text-align:center;">Diamond Foundry SCD</div>
    </div>
    """, unsafe_allow_html=True)

    # Temperature
    r1a, r1b = st.columns(2)
    with r1a:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Peak Chip Temperature", f"{PEAK_TEMP_C}°C")
        st.markdown('</div>', unsafe_allow_html=True)
    with r1b:
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Peak Chip Temperature", f"{d_temp}°C",
                  delta=f"-{TEMP_REDUCTION_C}°C cooler", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # Power
    r2a, r2b = st.columns(2)
    with r2a:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Total Facility Power", f"{facility_kw:,.0f} kW")
        st.markdown('</div>', unsafe_allow_html=True)
    with r2b:
        pct_power = (1 - d_facility_kw / facility_kw) * 100
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Total Facility Power", f"{d_facility_kw:,.0f} kW",
                  delta=f"-{pct_power:.0f}% power draw", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # CO₂
    r3a, r3b = st.columns(2)
    with r3a:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Annual CO₂ Emissions", f"{annual_co2:,.0f} tons")
        st.markdown('</div>', unsafe_allow_html=True)
    with r3b:
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Annual CO₂ Emissions", f"{d_co2:,.0f} tons",
                  delta=f"-{saved_co2:,.0f} tons/year", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # Water
    r4a, r4b = st.columns(2)
    with r4a:
        st.markdown('<div class="df-muted-col">', unsafe_allow_html=True)
        st.metric("Annual Water Usage", f"{annual_water:,.0f} m³")
        st.markdown('</div>', unsafe_allow_html=True)
    with r4b:
        st.markdown('<div class="df-diamond-col">', unsafe_allow_html=True)
        st.metric("Annual Water Usage", f"{d_water:,.0f} m³",
                  delta=f"-{saved_water:,.0f} m³/year", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Savings banner ──
    st.markdown(f"""
    <div class="df-savings-card" style="margin-top:28px;">
        <div class="df-label" style="text-align:center;">Annual Savings with Diamond Foundry</div>
        <div style="display:flex;justify-content:space-around;text-align:center;margin-top:16px;flex-wrap:wrap;">
            <div style="padding:8px 16px;">
                <div class="df-impact-num">{saved_mwh:,.0f}</div>
                <div class="df-impact-label">MWh Energy Saved</div>
            </div>
            <div style="padding:8px 16px;">
                <div class="df-impact-num">{saved_co2:,.0f}</div>
                <div class="df-impact-label">Tons CO₂ Avoided</div>
            </div>
            <div style="padding:8px 16px;">
                <div class="df-impact-num">{saved_gal / 1e6:,.1f}M</div>
                <div class="df-impact-label">Gallons Water Saved</div>
            </div>
            <div style="padding:8px 16px;">
                <div class="df-impact-num">${saved_cost / 1e6:,.1f}M</div>
                <div class="df-impact-label">Annual Cost Savings</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts ──
    st.markdown("<br>", unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)

    with ch1:
        fig_power = go.Figure()
        fig_power.add_trace(go.Bar(
            name='IT Load (GPUs)', x=['Traditional<br>Silicon', 'Diamond<br>Foundry SCD'],
            y=[it_kw, it_kw], marker_color="rgba(34,30,30,0.15)", marker_cornerradius=4,
            text=[f'{it_kw:,.0f} kW'] * 2, textposition='inside',
            textfont=dict(color=DF_BLACK, size=12, family="Inter"),
            hovertemplate='IT Load: %{y:,.0f} kW<extra></extra>',
        ))
        fig_power.add_trace(go.Bar(
            name='Cooling Overhead', x=['Traditional<br>Silicon', 'Diamond<br>Foundry SCD'],
            y=[cooling_kw, d_cooling_kw],
            marker_color=["rgba(255,85,50,0.4)", DF_ORANGE], marker_cornerradius=4,
            text=[f'{cooling_kw:,.0f} kW', f'{d_cooling_kw:,.0f} kW'],
            textposition='inside', textfont=dict(color=DF_WHITE, size=12, family="Inter"),
            hovertemplate='Cooling: %{y:,.0f} kW<extra></extra>',
        ))
        fig_power.update_layout(
            barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="rgba(34,30,30,0.4)", size=12),
            height=350, margin=dict(l=20, r=20, t=40, b=20),
            title=dict(text="Power Breakdown (kW)", font=dict(size=14, color=DF_BLACK)),
            yaxis=dict(showgrid=True, gridcolor="rgba(226,226,226,0.5)", zeroline=False,
                       tickfont=dict(color="rgba(34,30,30,0.4)")),
            xaxis=dict(tickfont=dict(color=DF_BLACK, size=12)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
                        font=dict(color="rgba(34,30,30,0.4)", size=11)),
            bargap=0.4,
        )
        st.plotly_chart(fig_power, use_container_width=True, config={'displayModeBar': False})

    with ch2:
        pct_red = (saved_co2 / annual_co2) * 100 if annual_co2 > 0 else 0
        fig_donut = go.Figure()
        fig_donut.add_trace(go.Pie(
            labels=['CO₂ Avoided', 'Remaining'],
            values=[saved_co2, d_co2], hole=0.7,
            marker=dict(colors=[DF_ORANGE, "rgba(34,30,30,0.1)"], line=dict(width=0)),
            textinfo='none',
            hovertemplate='%{label}: %{value:,.0f} tons<extra></extra>',
        ))
        fig_donut.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="rgba(34,30,30,0.4)"),
            height=350, margin=dict(l=20, r=20, t=40, b=20),
            title=dict(text="CO₂ Reduction Impact", font=dict(size=14, color=DF_BLACK)),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                        font=dict(color="rgba(34,30,30,0.4)", size=11)),
            annotations=[dict(
                text=f"<b>{pct_red:.0f}%</b><br><span style='font-size:12px'>reduction</span>",
                x=0.5, y=0.5, font=dict(size=28, color=DF_ORANGE, family="Inter"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})


calculator_fragment()

st.markdown("---")


# ══════════════════════════════════════════════════════════════
#  SECTION 3 — FROM METHANE TO DIAMOND
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-label">The Process</div>', unsafe_allow_html=True)
st.markdown("## From Greenhouse Gas to Diamond")
st.markdown(f"""
<p class="df-body" style="margin-bottom:32px;">
Diamond Foundry doesn't mine diamonds. It crystallizes them from methane,
a potent greenhouse gas. Proprietary plasma reactors powered by green energy
transform a climate problem into the world's most advanced thermal substrate.
</p>
""", unsafe_allow_html=True)

# Process steps — rendered as single HTML flexbox for proper sizing
steps = [
    ("factory", "Methane Capture",
     "CH₄ greenhouse gas sourced as carbon feedstock. A climate liability becomes raw material."),
    ("zap", "Plasma Reactor",
     "10th-gen reactors at 150× productivity. Methane broken into atomic carbon."),
    ("diamond", "Crystal Growth",
     "Carbon atoms self-assemble into single-crystal diamond. Patented heteroepitaxy."),
    ("layers", "Wafer Finishing",
     "Polished to angstrom-level flatness. Atomically bonded to silicon or SiC."),
    ("cpu", "AI-Ready Substrate",
     "SCD wafer conducts heat 14.7× better than silicon. Next-gen AI chips, enabled."),
]

step_html_items = []
for i, (icon, title, desc) in enumerate(steps):
    step_html_items.append(f"""
    <div class="df-step" style="flex:1;min-width:160px;">
        <div>{svg_icon(icon, 28, DF_WHITE)}</div>
        <div class="df-step-title">{title}</div>
        <div class="df-step-desc">{desc}</div>
    </div>
    """)
    if i < len(steps) - 1:
        step_html_items.append(f"""
        <div class="df-step-arrow-sep" style="display:flex;align-items:center;padding:0 4px;flex-shrink:0;">
            {svg_icon("arrow-right", 18, "rgba(34,30,30,0.15)")}
        </div>
        """)

st.markdown(f"""
<div style="display:flex;gap:8px;align-items:stretch;flex-wrap:wrap;">
    {"".join(step_html_items)}
</div>
""", unsafe_allow_html=True)

# Carbon sequestration callout
st.markdown(f"""
<div class="df-dark-card" style="margin-top:36px;text-align:center;">
    <div style="font-size:24px;font-weight:400;color:{DF_WHITE};letter-spacing:-0.03em;margin-bottom:8px;">
        Crystallizing Greenhouse Gas into Single-Crystal Diamond
    </div>
    <div style="font-size:15px;color:rgba(255,255,255,0.4);max-width:600px;margin:0 auto;line-height:1.7;">
        Every diamond wafer permanently locks carbon atoms
        into the hardest, most thermally conductive material known to science.
        Powered by hydroelectric and solar energy.
    </div>
    <div style="display:flex;justify-content:center;gap:56px;margin-top:28px;flex-wrap:wrap;">
        <div style="text-align:center;">
            <div style="font-size:32px;font-weight:400;color:{DF_WHITE};letter-spacing:-0.03em;">97%</div>
            <div class="df-impact-label">of global SCD capacity</div>
        </div>
        <div>
            <div style="font-size:32px;font-weight:400;color:{DF_WHITE};letter-spacing:-0.03em;">10th Gen</div>
            <div class="df-impact-label">proprietary reactors</div>
        </div>
        <div>
            <div style="font-size:32px;font-weight:400;color:{DF_WHITE};letter-spacing:-0.03em;">100%</div>
            <div class="df-impact-label">green energy powered</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════
#  SECTION 4 — GLOBAL IMPACT AT SCALE
# ══════════════════════════════════════════════════════════════

st.markdown('<div class="df-label">The Big Picture</div>', unsafe_allow_html=True)
st.markdown("## If Every AI Data Center Used Diamond")
st.markdown(f"""
<p class="df-body" style="margin-bottom:32px;">
The world is building AI infrastructure at an unprecedented pace. Here's what it would mean
if Diamond Foundry's SCD technology were deployed across the global AI data center fleet.
</p>
""", unsafe_allow_html=True)

# Global estimates
g_ai_twh = GLOBAL_DC_TWH * AI_FRACTION
g_cooling_twh = g_ai_twh * COOLING_FRACTION
g_saved_twh = g_cooling_twh * COOLING_REDUCTION
g_co2_mt = g_saved_twh * 1e6 * CARBON_INTENSITY / 1e6
g_water_bgal = g_cooling_twh * 1e6 * WATER_M3_PER_MWH * 264.172 / 1e9
g_homes = g_saved_twh * 1e6 / 10.5
g_cars = g_co2_mt * 1e6 / 4.6

g_cols = st.columns(4)
global_stats = [
    (f"{g_saved_twh:.1f}", "TWh", "Energy saved annually",
     "Equivalent to powering a small country"),
    (f"{g_co2_mt:.1f}M", "tons", "CO₂ emissions avoided",
     f"Like removing {g_cars/1e6:.1f}M cars from roads"),
    (f"{g_water_bgal:.0f}B", "gallons", "Water conserved",
     "Enough to supply a major city for a year"),
    (f"{g_homes/1e6:.1f}M", "homes", "Equivalent energy freed",
     "Redirected from cooling to useful compute"),
]
for col, (num, unit, label, sublabel) in zip(g_cols, global_stats):
    with col:
        st.markdown(f"""
        <div class="df-global-card">
            <div class="df-global-num">{num}</div>
            <div class="df-global-unit">{unit}</div>
            <div class="df-global-label">{label}</div>
            <div class="df-global-sub">{sublabel}</div>
        </div>
        """, unsafe_allow_html=True)

# Growth projection chart
st.markdown("<br>", unsafe_allow_html=True)

years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
baseline = [460, 550, 660, 790, 950, 1100, 1280]
with_diamond = [460, 530, 610, 700, 790, 880, 980]

fig_proj = go.Figure()
fig_proj.add_trace(go.Scatter(
    x=years, y=baseline, name='Without Diamond (Baseline)',
    line=dict(color="rgba(34,30,30,0.2)", width=2, dash='dot'),
    mode='lines+markers', marker=dict(size=6, color="rgba(34,30,30,0.2)"),
    hovertemplate='%{x}: %{y:,.0f} TWh<extra>Baseline</extra>',
))
fig_proj.add_trace(go.Scatter(
    x=years, y=with_diamond, name='With Diamond Foundry SCD',
    line=dict(color=DF_ORANGE, width=2),
    mode='lines+markers', marker=dict(size=6, color=DF_ORANGE),
    fill='tonexty', fillcolor="rgba(255,85,50,0.06)",
    hovertemplate='%{x}: %{y:,.0f} TWh<extra>With Diamond</extra>',
))
fig_proj.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", color="rgba(34,30,30,0.4)", size=12),
    height=380, margin=dict(l=20, r=20, t=50, b=20),
    title=dict(text="Projected Global Data Center Energy Consumption (TWh)",
               font=dict(size=14, color=DF_BLACK)),
    xaxis=dict(showgrid=False, tickfont=dict(color="rgba(34,30,30,0.4)", size=12), dtick=1),
    yaxis=dict(showgrid=True, gridcolor="rgba(226,226,226,0.5)", zeroline=False,
               tickfont=dict(color="rgba(34,30,30,0.4)"), ticksuffix=" TWh"),
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,
                font=dict(color="rgba(34,30,30,0.4)", size=12)),
)
fig_proj.add_annotation(
    x=2029, y=(baseline[5] + with_diamond[5]) / 2,
    text=f"<b>{baseline[5] - with_diamond[5]} TWh saved</b>",
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

st.markdown('<div class="df-label">The Vision</div>', unsafe_allow_html=True)
st.markdown("## Diamond Foundry's Three-Decade Master Plan")

timeline = [
    ("2013", "Introduce sustainably created diamond wherever mined diamond has been able to go",
     "Diamond Foundry launched with lab-grown gems. Proving that diamonds could be created "
     "from methane using green energy, with zero mining. Today: 26% market share of rough diamonds."),
    ("2023", "Introduce single-crystal diamond wafers and put a diamond behind every chip",
     "World's first SCD wafers created. $200M+ revenue with 26% net profit margin. "
     "Partnerships with Infineon. Global manufacturing across USA, Spain, and Germany."),
    ("2033", "Introduce diamond as a semiconductor and deliver on its 17,200× merit over silicon",
     "The ultimate vision: diamond-based semiconductor devices. Not just thermal substrates, "
     "but active diamond electronics. Unlocking the full 17,200× semiconductor figure of merit."),
]
for year, headline, desc in timeline:
    st.markdown(f"""
    <div class="df-tl-item">
        <div class="df-tl-year">{year}</div>
        <div class="df-tl-headline">{headline}</div>
        <div class="df-tl-text">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="df-footer">
    <div style="margin-bottom:16px;display:flex;justify-content:center;">
        <img src="{logo_b64(LOGO_FULL)}" alt="Diamond Foundry"
             style="width:260px;opacity:0.4;filter:invert(1);" />
    </div>
    <div style="font-size:14px;color:rgba(255,255,255,0.3);line-height:1.7;">
        Empowering mega-tech industry to shape the future.<br>
        <a href="https://www.df.com" target="_blank"
           style="color:{DF_ORANGE};text-decoration:none;">df.com</a>
    </div>
    <div style="margin-top:24px;font-size:12px;color:rgba(255,255,255,0.15);">
        Interactive tool built for Diamond Foundry
    </div>
</div>
""", unsafe_allow_html=True)
