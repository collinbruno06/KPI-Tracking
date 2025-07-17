import streamlit as st
import pandas as pd
import plotly.express as px

st.title("KPI Tracking Application")
st.write("Track and manage KPI scores for HR functions on a monthly basis.")

# Define KPI parameters and months
parameters = ["Recruitment", "HRBP", "HR Operations", "Payroll"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# Initialize session state to store monthly data
if "monthly_kpi_data" not in st.session_state:
    st.session_state.monthly_kpi_data = {}

# Select month
selected_month = st.selectbox("Select Month to Update KPI", months)

# Initialize data for selected month if not already present
if selected_month not in st.session_state.monthly_kpi_data:
    st.session_state.monthly_kpi_data[selected_month] = []

# Input KPI data for selected month
st.subheader(f"Enter KPI Data for {selected_month}")
for param in parameters:
    st.markdown(f"### KPI: {param}")
    target_score = st.number_input(f"Target Score for {param} (Manager)", min_value=0, max_value=100, key=f"{selected_month}_{param}_target")
    attained_score = st.number_input(f"Attained Score for {param} (Employee)", min_value=0, max_value=100, key=f"{selected_month}_{param}_attained")
    employee_feedback = st.text_area(f"Employee Feedback for {param}", key=f"{selected_month}_{param}_emp_fb")
    manager_feedback = st.text_area(f"Manager Feedback for {param}", key=f"{selected_month}_{param}_mgr_fb")

    # Save data
    st.session_state.monthly_kpi_data[selected_month].append({
        "Month": selected_month,
        "Parameter": param,
        "Target Score": target_score,
        "Attained Score": attained_score,
        "Employee Feedback": employee_feedback,
        "Manager Feedback": manager_feedback
    })

# Combine all monthly data into a single DataFrame
all_data = []
for month, entries in st.session_state.monthly_kpi_data.items():
    all_data.extend(entries)

df = pd.DataFrame(all_data)

# Display full KPI summary
st.subheader("Full KPI Summary")
st.dataframe(df)

# Monthly totals
monthly_totals = df.groupby("Month")[["Target Score", "Attained Score"]].sum().reset_index()

st.subheader("Monthly Total Scores")
st.dataframe(monthly_totals)

# Bar chart visualization
st.subheader("Monthly KPI Performance")
fig = px.bar(monthly_totals, x="Month", y=["Target Score", "Attained Score"],
             barmode="group", title="Monthly Target vs Attained Scores")
st.plotly_chart(fig)

# CSV download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download KPI Data as CSV", data=csv, file_name='kpi_tracking_data.csv', mime='text/csv')
