
import pandas as pd

# Load the processed patient event data
df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

# Calculate waiting-time metrics for each patient
patient_summary = (
    df.groupby("case_id")
    .agg(
        total_events=("event_id", "count"),
        total_waiting_time=("waiting_time_minutes", "sum"),
        average_waiting_time=("waiting_time_minutes", "mean"),
        total_activity_duration=("activity_duration_minutes", "sum")
    )
    .reset_index()
)

# Round time values
patient_summary["average_waiting_time"] = (
    patient_summary["average_waiting_time"].round(2)
)

# Rank patients by total waiting time
patient_summary = patient_summary.sort_values(
    by="total_waiting_time",
    ascending=False
)

# Add a rank column
patient_summary.insert(
    0, "waiting_time_rank",
    range(1, len(patient_summary) + 1)
)

# Save the report
patient_summary.to_csv(
    "reports/patient_bottleneck_summary.csv",
    index=False
)

# Display the 10 patients with the highest total waiting time
print("\nTop 10 Patients by Total Waiting Time:\n")
print(patient_summary.head(10).to_string(index=False))

print("\nTotal patients analyzed:", len(patient_summary))
print("Report saved to reports/patient_bottleneck_summary.csv")
