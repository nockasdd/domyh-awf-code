---
library: supabase
version: latest
latest: true
category: database
official_docs: https://supabase.com/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# Supabase

> Supabase — Open source Firebase alternative. PostgreSQL + Auth + Storage + Realtime.
> Docs: https://supabase.com/docs

## Installation

```bash
npm install @supabase/supabase-js
```

```ts
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// With TypeScript types (generated)
// npx supabase gen types typescript --project-id YOUR_PROJECT > src/types/database.ts
import type { Database } from './types/database';
const supabase = createClient<Database>(url, key);
```

## Database Queries

```ts
// SELECT
const { data, error } = await supabase
  .from('posts')
  .select('*, author:users(name, email)')
  .eq('published', true)
  .order('created_at', { ascending: false })
  .range(0, 9);

// INSERT
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'New Post', content: 'Hello' })
  .select()
  .single();

// UPDATE
const { error } = await supabase
  .from('posts')
  .update({ title: 'Updated' })
  .eq('id', 1);

// DELETE
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', 1);

// RPC (stored procedures)
const { data } = await supabase.rpc('get_top_posts', { limit_count: 10 });

// UPSERT (insert or update)
const { data, error } = await supabase
  .from('users')
  .upsert(
    { username: 'supabot', bio: 'Updated bio' },
    { onConflict: 'username' }
  )
  .select();
```

## Filters Reference

```ts
// Comparison filters
.eq('column', value)         // column = value
.neq('column', value)        // column != value
.gt('column', value)         // column > value
.gte('column', value)        // column >= value
.lt('column', value)         // column < value
.lte('column', value)        // column <= value

// Pattern matching
.like('name', '%Lu%')        // case-sensitive LIKE
.ilike('name', '%lu%')       // case-insensitive ILIKE

// NULL / Boolean checks
.is('deleted_at', null)      // IS NULL
.is('active', true)          // IS TRUE

// Array / set filters
.in('status', ['active', 'pending'])  // IN (...)
.contains('tags', ['urgent'])         // @> (array/jsonb contains)
.containedBy('days', ['mon', 'tue'])  // <@ (contained by)

// Range filters (for range columns)
.rangeGt('during', '[2024-01-01, 2024-02-01)')   // range > range
.rangeGte('during', '[2024-01-01, 2024-02-01)')  // range >= range
.rangeLt('during', '[2024-01-01, 2024-02-01)')   // range < range
.rangeLte('during', '[2024-01-01, 2024-02-01)')  // range <= range

// Full text search
.textSearch('content', 'react & nextjs', { type: 'websearch' })

// Logical operators
.or('status.eq.active, status.eq.pending')  // OR
.not('status', 'eq', 'deleted')             // NOT

// ⚠️ Filters MUST come after .select()/.update()/.delete(), not before!
```

## Modifiers

```ts
// Order
.order('created_at', { ascending: false })
.order('name', { ascending: true, nullsFirst: false })

// Pagination
.range(0, 9)                  // rows 0-9 (10 rows per page)
.limit(10)                    // max 10 rows
.limit(1, { foreignTable: 'cities' })  // limit on joined table

// Single row
.single()                     // returns object (throws if 0 or 2+ rows)
.maybeSingle()                // returns object | null (throws if 2+ rows)

// Count
.select('*', { count: 'exact', head: true })  // count without data

// Abort signal
.select().abortSignal(controller.signal)
```

## Auth

```ts
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
  options: {
    emailRedirectTo: 'http://localhost:3000/welcome',
    data: { full_name: 'John Doe' },  // user_metadata
  },
});

// Sign in with password
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123',
});

// OAuth (Google, GitHub, Apple, Discord, etc.)
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'http://localhost:3000/callback',
    scopes: 'email profile',
  },
});

// Magic link (passwordless)
const { error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: { emailRedirectTo: 'http://localhost:3000/dashboard' },
});

// Phone OTP
const { error } = await supabase.auth.signInWithOtp({
  phone: '+1234567890',
});
// Verify OTP
const { data, error } = await supabase.auth.verifyOtp({
  phone: '+1234567890',
  token: '123456',
  type: 'sms',
});

// Get current user
const { data: { user } } = await supabase.auth.getUser();

// Get session
const { data: { session } } = await supabase.auth.getSession();

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  // event: 'SIGNED_IN' | 'SIGNED_OUT' | 'TOKEN_REFRESHED' |
  //        'USER_UPDATED' | 'PASSWORD_RECOVERY'
  console.log(event, session);
});

// Update user
const { data, error } = await supabase.auth.updateUser({
  password: 'new-password',
  data: { full_name: 'Updated Name' },
});

// Password reset
await supabase.auth.resetPasswordForEmail('user@example.com', {
  redirectTo: 'http://localhost:3000/reset-password',
});

// Sign out
await supabase.auth.signOut();
```

## Storage

```ts
// Upload
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`public/${userId}.png`, file, { contentType: 'image/png' });

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar.png');
```

## Realtime

```ts
const channel = supabase
  .channel('table-changes')
  .on('postgres_changes', {
    event: '*', // INSERT | UPDATE | DELETE
    schema: 'public',
    table: 'messages',
  }, (payload) => {
    console.log('Change:', payload);
  })
  .subscribe();

// Cleanup
supabase.removeChannel(channel);
```

## Edge Functions (Deno)

```ts
// supabase/functions/hello/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  );

  const { data } = await supabase.from('posts').select('*');
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  });
});
```

```bash
# Deploy
supabase functions serve hello --env-file .env.local  # local dev
supabase functions deploy hello                        # deploy to production
```

## Row Level Security (RLS)

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- SELECT policy: users see own posts
CREATE POLICY "Users can view own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);

-- INSERT policy: users create own posts
CREATE POLICY "Users can create posts" ON posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- UPDATE policy: users update own posts
CREATE POLICY "Users can update own posts" ON posts
  FOR UPDATE USING (auth.uid() = user_id);

-- Public read access
CREATE POLICY "Anyone can read" ON posts
  FOR SELECT USING (true);

-- Role-based access
CREATE POLICY "Admins can do anything" ON posts
  USING (auth.jwt() ->> 'role' = 'admin');
```

## AI & Vectors (pgvector)

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(1536)  -- OpenAI ada-002 dimension
);

-- Similarity search function
CREATE FUNCTION match_documents(
  query_embedding VECTOR(1536),
  match_threshold FLOAT DEFAULT 0.78,
  match_count INT DEFAULT 10
) RETURNS TABLE (id BIGINT, content TEXT, similarity FLOAT) AS $$
  SELECT id, content, 1 - (embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (embedding <=> query_embedding) > match_threshold
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$ LANGUAGE SQL STABLE;
```

```ts
// Use from supabase-js
const { data } = await supabase.rpc('match_documents', {
  query_embedding: embedding,  // from OpenAI/Gemini
  match_threshold: 0.78,
  match_count: 5,
});
```

## Modules

| Module | Description |
|:-------|:-----------|
| **AI & Vectors** | pgvector + embeddings for semantic search |
| **Cron** | pg_cron for scheduled jobs |
| **Queues** | pgmq for message queues |
| **Data REST API** | Auto-generated REST from PostgreSQL schema |
| **GraphQL API** | Auto-generated GraphQL from PostgreSQL schema |

## Type Generation

```bash
# Generate TypeScript types from database schema
npx supabase gen types typescript --project-id YOUR_PROJECT > src/types/database.ts

# Usage
import type { Database } from './types/database';
const supabase = createClient<Database>(url, key);
// Now fully typed: supabase.from('posts').select('*') → typed rows
```

## Realtime

```ts
// Subscribe to database changes
const channel = supabase
  .channel('posts-changes')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change:', payload.eventType, payload.new);
    }
  )
  .subscribe();

// Presence — track online users
const presenceChannel = supabase
  .channel('online-users')
  .on('presence', { event: 'sync' }, () => {
    const state = presenceChannel.presenceState();
    console.log('Online:', Object.keys(state).length);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await presenceChannel.track({ user_id: '123', online_at: new Date() });
    }
  });

// Broadcast — send ephemeral messages
const broadcastChannel = supabase.channel('room-1');
broadcastChannel.send({ type: 'broadcast', event: 'cursor', payload: { x: 100, y: 200 } });

// Cleanup
supabase.removeChannel(channel);
```

## Storage

```ts
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`public/${userId}.png`, file, {
    cacheControl: '3600',
    upsert: true,
  });

// Download file
const { data: blob } = await supabase.storage
  .from('avatars')
  .download('public/avatar.png');

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar.png');

// List files
const { data: files } = await supabase.storage
  .from('avatars')
  .list('public', { limit: 100, offset: 0 });

// Delete file
await supabase.storage.from('avatars').remove(['public/old.png']);
```

## Gotchas

⚠️ **RLS required**: Row Level Security must be enabled for client-side queries. Without policies, NO rows visible.

⚠️ **Anon key is public**: Use `service_role` key only on server-side — it bypasses RLS.

⚠️ **`.select()` after insert/update**: Required to get data back. Without it, returns `null`.

⚠️ **`.single()`**: Throws error if 0 or 2+ rows returned. Use `.maybeSingle()` for 0 or 1.

⚠️ **Filters order**: Filters MUST chain after `.select()`/`.update()`/`.delete()`, not before.

⚠️ **`.is()` for NULL**: Use `.is('col', null)`, NOT `.eq('col', null)` — SQL null semantics.

⚠️ **Edge Functions**: Run on Deno, not Node.js. Use `npm:` or `esm.sh` for npm packages.

⚠️ **Type generation**: Run `supabase gen types` after EVERY schema change for type safety.

⚠️ **`onConflict` for upsert**: Must specify the unique column(s). Primary keys must be in `values`.

⚠️ **Auth tokens**: Session auto-refreshes. Listen `onAuthStateChange` for `TOKEN_REFRESHED` events.

⚠️ **Realtime RLS**: `postgres_changes` channel requires SELECT policy on the table.

⚠️ **Storage policies**: Uses RLS. Set bucket to `public: true` for unauthenticated access.

⚠️ **Max 1000 rows default**: API returns max 1000 rows by default. Change in project API settings.

⚠️ **6 client libraries**: JavaScript, Flutter, Python, C#, Swift, Kotlin.
