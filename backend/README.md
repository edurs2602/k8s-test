# FastAPI Backend

A FastAPI backend application with async SQLAlchemy and PostgreSQL support.

## Features

- FastAPI with async/await support
- SQLAlchemy 2.0 (async) ORM
- Pydantic v2 data validation
- Neon PostgreSQL support
- Alembic database migrations
- UV package management

## Development

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Run development server
uvicorn app.main:app --reload

# Run migrations
alembic upgrade head
```

## Endpoints

- `/` - API info
- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation
- `/health` - Health check endpoint
- `/items` - CRUD operations for items