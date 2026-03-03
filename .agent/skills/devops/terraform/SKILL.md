---
name: terraform
description: "Terraform IaC patterns for cloud infrastructure. Use when working with .tf files or managing cloud resources."
category: devops
---

# Terraform IaC

> HCL • Modules • Remote State • Multi-cloud

---

## Khi Nào Dùng

- Quản lý infrastructure bằng code
- Multi-cloud provisioning (AWS, GCP, Azure)
- Reproducible environments (dev/staging/prod)

## Core Patterns

### Module Design

```hcl
# modules/vpc/main.tf
variable "cidr_block" { type = string }
resource "aws_vpc" "main" { cidr_block = var.cidr_block }
output "vpc_id" { value = aws_vpc.main.id }

# Usage
module "vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}
```

### Remote State

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Workspace Strategy

```bash
terraform workspace new staging
terraform workspace select prod
terraform plan -var-file=envs/prod.tfvars
```

## CI/CD Pipeline

```
1. terraform fmt -check     # Format check
2. terraform validate       # Syntax validation
3. terraform plan -out=plan # Preview changes
4. APPROVAL GATE            # Manual approval
5. terraform apply plan     # Apply approved plan
```

## Common Traps

| Trap              | Fix                                       |
| ----------------- | ----------------------------------------- |
| State conflicts   | Remote backend + DynamoDB locking         |
| Drift detection   | Regular `terraform plan` in CI            |
| Secret exposure   | Use `sensitive = true`, vault integration |
| Large state files | Split into modules, use workspaces        |

---
