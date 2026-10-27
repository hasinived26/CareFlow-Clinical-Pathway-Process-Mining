import pandas as pd

# Load the processed patient event data
df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

# Convert waiting and activity duration columns to numeric values
df["waiting_time_minutes"] = pd.to_numeric(
    df["waiting_time_minutes"], errors="coerce"
)
df["activity_duration_minutes"] = pd.to_numeric(
    df["activity_duration_minutes"], errors="coerce"
)

# Calculate bottleneck metrics for each activity
bottleneck_summary = (
    df.groupby("activity")
    .agg(
        event_count=("event_id", "count"),
        average_waiting_time=("waiting_time_minutes", "mean"),
        median_waiting_time=("waiting_time_minutes", "median"),
        p90_waiting_time=(
            "waiting_time_minutes",
            lambda x: x.quantile(0.90)
        ),
        total_waiting_time=("waiting_time_minutes", "sum"),
        average_activity_duration=(
            "activity_duration_minutes", "mean"
        )
    )
    .reset_index()
)

# Round time values to 2 decimal places
time_columns = [
    "average_waiting_time",
    "median_waiting_time",
    "p90_waiting_time",
    "total_waiting_time",
    "average_activity_duration"
]

bottleneck_summary[time_columns] = bottleneck_summary[
    time_columns
].round(2)

# Sort activities by average waiting time, highest first
bottleneck_summary = bottleneck_summary.sort_values(
    by="average_waiting_time", ascending=False
)

# Save the report
bottleneck_summary.to_csv(
    "reports/activity_bottleneck_summary.csv",
    index=False
)

# Display the results
print("\nActivity Bottleneck Summary:\n")
print(bottleneck_summary.to_string(index=False))

print("\nReport saved to reports/activity_bottleneck_summary.csv")
