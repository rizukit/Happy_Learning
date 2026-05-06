import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os
import base64
import math

# --- Configuration & Assets ---
DB_FILE = "growth_data.csv"
PLANTS = ["🌻", "🌷", "🌹", "🌺", "🌸", "🌼", "🌽", "🥕", "🍓", "🍎", "🥦", "🍅", "🍄", "🍀"]
ANIMALS = ["🦋", "🐝", "🐥", "🪿", "🦊", "🦌", "🐿️", "🦄", "🦥", "🐣", "🦕", "🦓", "🐕", "🦩", "🦜"]
# Ensure this filename exactly matches your GitHub upload
LOCAL_IMAGE_PATH = "Hpylng _background2.png"

# --- Database Operations ---
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Language", "Minutes", "Icon", "PosX", "PosY"])
    df.to_csv(DB_FILE, index=False)

def load_data():
    df = pd.read_csv(DB_FILE)
    # Self-healing for missing coordinate columns
    if "PosX" not in df.columns:
        df["PosX"] = [random.randint(5, 90) for _ in range(len(df))]
    if "PosY" not in df.columns:
        df["PosY"] = [random.randint(65, 85) for _ in range(len(df))]
        df.to_csv(DB_FILE, index=False)
    return df

def add_entry(lang, mins):
    icon = random.choice(ANIMALS if random.random() > 0.8 else PLANTS)
    existing_data = load_data()
    
    # Coordinates of gnomes to avoid (Percentage of background)
    gnome_zones = [
        {'x': [10, 30], 'y': [75, 95]},  # Left gnome
        {'x': [55, 85], 'y': [65, 85]},  # Right gnomes
    ]
    
    # Buffer distance between emojis (in % units)
    min_dist_between_emojis = 8 
    max_attempts = 100
    
    # Default position in case we can't find a perfect spot
    final_pos = (random.randint(5, 90), random.randint(65, 85))
    
    for _ in range(max_attempts):
        test_x = random.randint(5, 90)
        test_y = random.randint(65, 85)
        
        # Check 1: Gnome Collision
        hits_gnome = any(
            z['x'][0] <= test_x <= z['x'][1] and z['y'][0] <= test_y <= z['y'][1] 
            for z in gnome_zones
        )
        
        # Check 2: Emoji Collision (Check distance to all existing items)
        hits_emoji = False
        for _, row in existing_data.iterrows():
            distance = math.sqrt((test_x - row['PosX'])**2 + (test_y - row['PosY'])**2)
            if distance < min_dist_between_emojis:
                hits_emoji = True
                break
        
        if not hits_gnome and not hits_emoji:
            final_pos = (test_x, test_y)
            break
            
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), lang, mins, icon, final_pos[0], final_pos[1]]], 
                            columns=["Date", "Language", "Minutes", "Icon", "PosX", "PosY"])
    new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
    return icon

# --- Background Image Processing ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Application Layout ---
st.set_page_config(page_title="My Language Garden", layout="wide")

if os.path.exists(LOCAL_IMAGE_PATH):
    img_base64 = get_base64_of_bin_file(LOCAL_IMAGE_PATH)
    background_css = f'background-image: url("data:image/png;base64,{img_base64}");'
else:
    background_css = 'background-color: #f0f2f6;'

st.markdown(f"""
    <style>
    .garden-container {{
        {background_css}
        background-size: cover;
        background-position: center bottom;
        height: 600px;
        border-radius: 20px;
        position: relative;
        border: 4px solid #5d4037;
        margin-bottom: 20px;
        overflow: hidden;
    }}
    .emoji-item {{
        position: absolute;
        font-size: 50px;
        transform: translate(-50%, -50%);
        transition: all 0.5s ease-in-out;
        filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.4));
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🌳 My Language Growth Garden 🌳")

# --- Sidebar Management ---
with st.sidebar:
    st.header("Log Your Progress")
    language = st.selectbox("Language", ["English", "German"])
    minutes = st.number_input("Speaking Time (min)", min_value=1, value=30)
    
    if st.button("Plant in Garden"):
        add_entry(language, minutes)
        st.success("Wonderful!!") 
        st.balloons()
        st.rerun()

# --- Visualization & Editing ---
data = load_data()

col1, col2 = st.columns(2)
col1.metric("English Total", f"{data[data['Language']=='English']['Minutes'].sum()} min")
col2.metric("German Total", f"{data[data['Language']=='German']['Minutes'].sum()} min")

# Render Garden
garden_html = '<div class="garden-container">'
for _, row in data.iterrows():
    garden_html += f'<div class="emoji-item" style="left: {row["PosX"]}%; top: {row["PosY"]}%;">{row["Icon"]}</div>'
garden_html += '</div>'
st.markdown(garden_html, unsafe_allow_html=True)

# History Management Table
st.subheader("Manage Your Achievements")
st.info("💡 Edit minutes directly or select a row and press 'Delete' to remove an entry.")

edited_data = st.data_editor(
    data, 
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Icon": st.column_config.Column(disabled=True),
        "PosX": st.column_config.Column(disabled=True),
        "PosY": st.column_config.Column(disabled=True),
        "Date": st.column_config.Column(disabled=True),
    }
)

if not edited_data.equals(data):
    edited_data.to_csv(DB_FILE, index=False)
    st.rerun()
