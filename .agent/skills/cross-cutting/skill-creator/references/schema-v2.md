# META.yaml v2 Schema Reference

## Required Fields

| Field      | Type   | Max Length | Description                                                                |
| ---------- | ------ | ---------- | -------------------------------------------------------------------------- |
| `name`     | string | 30 chars   | Lowercase, hyphen-separated identifier                                     |
| `version`  | string | -          | Semver string (e.g., "6.4.2")                                              |
| `category` | enum   | -          | One of: core, languages, frameworks, cross-cutting, devops, tooling, ai-ml |
| `desc`     | string | 80 chars   | Short description for listings                                             |

## Recommended Fields

| Field                    | Type   | Max Length | Description                                |
| ------------------------ | ------ | ---------- | ------------------------------------------ |
| `display`                | string | 50 chars   | Human-readable display name                |
| `tier`                   | int    | -          | 1=core, 2=standard, 3=specialized          |
| `priority`               | int    | -          | 0-6 (lower = higher priority)              |
| `trigger_desc`           | string | 1024 chars | Rich semantic description for HSA matching |
| `triggers.file_patterns` | list   | -          | File globs for auto-detection              |
| `triggers.keywords`      | list   | 30 items   | Keywords for BM25 matching                 |
| `triggers.intents`       | list   | 10 items   | User intent descriptions                   |
| `caps`                   | list   | 6 items    | Capability descriptions                    |
| `compatibility`          | string | 100 chars  | Environment requirements                   |

## Optional Fields

| Field                    | Type | Description                        |
| ------------------------ | ---- | ---------------------------------- |
| `related_skills`         | list | Other skills to cross-reference    |
| `prevent_confusion_with` | map  | Disambiguation from similar skills |
| `data_files`             | list | Paths to data/ YAML files          |
| `patterns.total`         | int  | Total pattern count                |
| `patterns.domains`       | map  | Domain breakdown                   |

## Validation Rules

1. `name` must be unique across all skills
2. `desc` must not exceed 80 characters
3. `trigger_desc` must not exceed 1024 characters
4. `triggers.keywords` should have 5-30 items
5. `caps` should have 3-6 items
6. `compatibility` should specify minimum versions
7. File patterns must use standard glob syntax
