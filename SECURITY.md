# Security Policy

Report vulnerabilities through GitHub private vulnerability reporting; do not open a public issue. Include affected paths, reproduction steps, impact, and mitigation ideas.

The latest release and `main` are supported. Credentials, NYC financial records, warehouse extracts, model artifacts, and populated `.env` files must never be committed. Production secrets belong in the deployment platform's secret manager.

Release consumers must verify the Cosign signature, review the SPDX SBOM, and deploy immutable image digests.
