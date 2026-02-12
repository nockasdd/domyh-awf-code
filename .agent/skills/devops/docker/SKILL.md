# Docker Containerization

Docker containerization patterns for builds, security, and deployment. Covers Compose v5, Hardened Images, Build Cloud, Bake.

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

## Best Practices

- Use specific image tags (never `latest` in production)
- Order Dockerfile instructions for cache optimization
- Use `.dockerignore` to reduce build context
- Run as non-root user (`USER 1001`)
- Use COPY instead of ADD (explicit behavior)

## Data Files

- `data/dockerfile.yaml` — Dockerfile patterns
- `data/compose.yaml` — Docker Compose patterns
- `data/security.yaml` — Container security patterns
