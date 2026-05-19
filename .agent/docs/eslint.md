---
library: eslint
version: 9.x
latest: true
category: api-tool
official_docs: https://eslint.org/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# ESLint v9

> ESLint — Pluggable JavaScript/TypeScript linter.
> Current: v9 (flat config) | Previous: v8 (`.eslintrc`)
> Docs: https://eslint.org/docs

## Version Comparison

| Feature | v8 | v9 |
|:--------|:---|:---|
| Config | `.eslintrc.*` files | `eslint.config.js` (flat) |
| Config format | JSON/YAML/JS | JavaScript/TypeScript only |
| `env` field | ✅ `env: { browser: true }` | ❌ Use `globals` package |
| `extends` | ✅ Strings | ❌ Use array spread |
| Plugins | `plugins: ["react"]` | `import pluginReact from '...'` |
| `--ext` flag | ✅ | ❌ Use config `files` array |

## Installation

```bash
npm install -D eslint @eslint/js typescript-eslint
npm init @eslint/config@latest   # interactive setup
```

## Flat Config (v9)

```ts
// eslint.config.js (or .mjs, .ts)
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactPlugin from 'eslint-plugin-react';
import globals from 'globals';

export default [
  // Global ignores
  { ignores: ['dist/', 'node_modules/', '*.config.js'] },

  // Base JS rules
  js.configs.recommended,

  // TypeScript rules
  ...tseslint.configs.recommended,

  // React rules
  {
    files: ['**/*.{tsx,jsx}'],
    plugins: { react: reactPlugin },
    rules: {
      'react/jsx-uses-react': 'off',
      'react/react-in-jsx-scope': 'off',
    },
  },

  // Global settings
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
      parserOptions: { project: './tsconfig.json' },
    },
    rules: {
      'no-console': 'warn',
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
];
```

## CLI

```bash
npx eslint .                         # lint all
npx eslint src/ --fix                # auto-fix
npx eslint --inspect-config          # visualize config
npx eslint --print-config src/app.ts # show resolved config for file
```

## Common Rules

```ts
rules: {
  // Errors
  'no-console': 'warn',
  'no-debugger': 'error',
  'no-duplicate-imports': 'error',
  'prefer-const': 'error',

  // TypeScript
  '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  '@typescript-eslint/no-explicit-any': 'warn',
  '@typescript-eslint/consistent-type-imports': 'error',
  '@typescript-eslint/no-floating-promises': 'error',
}
```

## Core Concepts

| Concept | Description |
|:--------|:-----------|
| **Rules** | Core building block — validates code expectations |
| **Rule Fixes** | Auto-fixable via `--fix` flag |
| **Rule Suggestions** | IDE suggestions (not auto-applied) |
| **Plugins** | npm modules with custom rules (e.g. `typescript-eslint`, `eslint-plugin-react`) |
| **Parsers** | Convert code to AST — built-in: Espree, custom: `@typescript-eslint/parser` |
| **Shareable Configs** | Shared via npm (e.g. `eslint-config-airbnb-base`) |
| **Processors** | Extract JS from other files (e.g. `@eslint/markdown` for .md code blocks) |
| **Formatters** | Control CLI output format |

## TypeScript Config Support

```ts
// eslint.config.ts (TypeScript config — v9.x)
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,  // auto-detect tsconfig
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
);
```

## Custom Rule

```ts
// eslint-local-rules/no-magic-numbers.js
export default {
  meta: {
    type: 'suggestion',
    docs: { description: 'Disallow magic numbers' },
    fixable: 'code',
    schema: [{ type: 'object', properties: { ignore: { type: 'array' } } }],
  },
  create(context) {
    const ignore = context.options[0]?.ignore ?? [0, 1];
    return {
      Literal(node) {
        if (typeof node.value === 'number' && !ignore.includes(node.value)) {
          context.report({ node, message: `No magic number: ${node.value}` });
        }
      },
    };
  },
};
```

## Inline Config

```ts
/* eslint-disable @typescript-eslint/no-explicit-any */
const data: any = {};
/* eslint-enable @typescript-eslint/no-explicit-any */

// eslint-disable-next-line no-console
console.log('debug');

const x = 1; // eslint-disable-line no-unused-vars
```

## Ignoring Files

```ts
// eslint.config.js — global ignores (first item, no other keys)
export default [
  { ignores: ['dist/', 'node_modules/', 'coverage/', '*.min.js'] },
  // ... other config objects
];

// Per-pattern ignores
{
  files: ['**/*.test.ts'],
  rules: { 'no-console': 'off' },
}
```

## Gotchas

⚠️ **v9**: No `.eslintrc.*` — only `eslint.config.js` (flat config).

⚠️ **v9**: No `extends: "eslint:recommended"` — use `import js from '@eslint/js'; js.configs.recommended`.

⚠️ **v9**: No `env: { browser: true }` — use `globals` package: `globals.browser`.

⚠️ **v9**: `plugins` is an object `{ react: pluginReact }`, not string array.

⚠️ **Migration**: Use `npx @eslint/migrate-config .eslintrc.json` to convert.

⚠️ **TypeScript config**: `eslint.config.ts` supported — use `typescript-eslint` helper.

⚠️ **`--inspect-config`**: Visualize resolved config in browser for debugging.
