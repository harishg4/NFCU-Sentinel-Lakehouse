# CI/CD Promotion and Rollback Runbook

## Purpose

Operational steps for promoting the Databricks bundle across `dev -> qa -> prod` and performing rollback if a release fails.

## Prerequisites

- GitHub Environments configured: `dev`, `qa`, `prod`
- Required reviewers enabled for `qa` and `prod` environments
- Environment secrets configured:
  - `DATABRICKS_HOST`
  - `DATABRICKS_TOKEN`
- Optional notification secrets:
  - `SLACK_WEBHOOK_URL`
  - `PAGERDUTY_EVENTS_URL`

## Promotion Flow

1. Merge PR into `main`.
2. Verify `ci` workflow passed (lint/tests).
3. `databricks-cd` auto-deploys to `dev` on `main`.
4. Trigger `databricks-cd` manually:
   - `target=qa`
   - `run_job=true` (or `false` for deploy-only)
5. Approve `qa` environment gate and verify run.
6. Trigger `databricks-cd` manually:
   - `target=prod`
   - `run_job=true` (or `false` for deploy-only)
7. Approve `prod` environment gate and verify run.

## Rollback Flow

Use the same `databricks-cd` workflow with a known good commit/tag:

1. Open `databricks-cd` -> `Run workflow`.
2. Set:
   - `target`: `dev`/`qa`/`prod`
   - `rollback_ref`: `<tag-or-commit-sha>`
   - `run_job`: `true` (or `false` if only redeploy is needed)
3. Run and approve gate for `qa`/`prod` when prompted.
4. Validate system health and table freshness after rollback.

## Verification Checklist

- Databricks run status is `TERMINATED/SUCCESS`.
- Bronze tables exist and row counts are non-zero.
- No critical alerts in Slack/PagerDuty.
- Audit trail/comment added to Linear release task.
