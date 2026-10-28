import pandas as pd

df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")
summary = pd.read_csv("reports/activity_bottleneck_summary.csv")


check = (
    df.groupby("activity")["waiting_time_minutes"]
    .mean()
    .reset_index()
    .rename(columns={"waiting_time_minutes": "recalculated_average"})
)


comparison = summary.merge(check, on="activity", how="left")

comparison["difference"] = (
    comparison["average_waiting_time"]
    - comparison["recalculated_average"].round(2)
).round(2)


comparison["validation_status"] = comparison["difference"].apply(
    lambda x: "PASS" if abs(x) < 0.01 else "CHECK"
)

comparison.to_csv(
    "reports/bottleneck_validation_report.csv",
    index=False
)

print("\nBottleneck Validation Results:\n")
print(
    comparison[
        ["activity", "average_waiting_time",
         "recalculated_average", "difference",
         "validation_status"]
    ].to_string(index=False)
)

print("\nValidation status:")
print(comparison["validation_status"].value_counts().to_string())
print("\nReport saved to reports/bottleneck_validation_report.csv")
