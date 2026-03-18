# CI/CD — Advanced Patterns

## Table of Contents

- [GitHub Actions Advanced](#github-actions-advanced)
- [GitLab CI Patterns](#gitlab-ci-patterns)
- [Matrix & Reusable Workflows](#matrix--reusable-workflows)
- [Security in CI/CD](#security-in-cicd)
- [Deployment Strategies](#deployment-strategies)

---

## GitHub Actions Advanced

### Optimized Build Pipeline

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api: ['api/**', 'shared/**']
            web: ['web/**', 'shared/**']

  test-api:
    needs: changes
    if: needs.changes.outputs.api == 'true'
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 5s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: 'api/go.mod'
          cache: true
      - run: go test ./... -race -coverprofile=coverage.out
        working-directory: api
      - uses: codecov/codecov-action@v4
        with:
          file: api/coverage.out

  test-web:
    needs: changes
    if: needs.changes.outputs.web == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: 'web/.nvmrc'
          cache: 'pnpm'
          cache-dependency-path: 'web/pnpm-lock.yaml'
      - run: pnpm install --frozen-lockfile && pnpm test
        working-directory: web
```

---

## GitLab CI Patterns

### Pipeline with Stages

```yaml
stages: [test, build, deploy]

variables:
  DOCKER_BUILDKIT: "1"

.go-cache: &go-cache
  cache:
    key: go-${CI_COMMIT_REF_SLUG}
    paths: [.cache/go]
    policy: pull-push

test:
  stage: test
  image: golang:1.24
  <<: *go-cache
  script:
    - go test ./... -race -count=1
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

build:
  stage: build
  image: docker:27
  services: [docker:27-dind]
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

---

## Matrix & Reusable Workflows

### Matrix Strategy

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    go-version: ['1.23', '1.24']
    exclude:
      - os: macos-latest
        go-version: '1.23'
    include:
      - os: ubuntu-latest
        go-version: '1.24'
        coverage: true
```

### Reusable Workflow

```yaml
# .github/workflows/deploy.yml (reusable)
on:
  workflow_call:
    inputs:
      environment: { type: string, required: true }
      image_tag: { type: string, required: true }
    secrets:
      KUBE_CONFIG: { required: true }

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: azure/k8s-set-context@v4
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      - run: |
          kubectl set image deployment/api api=${{ inputs.image_tag }}
          kubectl rollout status deployment/api --timeout=300s

# Caller workflow
jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
      image_tag: ghcr.io/myorg/api:${{ github.sha }}
    secrets: inherit
```

---

## Security in CI/CD

```yaml
security_checklist:
  secrets:
    - "Use GitHub/GitLab secrets (never hardcode)"
    - "Rotate keys quarterly"
    - "Use OIDC for cloud auth (no long-lived tokens)"
    - "Mask secrets in logs: echo '::add-mask::$SECRET'"
  supply_chain:
    - "Pin action versions by SHA: actions/checkout@abc123"
    - "Use dependabot/renovate for action updates"
    - "Sign commits and artifacts (Sigstore/cosign)"
    - "SBOM generation: syft, trivy"
  permissions:
    - "Minimal GITHUB_TOKEN permissions per job"
    - |
      permissions:
        contents: read
        packages: write
  scanning:
    - "SAST: CodeQL, Semgrep"
    - "SCA: Snyk, Trivy"
    - "Container: docker scout, grype"
    - "Secrets: gitleaks, trufflehog"
```

---

## Deployment Strategies

```yaml
strategies:
  blue_green:
    description: "Two identical environments, switch traffic"
    rollback: "Instant (switch back)"
    downtime: "Zero"
    cost: "2x infrastructure during deployment"

  canary:
    description: "Route small % of traffic to new version"
    steps:
      - "Deploy canary (5% traffic)"
      - "Monitor metrics (error rate, latency)"
      - "Increase to 25%, 50%, 100%"
      - "Rollback if metrics degrade"

  rolling:
    description: "Replace instances one by one"
    config: |
      spec:
        strategy:
          type: RollingUpdate
          rollingUpdate:
            maxSurge: 25%
            maxUnavailable: 0

  feature_flags:
    description: "Deploy code, enable via flag"
    tools: ["LaunchDarkly", "Unleash", "Flagsmith"]
    benefit: "Decouple deployment from release"
```

---
