ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /api

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app/ ./app/
COPY artifacts/ ./artifacts/

ENV PATH="/api/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
