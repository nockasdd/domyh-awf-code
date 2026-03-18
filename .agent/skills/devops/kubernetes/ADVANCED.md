# Kubernetes — Advanced Patterns

## Table of Contents

- [Helm Charts](#helm-charts)
- [Networking & Ingress](#networking--ingress)
- [Scaling Strategies](#scaling-strategies)
- [Security](#security)
- [Debugging](#debugging)
- [Operators & CRDs](#operators--crds)

---

## Helm Charts

### Template Patterns

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "app.fullname" . }}
  labels:
    {{- include "app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "app.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets: {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          livenessProbe:
            httpGet:
              path: /healthz
              port: {{ .Values.service.port }}
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /readyz
              port: {{ .Values.service.port }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          envFrom:
            - configMapRef:
                name: {{ include "app.fullname" . }}
            - secretRef:
                name: {{ include "app.fullname" . }}
```

### Values Structure

```yaml
# values.yaml
replicaCount: 2

image:
  repository: ghcr.io/myorg/myapp
  tag: ""  # Defaults to Chart.appVersion
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 3000

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPU: 70
```

---

## Networking & Ingress

### Ingress with TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts: [app.example.com]
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-svc
                port: { number: 8080 }
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-svc
                port: { number: 3000 }
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: [Ingress, Egress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - port: 5432
    - to:  # Allow DNS
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
```

---

## Scaling Strategies

### HPA (Horizontal Pod Autoscaler)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

### KEDA (Event-Driven)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: worker-scaler
spec:
  scaleTargetRef:
    name: worker
  minReplicaCount: 0   # Scale to zero
  maxReplicaCount: 50
  triggers:
    - type: rabbitmq
      metadata:
        queueName: tasks
        queueLength: "10"  # 1 pod per 10 messages
```

---

## Security

### RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-binding
subjects:
  - kind: ServiceAccount
    name: app-sa
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Standards

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    fsGroup: 65532
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:latest
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: [ALL]
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: { sizeLimit: 100Mi }
```

---

## Debugging

### Essential kubectl

```bash
# Quick pod status
kubectl get pods -o wide --sort-by='.status.startTime'

# Describe events (troubleshoot scheduling)
kubectl describe pod <pod> | tail -20

# Logs with follow
kubectl logs <pod> -f --since=5m
kubectl logs <pod> --previous  # Crashed container logs

# Ephemeral debug container (k8s 1.25+)
kubectl debug -it <pod> --image=nicolaka/netshoot --target=app

# Port forward
kubectl port-forward svc/api 8080:8080

# Resource usage
kubectl top pods --sort-by=memory
kubectl top nodes

# Exec into pod
kubectl exec -it <pod> -- sh

# Copy files
kubectl cp <pod>:/app/logs ./debug-logs
```

### Common Issues

```yaml
troubleshooting:
  CrashLoopBackOff:
    - "Check logs: kubectl logs <pod> --previous"
    - "Verify CMD/ENTRYPOINT in Dockerfile"
    - "Check resource limits (OOMKilled)"
  ImagePullBackOff:
    - "Verify image name and tag"
    - "Check imagePullSecrets"
    - "Test: docker pull <image> locally"
  Pending:
    - "Check events: kubectl describe pod"
    - "Insufficient resources? kubectl describe node"
    - "PVC not bound? kubectl get pvc"
```

---

## Operators & CRDs

### Custom Resource Definition

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.app.example.com
spec:
  group: app.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                engine:
                  type: string
                  enum: [postgres, mysql]
                version:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames: [db]
```

```yaml
# Usage
apiVersion: app.example.com/v1
kind: Database
metadata:
  name: mydb
spec:
  engine: postgres
  version: "17"
  replicas: 3
```

---
