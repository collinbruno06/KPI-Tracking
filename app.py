import streamlit as st
import pandas as pd

st.title("KPI Tracking Application")
st.write("Track and manage KPI scores for HR functions.")

parameters = ["Recruitment", "HRBP", "HR Operations", "Payroll"]
kpi_data = []

for param in parameters:
    st.subheader(f"KPI: {param}")
    target_score = st.number_input(f"Target Score for {param} (Manager)", min_value=0, max_value=100)
    attained_score = st.number_input(f"Attained Score for {param} (Employee)", min_value=0, max_value=100)
    employee_feedback = st.text_area(f"Employee Feedback for {param}")
    manager_feedback = st.text_area(f"Manager Feedback for {param}")
    
    kpi_data.append({
        "Parameter": param,
        "Target Score": target_score,
        "Attained Score": attained_score,
        "Employee Feedback": employee_feedback,
        "Manager Feedback": manager_feedback
    })

df = pd.DataFrame(kpi_data)
st.subheader("KPI Summary")
st.dataframe(df)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download KPI Data as CSV", data=csv, file_name='kpi_tracking_data.csv', mime='text/csv')
