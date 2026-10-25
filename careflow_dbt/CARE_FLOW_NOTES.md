# CareFlow — BigQuery and dbt

## Work Completed
- Connected Google BigQuery with dbt.
- Created the `patient_events_clean` model from `patient_events_raw`.
- Preserved the event data columns while cleaning activity and pathway names.
- Added data-quality tests for missing patient IDs, missing event IDs, and duplicate event IDs.
- Successfully passed all three dbt tests.

## Next Steps
- Create a patient summary model.
- Perform bottleneck analysis using waiting times and activity durations.
- Calculate KPIs and develop a Power BI dashboard.