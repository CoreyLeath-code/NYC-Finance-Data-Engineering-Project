# NYC Finance Data Engineering Project

[![CI](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/actions/workflows/ci.yml)
[![Supply chain](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/actions/workflows/supply-chain.yml/badge.svg?branch=main)](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/actions/workflows/supply-chain.yml)
[![License](https://img.shields.io/github/license/CoreyLeath-code/NYC-Finance-Data-Engineering-Project)](LICENSE)

A research-oriented data engineering reference implementation for validating, transforming, benchmarking, serving, and monitoring NYC finance time-series data.

> This repository uses synthetic examples and is not a production financial reporting or trading system. Do not process confidential financial records without environment-specific access controls, retention rules, encryption, auditing, and legal review.


## Production Readiness Guide

> This section is the portfolio audit entry point for **NYC-Finance-Data-Engineering-Project**. It describes an engineering promotion path; it is not a claim that the repository is already production-authorized.

[![CI](https://img.shields.io/github/actions/workflow/status/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/ci.yml?branch=main&label=CI)](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/actions) [![License](https://img.shields.io/github/license/CoreyLeath-code/NYC-Finance-Data-Engineering-Project)](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/blob/main/LICENSE)

### Architecture flowchart

```mermaid
flowchart LR
    Client --> Gateway --> Services[API + workers] --> Events[(Event bus)] --> Store[(State)]
```

### Quickstart and local validation

The supported local path should be reproducible from a clean checkout. The inferred stack for this repository is **Python/platform services**.

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
pytest -q
```

If the project uses external services, model artifacts, cloud credentials, or private data, start them through documented local fixtures or mocks. Never place secrets or identifiable records in the repository.

### Research-style metrics and benchmarks

| Evidence | Required record |
|---|---|
| Correctness | Test command, commit SHA, runtime, and pass/fail result |
| Performance | Warm-up, sample count, concurrency, median, p95, p99, throughput, and memory |
| Data/model quality | Dataset version, split strategy, leakage controls, calibration, subgroup results, and uncertainty |
| Runtime | Image digest, health-check latency, resource limits, and rollback target |
| Security | Dependency, secret, SAST, container, and SBOM results |

A benchmark number belongs in a versioned artifact tied to a commit and hardware/runtime description. Engineering benchmarks must not be presented as clinical, financial, safety, or model-quality validation without the appropriate domain evidence.

### Extended Q&A

**What is production-ready for this repository?**  
A reproducible build, tested public contract, controlled configuration, observable runtime, documented security boundary, versioned artifacts, and a tested rollback path.

**What must remain explicit?**  
The intended use, excluded use, data/credential handling, model or algorithm limitations, and which metrics are measured versus aspirational.

**What should be completed next?**  
Use the linked production-readiness issue for this repository as the checklist. Resolve missing tests, deployment instructions, observability, supply-chain controls, and release evidence before attaching a production claim.


## Research objective

The primary engineering question is: how reliably and efficiently can the pipeline validate and transform a documented finance time-series contract under a repeatable workload?

The benchmark reports:

- median and p95 transform duration
- median rows per second
- input/output row counts
- null-cell count
- dataset size and random seed
- Python, pandas, NumPy, and platform versions
- individual timing samples

## Metrics and benchmark status

The former README listed throughput, RPS, completeness, drift sensitivity, and coverage values without a versioned result artifact or reproducible protocol. Those numbers are not retained as research findings.

| Measure | Recorded | Current published result |
|---|---:|---:|
| Median transform duration | Yes | Pending a committed environment-labeled run |
| P95 transform duration | Yes | Pending |
| Median rows/second | Yes | Pending |
| Input/output rows | Yes | Pending |
| Null cells | Yes | Pending |
| API request count/latency | Runtime telemetry | Environment-specific |
| Test coverage | Enforced in CI | See current workflow run |

Run the deterministic microbenchmark:

```bash
python -m pip install -r requirements.txt
python benchmarks/pipeline_benchmark.py \
  --rows 100000 \
  --repeats 5 \
  --seed 2026 \
  --output benchmarks/results/latest.json
```

The JSON file is the canonical result record. Before publishing a result, add the commit SHA, runner hardware, storage mode, dataset provenance, and whether caches were warm. Synthetic microbenchmarks do not establish production Kafka, warehouse, network, or end-to-end performance.

## Data contract

Required input columns:

| Column | Constraint |
|---|---|
| `timestamp` | parseable timestamp; normalized to UTC |
| `open` | numeric and greater than zero |
| `close` | numeric |
| `volume` | numeric and non-negative |

The ETL pipeline rejects missing columns, invalid values, and empty inputs; removes duplicate rows; sorts by timestamp; derives return and weekday fields; and replaces the processed CSV atomically.

## Senior review follow-up: lineage, quality, and reproducibility

This section closes the documentation items tracked in [issue #8](https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/issues/8). The benchmark is intentionally scoped to deterministic in-memory transformation work; it is not an end-to-end streaming, warehouse, or financial-performance claim.

### Verification contract

From a clean checkout:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
pytest tests api/test_api.py
python benchmarks/pipeline_benchmark.py --output benchmarks/results/latest.json
python -m json.tool benchmarks/results/latest.json
docker compose config --quiet
docker compose up --build -d api dashboard
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
curl http://localhost:8000/metrics
docker compose down
```

The JSON benchmark must include the commit SHA, dataset/provenance identifier, row volume, warm-up policy, storage mode, runner hardware, and whether caches were warm. CI coverage, dependency/secret/container scan results, image digest, and SBOM are release evidence and should be linked to the workflow run that produced them.

### Engineering decisions and data failure modes

- **Contract-first ETL:** schema and value checks make drift visible before serving, but upstream contract changes still require an explicit migration or quarantine policy.
- **Idempotency vs. backfill speed:** atomic outputs make retries safe, while large historical backfills need bounded batches, checkpointing, and a reconciliation report.
- **Local Compose vs. production topology:** Compose is a reproducible developer boundary; Kafka, Airflow, cloud IAM, warehouse performance, and multi-region recovery remain environment-specific extensions.
- **Next production step:** attach a versioned sample dataset and lineage record to the benchmark, then exercise a schema-drift fixture and a failed-write recovery path before making throughput or quality claims.


## Quick start

```bash
git clone https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project.git
cd NYC-Finance-Data-Engineering-Project
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
pytest tests api/test_api.py
```

Run the local API and dashboard:

```bash
docker compose up --build api dashboard
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
curl http://localhost:8000/metrics
```

Run ETL after placing a contract-compatible CSV at `data/raw/nyc_finance_synthetic.csv`:

```bash
docker compose --profile pipeline run --rm etl
```

## API boundaries

The API loads a model only when `/predict` is called. Without `MODEL_PATH`, health remains available, readiness reports `degraded`, and prediction returns HTTP 503. Feature vectors must contain 1–512 numeric values and unknown request fields are rejected.

## L5 nine-tier deployment hygiene

| Tier | Control | Repository evidence |
|---:|---|---|
| 1 | Reproducibility | bounded dependencies, deterministic benchmark, JSON provenance |
| 2 | Data integrity | schema, type/value checks, deduplication, atomic output |
| 3 | Code quality | Ruff, Bandit, pytest, focused coverage, pip-audit |
| 4 | Artifact hygiene | minimal API/ETL/dashboard stages, non-root user, health check |
| 5 | Environment parity | Compose health conditions, pinned Postgres, read-only services |
| 6 | Orchestration safety | probes, resources, rolling updates, seccomp, default-deny network policy |
| 7 | Supply-chain trust | Trivy, SPDX SBOM, GHCR version tags, keyless Cosign signing |
| 8 | Observability | pipeline metrics plus health, readiness, request, and latency endpoints |
| 9 | Governance | CODEOWNERS, SECURITY.md, limitations, release gates, rollback |

See [docs/L5_DEPLOYMENT_HYGIENE.md](docs/L5_DEPLOYMENT_HYGIENE.md) for evidence, release gates, exceptions, and residual environment responsibilities.

## Deployment

Validate locally:

```bash
docker build --target api -t nyc-finance-api:local .
docker compose config --quiet
docker run --rm -v "$PWD:/work" ghcr.io/yannh/kubeconform:v0.7.0 \
  -strict -summary /work/infra/k8s
```

Release images are built, scanned, supplied with an SPDX SBOM, pushed to GHCR, and signed when a semantic version tag such as `v0.2.0` is pushed. Replace the example Kubernetes image tag with the verified immutable release digest before deployment.

```bash
kubectl apply -f infra/k8s/
kubectl rollout status deployment/nyc-finance-api
kubectl rollout undo deployment/nyc-finance-api
```

## Repository layout

```text
api/                    validated inference and operations API
benchmarks/             reproducible performance protocol
dashboard/              Streamlit visualization
src/pipelines/          ETL contracts and transformation
tests/                  ETL tests
requirements/           minimal service dependencies
infra/k8s/              deployment, service, and network policy
.github/workflows/      quality and supply-chain automation
docs/                   L5 control evidence
```

## Implemented versus optional architecture

Implemented and verified here: CSV ETL, FastAPI, Streamlit, PostgreSQL Compose service, Docker, Kubernetes manifests, Prometheus metrics, CI, scanning, SBOM, and release signing.

Kafka, Airflow, Snowflake, S3, MLflow tracking, and multi-region cloud infrastructure appear in exploratory modules or architecture history but are not validated by the default local deployment or benchmark. Treat them as optional extensions until they have environment-specific integration tests and measured evidence.

## Known limitations

- No versioned public production dataset or published benchmark artifact is included.
- The benchmark measures in-memory transform work, not end-to-end streaming or warehouse latency.
- The repository does not ship a trained model.
- Readiness is informational and returns HTTP 200 with a degraded status when the model is absent.
- Cloud IAM, secrets, encryption, backups, retention, cost controls, and incident response are deployment-specific.

## License

See the repository license. Dataset licensing and financial-data obligations are separate from the source-code license.
