import pandas as pd
from pathlib import Path

input_file = Path("data/processed/careflow_patient_events_clean.csv")

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

events = pd.read_csv(input_file)

event_log = events[["case_id", "activity", "event_timestamp"]].copy()

# Standardize column names for PM4Py
event_log = event_log.rename(columns={"case_id": "case:concept:name",
    "activity": "concept:name",
    "event_timestamp": "time:timestamp"
})

# Convert timestamps
event_log["time:timestamp"] = pd.to_datetime(
    event_log["time:timestamp"],
    errors="raise"
)

# Sort events chronologically within each case
event_log = event_log.sort_values(
    ["case:concept:name", "time:timestamp"],
    kind="stable"
).reset_index(drop=True)

# Validate required fields
assert event_log["case:concept:name"].notna().all()
assert event_log["concept:name"].notna().all()
assert event_log["time:timestamp"].notna().all()

# Save event log
output_file = output_dir / "careflow_process_event_log.csv"
event_log.to_csv(output_file, index=False)

print("Event log prepared successfully!")
print("Total events:", len(event_log))
print("Unique patient cases:", event_log["case:concept:name"].nunique())
print("Unique activities:", event_log["concept:name"].nunique())
print("Saved to:", output_file)
