---
description: "▶️ Start development server: detect stack, run dev commands, validate output"
skills: { required: [], contextual: [auto] }
success_criteria: "Dev server running, health check passes"
---

# ▶️ /dev — Dev Pro

> Intelligent Development Runner
> 📚 Auto-detect Stack • HMR 2025 • Error Recovery • Multi-service

---

## DEV FLOW

1. **DETECT** — `hsa_declare_intent("start dev server")`, identify stack via HSA (`hsa_detect_stack`), verify environment (`hsa_detect_environment`), find dev commands, check monorepo (nx.json, turbo.json, pnpm-workspace.yaml, package.json workspaces). Show: `[Step 1/6] Detecting stack...`
2. **DEPS CHECK** — Verify dependencies installed:
   - Node.js: `node_modules/` exists? → If not: auto-run `npm install` (or yarn/pnpm/bun)
   - Go: `go.sum` exists? → If not: `go mod download`
   - Python: `venv/` or `.venv/` exists? → If not: `python -m venv .venv && pip install -r requirements.txt`
   - Rust: Run `cargo check` to verify
     → Show: `[Step 2/6] Dependencies ✅` or `Installing dependencies...`
3. **SERVICES** — Check required services (DB, Redis, message queue):
   - Docker Compose found? → Offer `docker-compose up -d`
   - `.env` references DB_HOST? → Check if DB accessible
   - Redis required? → Check `redis-cli ping`
     → Show: `[Step 3/6] Services: PostgreSQL ✅ | Redis ✅`
4. **SETUP** — Set environment, check ports:
   - Load `.env` / `.env.local`
   - Check if default port available (3000, 8080, etc.)
   - If port in use: suggest next available or show what's using it
     → Show: `[Step 4/6] Port 3000 available ✅`
5. **START** — Run dev command, watch output:
   - On crash/error: show error + common fixes + offer auto-restart
   - On monorepo: offer parallel start for multiple packages
     → Show: `[Step 5/6] Starting server...`
6. **VALIDATE** — Confirm server running, show access URL:
   - Check health endpoint responds
   - Show URL for browser access
      → Show: `[Step 6/7] ✅ Server running at http://localhost:3000`
7. **SYNC** — `hsa_check_changes` to update index after dependency installs or config changes

---

## ERROR RECOVERY

```yaml
on_crash:
  1_show_error: "Display clear error message"
  2_common_fixes:
    port_in_use: "Kill process on port: npx kill-port 3000"
    missing_env: "Create .env from .env.example"
    missing_deps: "Run: npm install"
    db_not_running: "Start DB: docker-compose up -d db"
    permission: "Check file permissions"
  3_auto_restart: "Offer: Restart server? (y/n)"
  4_max_retries: 3 # Stop after 3 consecutive crashes

on_port_in_use:
  detect: "lsof -i :PORT (Unix) | netstat -ano | findstr PORT (Windows)"
  options:
    - "Kill existing process"
    - "Use next available port"
    - "Show what's using the port"
```

---

## COMMANDS

| Command           | Description           |
| ----------------- | --------------------- |
| `/dev`            | Start dev server      |
| `/dev stop`       | Stop server           |
| `/dev restart`    | Restart server        |
| `/dev logs`       | View logs             |
| `/dev port [num]` | Use specific port     |
| `/dev --all`      | Start all services    |
| `/dev --clean`    | Clean install + start |

---

## 🔧 DEV COMMANDS BY STACK

| Framework            | Dev Command                  | Alt                     |
| -------------------- | ---------------------------- | ----------------------- |
| **Next.js**          | `next dev`                   | `npm run dev`           |
| **Vite**             | `vite`                       | `npm run dev`           |
| **Remix**            | `remix dev`                  | `npm run dev`           |
| **Nuxt**             | `nuxt dev`                   | `npm run dev`           |
| **Angular**          | `ng serve`                   | `npm start`             |
| **Go (Air)**         | `air`                        | `go run .`              |
| **Go (Gin)**         | `go run main.go`             | `air`                   |
| **Python (Django)**  | `python manage.py runserver` | `./manage.py runserver` |
| **Python (FastAPI)** | `uvicorn main:app --reload`  | `fastapi dev`           |
| **Python (Flask)**   | `flask run --debug`          | `python app.py`         |
| **Rust (Cargo)**     | `cargo run`                  | `cargo watch -x run`    |
| **Java (Spring)**    | `./mvnw spring-boot:run`     | `./gradlew bootRun`     |
| **PHP (Laravel)**    | `php artisan serve`          | `valet`                 |
| **PHP (Symfony)**    | `symfony server:start`       | `php -S localhost:8000` |
| **Ruby (Rails)**     | `rails server`               | `bin/dev`               |

---

## 🐳 MULTI-SERVICE / MONOREPO

```yaml
monorepo_detection:
  nx: "nx.json → nx run-many --target=dev"
  turbo: "turbo.json → turbo dev"
  pnpm: "pnpm-workspace.yaml → pnpm -r dev"
  npm: "package.json workspaces → npm run dev --workspaces"
  lerna: "lerna.json → lerna run dev --parallel"

docker_compose:
  detected: "docker-compose.yml exists"
  action: "Offer: Start all services with docker-compose up -d?"
  selective: "Or start specific: docker-compose up -d db redis"
```

---

## ⚡ HMR 2025 STANDARDS

| Metric             | Target                     |
| ------------------ | -------------------------- |
| Module update      | < 100ms                    |
| Full reload        | < 1s                       |
| State preservation | React/Vue state maintained |
| Cold start         | < 3s                       |

### Modern Bundlers

| Tool      | Speed        | Use Case                 |
| --------- | ------------ | ------------------------ |
| Vite      | ⚡ Fast      | Default for new projects |
| Turbopack | ⚡⚡ Fastest | Next.js 15+              |
| Rspack    | ⚡⚡ Fast    | webpack migration        |
| esbuild   | ⚡⚡ Fastest | Build-only               |
---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** — Update session memory:
   - Append task summary to `memory/session.md` (per SESSION_005 format)
   - If key decision made → append to `memory/decisions.md`
3. **SNAPSHOT** — If this is the last task in session:
   - Update `memory/CONTEXT_SNAPSHOT.md` (Recent Changes, Status, Decisions)
4. **ANCHOR** (if HSA available):
   - `hsa_track_progress(level: "action", label: "[workflow] completed", status: "completed")`
   - `hsa_save_anchor(content: "[SESSION] Done: [summary]. Files: [list].", category: "context")`

