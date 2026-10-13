import pandas as pd
from pathlib import Path

file_path=Path("data/raw/careflow_synthetic_dataset.xlsx")

excel_file = pd.ExcelFile(file_path) #Load file

print("Available sheets:")
print(excel_file.sheet_names)

for sheet in excel_file.sheet_names:
    df=pd.read_excel(file_path, sheet_name=sheet)

    print(f"\n{'=' * 40}")
    print("Sheet:",sheet)
    print("Shape (rows, columns):",df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:",df.duplicated().sum())

#Additional Validation

events=pd.read_excel("data/raw/careflow_synthetic_dataset.xlsx",sheet_name="Patient_Events")

summary = pd.read_excel("data/raw/careflow_synthetic_dataset.xlsx",sheet_name="Patient_Summary")

events["event_timestamp"]=pd.to_datetime(events["event_timestamp"], errors="coerce")

print("\n--- ADDITIONAL VALIDATION ---")

print("Invalid event timestamps:",events["event_timestamp"].isna().sum())

print("Duplicate event IDs:",events["event_id"].duplicated().sum())

for col in ["waiting_time_minutes","activity_duration_minutes"]:
    print(f"Negative{col}:",(events[col]<0).sum())

events=events.sort_values(["case_id","event_order"])

timestamp_gaps=(events.groupby("case_id")["event_timestamp"].diff())

print("Negative timestamp gaps:",(timestamp_gaps < pd.Timedelta(0)).sum())


print("Duplicate patient IDs:",summary["patient_id"].duplicated().sum())
print("--- VALIDATION COMPLETE ---")


#Event sequence consistency

print("\n--- SEQUENCE VALIDATION ---")

duplicate_orders=events.duplicated(subset=["case_id","event_order"]).sum()

print("Duplicate event orders:",duplicate_orders)

order_gaps = 0

for case_id,group in events.groupby("case_id"):
    orders = sorted(group["event_order"].dropna())
    if orders and orders != list(range(1, len(orders) + 1)):
        order_gaps += 1

print("Patients with missing or irregular event order:",order_gaps)

event_counts=events.groupby("case_id").size()

summary_counts=summary.set_index("patient_id")["number_of_events"]

common_patients=event_counts.index.intersection(summary_counts.index)

mismatches=(event_counts.loc[common_patients] != summary_counts.loc[common_patients]).sum()

print("Patient event-count mismatches:",mismatches)
print("--- SEQUENCE VALIDATION COMPLETE ---")

#Save processed Dataset

from pathlib import Path

output_dir=Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

file_path="data/raw/careflow_synthetic_dataset.xlsx"

events=pd.read_excel(file_path, sheet_name="Patient_Events")

summary=pd.read_excel(file_path, sheet_name="Patient_Summary")

events["event_timestamp"]=pd.to_datetime(events["event_timestamp"])

summary["start_timestamp"]=pd.to_datetime(summary["start_timestamp"])

summary["end_timestamp"]=pd.to_datetime(summary["end_timestamp"])

events=events.sort_values(["case_id", "event_order"]).reset_index(drop=True)

events.to_csv(
    output_dir / "careflow_patient_events_clean.csv",
    index=False
)

summary.to_csv(
    output_dir / "careflow_patient_summary_clean.csv",
    index=False
)

print("\nProcessed datasets saved successfully!")
print("Event records:", len(events))
print("Patient summary records:", len(summary))
print("Event columns:", len(events.columns))
print("Summary columns:", len(summary.columns))
