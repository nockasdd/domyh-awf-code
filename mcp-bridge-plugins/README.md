# MCP Bridge Plugins

Welcome to the DOMYH Awesome Code Agent's **MCP (Model Context Protocol) Bridge Plugins** directory. 

These plugins act as translators and dedicated communication channels between the DOMYH AI Agent (HSA Engine) and specialized target applications, allowing the AI to remotely control, inspect, and modify external environments in real-time.

## 🌉 The Bridge Architecture

Each bridge operates using the following standard architecture:

```mermaid
flowchart LR
    A[HSA Engine\n(DOMYH Agent)] <-->|MCP Protocol\n(stdio)| B(Bridge Server\nPython/TypeScript)
    B <-->|HTTP / ZMQ / RPC| C[Target Application\nPlugin/Script]
    C <-->|Native API| D[(Application State)]
```

When the DOMYH Agent calls `hsa_bridge(target="...")`, the HSA Engine automatically spawns the corresponding **Bridge Server** as a subprocess. The Bridge Server then communicates over the local network (HTTP, WebSocket, or ZMQ) with the **Target Application Plugin** running inside the host application.

## 📦 Available Plugins

Choose a specific plugin directory below for detailed installation and usage instructions:

### 🎮 Game Engines (TypeScript)
Used for Text-to-Game development, asset manipulation, level design, and automation:
- 🟢 **[Unity Editor Bridge](./unity-bridge/README.md)** — C#/TypeScript bridge for Unity 2022+ (Scene manipulation, asset imports).
- 🔵 **[Unreal Engine Bridge](./ue-bridge/README.md)** — Python/TypeScript bridge for Unreal Engine 5.x+ (Remote Control API, EditorActorSubsystem).

### 🛠️ Reverse Engineering (Python)
Used for dynamic analysis, memory inspection, and binary translation:
- 🔴 **[IDA Pro Bridge](./ida-bridge/README.md)** — Python bridge for Hex-Rays IDA Pro 8.x/9.x (Decompilation, Xrefs, Renaming).
- 🟣 **[x64dbg Bridge](./x64dbg-bridge/README.md)** — Python/ZMQ bridge for x64dbg (Registers, memory hex dumps, breakpoints, stepping).

## 🚀 General Prerequisites

While each bridge has specific requirements, generally you will need:
- **Node.js 18+** & `pnpm` (for Game Engine TypeScript bridges)
- **Python 3.10+** & `uv` (for Reverse Engineering Python bridges)
