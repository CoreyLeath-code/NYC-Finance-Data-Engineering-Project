# NYC Finance Data Engineering Project — L6 Engineering Audit

## Executive assessment

This repository has a credible portfolio-scale data engineering core: contract-first pandas ETL, machine-readable benchmark evidence, an operational FastAPI boundary, Prometheus instrumentation, local Compose topology, non-root multi-stage containers, Kubernetes validation, and supply-chain controls.

The primary senior-level concern is **scope separation**. The repository contains exploratory references to broader streaming/cloud technologies, but the verified local path is CSV ETL + local storage/services + FastAPI/Streamlit. Claims should stay anchored to that boundary until integration tests prove otherwise.

## Verified architecture

1. A contract-compatible finance CSV enters the ETL path.
2. Required columns and numeric/value constraints are validated.
3. Timestamps are normalized, duplicates removed, rows sorted, and derived fields calculated.
4. Processed output is replaced atomically.
5. The benchmark calls the transform function against a deterministic synthetic dataset.
6. The FastAPI service provides liveness, readiness, metrics, and lazy model inference.
7. The repository does not ship a trained model; prediction fails with 503 when the artifact is unavailable.
8. CI builds API, ETL, and dashboard images and validates Compose/Kubernetes configuration.

## Evidence quality

### Strong evidence

- deterministic synthetic dataset generation with explicit seed
- machine-readable JSON benchmark samples
- median and p95 transform latency
- output-row and null-cell integrity checks
- pytest + coverage gate
- Ruff, Bandit, and pip-audit
- non-root API container verification
- live API health smoke test
- Trivy image scan and SPDX SBOM
- semantic-tag GHCR publishing and Cosign signing

### Evidence that is still missing

- versioned representative external dataset and lineage record
- Postgres write throughput and recovery evidence
- end-to-end network/service latency under controlled concurrency
- schema-evolution/quarantine experiments
- backup/restore and disaster-recovery drills
- environment-specific IAM, encryption, secret rotation, and retention controls
- trained model artifact provenance and model-quality evaluation

## P0 gaps

### 1. Readiness semantics

`/readyz` currently returns HTTP 200 even when its status is `degraded`. If deployment policy requires a model before accepting traffic, readiness should return a failing status code when the artifact is absent.

### 2. Data lineage

A production data platform needs a durable lineage tuple: source identifier, source checksum/version, transformation code commit, schema version, output artifact identifier, and run ID. The current benchmark records useful runtime evidence but not a full source-to-output lineage chain.

### 3. Schema evolution and quarantine

The contract correctly rejects invalid data, but production ingestion also needs a deliberate policy for upstream schema changes: reject, quarantine, migrate, or dual-read. Add fixtures for missing/renamed/new columns and verify the chosen behavior.

### 4. Storage-boundary integration

The in-memory benchmark is valuable regression evidence but says nothing about database ingest, transaction behavior, retries, connection exhaustion, or partial-write recovery. Add Testcontainers-backed Postgres integration tests before making storage-capacity claims.

## P1 gaps

### Controlled load testing

Add a reproducible experiment that measures the complete API and persistence path with:

- fixed hardware/runner identity
- warm-up period
- controlled concurrency levels
- request count and payload shape
- median/p95/p99 latency
- throughput
- error rate
- CPU and memory utilization
- saturation point

### Artifact provenance

When a model is introduced, pin it by immutable digest and record training/evaluation lineage separately from application-image provenance.

### Release provenance

The repository now publishes source archives with SHA-256 checksums and a signed GHCR image. Future hardening should attach SBOM/provenance artifacts directly to the GitHub Release and consider SLSA-compatible attestations.

## Release recommendation

A v1.1.0 portfolio release is appropriate after CI is green because the release is primarily an engineering-contract upgrade: README evidence alignment, benchmark provenance, release automation, and safer manual package recovery. It should not be described as a production financial-platform certification.
