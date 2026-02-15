import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="SafeTab Pro", layout="wide")
st.title("🛡️ SafeTab: Smart Search & Sync")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
URL = "https://docs.google.com/spreadsheets/d/1-1hSN2Us6wTdrhKiwy_58AlVZHX6kwjxPPrGWnpocN4/edit"

# --- SIDEBAR: RECORD SUBMISSION ---
st.sidebar.header("📥 Record Submission")
with st.sidebar.form("input_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    tab_id = st.text_input("Tablet ID")
    submitted = st.form_submit_button("Log Tablet")

if submitted and name and tab_id:
    # 1. Read current data with ttl=0 to ensure we see the latest
    df = conn.read(spreadsheet=URL, ttl=0)
    
    # 2. Create the new row
    new_entry = pd.DataFrame([{
        "Name": name, 
        "Tablet ID": tab_id, 
        "Time": datetime.now().strftime("%H:%M"), 
        "Date": datetime.now().strftime("%Y-%m-%d")
    }])
    
    # 3. Combine old data with the new entry
    updated_df = pd.concat([df, new_entry], ignore_index=True)
    
    # 4. Save back to Google Sheets
    conn.update(spreadsheet=URL, data=updated_df)
    
    st.sidebar.success(f"✅ Verified: {name}")
    st.rerun()

# --- MAIN PAGE: SEARCH & VIEW ---
# Load data for display
data = conn.read(spreadsheet=URL, ttl=0)

st.subheader("🔍 Search Records")
search_query = st.text_input("Search by Name or Tablet ID")

if search_query:
    # Filter the data based on search
    filtered_data = data[data.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
    st.dataframe(filtered_data, use_container_width=True)
else:
    st.write("Current Logs:")
    st.dataframe(data, use_container_width=True)

# Download button for your reports
csv = data.to_csv(index=False).encode('utf-8')
st.download_button("📂 Download CSV Report", csv, "daily_report.csv", "text/csv")
