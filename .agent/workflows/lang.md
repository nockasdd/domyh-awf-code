---
description: 🌐 Switch agent language (English ↔ Vietnamese)
---

# /lang — Language Switching

## Purpose

Switch the agent's response language between supported languages. Affects all subsequent responses in the session AND persists globally for new projects.

## Supported Languages

| Code | Language | Flag |
|------|----------|------|
| `en` | English | 🇺🇸 |
| `vi` | Tiếng Việt | 🇻🇳 |

## Steps

### 1. Parse Language Argument

- `/lang vi` → Switch to Vietnamese
- `/lang en` → Switch to English
- `/lang` → Show current language + toggle

### 2. Update Session Language

Update the active session language preference:
- Set `manifest.yaml` → `lang:` field
- If MCP connected: `hsa_session({ action: 'anchor', category: 'convention', content: 'Language: <lang>' })`

### 3. Persist to state.json

- Read `.agent/memory/state.json`
- Set `preferences.language` = new language
- Write back to file

### 4. Persist to Global Preferences

- Write language to `~/.nockdev/hsa/user-preferences.json`
- This ensures ALL future new projects inherit this language
- Format: `{ "language": "<lang>", "updated_at": "<ISO>", "source": "/lang" }`

### 5. Confirm

Respond in the **new** language to confirm the switch:
- `en`: "✅ Language switched to English"
- `vi`: "✅ Đã chuyển sang Tiếng Việt"

## Examples

```
/lang vi     → ✅ Đã chuyển sang Tiếng Việt
/lang en     → ✅ Language switched to English
/lang        → Current: vi (Tiếng Việt). Use /lang en to switch.
```

## Notes

- Language preference persists both per-session AND globally
- Code, technical terms, and commands remain in English regardless of language setting
- i18n files: `.agent/i18n/en.yaml` and `.agent/i18n/vi.yaml`
- Global preferences: `~/.nockdev/hsa/user-preferences.json`
