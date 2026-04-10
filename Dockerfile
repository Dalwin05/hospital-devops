# ── Stage 1: build deps ─────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /install
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install/deps --no-cache-dir -r requirements.txt

# ── Stage 2: final image ─────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="your-email@college.edu"
LABEL description="Hospital Management Portal – DevOps Project 24CS2018"

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY --from=builder /install/deps /usr/local
COPY app/       ./app/
COPY templates/ ./templates/
COPY static/    ./static/

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["python", "app/app.py"]
