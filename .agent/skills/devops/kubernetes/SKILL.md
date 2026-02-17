---
name: kubernetes
version: "6.3.1"
category: infrastructure
---

# Kubernetes Orchestration

Kubernetes orchestration patterns for K8s 1.32-1.33+. Covers Gateway API, Sidecar Containers, Kueue, Pod Security.

## Decision Tree

```
Task → What are you deploying to K8s?
  ├─ Stateless web app
  │   ├─ Simple → Deployment + Service + Ingress
  │   └─ Advanced → Deployment + Gateway API (HTTPRoute)
  ├─ Stateful service (database, cache)
  │   └─ StatefulSet + PersistentVolumeClaim
  ├─ Background job
  │   ├─ One-time → Job with backoffLimit
  │   ├─ Scheduled → CronJob
  │   └─ Queued → Kueue (fair scheduling)
  ├─ Networking
  │   ├─ Modern → Gateway API (HTTPRoute, GRPCRoute)
  │   └─ Legacy → Ingress (nginx/traefik)
  └─ Package management
      ├─ Templating → Helm charts
      └─ Patching → Kustomize overlays
```

## Quick Start — Deployment + Service

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0 # Zero-downtime
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

## Quick Start — Gateway API

```yaml
# gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: myapp-route
spec:
  parentRefs:
    - name: main-gateway
  hostnames:
    - "api.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: myapp
          port: 80
          weight: 100
```

## Production Checklist

- [ ] Set `requests` AND `limits` on all containers
- [ ] Add `readinessProbe` and `livenessProbe`
- [ ] Use `PodDisruptionBudget` (minAvailable: 1)
- [ ] Apply `Pod Security Standards` (restricted)
- [ ] Set `securityContext.runAsNonRoot: true`
- [ ] Use `Namespace` isolation for multi-tenancy
- [ ] Configure `NetworkPolicy` for pod-to-pod isolation
- [ ] Enable `HorizontalPodAutoscaler` for scaling
- [ ] Use `topologySpreadConstraints` across zones
- [ ] Implement `startupProbe` for slow-starting apps

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

## Data Files

- `data/gateway-api.yaml` — Gateway API patterns
- `data/workloads.yaml` — Workload patterns
- `data/security.yaml` — K8s security patterns
- `data/scheduling.yaml` — Scheduling patterns
