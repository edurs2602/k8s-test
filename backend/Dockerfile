FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install uv --no-cache-dir

COPY pyproject.toml README.md ./

RUN uv pip install --system --no-cache-dir .

FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./app ./app
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]