import pandas as pd

df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

activity = pd.read_csv("reports/activity_bottleneck_summary.csv")

kpi_summary = pd.DataFrame([{
    "total_patients": df["case_id"].nunique(),
    "total_events": df["event_id"].nunique(),
    "total_activities": df["activity"].nunique(),
    "average_waiting_time": round(
        df["waiting_time_minutes"].mean(), 2
    ),
    "median_waiting_time": round(
        df["waiting_time_minutes"].median(), 2
    ),
    "total_waiting_time": df["waiting_time_minutes"].sum(),
    "average_activity_duration": round(
        df["activity_duration_minutes"].mean(), 2
    ),
    "total_activity_duration": df[
        "activity_duration_minutes"
    ].sum(),
    "highest_waiting_activity": activity.iloc[0]["activity"],
    "highest_average_waiting_time": activity.iloc[0][
        "average_waiting_time"
    ]
}])

kpi_summary.to_csv(
    "reports/powerbi_kpi_summary.csv",
    index=False
)

print("\nPower BI KPI Summary:\n")
print(kpi_summary.to_string(index=False))
print("\nReport saved to reports/powerbi_kpi_summary.csv")
