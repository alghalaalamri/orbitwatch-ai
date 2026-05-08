import streamlit as st
from PIL import Image
import numpy as np
import cv2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OrbitWatch AI",
    page_icon=None,
    layout="wide"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600&family=Orbitron:wght@400;600;900&display=swap');

/* ─── CSS VARIABLES ─────────────────────────────── */
:root {
    --void:      #0b1120;
    --surface:   #111827;
    --panel:     #172554;

    --border:    rgba(125, 170, 220, 0.16);
    --border-hi: rgba(125, 170, 220, 0.34);

    --accent:    #7dd3fc;
    --accent-lo: rgba(125, 211, 252, 0.32);

    --text-hi:   #e6f1ff;
    --text-mid:  rgba(220, 232, 245, 0.78);
    --text-lo:   rgba(170, 195, 220, 0.55);

    --good:      #4ade80;
    --warn:      #fbbf24;
    --danger:    #fb7185;
}

/* ─── BASE ───────────────────────────────────────── */
.stApp {
    background: linear-gradient(
    180deg,
    #0b1120 0%,
    #111827 100%
);
    color: var(--text-hi);
    font-family: 'Rajdhani', sans-serif;
}

#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1280px; }

/* ─── NOISE GRAIN ────────────────────────────────── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.028'/%3E%3C/svg%3E");
    background-size: 200px 200px;
    pointer-events: none;
    z-index: 999;
}

/* ─── NEBULA DEPTH ───────────────────────────────── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 15% 20%, rgba(20, 55, 100, 0.18) 0%, transparent 70%),
        radial-gradient(ellipse 50% 60% at 85% 75%, rgba(10, 35, 75, 0.14) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ─── HERO ───────────────────────────────────────── */
.hero {
    padding: 40px 0 36px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
}

.hero-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.28em;
    color: var(--text-lo);
    margin-bottom: 16px;
    text-transform: uppercase;
}

.hero-wordmark {
    display: flex;
    align-items: baseline;
    margin-bottom: 14px;
}

.hero-word-orbit {
    font-family: 'Orbitron', monospace;
    font-size: 3.4rem;
    font-weight: 900;
    color: var(--text-hi);
    letter-spacing: 0.05em;
    line-height: 1;
    text-shadow: 0 0 60px rgba(91, 163, 217, 0.18);
}

.hero-word-watch {
    font-family: 'Orbitron', monospace;
    font-size: 3.4rem;
    font-weight: 400;
    color: var(--accent);
    letter-spacing: 0.05em;
    line-height: 1;
    text-shadow: 0 0 40px rgba(91, 163, 217, 0.28);
}

.hero-rule {
    width: 52px;
    height: 1px;
    background: linear-gradient(90deg, var(--accent), transparent);
    margin-bottom: 14px;
}

.hero-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    font-weight: 300;
    color: var(--text-mid);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* ─── TELEMETRY RAIL ─────────────────────────────── */
.telem-rail {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border: 1px solid var(--border);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 40px;
    background: var(--surface);
}

.telem-cell {
    padding: 16px 22px;
    border-right: 1px solid var(--border);
    position: relative;
}
.telem-cell:last-child { border-right: none; }

.telem-cell::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, var(--accent-lo), transparent 80%);
}

.telem-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.25em;
    color: var(--text-lo);
    text-transform: uppercase;
    margin-bottom: 6px;
}

.telem-value {
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-hi);
    letter-spacing: 0.06em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.pulse {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--good);
    box-shadow: 0 0 6px var(--good);
    flex-shrink: 0;
    animation: blink 2.4s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.15; }
}

/* ─── UPLOAD ─────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border-radius: 2px !important;
    padding: 22px !important;
    border: 1px solid var(--border) !important;
}

[data-testid="stFileUploader"] label p {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    color: var(--text-mid) !important;
    letter-spacing: 0.12em !important;
}

/* ─── BUTTONS ────────────────────────────────────── */
.stButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 2px !important;
    padding: 9px 26px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    transition: background 0.18s, box-shadow 0.18s !important;
}

.stButton > button:hover {
    background: rgba(91, 163, 217, 0.07) !important;
    box-shadow: 0 0 18px rgba(91, 163, 217, 0.10) !important;
    color: var(--text-hi) !important;
}

/* ─── IMAGES ─────────────────────────────────────── */
[data-testid="stImage"] img {
    border-radius: 2px !important;
    border: 1px solid var(--border) !important;
    display: block;
}
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(125,170,220,0.18) !important;
    border-radius: 2px !important;
    padding: 28px !important;
    transition: 0.2s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(125,170,220,0.28) !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #d6e8f5 !important;
}

[data-testid="stFileUploaderDropzone"] small {
    color: rgba(220,232,245,0.72) !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: rgba(255,255,255,0.04) !important;
    color: #d6e8f5 !important;
    border: 1px solid rgba(125,170,220,0.18) !important;
}
[data-testid="stCaptionContainer"] p {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.58rem !important;
    color: var(--text-lo) !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    margin-top: 8px !important;
}

/* ─── METRICS ────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--panel) !important;
    border-radius: 2px !important;
    padding: 20px 22px !important;
    border: 1px solid var(--border) !important;
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-lo), transparent);
}

[data-testid="stMetricLabel"] > div {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.56rem !important;
    letter-spacing: 0.22em !important;
    color: var(--text-lo) !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] > div {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
    color: var(--text-hi) !important;
    letter-spacing: 0.04em !important;
}

/* ─── STATUS CARDS ───────────────────────────────── */
.status-card {
    padding: 22px 28px;
    border-radius: 2px;
    border: 1px solid;
    position: relative;
    overflow: hidden;
    margin-top: 4px;
}

.status-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
}

.sc-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.sc-label::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

.sc-body {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.7;
    color: var(--text-mid);
    letter-spacing: 0.04em;
}

.sc-good  { background: rgba(20,50,30,0.35);  border-color: rgba(74,222,128,0.15); }
.sc-good::before  { background: var(--good); }
.sc-good  .sc-label { color: var(--good); }
.sc-good  .sc-label::before { background: var(--good); box-shadow: 0 0 6px var(--good); }

.sc-warn  { background: rgba(50,35,10,0.35);  border-color: rgba(245,158,11,0.15); }
.sc-warn::before  { background: var(--warn); }
.sc-warn  .sc-label { color: var(--warn); }
.sc-warn  .sc-label::before { background: var(--warn); box-shadow: 0 0 6px var(--warn); }

.sc-danger { background: rgba(50,12,12,0.35); border-color: rgba(248,113,113,0.15); }
.sc-danger::before { background: var(--danger); }
.sc-danger .sc-label { color: var(--danger); }
.sc-danger .sc-label::before { background: var(--danger); box-shadow: 0 0 6px var(--danger); animation: blink 1.4s ease-in-out infinite; }

/* ─── HEADINGS + BODY ────────────────────────────── */
h2 {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: var(--accent) !important;
    letter-spacing: 0.26em !important;
    text-transform: uppercase !important;
    border: none !important;
    margin-top: 40px !important;
    margin-bottom: 16px !important;
}

h3 {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: var(--text-lo) !important;
    letter-spacing: 0.28em !important;
    text-transform: uppercase !important;
    margin-top: 36px !important;
    margin-bottom: 12px !important;
}

p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    color: var(--text-mid) !important;
    line-height: 1.8 !important;
    letter-spacing: 0.03em !important;
}

/* ─── CODE BLOCK ─────────────────────────────────── */
pre, code {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--accent) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.78rem !important;
    line-height: 2.0 !important;
    letter-spacing: 0.06em !important;
}

/* ─── DIVIDER ────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 44px 0 !important;
}

/* ─── EMPTY STATE ────────────────────────────────── */
.empty-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100px 0;
    gap: 18px;
}

.empty-crosshair {
    width: 48px;
    height: 48px;
    position: relative;
    margin-bottom: 8px;
}

.empty-crosshair::before {
    content: '';
    position: absolute;
    width: 1px; height: 100%;
    left: 50%; top: 0;
    background: var(--text-lo);
}

.empty-crosshair::after {
    content: '';
    position: absolute;
    height: 1px; width: 100%;
    top: 50%; left: 0;
    background: var(--text-lo);
}

.empty-ring {
    width: 48px; height: 48px;
    border: 1px solid var(--text-lo);
    border-radius: 50%;
    position: absolute;
    top: 0; left: 0;
}

.empty-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-lo);
    letter-spacing: 0.28em;
    text-transform: uppercase;
    text-align: center;
    line-height: 2.4;
}

/* ─── SCROLLBAR ──────────────────────────────────── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 2px; }

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">LOW EARTH ORBIT &nbsp;&middot;&nbsp; ONBOARD INFERENCE &nbsp;&middot;&nbsp; WILDFIRE DETECTION</div>
    <div class="hero-wordmark">
        <span class="hero-word-orbit">ORBIT</span><span class="hero-word-watch">WATCH</span>
    </div>
    <div class="hero-rule"></div>
    <div class="hero-sub">Real-time satellite AI &nbsp;&mdash;&nbsp; frame triage &amp; priority downlink</div>
</div>
""", unsafe_allow_html=True)

# ---------------- TELEMETRY RAIL ----------------
st.markdown("""
<div class="telem-rail">
    <div class="telem-cell">
        <div class="telem-label">Satellite ID</div>
        <div class="telem-value">DPHI-01</div>
    </div>
    <div class="telem-cell">
        <div class="telem-label">Orbit Status</div>
        <div class="telem-value"><span class="pulse"></span>ACTIVE</div>
    </div>
    <div class="telem-cell">
        <div class="telem-label">Inference Mode</div>
        <div class="telem-value">ONBOARD</div>
    </div>
    <div class="telem-cell">
        <div class="telem-label">Downlink</div>
        <div class="telem-value">LIMITED</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- IMAGE INPUT ----------------
demo_mode = st.button("LOAD DEMO SATELLITE FRAME")

uploaded_file = st.file_uploader(
    "Upload satellite image  //  jpg · jpeg · png",
    type=["jpg", "jpeg", "png"]
)

image = None

if demo_mode:
    image = Image.open("assets/wildfire_demo.jpg").convert("RGB")
elif uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

# ---------------- ANALYSIS ----------------
if image is not None:

    image_np = np.array(image)
    hsv      = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

    lower_fire = np.array([0, 50, 50])
    upper_fire = np.array([35, 255, 255])
    fire_mask  = cv2.inRange(hsv, lower_fire, upper_fire)

    gray       = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    smoke_mask = cv2.inRange(gray, 160, 240)

    fire_score  = np.sum(fire_mask  > 0) / fire_mask.size
    smoke_score = np.sum(smoke_mask > 0) / smoke_mask.size
    risk_score  = min((fire_score * 8 + smoke_score * 2) * 100, 100)

    overlay = image_np.copy()
    overlay[fire_mask  > 0] = [255, 80,  0]
    overlay[smoke_mask > 0] = [210, 210, 210]
    blended = cv2.addWeighted(image_np, 0.72, overlay, 0.28, 0)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.image(image,   caption="RAW SATELLITE FRAME", use_container_width=True)
    with col2:
        st.image(blended, caption="ANOMALY OVERLAY",     use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="medium")
    with m1:
        st.metric("Wildfire Risk", f"{risk_score:.1f}%")
    with m2:
        bandwidth = "68%" if risk_score > 25 else ("84%" if risk_score > 10 else "92%")
        st.metric("Bandwidth Saved", bandwidth)
    with m3:
        decision = "PRIORITY DOWNLINK" if risk_score > 25 else ("STORE FOR REVIEW" if risk_score > 10 else "IGNORE FRAME")
        st.metric("Satellite Decision", decision)

    st.markdown("<br>", unsafe_allow_html=True)

    if risk_score > 25:
        st.markdown("""
        <div class="status-card sc-danger">
            <div class="sc-label">HIGH-RISK ANOMALY DETECTED</div>
            <div class="sc-body">
                Thermal and spectral signature consistent with active wildfire event.<br>
                Initiating priority downlink — transmitting to ground station immediately.
            </div>
        </div>""", unsafe_allow_html=True)

    elif risk_score > 10:
        st.markdown("""
        <div class="status-card sc-warn">
            <div class="sc-label">MODERATE ANOMALY — REVIEW QUEUED</div>
            <div class="sc-body">
                Possible early-stage thermal event detected.<br>
                Frame stored onboard and flagged for next scheduled downlink window.
            </div>
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="status-card sc-good">
            <div class="sc-label">NOMINAL — FRAME SUPPRESSED</div>
            <div class="sc-body">
                No significant thermal or smoke signature detected.<br>
                Frame filtered onboard. Bandwidth conserved.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("## Why onboard inference matters")
    st.markdown("""
    Satellites capture continuous imagery across thousands of kilometers per orbit cycle.
    Transmitting every frame to Earth is bandwidth-prohibitive and operationally expensive.
    OrbitWatch runs the full detection pipeline directly in orbit — only frames with confirmed
    anomaly signatures are downlinked, reducing transmission load by up to 90%.
    """)

    

# ---------------- EMPTY STATE ----------------
else:
    st.markdown("""
    <div class="empty-wrap">
        <div class="empty-crosshair">
            <div class="empty-ring"></div>
        </div>
        <div class="empty-label">
            AWAITING SATELLITE IMAGERY<br>
            LOAD DEMO FRAME OR UPLOAD A THERMAL IMAGE
        </div>
    </div>
    """, unsafe_allow_html=True)