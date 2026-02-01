# 🌍 i18n — DOMYH Agent v3.0

Language files for internationalization.

## Files

| File      | Language   | Status       |
| --------- | ---------- | ------------ |
| `en.yaml` | English    | ✅ Default   |
| `vi.yaml` | Tiếng Việt | ✅ Supported |

## Usage

Set language in `manifest.yaml`:

```yaml
lang: en # or vi
```

Or switch at runtime: `/lang vi`

## Adding Languages

1. Copy `en.yaml` to `{lang}.yaml`
2. Translate all values
3. Add to `manifest.yaml` i18n section

---

_DOMYH Agent v3.0 • NockDev_
