---
library: prisma
version: 6.x
latest: true
category: database
official_docs: https://www.prisma.io/docs
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://prisma.io/docs/llms-full.txt
---

# Prisma Documentation - Full Content Feed

This file contains the complete Prisma documentation in machine-readable format.
Includes both v7 (current) and v6 documentation.

---


# Getting started (/docs/accelerate/getting-started)



Prerequisites [#prerequisites]

To get started with Accelerate, you will need the following:

* A [Prisma Data Platform account](https://console.prisma.io)
* A project that uses [Prisma Client](/orm/prisma-client/setup-and-configuration/introduction) `4.16.1` or higher. If your project is using interactive transactions, you need to use `5.1.1` or higher. (We always recommend using the latest version of Prisma.)
* A hosted PostgreSQL, MySQL/MariaDB, PlanetScale, CockroachDB, or MongoDB database

1. Enable Accelerate [#1-enable-accelerate]

Navigate to your Prisma Data Platform project, choose an environment, and enable Accelerate by providing your database connection string and selecting the region nearest your database.

<CalloutContainer type="info">
  <CalloutDescription>
    If you require IP allowlisting or firewall configurations with trusted IP addresses, enable Static IP for enhanced security. Learn more on [how to enable static IP for Accelerate in the Platform Console](/accelerate/static-ip).
  </CalloutDescription>
</CalloutContainer>

2. Add Accelerate to your application [#2-add-accelerate-to-your-application]

2.1. Update your database connection string [#21-update-your-database-connection-string]

Once enabled, you'll be prompted to generate a connection string that you'll use to authenticate requests.

Replace your direct database URL with your new Accelerate connection string.

```bash title=".env"

# init (/docs/cli/init)



The `prisma init` command bootstraps a fresh Prisma project within the current directory.

Usage [#usage]

```bash
prisma init [options]
```

The command creates a `prisma` directory containing a `schema.prisma` file. By default, the project is configured for [local Prisma Postgres](/postgres/database/local-development), but you can choose a different database using the `--datasource-provider` option.

Options [#options]

| Option                  | Description                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| `-h`, `--help`          | Display help message                                                                                      |
| `--db`                  | Provision a fully managed Prisma Postgres database on the Prisma Data Platform                            |
| `--datasource-provider` | Define the datasource provider: `postgresql`, `mysql`, `sqlite`, `sqlserver`, `mongodb`, or `cockroachdb` |
| `--generator-provider`  | Define the generator provider to use (default: `prisma-client-js`)                                        |
| `--preview-feature`     | Define a preview feature to use (can be specified multiple times)                                         |
| `--output`              | Define Prisma Client generator output path                                                                |
| `--url`                 | Define a custom datasource URL                                                                            |

Flags [#flags]

| Flag           | Description                                     |
| -------------- | ----------------------------------------------- |
| `--with-model` | Add an example model to the created schema file |

Examples [#examples]

Set up a new Prisma project (default) [#set-up-a-new-prisma-project-default]

Sets up a new project configured for local Prisma Postgres:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a datasource provider [#specify-a-datasource-provider]

Set up a new project with MySQL as the datasource provider:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --datasource-provider mysql
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a generator provider [#specify-a-generator-provider]

Set up a project with a specific generator provider:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --generator-provider prisma-client-js
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify preview features [#specify-preview-features]

Set up a project with specific preview features enabled:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --preview-feature metrics
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Multiple preview features:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --preview-feature views --preview-feature metrics
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a custom output path [#specify-a-custom-output-path]

Set up a project with a custom output path for Prisma Client:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --output ./generated-client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --output ./generated-client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --output ./generated-client
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --output ./generated-client
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Specify a custom datasource URL [#specify-a-custom-datasource-url]

Set up a project with a specific database URL:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --url mysql://user:password@localhost:3306/mydb
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Add an example model [#add-an-example-model]

Set up a project with an example `User` model:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --with-model
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --with-model
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --with-model
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --with-model
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Provision a Prisma Postgres database [#provision-a-prisma-postgres-database]

Create a new project with a managed Prisma Postgres database:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma init --db
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma init --db
    ```
  </CodeBlockTab>
</CodeBlockTabs>

This requires authentication with the [Prisma Data Platform Console](https://console.prisma.io).

Generated files [#generated-files]

After running `prisma init`, you'll have the following files:

prisma/schema.prisma [#prismaschemaprisma]

The Prisma schema file where you define your data model:

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}
```

prisma.config.ts [#prismaconfigts]

A TypeScript configuration file for Prisma:

```typescript
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});
```

.env [#env]

Environment variables file for your project:

```bash
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

.gitignore [#gitignore]

Git ignore file configured for Prisma projects:

```bash
node_modules
.env
/generated/prisma
```



# Getting Started (/docs/console/getting-started)



This guide walks you through setting up your Console account and creating your first project.

Prerequisites [#prerequisites]

* A GitHub account (for authentication)
* A Prisma project (optional, but recommended)

Step 1: Create your account [#step-1-create-your-account]

1. Go to [console.prisma.io/login](https://console.prisma.io/login)
2. Click **Sign in with GitHub**
3. Authorize Prisma Console to access your GitHub account

You now have a Console account with a default workspace.

Step 2: Set up a workspace [#step-2-set-up-a-workspace]

When you create an account, a default workspace is automatically created for you. You can create additional workspaces for different teams or organizations.

Create a workspace (optional) [#create-a-workspace-optional]

To create an additional workspace:

1. Click the workspace dropdown in the top navigation
2. Click **Create Workspace**
3. Enter a name for your workspace
4. Click **Create**

Using the CLI [#using-the-cli]

List all workspaces:

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform workspace show --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform workspace show --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 3: Create a project [#step-3-create-a-project]

Projects organize your databases and environments within a workspace.

Using the Console web interface [#using-the-console-web-interface]

1. Navigate to your workspace
2. Click **Create Project**
3. Enter a project name
4. Click **Create**

Using the CLI [#using-the-cli-1]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform project create --workspace $WORKSPACE_ID --name "My Project" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 4: Create a resource [#step-4-create-a-resource]

Resources are the actual databases or environments within your project.

For Prisma Postgres [#for-prisma-postgres]

1. Navigate to your project
2. Click **Create Database**
3. Enter a database name
4. Select a region
5. Click **Create**

For Accelerate [#for-accelerate]

1. Navigate to your project
2. Click **Create Environment**
3. Enter an environment name (e.g., "production")
4. Click **Create**

Using the CLI [#using-the-cli-2]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform environment create --project $PROJECT_ID --name "production" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 5: Generate a connection string [#step-5-generate-a-connection-string]

Connection strings authenticate your application's requests to Prisma products.

Using the Console web interface [#using-the-console-web-interface-1]

1. Navigate to your resource (database or environment)
2. Click **Connection Strings** tab
3. Click **Create Connection String**
4. Enter a name for the connection string
5. Copy the connection string and store it securely
6. Click **Done**

Using the CLI [#using-the-cli-3]

<CodeBlockTabs defaultValue="npm" groupId="package-manager" persist>
  <CodeBlockTabsList>
    <CodeBlockTabsTrigger value="npm">
      npm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="pnpm">
      pnpm
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="yarn">
      yarn
    </CodeBlockTabsTrigger>

    <CodeBlockTabsTrigger value="bun">
      bun
    </CodeBlockTabsTrigger>
  </CodeBlockTabsList>

  <CodeBlockTab value="npm">
    ```bash
    npx prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="pnpm">
    ```bash
    pnpm dlx prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="yarn">
    ```bash
    yarn dlx prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>

  <CodeBlockTab value="bun">
    ```bash
    bunx --bun prisma platform apikey create --environment $ENVIRONMENT_ID --name "production-key" --early-access
    ```
  </CodeBlockTab>
</CodeBlockTabs>

Step 6: Use the connection string in your application [#step-6-use-the-connection-string-in-your-application]

Add the connection string to your `.env` file:

```bash

## Prerequisites

- [Node.js 20+](https://nodejs.org)
- [Any other prerequisites]


## 2. Install and Configure Prisma


### 2.1. Install dependencies

To get started with Prisma, you'll need to install a few dependencies:

```npm
npm install prisma tsx @types/pg --save-dev
```

```npm
npm install @prisma/client @prisma/adapter-pg dotenv pg
```

:::info

If you are using a different database provider (MySQL, SQL Server, SQLite), install the corresponding driver adapter package instead of `@prisma/adapter-pg`. For more information, see [Database drivers](/orm/core-concepts/supported-databases/database-drivers).

:::

Once installed, initialize Prisma in your project:

```npm
npx prisma init --db --output ../generated/prisma
```

:::info
You'll need to answer a few questions while setting up your Prisma Postgres database. Select the region closest to your location and a memorable name for your database.
:::

This will create:

- A `prisma` directory with a `schema.prisma` file
- A Prisma Postgres database
- A `.env` file containing the `DATABASE_URL`
- A `prisma.config.ts` file for configuration


## CORRECT INSTALLATION

```bash

## CORRECT PRISMA INITIALIZATION

```npm
npx prisma init --db --output ../src/generated/prisma
```


## CORRECT INSTALLATION

```bash

## CORRECT PRISMA INITIALIZATION

> **FOR AI ASSISTANTS**: This command is **interactive** and requires user input. You **MUST ask the user to run this command manually** in their own terminal, then **wait for them to confirm completion** before proceeding with the next steps. Do NOT attempt to run this command yourself.

```bash

# Initialize Prisma AND create a real Prisma Postgres cloud database
npx prisma init --db --output ../app/generated/prisma
```

This command:

- Authenticates you with Prisma Console (if needed)
- Prompts for **region** and **project name**
- **Creates a cloud Prisma Postgres database**
- Generates:
  - `prisma/schema.prisma` (with correct output path)
  - `prisma.config.ts` (with dotenv import)
  - **`.env` with a `DATABASE_URL`**

**IMPORTANT**: Ensure the generated `.env` uses a `postgres://` URL scheme. If it generates `prisma+postgres://`, replace it with the standard TCP connection string available in the Prisma Console.

```text
DATABASE_URL="postgres://..."
```

**IMPORTANT**: Do NOT use `npx prisma init` without `--db` as this only creates local files without a database.


## COMPLETE SETUP WORKFLOW

User should follow these steps (AI should provide these instructions):

1. **Install dependencies**:

   ```npm
   npm install prisma tsx --save-dev
   ```

   ```npm
   npm install @prisma/adapter-pg @prisma/client dotenv
   ```

2. **Initialize Prisma AND create Prisma Postgres database** (⚠️ USER MUST RUN MANUALLY):

   > **AI ASSISTANT**: Ask the user to run this command in their own terminal. This is interactive and requires user input. Wait for the user to confirm completion before continuing.

   ```npm
   npx prisma init --db --output ../app/generated/prisma
   ```

   The user should follow the terminal prompts to:
   - Authenticate with Prisma Console (if needed)
   - Choose a region (e.g., us-east-1)
   - Name your project

   Once complete, this creates `prisma/schema.prisma`, `prisma.config.ts`, AND `.env` with the `DATABASE_URL`.

   **User should confirm when done** so the AI can proceed with the next steps.

3. **Verify `.env` was created** - Ensure `DATABASE_URL` uses `postgres://`. If it uses `prisma+postgres://`, change it to the TCP connection string.

   ```text
   DATABASE_URL="postgres://..."
   ```

   **Do NOT invent or manually change this URL. Use the one from Prisma Console.**

4. **Update `prisma/schema.prisma`** - Add the User model (generator and datasource are already configured):

   ```prisma
   model User {
     id        Int      @id @default(autoincrement())
     email     String   @unique
     name      String?
     createdAt DateTime @default(now())
     updatedAt DateTime @updatedAt
   }
   ```

5. **Create `lib/prisma.ts`** with correct import path including `/client` and using `@prisma/adapter-pg`.

6. **Add npm scripts** to `package.json` for `db:test` and `db:studio`

7. **Create `scripts/test-database.ts`** test script

8. **Push schema to database**:

   ```npm
   npx prisma db push
   ```

9. **Generate Prisma Client**:

   ```npm
   npx prisma generate
   ```

10. **Test the setup**:

    ```bash
    npm run db:test
    ```

11. **Start development server**:
    ```bash
    npm run dev
    ```


## CORRECT INSTALLATION

```bash

## Install dependencies

At repo root:

```bash

## CORRECT INSTALLATION

```bash

## CORRECT PRISMA INITIALIZATION

```npm
npx prisma init --db --output ../src/generated/prisma
```
