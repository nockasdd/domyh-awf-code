---
library: deno
version: 2.x
latest: true
category: runtime
official_docs: https://docs.deno.com
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://docs.deno.com/llms-full.txt
---

# Deno Documentation - Full Content

> This document contains the full content of the Deno documentation website.


## Install `deployctl`

With the Deno runtime installed, you can install the `deployctl` utility with
the following command:

```sh
deno install -gArf jsr:@deno/deployctl
```

The `-A` option in the deno install command grants all permissions to the
installed script. You can opt not to use it, in which case you will be prompted
to grant the necessary permissions when needed during the execution of the tool.


## Install Deno and `deployctl`

If you haven't already, you can
[install the Deno runtime](/runtime/getting_started/installation) using one of
the commands below:

<deno-tabs group-id="operating-systems">
<deno-tab value="mac" label="macOS" default>

```sh
curl -fsSL https://deno.land/install.sh | sh
```

</deno-tab>
<deno-tab value="windows" label="Windows">

```powershell
irm https://deno.land/install.ps1 | iex
```

</deno-tab>
<deno-tab value="linux" label="Linux">

```sh
curl -fsSL https://deno.land/install.sh | sh
```

</deno-tab>
</deno-tabs>

After Deno is installed, install the [`deployctl`](./deployctl.md) utility:

```sh
deno install -A jsr:@deno/deployctl --global
```

You can confirm `deployctl` has been installed correctly by running:

```console
deployctl --help
```

Now, you're ready to deploy a Deno script from the command line!


## Setup Postgres

To get started, we need to create a new Postgres instance for us to connect to.
For this tutorial, we will be using [Neon Postgres](https://neon.tech/) as they
provide free, managed Postgres instances. If you like to host your database
somewhere else, you can do that too.

1. Visit https://neon.tech/ and click **Sign up** to sign up with an email,
   Github, Google, or partner account. After signing up, you are directed to the
   Neon Console to create your first project.
2. Enter a name for your project, select a Postgres version, provide a database
   name, and select a region. Generally, you'll want to select the region
   closest to your application. When you're finished, click **Create project**.
3. You are presented with the connection string for your new project, which you
   can use to connect to your database. Save the connection string, which looks
   something like this:

   ```sh
   postgres://alex:AbC123dEf@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

   You will need the connection string in the next step.


## Setup Postgres

> This tutorial will focus entirely on connecting to Postgres unencrypted. If
> you would like to use encryption with a custom CA certificate, use the
> documentation [here](https://deno-postgres.com/#/?id=ssltls-connection).

To get started, we need to create a new Postgres instance for us to connect to.
For this tutorial, we will be using [Supabase](https://supabase.com) as they
provide free, managed Postgres instances. If you like to host your database
somewhere else, you can do that too.

1. Visit https://app.supabase.io/ and click **New project**.
2. Select a name, password, and region for your database. Make sure to save the
   password, as you will need it later.
3. Click **Create new project**. Creating the project can take a while, so be
   patient.


## Setup Postgres

There are several ways to set up a Prisma Postgre database for your Prisma
project. This guide covers the most common approaches.


### 1. Install dependencies

First, install the required dependencies:

```bash
deno install npm:@prisma/client
deno install npm:@prisma/extension-accelerate
deno install npm:dotenv-cli
```

:::note

The `dotenv-cli` package is needed because Prisma Client doesn't read `.env`
files by default on Deno.

:::


# Getting started

> Step-by-step guide to creating and configuring your first Deno Deploy application, including organization setup, build configuration, environment variables, and deployment monitoring.

URL: https://docs.deno.com/deploy/getting_started



### Install command

Command for installing dependencies (e.g., `npm install`, `deno install`). This
can be empty for Deno applications without a `package.json`.


# Deno KV Quick Start

URL: https://docs.deno.com/deploy/kv/


Deno KV is a
[key-value database](https://en.wikipedia.org/wiki/Key%E2%80%93value_database)
built directly into the Deno runtime, available in the
[`Deno.Kv` namespace](https://docs.deno.com/api/deno/~/Deno.Kv). It can be used
for many kinds of data storage use cases, but excels at storing simple data
structures that benefit from very fast reads and writes. Deno KV is available in
the Deno CLI and on [Deno Deploy](/deploy/reference/deno_kv/).

:::caution

Deno KV is still in development and may change. To use it, you must pass the
`--unstable-kv` flag to Deno.

:::

Let's walk through the key features of Deno KV.


## Installation and usage

Use your preferred npm client to install the client library for Node.js using
one of the commands below.

<deno-tabs group-id="npm-client">
<deno-tab value="npm" label="npm" default>

```sh
npm install @deno/kv
```

</deno-tab>
<deno-tab value="pnpm" label="pnpm">

```sh
pnpm add @deno/kv
```

</deno-tab>
<deno-tab value="yarn" label="yarn">

```sh
yarn add @deno/kv
```

</deno-tab>
</deno-tabs>

Once you've added the package to your Node project, you can import the `openKv`
function (supports both ESM `import` and CJS `require`-based usage):

```js
import { openKv } from "@deno/kv";

// Connect to a KV instance
const kv = await openKv("<KV Connect URL>");

// Write some data
await kv.set(["users", "alice"], { name: "Alice" });

// Read it back
const result = await kv.get(["users", "alice"]);
console.log(result.value); // { name: "Alice" }
```

By default, the access token used for authentication comes from the
`DENO_KV_ACCESS_TOKEN` environment variable. You can also pass it explicitly:

```js
import { openKv } from "@deno/kv";

const kv = await openKv("<KV Connect URL>", { accessToken: myToken });
```

Once your Deno KV client is initialized, the same API available in Deno may be
used in Node as well.


## Setup Guides


### AWS: Easy setup with `deno deploy setup-aws`

For instructions on how to set up AWS with Deno Deploy using the
`deno deploy setup-aws` command, please see the instructions on the AWS cloud
integration setup page in your app settings.


#### Prerequisites

- AWS CLI installed and configured
- Permissions to create IAM roles, OIDC providers, and attach policies


### GCP: Easy setup with `deno deploy setup-gcp`

For instructions on how to set up GCP with Deno Deploy using the
`deno deploy setup-gcp` command, please see the instructions on the Google cloud
integration setup page in your app settings.


#### Prerequisites

- gcloud CLI installed and authenticated
- Access to create workload identity pools, service accounts, and grant IAM
  roles
- Required APIs enabled:
  - `iam.googleapis.com`
  - `iamcredentials.googleapis.com`
  - `sts.googleapis.com`


## Getting Started


# or npm install @deno/astro-adapter

# or npm install nitro-nightly@latest
```

2. Configure your `vite.config.ts` to use the Nitro plugin:

```ts title="vite.config.ts"
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import { defineConfig } from "vite";
import { nitro } from "nitro/vite";
import viteReact from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [tanstackStart(), nitro(), viteReact()],
});
```

Deno Deploy automatically configures Nitro, so no additional preset
configuration is needed.


## Getting started

To start using the tunnel feature, you'll need to have Deno installed on your
local machine. You can then pass the `--tunnel` flag when running your Deno
application locally, either with `deno task` or `deno run`. For example:

```sh
deno run --tunnel -A main.ts
```

The first time you run this command, you'll be prompted to authenticate with
Deno Deploy and choose which Deno Deploy app you want to connect the tunnel to.
Once authenticated, a secure tunnel will be established, and you'll receive a
public URL that forwards traffic to your local server.

You can also specify `--tunnel` for `deno task` commands defined in your
`deno.json` or `package.json` file:

```json
{
  "tasks": {
    "dev": "astro dev"
  }
}
```

Then run the task with:

```bash
deno task --tunnel dev
```


# Getting Started with OpenTelemetry in Deno

> Set up basic OpenTelemetry instrumentation in a Deno application. This tutorial covers creating a simple HTTP server with custom metrics and traces, and viewing the telemetry data.

URL: https://docs.deno.com/examples/basic_opentelemetry_tutorial/


OpenTelemetry provides powerful observability tools for your applications. With
Deno's built-in OpenTelemetry support, you can easily instrument your code to
collect metrics, traces, and logs.

This tutorial will walk you through setting up a simple Deno application with
OpenTelemetry instrumentation.


## Prerequisites

- Deno 2.3 or later


### Use context-specific setup

When tests within a describe block need different setup, use nested describes
with their own `beforeEach` hooks rather than conditional logic:

```ts
// Good
describe("User operations", () => {
  describe("when user is logged in", () => {
    beforeEach(() => {
      // Setup logged-in user
    });

    it("should show the dashboard", () => {
      // Test
    });
  });

  describe("when user is logged out", () => {
    beforeEach(() => {
      // Setup logged-out state
    });

    it("should redirect to login", () => {
      // Test
    });
  });
});

// Avoid
describe("User operations", () => {
  beforeEach(() => {
    // Setup base state
    if (isLoggedInTest) {
      // Setup logged-in state
    } else {
      // Setup logged-out state
    }
  });

  it("should show dashboard when logged in", () => {
    isLoggedInTest = true;
    // Test
  });

  it("should redirect to login when logged out", () => {
    isLoggedInTest = false;
    // Test
  });
});
```


## Initialize a new project

First, create a new directory for your project and navigate into it.

```sh
deno init chat-app
cd deno-chat-app
```


## Setup `denoflare`

In order to deploy Deno to Cloudflare, we'll use this community created CLI
[`denoflare`](https://denoflare.dev/).

[Install it](https://denoflare.dev/cli/#installation):

```shell
deno install --unstable-worker-options --allow-read --allow-net --global --allow-env --allow-run --name denoflare --force \
https://raw.githubusercontent.com/skymethod/denoflare/v0.6.0/cli/cli.ts
```


## Prerequisites

1. A [GitHub](https://github.com) account
2. [Deno installed](https://docs.deno.com/runtime/manual/getting_started/installation)
   on your local machine
3. A [Deno Deploy](https://console.deno.com/account) account


## Prerequisites

Before using the deploy command, you will need a Deno Deploy account, and a Deno
Deploy organization set up on that account.

To create an account visit
[the Deno Deploy dashboard](https://console.deno.com/). To create an
organization, follow the steps in the


## Prerequisites

1. A [GitHub](https://github.com) account
2. [Deno installed](https://docs.deno.com/runtime/manual/getting_started/installation)
   on your local machine
3. Access to the [Deno Deploy account](https://console.deno.com/)
4. Basic familiarity with
   [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)


## Install Drizzle

First, we'll install the required dependencies using Deno's npm compatibility.
We'll be using Drizzle with
[Postgres](https://orm.drizzle.team/docs/get-started-postgresql), but you can
also use [MySQL](https://orm.drizzle.team/docs/get-started-mysql) or
[SQLite](https://orm.drizzle.team/docs/get-started-sqlite). (If you don't have
Postgres, you can [install it here](https://www.postgresql.org/download/).)

```bash
deno install npm:drizzle-orm npm:drizzle-kit npm:pg npm:@types/pg
```

This installs Drizzle ORM and its associated tools —
[drizzle-kit](https://orm.drizzle.team/docs/kit-overview) for schema migrations,
[pg](https://www.npmjs.com/package/pg) for PostgreSQL connectivity, and
[the TypeScript types for PostgreSQL](https://www.npmjs.com/package/@types/pg).
These packages will allow us to interact with our database in a type-safe way
while maintaining compatibility with Deno's runtime environment.

It will also create a `deno.json` file in your project root to manage the npm
dependencies:

```json
{
  "imports": {
    "@types/pg": "npm:@types/pg@^8.11.10",
    "drizzle-kit": "npm:drizzle-kit@^0.27.2",
    "drizzle-orm": "npm:drizzle-orm@^0.36.0",
    "pg": "npm:pg@^8.13.1"
  }
}
```


## Initialize a new deno project

In your commandline run the command to create a new starter project, then
navigate into the project directory:

```sh
deno init my-express-project
cd my-express-project
```


## Install Express

To install Express, we'll use the `npm:` module specifier. This specifier allows
us to import modules from npm:

```sh
deno add npm:express
```

This will add the latest `express` package to the `imports` field in your
`deno.json` file. Now you can import `express` in your code with
`import express from "express";`.


# Initialize a project

> Guide to creating and structuring new Deno projects. Learn about starting a new project, task configuration, dependency management, and best practices for growing applications.

URL: https://docs.deno.com/examples/initialize_project_tutorial/


While it is possible to run scripts directly with `deno run`, for larger
projects it is recommended to create a sensible directory structure. This way
you can organize your code, manage dependencies, script tasks and run tests more
easily.

Initialize a new project by running the following command:

```sh
deno init my_project
```

Where `my_project` is the name of your project. You can
[read more about the project structure](/runtime/getting_started/first_project/).


## Initialize a new project

First, create a new directory for your project and initialize it:

```bash
mkdir deno-llm-chat
cd deno-llm-chat
deno init
```


## Setup the API routes

This app will have two API routes. They will serve the following:

- the full list of dinosaurs for an index page
- individual dinosaur information for an individual dinosaur page

Both will be `*.get.ts` files, which Nuxt automatically converts to API
endpoints to respond to `GET` requests.
[The filename convention determines both the HTTP method and the route path](https://nuxt.com/docs/guide/directory-structure/server#matching-http-method).

The initial `dinosaurs.get.ts` is fairly simple and uses
[`defineCachedEventHandler`](https://nitro.build/guide/cache) to create a cached
endpoint for better performance. This handler simply returns our full dinosaur
data array without any filtering:

```tsx title="server/api/dinosaurs.get.ts"
import data from "./data.json" with { type: "json" };

export default defineCachedEventHandler(() => {
  return data;
});
```

The `GET` route for the individual dinosaur has a little more logic. It extracts
the name parameter from the event context, performs case-insensitive matching to
find the requested dinosaur, and includes proper error handling for missing or
invalid dinosaur names. We'll create a `dinosaurs` directory, then to pass the
name parameter, we'll make a new file named `[name].get.ts`:

```tsx title="server/api/dinosaurs/[name].get.ts"
import data from "../data.json";

export default defineCachedEventHandler((event) => {
  const name = getRouterParam(event, "name");

  if (!name) {
    throw createError({
      statusCode: 400,
      message: "No dinosaur name provided",
    });
  }

  const dinosaur = data.find(
    (dino) => dino.name.toLowerCase() === name.toLowerCase(),
  );

  if (!dinosaur) {
    throw createError({
      statusCode: 404,
      message: "Dinosaur not found",
    });
  }

  return dinosaur;
});
```

Run the server with `deno task dev` and visit
[http://localhost:3000/api/dinosaurs](http://localhost:3000/api/dinosaurs) in
your browser, you should see the raw JSON response showing all of the dinosaurs!

![Setting up API](./images/how-to/nuxt/nuxt-1.webp)

You can also retrieve data for a single dinosaur by visiting a particular
dinosaur name, for example:
[http://localhost:3000/api/dinosaurs/aardonyx](http://localhost:3000/api/dinosaurs/aardonyx).

![Setting up API](./images/how-to/nuxt/nuxt-2.webp)

Next, we'll setup the frontend with Vue to display the index page and each
individual dinosaur page.


## Setup the Vue frontend

We want to set up two pages within the app:

- An index page which will list all of the dinosaurs
- An individual dinosaur page showing more information about the selected
  dinosaur.

First, create the index page. Nuxt uses
[file-system routing](https://nuxt.com/docs/getting-started/routing), so we will
create a `pages` directory in the root, and within that an index page called
`index.vue`.

To get the data, we’ll use the `useFetch` composable to hit the API endpoint we
created in the previous section:

```tsx title="pages/index.vue"
<script setup lang="ts">
const { data: dinosaurs } = await useFetch("/api/dinosaurs");
</script>

<template>
  <main id="content">
    <h1 class="text-2xl font-bold mb-4">Welcome to the Dinosaur app</h1>
    <p class="mb-4">Click on a dinosaur below to learn more.</p>
    <ul class="space-y-2">
      <li v-for="dinosaur in dinosaurs" :key="dinosaur.name">
        <NuxtLink
          :to="'/' + dinosaur.name.toLowerCase()"
          class="text-blue-600 hover:text-blue-800 hover:underline"
        >
          {{ dinosaur.name }}
        </NuxtLink>
      </li>
    </ul>
  </main>
</template>
```

For the page that shows information on each dinosaur, we'll create a new dynamic
page called `[name].vue`. This page uses Nuxt's
[dynamic route parameters](https://nuxt.com/docs/getting-started/routing#route-parameters),
where the `[name]` in the filename can be accessed in JavaScript as
`route.params.name`. We’ll use the `useRoute` composable to access the route
parameters and `useFetch` to get the specific dinosaur's data based on the name
parameter:

```tsx title="pages/[name].vue"
<script setup lang="ts">
const route = useRoute();
const { data: dinosaur } = await useFetch(
  `/api/dinosaurs/${route.params.name}`
);
</script>

<template>
  <main v-if="dinosaur">
    <h1 class="text-2xl font-bold mb-4">{{ dinosaur.name }}</h1>
    <p class="mb-4">{{ dinosaur.description }}</p>
    <NuxtLink to="/" class="text-blue-600 hover:text-blue-800 hover:underline">
      Back to all dinosaurs
    </NuxtLink>
  </main>
</template>
```

Next, we’ll have to connect these Vue components together so that they render
properly when we visit the root of the domain. Let’s update `app.vue` at the
root of the directory to serve our application’s root component. We’ll use
[`NuxtLayout`](https://nuxt.com/docs/api/components/nuxt-layout) for consistent
page structure and [`NuxtPage`](https://nuxt.com/docs/api/components/nuxt-page)
for dynamic page rendering:

```tsx title="app.vue"
<template>
  <NuxtLayout>
    <div>
      <nav class="p-4 bg-gray-100">
        <NuxtLink to="/" class="text-blue-600 hover:text-blue-800">
          Dinosaur Encyclopedia
        </NuxtLink>
      </nav>

      <div class="container mx-auto p-4">
        <NuxtPage />
      </div>
    </div>
  </NuxtLayout>
</template>;
```

Run the server with `deno task dev` and see how it looks at
[http://localhost:3000](http://localhost:3000):

Looks great!

```bash
deno install -D npm:tailwindcss npm:@tailwindcss/vite
```

Then, we're going to update the `nuxt.config.ts`. Import the Tailwind dependency
and configure the Nuxt application for Deno compatibility, We'll enable
development tools, and set up Tailwind CSS:

```tsx title="nuxt.config.ts"
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  nitro: {
    preset: "deno",
  },
  app: {
    head: {
      title: "Dinosaur Encyclopedia",
    },
  },
  css: ["~/assets/css/main.css"],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
});
```

Next, create a new css file, `assets/css/main.css`, and add an import `@import`
that imports tailwind, as well as the tailwind utilities:

```tsx title="assets/css/main.css"
@import "tailwindcss";

@tailwind base;
@tailwind components;
@tailwind utilities;
```


## React app setup


## Examples


## Quick start


### Environment setup

```bash

## Getting started
