# CI/CD Pipelines

CI/CD pipeline patterns for GitHub Actions, GitLab CI, and GitOps. Includes SLSA Build Level 3, ARM64 runners, security scanning.

## Patterns (20 total)

### GitHub Actions (6)

- Reusable workflows with `workflow_call`
- Composite actions for shared steps
- ARM64 runner configuration (GitHub-hosted)
- SLSA Build Level 3 attestation
- Matrix builds with dynamic strategy
- Deployment environments with protection rules

### GitLab CI (5)

- Multi-project pipeline orchestration
- Auto DevOps configuration
- GitLab Container Registry integration
- Merge train configuration
- Dynamic child pipelines

### Security (5)

- Dependency review action (license + vulnerability)
- Code scanning with CodeQL
- Secret scanning with push protection
- Artifact attestation (SLSA provenance)
- Supply chain security (SBOM generation)

### Deployment (4)

- Blue/green deployment patterns
- Canary release with progressive rollout
- GitOps with ArgoCD/Flux
- Multi-environment promotion pipeline

## Best Practices

- Pin actions to commit SHA (not tags)
- Use OIDC for cloud provider auth (no long-lived secrets)
- Cache dependencies (npm, pip, go modules)
- Fail fast with `continue-on-error: false`
- Set timeout-minutes on all jobs

## Data Files

- `data/github-actions.yaml` — GitHub Actions patterns
- `data/gitlab-ci.yaml` — GitLab CI patterns
- `data/security.yaml` — Pipeline security patterns
