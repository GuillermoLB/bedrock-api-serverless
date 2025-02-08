# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTETIME=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Create a non-privileged user first
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Then create directories and set permissions
RUN mkdir -p migrations/versions && \
    chown -R appuser:appuser migrations && \
    chmod -R 777 migrations

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code
COPY . .
RUN chown -R appuser:appuser /app

# Switch to non-privileged user
USER appuser

EXPOSE 8000

CMD uvicorn 'app.main:app' --host=0.0.0.0 --port=8000
