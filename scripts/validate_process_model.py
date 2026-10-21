
import pandas as pd
import pm4py
from pathlib import Path

# Load the prepared event log
file_path=Path(
    "data/processed/careflow_process_event_log.csv"
)

event_log=pd.read_csv(file_path)
event_log["time:timestamp"] = pd.to_datetime(
    event_log["time:timestamp"]
)

# Format the event log for PM4Py
event_log = pm4py.format_dataframe(
    event_log,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

# Discover the process model
process_tree=pm4py.discover_process_tree_inductive(
    event_log
)

# Check how well the model fits the observed event log
fitness = pm4py.fitness_token_based_replay(
    event_log,
    *pm4py.convert_to_petri_net(process_tree)
)

print("\n--- PROCESS MODEL VALIDATION ---")
print("Patient cases:", event_log["case:concept:name"].nunique())
print("Activities:", event_log["concept:name"].nunique())
print("Fitness results:", fitness)
print("\n--- VALIDATION COMPLETE ---")
