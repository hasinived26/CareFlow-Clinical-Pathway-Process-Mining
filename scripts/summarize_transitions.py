
import pandas as pd
from pathlib import Path

input_file = Path("data/processed/careflow_process_event_log.csv")
output_file = Path("reports/activity_transition_summary.csv")

df = pd.read_csv(input_file)

df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])
df = df.sort_values(["case:concept:name", "time:timestamp"])

df["next_activity"] = df.groupby("case:concept:name")["concept:name"].shift(-1)

transitions = (
    df.dropna(subset=["next_activity"])
    .groupby(["concept:name", "next_activity"])
    .size()
    .reset_index(name="transition_count")
    .sort_values("transition_count", ascending=False)
)

output_file.parent.mkdir(parents=True, exist_ok=True)
transitions.to_csv(output_file, index=False)

print("Transition summary created successfully.")
print(transitions.head(10).to_string(index=False))
