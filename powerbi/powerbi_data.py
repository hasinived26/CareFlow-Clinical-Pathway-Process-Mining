import pandas as pd

df = pd.read_csv('careflow_patient_events.csv')
df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

# Sort 
df = df.sort_values(by=['case_id', 'event_order']).reset_index(drop=True)

df['from_activity'] = df.groupby('case_id')['activity'].shift(1).fillna('Start')

# Transition Bottleneck 
transitions_df = df[['case_id', 'from_activity', 'activity', 'waiting_time_minutes', 
                     'triage_level', 'case_complexity', 'pathway_type']].copy()

transitions_df.rename(columns={
    'activity': 'to_activity',
    'waiting_time_minutes': 'transition_time_minutes'
}, inplace=True)

transitions_df = transitions_df[transitions_df['from_activity'] != 'Start'].copy()
transitions_df.to_csv('powerbi_transition_bottlenecks.csv', index=False)

# Patient KPIs
patient_kpis = df.groupby('case_id').agg(
    triage_level=('triage_level', 'first'),
    case_complexity=('case_complexity', 'first'),
    pathway_type=('pathway_type', 'first'),
    total_waiting_time=('waiting_time_minutes', 'sum'),
    total_activity_time=('activity_duration_minutes', 'sum'),
    start_time=('event_timestamp', 'min'),
    end_time=('event_timestamp', 'max'),
    loopback_count=('loopback_transition', lambda x: (x == 'Yes').sum())
).reset_index()

# Total Length of Stay in minutes
patient_kpis['total_los_minutes'] = (patient_kpis['end_time'] - patient_kpis['start_time']).dt.total_seconds() / 60
patient_kpis = patient_kpis.drop(columns=['start_time', 'end_time'])
patient_kpis.to_csv('powerbi_patient_kpis.csv', index=False)

# Slow departments
activity_perf = df.groupby('activity').agg(
    avg_waiting_time=('waiting_time_minutes', 'mean'),
    avg_activity_duration=('activity_duration_minutes', 'mean'),
    total_occurrences=('event_id', 'count')
).reset_index()

activity_perf.to_csv('powerbi_activity_performance.csv', index=False)

print(" Success! 3 Power BI tables generated:")
print("1. powerbi_transition_bottlenecks.csv")
print("2. powerbi_patient_kpis.csv")
print("3. powerbi_activity_performance.csv")