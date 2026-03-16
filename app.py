import streamlit as st
import json
import random
import time
import textwrap
import streamlit.components.v1 as components
import base64

def get_base64_bg(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    bg_b64 = get_base64_bg("images/bg.png")
    BG_CSS = f"url('data:image/png;base64,{bg_b64}') no-repeat center center fixed"
except Exception:
    BG_CSS = "#0D0B0E"

# ============================================
# Clayens — Luxury Tombola Theme
# ============================================

st.set_page_config(
    page_title="Clayens Tombola",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# LOAD EMPLOYEES
# ============================================
with open("employees.json", "r") as f:
    employees_data = json.load(f)

# ============================================
# SESSION STATE INIT
# ============================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "winners_list" not in st.session_state:
    st.session_state.winners_list = []
if "draw_done" not in st.session_state:
    st.session_state.draw_done = False

# ============================================
# GLOBAL CSS — LUXURY DARK GOLD THEME
# ============================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Cormorant+Garamond:wght@300;400;500;600&family=Montserrat:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: {BG_CSS} !important;
    background-size: cover !important;
    font-family: 'Montserrat', sans-serif;
    color: #F5EDD6;
}}

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stHeader"],
[data-testid="stToolbar"], [data-testid="stDecoration"] {{
    display: none !important;
}}

[data-testid="stAppViewContainer"] {{
    background: transparent !important;
}}

[data-testid="stMain"] {{
    background: transparent !important;
    padding: 0 !important;
}}

.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

/* ── Noise texture overlay ── */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    background-size: 200px 200px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}}

/* ── Page wrapper ── */
.page-wrap {{
    position: relative;
    min-height: 100vh;
    padding: 0;
    overflow: hidden;
}}

/* ── Ambient glow orbs ── */
.orb {{
    position: fixed;
    border-radius: 50%;
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.15;
}}
.orb-1 {{ width: 500px; height: 500px; background: #C4A44A; top: -150px; left: -100px; }}
.orb-2 {{ width: 400px; height: 400px; background: #8B1A1A; bottom: -100px; right: -80px; }}
.orb-3 {{ width: 300px; height: 300px; background: #1A3A5C; top: 50%; left: 50%; transform: translate(-50%, -50%); }}

/* ── Header ── */
.luxury-header {{
    position: relative;
    text-align: center;
    padding: 60px 20px 40px;
    z-index: 1;
}}

.luxury-header .eyebrow {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 300;
    font-size: 11px;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: #C4A44A;
    margin-bottom: 16px;
    display: block;
}}

.luxury-header h1 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(52px, 8vw, 88px);
    font-weight: 900;
    font-style: italic;
    line-height: 0.9;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #F5EDD6 0%, #C4A44A 40%, #F5EDD6 70%, #C4A44A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}}

.luxury-header .sub {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 18px;
    font-weight: 300;
    color: rgba(245, 237, 214, 0.5);
    letter-spacing: 2px;
}}

.gold-divider {{
    width: 120px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C4A44A, transparent);
    margin: 20px auto;
}}

/* ── Category Grid ── */
.categories-section {{
    position: relative;
    z-index: 1;
    padding: 0 40px 60px;
    max-width: 1200px;
    margin: 0 auto;
}}

.section-label {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #C4A44A;
    text-align: center;
    margin-bottom: 40px;
}}

/* ── Category Card ── */
.cat-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(196,164,74,0.2);
    border-radius: 4px;
    padding: 28px 20px 22px;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}}

.cat-card::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(196,164,74,0.08) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.35s;
}}

.cat-card:hover {{
    border-color: rgba(196,164,74,0.6);
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 30px rgba(196,164,74,0.1);
    background: rgba(255,255,255,0.06);
}}
.cat-card:hover::before {{ opacity: 1; }}

.cat-name {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #F5EDD6;
    margin-top: 14px;
    letter-spacing: 0.5px;
}}

.cat-count {{
    font-size: 10px;
    letter-spacing: 3px;
    color: #C4A44A;
    margin-top: 6px;
    text-transform: uppercase;
}}

/* ── Streamlit button overrides ── */
.stButton > button {{
    background: transparent !important;
    border: 1px solid rgba(196,164,74,0.5) !important;
    color: #C4A44A !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 12px 28px !important;
    border-radius: 2px !important;
    transition: all 0.3s !important;
    width: 100% !important;
    margin-top: 14px !important;
}}

.stButton > button:hover {{
    background: rgba(196,164,74,0.12) !important;
    border-color: #C4A44A !important;
    box-shadow: 0 0 20px rgba(196,164,74,0.15) !important;
    color: #F5EDD6 !important;
}}

.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #C4A44A, #8B6914) !important;
    border: none !important;
    color: #0D0B0E !important;
    font-weight: 600 !important;
    letter-spacing: 3px !important;
    box-shadow: 0 4px 24px rgba(196,164,74,0.25) !important;
}}

.stButton > button[kind="primary"]:hover {{
    background: linear-gradient(135deg, #D4B45A, #9B7924) !important;
    box-shadow: 0 6px 32px rgba(196,164,74,0.4) !important;
    color: #0D0B0E !important;
    transform: translateY(-1px) !important;
}}

/* ── Number input ── */
.stNumberInput > div > div > input {{
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(196,164,74,0.3) !important;
    border-radius: 2px !important;
    color: #F5EDD6 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 22px !important;
    text-align: center !important;
}}
.stNumberInput label {{
    color: rgba(245,237,214,0.6) !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
}}

/* ── Draw Stage ── */
.draw-stage {{
    position: relative;
    z-index: 1;
    padding: 20px 40px 60px;
    max-width: 900px;
    margin: 0 auto;
}}

.draw-meta {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 40px;
}}

.draw-badge {{
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #0D0B0E;
    background: linear-gradient(135deg, #C4A44A, #8B6914);
    padding: 6px 16px;
    border-radius: 1px;
}}

.draw-category-title {{
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-style: italic;
    color: #F5EDD6;
}}

/* ── Slot Machine Card ── */
.slot-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 0;
}}

.slot-card {{
    width: 480px;
    max-width: 90vw;
    height: 200px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(196,164,74,0.3);
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(196,164,74,0.1);
}}

.slot-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C4A44A, transparent);
}}

.slot-card::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,164,74,0.4), transparent);
}}

.slot-name {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(24px, 4vw, 38px);
    font-weight: 700;
    color: #C4A44A;
    letter-spacing: 1px;
    text-align: center;
    padding: 0 20px;
    line-height: 1.2;
}}

.slot-name.spinning {{
    animation: blur-spin 0.08s ease infinite alternate;
}}

.slot-name.revealed {{
    animation: reveal-glow 0.6s ease forwards;
}}

@keyframes blur-spin {{
    from {{ filter: blur(2px); opacity: 0.7; transform: translateY(-2px); }}
    to   {{ filter: blur(0px); opacity: 1;   transform: translateY(2px);  }}
}}

@keyframes reveal-glow {{
    0%   {{ filter: blur(4px); opacity: 0; transform: scale(0.9); }}
    60%  {{ filter: blur(0); opacity: 1; transform: scale(1.05); }}
    100% {{ filter: blur(0); opacity: 1; transform: scale(1); color: #F5EDD6; }}
}}

.slot-label {{
    font-family: 'Montserrat', sans-serif;
    font-size: 8px;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: rgba(196,164,74,0.5);
    margin-top: 10px;
}}

/* ── Winners List ── */
.winners-panel {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(196,164,74,0.15);
    border-radius: 4px;
    padding: 28px 32px;
    margin-top: 10px;
}}

.winners-panel h3 {{
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-style: italic;
    color: #C4A44A;
    letter-spacing: 1px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(196,164,74,0.15);
    padding-bottom: 12px;
}}

.winner-row {{
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    animation: slide-in 0.4s ease forwards;
    opacity: 0;
    transform: translateX(-10px);
}}

@keyframes slide-in {{
    to {{ opacity: 1; transform: translateX(0); }}
}}

.winner-num {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 300;
    color: rgba(196,164,74,0.4);
    min-width: 40px;
    line-height: 1;
}}

.winner-name {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 600;
    color: #F5EDD6;
    letter-spacing: 0.5px;
}}

.winner-trophy {{
    margin-left: auto;
    font-size: 20px;
    filter: grayscale(0.3);
}}

/* ── Back button special ── */
.back-btn .stButton > button {{
    border-color: rgba(255,255,255,0.15) !important;
    color: rgba(245,237,214,0.5) !important;
    font-size: 10px !important;
}}
.back-btn .stButton > button:hover {{
    border-color: rgba(255,255,255,0.3) !important;
    color: #F5EDD6 !important;
    background: transparent !important;
    box-shadow: none !important;
}}

/* ── Confetti canvas ── */
#confetti-canvas {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 9999;
}}

/* ── Streamlit image ── */
[data-testid="stImage"] img {{
    border-radius: 3px;
    border: 1px solid rgba(196,164,74,0.15);
    filter: brightness(0.9) saturate(0.9);
    transition: filter 0.3s;
}}
[data-testid="stImage"] img:hover {{
    filter: brightness(1) saturate(1);
}}

/* ── Responsive ── */
@media (max-width: 768px) {{
    .luxury-header {{ padding: 40px 16px 30px; }}
    .categories-section {{ padding: 0 16px 40px; }}
    .draw-stage {{ padding: 16px 16px 40px; }}
}}
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFETTI JS
# ============================================
CONFETTI_JS = """
<canvas id="confetti-canvas"></canvas>
<script>
(function(){
  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const COLORS = ['#C4A44A','#F5EDD6','#8B1A1A','#1A3A5C','#E8D5A3','#fff'];
  const pieces = Array.from({length:120}, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * -canvas.height,
    w: Math.random()*8+4,
    h: Math.random()*14+6,
    color: COLORS[Math.floor(Math.random()*COLORS.length)],
    rot: Math.random()*Math.PI*2,
    vx: (Math.random()-0.5)*3,
    vy: Math.random()*4+2,
    vr: (Math.random()-0.5)*0.15,
    opacity: Math.random()*0.7+0.3
  }));

  let frame = 0;
  function animate(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    pieces.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.rot += p.vr;
      if(p.y > canvas.height+20){ p.y = -20; p.x = Math.random()*canvas.width; }
      ctx.save();
      ctx.globalAlpha = p.opacity;
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
      ctx.restore();
    });
    frame++;
    if(frame < 220) requestAnimationFrame(animate);
    else { ctx.clearRect(0,0,canvas.width,canvas.height); }
  }
  animate();
})();
</script>
"""

def scroll_top():
    components.html("<script>window.parent.scrollTo(0,0);</script>", height=0)

# ============================================
# AMBIENT ORBS
# ============================================
def ambient_orbs():
    st.markdown("""
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    """, unsafe_allow_html=True)

# ============================================
# PAGE 1 — HOME
# ============================================
if st.session_state.page == "home":

    ambient_orbs()

    st.markdown("""
    <div class="luxury-header">
        <span class="eyebrow">Clayens · Annual Event</span>
        <h1>Tombola</h1>
        <div class="gold-divider"></div>
        <p class="sub">Select a category to begin the draw</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="categories-section">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Categories</p>', unsafe_allow_html=True)

    categories = list(employees_data.keys())
    cols = st.columns(len(categories) if len(categories) <= 4 else 4)

    for i, category in enumerate(categories):
        col_idx = i % len(cols)
        count = len(employees_data[category])
        with cols[col_idx]:
            st.markdown(f"""
            <div class="cat-card">
                <div class="cat-name">{category}</div>
                <div class="cat-count">{count} participant{"s" if count != 1 else ""}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Enter Draw", key=f"cat-{category}"):
                st.session_state.selected_category = category
                st.session_state.winners_list = []
                st.session_state.draw_done = False
                st.session_state.page = "draw"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE 2 — DRAW SCREEN
# ============================================
elif st.session_state.page == "draw":

    ambient_orbs()

    category = st.session_state.selected_category
    people = employees_data[category]

    st.markdown('<div class="draw-stage">', unsafe_allow_html=True)

    # ── Back + Header ──
    col_back, col_title = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="back"):
            st.session_state.page = "home"
            st.session_state.winners_list = []
            st.session_state.draw_done = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_title:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; padding-top:8px;">
            <span class="draw-badge">Draw</span>
            <span class="draw-category-title">{category}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ── Controls ──
    col_n, col_btn = st.columns([2, 3])
    with col_n:
        num_winners = st.number_input(
            "Number of Winners",
            min_value=1,
            max_value=len(people),
            value=1,
            step=1,
            key="num_winners"
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        start = st.button("✦  Begin the Draw  ✦", type="primary", use_container_width=True, key="start_draw")

    # ── Slot Machine Stage ──
    slot_ph = st.empty()

    # ── Idle state ──
    slot_ph.markdown("""
    <div class="slot-wrap">
        <div class="slot-card">
            <div class="slot-name" style="color:rgba(196,164,74,0.3); font-style:italic;">Awaiting draw…</div>
            <div class="slot-label">Ready</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Winners panel ──
    winners_ph = st.empty()

    if st.session_state.winners_list:
        rows_html = "".join([
            f"""<div class="winner-row" style="animation-delay:{j*0.08}s">
                    <span class="winner-num">{"0" if j+1 < 10 else ""}{j+1}</span>
                    <span class="winner-name">{w}</span>
                    <span class="winner-trophy">🏆</span>
                </div>"""
            for j, w in enumerate(st.session_state.winners_list)
        ])
        winners_ph.markdown(f"""
        <div class="winners-panel">
            <h3>✦ Winners</h3>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

    # ── Draw Logic ──
    if start:
        available = people.copy()
        all_winners = []

        for turn in range(1, int(num_winners) + 1):
            scroll_top()

            # Slot spin animation
            for frame in range(28):
                name = random.choice(available)
                speed = 0.08 if frame < 16 else 0.11 + (frame - 16) * 0.01
                slot_ph.markdown(f"""
                <div class="slot-wrap">
                    <div class="slot-card">
                        <div class="slot-name spinning">{textwrap.shorten(name, width=30, placeholder="…")}</div>
                        <div class="slot-label">Drawing #{turn}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(speed)

            # Winner reveal
            winner = random.choice(available)
            available.remove(winner)
            all_winners.append(winner)
            st.session_state.winners_list = all_winners.copy()

            slot_ph.markdown(f"""
            <div class="slot-wrap">
                <div class="slot-card">
                    <div class="slot-name revealed">{textwrap.shorten(winner, width=30, placeholder="…")}</div>
                    <div class="slot-label">Winner #{turn}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confetti on last winner
            if turn == int(num_winners):
                components.html(CONFETTI_JS, height=0)

            # Update winners panel live
            rows_html = "".join([
                f"""<div class="winner-row" style="animation-delay:{j*0.08}s">
                        <span class="winner-num">{"0" if j+1 < 10 else ""}{j+1}</span>
                        <span class="winner-name">{w}</span>
                        <span class="winner-trophy">🏆</span>
                    </div>"""
                for j, w in enumerate(all_winners)
            ])
            winners_ph.markdown(f"""
            <div class="winners-panel">
                <h3>✦ Winners</h3>
                {rows_html}
            </div>
            """, unsafe_allow_html=True)

            time.sleep(3)

        st.session_state.draw_done = True

    st.markdown('</div>', unsafe_allow_html=True)