## slim версия

```dockerfile
# Базовый образ Python на Debian slim для этапа сборки зависимостей.
FROM python:3.14.6-slim AS builder

# Версия Python и UV.
ARG python_version=3.14
ARG uv_version=0.11.31

# Используем sh с режимами:
# -e: остановка при ошибке,
# -x: вывод выполняемых команд,
# -c: выполнение строки команды.
SHELL ["/bin/sh", "-exc"]

# Рабочая директория внутри контейнера.
WORKDIR /app

# Устанавливаем curl и ca-certificates, чтобы скачать установщик uv по HTTPS.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl

# Скачиваем официальный установщик uv.
ADD https://astral.sh/uv/$uv_version/install.sh /uv-installer.sh

# Устанавливаем uv в образ сборщика.
RUN sh /uv-installer.sh

# Настраиваем окружение для uv и Python:
# PATH добавляет uv в доступные команды,
# UV_PYTHON фиксирует версию Python,
# UV_PYTHON_DOWNLOADS=never запрещает uv скачивать Python,
# UV_PROJECT_ENVIRONMENT задает путь к виртуальному окружению,
# UV_LINK_MODE=copy копирует файлы вместо ссылок,
# UV_COMPILE_BYTECODE=1 компилирует .pyc при установке,
# PYTHONOPTIMIZE=1 запускает Python в оптимизированном режиме.
ENV PATH="/root/.local/bin/:$PATH" \
    UV_PYTHON="python$python_version" \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONOPTIMIZE=1

# Копируем только файлы зависимостей, чтобы слой установки кешировался отдельно от кода приложения.
COPY pyproject.toml uv.lock /app/

# Устанавливаем production-зависимости в виртуальное окружение:
# --no-dev исключает dev-зависимости,
# --no-install-project не устанавливает сам проект,
# --frozen требует строго использовать uv.lock,
# cache mount ускоряет повторные сборки.
RUN --mount=type=cache,destination=/root/.cache/uv uv sync \
  --no-dev \
  --no-install-project \
  --frozen


# Финальный runtime-образ на Debian slim.
FROM python:3.14.6-slim

# UID и GID пользователя приложения, чтобы не запускать процесс от root.
ARG user_id=1000
ARG group_id=1000

# Рабочая директория приложения.
WORKDIR /app

# Используем sh с остановкой при ошибках и выводом команд.
SHELL ["/bin/sh", "-exc"]

# Устанавливаем runtime-зависимости:
# curl и ca-certificates нужны для HTTPS-запросов.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl

# Создаем группу и пользователя приложения, затем назначаем владельца директории /app.
RUN addgroup --gid $group_id app && \
    adduser --disabled-password --home /app --uid $user_id --gid $group_id app && \
    chown -R $user_id:$group_id /app;

# Настраиваем runtime-окружение:
# PATH добавляет venv первым,
# PYTHONOPTIMIZE включает оптимизированный режим,
# PYTHONFAULTHANDLER выводит traceback при аварийных ошибках,
# PYTHONUNBUFFERED отключает буферизацию stdout/stderr.
ENV PATH=/app/venv/bin:$PATH \
    PYTHONOPTIMIZE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

# Копируем код приложения и сразу назначаем владельца.
COPY --chown=$user_id:$group_id . /app

# Копируем готовое виртуальное окружение из builder-этапа.
COPY --link --from=builder /app/venv/ /app/venv


# Переключаемся на непривилегированного пользователя.
USER $user_id:$group_id

# Документируем порт, который слушает приложение.
EXPOSE 8000/tcp

# При остановке контейнера отправляем SIGINT приложению.
STOPSIGNAL SIGINT

# Команда запуска приложения.
CMD ["/bin/bash", "/app/run.sh"]
```

## alpine версия

```dockerfile
# Базовый образ Python на Alpine для этапа сборки зависимостей.
FROM python:3.14.6-alpine AS builder

# Используем sh с режимами:
# -e: остановка при ошибке,
# -x: вывод выполняемых команд,
# -c: выполнение строки команды.
SHELL ["/bin/sh", "-exc"]

# Версия Python и UV.
ARG python_version=3.14
ARG uv_version=0.11.31

# Рабочая директория внутри контейнера.
WORKDIR /app

# Устанавливаем build-зависимости:
# curl и ca-certificates нужны для скачивания uv по HTTPS.
RUN apk add --update --no-cache \
    curl \
    ca-certificates

# Скачиваем официальный установщик uv.
ADD https://astral.sh/uv/$uv_version/install.sh /uv-installer.sh

# Устанавливаем uv в образ сборщика.
RUN sh /uv-installer.sh

# Настраиваем окружение для uv и Python.
ENV PATH="/root/.local/bin/:$PATH" \
    UV_PYTHON="python$python_version" \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONOPTIMIZE=1

# Копируем только файлы зависимостей, чтобы слой установки кешировался отдельно от кода приложения.
COPY pyproject.toml uv.lock /app/

# Устанавливаем production-зависимости в виртуальное окружение.
RUN --mount=type=cache,destination=/root/.cache/uv uv sync \
  --no-dev \
  --no-install-project \
  --frozen

# Финальный runtime-образ на Alpine.
FROM python:3.14.6-alpine

# UID и GID пользователя приложения.
ARG user_id=1000
ARG group_id=1001

# Рабочая директория приложения.
WORKDIR /app

# Используем sh с остановкой при ошибках и выводом команд.
SHELL ["/bin/sh", "-exc"]

# Устанавливаем runtime-зависимости:
# curl и ca-certificates нужны для HTTPS-запросов.
RUN apk add --update --no-cache \
    ca-certificates \
    curl

# Создаем группу и пользователя приложения, затем назначаем владельца директории /app.
RUN addgroup -g $group_id appgroup \
    && adduser -D -h /app -u $user_id app $group_id \
    && chown -R $user_id:$group_id /app;

# Настраиваем runtime-окружение:
# PATH добавляет venv первым,
# PYTHONOPTIMIZE включает оптимизированный режим,
# PYTHONFAULTHANDLER выводит traceback при аварийных ошибках,
# PYTHONUNBUFFERED отключает буферизацию stdout/stderr.
ENV PATH=/app/venv/bin:$PATH \
    PYTHONOPTIMIZE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

# Копируем код приложения и сразу назначаем владельца.
COPY --chown=$user_id:$group_id . /app

# Копируем готовое виртуальное окружение из builder-этапа.
COPY --link --from=builder /app/venv/ /app/venv

# Переключаемся на непривилегированного пользователя.
USER $user_id:$group_id

# Документируем порт, который слушает приложение.
EXPOSE 8000/tcp

# При остановке контейнера отправляем SIGINT приложению.
STOPSIGNAL SIGINT

# Команда запуска приложения. В Alpine bash отсутствует по умолчанию.
CMD ["/bin/sh", "/app/run.sh"]
```
