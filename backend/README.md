# backend

Phase 2/3 backend foundation for SalesGenius AI.

## Run locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Available endpoints
- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`
- `GET /api/v1/meta`

## Database migrations (Alembic)

```bash
cd backend
alembic upgrade head
```
