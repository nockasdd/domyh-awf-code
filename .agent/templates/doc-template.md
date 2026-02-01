---
name: doc-template
version: "4.3.0"
type: wizard
triggers: ["/doc", "/generate"]
---

# Documentation Template

## {FEATURE_NAME}

### Overview

{DESCRIPTION}

### Usage

```{LANG}
{USAGE_EXAMPLE}
```

### Parameters

| Name      | Type     | Required | Description |
| --------- | -------- | -------- | ----------- |
| {PARAM_1} | {TYPE_1} | Yes/No   | {DESC_1}    |
| {PARAM_2} | {TYPE_2} | Yes/No   | {DESC_2}    |

### Returns

- **Success:** {SUCCESS_RESPONSE}
- **Error:** {ERROR_RESPONSE}

### Examples

#### Basic Usage

```{LANG}
{EXAMPLE_1}
```

#### Advanced Usage

```{LANG}
{EXAMPLE_2}
```

### Errors

| Code    | Meaning | Solution |
| ------- | ------- | -------- |
| {ERR_1} | {MSG_1} | {FIX_1}  |
| {ERR_2} | {MSG_2} | {FIX_2}  |

---

_DOMYH Agent v4.2_
