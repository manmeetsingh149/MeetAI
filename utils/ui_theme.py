"""Inject MeetAi theme (teal / amber / indigo) for Streamlit."""


def inject_theme() -> None:
    import streamlit as st

    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;0,9..40,800&family=Sora:wght@400;600;700;800&display=swap');

:root {
    --bg-deep: #040a0f;
    --bg: #081218;
    --surface: rgba(10, 28, 36, 0.78);
    --surface-2: rgba(14, 38, 48, 0.88);
    --border: rgba(20, 184, 166, 0.22);
    --accent: #14b8a6;
    --accent-2: #f59e0b;
    --accent-3: #818cf8;
    --accent-4: #fb923c;
    --glow-primary: rgba(20, 184, 166, 0.5);
    --glow-secondary: rgba(245, 158, 11, 0.4);
    --text: #ecfdf8;
    --text-muted: #8fb8b0;
    --success: #22c55e;
    --accent-rgb: 20, 184, 166;
    --accent-2-rgb: 245, 158, 11;
    --accent-3-rgb: 129, 140, 248;
}

/* ── Animated aurora background ── */
.stApp {
    background: var(--bg-deep) !important;
    position: relative;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 15% -10%, rgba(20,184,166,0.32) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 92% 8%, rgba(245,158,11,0.22) 0%, transparent 50%),
        radial-gradient(ellipse 50% 60% at 50% 100%, rgba(129,140,248,0.18) 0%, transparent 55%),
        linear-gradient(180deg, #040a0f 0%, #081218 45%, #0c1f24 100%);
    animation: auroraShift 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(var(--accent-rgb),0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(var(--accent-rgb),0.05) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse at center, black 20%, transparent 75%);
    pointer-events: none;
    z-index: 0;
    animation: gridDrift 20s linear infinite;
}

@keyframes auroraShift {
    0% { filter: hue-rotate(0deg) brightness(1); }
    100% { filter: hue-rotate(18deg) brightness(1.08); }
}

@keyframes gridDrift {
    0% { transform: translateY(0); }
    100% { transform: translateY(48px); }
}

/* Floating orbs */
.orb-layer {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

/* Keep decorative layers behind all Streamlit widgets */
.stApp::before,
.stApp::after {
    z-index: 0 !important;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.5;
    animation: orbFloat 8s ease-in-out infinite;
}
.orb-1 { width: 320px; height: 320px; background: #14b8a6; top: -80px; left: -60px; animation-delay: 0s; }
.orb-2 { width: 280px; height: 280px; background: #f59e0b; top: 40%; right: -100px; animation-delay: -3s; }
.orb-3 { width: 240px; height: 240px; background: #6366f1; bottom: -60px; left: 30%; animation-delay: -5s; }

@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(30px, -20px) scale(1.05); }
    66% { transform: translate(-20px, 25px) scale(0.95); }
}

/* Main content and sidebar above fixed aurora layers */
[data-testid="stAppViewContainer"],
[data-testid="stSidebar"],
section.main,
.block-container {
    position: relative;
    z-index: 2;
}

.block-container {
    padding-top: 2rem !important;
    max-width: 1200px !important;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Sora', sans-serif !important;
}

/* Sidebar glass */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(6,18,24,0.97) 0%, rgba(4,10,15,0.99) 100%) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 40px rgba(var(--accent-rgb),0.12) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Hero */
.hero-wrap {
    text-align: center;
    padding: 2rem 1rem 2.5rem;
    animation: fadeSlideUp 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.hero-title {
    font-family: 'Sora', sans-serif !important;
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    margin: 0;
    background: linear-gradient(
        120deg,
        #fff 0%,
        #99f6e4 18%,
        #14b8a6 38%,
        #f59e0b 58%,
        #a5b4fc 78%,
        #fff 100%
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmerText 4s linear infinite;
    filter: drop-shadow(0 0 30px rgba(var(--accent-rgb),0.35));
}

.hero-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin-top: 1rem;
    animation: fadeSlideUp 0.8s 0.15s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.hero-pills {
    display: flex;
    gap: 0.6rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1.5rem;
    animation: fadeSlideUp 0.8s 0.3s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes shimmerText {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Glass cards */
.card {
    background: linear-gradient(135deg, rgba(12,32,40,0.8) 0%, rgba(6,16,22,0.9) 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.35s ease, border-color 0.35s ease;
    animation: cardEnter 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3), var(--accent));
    background-size: 200% 100%;
    animation: borderFlow 3s linear infinite;
}

.card::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(var(--accent-rgb),0.1) 0%, transparent 50%);
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
}

.card:hover {
    transform: translateY(-6px) scale(1.01);
    border-color: rgba(var(--accent-rgb),0.45);
    box-shadow:
        0 20px 50px rgba(0,0,0,0.4),
        0 0 40px var(--glow-primary),
        inset 0 1px 0 rgba(255,255,255,0.06);
}

.card:hover::after { opacity: 1; }

.card-delay-1 { animation-delay: 0.1s; }
.card-delay-2 { animation-delay: 0.2s; }
.card-delay-3 { animation-delay: 0.3s; }
.card-delay-4 { animation-delay: 0.4s; }
.card-delay-5 { animation-delay: 0.5s; }

@keyframes cardEnter {
    from { opacity: 0; transform: translateY(20px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes borderFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

.card-title {
    font-family: 'Sora', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent-2);
    margin-bottom: 0.85rem;
}

.card-content {
    font-size: 0.9rem;
    line-height: 1.75;
    color: var(--text);
}

.card-title-lg {
    font-family: 'Sora', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff, #5eead4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    animation: badgePulse 2.5s ease-in-out infinite;
}
.badge-teal {
    background: linear-gradient(135deg, rgba(20,184,166,0.35), rgba(13,148,136,0.2));
    color: #99f6e4;
    border: 1px solid rgba(20,184,166,0.5);
    box-shadow: 0 0 20px rgba(20,184,166,0.25);
}
.badge-amber {
    background: linear-gradient(135deg, rgba(245,158,11,0.32), rgba(217,119,6,0.15));
    color: #fde68a;
    border: 1px solid rgba(245,158,11,0.45);
    box-shadow: 0 0 20px rgba(245,158,11,0.2);
    animation-delay: 0.3s;
}
.badge-green {
    background: linear-gradient(135deg, rgba(34,197,94,0.3), rgba(22,163,74,0.15));
    color: #86efac;
    border: 1px solid rgba(34,197,94,0.45);
    box-shadow: 0 0 20px rgba(34,197,94,0.2);
    animation-delay: 0.6s;
}
.badge-indigo {
    background: linear-gradient(135deg, rgba(129,140,248,0.35), rgba(99,102,241,0.15));
    color: #c7d2fe;
    border: 1px solid rgba(129,140,248,0.45);
    animation-delay: 0.9s;
}

@keyframes badgePulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 15px rgba(var(--accent-rgb),0.2); }
    50% { transform: scale(1.04); box-shadow: 0 0 25px rgba(var(--accent-rgb),0.35); }
}

/* Status pipeline */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 0.85rem 1.1rem;
    background: rgba(8,24,32,0.65);
    border-radius: 12px;
    margin: 0.45rem 0;
    border: 1px solid rgba(var(--accent-rgb),0.15);
    font-size: 0.82rem;
    transition: all 0.3s ease;
    animation: fadeSlideUp 0.5s ease both;
}
.status-bar:hover {
    background: rgba(12,32,42,0.85);
    border-color: rgba(var(--accent-rgb),0.35);
    transform: translateX(4px);
}

.status-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-active {
    background: var(--accent-2);
    box-shadow: 0 0 12px var(--glow-secondary), 0 0 24px var(--glow-secondary);
    animation: dotPulse 1.2s ease-in-out infinite;
}
.dot-done {
    background: var(--success);
    box-shadow: 0 0 10px rgba(52,211,153,0.6);
    animation: dotPop 0.4s ease;
}
.dot-pending { background: rgba(var(--accent-rgb),0.15); border: 1px solid rgba(var(--accent-rgb),0.28); }

@keyframes dotPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.7; }
}
@keyframes dotPop {
    0% { transform: scale(0); }
    70% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

/* Chat */
.chat-container {
    background: linear-gradient(160deg, rgba(10,28,36,0.92), rgba(4,12,18,0.96));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    max-height: 440px;
    overflow-y: auto;
    margin-bottom: 1rem;
    box-shadow: inset 0 0 60px rgba(var(--accent-rgb),0.06);
    animation: cardEnter 0.6s 0.2s both;
}

.chat-msg {
    margin-bottom: 1.1rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    animation: msgSlide 0.4s ease both;
}

@keyframes msgSlide {
    from { opacity: 0; transform: translateX(12px); }
    to { opacity: 1; transform: translateX(0); }
}

.chat-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.user-label { color: var(--accent-3); }
.bot-label { color: var(--accent-2); }

.chat-bubble {
    display: inline-block;
    padding: 0.75rem 1.15rem;
    border-radius: 16px;
    font-size: 0.88rem;
    line-height: 1.65;
    max-width: 88%;
    transition: transform 0.2s ease;
}
.chat-bubble:hover { transform: scale(1.02); }

.user-bubble {
    background: linear-gradient(135deg, rgba(var(--accent-rgb),0.32), rgba(13,148,136,0.18));
    border: 1px solid rgba(var(--accent-rgb),0.4);
    align-self: flex-end;
    box-shadow: 0 4px 20px rgba(var(--accent-rgb),0.2);
}
.bot-bubble {
    background: linear-gradient(135deg, rgba(var(--accent-2-rgb),0.22), rgba(217,119,6,0.08));
    border: 1px solid rgba(var(--accent-2-rgb),0.35);
    align-self: flex-start;
    box-shadow: 0 4px 20px rgba(var(--accent-2-rgb),0.15);
}

/* Empty state */
.empty-hero {
    text-align: center;
    padding: 4rem 2rem;
    animation: fadeSlideUp 0.9s ease both;
}
.empty-icon {
    font-size: 5rem;
    display: inline-block;
    animation: iconBounce 2.5s ease-in-out infinite;
    filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),0.45));
}
@keyframes iconBounce {
    0%, 100% { transform: translateY(0) rotate(-5deg); }
    50% { transform: translateY(-16px) rotate(5deg); }
}
.empty-title {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    margin: 1rem 0 0.5rem;
    background: linear-gradient(135deg, #fff, #14b8a6, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.empty-desc {
    color: var(--text-muted);
    font-size: 0.95rem;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.8;
}

/* Feature rings */
.feature-ring {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 2.5rem;
    flex-wrap: wrap;
}
.feature-item {
    text-align: center;
    animation: fadeSlideUp 0.8s ease both;
}
.feature-icon {
    width: 64px; height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    margin: 0 auto 0.6rem;
    border: 2px solid var(--border);
    background: rgba(10,28,36,0.65);
    animation: ringSpin 8s linear infinite;
    box-shadow: 0 0 30px rgba(var(--accent-rgb),0.2);
}
.feature-item:nth-child(2) .feature-icon { animation-delay: -2s; border-color: rgba(var(--accent-2-rgb),0.45); }
.feature-item:nth-child(3) .feature-icon { animation-delay: -4s; border-color: rgba(var(--accent-3-rgb),0.45); }
.feature-label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
}

@keyframes ringSpin {
    0% { box-shadow: 0 0 20px rgba(var(--accent-rgb),0.3); }
    50% { box-shadow: 0 0 35px rgba(var(--accent-2-rgb),0.4); }
    100% { box-shadow: 0 0 20px rgba(var(--accent-rgb),0.3); }
}

/* Transcript */
.transcript-box {
    background: rgba(4,14,20,0.85);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    font-size: 0.84rem;
    line-height: 1.85;
    max-height: 320px;
    overflow-y: auto;
    color: var(--text-muted);
}

/* Streamlit widgets */
.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    background: rgba(8,22,30,0.85) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(var(--accent-rgb),0.25), 0 0 20px rgba(var(--accent-rgb),0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #14b8a6 0%, #0d9488 45%, #0891b2 100%) !important;
    background-size: 200% auto !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1) !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 20px rgba(var(--accent-rgb),0.4) !important;
    animation: btnGlow 3s ease-in-out infinite !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 35px rgba(var(--accent-rgb),0.5), 0 0 30px rgba(var(--accent-2-rgb),0.28) !important;
    background-position: right center !important;
}
.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

@keyframes btnGlow {
    0%, 100% { box-shadow: 0 4px 20px rgba(var(--accent-rgb),0.4); }
    50% { box-shadow: 0 4px 28px rgba(var(--accent-2-rgb),0.35); }
}

.stButton > button[kind="secondary"] {
    background: rgba(10,28,36,0.85) !important;
    border: 1px solid var(--border) !important;
    animation: none !important;
}

[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    box-shadow: 0 4px 20px rgba(var(--accent-2-rgb),0.35) !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important;
    animation: progressShine 2s linear infinite !important;
}
@keyframes progressShine {
    0% { filter: brightness(1); }
    50% { filter: brightness(1.3); }
    100% { filter: brightness(1); }
}

.stSpinner > div { border-top-color: var(--accent-2) !important; }

div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(10px);
    animation: fadeSlideUp 0.4s ease both;
}

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent-2), transparent) !important;
    margin: 2rem 0 !important;
    opacity: 0.6;
}

[data-testid="stExpander"] {
    background: rgba(8,22,30,0.65) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
    border-radius: 8px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-3); }

.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(90deg, #fff, var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeSlideUp 0.6s ease both;
}

.sidebar-brand {
    padding: 0.5rem 0 1rem;
    animation: fadeSlideUp 0.6s ease both;
}

[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label, .stSelectbox label { color: var(--text-muted) !important; font-size: 0.8rem !important; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
}
</style>

<div class="orb-layer" aria-hidden="true">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>
""",
        unsafe_allow_html=True,
    )
