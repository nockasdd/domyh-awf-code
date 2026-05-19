---
library: nextjs
version: 16.x
latest: true
category: frontend
official_docs: https://nextjs.org/docs
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://nextjs.org/docs/llms-full.txt
---

# Next.js Documentation

@doc-version: >=v16.2.1
@doc-version-notes: Some features may have extended or refined behavior in minor or patch releases
@router: App Router
@router-note: Unless otherwise noted in each section, these documents apply to the App Router


---
title: Getting Started
description: Learn how to create full-stack web applications with the Next.js App Router.
url: "https://nextjs.org/docs/app/getting-started"
version: 16.2.1
---


# Getting Started

Welcome to the Next.js documentation!

This **Getting Started** section will help you create your first Next.js app and learn the core features you'll use in every project.


# Installation

Create a new Next.js app and run it locally.


## Quick start

1. Create a new Next.js app named `my-app`
2. `cd my-app` and start the dev server.
3. Visit `http://localhost:3000`.

```bash package="pnpm"
pnpm create next-app@latest my-app --yes
cd my-app
pnpm dev
```

```bash package="npm"
npx create-next-app@latest my-app --yes
cd my-app
npm run dev
```

```bash package="yarn"
yarn create next-app@latest my-app --yes
cd my-app
yarn dev
```

```bash package="bun"
bun create next-app@latest my-app --yes
cd my-app
bun dev
```

* `--yes` skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias `@/*`, and includes `AGENTS.md` (with a `CLAUDE.md` that references it) to guide coding agents to write up-to-date Next.js code.


## Manual installation

To manually create a new Next.js app, install the required packages:

```bash package="pnpm"
pnpm i next@latest react@latest react-dom@latest
```

```bash package="npm"
npm i next@latest react@latest react-dom@latest
```

```bash package="yarn"
yarn add next@latest react@latest react-dom@latest
```

```bash package="bun"
bun add next@latest react@latest react-dom@latest
```

> **Good to know**:
>
> * The `App Router` uses [React canary releases](https://react.dev/blog/2023/05/03/react-canaries) built-in, which include all the stable React 19 changes, as well as newer features being validated in frameworks, but you should still declare react and react-dom in package.json for tooling and ecosystem compatibility.
> * The `Pages Router` uses the React version from your `package.json`.

Then, add the following scripts to your `package.json` file:

```json filename="package.json"
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

These scripts refer to the different stages of developing an application:

* `next dev`: Starts the development server using Turbopack (default bundler).
* `next build`: Builds the application for production.
* `next start`: Starts the production server.
* `eslint`: Runs ESLint.

Turbopack is now the default bundler. To use Webpack run `next dev --webpack` or `next build --webpack`. See the [Turbopack docs](/docs/app/api-reference/turbopack) for configuration details.


## Getting started


### 4. Check your Tailwind CSS setup

If you're using Tailwind CSS, make sure it's set up correctly.

A common mistake is configuring your `content` array in a way which includes `node_modules` or other large directories of files that should not be scanned.

Tailwind CSS version 3.4.8 or newer will warn you about settings that might slow down your build.

1. In your `tailwind.config.js`, be specific about which files to scan:

   ```jsx
   module.exports = {
     content: [
       './src/**/*.{js,ts,jsx,tsx}', // Good
       // This might be too broad
       // It will match `packages/**/node_modules` too
       // '../../packages/**/*.{js,ts,jsx,tsx}',
     ],
   }
   ```

2. Avoid scanning unnecessary files:

   ```jsx
   module.exports = {
     content: [
       // Better - only scans the 'src' folder
       '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
     ],
   }
   ```


## Getting started

**Requirements:** Next.js 16 or above

Add `next-devtools-mcp` to the `.mcp.json` file at the root of your project:

```json filename=".mcp.json"
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

That's it! When you start your development server, `next-devtools-mcp` will automatically discover and connect to your running Next.js instance.

For more configuration options, see the [next-devtools-mcp repository](https://github.com/vercel/next-devtools-mcp).


## Install dependencies

The `@next/mdx` package, and related packages, are used to configure Next.js so it can process markdown and MDX. **It sources data from local files**, allowing you to create pages with a `.md` or `.mdx` extension, directly in your `/pages` or `/app` directory.

Install these packages to render MDX with Next.js:

```bash package="pnpm"
pnpm add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```bash package="npm"
npm install @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```bash package="yarn"
yarn add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```bash package="bun"
bun add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```


### Slow initial page loading time

Create React App uses purely client-side rendering. Client-side only applications, also known as [single-page applications (SPAs)](/docs/app/guides/single-page-applications), often experience slow initial page loading time. This happens due to a couple of reasons:

1. The browser needs to wait for the React code and your entire application bundle to download and run before your code is able to send requests to load data.
2. Your application code grows with every new feature and dependency you add.


### Step 1: Install the Next.js Dependency

Install Next.js in your existing project:

```bash package="pnpm"
pnpm add next@latest
```

```bash package="npm"
npm install next@latest
```

```bash package="yarn"
yarn add next@latest
```

```bash package="bun"
bun add next@latest
```


### TypeScript Setup

Next.js automatically sets up TypeScript if you have a `tsconfig.json`. Make sure `next-env.d.ts` is listed in your `tsconfig.json` `include` array:

```json
{
  "include": ["next-env.d.ts", "app/**/*", "src/**/*"]
}
```


### Slow initial page loading time

If you have built your application with the [default Vite plugin for React](https://github.com/vitejs/vite-plugin-react/tree/main/packages/plugin-react), your application is a purely client-side application. Client-side only applications, also known as single-page applications (SPAs), often experience slow initial page loading time. This happens due to a couple of reasons:

1. The browser needs to wait for the React code and your entire application bundle to download and run before your code is able to send requests to load some data.
2. Your application code grows with every new feature and extra dependency you add.


### Step 1: Install the Next.js Dependency

The first thing you need to do is to install `next` as a dependency:

```bash package="pnpm"
pnpm add next@latest
```

```bash package="npm"
npm install next@latest
```

```bash package="yarn"
yarn add next@latest
```

```bash package="bun"
bun add next@latest
```


## Getting Started

OpenTelemetry is extensible but setting it up properly can be quite verbose.
That's why we prepared a package `@vercel/otel` that helps you get started quickly.


### Step 1: Installation

Install the plugin by running the following command:

```bash package="pnpm"
pnpm add @next/bundle-analyzer
```

```bash package="npm"
npm install @next/bundle-analyzer
```

```bash package="yarn"
yarn add @next/bundle-analyzer
```

```bash package="bun"
bun add @next/bundle-analyzer
```

Then, add the bundle analyzer's settings to your `next.config.js`.

```js filename="next.config.js"
/** @type {import('next').NextConfig} */
const nextConfig = {}

const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer(nextConfig)
```


### Dialog and initialization logic

Activity preserves dialog open/closed state. This also affects Effects that run based on that state.

**When to keep it:** A multi-step wizard or a settings panel that the user was actively working in. Preserving the step and input state avoids losing progress.

**When to reset it:** A dialog that runs initialization logic (like focusing an input) each time it opens. If the user navigated away while the dialog was open, Activity preserves `isDialogOpen: true`. Opening it again sets it to `true` when it's already `true`, so no state change happens and the Effect doesn't re-run.

Consider this example:

```tsx
'use client'

import { useState, useRef, useEffect } from 'react'

function ProductTab() {
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (isDialogOpen) {
      inputRef.current?.focus()
    }
  }, [isDialogOpen])

  // ...
}
```

If the user navigated away while the dialog was open, returning and opening the dialog won't trigger the focus Effect because `isDialogOpen` was already `true`.

To fix this, derive the dialog state from something outside the preserved component state like a search param:

```tsx highlight={3,7-9,20,25}
'use client'

import { useSearchParams, useRouter } from 'next/navigation'
import { useEffect, useRef } from 'react'

function ProductTab() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const isDialogOpen = searchParams.get('edit') === 'true'
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (isDialogOpen) {
      inputRef.current?.focus()
    }
  }, [isDialogOpen])

  return (
    <div>
      <button onClick={() => router.push('?edit=true')}>Edit Product</button>

      {isDialogOpen && (
        <dialog open>
          <input ref={inputRef} placeholder="Product name" />
          <button onClick={() => router.replace('?', { scroll: false })}>
            Close
          </button>
        </dialog>
      )}
    </div>
  )
}
```

With this approach, `isDialogOpen` derives from the URL rather than component state. When navigating away and returning, the search param is cleared (the URL changed), so `isDialogOpen` becomes `false`. Opening the dialog sets the param, which changes `isDialogOpen` and triggers the Effect.


## Installing Tailwind v3

Install Tailwind CSS and its peer dependencies, then run the `init` command to generate both `tailwind.config.js` and `postcss.config.js` files:

```bash package="pnpm"
pnpm add -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
```

```bash package="npm"
npm install -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
```

```bash package="yarn"
yarn add -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
```

```bash package="bun"
bun add -D tailwindcss@^3 postcss autoprefixer
bunx tailwindcss init -p
```


## Manual setup

To manually set up Cypress, install `cypress` as a dev dependency:

```bash package="pnpm"
pnpm add -D cypress
```

```bash package="npm"
npm install -D cypress
```

```bash package="yarn"
yarn add -D cypress
```

```bash package="bun"
bun add -D cypress
```

Add the Cypress `open` command to the `package.json` scripts field:

```json filename="package.json"
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "cypress:open": "cypress open"
  }
}
```

Run Cypress for the first time to open the Cypress testing suite:

```bash package="pnpm"
pnpm cypress:open
```

```bash package="npm"
npm run cypress:open
```

```bash package="yarn"
yarn cypress:open
```

```bash package="bun"
bun run cypress:open
```

You can choose to configure **E2E Testing** and/or **Component Testing**. Selecting any of these options will automatically create a `cypress.config.js` file and a `cypress` folder in your project.


## Manual setup

Since the release of [Next.js 12](https://nextjs.org/blog/next-12), Next.js now has built-in configuration for Jest.

To set up Jest, install `jest` and the following packages as dev dependencies:

```bash package="pnpm"
pnpm add -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
```

```bash package="npm"
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
```

```bash package="yarn"
yarn add -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
```

```bash package="bun"
bun add -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
```

Generate a basic Jest configuration file by running the following command:

```bash package="pnpm"
pnpm create jest@latest
```

```bash package="npm"
npm init jest@latest
```

```bash package="yarn"
yarn create jest@latest
```

```bash package="bun"
bun create jest@latest
```

This will take you through a series of prompts to setup Jest for your project, including automatically creating a `jest.config.ts|js` file.

Update your config file to use `next/jest`. This transformer has all the necessary configuration options for Jest to work with Next.js:

```ts filename="jest.config.ts" switcher
import type { Config } from 'jest'
import nextJest from 'next/jest.js'

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})

// Add any custom config to be passed to Jest
const config: Config = {
  coverageProvider: 'v8',
  testEnvironment: 'jsdom',
  // Add more setup options before each test is run
  // setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
export default createJestConfig(config)
```

```js filename="jest.config.js" switcher
const nextJest = require('next/jest')

/** @type {import('jest').Config} */
const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})

// Add any custom config to be passed to Jest
const config = {
  coverageProvider: 'v8',
  testEnvironment: 'jsdom',
  // Add more setup options before each test is run
  // setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(config)
```

Under the hood, `next/jest` is automatically configuring Jest for you, including:

* Setting up `transform` using the [Next.js Compiler](/docs/architecture/nextjs-compiler).
* Auto mocking stylesheets (`.css`, `.module.css`, and their scss variants), image imports and [`next/font`](/docs/app/api-reference/components/font).
* Loading `.env` (and all variants) into `process.env`.
* Ignoring `node_modules` from test resolving and transforms.
* Ignoring `.next` from test resolving.
* Loading `next.config.js` for flags that enable SWC transforms.

> **Good to know**: To test environment variables directly, load them manually in a separate setup script or in your `jest.config.ts` file. For more information, please see [Test Environment Variables](/docs/app/guides/environment-variables#test-environment-variables).


## Manual setup

To install Playwright, run the following command:

```bash package="pnpm"
pnpm create playwright
```

```bash package="npm"
npm init playwright
```

```bash package="yarn"
yarn create playwright
```

```bash package="bun"
bun create playwright
```

This will take you through a series of prompts to setup and configure Playwright for your project, including adding a `playwright.config.ts` file. Please refer to the [Playwright installation guide](https://playwright.dev/docs/intro#installation) for the step-by-step guide.


## Manual Setup

To manually set up Vitest, install `vitest` and the following packages as dev dependencies:

```bash package="pnpm"

## Getting Started

To get started, install the `@next/third-parties` library:

```bash package="pnpm"
pnpm add @next/third-parties@latest next@latest
```

```bash package="npm"
npm install @next/third-parties@latest next@latest
```

```bash package="yarn"
yarn add @next/third-parties@latest next@latest
```

```bash package="bun"
bun add @next/third-parties@latest next@latest
```

`@next/third-parties` is currently an **experimental** library under active development. We recommend installing it with the **latest** or **canary** flags while we work on adding more third-party integrations.


#### Setup

Add the following configuration to your MCP client, for each coding agent you can read [this section](https://github.com/vercel/next-devtools-mcp#mcp-client-configuration) for configuration details.

**example:**

```json filename=".mcp.json"
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

For more information, visit the [`next-devtools-mcp`](https://github.com/vercel/next-devtools-mcp) documentation to configure with your MCP client.

> **Note:** Using `next-devtools-mcp@latest` ensures that your MCP client will always use the latest version of the Next.js DevTools MCP server.


## Caching APIs


### Using a font definitions file

Every time you call the `localFont` or Google font function, that font will be hosted as one instance in your application. Therefore, if you need to use the same font in multiple places, you should load it in one place and import the related font object where you need it. This is done using a font definitions file.

For example, create a `fonts.ts` file in a `styles` folder at the root of your app directory.

Then, specify your font definitions as follows:

```ts filename="styles/fonts.ts" switcher
import { Inter, Lora, Source_Sans_3 } from 'next/font/google'
import localFont from 'next/font/local'

// define your variable fonts
const inter = Inter()
const lora = Lora()
// define 2 weights of a non-variable font
const sourceCodePro400 = Source_Sans_3({ weight: '400' })
const sourceCodePro700 = Source_Sans_3({ weight: '700' })
// define a custom local font where GreatVibes-Regular.ttf is stored in the styles folder
const greatVibes = localFont({ src: './GreatVibes-Regular.ttf' })

export { inter, lora, sourceCodePro400, sourceCodePro700, greatVibes }
```

```js filename="styles/fonts.js" switcher
import { Inter, Lora, Source_Sans_3 } from 'next/font/google'
import localFont from 'next/font/local'

// define your variable fonts
const inter = Inter()
const lora = Lora()
// define 2 weights of a non-variable font
const sourceCodePro400 = Source_Sans_3({ weight: '400' })
const sourceCodePro700 = Source_Sans_3({ weight: '700' })
// define a custom local font where GreatVibes-Regular.ttf is stored in the styles folder
const greatVibes = localFont({ src: './GreatVibes-Regular.ttf' })

export { inter, lora, sourceCodePro400, sourceCodePro700, greatVibes }
```

You can now use these definitions in your code as follows:

```tsx filename="app/page.tsx" switcher
import { inter, lora, sourceCodePro700, greatVibes } from '../styles/fonts'

export default function Page() {
  return (
    <div>
      <p className={inter.className}>Hello world using Inter font</p>
      <p style={lora.style}>Hello world using Lora font</p>
      <p className={sourceCodePro700.className}>
        Hello world using Source_Sans_3 font with weight 700
      </p>
      <p className={greatVibes.className}>My title in Great Vibes font</p>
    </div>
  )
}
```

```jsx filename="app/page.js" switcher
import { inter, lora, sourceCodePro700, greatVibes } from '../styles/fonts'

export default function Page() {
  return (
    <div>
      <p className={inter.className}>Hello world using Inter font</p>
      <p style={lora.style}>Hello world using Lora font</p>
      <p className={sourceCodePro700.className}>
        Hello world using Source_Sans_3 font with weight 700
      </p>
      <p className={greatVibes.className}>My title in Great Vibes font</p>
    </div>
  )
}
```

To make it easier to access the font definitions in your code, you can define a path alias in your `tsconfig.json` or `jsconfig.json` files as follows:

```json filename="tsconfig.json"
{
  "compilerOptions": {
    "paths": {
      "@/fonts": ["./styles/fonts"]
    }
  }
}
```

You can now import any font definition as follows:

```tsx filename="app/about/page.tsx" switcher
import { greatVibes, sourceCodePro400 } from '@/fonts'
```

```jsx filename="app/about/page.js" switcher
import { greatVibes, sourceCodePro400 } from '@/fonts'
```


## Functions


### Basic setup

To use `cacheLife`, first enable the [`cacheComponents` flag](/docs/app/api-reference/config/next-config-js/cacheComponents) in your `next.config.js` file:

```ts filename="next.config.ts" switcher
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

```js filename="next.config.js" switcher
const nextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

`cacheLife` requires the `use cache` directive, which must be placed at the file level or at the top of an async function or component.

> **Good to know**:
>
> * If used, `cacheLife` should be placed within the function whose output is being cached, even when the `use cache` directive is at file level
> * Only one `cacheLife` call should execute per function invocation. You can call `cacheLife` in different control flow branches, but ensure only one executes per run. See the [conditional cache lifetimes](#conditional-cache-lifetimes) example


### `width`, `initialScale`, `maximumScale` and `userScalable`

> **Good to know**: The `viewport` meta tag is automatically set, and manual configuration is usually unnecessary as the default is sufficient. However, the information is provided for completeness.

```tsx filename="layout.tsx | page.tsx" switcher
import type { Viewport } from 'next'

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  // Also supported but less commonly used
  // interactiveWidget: 'resizes-visual',
}
```

```jsx filename="layout.jsx | page.jsx" switcher
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  // Also supported but less commonly used
  // interactiveWidget: 'resizes-visual',
}
```

```html filename="<head> output" hideLineNumbers
<meta
  name="viewport"
  content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"
/>
```


## API Reference


# Install the adapter, build the app, and deploy or start it.
node -e "
const pkg=JSON.parse(require('fs').readFileSync('package.json','utf8'));
pkg.dependencies=pkg.dependencies||{};
pkg.dependencies['adapter']='file:${ADAPTER_DIR}';
require('fs').writeFileSync('package.json',JSON.stringify(pkg,null,2));
" >&2


## Options


## Setup ESLint

Get linting working quickly with the ESLint CLI (flat config):

1. Install ESLint and the Next.js config:

   ```bash package="pnpm"
   pnpm add -D eslint eslint-config-next
   ```

   ```bash package="npm"
   npm i -D eslint eslint-config-next
   ```

   ```bash package="yarn"
   yarn add --dev eslint eslint-config-next
   ```

   ```bash package="bun"
   bun add -d eslint eslint-config-next
   ```

2. Create `eslint.config.mjs` with the Next.js config:

   ```js filename="eslint.config.mjs"
   import { defineConfig, globalIgnores } from 'eslint/config'
   import nextVitals from 'eslint-config-next/core-web-vitals'

   const eslintConfig = defineConfig([
     ...nextVitals,
     // Override default ignores of eslint-config-next.
     globalIgnores([
       // Default ignores of eslint-config-next:
       '.next/**',
       'out/**',
       'build/**',
       'next-env.d.ts',
     ]),
   ])

   export default eslintConfig
   ```

3. Run ESLint:

   ```bash package="pnpm"
   pnpm exec eslint .
   ```

   ```bash package="npm"
   npx eslint .
   ```

   ```bash package="yarn"
   yarn eslint .
   ```

   ```bash package="bun"
   bunx eslint .
   ```


## Getting started

Turbopack is now the **default bundler** in Next.js. No configuration is needed to use Turbopack:

```json filename="package.json" highlight={3}
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```


# Getting Started



 - [Installation](/docs/pages/getting-started/installation)
 - [Project Structure](/docs/pages/getting-started/project-structure)
 - [Images](/docs/pages/getting-started/images)
 - [Fonts](/docs/pages/getting-started/fonts)
 - [CSS](/docs/pages/getting-started/css)
 - [Deploying](/docs/pages/getting-started/deploying)

---
title: Installation
description: "How to create a new Next.js application with `create-next-app`. Set up TypeScript, ESLint,and configure your `next.config.js` file."
url: "https://nextjs.org/docs/pages/getting-started/installation"
version: 16.2.1
router: Pages Router
---


# Installation


## Manual installation

To manually create a new Next.js app, install the required packages:

```bash package="pnpm"
pnpm i next@latest react@latest react-dom@latest
```

```bash package="npm"
npm i next@latest react@latest react-dom@latest
```

```bash package="yarn"
yarn add next@latest react@latest react-dom@latest
```

```bash package="bun"
bun add next@latest react@latest react-dom@latest
```

> **Good to know**:
>
> * The `App Router` uses [React canary releases](https://react.dev/blog/2023/05/03/react-canaries) built-in, which include all the stable React 19 changes, as well as newer features being validated in frameworks, but you should still declare react and react-dom in package.json for tooling and ecosystem compatibility.
> * The `Pages Router` uses the React version from your `package.json`.

Then, add the following scripts to your `package.json` file:

```json filename="package.json"
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

These scripts refer to the different stages of developing an application:

* `next dev`: Starts the development server using Turbopack (default bundler).
* `next build`: Builds the application for production.
* `next start`: Starts the production server.
* `eslint`: Runs ESLint.

Turbopack is now the default bundler. To use Webpack run `next dev --webpack` or `next build --webpack`. See the [Turbopack docs](/docs/app/api-reference/turbopack) for configuration details.


## Getting started

To get started, add the `i18n` config to your `next.config.js` file.

Locales are [UTS Locale Identifiers](https://www.unicode.org/reports/tr35/tr35-59/tr35.html#Identifiers), a standardized format for defining locales.

Generally a Locale Identifier is made up of a language, region, and script separated by a dash: `language-region-script`. The region and script are optional. An example:

* `en-US` - English as spoken in the United States
* `nl-NL` - Dutch as spoken in the Netherlands
* `nl` - Dutch, no specific region

If user locale is `nl-BE` and it is not listed in your configuration, they will be redirected to `nl` if available, or to the default locale otherwise.
If you don't plan to support all regions of a country, it is therefore a good practice to include country locales that will act as fallbacks.

```js filename="next.config.js"
module.exports = {
  i18n: {
    // These are all the locales you want to support in
    // your application
    locales: ['en-US', 'fr', 'nl-NL'],
    // This is the default locale you want to be used when visiting
    // a non-locale prefixed path e.g. `/hello`
    defaultLocale: 'en-US',
    // This is a list of locale domains and the default locale they
    // should handle (these are only required when setting up domain routing)
    // Note: subdomains must be included in the domain value to be matched e.g. "fr.example.com".
    domains: [
      {
        domain: 'example.com',
        defaultLocale: 'en-US',
      },
      {
        domain: 'example.nl',
        defaultLocale: 'nl-NL',
      },
      {
        domain: 'example.fr',
        defaultLocale: 'fr',
        // an optional http field can also be used to test
        // locale domains locally with http instead of https
        http: true,
      },
    ],
  },
}
```


## Install dependencies

The `@next/mdx` package, and related packages, are used to configure Next.js so it can process markdown and MDX. **It sources data from local files**, allowing you to create pages with a `.md` or `.mdx` extension, directly in your `/pages` or `/app` directory.

Install these packages to render MDX with Next.js:

```bash package="pnpm"
pnpm add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```bash package="npm"
npm install @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```bash package="yarn"
yarn add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

```bash package="bun"
bun add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```


### Slow initial page loading time

Create React App uses purely client-side rendering. Client-side only applications, also known as [single-page applications (SPAs)](/docs/app/guides/single-page-applications), often experience slow initial page loading time. This happens due to a couple of reasons:

1. The browser needs to wait for the React code and your entire application bundle to download and run before your code is able to send requests to load data.
2. Your application code grows with every new feature and dependency you add.


### Step 1: Install the Next.js Dependency

Install Next.js in your existing project:

```bash package="pnpm"
pnpm add next@latest
```

```bash package="npm"
npm install next@latest
```

```bash package="yarn"
yarn add next@latest
```

```bash package="bun"
bun add next@latest
```


### TypeScript Setup

Next.js automatically sets up TypeScript if you have a `tsconfig.json`. Make sure `next-env.d.ts` is listed in your `tsconfig.json` `include` array:

```json
{
  "include": ["next-env.d.ts", "app/**/*", "src/**/*"]
}
```


### Step 1: Install the Next.js Dependency

The first thing you need to do is to install `next` as a dependency:

```bash package="pnpm"
pnpm add next@latest
```

```bash package="npm"
npm install next@latest
```

```bash package="yarn"
yarn add next@latest
```

```bash package="bun"
bun add next@latest
```


## Functions


## API Reference
