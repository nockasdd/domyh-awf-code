---
name: kubernetes
detect:
  ["*.yaml:kind", "helm/", "kustomization.yaml", "Chart.yaml", "values.yaml"]
version: "6.1.2"
category: devops
tier: 1
---

# Kubernetes Patterns — DOMYH Awesome Code v6.1.2

> **Version**: Kubernetes 1.30/1.31 (2025-2026)
> **Runtime**: Container orchestration platform
> **Philosophy**: Declarative infrastructure, GitOps, immutable deployments

---

## 🎯 When to Use This Skill

Use for: Pod management, deployments, services, Helm charts, ArgoCD GitOps, scaling, security.
**NOT for**: Docker builds (→ docker skill), cloud providers (→ aws/gcp skills).

---

## 📦 Ecosystem Tools (2025-2026)

### Core CLI Tools

| Tool               | Use Case                 | Install                |
| ------------------ | ------------------------ | ---------------------- |
| **kubectl**        | Cluster management       | `brew install kubectl` |
| **Helm 3**         | Package manager          | `brew install helm`    |
| **Kustomize**      | Config customization     | Built into kubectl     |
| **k9s**            | Terminal UI              | `brew install k9s`     |
| **kubectx/kubens** | Context/namespace switch | `brew install kubectx` |

### GitOps & CD

| Tool              | Use Case             | Install                          |
| ----------------- | -------------------- | -------------------------------- |
| **ArgoCD**        | GitOps CD 🏆         | `kubectl apply -n argocd`        |
| **Flux v2**       | GitOps alternative   | `flux bootstrap`                 |
| **Argo Rollouts** | Progressive delivery | `kubectl apply -n argo-rollouts` |

### IDE Support

| IDE          | Extension         | Features                                    |
| ------------ | ----------------- | ------------------------------------------- |
| **Lens**     | Native            | Real-time dashboard, multi-cluster, logs 🏆 |
| **VS Code**  | Kubernetes ext    | YAML validation, kubectl integration        |
| **IntelliJ** | Kubernetes plugin | Helm support, resource browser              |

---

## 🏗️ Kubernetes 1.30/1.31 Features

### New in 1.31 (2025)

```yaml
# ✅ AppArmor (STABLE) - Security profiles
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    appArmorProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:v1
```

### PodDisruptionBudget với PodHealthyPolicy

```yaml
# ✅ PDB with AlwaysAllow policy (1.31)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
  unhealthyPodEvictionPolicy: AlwaysAllow
```

---

## 📋 Deployment Best Practices

### Production-Ready Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
    version: v1.2.3
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0 # Zero downtime
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.2.3
    spec:
      # ✅ Security Context (mandatory)
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault

      # ✅ Service Account (principle of least privilege)
      serviceAccountName: app-sa
      automountServiceAccountToken: false

      containers:
        - name: app
          image: myapp:v1.2.3
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8080
              protocol: TCP

          # ✅ Resource Management (REQUIRED)
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"

          # ✅ Health Probes (REQUIRED)
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5

          # ✅ Startup Probe (slow-starting apps)
          startupProbe:
            httpGet:
              path: /health
              port: 8080
            failureThreshold: 30
            periodSeconds: 10

          # ✅ Environment Variables
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: password

          # ✅ Container Security
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

          # ✅ Volume Mounts
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: config
              mountPath: /app/config
              readOnly: true

      # ✅ Volumes
      volumes:
        - name: tmp
          emptyDir: {}
        - name: config
          configMap:
            name: app-config

      # ✅ Topology Spread (High Availability)
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: myapp
```

---

## 🔧 Helm Best Practices

### Chart Structure

```
mychart/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
└── charts/           # Dependencies
```

### values.yaml Pattern

```yaml
# values.yaml
replicaCount: 3

image:
  repository: myapp
  tag: "v1.2.3" # Always pinned tag, no :latest
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilization: 70

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
```

### Template với Helpers

```yaml
{{/* templates/_helpers.tpl */}}
{{- define "app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "app.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

---

## 🔄 ArgoCD GitOps Patterns

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: HEAD
    path: apps/myapp/overlays/prod

    # ✅ Helm source
    # helm:
    #   valueFiles:
    #     - values-prod.yaml

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### ApplicationSet (Multi-Cluster)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-clusters
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production
  template:
    metadata:
      name: "{{name}}-myapp"
    spec:
      project: default
      source:
        repoURL: https://github.com/org/gitops-repo.git
        targetRevision: HEAD
        path: apps/myapp/overlays/{{metadata.labels.env}}
      destination:
        server: "{{server}}"
        namespace: myapp
```

---

## 📊 HorizontalPodAutoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    # ✅ CPU-based scaling
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    # ✅ Memory-based scaling
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

---

## 🔐 Security Best Practices

### NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              role: database
      ports:
        - protocol: TCP
          port: 5432
```

### RBAC Least Privilege

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list"]
    resourceNames: ["app-config", "app-secrets"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
subjects:
  - kind: ServiceAccount
    name: app-sa
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

---

## 🛠️ Essential Commands

```bash
# Context Management
kubectl config get-contexts
kubectl config use-context prod-cluster
kubectx prod-cluster  # Faster with kubectx

# Resource Management
kubectl get pods -n myapp -o wide
kubectl describe pod myapp-xxx -n myapp
kubectl logs -f myapp-xxx -n myapp --tail=100
kubectl exec -it myapp-xxx -n myapp -- /bin/sh

# Debugging
kubectl get events -n myapp --sort-by='.lastTimestamp'
kubectl top pods -n myapp
kubectl rollout status deployment/myapp -n myapp
kubectl rollout undo deployment/myapp -n myapp

# Helm
helm install myapp ./mychart -f values-prod.yaml -n myapp
helm upgrade myapp ./mychart -f values-prod.yaml -n myapp
helm list -n myapp
helm history myapp -n myapp

# ArgoCD
argocd app list
argocd app sync myapp
argocd app diff myapp
```

---

## ✅ Production Checklist

### Resource Configuration

- [ ] Resource requests/limits set
- [ ] HPA configured with appropriate thresholds
- [ ] VPA considered for optimization

### Reliability

- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Startup probe for slow apps
- [ ] PodDisruptionBudget set
- [ ] Topology spread constraints

### Security

- [ ] runAsNonRoot: true
- [ ] readOnlyRootFilesystem: true
- [ ] Drop ALL capabilities
- [ ] NetworkPolicies defined
- [ ] RBAC least privilege
- [ ] Secrets encrypted at rest
- [ ] Image scanning in CI/CD

### Observability

- [ ] Structured logging
- [ ] Metrics exported
- [ ] Tracing enabled
- [ ] Alerts configured

---

_DOMYH Awesome Code v6.1.2 • Kubernetes 1.30/1.31_
