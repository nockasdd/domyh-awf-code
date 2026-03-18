# AWS — Advanced Patterns

## Table of Contents

- [CDK (Infrastructure as Code)](#cdk-infrastructure-as-code)
- [Lambda Advanced](#lambda-advanced)
- [ECS/Fargate Patterns](#ecsfargate-patterns)
- [Cost Optimization](#cost-optimization)

---

## CDK (Infrastructure as Code)

### Stack Composition

```typescript
// lib/api-stack.ts
export class ApiStack extends cdk.Stack {
  public readonly api: apigw.RestApi

  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props)

    const fn = new lambda.Function(this, 'Handler', {
      runtime: lambda.Runtime.PROVIDED_AL2023,
      handler: 'bootstrap',
      code: lambda.Code.fromAsset('api/dist'),
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      environment: {
        TABLE_NAME: props.table.tableName,
        STAGE: props.stage,
      },
      tracing: lambda.Tracing.ACTIVE,
    })

    props.table.grantReadWriteData(fn)

    this.api = new apigw.RestApi(this, 'Api', {
      restApiName: `${props.stage}-api`,
      deployOptions: { stageName: props.stage },
    })

    this.api.root.addProxy({
      defaultIntegration: new apigw.LambdaIntegration(fn),
    })
  }
}

// bin/app.ts
const app = new cdk.App()
const stage = app.node.tryGetContext('stage') || 'dev'

const db = new DatabaseStack(app, `${stage}-db`, { stage })
new ApiStack(app, `${stage}-api`, { stage, table: db.table })
```

---

## Lambda Advanced

### Powertools (Structured Logging + Tracing)

```go
// Go Lambda with Powertools
func handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
    logger := log.With("requestId", event.RequestContext.RequestID)

    // Cold start optimization: init outside handler
    user, err := getUser(ctx, event.PathParameters["id"])
    if err != nil {
        logger.Error("failed to get user", "error", err)
        return response(404, `{"error":"not found"}`), nil
    }

    return response(200, marshal(user)), nil
}

// Performance tips
var (
    db   *dynamodb.Client  // Reused across invocations
    once sync.Once
)

func init() {
    cfg, _ := config.LoadDefaultConfig(context.Background())
    db = dynamodb.NewFromConfig(cfg)
}
```

```yaml
lambda_best_practices:
  - "ARM64 (Graviton): 20% cheaper, often faster"
  - "Provisioned concurrency for latency-sensitive"
  - "Lambda Layers for shared dependencies"
  - "SnapStart (Java) for cold start reduction"
  - "Power tuning: aws-lambda-power-tuning"
  - "Minimum memory: 128MB, sweet spot often 256-512MB"
```

---

## ECS/Fargate Patterns

```yaml
architecture:
  service_connect:
    description: "Service mesh built into ECS"
    benefit: "No sidecar management, automatic service discovery"

  capacity_provider:
    fargate:
      use_when: "Variable workloads, no server management"
      spot: "70% cheaper, for fault-tolerant workloads"
    ec2:
      use_when: "GPU, high IO, cost optimization at scale"

  auto_scaling:
    target_tracking:
      cpu: 70
      memory: 80
    step_scaling:
      - { threshold: 90, adjustment: "+3" }
      - { threshold: 50, adjustment: "-1" }
    scale_to_zero:
      tool: "KEDA with SQS/EventBridge trigger"
```

---

## Cost Optimization

```yaml
strategies:
  compute:
    - "Use Spot instances (up to 90% savings)"
    - "Right-size with Compute Optimizer"
    - "Graviton (ARM): 20% cost reduction"
    - "Savings Plans: 1-3 year commitments"

  storage:
    - "S3 Intelligent-Tiering (auto-optimize)"
    - "EBS gp3 over gp2 (20% cheaper)"
    - "Lifecycle policies for old data"

  database:
    - "Aurora Serverless v2 for variable workloads"
    - "Reserved instances for stable workloads"
    - "DynamoDB on-demand for unpredictable traffic"

  monitoring:
    - "AWS Cost Explorer + Budgets"
    - "Tag everything: team, project, environment"
    - "Monthly cost review ritual"
```

---
