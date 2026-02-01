---
name: aws
detect:
  [
    "serverless.yml",
    "sam.yaml",
    "cdk.json",
    "template.yaml",
    "aws-cdk",
    "@aws-sdk",
  ]
version: "4.3.0"
category: cloud
tier: 2
---

# AWS Development Patterns — DOMYH Agent v4.3

> Comprehensive guide for AWS serverless, containers, and IaC (2025-2026)

## 🔍 Detection Patterns

```yaml
file_patterns:
  serverless: ["serverless.yml", "serverless.ts"]
  sam: ["sam.yaml", "template.yaml", "samconfig.toml"]
  cdk: ["cdk.json", "cdk.out/", "*.cdk.ts"]
  terraform: ["*.tf", "terraform.tfstate"]

code_patterns:
  sdk_v3: ["@aws-sdk/client-*", "from '@aws-sdk/"]
  sdk_python: ["import boto3", "from boto3"]
  lambda: ["APIGatewayProxyHandler", "aws-lambda"]
  powertools: ["aws_lambda_powertools", "@aws-lambda-powertools"]

env_variables:
  - AWS_REGION
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_PROFILE
```

---

## 📊 Service Decision Matrix

### Compute Selection

| Requirement                     | Service        | Pricing Model         |
| ------------------------------- | -------------- | --------------------- |
| **Short tasks (<15min)**        | Lambda         | Per invocation        |
| **Containers (serverless)**     | Fargate        | Per vCPU/memory       |
| **Containers (cost-optimized)** | ECS + EC2      | Instance + container  |
| **Long-running containers**     | ECS + Graviton | 20% better price-perf |
| **Kubernetes**                  | EKS + Fargate  | Managed K8s           |

### Database Selection

| Use Case                      | Service              | When to Use               |
| ----------------------------- | -------------------- | ------------------------- |
| **Key-value, simple queries** | DynamoDB             | Serverless, <10ms latency |
| **Relational, ACID**          | RDS Aurora           | PostgreSQL/MySQL          |
| **Serverless SQL**            | Aurora Serverless v2 | Variable workloads        |
| **Time-series data**          | Timestream           | IoT, metrics              |
| **Cache**                     | ElastiCache          | Redis/Memcached           |

### Event/Messaging Selection

| Pattern                    | Service        | Characteristics                 |
| -------------------------- | -------------- | ------------------------------- |
| **Pub/Sub broadcast**      | SNS            | Push to multiple subscribers    |
| **Queue (async)**          | SQS            | Buffering, retry, at-least-once |
| **Event routing**          | EventBridge    | Filter, transform, route        |
| **Workflow orchestration** | Step Functions | State machine, long-running     |

---

## ⚡ Lambda Patterns

### Handler with AWS SDK v3

```typescript
import { APIGatewayProxyHandler, APIGatewayProxyResult } from "aws-lambda";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand } from "@aws-sdk/lib-dynamodb";

// Initialize outside handler (reuse connection)
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

export const handler: APIGatewayProxyHandler = async (
  event,
): Promise<APIGatewayProxyResult> => {
  try {
    const userId = event.pathParameters?.id;

    const result = await docClient.send(
      new GetCommand({
        TableName: process.env.TABLE_NAME!,
        Key: { id: userId },
      }),
    );

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify(result.Item),
    };
  } catch (error) {
    console.error("Error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error" }),
    };
  }
};
```

### Lambda Powertools (Python)

```python
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
tracer = Tracer()
metrics = Metrics()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def handler(event: dict, context: LambdaContext) -> dict:
    logger.info("Processing request")

    with tracer.capture_method():
        result = process_business_logic(event)

    metrics.add_metric(name="OrdersProcessed", unit=MetricUnit.Count, value=1)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
```

### Cold Start Optimization

```yaml
optimization_checklist:
  - Use ARM64/Graviton (faster startup, 20% cheaper)
  - Minimize package size (< 50MB uncompressed)
  - Use Lambda Layers for shared dependencies
  - Initialize SDK clients outside handler
  - Use Provisioned Concurrency for critical paths
  - Enable SnapStart (Java/Python only)

runtime_recommendations:
  nodejs: "Node.js 22.x" # Fastest cold start
  python: "Python 3.13" # Good balance
  java: "Java 21 + SnapStart" # Required for Java
  dotnet: ".NET 8 or 10" # Native AOT for cold start
```

---

## 🗄️ DynamoDB Patterns

### Single-Table Design

```typescript
// Entity types in single table
interface TableItem {
  PK: string; // Partition key: TYPE#ID
  SK: string; // Sort key: TYPE#ID or metadata
  GSI1PK?: string; // Global Secondary Index
  GSI1SK?: string;
  data: Record<string, any>;
  ttl?: number; // Time-to-live (epoch seconds)
}

// Access patterns
const patterns = {
  // User by ID
  getUser: { PK: "USER#123", SK: "PROFILE" },

  // Orders by user
  getUserOrders: { PK: "USER#123", SK: "ORDER#" }, // begins_with

  // Order by ID (GSI)
  getOrderById: { GSI1PK: "ORDER#456", GSI1SK: "ORDER#456" },
};
```

### DynamoDB Operations

```typescript
import {
  DynamoDBDocumentClient,
  QueryCommand,
  PutCommand,
} from "@aws-sdk/lib-dynamodb";

// Query with begins_with
const orders = await docClient.send(
  new QueryCommand({
    TableName: "SingleTable",
    KeyConditionExpression: "PK = :pk AND begins_with(SK, :sk)",
    ExpressionAttributeValues: {
      ":pk": `USER#${userId}`,
      ":sk": "ORDER#",
    },
    Limit: 20,
    ScanIndexForward: false, // Newest first
  }),
);

// Conditional put (prevent overwrites)
await docClient.send(
  new PutCommand({
    TableName: "SingleTable",
    Item: {
      PK: `USER#${userId}`,
      SK: "PROFILE",
      email,
      createdAt: Date.now(),
      ttl: Math.floor(Date.now() / 1000) + 86400 * 30, // 30 days TTL
    },
    ConditionExpression: "attribute_not_exists(PK)",
  }),
);
```

---

## 📦 S3 Patterns

### Presigned URLs

```typescript
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({});

// Upload presigned URL
const uploadUrl = await getSignedUrl(
  s3,
  new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `uploads/${userId}/${filename}`,
    ContentType: "image/jpeg",
  }),
  { expiresIn: 3600 },
);

// Download presigned URL
const downloadUrl = await getSignedUrl(
  s3,
  new GetObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `uploads/${userId}/${filename}`,
  }),
  { expiresIn: 3600 },
);
```

### S3 Event Trigger

```typescript
import { S3Handler } from "aws-lambda";
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

export const handler: S3Handler = async (event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, " "));

    console.log(`Processing: s3://${bucket}/${key}`);

    // Process uploaded file
    const response = await s3.send(
      new GetObjectCommand({ Bucket: bucket, Key: key }),
    );
    const content = await response.Body?.transformToString();

    // Do something with content
  }
};
```

---

## 🔄 Event-Driven Architecture

### EventBridge + Step Functions

```typescript
import * as cdk from "aws-cdk-lib";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as sfn from "aws-cdk-lib/aws-stepfunctions";

// EventBridge rule triggers Step Functions
const rule = new events.Rule(this, "OrderRule", {
  eventPattern: {
    source: ["orders.service"],
    detailType: ["OrderPlaced"],
  },
});

rule.addTarget(
  new targets.SfnStateMachine(orderWorkflow, {
    input: events.RuleTargetInput.fromEventPath("$.detail"),
  }),
);
```

### SNS + SQS Fan-Out

```typescript
import * as sns from "aws-cdk-lib/aws-sns";
import * as sqs from "aws-cdk-lib/aws-sqs";
import * as subscriptions from "aws-cdk-lib/aws-sns-subscriptions";

// Topic
const orderTopic = new sns.Topic(this, "OrderTopic");

// Multiple queues subscribe
const inventoryQueue = new sqs.Queue(this, "InventoryQueue");
const paymentQueue = new sqs.Queue(this, "PaymentQueue");
const notificationQueue = new sqs.Queue(this, "NotificationQueue");

orderTopic.addSubscription(new subscriptions.SqsSubscription(inventoryQueue));
orderTopic.addSubscription(new subscriptions.SqsSubscription(paymentQueue));
orderTopic.addSubscription(
  new subscriptions.SqsSubscription(notificationQueue),
);
```

---

## 🏗️ Infrastructure as Code

### CDK Stack Template

```typescript
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { Construct } from "constructs";

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table
    const table = new dynamodb.Table(this, "Table", {
      partitionKey: { name: "PK", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "SK", type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      pointInTimeRecovery: true,
      timeToLiveAttribute: "ttl",
    });

    table.addGlobalSecondaryIndex({
      indexName: "GSI1",
      partitionKey: { name: "GSI1PK", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "GSI1SK", type: dynamodb.AttributeType.STRING },
    });

    // Lambda function
    const fn = new lambda.Function(this, "Handler", {
      runtime: lambda.Runtime.NODEJS_22_X,
      architecture: lambda.Architecture.ARM_64, // Graviton
      handler: "index.handler",
      code: lambda.Code.fromAsset("lambda"),
      environment: {
        TABLE_NAME: table.tableName,
        NODE_OPTIONS: "--enable-source-maps",
      },
      tracing: lambda.Tracing.ACTIVE,
      memorySize: 256,
      timeout: cdk.Duration.seconds(10),
    });

    table.grantReadWriteData(fn);

    // API Gateway
    const api = new apigateway.RestApi(this, "Api", {
      restApiName: "MyApi",
      deployOptions: {
        stageName: "prod",
        tracingEnabled: true,
        metricsEnabled: true,
      },
    });

    const items = api.root.addResource("items");
    items.addMethod("GET", new apigateway.LambdaIntegration(fn));
    items.addMethod("POST", new apigateway.LambdaIntegration(fn));
  }
}
```

### SAM Template

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Description: Serverless API

Globals:
  Function:
    Timeout: 10
    Runtime: nodejs22.x
    Architectures:
      - arm64
    Tracing: Active
    Environment:
      Variables:
        TABLE_NAME: !Ref Table

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/api.handler
      Events:
        GetItems:
          Type: Api
          Properties:
            Path: /items
            Method: get
        CreateItem:
          Type: Api
          Properties:
            Path: /items
            Method: post
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref Table
    Metadata:
      BuildMethod: esbuild
      BuildProperties:
        Minify: true
        Target: "es2022"
        Sourcemap: true

  Table:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
```

---

## 🐳 ECS/Fargate Patterns

### Fargate Service with CDK

```typescript
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ecsPatterns from "aws-cdk-lib/aws-ecs-patterns";

// Application Load Balanced Fargate Service
const service = new ecsPatterns.ApplicationLoadBalancedFargateService(
  this,
  "Service",
  {
    cluster,
    taskImageOptions: {
      image: ecs.ContainerImage.fromAsset("./app"),
      environment: {
        NODE_ENV: "production",
      },
      secrets: {
        DATABASE_URL: ecs.Secret.fromSecretsManager(dbSecret),
      },
    },
    cpu: 512,
    memoryLimitMiB: 1024,
    desiredCount: 2,
    capacityProviderStrategies: [
      { capacityProvider: "FARGATE_SPOT", weight: 2 }, // 70% cheaper
      { capacityProvider: "FARGATE", weight: 1 },
    ],
    runtimePlatform: {
      cpuArchitecture: ecs.CpuArchitecture.ARM64, // Graviton
      operatingSystemFamily: ecs.OperatingSystemFamily.LINUX,
    },
  },
);

// Auto-scaling
service.service
  .autoScaleTaskCount({
    minCapacity: 2,
    maxCapacity: 10,
  })
  .scaleOnCpuUtilization("CpuScaling", {
    targetUtilizationPercent: 70,
  });
```

---

## 🔒 Security Best Practices

### IAM Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:Query", "dynamodb:PutItem"],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/MyTable",
        "arn:aws:dynamodb:*:*:table/MyTable/index/*"
      ],
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": ["${aws:PrincipalTag/tenant_id}"]
        }
      }
    }
  ]
}
```

### Secrets Manager

```typescript
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";

const client = new SecretsManagerClient({});

// Cache secrets for Lambda reuse
let cachedSecret: Record<string, string> | null = null;

export async function getSecret(
  secretName: string,
): Promise<Record<string, string>> {
  if (cachedSecret) return cachedSecret;

  const response = await client.send(
    new GetSecretValueCommand({
      SecretId: secretName,
    }),
  );

  cachedSecret = JSON.parse(response.SecretString!);
  return cachedSecret;
}
```

---

## 💰 Cost Optimization

### Cost Checklist

```yaml
lambda:
  - [ ] Use ARM64/Graviton (20% cheaper)
  - [ ] Right-size memory (test with Power Tuner)
  - [ ] Use Provisioned Concurrency only for critical paths
  - [ ] Enable Compute Savings Plans (1-3 year)

dynamodb:
  - [ ] Use On-Demand for unpredictable traffic
  - [ ] Switch to Provisioned with Auto-scaling when stable
  - [ ] Enable TTL to auto-delete old data
  - [ ] Use DynamoDB Reserved Capacity (committed)

s3:
  - [ ] Configure lifecycle rules (Intelligent-Tiering)
  - [ ] Use S3 Glacier for archival
  - [ ] Enable compression before upload

fargate:
  - [ ] Use Fargate Spot (up to 70% discount)
  - [ ] Right-size CPU/memory (Compute Optimizer)
  - [ ] Use Graviton processors (ARM64)
  - [ ] Commit to Compute Savings Plans
```

---

## 🔧 CLI Commands

```bash
# Deploy CDK
cdk bootstrap
cdk deploy --all

# Deploy SAM
sam build
sam deploy --guided

# Lambda logs
aws logs tail /aws/lambda/MyFunction --follow

# DynamoDB query
aws dynamodb query \
  --table-name MyTable \
  --key-condition-expression "PK = :pk" \
  --expression-attribute-values '{":pk":{"S":"USER#123"}}'

# S3 sync
aws s3 sync ./dist s3://my-bucket/

# ECS update service
aws ecs update-service --cluster MyCluster --service MyService --force-new-deployment
```

---

## ✅ Production Checklist

- [ ] IAM roles follow least privilege
- [ ] Secrets in Secrets Manager / SSM Parameter Store
- [ ] CloudWatch alarms configured
- [ ] X-Ray tracing enabled
- [ ] VPC configured (if needed)
- [ ] CORS configured correctly
- [ ] Error handling with retry logic
- [ ] Dead Letter Queue (DLQ) for failed messages
- [ ] Point-in-Time Recovery enabled (DynamoDB/RDS)
- [ ] S3 versioning enabled

---

_DOMYH Agent v4.3 • AWS Development Patterns • 2025-2026_
