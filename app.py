import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.title("🛡️ SafeTab: Permanent Record System")

# 1. Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Sidebar for Submission
st.sidebar.header("Record Submission")
student_name = st.sidebar.text_input("Student Name")
tablet_id = st.sidebar.text_input("Tablet ID")

if st.sidebar.button("Submit Tablet"):
    if student_name and tablet_id:
        # Create a new row of data
        new_row = pd.DataFrame([{
            "Name": student_name,
            "Tablet ID": tablet_id,
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Status": "Submitted"
        }])
        
        # Read existing data and add the new row
        existing_data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1-1hSN2Us6wTdrhKiwy_58AlVZHX6kwjxPPrGWnpocN4/edit?usp=drivesdk")
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # Update the Google Sheet
        conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1-1hSN2Us6wTdrhKiwy_58AlVZHX6kwjxPPrGWnpocN4/edit?usp=drivesdk", data=updated_df)
        st.sidebar.success("Saved to Google Sheets!")
    else:
        st.sidebar.error("Please fill all fields")

# 3. Display the Log from Google Sheets
st.subheader("Live Spreadsheet Data")
data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1-1hSN2Us6wTdrhKiwy_58AlVZHX6kwjxPPrGWnpocN4/edit?usp=drivesdk")
st.dataframe(data)

# 4. Download Button
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Daily Report (CSV)",
    data=csv,
    file_name=f"tablet_report_{datetime.now().strftime('%Y-%m-%d')}.csv",
    mime='text/csv',
)
