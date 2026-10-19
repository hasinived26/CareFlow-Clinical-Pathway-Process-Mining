import pandas as pd

events = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

events["event_timestamp"] = pd.to_datetime(events["event_timestamp"])

events = events.sort_values(["case_id", "event_order"]).copy()

events["next_event_timestamp"] = (events.groupby("case_id")["event_timestamp"].shift(-1))

events["calculated_transition_minutes"] = (events["next_event_timestamp"] - events["event_timestamp"]
                                           ).dt.total_seconds() / 60

events["waiting_time_matches"] = (events["waiting_time_minutes"].round(2)
                                  == events["calculated_transition_minutes"].round(2))

print("\n--- PATIENT JOURNEY VALIDATION ---")
print("Total events:", len(events))
print("Negative transition times:",(events["calculated_transition_minutes"] < 0).sum())
print("Recorded waiting times:",events["waiting_time_minutes"].notna().sum())
print("Waiting times matching timestamp gaps:",events["waiting_time_matches"].sum())
print("Events without a next event:",events["next_event_timestamp"].isna().sum())

events.to_csv("reports/patient_journey_validation.csv",index=False)

print("\nDetailed results saved to:")
print("reports/patient_journey_validation.csv")

print("\n--- SAMPLE WAITING TIME COMPARISON ---")

columns = [
    "case_id",
    "event_order",
    "activity",
    "event_timestamp",
    "waiting_time_minutes",
    "calculated_transition_minutes",
]

print(events[columns].head(15).to_string(index=False))

file_path = "data/raw/careflow_synthetic_dataset.xlsx"

dictionary = pd.read_excel(file_path,sheet_name="Data_Dictionary")

print("\n--- TIME COLUMN DEFINITIONS ---")

keywords = ["waiting", "duration", "timestamp", "event"]

for _, row in dictionary.iterrows():
    column_name = str(row["column_name"])
    definition = str(row["definition"])
    if any(word in column_name.lower() or word in definition.lower()
           for word in keywords):
        print(f"{column_name}: {definition}")


import pandas as pd

file_path = "data/raw/careflow_synthetic_dataset.xlsx"

events = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

summary = pd.read_csv("data/processed/careflow_patient_summary_clean.csv")

# Calculate totals from event records
calculated = events.groupby("case_id").agg(
    calculated_waiting_time=("waiting_time_minutes", "sum"),
    calculated_activity_duration=("activity_duration_minutes", "sum"),
    calculated_event_count=("event_id", "count")
).reset_index()

comparison = summary.merge(
    calculated,
    left_on="patient_id",
    right_on="case_id",
    how="left",
    validate="one_to_one"
)

print("\n--- SUMMARY CONSISTENCY CHECK ---")
print("Waiting-time mismatches:",
    (
        comparison["total_waiting_time_minutes"]
        != comparison["calculated_waiting_time"]
    ).sum()
)

print("Activity-duration mismatches:",
    (
        comparison["total_activity_duration_minutes"]
        != comparison["calculated_activity_duration"]
    ).sum()
)

print("Event-count mismatches:",
    (
        comparison["number_of_events"]
        != comparison["calculated_event_count"]
    ).sum()
)

# Save summary consistency report

from pathlib import Path

report_dir = Path("reports")
report_dir.mkdir(parents=True, exist_ok=True)

comparison.to_csv(
    report_dir / "summary_consistency_report.csv",
    index=False
)

print("\nSummary consistency report saved successfully!")
