import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os
import base64

# --- Settings ---
DB_FILE = "growth_data.csv"
PLANTS = ["🌻", "🌷", "🌹", "🌺", "🌸", "🌼", "🌽", "🥕", "🍓", "🍎", "🥦", "🍅", "🍄"]
ANIMALS = ["🦋", "🐝", "🐥", "🐰", "🦊", "🦌", "🐿️", "🦄", "🦥", "🐣"]

# Matches your filename in the repository exactly
LOCAL_IMAGE_PATH = "Hpylng _background.png"

# --- Database Setup ---
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Language", "Minutes", "Icon", "PosX", "PosY"])
    df.to_csv(DB_FILE, index=False)

def load_data():
    df = pd.read_csv(DB_FILE)
    # SELF-HEALING: If PosX or PosY are missing from old data, add them randomly
    if "PosX" not in df.columns:
        df["PosX"] = [random.randint(5, 90) for _ in range(len(df))]
    if "PosY" not in df.columns:
        df["PosY"] = [random.randint(65, 85) for _ in range(len(df))]
        # Save fixed version back to disk
        df.to_csv(DB_FILE, index=False)
    return df

def add_entry(lang, mins):
    icon = random.choice(ANIMALS if random.random() > 0.8 else PLANTS)
    pos_x = random.randint(5, 90)
    pos_y = random.randint(65, 85)
    
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), lang, mins, icon, pos_x, pos_y]], 
                            columns=["Date", "Language", "Minutes", "Icon", "PosX", "PosY"])
    new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
    return icon

# --- Background Image Helper ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Dashboard UI ---
st.set_page_config(page_title="My Happy Language Garden", layout="wide")

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
        border-radius: 20 Re0px;
        position: relative;
        border: 4px solid #5d4037;
        margin-bottom: 20px;
        overflow: hidden;
    }}
    .emoji-item {{
        position: absolute;
        font-size: 50px;
        transition: all 0.5s ease-in-out;
        filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.4));
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🌳 My Happy Language Growth Garden")

with st.sidebar:
    st.header("Log Your Progress")
    language = st.selectbox("Language", ["English", "German"])
    minutes = st.number_input("Speaking Time (min)", min_value=1, value=30)
    if st.button("Plant in Garden"):
        add_entry(language, minutes)
        st.success("Wonderful!!")
        st.balloons()

# Load data and fix missing columns if necessary
data = load_data()

col1, col2 = st.columns(2)
col1.metric("English Total", f"{data[data['Language']=='English']['Minutes'].sum()} min")
col2.metric("German Total", f"{data[data['Language']=='German']['Minutes'].sum()} min")

# Render the Garden
garden_html = '<div class="garden-container">'
for _, row in data.iterrows():
    garden_html += f'<div class="emoji-item" style="left: {row["PosX"]}%; top: {row["PosY"]}%;">{row["Icon"]}</div>'
garden_html += '</div>'

st.markdown(garden_html, unsafe_allow_html=True)

with st.expander("View Amazing Achievement History"):
    st.dataframe(data)
