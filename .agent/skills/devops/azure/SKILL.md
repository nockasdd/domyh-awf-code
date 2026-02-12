# Microsoft Azure

> Azure Functions • Azure DevOps • Cosmos DB • AKS

---

## Khi Nào Dùng

- Deploy serverless functions (Azure Functions)
- CI/CD pipelines (Azure DevOps)
- NoSQL database (Cosmos DB)
- Enterprise app deployment

## Service Selection

| Service             | Type                 | Best For               |
| ------------------- | -------------------- | ---------------------- |
| **Azure Functions** | Serverless functions | Event-driven, webhooks |
| **App Service**     | Managed web apps     | APIs, web apps         |
| **AKS**             | Managed Kubernetes   | Microservices          |
| **Cosmos DB**       | Multi-model NoSQL    | Global distribution    |
| **Azure SQL**       | Managed SQL          | Relational data        |

## Azure Functions Quick Start

```bash
func init MyProject --typescript
func new --name HttpTrigger --template "HTTP trigger"
func start  # Local development
az functionapp publish MyFunctionApp  # Deploy
```

## Common Traps

| Trap            | Fix                                          |
| --------------- | -------------------------------------------- |
| Cold starts     | Premium plan, keep-alive pings               |
| Entra ID config | Use managed identity, DefaultAzureCredential |
| Cost management | Azure Cost Management + budget alerts        |

---

_DOMYH Awesome Code • Azure Skill v1.0.0_
