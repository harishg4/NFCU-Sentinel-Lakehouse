# Databricks-Native Tech Stack (Finalized Baseline)

## Core Platform

- Databricks Workspace (AWS/GCP acceptable)
- Unity Catalog
- Delta Lake
- Databricks SQL Warehouse

## Ingestion and Processing

- PySpark batch pipelines
- Structured Streaming
- Auto Loader
- JDBC + file/API ingestion connectors

## Orchestration and CI/CD

- Databricks Workflows (replace ADF)
- GitHub for source control
- GitHub Actions or Databricks Asset Bundles CI flow

## Governance and Security

- Unity Catalog ACLs
- Row filters and column masking
- Secrets management via Databricks secret scopes

## Quality and Monitoring

- Config-driven DQ framework (X-001)
- Pipeline monitoring framework (X-002)
- Job alerts + optional Slack/PagerDuty notifications

## BI and Consumption

- Power BI connected to Databricks SQL
- Fraud ops dashboard
- Compliance dashboard
