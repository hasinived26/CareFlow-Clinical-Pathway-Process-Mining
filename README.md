# CareFlow – Clinical Pathway Process Mining

## About the Project

CareFlow is a data analytics project that focuses on understanding patient journeys in a healthcare system.

The project uses patient event data to study how patients move through different stages of a clinical pathway. It helps identify delays, waiting-time bottlenecks and areas where the process can be improved.

The main goal is to understand how the healthcare workflow works and find opportunities to make it more efficient.

## Problem Statement

In healthcare systems, patients go through several stages, such as registration, triage, assessment, diagnostic tests, treatment and discharge.

Delays at any of these stages can increase the overall waiting time and affect the efficiency of the healthcare process.

Without proper analysis, it can be difficult to identify where these delays occur and which stages need improvement.

CareFlow uses data analytics and process mining to study these patient journeys and identify bottlenecks.

## Project Objectives

- Understand patient journeys through different clinical activities.
- Analyse waiting time at each stage.
- Identify activities that contribute most to delays.
- Compare waiting times across different pathways and triage levels.
- Study patient-level waiting time and process variations.
- Present the findings through an interactive Power BI dashboard.

## Dataset

The project uses a synthetic healthcare dataset containing patient event information.

The dataset includes:
- Patient and event IDs
- Activity names
- Event timestamps
- Previous activities
- Pathway types
- Triage levels
- Waiting time
- Activity duration
- Case complexity

### Dataset Overview

- **Patients:** 300
- **Events:** 2,562
- **Activities:** 8

## Technologies Used

- **Python:** Data preprocessing and analysis
- **Pandas:** Data cleaning and manipulation
- **Google BigQuery:** Cloud data storage and querying
- **dbt:** Data transformation and testing
- **PM4Py:** Process discovery and conformance analysis
- **Power BI:** Dashboard creation and visualisation
- **Git and GitHub:** Version control and project management

## Project Workflow

### 1. Data Preprocessing
- Inspected the original dataset.
- Checked missing values and duplicate records.
- Validated timestamps and event ordering.
- Checked waiting times and activity durations.
- Prepared clean datasets for further analysis.

### 2. Data Validation
- Checked patient and event IDs.
- Validated patient journeys.
- Compared summary data with event-level data.
- Generated data quality reports.

### 3. Process Mining
- Created an event log from the processed data.
- Discovered the patient workflow using PM4Py.
- Generated a process map.
- Performed conformance checking on the event log.

### 4. BigQuery and dbt
- Uploaded the patient event data to BigQuery.
- Created a cleaned data model using dbt.
- Added tests for missing and duplicate IDs.
- Executed the model and checked the results.

### 5. Bottleneck Analysis
- Analysed average waiting time for each activity.
- Identified patients with higher waiting times.
- Compared waiting times across pathway types.
- Compared waiting times across triage levels and case complexity.
- Analysed the contribution of different activities to total waiting time.

### 6. Power BI Dashboard
Created an interactive, single-page dashboard containing:
- Total Patients
- Total Events
- Average Waiting Time
- Total Activity Wait Time
- Waiting Time Contribution by Activity
- Average Waiting Time by Activity
- Patients by Case Complexity
- Average Waiting Time by Triage Level

The dashboard also includes filters for pathway type, triage level and case complexity.

## Key Findings

- Treatment has the highest average waiting time at approximately 55.61 minutes.
- Diagnostic Test has an average waiting time of approximately 45.05 minutes.
- Clinical Review has an average waiting time of approximately 37.03 minutes.
- These three activities contribute approximately 64.60% of the total waiting time.
- High-complexity cases have a higher average waiting time than medium- and low-complexity cases.

## Project Structure

```text
CareFlow/
│
├── Dashboard/
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
├── reports/
├── careflow_dbt/
│
├── README.md
└── .gitignore
```

## Conclusion

CareFlow demonstrates how data analytics and process mining can be used to understand healthcare workflows.

By analysing patient journeys and waiting times, the project identifies activities that contribute to delays and provides useful insights through an interactive dashboard.

The findings can help highlight areas where further investigation and process improvement may be needed.

## Note

This project uses synthetic patient data for academic and analytical purposes. The results are not based on real hospital records and should not be treated as clinical recommendations.

The process discovery and conformance results describe the supplied dataset and do not independently establish that the workflow represents real-world clinical practice.