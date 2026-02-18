# NFCU Project Documentation Hub

This folder is the single source of truth for project context, generated artifacts, and verification evidence.

## Structure

- `00-input/`: Raw source inputs (briefs, screenshots, notes, links)
- `01-context/`: Canonical project summary and scope
- `02-architecture/`: Architecture interpretation and decisions
- `03-tech-stack/`: Finalized technology stack and alternatives
- `04-plan/`: Execution roadmap and milestone breakdown
- `05-verification/`: What was verified, how, and current status
- `06-outputs/`: Publish-ready content (GitHub/LinkedIn summaries, diagrams list)

## Working Rules

1. Add new source files to `00-input/` first.
2. Update derived decisions in `01-context/` and `03-tech-stack/`.
3. Record every check in `05-verification/verification-log.md`.
4. Keep publish-ready drafts in `06-outputs/`.

## Current Direction

- Platform direction: Databricks-native (non-Azure fallback)
- Delivery goals: portfolio-ready GitHub repo + LinkedIn narrative
