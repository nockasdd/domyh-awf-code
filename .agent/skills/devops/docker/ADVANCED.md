# Docker — Advanced Patterns

> DOMYH Awesome Code v6.1.2 — Tier 3 Reference

## Table of Contents

- [BuildKit Advanced Features](#buildkit-advanced-features)
- [Production Security](#production-security)
- [Multi-Architecture Builds](#multi-architecture-builds)
- [Container Networking](#container-networking)
- [Orchestration Patterns](#orchestration-patterns)
- [Debugging & Troubleshooting](#debugging--troubleshooting)

---

## BuildKit Advanced Features

### Cache Mounts (Persistent Across Builds)

```dockerfile
# syntax=docker/dockerfile:1

# ✅ npm/yarn cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --frozen-lockfile

# ✅ pnpm cache mount (different location)
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

# ✅ apt cache mount (speeds up apt-get significantly)
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ pip cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# ✅ Go modules cache
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/server ./cmd/server

# ✅ Rust cargo cache
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/usr/local/cargo/git \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

### Secret Mounts (Build-Time Secrets)

```dockerfile
# ✅ NPM private registry token (not in image)
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) \
    npm ci

# ✅ Git credentials for private repos
RUN --mount=type=secret,id=git_token \
    GIT_TOKEN=$(cat /run/secrets/git_token) \
    git clone https://${GIT_TOKEN}@github.com/org/private.git

# Build command:
# docker build \
#   --secret id=npm_token,src=.npmrc \
#   --secret id=git_token,src=.git-token \
#   -t myapp .
```

### SSH Agent Forwarding

```dockerfile
# ✅ Clone private repo using SSH
RUN --mount=type=ssh \
    mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    git clone git@github.com:org/private-repo.git

# Build command (forwards SSH agent):
# docker build --ssh default -t myapp .
```

### Here Documents (Multi-line Scripts)

```dockerfile
# ✅ Multi-line script with heredoc (BuildKit)
RUN <<EOF
#!/bin/bash
set -e
apt-get update
apt-get install -y --no-install-recommends \
    curl \
    ca-certificates
rm -rf /var/lib/apt/lists/*
EOF

# ✅ Create config file with heredoc
COPY <<EOF /etc/myapp/config.yaml
database:
  host: postgres
  port: 5432
logging:
  level: info
EOF
```

---

## Production Security

### Distroless Images

```dockerfile
# Build stage with tools
FROM golang:1.24-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /server

# ✅ Distroless: No shell, no package manager
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

### Chainguard Images (Security + Updates)

```dockerfile
# ✅ Chainguard: Hardened + updated base images
FROM cgr.dev/chainguard/node:latest AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/main.js"]
```

### Read-Only Filesystem

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    # ✅ Read-only root filesystem
    read_only: true
    # ✅ Writable tmpfs for temp files
    tmpfs:
      - /tmp:size=100M,mode=1777
      - /var/run
    # ✅ Security options
    security_opt:
      - no-new-privileges:true
    # ✅ Drop all capabilities
    cap_drop:
      - ALL
    # ✅ Add only what's needed
    cap_add:
      - NET_BIND_SERVICE # Only if binding to port < 1024
```

### Rootless Docker

```bash
# Install rootless Docker
dockerd-rootless-setuptool.sh install

# Start rootless daemon
systemctl --user start docker

# Set socket path
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock

# Verify
docker info | grep "rootless"
```

### Container Security Scanning

```bash
# Docker Scout (integrated)
docker scout cves myimage:latest
docker scout recommendations myimage:latest

# Trivy (comprehensive)
trivy image --severity HIGH,CRITICAL myimage:latest

# Grype (fast)
grype myimage:latest

# Snyk (with remediation)
snyk container test myimage:latest
```

---

## Multi-Architecture Builds

### Using docker buildx

```bash
# Create multi-platform builder
docker buildx create --name multiarch --driver docker-container --use

# Build for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag myapp:latest \
  --push \
  .

# Build and load locally (single arch)
docker buildx build \
  --platform linux/amd64 \
  --tag myapp:latest \
  --load \
  .

# Inspect manifest
docker buildx imagetools inspect myapp:latest
```

### Dockerfile for Multi-Arch

```dockerfile
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM golang:1.24-alpine AS builder

# ✅ BuildKit provides these ARGs automatically
ARG TARGETOS
ARG TARGETARCH

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# ✅ Cross-compile for target architecture
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -ldflags="-s -w" -o /server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /server /server
ENTRYPOINT ["/server"]
```

---

## Container Networking

### Network Types

```yaml
# docker-compose.yml
services:
  frontend:
    networks:
      - public

  app:
    networks:
      - public
      - backend

  db:
    networks:
      - backend # Not accessible from public

networks:
  public:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24

  backend:
    driver: bridge
    internal: true # ✅ No internet access
    ipam:
      config:
        - subnet: 172.21.0.0/24
```

### Custom DNS and Aliases

```yaml
services:
  app:
    networks:
      backend:
        aliases:
          - api
          - backend-api
        ipv4_address: 172.21.0.10

  db:
    networks:
      backend:
        aliases:
          - postgres
          - database
```

### Host Networking (Performance)

```yaml
services:
  # ✅ Use host network for max performance (no NAT)
  high-performance-app:
    network_mode: host
    # Note: port mapping not available with host mode
```

---

## Orchestration Patterns

### Rolling Updates

```yaml
services:
  app:
    image: myapp:${VERSION:-latest}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1 # Update 1 at a time
        delay: 10s # Wait between updates
        failure_action: rollback
        order: start-first # Start new before stopping old
        monitor: 30s # Health check duration
      rollback_config:
        parallelism: 0 # Rollback all at once
        order: stop-first
```

### Blue-Green Deployment Pattern

```yaml
# docker-compose.blue.yml
services:
  app:
    image: myapp:blue
    networks:
      - production
    deploy:
      labels:
        - "traefik.http.routers.app.rule=Host(`app.example.com`)"

# docker-compose.green.yml
services:
  app:
    image: myapp:green
    networks:
      - production
    deploy:
      labels:
        - "traefik.http.routers.app-canary.rule=Host(`app.example.com`) && Headers(`X-Canary`, `true`)"
```

### Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 1G
          pids: 100 # Process limit
        reservations:
          cpus: "0.5"
          memory: 256M
    # ✅ OOM behavior
    oom_kill_disable: false
    oom_score_adj: -500 # Lower = less likely to be killed
```

---

## Debugging & Troubleshooting

### Interactive Debugging

```bash
# Shell into running container
docker exec -it myapp /bin/sh

# Shell with root (if needed)
docker exec -u root -it myapp /bin/sh

# Run one-off container with current directory
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  node:22-alpine /bin/sh

# Debug distroless (no shell) - use debug image
docker run -it --rm \
  gcr.io/distroless/base-debian12:debug \
  busybox sh
```

### Container Inspection

```bash
# Full container details
docker inspect myapp

# Get specific field
docker inspect --format='{{.State.Status}}' myapp
docker inspect --format='{{.NetworkSettings.IPAddress}}' myapp
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myapp

# View image layers
docker history myapp:latest --no-trunc

# Analyze image size
docker image inspect myapp:latest --format='{{.Size}}' | numfmt --to=iec
```

### Log Analysis

```bash
# Follow logs
docker logs -f myapp

# Tail last 100 lines
docker logs --tail 100 myapp

# Logs with timestamps
docker logs -t myapp

# Logs since timestamp
docker logs --since 2025-01-01T00:00:00 myapp

# Compose logs (all services)
docker compose logs -f

# Compose logs (specific service)
docker compose logs -f app
```

### Resource Monitoring

```bash
# Real-time resource usage
docker stats

# One-shot stats
docker stats --no-stream

# Container processes
docker top myapp

# Disk usage summary
docker system df

# Detailed disk usage
docker system df -v
```

### Cleanup Commands

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune -a --volumes

# Remove ALL containers, images, volumes (careful!)
docker system prune -a --volumes -f
```

---

_DOMYH Awesome Code v6.1.2 — Docker Advanced Patterns — 2025-2026_
