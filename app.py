import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

# --- CONFIGURATION ---
DB_FILE = "growth_data.csv"
PLANTS = ["🌻", "🌷", "🌹", "🌺", "🌸", "🌼", "🌽", "🥕", "🍓", "🍎", "🥦", "🍇","🍄","🍅"]
ANIMALS = ["🦋", "🐝", "🐥", "🐰", "🦊", "🦌", "🐿️","🐣","🦄"]

# Initialize data file if it doesn't exist
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Language", "Minutes", "Icon"])
    df.to_csv(DB_FILE, index=False)

def load_data():
    return pd.read_csv(DB_FILE)

def add_entry(lang, mins):
    # Randomly pick an icon: 80% chance for plants, 20% for animals
    icon = random.choice(ANIMALS if random.random() > 0.8 else PLANTS)
    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), lang, mins, icon]], 
                            columns=["Date", "Language", "Minutes", "Icon"])
    new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
    return icon

# --- DASHBOARD UI ---
st.set_page_config(page_title="Language Garden", layout="wide")
st.title("🌱 My Language Growth Garden")

# Sidebar for inputs
with st.sidebar:
    st.header("Log Your Lesson")
    language = st.selectbox("Language", ["English", "German"])
    minutes = st.number_input("Minutes Spoken", min_value=1, max_value=300, value=30)
    
    if st.button("Add to Garden"):
        new_icon = add_entry(language, minutes)
        st.success(f"Added a {new_icon} to your garden!")
        st.balloons()

# Load and process data
data = load_data()

# Statistics Row
col1, col2, col3 = st.columns(3)
col1.metric("Total English", f"{data[data['Language']=='English']['Minutes'].sum()} mins")
col2.metric("Total German", f"{data[data['Language']=='German']['Minutes'].sum()} mins")
col3.metric("Garden Size", f"{len(data)} Items")

# --- THE GARDEN DISPLAY ---
st.subheader("Your Living Achievement Garden")
if not data.empty:
    # Join all icons into a "garden" string
    garden_display = " ".join(data['Icon'].tolist())
    st.markdown(f"<div style='font-size: 50px; line-height: 1.5; letter-spacing: 10px;'>{garden_display}</div>", 
                unsafe_allow_html=True)
else:
    st.info("Your garden is empty. Start speaking to plant some seeds!")

# Recent History Table
with st.expander("View Lesson History"):
    st.table(data.tail(10))
