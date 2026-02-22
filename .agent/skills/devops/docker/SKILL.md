---
name: docker
version: "6.3.9"
category: infrastructure
---

# Docker Containerization

Docker containerization patterns for builds, security, and deployment. Covers Compose v5, Hardened Images, Build Cloud, Bake.

## Decision Tree

```
Task → What are you building?
  ├─ Development environment
  │   ├─ Single service → Dockerfile + docker run
  │   └─ Multi-service → docker-compose.yml
  │       ├─ Hot reload → Compose watch
  │       └─ DB included → services + healthcheck
  ├─ Production image
  │   ├─ Node.js → Multi-stage (builder → node:alpine)
  │   ├─ Go → Multi-stage (builder → scratch/distroless)
  │   ├─ Python → Multi-stage (builder → python:slim)
  │   └─ Static site → Multi-stage (build → nginx:alpine)
  └─ CI/CD
      ├─ Multi-platform → Buildx (linux/amd64 + arm64)
      └─ Complex builds → Docker Bake (HCL)
```

## Quick Start — Multi-Stage Build (Node.js)

```dockerfile
# Stage 1: Build
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:22-alpine
RUN addgroup -g 1001 -S appuser && adduser -u 1001 -S appuser -G appuser
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app/dist ./dist
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

## Compose v5 — Dev Environment

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      target: builder # Use builder stage for dev
    volumes:
      - .:/app
      - /app/node_modules # Anonymous volume (don't mount)
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASS:-dev}
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

volumes:
  pgdata:
```

## Security Hardening Checklist

- [ ] Use specific image tags (never `:latest` in production)
- [ ] Run as non-root user (`USER 1001`)
- [ ] Use `COPY` instead of `ADD`
- [ ] Add `.dockerignore` (exclude `.git`, `node_modules`, `.env`)
- [ ] Use distroless/chainguard base images for production
- [ ] Scan with Docker Scout: `docker scout quickview`
- [ ] Sign images with cosign
- [ ] Set resource limits: `--memory=512m --cpus=1`
- [ ] Use `--init` flag for proper signal handling
- [ ] Order Dockerfile instructions for cache optimization

## Patterns (18 total)

### Build (5)

- Multi-stage builds for minimal images
- BuildKit with `--mount=type=cache` for fast rebuilds
- Docker Bake (HCL) for multi-platform builds
- Build Cloud for remote builder instances
- Buildx for cross-platform (linux/amd64, linux/arm64)

### Compose (5)

- Compose v5 with `watch` for live reload
- Service profiles for dev/test/prod
- Compose `include` for modular configs
- Health checks with `test`, `interval`, `retries`
- Named volumes with backup strategies

### Security (4)

- Hardened base images (distroless, chainguard)
- Rootless container execution
- Docker Scout for vulnerability scanning
- Content trust and image signing (cosign)

### Runtime (4)

- Init containers (`--init` flag)
- Resource limits (memory, CPU)
- Logging drivers configuration
- Container networking (bridge, host, overlay)

## Data Files

- `data/dockerfile.yaml` — Dockerfile patterns
- `data/compose.yaml` — Docker Compose patterns
- `data/security.yaml` — Container security patterns
