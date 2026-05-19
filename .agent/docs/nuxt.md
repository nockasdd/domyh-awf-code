---
library: nuxt
version: 4.x
latest: true
category: fullstack-framework
official_docs: https://nuxt.com/docs
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://nuxt.com/llms-full.txt
---

# Introduction

Nuxt is a free and [open-source framework](https://github.com/nuxt/nuxt){rel="&#x22;nofollow&#x22;"} with an intuitive and extendable way to create type-safe, performant and production-grade full-stack web applications and websites with [Vue.js](https://vuejs.org){rel="&#x22;nofollow&#x22;"}.

We made everything so you can start writing `.vue` files from the beginning while enjoying hot module replacement in development and a performant application in production with server-side rendering by default.

Nuxt has no vendor lock-in, allowing you to deploy your application [**everywhere, even on the edge**](https://nuxt.com/blog/nuxt-on-the-edge).

::tip
If you want to play around with Nuxt in your browser, you can [try it out in one of our online sandboxes](https://nuxt.com/docs/4.x/getting-started/installation#play-online).
::


# Installation


### Prerequisites

- **Node.js** - [`20.x`](https://nodejs.org/en){rel="&#x22;nofollow&#x22;"} or newer (but we recommend the [active LTS release](https://github.com/nodejs/release#release-schedule){rel="&#x22;nofollow&#x22;"})
- **Text editor** - There is no IDE requirement, but we recommend [Visual Studio Code](https://code.visualstudio.com/){rel="&#x22;nofollow&#x22;"} with the [official Vue extension](https://marketplace.visualstudio.com/items?itemName=Vue.volar){rel="&#x22;nofollow&#x22;"} (previously known as Volar) or [WebStorm](https://www.jetbrains.com/webstorm/){rel="&#x22;nofollow&#x22;"}, which, along with [other JetBrains IDEs](https://www.jetbrains.com/ides/){rel="&#x22;nofollow&#x22;"}, offers great Nuxt support right out-of-the-box. If you use another editor, such as Neovim, you can configure [Vue Language Server](https://github.com/vuejs/language-tools){rel="&#x22;nofollow&#x22;"} support by following the [Vue Language Tools setup guides](https://github.com/vuejs/language-tools/wiki){rel="&#x22;nofollow&#x22;"}.
- **Terminal** - In order to run Nuxt commands

::note
Additional notes for an optimal setup:

- **Node.js**: Make sure to use an even numbered version (20, 22, etc.)
- **Neovim**: When configuring the Vue TypeScript plugin, make sure `location` points to the `@vue/language-server` package directory, not its binary. See the [Neovim setup guide](https://github.com/vuejs/language-tools/wiki/Neovim){rel=""nofollow""} for a working configuration.
- **WSL**: If you are using Windows and experience slow HMR, you may want to try using [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install){rel=""nofollow""} which may solve some performance issues.
- **Windows slow DNS resolution**: Instead of using `localhost:3000` for local dev server on Windows, use `127.0.0.1` for much faster loading experience on browsers.
::

Open a terminal (if you're using [Visual Studio Code](https://code.visualstudio.com){rel="&#x22;nofollow&#x22;"}, you can open an [integrated terminal](https://code.visualstudio.com/docs/terminal/basics){rel="&#x22;nofollow&#x22;"}) and use the following command to create a new starter project:

::code-group{sync="pm"}
```bash [npm]
npm create nuxt@latest <project-name>
```

```bash [yarn]
yarn create nuxt <project-name>
```

```bash [pnpm]
pnpm create nuxt@latest <project-name>
```

```bash [bun]
bun create nuxt@latest <project-name>
```

```bash [deno]
deno -A npm:create-nuxt@latest <project-name>
```
::

::tip
Alternatively, you can find other starters or themes by opening [nuxt.new](https://nuxt.new){rel=""nofollow""} and following the instructions there.
::

Open your project folder in Visual Studio Code:

```bash [Terminal]
code <project-name>
```

Or change directory into your new project from your terminal:

```bash
cd <project-name>
```


### Initializing State

Most of the time, you will want to initialize your state with data that resolves asynchronously. You can use the [`app.vue`](https://nuxt.com/docs/4.x/directory-structure/app/app) component with the [`callOnce`](https://nuxt.com/docs/4.x/api/utils/call-once) util to do so.

```vue [app/app.vue] twoslash
<script setup lang="ts">
const websiteConfig = useState('config')

await callOnce(async () => {
  websiteConfig.value = await $fetch('https://my-cms.com/api/website-config')
})
</script>
```

::tip
This is similar to the [`nuxtServerInit` action](https://v2.nuxt.com/docs/directory-structure/store/#the-nuxtserverinit-action){rel=""nofollow""} in Nuxt 2, which allows filling the initial state of your store server-side before rendering the page.
::

:read-more{to="https://nuxt.com/docs/4.x/api/utils/call-once"}


## Installation

In order to allow you to manage your other testing dependencies, `@nuxt/test-utils` ships with various optional peer dependencies. For example:

- you can choose between `happy-dom` and `jsdom` for a runtime Nuxt environment
- you can choose between `vitest`, `cucumber`, `jest` and `playwright` for end-to-end test runners
- `playwright-core` is only required if you wish to use the built-in browser testing utilities (and are not using `@playwright/test` as your test runner)

::code-group{sync="pm"}
```bash [npm]
npm i --save-dev @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```

```bash [yarn]
yarn add --dev @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```

```bash [pnpm]
pnpm add -D @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```

```bash [bun]
bun add --dev @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```
::


### Setup

1. Add `@nuxt/test-utils/module` to your `nuxt.config` file (optional). It adds a Vitest integration to your Nuxt DevTools which supports running your unit tests in development.
   ```ts twoslash
   export default defineNuxtConfig({
     modules: [
       '@nuxt/test-utils/module',
     ],
   })
   ```
2. Create a `vitest.config.ts` with the following content:
   ```ts twoslash
   import { defineConfig } from 'vitest/config'
   import { defineVitestProject } from '@nuxt/test-utils/config'

   export default defineConfig({
     test: {
       projects: [
         {
           test: {
             name: 'unit',
             include: ['test/unit/*.{test,spec}.ts'],
             environment: 'node',
           },
         },
         {
           test: {
             name: 'e2e',
             include: ['test/e2e/*.{test,spec}.ts'],
             environment: 'node',
           },
         },
         await defineVitestProject({
           test: {
             name: 'nuxt',
             include: ['test/nuxt/*.{test,spec}.ts'],
             environment: 'nuxt',
           },
         }),
       ],
     },
   })
   ```

::tip
When importing `@nuxt/test-utils` in your vitest config, It is necessary to have `"type": "module"` specified in your `package.json` or rename your vitest config file appropriately.

> i.e., `vitest.config.m{ts,js}`.
::

::tip
It is possible to set environment variables for testing by using the `.env.test` file.
::


#### Alternative: Simple Setup

If you prefer a simpler setup and want all tests to run in the Nuxt environment, you can use the basic configuration:

```ts twoslash
import { defineVitestConfig } from '@nuxt/test-utils/config'
import { fileURLToPath } from 'node:url'

export default defineVitestConfig({
  test: {
    environment: 'nuxt',
    // you can optionally set Nuxt-specific environment options
    // environmentOptions: {
    //   nuxt: {
    //     rootDir: fileURLToPath(new URL('./playground', import.meta.url)),
    //     domEnvironment: 'happy-dom', // 'happy-dom' (default) or 'jsdom'
    //     overrides: {
    //       // other Nuxt config you want to pass
    //     }
    //   }
    // }
  },
})
```

If you're using the simple setup with `environment: 'nuxt'` by default, you can opt *out* of the [Nuxt environment](https://vitest.dev/guide/environment.html#test-environment){rel="&#x22;nofollow&#x22;"} per test file as needed.

```ts twoslash
// @vitest-environment node
import { test } from 'vitest'

test('my test', () => {
  // ... test without Nuxt environment!
})
```

::warning
This approach is not recommended as it creates a hybrid environment where Nuxt Vite plugins run but the Nuxt entry and `nuxtApp` are not initialized. This can lead to hard-to-debug errors.
::


### Setup

In each `describe` block where you are taking advantage of the `@nuxt/test-utils/e2e` helper methods, you will need to set up the test context before beginning.

```ts [test/my-test.spec.ts] twoslash
import { describe, test } from 'vitest'
import { $fetch, setup } from '@nuxt/test-utils/e2e'

describe('My test', async () => {
  await setup({
    // test context options
  })

  test('my test', () => {
    // ...
  })
})
```

Behind the scenes, `setup` performs a number of tasks in `beforeAll`, `beforeEach`, `afterEach` and `afterAll` to set up the Nuxt test environment correctly.

Please use the options below for the `setup` method.


# Module setups (automatically added by Nuxt)
setups.@nuxt/test-utils="3.23.0"
```

If present, the properties in the `nuxt.config` file will overwrite the properties in `.nuxtrc` file.

::note
Nuxt automatically adds a `setups` section to track module installation and upgrade state. This is used internally for [module lifecycle hooks](https://nuxt.com/docs/4.x/api/kit/modules#using-lifecycle-hooks-for-module-installation-and-upgrade) and should not be modified manually.
::

::read-more{to="https://nuxt.com/docs/4.x/api/configuration/nuxt-config"}
Discover all the available options in the **Nuxt configuration** documentation.
::


## Quick Setup

```bash
npx nuxt module add eslint
```

Start your Nuxt app, a `eslint.config.mjs` file will be generated under your project root. You can customize it as needed.

You can learn more about the module and customizations in [Nuxt ESLint's documentation](https://eslint.nuxt.com/packages/module){rel="&#x22;nofollow&#x22;"}.



## Avoid costly plugin setup

A large number of plugins can cause performance issues, especially if they require expensive computations or take too long to initialize. Since plugins run during the hydration phase, inefficient setups can block rendering and degrade the user experience.


## Setup

The Nuxt MCP server uses HTTP transport and can be installed in different AI assistants.


#### Setup Instructions

1. Open Claude Desktop and navigate to "Settings" > "Developer".
2. Click on "Edit Config". This will open the local Claude directory.
3. Modify the `claude_desktop_config.json`file with your custom MCP server configuration.
   ```json \[claude\_desktop\_config.json]
   {
     "mcpServers": {
       "nuxt": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "https://nuxt.com/mcp"
         ]
       }
     }
   }
   ```
4. Restart Claude Desktop app. The Nuxt MCP server should now be registered.


## Handle Async Setup

As we've seen, Nuxt modules can be asynchronous. For example, you may want to develop a module that needs fetching some API or calling an async function.

However, be careful with asynchronous behaviors as Nuxt will wait for your module to setup before going to the next module and starting the development server, build process, etc. Prefer deferring time-consuming logic to Nuxt hooks.

::warning
If your module takes more than **1 second** to setup, Nuxt will emit a warning about it.
::


## Install nuxt-auth-utils

Install the `nuxt-auth-utils` module using the `nuxt` CLI.

```bash [Terminal]
npx nuxt module add auth-utils
```

::callout
This command will install `nuxt-auth-utils` as dependency and push it in the `modules` section of our `nuxt.config.ts`
::


### Install Dependency

You can install the latest Nuxt Kit by adding it to the `dependencies` section of your `package.json`. However, please consider always explicitly installing the `@nuxt/kit` package even if it is already installed by Nuxt.

::note
`@nuxt/kit` and `@nuxt/schema` are key dependencies for Nuxt. If you are installing it separately, make sure that the versions of `@nuxt/kit` and `@nuxt/schema` are equal to or greater than your `nuxt` version to avoid any unexpected behavior.
::

```json [package.json]
{
  "dependencies": {
    "@nuxt/kit": "npm:@nuxt/kit-nightly@latest"
  }
}
```


## Setup

In order to use `<NuxtPicture>` you should install and enable the Nuxt Image module:

```bash [Terminal]
npx nuxt module add image
```

::read-more{target="_blank" to="https://image.nuxt.com/usage/nuxt-picture"}
Read more about the `<NuxtPicture>` component.
::



## Setup

In order to use `<NuxtImg>` you should install and enable the Nuxt Image module:

```bash [Terminal]
npx nuxt module add image
```


#### Using Lifecycle Hooks for Module Installation and Upgrade

You can define lifecycle hooks that run when your module is first installed or upgraded to a new version. These hooks are useful for performing one-time setup tasks, database migrations, or cleanup operations.

::important
For lifecycle hooks to work, you **must** provide both `meta.name` and `meta.version` in your module definition. The hooks use these values to track the module's installation state in the project's `.nuxtrc` file.
::

Lifecycle hooks run before the main `setup` function, and if a hook throws an error, it's logged but doesn't stop the build process.

**`onInstall`** runs only once when the module is first added to a project.

**`onUpgrade`** runs each time the module version increases (using semver comparison) — but only once for each version bump.

##### Example

```ts
import { defineNuxtModule } from '@nuxt/kit'
import semver from 'semver'

export default defineNuxtModule({
  meta: {
    name: 'my-awesome-module',
    version: '1.2.0', // Required for lifecycle hooks
    configKey: 'myAwesomeModule',
  },
  defaults: {
    apiKey: '',
    enabled: true,
  },

  onInstall (nuxt) {
    // This runs only when the module is first installed
    console.log('Setting up my-awesome-module for the first time!')

    // You might want to:
    // - Create initial configuration files
    // - Set up database schemas
    // - Display welcome messages
    // - Perform initial data migration
  },

  onUpgrade (nuxt, options, previousVersion) {
    // This runs when the module is upgraded to a newer version
    console.log(`Upgrading my-awesome-module from ${previousVersion} to 1.2.0`)

    // You might want to:
    // - Migrate configuration files
    // - Update database schemas
    // - Clean up deprecated files
    // - Display upgrade notes

    if (semver.lt(previousVersion, '1.1.0')) {
      console.log('⚠️  Breaking changes in 1.1.0 - please check the migration guide')
    }
  },

  setup (options, nuxt) {
    // Regular setup logic runs on every build
    if (options.enabled) {
      // Configure the module
    }
  },
})
```


## `installModule`

::callout{type="warning"}
**Deprecated:** Use the [`moduleDependencies`](https://nuxt.com/docs/4.x/api/kit/modules#specifying-module-dependencies) option in `defineNuxtModule` instead. The `installModule` function will be removed (or may become non-blocking) in a future version.
::

Install specified Nuxt module programmatically. This is helpful when your module depends on other modules. You can pass the module options as an object to `inlineOptions` and they will be passed to the module's `setup` function.


#### `objectDefinitions`

##### `defineNuxtComponent`

- **Type**: `array`
- **Default**

```json
[
  "asyncData",
  "setup"
]
```

##### `defineNuxtPlugin`

- **Type**: `array`
- **Default**

```json
[
  "setup"
]
```

##### `definePageMeta`

- **Type**: `array`
- **Default**

```json
[
  "middleware",
  "validate"
]
```


#### `ignoreInitial`

- **Type**: `boolean`
- **Default:** `true`


## Setup

To contribute to Nuxt, you need to set up a local environment.

1. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo){rel="&#x22;nofollow&#x22;"} the [`nuxt/nuxt`](https://github.com/nuxt/nuxt){rel="&#x22;nofollow&#x22;"} repository to your own GitHub account and then [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository){rel="&#x22;nofollow&#x22;"} it to your local device.
2. Ensure using the latest [Node.js](https://nodejs.org/en){rel="&#x22;nofollow&#x22;"}
3. Enable [Corepack](https://github.com/nodejs/corepack){rel="&#x22;nofollow&#x22;"} to have `pnpm` and `yarn`
   ```bash \[Terminal]
   corepack enable
   ```
4. Run `pnpm install --frozen-lockfile`to Install the dependencies with pnpm:
   ```bash \[Terminal]
   pnpm install --frozen-lockfile
   ```
   :note[If you are adding a dependency, please use `pnpm add`. :br
   The `pnpm-lock.yaml` file is the source of truth for all Nuxt dependencies.]
5. Activate the passive development system
   ```bash \[Terminal]
   pnpm dev:prepare
   ```
6. Check out a branch where you can work and commit your changes:
   ```bash \[Terminal]
   git checkout -b my-new-branch
   ```

Then, test your changes against the [playground](https://nuxt.com/docs/4.x/community/framework-contribution#playground) and [test](https://nuxt.com/docs/4.x/community/framework-contribution#testing) your changes before submitting a pull request.


### Install Nuxt Bridge

Install `@nuxt/bridge` and `nuxi` as development dependencies:

::code-group{sync="pm"}
```bash [npm]
npm install -D @nuxt/bridge nuxi
```

```bash [yarn]
yarn add --dev @nuxt/bridge nuxi
```

```bash [pnpm]
pnpm add -D @nuxt/bridge nuxi
```

```bash [bun]
bun add -D @nuxt/bridge nuxi
```

```bash [deno]
deno add -D npm:@nuxt/bridge npm:nuxi
```
::


## `onGlobalSetup`

This function has been removed, but its use cases can be met by using [`useNuxtApp`](https://nuxt.com/docs/4.x/api/composables/use-nuxt-app) or [`useState`](https://nuxt.com/docs/4.x/api/composables/use-state) within `defineNuxtPlugin`. You can also run any custom code within the `setup()` function of a layout.

```diff
- import { onGlobalSetup } from '@nuxtjs/composition-api'

- export default () => {
-   onGlobalSetup(() => {
+ export default defineNuxtPlugin((nuxtApp) => {
+   nuxtApp.hook('vue:setup', () => {
      // ...
    })
- }
+ })
```


### Install Nuxi

Install `nuxi` as a development dependency:

::code-group{sync="pm"}
```bash [npm]
npm install -D nuxi
```

```bash [yarn]
yarn add --dev nuxi
```

```bash [pnpm]
pnpm add -D nuxi
```

```bash [bun]
bun add -D nuxi
```

```bash [deno]
deno add -D npm:nuxi
```
::


# Installation


### Prerequisites

- **Node.js** - [`20.x`](https://nodejs.org/en){rel="&#x22;nofollow&#x22;"} or newer (but we recommend the [active LTS release](https://github.com/nodejs/release#release-schedule){rel="&#x22;nofollow&#x22;"})
- **Text editor** - There is no IDE requirement, but we recommend [Visual Studio Code](https://code.visualstudio.com/){rel="&#x22;nofollow&#x22;"} with the [official Vue extension](https://marketplace.visualstudio.com/items?itemName=Vue.volar){rel="&#x22;nofollow&#x22;"} (previously known as Volar) or [WebStorm](https://www.jetbrains.com/webstorm/){rel="&#x22;nofollow&#x22;"}, which, along with [other JetBrains IDEs](https://www.jetbrains.com/ides/){rel="&#x22;nofollow&#x22;"}, offers great Nuxt support right out-of-the-box. If you use another editor, such as Neovim, you can configure [Vue Language Server](https://github.com/vuejs/language-tools){rel="&#x22;nofollow&#x22;"} support by following the [Vue Language Tools setup guides](https://github.com/vuejs/language-tools/wiki){rel="&#x22;nofollow&#x22;"}.
- **Terminal** - In order to run Nuxt commands

::note
Additional notes for an optimal setup:

- **Node.js**: Make sure to use an even numbered version (20, 22, etc.)
- **Neovim**: When configuring the Vue TypeScript plugin, make sure `location` points to the `@vue/language-server` package directory, not its binary. See the [Neovim setup guide](https://github.com/vuejs/language-tools/wiki/Neovim){rel=""nofollow""} for a working configuration.
- **WSL**: If you are using Windows and experience slow HMR, you may want to try using [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install){rel=""nofollow""} which may solve some performance issues.
- **Windows slow DNS resolution**: Instead of using `localhost:3000` for local dev server on Windows, use `127.0.0.1` for much faster loading experience on browsers.
::

Open a terminal (if you're using [Visual Studio Code](https://code.visualstudio.com){rel="&#x22;nofollow&#x22;"}, you can open an [integrated terminal](https://code.visualstudio.com/docs/terminal/basics){rel="&#x22;nofollow&#x22;"}) and use the following command to create a new starter project:

::code-group{sync="pm"}
```bash [npm]
npm create nuxt@latest <project-name>
```

```bash [yarn]
yarn create nuxt <project-name>
```

```bash [pnpm]
pnpm create nuxt@latest <project-name>
```

```bash [bun]
bun create nuxt@latest <project-name>
```

```bash [deno]
deno -A npm:create-nuxt@latest <project-name>
```
::

::tip
Alternatively, you can find other starters or themes by opening [nuxt.new](https://nuxt.new){rel=""nofollow""} and following the instructions there.
::

Open your project folder in Visual Studio Code:

```bash [Terminal]
code <project-name>
```

Or change directory into your new project from your terminal:

```bash
cd <project-name>
```


### Initializing State

Most of the time, you will want to initialize your state with data that resolves asynchronously. You can use the [`app.vue`](https://nuxt.com/docs/4.x/directory-structure/app/app) component with the [`callOnce`](https://nuxt.com/docs/4.x/api/utils/call-once) util to do so.

```vue [app/app.vue] twoslash
<script setup lang="ts">
const websiteConfig = useState('config')

await callOnce(async () => {
  websiteConfig.value = await $fetch('https://my-cms.com/api/website-config')
})
</script>
```

::tip
This is similar to the [`nuxtServerInit` action](https://v2.nuxt.com/docs/directory-structure/store/#the-nuxtserverinit-action){rel=""nofollow""} in Nuxt 2, which allows filling the initial state of your store server-side before rendering the page.
::

:read-more{to="https://nuxt.com/docs/4.x/api/utils/call-once"}


## Installation

In order to allow you to manage your other testing dependencies, `@nuxt/test-utils` ships with various optional peer dependencies. For example:

- you can choose between `happy-dom` and `jsdom` for a runtime Nuxt environment
- you can choose between `vitest`, `cucumber`, `jest` and `playwright` for end-to-end test runners
- `playwright-core` is only required if you wish to use the built-in browser testing utilities (and are not using `@playwright/test` as your test runner)

::code-group{sync="pm"}
```bash [npm]
npm i --save-dev @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```

```bash [yarn]
yarn add --dev @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```

```bash [pnpm]
pnpm add -D @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```

```bash [bun]
bun add --dev @nuxt/test-utils vitest @vue/test-utils happy-dom playwright-core
```
::


### Setup

1. Add `@nuxt/test-utils/module` to your `nuxt.config` file (optional). It adds a Vitest integration to your Nuxt DevTools which supports running your unit tests in development.
   ```ts twoslash
   export default defineNuxtConfig({
     modules: [
       '@nuxt/test-utils/module',
     ],
   })
   ```
2. Create a `vitest.config.ts` with the following content:
   ```ts twoslash
   import { defineConfig } from 'vitest/config'
   import { defineVitestProject } from '@nuxt/test-utils/config'

   export default defineConfig({
     test: {
       projects: [
         {
           test: {
             name: 'unit',
             include: ['test/unit/*.{test,spec}.ts'],
             environment: 'node',
           },
         },
         {
           test: {
             name: 'e2e',
             include: ['test/e2e/*.{test,spec}.ts'],
             environment: 'node',
           },
         },
         await defineVitestProject({
           test: {
             name: 'nuxt',
             include: ['test/nuxt/*.{test,spec}.ts'],
             environment: 'nuxt',
           },
         }),
       ],
     },
   })
   ```

::tip
When importing `@nuxt/test-utils` in your vitest config, It is necessary to have `"type": "module"` specified in your `package.json` or rename your vitest config file appropriately.

> i.e., `vitest.config.m{ts,js}`.
::

::tip
It is possible to set environment variables for testing by using the `.env.test` file.
::


### Setup

In each `describe` block where you are taking advantage of the `@nuxt/test-utils/e2e` helper methods, you will need to set up the test context before beginning.

```ts [test/my-test.spec.ts] twoslash
import { describe, test } from 'vitest'
import { $fetch, setup } from '@nuxt/test-utils/e2e'

describe('My test', async () => {
  await setup({
    // test context options
  })

  test('my test', () => {
    // ...
  })
})
```

Behind the scenes, `setup` performs a number of tasks in `beforeAll`, `beforeEach`, `afterEach` and `afterAll` to set up the Nuxt test environment correctly.

Please use the options below for the `setup` method.


## Quick Setup

```bash
npx nuxt module add eslint
```

Start your Nuxt app, a `eslint.config.mjs` file will be generated under your project root. You can customize it as needed.

You can learn more about the module and customizations in [Nuxt ESLint's documentation](https://eslint.nuxt.com/packages/module){rel="&#x22;nofollow&#x22;"}.



#### `ignoreInitial`

- **Type**: `boolean`
- **Default:** `true`
