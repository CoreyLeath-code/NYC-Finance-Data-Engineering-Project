# n8n automation

## Scope and audit

This repository contains a deterministic ETL benchmark and a GitHub Actions `ci.yml` workflow that supports manual dispatch. Its pre-existing n8n workflow scheduled `python train.py`, but no `train.py` exists in the repository. Running it from an n8n container would therefore fail and would also assume the repository checkout, dependencies, input data, and model-training infrastructure exist in that container.

The replacement definition is an inactive manual dispatch of the existing GitHub Actions CI workflow. It lets n8n request the repository's already-defined validation path without duplicating ETL, benchmarking, or model-training logic.

## Required configuration

Use a self-hosted n8n deployment. Do not commit its URL, OAuth credential, or token.

| Variable | Required | Purpose |
| --- | --- | --- |
| `N8N_BASE_URL` | Yes | Base URL for the self-hosted n8n instance. No n8n URL is embedded in workflow JSON. |
| `GITHUB_OWNER` | Yes | GitHub owner; set to `CoreyLeath-code`. |
| `GITHUB_TOKEN` | Optional | HTTP Request fallback only; put it in n8n's environment or credential store, never in the repository. |

Bind one organization-wide GitHub OAuth credential in n8n. The CI-dispatch workflow needs permission to dispatch workflows in this repository; the label bootstrap needs permission to read/create labels.

## Workflows

### Run repository validation

- **Definition:** `n8n/workflow.json`
- **Trigger:** Manual execution only.
- **Actions:** Dispatches the already committed `.github/workflows/ci.yml` on `main`. That workflow is the canonical place for tests, coverage, benchmark smoke testing, image build checks, and deployment-manifest validation.
- **Does not do:** Run missing training code, create a repository checkout in n8n, invent a dataset/model, publish metrics, or deploy infrastructure.
- **Manual execution:** Import the inactive JSON, bind the GitHub OAuth credential, confirm `GITHUB_OWNER`, then activate only for an approved manual run.
- **Failure recovery:** Use the linked GitHub Actions run as the execution record. Disable the workflow if dispatch is unexpected; correct credential permissions or the CI workflow, then retry manually.

### Label bootstrap

- **Definition:** `n8n/label-bootstrap.json`
- **Trigger:** Manual execution only.
- **Actions:** Reads the repository labels and creates only missing labels from the requested organization list. Existing labels and colors are never updated.
- **Manual execution:** Import, bind the GitHub OAuth credential, verify `GITHUB_OWNER`, and run once.
- **Failure recovery:** Correct credential permissions and rerun. It is idempotent because it only posts labels absent from the preceding response.

## Deliberately skipped automation

| Candidate | Reason |
| --- | --- |
| Scheduled training or ETL execution | n8n has no verified checkout, data volume, model artifact, secret, or execution environment for this repository. The prior `train.py` command has no corresponding source file. |
| Automatic benchmark/metric publication | CI already produces reviewable benchmark artifacts; no policy permits an external system to commit or publish hardware-sensitive values. |
| Release automation | Existing supply-chain automation handles release tags, image publishing, SBOMs, and signing. |
| Security monitoring | Existing CI and supply-chain workflows own scanning; no incident-routing destination or escalation policy is present. |
| Issue/PR automation | An open CI baseline PR already addresses GitHub automation, and no review/comment policy is committed. |

## Validation

Each workflow definition is JSON-parsed after committing and is confirmed inactive. No n8n runtime validation occurs here because `N8N_BASE_URL`, the n8n credential binding, and target runtime are not configured in this workspace.