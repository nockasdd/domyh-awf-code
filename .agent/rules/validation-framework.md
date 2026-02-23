---
name: validation-framework
priority: 0
always_apply: true
category: quality
version: "4.5"
---

# ✅ Validation Framework v6.4.2

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📝 **Note**: Consolidates `pre-check-validation.md` + `architecture-aware-implementation.md`

## Enforcement Level: BLOCK

## Description

Before creating ANY new code, agent MUST pass 6-phase validation.

---

## 🔴 6-Phase Pre-Implementation Validation

```
┌──────────────────────────────────────────────────────────────┐
│ Phase 1: NECESSITY — Is it needed?                           │
│ → Check user request, YAGNI principle                        │
├──────────────────────────────────────────────────────────────┤
│ Phase 2: DISCOVERY — What exists?                            │
│ → Search for similar files, patterns, utilities              │
├──────────────────────────────────────────────────────────────┤
│ Phase 3: SCOPE — Does request cover this?                    │
│ → Verify against original request, avoid scope creep         │
├──────────────────────────────────────────────────────────────┤
│ Phase 4: PLACEMENT — Where does it fit?                      │
│ → Determine layer, file, module location                     │
├──────────────────────────────────────────────────────────────┤
│ Phase 5: CONNECTIVITY — How will it be used?                 │
│ → Trace imports, exports, consumers                          │
├──────────────────────────────────────────────────────────────┤
│ Phase 6: REGISTRATION — What needs update?                   │
│ → index.json, manifests, exports                             │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Necessity (YAGNI)

| Question                   | If NO          |
| -------------------------- | -------------- |
| User explicitly requested? | ❌ STOP        |
| Will be used immediately?  | ❌ STOP        |
| No library solution?       | ⚠️ Use library |

```yaml
red_flags:
  - "Nice to have" features
  - "While I'm here..." changes
  - Building for hypothetical future
  - Adding unused dependencies
```

---

## Phase 2: Discovery

```yaml
search_checklist:
  - grep_search: similar function names
  - Check: utils/, shared/, lib/ directories
  - Review: index files for existing components
  - Verify: no deprecated/moved version exists
```

---

## Phase 3: Scope Validation

| Requested?            | Action     |
| --------------------- | ---------- |
| Explicitly in request | ✅ Proceed |
| Implied by request    | ⚠️ Clarify |
| Not mentioned         | ❌ STOP    |

---

## Phase 4: Placement

### Layer Decision

| Code Type      | Location                    |
| -------------- | --------------------------- |
| Shared utility | `utils/`, `lib/`, `shared/` |
| Domain logic   | `services/`, `domain/`      |
| API handler    | `handlers/`, `routes/`      |
| Data access    | `repositories/`, `store/`   |
| View/UI        | `components/`, `views/`     |

---

## Phase 5: Connectivity

Before creating file, trace:

```yaml
connectivity_check:
  imports:
    - What modules will import this?
    - Are import paths correct?
  exports:
    - What needs to be exported?
    - Default vs named exports?
  consumers:
    - Who will call these functions?
    - What parameters needed?
```

---

## Phase 6: Registration

After creating file, update:

```yaml
registration_checklist:
  - [ ] index.json or manifest.yaml
  - [ ] Export from parent module
  - [ ] Type definitions if TypeScript
  - [ ] README if significant
```

---

## 📋 Quick Checklist

- [ ] User requested this? (Phase 1)
- [ ] Searched for similar? (Phase 2)
- [ ] Within scope? (Phase 3)
- [ ] Know where to place? (Phase 4)
- [ ] Know who uses it? (Phase 5)
- [ ] Will update registry? (Phase 6)

---

## ❌ BLOCK Conditions

Agent MUST NOT proceed if:

```yaml
block_conditions:
  - No explicit user request
  - Similar code already exists
  - Out of scope for request
  - Placement unclear
  - YAGNI violation detected
```

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Trước khi tạo BẤT KỲ code mới nào, agent PHẢI qua 6 phase validation.

## 6 Phase

1. **Necessity** — Có thực sự cần không? (YAGNI)
2. **Discovery** — Có gì tương tự chưa?
3. **Scope** — Có trong phạm vi yêu cầu không?
4. **Placement** — Đặt ở đâu?
5. **Connectivity** — Ai sẽ dùng?
6. **Registration** — Cần update index nào?

## Checklist Nhanh

- [ ] User yêu cầu? (Phase 1)
- [ ] Đã tìm tương tự? (Phase 2)
- [ ] Trong scope? (Phase 3)
- [ ] Biết đặt ở đâu? (Phase 4)
- [ ] Biết ai dùng? (Phase 5)
- [ ] Sẽ update registry? (Phase 6)

---

_DOMYH Awesome Code • Consolidated Validation Framework_
