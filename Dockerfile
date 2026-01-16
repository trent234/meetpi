# ---- base python ----
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- builder ----
FROM base AS builder

WORKDIR /app

# copy only dependency metadata (cache-friendly)
COPY pyproject.toml ./

# create venv and install deps without uv/lockfile
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir PyJWT>=2.8.0 bottle>=0.12.25

# ---- runtime ----
FROM base AS runtime

# copy venv from builder
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY src ./src

# make the package in src importable when running as a module
ENV PYTHONPATH="/app/src"

# expose port for the web server
EXPOSE 8080

# run - invoke the package module so the installed venv and package layout work
# Use ENTRYPOINT so arguments passed to `docker run` are forwarded to the program.
ENTRYPOINT ["python", "-m", "meetpi.web"]
