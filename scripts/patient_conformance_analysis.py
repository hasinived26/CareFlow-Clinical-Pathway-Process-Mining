import pandas as pd
import pm4py
from pathlib import Path

file_path = Path("data/processed/careflow_process_event_log.csv")
event_log = pd.read_csv(file_path)

event_log["time:timestamp"] = pd.to_datetime(
    event_log["time:timestamp"]
)

event_log = pm4py.format_dataframe(
    event_log,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

log = pm4py.convert_to_event_log(event_log)

process_tree = pm4py.discover_process_tree_inductive(log)

net, initial_marking, final_marking = (
    pm4py.convert_to_petri_net(process_tree)
)

diagnostics = pm4py.conformance_diagnostics_token_based_replay(
    log,
    net,
    initial_marking,
    final_marking
)

results = []

for trace, diagnostic in zip(log, diagnostics):

    case_id = trace.attributes["concept:name"]

    results.append({
        "case_id": case_id,
        "trace_is_fit": diagnostic["trace_is_fit"],
        "trace_fitness": diagnostic["trace_fitness"],
        "missing_tokens": diagnostic["missing_tokens"],
        "remaining_tokens": diagnostic["remaining_tokens"],
        "consumed_tokens": diagnostic["consumed_tokens"],
        "produced_tokens": diagnostic["produced_tokens"]
    })

conformance_report = pd.DataFrame(results)

output_path = Path("reports/patient_conformance_report.csv")

conformance_report.to_csv(output_path, index=False)

print("\n--- PATIENT CONFORMANCE ANALYSIS ---")
print("Total patients:", len(conformance_report))
print("Fitting patients:",
    conformance_report["trace_is_fit"].sum())
print("Non-fitting patients:",
    (~conformance_report["trace_is_fit"]).sum())
print("Average trace fitness:",
    round(conformance_report["trace_fitness"].mean(), 4))
print("\nConformance report saved to:", output_path)
print("\n--- ANALYSIS COMPLETE ---")
