import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyreadstat


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Human-AI Collaboration Behaviour",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME COLOURS — RUST / BEIGE / CREAM / BROWN
# ============================================================

DEEP_RUST = "#8F3F2F"
RUST = "#A94F35"
BURNT_ORANGE = "#C46A43"
WARM_BEIGE = "#E7D7C3"
LIGHT_BEIGE = "#F3E8D8"
CREAM = "#FBF7F0"
DARK_BROWN = "#382823"
BROWN = "#654A40"
SOFT_TAUPE = "#B8A397"
WHITE = "#FFFDFC"
BORDER = "#D8C5B5"

# Aliases kept so downstream chart code reads naturally
TEXT_DARK = DARK_BROWN
MUTED = BROWN
PRIMARY_ACCENT = RUST
SECONDARY_ACCENT = BURNT_ORANGE

# Per-RAIC-category tonal accents (all still within the existing palette)
RAIC_ACCENTS = {
    "AI-Dependent User": BURNT_ORANGE,
    "Developing AI Collaborator": RUST,
    "Balanced AI Collaborator": DEEP_RUST,
    "Responsible AI Collaborator": DARK_BROWN,
}


# ============================================================
# CUSTOM THEME
# ============================================================

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: Georgia, "Times New Roman", serif !important;
    }}

    /* ---------------- APP BACKGROUND ---------------- */

    .stApp {{
        background-color: #F3E8D8;
        background-image:
            radial-gradient(circle at 18% 8%, rgba(196,106,67,0.10) 0%, rgba(196,106,67,0) 32%),
            radial-gradient(circle at 92% 4%, rgba(143,63,47,0.09) 0%, rgba(143,63,47,0) 30%),
            radial-gradient(rgba(143,63,47,0.09) 1px, transparent 1px),
            linear-gradient(135deg, #FBF7F0 0%, #F3E8D8 55%, #E7D7C3 100%);
        background-size: auto, auto, 26px 26px, auto;
        background-position: 0 0, 0 0, 0 0, 0 0;
        color: {DARK_BROWN};
        font-family: Georgia, "Times New Roman", serif;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
        height: 2.2rem;
    }}

    .main .block-container {{
        max-width: 1360px;
        padding-top: 0.4rem;
        padding-bottom: 2rem;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    div.block-container > div:first-child {{
        margin-top: 0 !important;
    }}

    h1 {{
        font-family: "Playfair Display", Georgia, serif !important;
        color: {DARK_BROWN} !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
        font-size: 2.05rem !important;
        margin-bottom: 0.1rem !important;
    }}

    h2, h3, h4, h5, h6 {{
        font-family: "Playfair Display", Georgia, serif !important;
        color: {DEEP_RUST} !important;
        font-weight: 700 !important;
    }}

    p, span, div, label, li {{
        font-family: Georgia, "Times New Roman", serif;
    }}

    p {{
        color: {DARK_BROWN};
    }}

    ::selection {{
        background: rgba(196,106,67,0.28);
    }}

    /* ---------------- TOP APP TITLE BAND ---------------- */

    .app-title-band {{
        position: relative;
        padding: 6px 4px 10px 4px;
        margin-bottom: 4px;
    }}

    .app-eyebrow {{
        font-family: "Inter", sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2.2px;
        text-transform: uppercase;
        color: {RUST};
        margin-bottom: 2px;
    }}

    .app-title-band h1 {{
        margin-bottom: 2px !important;
    }}

    .app-title-rule {{
        width: 56px;
        height: 3px;
        border-radius: 3px;
        background: linear-gradient(90deg, {DEEP_RUST}, {BURNT_ORANGE});
        margin-top: 6px;
    }}

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {{
        background-color: #8F3F2F;
        background-image:
            radial-gradient(rgba(255,253,252,0.07) 1px, transparent 1px),
            linear-gradient(180deg, #5C2D25 0%, #8F3F2F 50%, #A94F35 100%);
        background-size: 20px 20px, auto;
    }}

    section[data-testid="stSidebar"] * {{
        color: {CREAM} !important;
        font-family: Georgia, "Times New Roman", serif;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        font-family: "Playfair Display", Georgia, serif !important;
        color: {CREAM} !important;
    }}

    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] > div > div > div > label {{
        font-family: "Inter", sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.9px;
        text-transform: uppercase;
        opacity: 0.92;
    }}

    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: rgba(255,253,252,0.96);
        color: {DARK_BROWN} !important;
        border-radius: 10px;
        border: 1px solid rgba(255,253,252,0.35);
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: border 0.18s ease, box-shadow 0.18s ease;
    }}

    section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {{
        border: 1px solid {CREAM};
    }}

    section[data-testid="stSidebar"] [data-baseweb="select"] span {{
        color: {DARK_BROWN} !important;
    }}

    section[data-testid="stSidebar"] [data-baseweb="tag"] {{
        background: {BURNT_ORANGE} !important;
        border-radius: 6px !important;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        background: rgba(255,253,252,0.08) !important;
        border: 1.5px solid rgba(255,253,252,0.55) !important;
        color: {CREAM} !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-family: "Inter", sans-serif !important;
        letter-spacing: 0.4px;
        transition: all 0.18s ease;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255,253,252,0.20) !important;
        border-color: {CREAM} !important;
        transform: translateY(-1px);
    }}

    .sidebar-heading {{
        font-family: "Playfair Display", Georgia, serif !important;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0px;
    }}

    .sidebar-sub {{
        color: rgba(251,247,240,0.78) !important;
        font-size: 0.78rem !important;
        font-family: "Inter", sans-serif !important;
        letter-spacing: 0.3px;
        margin-top: -4px;
        margin-bottom: 14px;
    }}

    .sidebar-divider {{
        height: 1px;
        background: rgba(255,253,252,0.22);
        margin: 14px 0 14px 0;
        border: none;
    }}

    .sidebar-section-label {{
        font-family: "Inter", sans-serif !important;
        font-size: 0.66rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        color: rgba(251,247,240,0.60) !important;
        margin: 2px 0 6px 2px;
    }}

    /* ---------------- NAVIGATION (segmented control) ---------------- */

    div[role="radiogroup"] {{
        background: rgba(255,253,252,0.80);
        backdrop-filter: blur(6px);
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 6px;
        gap: 4px;
        box-shadow: 0 4px 16px rgba(56,40,35,0.09);
    }}

    div[role="radiogroup"] label {{
        font-family: "Inter", sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.2px;
        color: {BROWN} !important;
        border-radius: 10px;
        padding: 7px 15px;
        transition: all 0.16s ease;
    }}

    div[role="radiogroup"] label:hover {{
        background: rgba(196,106,67,0.10);
    }}

    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {{
        background: linear-gradient(135deg, {DEEP_RUST}, {RUST}) !important;
        box-shadow: 0 3px 10px rgba(143,63,47,0.35);
    }}

    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) div {{
        color: {CREAM} !important;
        font-weight: 700 !important;
    }}

    /* ---------------- METRICS (native st.metric fallback) ---------------- */

    div[data-testid="stMetric"] {{
        background: rgba(255,253,252,0.85);
        border: 1px solid {BORDER};
        border-left: 3px solid {RUST};
        border-radius: 13px;
        padding: 9px 12px;
        min-height: 78px;
        box-shadow: 0 3px 12px rgba(56,40,35,0.07);
    }}

    div[data-testid="stMetricLabel"] {{
        font-family: "Inter", sans-serif !important;
        color: {BROWN} !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    div[data-testid="stMetricValue"] {{
        font-family: "Playfair Display", Georgia, serif !important;
        color: {DEEP_RUST} !important;
        font-size: 1.32rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }}

    /* ---------------- CUSTOM PREMIUM METRIC CARDS ---------------- */

    .kpi-card {{
        position: relative;
        background: linear-gradient(160deg, rgba(255,253,252,0.94), rgba(251,247,240,0.72));
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 14px 16px 12px 16px;
        box-shadow: 0 4px 16px rgba(56,40,35,0.08);
        overflow: hidden;
        min-height: 92px;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(56,40,35,0.13);
    }}

    .kpi-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background: linear-gradient(90deg, {DEEP_RUST}, {BURNT_ORANGE}, {WARM_BEIGE});
    }}

    .kpi-card::after {{
        content: "";
        position: absolute;
        bottom: -22px; right: -22px;
        width: 62px; height: 62px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(196,106,67,0.14), rgba(196,106,67,0));
    }}

    .kpi-label {{
        position: relative;
        z-index: 1;
        font-family: "Inter", sans-serif;
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.9px;
        text-transform: uppercase;
        color: {BROWN};
        margin-bottom: 6px;
    }}

    .kpi-value {{
        position: relative;
        z-index: 1;
        font-family: "Playfair Display", Georgia, serif;
        font-size: 1.62rem;
        font-weight: 700;
        color: {DEEP_RUST};
    }}

    /* ---------------- CONTAINERS / CARDS ---------------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: linear-gradient(160deg, rgba(255,253,252,0.80), rgba(251,247,240,0.62));
        border: 1px solid {BORDER};
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(56,40,35,0.08);
    }}

    .stCaption {{
        color: {BROWN} !important;
        font-family: "Inter", sans-serif !important;
    }}

    .stMarkdown {{
        color: {DARK_BROWN};
        font-family: Georgia, "Times New Roman", serif;
    }}

    /* ---------------- SECTION HEADINGS ---------------- */

    .section-heading {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
        margin-bottom: 2px;
    }}

    .section-marker {{
        width: 9px;
        height: 9px;
        border-radius: 3px;
        background: {RUST};
        transform: rotate(45deg);
        flex-shrink: 0;
    }}

    .section-heading h3 {{
        margin: 0 !important;
    }}

    .section-rule-full {{
        height: 1px;
        background: linear-gradient(90deg, {BORDER}, transparent);
        margin: 2px 0 14px 0;
    }}

    /* ---------------- PAGE HEADER SYSTEM ---------------- */

    .page-header-wrap {{
        position: relative;
        padding: 14px 20px 16px 20px;
        margin-bottom: 6px;
        border-radius: 16px;
        background: linear-gradient(120deg, rgba(231,215,195,0.55), rgba(251,247,240,0.35));
        border: 1px solid {BORDER};
        overflow: hidden;
    }}

    .page-header-shape {{
        position: absolute;
        top: -40px;
        right: -30px;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(169,79,53,0.13), rgba(169,79,53,0));
        z-index: 0;
    }}

    .page-header-eyebrow {{
        position: relative;
        z-index: 1;
        font-family: "Inter", sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: {RUST};
        margin-bottom: 3px;
    }}

    .page-header-title {{
        position: relative;
        z-index: 1;
        font-family: "Playfair Display", Georgia, serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: {DARK_BROWN};
        margin-bottom: 3px;
    }}

    .page-header-rule {{
        position: relative;
        z-index: 1;
        width: 46px;
        height: 3px;
        border-radius: 3px;
        background: linear-gradient(90deg, {DEEP_RUST}, {BURNT_ORANGE});
    }}

    /* ---------------- INFERENCE BOX ---------------- */

    .inference-box {{
        position: relative;
        background: linear-gradient(120deg, rgba(255,253,252,0.92), rgba(243,232,216,0.55));
        border-left: 4px solid {RUST};
        border-radius: 10px;
        padding: 11px 15px;
        margin: 6px 0 20px 0;
        box-shadow: 0 3px 10px rgba(56,40,35,0.07);
    }}

    .inference-title {{
        color: {DEEP_RUST};
        font-family: "Inter", sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .inference-text {{
        color: {DARK_BROWN};
        font-family: Georgia, serif;
        font-size: 0.87rem;
        line-height: 1.55;
    }}

    /* ---------------- RAIC CATEGORY CARDS ---------------- */

    .raic-card {{
        position: relative;
        background: linear-gradient(135deg, rgba(255,253,252,0.94), rgba(251,247,240,0.75));
        border: 1px solid {BORDER};
        border-left: 4px solid var(--accent, {BURNT_ORANGE});
        border-radius: 13px;
        padding: 13px 16px 13px 18px;
        margin-bottom: 10px;
        overflow: hidden;
        transition: transform 0.16s ease, box-shadow 0.16s ease;
        box-shadow: 0 2px 8px rgba(56,40,35,0.05);
    }}

    .raic-card:hover {{
        transform: translateX(2px);
        box-shadow: 0 6px 16px rgba(56,40,35,0.10);
    }}

    .raic-index-num {{
        position: absolute;
        top: 6px;
        right: 14px;
        font-family: "Playfair Display", serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--accent, {BURNT_ORANGE});
        opacity: 0.12;
        line-height: 1;
    }}

    .raic-name {{
        position: relative;
        z-index: 1;
        color: var(--accent, {DEEP_RUST});
        font-family: "Playfair Display", serif;
        font-size: 0.98rem;
        font-weight: 700;
    }}

    .raic-score {{
        position: relative;
        z-index: 1;
        display: inline-block;
        color: {CREAM};
        background: var(--accent, {RUST});
        font-family: "Inter", sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        padding: 2px 9px;
        border-radius: 20px;
        margin: 5px 0 6px 0;
    }}

    .raic-description {{
        position: relative;
        z-index: 1;
        color: {DARK_BROWN};
        font-family: Georgia, serif;
        font-size: 0.82rem;
        line-height: 1.48;
        max-width: 92%;
    }}

    /* ---------------- DATAFRAME ---------------- */

    [data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {BORDER};
        box-shadow: 0 3px 12px rgba(56,40,35,0.07);
    }}

    /* ---------------- GET STARTED PAGE ---------------- */

    .hero-wrap {{
        position: relative;
        padding: 34px 34px 26px 34px;
        overflow: hidden;
        border-radius: 22px;
        background:
            radial-gradient(circle at 85% 0%, rgba(196,106,67,0.12), rgba(196,106,67,0) 55%),
            linear-gradient(135deg, rgba(255,253,252,0.55), rgba(231,215,195,0.35));
        border: 1px solid {BORDER};
        box-shadow: 0 10px 30px rgba(56,40,35,0.09);
    }}

    .hero-circle-1 {{
        position: absolute;
        top: -80px;
        right: -70px;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(169,79,53,0.18) 0%, rgba(169,79,53,0.0) 70%);
        z-index: 0;
    }}

    .hero-circle-2 {{
        position: absolute;
        bottom: -70px;
        left: -55px;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 1.5px solid rgba(143,63,47,0.20);
        background: transparent;
        z-index: 0;
    }}

    .hero-circle-3 {{
        position: absolute;
        top: 40%;
        right: 8%;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        border: 1px dashed rgba(196,106,67,0.30);
        z-index: 0;
    }}

    .hero-dotgrid {{
        position: absolute;
        top: 18px;
        left: 55%;
        width: 130px;
        height: 90px;
        background-image: radial-gradient(rgba(143,63,47,0.22) 1.4px, transparent 1.4px);
        background-size: 13px 13px;
        z-index: 0;
        opacity: 0.7;
    }}

    .hero-badge {{
        position: relative;
        z-index: 1;
        display: inline-block;
        font-family: "Inter", sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        color: {DEEP_RUST};
        background: rgba(196,106,67,0.12);
        border: 1px solid rgba(196,106,67,0.30);
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 14px;
    }}

    .hero-title {{
        position: relative;
        z-index: 1;
        font-size: 2.5rem;
        font-weight: 800;
        color: {DARK_BROWN};
        margin-bottom: 4px;
        font-family: "Playfair Display", Georgia, serif;
        line-height: 1.12;
    }}

    .hero-subtitle {{
        position: relative;
        z-index: 1;
        font-size: 0.92rem;
        color: {RUST};
        letter-spacing: 1.4px;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 20px;
        font-family: "Inter", sans-serif;
    }}

    .hero-intro {{
        position: relative;
        z-index: 1;
        font-size: 0.99rem;
        color: {BROWN};
        max-width: 700px;
        line-height: 1.7;
        font-family: Georgia, serif;
    }}

    .metric-card {{
        background: linear-gradient(160deg, rgba(255,253,252,0.92), rgba(251,247,240,0.68));
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 15px 17px;
        box-shadow: 0 4px 16px rgba(56,40,35,0.08);
        position: relative;
        overflow: hidden;
        min-height: 96px;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 24px rgba(56,40,35,0.13);
    }}

    .metric-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, {DEEP_RUST}, {BURNT_ORANGE});
    }}

    .metric-card::after {{
        content: "";
        position: absolute;
        top: -18px;
        right: -18px;
        width: 46px;
        height: 46px;
        border-radius: 50%;
        border: 1px solid rgba(196,106,67,0.25);
    }}

    .metric-label {{
        position: relative;
        z-index: 1;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.7px;
        text-transform: uppercase;
        color: {BROWN};
        margin-bottom: 7px;
        font-family: "Inter", sans-serif;
    }}

    .metric-value {{
        position: relative;
        z-index: 1;
        font-size: 1.75rem;
        font-weight: 700;
        color: {DEEP_RUST};
        font-family: "Playfair Display", Georgia, serif;
    }}

    .step-card {{
        background: linear-gradient(160deg, rgba(255,253,252,0.86), rgba(251,247,240,0.60));
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 17px 19px;
        box-shadow: 0 4px 16px rgba(56,40,35,0.07);
        min-height: 138px;
        position: relative;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .step-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(56,40,35,0.12);
    }}

    .step-number {{
        font-size: 1.55rem;
        font-weight: 700;
        color: {WARM_BEIGE};
        -webkit-text-stroke: 1.2px {RUST};
        margin-bottom: 5px;
        font-family: "Playfair Display", serif;
    }}

    .step-title {{
        font-size: 1.02rem;
        font-weight: 700;
        color: {DEEP_RUST};
        margin-bottom: 6px;
        font-family: "Playfair Display", serif;
    }}

    .step-text {{
        font-size: 0.84rem;
        color: {BROWN};
        line-height: 1.5;
        font-family: Georgia, serif;
    }}

    .explore-heading {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        font-weight: 700;
        color: {DARK_BROWN};
        margin-top: 30px;
        margin-bottom: 15px;
        font-family: "Playfair Display", serif;
    }}

    /* CTA style enter-dashboard button */
    div[data-testid="stButton"] > button[kind="primary"],
    .enter-btn button {{
        background: linear-gradient(135deg, {DEEP_RUST}, {RUST}) !important;
        color: {CREAM} !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.4px;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 6px 18px rgba(143,63,47,0.35) !important;
        transition: all 0.18s ease !important;
        font-family: "Inter", sans-serif !important;
    }}

    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(143,63,47,0.42) !important;
    }}

    .footer-line {{
        color: {BROWN};
        font-size: 0.78rem;
        text-align: left;
        font-family: "Inter", sans-serif;
        letter-spacing: 0.2px;
        opacity: 0.85;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = r"C:\Users\MY-HP\Desktop\Human_AI_Collaboration\SPSS Data(1).sav"

df, meta = pyreadstat.read_sav(DATA_PATH)
df.attrs = {}

original_columns = list(df.columns)
original_variable_count = len(original_columns)


# ============================================================
# SPSS VALUE LABELS
# ============================================================

value_labels = meta.variable_value_labels


def convert_value_labels(series, variable):

    labels = value_labels.get(variable, {})

    if not labels:
        return series.astype(str)

    def convert(value):

        if pd.isna(value):
            return "Missing"

        if value in labels:
            return str(labels[value])

        try:
            number = float(value)

            if number in labels:
                return str(labels[number])

            if number.is_integer() and int(number) in labels:
                return str(labels[int(number)])

        except Exception:
            pass

        return str(value)

    return series.apply(convert)


# ============================================================
# CREATE READABLE LABEL COLUMNS
# ============================================================

label_variables = [
    "Age",
    "Education",
    "Occupation",
    "AI_Experience",
    "AI_Usage",
    "Preferred_AI",
    "Primary_AI",
    "Prompt_Confidence"
]

for variable in label_variables:

    if variable in df.columns:

        df[f"{variable}_Label"] = convert_value_labels(
            df[variable],
            variable
        )


# ============================================================
# FRIENDLY FILTER NAMES
# ============================================================

display_names = {
    "Age": "Age",
    "Education": "Education",
    "Occupation": "Occupation",
    "AI_Experience": "AI Experience",
    "AI_Usage": "AI Usage Frequency",
    "Preferred_AI": "Preferred AI",
    "Primary_AI": "Primary AI Purpose",
    "Prompt_Confidence": "Prompt Confidence"
}


# ============================================================
# CORRECT LOGICAL ORDERS
# ============================================================

age_order = [
    "Under 18", "18–24", "18-24", "25–34", "25-34",
    "35–44", "35-44", "45+"
]

education_order = [
    "School", "UG", "Undergraduate", "PG", "Postgraduate", "Others"
]

occupation_order = [
    "Student", "Academic", "Employed", "Self-employed",
    "Self Employed", "Not in Workforce", "Others"
]

experience_order = [
    "<6m", "<6 months", "Less than 6 months",
    "6m–1y", "6m-1y", "6 months–1 year", "6 months-1 year",
    "1–2y", "1-2y", "1–2 years", "1-2 years",
    ">2y", ">2 years", "More than 2 years"
]

usage_order = [
    "Rarely", "Few/month", "A few times per month",
    "Few/week", "A few times per week", "Once/day", "Once a day",
    "Several/day", "Several times a day"
]

preferred_ai_order = [
    "ChatGPT", "Gemini", "Copilot", "Claude",
    "Perplexity", "Meta", "Meta AI", "Others"
]

purpose_order = [
    "Academic", "Professional Productivity",
    "Technical", "Personal/Creative", "Others"
]

prompt_order = [
    "Very Low", "Low", "Moderate", "High", "Very High"
]


# ============================================================
# FUNCTION: ORDER VALUES
# ============================================================

def get_ordered_values(series, preferred_order):

    values = [
        str(x)
        for x in series.dropna().unique()
        if str(x) != "Missing"
    ]

    ordered = []

    for item in preferred_order:

        if item in values:
            ordered.append(item)

    for item in values:

        if item not in ordered:
            ordered.append(item)

    return ordered


# ============================================================
# RAIC CATEGORY
# ============================================================

def get_raic_category(score):

    if pd.isna(score):
        return "Missing"

    score = float(score)

    if 7 <= score <= 13:
        return "AI-Dependent User"

    if 14 <= score <= 20:
        return "Developing AI Collaborator"

    if 21 <= score <= 27:
        return "Balanced AI Collaborator"

    if 28 <= score <= 35:
        return "Responsible AI Collaborator"

    return "Outside Range"


df["RAIC_Category_Label"] = df["SUMRAIC"].apply(
    get_raic_category
)

RAIC_ORDER = [
    "AI-Dependent User",
    "Developing AI Collaborator",
    "Balanced AI Collaborator",
    "Responsible AI Collaborator"
]


# ============================================================
# GET STARTED — STANDALONE LANDING PAGE
# ============================================================
#
# The landing page is a completely separate screen. It renders with no
# sidebar, no filters, no top navigation and no dashboard content. Only
# once the user presses "GET STARTED →" does the real dashboard appear.

if "started" not in st.session_state:
    st.session_state.started = False


def render_get_started_page():

    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-circle-1"></div>
            <div class="hero-circle-2"></div>
            <div class="hero-circle-3"></div>
            <div class="hero-dotgrid"></div>
            <div class="hero-badge">Human + AI · Behavioural Research</div>
            <div class="hero-title">Human–AI Collaboration and<br>Responsible AI Usage</div>
            <div class="hero-subtitle">A Behavioural Analytics Study</div>
            <div class="hero-intro">
                This dashboard presents behavioural insights into how individuals
                collaborate with AI — how they use AI-generated suggestions,
                evaluate outputs, verify information, and maintain independent
                judgement. It combines questionnaire-based behavioural analytics
                with statistical analysis to measure and support responsible,
                well-governed AI usage.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    m1, m2, m3, m4 = st.columns(4)

    metric_data = [
        ("Valid Respondents", "267"),
        ("Questionnaire Items", "15"),
        ("Behavioural Items", "Q9–Q15"),
        ("RAIC Index", "0–100"),
    ]

    for col, (label, value) in zip([m1, m2, m3, m4], metric_data):

        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.write("")

    b_left, b_center, b_right = st.columns([2.2, 1.6, 2.2])

    with b_center:

        if st.button(
            "GET STARTED →",
            key="get_started_btn",
            type="primary",
            use_container_width=True
        ):
            st.session_state.started = True
            st.rerun()

    st.write("")
    st.markdown(
        """
        <p style="text-align:center; color:#654A40; font-size:0.8rem;
                  font-family:'Inter', sans-serif; letter-spacing:0.3px;">
            Enter the dashboard to explore Home, AI Usage, RAIC Analysis,
            Relationships and Data.
        </p>
        """,
        unsafe_allow_html=True
    )


if not st.session_state.started:

    render_get_started_page()
    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown(
    '<div class="sidebar-heading">Dashboard Filters</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown(
    '<div class="sidebar-sub">Explore respondent groups</div>',
    unsafe_allow_html=True
)

filter_information = [
    ("Age", age_order),
    ("Education", education_order),
    ("Occupation", occupation_order),
    ("AI_Experience", experience_order),
    ("AI_Usage", usage_order),
    ("Preferred_AI", preferred_ai_order),
    ("Primary_AI", purpose_order),
    ("Prompt_Confidence", prompt_order)
]


# ============================================================
# REMOVE ALL FILTERS — ON TOP
# ============================================================

if st.sidebar.button(
    "✕  Remove All Filters",
    key="remove_all_filters",
    use_container_width=True
):

    for variable, _ in filter_information:
        st.session_state[f"filter_{variable}"] = []

    st.rerun()

st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-section-label">Demographics</div>',
    unsafe_allow_html=True
)


# ============================================================
# MULTISELECT DROPDOWN FILTERS
# ============================================================

filters = {}

demographic_vars = {"Age", "Education", "Occupation"}
behaviour_vars = {"AI_Experience", "AI_Usage", "Preferred_AI", "Primary_AI", "Prompt_Confidence"}

for variable, preferred_order in filter_information:

    label_column = f"{variable}_Label"

    if label_column not in df.columns:
        continue

    if variable == "AI_Experience":
        st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.sidebar.markdown(
            '<div class="sidebar-section-label">AI Behaviour</div>',
            unsafe_allow_html=True
        )

    available = get_ordered_values(
        df[label_column],
        preferred_order
    )

    selected = st.sidebar.multiselect(
        display_names[variable],
        options=available,
        default=None,
        placeholder="Select options...",
        key=f"filter_{variable}"
    )

    filters[variable] = selected


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

for variable, selected in filters.items():

    label_column = f"{variable}_Label"

    if selected:
        filtered_df = filtered_df[
            filtered_df[label_column].isin(selected)
        ]


# ============================================================
# NAVIGATION
# ============================================================

st.markdown(
    """
    <div class="app-title-band">
        <div class="app-eyebrow">Behavioural Analytics Platform</div>
        <h1>Human–AI Collaboration Behaviour</h1>
        <div class="app-title-rule"></div>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.radio(
    "Dashboard Navigation",
    [
        "Home",
        "AI Usage",
        "RAIC Analysis",
        "Relationships",
        "Data"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def inference(text):

    st.markdown(
        f"""
        <div class="inference-box">
            <div class="inference-title">Inference</div>
            <div class="inference-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_heading(text):

    st.markdown(
        f"""
        <div class="section-heading">
            <span class="section-marker"></span>
            <h3>{text}</h3>
        </div>
        <div class="section-rule-full"></div>
        """,
        unsafe_allow_html=True
    )


def page_header(title, subtitle=""):

    st.markdown(
        f"""
        <div class="page-header-wrap">
            <div class="page-header-shape"></div>
            <div class="page-header-eyebrow">{subtitle}</div>
            <div class="page-header-title">{title}</div>
            <div class="page-header-rule"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def kpi_row(items):
    """items: list of (label, value) tuples rendered as premium KPI cards."""

    cols = st.columns(len(items))

    for col, (label, value) in zip(cols, items):

        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def show_chart(fig):

    left, center, right = st.columns([1.2, 4.8, 1.2])

    with center:
        st.pyplot(fig, use_container_width=False)

    plt.close(fig)


def style_axes(ax):

    ax.set_facecolor(WHITE)

    for spine in ax.spines.values():
        spine.set_color(BORDER)

    ax.tick_params(axis="both", colors=DARK_BROWN, labelsize=8)
    ax.title.set_color(DARK_BROWN)
    ax.xaxis.label.set_color(DARK_BROWN)
    ax.yaxis.label.set_color(DARK_BROWN)


def category_cards():

    section_heading("RAIC Behaviour Categories")

    descriptions = {
        "AI-Dependent User":
            "Relatively high dependence on AI, with limited human contribution, evaluation, verification, or independent judgement.",

        "Developing AI Collaborator":
            "Some human involvement is present, but prompt refinement, critical evaluation, verification, and independent judgement can be strengthened.",

        "Balanced AI Collaborator":
            "AI is used as a supporting tool while the individual contributes ideas, evaluates outputs, verifies information, and maintains independent judgement.",

        "Responsible AI Collaborator":
            "Strong Human-AI collaboration with active interaction, critical evaluation, verification, independent judgement, and responsible decision-making."
    }

    ranges = {
        "AI-Dependent User": "RAW SCORE 7–13",
        "Developing AI Collaborator": "RAW SCORE 14–20",
        "Balanced AI Collaborator": "RAW SCORE 21–27",
        "Responsible AI Collaborator": "RAW SCORE 28–35"
    }

    for index, category in enumerate(RAIC_ORDER, start=1):

        accent = RAIC_ACCENTS.get(category, BURNT_ORANGE)

        st.markdown(
            f"""
            <div class="raic-card" style="--accent:{accent};">
                <div class="raic-index-num">{index:02d}</div>
                <div class="raic-name">{category}</div>
                <div class="raic-score">{ranges[category]}</div>
                <div class="raic-description">
                    {descriptions[category]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# HOME
# ============================================================

if page == "Home":

    page_header("Project Overview", "Getting Oriented")

    st.write(
        "This project examines Human-AI collaboration behaviour by analysing "
        "how individuals use AI, interact with AI-generated suggestions, "
        "evaluate outputs, verify information, and maintain independent judgement."
    )

    st.write(
        "The platform uses questionnaire-based behavioural analytics, "
        "Python analysis, and Streamlit visualisation to measure and improve "
        "responsible AI usage."
    )

    section_heading("Project Objective")

    st.write(
        "To measure and analyse Human-AI collaboration behaviour across "
        "different demographic and AI-usage groups and provide behavioural "
        "insights for improving responsible AI usage."
    )

    section_heading("Dataset Overview")

    if len(filtered_df) > 0:
        mean_raic_display = f"{filtered_df['RAIC'].mean():.2f}"
        mean_raw_display = f"{filtered_df['SUMRAIC'].mean():.2f}/35"
    else:
        mean_raic_display = "—"
        mean_raw_display = "—"

    kpi_row([
        ("Respondents", len(filtered_df)),
        ("Original Variables", original_variable_count),
        ("Mean RAIC", mean_raic_display),
        ("Mean Raw Score", mean_raw_display),
    ])

    st.write("")
    section_heading("RAIC Behaviour Distribution")

    counts = (
        filtered_df["RAIC_Category_Label"]
        .value_counts()
        .reindex(RAIC_ORDER, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6.0, 3.6), dpi=110)

    bars = ax.bar(
        counts.index,
        counts.values,
        color=[WARM_BEIGE, BURNT_ORANGE, RUST, DEEP_RUST],
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("RAIC Behaviour Distribution", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Respondents", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            str(int(bar.get_height())),
            ha="center", va="bottom", fontsize=8,
            fontweight="bold", color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    if len(filtered_df) > 0:
        dominant = filtered_df["RAIC_Category_Label"].value_counts().idxmax()
        dominant_count = filtered_df["RAIC_Category_Label"].value_counts().max()

        inference(
            f"The most common RAIC behaviour in the current selection is "
            f"<b>{dominant}</b>, representing {dominant_count} respondents "
            f"({dominant_count / len(filtered_df) * 100:.1f}%). "
            f"This indicates the dominant behavioural profile within the "
            f"selected respondent group."
        )

    section_heading("How RAIC Is Calculated")

    st.write(
        "RAIC is based on the seven behavioural items Q9–Q15, with each "
        "item scored from 1 to 5."
    )

    st.write(
        "The seven responses are added to obtain a raw score ranging from "
        "7 to 35. The raw score is then converted into a 0–100 index by "
        "expressing the respondent's score above the minimum possible score "
        "of 7 relative to the total scoring range of 28 points."
    )

    st.write(
        "A raw score of 7 therefore corresponds to 0, while a raw score "
        "of 35 corresponds to 100."
    )

    st.write(
        "The RAIC category is assigned using the raw Q9–Q15 total."
    )

    st.write(
        "Example: a raw score of 25 corresponds to a RAIC index of "
        "64.29 and falls under the **Balanced AI Collaborator** category."
    )

    category_cards()


# ============================================================
# AI USAGE
# ============================================================

elif page == "AI Usage":

    page_header("AI Usage and Experience", "Usage Patterns")

    st.write(
        "This section presents the distribution of AI usage frequency, "
        "preferred AI tools, and AI experience among respondents."
    )

    section_heading("AI Usage Frequency")

    data = (
        filtered_df["AI_Usage_Label"]
        .value_counts()
        .reindex(
            get_ordered_values(filtered_df["AI_Usage_Label"], usage_order),
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=110)

    bars = ax.bar(
        data.index, data.values,
        color=RUST,
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("AI Usage Frequency", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Respondents", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            int(bar.get_height()),
            ha="center", va="bottom", fontsize=8, color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    if len(filtered_df) > 0:

        inference(
            "In the full dataset, 47.9% of respondents report using AI "
            "several times a day and 26.6% report using it a few times "
            "per week. The pattern indicates that AI is regularly integrated "
            "into the activities of a substantial proportion of respondents."
        )

    section_heading("Preferred AI Tools")

    data = (
        filtered_df["Preferred_AI_Label"]
        .value_counts()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=110)

    bars = ax.bar(
        data.index, data.values,
        color=BURNT_ORANGE,
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("Preferred AI Tools", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Respondents", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            int(bar.get_height()),
            ha="center", va="bottom", fontsize=8, color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    if len(filtered_df) > 0:
        tool_counts = filtered_df["Preferred_AI_Label"].value_counts()
        top_tool = tool_counts.index[0]
        top_count = tool_counts.iloc[0]

        inference(
            f"{top_tool} is the most preferred AI tool in the current "
            f"selection, used by {top_count} respondents "
            f"({top_count / len(filtered_df) * 100:.1f}%). "
            f"The result describes tool preference within the sample and "
            f"does not indicate comparative tool performance."
        )

    section_heading("AI Experience")

    experience_values = get_ordered_values(
        filtered_df["AI_Experience_Label"], experience_order
    )

    data = (
        filtered_df["AI_Experience_Label"]
        .value_counts()
        .reindex(experience_values, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=110)

    bars = ax.bar(
        data.index, data.values,
        color=RUST,
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("AI Experience Distribution", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Respondents", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            int(bar.get_height()),
            ha="center", va="bottom", fontsize=8, color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "The full dataset contains a substantial proportion of respondents "
        "with sustained AI experience. The 1–2 year and more-than-2-year "
        "groups together account for 58.8% of respondents, providing "
        "representation from users with longer exposure to AI tools."
    )


# ============================================================
# RAIC ANALYSIS
# ============================================================

elif page == "RAIC Analysis":

    page_header("Responsible AI Collaboration Index", "Core Metric")

    st.write(
        "RAIC summarises behavioural performance across Human-AI "
        "collaboration, critical evaluation, verification, independence, "
        "and responsible decision-making."
    )

    section_heading("RAIC Summary")

    if len(filtered_df) > 0:

        mean_raic = filtered_df["RAIC"].mean()
        mean_raw = filtered_df["SUMRAIC"].mean()
        median_raic = filtered_df["RAIC"].median()

        dominant = (
            filtered_df["RAIC_Category_Label"]
            .value_counts()
            .idxmax()
        )

        kpi_row([
            ("Mean RAIC Index", f"{mean_raic:.2f}"),
            ("Mean Raw Score", f"{mean_raw:.2f} / 35"),
            ("Median RAIC", f"{median_raic:.2f}"),
        ])

        accent = RAIC_ACCENTS.get(dominant, RUST)

        st.markdown(
            f"""
            <div class="raic-card" style="--accent:{accent}; margin-top:12px;">
                <div class="raic-name">Dominant Behaviour</div>
                <div class="raic-description">
                    <b>{dominant}</b> is the most common RAIC category in
                    the current respondent selection.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    section_heading("RAIC Distribution")

    fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=110)

    ax.hist(
        filtered_df["RAIC"].dropna(),
        bins=12,
        color=BURNT_ORANGE,
        edgecolor=DARK_BROWN,
        linewidth=0.8
    )

    ax.set_title("Distribution of RAIC Index", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_xlabel("RAIC Index (0–100)", color=DARK_BROWN)
    ax.set_ylabel("Respondents", color=DARK_BROWN)

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    if len(filtered_df) > 0:
        inference(
            f"The full dataset has a mean raw Q9–Q15 score of "
            f"{df['SUMRAIC'].mean():.2f}/35, corresponding to an average "
            f"RAIC index of {df['RAIC'].mean():.2f}. The distribution shows "
            f"variation in responsible Human-AI collaboration behaviour "
            f"across respondents."
        )

    section_heading("RAIC Score Spread")

    fig, ax = plt.subplots(figsize=(6.2, 3.3), dpi=110)

    ax.boxplot(
        filtered_df["RAIC"].dropna(),
        vert=False,
        patch_artist=True,
        boxprops=dict(facecolor=LIGHT_BEIGE, edgecolor=DARK_BROWN),
        medianprops=dict(color=DEEP_RUST, linewidth=2),
        whiskerprops=dict(color=RUST),
        capprops=dict(color=RUST)
    )

    ax.set_title("RAIC Box Plot", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_xlabel("RAIC Index (0–100)", color=DARK_BROWN)
    ax.set_yticks([])

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "The box plot shows the central tendency and spread of RAIC scores. "
        "It provides a compact view of the median, middle 50% of observations, "
        "overall variability, and potential extreme observations."
    )

    section_heading("Mean RAIC Across AI Experience")

    exp_order_actual = get_ordered_values(
        filtered_df["AI_Experience_Label"], experience_order
    )

    means = (
        filtered_df
        .groupby("AI_Experience_Label", observed=False)["RAIC"]
        .mean()
        .reindex(exp_order_actual)
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=110)

    bars = ax.bar(
        means.index, means.values,
        color=RUST,
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("Mean RAIC by AI Experience", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Mean RAIC Index", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}",
            ha="center", va="bottom", fontsize=8, color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "Mean RAIC differs across AI experience groups, indicating descriptive "
        "variation in responsible Human-AI collaboration behaviour. The "
        "difference should be interpreted together with the relevant statistical "
        "test rather than from the bar heights alone."
    )

    section_heading("Mean RAIC Across AI Usage Frequency")

    usage_order_actual = get_ordered_values(
        filtered_df["AI_Usage_Label"], usage_order
    )

    means = (
        filtered_df
        .groupby("AI_Usage_Label", observed=False)["RAIC"]
        .mean()
        .reindex(usage_order_actual)
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=110)

    bars = ax.bar(
        means.index, means.values,
        color=BURNT_ORANGE,
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("Mean RAIC by AI Usage Frequency", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Mean RAIC Index", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}",
            ha="center", va="bottom", fontsize=8, color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "The mean RAIC values vary across AI usage-frequency groups. "
        "This provides a descriptive comparison of responsible AI behaviour "
        "across different levels of AI usage, while statistical testing is "
        "required to determine whether the observed differences are significant."
    )

    section_heading("Mean RAIC Across Prompt Confidence")

    prompt_order_actual = get_ordered_values(
        filtered_df["Prompt_Confidence_Label"], prompt_order
    )

    means = (
        filtered_df
        .groupby("Prompt_Confidence_Label", observed=False)["RAIC"]
        .mean()
        .reindex(prompt_order_actual)
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=110)

    bars = ax.bar(
        means.index, means.values,
        color=SOFT_TAUPE,
        edgecolor=DARK_BROWN,
        linewidth=0.7
    )

    ax.set_title("Mean RAIC by Prompt Confidence", fontsize=12.5,
                 fontweight="bold", color=DARK_BROWN)
    ax.set_ylabel("Mean RAIC Index", color=DARK_BROWN)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}",
            ha="center", va="bottom", fontsize=8, color=DARK_BROWN
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "Mean RAIC varies across prompt-confidence levels. At the component "
        "level, Prompt Confidence was statistically significant for "
        "Co-Creative Engagement, Critical Appraisal & Verification, and "
        "Cognitive Autonomy, indicating that prompt confidence is an important "
        "behavioural factor within the framework."
    )

    category_cards()


# ============================================================
# RELATIONSHIPS
# ============================================================

elif page == "Relationships":

    page_header("Behavioural Relationships", "Cross-Cutting Analysis")

    st.write(
        "This section examines the relationship between AI usage frequency, "
        "RAIC behavioural categories, and the three major behavioural components."
    )

    section_heading("RAIC Categories Across AI Usage Frequency")

    usage_order_actual = get_ordered_values(
        filtered_df["AI_Usage_Label"], usage_order
    )

    cross_tab = pd.crosstab(
        filtered_df["AI_Usage_Label"],
        filtered_df["RAIC_Category_Label"],
        normalize="index"
    ) * 100

    cross_tab = cross_tab.reindex(
        index=usage_order_actual,
        columns=RAIC_ORDER,
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.9), dpi=110)

    bottom = np.zeros(len(cross_tab))

    category_colours = [WARM_BEIGE, BURNT_ORANGE, RUST, DEEP_RUST]

    for i, category in enumerate(RAIC_ORDER):

        ax.bar(
            cross_tab.index,
            cross_tab[category],
            bottom=bottom,
            label=category,
            color=category_colours[i],
            edgecolor=WHITE,
            linewidth=0.5
        )

        bottom += cross_tab[category].values

    ax.set_title(
        "RAIC Categories Across AI Usage Frequency",
        fontsize=12.5,
        fontweight="bold",
        color=DARK_BROWN
    )

    ax.set_ylabel("Percentage", color=DARK_BROWN)
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=18, labelsize=8)

    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.22),
        ncol=2,
        frameon=False,
        fontsize=7.5
    )

    for text in legend.get_texts():
        text.set_color(DARK_BROWN)

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "The 100% stacked chart compares the proportion of RAIC behavioural "
        "categories within each AI usage-frequency group. It helps identify "
        "differences in group composition without implying that frequency of "
        "AI use causes a particular RAIC category."
    )

    section_heading("RAIC and Critical Appraisal & Verification")

    fig, ax = plt.subplots(figsize=(6.2, 3.9), dpi=110)

    ax.scatter(
        filtered_df["RAIC"],
        filtered_df["CAV"],
        s=27,
        alpha=0.68,
        color=BURNT_ORANGE,
        edgecolors=DARK_BROWN,
        linewidths=0.45
    )

    ax.set_title(
        "RAIC vs Critical Appraisal & Verification",
        fontsize=12.5,
        fontweight="bold",
        color=DARK_BROWN
    )

    ax.set_xlabel("RAIC Index", color=DARK_BROWN)
    ax.set_ylabel("CAV Score", color=DARK_BROWN)

    full_corr = df[["RAIC", "CAV"]].dropna()

    if len(full_corr) > 1:

        r = full_corr["RAIC"].corr(full_corr["CAV"])

        ax.text(
            0.04, 0.93, f"r = {r:.3f}",
            transform=ax.transAxes,
            fontsize=9,
            fontweight="bold",
            color=DARK_BROWN,
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor=LIGHT_BEIGE,
                edgecolor=BORDER
            )
        )

    style_axes(ax)
    plt.tight_layout()

    with st.container(border=True):
        show_chart(fig)

    inference(
        "Critical Appraisal & Verification has a very strong positive "
        "relationship with RAIC. In the full dataset, Pearson's correlation "
        "is r = 0.896. Respondents with stronger critical appraisal and "
        "verification behaviour therefore tend to have higher RAIC scores. "
        "This is an association and does not establish causation."
    )

    section_heading("Component Correlation Matrix")

    correlation_matrix = (
        filtered_df[["CCE", "CAV", "CAU"]]
        .corr()
        .round(3)
    )

    correlation_matrix = correlation_matrix.rename(
        index={
            "CCE": "Co-Creative Engagement",
            "CAV": "Critical Appraisal & Verification",
            "CAU": "Cognitive Autonomy"
        },
        columns={
            "CCE": "Co-Creative Engagement",
            "CAV": "Critical Appraisal & Verification",
            "CAU": "Cognitive Autonomy"
        }
    )

    with st.container(border=True):
        st.dataframe(correlation_matrix, use_container_width=True)

    inference(
        "The three RAIC components are positively related. In the full dataset, "
        "Co-Creative Engagement and Critical Appraisal & Verification show "
        "r = 0.642, Co-Creative Engagement and Cognitive Autonomy show "
        "r = 0.445, while Critical Appraisal & Verification and Cognitive "
        "Autonomy show the strongest component relationship at r = 0.674."
    )


# ============================================================
# DATA
# ============================================================

elif page == "Data":

    page_header("Filtered Dataset", "Raw Records")

    st.write(
        "The table displays the selected respondents using readable category "
        "labels rather than SPSS numeric codes."
    )

    display_df = filtered_df.copy()

    replacement_columns = [
        "Age", "Education", "Occupation", "AI_Experience",
        "AI_Usage", "Preferred_AI", "Primary_AI", "Prompt_Confidence"
    ]

    for variable in replacement_columns:

        label_column = f"{variable}_Label"

        if label_column in display_df.columns:
            display_df[variable] = display_df[label_column]

    helper_columns = [
        "Age_Label", "Education_Label", "Occupation_Label",
        "AI_Experience_Label", "AI_Usage_Label",
        "Preferred_AI_Label", "Primary_AI_Label",
        "Prompt_Confidence_Label", "RAIC_Category_Label"
    ]

    display_df = display_df.drop(
        columns=[col for col in helper_columns if col in display_df.columns]
    )

    with st.container(border=True):
        st.dataframe(
            display_df,
            use_container_width=True,
            height=500
        )

    section_heading("Dataset Information")

    kpi_row([
        ("Filtered Respondents", len(filtered_df)),
        ("Original Variables", original_variable_count),
        ("Behavioural Items", "Q9–Q15"),
    ])

    st.write("")
    section_heading("RAIC Reference")

    st.write(
        "Q9–Q15 → Raw Score (7–35) → RAIC Index (0–100) → "
        "RAIC Behaviour Category"
    )

    category_cards()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <p class="footer-line">
        Human–AI Collaboration Behaviour &nbsp;|&nbsp; Behavioural Analytics Dashboard
    </p>
    """,
    unsafe_allow_html=True
)