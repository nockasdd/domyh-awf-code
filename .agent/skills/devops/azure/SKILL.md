---
name: azure
version: "6.4.5"
category: devops
---

# Azure Cloud Services

Azure cloud services patterns for enterprise workloads. Covers App Service, AKS, Functions, Cosmos DB, Azure AI.

## Decision Tree

```
Task → What are you deploying?
  ├─ Web API
  │   ├─ Simple → App Service (PaaS)
  │   ├─ Event-driven → Azure Functions
  │   └─ Complex / microservices → AKS (Kubernetes)
  ├─ Static website
  │   └─ Azure Static Web Apps + CDN
  ├─ Database
  │   ├─ Relational → Azure SQL / PostgreSQL Flexible
  │   ├─ NoSQL → Cosmos DB
  │   └─ Cache → Azure Cache for Redis
  ├─ AI/ML
  │   ├─ OpenAI models → Azure OpenAI Service
  │   ├─ Custom models → Azure ML
  │   └─ Search → Azure AI Search (vector + hybrid)
  └─ DevOps
      ├─ CI/CD → Azure DevOps Pipelines or GitHub Actions
      └─ IaC → Bicep (Azure-native) or Terraform
```

## Quick Start — App Service

```bash
# Create and deploy
az group create --name myapp-rg --location eastus
az appservice plan create --name myplan --resource-group myapp-rg --sku B1 --is-linux
az webapp create --name myapp --resource-group myapp-rg --plan myplan --runtime "NODE:22-lts"
az webapp up --name myapp --resource-group myapp-rg
```

## Quick Start — Azure Functions

```typescript
// src/functions/httpTrigger.ts
import { app, HttpRequest, HttpResponseInit } from "@azure/functions";

app.http("hello", {
  methods: ["GET", "POST"],
  authLevel: "anonymous",
  handler: async (request: HttpRequest): Promise<HttpResponseInit> => {
    const name = request.query.get("name") || "World";
    return { body: `Hello, ${name}!` };
  },
});
```

## Quick Start — Azure OpenAI

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-21",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Patterns (20 total)

### Compute (5)

- App Service deployment slots (zero-downtime)
- Azure Functions with Durable Functions
- AKS cluster with managed identity
- Container Apps (serverless containers)
- Azure Spring Apps for Java

### Data (5)

- Cosmos DB partition strategies
- Azure SQL Hyperscale
- PostgreSQL Flexible Server
- Azure Cache for Redis
- Event Hubs for streaming

### AI (5)

- Azure OpenAI GPT-4o integration
- Azure AI Search (vector + hybrid)
- Azure ML endpoints
- Prompt Flow orchestration
- Content Safety filters

### Infrastructure (5)

- Bicep modules (IaC)
- Azure DevOps pipelines
- Managed Identity (passwordless)
- Key Vault integration
- Private Endpoints

## Data Files

- `data/compute.yaml` — App Service, Functions, AKS patterns
- `data/data.yaml` — Cosmos DB, SQL, Redis patterns
- `data/ai.yaml` — Azure OpenAI, AI Search patterns
