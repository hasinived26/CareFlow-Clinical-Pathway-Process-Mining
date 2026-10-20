# CareFlow - Process Model Validation

import pandas as pd
import pm4py
from pathlib import Path

def load_event_log(file_path):
    """Load the prepared CareFlow event log."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Event log not found: {file_path}"
        )

    event_log = pd.read_csv(file_path)

    print("Event log loaded successfully.")
    print("Total events:", len(event_log))

    return event_log


def prepare_event_log(event_log):
    """Validate required fields and prepare data for PM4Py."""

    required_columns = [
        "case:concept:name",
        "concept:name",
        "time:timestamp",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in event_log.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Convert timestamps
    event_log["time:timestamp"] = pd.to_datetime(
        event_log["time:timestamp"],
        errors="raise"
    )

    # Check required values
    if event_log[required_columns].isnull().any().any():
        raise ValueError(
            "Missing values found in required event-log fields."
        )

    # Sort events chronologically within each case
    event_log = event_log.sort_values(
        ["case:concept:name", "time:timestamp"],
        kind="stable"
    ).reset_index(drop=True)

    # Format the event log for PM4Py
    event_log = pm4py.format_dataframe(
        event_log,
        case_id="case:concept:name",
        activity_key="concept:name",
        timestamp_key="time:timestamp",
    )

    return event_log


def main():
    file_path = Path(
        "data/processed/careflow_process_event_log.csv"
    )

    event_log = load_event_log(file_path)
    event_log = prepare_event_log(event_log)

    print("\n--- EVENT LOG SUMMARY ---")
    print("Total events:", len(event_log))
    print(
        "Patient cases:",
        event_log["case:concept:name"].nunique()
    )
    print(
        "Unique activities:",
        event_log["concept:name"].nunique()
    )

    print("\nEvent log preparation completed.")


if __name__ == "__main__":
    main()
