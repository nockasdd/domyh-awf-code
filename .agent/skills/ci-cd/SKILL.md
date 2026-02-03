---
name: ci-cd
detect:
  [
    ".github/workflows/",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    "azure-pipelines.yml",
    "bitbucket-pipelines.yml",
  ]
version: "6.0.0"
category: devops
tier: 1
---

# CI/CD Patterns — DOMYH Awesome Code v5.5

> Comprehensive guide for GitHub Actions, GitLab CI, Azure DevOps (2025-2026)

## 🔍 Platform Detection

```yaml
detection:
  github_actions:
    - ".github/workflows/*.yml"
    - ".github/workflows/*.yaml"

  gitlab_ci:
    - ".gitlab-ci.yml"
    - ".gitlab-ci.yaml"

  azure_devops:
    - "azure-pipelines.yml"
    - ".azure-pipelines/*.yml"

  jenkins:
    - "Jenkinsfile"
    - "jenkins/*.groovy"

  circleci:
    - ".circleci/config.yml"
```

---

## 📊 Platform Comparison

| Feature          | GitHub Actions              | GitLab CI               | Azure DevOps            |
| ---------------- | --------------------------- | ----------------------- | ----------------------- |
| **Config**       | YAML per workflow           | Single `.gitlab-ci.yml` | YAML pipeline           |
| **Runners**      | GitHub-hosted + Self-hosted | GitLab + Self-hosted    | Microsoft + Self-hosted |
| **Cache**        | `actions/cache`             | Built-in `cache:`       | Pipeline caching        |
| **Artifacts**    | `upload/download-artifact`  | `artifacts:`            | Publish artifacts       |
| **Secrets**      | Secrets + OIDC              | Variables               | Key Vault integration   |
| **Environments** | Environments + Protection   | Environments            | Stages + Approvals      |

---

## 🚀 GitHub Actions

### Complete CI/CD Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch: # Manual trigger

permissions:
  contents: read
  packages: write
  id-token: write # OIDC

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ─────────────────────────────────────────────
  # LINT & TEST
  # ─────────────────────────────────────────────
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "npm"

      - run: npm ci
      - run: npm run lint
      - run: npm run test -- --coverage

      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true

  # ─────────────────────────────────────────────
  # BUILD & PUSH DOCKER IMAGE
  # ─────────────────────────────────────────────
  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  # ─────────────────────────────────────────────
  # SECURITY SCANNING
  # ─────────────────────────────────────────────
  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: "sarif"
          output: "trivy-results.sarif"

      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: "trivy-results.sarif"

  # ─────────────────────────────────────────────
  # DEPLOY TO STAGING
  # ─────────────────────────────────────────────
  deploy-staging:
    needs: [build, security]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      # OIDC Authentication (no secrets stored!)
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster staging \
            --service app \
            --force-new-deployment

  # ─────────────────────────────────────────────
  # DEPLOY TO PRODUCTION
  # ─────────────────────────────────────────────
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsProd
          aws-region: us-east-1

      - name: Deploy to Production
        run: |
          aws ecs update-service \
            --cluster production \
            --service app \
            --force-new-deployment
```

### Matrix Builds

```yaml
jobs:
  test:
    strategy:
      fail-fast: false # Continue other jobs on failure
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18
        include:
          - os: ubuntu-latest
            node: 22
            coverage: true
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: "npm"
      - run: npm ci
      - run: npm test
      - if: matrix.coverage
        uses: codecov/codecov-action@v4
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      cluster:
        required: true
        type: string
    secrets:
      AWS_ROLE_ARN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy to ${{ inputs.environment }}
        run: |
          aws ecs update-service \
            --cluster ${{ inputs.cluster }} \
            --service app \
            --force-new-deployment

# Usage in caller workflow
jobs:
  deploy-prod:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
      cluster: prod-cluster
    secrets:
      AWS_ROLE_ARN: ${{ secrets.PROD_AWS_ROLE }}
```

### Composite Actions

```yaml
# .github/actions/setup-node-build/action.yml
name: "Setup Node and Build"
description: "Sets up Node.js, installs dependencies, and builds"

inputs:
  node-version:
    description: "Node.js version"
    required: false
    default: "22"

runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: "npm"

    - name: Install dependencies
      shell: bash
      run: npm ci

    - name: Build
      shell: bash
      run: npm run build

# Usage
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-node-build
        with:
          node-version: "22"
```

### OIDC Authentication (No Secrets!)

```yaml
# AWS OIDC
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/GitHubActions
    aws-region: us-east-1

# Azure OIDC
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

# GCP OIDC
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: "projects/123/locations/global/workloadIdentityPools/pool/providers/github"
    service_account: "github-actions@project.iam.gserviceaccount.com"
```

### Caching Strategies

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: "npm" # Built-in caching

# Custom cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Docker layer caching
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Gradle
- uses: actions/cache@v4
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*') }}
```

---

## 🦊 GitLab CI

### Complete Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  DOCKER_DRIVER: overlay2

# ─────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────
build:
  stage: build
  image: docker:26
  services:
    - docker:26-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Kaniko (Kubernetes-safe, no Docker-in-Docker)
build-kaniko:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:v1.21.0
    entrypoint: [""]
  script:
    - /kaniko/executor
      --context $CI_PROJECT_DIR
      --dockerfile $CI_PROJECT_DIR/Dockerfile
      --destination $DOCKER_IMAGE
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ─────────────────────────────────────────────
# TEST
# ─────────────────────────────────────────────
test:
  stage: test
  image: node:22-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci
  script:
    - npm run lint
    - npm test -- --coverage
  coverage: '/Coverage: (\d+\.\d+)%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura.xml
    expire_in: 1 week

# ─────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────
sast:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep --config=auto --sarif -o semgrep.sarif .
  artifacts:
    reports:
      sast: semgrep.sarif

container-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $DOCKER_IMAGE
  allow_failure: true

# ─────────────────────────────────────────────
# DEPLOY
# ─────────────────────────────────────────────
deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://app.example.com
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  needs:
    - deploy-staging
```

### Rules & Conditions

```yaml
# Conditional jobs
job:
  rules:
    # On merge requests
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

    # On default branch
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

    # When specific files change
    - changes:
        - src/**/*
        - package.json

    # Manual trigger
    - when: manual
      allow_failure: true

    # Scheduled pipelines
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

---

## 🔷 Azure DevOps

### Multi-Stage Pipeline

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - src/*
    exclude:
      - docs/*

pr:
  branches:
    include:
      - main

variables:
  - group: production-secrets
  - name: dockerImage
    value: "myregistry.azurecr.io/app"

stages:
  # ─────────────────────────────────────────────
  # BUILD
  # ─────────────────────────────────────────────
  - stage: Build
    displayName: "Build & Test"
    jobs:
      - job: BuildJob
        pool:
          vmImage: "ubuntu-latest"
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: "22.x"
            displayName: "Install Node.js"

          - task: Cache@2
            inputs:
              key: 'npm | "$(Agent.OS)" | package-lock.json'
              path: "node_modules"
            displayName: "Cache npm"

          - script: npm ci
            displayName: "Install dependencies"

          - script: npm run lint
            displayName: "Lint"

          - script: npm test -- --coverage
            displayName: "Test"

          - task: PublishTestResults@2
            inputs:
              testResultsFormat: "JUnit"
              testResultsFiles: "**/junit.xml"

          - task: PublishCodeCoverageResults@1
            inputs:
              codeCoverageTool: "Cobertura"
              summaryFileLocation: "coverage/cobertura.xml"

          - task: Docker@2
            inputs:
              containerRegistry: "azureContainerRegistry"
              repository: "app"
              command: "buildAndPush"
              Dockerfile: "Dockerfile"
              tags: |
                $(Build.BuildId)
                latest

  # ─────────────────────────────────────────────
  # DEPLOY STAGING
  # ─────────────────────────────────────────────
  - stage: DeployStaging
    displayName: "Deploy to Staging"
    dependsOn: Build
    condition: succeeded()
    jobs:
      - deployment: DeployStaging
        displayName: "Deploy Staging"
        pool:
          vmImage: "ubuntu-latest"
        environment: "staging"
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebAppContainer@1
                  inputs:
                    azureSubscription: "Azure Subscription"
                    appName: "app-staging"
                    imageName: "$(dockerImage):$(Build.BuildId)"

  # ─────────────────────────────────────────────
  # DEPLOY PRODUCTION
  # ─────────────────────────────────────────────
  - stage: DeployProduction
    displayName: "Deploy to Production"
    dependsOn: DeployStaging
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProduction
        displayName: "Deploy Production"
        pool:
          vmImage: "ubuntu-latest"
        environment: "production" # Requires approval
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebAppContainer@1
                  inputs:
                    azureSubscription: "Azure Subscription"
                    appName: "app-production"
                    imageName: "$(dockerImage):$(Build.BuildId)"
```

---

## 🔒 DevSecOps Patterns

### Security Scanning Pipeline

```yaml
# GitHub Actions security workflow
name: Security Scan

on:
  push:
    branches: [main]
  schedule:
    - cron: "0 0 * * *" # Daily

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      # Dependency scanning
      - uses: actions/checkout@v4
      - name: Run Dependabot
        uses: dependabot/fetch-metadata@v2

      # Secret scanning
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # SAST
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript, typescript
      - uses: github/codeql-action/analyze@v3

      # Container scanning
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: "fs"
          format: "sarif"
          output: "trivy.sarif"
          severity: "CRITICAL,HIGH"
```

---

## 🎯 Best Practices Checklist

### Pipeline Design

- [ ] Parallel jobs for independent tasks
- [ ] Cache dependencies (npm, pip, maven)
- [ ] Matrix builds for multi-platform
- [ ] Fail-fast disabled for comprehensive results
- [ ] Concurrency limits to prevent waste

### Security

- [ ] OIDC instead of long-lived secrets
- [ ] Secret scanning enabled
- [ ] Dependency scanning (Dependabot/Renovate)
- [ ] Container image scanning
- [ ] SAST integrated in pipeline
- [ ] Minimal GITHUB_TOKEN permissions

### Deployment

- [ ] Environment protection rules
- [ ] Required reviewers for production
- [ ] Deployment status checks
- [ ] Rollback strategy defined
- [ ] Blue/green or canary deployment

### Monitoring

- [ ] Pipeline duration tracking
- [ ] Test coverage reporting
- [ ] Deployment frequency metrics
- [ ] MTTR (Mean Time To Recovery) tracking

---

_DOMYH Awesome Code v6.0.0 • CI/CD Patterns • 2025-2026_
