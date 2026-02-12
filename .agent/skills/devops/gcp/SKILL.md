# Google Cloud Platform

> Cloud Run • Cloud Functions • BigQuery • Firestore

---

## Khi Nào Dùng

- Deploy containerized apps (Cloud Run)
- Serverless functions (Cloud Functions)
- Big data analytics (BigQuery)

## Service Selection

| Service             | Type                   | Best For              |
| ------------------- | ---------------------- | --------------------- |
| **Cloud Run**       | Serverless containers  | APIs, web apps        |
| **Cloud Functions** | Event-driven functions | Webhooks, triggers    |
| **GKE**             | Managed K8s            | Complex microservices |
| **BigQuery**        | Data warehouse         | Analytics, ML         |
| **Firestore**       | NoSQL document DB      | Real-time apps        |
| **Cloud SQL**       | Managed SQL            | Relational data       |

## Cloud Run Quick Start

```bash
gcloud run deploy my-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## Common Traps

| Trap           | Fix                                    |
| -------------- | -------------------------------------- |
| Cold starts    | Min instances, Cloud Run always-on     |
| IAM complexity | Use workload identity, least privilege |
| Cost spike     | Budget alerts, quotas                  |

---

_DOMYH Awesome Code • GCP Skill v1.0.0_
