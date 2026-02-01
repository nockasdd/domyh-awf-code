---
description: 🌍 Switch agent language (en/vi) and update preferences
---

# 🌍 /lang — Language Switching

> Chuyển đổi ngôn ngữ agent giữa English và Tiếng Việt
> 📁 Config: `.agent/memory/state.json` → `preferences.language`

---

## 🔄 LANGUAGE FLOW

```
User: /lang [code]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: VALIDATE                       │
│ ▸ Check language code (en/vi)           │
│ ▸ Load i18n strings                     │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: UPDATE                         │
│ ▸ Update memory/state.json              │
│ ▸ Update manifest.yaml                  │
│ ▸ Update config.yaml                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: CONFIRM                        │
│ ▸ Display new language setting          │
│ ▸ Show sample response                  │
└─────────────────────────────────────────┘
```

---

## 📋 SUPPORTED LANGUAGES

| Code | Language   | i18n File             |
| ---- | ---------- | --------------------- |
| `en` | English    | `.agent/i18n/en.yaml` |
| `vi` | Tiếng Việt | `.agent/i18n/vi.yaml` |

---

## 🔧 COMMANDS

| Command        | Description                |
| -------------- | -------------------------- |
| `/lang`        | Hiển thị ngôn ngữ hiện tại |
| `/lang vi`     | Chuyển sang Tiếng Việt     |
| `/lang en`     | Switch to English          |
| `/lang status` | Kiểm tra cấu hình ngôn ngữ |

---

## 📁 FILES TO UPDATE

Khi chuyển ngôn ngữ, cập nhật các files sau:

### 1. memory/state.json

```json
{
  "preferences": {
    "language": "vi" // hoặc "en"
  }
}
```

### 2. manifest.yaml

```yaml
lang: vi # hoặc en
```

### 3. config.yaml (optional)

```yaml
i18n:
  default: "vi" # hoặc "en"
```

---

## 📊 OUTPUT FORMAT

### /lang vi

```
🌍 LANGUAGE SWITCHED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Đã chuyển sang: Tiếng Việt

Files Updated:
├── ✅ memory/state.json (preferences.language)
├── ✅ manifest.yaml (lang)
└── ✅ config.yaml (i18n.default)

Từ giờ tất cả responses sẽ bằng Tiếng Việt.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### /lang en

```
🌍 LANGUAGE SWITCHED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Switched to: English

Files Updated:
├── ✅ memory/state.json (preferences.language)
├── ✅ manifest.yaml (lang)
└── ✅ config.yaml (i18n.default)

All responses will now be in English.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ⚠️ IMPORTANT RULES

1. **GEMINI.md Header** - PHẢI có instruction ngôn ngữ:

   ```markdown
   > 🌍 **Language**: Tiếng Việt — LUÔN trả lời bằng tiếng Việt
   ```

2. **Consistency** - Tất cả 3 files phải đồng bộ:
   - `state.json` → `preferences.language`
   - `manifest.yaml` → `lang`
   - `config.yaml` → `i18n.default`

3. **Persistence** - Language setting persist across sessions

---

## 🔗 RELATED

- `/save` - Lưu preferences vào memory files
- `/help` - Hiển thị commands với ngôn ngữ hiện tại
- `/status` - Kiểm tra project status

---

_DOMYH Awesome Code v4.3 • Language Switching • i18n Support_
