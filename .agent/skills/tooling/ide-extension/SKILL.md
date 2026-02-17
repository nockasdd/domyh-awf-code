---
name: ide-extension
version: "6.3.1"
category: tooling
---

# IDE Extension Development — VS Code • JetBrains • Neovim

> Multi-IDE extension development  
> LSP • DAP • Webviews • Plugin SDKs

---

## Khi Nào Dùng

- Phát triển VS Code extension
- Build JetBrains plugin (IntelliJ, WebStorm, etc.)
- Viết Neovim plugin (Lua)
- Implement Language Server (LSP) cho ngôn ngữ mới

## VS Code Extension Architecture

```
┌────────────────────────────────────────┐
│ VS Code (Electron)                     │
│  ┌──────────────┐  ┌────────────────┐ │
│  │ Main Process │  │ Extension Host │ │ ← Isolated process
│  │ (UI, Window) │  │  ┌──────────┐  │ │
│  │              │  │  │ Your Ext │  │ │
│  │              │  │  └──────────┘  │ │
│  └──────────────┘  └────────────────┘ │
│                    ┌────────────────┐  │
│                    │   Webview      │  │ ← Sandboxed iframe
│                    │ (React/Vue)   │  │
│                    └────────────────┘  │
└────────────────────────────────────────┘
```

### package.json Contribution Points

```json
{
  "contributes": {
    "commands": [{ "command": "ext.doSomething", "title": "Do Something" }],
    "keybindings": [{ "command": "ext.doSomething", "key": "ctrl+shift+p" }],
    "views": { "explorer": [{ "id": "myView", "name": "My View" }] },
    "configuration": { "properties": { "ext.setting": { "type": "boolean" } } }
  },
  "activationEvents": ["onLanguage:typescript", "onCommand:ext.doSomething"]
}
```

### Extension Lifecycle

```typescript
export function activate(context: vscode.ExtensionContext) {
  // Register commands, providers, etc.
  const disposable = vscode.commands.registerCommand("ext.doSomething", () => { ... });
  context.subscriptions.push(disposable);
}
export function deactivate() { /* cleanup */ }
```

## Language Server Protocol (LSP)

### When to Use

- Code completion, go-to-definition, hover info
- Diagnostics (errors/warnings)
- Code actions (quick fixes, refactoring)
- Supporting same language across multiple IDEs

### Server Setup

```typescript
const connection = createConnection(ProtocoLConnection);
const documents = new TextDocuments(TextDocument);
connection.onInitialize((_params) => ({
  capabilities: {
    completionProvider: { triggerCharacters: ["."] },
    hoverProvider: true,
    definitionProvider: true,
  },
}));
documents.listen(connection);
connection.listen();
```

## JetBrains Plugin (Quick Reference)

- **plugin.xml**: Extension points, actions, services
- **PSI**: Program Structure Interface for code analysis
- **Services**: Application/project/module-level singletons
- **Remote Dev**: Ensure backend compatibility

## Neovim Plugin (Quick Reference)

- **Lua**: `lua/pluginname/init.lua` entry point
- **Setup**: `require("pluginname").setup({ ... })` pattern
- **LSP**: `vim.lsp.start({ name, cmd, root_dir })` native LSP
- **lazy.nvim**: Modern plugin manager

## Common Traps

| Trap                | Fix                                     |
| ------------------- | --------------------------------------- |
| Extension slows IDE | Lazy activation, async operations       |
| Webview state lost  | `getState`/`setState` persistence       |
| LSP not connecting  | Check stdio/IPC transport, log stderr   |
| Memory leaks        | Dispose subscriptions in `deactivate()` |

---

_DOMYH Awesome Code • IDE Extension Skill v1.0.0_
