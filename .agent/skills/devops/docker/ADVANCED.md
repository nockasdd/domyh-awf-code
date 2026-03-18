# Docker — Advanced Patterns

## Table of Contents

- [Multi-Stage Builds](#multi-stage-builds)
- [Security Hardening](#security-hardening)
- [Compose Patterns](#compose-patterns)
- [Networking](#networking)
- [Debugging & Troubleshooting](#debugging--troubleshooting)

---

## Multi-Stage Builds

### Go Application (Optimized)

```dockerfile
# Stage 1: Build
FROM golang:1.24-alpine AS builder
WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build with optimizations
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w -X main.version=$(git describe --tags)" \
    -o /app/server ./cmd/server

# Stage 2: Runtime (scratch = smallest possible)
FROM scratch
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Node.js/Nuxt Application

```dockerfile
FROM node:22-alpine AS base
RUN corepack enable && corepack prepare pnpm@latest --activate

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

# Runtime
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
COPY --from=builder --chown=app:app /app/.output ./.output

USER app
EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
```

### BuildKit Cache Mounts

```dockerfile
# Cache package manager downloads between builds
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/server ./cmd/server

# Cache pnpm store
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
```

---

## Security Hardening

### Non-Root User

```dockerfile
# Create non-root user in build stage
RUN addgroup -g 65532 -S nonroot && \
    adduser -u 65532 -S nonroot -G nonroot

USER nonroot:nonroot
```

### Read-Only Filesystem

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    read_only: true
    tmpfs:
      - /tmp:size=100M
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
```

### Secrets Management

```dockerfile
# ✅ Use BuildKit secrets (never in image layers)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    pnpm install --frozen-lockfile

# Build: docker build --secret id=npmrc,src=.npmrc .
```

### Image Scanning

```yaml
# CI pipeline
steps:
  - run: docker build -t myapp .
  - run: docker scout cves myapp --only-severity critical,high
  - run: trivy image --severity HIGH,CRITICAL myapp
```

---

## Compose Patterns

### Service Dependencies & Health

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
    secrets:
      - db_password

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    env_file: .env
    ports:
      - "${PORT:-3000}:3000"

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  pgdata:
```

### Compose Profiles

```yaml
services:
  app:
    # Always runs
    build: .

  debug-tools:
    profiles: ["debug"]
    image: nicolaka/netshoot
    network_mode: "service:app"

  monitoring:
    profiles: ["monitoring"]
    image: grafana/grafana

# Usage:
# docker compose up                        # Only app
# docker compose --profile debug up        # + debug tools
# docker compose --profile monitoring up   # + monitoring
```

---

## Networking

### Custom Networks

```yaml
services:
  frontend:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend  # Not accessible from frontend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

---

## Debugging & Troubleshooting

### Essential Commands

```bash
# Inspect container
docker inspect <container> --format '{{json .State}}'
docker stats --no-stream

# Debug running container
docker exec -it <container> sh
docker logs <container> --since 5m --follow

# Network debugging
docker network inspect bridge
docker run --rm --net=host nicolaka/netshoot tcpdump -i any port 3000

# Disk usage
docker system df
docker builder prune --filter "until=24h"

# Copy files from container
docker cp <container>:/app/logs ./debug-logs
```

### Layer Analysis

```bash
# Analyze image layers (find bloat)
docker history myapp --no-trunc --format "table {{.Size}}\t{{.CreatedBy}}"

# Use dive for interactive analysis
dive myapp:latest
```

---
