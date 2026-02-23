---
name: gcp
version: "6.4.0"
category: devops
---

# GCP Cloud Services

Google Cloud Platform patterns for compute, data, and AI/ML. Covers Cloud Run, GKE, Cloud Functions, Firestore, Vertex AI.

## Decision Tree

```
Task → What are you deploying?
  ├─ Web API / Microservice
  │   ├─ Stateless container → Cloud Run (serverless)
  │   ├─ Event-driven → Cloud Functions (2nd gen)
  │   └─ Complex orchestration → GKE Autopilot
  ├─ Static website
  │   └─ Cloud Storage + Cloud CDN + Load Balancer
  ├─ Database
  │   ├─ Relational → Cloud SQL (PostgreSQL/MySQL)
  │   ├─ Global NoSQL → Firestore
  │   ├─ Wide column → Bigtable
  │   └─ Analytics → BigQuery
  ├─ AI/ML
  │   ├─ Gemini models → Vertex AI
  │   ├─ Custom training → Vertex AI Training
  │   └─ Vector search → Vertex AI Vector Search
  └─ DevOps
      ├─ CI/CD → Cloud Build or GitHub Actions
      └─ IaC → Terraform (recommended) or Pulumi
```

## Quick Start — Cloud Run

```bash
# Build + deploy in one step
gcloud run deploy myapp \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 10 \
  --memory 512Mi \
  --cpu 1
```

## Quick Start — Vertex AI (Gemini)

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="my-project", location="us-central1")
model = GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Hello, Gemini!")
print(response.text)
```

## Quick Start — Firestore

```typescript
import { initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";

initializeApp();
const db = getFirestore();

// Write
await db.collection("users").doc("user1").set({
  name: "Alice",
  email: "alice@example.com",
});

// Read with real-time listener
db.collection("users").onSnapshot((snapshot) => {
  snapshot.docChanges().forEach((change) => {
    console.log(change.type, change.doc.data());
  });
});
```

## Patterns (22 total)

### Compute (5)

- Cloud Run multi-container, jobs, services
- Cloud Functions 2nd gen (event-driven)
- GKE Autopilot (managed K8s)
- Compute Engine (VMs) with MIGs
- Cloud Tasks for async processing

### Data (6)

- BigQuery (analytics, ML, streaming)
- Firestore (real-time, offline sync)
- Cloud SQL with IAM auth
- Memorystore (Redis/Valkey)
- Pub/Sub for messaging
- Cloud Storage lifecycle policies

### AI (5)

- Vertex AI Gemini 2.0 integration
- Vertex AI Vector Search
- Custom model training + endpoints
- Agent Builder
- Document AI

### Infrastructure (6)

- Terraform modules for GCP
- Cloud Build CI/CD pipelines
- Workload Identity Federation
- Secret Manager
- Cloud Armor (WAF)
- VPC Service Controls

## Data Files

- `data/compute.yaml` — Cloud Run, Functions, GKE patterns
- `data/data.yaml` — BigQuery, Firestore, Pub/Sub patterns
- `data/ai.yaml` — Vertex AI, Gemini patterns
