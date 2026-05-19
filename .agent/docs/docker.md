---
library: docker
version: latest
latest: true
category: devops
official_docs: https://docs.docker.com
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# Docker

> Docker — Container platform for building, sharing, and running applications.
> Docs: https://docs.docker.com

## Dockerfile

### Node.js Production

```dockerfile
# Multi-stage build (optimized)
FROM node:22-alpine AS base
WORKDIR /app

# Install dependencies (cached layer)
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Build
FROM base AS builder
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production image
FROM base AS runner
ENV NODE_ENV=production

# Security: non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 appuser

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

### Python Production

```dockerfile
FROM python:3.14-slim AS base
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Init (Scaffolding)

```bash
# Auto-generate Dockerfile, compose.yaml, .dockerignore
docker init
# Supports: Node.js, Python, Go, Rust, ASP.NET, PHP, Java
# Creates best-practice multi-stage Dockerfile automatically
```

### Optimizations

```dockerfile
# .dockerignore (ALWAYS create)
node_modules
.git
.env
.env.local
dist
*.md
.vscode
.idea
coverage
__pycache__
.pytest_cache

# Layer caching best practices:
# 1. Copy package files FIRST (cache npm install)
# 2. Copy source code LAST (changes most frequently)
# 3. Use --omit=dev for production
# 4. Use alpine/slim base images
# 5. Combine RUN commands to reduce layers
```

## Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    networks:
      - app-network
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

## Networking

```yaml
# Custom network
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # no external access

services:
  app:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend  # only accessible from backend network
```

```bash
# Create network
docker network create my-network

# Connect container
docker network connect my-network my-container

# DNS: containers on same network use service name as hostname
# e.g., app connects to db via "db:5432"
```

## CLI Commands

```bash
# Build
docker build -t my-app:latest .
docker build -t my-app:latest --target builder .  # specific stage
docker build --no-cache -t my-app .

# Run
docker run -d --name my-app -p 3000:3000 my-app:latest
docker run -it --rm my-app:latest sh                # interactive shell
docker run -d --env-file .env my-app:latest
docker run -d -v $(pwd)/data:/app/data my-app       # mount volume

# Compose
docker compose up -d                  # start all services
docker compose up -d --build          # rebuild and start
docker compose down                   # stop and remove
docker compose down -v                # also remove volumes
docker compose logs -f app            # follow logs
docker compose exec app sh            # shell into running container
docker compose ps                     # list running services

# Management
docker ps                             # running containers
docker ps -a                          # all containers
docker logs -f container_name         # follow logs
docker exec -it container_name sh     # shell into container
docker stop container_name
docker rm container_name
docker system prune -a                # remove all unused resources
docker volume ls                      # list volumes
docker image ls                       # list images

# Debug
docker inspect container_name         # full container info
docker stats                          # live resource usage
docker top container_name             # processes in container
```

## CI/CD Patterns

```yaml
# GitHub Actions
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/user/app:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t my-app:latest --push .
```

## Docker Compose

```yaml
# docker-compose.yml (Compose V2)
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src  # bind mount for dev
    networks:
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - backend

volumes:
  pgdata:

networks:
  backend:
    driver: bridge
```

```bash
# Compose commands
docker compose up -d                   # start detached
docker compose up --build              # rebuild + start
docker compose down                    # stop + remove
docker compose down -v                 # stop + remove + volumes
docker compose logs -f app             # follow logs
docker compose exec app sh             # shell into container
docker compose ps                      # list running services
docker compose pull                    # pull latest images
```

## Multi-stage Build (Production)

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER nextjs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Networking

```bash
# Create custom network
docker network create my-network

# Connect containers
docker run --network my-network --name api my-api
docker run --network my-network --name db postgres

# Container DNS: containers reference each other by name
# api can connect to db:5432 via Docker DNS
```

## Security

```bash
# Scan image for vulnerabilities
docker scout cves my-image:latest
docker scout quickview my-image:latest

# Best practices
# 1. Use specific image tags (not :latest)
# 2. Run as non-root user (USER node)
# 3. Use .dockerignore
# 4. Scan with docker scout
# 5. Use multi-stage builds (no build tools in prod)
# 6. Set read-only filesystem: --read-only
```

## Gotchas

⚠️ **`.dockerignore`**: ALWAYS create. Without it, `node_modules/`, `.git/`, etc. bloat context.

⚠️ **Multi-stage builds**: Use `FROM ... AS builder` → `COPY --from=builder` for smaller images.

⚠️ **Layer caching**: Order matters. Copy `package.json` before source code to cache `npm ci`.

⚠️ **`USER node`**: Run as non-root in production. Never run containers as root.

⚠️ **`HEALTHCHECK`**: Add to detect crashed processes. Compose `depends_on.condition: service_healthy`.

⚠️ **`volumes`**: Named volumes persist data. Bind mounts sync host files.

⚠️ **`docker compose up --build`**: Must use `--build` to rebuild after code changes.

⚠️ **Alpine**: Smaller images but uses `musl` (not `glibc`). Some native modules may not work.

⚠️ **`ENV NODE_ENV=production`**: Set in Dockerfile — npm omits devDependencies, Express enables caching.

⚠️ **Compose V2**: Use `docker compose` (space) not `docker-compose` (hyphen, legacy).

⚠️ **Docker Scout**: Use `docker scout cves` to scan for CVEs before deploying.

⚠️ **Networking**: Containers on same network use service names as hostnames (Docker DNS).
