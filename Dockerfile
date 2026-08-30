FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

COPY src ./src

RUN uv sync --frozen --no-dev

CMD ["uv", "run", "--no-sync", "python", "-m", "slack_assistant.main"]