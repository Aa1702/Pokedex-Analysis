import streamlit as st
import sqlite3
import pandas as pd
import base64
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Sky Pokedex", layout="wide", initial_sidebar_state="collapsed")

# ---------- 1. BASE DIRECTORY ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- 2. BACKGROUND ----------
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

background_path = os.path.join(BASE_DIR, "images", "background.png")
bg_base64 = get_base64(background_path)

# ---------- 3. CSS ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

[data-testid="stSidebar"] {{ display: none; }}
[data-testid="stHeader"] {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

.stApp {{
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: 500px;
    background-repeat: repeat;
    animation: moveClouds 60s linear infinite;
}}

@keyframes moveClouds {{
    from {{ background-position: 0 0; }}
    to {{ background-position: 1000px 0; }}
}}

img {{
    image-rendering: pixelated !important;
    image-rendering: crisp-edges !important;
}}

div.stButton button {{
    background: transparent !important;
    border: none !important;
    margin-top: -10px !important;
    width: 100% !important;
}}

div.stButton button p {{
    font-family: 'Press Start 2P' !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    color: #2c3e50 !important;
    margin: 0 !important;
}}

div.stButton > button:hover {{
    color: #000 !important;
    transform: scale(1.1);
}}

[data-testid="stImage"] {{
    display: flex;
    justify-content: center;
    align-items: center;
}}
</style>
""", unsafe_allow_html=True)

# ---------- 4. DATABASE ----------
db_path = os.path.join(BASE_DIR, "data", "pokedex.db")

if not os.path.exists(db_path):
    st.error(f"Database not found at: {db_path}")
    st.stop()

conn = sqlite3.connect(db_path)
df = pd.read_sql("SELECT * FROM pokemon", conn)
conn.close()

# ---------- 5. SESSION STATE ----------
if "category" not in st.session_state:
    st.session_state.category = "attack"

# ---------- 6. ICON BUTTON ----------
def icon_button(col, file_name, label, key, stat_slug):
    with col:
        img_path = os.path.join(BASE_DIR, "images", file_name)

        if os.path.exists(img_path):
            st.image(img_path, width=100)

        if st.button(label, key=key):
            st.session_state.category = stat_slug
            st.rerun()

# ---------- 7. TITLE ----------
st.markdown(f"""
<div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
    <h1 style="color: #2c3e50; text-shadow: 4px 4px 0 #ffffff; font-family: 'Press Start 2P'; font-size: 35px;">
        ✨ {st.session_state.category.upper()} SQUAD ✨
    </h1>
</div>
""", unsafe_allow_html=True)

# ---------- 8. NAVIGATION ----------
spacer_left, col1, col2, col3, col4, spacer_right = st.columns([3,1,1,1,1,3])

icon_button(col1, "image1.png", "Attack",  "atk_btn", "attack")
icon_button(col2, "image2.png", "Defense", "def_btn", "defense")
icon_button(col3, "image3.png", "Speed",   "spd_btn", "speed")
icon_button(col4, "image4.png", "HP",      "hp_btn",  "hp")

# ---------- 9. DATA & CHART ----------
current_stat = st.session_state.category
top_8 = df.sort_values(by=current_stat, ascending=False).head(8)
max_val = df[current_stat].max()

bars_html = ""

for _, p in top_8.iterrows():
    stat_value = p[current_stat]
    percent = (stat_value / max_val) * 100
    sprite = p["sprite_url"] if p["sprite_url"] else ""
    cry = p["cry_url"] if p["cry_url"] else ""
    poke_name = p["name"]

    bars_html += f"""
    <div onclick="interact('{poke_name}', '{percent}%')" style="cursor:pointer;display:flex;flex-direction:column;align-items:center;width:100px;">
        <div style="height:250px;width:45px;display:flex;align-items:flex-end;justify-content:center;position:relative;">
            <div id="val-{poke_name}" class="stat-number">{stat_value}</div>
            <div id="bar-{poke_name}" class="pixel-bar"></div>
        </div>
        <img id="img-{poke_name}" src="{sprite}" class="poke-img">
        <div class="name-tag">{poke_name.title()}</div>
        <audio id="audio-{poke_name}" src="{cry}"></audio>
    </div>
    """

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
body {{ background: transparent; margin:0; overflow:hidden; }}
.container {{
    display:flex;
    justify-content:center;
    gap:15px;
    align-items:flex-end;
    height:450px;
    padding-bottom:20px;
}}
.pixel-bar {{
    width:100%;
    background:linear-gradient(180deg,#fff 0%,#ff9ff3 100%);
    border:3px solid #fff;
    border-radius:10px;
    box-shadow:0 0 10px rgba(255,255,255,0.6);
    height:0%;
    transition:height 1s cubic-bezier(0.175,0.885,0.32,1.275);
    position:relative;
}}
.stat-number {{
    position:absolute;
    top:-30px;
    width:100%;
    text-align:center;
    font-family:'Press Start 2P';
    font-size:12px;
    color:#2c3e50;
    text-shadow:2px 2px 0px #fff;
    opacity:0;
    transition:opacity 0.5s ease-in;
    z-index:10;
}}
.poke-img {{
    width:85px;
    image-rendering:pixelated;
    filter:drop-shadow(0 0 5px #fff);
    transition:transform 0.2s;
    margin-top:10px;
}}
.name-tag {{
    margin-top:5px;
    font-size:10px;
    color:#2c3e50;
    text-shadow:1px 1px 0 #fff;
    background:rgba(255,255,255,0.9);
    padding:6px 12px;
    border-radius:20px;
    font-family:'Press Start 2P';
    font-weight:bold;
}}
</style>
</head>
<body>
<div class="container">{bars_html}</div>
<script>
function interact(name, height) {{
    var audio = document.getElementById("audio-" + name);
    if(audio) {{ audio.volume = 0.5; audio.play(); }}

    var img = document.getElementById("img-" + name);
    if(img) {{
        img.style.transform = "scale(1.4) translateY(-10px)";
        setTimeout(() => {{
            img.style.transform = "scale(1) translateY(0)";
        }}, 300);
    }}

    var bar = document.getElementById("bar-" + name);
    var val = document.getElementById("val-" + name);

    if(bar) {{
        if(bar.style.height === height) {{
            bar.style.height = "0%";
            val.style.opacity = "0";
        }} else {{
            bar.style.height = height;
            setTimeout(() => {{
                val.style.opacity = "1";
            }}, 300);
        }}
    }}
}}
</script>
</body>
</html>
""", height=500)