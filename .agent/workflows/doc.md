---
name: doc
trigger: ["/doc", "docs", "documentation", "tài liệu"]
persona: technical_writer
description: "📝 Generate documentation: API docs, README, code comments, and changelogs"
---

# 📝 /doc — Doc Pro v3.1

> AI-Powered Documentation Generation
> 📚 30+ Languages • Docs-as-Code • Auto-API Specs

---

## 🔄 DOCUMENTATION FLOW

```
User: /doc [type]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: ANALYZE (Auto)                │
│ ▸ Detect tech stack                     │
│ ▸ Scan codebase structure               │
│ ▸ Identify undocumented items           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: PLAN                           │
│ ▸ Show documentation gaps               │
│ ▸ Estimate scope                        │
│ ⛔ STOP if large → confirm scope        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: GENERATE                       │
│ ▸ Create doc content                    │
│ ▸ Use language-specific format          │
│ ▸ Add examples & diagrams               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: VALIDATE                       │
│ ▸ Check links & references              │
│ ▸ Verify code examples compile          │
│ ▸ Lint documentation                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: OUTPUT                         │
│ ▸ Generate files (MD/HTML/PDF)          │
│ ▸ Update existing docs                  │
│ ▸ Show summary                          │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command          | Description                | Output            |
| ---------------- | -------------------------- | ----------------- |
| `/doc`           | Auto-detect & generate all | Mixed             |
| `/doc readme`    | Generate/update README     | Markdown          |
| `/doc api`       | API documentation          | OpenAPI/Swagger   |
| `/doc code`      | Code comments → docs       | Language-specific |
| `/doc changelog` | Generate CHANGELOG         | Markdown          |
| `/doc config`    | Configuration docs         | Markdown          |
| `/doc --check`   | Audit existing docs        | Report            |

---

## 📋 PHASE 1: ANALYZE

### Documentation Audit:

```
📊 DOCUMENTATION ANALYSIS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack: TypeScript + Express
Files scanned: 145

Coverage:
├── Functions: 78/120 (65%) 📝 42 undocumented
├── Classes: 12/15 (80%) 📝 3 undocumented
├── API Endpoints: 23/35 (66%) 📝 12 undocumented
├── Types/Interfaces: 45/60 (75%) 📝 15 undocumented
└── README: ⚠️ Outdated (6 months ago)

Priority:
1. 🔴 12 public API endpoints (no docs)
2. 🟡 42 exported functions (no JSDoc)
3. 🟢 README update (minor)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🌐 DOCUMENTATION TOOLS (30+ Languages)

### Backend / Systems

````yaml
# ═══════════════════════════════════════════════════════════════
# COMPILED LANGUAGES
# ═══════════════════════════════════════════════════════════════

go:
  inline: "// GoDoc comments"
  generator: "godoc, pkgsite"
  api: "swaggo/swag"
  command: "swag init && go doc ./..."
  format: "godoc format"
  example: |
    // GetUser retrieves a user by ID.
    //
    // Parameters:
    //   - id: The user's unique identifier
    //
    // Returns the user or an error if not found.
    func GetUser(id string) (*User, error)

rust:
  inline: "/// Rustdoc comments"
  generator: "rustdoc"
  api: "utoipa (OpenAPI)"
  command: "cargo doc --open"
  format: "Markdown in comments"
  example: |
    /// Retrieves a user by ID.
    ///
    /// # Arguments
    /// * `id` - The user's unique identifier
    ///
    /// # Returns
    /// The user or an error if not found.
    ///
    /// # Examples
    /// ```
    /// let user = get_user("123")?;
    /// ```
    pub fn get_user(id: &str) -> Result<User, Error>

java:
  inline: "/** Javadoc */"
  generator: "javadoc"
  api: "springdoc-openapi"
  command: "mvn javadoc:javadoc"
  format: "HTML output"
  example: |
    /**
     * Retrieves a user by ID.
     *
     * @param id The user's unique identifier
     * @return The user object
     * @throws UserNotFoundException if user not found
     */
    public User getUser(String id)

kotlin:
  inline: "/** KDoc */"
  generator: "Dokka"
  api: "springdoc-openapi-kotlin"
  command: "gradle dokkaHtml"
  format: "HTML, Markdown, Javadoc"
  example: |
    /**
     * Retrieves a user by ID.
     *
     * @param id The user's unique identifier
     * @return The user object
     * @throws UserNotFoundException if user not found
     */
    fun getUser(id: String): User

csharp:
  inline: "/// XML comments"
  generator: "DocFX, Sandcastle"
  api: "Swashbuckle (Swagger)"
  command: "dotnet build /p:GenerateDocumentationFile=true"
  format: "XML → HTML"
  example: |
    /// <summary>
    /// Retrieves a user by ID.
    /// </summary>
    /// <param name="id">The user's unique identifier</param>
    /// <returns>The user object</returns>
    /// <exception cref="UserNotFoundException">User not found</exception>
    public User GetUser(string id)

cpp:
  inline: "/// Doxygen comments"
  generator: "Doxygen"
  api: "N/A (manual OpenAPI)"
  command: "doxygen Doxyfile"
  format: "HTML, LaTeX, RTF"
  example: |
    /**
     * @brief Retrieves a user by ID.
     * @param id The user's unique identifier
     * @return Pointer to user or nullptr
     * @throws std::runtime_error if not found
     */
    User* getUser(const std::string& id);

c:
  inline: "/** Doxygen */"
  generator: "Doxygen"
  api: "N/A"
  command: "doxygen"
  format: "HTML, man pages"
  example: |
    /**
     * @brief Retrieves a user by ID.
     * @param id The user's unique identifier
     * @return Pointer to user struct or NULL
     */
    struct User* get_user(const char* id);

# ═══════════════════════════════════════════════════════════════
# SCRIPTING LANGUAGES
# ═══════════════════════════════════════════════════════════════

python:
  inline: '"""Docstrings (PEP 257)"""'
  generator: "Sphinx, MkDocs, pdoc"
  api: "FastAPI (auto-OpenAPI)"
  command: "sphinx-build -b html docs/ _build/"
  format: "reStructuredText, Markdown"
  styles: ["Google", "NumPy", "Sphinx"]
  example: |
    def get_user(id: str) -> User:
        """Retrieve a user by ID.

        Args:
            id: The user's unique identifier.

        Returns:
            The user object.

        Raises:
            UserNotFoundError: If user doesn't exist.

        Example:
            >>> user = get_user("123")
            >>> print(user.name)
        """

ruby:
  inline: "# YARD comments"
  generator: "YARD, RDoc"
  api: "rswag (Swagger for Rails)"
  command: "yard doc"
  format: "HTML"
  example: |
    # Retrieves a user by ID.
    #
    # @param id [String] the user's unique identifier
    # @return [User] the user object
    # @raise [UserNotFoundError] if user not found
    def get_user(id)

php:
  inline: "/** PHPDoc */"
  generator: "phpDocumentor"
  api: "L5-Swagger, Scramble"
  command: "phpDocumentor -d src -t docs"
  format: "HTML"
  example: |
    /**
     * Retrieves a user by ID.
     *
     * @param string $id The user's unique identifier
     * @return User The user object
     * @throws UserNotFoundException If user not found
     */
    public function getUser(string $id): User

perl:
  inline: "=head1 POD"
  generator: "Pod::Simple"
  api: "N/A"
  command: "pod2html"
  format: "POD → HTML"
  example: |
    =head2 get_user

    Retrieves a user by ID.

    =head3 Parameters

    =over

    =item id - The user's unique identifier

    =back

    =cut

lua:
  inline: "--- LDoc comments"
  generator: "LDoc"
  api: "N/A"
  command: "ldoc ."
  format: "HTML"
  example: |
    --- Retrieves a user by ID.
    -- @param id string The user's identifier
    -- @return User the user object
    -- @raise error if not found
    function get_user(id)

# ═══════════════════════════════════════════════════════════════
# JAVASCRIPT / TYPESCRIPT
# ═══════════════════════════════════════════════════════════════

javascript:
  inline: "/** JSDoc */"
  generator: "JSDoc, documentation.js"
  api: "swagger-jsdoc"
  command: "npx jsdoc -c jsdoc.json"
  format: "HTML, Markdown"
  example: |
    /**
     * Retrieves a user by ID.
     *
     * @param {string} id - The user's unique identifier
     * @returns {Promise<User>} The user object
     * @throws {UserNotFoundError} If user not found
     *
     * @example
     * const user = await getUser('123');
     */
    async function getUser(id) {}

typescript:
  inline: "/** TSDoc */"
  generator: "TypeDoc"
  api: "tsoa, swagger-typescript-api"
  command: "npx typedoc --out docs src"
  format: "HTML, Markdown"
  example: |
    /**
     * Retrieves a user by ID.
     *
     * @param id - The user's unique identifier
     * @returns The user object
     * @throws {@link UserNotFoundError} If user not found
     *
     * @example
     * ```typescript
     * const user = await getUser('123');
     * console.log(user.name);
     * ```
     */
    async function getUser(id: string): Promise<User>

react:
  inline: "/** JSDoc + PropTypes/TypeScript */"
  generator: "Storybook, react-docgen"
  api: "N/A"
  command: "npx storybook build"
  format: "Storybook UI"
  example: |
    /**
     * UserCard displays user information.
     *
     * @component
     * @example
     * <UserCard user={userData} onClick={handleClick} />
     */
    interface UserCardProps {
      /** The user data to display */
      user: User;
      /** Click handler */
      onClick?: () => void;
    }

# ═══════════════════════════════════════════════════════════════
# MOBILE
# ═══════════════════════════════════════════════════════════════

swift:
  inline: "/// Documentation comments"
  generator: "DocC, Jazzy"
  api: "N/A"
  command: "swift package generate-documentation"
  format: "DocC archive"
  example: |
    /// Retrieves a user by ID.
    ///
    /// - Parameter id: The user's unique identifier
    /// - Returns: The user object
    /// - Throws: `UserError.notFound` if user doesn't exist
    ///
    /// ```swift
    /// let user = try getUser(id: "123")
    /// ```
    func getUser(id: String) throws -> User

dart:
  inline: "/// DartDoc comments"
  generator: "dartdoc"
  api: "N/A"
  command: "dart doc"
  format: "HTML"
  example: |
    /// Retrieves a user by ID.
    ///
    /// [id] is the user's unique identifier.
    ///
    /// Returns the [User] object.
    ///
    /// Throws [UserNotFoundException] if not found.
    ///
    /// Example:
    /// ```dart
    /// final user = await getUser('123');
    /// ```
    Future<User> getUser(String id)

# ═══════════════════════════════════════════════════════════════
# FUNCTIONAL
# ═══════════════════════════════════════════════════════════════

elixir:
  inline: "@doc comments"
  generator: "ExDoc"
  api: "OpenApiSpex"
  command: "mix docs"
  format: "HTML"
  example: |
    @doc """
    Retrieves a user by ID.

    ## Parameters
      - id: The user's unique identifier

    ## Examples
        iex> get_user("123")
        {:ok, %User{}}
    """
    @spec get_user(String.t()) :: {:ok, User.t()} | {:error, term()}
    def get_user(id)

haskell:
  inline: "-- | Haddock comments"
  generator: "Haddock"
  api: "servant-swagger"
  command: "cabal haddock"
  format: "HTML"
  example: |
    -- | Retrieves a user by ID.
    --
    -- >>> getUser "123"
    -- Right (User "123" "John")
    getUser :: UserId -> IO (Either Error User)

scala:
  inline: "/** Scaladoc */"
  generator: "Scaladoc"
  api: "tapir (OpenAPI)"
  command: "sbt doc"
  format: "HTML"
  example: |
    /** Retrieves a user by ID.
      *
      * @param id The user's unique identifier
      * @return The user object
      * @throws UserNotFoundException if not found
      */
    def getUser(id: String): User

# ═══════════════════════════════════════════════════════════════
# API SPECIFICATION
# ═══════════════════════════════════════════════════════════════

openapi:
  format: "OpenAPI 3.1 (YAML/JSON)"
  tools: ["Swagger UI", "Redoc", "Stoplight"]
  generators: ["swagger-codegen", "openapi-generator"]
  example: |
    openapi: 3.1.0
    paths:
      /users/{id}:
        get:
          summary: Get user by ID
          parameters:
            - name: id
              in: path
              required: true
              schema:
                type: string
          responses:
            '200':
              description: User found
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/User'

graphql:
  format: "GraphQL SDL + descriptions"
  tools: ["GraphQL Playground", "Apollo Studio"]
  example: |
    """
    Represents a user in the system.
    """
    type User {
      "Unique identifier"
      id: ID!
      "User's display name"
      name: String!
    }

    type Query {
      "Retrieves a user by ID"
      user(id: ID!): User
    }
````

---

## 📋 PHASE 2: PLAN

### Documentation Scope:

```
📋 DOCUMENTATION PLAN

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scope: Full documentation update
Estimated time: ~15 minutes

Tasks:
├── [1] README.md
│   ├── Update installation
│   ├── Add quick start
│   └── Update API section
│
├── [2] API Documentation
│   ├── Generate OpenAPI spec
│   ├── Document 12 new endpoints
│   └── Add request/response examples
│
├── [3] Code Documentation
│   ├── Add JSDoc to 42 functions
│   ├── Document 15 types
│   └── Add usage examples
│
└── [4] CHANGELOG
    └── Generate from commits

Total items: 73 documentation updates

⛔ Proceed? (y/n/partial):
```

---

## 📋 PHASE 3: GENERATE

### README Template:

```markdown
# Project Name

> One-line description

[![Build Status](badge)](#) [![License](badge)](#)

## 🚀 Quick Start

\`\`\`bash
npm install project-name
\`\`\`

## 📖 Documentation

- [API Reference](./docs/api.md)
- [Configuration](./docs/config.md)
- [Examples](./examples/)

## 🔧 Configuration

| Variable  | Description | Default  |
| --------- | ----------- | -------- |
| `API_KEY` | API key     | Required |

## 📝 License

MIT
```

### CHANGELOG Template:

```markdown
# Changelog

All notable changes documented here.

## [Unreleased]

### Added

- Feature X (#123)

### Changed

- Improved Y performance

### Fixed

- Bug in Z (#456)

## [1.0.0] - 2026-01-31

### Added

- Initial release
```

---

## 📋 PHASE 4: VALIDATE

### Documentation Checks:

```yaml
validation:
  links:
    - Check internal links work
    - Check external URLs accessible
    - Verify anchor references

  code_examples:
    - Syntax highlight valid
    - Examples compile/run
    - Output matches description

  formatting:
    - Consistent header levels
    - No orphan images
    - Tables properly formatted

  completeness:
    - All public APIs documented
    - Parameters described
    - Return values specified
    - Examples provided
```

### Validation Output:

```
✅ DOCUMENTATION VALIDATED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Links: ✅ 45/45 valid
Code examples: ✅ 12/12 compile
Format: ✅ No issues
Coverage: ✅ 100% public APIs

Warnings:
└── 2 functions missing examples (optional)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 5: OUTPUT

### Generation Summary:

```
📝 DOCUMENTATION GENERATED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Created/Updated:
├── README.md (updated)
├── docs/api.md (created)
├── docs/openapi.yaml (created)
├── CHANGELOG.md (updated)
└── src/**/*.ts (JSDoc added)

Stats:
├── Functions documented: 42 new
├── API endpoints: 12 new
├── Types/Interfaces: 15 new
├── Examples added: 23
└── Total lines: +850

Output formats:
├── Markdown: docs/
├── OpenAPI: docs/openapi.yaml
└── HTML: npm run docs:build

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Preview: npm run docs:serve
2️⃣ Commit: git commit -am "docs: update documentation"
3️⃣ Deploy docs: /deploy docs

Enter number:
```

---

## 🔧 SUB-COMMANDS

| Command              | Description        |
| -------------------- | ------------------ |
| `/doc`               | Auto-generate all  |
| `/doc readme`        | README only        |
| `/doc api`           | API spec (OpenAPI) |
| `/doc code`          | Inline code docs   |
| `/doc changelog`     | CHANGELOG from git |
| `/doc --check`       | Audit coverage     |
| `/doc --format html` | Output as HTML     |

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Focus on public APIs first
  - Skip internal/private functions
  - Prioritize undocumented items
  - Batch similar patterns

  # Use templates
  - Apply language-specific templates
  - Generate from function signatures
  - Infer from type definitions

  # Incremental updates
  - Only modify changed files
  - Preserve existing good docs
  - Add missing pieces only
```

---

## 📜 RULES APPLIED

| Phase    | Rules                            |
| -------- | -------------------------------- |
| Analyze  | `context-management`             |
| Plan     | `stop-conditions` (if large)     |
| Generate | `quality`, `safety` (no secrets) |
| Validate | `evidence`                       |
| Output   | `edit-verification`              |

---

## 🤖 AI-OPTIMIZED DOCS (v3.1)

```yaml
ai_optimized_docs:
  description: "Documentation for both humans and AI"

  llms_txt:
    purpose: "Help AI understand your project"
    content:
      - "Project overview and purpose"
      - "Architecture summary"
      - "API endpoint list"
      - "Key concepts and terminology"
    location: "/llms.txt or /docs/llms.txt"
    format: "Plain text, concise"

  docs_as_code:
    principles:
      - "Docs live with code"
      - "Version controlled"
      - "CI/CD validated"
      - "Auto-generated where possible"

    tools:
      static_site: ["Docusaurus", "VitePress", "Astro"]
      api_docs: ["Redocly", "Swagger UI"]
      diagrams: ["Mermaid", "PlantUML"]

  mcp_integration:
    description: "Model Context Protocol for AI tools"
    expose:
      - "API schemas"
      - "Code navigation"
      - "Documentation search"

  commands:
    generate_llms: "/doc llms"
    ai_optimize: "/doc ai [optimize|verify]"
```

---

## 📚 AUTO API SPECS (v3.1)

```yaml
auto_api_specs:
  description: "Generate API documentation from code"

  sources:
    annotations:
      - "JSDoc/TSDoc"
      - "GoDoc"
      - "Python docstrings"
      - "Swagger annotations"

    runtime:
      description: "Capture from actual requests"
      tools: ["Optic", "Apidog"]

    contracts:
      - "OpenAPI 3.1"
      - "GraphQL SDL"
      - "AsyncAPI"
      - "JSON Schema"

  generation:
    from_code:
      command: "/doc api generate"
      output: "openapi.yaml"

    from_tests:
      command: "/doc api capture"
      source: "Integration tests"

  validation:
    examples: "Must be executable"
    types: "Must match implementation"
    deprecations: "Clearly marked"
    breaking_changes: "Diff detection"

  commands:
    generate: "/doc api generate"
    validate: "/doc api validate"
    diff: "/doc api diff [old] [new]"
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command             | Description          |
| ------------------- | -------------------- |
| `/doc`              | Auto-generate all    |
| `/doc readme`       | README only          |
| `/doc api generate` | Generate OpenAPI     |
| `/doc api validate` | Validate API spec    |
| `/doc llms`         | Generate llms.txt    |
| `/doc ai optimize`  | AI-optimize all docs |
| `/doc changelog`    | CHANGELOG from git   |
| `/doc --check`      | Audit coverage       |

---

_DOMYH Awesome Code v6.1.2 • Doc Pro v3.1 • AI-Optimized + Auto API_
