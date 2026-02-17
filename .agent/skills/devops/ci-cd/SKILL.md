---
name: ci-cd
version: "6.3.1"
category: infrastructure
---

# CI/CD Pipelines

CI/CD pipeline patterns for GitHub Actions, GitLab CI, and GitOps. Includes SLSA Build Level 3, ARM64 runners, security scanning.

## Decision Tree

```
Task → What CI/CD platform?
  ├─ GitHub Actions
  │   ├─ Simple project → Single workflow file
  │   ├─ Monorepo → Path filters + matrix
  │   └─ Org-wide → Reusable workflows (workflow_call)
  ├─ GitLab CI
  │   ├─ Simple → .gitlab-ci.yml stages
  │   └─ Multi-project → Pipeline triggers
  └─ Deployment strategy
      ├─ Simple → Push-to-deploy (main branch)
      ├─ Staged → Environment promotion (dev → staging → prod)
      ├─ Zero-downtime → Blue/green with health checks
      └─ Risk-managed → Canary with progressive rollout
```

## Quick Start — GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build-test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "npm"
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

  deploy:
    needs: build-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    permissions:
      id-token: write # OIDC
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: npm ci && npm run build
      - run: aws s3 sync dist/ s3://${{ vars.BUCKET }}
```

## Quick Start — Reusable Workflow

```yaml
# .github/workflows/reusable-build.yml
name: Build
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: "22"
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci
      - run: npm run build
```

```yaml
# Caller workflow
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: "22"
```

## Security Best Practices

- [ ] Pin actions to full SHA: `uses: actions/checkout@abc123`
- [ ] Use OIDC for cloud auth (no long-lived secrets)
- [ ] Set `permissions` on job/workflow level (least privilege)
- [ ] Enable Dependabot for workflow dependency updates
- [ ] Add `timeout-minutes` on all jobs
- [ ] Use `continue-on-error: false` (default, be explicit)
- [ ] Cache dependencies to reduce build time
- [ ] Scan with CodeQL and dependency review
- [ ] Generate SBOM for supply chain security
- [ ] Use SLSA Level 3 attestation for artifacts

## Patterns (20 total)

### GitHub Actions (6)

- Reusable workflows with `workflow_call`
- Composite actions for shared steps
- ARM64 runner configuration (GitHub-hosted)
- SLSA Build Level 3 attestation
- Matrix builds with dynamic strategy
- Deployment environments with protection rules

### GitLab CI (5)

- Multi-project pipeline orchestration
- Auto DevOps configuration
- GitLab Container Registry integration
- Merge train configuration
- Dynamic child pipelines

### Security (5)

- Dependency review action (license + vulnerability)
- Code scanning with CodeQL
- Secret scanning with push protection
- Artifact attestation (SLSA provenance)
- Supply chain security (SBOM generation)

### Deployment (4)

- Blue/green deployment patterns
- Canary release with progressive rollout
- GitOps with ArgoCD/Flux
- Multi-environment promotion pipeline

## Data Files

- `data/github-actions.yaml` — GitHub Actions patterns
- `data/gitlab-ci.yaml` — GitLab CI patterns
- `data/security.yaml` — Pipeline security patterns
