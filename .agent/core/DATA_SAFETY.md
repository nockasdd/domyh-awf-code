# DOMYH Awesome Code Data Safety v4.3

> Sensitive data handling based on 2025 AI data hygiene standards

## Sensitive Patterns

| Category    | Patterns                  | Action    |
| ----------- | ------------------------- | --------- |
| Credentials | password, passwd, secret  | REDACT    |
| API Keys    | api_key, apikey, token    | REDACT    |
| Crypto      | private_key, secret_key   | NEVER LOG |
| PII         | email, phone, ssn         | MASK      |
| Infra       | connection_string, db_url | WARN      |

---

## Detection Rules

```yaml
patterns:
  high_risk:
    - "password\\s*[:=]\\s*['\"]?\\w+"
    - "api[_-]?key\\s*[:=]"
    - "secret\\s*[:=]"
    - "BEGIN.*PRIVATE KEY"

  medium_risk:
    - "token\\s*[:=]"
    - "auth[_-]?header"
    - "bearer\\s+\\w+"

  low_risk:
    - "connection[_-]?string"
    - "database[_-]?url"
```

---

## Actions by Severity

### High Risk (NEVER)

- Never include in outputs
- Never log to console
- Never store in cache

### Medium Risk (REDACT)

- Replace with `[REDACTED]`
- Warn user before showing
- Exclude from file diffs

### Low Risk (WARN)

- Show warning before display
- Ask before including in reports

---

## Output Filtering

```yaml
before_output:
  - Scan for patterns
  - Apply redaction
  - Log detection (not content)

formats:
  - "[REDACTED:password]"
  - "[REDACTED:api_key]"
  - "***"
```

---

## Safe Practices

### DO

- Use environment variable references
- Suggest .env patterns
- Recommend secrets managers

### DON'T

- Echo secrets in commands
- Include keys in code examples
- Store credentials in cache

---

_DOMYH Awesome Code v4.3 — Data Safety Rules_
