---
name: deploy-plan
version: "6.2.7"
type: plan
triggers: ["/deploy"]
---

# Deploy Plan Template

## {PROJECT_NAME} → {ENVIRONMENT}

### Pre-checks

- [ ] Tests passing
- [ ] Build successful
- [ ] Env vars configured
- [ ] Rollback ready

### Steps

| #   | Step   | Command        | Status |
| --- | ------ | -------------- | ------ |
| 1   | Build  | `{BUILD_CMD}`  | ⬜     |
| 2   | Push   | `{PUSH_CMD}`   | ⬜     |
| 3   | Deploy | `{DEPLOY_CMD}` | ⬜     |
| 4   | Verify | `{VERIFY_CMD}` | ⬜     |

### Environment

| Variable | Value   |
| -------- | ------- |
| {ENV_1}  | {VAL_1} |
| {ENV_2}  | {VAL_2} |

### Verification

- [ ] Health check passing
- [ ] Logs clean
- [ ] Metrics normal
- [ ] No errors in monitoring

### Rollback

```bash
{ROLLBACK_CMD}
```

### Notes

{NOTES}

---

\_DOMYH Awesome Code
