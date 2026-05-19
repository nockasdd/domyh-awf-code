---
library: zod
version: 4.x
latest: true
category: frontend
official_docs: https://zod.dev
last_updated: 2026-03-20
last_checked: 2026-03-21
source: zod.dev + curated
---

# Zod v4

> Zod — TypeScript-first schema validation with static type inference.
> 30M+ npm/week. v4: 14x faster string parsing, 57% smaller bundle, JSON Schema built-in.
> Docs: https://zod.dev

## Version Comparison

| Feature | v3 | v4 |
|:--------|:---|:---|
| String parse speed | baseline | 14x faster |
| Array parse speed | baseline | 7x faster |
| Object parse speed | baseline | 6.5x faster |
| Bundle size | baseline | 57% smaller |
| `z.interface()` | ❌ | ✅ (recursive, optional keys) |
| `z.email()` top-level | ❌ | ✅ (deprecated on string) |
| `.toJSONSchema()` | ❌ (need zod-to-json-schema) | ✅ Built-in |
| `z.file()` | ❌ | ✅ |
| `z.stringbool()` | ❌ | ✅ |
| `z.templateLiteral()` | ❌ | ✅ |
| `@zod/mini` | ❌ | ✅ (85% smaller) |
| Error API | `message`, `invalid_type_error` | Unified `error` param |

## Installation

```bash
npm install zod            # v4 (latest)
npm install zod@3          # v3 (legacy)

# Minimal bundle (85% smaller)
npm install @zod/mini
```

## Primitives & Basics

```ts
import { z } from 'zod';

// Primitives
const str = z.string();
const num = z.number();
const bool = z.boolean();
const date = z.date();
const bigint = z.bigint();
const symbol = z.symbol();
const undef = z.undefined();
const nul = z.null();
const voidType = z.void();
const any = z.any();
const unknown = z.unknown();
const never = z.never();

// Parse (throws on error)
str.parse("hello");     // "hello"
str.parse(42);          // throws ZodError

// Safe parse (returns result object)
const result = str.safeParse("hello");
if (result.success) {
    result.data;  // "hello"
} else {
    result.error; // ZodError
}
```

## Top-Level Format Validators (v4 NEW)

```ts
// ⚠️ v4: Use top-level functions instead of z.string().email()
z.email();                             // email (z.string().email() deprecated)
z.url();                               // URL
z.uuid();                              // UUID
z.emoji();                             // emoji
z.iso.datetime();                      // ISO 8601 datetime
z.iso.date();                          // ISO date
z.iso.time();                          // ISO time

// Custom email regex
z.email({ pattern: "html5" });         // HTML5 email regex
z.email({ pattern: /custom-regex/ });  // custom regex
```

## String & Number Validations

```ts
z.string().min(1, "Required")         // min length
z.string().max(255)                    // max length
z.string().length(5)                   // exact length
z.string().regex(/^[a-z]+$/)           // regex
z.string().includes("@")              // contains
z.string().startsWith("https://")      // starts with
z.string().endsWith(".com")            // ends with
z.string().trim()                      // trim whitespace
z.string().toLowerCase()               // transform to lowercase
z.string().toUpperCase()               // transform to uppercase

z.number().int()                       // integer only
z.number().positive()                  // > 0
z.number().negative()                  // < 0
z.number().nonnegative()               // >= 0
z.number().min(1)                      // >= 1
z.number().max(100)                    // <= 100
z.number().multipleOf(5)               // divisible by 5
z.number().finite()                    // no Infinity
z.number().safe()                      // within MAX_SAFE_INTEGER
// ⚠️ v4: z.number() only accepts safe integers by default, ±Infinity rejected
```

## Objects — z.object() vs z.interface() (v4 NEW)

```ts
// z.object() — works like v3 (still supported)
const UserSchema = z.object({
    name: z.string().min(1),
    email: z.email(),
    age: z.number().int().min(0).optional(),
    role: z.enum(["admin", "user", "moderator"]),
});

// z.interface() — v4 NEW: better optional handling + recursive types
const UserInterface = z.interface({
    name: z.string(),
    email: z.email(),
    "age?": z.number(),          // ⚠️ "?" suffix = key optional (not just value optional)
    role: z.enum(["admin", "user"]),
});
// With z.interface(): "age?" means the key CAN be omitted entirely
// With z.object():    .optional() means value can be undefined but key exists

// Recursive types (v4 — no z.lazy() needed!)
const CategorySchema = z.interface({
    name: z.string(),
    get children() { return z.array(CategorySchema); },  // recursive via getter
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Object methods (same as v3)
UserSchema.partial();                  // all fields optional
UserSchema.required();                 // all fields required
UserSchema.pick({ name: true });       // pick fields
UserSchema.omit({ age: true });        // omit fields
UserSchema.extend({ phone: z.string() });
UserSchema.merge(OtherSchema);
UserSchema.passthrough();              // allow unknown keys
UserSchema.strict();                   // reject unknown keys
UserSchema.strip();                    // strip unknown keys (default)
```

## Arrays & Tuples

```ts
z.array(z.string());                   // string[]
z.array(z.number()).min(1).max(10);    // 1-10 numbers
z.array(z.string()).nonempty();        // at least 1 element
z.string().array();                    // equivalent shorthand

z.tuple([z.string(), z.number()]);     // [string, number]
z.tuple([z.string(), z.number()]).rest(z.boolean());
```

## Unions & Discriminated Unions

```ts
z.union([z.string(), z.number()]);     // string | number
z.string().or(z.number());            // equivalent

// Discriminated union (better error messages)
const EventSchema = z.discriminatedUnion("type", [
    z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
    z.object({ type: z.literal("keypress"), key: z.string() }),
    z.object({ type: z.literal("scroll"), delta: z.number() }),
]);
```

## Transforms & Coercion

```ts
// Transform
const NumberFromString = z.string().transform(Number);
NumberFromString.parse("42");  // 42

// Coerce
z.coerce.string();    // String(input)
z.coerce.number();    // Number(input)
z.coerce.boolean();   // Boolean(input)
z.coerce.date();      // new Date(input)

// v4 NEW: z.stringbool() — smart string-to-boolean
z.stringbool();
// "true", "on", "yes", "1"  → true
// "false", "off", "no", "0" → false

// Refine — custom validation
const PasswordSchema = z.string()
    .min(8)
    .refine(s => /[A-Z]/.test(s), "Must contain uppercase")
    .refine(s => /[0-9]/.test(s), "Must contain number");

// Superrefine — detailed errors
const FormSchema = z.object({
    password: z.string(),
    confirm: z.string(),
}).superRefine((data, ctx) => {
    if (data.password !== data.confirm) {
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: "Passwords don't match",
            path: ["confirm"],
        });
    }
});
```

## File Validation (v4 NEW)

```ts
const FileSchema = z.file()
    .min(1024)                         // min 1KB
    .max(5 * 1024 * 1024)             // max 5MB
    .type("image/png");                // MIME type

// Usage with form data
const UploadSchema = z.object({
    avatar: z.file().type("image/*").max(2 * 1024 * 1024),
    document: z.file().type("application/pdf"),
});
```

## JSON Schema Conversion (v4 NEW)

```ts
import { z } from 'zod';

const UserSchema = z.object({
    name: z.string(),
    email: z.email(),
    age: z.number().int().min(0),
});

// Convert to JSON Schema — built-in, no external lib needed
const jsonSchema = z.toJSONSchema(UserSchema);
// {
//   type: "object",
//   properties: {
//     name: { type: "string" },
//     email: { type: "string", format: "email" },
//     age: { type: "integer", minimum: 0 }
//   },
//   required: ["name", "email", "age"]
// }

// Useful for: OpenAPI spec, dynamic form generation, AI structured output
```

## Template Literals (v4 NEW)

```ts
const CSSUnit = z.templateLiteral([z.number(), z.literal("px")]);
CSSUnit.parse("42px");   // ✅
CSSUnit.parse("42em");   // ❌

const Route = z.templateLiteral([z.literal("/api/"), z.string()]);
Route.parse("/api/users");  // ✅
```

## Metadata & Registry (v4 NEW)

```ts
// Attach metadata to schemas
const UserSchema = z.object({
    name: z.string(),
    email: z.email(),
}).meta({ tableName: "users", description: "User account" });

// Global registry
const registry = z.registry<{ description: string }>();
registry.register(UserSchema, { description: "User schema" });
```

## With react-hook-form

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
    email: z.email(),              // v4: top-level
    password: z.string().min(8),
});

type FormData = z.infer<typeof schema>;

const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
});
```

## With Server Actions (Next.js)

```ts
"use server";
import { z } from "zod";

const CreatePostSchema = z.object({
    title: z.string().min(1).max(200),
    content: z.string().min(1),
});

export async function createPost(formData: FormData) {
    const result = CreatePostSchema.safeParse({
        title: formData.get("title"),
        content: formData.get("content"),
    });

    if (!result.success) {
        return { errors: result.error.flatten().fieldErrors };
    }

    await db.post.create({ data: result.data });
}
```

## Error Handling (v4 CHANGED)

```ts
// v4: Unified error parameter (replaces message, invalid_type_error, required_error)
const schema = z.string({
    error: "Custom error message",      // unified error param
});

// Or function form for dynamic messages
const schema2 = z.string({
    error: (issue) => `Expected string, got ${typeof issue.input}`,
});

// Error formatting
const result = schema.safeParse(42);
if (!result.success) {
    result.error.issues;               // detailed issues array
    z.prettifyError(result.error);     // v4: human-readable format
    result.error.flatten();            // flat format for forms (still works)
}
```

## Migration from v3

```ts
// ⚠️ BREAKING: z.string().email() → z.email()
// v3:
z.string().email()
// v4 (preferred):
z.email()

// ⚠️ BREAKING: Error customization
// v3:
z.string({ required_error: "Required", invalid_type_error: "Must be string" })
// v4:
z.string({ error: "Must be a valid string" })

// ⚠️ BREAKING: z.number() rejects ±Infinity by default

// ⚠️ BREAKING: .default() + .optional() behavior changed
// v4: default value ALWAYS returned even if key missing from input
```

## Gotchas

⚠️ **v4 install**: `npm install zod` now installs v4. Pin `zod@3` for legacy.

⚠️ **`z.email()` top-level**: `z.string().email()` still works at runtime but deprecated in TypeScript.

⚠️ **`z.interface()` vs `z.object()`**: Use `z.interface()` for recursive types and true optional keys.

⚠️ **JSON Schema**: Use `z.toJSONSchema(schema)` — no more `zod-to-json-schema` package needed.

⚠️ **Error API**: Unified `error` param replaces `message`, `invalid_type_error`, `required_error`.

⚠️ **Bundle size**: Use `@zod/mini` for 85% smaller bundle in performance-sensitive apps.

⚠️ **`.parse()` throws**: Use `.safeParse()` for non-throwing validation. Check `result.success`.

⚠️ **Type inference**: Always use `z.infer<typeof Schema>` — never manually type.

⚠️ **`.transform()` changes type**: After transform, inferred type changes. Input ≠ output type.

⚠️ **Default values + optional**: v4 ALWAYS returns caught/default values, even if key missing from input.

⚠️ **Performance**: Schema *creation* may be slower (JIT compilation), but *parsing* is 7-14x faster.
