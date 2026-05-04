import streamlit as st
import random
import time
from datetime import datetime, timezone

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Fermah Protocol Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  (dark cyber theme, mobile-first)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── reset & base ── */
:root {
  --green:  #00ffa0;
  --blue:   #00c8ff;
  --dark:   #05050a;
  --card:   #0a0a14;
  --card2:  #0d0d1a;
  --border: rgba(255,255,255,0.07);
  --border-green: rgba(0,255,160,0.2);
  --text:   rgba(255,255,255,0.85);
  --muted:  rgba(255,255,255,0.35);
}

html, body, .stApp {
  background: var(--dark) !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* grid background */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,255,160,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,160,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--dark); }
::-webkit-scrollbar-thumb { background: rgba(0,255,160,0.2); border-radius: 2px; }

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1300px !important; }

/* ── TOP HEADER ── */
.dash-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  padding: 14px 24px;
  background: rgba(5,5,10,0.92);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 24px;
}
.logo {
  display: flex; align-items: center; gap: 10px;
  font-family: 'Syne', sans-serif; font-weight: 800; font-size: 20px; color:#fff;
}
.logo-pi {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--green), var(--blue));
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 17px; font-weight: 900; color:#000;
  box-shadow: 0 0 18px rgba(0,255,160,0.3);
}
.badges { display: flex; gap: 8px; flex-wrap: wrap; }
.hbadge {
  display: flex; align-items: center; gap: 6px;
  padding: 5px 13px;
  background: rgba(0,255,160,0.06);
  border: 1px solid var(--border-green);
  border-radius: 100px;
  font-family: 'Space Mono', monospace;
  font-size: 11px; color: var(--green); letter-spacing: 0.08em;
}
.hbadge.blue { background: rgba(0,200,255,0.06); border-color: rgba(0,200,255,0.2); color: var(--blue); }
.live-dot {
  width: 6px; height: 6px; background: var(--green); border-radius: 50%;
  box-shadow: 0 0 6px var(--green);
  animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── STAT CARDS ── */
.stats-row { display: grid; gap: 14px; margin-bottom: 24px; }
.stat-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 18px 22px;
  position: relative; overflow: hidden; transition: border-color .2s;
}
.stat-card:hover { border-color: var(--border-green); }
.stat-card::before {
  content: ''; position: absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, var(--green), var(--blue));
  opacity: 0; transition: opacity .2s;
}
.stat-card:hover::before { opacity: 1; }
.stat-lbl {
  font-family:'Space Mono',monospace; font-size:10px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.12em; margin-bottom:8px;
}
.stat-val {
  font-family:'Syne',sans-serif; font-size:28px; font-weight:800;
  color:var(--green); line-height:1; text-shadow:0 0 20px rgba(0,255,160,.3);
}
.stat-val.blue  { color:var(--blue); text-shadow:0 0 20px rgba(0,200,255,.3); }
.stat-val.white { color:#fff; text-shadow:none; }
.stat-sub { font-size:12px; color:var(--muted); margin-top:5px; }

/* ── SECTION TITLE ── */
.sec-title {
  font-family:'Syne',sans-serif; font-size:17px; font-weight:700; color:#fff;
  margin-bottom:14px; display:flex; align-items:center; gap:10px;
}
.sec-title::after { content:''; flex:1; height:1px; background:var(--border); }

/* ── PIPELINE BOX ── */
.pipe-box {
  background: var(--card); border:1px solid var(--border);
  border-radius:16px; padding:24px; margin-bottom:24px;
}

/* ── PIPELINE STEPS ── */
.step {
  display:flex; align-items:center; gap:14px;
  padding:12px 16px; background:var(--card2); border:1px solid var(--border);
  border-radius:10px; margin-bottom:8px; transition:all .3s;
}
.step.done  { border-color:rgba(0,255,160,.25); }
.step.running { border-color:var(--green); }
.step-icon {
  width:34px; height:34px; border-radius:8px;
  background:rgba(255,255,255,.04); border:1px solid var(--border);
  display:flex; align-items:center; justify-content:center; font-size:15px; flex-shrink:0;
}
.step.running .step-icon { background:rgba(0,255,160,.1); border-color:var(--border-green); }
.step.done   .step-icon { background:rgba(0,255,160,.12); border-color:rgba(0,255,160,.3); }
.step-name { font-size:13px; font-weight:600; color:var(--text); margin-bottom:2px; }
.step.running .step-name { color:var(--green); }
.step-desc { font-family:'Space Mono',monospace; font-size:9px; color:var(--muted); letter-spacing:.05em; }
.step-badge {
  font-size:10px; padding:3px 9px; border-radius:100px;
  background:rgba(255,255,255,.05); color:var(--muted);
  font-family:'Space Mono',monospace; letter-spacing:.05em; flex-shrink:0;
}
.step-badge.running { background:rgba(0,255,160,.1); color:var(--green); }
.step-badge.done    { background:rgba(0,255,160,.12); color:var(--green); }

/* fanout chips */
.fanout-row { display:flex; align-items:center; gap:8px; padding:6px 16px 6px 64px; flex-wrap:wrap; }
.fanout-chip {
  width:18px; height:7px; background:rgba(0,255,160,.1);
  border:1px solid rgba(0,255,160,.15); border-radius:2px;
}
.fanout-chip.lit {
  background:rgba(0,255,160,.45); border-color:rgba(0,255,160,.6);
  box-shadow:0 0 4px rgba(0,255,160,.3);
}

/* ── OPERATORS ── */
.op-card {
  background:var(--card2); border:1px solid var(--border);
  border-radius:10px; padding:14px; text-align:center; transition:all .3s;
}
.op-card.busy { border-color:rgba(0,255,160,.3); background:rgba(0,255,160,.03); }
.op-card.idle { opacity:.5; }
.op-type { font-family:'Space Mono',monospace; font-size:9px; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; margin-bottom:6px; }
.op-icon { font-size:22px; margin-bottom:6px; }
.op-id   { font-family:'Space Mono',monospace; font-size:10px; color:var(--text); margin-bottom:3px; }
.op-dot  { width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,.12); margin:4px auto; }
.op-card.busy .op-dot { background:var(--green); box-shadow:0 0 6px var(--green); }
.op-task { font-size:10px; color:var(--muted); font-family:'Space Mono',monospace; }
.op-card.busy .op-task { color:var(--green); }
.op-rep  { font-family:'Space Mono',monospace; font-size:9px; color:rgba(255,255,255,.2); margin-top:4px; }

/* ── CREATOR FORM ── */
.card-box {
  background:var(--card); border:1px solid var(--border);
  border-radius:14px; padding:24px; margin-bottom:20px;
}
.form-lbl {
  font-family:'Space Mono',monospace; font-size:10px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.12em; margin-bottom:6px; display:block;
}

/* type pills */
.pills { display:flex; gap:8px; flex-wrap:wrap; }
.pill {
  padding:6px 14px; border-radius:100px; border:1px solid var(--border);
  font-size:12px; color:var(--muted); cursor:pointer; background:var(--card2);
  transition:all .2s;
}
.pill.sel { background:rgba(0,255,160,.1); border-color:var(--border-green); color:var(--green); }

/* leaderboard */
.lb-item {
  display:flex; align-items:center; gap:12px;
  padding:11px 13px; background:var(--card2); border:1px solid var(--border);
  border-radius:10px; margin-bottom:8px; transition:all .2s;
}
.lb-item:hover { border-color:var(--border-green); }
.lb-rank { font-family:'Syne',sans-serif; font-size:15px; font-weight:800; width:22px; text-align:center; }
.rank-1{color:#ffd700;} .rank-2{color:#c0c0c0;} .rank-3{color:#cd7f32;} .rank-o{color:var(--muted);font-size:12px;}
.lb-avatar {
  width:34px; height:34px; border-radius:50%;
  background:linear-gradient(135deg,rgba(0,255,160,.3),rgba(0,200,255,.3));
  display:flex; align-items:center; justify-content:center; font-size:15px;
  border:1px solid rgba(0,255,160,.15); flex-shrink:0;
}
.lb-info { flex:1; }
.lb-name { font-size:13px; font-weight:600; color:var(--text); margin-bottom:1px; }
.lb-type { font-family:'Space Mono',monospace; font-size:9px; color:var(--muted); letter-spacing:.05em; }
.lb-spots { font-family:'Syne',sans-serif; font-size:17px; font-weight:800; color:var(--green); }
.lb-slbl  { font-family:'Space Mono',monospace; font-size:9px; color:var(--muted); text-transform:uppercase; }

/* feed */
.feed-item {
  display:flex; align-items:center; gap:12px;
  padding:12px 14px; background:var(--card2); border:1px solid var(--border);
  border-radius:10px; margin-bottom:8px;
}
.feed-icon { font-size:22px; flex-shrink:0; }
.feed-title { font-size:13px; font-weight:600; color:var(--text); margin-bottom:2px; }
.feed-meta  { font-family:'Space Mono',monospace; font-size:10px; color:var(--muted); }
.feed-badge {
  font-size:10px; padding:3px 10px; border-radius:100px;
  font-family:'Space Mono',monospace; flex-shrink:0;
}
.badge-thread { background:rgba(0,200,255,.1); color:var(--blue);   border:1px solid rgba(0,200,255,.2); }
.badge-art    { background:rgba(255,100,200,.1);color:#ff64c8;      border:1px solid rgba(255,100,200,.2);}
.badge-video  { background:rgba(255,160,0,.1);  color:#ffa000;      border:1px solid rgba(255,160,0,.2); }
.badge-tool   { background:rgba(0,255,160,.1);  color:var(--green); border:1px solid var(--border-green);}
.badge-meme   { background:rgba(255,255,0,.07); color:#ffe94d;      border:1px solid rgba(255,255,0,.15); }

/* countdown */
.countdown-row { display:flex; align-items:center; gap:20px; flex-wrap:wrap; }
.cu-num { font-family:'Syne',sans-serif; font-size:26px; font-weight:800; color:var(--green); line-height:1; text-shadow:0 0 12px rgba(0,255,160,.3); }
.cu-lbl { font-family:'Space Mono',monospace; font-size:9px; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; margin-top:3px; }

/* my-stats bar */
.my-stats { display:flex; gap:20px; flex-wrap:wrap; align-items:center; }
.my-num { font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:var(--green); }
.my-lbl { font-family:'Space Mono',monospace; font-size:9px; color:var(--muted); text-transform:uppercase; }

/* learn cards */
.learn-card {
  background:var(--card); border:1px solid var(--border); border-radius:14px;
  padding:24px; cursor:pointer; transition:all .2s; margin-bottom:12px;
}
.learn-card:hover { border-color:var(--border-green); background:rgba(0,255,160,.02); }
.learn-icon  { font-size:28px; margin-bottom:10px; }
.learn-title { font-family:'Syne',sans-serif; font-size:16px; font-weight:700; color:#fff; margin-bottom:6px; }
.learn-desc  { font-size:13px; color:var(--muted); line-height:1.6; }

/* chat box */
.chat-box {
  background:var(--card); border:1px solid var(--border-green);
  border-radius:14px; padding:20px; margin-top:16px;
}
.chat-header {
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:14px;
}
.ai-badge {
  font-family:'Space Mono',monospace; font-size:9px;
  background:rgba(0,255,160,.1); border:1px solid var(--border-green);
  color:var(--green); padding:3px 9px; border-radius:100px; letter-spacing:.1em;
}
.chat-msg {
  padding:11px 14px; border-radius:10px; font-size:13px; line-height:1.65;
  margin-bottom:10px;
}
.chat-msg.user {
  background:rgba(0,255,160,.06); border:1px solid var(--border-green);
  color:var(--text); margin-left:auto; max-width:85%;
}
.chat-msg.assistant {
  background:var(--dark); border:1px solid var(--border); color:rgba(255,255,255,.75);
}
.msg-lbl {
  font-family:'Space Mono',monospace; font-size:9px; text-transform:uppercase;
  letter-spacing:.1em; margin-bottom:5px; opacity:.5;
}

/* ecosystem cards */
.eco-card {
  background:var(--card); border:1px solid var(--border); border-radius:10px;
  padding:16px; text-align:center; transition:all .2s;
}
.eco-card:hover { border-color:rgba(0,255,160,.25); }
.eco-name { font-family:'Syne',sans-serif; font-size:13px; font-weight:700; color:#fff; }
.eco-sub  { font-size:11px; color:var(--muted); margin-top:3px; }

/* backed by tags */
.backer {
  display:inline-block; padding:7px 16px;
  background:var(--card); border:1px solid var(--border); border-radius:8px;
  font-size:13px; color:var(--muted); margin:4px;
}

/* progress bar */
.prog-wrap { background:rgba(255,255,255,.04); border-radius:100px; height:4px; overflow:hidden; margin-top:14px; }
.prog-fill {
  height:100%; background:linear-gradient(90deg,var(--green),var(--blue));
  border-radius:100px; box-shadow:0 0 8px rgba(0,255,160,.5);
  transition:width .5s ease;
}

/* how-ops grid */
.how-ops { display:grid; gap:14px; }

/* toast-like alert */
.toast-green {
  background:rgba(0,255,160,.06); border:1px solid var(--border-green);
  border-radius:10px; padding:12px 16px; color:var(--green);
  font-family:'DM Sans',sans-serif; font-size:14px; margin-top:10px;
}

/* ── RESPONSIVE ── */
@media (max-width: 700px) {
  .dash-header { padding: 12px 14px; }
  .logo { font-size: 17px; }
  .stat-val { font-size: 22px; }
  .pipe-box, .card-box { padding: 16px; }
  .step { padding: 10px 12px; gap: 10px; }
  .fanout-row { padding-left: 44px; }
}

/* override streamlit defaults for dark theme */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--card2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stButton > button {
  background: var(--green) !important;
  color: #000 !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em !important;
  transition: all .2s !important;
}
.stButton > button:hover { box-shadow: 0 0 20px rgba(0,255,160,.4) !important; transform: translateY(-1px) !important; }
.stTabs [role="tab"] {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  color: var(--muted) !important;
  background: transparent !important;
  border: none !important;
}
.stTabs [role="tab"][aria-selected="true"] { color: var(--green) !important; border-bottom: 2px solid var(--green) !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(5,5,10,.6) !important; border-bottom: 1px solid var(--border) !important; gap: 4px !important; }
div[data-testid="metric-container"] { display: none; }
.stAlert { background: var(--card2) !important; border-color: var(--border-green) !important; color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "total_proofs" not in st.session_state:
    st.session_state.total_proofs = 127_453
if "submissions" not in st.session_state:
    st.session_state.submissions = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}   # keyed by topic
if "chat_topic" not in st.session_state:
    st.session_state.chat_topic = None
if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="logo">
    <div class="logo-pi">π</div>
    Fermah Dashboard
  </div>
  <div class="badges">
    <div class="hbadge"><div class="live-dot"></div>MAINNET LIVE</div>
    <div class="hbadge blue">CREATOR PROGRAM ACTIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ Proof Pipeline",
    "🖥️ Operator Network",
    "🎨 Creator Tracker",
    "📚 Learn Fermah",
])

# ══════════════════════════════════════════════
# TAB 1 — PROOF PIPELINE
# ══════════════════════════════════════════════
with tab1:
    # Animate total proofs
    st.session_state.total_proofs += random.randint(1, 3)

    cols = st.columns(4)
    stats = [
        ("Total Proofs Generated", f"{st.session_state.total_proofs:,}", "+2,847 today", ""),
        ("Avg Proof Time",         "9.4 min",                             "ZKsync Era batches", "blue"),
        ("Active Operators",       "34",                                   "GPU + FPGA nodes",   "white"),
        ("Uptime SLA",             "99.9%",                               "Since mainnet launch",""),
    ]
    for col, (lbl, val, sub, cls) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-lbl">{lbl}</div>
              <div class="stat-val {cls}">{val}</div>
              <div class="stat-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="pipe-box">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">ZK Proof Pipeline Simulator</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        proof_system = st.selectbox("Proof System", [
            "ZKsync Era (Boojum)",
            "Scroll (zkEVM)",
            "RISC Zero zkVM",
            "Airbender (EthProofs)",
        ], label_visibility="collapsed")
    with c2:
        run_clicked = st.button("▶ Run Pipeline")
    with c3:
        reset_clicked = st.button("↺  Reset")

    STEPS = [
        ("📥", "Proof Request Submission",    "SEEKER → FERMAH FROBEN · REST API call",          "~2s",   0.6),
        ("🔍", "Matchmaker Routing",          "CAPABILITY CHECK · REPUTATION SCORE · VRAM",      "~1s",   0.5),
        ("🧠", "Witness Generation",          "CPU-INTENSIVE · 13+ CIRCUIT TYPES · ~20MB CBOR",  "~2 min",1.2),
        ("⚡", "Circuit Proving (GPU Fanout)","~500 TASKS · 30-35 GPU MACHINES · FRI via SHIVINI","~5 min",2.0),
        ("🔗", "Leaf + Node Aggregation",     "RECURSIVE PROOF FOLDING → SINGLE PROOF",          "~90s",  1.0),
        ("🗜️", "SNARK Compression",           "FFLONK / PLONK WRAPPER · GPU-INTENSIVE",          "~60s",  0.8),
        ("✅", "On-Chain Submission",          "COMPRESSED PROOF → L1 ETHEREUM",                 "~30s",  0.6),
    ]

    step_placeholder = st.empty()
    progress_placeholder = st.empty()
    result_placeholder = st.empty()

    def render_steps(active=-1, done_up_to=-1, fanout=False):
        html = ""
        for i, (icon, name, desc, timing, _) in enumerate(STEPS):
            state = ""
            badge_cls = ""
            badge_txt = "PENDING"
            if i <= done_up_to:
                state = "done";    badge_cls = "done";    badge_txt = "DONE ✓"
            elif i == active:
                state = "running"; badge_cls = "running"; badge_txt = "RUNNING"
            html += f"""
            <div class="step {state}">
              <div class="step-icon">{icon}</div>
              <div style="flex:1">
                <div class="step-name">{name}</div>
                <div class="step-desc">{desc}</div>
              </div>
              <div style="text-align:right;flex-shrink:0">
                <div style="font-family:'Space Mono',monospace;font-size:11px;color:{'var(--green)' if state=='running' else 'var(--muted)'};">{timing}</div>
                <div class="step-badge {badge_cls}">{badge_txt}</div>
              </div>
            </div>"""
            if i == 3 and fanout:
                chips = "".join('<div class="fanout-chip lit"></div>' for _ in range(35))
                html += f"""<div class="fanout-row">
                  <span style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-right:6px">FANNING OUT →</span>
                  {chips}
                  <span style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-left:6px">~500 GPU tasks · 35 operators</span>
                </div>"""
        return html

    if reset_clicked:
        st.session_state.pipeline_done = False

    # Default idle render
    step_placeholder.markdown(render_steps(), unsafe_allow_html=True)
    progress_placeholder.markdown(
        '<div class="prog-wrap"><div class="prog-fill" style="width:0%"></div></div>',
        unsafe_allow_html=True)

    if run_clicked:
        st.session_state.pipeline_done = False
        for i, (icon, name, desc, timing, delay) in enumerate(STEPS):
            step_placeholder.markdown(render_steps(active=i, done_up_to=i-1, fanout=(i>=3)), unsafe_allow_html=True)
            pct = int((i + 0.5) / len(STEPS) * 100)
            progress_placeholder.markdown(
                f'<div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>',
                unsafe_allow_html=True)
            time.sleep(delay)
            step_placeholder.markdown(render_steps(active=-1, done_up_to=i, fanout=(i>=3)), unsafe_allow_html=True)

        progress_placeholder.markdown(
            '<div class="prog-wrap"><div class="prog-fill" style="width:100%"></div></div>',
            unsafe_allow_html=True)
        result_placeholder.markdown(
            '<div class="toast-green">✓ Proof submitted to Ethereum mainnet! 🎉</div>',
            unsafe_allow_html=True)
        st.session_state.pipeline_done = True

    st.markdown("</div>", unsafe_allow_html=True)  # close pipe-box

# ══════════════════════════════════════════════
# TAB 2 — OPERATOR NETWORK
# ══════════════════════════════════════════════
with tab2:
    cols = st.columns(4)
    op_stats = [
        ("Total Operators", "34",    "Connected nodes",          ""),
        ("GPU Nodes",       "28",    "Avg 24GB VRAM",            "blue"),
        ("Tasks / Hour",    "1,840", "Circuit proving jobs",     ""),
        ("Avg Reputation",  "97.2%", "Completion rate",          "white"),
    ]
    for col, (lbl, val, sub, cls) in zip(cols, op_stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-lbl">{lbl}</div>
              <div class="stat-val {cls}">{val}</div>
              <div class="stat-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-title" style="margin-top:8px">Live Operator Network</div>', unsafe_allow_html=True)

    OP_TYPES  = ['ZKSyncCP','ZKSyncWG','ScrollEVM','RISC0','Airbender']
    OP_ICONS  = ['🖥️','💻','⚡','🔮','🌀']

    op_cols = st.columns(5)
    for i in range(35):
        busy = random.random() > 0.35
        t_idx = i % len(OP_TYPES)
        rep   = round(94 + random.random()*6, 1)
        col   = op_cols[i % 5]
        with col:
            st.markdown(f"""
            <div class="op-card {'busy' if busy else 'idle'}">
              <div class="op-type">{OP_TYPES[t_idx]}</div>
              <div class="op-icon">{OP_ICONS[t_idx]}</div>
              <div class="op-id">OP-{str(i+1).zfill(3)}</div>
              <div class="op-dot"></div>
              <div class="op-task">{'Proving...' if busy else 'Idle'}</div>
              <div class="op-rep">{rep}% rep</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="pipe-box">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title" style="font-size:15px">How Operators Work</div>', unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3)
    for col, (num, body) in zip([h1,h2,h3],[
        ("1. Connect",      "Run a single binary over mutual TLS. Connect to the Fermah Froben runtime. No config needed for ZK internals."),
        ("2. Receive Tasks","Matchmaker routes circuit prover batches to your machine based on capability, VRAM, and reputation score."),
        ("3. Earn",         "Get paid per delegation. Run multiple machines under one identity. Reputation compounds with every completed proof."),
    ]):
        with col:
            st.markdown(f"""
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--green);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px">{num}</div>
            <div style="font-size:13px;color:var(--muted);line-height:1.6">{body}</div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — CREATOR TRACKER
# ══════════════════════════════════════════════
with tab3:
    # Countdown
    now = datetime.now(timezone.utc)
    day_of_week = now.weekday()  # Mon=0 … Sun=6
    days_to_sunday = (6 - day_of_week) % 7
    from datetime import timedelta
    next_sunday = now + timedelta(days=days_to_sunday)
    next_close  = next_sunday.replace(hour=12, minute=0, second=0, microsecond=0)
    if next_close < now:
        next_close += timedelta(days=7)
    diff = next_close - now
    total_secs = int(diff.total_seconds())
    cd_days = total_secs // 86400
    cd_hrs  = (total_secs % 86400) // 3600
    cd_mins = (total_secs % 3600)  // 60
    cd_secs = total_secs % 60

    st.markdown(f"""
    <div class="card-box" style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin-bottom:20px">
      <div>
        <div style="font-family:'Space Mono',monospace;font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px">Submission Window Closes In</div>
        <div class="countdown-row">
          <div><div class="cu-num">{cd_days:02d}</div><div class="cu-lbl">Days</div></div>
          <div style="color:var(--muted);font-size:20px;padding-top:2px">:</div>
          <div><div class="cu-num">{cd_hrs:02d}</div><div class="cu-lbl">Hours</div></div>
          <div style="color:var(--muted);font-size:20px;padding-top:2px">:</div>
          <div><div class="cu-num">{cd_mins:02d}</div><div class="cu-lbl">Mins</div></div>
          <div style="color:var(--muted);font-size:20px;padding-top:2px">:</div>
          <div><div class="cu-num">{cd_secs:02d}</div><div class="cu-lbl">Secs</div></div>
        </div>
      </div>
      <div style="flex:1;font-size:13px;color:var(--muted);line-height:1.7;min-width:200px">
        <strong style="color:var(--text)">Window:</strong> Mon 00:00 UTC → Sun 12:00 PM UTC<br>
        <strong style="color:var(--text)">Top 5</strong> creators spotlighted every week.<br>
        <strong style="color:var(--text)">3 spotlights</strong> → Contributor role 🏅 unlocked permanently.
      </div>
    </div>""", unsafe_allow_html=True)

    # My stats
    my_spotlights  = sum(1 for s in st.session_state.submissions if s.get("spotlight"))
    my_submissions = len(st.session_state.submissions)
    st.markdown(f"""
    <div class="card-box my-stats" style="margin-bottom:20px">
      <div><div class="my-num">{my_spotlights}</div><div class="my-lbl">My Spotlights</div></div>
      <div><div class="my-num">{my_submissions}</div><div class="my-lbl">Submissions</div></div>
      <div><div class="my-num" style="color:var(--blue)">0</div><div class="my-lbl">Week Streak</div></div>
      <div style="flex:1;min-width:180px">
        <div style="display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-bottom:5px">
          <span>Progress to Contributor 🏅</span>
          <span>{my_spotlights} / 3 spotlights</span>
        </div>
        <div class="prog-wrap"><div class="prog-fill" style="width:{min(my_spotlights/3*100,100):.0f}%"></div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    # ── SUBMIT FORM ──
    with left:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown('<div class="sec-title" style="font-size:16px;margin-bottom:16px">Submit Your Creation</div>', unsafe_allow_html=True)

        handle = st.text_input("Your Handle", placeholder="@yourhandle", label_visibility="collapsed",
                               key="f_handle")
        st.markdown('<span class="form-lbl">Your Handle</span>', unsafe_allow_html=True)
        title_inp = st.text_input("Content Title", placeholder="e.g. Fermah ZK Explainer Thread",
                                  label_visibility="collapsed", key="f_title")
        st.markdown('<span class="form-lbl">Content Title</span>', unsafe_allow_html=True)

        content_type = st.radio("Content Type",
            ["✍️ Thread", "🎨 Art", "🎥 Video", "🛠️ Tool", "😂 Meme"],
            horizontal=True, label_visibility="collapsed")
        st.markdown('<span class="form-lbl">Content Type</span>', unsafe_allow_html=True)

        desc = st.text_area("Link / Description",
                            placeholder="Paste your tweet URL or describe your submission...",
                            label_visibility="collapsed", key="f_desc", height=80)
        st.markdown('<span class="form-lbl">Link / Description</span>', unsafe_allow_html=True)

        if st.button("🚀 Submit to Creator Program"):
            if handle and title_inp and content_type:
                type_key = content_type.split()[1].lower()
                st.session_state.submissions.insert(0, {
                    "handle": handle, "title": title_inp,
                    "type": type_key,
                    "emoji": content_type.split()[0],
                    "badge": f"badge-{type_key}",
                    "spotlight": False,
                })
                st.success("🚀 Submission sent! Good luck this week 🐬")
            else:
                st.warning("⚠️ Please fill Handle, Title and select a type!")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── LEADERBOARD ──
    with right:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown('<div class="sec-title" style="font-size:16px;margin-bottom:14px">🏆 Weekly Leaderboard</div>', unsafe_allow_html=True)
        SAMPLE_ENTRIES = [
            {"handle":"@zkbuilder",    "title":"Fermah Froben Deep Dive Thread",      "type":"thread","emoji":"✍️","badge":"badge-thread","spotlights":3},
            {"handle":"@cryptoart_pi", "title":"Fermah x ZK — Motion Graphic",       "type":"art",   "emoji":"🎨","badge":"badge-art",   "spotlights":2},
            {"handle":"@0xfermah_fan", "title":"Fermah Explained in 60 Seconds",     "type":"video", "emoji":"🎥","badge":"badge-video", "spotlights":2},
            {"handle":"@builder_zk",   "title":"Proof Cost Estimator Tool",           "type":"tool",  "emoji":"🛠️","badge":"badge-tool",  "spotlights":1},
            {"handle":"@mememaster99", "title":"Fermah vs. Solo Proving Meme",        "type":"meme",  "emoji":"😂","badge":"badge-meme",  "spotlights":1},
        ]
        for i, e in enumerate(SAMPLE_ENTRIES):
            rank_sym   = ["🥇","🥈","🥉"][i] if i < 3 else str(i+1)
            rank_cls   = ["rank-1","rank-2","rank-3"][i] if i < 3 else "rank-o"
            contrib    = "🏅" if e["spotlights"] >= 3 else ""
            st.markdown(f"""
            <div class="lb-item">
              <div class="lb-rank {rank_cls}">{rank_sym}</div>
              <div class="lb-avatar">{e['emoji']}</div>
              <div class="lb-info">
                <div class="lb-name">{e['handle']} {contrib}</div>
                <div class="lb-type">{e['type'].upper()} · {e['title']}</div>
              </div>
              <div style="text-align:right;flex-shrink:0">
                <div class="lb-spots">{e['spotlights']}</div>
                <div class="lb-slbl">Spotlights</div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── RECENT FEED ──
    st.markdown('<div class="sec-title">📥 Recent Submissions Feed</div>', unsafe_allow_html=True)
    all_feed = st.session_state.submissions + [
        {"handle":"@zkbuilder","title":"Fermah Froben Deep Dive Thread","emoji":"✍️","badge":"badge-thread","type":"thread"},
        {"handle":"@cryptoart_pi","title":"Fermah x ZK — Motion Graphic","emoji":"🎨","badge":"badge-art","type":"art"},
        {"handle":"@0xfermah_fan","title":"Fermah Explained in 60 Seconds","emoji":"🎥","badge":"badge-video","type":"video"},
    ]
    for e in all_feed[:6]:
        st.markdown(f"""
        <div class="feed-item">
          <div class="feed-icon">{e['emoji']}</div>
          <div style="flex:1">
            <div class="feed-title">{e['title']}</div>
            <div class="feed-meta">{e['handle']} · Week 1</div>
          </div>
          <div class="feed-badge {e['badge']}">{e['type'].upper()}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — LEARN FERMAH (Static Q&A — no API needed)
# ══════════════════════════════════════════════
with tab4:

    # ── Static Q&A knowledge base ──
    STATIC_QA = {
        "zk": {
            "icon": "🔐",
            "title": "What is a ZK Proof?",
            "desc": "Prove something is true without revealing the underlying data. The foundation of Fermah's entire stack.",
            "welcome": "A Zero-Knowledge Proof (ZKP) lets you prove that a statement is true without revealing any information beyond the truth of that statement itself. Imagine proving you know a password without actually sharing the password — that's the essence of ZK.\n\nIn blockchain, ZK proofs are used to verify thousands of transactions off-chain and submit a single tiny proof to Layer 1 (Ethereum). This dramatically reduces gas costs and increases throughput. ZK Rollups like ZKsync and Scroll use this technique to scale Ethereum.\n\nFermah sits at the heart of this — generating these computationally heavy proofs at scale using a distributed network of GPU operators, so any protocol can access ZK proving without running their own infrastructure.",
            "qas": [
                {
                    "q": "ZK proof kya hota hai?",
                    "a": "Zero-Knowledge Proof ek aisi technique hai jisme aap prove kar sakte hain ki koi baat sach hai — bina us baat ki underlying information share kiye. Jaise password bataye bina prove karna ki aapko password pata hai.\n\nBlockchain mein yeh thousands of transactions ko off-chain verify karne ke liye use hota hai, aur sirf ek chota sa proof L1 pe submit hota hai."
                },
                {
                    "q": "What is a ZK Rollup?",
                    "a": "A ZK Rollup bundles (rolls up) hundreds or thousands of transactions off the main Ethereum chain, computes a ZK proof that all those transactions are valid, and then submits just that proof to Ethereum L1.\n\nThis means Ethereum only needs to verify one small proof instead of thousands of individual transactions — massively reducing cost and increasing speed. ZKsync Era and Scroll are leading ZK Rollups that Fermah powers."
                },
                {
                    "q": "What proof systems does Fermah support?",
                    "a": "Fermah supports multiple proof systems:\n\n• Boojum (FRI-based) — used by ZKsync Era\n• zkEVM — used by Scroll for EVM-compatible proving\n• RISC Zero zkVM — general purpose zkVM for any computation\n• Airbender — used in EthProofs for Ethereum block proving\n\nEach system has different circuit types, VRAM requirements, and performance characteristics. Fermah's Matchmaker routes tasks to the right operator for each system."
                },
                {
                    "q": "Why is proof generation expensive?",
                    "a": "Generating a ZK proof requires massive computation. For a single ZKsync Era batch, Fermah spawns 500+ parallel GPU tasks across 30-35 machines — running for 8-12 minutes total.\n\nThe process involves Witness Generation (CPU-heavy, ~2 min), Circuit Proving (GPU fan-out, ~5 min), Leaf+Node Aggregation (recursive folding, ~90s), and SNARK Compression (GPU, ~60s). Without a distributed network like Fermah, protocols would need to own and maintain enormous GPU infrastructure themselves."
                },
                {
                    "q": "What is a circuit in ZK?",
                    "a": "A ZK circuit is a mathematical representation of a computation that can be proven. Think of it like a blueprint — it defines exactly what needs to be computed and constraints that must hold.\n\nZKsync Era alone has 13+ different circuit types (each handling different EVM operations). Each circuit type may need a different prover, different VRAM, and different GPU configuration. Fermah's Matchmaker handles all this routing automatically."
                },
            ]
        },
        "froben": {
            "icon": "🏪",
            "title": "Fermah Froben Explained",
            "desc": "The universal proof market — how Seekers, Matchmakers and Operators work together.",
            "welcome": "Fermah Froben is the universal ZK proof marketplace — a system where anyone who needs a ZK proof (a Seeker) can get one generated without owning any GPU hardware.\n\nThe flow works in three layers: Seekers submit proof requests via a simple REST API call. The Matchmaker then filters available Operators by their hardware capability, VRAM, supported proof systems, and reputation score — and assigns the job. Operators run Fermah's single binary over mutual TLS, receive circuit proving batches, compute the proof, and return the result.\n\nPartners using Froben today include ZKsync, Scroll, Boundless, LayerEdge, zkVerify, Aligned, and Hylé. A ZKsync Era batch proof spawns 500+ GPU tasks across 30-35 machines and completes in 8-12 minutes.",
            "qas": [
                {
                    "q": "Froben ka flow kya hai step by step?",
                    "a": "Froben ka end-to-end flow:\n\n1️⃣ Seeker REST API call karta hai proof request ke saath\n2️⃣ Matchmaker request receive karta hai aur eligible Operators filter karta hai (capability, VRAM, reputation ke basis pe)\n3️⃣ Operator ko task assign hota hai, woh circuit proving karta hai apne GPU pe\n4️⃣ Proof generate hota hai, aggregate hota hai, aur Seeker ko return hota hai\n5️⃣ Seeker compressed proof ko L1 Ethereum pe submit karta hai"
                },
                {
                    "q": "Who are Seekers?",
                    "a": "Seekers are protocols or applications that need ZK proofs generated but don't want to run their own GPU infrastructure. Examples include ZKsync (needs block proofs), Scroll (needs zkEVM proofs), Boundless, and any app building on ZK technology.\n\nSeekers call Fermah's REST API with their proof request — specifying the proof system, input data, and requirements. Fermah handles everything else from routing to generation to delivery."
                },
                {
                    "q": "How does the Matchmaker work?",
                    "a": "The Matchmaker is Fermah's intelligent routing engine. When a proof request comes in, it filters available Operators by:\n\n• Proof system support (Boojum, zkEVM, RISC Zero, etc.)\n• Available VRAM (some circuits need 24GB+)\n• Reputation score (completion rate history)\n• Current load and availability\n\nIt then assigns circuit-proving sub-tasks to the best matched operators and coordinates the fan-out across 30-35 machines for large batches."
                },
                {
                    "q": "How do Operators earn?",
                    "a": "Operators earn by running GPU hardware and completing proof tasks assigned by the Matchmaker. Key facts:\n\n• Run a single binary — no complex ZK configuration needed\n• Connect via mutual TLS (mTLS) for secure communication\n• Get paid per delegation (per completed task)\n• Can run multiple machines under one operator identity\n• Reputation score compounds with each successful proof\n• Higher reputation → more tasks → more earnings"
                },
                {
                    "q": "Which protocols use Fermah?",
                    "a": "Current Fermah partners and integrations:\n\n🔷 ZKsync Era — block proving (Boojum/FRI)\n📜 Scroll — high-load zkEVM proving\n🔗 Boundless — ZK infrastructure layer\n🌊 Flashcast — on-chain prediction markets\n✅ zkVerify — ZK verification layer\n🔺 Aligned — fast ZK verification\n🟣 Hylé — ZK-native settlement\n🔵 LayerEdge — edge ZK computation\n\nFermah has generated 127,000+ proofs since mainnet launch with 99.9% uptime SLA."
                },
            ]
        },
        "kernel": {
            "icon": "⚙️",
            "title": "Fermah Kernel",
            "desc": "The autonomous workflow engine that powers everything — ending the last human-in-the-loop problem.",
            "welcome": "Fermah Kernel is an autonomous workflow engine that eliminates human-in-the-loop dependencies from crypto protocols. Most blockchain systems today still rely on humans for critical steps — manual proof orchestration, resolution committees, oracle updates, and 48-hour dispute windows.\n\nKernel replaces all of these with deterministic, programmable automation. A complex multi-step process that would normally require human intervention at every stage can now run end-to-end with zero manual involvement.\n\nThe best demonstration of Kernel is Flashcast — Fermah's prediction market product. When a question is tweeted, Flashcast uses Kernel to spin up a live prediction market on-chain in 3 seconds, source real-world data, verify it with ZK proofs, and resolve the market automatically — no committees, no delays, no humans.",
            "qas": [
                {
                    "q": "Kernel kya solve karta hai?",
                    "a": "Kernel in human-in-the-loop problems ko solve karta hai:\n\n❌ Manual proof orchestration → ✅ Automated\n❌ Resolution committees → ✅ On-chain automatic resolution\n❌ Manual oracle updates → ✅ Programmatic data feeds\n❌ 48-hour dispute windows → ✅ Instant ZK-verified resolution\n\nKernel ki wajah se complex multi-step crypto workflows bina kisi human intervention ke chalte hain — deterministically aur reliably."
                },
                {
                    "q": "What is Flashcast?",
                    "a": "Flashcast is Fermah's flagship demo of Kernel — a fully autonomous prediction market system.\n\nHere's what happens in 3 seconds when a question is tweeted:\n1. Kernel detects the question\n2. Spins up a live prediction market on-chain\n3. Users can bet on outcomes\n4. When the event resolves, Kernel fetches real-world data\n5. Generates a ZK proof of the correct outcome\n6. Resolves the market on-chain automatically\n\nNo resolution committee. No 48-hour window. No manual steps. Just pure automated, ZK-verified resolution."
                },
                {
                    "q": "How is Kernel different from smart contracts?",
                    "a": "Smart contracts execute logic on-chain when triggered, but they can't autonomously initiate complex multi-step off-chain workflows.\n\nKernel goes further — it orchestrates entire pipelines that span off-chain computation (ZK proving), external data sources (oracles), and on-chain execution. It can handle conditional branching, retries, multi-party coordination, and proof verification — all without any human stepping in.\n\nThink of smart contracts as individual functions, and Kernel as the autonomous program that calls them in the right sequence with the right data."
                },
                {
                    "q": "What workflows can Kernel automate?",
                    "a": "Kernel is general purpose — any crypto workflow that currently needs human coordination can be automated. Examples:\n\n• Prediction market creation and resolution (Flashcast)\n• ZK proof orchestration across multiple operators\n• Cross-chain bridge operations with ZK verification\n• Automated protocol upgrades triggered by on-chain conditions\n• Oracle data pipelines with ZK-attested accuracy\n• DAO governance execution without manual multisig delays\n\nIf it has a defined set of steps and conditions, Kernel can run it."
                },
                {
                    "q": "Is Kernel live?",
                    "a": "Yes — Kernel is live on mainnet and powering Flashcast today. Fermah launched mainnet with 99.9% uptime SLA and 127,000+ proofs generated.\n\nKernel runs alongside Froben (the proof marketplace) as Fermah's second core product. Together they form a full-stack ZK infrastructure: Froben handles proof generation at scale, Kernel handles the automation of workflows that depend on those proofs."
                },
            ]
        },
    }

    # Session state for static Q&A
    if "learn_topic" not in st.session_state:
        st.session_state.learn_topic = None
    if "learn_history" not in st.session_state:
        st.session_state.learn_history = {}

    # Topic cards
    lc1, lc2, lc3 = st.columns(3)
    for col, (key, t) in zip([lc1, lc2, lc3], STATIC_QA.items()):
        with col:
            if st.button(
                f"{t['icon']}  {t['title']}\n\n{t['desc']}",
                key=f"learn_{key}",
                use_container_width=True,
            ):
                st.session_state.learn_topic = key
                if key not in st.session_state.learn_history:
                    st.session_state.learn_history[key] = [
                        {"role": "assistant", "content": t["welcome"]}
                    ]

    # Chat Box
    if st.session_state.learn_topic:
        tkey = st.session_state.learn_topic
        t    = STATIC_QA[tkey]
        hist = st.session_state.learn_history.get(tkey, [])

        st.markdown(f"""
        <div class="chat-box">
          <div class="chat-header">
            <div style="display:flex;align-items:center;gap:10px;font-family:'Syne',sans-serif;font-weight:700;font-size:16px;color:#fff">
              {t['icon']} {t['title']}
              <span class="ai-badge">KNOWLEDGE BASE</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Render conversation history
        for msg in hist:
            role_lbl = "👤 You" if msg["role"] == "user" else "✦ Fermah Guide"
            st.markdown(f"""
            <div class="chat-msg {msg['role']}">
              <div class="msg-lbl">{role_lbl}</div>
              <div>{msg['content'].replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)

        # Suggested questions
        st.markdown(
            '<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:var(--muted);'
            'text-transform:uppercase;letter-spacing:.1em;margin:14px 0 8px">Suggested Questions</div>',
            unsafe_allow_html=True,
        )
        q_cols = st.columns(2)
        for idx, qa in enumerate(t["qas"]):
            with q_cols[idx % 2]:
                if st.button(f"❓ {qa['q']}", key=f"sq_{tkey}_{idx}", use_container_width=True):
                    hist.append({"role": "user",      "content": qa["q"]})
                    hist.append({"role": "assistant",  "content": qa["a"]})
                    st.session_state.learn_history[tkey] = hist
                    st.rerun()

        # Custom question input
        st.markdown("<br>", unsafe_allow_html=True)
        ci1, ci2 = st.columns([5, 1])
        with ci1:
            custom_q = st.text_input(
                "Apna sawaal poochho...",
                placeholder="Type your question here...",
                label_visibility="collapsed",
                key=f"custom_q_{tkey}",
            )
        with ci2:
            ask_btn = st.button("Ask ✦", key=f"ask_custom_{tkey}")

        if ask_btn and custom_q.strip():
            # Fuzzy match against known Q&A
            q_lower = custom_q.lower()
            matched = None
            best_score = 0
            for qa in t["qas"]:
                keywords = set(qa["q"].lower().split())
                user_words = set(q_lower.split())
                score = len(keywords & user_words)
                if score > best_score:
                    best_score = score
                    matched = qa
            if matched and best_score >= 1:
                answer = matched["a"]
            else:
                answer = (
                    f"Yeh specific sawaal abhi knowledge base mein nahi hai, "
                    f"lekin upar ke suggested questions se related info mil sakti hai.\n\n"
                    f"Fermah ke baare mein aur jaanne ke liye visit karein: https://fermah.xyz"
                )
            hist.append({"role": "user",     "content": custom_q.strip()})
            hist.append({"role": "assistant","content": answer})
            st.session_state.learn_history[tkey] = hist
            st.rerun()

        if st.button("✕ Close", key=f"close_learn_{tkey}"):
            st.session_state.learn_topic = None
            st.rerun()

    # Ecosystem
    st.markdown('<br><div class="sec-title">🌐 Fermah Ecosystem</div>', unsafe_allow_html=True)
    eco_items = [
        ("🔷","ZKsync","Block proving"),
        ("📜","Scroll","High-load proving"),
        ("🔗","Boundless","ZK infrastructure"),
        ("✅","zkVerify","Verification layer"),
        ("🌊","Flashcast","Prediction markets"),
    ]
    eco_cols = st.columns(5)
    for col, (icon, name, sub) in zip(eco_cols, eco_items):
        with col:
            st.markdown(f"""
            <div class="eco-card">
              <div style="font-size:20px;margin-bottom:6px">{icon}</div>
              <div class="eco-name">{name}</div>
              <div class="eco-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    # Backed by
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">💎 Backed By</div>', unsafe_allow_html=True)
    backers = ["a16z CSX","Lemniscap","Bankless Ventures","Lambda Class","Balaji Srinivasan",
               "Polygon Founders","Aztec (Zac Williamson)","Celestia (Mustafa Al-Bassam)","LongHash Ventures"]
    st.markdown(" ".join(f'<span class="backer">{b}</span>' for b in backers), unsafe_allow_html=True)
