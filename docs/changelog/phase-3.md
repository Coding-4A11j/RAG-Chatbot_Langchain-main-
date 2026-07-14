# Changelog — Phase 3

## Date
2026-07-14

## Completed
- Added SQLAlchemy database foundation (`Base`, naming conventions, timestamp mixin, engine/session setup).
- Added initial SalesGenius domain models for:
  - organizations, users, companies, leads, deals, meetings, tasks, notes
  - campaigns, emails, activities
  - ai_logs, audit_logs
  - subscriptions, billing_records, integrations
- Added PostgreSQL-focused database configuration via `DATABASE_URL`.
- Added Alembic scaffolding:
  - `backend/alembic.ini`
  - `backend/alembic/env.py`
  - `backend/alembic/script.py.mako`
  - initial migration `backend/alembic/versions/20260714_01_initial_schema.py`
- Updated backend docs and environment example for migration workflow.

## Notes
- This phase provides schema and migration scaffolding; application service/repository usage will be wired in subsequent phases.
