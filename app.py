import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

# --- Settings ---
DB_FILE = "growth_data.csv"
PLANTS = ["🌻", "🌷", "🌹", "🌺", "🌸", "🌼", "🌽", "🥕", "🍓", "🍎", "🥦", "🍅","🍄"]
ANIMALS = ["🦋", "🐝", "🐥", "🐰", "🦊", "🦌", "🐿️","🦄","🦥","🐣"]

# Change the URL 
##GARDEN_IMAGE = "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?q=80&w=2000&auto=format&fit=crop"

LOCAL_IMAGE_PATH = "Hpylng _background.png"

if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Language", "Minutes", "Icon", "PosX", "PosY"])
    df.to_csv(DB_FILE, index=False)

def load_data():
    return pd.read_csv(DB_FILE)

def add_entry(lang, mins):
    icon = random.choice(ANIMALS if random.random() > 0.8 else PLANTS)
    #decide the random location in garden
    pos_x = random.randint(5, 90)
    pos_y = random.randint(60, 90)
    
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), lang, mins, icon, pos_x, pos_y]], 
                            columns=["Date", "Language", "Minutes", "Icon", "PosX", "PosY"])
    new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
    return icon

# --- background design ---
st.set_page_config(page_title="My Language Garden", layout="wide")

# to fix background and letter using CSS
st.markdown(f"""
    <style>
    .garden-container {{
        background-image: url("{GARDEN_IMAGE}");
        background-size: cover;
        background-position: center;
        height: 500px;
        border-radius: 20px;
        position: relative;
        border: 5px solid #2e7d32;
        margin-bottom: 20px;
        overflow: hidden;
    }}
    .emoji-item {{
        position: absolute;
        font-size: 40px;
        transition: all 0.5s ease-in-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🌳 My Language Growth Garden")

# sider bar setting
with st.sidebar:
    st.header("Record your learning")
    language = st.selectbox("Language", ["English", "German"])
    minutes = st.number_input("Time", min_value=1, value=30)
    if st.button("Add garden"):
        add_entry(language, minutes)
        st.balloons()

# Reading data
data = load_data()

# statistics
c1, c2 = st.columns(2)
c1.metric("English Total", f"{data[data['Language']=='English']['Minutes'].sum()} min")
c2.metric("German Total", f"{data[data['Language']=='German']['Minutes'].sum()} min")

# --- Show Garden ---
#use HTML
garden_html = '<div class="garden-container">'
for _, row in data.iterrows():
    garden_html += f'<div class="emoji-item" style="left: {row["PosX"]}%; top: {row["PosY"]}%;">{row["Icon"]}</div>'
garden_html += '</div>'

st.markdown(garden_html, unsafe_allow_html=True)

# history
with st.expander("Check your amazing achievement!"):
    st.dataframe(data)
