# SalesGenius AI — Phase 1 System Architecture

## 1) Monorepo Architecture
- `frontend/`: Next.js 15 app (React 19, TypeScript, Tailwind, shadcn/ui).
- `backend/`: FastAPI services (REST APIs, auth, CRM, integrations gateway).
- `ai/`: LangGraph orchestration layer (agents, tools, memory, RAG pipelines).
- `shared/`: cross-layer contracts (schemas, API types, common constants).
- `infra/`, `docker/`, `nginx/`, `.github/`, `scripts/`, `docs/`: ops + delivery + docs.

## 2) Runtime Topology
- Client communicates with FastAPI gateway.
- FastAPI routes synchronous requests and dispatches async jobs to Celery.
- Celery workers process AI generation, enrichment, and integration sync tasks.
- Redis supports queueing, caching, and short-lived session/operation state.
- PostgreSQL stores transactional SaaS data.
- Qdrant stores embeddings for semantic retrieval.
- Object storage (S3) stores exports and generated documents.

## 3) AI & Agent Architecture
- LangGraph-driven agents per business domain (research, email, proposal, meeting, CRM, analytics, follow-up, pipeline).
- Tool-calling adapters for CRM data access, integrations, and document generation.
- RAG subsystem: ingestion pipeline → chunking/embedding → vector retrieval → grounded response generation.
- Memory strategy: session memory + organization context memory with governance controls.

## 4) API-First Principles
- Versioned REST APIs (`/api/v1/...`) with strict request/response schemas.
- Unified error envelope, trace IDs, and deterministic status codes.
- OAuth/integration callback routes isolated under integration boundaries.
- OpenAPI/Swagger generated from source models.

## 5) Security Architecture Baseline
- JWT access/refresh token lifecycle with rotation.
- Organization-aware RBAC and permission checks in service layer.
- Rate limiting and abuse controls at API edge.
- Audit trail for identity, billing, admin, and data-modifying actions.
- Secrets via environment-based secret managers for all environments.
