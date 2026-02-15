import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ---------------- PAGE SETUP ---------------- #
st.set_page_config(page_title="SafeTab Pro", layout="wide")
st.title("🛡️ SafeTab: Smart Search & Sync")

# ---------------- GOOGLE SHEETS CONNECTION ---------------- #
conn = st.connection("gsheets", type=GSheetsConnection)

# ---------------- SIDEBAR: RECORD SUBMISSION ---------------- #
st.sidebar.header("📥 Record Submission")

with st.sidebar.form("input_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    tab_id = st.text_input("Tablet ID")
    submitted = st.form_submit_button("Log Tablet")

# ---------------- HANDLE FORM SUBMISSION ---------------- #
if submitted and name and tab_id:
    
    # Read existing sheet data
    try:
        df = conn.read(ttl=0)
    except:
        df = pd.DataFrame(columns=["Name", "Tablet ID", "Time", "Date"])

    # Create new entry
    new_entry = pd.DataFrame([{
        "Name": name,
        "Tablet ID": tab_id,
        "Time": datetime.now().strftime("%H:%M"),
        "Date": datetime.now().strftime("%Y-%m-%d")
    }])

    # Append new entry
    updated_df = pd.concat([df, new_entry], ignore_index=True)

    # Update Google Sheet
    conn.update(data=updated_df)

    st.sidebar.success(f"✅ Logged successfully: {name}")
    st.rerun()

# ---------------- MAIN PAGE: DISPLAY DATA ---------------- #
st.subheader("🔍 Current Logs")

try:
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True)
except:
    st.info("No records found yet. Log your first tablet!")
