---
library: terraform
version: "1.14"
latest: true
category: infra
official_docs: https://developer.hashicorp.com/terraform
last_updated: 2026-03-21
last_checked: 2026-03-21
source: ai-enhanced from hashicorp.com + web research
---

# Terraform v1.14

> Terraform — Infrastructure as Code tool for building, changing, and versioning infrastructure safely.
> Current: v1.14.7 (Mar 2026) | Previous: v1.11 (Feb 2025)
> Docs: https://developer.hashicorp.com/terraform

## Version Comparison

| Feature | v1.10 | v1.11 | v1.14 |
|:--------|:------|:------|:------|
| Ephemeral resources | ✅ New | ✅ | ✅ |
| Write-only arguments | ❌ | ✅ New | ✅ |
| `ephemeralasnull` function | ✅ | ✅ | ✅ |
| S3 conditional writes (no DynamoDB) | ❌ | ✅ | ✅ |
| `terraform modules -json` | ❌ | ✅ | ✅ |
| Test `state_key` attribute | ❌ | ✅ | ✅ |
| Negative indices in `element()` | ✅ | ✅ | ✅ |
| `-state` flag | ⚠️ Deprecated | ⚠️ | ⚠️ |

## Installation

```bash
# macOS (Homebrew)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Linux (apt)
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Windows (winget)
winget install Hashicorp.Terraform

# Docker
docker run --rm -v $(pwd):/workspace hashicorp/terraform:1.14 init

# Version manager (tfenv)
brew install tfenv
tfenv install 1.14.7
tfenv use 1.14.7

# Verify
terraform version
```

## Configuration

```hcl
# main.tf — Provider & backend configuration
terraform {
  required_version = ">= 1.14.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # S3 backend (v1.11+: conditional writes, no DynamoDB needed)
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    use_lockfile   = true  # v1.11+ S3 conditional writes
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

## Core API (HCL)

### Variables & Outputs

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}

variable "instance_count" {
  type    = number
  default = 2
}

variable "tags" {
  type = map(string)
  default = {
    Project = "demo"
  }
}

# Sensitive variable
variable "db_password" {
  type      = string
  sensitive = true
}

# outputs.tf
output "instance_ips" {
  description = "Public IPs of instances"
  value       = aws_instance.web[*].public_ip
}

output "db_endpoint" {
  value     = aws_rds_cluster.main.endpoint
  sensitive = true
}
```

### Resources & Data Sources

```hcl
# Resources — managed infrastructure
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = merge(var.tags, {
    Name = "web-${count.index + 1}"
  })

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = var.environment == "prod"
    ignore_changes        = [tags["UpdatedAt"]]
  }
}

# Data sources — read existing infrastructure
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Dynamic blocks
resource "aws_security_group" "web" {
  name = "web-sg"

  dynamic "ingress" {
    for_each = [80, 443]
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

### Ephemeral Resources (v1.10+)

```hcl
# Ephemeral resources — temporary data NOT stored in state
ephemeral "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

# Use ephemeral values — never persisted
resource "aws_rds_cluster" "main" {
  master_password = ephemeral.aws_secretsmanager_secret_version.db_password.secret_string
}

# Ephemeral variables
variable "api_token" {
  type      = string
  ephemeral = true  # not stored in state or plan
}

# Write-only arguments (v1.11+) — passed to provider, not stored
resource "aws_db_instance" "main" {
  engine         = "postgres"
  instance_class = "db.t3.micro"

  password = var.db_password  # write-only: provider receives it but never stores
}
```

### Modules

```hcl
# modules/vpc/main.tf
variable "cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
  tags       = { Name = "main-vpc" }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

# Root module — calling child module
module "vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.1.0.0/16"
}

# Registry module
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "my-cluster"
  cluster_version = "1.31"
  vpc_id          = module.vpc.vpc_id
}
```

### Loops & Conditionals

```hcl
# for_each (preferred over count for named resources)
resource "aws_iam_user" "team" {
  for_each = toset(["alice", "bob", "charlie"])
  name     = each.key
}

# Conditional resource creation
resource "aws_cloudwatch_alarm" "high_cpu" {
  count = var.environment == "prod" ? 1 : 0
  # ... alarm config
}

# for expressions
locals {
  upper_names = [for name in var.names : upper(name)]
  name_map    = { for name in var.names : name => upper(name) }
  filtered    = [for s in var.subnets : s if s.public]
}

# Negative index (v1.10+)
element(var.list, -1)  # last element
```

### Testing (v1.6+)

```hcl
# tests/vpc.tftest.hcl
run "create_vpc" {
  command = plan

  # v1.11+: state_key for isolated test state
  state_key = "vpc_test"

  variables {
    cidr_block = "10.99.0.0/16"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.99.0.0/16"
    error_message = "VPC CIDR mismatch"
  }
}

# Run tests
# terraform test
# terraform test -filter=tests/vpc.tftest.hcl
```

## Common Patterns

```hcl
# 1. Environment-specific config with workspaces
# terraform workspace new staging
# terraform workspace select prod
locals {
  env_config = {
    dev     = { instance_type = "t3.micro",  count = 1 }
    staging = { instance_type = "t3.small",  count = 2 }
    prod    = { instance_type = "t3.medium", count = 3 }
  }
  config = local.env_config[terraform.workspace]
}

# 2. State import
import {
  to = aws_instance.legacy
  id = "i-0123456789abcdef0"
}
# Then: terraform plan -generate-config-out=generated.tf

# 3. Moved blocks (refactoring without destroy)
moved {
  from = aws_instance.web
  to   = module.compute.aws_instance.web
}

# 4. Preconditions & Postconditions
resource "aws_instance" "web" {
  instance_type = var.instance_type

  lifecycle {
    precondition {
      condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
      error_message = "Only t3 instances allowed."
    }
    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have public IP."
    }
  }
}

# 5. CI/CD workflow
# terraform init -backend-config=prod.hcl
# terraform plan -out=tfplan
# terraform show -json tfplan > plan.json
# terraform apply tfplan
```

## Gotchas & Breaking Changes

### General Gotchas

- ⚠️ **State file is sensitive**: Contains ALL resource data including secrets. Encrypt at rest, restrict access.
- ⚠️ **`count` vs `for_each`**: `count` uses index — removing middle item shifts all subsequent. Use `for_each` with map/set.
- ⚠️ **Provider version drift**: Always pin provider versions (`~> 5.0`). Unpinned = potential breaking changes.
- ⚠️ **Circular dependencies**: Terraform can't resolve cycles. Use `depends_on` sparingly.
- ⚠️ **`terraform destroy` is IRREVERSIBLE**: No undo. Always `plan -destroy` first.
- ⚠️ **Remote state concurrency**: Without locking, parallel applies corrupt state. Always enable state locking.
- ⚠️ **HCL is NOT a programming language**: Don't force complex loops/conditionals — use modules instead.
- ⚠️ **`terraform.workspace` in modules**: Workspace name available but can cause unexpected behavior — prefer variables.
- ⚠️ **`-target` is for emergencies only**: Targeted applies skip dependency graph — state can drift.

### v1.11 Breaking Changes
- ⚠️ **S3 backend changes**: Conditional writes enabled by default — may affect custom locking implementations.
- ⚠️ **AzureRM storage backend**: Some breaking changes reported — test before upgrading.

### v1.10 Breaking Changes
- ⚠️ **`-state` flag deprecated**: Will be removed in future version. Migrate to backend config.

## Migration

### From Terraform 1.9 → 1.10
1. Review and adopt ephemeral resources for secrets
2. Update to Python-style negative indices in `element()`
3. Address `-state` flag deprecation warnings

### From Terraform 1.10 → 1.11+
1. Adopt write-only arguments for sensitive resource properties
2. Migrate S3 backend to use `use_lockfile = true` (drop DynamoDB)
3. Use `state_key` in test runs for isolated state
4. Pin version: `required_version = ">= 1.11.0"`

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio ≥ 70:30
- Keep 5-30KB per file
-->
