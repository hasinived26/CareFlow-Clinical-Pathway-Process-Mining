import pandas as pd
import pm4py
from pathlib import Path

# Load prepared event log
input_file = Path("data/processed/careflow_process_event_log.csv")

output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

event_log = pd.read_csv(input_file)

event_log["time:timestamp"] = pd.to_datetime(event_log["time:timestamp"])

# Prepare data for PM4Py
event_log = pm4py.format_dataframe(
    event_log,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

# Discover process model
process_model = pm4py.discover_process_tree_inductive(event_log)

# Convert process tree to Petri net
net, initial_marking, final_marking = (
    pm4py.convert_to_petri_net(process_model)
)

# Save process visualization
pm4py.save_vis_petri_net(
    net,
    initial_marking,
    final_marking,
    str(output_dir / "careflow_process_map.png")
)

print("Process discovery completed!")
print("Patient cases:", event_log["case:concept:name"].nunique())
print("Activities:", event_log["concept:name"].nunique())
print("Process map saved to reports/careflow_process_map.png")
