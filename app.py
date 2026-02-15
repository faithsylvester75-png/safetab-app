import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="SafeTab Pro", layout="wide")
st.title("🛡️ SafeTab: Smart Search & Sync")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
URL = "PASTE_YOUR_GOOGLE_SHEET_URL_HERE"

# --- SIDEBAR: NEW SUBMISSION ---
st.sidebar.header("📥 Record Submission")
with st.sidebar.form("input_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    tab_id = st.text_input("Tablet ID")
    submitted = st.form_submit_button("Log Tablet")

if submitted and name and tab_id:
    df = conn.read(spreadsheet=URL)
    new_entry = pd.DataFrame([{"Name": name, "Tablet ID": tab_id, "Time": datetime.now().strftime("%H:%M"), "Date": datetime.now().strftime("%Y-%m-%d")}])
    updated_df = pd.concat([df, new_entry], ignore_index=True)
    conn.update(spreadsheet=URL, data=updated_df)
    st.sidebar.success(f"Verified: {name}")

# --- MAIN PAGE: SEARCH & VIEW ---
# Load data
data = conn.read(spreadsheet=URL)

# Search Functionality
st.subheader("🔍 Search Records")
search_query = st.text_input("Enter Student Name or Tablet ID to check status")

if search_query:
    filtered_data = data[data.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
    st.write(f"Found {len(filtered_data)} record(s):")
    st.dataframe(filtered_data, use_container_width=True)
else:
    st.write("Showing all records for today:")
    st.dataframe(data, use_container_width=True)

# Download Button for the Prefect's Report
csv = data.to_csv(index=False).encode('utf-8')
st.download_button("📂 Download CSV Report", csv, "daily_report.csv", "text/csv")
