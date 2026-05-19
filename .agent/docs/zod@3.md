---
library: zod
version: 3
latest: false
category: frontend
official_docs: https://zod.dev
last_updated: 2026-03-20
source: zod.dev + curated
---

# Zod v3

> Zod v3 — TypeScript-first schema validation with static type inference.
> ⚠️ This is LEGACY. For latest, use `zod.md` (Zod v4).
> Docs: https://zod.dev

## Installation

```bash
npm install zod
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

## String Validations

```ts
z.string().min(1, "Required")         // min length
z.string().max(255)                    // max length
z.string().length(5)                   // exact length
z.string().email("Invalid email")      // email format
z.string().url()                       // URL format
z.string().uuid()                      // UUID format
z.string().cuid()                      // CUID format
z.string().regex(/^[a-z]+$/)           // regex
z.string().includes("@")              // contains
z.string().startsWith("https://")      // starts with
z.string().endsWith(".com")            // ends with
z.string().trim()                      // trim whitespace
z.string().toLowerCase()               // transform to lowercase
z.string().toUpperCase()               // transform to uppercase
z.string().datetime()                  // ISO 8601 datetime
z.string().ip()                        // IP address (v4 or v6)
```

## Number Validations

```ts
z.number().int()                       // integer only
z.number().positive()                  // > 0
z.number().negative()                  // < 0
z.number().nonnegative()               // >= 0
z.number().min(1)                      // >= 1
z.number().max(100)                    // <= 100
z.number().multipleOf(5)               // divisible by 5
z.number().finite()                    // no Infinity
z.number().safe()                      // within Number.MAX_SAFE_INTEGER
```

## Objects

```ts
const UserSchema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
    age: z.number().int().min(0).optional(),
    role: z.enum(["admin", "user", "moderator"]),
    settings: z.object({
        theme: z.enum(["light", "dark"]).default("light"),
        notifications: z.boolean().default(true),
    }),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;
// { name: string; email: string; age?: number; role: "admin" | "user" | "moderator"; settings: { ... } }

// Parse
const user = UserSchema.parse(data);

// Object methods
UserSchema.partial();                  // all fields optional
UserSchema.required();                 // all fields required
UserSchema.pick({ name: true, email: true });  // pick fields
UserSchema.omit({ age: true });        // omit fields
UserSchema.extend({ phone: z.string() });      // add fields
UserSchema.merge(OtherSchema);         // merge schemas
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
z.tuple([z.string(), z.number()]).rest(z.boolean());  // [string, number, ...boolean[]]
```

## Unions & Discriminated Unions

```ts
// Union
z.union([z.string(), z.number()]);     // string | number
z.string().or(z.number());            // equivalent

// Discriminated union (better error messages)
const EventSchema = z.discriminatedUnion("type", [
    z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
    z.object({ type: z.literal("keypress"), key: z.string() }),
    z.object({ type: z.literal("scroll"), delta: z.number() }),
]);
```

## Transforms & Refinements

```ts
// Transform — change value
const NumberFromString = z.string().transform(Number);
NumberFromString.parse("42");  // 42

// Coerce — auto-convert input
z.coerce.string();    // String(input)
z.coerce.number();    // Number(input)
z.coerce.boolean();   // Boolean(input)
z.coerce.date();      // new Date(input)

// Refine — custom validation
const PasswordSchema = z.string()
    .min(8)
    .refine(s => /[A-Z]/.test(s), "Must contain uppercase")
    .refine(s => /[0-9]/.test(s), "Must contain number")
    .refine(s => /[!@#$%]/.test(s), "Must contain special char");

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

## Records, Maps & Sets

```ts
z.record(z.string(), z.number());      // Record<string, number>
z.map(z.string(), z.object({}));       // Map<string, object>
z.set(z.number());                     // Set<number>
```

## With react-hook-form

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
    email: z.string().email(),
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

## Gotchas

⚠️ **`.parse()` throws**: Use `.safeParse()` for non-throwing validation. Check `result.success`.

⚠️ **Type inference**: Always use `z.infer<typeof Schema>` — never manually type. Schema IS the source of truth.

⚠️ **`.transform()` changes type**: After transform, inferred type changes. Input type ≠ output type.

⚠️ **`.coerce`**: Auto-converts inputs. `z.coerce.number()` converts `"42"` → `42`. Use for form data.

⚠️ **Default values**: `z.string().default("hello")` — only used if value is `undefined`, NOT `null`.

⚠️ **`.optional()` vs `.nullable()`**: `optional()` = `T | undefined`. `nullable()` = `T | null`. Use `.nullish()` for both.

⚠️ **Discriminated unions**: `z.discriminatedUnion()` gives MUCH better error messages than `z.union()`.

⚠️ **Error formatting**: Use `error.flatten()` for forms, `error.format()` for nested objects.
