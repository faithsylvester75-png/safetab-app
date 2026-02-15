import streamlit as st
import pandas as pd
from datetime import datetime

# App Title
st.title("🛡️ SafeTab: Prefect Record System")

# Initialize a simple "database" in memory
if 'records' not in st.session_state:
    st.session_state.records = pd.DataFrame(columns=["Name", "Tablet ID", "Time", "Status"])

# Sidebar for Submission
st.sidebar.header("Record Submission")
student_name = st.sidebar.text_input("Student Name")
tablet_id = st.sidebar.text_input("Tablet ID / Scan Code")
condition = st.sidebar.selectbox("Condition", ["Perfect", "Dirty", "Damaged"])

if st.sidebar.button("Submit Tablet"):
    if student_name and tablet_id:
        new_data = {
            "Name": student_name,
            "Tablet ID": tablet_id,
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Status": "Submitted"
        }
        st.session_state.records = pd.concat([st.session_state.records, pd.DataFrame([new_data])], ignore_index=True)
        st.sidebar.success(f"Recorded {student_name}'s tablet!")
    else:
        st.sidebar.error("Please enter both Name and ID")

# Main Dashboard
st.subheader("Daily Submission Log")
st.table(st.session_state.records)

# Summary Stats
st.metric(label="Tablets Collected", value=len(st.session_state.records))
