---
name: deploy
trigger: ["/deploy", "release", "production", "ship"]
persona: devops
description: "🚀 Deploy to production with pre-checks, rollback plan, and post-verification"
---

# 🚀 /deploy — Production Deployment Pro v3.0

> Zero-Downtime Deployments with Rollback Safety
> 📚 15+ Platforms • Health Checks • Progressive Delivery

---

## 🔄 DEPLOYMENT FLOW

```
User: /deploy [env]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: PRE-FLIGHT (Auto)             │
│ ▸ Detect stack & platform               │
│ ▸ Run pre-deploy checks                 │
│ ⛔ STOP if checks fail                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: BUILD                          │
│ ▸ Create production build               │
│ ▸ Generate release version              │
│ ▸ Create deployment artifacts           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: DEPLOY                         │
│ ▸ Execute deployment strategy           │
│ ▸ Progressive rollout (if canary)       │
│ ▸ Health checks at each stage           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: VERIFY                         │
│ ▸ Smoke tests                           │
│ ▸ Health endpoint checks                │
│ ▸ Monitor error rates                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: FINALIZE                       │
│ ▸ Tag release in Git                    │
│ ▸ Update changelog                      │
│ ▸ Notify team                           │
│ ▸ Document rollback point               │
└─────────────────────────────────────────┘
```

---

## 📋 PHASE 1: PRE-FLIGHT CHECKS

### Automated Pre-Deploy Checklist:

```
🛫 PRE-FLIGHT CHECKS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests:
├── Unit tests: ✅ 156/156 passed
├── Integration: ✅ 23/23 passed
└── E2E: ✅ 12/12 passed

Security:
├── Vulnerability scan: ✅ No critical
├── Secrets audit: ✅ No exposed secrets
└── Dependencies: ✅ No known CVEs

Quality:
├── Code review: ✅ Approved
├── Coverage: ✅ 85% (>80% threshold)
└── Linting: ✅ No errors

Config:
├── Env vars: ✅ All required present
├── Rollback plan: ✅ Documented
└── On-call: ✅ Assigned

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ✅ READY TO DEPLOY
```

### ⛔ STOP Conditions:

```yaml
stop_if:
  - Tests failing
  - P0/P1 open issues
  - No rollback plan
  - Missing required env vars
  - Unapproved changes
  - Outside deployment window
```

---

## 🌐 PLATFORM REGISTRY (15+ Platforms)

### Cloud / PaaS

```yaml
# ═══════════════════════════════════════════════════════════════
# FRONTEND / STATIC / JAMSTACK
# ═══════════════════════════════════════════════════════════════

vercel:
  build: "npm run build"
  deploy: "vercel --prod"
  rollback: "vercel rollback"
  preview: "vercel"
  env: "vercel env pull"
  health: "/_health, automatic"

netlify:
  build: "npm run build"
  deploy: "netlify deploy --prod"
  rollback: "netlify rollback"
  preview: "netlify deploy"
  env: "netlify env:import .env"
  health: "Deploy previews"

cloudflare_pages:
  build: "npm run build"
  deploy: "wrangler pages deploy"
  rollback: "Revert via dashboard"
  preview: "Branch deploys"
  env: "wrangler pages secret"
  health: "Automatic health"

github_pages:
  build: "npm run build"
  deploy: "gh-pages -d dist"
  rollback: "git revert && deploy"
  preview: "Branch deploys"
  env: "Repository secrets"
  health: "Manual check"

# ═══════════════════════════════════════════════════════════════
# BACKEND / CONTAINERS
# ═══════════════════════════════════════════════════════════════

docker:
  build: "docker build -t app:latest ."
  deploy: "docker-compose up -d"
  rollback: "docker-compose down && docker-compose up -d --build app:previous"
  health: "HEALTHCHECK instruction"
  registry: "docker push registry/app:tag"

kubernetes:
  build: "docker build && kubectl apply"
  deploy: "kubectl apply -f k8s/"
  rollback: "kubectl rollout undo deployment/app"
  health: "livenessProbe, readinessProbe"
  strategy: "RollingUpdate, Blue-Green, Canary"

aws_ecs:
  build: "docker build && ecr push"
  deploy: "aws ecs update-service"
  rollback: "aws ecs update-service --task-definition previous"
  health: "ALB health checks"
  strategy: "Rolling, Blue-Green"

aws_lambda:
  build: "sam build"
  deploy: "sam deploy --guided"
  rollback: "aws lambda update-function-code --s3-key previous.zip"
  health: "CloudWatch Alarms"
  alias: "Lambda versions + aliases"

gcp_cloud_run:
  build: "gcloud builds submit"
  deploy: "gcloud run deploy"
  rollback: "gcloud run services update-traffic --to-revisions=REV=100"
  health: "Container health checks"
  strategy: "Traffic splitting"

azure_app_service:
  build: "az acr build"
  deploy: "az webapp deployment"
  rollback: "az webapp deployment slot swap"
  health: "Health check path"
  strategy: "Deployment slots"

# ═══════════════════════════════════════════════════════════════
# VPS / BARE METAL
# ═══════════════════════════════════════════════════════════════

vps_ssh:
  build: "Local build or remote"
  deploy: "scp + ssh commands"
  rollback: "Keep previous release folder"
  health: "curl healthcheck"
  strategy: "Symlink swap"

pm2:
  build: "npm run build"
  deploy: "pm2 deploy production"
  rollback: "pm2 deploy production revert 1"
  health: "pm2 monit"
  strategy: "Zero-downtime reload"

systemd:
  build: "Build locally"
  deploy: "scp && systemctl restart"
  rollback: "Keep previous binary"
  health: "systemctl status"
  strategy: "Service reload"

# ═══════════════════════════════════════════════════════════════
# SPECIALIZED
# ═══════════════════════════════════════════════════════════════

railway:
  build: "Automatic from Git"
  deploy: "railway up"
  rollback: "Railway dashboard"
  health: "Automatic"
  env: "railway variables"

fly_io:
  build: "fly deploy"
  deploy: "fly deploy --strategy rolling"
  rollback: "fly releases rollback"
  health: "fly status"
  strategy: "Rolling, Blue-Green"

render:
  build: "Automatic from Git"
  deploy: "Push to branch"
  rollback: "Render dashboard"
  health: "Health check path"
  env: "render.yaml"

heroku:
  build: "Automatic buildpacks"
  deploy: "git push heroku main"
  rollback: "heroku releases:rollback"
  health: "Heroku metrics"
  env: "heroku config:set"
```

### Language-Specific Build Commands:

```yaml
builds:
  # Frontend
  react: "npm run build"
  nextjs: "next build"
  vue: "npm run build"
  svelte: "npm run build"
  angular: "ng build --prod"

  # Backend
  go: "go build -o app -ldflags='-s -w'"
  rust: "cargo build --release"
  java: "mvn package -DskipTests"
  kotlin: "gradle build"
  csharp: "dotnet publish -c Release"
  python: "pip install -r requirements.txt"
  ruby: "bundle install --deployment"
  php: "composer install --no-dev"

  # Mobile
  ios: "xcodebuild -scheme App archive"
  android: "./gradlew assembleRelease"
  flutter: "flutter build apk --release"
  react_native: "npx react-native build-android --mode=release"
```

---

## 📋 PHASE 2: BUILD

### Build Output:

```
🔨 BUILD STARTED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack: Next.js + TypeScript
Platform: Vercel
Version: v2.5.0 (auto-generated)
Commit: abc1234 "feat: add user dashboard"

Building...
├── [1/4] Installing dependencies... ✅ 45s
├── [2/4] Compiling TypeScript... ✅ 30s
├── [3/4] Building production... ✅ 60s
└── [4/4] Optimizing assets... ✅ 15s

Output:
├── Bundle size: 245KB (gzipped)
├── Static pages: 12
├── Dynamic routes: 5
└── API routes: 8

Build time: 2m 30s
Status: ✅ BUILD SUCCESS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 3: DEPLOY

### Deployment Strategies:

```yaml
strategies:
  # ═══════════════════════════════════════
  # BLUE-GREEN (Zero Downtime)
  # ═══════════════════════════════════════
  blue_green:
    description: "Two identical environments, instant switch"
    rollback: "Instant (switch back)"
    risk: "Low"
    cost: "2x infrastructure"
    steps:
      - Deploy to inactive environment (green)
      - Run health checks on green
      - Switch load balancer to green
      - Keep blue as rollback target
    use_when:
      - Zero-downtime required
      - Quick rollback needed
      - Sufficient infrastructure budget

  # ═══════════════════════════════════════
  # CANARY (Progressive)
  # ═══════════════════════════════════════
  canary:
    description: "Gradual traffic shift, monitor metrics"
    rollback: "Route all traffic back to stable"
    risk: "Very Low"
    cost: "Minimal overhead"
    steps:
      - Deploy new version alongside old
      - Route 5% traffic to new version
      - Monitor errors, latency, metrics
      - Gradually increase (25% → 50% → 100%)
      - Remove old version when stable
    use_when:
      - High-risk changes
      - Need real-user validation
      - Metrics-based confidence

  # ═══════════════════════════════════════
  # ROLLING (Gradual Replace)
  # ═══════════════════════════════════════
  rolling:
    description: "Replace instances one by one"
    rollback: "Rollout undo"
    risk: "Medium"
    cost: "Minimal"
    steps:
      - Replace 1 instance with new version
      - Health check new instance
      - Continue until all replaced
    use_when:
      - Standard deployments
      - Kubernetes default
      - Multiple replicas

  # ═══════════════════════════════════════
  # RECREATE (Simple)
  # ═══════════════════════════════════════
  recreate:
    description: "Stop old, start new (has downtime)"
    rollback: "Deploy previous version"
    risk: "High"
    cost: "Lowest"
    steps:
      - Stop all old instances
      - Deploy new version
      - Start new instances
    use_when:
      - Dev/staging environments
      - Downtime acceptable
      - Simple applications
```

### Deployment Progress:

```
🚀 DEPLOYING

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Strategy: Canary (Progressive)
Target: Production
Version: v2.5.0

Progress:
├── [1/5] Deploying to canary... ✅
├── [2/5] Health check (5% traffic)... ✅
│   └── Error rate: 0.01% ✅ (<0.1% threshold)
├── [3/5] Scaling to 25%... ✅
│   └── Latency p99: 120ms ✅ (<200ms threshold)
├── [4/5] Scaling to 100%... ⏳ In progress
└── [5/5] Cleanup old version... ⏳ Pending

Current traffic split:
├── v2.5.0 (new): 50%
└── v2.4.0 (old): 50%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 4: VERIFY

### Health Checks:

```yaml
health_checks:
  # HTTP endpoint checks
  http:
    - endpoint: "/health"
      expect_status: 200
      timeout: 5s

    - endpoint: "/api/status"
      expect_status: 200
      expect_body: '{"status":"ok"}'

    - endpoint: "/"
      expect_status: 200

  # Smoke tests
  smoke_tests:
    - "Homepage loads"
    - "API returns data"
    - "Auth flow works"
    - "Critical path functional"

  # Metrics thresholds
  metrics:
    - metric: "error_rate"
      threshold: "<0.1%"
      window: "5m"

    - metric: "p99_latency"
      threshold: "<500ms"
      window: "5m"

    - metric: "cpu_usage"
      threshold: "<80%"
```

### Verification Output:

```
✅ VERIFICATION COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Health Checks:
├── /health: ✅ 200 OK (45ms)
├── /api/status: ✅ 200 OK (120ms)
└── /: ✅ 200 OK (230ms)

Smoke Tests:
├── Homepage loads: ✅ Pass
├── API returns data: ✅ Pass
├── Auth flow works: ✅ Pass
└── Critical path: ✅ Pass

Metrics (5min window):
├── Error rate: 0.02% ✅ (<0.1%)
├── p99 latency: 180ms ✅ (<500ms)
├── CPU usage: 35% ✅ (<80%)
└── Memory: 65% ✅ (<90%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ✅ DEPLOYMENT VERIFIED
```

---

## 📋 PHASE 5: FINALIZE

### Release Documentation:

```
🎉 DEPLOYMENT SUCCESSFUL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Release: v2.5.0
Environment: Production
URL: https://app.example.com
Time: 2026-01-31 18:15:00 UTC
Duration: 4m 30s

Git:
├── Commit: abc1234
├── Tag: v2.5.0 ✅ Created
└── Branch: main

Changelog:
├── ✨ feat: add user dashboard
├── 🐛 fix: login timeout issue
└── 📝 docs: update API docs

Rollback:
├── Command: vercel rollback
├── Previous: v2.4.0
└── Rollback time: ~30s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Monitor metrics (next 15min)
2️⃣ Announce in #releases
3️⃣ If issues: /rollback

Enter number:
```

---

## ⏪ ROLLBACK

### Rollback Commands by Platform:

```yaml
rollback_commands:
  vercel: "vercel rollback"
  netlify: "netlify rollback"
  kubernetes: "kubectl rollout undo deployment/app"
  docker: "docker-compose up -d app:previous"
  heroku: "heroku releases:rollback"
  aws_ecs: "aws ecs update-service --task-definition previous"
  fly_io: "fly releases rollback"
  pm2: "pm2 deploy production revert 1"
```

### Rollback Flow:

```
⏪ ROLLBACK INITIATED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current: v2.5.0 (problematic)
Target: v2.4.0 (last stable)
Reason: [User specified or auto-detected]

Progress:
├── [1/3] Switching traffic... ✅
├── [2/3] Health check... ✅
└── [3/3] Cleanup... ✅

Status: ✅ ROLLBACK COMPLETE
Active version: v2.4.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 SUB-COMMANDS

| Command            | Description                 |
| ------------------ | --------------------------- |
| `/deploy`          | Deploy to production        |
| `/deploy staging`  | Deploy to staging           |
| `/deploy --dry`    | Dry run (preview only)      |
| `/deploy --force`  | Skip pre-checks (dangerous) |
| `/deploy --canary` | Force canary strategy       |
| `/rollback`        | Rollback to previous        |

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Be efficient with checks
  - Run automated checks, show summary only
  - Skip verbose build logs unless error
  - Show only changed metrics

  # Focus on what matters
  - Highlight failures, summarize successes
  - Use progressive disclosure
  - Provide rollback command upfront
```

---

## 📜 RULES APPLIED

| Phase      | Rules                         |
| ---------- | ----------------------------- |
| Pre-flight | `safety`, `stop-conditions`   |
| Build      | `terminal-safety`             |
| Deploy     | `safety`, `edit-verification` |
| Verify     | `evidence`, `terminal-safety` |
| Finalize   | `safety` (no secrets in logs) |

---

## 🔄 GITOPS INTEGRATION (v3.1)

```yaml
gitops_standard:
  description: "Git as single source of truth"

  principles:
    declarative: "Desired state in Git"
    versioned: "Full audit trail"
    automated: "Reconciliation loop"
    immutable: "No manual changes"

  tools:
    kubernetes:
      - "ArgoCD"
      - "Flux"
      - "Rancher Fleet"
    serverless:
      - "Serverless Framework"
      - "SST"
      - "Pulumi"
    containers:
      - "Docker Compose"
      - "Helm"

  workflow:
    1: "Push to Git"
    2: "CI builds and tests"
    3: "Create deployment manifest"
    4: "GitOps controller detects change"
    5: "Apply to cluster"
    6: "Verify health"

  commands:
    sync: "/deploy gitops sync"
    diff: "/deploy gitops diff"
    history: "/deploy gitops history"
```

---

## 🎯 PROGRESSIVE DELIVERY (v3.1)

```yaml
progressive_delivery:
  description: "Gradual rollout with automatic rollback"

  strategies:
    canary:
      stages: [1%, 5%, 25%, 100%]
      validation: "Metrics + latency check"
      auto_rollback: "On threshold breach"
      duration: "10min per stage"

    blue_green:
      cutover: "DNS or load balancer switch"
      rollback: "Instant to blue"
      validation: "Health check before switch"

    feature_flags:
      providers:
        - "LaunchDarkly"
        - "Split"
        - "Unleash"
        - "PostHog"
      gradual_rollout: true
      user_targeting: true

  ai_monitor:
    capabilities:
      health_check: "Real-time metrics"
      anomaly_detection: "Compare to baseline"
      predictive_alert: "Before impact"
      auto_rollback: "With confidence > 90%"

    metrics:
      - "Error rate"
      - "Latency p50/p99"
      - "CPU/Memory"
      - "Request count"

  commands:
    progressive: "/deploy progressive [strategy]"
    canary: "/deploy canary [percentage]"
    promote: "/deploy promote"
    monitor: "/deploy monitor [status|rollback]"
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command                          | Description            |
| -------------------------------- | ---------------------- |
| `/deploy`                        | Deploy to production   |
| `/deploy staging`                | Deploy to staging      |
| `/deploy gitops sync`            | GitOps sync            |
| `/deploy gitops diff`            | Show pending changes   |
| `/deploy progressive [strategy]` | Progressive delivery   |
| `/deploy canary [%]`             | Canary deployment      |
| `/deploy monitor`                | AI deployment monitor  |
| `/deploy --dry`                  | Dry run (preview only) |
| `/rollback`                      | Rollback to previous   |

---

_DOMYH Awesome Code v4.3 • Deploy Pro v3.1 • GitOps + Progressive Delivery_
