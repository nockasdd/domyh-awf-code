# Terraform — Advanced Patterns

## Table of Contents

- [Module Design](#module-design)
- [State Management](#state-management)
- [Workspaces & Environments](#workspaces--environments)
- [Import & Moved Blocks](#import--moved-blocks)
- [Testing](#testing)

---

## Module Design

### Composable Module

```hcl
# modules/service/main.tf
variable "name" { type = string }
variable "image" { type = string }
variable "port" { type = number, default = 3000 }
variable "env" { type = map(string), default = {} }
variable "replicas" { type = number, default = 2 }
variable "cpu" { type = string, default = "256" }
variable "memory" { type = string, default = "512" }

resource "aws_ecs_service" "this" {
  name            = var.name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = var.replicas

  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [aws_security_group.this.id]
  }
}

resource "aws_ecs_task_definition" "this" {
  family                   = var.name
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory

  container_definitions = jsonencode([{
    name      = var.name
    image     = var.image
    essential = true
    portMappings = [{ containerPort = var.port }]
    environment = [for k, v in var.env : { name = k, value = v }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"  = "/ecs/${var.name}"
        "awslogs-region" = data.aws_region.current.name
      }
    }
  }])
}

output "service_url" { value = aws_lb.this.dns_name }
```

### Module Usage

```hcl
module "api" {
  source   = "./modules/service"
  name     = "api"
  image    = "ghcr.io/myorg/api:${var.api_version}"
  port     = 8080
  replicas = var.environment == "prod" ? 3 : 1
  env = {
    DATABASE_URL = module.database.connection_string
    REDIS_URL    = module.cache.endpoint
  }
}
```

---

## State Management

```yaml
backends:
  s3:
    config: |
      backend "s3" {
        bucket         = "myorg-terraform-state"
        key            = "services/api/terraform.tfstate"
        region         = "ap-southeast-1"
        dynamodb_table = "terraform-locks"
        encrypt        = true
      }
    best_practices:
      - "Enable versioning on S3 bucket"
      - "Use DynamoDB for state locking"
      - "One state file per service/environment"

  state_commands:
    - "terraform state list                    # List all resources"
    - "terraform state show aws_instance.web   # Show resource details"
    - "terraform state mv old.name new.name    # Rename without destroy"
    - "terraform state rm aws_instance.old     # Remove from state (keep resource)"
    - "terraform state pull > backup.tfstate   # Backup state"
```

---

## Workspaces & Environments

```hcl
# environments/prod/main.tf
module "infra" {
  source = "../../modules/infra"

  environment = "prod"
  region      = "ap-southeast-1"
  vpc_cidr    = "10.0.0.0/16"
}

# terraform.tfvars per environment
# environments/prod/terraform.tfvars
environment    = "prod"
instance_type  = "t3.large"
min_instances  = 3
max_instances  = 10
```

```yaml
workspace_strategy:
  option_a: "Directory-based (recommended)"
  structure: |
    environments/
      dev/
        main.tf
        terraform.tfvars
      staging/
        main.tf
        terraform.tfvars
      prod/
        main.tf
        terraform.tfvars
    modules/
      service/
      database/
      network/
```

---

## Import & Moved Blocks

```hcl
# Import existing resources (Terraform 1.5+)
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket"
}

# Refactor without destroy (Terraform 1.1+)
moved {
  from = aws_instance.web
  to   = module.compute.aws_instance.web
}

moved {
  from = module.old_name
  to   = module.new_name
}
```

---

## Testing

```hcl
# tests/service.tftest.hcl (Terraform 1.6+)
run "plan_service" {
  command = plan

  variables {
    name     = "test-api"
    image    = "nginx:latest"
    replicas = 1
  }

  assert {
    condition     = aws_ecs_service.this.desired_count == 1
    error_message = "Replica count should be 1"
  }
}

run "apply_service" {
  command = apply

  assert {
    condition     = output.service_url != ""
    error_message = "Service URL should not be empty"
  }
}
```

---
