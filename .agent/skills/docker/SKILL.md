---
name: docker
detect:
  ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore"]
version: "6.0.0"
category: devops
tier: 1
---

# Docker Patterns — DOMYH Awesome Code v5.5

> Docker Engine 28+ & Docker Compose v2 — 2025-2026

## 🔍 Docker Detection

```yaml
docker_indicators:
  - "Dockerfile, .dockerignore"
  - "docker-compose.yml, docker-compose.yaml"
  - "FROM, RUN, COPY, CMD, ENTRYPOINT"
  - "services:, volumes:, networks:"
  - "docker build, docker run"
  - "HEALTHCHECK, EXPOSE, WORKDIR"

container_runtime:
  - Docker Engine 28+
  - Docker Desktop 4.47+
  - Podman (alternative)
  - nerdctl (K8s-native)
```

---

## 📊 Docker Ecosystem (2025-2026)

### Key Tools

| Tool                  | Purpose              | Use Case                |
| --------------------- | -------------------- | ----------------------- |
| **Docker Engine 28**  | Container runtime    | Core containerization   |
| **Docker Compose v2** | Multi-container apps | Local dev, testing      |
| **BuildKit**          | Advanced builds      | Multi-stage, caching    |
| **Docker Scout**      | Security scanning    | Vulnerability detection |
| **Docker Buildx**     | Multi-arch builds    | ARM64, x86_64           |
| **Containerd**        | Container runtime    | K8s integration         |

### Base Image Selection

| Image Type     | Size  | Use Case           | Example                   |
| -------------- | ----- | ------------------ | ------------------------- |
| **Alpine**     | ~5MB  | Minimal apps       | `node:22-alpine`          |
| **Slim**       | ~50MB | Most apps          | `python:3.12-slim`        |
| **Distroless** | ~20MB | Security-critical  | `gcr.io/distroless/base`  |
| **Scratch**    | 0B    | Static binaries    | Go, Rust                  |
| **Chainguard** | ~10MB | Security + updates | `cgr.dev/chainguard/node` |

---

## 📦 Dockerfile Best Practices

### Multi-Stage Build (Node.js)

```dockerfile
# syntax=docker/dockerfile:1
# ✅ Always use latest syntax for BuildKit features

# ═══════════════════════════════════════════════════════════
# STAGE 1: Dependencies
# ═══════════════════════════════════════════════════════════
FROM node:22-alpine AS deps
WORKDIR /app

# Copy only package files (cache optimization)
COPY package.json package-lock.json ./

# ✅ BuildKit cache mount for faster builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci --frozen-lockfile

# ═══════════════════════════════════════════════════════════
# STAGE 2: Build
# ═══════════════════════════════════════════════════════════
FROM node:22-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
RUN npm run build

# ═══════════════════════════════════════════════════════════
# STAGE 3: Production
# ═══════════════════════════════════════════════════════════
FROM node:22-alpine AS runner
WORKDIR /app

# ✅ Set production environment
ENV NODE_ENV=production

# ✅ Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

# ✅ Copy only production files
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/package.json ./

# ✅ Switch to non-root user
USER appuser

# ✅ Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Multi-Stage Build (Go)

```dockerfile
# syntax=docker/dockerfile:1

# ═══════════════════════════════════════════════════════════
# STAGE 1: Build
# ═══════════════════════════════════════════════════════════
FROM golang:1.24-alpine AS builder
WORKDIR /app

# ✅ Copy go.mod first for cache
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# ✅ Build static binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /server ./cmd/server

# ═══════════════════════════════════════════════════════════
# STAGE 2: Production (Scratch = minimal)
# ═══════════════════════════════════════════════════════════
FROM scratch

# ✅ Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# ✅ Copy binary
COPY --from=builder /server /server

# ✅ Run as non-root (UID 65534 = nobody)
USER 65534:65534

EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Multi-Stage Build (Python)

```dockerfile
# syntax=docker/dockerfile:1

# ═══════════════════════════════════════════════════════════
# STAGE 1: Build dependencies
# ═══════════════════════════════════════════════════════════
FROM python:3.12-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# ═══════════════════════════════════════════════════════════
# STAGE 2: Production
# ═══════════════════════════════════════════════════════════
FROM python:3.12-slim AS runner
WORKDIR /app

# ✅ Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ✅ Non-root user
RUN useradd --system --uid 1001 appuser
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔐 Security Best Practices

### Critical Rules

| Rule                     | Implementation                          |
| ------------------------ | --------------------------------------- |
| **Non-root user**        | `USER appuser` at end                   |
| **Pin versions**         | `FROM node:22.0.0-alpine` not `:latest` |
| **Minimal base**         | Alpine, Distroless, Scratch             |
| **No secrets in image**  | Use `--mount=type=secret`               |
| **Read-only filesystem** | `read_only: true` in Compose            |
| **Drop capabilities**    | `cap_drop: [ALL]`                       |
| **Scan vulnerabilities** | Docker Scout, Trivy, Grype              |

### Secrets Management (BuildKit)

```dockerfile
# ✅ Build with secrets (NOT stored in image)
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci

# Build command:
# docker build --secret id=npm_token,src=.npmrc .
```

### SSH for Private Repos

```dockerfile
# ✅ Use SSH agent forwarding
RUN --mount=type=ssh \
    git clone git@github.com:org/private-repo.git

# Build command:
# docker build --ssh default .
```

### Security Scanning

```bash
# Docker Scout (built-in)
docker scout cves myimage:latest

# Trivy
trivy image myimage:latest

# Grype
grype myimage:latest
```

---

## 🚀 Docker Compose v2 (2025)

### Modern Compose File

> **Note**: `version:` field is obsolete in Docker Compose v2

```yaml
# ✅ No version field needed (Compose v2+)
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    image: myapp:${VERSION:-latest}
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://postgres:secret@db:5432/app
      REDIS_URL: redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    # ✅ Security hardening
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    # ✅ Resource limits
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    networks:
      - frontend
      - backend
    restart: unless-stopped

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redisdata:/data
    networks:
      - backend
    restart: unless-stopped

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true # ✅ No external access

volumes:
  pgdata:
  redisdata:
```

### Production Compose with Deploy

```yaml
services:
  app:
    image: myapp:${VERSION:-latest}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        order: start-first
      rollback_config:
        parallelism: 0
        order: stop-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

### Compose Profiles

```yaml
services:
  app:
    build: .
    profiles: ["dev", "prod"]

  db:
    image: postgres:17-alpine
    profiles: ["dev", "prod"]

  # Only in development
  db-admin:
    image: dpage/pgadmin4
    profiles: ["dev"]
    ports:
      - "5050:80"

  # Only in testing
  test-runner:
    build:
      context: .
      target: test
    profiles: ["test"]
    command: npm test
```

```bash
# Run specific profile
docker compose --profile dev up
docker compose --profile test run test-runner
```

---

## 📁 .dockerignore

```dockerfile
# Version Control
.git
.gitignore
.gitattributes

# Dependencies (rebuild in container)
node_modules
.pnpm-store
vendor

# Build artifacts
dist
build
*.log

# Development files
.env
.env.local
.env.*.local
*.md
LICENSE

# IDE
.vscode
.idea
*.swp

# Testing
coverage
.nyc_output
*.test.js
*.spec.js

# Docker
Dockerfile*
docker-compose*
.dockerignore

# OS files
.DS_Store
Thumbs.db
```

---

## ⚡ BuildKit Features

### Cache Mounts

```dockerfile
# ✅ npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# ✅ apt cache
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y build-essential

# ✅ pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# ✅ Go modules cache
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

### Bind Mounts (Build Context)

```dockerfile
# ✅ Bind source files without COPY layer
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    npm ci
```

---

## 📋 Common Commands

### Build

```bash
# Basic build
docker build -t myapp:latest .

# Build with BuildKit (recommended)
DOCKER_BUILDKIT=1 docker build -t myapp:latest .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .

# Build with specific target stage
docker build --target builder -t myapp:builder .

# Build with build args
docker build --build-arg VERSION=1.0.0 -t myapp:1.0.0 .

# Pull latest base image
docker build --pull -t myapp:latest .

# No cache (clean build)
docker build --no-cache -t myapp:latest .
```

### Run & Debug

```bash
# Run container
docker run -d -p 3000:3000 --name myapp myapp:latest

# Run with environment file
docker run -d --env-file .env myapp:latest

# Interactive shell
docker run -it --rm myapp:latest /bin/sh

# Execute command in running container
docker exec -it myapp /bin/sh

# View logs
docker logs -f myapp

# Inspect container
docker inspect myapp
```

### Compose

```bash
# Start services
docker compose up -d

# Rebuild and start
docker compose up -d --build

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f app

# Scale service
docker compose up -d --scale app=3

# Run one-off command
docker compose run --rm app npm test
```

---

## ✅ Production Checklist

### Dockerfile

- [ ] Multi-stage build
- [ ] Pin base image versions (no :latest)
- [ ] Non-root user
- [ ] HEALTHCHECK defined
- [ ] .dockerignore exists
- [ ] No secrets in image

### Security

- [ ] Vulnerability scan passed
- [ ] Read-only filesystem (where possible)
- [ ] Capabilities dropped
- [ ] Resource limits set
- [ ] No-new-privileges enabled

### Compose

- [ ] Health checks for all services
- [ ] depends_on with conditions
- [ ] Restart policies defined
- [ ] Resource limits configured
- [ ] Logging configured
- [ ] Networks isolated

---

_DOMYH Awesome Code v6.0.0 • Docker Patterns • 2025-2026_
