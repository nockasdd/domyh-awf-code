---
name: generate
trigger: ["/generate", "gen", "scaffold", "tạo"]
persona: developer
description: "🏗️ Code generation: models, APIs, components, services, and tests from templates"
---

# 🏗️ /generate — Code Generation Pro v3.0

> AI-Powered Scaffolding & Templates
> 📚 30+ Languages • CRUD • Components • APIs

---

## 🔄 GENERATION FLOW

```
User: /generate [type] [name]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT (Auto)                 │
│ ▸ Detect project stack                  │
│ ▸ Find existing patterns                │
│ ▸ Load project conventions              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: CONFIGURE                      │
│ ▸ Collect required inputs               │
│ ▸ Show generation preview               │
│ ⛔ STOP → Confirm before generate       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: GENERATE                       │
│ ▸ Create files from templates           │
│ ▸ Apply naming conventions              │
│ ▸ Add imports/registrations             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: INTEGRATE                      │
│ ▸ Update index/barrel files             │
│ ▸ Register routes (if API)              │
│ ▸ Update DI container (if service)      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Compile/lint check                    │
│ ▸ Show generated files                  │
│ ▸ Suggest next steps                    │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command                      | Description             | Output                      |
| ---------------------------- | ----------------------- | --------------------------- |
| `/generate model [name]`     | Generate model/entity   | Model + Repository + Tests  |
| `/generate api [name]`       | Generate CRUD API       | Controller + Service + DTO  |
| `/generate component [name]` | Generate UI component   | Component + Styles + Tests  |
| `/generate service [name]`   | Generate service layer  | Service + Interface + Tests |
| `/generate test [file]`      | Generate tests for file | Unit + Integration tests    |
| `/generate crud [name]`      | Full CRUD stack         | All layers                  |
| `/generate hook [name]`      | React/Vue hook          | Hook + Tests                |
| `/generate page [name]`      | Full page               | Page + Components + API     |

---

## 📋 PHASE 1: DETECT

### Stack Detection:

```
🔍 PROJECT ANALYSIS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack Detected:
├── Framework: Next.js 14 (App Router)
├── Language: TypeScript
├── Database: PostgreSQL + Prisma
├── Testing: Jest + React Testing Library
└── Styling: Tailwind CSS

Conventions Found:
├── Naming: kebab-case files, PascalCase components
├── Structure: /src/app/, /src/components/
├── Pattern: Repository pattern for data access
└── Testing: __tests__/ folders

Templates Available:
├── ✅ Component (React)
├── ✅ Page (Next.js)
├── ✅ API Route (App Router)
├── ✅ Prisma Model
└── ✅ Service (Repository pattern)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🌐 GENERATION TOOLS (30+ Languages)

### Backend / Systems

```yaml
# ═══════════════════════════════════════════════════════════════
# GO
# ═══════════════════════════════════════════════════════════════

go:
  tools: ["go generate", "sqlc", "ent", "gorm gen"]
  scaffolding:
    model: |
      // internal/domain/user.go
      type User struct {
          ID        uuid.UUID `json:"id" db:"id"`
          Name      string    `json:"name" db:"name"`
          Email     string    `json:"email" db:"email"`
          CreatedAt time.Time `json:"created_at" db:"created_at"`
      }

    repository: |
      // internal/repository/user_repository.go
      type UserRepository interface {
          Create(ctx context.Context, user *domain.User) error
          GetByID(ctx context.Context, id uuid.UUID) (*domain.User, error)
          Update(ctx context.Context, user *domain.User) error
          Delete(ctx context.Context, id uuid.UUID) error
          List(ctx context.Context, limit, offset int) ([]*domain.User, error)
      }

    handler: |
      // internal/handler/user_handler.go
      func (h *UserHandler) Create(w http.ResponseWriter, r *http.Request) {
          var req CreateUserRequest
          if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
              respondError(w, http.StatusBadRequest, err)
              return
          }
          // ...
      }

# ═══════════════════════════════════════════════════════════════
# RUST
# ═══════════════════════════════════════════════════════════════

rust:
  tools: ["cargo-generate", "sea-orm-cli", "diesel_cli"]
  scaffolding:
    model: |
      // src/models/user.rs
      #[derive(Debug, Serialize, Deserialize, Queryable)]
      pub struct User {
          pub id: Uuid,
          pub name: String,
          pub email: String,
          pub created_at: DateTime<Utc>,
      }

      #[derive(Debug, Insertable)]
      #[diesel(table_name = users)]
      pub struct NewUser {
          pub name: String,
          pub email: String,
      }

# ═══════════════════════════════════════════════════════════════
# JAVA / KOTLIN
# ═══════════════════════════════════════════════════════════════

java:
  tools: ["Spring Initializr", "JHipster", "OpenAPI Generator"]
  scaffolding:
    entity: |
      @Entity
      @Table(name = "users")
      public class User {
          @Id
          @GeneratedValue(strategy = GenerationType.UUID)
          private UUID id;
          
          @Column(nullable = false)
          private String name;
          
          @Column(nullable = false, unique = true)
          private String email;
      }

    repository: |
      @Repository
      public interface UserRepository extends JpaRepository<User, UUID> {
          Optional<User> findByEmail(String email);
          List<User> findByNameContaining(String name);
      }

    service: |
      @Service
      @Transactional
      public class UserService {
          private final UserRepository userRepository;
          
          public User create(CreateUserDto dto) {
              User user = new User();
              user.setName(dto.getName());
              user.setEmail(dto.getEmail());
              return userRepository.save(user);
          }
      }

kotlin:
  tools: ["Spring Initializr", "Ktor Generator", "Exposed"]
  scaffolding:
    entity: |
      @Entity
      @Table(name = "users")
      data class User(
          @Id @GeneratedValue(strategy = GenerationType.UUID)
          val id: UUID = UUID.randomUUID(),
          val name: String,
          val email: String,
          val createdAt: Instant = Instant.now()
      )

# ═══════════════════════════════════════════════════════════════
# C# / .NET
# ═══════════════════════════════════════════════════════════════

csharp:
  tools: ["dotnet new", "EF Core scaffolding", "NSwag"]
  commands:
    - "dotnet new classlib -n MyProject.Domain"
    - "dotnet ef dbcontext scaffold"
  scaffolding:
    entity: |
      public class User
      {
          public Guid Id { get; set; }
          public string Name { get; set; } = string.Empty;
          public string Email { get; set; } = string.Empty;
          public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
      }

    repository: |
      public interface IUserRepository
      {
          Task<User?> GetByIdAsync(Guid id);
          Task<User> CreateAsync(User user);
          Task UpdateAsync(User user);
          Task DeleteAsync(Guid id);
      }

# ═══════════════════════════════════════════════════════════════
# PYTHON
# ═══════════════════════════════════════════════════════════════

python:
  tools: ["cookiecutter", "FastAPI generator", "Django startapp"]
  scaffolding:
    model_sqlalchemy: |
      # models/user.py
      from sqlalchemy import Column, String, DateTime
      from sqlalchemy.dialects.postgresql import UUID

      class User(Base):
          __tablename__ = "users"
          
          id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
          name = Column(String(255), nullable=False)
          email = Column(String(255), nullable=False, unique=True)
          created_at = Column(DateTime, default=datetime.utcnow)

    model_pydantic: |
      # schemas/user.py
      from pydantic import BaseModel, EmailStr

      class UserCreate(BaseModel):
          name: str
          email: EmailStr

      class UserResponse(BaseModel):
          id: UUID
          name: str
          email: str
          created_at: datetime
          
          class Config:
              from_attributes = True

    router_fastapi: |
      # routers/users.py
      @router.post("/", response_model=UserResponse)
      async def create_user(user: UserCreate, db: Session = Depends(get_db)):
          db_user = User(**user.dict())
          db.add(db_user)
          db.commit()
          return db_user

# ═══════════════════════════════════════════════════════════════
# RUBY
# ═══════════════════════════════════════════════════════════════

ruby:
  tools: ["rails generate", "hanami generate"]
  commands:
    - "rails g model User name:string email:string"
    - "rails g controller Users index show create update destroy"
    - "rails g scaffold User name:string email:string"

# ═══════════════════════════════════════════════════════════════
# PHP
# ═══════════════════════════════════════════════════════════════

php:
  tools: ["artisan make", "symfony make"]
  commands:
    laravel:
      - "php artisan make:model User -mfsc" # Model, migration, factory, seeder, controller
      - "php artisan make:resource UserResource"
      - "php artisan make:request StoreUserRequest"
    symfony:
      - "php bin/console make:entity User"
      - "php bin/console make:controller UserController"
      - "php bin/console make:crud User"

# ═══════════════════════════════════════════════════════════════
# TYPESCRIPT / NODE.JS
# ═══════════════════════════════════════════════════════════════

typescript:
  tools: ["plop", "hygen", "nx generate", "nest generate"]
  scaffolding:
    model_prisma: |
      // prisma/schema.prisma
      model User {
        id        String   @id @default(uuid())
        name      String
        email     String   @unique
        createdAt DateTime @default(now())
        updatedAt DateTime @updatedAt
      }

    service: |
      // src/services/user.service.ts
      export class UserService {
        constructor(private readonly prisma: PrismaClient) {}
        
        async create(data: CreateUserDto): Promise<User> {
          return this.prisma.user.create({ data });
        }
        
        async findById(id: string): Promise<User | null> {
          return this.prisma.user.findUnique({ where: { id } });
        }
      }

    controller: |
      // src/controllers/user.controller.ts
      export class UserController {
        constructor(private readonly userService: UserService) {}
        
        async create(req: Request, res: Response) {
          const user = await this.userService.create(req.body);
          res.status(201).json(user);
        }
      }

nestjs:
  tools: ["nest g resource", "nest g service", "nest g controller"]
  commands:
    - "nest g resource users" # Full CRUD
    - "nest g service users"
    - "nest g controller users"
    - "nest g module users"

nextjs:
  tools: ["Custom templates", "shadcn-ui add"]
  scaffolding:
    page: |
      // app/users/page.tsx
      export default async function UsersPage() {
        const users = await getUsers();
        return <UserList users={users} />;
      }

    api_route: |
      // app/api/users/route.ts
      export async function GET() {
        const users = await prisma.user.findMany();
        return Response.json(users);
      }

      export async function POST(request: Request) {
        const body = await request.json();
        const user = await prisma.user.create({ data: body });
        return Response.json(user, { status: 201 });
      }

# ═══════════════════════════════════════════════════════════════
# FRONTEND COMPONENTS
# ═══════════════════════════════════════════════════════════════

react:
  tools: ["plop", "hygen", "create-react-component"]
  scaffolding:
    component: |
      // components/UserCard/UserCard.tsx
      interface UserCardProps {
        user: User;
        onEdit?: () => void;
      }

      export function UserCard({ user, onEdit }: UserCardProps) {
        return (
          <div className="user-card">
            <h3>{user.name}</h3>
            <p>{user.email}</p>
            {onEdit && <button onClick={onEdit}>Edit</button>}
          </div>
        );
      }

    hook: |
      // hooks/useUsers.ts
      export function useUsers() {
        return useQuery({
          queryKey: ['users'],
          queryFn: () => api.get<User[]>('/users'),
        });
      }

vue:
  tools: ["vue generate", "nuxi add"]
  scaffolding:
    component: |
      <!-- components/UserCard.vue -->
      <script setup lang="ts">
      interface Props {
        user: User;
      }
      const props = defineProps<Props>();
      const emit = defineEmits<{ edit: [] }>();
      </script>

      <template>
        <div class="user-card">
          <h3>{{ user.name }}</h3>
          <p>{{ user.email }}</p>
        </div>
      </template>

# ═══════════════════════════════════════════════════════════════
# MOBILE
# ═══════════════════════════════════════════════════════════════

swift:
  tools: ["Xcode templates", "SwiftGen"]
  scaffolding:
    model: |
      struct User: Codable, Identifiable {
          let id: UUID
          let name: String
          let email: String
          let createdAt: Date
      }

    view: |
      struct UserView: View {
          let user: User
          
          var body: some View {
              VStack(alignment: .leading) {
                  Text(user.name).font(.headline)
                  Text(user.email).font(.subheadline)
              }
          }
      }

dart:
  tools: ["mason", "very_good_cli"]
  scaffolding:
    model: |
      @freezed
      class User with _$User {
        const factory User({
          required String id,
          required String name,
          required String email,
          required DateTime createdAt,
        }) = _User;
        
        factory User.fromJson(Map<String, dynamic> json) =>
            _$UserFromJson(json);
      }
```

---

## 📋 PHASE 2: CONFIGURE

### Generation Preview:

```
🏗️ GENERATION PREVIEW

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Command: /generate crud User
Entity: User

Files to create:
├── 📁 prisma/
│   └── schema.prisma (update)
├── 📁 src/
│   ├── 📁 models/
│   │   └── user.model.ts (new)
│   ├── 📁 services/
│   │   └── user.service.ts (new)
│   ├── 📁 controllers/
│   │   └── user.controller.ts (new)
│   ├── 📁 dto/
│   │   ├── create-user.dto.ts (new)
│   │   └── update-user.dto.ts (new)
│   └── 📁 __tests__/
│       └── user.service.test.ts (new)
└── 📁 routes/
    └── index.ts (update)

Fields:
├── id: UUID (auto)
├── name: string (required)
├── email: string (unique)
├── createdAt: DateTime (auto)
└── updatedAt: DateTime (auto)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ Proceed? (y/n/customize):
```

---

## 📋 PHASE 3-4: GENERATE & INTEGRATE

### Generation Output:

```
🏗️ GENERATING...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/6] Creating Prisma model... ✅
[2/6] Creating user.model.ts... ✅
[3/6] Creating user.service.ts... ✅
[4/6] Creating user.controller.ts... ✅
[5/6] Creating DTOs... ✅
[6/6] Creating tests... ✅

Integrating:
├── Updated prisma/schema.prisma
├── Updated src/routes/index.ts
└── Updated src/services/index.ts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 5: VERIFY

### Verification & Next Steps:

```
✅ GENERATION COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Created: 7
Lines Added: 245

Compilation: ✅ No errors
Linting: ✅ No issues
Tests: ⚠️ 1 test file needs implementation

Generated Endpoints:
├── POST   /api/users     → Create
├── GET    /api/users     → List
├── GET    /api/users/:id → Get by ID
├── PUT    /api/users/:id → Update
└── DELETE /api/users/:id → Delete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Run migration: npx prisma migrate dev
2️⃣ Complete tests: npm test
3️⃣ Test API: /debug api users
4️⃣ Generate more: /generate [type] [name]

Enter number:
```

---

## 🔧 TEMPLATES REFERENCE

### Common Generation Patterns:

```yaml
patterns:
  # Model + Repository + Tests
  model:
    creates:
      - "{name}.model.ts"
      - "{name}.repository.ts"
      - "{name}.model.test.ts"

  # Full CRUD Stack
  crud:
    creates:
      - "{name}.model.ts"
      - "{name}.service.ts"
      - "{name}.controller.ts"
      - "{name}.dto.ts"
      - "{name}.repository.ts"
      - "{name}.routes.ts"
      - "{name}.test.ts"
    integrates:
      - "routes/index.ts"
      - "prisma/schema.prisma"

  # React Component
  component:
    creates:
      - "{Name}/{Name}.tsx"
      - "{Name}/{Name}.test.tsx"
      - "{Name}/{Name}.module.css"
      - "{Name}/index.ts"

  # API Route (Next.js)
  api:
    creates:
      - "app/api/{name}/route.ts"
      - "app/api/{name}/[id]/route.ts"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Use project patterns
  - Infer structure from existing code
  - Apply detected naming conventions
  - Reuse existing imports

  # Minimal prompts
  - Single command with defaults
  - Preview before generate
  - Batch similar files
```

---

## 📜 RULES APPLIED

| Phase     | Rules                |
| --------- | -------------------- |
| Detect    | `context-management` |
| Configure | `stop-conditions`    |
| Generate  | `edit-verification`  |
| Integrate | `safety`             |
| Verify    | `evidence`           |

---

## 🎨 MULTI-MODAL OUTPUT (v3.1)

```yaml
multi_modal_output:
  description: "Generate multiple output formats"

  formats:
    code:
      languages:
        - "TypeScript"
        - "Go"
        - "Python"
        - "Rust"
        - "Java"
      patterns: ["CRUD", "Repository", "Factory"]

    documentation:
      formats:
        - "Markdown"
        - "OpenAPI 3.1"
        - "AsyncAPI"
        - "GraphQL SDL"

    config:
      formats:
        - "YAML"
        - "JSON"
        - "TOML"
        - "HCL"

    diagrams:
      formats:
        - "Mermaid"
        - "PlantUML"
        - "D2"
      types: ["ER", "Sequence", "Architecture"]

  templates:
    crud:
      description: "Full CRUD operations"
      includes: ["Model", "Repository", "Service", "Controller", "Tests"]

    api:
      description: "REST/GraphQL endpoints"
      includes: ["Routes", "DTOs", "Validation", "OpenAPI"]

    component:
      description: "UI component with tests"
      includes: ["Component", "Styles", "Stories", "Tests"]

  commands:
    generate: "/generate [type] [name]"
    diagram: "/generate diagram [type] [name]"
```

---

## 🛡️ GENERATION QUALITY (v3.1)

```yaml
generation_quality:
  description: "Ensure generated code meets standards"

  post_generate:
    lint_check: true
    type_check: true
    import_organize: true
    format: true

  auto_fix:
    enabled: true
    safe_only: true

  validation:
    compile: "Language-specific build"
    tests: "Generate tests alongside"
    coverage: "Meet project threshold"

  integration:
    barrel_files: "Update index.ts exports"
    routes: "Register in router"
    di: "Add to container"

  commands:
    validate: "/generate --validate"
    dry_run: "/generate --dry [type] [name]"
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command                    | Description      |
| -------------------------- | ---------------- |
| `/generate [type] [name]`  | Generate code    |
| `/generate crud [name]`    | Full CRUD stack  |
| `/generate api [name]`     | REST/GraphQL API |
| `/generate component`      | UI component     |
| `/generate diagram [type]` | Generate diagram |
| `/generate --dry`          | Preview only     |
| `/generate --validate`     | With validation  |

---

_DOMYH Agent v4.3 • Generate Pro v3.1 • Multi-Modal + Quality Gates_
