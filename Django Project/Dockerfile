FROM python:3.14.6-slim AS build

ARG uv_version=0.11.31
ARG python_version=3.14

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/$uv_version/install.sh /uv-installer.sh
RUN sh /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH" \
    UV_PYTHON="python$python_version" \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONOPTIMIZE=1

COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,destination=/root/.cache/uv uv sync \
    --no-dev \
    --no-install-project \
    --frozen


FROM python:3.14.6-slim

ARG user_id=1000
ARG group_id=1001

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --gid $group_id app && \
    adduser --disabled-password --home /app --uid $user_id --gid $group_id app && \
    chown -R $user_id:$group_id /app;

ENV PATH=/app/venv/bin:$PATH \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

COPY --chown=$user_id:$group_id django-project /app
COPY --link --chown=$user_id:$group_id --from=build /app/venv /app/venv

EXPOSE 8000/tcp
STOPSIGNAL SIGINT

USER $user_id:$group_id

CMD ["/bin/sh", "/app/run.sh"]
