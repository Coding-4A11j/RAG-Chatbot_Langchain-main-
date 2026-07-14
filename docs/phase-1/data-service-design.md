# SalesGenius AI — Phase 1 Data & Service Design

## 1) Bounded Contexts
- **Auth & Identity**: users, credentials, sessions, MFA, OAuth identities.
- **CRM Core**: leads, companies, deals, tasks, notes, tags, pipeline stages.
- **Intelligence**: enrichment requests/results, source metadata, risk/opportunity analysis.
- **Outreach**: email templates, generated variants, campaigns, sends, replies.
- **Meetings**: meeting events, notes, action items, follow-up artifacts.
- **Analytics**: KPI snapshots, funnel metrics, performance aggregates.
- **Billing**: plans, subscriptions, invoices, usage events.
- **Admin & Governance**: audit logs, API keys, integration configs, role policies.

## 2) Core Entity Ownership
- Auth owns user lifecycle and access artifacts.
- CRM owns lead/company/deal lifecycle and pipeline state.
- Outreach owns message generation and campaign execution state.
- Intelligence owns enrichment pipelines and derived strategic outputs.
- Analytics consumes event streams and materialized summaries.
- Billing governs feature entitlements and usage limits.

## 3) Integration Strategy
- Provider adapter model with normalized integration interface.
- Initial priority adapters:
  - Google (Calendar/Gmail)
  - Outlook
  - Slack
  - Stripe
  - HubSpot/Salesforce bridge points
- Webhook ingestion with signature validation, replay protection, and idempotency keys.
- Outbound integration tasks executed via Celery with retry/backoff and dead-letter policy.

## 4) Data Governance Baseline
- Organization-scoped row ownership and enforced tenant filters.
- Soft-delete for business records requiring auditability.
- PII-aware logging policy and redaction for sensitive fields.
- Index-first strategy for high-cardinality filters (pipeline, owner, status, timestamps).
