---
library: drizzle
version: latest
latest: true
category: database
official_docs: https://orm.drizzle.team
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://orm.drizzle.team/llms-full.txt
---

# Drizzle

> Drizzle is a modern TypeScript ORM developers wanna use in their next project. It is lightweight at only ~7.4kb minified+gzipped, and it's tree shakeable with exactly 0 dependencies. It supports every PostgreSQL, MySQL, SQLite and SingleStore database and is serverless-ready by design.

Source: https://orm.drizzle.team/docs/arktype

import Npm from '@mdx/Npm.astro';
import Callout from '@mdx/Callout.astro';

<Callout type="error">
Starting from `drizzle-orm@1.0.0-beta.15`, `drizzle-arktype` has been deprecated in favor of first-class schema generation support within Drizzle ORM itself

You can still use `drizzle-arktype` package but all new update will be added to Drizzle ORM directly
</Callout>


### Install the dependencies

<Npm>
arktype
</Npm>


## Quickstart


#### Step 1 - Install packages
<Npm>
drizzle-orm @aws-sdk/client-rds-data
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query
```typescript copy
import { drizzle } from 'drizzle-orm/aws-data-api/pg';

// These three properties are required. You can also specify
// any property from the RDSDataClient type inside the connection object.
const db = drizzle({ connection: {
  database: process.env['DATABASE']!,
  secretArn: process.env['SECRET_ARN']!,
  resourceArn: process.env['RESOURCE_ARN']!,
}});

await db.select().from(...);
```

If you need to provide your existing driver:

```typescript copy
import { drizzle } from 'drizzle-orm/aws-data-api/pg';
import { RDSDataClient } from '@aws-sdk/client-rds-data';

const rdsClient = new RDSDataClient({ region: 'us-east-1' });

const db = drizzle(rdsClient, {
  database: process.env['DATABASE']!,
  secretArn: process.env['SECRET_ARN']!,
  resourceArn: process.env['RESOURCE_ARN']!,
});

await db.select().from(...);
```


#### Step 1 - Install packages
<Npm>
drizzle-orm
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query
```typescript copy
import 'dotenv/config';
import { drizzle } from 'drizzle-orm/bun-sql';

const db = drizzle(process.env.DATABASE_URL);

const result = await db.select().from(...);
```

If you need to provide your existing driver:
```typescript copy
import 'dotenv/config';
import { drizzle } from 'drizzle-orm/bun-sql';
import { SQL } from 'bun';

const client = new SQL(process.env.DATABASE_URL!);
const db = drizzle({ client });
```


#### Step 1 - Install packages
<Npm>
drizzle-orm
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query
```typescript copy
import { drizzle } from 'drizzle-orm/bun-sqlite';

const db = drizzle();

const result = await db.select().from(...);
```

If you need to provide your existing driver:
```typescript copy
import { drizzle } from 'drizzle-orm/bun-sqlite';
import { Database } from 'bun:sqlite';

const sqlite = new Database('sqlite.db');
const db = drizzle({ client: sqlite });

const result = await db.select().from(...);
```

If you want to use **sync** APIs:
```typescript copy
import { drizzle } from 'drizzle-orm/bun-sqlite';
import { Database } from 'bun:sqlite';

const sqlite = new Database('sqlite.db');
const db = drizzle({ client: sqlite });

const result = db.select().from(users).all();
const result = db.select().from(users).get();
const result = db.select().from(users).values();
const result = db.select().from(users).run();
```


#### Step 1 - Install packages
<Npm>
drizzle-orm
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query

You would need to have either a `wrangler.json` or a `wrangler.toml` file for D1 database and will look something like this:
<CodeTabs items={["wrangler.json", "wrangler.toml"]}>
```json
{
    "name": "YOUR_PROJECT_NAME",
    "main": "src/index.ts",
    "compatibility_date": "2024-09-26",
    "compatibility_flags": [
        "nodejs_compat"
    ],
    "d1_databases": [
        {
            "binding": "BINDING_NAME",
            "database_name": "YOUR_DB_NAME",
            "database_id": "YOUR_DB_ID",
            "migrations_dir": "drizzle/migrations"
        }
    ]
}
```
```toml
name = "YOUR_PROJECT_NAME"
main = "src/index.ts"
compatibility_date = "2022-11-07"
node_compat = true

[[ d1_databases ]]
binding = "BINDING_NAME"
database_name = "YOUR_DB_NAME"
database_id = "YOUR_DB_ID"
migrations_dir = "drizzle/migrations"
```
</CodeTabs>

Make your first D1 query:
```typescript copy
import { drizzle } from 'drizzle-orm/d1';

export interface Env {
  <BINDING_NAME>: D1Database;
}

export default {
  async fetch(request: Request, env: Env) {
    const db = drizzle(env.<BINDING_NAME>);
    const result = await db.select().from(users).all()
    return Response.json(result);
  },
};
```


#### Step 1 - Install packages
<Npm>
drizzle-orm
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query

You would need to have a `wrangler.toml` file for Durable Objects database and will look something like this:
```toml {16-18,21-24}
#:schema node_modules/wrangler/config-schema.json
name = "sqlite-durable-objects"
main = "src/index.ts"
compatibility_date = "2024-11-12"
compatibility_flags = [ "nodejs_compat" ]


#### Step 1 - Install packages
<Npm>
drizzle-orm effect @effect/sql-pg pg
-D drizzle-kit @types/pg
</Npm>


#### Step 2 - Initialize the driver and make a query

Drizzle provides an Effect-native API that integrates with Effect's service pattern. Use `PgDrizzle.makeWithDefaults()` 
to quickly create a Drizzle database instance with sensible defaults (no logging, no caching).

```typescript copy
import 'dotenv/config';
import * as PgDrizzle from 'drizzle-orm/effect-postgres';
import { PgClient } from '@effect/sql-pg';
import * as Effect from 'effect/Effect';
import * as Redacted from 'effect/Redacted';
import { sql } from 'drizzle-orm';
import { types } from 'pg';

// Configure the PgClient layer with type parsers
const PgClientLive = PgClient.layer({
  url: Redacted.make(process.env.DATABASE_URL!),
  types: {
    getTypeParser: (typeId, format) => {
      // Return raw values for date/time types to let Drizzle handle parsing
      if ([1184, 1114, 1082, 1186, 1231, 1115, 1185, 1187, 1182].includes(typeId)) {
        return (val: any) => val;
      }
      return types.getTypeParser(typeId, format);
    },
  },
});

const program = Effect.gen(function*() {
  // Create the database with default services (no logging, no caching)
  const db = yield* PgDrizzle.makeWithDefaults();

  // Execute queries
  const result = yield* db.execute<{ id: number }>(sql`SELECT 1 as id`);
  console.log(result);
});

// Run the program with the PgClient layer
Effect.runPromise(program.pipe(Effect.provide(PgClientLive)));
```


#### Install babel plugin
It's necessary to bundle SQL migration files as string directly to your bundle.
```shell
npm install babel-plugin-inline-import
```


#### Step 1 - Install packages
<Npm>
drizzle-orm @neondatabase/serverless
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query
<CodeTabs items={["Neon HTTP", "Neon Websockets", "node-postgres", "postgres.js"]}>
```typescript
import { drizzle } from 'drizzle-orm/neon-http';

const db = drizzle(process.env.DATABASE_URL);

const result = await db.execute('select 1');
```
<Section> 
```typescript 
import { drizzle } from 'drizzle-orm/neon-serverless';

const db = drizzle(process.env.DATABASE_URL);

const result = await db.execute('select 1');
```
```typescript
// For Node.js - make sure to install the 'ws' and 'bufferutil' packages
import { drizzle } from 'drizzle-orm/neon-serverless';
import ws from 'ws';

const db = drizzle({
  connection: process.env.DATABASE_URL,
  ws: ws,
});

const result = await db.execute('select 1');
```
<Callout type="warning" emoji="⚙️"> 
Additional configuration is required to use WebSockets in environments where the `WebSocket` global is not defined, such as Node.js. 
Add the `ws` and `bufferutil` packages to your project's dependencies, and set `ws` in the Drizzle config. 
</Callout>
</Section> 
```typescript 
// Make sure to install the 'pg' package 
import { drizzle } from 'drizzle-orm/node-postgres';

const db = drizzle(process.env.DATABASE_URL);
 
const result = await db.execute('select 1');
```
```typescript
// Make sure to install the 'postgres' package
import { drizzle } from 'drizzle-orm/postgres-js';

const db = drizzle(process.env.DATABASE_URL);

const result = await db.execute('select 1');
```
</CodeTabs>

If you need to provide your existing drivers:

<CodeTabs items={["Neon HTTP", "Neon Websockets", "node-postgres", "postgres.js"]}>
```typescript
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';

const sql = neon(process.env.DATABASE_URL!);
const db = drizzle({ client: sql });

const result = await db.execute('select 1');
```
<Section> 
```typescript 
import { Pool } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-serverless';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle({ client: pool })

const result = await db.execute('select 1');
```
```typescript
// For Node.js - make sure to install the 'ws' and 'bufferutil' packages
import { Pool, neonConfig } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-serverless';

neonConfig.webSocketConstructor = ws;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle({ client: pool })

const result = await db.execute('select 1');
```
<Callout type="warning" emoji="⚙️"> 
Additional configuration is required to use WebSockets in environments where the `WebSocket` global is not defined, such as Node.js. 
Add the `ws` and `bufferutil` packages to your project's dependencies, and set `ws` in the Drizzle config. 
</Callout>
</Section> 
```typescript 
// Make sure to install the 'pg' package 
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});
const db = drizzle({ client: pool });
 
const result = await db.execute('select 1');
```
```typescript
// Make sure to install the 'postgres' package
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const queryClient = postgres(process.env.DATABASE_URL);
const db = drizzle({ client: queryClient });

const result = await db.execute('select 1');
```
</CodeTabs>


#### Step 1 - Install packages

<Npm>
drizzle-orm postgres
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query

```typescript copy filename="index.ts"
// Make sure to install the 'pg' package
import { drizzle } from 'drizzle-orm/node-postgres'

const db = drizzle(process.env.NILEDB_URL);

const response = await db.select().from(...);
```

If you need to provide your existing driver:

```typescript copy filename="index.ts"
// Make sure to install the 'pg' package
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});
const db = drizzle({ client: pool });

const response = await db.select().from(...);
```


#### Step 1 - Install packages
<Npm>
drizzle-orm
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query
```typescript copy
import { drizzle } from 'drizzle-orm/node-sqlite';

const db = drizzle("sqlite.db");

const result = await db.select().from(...);
```

If you need to provide your existing driver:
```typescript copy
import { drizzle } from 'drizzle-orm/node-sqlite';
import { DatabaseSync } from 'node:sqlite';

const sqlite = new DatabaseSync('sqlite.db');
const db = drizzle({ client: sqlite });

const result = await db.select().from(...);
```

If you want to use **sync** APIs:
```typescript copy
import { drizzle } from 'drizzle-orm/node-sqlite';
import { DatabaseSync } from 'node:sqlite';

const sqlite = new Database('sqlite.db');
const db = drizzle({ client: sqlite });

const result = db.select().from(users).all();
const result = db.select().from(users).get();
const result = db.select().from(users).values();
const result = db.select().from(users).run();
```


#### Install babel plugin
It's necessary to bundle SQL migration files as string directly to your bundle.
```shell
npm install babel-plugin-inline-import
```


#### Step 1 - Install packages

<Npm>
drizzle-orm @electric-sql/pglite
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query
<CodeTabs items={["In-Memory", "In directory", "With extra config options"]}>
```typescript copy"
import { drizzle } from 'drizzle-orm/pglite';

const db = drizzle();

await db.select().from(...);
```
```typescript copy"
import { drizzle } from 'drizzle-orm/pglite';

const db = drizzle('path-to-dir');

await db.select().from(...);
```
```typescript copy"
import { drizzle } from 'drizzle-orm/pglite';

// connection is a native PGLite configuration
const db = drizzle({ connection: { dataDir: 'path-to-dir' }});

await db.select().from(...);
```
</CodeTabs>

If you need to provide your existing driver:

```typescript copy"
import { PGlite } from '@electric-sql/pglite';
import { drizzle } from 'drizzle-orm/pglite';

// In-memory Postgres
const client = new PGlite();
const db = drizzle({ client });

await db.select().from(users);
```


#### Step 1 - Install packages

<Npm>drizzle-orm pg -D drizzle-kit @types/pg</Npm>


#### Step 2 - Initialize the driver and make a query

<CodeTabs items={["Connection URL", "With config", "With existing client"]}>
```typescript copy
import { drizzle } from 'drizzle-orm/node-postgres';

const db = drizzle(process.env.DATABASE_URL);

const result = await db.execute('select 1');

````
```typescript copy
import { drizzle } from 'drizzle-orm/node-postgres';

const db = drizzle({
  connection: {
    connectionString: process.env.DATABASE_URL,
    ssl: true
  }
});

const result = await db.execute('select 1');
````

```typescript copy
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});
const db = drizzle({ client: pool });

const result = await db.execute("select 1");
```

</CodeTabs>


#### Step 1 - Install packages

<Npm>drizzle-orm @neondatabase/serverless -D drizzle-kit</Npm>


#### Step 2 - Initialize the driver and make a query

<CodeTabs items={["Neon HTTP", "Neon WebSockets"]}>
```typescript copy
import { neon, neonConfig } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';

// Required for PlanetScale Postgres connections
neonConfig.fetchEndpoint = (host) => `https://${host}/sql`;

const sql = neon(process.env.DATABASE_URL!);
const db = drizzle({ client: sql });

const result = await db.execute('select 1');

````
<Section>
```typescript copy
import { Pool, neonConfig } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-serverless';

// Required for PlanetScale Postgres connections
neonConfig.pipelineConnect = false;
neonConfig.wsProxy = (host, port) => `${host}/v2?address=${host}:${port}`;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle({ client: pool });

const result = await db.execute('select 1');
````

```typescript copy
// For Node.js environments - install 'ws' package
import ws from "ws";
import { Pool, neonConfig } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-serverless";

neonConfig.webSocketConstructor = ws;
// Required for PlanetScale Postgres connections
neonConfig.pipelineConnect = false;
neonConfig.wsProxy = (host, port) => `${host}/v2?address=${host}:${port}`;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle({ client: pool });

const result = await db.execute("select 1");
```

</Section>
</CodeTabs>

<Callout title="Connection URL format">
  {`postgresql://{username}:{password}@{host}:{port}/postgres?sslmode=verify-full`}
</Callout>

<Callout title="Connection ports" type="info">
  PlanetScale Postgres supports two connection ports:

`5432`: Direct connection to PostgreSQL. Total connections are limited by your cluster's `max_connections` setting.

`6432`: Connection via PgBouncer for connection pooling. Recommended when you have many simultaneous connections.

  </Callout>


#### Step 1 - Install packages

<Npm>drizzle-orm @planetscale/database -D drizzle-kit</Npm>


#### Step 2 - Initialize the driver and make a query

```typescript copy"
import { drizzle } from "drizzle-orm/planetscale-serverless";

const db = drizzle({ connection: {
  host: process.env["DATABASE_HOST"],
  username: process.env["DATABASE_USERNAME"],
  password: process.env["DATABASE_PASSWORD"],
}});

const response = await db.select().from(...)
```

If you need to provide your existing driver

```typescript copy"
import { drizzle } from "drizzle-orm/planetscale-serverless";
import { Client } from "@planetscale/database";

const client = new Client({
  host: process.env["DATABASE_HOST"],
  username: process.env["DATABASE_USERNAME"],
  password: process.env["DATABASE_PASSWORD"],
});

const db = drizzle({ client });
```

Make sure to checkout the PlanetScale official **[MySQL courses](https://planetscale.com/courses/mysql-for-developers)**,
we think they're outstanding 🙌


#### Step 1 - Install packages
<CodeTabs items={["node-postgres (pg)", "postgres.js"]}>
<Npm>
drizzle-orm pg
-D drizzle-kit
</Npm>

<Npm>
drizzle-orm postres
-D drizzle-kit
</Npm>

</CodeTabs>



#### Step 2 - Initialize the driver and make a query
<CodeTabs items={["node-postgres (pg)", "postgres.js"]}>
```typescript 
// Make sure to install the 'pg' package 
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});
const db = drizzle({ client: pool });
 
const result = await db.execute('select 1');
```
```typescript
// Make sure to install the 'postgres' package
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const queryClient = postgres(process.env.DATABASE_URL);
const db = drizzle({ client: queryClient });

const result = await db.execute('select 1');
```
</CodeTabs>


#### Step 1 - Install packages
<Npm>
drizzle-orm@beta @sqlitecloud/drivers
-D drizzle-kit@beta
</Npm>


#### Step 2 - Initialize the driver and make a query
```typescript
import { drizzle } from 'drizzle-orm/sqlite-cloud';

const db = drizzle(process.env.SQLITE_CLOUD_CONNECTION_STRING);

const result = await db.execute('select 1');
```

If you need to provide your existing drivers:

```typescript
import { Database } from '@sqlitecloud/drivers';
import { drizzle } from 'drizzle-orm/sqlite-cloud';

const client = new Database(process.env.SQLITE_CLOUD_CONNECTION_STRING!);
const db = drizzle({ client });

const result = await db.execute('select 1');
```


#### Step 1 - Install packages

<Npm>
drizzle-orm postgres
-D drizzle-kit
</Npm>


#### Step 2 - Initialize the driver and make a query

```typescript copy filename="index.ts"
import { drizzle } from 'drizzle-orm/postgres-js'

const db = drizzle(process.env.DATABASE_URL);

const allUsers = await db.select().from(...);
```

If you need to provide your existing driver:
```typescript copy filename="index.ts"
import { drizzle } from 'drizzle-orm/postgres-js'
import postgres from 'postgres'

const client = postgres(process.env.DATABASE_URL)
const db = drizzle({ client });

const allUsers = await db.select().from(...);
```

If you decide to use connection pooling via Supabase (described [here](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)), and have "Transaction" pool mode enabled, then ensure to turn off prepare, as prepared statements are not supported. 

```typescript copy filename="index.ts"
import { drizzle } from 'drizzle-orm/postgres-js'
import postgres from 'postgres'

// Disable prefetch as it is not supported for "Transaction" pool mode 
const client = postgres(process.env.DATABASE_URL, { prepare: false })
const db = drizzle({ client });

const allUsers = await db.select().from(...);
```

Connect to your database using the Connection Pooler for **serverless environments**, and the Direct Connection for **long-running servers**.


#### Step 1 - Install packages
<Npm>
drizzle-orm @tidbcloud/serverless
-D drizzle-kit
</Npm>


#### Step 1 - Install packages
<Npm>
drizzle-orm@beta @tursodatabase/database
-D drizzle-kit@beta
</Npm>


#### Step 1 - Install packages
<Npm>
drizzle-orm @libsql/client
-D drizzle-kit
</Npm>


## Installation

<Npm>drizzle-seed</Npm>
