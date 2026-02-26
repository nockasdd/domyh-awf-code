---
name: migrate-plan
type: plan
triggers: ["/migrate"]
---

# Migration Plan Template

## {MIGRATION_NAME}

### Overview

| Field    | Value        |
| -------- | ------------ |
| Type     | {TYPE}       |
| Risk     | {RISK_LEVEL} |
| Downtime | {DOWNTIME}   |

### Pre-migration

- [ ] Backup database
- [ ] Test in staging
- [ ] Notify users
- [ ] Prepare rollback

### Steps

| #   | Step     | Command   | Verify    |
| --- | -------- | --------- | --------- |
| 1   | {STEP_1} | `{CMD_1}` | {CHECK_1} |
| 2   | {STEP_2} | `{CMD_2}` | {CHECK_2} |
| 3   | {STEP_3} | `{CMD_3}` | {CHECK_3} |

### Rollback

```bash
{ROLLBACK_CMD}
```

### Post-migration

- [ ] Verify data integrity
- [ ] Run health checks
- [ ] Monitor for issues
- [ ] Update documentation

---
