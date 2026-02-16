import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="SafeTab Pro", layout="wide")
st.title("🛡️ SafeTab: Smart Search & Sync")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
URL = "https://docs.google.com/spreadsheets/d/1-1hSN2Us6wTdrhKiwy_58AlVZHX6kwjxPPrGWnpocN4/edit"

# SIDEBAR: RECORD SUBMISSION
st.sidebar.header("📥 Record Submission")
with st.sidebar.form("input_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    tab_id = st.text_input("Tablet ID")
    submitted = st.form_submit_button("Log Tablet")

if submitted and name and tab_id:
    # Read with ttl=0 to bypass cache
    df = conn.read(spreadsheet=URL, ttl=0)
    
    new_entry = pd.DataFrame([{
        "Name": name, 
        "Tablet ID": tab_id, 
        "Time": datetime.now().strftime("%H:%M"), 
        "Date": datetime.now().strftime("%Y-%m-%d")
    }])
    
    updated_df = pd.concat([df, new_entry], ignore_index=True)
    
    # Force the update using the explicit URL
    conn.update(spreadsheet=URL, data=updated_df)
    
    st.sidebar.success(f"✅ Verified: {name}")
    st.rerun()

# MAIN PAGE: VIEW DATA
try:
    data = conn.read(spreadsheet=URL, ttl=0)
    st.subheader("🔍 Current Logs")
    st.dataframe(data, use_container_width=True)
except Exception as e:
    st.info("System Ready. Please log a tablet to begin.")
