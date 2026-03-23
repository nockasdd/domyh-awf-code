---
description: "🚀 Deploy to production with pre-checks, rollback plan, and post-verification"
skills:
  {
    required: [ci-cd],
    contextual: [docker, kubernetes, aws, terraform, gcp, azure],
  }
success_criteria: "Deployed, health checks pass, monitoring stable for 15min"
---

# 🚀 /deploy — Deploy Pro

> Zero-Downtime Deployments with Rollback Safety
> 📚 16 Platforms • Progressive Delivery • GitOps • Post-Deploy Monitoring

---

${RULES_DEPLOY}
## DEPLOYMENT FLOW

1. **PRE-FLIGHT** (Auto) — `hsa_session("deploy to {environment}")`, detect stack via HSA (`hsa_detect`), verify environment (`hsa_detect`), load deploy context (`hsa_search`). Run pre-flight checklist:
   - [ ] Tests pass (`npm test` / `go test ./...`)
   - [ ] Security scan (no P0 vulnerabilities)
   - [ ] Dependencies up to date (no critical outdated)
   - [ ] Environment variables configured
   - [ ] Database migrations pending? → Run first
   - [ ] Feature flags configured?
   - [ ] Rollback plan documented
   - [ ] Team notified? (Slack/Discord/Email)
         → ⛔ STOP if any critical check fails. Show: `[Pre-flight 6/8] ✅`
2. **BUILD** — Create production build, generate version tag, create artifacts
3. **DEPLOY** — Execute strategy (rolling/canary/blue-green/recreate), health checks at each stage. Show: `[Deploy] Canary 5% → monitoring...`
4. **VERIFY** — Smoke tests, health endpoints, error rate <0.1%, latency p99 <500ms, CPU <80%
5. **MONITOR** — Watch metrics for 15 minutes post-deploy:
   ```
   ⏱️ Monitoring window: 15min remaining...
   📊 Error rate: 0.02% ✅ | p99: 280ms ✅ | CPU: 45% ✅
   → Auto-rollback if: error_rate > 0.5% OR p99 > 1000ms OR CPU > 90%
   ```
6. **FINALIZE** — Tag release in git, update changelog, document rollback point, release deploy lock
7. **SYNC** — `hsa_check_changes` to update index after deployment config changes

---

## PRE-FLIGHT CHECKLIST

```yaml
pre_flight:
  required:
    - test_pass: "All tests must pass"
    - no_p0_vulns: "No P0 security vulnerabilities"
    - env_vars: "All required env vars set"
    - rollback_plan: "Rollback steps documented"
  recommended:
    - db_migrations: "Run pending migrations first"
    - feature_flags: "Toggle flags for new features"
    - team_notify: "Notify team in communication channel"
    - staging_tested: "Verified in staging environment"
    - changelog: "CHANGELOG.md updated"

  on_fail:
    required: "⛔ STOP — Cannot deploy"
    recommended: "⚠️ WARNING — Proceed with caution?"
```

---

## DEPLOY LOCK

```yaml
# Prevent concurrent deployments
deploy_lock:
  file: ".domyh/deploy.lock"
  content: |
    deployer: [user/agent]
    started: [ISO timestamp]
    environment: [production/staging]
    version: [tag]
  behavior:
    on_lock_exists: "⛔ STOP — Another deployment in progress"
    on_complete: "Remove lock file"
    on_timeout: "Auto-release after 30 minutes"
```

---

## PLATFORM REGISTRY

### Cloud / PaaS

```yaml
# platform: build | deploy | rollback | health
vercel: npm run build | vercel --prod | vercel rollback | automatic
netlify: npm run build | netlify deploy --prod | netlify rollback | deploy previews
cloudflare: npm run build | wrangler pages deploy | dashboard revert | automatic
gh_pages: npm run build | gh-pages -d dist | git revert + deploy | manual
railway: auto from git | railway up | dashboard | automatic
fly_io: fly deploy | fly deploy --strategy rolling | fly releases rollback | fly status
render: auto from git | push to branch | dashboard | health path
heroku: auto buildpacks | git push heroku main | heroku releases:rollback | metrics
```

### Containers / Cloud

```yaml
docker: docker build -t app . | docker-compose up -d | tag previous | HEALTHCHECK
kubernetes: docker build + apply | kubectl apply -f k8s/ | kubectl rollout undo | liveness/readiness
aws_ecs: docker build + ecr push | aws ecs update-service | --task-definition prev | ALB health
aws_lambda: sam build | sam deploy --guided | --s3-key previous.zip | CloudWatch
gcp_run: gcloud builds submit | gcloud run deploy | --to-revisions=REV=100 | container health
azure: az acr build | az webapp deployment | slot swap | health path
```

### VPS / Bare Metal

```yaml
vps_ssh: local/remote build | scp + ssh | keep prev release folder | curl health
pm2: npm run build | pm2 deploy production | pm2 deploy revert 1 | pm2 monit
systemd: build locally | scp + systemctl restart | keep prev binary | systemctl status
```

### Build Commands by Stack

```yaml
# Frontend: react/vue/svelte/angular → npm run build | nextjs → next build
# Backend: go build -o app -ldflags='-s -w' | cargo build --release | mvn package | dotnet publish -c Release
# Mobile: xcodebuild archive | ./gradlew assembleRelease | flutter build apk --release
```

---

## DEPLOYMENT STRATEGIES

| Strategy       | Rollback              | Risk            | Cost     | Use When                 |
| -------------- | --------------------- | --------------- | -------- | ------------------------ |
| **Blue-Green** | Instant (switch back) | Low             | 2x infra | Zero-downtime required   |
| **Canary**     | Route back to stable  | Very Low        | Minimal  | High-risk, metrics-based |
| **Rolling**    | Rollout undo          | Medium          | Minimal  | Standard K8s deploy      |
| **Recreate**   | Deploy prev version   | High (downtime) | Lowest   | Dev/staging only         |

### Canary Stages: 1% → 5% → 25% → 100% (10min/stage, auto-rollback on threshold breach)

---

## POST-DEPLOY MONITORING

```yaml
monitoring:
  duration: 15min # Watch window after deploy
  interval: 30s # Check frequency

  thresholds:
    error_rate: 0.5% # Auto-rollback if exceeded
    p99_latency: 1000ms # Auto-rollback if exceeded
    cpu_usage: 90% # Warning, manual decision
    memory: 85% # Warning, manual decision

  actions:
    breach_critical: "AUTO-ROLLBACK + notify team"
    breach_warning: "ALERT team, continue monitoring"
    all_clear: "✅ Deploy stable, proceed to finalize"
```

---

## HEALTH CHECKS

```yaml
checks:
  http: ["/health → 200", "/api/status → 200 {status:ok}", "/ → 200"]
  smoke:
    [
      Homepage loads,
      API returns data,
      Auth flow works,
      Critical path functional,
    ]
  metrics: [error_rate <0.1% (5m), p99_latency <500ms (5m), cpu <80%]
```

---

## SUB-COMMANDS

| Command                          | Description           |
| -------------------------------- | --------------------- |
| `/deploy`                        | Deploy to production  |
| `/deploy staging`                | Deploy to staging     |
| `/deploy --dry`                  | Dry run (preview)     |
| `/deploy --force`                | Skip pre-checks ⚠️    |
| `/deploy --canary`               | Force canary strategy |
| `/deploy gitops sync`            | GitOps sync           |
| `/deploy progressive [strategy]` | Progressive delivery  |
| `/deploy monitor`                | AI deployment monitor |
| `/deploy --checklist`            | Show pre-flight only  |
| `/deploy readiness`              | SRE readiness check   |
| `/deploy signoff`                | Stakeholder sign-off  |
| `/deploy validate-prompts`       | AI prompt validation  |
| `/deploy rollback`                 | Rollback to previous  |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

