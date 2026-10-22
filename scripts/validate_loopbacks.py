import pandas as pd

events = pd.read_csv(
    "data/processed/careflow_patient_events_clean.csv"
)

events = events.sort_values(
    ["case_id", "event_order"]
).copy()


events["actual_transition"] = (
    events["previous_activity"].astype("string")
    + " -> "
    + events["activity"].astype("string")
)

print("\n--- LOOP-BACK VALIDATION ---")
print("\nRecorded loop-back values:")
print(events["loopback_transition"].value_counts(dropna=False))
print("\nMost frequent actual transitions:")
print(events["actual_transition"].value_counts().head(15))
print("\nSample events marked as loop-backs:")
print(
    events.loc[
        events["loopback_transition"].notna(),
        ["case_id", "event_order", "previous_activity",
         "activity", "loopback_transition"]
    ].head(15).to_string(index=False)
)


# Comparing recorded loop-back flags with actual transitions

events["actual_loopback"] = (
    (
        (events["previous_activity"] == "Clinical Review")
        & (events["activity"] == "Diagnostic Test")
    )
    |
    (
        (events["previous_activity"] == "Clinical Review")
        & (events["activity"] == "Initial Assessment")
    )
)

events["recorded_loopback"] = (
    events["loopback_transition"].astype(str).str.strip().str.lower()
    == "yes"
)

print("\n--- LOOP-BACK FLAG CHECK ---")
print(
    "Actual transitions matching our loop-back rule:",
    events["actual_loopback"].sum()
)
print(
    "Recorded loop-back flags:",
    events["recorded_loopback"].sum()
)
print(
    "Actual transitions not flagged:",
    (
        events["actual_loopback"]
        & ~events["recorded_loopback"]
    ).sum()
)
print(
    "Flagged events not matching our rule:",
    (
        ~events["actual_loopback"]
        & events["recorded_loopback"]
    ).sum()
)
