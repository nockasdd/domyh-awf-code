# Kubernetes Orchestration

Kubernetes orchestration patterns for K8s 1.32-1.33+. Covers Gateway API, Sidecar Containers, Kueue, Pod Security.

## Patterns (20 total)

### Networking (5)

- Gateway API (HTTPRoute, GRPCRoute, TLSRoute)
- Service mesh integration (Istio, Linkerd)
- Network Policies for pod-to-pod isolation
- DNS configuration and CoreDNS tuning
- Ingress to Gateway API migration

### Workloads (5)

- Sidecar Containers (native K8s 1.28+ support)
- Init containers for setup tasks
- Deployment rolling update strategies
- StatefulSet with persistent volumes
- Job/CronJob with deadline and backoff

### Security (5)

- Pod Security Standards (Restricted, Baseline, Privileged)
- RBAC with least-privilege principles
- Service Account token projection
- Secrets management (external-secrets, sealed-secrets)
- Container runtime sandboxing (gVisor, Kata)

### Scheduling (5)

- Kueue for job queuing and fair scheduling
- Node affinity and anti-affinity rules
- Topology spread constraints
- Priority classes for preemption
- Cluster autoscaler configuration

## Best Practices

- Use Namespace isolation for multi-tenancy
- Set resource requests AND limits on all containers
- Use PodDisruptionBudget for high availability
- Enable audit logging for security compliance
- Use Helm or Kustomize for reproducible deployments

## Data Files

- `data/gateway-api.yaml` — Gateway API patterns
- `data/workloads.yaml` — Workload patterns
- `data/security.yaml` — K8s security patterns
- `data/scheduling.yaml` — Scheduling patterns
