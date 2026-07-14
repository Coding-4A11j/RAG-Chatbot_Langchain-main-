# SalesGenius AI — Phase 1 Engineering Standards

## 1) Architecture Rules
- Apply Clean Architecture per bounded context.
- Enforce service layer orchestration and repository abstraction for persistence.
- Keep frameworks at outer layers; core domain logic remains framework-agnostic.
- Use dependency injection at application/service boundaries.

## 2) Validation & Error Contracts
- Validate all input using typed schemas at API boundaries.
- Return consistent error envelopes with machine-readable error codes.
- Separate user-safe messages from internal diagnostic metadata.

## 3) Observability Baseline
- Structured logs with trace/correlation IDs.
- Metrics for API latency, queue depth, job execution success/failure.
- Health and readiness probes for all critical services.

## 4) Security Defaults
- Principle of least privilege for users, service accounts, and integrations.
- Mandatory RBAC checks on every protected endpoint.
- Input sanitization and parameterized database access only.
- Secure headers and transport security enforced by edge configuration.

## 5) Test Strategy Gates
- Unit tests for domain logic and service contracts.
- Integration tests for API + persistence + queue paths.
- End-to-end flows for critical user journeys.
- Security-focused tests for auth, access control, and input handling.

## 6) Definition of Done (Module-Level)
A module is complete when:
1. Functional scope and API contracts are implemented.
2. Required tests pass at unit/integration levels.
3. Security checks and validation rules are enforced.
4. Observability hooks are present for production operations.
5. Documentation and changelog are updated.
6. Phase review approval is received before progressing.
