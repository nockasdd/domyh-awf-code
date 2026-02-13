---
description: "📝 Generate documentation: API docs, README, code comments, and changelogs"
skills: { required: [], contextual: [auto] }
---

# 📝 /doc — Doc Pro

> AI-Powered Documentation Generation
> 📚 20+ Languages • Docs-as-Code • Auto-API Specs

---

## DOCUMENTATION FLOW

1. **ANALYZE** (Auto) — Detect stack via HSA (`hsa_detect_stack`), load code context (`hsa_get_context`), scan codebase, identify undocumented items
2. **PLAN** — Show documentation gaps, estimate scope → ⛔ STOP if large: confirm scope
3. **GENERATE** — Create doc content, use language-specific format, add examples & diagrams
4. **VALIDATE** — Check links/references, verify code examples compile, lint docs
5. **OUTPUT** — Generate files (MD/HTML/PDF), update existing docs, show summary
6. **SYNC** — `hsa_check_changes` to update index after documentation file changes

---

## DOC TOOLS BY LANGUAGE

```yaml
# language: inline format | generator | api docs | command
go:         "// GoDoc"              | godoc, pkgsite     | swaggo/swag          | swag init; go doc ./...
rust:       "/// Rustdoc"           | rustdoc             | utoipa               | cargo doc --open
java:       "/** Javadoc */"        | javadoc             | springdoc-openapi    | mvn javadoc:javadoc
kotlin:     "/** KDoc */"           | Dokka               | springdoc-kotlin     | gradle dokkaHtml
csharp:     "/// XML comments"      | DocFX, Sandcastle   | Swashbuckle          | dotnet build /p:GenerateDocumentationFile=true
cpp:        "/// Doxygen"           | Doxygen             | —                    | doxygen Doxyfile
c:          "/** Doxygen */"        | Doxygen             | —                    | doxygen
python:     '"""Docstrings"""'      | Sphinx, MkDocs      | FastAPI auto-OpenAPI | sphinx-build -b html docs/ _build/
ruby:       "# YARD"               | YARD, RDoc          | rswag                | yard doc
php:        "/** PHPDoc */"         | phpDocumentor       | L5-Swagger, Scramble | phpDocumentor -d src -t docs
perl:       "=head1 POD"           | Pod::Simple         | —                    | pod2html
lua:        "--- LDoc"             | LDoc                | —                    | ldoc .
javascript: "/** JSDoc */"         | JSDoc               | swagger-jsdoc        | npx jsdoc -c jsdoc.json
typescript: "/** TSDoc */"         | TypeDoc             | tsoa                 | npx typedoc --out docs src
react:      "/** JSDoc + TS */"    | Storybook           | —                    | npx storybook build
swift:      "/// DocC"             | DocC, Jazzy         | —                    | swift package generate-documentation
dart:       "/// DartDoc"          | dartdoc             | —                    | dart doc
elixir:     '@doc """..."""'       | ExDoc               | OpenApiSpex          | mix docs
haskell:    "-- | Haddock"         | Haddock             | servant-swagger      | cabal haddock
scala:      "/** Scaladoc */"      | Scaladoc            | tapir                | sbt doc
```

### API Spec Formats

```yaml
openapi: "OpenAPI 3.1 (YAML/JSON)" | tools: Swagger UI, Redoc, Stoplight
graphql: "GraphQL SDL + descriptions" | tools: Playground, Apollo Studio
```

---

## DOCSTRING STYLES (Python)

| Style  | Used By                       |
| ------ | ----------------------------- |
| Google | Google projects, most popular |
| NumPy  | Scientific Python             |
| Sphinx | Official Sphinx format        |

---

## README TEMPLATE

```markdown
# Project Name

> One-line description

## 🚀 Quick Start

## 📖 Documentation

## 🔧 Configuration (env table)

## 📝 License
```

## CHANGELOG FORMAT

```
## [Unreleased]
### Added / Changed / Fixed
## [1.0.0] - YYYY-MM-DD
```

---

## VALIDATION CHECKS

```yaml
links: Check internal + external URLs, verify anchors
code_examples: Syntax valid, examples compile/run, output matches
formatting: Consistent headers, no orphan images, tables formatted
completeness: All public APIs documented, params described, return values, examples
```

---

## AI-OPTIMIZED DOCS

```yaml
llms_txt: "Help AI understand project" → /llms.txt (overview, architecture, API list, key concepts)
docs_as_code: "Docs live with code, version controlled, CI validated, auto-generated"
```

---

## SUB-COMMANDS

| Command              | Description        |
| -------------------- | ------------------ |
| `/doc`               | Auto-generate all  |
| `/doc readme`        | README only        |
| `/doc api`           | API spec (OpenAPI) |
| `/doc code`          | Inline code docs   |
| `/doc changelog`     | CHANGELOG from git |
| `/doc --check`       | Audit coverage     |
| `/doc --format html` | Output as HTML     |
