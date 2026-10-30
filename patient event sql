{{ config(materialized='table') }}

SELECT
    case_id,
    event_id,
    event_order,
    TRIM(activity) AS activity,
    event_timestamp,
    waiting_time_minutes,
    activity_duration_minutes,
    TRIM(pathway_type) AS pathway_type,
    loopback_transition,
    previous_activity,
    triage_level,
    case_complexity
FROM `careflow-512709.careflow_dataset.patient_events_raw`
