# AWS Cloud Services

AWS cloud services patterns for serverless, containers, and AI/ML. Covers Lambda, S3, ECS, EKS, Bedrock, and SageMaker.

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
- S3 metadata management
- S3 lifecycle policies
- Cross-region replication

### Kubernetes (5)

- EKS cluster configuration
- EKS Pod Identity (replaces IRSA)
- EKS capabilities and add-ons
- Fargate profiles for EKS
- EKS auto-mode

### AI/ML (5)

- Bedrock foundation models integration
- SageMaker model training pipeline
- MLFlow experiment tracking
- Bedrock Agents for autonomous tasks
- SageMaker inference endpoints

### Serverless (4)

- API Gateway + Lambda patterns
- Step Functions orchestration
- DynamoDB single-table design
- CloudFront edge functions

## Data Files

- `data/lambda.yaml` — Lambda patterns and configs
- `data/s3.yaml` — S3 patterns and lifecycle
- `data/eks.yaml` — EKS cluster patterns
- `data/ai-ml.yaml` — Bedrock and SageMaker patterns
- `data/cli.yaml` — AWS CLI reference
