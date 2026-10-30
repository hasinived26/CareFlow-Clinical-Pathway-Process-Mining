import pandas as pd

df = pd.read_csv("data/processed/careflow_patient_events_clean.csv")

categories = [
    "pathway_type",
    "triage_level",
    "case_complexity"
]

for category in categories:

    summary = (
        df.groupby(category, dropna=False)
        .agg(
            patient_count=("case_id", "nunique"),
            event_count=("event_id", "count"),
            average_waiting_time=("waiting_time_minutes", "mean"),
            median_waiting_time=("waiting_time_minutes", "median"),
            total_waiting_time=("waiting_time_minutes", "sum"),
            average_activity_duration=(
                "activity_duration_minutes", "mean"
            )
        )
        .reset_index()
    )

    time_columns = [
        "average_waiting_time",
        "median_waiting_time",
        "total_waiting_time",
        "average_activity_duration"
    ]

    summary[time_columns] = summary[time_columns].round(2)
    summary = summary.sort_values(
        by="average_waiting_time",
        ascending=False
    )

    filename = f"reports/{category}_bottleneck_summary.csv"
    summary.to_csv(filename, index=False)

    print(f"\nBottleneck Analysis by {category}:\n")
    print(summary.to_string(index=False))
    print(f"\nReport saved to {filename}")

print("\nAll pathway comparison reports generated successfully!")
