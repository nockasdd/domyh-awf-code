---
library: astro
version: 5.x
latest: true
category: meta-framework
official_docs: https://docs.astro.build
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://docs.astro.build/llms-full.txt
---

# Why Astro?

> Astro is the web framework for building content-driven websites like blogs, marketing, and e-commerce. Learn why Astro might be a good choice for your next website.

**Astro** is the web framework for building **content-driven websites** like blogs, marketing, and e-commerce. Astro is best-known for pioneering a new [frontend architecture](/en/concepts/islands/) to reduce JavaScript overhead and complexity compared to other frameworks. If you need a website that loads fast and has great SEO, then Astro is for you.


# Install Astro

> How to install Astro and start a new project.

The [`create astro` CLI command](#install-from-the-cli-wizard) is the fastest way to start a new Astro project from scratch. It will walk you through every step of setting up your new Astro project and allow you to choose from a few different official starter templates.

You can also run the CLI command with the `template` flag to begin your project using any existing theme or starter template. Explore our [themes and starters showcase](https://astro.build/themes/) where you can browse themes for blogs, portfolios, documentation sites, landing pages, and more!

To install Astro manually instead, see our [step-by-step manual installation guide](#manual-setup).

Online previews

Prefer to try Astro in your browser? Visit [astro.new](https://astro.new/) to browse our starter templates and spin up a new Astro project without ever leaving your browser.


## Prerequisites

[Section titled “Prerequisites”](#prerequisites)

* **Node.js** - `v22.12.0` or higher. Odd-numbered versions like `v23` are not supported.
* **Text editor** - We recommend [VS Code](https://code.visualstudio.com/) with our [Official Astro extension](https://marketplace.visualstudio.com/items?itemName=astro-build.astro-vscode).
* **Terminal** - Astro is accessed through its command-line interface (CLI).


## Install from the CLI wizard

[Section titled “Install from the CLI wizard”](#install-from-the-cli-wizard)

You can run `create astro` anywhere on your machine, so there’s no need to create a new empty directory for your project before you begin. If you don’t have an empty directory yet for your new project, the wizard will help create one for you automatically.

1. Run the following command in your terminal to start the install wizard:

   * npm

     ```shell
     # create a new project with npm
     npm create astro@latest
     ```

   * pnpm

     ```shell
     # create a new project with pnpm
     pnpm create astro@latest
     ```

   * Yarn

     ```shell
     # create a new project with yarn
     yarn create astro
     ```

   If all goes well, you will see a success message followed by some recommended next steps.

2. Now that your project has been created, you can `cd` into your new project directory to begin using Astro.

3. If you skipped the “Install dependencies?” step during the CLI wizard, then be sure to install your dependencies before continuing.

   * npm

     ```shell
     npm install
     ```

   * pnpm

     ```shell
     pnpm install
     ```

   * Yarn

     ```shell
     yarn install
     ```

4. You can now [start the Astro dev server](/en/develop-and-build/#start-the-astro-dev-server) and see a live preview of your project while you build!


## CLI installation flags

[Section titled “CLI installation flags”](#cli-installation-flags)

You can run the `create astro` command with additional flags to customize the setup process (e.g. answering “yes” to all questions, skipping the Houston animation) or your new project (e.g. install git or not, add integrations).

See [all the available `create astro` command flags](https://github.com/withastro/astro/blob/main/packages/create-astro/README.md).


## Manual Setup

[Section titled “Manual Setup”](#manual-setup)

This guide will walk you through the steps to manually install and configure a new Astro project.

If you prefer not to use our automatic `create astro` CLI tool, you can set up your project yourself by following the guide below.

1. Create your directory

   Create an empty directory with the name of your project, and then navigate into it.

   ```bash
   mkdir my-astro-project
   cd my-astro-project
   ```

   Once you are in your new directory, create your project `package.json` file. This is how you will manage your project dependencies, including Astro. If you aren’t familiar with this file format, run the following command to create one.

   * npm

     ```shell
     npm init --yes
     ```

   * pnpm

     ```shell
     pnpm init
     ```

   * Yarn

     ```shell
     yarn init --yes
     ```

2. Install Astro

   First, install the Astro project dependencies inside your project.

   Important

   Astro must be installed locally, not globally. Make sure you are *not* running `npm install -g astro` `pnpm add -g astro` or `yarn add global astro`.

   * npm

     ```shell
     npm install astro
     ```

   * pnpm

     ```shell
     pnpm add astro
     ```

   * Yarn

     ```shell
     yarn add astro
     ```

   Then, replace any placeholder “scripts” section of your `package.json` with the following:

   package.json

   ```diff
   {
     "scripts": {
       -"test": "echo \"Error: no test specified\" && exit 1",
       +"dev": "astro dev",
       +"build": "astro build",
       +"preview": "astro preview"
     },
   }
   ```

   You’ll use these scripts later in the guide to start Astro and run its different commands.

3. Create your first page

   In your text editor, create a new file in your directory at `src/pages/index.astro`. This will be your first Astro page in the project.

   For this guide, copy and paste the following code snippet (including `---` dashes) into your new file:

   src/pages/index.astro

   ```astro
   ---
   // Welcome to Astro! Everything between these triple-dash code fences
   // is your "component frontmatter". It never runs in the browser.
   console.log('This runs in your terminal, not the browser!');
   ---
   <!-- Below is your "component template." It's just HTML, but with
       some magic sprinkled in to help you build great templates. -->
   <html>
     <body>
       <h1>Hello, World!</h1>
     </body>
   </html>
   <style>
     h1 {
       color: orange;
     }
   </style>
   ```

4. Create your first static asset

   You will also want to create a `public/` directory to store your static assets. Astro will always include these assets in your final build, so you can safely reference them from inside your component templates.

   In your text editor, create a new file in your directory at `public/robots.txt`. `robots.txt` is a simple file that most sites will include to tell search bots like Google how to treat your site.

   For this guide, copy and paste the following code snippet into your new file:

   public/robots.txt

   ```diff
   # Example: Allow all bots to scan and index your site.
   # Full syntax: https://developers.google.com/search/docs/advanced/robots/create-robots-txt
   User-agent: *
   Allow: /
   ```

5. Create `astro.config.mjs`

   Astro is configured using `astro.config.mjs`. This file is optional if you do not need to configure Astro, but you may wish to create it now.

   Create `astro.config.mjs` at the root of your project, and copy the code below into it:

   astro.config.mjs

   ```js
   import { defineConfig } from "astro/config";


   // https://astro.build/config
   export default defineConfig({});
   ```

   If you want to include [UI framework components](/en/guides/framework-components/) such as React, Svelte, etc. or use other tools such as MDX or Partytown in your project, here is where you will [manually import and configure integrations](/en/guides/integrations-guide/).

   Read Astro’s [API configuration reference](/en/reference/configuration-reference/) for more information.

6. Add TypeScript support

   TypeScript is configured using `tsconfig.json`. Even if you don’t write TypeScript code, this file is important so that tools like Astro and VS Code know how to understand your project. Some features (like npm package imports) aren’t fully supported in the editor without a `tsconfig.json` file.

   If you do intend to write TypeScript code, using Astro’s `strict` or `strictest` template is recommended. You can view and compare the three template configurations at [astro/tsconfigs/](https://github.com/withastro/astro/blob/main/packages/astro/tsconfigs/).

   Create `tsconfig.json` at the root of your project, and copy the code below into it. (You can use `base`, `strict`, or `strictest` for your TypeScript template):

   tsconfig.json

   ```json
   {
     "extends": "astro/tsconfigs/base"
   }
   ```

   Read Astro’s [TypeScript setup guide](/en/guides/typescript/#setup) for more information.

7. Next Steps

   If you have followed the steps above, your project directory should now look like this:

   * node\_modules/

     * …

   * public/

     * robots.txt

   * src/

     * pages/

       * index.astro

   * astro.config.mjs

   * package-lock.json or `yarn.lock`, `pnpm-lock.yaml`, etc.

   * package.json

   * tsconfig.json

8. You can now [start the Astro dev server](/en/develop-and-build/#start-the-astro-dev-server) and see a live preview of your project while you build!


# Editor setup

> Set up your code editor to build with Astro.

Customize your code editor to improve the Astro developer experience and unlock new features.


## Installation

[Section titled “Installation”](#installation)

Install the [`@astrojs/db` integration](/en/guides/integrations-guide/db/) using the built-in `astro add` command:

* npm

  ```sh
  npx astro add db
  ```

* pnpm

  ```sh
  pnpm astro add db
  ```

* Yarn

  ```sh
  yarn astro add db
  ```


### Getting started with Turso

[Section titled “Getting started with Turso”](#getting-started-with-turso)

Turso is the company behind [libSQL](https://github.com/tursodatabase/libsql), the open-source fork of SQLite that powers Astro DB. They provide a fully managed libSQL database platform and are fully compatible with Astro.

The steps below will guide you through the process of installing the Turso CLI, logging in (or signing up), creating a new database, getting the required environmental variables, and pushing the schema to the remote database.

1. Install the [Turso CLI](https://docs.turso.tech/cli/installation).

2. [Log in or sign up](https://docs.turso.tech/cli/authentication) to Turso.

3. Create a new database. In this example the database name is `andromeda`.

   ```sh
   turso db create andromeda
   ```

4. Run the `show` command to see information about the newly created database:

   ```sh
   turso db show andromeda
   ```

   Copy the `URL` value and set it as the value for `ASTRO_DB_REMOTE_URL`.

   .env

   ```dotenv
   ASTRO_DB_REMOTE_URL=libsql://andromeda-houston.turso.io
   ```

5. Create a new token to authenticate requests to the database:

   ```sh
   turso db tokens create andromeda
   ```

   Copy the output of the command and set it as the value for `ASTRO_DB_APP_TOKEN`.

   .env

   ```diff
   ASTRO_DB_REMOTE_URL=libsql://andromeda-houston.turso.io
   +ASTRO_DB_APP_TOKEN=eyJhbGciOiJF...3ahJpTkKDw
   ```

6. Push your DB schema and metadata to the new Turso database.

   ```sh
   astro db push --remote
   ```

7. Congratulations, now you have a database connected! Give yourself a break. 👾

   ```sh
   turso relax
   ```

To explore more features of Turso, check out the [Turso docs](https://docs.turso.tech).


### Installation

[Section titled “Installation”](#installation)

* npm

  ```shell
  npm install better-auth
  ```

* pnpm

  ```shell
  pnpm add better-auth
  ```

* Yarn

  ```shell
  yarn add better-auth
  ```

For detailed setup instructions, check out the [Better Auth Installation Guide](https://www.better-auth.com/docs/installation).


### Installation

[Section titled “Installation”](#installation-1)

Install `@clerk/astro` using the package manager of your choice.

* npm

  ```shell
  npm install @clerk/astro
  ```

* pnpm

  ```shell
  pnpm add @clerk/astro
  ```

* Yarn

  ```shell
  yarn add @clerk/astro
  ```


## Initializing Firebase in Astro

[Section titled “Initializing Firebase in Astro”](#initializing-firebase-in-astro)


### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

* A [Firebase project with a web app configured](https://firebase.google.com/docs/web/setup).

* An Astro project with [`output: 'server'` for on-demand rendering](/en/guides/on-demand-rendering/) enabled.

* Firebase credentials: You will need two sets of credentials to connect Astro to Firebase:

  * Web app credentials: These credentials will be used by the client side of your app. You can find them in the Firebase console under *Project settings > General*. Scroll down to the **Your apps** section and click on the **Web app** icon.
  * Project credentials: These credentials will be used by the server side of your app. You can generate them in the Firebase console under *Project settings > Service accounts > Firebase Admin SDK > Generate new private key*.


### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

To connect Astro with Firebase, install the following packages using the single command below for your preferred package manager:

* `firebase` - the Firebase SDK for the client side
* `firebase-admin` - the Firebase Admin SDK for the server side

- npm

  ```shell
  npm install firebase firebase-admin
  ```

- pnpm

  ```shell
  pnpm add firebase firebase-admin
  ```

- Yarn

  ```shell
  yarn add firebase firebase-admin
  ```

Next, create a folder named `firebase` in the `src/` directory and add two new files to this folder: `client.ts` and `server.ts`.

In `client.ts`, add the following code to initialize Firebase in the client using your web app credentials and the `firebase` package:

src/firebase/client.ts

```ts
import { initializeApp } from "firebase/app";


const firebaseConfig = {
  apiKey: "my-public-api-key",
  authDomain: "my-auth-domain",
  projectId: "my-project-id",
  storageBucket: "my-storage-bucket",
  messagingSenderId: "my-sender-id",
  appId: "my-app-id",
};


export const app = initializeApp(firebaseConfig);
```

Note

Remember to replace the `firebaseConfig` object with your own web app credentials.

In `server.ts`, add the following code to initialize Firebase in the server using your project credentials and the `firebase-admin` package:

src/firebase/server.ts

```ts
import type { ServiceAccount } from "firebase-admin";
import { initializeApp, cert, getApps } from "firebase-admin/app";


const activeApps = getApps();
const serviceAccount = {
  type: "service_account",
  project_id: import.meta.env.FIREBASE_PROJECT_ID,
  private_key_id: import.meta.env.FIREBASE_PRIVATE_KEY_ID,
  private_key: import.meta.env.FIREBASE_PRIVATE_KEY,
  client_email: import.meta.env.FIREBASE_CLIENT_EMAIL,
  client_id: import.meta.env.FIREBASE_CLIENT_ID,
  auth_uri: import.meta.env.FIREBASE_AUTH_URI,
  token_uri: import.meta.env.FIREBASE_TOKEN_URI,
  auth_provider_x509_cert_url: import.meta.env.FIREBASE_AUTH_CERT_URL,
  client_x509_cert_url: import.meta.env.FIREBASE_CLIENT_CERT_URL,
};


const initApp = () => {
  if (import.meta.env.PROD) {
    console.info('PROD env detected. Using default service account.')
    // Use default config in firebase functions. Should be already injected in the server by Firebase.
    return initializeApp()
  }
  console.info('Loading service account from env.')
  return initializeApp({
    credential: cert(serviceAccount as ServiceAccount)
  })
}


export const app = activeApps.length === 0 ? initApp() : activeApps[0];
```

Note

Remember to replace the `serviceAccount` object with your own project credentials.

Finally, your project should now include these new files:

* src

  * env.d.ts

  * firebase

    * **client.ts**
    * **server.ts**

* .env

* astro.config.mjs

* package.json


### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

* An Astro project [initialized with Firebase](#initializing-firebase-in-astro).
* A Firebase project with email/password authentication enabled in the Firebase console under *Authentication > Sign-in* method.


### Prerequisites

[Section titled “Prerequisites”](#prerequisites-2)

* An Astro project initialized with Firebase as described in the [Initializing Firebase in Astro](#initializing-firebase-in-astro) section.

* A Firebase project with a Firestore database. You can follow the [Firebase documentation to create a new project and set up a Firestore database](https://firebase.google.com/docs/firestore/quickstart).

In this recipe, the Firestore collection will be called **friends** and will contain documents with the following fields:

* `id`: autogenerated by Firestore
* `name`: a string field
* `age`: a number field
* `isBestFriend`: a boolean field


### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

* A [Neon](https://console.neon.tech/signup) account with a created project
* Neon database connection string
* An Astro project with [on-demand rendering (SSR)](/en/guides/on-demand-rendering/) enabled


### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

Install the `@neondatabase/serverless` package to connect to Neon:

```bash
npm install @neondatabase/serverless
```


### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

* An Astro project with an adapter installed to enable [on-demand rendering (SSR)](/en/guides/on-demand-rendering/).


### Install dependencies and initialize Prisma

[Section titled “Install dependencies and initialize Prisma”](#install-dependencies-and-initialize-prisma)

Run the following commands to install the necessary Prisma dependencies:

```bash
npm install prisma tsx --save-dev
npm install @prisma/adapter-pg @prisma/client
```

Once installed, initialize Prisma in your project with the following command:

```bash
npx prisma init --db --output ./generated
```

You’ll need to answer a few questions while setting up your Prisma Postgres database. Select the region closest to your location and a memorable name for your database, like “My Astro Project.”

This will create:

* A `prisma/` directory with a `schema.prisma` file
* A `.env` file with a `DATABASE_URL` already set


### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

* An Astro project with an adapter installed to enable [on-demand rendering (SSR)](/en/guides/on-demand-rendering/).
* A [Prisma Postgres](https://pris.ly/ppg) database with a TCP enabled connection string


### Install dependencies

[Section titled “Install dependencies”](#install-dependencies)

This example uses [`pg`, a PostgreSQL client for Node.js](https://github.com/brianc/node-postgres) to make a direct TCP connection.

Run the following command to install the `pg` package:

```bash
npm install pg
```


## Install

[Section titled “Install”](#install)

Sentry captures data by using an SDK within your application’s runtime.

Install the SDK by running the following command for the package manager of your choice in the Astro CLI:

* npm

  ```shell
  npx astro add @sentry/astro
  ```

* pnpm

  ```shell
  pnpm astro add @sentry/astro
  ```

* Yarn

  ```shell
  yarn astro add @sentry/astro
  ```

The astro CLI installs the SDK package and adds the Sentry integration to your `astro.config.mjs` file.


## Test your setup

[Section titled “Test your setup”](#test-your-setup)

Add the following `<button>` element to one of your `.astro` pages. This will allow you to manually trigger an error so you can test the error reporting process.

src/pages/index.astro

```astro
<button onclick="throw new Error('This is a test error')">Throw test error</button>
```

To view and resolve the recorded error, log into [sentry.io](https://sentry.io/) and open your project.


## Initializing Supabase in Astro

[Section titled “Initializing Supabase in Astro”](#initializing-supabase-in-astro)


### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

* An Astro project [initialized with Supabase](#initializing-supabase-in-astro).
* A Supabase project with email/password authentication enabled. You can enable this in the **Authentication > Providers** tab of your Supabase project.


# Unknown configuration error.
