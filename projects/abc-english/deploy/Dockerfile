# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# System deps kept minimal. If you later need audio/ffmpeg add here.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ABC_CONFIG=/app/config/settings.docker.yaml

# 1. Install Python dependencies first (layer cache).
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
 && pip install --no-cache-dir gunicorn

# 2. Copy application source.
COPY . /app

EXPOSE 8000

# gunicorn manages worker lifecycle; uvicorn worker handles ASGI.
# web.wsgi exposes a module-level `app` built from create_app().
CMD ["gunicorn", "web.wsgi:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "2", \
     "-b", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
