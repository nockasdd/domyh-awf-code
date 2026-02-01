# CI/CD — Advanced Patterns

# DOMYH Awesome Code v4.3 — Tier 3 Reference

## Table of Contents

- [GitOps with ArgoCD](#gitops-with-argocd)
- [Progressive Delivery](#progressive-delivery)
- [Multi-Environment Strategies](#multi-environment-strategies)
- [Advanced GitHub Actions](#advanced-github-actions)
- [Advanced GitLab CI](#advanced-gitlab-ci)
- [Security Deep Dive](#security-deep-dive)
- [Performance Optimization](#performance-optimization)

---

## GitOps with ArgoCD

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/infra.git
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Sync Waves (Ordered Deployment)

```yaml
# 1. Secrets first
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  annotations:
    argocd.argoproj.io/sync-wave: "-1"

---
# 2. ConfigMaps
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"

---
# 3. Deployment last
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

---

## Progressive Delivery

### Blue-Green with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app
spec:
  replicas: 5
  strategy:
    blueGreen:
      activeService: app-active
      previewService: app-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
      prePromotionAnalysis:
        templates:
          - templateName: success-rate
        args:
          - name: service-name
            value: app-preview
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m])) /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

### Canary with Flagger

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  progressDeadlineSeconds: 600
  service:
    port: 80
    targetPort: 8080
    gateways:
      - public-gateway.istio-system.svc.cluster.local
    hosts:
      - app.example.com
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
    webhooks:
      - name: load-test
        url: http://flagger-loadtester/
        timeout: 5s
        metadata:
          cmd: "hey -z 1m -q 10 -c 2 http://app-canary.production/"
```

---

## Multi-Environment Strategies

### Kustomize Overlays

```
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── development/
│   │   ├── kustomization.yaml
│   │   └── replica-patch.yaml
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── replica-patch.yaml
│   └── production/
│       ├── kustomization.yaml
│       ├── replica-patch.yaml
│       └── resource-patch.yaml
```

```yaml
# k8s/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - ../../base

patchesStrategicMerge:
  - replica-patch.yaml
  - resource-patch.yaml

configMapGenerator:
  - name: app-config
    envs:
      - .env.production

images:
  - name: app
    newName: ghcr.io/org/app
    newTag: v1.2.3
```

---

## Advanced GitHub Actions

### Dynamic Matrix Generation

```yaml
jobs:
  generate-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set-matrix
        run: |
          # Generate matrix from changed directories
          DIRS=$(find packages -mindepth 1 -maxdepth 1 -type d | jq -R -s -c 'split("\n")[:-1]')
          echo "matrix={\"package\":$DIRS}" >> $GITHUB_OUTPUT

  build:
    needs: generate-matrix
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      - run: cd ${{ matrix.package }} && npm ci && npm run build
```

### Workflow Dispatch with Inputs

```yaml
name: Manual Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options:
          - staging
          - production
      version:
        description: "Version to deploy"
        required: true
        type: string
      dry-run:
        description: "Dry run mode"
        required: false
        type: boolean
        default: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy ${{ inputs.version }} to ${{ inputs.environment }}
        run: |
          if [ "${{ inputs.dry-run }}" == "true" ]; then
            echo "DRY RUN: Would deploy ${{ inputs.version }}"
          else
            ./deploy.sh ${{ inputs.version }}
          fi
```

### Path-based Triggers

```yaml
on:
  push:
    branches: [main]
    paths:
      - "packages/api/**"
      - "!packages/api/**/*.md"
      - "!packages/api/**/*.test.ts"
  pull_request:
    branches: [main]
    paths:
      - "packages/api/**"

jobs:
  build-api:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: packages/api
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
```

---

## Advanced GitLab CI

### Parent-Child Pipelines

```yaml
# .gitlab-ci.yml (parent)
stages:
  - generate
  - trigger

generate-config:
  stage: generate
  script:
    - ./scripts/generate-pipeline.sh > child-pipeline.yml
  artifacts:
    paths:
      - child-pipeline.yml

trigger-child:
  stage: trigger
  trigger:
    include:
      - artifact: child-pipeline.yml
        job: generate-config
    strategy: depend
```

### DAG (Directed Acyclic Graph)

```yaml
stages:
  - build
  - test
  - deploy

build-frontend:
  stage: build
  script: cd frontend && npm run build

build-backend:
  stage: build
  script: cd backend && go build

test-frontend:
  stage: test
  needs: [build-frontend]
  script: cd frontend && npm test

test-backend:
  stage: test
  needs: [build-backend]
  script: cd backend && go test

deploy:
  stage: deploy
  needs:
    - job: test-frontend
    - job: test-backend
  script: ./deploy.sh
```

---

## Security Deep Dive

### Supply Chain Security

```yaml
# GitHub Actions with artifact attestation
name: Build with SLSA Provenance

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      attestations: write
    steps:
      - uses: actions/checkout@v4

      - name: Build artifact
        run: |
          npm ci
          npm run build
          tar -czf artifact.tar.gz dist/

      - name: Generate attestation
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: artifact.tar.gz
```

### Container Signing with Cosign

```yaml
- name: Install Cosign
  uses: sigstore/cosign-installer@v3

- name: Sign container image
  env:
    COSIGN_EXPERIMENTAL: "true"
  run: |
    cosign sign --yes ghcr.io/org/app:${{ github.sha }}

- name: Verify signature
  run: |
    cosign verify ghcr.io/org/app:${{ github.sha }} \
      --certificate-identity-regexp='https://github.com/org/*' \
      --certificate-oidc-issuer='https://token.actions.githubusercontent.com'
```

### SBOM Generation

```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    path: .
    format: spdx-json
    output-file: sbom.spdx.json

- name: Upload SBOM
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: sbom.spdx.json

- name: Scan SBOM for vulnerabilities
  uses: anchore/scan-action@v4
  with:
    sbom: sbom.spdx.json
    fail-build: true
    severity-cutoff: high
```

---

## Performance Optimization

### Parallel Test Sharding

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "npm"
      - run: npm ci
      - run: npm test -- --shard=${{ matrix.shard }}/${{ strategy.job-total }}
```

### Self-hosted Runner Optimization

```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, arm64, high-memory]
    steps:
      - uses: actions/checkout@v4
      - name: Build with local cache
        run: |
          export CCACHE_DIR=${{ runner.temp }}/ccache
          cmake --build . --parallel $(nproc)
```

### Docker Build Optimization

```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ghcr.io/org/app:${{ github.sha }}
    cache-from: |
      type=gha
      type=registry,ref=ghcr.io/org/app:buildcache
    cache-to: |
      type=gha,mode=max
      type=registry,ref=ghcr.io/org/app:buildcache,mode=max
    platforms: linux/amd64,linux/arm64
    build-args: |
      BUILDKIT_INLINE_CACHE=1
```

---

## Metrics & Observability

### DORA Metrics Collection

```yaml
# Deploy tracking
- name: Record deployment
  run: |
    curl -X POST "${{ secrets.METRICS_ENDPOINT }}/deployments" \
      -H "Content-Type: application/json" \
      -d '{
        "commit_sha": "${{ github.sha }}",
        "environment": "production",
        "deployed_at": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
        "lead_time_seconds": "${{ steps.lead-time.outputs.seconds }}"
      }'
```

---

_DOMYH Awesome Code v4.3 — CI/CD Advanced Patterns_
