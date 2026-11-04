import pandas as pd
from pathlib import Path

file_path = Path("reports/patient_conformance_report.csv")
df = pd.read_csv(file_path)

summary = pd.DataFrame([{
    "total_patients": len(df),
    "fitting_patients": df["trace_is_fit"].sum(),
    "non_fitting_patients": (~df["trace_is_fit"]).sum(),
    "patients_with_missing_tokens": (df["missing_tokens"] > 0).sum(),
    "patients_with_remaining_tokens": (df["remaining_tokens"] > 0).sum(),
    "total_missing_tokens": df["missing_tokens"].sum(),
    "total_remaining_tokens": df["remaining_tokens"].sum(),
    "average_trace_fitness": round(df["trace_fitness"].mean(), 4)
}])

deviations = df[
    (df["missing_tokens"] > 0) |
    (df["remaining_tokens"] > 0) |
    (~df["trace_is_fit"])
]

summary.to_csv(
    "reports/conformance_deviation_summary.csv",
    index=False
)

deviations.to_csv(
    "reports/patient_conformance_deviations.csv",
    index=False
)

print("\n--- CONFORMANCE DEVIATION ANALYSIS ---")
print(summary.to_string(index=False))

print("\nPatients with deviations:", len(deviations))

if deviations.empty:
    print("No token-level deviations found.")

print("\nReports saved successfully.")
