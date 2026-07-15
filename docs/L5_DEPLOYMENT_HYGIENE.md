# L5 Nine-Tier Deployment Hygiene

L5 means each tier has repository implementation, automated evidence, a named owner, and a documented operational response. It is an engineering baseline, not regulatory certification.

| Tier | Control | Evidence |
|---:|---|---|
| 1 | Reproducibility | bounded dependencies, Python 3.11, seeded benchmark, versioned JSON schema |
| 2 | Data integrity | required schema, type/value validation, deduplication, atomic output |
| 3 | Code quality | Ruff, Bandit, pytest, focused coverage gate, dependency audit |
| 4 | Artifact hygiene | separate minimal images, non-root UID, health check, no pip cache |
| 5 | Environment parity | Compose health dependencies, read-only filesystems, pinned Postgres |
| 6 | Orchestration safety | offline schema validation, probes, limits, rolling updates, seccomp, network policy |
| 7 | Supply-chain trust | Trivy gate, SPDX SBOM, GHCR immutable release, keyless Cosign signature |
| 8 | Observability | pipeline metrics, health/readiness, Prometheus request and latency metrics |
| 9 | Governance | CODEOWNERS, private disclosure, limitations, release and rollback procedure |

## Release gates

A release requires green CI, a passing image scan, an uploaded SBOM, benchmark provenance, an immutable version tag, signature verification, and an identified rollback owner. Apply Kubernetes changes with `kubectl rollout status`; revert with `kubectl rollout undo deployment/nyc-finance-api`.

## Exceptions

Any waiver must identify the risk, owner, compensating control, expiry date, and removal plan. Cloud IAM, managed secrets, encryption keys, production network policy, backups, data retention, and incident response remain environment-specific responsibilities.
