import pandas as pd

df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

summary = (
    df.groupby("activity")
    .agg(
        event_count=("event_id", "count"),
        total_waiting_time=("waiting_time_minutes", "sum"),
        average_waiting_time=("waiting_time_minutes", "mean")
    )
    .reset_index()
)

overall_waiting = summary["total_waiting_time"].sum()

summary["waiting_contribution_percent"] = (
    summary["total_waiting_time"] / overall_waiting * 100
).round(2)

summary = summary.sort_values(
    by="total_waiting_time",
    ascending=False
)

summary["cumulative_contribution_percent"] = (
    summary["waiting_contribution_percent"].cumsum().round(2)
)

summary["average_waiting_time"] = (
    summary["average_waiting_time"].round(2)
)

summary.to_csv(
    "reports/waiting_time_contribution.csv",
    index=False
)

print("\nWaiting Time Contribution Analysis:\n")
print(summary.to_string(index=False))
print("\nTotal waiting time:", overall_waiting, "minutes")
print("\nReport saved to reports/waiting_time_contribution.csv")
