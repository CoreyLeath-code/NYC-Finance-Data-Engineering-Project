FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Apply available Debian security fixes during the image build. Release images
# remain gated by Trivy, so fixable HIGH/CRITICAL findings are remediated rather
# than ignored or waived.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade \
      "pip>=26.1,<27" \
      "setuptools>=80.9,<81" \
      "wheel>=0.46.2,<0.47" \
      "jaraco.context>=6.1,<7" \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home /app app

FROM base AS api
COPY api/requirements.txt /tmp/requirements.txt
RUN python -m pip install --requirement /tmp/requirements.txt \
    && rm -rf \
        /usr/local/bin/pip \
        /usr/local/bin/pip3 \
        /usr/local/bin/pip3.11 \
        /usr/local/lib/python3.11/site-packages/pip \
        /usr/local/lib/python3.11/site-packages/pip-*.dist-info
COPY --chown=app:app api ./api
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]

FROM base AS etl
COPY requirements/etl.txt /tmp/requirements.txt
RUN python -m pip install --requirement /tmp/requirements.txt
COPY --chown=app:app src ./src
COPY --chown=app:app run_etl.py run_etl.sh ./
USER 10001:10001
CMD ["python", "run_etl.py"]

FROM base AS dashboard
COPY requirements/dashboard.txt /tmp/requirements.txt
RUN python -m pip install --requirement /tmp/requirements.txt
COPY --chown=app:app dashboard ./dashboard
USER 10001:10001
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
