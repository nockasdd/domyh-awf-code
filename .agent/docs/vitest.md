---
library: vitest
version: 3.x
latest: true
category: testing
official_docs: https://vitest.dev
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://vitest.dev/llms-full.txt
---

# Getting Started advanced {#getting-started}

::: warning
This guide lists advanced APIs to run tests via a Node.js script. If you just want to [run tests](/guide/), you probably don't need this. It is primarily used by library authors.
:::

You can import any method from the `vitest/node` entry-point.


## isFinite

* **Type:** `<T>(value: T, message?: string) => void`

Asserts that `value` is a finite number (not NaN, Infinity).

```ts
import { assert, test } from 'vitest'

const colors = 3

test('assert.isFinite', () => {
  assert.isFinite(colors, 'colors is number not NaN or Infinity')
})
```


## Installation

For easier setup, you can use `vitest init browser` command to install required dependencies and create browser configuration.

::: code-group

```bash [npm]
npx vitest init browser
```

```bash [yarn]
yarn exec vitest init browser
```

```bash [pnpm]
pnpx vitest init browser
```

```bash [bun]
bunx vitest init browser
```

:::


### Manual Installation

You can also install packages manually. Vitest always requires a provider to be defined. You can chose either [`preview`](/config/browser/preview), [`playwright`](/config/browser/playwright) or [`webdriverio`](/config/browser/webdriverio).

If you want to just preview how your tests look, you can use the `preview` provider:

::: code-group

```bash [npm]
npm install -D vitest @vitest/browser-preview
```

```bash [yarn]
yarn add -D vitest @vitest/browser-preview
```

```bash [pnpm]
pnpm add -D vitest @vitest/browser-preview
```

```bash [bun]
bun add -D vitest @vitest/browser-preview
```

:::

::: warning
However, to run tests in CI you need to install either [`playwright`](https://npmx.dev/package/playwright) or [`webdriverio`](https://npmx.dev/package/webdriverio). We also recommend switching to either one of them for testing locally instead of using the default `preview` provider since it relies on simulating events instead of using Chrome DevTools Protocol.

If you don't already use one of these tools, we recommend starting with Playwright because it supports parallel execution, which makes your tests run faster.

::: tabs key:provider
\== Playwright
[Playwright](https://npmx.dev/package/playwright) is a framework for Web Testing and Automation.

::: code-group

```bash [npm]
npm install -D vitest @vitest/browser-playwright
```

```bash [yarn]
yarn add -D vitest @vitest/browser-playwright
```

```bash [pnpm]
pnpm add -D vitest @vitest/browser-playwright
```

```bash [bun]
bun add -D vitest @vitest/browser-playwright
```

\== WebdriverIO

[WebdriverIO](https://npmx.dev/package/webdriverio) allows you to run tests locally using the WebDriver protocol.

::: code-group

```bash [npm]
npm install -D vitest @vitest/browser-webdriverio
```

```bash [yarn]
yarn add -D vitest @vitest/browser-webdriverio
```

```bash [pnpm]
pnpm add -D vitest @vitest/browser-webdriverio
```

```bash [bun]
bun add -D vitest @vitest/browser-webdriverio
```

:::


### `vitest init`

`vitest init <name>` can be used to setup project configuration. At the moment, it only supports [`browser`](/guide/browser/) value:

```bash
vitest init browser
```


### Setup

For permanent setup in zsh, add this to your `~/.zshrc`:

```bash

### api.strictPort

* **CLI:** `--api.strictPort`

Set to true to exit if port is already in use, instead of automatically trying the next available port


### sequence.setupFiles

* **CLI:** `--sequence.setupFiles <order>`
* **Config:** [sequence.setupFiles](/config/sequence#sequence-setupfiles)

Changes the order in which setup files are executed. Accepted values are: "list" and "parallel". If set to "list", will run setup files in the order they are defined. If set to "parallel", will run setup files in parallel (default: `"parallel"`)


## Coverage Setup

::: tip
All coverage options are listed in [Coverage Config Reference](/config/coverage).
:::

To test with coverage enabled, you can pass the `--coverage` flag in CLI or set `coverage.enabled` in `vitest.config.ts`:

::: code-group

```json [package.json]
{
  "scripts": {
    "test": "vitest",
    "coverage": "vitest run --coverage"
  }
}
```

```ts [vitest.config.ts]
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    coverage: {
      enabled: true
    },
  },
})
```

:::


# Getting Started


## Automatic Dependency Installation

Vitest will prompt you to install certain dependencies if they are not already installed. You can disable this behavior by setting the `VITEST_SKIP_INSTALL_CHECKS=1` environment variable.


# globalSetup

* **Type:** `string | string[]`

Path to global setup files relative to project [root](/config/root).

A global setup file can either export named functions `setup` and `teardown` or a `default` function that returns a teardown function:

::: code-group

```js [exports]
export function setup(project) {
  console.log('setup')
}

export function teardown() {
  console.log('teardown')
}
```

```js [default]
export default function setup(project) {
  console.log('setup')

  return function teardown() {
    console.log('teardown')
  }
}
```

:::

Note that the `setup` method and a `default` function receive a [test project](/api/advanced/test-project) as the first argument. The global setup is called before the test workers are created and only if there is at least one test queued, and teardown is called after all test files have finished running. In [watch mode](/config/watch), the teardown is called before the process is exited instead. If you need to reconfigure your setup before the test rerun, you can use [`onTestsRerun`](#handling-test-reruns) hook instead.

Multiple global setup files are possible. `setup` and `teardown` are executed sequentially with teardown in reverse order.

::: danger
Beware that the global setup is running in a different global scope before test workers are even created, so your tests don't have access to global variables defined here. However, you can pass down serializable data to tests via [`provide`](/config/provide) method and read them in your tests via `inject` imported from `vitest`:

:::code-group

```ts [example.test.ts]
import { inject } from 'vitest'

inject('wsPort') === 3000
```

```ts [globalSetup.ts]
import type { TestProject } from 'vitest/node'

export default function setup(project: TestProject) {
  project.provide('wsPort', 3000)
}

declare module 'vitest' {
  export interface ProvidedContext {
    wsPort: number
  }
}
```

If you need to execute code in the same process as tests, use [`setupFiles`](/config/setupfiles) instead, but note that it runs before every test file.
:::


## Setup

To get started, put a `if (import.meta.vitest)` block at the end of your source file and write some tests inside it. For example:

```ts [src/index.ts]
// the implementation
export function add(...args: number[]) {
  return args.reduce((a, b) => a + b, 0)
}

// in-source test suites
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest
  it('add', () => {
    expect(add()).toBe(0)
    expect(add(1)).toBe(1)
    expect(add(1, 2, 3)).toBe(6)
  })
}
```

Update the `includeSource` config for Vitest to grab the files under `src/`:

```ts [vitest.config.ts]
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    includeSource: ['src/**/*.{js,ts}'], // [!code ++]
  },
})
```

Then you can start to test!

```bash
$ npx vitest
```


## userEvent.setup

```ts
function setup(): UserEvent
```

Creates a new user event instance. This is useful if you need to keep the state of keyboard to press and release buttons correctly.

::: warning
Unlike `@testing-library/user-event`, the default `userEvent` instance from `vitest/browser` is created once, not every time its methods are called! You can see the difference in how it works in this snippet:

```ts
import { userEvent as vitestUserEvent } from 'vitest/browser'
import { userEvent as originalUserEvent } from '@testing-library/user-event'

await vitestUserEvent.keyboard('{Shift}') // press shift without releasing
await vitestUserEvent.keyboard('{/Shift}') // releases shift

await originalUserEvent.keyboard('{Shift}') // press shift without releasing
await originalUserEvent.keyboard('{/Shift}') // DID NOT release shift because the state is different
```

This behaviour is more useful because we do not emulate the keyboard, we actually press the Shift, so keeping the original behaviour would cause unexpected issues when typing in the field.
:::


# Multiple Setups

You can specify several different browser setups using the [`browser.instances`](/config/browser/instances) option.

The main advantage of using the `browser.instances` over the [test projects](/guide/projects) is improved caching. Every project will use the same Vite server meaning the file transform and [dependency pre-bundling](https://vite.dev/guide/dep-pre-bundling.html) has to happen only once.


## Different Setups

You can also specify different config options independently from the browser (although, the instances *can* also have `browser` fields):

::: code-group

```ts [vitest.config.ts]
import { defineConfig } from 'vitest/config'
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: playwright(),
      headless: true,
      instances: [
        {
          browser: 'chromium',
          name: 'chromium-1',
          setupFiles: ['./ratio-setup.ts'],
          provide: {
            ratio: 1,
          },
        },
        {
          browser: 'chromium',
          name: 'chromium-2',
          provide: {
            ratio: 2,
          },
        },
      ],
    },
  },
})
```

```ts [example.test.ts]
import { expect, inject, test } from 'vitest'
import { globalSetupModifier } from './example.js'

test('ratio works', () => {
  expect(inject('ratio') * globalSetupModifier).toBe(14)
})
```

:::

In this example Vitest will run all tests in `chromium` browser, but execute a `'./ratio-setup.ts'` file only in the first configuration and inject a different `ratio` value depending on the [`provide` field](/config/provide).

::: warning
Note that you need to define the custom `name` value if you are using the same browser name because Vitest will assign the `browser` as the project name otherwise.
:::


# Recipes


## onInit

```ts
function onInit(vitest: Vitest): Awaitable<void>
```

This method is called when [Vitest](/api/advanced/vitest) was initiated or started, but before the tests were filtered.

::: info
Internally this method is called inside [`vitest.start`](/api/advanced/vitest#start), [`vitest.init`](/api/advanced/vitest#init) or [`vitest.mergeReports`](/api/advanced/vitest#mergereports). If you are using programmatic API, make sure to call either one depending on your needs before calling [`vitest.runTestSpecifications`](/api/advanced/vitest#runtestspecifications), for example. Built-in CLI will always run methods in correct order.
:::

Note that you can also get access to `vitest` instance from test cases, suites and test modules via a [`project`](/api/advanced/test-project) property, but it might also be useful to store a reference to `vitest` in this method.

::: details Example

```ts
import type { Reporter, TestSpecification, Vitest } from 'vitest/node'

class MyReporter implements Reporter {
  private vitest!: Vitest

  onInit(vitest: Vitest) {
    this.vitest = vitest
  }

  onTestRunStart(specifications: TestSpecification[]) {
    console.log(
      specifications.length,
      'test files will run in',
      this.vitest.config.root,
    )
  }
}

export default new MyReporter()
```

:::


## onBrowserInit {#onbrowserinit}

```ts
function onBrowserInit(project: TestProject): Awaitable<void>
```

This method is called when the browser instance is initiated. It receives an instance of the project for which the browser is initiated. `project.browser` will always be defined when this method is called.


## sequence.setupFiles {#sequence-setupfiles}

* **Type**: `'list' | 'parallel'`
* **Default**: `'parallel'`
* **CLI**: `--sequence.setupFiles=<value>`

Changes the order in which setup files are executed.

* `list` will run setup files in the order they are defined
* `parallel` will run setup files in parallel

---

---
url: /config/server.md
---


# setupFiles

* **Type:** `string | string[]`

Paths to setup files resolved relative to the [`root`](/config/root). They will run before each *test file* in the same process. By default, all test files run in parallel, but you can configure it with [`sequence.setupFiles`](/config/sequence#sequence-setupfiles) option.

Vitest will ignore any exports from these files.

:::warning
Note that setup files are executed in the same process as tests, unlike [`globalSetup`](/config/globalsetup) that runs once in the main thread before any test worker is created.
:::

:::info
Editing a setup file will automatically trigger a rerun of all tests.
:::

If you have a heavy process running in the background, you can use `process.env.VITEST_POOL_ID` (integer-like string) inside to distinguish between workers and spread the workload.

:::warning
If [isolation](/config/isolate) is disabled, imported modules are cached, but the setup file itself is executed again before each test file, meaning that you are accessing the same global object before each test file. Make sure you are not doing the same thing more than necessary.

For example, you may rely on a global variable:

```ts
import { config } from '@some-testing-lib'

if (!globalThis.setupInitialized) {
  config.plugins = [myCoolPlugin]
  computeHeavyThing()
  globalThis.setupInitialized = true
}

// hooks reset before each test file
afterEach(() => {
  cleanup()
})

globalThis.resetBeforeEachTest = true
```

:::

---

---
url: /config/silent.md
---


## API


#### Setup and Cleanup with `onCleanup`

For fixtures that need setup or cleanup logic, use a function. The `onCleanup` callback registers teardown logic that runs after the fixture's scope ends:

```ts
import { test as baseTest } from 'vitest'

export const test = baseTest
  .extend('tempFile', async ({}, { onCleanup }) => {
    const filePath = `/tmp/test-${Date.now()}.txt`
    await fs.writeFile(filePath, 'test data')

    // Register cleanup - runs after test completes
    onCleanup(async () => {
      await fs.unlink(filePath)
    })

    return filePath
  })
```

For more complex examples:

```ts
const test = baseTest
  .extend('database', { scope: 'file' }, async ({}, { onCleanup }) => {
    const db = await createDatabase()
    await db.connect()

    onCleanup(async () => {
      await db.disconnect()
    })

    return db
  })
  .extend('user', async ({ database }, { onCleanup }) => {
    const user = await database.createTestUser()

    onCleanup(async () => {
      await database.deleteUser(user.id)
    })

    return user
  })
```

::: warning
The `onCleanup` function can only be called **once per fixture**. If you need multiple cleanup operations, either combine them into a single cleanup function, or split your fixture into multiple smaller fixtures:

```ts
// ❌ This will throw an error
const test = baseTest
  .extend('resources', async ({}, { onCleanup }) => {
    const a = await acquireA()
    onCleanup(() => releaseA(a))

    const b = await acquireB()
    onCleanup(() => releaseB(b)) // Error: onCleanup can only be called once

    return { a, b }
  })

// ✅ Split into separate fixtures (recommended)
const test = baseTest
  .extend('resourceA', async ({}, { onCleanup }) => {
    const a = await acquireA()
    onCleanup(() => releaseA(a))
    return a
  })
  .extend('resourceB', async ({}, { onCleanup }) => {
    const b = await acquireB()
    onCleanup(() => releaseB(b))
    return b
  })
```

Splitting into separate fixtures is the recommended approach as it provides better isolation and makes dependencies explicit.
:::


### Fixture Initialization

Vitest runner will smartly initialize your fixtures and inject them into the test context based on usage.

```ts
import { test as baseTest } from 'vitest'

const test = baseTest
  .extend('database', async () => {
    console.log('database initializing')
    return createDatabase()
  })
  .extend('cache', async () => {
    return createCache()
  })

// database will not run
test('no fixtures needed', () => {})
test('only cache', ({ cache }) => {})

// database will run
test('needs database', ({ database }) => {})
```

::: warning
When using `test.extend()` with fixtures, you should always use the object destructuring pattern `{ database }` to access context both in fixture function and test function.

```ts
test('context must be destructured', (context) => { // [!code --]
  expect(context.database).toBeDefined()
})

test('context must be destructured', ({ database }) => { // [!code ++]
  expect(database).toBeDefined()
})
```

:::


### 1. Initialization Phase

When you run `vitest`, the framework first loads your configuration and prepares the test environment.

**What happens:**

* [Command-line](/guide/cli) arguments are parsed
* [Configuration file](/config/) is loaded
* Project structure is validated

This phase can run again if the config file or one of its imports changes.

**Scope:** Main process (before any test workers are created)


### 2. Global Setup Phase

If you have configured [`globalSetup`](/config/globalsetup) files, they run once before any test workers are created.

**What happens:**

* `setup()` functions (or exported `default` function) from global setup files execute sequentially
* Multiple global setup files run in the order they are defined

**Scope:** Main process (separate from test workers)

**Important notes:**

* Global setup runs in a **different global scope** from your tests
* Tests cannot access variables defined in global setup (use [`provide`/`inject`](/config/provide) instead)
* Global setup only runs if there is at least one test queued

```ts [globalSetup.ts]
export function setup(project) {
  // Runs once before all tests
  console.log('Global setup')

  // Share data with tests
  project.provide('apiUrl', 'http://localhost:3000')
}

export function teardown() {
  // Runs once after all tests
  console.log('Global teardown')
}
```


### 4. Test File Setup Phase

Before each test file runs, [setup files](/config/setupfiles) are executed.

**What happens:**

* Setup files run in the same process as your tests
* By default, setup files run in **parallel** (configurable via [`sequence.setupFiles`](/config/sequence#sequence-setupfiles))
* Setup files execute before **each test file**
* Any global *state* or configuration can be initialized here

**Scope:** Worker process (same as your tests)

**Important notes:**

* If [isolation](/config/isolate) is disabled, setup files still rerun before each test file to trigger side effects, but imported modules are cached
* Editing a setup file triggers a rerun of all tests in watch mode

```ts [setupFile.ts]
import { afterEach } from 'vitest'

// Runs before each test file
console.log('Setup file executing')

// Register hooks that apply to all tests
afterEach(() => {
  cleanup()
})
```


## Getting Started

::: warning Browser Rendering Differences
Visual regression tests are **inherently unstable across different
environments**. Screenshots will look different on different machines because
of:

* Font rendering (the big one. Windows, macOS, Linux, they all render text
  differently)
* GPU drivers and hardware acceleration
* Whether you're running headless or not
* Browser settings and versions
* ...and honestly, sometimes just the phase of the moon

That's why Vitest includes the browser and platform in screenshot names (like
`button-chromium-darwin.png`).

For stable tests, use the same environment everywhere. We **strongly recommend**
cloud services like
[Azure App Testing](https://azure.microsoft.com/en-us/products/app-testing/)
or [Docker containers](https://playwright.dev/docs/docker).
:::

Visual regression testing in Vitest can be done through the
[`toMatchScreenshot` assertion](/api/browser/assertions.html#tomatchscreenshot):

```ts
import { expect, test } from 'vitest'
import { page } from 'vitest/browser'

test('hero section looks correct', async () => {
  // ...the rest of the test

  // capture and compare screenshot
  await expect(page.getByTestId('hero')).toMatchScreenshot('hero-section')
})
```


# ...browser setup
- name: Visual Regression Testing
  run: npm run test:visual
```
