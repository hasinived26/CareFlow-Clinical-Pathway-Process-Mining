import pandas as pd

df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")
kpi = pd.read_csv("reports/powerbi_kpi_summary.csv")

expected = {
    "total_patients": df["case_id"].nunique(),
    "total_events": df["event_id"].nunique(),
    "total_activities": df["activity"].nunique(),
    "average_waiting_time": round(df["waiting_time_minutes"].mean(), 2),
    "median_waiting_time": round(df["waiting_time_minutes"].median(), 2),
    "total_waiting_time": df["waiting_time_minutes"].sum()
}

results = []

for metric, expected_value in expected.items():
    actual_value = kpi.loc[0, metric]

    passed = abs(actual_value - expected_value) < 0.01

    results.append({
        "metric": metric,
        "expected_value": expected_value,
        "actual_value": actual_value,
        "status": "PASS" if passed else "FAIL"
    })


report = pd.DataFrame(results)
report.to_csv(
    "reports/powerbi_kpi_validation.csv",
    index=False
)

print("\nPower BI KPI Validation:\n")
print(report.to_string(index=False))
print("\nValidation Summary:")
print(report["status"].value_counts().to_string())
print("\nReport saved to reports/powerbi_kpi_validation.csv")
