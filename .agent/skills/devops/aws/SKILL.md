---
name: aws
description: "AWS cloud service patterns. Use when working with EC2, S3, Lambda, ECS, RDS, or other AWS services."
category: infrastructure
---

# AWS Cloud Services

AWS cloud services patterns for serverless, containers, and AI/ML. Covers Lambda, S3, ECS, EKS, Bedrock, and SageMaker.

## Decision Tree

```
Task → What are you deploying?
  ├─ API/Microservice
  │   ├─ Low traffic / event-driven → Lambda + API Gateway
  │   ├─ Medium traffic → ECS Fargate (containers)
  │   └─ High traffic / complex → EKS (Kubernetes)
  ├─ Static website
  │   └─ S3 + CloudFront (CDN)
  ├─ Data processing
  │   ├─ Batch → Step Functions + Lambda
  │   ├─ Stream → Kinesis + Lambda
  │   └─ ETL → Glue
  ├─ AI/ML
  │   ├─ Foundation models → Bedrock
  │   ├─ Custom training → SageMaker
  │   └─ RAG → Bedrock + OpenSearch Serverless
  └─ Database
      ├─ Relational → RDS (PostgreSQL/MySQL) or Aurora
      ├─ Key-value → DynamoDB
      ├─ Cache → ElastiCache (Redis/Valkey)
      └─ Vector → OpenSearch Serverless
```

## Quick Start — Lambda + API Gateway

```yaml
# template.yaml (SAM)
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: nodejs22.x
    MemorySize: 256
    Architectures: [arm64] # Graviton = cheaper + faster
    Environment:
      Variables:
        NODE_ENV: production

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: index.handler
      Events:
        Api:
          Type: HttpApi
          Properties:
            Path: /api/{proxy+}
            Method: ANY
```

```bash
# Deploy
sam build
sam deploy --guided
```

## Quick Start — ECS Fargate

```bash
# Create cluster + service
aws ecs create-cluster --cluster-name myapp
aws ecs create-service \
  --cluster myapp \
  --service-name api \
  --task-definition myapp:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## Quick Start — Bedrock

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Hello"}]
    })
)
result = json.loads(response['body'].read())
```

## Patterns (25 total)

### Compute (6)

- Lambda function design (event-driven, cold start optimization)
- Lambda Layers for shared dependencies
- ECS task definitions with Fargate
- ECS managed instances vs Fargate decision matrix
- Lambda Durable (step functions)
- EventBridge for event routing

### Storage (5)

- S3 Vectors (vector embeddings in S3)
- S3 Tables (Apache Iceberg format)
- S3 lifecycle policies and replication

### Kubernetes (5)

- EKS cluster configuration + Pod Identity
- Fargate profiles, auto-mode, add-ons

### AI/ML (5)

- Bedrock foundation models + Agents
- SageMaker training + inference endpoints

### Serverless (4)

- API Gateway + Lambda patterns
- Step Functions, DynamoDB single-table design

## Data Files

- `data/lambda.yaml` — Lambda patterns and configs
- `data/s3.yaml` — S3 patterns and lifecycle
- `data/eks.yaml` — EKS cluster patterns
- `data/ai-ml.yaml` — Bedrock and SageMaker patterns
- `data/cli.yaml` — AWS CLI reference
