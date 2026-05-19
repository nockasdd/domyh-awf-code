---
library: vite
version: 6.x
latest: true
category: frontend
official_docs: https://vite.dev
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/vitejs/vite/contents/docs/guide
---

# Features

At the very basic level, developing using Vite is not that different from using a static file server. However, Vite provides many enhancements over native ESM imports to support various features that are typically seen in bundler-based setups.


### TypeScript Compiler Options

Vite respects some of the options in `tsconfig.json` and sets the corresponding esbuild options. For each file, Vite uses the `tsconfig.json` in the closest parent directory. If that `tsconfig.json` contains a [`references`](https://www.typescriptlang.org/tsconfig/#references) field, Vite will use the referenced config file that satisfies the [`include`](https://www.typescriptlang.org/tsconfig/#include) and [`exclude`](https://www.typescriptlang.org/tsconfig/#exclude) fields.

When the options are set in both the Vite config and the `tsconfig.json`, the value in the Vite config takes precedence.

Some configuration fields under `compilerOptions` in `tsconfig.json` require special attention.


#### Other Compiler Options Affecting the Build Result

- [`extends`](https://www.typescriptlang.org/tsconfig#extends)
- [`importsNotUsedAsValues`](https://www.typescriptlang.org/tsconfig#importsNotUsedAsValues)
- [`preserveValueImports`](https://www.typescriptlang.org/tsconfig#preserveValueImports)
- [`verbatimModuleSyntax`](https://www.typescriptlang.org/tsconfig#verbatimModuleSyntax)
- [`jsx`](https://www.typescriptlang.org/tsconfig#jsx)
- [`jsxFactory`](https://www.typescriptlang.org/tsconfig#jsxFactory)
- [`jsxFragmentFactory`](https://www.typescriptlang.org/tsconfig#jsxFragmentFactory)
- [`jsxImportSource`](https://www.typescriptlang.org/tsconfig#jsxImportSource)
- [`experimentalDecorators`](https://www.typescriptlang.org/tsconfig#experimentalDecorators)

::: tip `skipLibCheck`
Vite starter templates have `"skipLibCheck": "true"` by default to avoid typechecking dependencies, as they may choose to only support specific versions and configurations of TypeScript. You can learn more at [vuejs/vue-cli#5688](https://github.com/vuejs/vue-cli/pull/5688).
:::


## api plugin


# Plugin API

Vite plugins extends Rolldown's plugin interface with a few extra Vite-specific options. As a result, you can write a Vite plugin once and have it work for both dev and build.

**It is recommended to go through [Rolldown's plugin documentation](https://rolldown.rs/apis/plugin-api) first before reading the sections below.**


## Plugins Config

Users will add plugins to the project `devDependencies` and configure them using the `plugins` array option.

```js [vite.config.js]
import vitePlugin from 'vite-plugin-feature'
import rollupPlugin from 'rollup-plugin-feature'

export default defineConfig({
  plugins: [vitePlugin(), rollupPlugin()],
})
```

Falsy plugins will be ignored, which can be used to easily activate or deactivate plugins.

`plugins` also accepts presets including several plugins as a single element. This is useful for complex features (like framework integration) that are implemented using several plugins. The array will be flattened internally.

```js
// framework-plugin
import frameworkRefresh from 'vite-plugin-framework-refresh'
import frameworkDevtools from 'vite-plugin-framework-devtools'

export default function framework(config) {
  return [frameworkRefresh(config), frameworkDevTools(config)]
}
```

```js [vite.config.js]
import { defineConfig } from 'vite'
import framework from 'vite-plugin-framework'

export default defineConfig({
  plugins: [framework()],
})
```


### `config`

- **Type:** `(config: UserConfig, env: { mode: string, command: string }) => UserConfig | null | void`
- **Kind:** `async`, `sequential`

  Modify Vite config before it's resolved. The hook receives the raw user config (CLI options merged with config file) and the current config env which exposes the `mode` and `command` being used. It can return a partial config object that will be deeply merged into existing config, or directly mutate the config (if the default merging cannot achieve the desired result).

  **Example:**

  ```js
  // return partial config (recommended)
  const partialConfigPlugin = () => ({
    name: 'return-partial',
    config: () => ({
      resolve: {
        alias: {
          foo: 'bar',
        },
      },
    }),
  })

  // mutate the config directly (use only when merging doesn't work)
  const mutateConfigPlugin = () => ({
    name: 'mutate-config',
    config(config, { command }) {
      if (command === 'build') {
        config.root = 'foo'
      }
    },
  })
  ```

  ::: warning Note
  User plugins are resolved before running this hook so injecting other plugins inside the `config` hook will have no effect.
  :::


### `configResolved`

- **Type:** `(config: ResolvedConfig) => void | Promise<void>`
- **Kind:** `async`, `parallel`

  Called after the Vite config is resolved. Use this hook to read and store the final resolved config. It is also useful when the plugin needs to do something different based on the command being run.

  **Example:**

  ```js
  const examplePlugin = () => {
    let config

    return {
      name: 'read-config',

      configResolved(resolvedConfig) {
        // store the resolved config
        config = resolvedConfig
      },

      // use stored config in other hooks
      transform(code, id) {
        if (config.command === 'serve') {
          // dev: plugin invoked by dev server
        } else {
          // build: plugin invoked by Rollup
        }
      },
    }
  }
  ```

  Note that the `command` value is `serve` in dev (in the cli `vite`, `vite dev`, and `vite serve` are aliases).


### `configureServer`

- **Type:** `(server: ViteDevServer) => (() => void) | void | Promise<(() => void) | void>`
- **Kind:** `async`, `sequential`
- **See also:** [ViteDevServer](./api-javascript#vitedevserver)

  Hook for configuring the dev server. The most common use case is adding custom middlewares to the internal [connect](https://github.com/senchalabs/connect) app:

  ```js
  const myPlugin = () => ({
    name: 'configure-server',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // custom handle request...
      })
    },
  })
  ```

  **Injecting Post Middleware**

  The `configureServer` hook is called before internal middlewares are installed, so the custom middlewares will run before internal middlewares by default. If you want to inject a middleware **after** internal middlewares, you can return a function from `configureServer`, which will be called after internal middlewares are installed:

  ```js
  const myPlugin = () => ({
    name: 'configure-server',
    configureServer(server) {
      // return a post hook that is called after internal middlewares are
      // installed
      return () => {
        server.middlewares.use((req, res, next) => {
          // custom handle request...
        })
      }
    },
  })
  ```

  **Storing Server Access**

  In some cases, other plugin hooks may need access to the dev server instance (e.g. accessing the WebSocket server, the file system watcher, or the module graph). This hook can also be used to store the server instance for access in other hooks:

  ```js
  const myPlugin = () => {
    let server
    return {
      name: 'configure-server',
      configureServer(_server) {
        server = _server
      },
      transform(code, id) {
        if (server) {
          // use server...
        }
      },
    }
  }
  ```

  Note `configureServer` is not called when running the production build so your other hooks need to guard against its absence.


### `configurePreviewServer`

- **Type:** `(server: PreviewServer) => (() => void) | void | Promise<(() => void) | void>`
- **Kind:** `async`, `sequential`
- **See also:** [PreviewServer](./api-javascript#previewserver)

  Same as [`configureServer`](/guide/api-plugin.html#configureserver) but for the preview server. Similarly to `configureServer`, the `configurePreviewServer` hook is called before other middlewares are installed. If you want to inject a middleware **after** other middlewares, you can return a function from `configurePreviewServer`, which will be called after internal middlewares are installed:

  ```js
  const myPlugin = () => ({
    name: 'configure-preview-server',
    configurePreviewServer(server) {
      // return a post hook that is called after other middlewares are
      // installed
      return () => {
        server.middlewares.use((req, res, next) => {
          // custom handle request...
        })
      }
    },
  })
  ```


### Removed `build.rollupOptions.watch.chokidar` option

The `build.rollupOptions.watch.chokidar` option was removed. Please migrate to the [`build.rolldownOptions.watch.watcher`](https://rolldown.rs/reference/InputOptions.watch#watcher) option.


### Removed object form `build.rollupOptions.output.manualChunks` and deprecate function form one

The object form `output.manualChunks` option is not supported anymore. The function form `output.manualChunks` is deprecated. Rolldown has the more flexible [`codeSplitting`](https://rolldown.rs/reference/OutputOptions.codeSplitting) option. See Rolldown's docs for more details about `codeSplitting`: [Manual Code Splitting - Rolldown](https://rolldown.rs/in-depth/manual-code-splitting).


## api environment runtimes


# Environment API for Runtimes

:::info Release Candidate
The Environment API is generally in the release candidate phase. We'll maintain stability in the APIs between major releases to allow the ecosystem to experiment and build upon them. However, note that [some specific APIs](/changes/#considering) are still considered experimental.

We plan to stabilize these new APIs (with potential breaking changes) in a future major release once downstream projects have had time to experiment with the new features and validate them.

Resources:

- [Feedback discussion](https://github.com/vitejs/vite/discussions/16358) where we are gathering feedback about the new APIs.
- [Environment API PR](https://github.com/vitejs/vite/pull/16471) where the new APIs were implemented and reviewed.

Please share your feedback with us.
:::


## Environment Factories

Environments factories are intended to be implemented by Environment providers like Cloudflare, and not by end users. Environment factories return a `EnvironmentOptions` for the most common case of using the target runtime for both dev and build environments. The default environment options can also be set so the user doesn't need to do it.

```ts
function createWorkerdEnvironment(
  userConfig: EnvironmentOptions,
): EnvironmentOptions {
  return mergeConfig(
    {
      resolve: {
        conditions: [
          /*...*/
        ],
      },
      dev: {
        createEnvironment(name, config) {
          return createWorkerdDevEnvironment(name, config, {
            hot: true,
            transport: customHotChannel(),
          })
        },
      },
      build: {
        createEnvironment(name, config) {
          return createWorkerdBuildEnvironment(name, config)
        },
      },
    },
    userConfig,
  )
}
```

Then the config file can be written as:

```js
import { createWorkerdEnvironment } from 'vite-environment-workerd'

export default {
  environments: {
    ssr: createWorkerdEnvironment({
      build: {
        outDir: '/dist/ssr',
      },
    }),
    rsc: createWorkerdEnvironment({
      build: {
        outDir: '/dist/rsc',
      },
    }),
  },
}
```

and frameworks can use an environment with the workerd runtime to do SSR using:

```js
const ssrEnvironment = server.environments.ssr
```


## Creating a New Environment Factory

A Vite dev server exposes two environments by default: a `client` environment and an `ssr` environment. The client environment is a browser environment by default, and the module runner is implemented by importing the virtual module `/@vite/client` to client apps. The SSR environment runs in the same Node runtime as the Vite server by default and allows application servers to be used to render requests during dev with full HMR support.

The transformed source code is called a module, and the relationships between the modules processed in each environment are kept in a module graph. The transformed code for these modules is sent to the runtimes associated with each environment to be executed. When a module is evaluated in the runtime, its imported modules will be requested triggering the processing of a section of the module graph.

A Vite Module Runner allows running any code by processing it with Vite plugins first. It is different from `server.ssrLoadModule` because the runner implementation is decoupled from the server. This allows library and framework authors to implement their layer of communication between the Vite server and the runner. The browser communicates with its corresponding environment using the server WebSocket and through HTTP requests. The Node Module runner can directly do function calls to process modules as it is running in the same process. Other environments could run modules connecting to a JS runtime like workerd, or a Worker Thread as Vitest does.

```dot
digraph module_runner {
  rankdir=LR
  node [shape=box style="rounded,filled" fontname="Arial" fontsize=11 margin="0.2,0.1" fontcolor="${#3c3c43|#ffffff}" color="${#c2c2c4|#3c3f44}"]
  edge [color="${#67676c|#98989f}" fontname="Arial" fontsize=10 fontcolor="${#67676c|#98989f}"]
  bgcolor="transparent"
  compound=true

  subgraph cluster_server {
    label="Vite Dev Server (Node.js)" labeljust=l fontname="Arial" fontsize=12
    style="rounded,filled" fillcolor="${#f6f6f7|#1a1a1f}" color="${#c2c2c4|#3c3f44}"
    fontcolor="${#3c3c43|#ffffff}"

    subgraph cluster_env {
      label="DevEnvironment" labeljust=l fontname="Arial" fontsize=11
      style="rounded,filled" fillcolor="${#f2ecfc|#2c273e}" color="${#c2c2c4|#3c3f44}"
      fontcolor="${#3c3c43|#ffffff}"

      plugins [label="Plugin\nPipeline" fillcolor="${#e9eaff|#222541}"]
      mg [label="Module\nGraph" fillcolor="${#e9eaff|#222541}"]
      hot [label="HotChannel" fillcolor="${#fcf4dc|#38301a}"]

      plugins -> mg [dir=both]
      mg -> hot [style=invis]
    }
  }

  subgraph cluster_runtime {
    label="Target Runtime" labeljust=l fontname="Arial" fontsize=12
    style="rounded,filled" fillcolor="${#f0fdf4|#131b15}" color="${#c2c2c4|#3c3f44}"
    fontcolor="${#3c3c43|#ffffff}"

    subgraph cluster_runner {
      label="ModuleRunner" labeljust=l fontname="Arial" fontsize=11
      style="rounded,filled" fillcolor="${#def5ed|#15312d}" color="${#c2c2c4|#3c3f44}"
      fontcolor="${#3c3c43|#ffffff}"

      evaluator [label="Module\nEvaluator" fillcolor="${#def5ed|#15312d}"]
      transport [label="Transport" fillcolor="${#fcf4dc|#38301a}"]
    }
  }

  hot -> transport [label="HMR / Module\nfetch & invoke" dir=both style=bold color="${#6f42c1|#c8abfa}"]
}
```

One of the goals of this feature is to provide a customizable API to process and run code. Users can create new environment factories using the exposed primitives.

```ts
import { DevEnvironment, HotChannel } from 'vite'

function createWorkerdDevEnvironment(
  name: string,
  config: ResolvedConfig,
  context: DevEnvironmentContext
) {
  const connection = /* ... */
  const transport: HotChannel = {
    on: (listener) => { connection.on('message', listener) },
    send: (data) => connection.send(data),
  }

  const workerdDevEnvironment = new DevEnvironment(name, config, {
    options: {
      resolve: { conditions: ['custom'] },
      ...context.options,
    },
    hot: true,
    transport,
  })
  return workerdDevEnvironment
}
```

There are [multiple communication levels for the `DevEnvironment`](/guide/api-environment-frameworks#devenvironment-communication-levels). To make it easier for frameworks to write runtime agnostic code, we recommend to implement the most flexible communication level possible.


## `ModuleRunnerOptions`

```ts twoslash
import type {
  InterceptorOptions as InterceptorOptionsRaw,
  ModuleRunnerHmr as ModuleRunnerHmrRaw,
  EvaluatedModules,
} from 'vite/module-runner'
import type { Debug } from '@type-challenges/utils'

type InterceptorOptions = Debug<InterceptorOptionsRaw>
type ModuleRunnerHmr = Debug<ModuleRunnerHmrRaw>
/** see below */
type ModuleRunnerTransport = unknown

// ---cut---
interface ModuleRunnerOptions {
  /**
   * A set of methods to communicate with the server.
   */
  transport: ModuleRunnerTransport
  /**
   * Configure how source maps are resolved.
   * Prefers `node` if `process.setSourceMapsEnabled` is available.
   * Otherwise it will use `prepareStackTrace` by default which overrides
   * `Error.prepareStackTrace` method.
   * You can provide an object to configure how file contents and
   * source maps are resolved for files that were not processed by Vite.
   */
  sourcemapInterceptor?:
    | false
    | 'node'
    | 'prepareStackTrace'
    | InterceptorOptions
  /**
   * Disable HMR or configure HMR options.
   *
   * @default true
   */
  hmr?: boolean | ModuleRunnerHmr
  /**
   * Custom module cache. If not provided, it creates a separate module
   * cache for each module runner instance.
   */
  evaluatedModules?: EvaluatedModules
}
```


## Config


## api javascript


# JavaScript API

Vite's JavaScript APIs are fully typed, and it's recommended to use TypeScript or enable JS type checking in VS Code to leverage the intellisense and validation.


## `InlineConfig`

The `InlineConfig` interface extends `UserConfig` with additional properties:

- `configFile`: specify config file to use. If not set, Vite will try to automatically resolve one from project root. Set to `false` to disable auto resolving.


#### Usage

```bash
vite [root]
```


## api environment plugins


# Environment API for Plugins

:::info Release Candidate
The Environment API is generally in the release candidate phase. We'll maintain stability in the APIs between major releases to allow the ecosystem to experiment and build upon them. However, note that [some specific APIs](/changes/#considering) are still considered experimental.

We plan to stabilize these new APIs (with potential breaking changes) in a future major release once downstream projects have had time to experiment with the new features and validate them.

Resources:

- [Feedback discussion](https://github.com/vitejs/vite/discussions/16358) where we are gathering feedback about the new APIs.
- [Environment API PR](https://github.com/vitejs/vite/pull/16471) where the new APIs were implemented and reviewed.

Please share your feedback with us.
:::


## Environment in Build Hooks

In the same way as during dev, plugin hooks also receive the environment instance during build, replacing the `ssr` boolean.
This also works for `renderChunk`, `generateBundle`, and other build only hooks.


## api environment frameworks


# Environment API for Frameworks

:::info Release Candidate
The Environment API is generally in the release candidate phase. We'll maintain stability in the APIs between major releases to allow the ecosystem to experiment and build upon them. However, note that [some specific APIs](/changes/#considering) are still considered experimental.

We plan to stabilize these new APIs (with potential breaking changes) in a future major release once downstream projects have had time to experiment with the new features and validate them.

Resources:

- [Feedback discussion](https://github.com/vitejs/vite/discussions/16358) where we are gathering feedback about the new APIs.
- [Environment API PR](https://github.com/vitejs/vite/pull/16471) where the new APIs were implemented and reviewed.

Please share your feedback with us.
:::


# Getting Started

<audio id="vite-audio">
  <source src="/vite.mp3" type="audio/mpeg">
</audio>


## Manual Installation

In your project, you can install the `vite` CLI using:

::: code-group

```bash [npm]
$ npm install -D vite
```

```bash [Yarn]
$ yarn add -D vite
```

```bash [pnpm]
$ pnpm add -D vite
```

```bash [Bun]
$ bun add -D vite
```

```bash [Deno]
$ deno add -D npm:vite
```

:::

And create an `index.html` file like this:

```html
<p>Hello Vite!</p>
```

Then run the appropriate CLI command in your terminal:

::: code-group

```bash [npm]
$ npx vite
```

```bash [Yarn]
$ yarn vite
```

```bash [pnpm]
$ pnpm vite
```

```bash [Bun]
$ bunx vite
```

```bash [Deno]
$ deno run -A npm:vite
```

:::

The `index.html` will be served on `http://localhost:5173`.


## env and mode
