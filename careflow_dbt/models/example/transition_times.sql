{{ config(materialized='table') }}

WITH ordered_events AS (
    SELECT 
        case_id,
        activity,
        event_timestamp,
        triage_level,
        case_complexity,
        LEAD(activity) OVER (PARTITION BY case_id ORDER BY event_timestamp) AS next_activity,
        LEAD(event_timestamp) OVER (PARTITION BY case_id ORDER BY event_timestamp) AS next_timestamp
    FROM {{ ref('patient_events_clean') }}
),
transition_durations AS (
    SELECT 
        activity AS from_activity,
        next_activity AS to_activity,
        triage_level,
        case_complexity,
        TIMESTAMP_DIFF(next_timestamp, event_timestamp, MINUTE) AS transition_time_minutes
    FROM ordered_events
    WHERE next_activity IS NOT NULL
)
SELECT 
    from_activity,
    to_activity,
    triage_level,
    case_complexity,
    COUNT(*) AS transition_count,
    ROUND(AVG(transition_time_minutes), 2) AS avg_transition_time_minutes,
    ROUND(MAX(transition_time_minutes), 2) AS max_transition_time_minutes
FROM transition_durations
GROUP BY 1, 2, 3, 4
ORDER BY from_activity, to_activity