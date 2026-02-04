# =============================================================================
# DOMYH Awesome Code CLI — Docker Image
# =============================================================================
# Multi-stage build for minimal image size
# Usage: docker run -v $(pwd):/project domyh/cli init
# =============================================================================

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /build

# Copy CLI package files
COPY domyh-awf-cli/package*.json ./domyh-awf-cli/
COPY domyh-awf-cli/tsconfig.json ./domyh-awf-cli/
COPY domyh-awf-cli/src ./domyh-awf-cli/src

# Copy agent files needed for CLI
COPY .agent ./agent-source/

# Build CLI
WORKDIR /build/domyh-awf-cli
RUN npm ci --only=production
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production

LABEL maintainer="NockDev"
LABEL description="DOMYH Awesome Code CLI - AI Coding Assistant"
LABEL version="6.1.2"

WORKDIR /app

# Copy built CLI
COPY --from=builder /build/domyh-awf-cli/dist ./dist
COPY --from=builder /build/domyh-awf-cli/package*.json ./
COPY --from=builder /build/domyh-awf-cli/node_modules ./node_modules

# Copy agent files
COPY --from=builder /build/agent-source ./.agent

# Create working directory for user projects
WORKDIR /project

# Set entrypoint to CLI
ENTRYPOINT ["node", "/app/dist/cli.js"]

# Default command shows help
CMD ["help"]
