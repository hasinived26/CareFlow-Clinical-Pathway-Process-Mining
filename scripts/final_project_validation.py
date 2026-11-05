import pandas as pd
from pathlib import Path

data_file = Path("data/processed/careflow_patient_events_clean.csv")

required_files = [
    "data/processed/careflow_patient_summary_clean.csv",
    "data/processed/careflow_process_event_log.csv",
    "reports/data_quality_report.json",
    "reports/activity_bottleneck_summary.csv",
    "reports/bottleneck_validation_report.csv",
    "reports/patient_bottleneck_summary.csv",
    "reports/triage_level_bottleneck_summary.csv",
    "reports/case_complexity_bottleneck_summary.csv",
    "reports/powerbi_kpi_summary.csv",
    "reports/powerbi_kpi_validation.csv",
    "reports/waiting_time_contribution.csv",
    "reports/patient_conformance_report.csv",
    "reports/conformance_deviation_summary.csv",
    "reports/patient_conformance_deviations.csv",
    "careflow_dbt/dbt_project.yml",
    "careflow_dbt/models/example/patient_events_clean.sql",
]

results = []

for file in required_files:
    results.append({
        "check": f"File exists: {file}",
        "status": "PASS" if Path(file).exists() else "FAIL"
    })

if data_file.exists():
    df = pd.read_csv(data_file)

    checks = {
        "Total events are 2562": len(df) == 2562,
        "Total patients are 300": df["case_id"].nunique() == 300,
        "Event IDs are unique": df["event_id"].is_unique,
        "No missing event IDs": df["event_id"].notna().all(),
        "No negative waiting times": (df["waiting_time_minutes"] >= 0).all(),
        "No negative activity durations": (
            df["activity_duration_minutes"] >= 0
        ).all()
    }

    for check, passed in checks.items():
        results.append({
            "check": check,
            "status": "PASS" if passed else "FAIL"
        })

kpi_file = Path("reports/powerbi_kpi_validation.csv")

if kpi_file.exists():
    kpi = pd.read_csv(kpi_file)
    passed = (kpi["status"] == "PASS").all()

    results.append({
        "check": "All Power BI KPI validations passed",
        "status": "PASS" if passed else "FAIL"
    })

conformance_file = Path("reports/patient_conformance_report.csv")

if conformance_file.exists():
    conformance = pd.read_csv(conformance_file)

    passed = (
        len(conformance) == 300
        and conformance["trace_is_fit"].all()
        and (conformance["trace_fitness"] == 1).all()
    )

    results.append({
        "check": "All 300 patient journeys fit the process model",
        "status": "PASS" if passed else "FAIL"
    })

report = pd.DataFrame(results)

print("\n--- CAREFLOW FINAL PROJECT VALIDATION ---\n")
print(report.to_string(index=False))
print("\nValidation Summary:")
print(report["status"].value_counts().to_string())

report.to_csv("reports/final_project_validation.csv", index=False)

print("\nReport saved to reports/final_project_validation.csv")
