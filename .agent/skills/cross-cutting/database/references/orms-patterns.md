## 📦 MySQL 8.x

### MySQL Core Patterns

```sql
-- ✅ Parameterized queries (use ? placeholder)
SELECT id, name FROM users WHERE id = ?;

-- ✅ Indexes
CREATE INDEX idx_users_email ON users(email);

-- ✅ Full-text search
CREATE FULLTEXT INDEX idx_products_search
    ON products(name, description);

SELECT * FROM products
WHERE MATCH(name, description) AGAINST('laptop' IN NATURAL LANGUAGE MODE);

-- ✅ Window functions
SELECT id, name, price,
       ROW_NUMBER() OVER (ORDER BY price DESC) AS rank,
       AVG(price) OVER () AS avg_price
FROM products;
```

### MySQL vs PostgreSQL

| Feature          | PostgreSQL              | MySQL             |
| ---------------- | ----------------------- | ----------------- |
| JSON Support     | JSONB (binary, indexed) | JSON (text-based) |
| Full-text Search | Built-in tsquery        | FULLTEXT index    |
| CTEs             | Optimized               | Less optimized    |
| Arrays           | Native                  | JSON workaround   |
| Enums            | Native                  | Limited           |
| Partitioning     | Declarative             | Hash, Range, List |
| Replication      | Logical + Physical      | Group Replication |

---

## 📦 ORMs Comparison (2025)

### Node.js/TypeScript

| ORM           | Type Safety | Performance | Bundle Size | Best For              |
| ------------- | ----------- | ----------- | ----------- | --------------------- |
| **Prisma 7**  | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐    | 90% smaller | Type-safe, Next.js    |
| **Drizzle**   | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  | ~7.4kb      | Serverless, SQL-first |
| **TypeORM**   | ⭐⭐⭐⭐    | ⭐⭐⭐      | Medium      | NestJS, Enterprise    |
| **Sequelize** | ⭐⭐⭐      | ⭐⭐⭐      | Medium      | Legacy, Beginner      |
| **Kysely**    | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  | Tiny        | Type-safe SQL builder |

### Python

| ORM                | Use Case                         |
| ------------------ | -------------------------------- |
| **SQLAlchemy 2.0** | Industry standard, async support |
| **Tortoise ORM**   | Async-first, Django-like         |
| **SQLModel**       | Pydantic + SQLAlchemy            |

### Go

| Library  | Use Case                    |
| -------- | --------------------------- |
| **GORM** | Full-featured ORM           |
| **sqlc** | Code generation from SQL    |
| **sqlx** | Extensions for database/sql |
| **pgx**  | PostgreSQL driver           |

---

## 🔷 Prisma Patterns

### Schema Definition

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@index([createdAt])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([published, createdAt])
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Prisma Queries

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

// ✅ Find with relations
const users = await prisma.user.findMany({
  where: { role: "ADMIN" },
  include: { posts: { where: { published: true } } },
  orderBy: { createdAt: "desc" },
  take: 10,
});

// ✅ Create with nested relations
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
    posts: {
      create: [{ title: "Hello World", content: "First post!" }],
    },
  },
  include: { posts: true },
});

// ✅ Transaction (atomic operations)
const [updatedUser, newPost] = await prisma.$transaction([
  prisma.user.update({
    where: { id: userId },
    data: { postCount: { increment: 1 } },
  }),
  prisma.post.create({
    data: { title: "New Post", authorId: userId },
  }),
]);

// ✅ Interactive transaction
await prisma.$transaction(async (tx) => {
  const balance = await tx.account.findUnique({
    where: { id: fromAccountId },
  });

  if (balance.amount < transferAmount) {
    throw new Error("Insufficient funds");
  }

  await tx.account.update({
    where: { id: fromAccountId },
    data: { amount: { decrement: transferAmount } },
  });

  await tx.account.update({
    where: { id: toAccountId },
    data: { amount: { increment: transferAmount } },
  });
});
```

---

## 🔶 Drizzle Patterns

### Schema Definition

```typescript
// schema.ts
import { pgTable, text, timestamp, boolean, index } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

export const users = pgTable(
  "users",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => crypto.randomUUID()),
    email: text("email").notNull().unique(),
    name: text("name"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => ({
    emailIdx: index("users_email_idx").on(table.email),
  }),
);

export const posts = pgTable(
  "posts",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => crypto.randomUUID()),
    title: text("title").notNull(),
    content: text("content"),
    published: boolean("published").default(false),
    authorId: text("author_id")
      .notNull()
      .references(() => users.id),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => ({
    authorIdx: index("posts_author_idx").on(table.authorId),
  }),
);

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### Drizzle Queries

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { eq, and, desc } from "drizzle-orm";
import * as schema from "./schema";

const db = drizzle(pool, { schema });

// ✅ SQL-like query API
const activeUsers = await db
  .select()
  .from(schema.users)
  .where(eq(schema.users.active, true))
  .orderBy(desc(schema.users.createdAt))
  .limit(10);

// ✅ Relational query API
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: eq(schema.posts.published, true),
    },
  },
});

// ✅ Transaction
await db.transaction(async (tx) => {
  await tx
    .update(schema.accounts)
    .set({ balance: sql`balance - 100` })
    .where(eq(schema.accounts.id, 1));

  await tx
    .update(schema.accounts)
    .set({ balance: sql`balance + 100` })
    .where(eq(schema.accounts.id, 2));
});
```

---
