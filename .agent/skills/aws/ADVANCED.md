# AWS — Advanced Patterns

# DOMYH Awesome Code v4.3 — Tier 3 Reference

## Table of Contents

- [Step Functions Workflows](#step-functions-workflows)
- [Multi-Region & Disaster Recovery](#multi-region--disaster-recovery)
- [Advanced DynamoDB](#advanced-dynamodb)
- [Observability & Monitoring](#observability--monitoring)
- [Advanced Security](#advanced-security)
- [Performance Optimization](#performance-optimization)

---

## Step Functions Workflows

### Order Processing Workflow (CDK)

```typescript
import * as sfn from "aws-cdk-lib/aws-stepfunctions";
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";

// Validate order
const validateOrder = new tasks.LambdaInvoke(this, "ValidateOrder", {
  lambdaFunction: validateFn,
  outputPath: "$.Payload",
});

// Process payment
const processPayment = new tasks.LambdaInvoke(this, "ProcessPayment", {
  lambdaFunction: paymentFn,
  outputPath: "$.Payload",
});

// Reserve inventory
const reserveInventory = new tasks.LambdaInvoke(this, "ReserveInventory", {
  lambdaFunction: inventoryFn,
  outputPath: "$.Payload",
});

// Send notification
const sendConfirmation = new tasks.SqsSendMessage(this, "SendConfirmation", {
  queue: notificationQueue,
  messageBody: sfn.TaskInput.fromJsonPathAt("$"),
});

// Error handling
const handleError = new tasks.SnsPublish(this, "NotifyError", {
  topic: errorTopic,
  message: sfn.TaskInput.fromJsonPathAt("$.error"),
});

// Parallel execution
const parallel = new sfn.Parallel(this, "ProcessParallel")
  .branch(processPayment)
  .branch(reserveInventory);

// State machine
const definition = validateOrder
  .next(
    new sfn.Choice(this, "IsValid?")
      .when(sfn.Condition.booleanEquals("$.isValid", true), parallel)
      .otherwise(handleError),
  )
  .next(sendConfirmation);

const stateMachine = new sfn.StateMachine(this, "OrderWorkflow", {
  definition,
  timeout: cdk.Duration.minutes(5),
  tracingEnabled: true,
});
```

### Wait for Callback Pattern

```typescript
// Wait for external system callback
const waitForApproval = new sfn.CustomState(this, "WaitForApproval", {
  stateJson: {
    Type: "Task",
    Resource: "arn:aws:states:::lambda:invoke.waitForTaskToken",
    Parameters: {
      FunctionName: approvalFn.functionArn,
      Payload: {
        "orderId.$": "$.orderId",
        "taskToken.$": "$$.Task.Token",
      },
    },
    HeartbeatSeconds: 3600,
    TimeoutSeconds: 86400, // 24 hours
  },
});

// External callback (from approval system)
// await sfnClient.send(new SendTaskSuccessCommand({
//   taskToken: token,
//   output: JSON.stringify({ approved: true })
// }));
```

---

## Multi-Region & Disaster Recovery

### DynamoDB Global Tables

```typescript
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

const globalTable = new dynamodb.TableV2(this, "GlobalTable", {
  partitionKey: { name: "PK", type: dynamodb.AttributeType.STRING },
  sortKey: { name: "SK", type: dynamodb.AttributeType.STRING },
  billing: dynamodb.Billing.onDemand(),
  replicas: [{ region: "us-west-2" }, { region: "eu-west-1" }],
  globalSecondaryIndexes: [
    {
      indexName: "GSI1",
      partitionKey: { name: "GSI1PK", type: dynamodb.AttributeType.STRING },
    },
  ],
});
```

### Cross-Region S3 Replication

```typescript
import * as s3 from "aws-cdk-lib/aws-s3";

const sourceBucket = new s3.Bucket(this, "SourceBucket", {
  versioned: true, // Required for replication
  encryption: s3.BucketEncryption.S3_MANAGED,
});

// In destination region stack
const destBucket = new s3.Bucket(destStack, "DestBucket", {
  versioned: true,
  encryption: s3.BucketEncryption.S3_MANAGED,
});

// Configure replication in source bucket
sourceBucket.addReplicationRule({
  destination: {
    bucket: destBucket.bucketArn,
    storageClass: s3.StorageClass.STANDARD_IA,
  },
  priority: 1,
});
```

### Route 53 Health Checks

```typescript
import * as route53 from "aws-cdk-lib/aws-route53";

const healthCheck = new route53.CfnHealthCheck(this, "ApiHealthCheck", {
  healthCheckConfig: {
    type: "HTTPS",
    fullyQualifiedDomainName: "api.example.com",
    resourcePath: "/health",
    requestInterval: 30,
    failureThreshold: 3,
  },
});

// Failover routing
new route53.CfnRecordSet(this, "FailoverRecord", {
  hostedZoneId: zone.hostedZoneId,
  name: "api.example.com",
  type: "A",
  setIdentifier: "primary",
  failover: "PRIMARY",
  healthCheckId: healthCheck.ref,
  aliasTarget: {
    dnsName: primaryAlb.loadBalancerDnsName,
    hostedZoneId: primaryAlb.loadBalancerCanonicalHostedZoneId,
  },
});
```

---

## Advanced DynamoDB

### Transaction Patterns

```typescript
import {
  TransactWriteCommand,
  TransactGetCommand,
} from "@aws-sdk/lib-dynamodb";

// Atomic transaction (all or nothing)
await docClient.send(
  new TransactWriteCommand({
    TransactItems: [
      {
        Put: {
          TableName: "SingleTable",
          Item: {
            PK: `ORDER#${orderId}`,
            SK: "ORDER",
            status: "CONFIRMED",
            total: orderTotal,
          },
          ConditionExpression: "attribute_not_exists(PK)",
        },
      },
      {
        Update: {
          TableName: "SingleTable",
          Key: { PK: `USER#${userId}`, SK: "STATS" },
          UpdateExpression: "ADD orderCount :inc, totalSpent :total",
          ExpressionAttributeValues: {
            ":inc": 1,
            ":total": orderTotal,
          },
        },
      },
      {
        Update: {
          TableName: "SingleTable",
          Key: { PK: `INVENTORY#${productId}`, SK: "STOCK" },
          UpdateExpression: "SET quantity = quantity - :qty",
          ConditionExpression: "quantity >= :qty",
          ExpressionAttributeValues: { ":qty": orderQty },
        },
      },
    ],
  }),
);
```

### DynamoDB Streams + Lambda

```typescript
import { DynamoDBStreamHandler } from "aws-lambda";
import { unmarshall } from "@aws-sdk/util-dynamodb";

export const handler: DynamoDBStreamHandler = async (event) => {
  for (const record of event.Records) {
    if (record.eventName === "INSERT" || record.eventName === "MODIFY") {
      const newItem = unmarshall(record.dynamodb!.NewImage!);

      // Aggregate, project, or sync to other systems
      if (newItem.PK.startsWith("ORDER#") && newItem.status === "SHIPPED") {
        await sendShippingNotification(newItem);
      }
    }
  }
};
```

### PartiQL for Complex Queries

```typescript
import { ExecuteStatementCommand } from "@aws-sdk/lib-dynamodb";

// Query with PartiQL
const result = await docClient.send(
  new ExecuteStatementCommand({
    Statement: `
    SELECT * FROM "SingleTable"
    WHERE PK = 'USER#123'
    AND begins_with(SK, 'ORDER#')
  `,
    Limit: 20,
  }),
);

// Batch operations with PartiQL
await docClient.send(
  new BatchExecuteStatementCommand({
    Statements: [
      {
        Statement:
          "UPDATE SingleTable SET status = 'ARCHIVED' WHERE PK = 'ORDER#1' AND SK = 'ORDER'",
      },
      {
        Statement:
          "UPDATE SingleTable SET status = 'ARCHIVED' WHERE PK = 'ORDER#2' AND SK = 'ORDER'",
      },
    ],
  }),
);
```

---

## Observability & Monitoring

### Lambda Powertools Complete Setup

```python
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer, idempotent
)

logger = Logger()
tracer = Tracer()
metrics = Metrics()
processor = BatchProcessor(event_type=EventType.SQS)

# Idempotency for exactly-once processing
persistence_layer = DynamoDBPersistenceLayer(table_name="IdempotencyTable")

@tracer.capture_method
def process_record(record: dict):
    """Process a single SQS record."""
    body = json.loads(record["body"])
    logger.info("Processing order", order_id=body["order_id"])

    with tracer.create_segment("business_logic"):
        result = process_order(body)

    metrics.add_metric("OrderProcessed", unit=MetricUnit.Count, value=1)
    return result

@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
@idempotent(persistence_store=persistence_layer)
def handler(event: dict, context):
    return processor.process(event, record_handler=process_record)
```

### CloudWatch Alarms with CDK

```typescript
import * as cloudwatch from "aws-cdk-lib/aws-cloudwatch";
import * as actions from "aws-cdk-lib/aws-cloudwatch-actions";

// Lambda error alarm
const errorAlarm = new cloudwatch.Alarm(this, "LambdaErrors", {
  metric: fn.metricErrors({
    period: cdk.Duration.minutes(5),
  }),
  threshold: 5,
  evaluationPeriods: 2,
  comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
  treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
});

errorAlarm.addAlarmAction(new actions.SnsAction(alertTopic));

// DynamoDB throttling alarm
const throttleAlarm = new cloudwatch.Alarm(this, "DynamoThrottle", {
  metric: table.metricThrottledRequestsForOperations({
    operations: [dynamodb.Operation.GET_ITEM, dynamodb.Operation.QUERY],
    period: cdk.Duration.minutes(1),
  }),
  threshold: 10,
  evaluationPeriods: 3,
});

// Dashboard
new cloudwatch.Dashboard(this, "AppDashboard", {
  widgets: [
    [
      new cloudwatch.GraphWidget({
        title: "Lambda Invocations",
        left: [fn.metricInvocations()],
        right: [fn.metricErrors()],
      }),
      new cloudwatch.GraphWidget({
        title: "DynamoDB",
        left: [table.metricConsumedReadCapacityUnits()],
        right: [table.metricConsumedWriteCapacityUnits()],
      }),
    ],
  ],
});
```

---

## Advanced Security

### VPC Lambda with NAT Gateway

```typescript
import * as ec2 from "aws-cdk-lib/aws-ec2";

const vpc = new ec2.Vpc(this, "Vpc", {
  maxAzs: 2,
  natGateways: 1,
  subnetConfiguration: [
    {
      name: "Private",
      subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      cidrMask: 24,
    },
    {
      name: "Public",
      subnetType: ec2.SubnetType.PUBLIC,
      cidrMask: 24,
    },
  ],
});

// Lambda in VPC
const fn = new lambda.Function(this, "VpcLambda", {
  runtime: lambda.Runtime.NODEJS_22_X,
  handler: "index.handler",
  code: lambda.Code.fromAsset("lambda"),
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
});

// VPC endpoints for AWS services (avoid NAT charges)
vpc.addInterfaceEndpoint("SecretsManager", {
  service: ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
});

vpc.addGatewayEndpoint("DynamoDB", {
  service: ec2.GatewayVpcEndpointAwsService.DYNAMODB,
});
```

### API Gateway with WAF

```typescript
import * as wafv2 from "aws-cdk-lib/aws-wafv2";

const webAcl = new wafv2.CfnWebACL(this, "WebAcl", {
  scope: "REGIONAL",
  defaultAction: { allow: {} },
  rules: [
    {
      name: "RateLimitRule",
      priority: 1,
      statement: {
        rateBasedStatement: {
          limit: 2000,
          aggregateKeyType: "IP",
        },
      },
      action: { block: {} },
      visibilityConfig: {
        sampledRequestsEnabled: true,
        cloudWatchMetricsEnabled: true,
        metricName: "RateLimitRule",
      },
    },
    {
      name: "AWSManagedRulesCommonRuleSet",
      priority: 2,
      overrideAction: { none: {} },
      statement: {
        managedRuleGroupStatement: {
          vendorName: "AWS",
          name: "AWSManagedRulesCommonRuleSet",
        },
      },
      visibilityConfig: {
        sampledRequestsEnabled: true,
        cloudWatchMetricsEnabled: true,
        metricName: "CommonRuleSet",
      },
    },
  ],
  visibilityConfig: {
    sampledRequestsEnabled: true,
    cloudWatchMetricsEnabled: true,
    metricName: "WebAcl",
  },
});

// Associate with API Gateway
new wafv2.CfnWebACLAssociation(this, "WebAclAssociation", {
  resourceArn: api.deploymentStage.stageArn,
  webAclArn: webAcl.attrArn,
});
```

---

## Performance Optimization

### Lambda Power Tuning

```yaml
# Deploy AWS Lambda Power Tuning (SAM)
# aws serverlessrepo deploy --application-id arn:aws:serverlessrepo:us-east-1:451282441545:applications/aws-lambda-power-tuning

# Run tuning
{
  "lambdaARN": "arn:aws:lambda:us-east-1:123456789:function:MyFunction",
  "powerValues": [128, 256, 512, 1024, 1536, 2048],
  "num": 50,
  "payload": "{}",
  "parallelInvocation": true,
  "strategy": "cost", # or "speed" or "balanced"
}
```

### DynamoDB DAX (Caching)

```typescript
import * as dax from "@aws-cdk/aws-dax";

const daxCluster = new dax.CfnCluster(this, "DaxCluster", {
  clusterName: "my-dax-cluster",
  nodeType: "dax.r5.large",
  replicationFactor: 2,
  iamRoleArn: daxRole.roleArn,
  subnetGroupName: daxSubnetGroup.ref,
  securityGroupIds: [daxSecurityGroup.securityGroupId],
});

// Client-side: use DAX client instead of DynamoDB client
// const dax = require('amazon-dax-client');
// const client = new dax.AmazonDaxClient({ endpoints: ['dax.xxx.clusters.us-east-1.amazonaws.com:8111'] });
```

### Provisioned Concurrency

```typescript
const version = fn.currentVersion;

new lambda.Alias(this, "ProdAlias", {
  aliasName: "prod",
  version,
  provisionedConcurrentExecutions: 10, // Always warm
});

// Auto-scaling provisioned concurrency
const target = new appscaling.ScalableTarget(this, "ScalableTarget", {
  serviceNamespace: appscaling.ServiceNamespace.LAMBDA,
  resourceId: `function:${fn.functionName}:prod`,
  scalableDimension: "lambda:function:ProvisionedConcurrency",
  minCapacity: 5,
  maxCapacity: 50,
});

target.scaleToTrackMetric("UtilizationScaling", {
  targetValue: 0.7,
  predefinedMetric:
    appscaling.PredefinedMetric.LAMBDA_PROVISIONED_CONCURRENCY_UTILIZATION,
});
```

---

_DOMYH Awesome Code v4.3 — AWS Advanced Patterns_
