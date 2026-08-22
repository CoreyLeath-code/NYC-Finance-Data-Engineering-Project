# Changelog

All notable changes to the NYC Finance Data Engineering Project are documented here.

## [Unreleased]

## [1.1.0] - 2026-08-22

### Added

- Semantic-tag GitHub Release workflow with source archive and SHA-256 checksum.
- Manual release recovery for existing semantic version tags.
- L6 engineering audit covering lineage, schema evolution, readiness, load testing, storage integration, and provenance.
- Expanded benchmark provenance including commit SHA, runner metadata, CPU information, explicit warm-up count, and nanosecond timing clock.

### Changed

- Rebuilt the README around the verified CSV ETL, FastAPI, Compose, Kubernetes, benchmark, and supply-chain boundaries.
- Added parser-safe architecture and system-design Mermaid diagrams.
- Clarified that in-memory ETL benchmarks are not streaming, warehouse, network, or production-capacity evidence.
- Hardened the GHCR supply-chain workflow with a stable lowercase image name and optional manual semantic-tag publication.

## [1.0.1] - 2025-06-10

### Fixed

- Corrected null-handling behavior in the historical load path.
- Improved transformation handling for an additional source column.

## [1.0.0] - 2025-05-25

### Added

- Initial NYC Finance data engineering project with extract, transform, load, tests, and CI foundations.

[Unreleased]: https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/CoreyLeath-code/NYC-Finance-Data-Engineering-Project/releases/tag/v1.0.0
