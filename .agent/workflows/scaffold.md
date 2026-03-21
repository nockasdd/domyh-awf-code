---
description: "🏗️ Unified scaffolding & code generation: components, pages, services, models, APIs from project patterns"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "Files generated matching project conventions, build passes"
---

# 🏗️ /scaffold — Scaffold Pro

> Unified Framework-Aware Code Generation
> 📚 Auto-Detect • Convention Matching • 30+ Templates • Multi-Stack
> ℹ️ Also accessible via `/generate` (alias)

---

## SCAFFOLD FLOW

1. **DETECT** (Auto) — Identify framework via HSA (`hsa_detect`), load patterns via HSA (`hsa_search`), scan existing components. Show: `[Step 1/6] Detecting React + TypeScript...`
2. **MATCH** — Analyze existing code patterns: naming (camelCase/snake_case/PascalCase), file organization (flat/nested), imports (absolute/relative/barrel), exports, test location. Show: `[Step 2/6] Found: camelCase, barrel exports, co-located tests`
3. **PREVIEW** — Show all files to be created with content preview → ⛔ STOP: confirm before generate
4. **GENERATE** — Create files from template, wire up imports/routes, add boilerplate tests. Show: `[Step 4/6] Creating UserCard (3 files)...`
5. **VERIFY** — Build check, list created files, suggest next steps
6. **SYNC** — `hsa_check_changes` to update index after file creation

---

## COMMANDS

| Command                       | Description            | Output                     |
| ----------------------------- | ---------------------- | -------------------------- |
| `/scaffold component [name]`  | UI component           | Component + styles + test  |
| `/scaffold page [name]`       | Page/route             | Page + layout              |
| `/scaffold service [name]`    | Service/repository     | Service + interface + test |
| `/scaffold model [name]`      | Data model/entity      | Model + migration          |
| `/scaffold api [route]`       | REST API endpoint      | Handler + service + test   |
| `/scaffold module [name]`     | Full module (CRUD)     | All files                  |
| `/scaffold hook [name]`       | Custom hook/composable | Hook + test                |
| `/scaffold test [file]`       | Test file for existing | Test file with coverage    |
| `/scaffold layout [name]`     | Layout component       | Layout + styles            |
| `/scaffold middleware [name]` | Middleware/interceptor | Middleware + test          |
| `/scaffold dto [name]`        | Data transfer object   | DTO + validation           |

> Alias: all commands also accessible via `/generate` (e.g., `/generate model User`)

---

## 📋 CONVENTION MATCHING

> Before generating, analyze existing code to match project conventions:

```yaml
pattern_scan:
  naming: "camelCase | snake_case | PascalCase | kebab-case"
  file_org: "flat | nested (component/__tests__/Component.test.ts)"
  imports: "absolute (@/...) | relative (./...) | barrel (index.ts)"
  exports: "default | named | barrel"
  tests: "co-located (__tests__/) | separate (tests/) | same-dir (.test.ts)"
  formatting: "prettier | eslint | language-default"
```

---

## 🔧 FRAMEWORK TEMPLATES

### Frontend

| Framework | component                                         | page                               | hook/composable                | service                          |
| --------- | ------------------------------------------------- | ---------------------------------- | ------------------------------ | -------------------------------- |
| React     | `src/components/{Name}/{Name}.tsx + test + index` | `src/pages/{Name}Page.tsx`         | `src/hooks/use{Name}.ts`       | `src/services/{name}.service.ts` |
| Next.js   | `components/{Name}/{Name}.tsx + module.css`       | `app/{name}/page.tsx + layout.tsx` | —                              | `lib/{name}.ts`                  |
| Nuxt      | `components/{Name}.vue`                           | `pages/{name}.vue`                 | `composables/use{Name}.ts`     | `server/api/{name}.ts`           |
| Vue       | `src/components/{Name}.vue`                       | `src/views/{Name}View.vue`         | `src/composables/use{Name}.ts` | `src/services/{name}.service.ts` |
| Angular   | `ng generate component {name}`                    | —                                  | —                              | `ng generate service {name}`     |
| Svelte    | `src/lib/components/{Name}.svelte`                | `src/routes/{name}/+page.svelte`   | —                              | `src/lib/services/{name}.ts`     |

### Backend

| Stack   | handler/controller                     | service                               | repository                             | model                        | test                   |
| ------- | -------------------------------------- | ------------------------------------- | -------------------------------------- | ---------------------------- | ---------------------- |
| Go      | `internal/handlers/{name}_handler.go`  | `internal/services/{name}_service.go` | `internal/repositories/{name}_repo.go` | `internal/models/{name}.go`  | `{file}_test.go`       |
| Express | `src/controllers/{name}.controller.ts` | `src/services/{name}.service.ts`      | —                                      | `src/models/{name}.model.ts` | —                      |
| Python  | `src/api/{name}_router.py`             | `src/services/{name}_service.py`      | —                                      | `src/models/{name}.py`       | `tests/test_{name}.py` |

> ⚠️ **Proportional Response**: For MICRO/SMALL tasks (≤50 LOC), generate ONLY the
> primary file (e.g., handler). Skip service/repository layers unless explicitly needed.
> See `rules/modules/proportional-response.yaml` for sizing rules.

### Mobile

| Stack        | screen                           | widget/component                 | state                               | model                    |
| ------------ | -------------------------------- | -------------------------------- | ----------------------------------- | ------------------------ |
| Flutter      | `lib/screens/{name}_screen.dart` | `lib/widgets/{name}_widget.dart` | `lib/blocs/{name}/{name}_bloc.dart` | `lib/models/{name}.dart` |
| React Native | `src/screens/{Name}Screen.tsx`   | `src/components/{Name}.tsx`      | `src/hooks/use{Name}.ts`            | —                        |

---

## 📦 Generator Tools by Stack

| Stack            | Generator Tools               | Model Pattern                | API Pattern                    |
| ---------------- | ----------------------------- | ---------------------------- | ------------------------------ |
| **Go**           | `go generate, sqlc, ent`      | Domain struct + JSON/DB tags | Handler → Service → Repository |
| **Rust**         | `cargo-generate, sea-orm-cli` | Struct + derive macros       | Axum handler → impl            |
| **Java**         | `Spring Initializr, JHipster` | @Entity + JPA annotations    | @RestController → @Service     |
| **Kotlin**       | `Spring Initializr, Ktor Gen` | data class + @Entity         | Ktor routes → Service          |
| **C#**           | `dotnet new, EF Core`         | Class + EF annotations       | Controller → Service           |
| **Python**       | `cookiecutter, FastAPI gen`   | SQLAlchemy/Pydantic          | @router → CRUD                 |
| **Ruby**         | `rails generate`              | ActiveRecord model           | Rails controller               |
| **PHP**          | `artisan make, symfony make`  | Eloquent/Doctrine            | Controller + Resource          |
| **TypeScript**   | `nest generate, hygen`        | Interface + Prisma           | Controller → Service           |
| **Next.js**      | `npx create-next-app`         | Prisma model                 | API route handler              |
| **Vue/Nuxt**     | `nuxi add`                    | Composable                   | Pages + API routes             |
| **Angular**      | `ng generate`                 | Interface + Service          | Component + Module             |
| **Flutter**      | `mason make`                  | Freezed model                | BLoC pattern                   |
| **React Native** | `npx create-expo-app`         | TypeScript model             | Hook + API layer               |

---

## 🎨 DESIGN-AWARE GENERATION

When scaffolding UI components:

1. **Detect Design System** — Check for existing tokens/theme
2. **Apply Component Decision Tree** — Reuse > Framework > Compose > Build
3. **Use Design Tokens** — Import from existing token files (no magic values)
4. **Add Accessibility** — Semantic HTML, ARIA labels, keyboard support
5. **Follow Atomic Level** — Assign correct level (atom/molecule/organism)

> Auto-triggered when `/scaffold component` or `/scaffold layout` is called. Load `domyh-design` skill for full UI guidelines.

---

## ⛔ SAFETY

- Preserve existing files — only create new ones
- Show file list before creation
- Confirm if > 5 files will be created
- Validate names against project conventions
- Detect and warn about naming conflicts
- Preserve import ordering conventions
---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

