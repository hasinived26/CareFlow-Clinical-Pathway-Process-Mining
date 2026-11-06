# CareFlow – dbt Data Transformation

## About

This folder contains the dbt project created for the CareFlow project.

We use dbt (Data Build Tool) to transform the raw patient event data stored in Google BigQuery into a cleaned table that can be used for further analysis.

## Tools Used

- **dbt Core:** To manage and execute data transformation models.
- **dbt BigQuery Adapter:** To connect dbt with Google BigQuery.
- **Google BigQuery:** To store and query patient event data.

## Data Source

The source data is stored in Google BigQuery.

- **Project:** `careflow-512709`
- **Dataset:** `careflow_dataset`
- **Source Table:** `patient_events_raw`

## Transformation Model

The main model is:

`models/example/patient_events_clean.sql`

This model:
- Reads data from the raw patient events table.
- Trims unnecessary spaces from activity and pathway names.
- Creates a cleaned table for further analysis.

The output is stored as:

`patient_events_clean`

## Data Quality Tests

The project includes the following tests:

- `case_id` should not contain NULL values.
- `event_id` should not contain NULL values.
- `event_id` should contain unique values.

These tests help check the basic quality and consistency of the transformed data.

## Running the Project

Make sure dbt Core, the BigQuery adapter and Google Cloud authentication are configured.

Run the following commands from the `careflow_dbt` directory:


dbt debug

To execute the transformation model:


dbt run

To execute the data quality tests:


dbt test

## Output

The main output is the `patient_events_clean` table in BigQuery.

It contains the cleaned patient event data used in the CareFlow analysis.

## Purpose

This dbt workflow helps organise data transformation and basic data quality testing before using the data for process mining and dashboard analysis.