# DOMYH Awesome Code Audit Policy v6.2.4

> Logging and accountability based on 2025 AI governance standards

## What to Log

| Category | Events                                  | Retention |
| -------- | --------------------------------------- | --------- |
| Critical | Permission escalations, destructive ops | 90 days   |
| High     | File modifications, deploys             | 30 days   |
| Medium   | Command executions                      | 7 days    |
| Low      | Read operations                         | Session   |

---

## Log Format

```json
{
  "timestamp": "ISO8601",
  "action": "action_type",
  "target": "file/resource",
  "result": "success/fail",
  "user_approved": true/false,
  "session_id": "uuid"
}
```

---

## Required Logging

### Always Log

- File deletions
- Production commands
- Permission denials
- Error loops (3+)
- User confirmations

### Never Log

- Sensitive data content
- API keys/secrets
- PII

---

## Audit Trail Requirements

1. **Immutable** — No modification of logs
2. **Complete** — All state-changing operations
3. **Searchable** — By session, action, time
4. **Exportable** — JSON format

---

## Compliance Mapping

| Standard    | Requirements      | Status |
| ----------- | ----------------- | ------ |
| EU AI Act   | Transparency logs | ✅     |
| NIST AI RMF | Decision trail    | ✅     |
| ISO 27001   | Access logs       | ✅     |

---

_DOMYH Awesome Code — Audit Policy_
