---
library: plugin-x64dbg
version: 1
latest: true
category: mcp-plugin
target_app: x64dbg (x64/x32)
transport: HTTP JSON-RPC http://127.0.0.1:15556
plugin_type: C++ DLL (.dp64 / .dp32)
last_updated: 2026-03-27
---

# plugin-x64dbg — HSA MCP Bridge for x64dbg

> Full x64dbg plugin SDK reference: plugin lifecycle, all PLUG_CB_* callbacks, scriptapi headers, bridge API, HTTP/JSON-RPC server implementation, and MCP dispatch table.

---

## 1. Architecture & Threading Model

x64dbg exposes two categories of APIs to plugins:

1. **Script::*** namespace APIs (scriptapi headers) — safe only from the **debug event thread** or **GUI message loop**.
2. **Dbg*** bridge functions (bridgemain.h) — **thread-safe**, callable from any plugin thread.

For the MCP HTTP server running on a daemon thread, ALWAYS use `Dbg*` bridge functions.

```
LLM Agent
  │  MCP tool call
  ▼
MCP Bridge (TypeScript) ──POST http://127.0.0.1:15556/x64dbg/...──► C++ HTTP Server (cpp-httplib)
                                                                        │  (plugin daemon thread)
                                                                        │
                                                                        ▼  Use Dbg* APIs (thread-safe)
                                                                     DbgMemRead / DbgGetRegDump
                                                                     DbgCmdExecDirect("StepOver")
                                                                     DbgEval("[EBP+8]", &result)
```

### 1.1. Thread Safety Rules

| API family | Thread-safe | Use from |
|:-----------|:------------|:---------|
| `Script::Debug::*`, `Script::Memory::*` | ❌ Only debug-loop thread | CB callbacks, not HTTP thread |
| `DbgMemRead / DbgMemWrite` | ✅ Yes | HTTP handler, any thread |
| `DbgCmdExecDirect(cmd)` | ✅ Yes | HTTP handler, any thread |
| `DbgEval(expr, &out)` | ✅ Yes | HTTP handler, any thread |
| `DbgGetRegDump(&regs)` | ✅ Yes | HTTP handler, any thread |
| `_plugin_logprint(msg)` | ✅ Yes | Any thread |

---

## 2. Plugin Lifecycle (Required Exports)

Every x64dbg plugin DLL **must** export exactly these 3 functions:

```cpp
// hsa_x64dbg_plugin.cpp
// Build: x64 → hsa_bridge.dp64, x86 → hsa_bridge.dp32
// Install: copy to x64dbg/release/x64/plugins/  (or x32/plugins/)

#include "pluginsdk/bridgemain.h"
#include "pluginsdk/_plugins.h"
#include "pluginsdk/_scriptapi_debug.h"
#include "pluginsdk/_scriptapi_memory.h"
#include "pluginsdk/_scriptapi_register.h"
#include "pluginsdk/_scriptapi_pattern.h"
#include "pluginsdk/_scriptapi_comment.h"
#include "pluginsdk/_scriptapi_gui.h"
#include "pluginsdk/_scriptapi_module.h"
#include "pluginsdk/_scriptapi_stack.h"
#include "pluginsdk/_scriptapi_symbol.h"
#include "httplib.h"    // https://github.com/yhirose/cpp-httplib (single header)
#include "json.hpp"     // https://github.com/nlohmann/json (single header)
#include <thread>

using json = nlohmann::json;

int pluginHandle = 0;
httplib::Server g_srv;

// ── pluginInit: called when plugin DLL is loaded ──────────────────
// Must set pluginVersion + sdkVersion.
// Return false to refuse loading.
bool pluginInit(PLUG_INITSTRUCT* initStruct) {
    initStruct->pluginVersion = 1;
    initStruct->sdkVersion    = PLUG_SDKVERSION;
    pluginHandle              = initStruct->pluginHandle;

    _plugin_logprint("[HSA] x64dbg plugin initializing...\n");

    // Register custom commands (accessible via x64dbg Script pane)
    _plugin_registercommand(pluginHandle, "hsa_status", [](int, char**) -> bool {
        _plugin_logprint("[HSA] Bridge is running\n");
        return true;
    }, false);

    // Start HTTP server on daemon thread
    std::thread([]() {
        RegisterRoutes(g_srv);
        _plugin_logprint("[HSA] HTTP server on http://127.0.0.1:15556\n");
        g_srv.listen("127.0.0.1", 15556);
    }).detach();

    return true;
}

// ── plugstop: called when plugin is unloaded ──────────────────────
void plugstop() {
    _plugin_unregistercommand(pluginHandle, "hsa_status");
    g_srv.stop();
    _plugin_logprint("[HSA] x64dbg plugin stopped\n");
}

// ── plugsetup: called after init to configure menu items ─────────
void plugsetup(PLUG_SETUPSTRUCT* setupStruct) {
    // setupStruct->hMenuDisasm  — context menu in disassembly view
    // setupStruct->hMenuDump    — context menu in dump view
    // setupStruct->hMenuStack   — context menu in stack view
    // _plugin_menuaddentry(setupStruct->hMenuDisasm, MENU_DISASM_ENTRY, "&HSA Analyze");
}
```

---

## 3. PLUG_CB_* Callback Reference (Full)

Register callbacks with `_plugin_registercallback(handle, CB_TYPE, fn)`.

```cpp
// Breakpoint hit
PLUG_EXPORT void CBBREAKPOINT(CBTYPE, void* info) {
    auto* bp = (PLUG_CB_BREAKPOINT*)info;
    // bp->breakpoint: BRIDGEBP*
    // bp->breakpoint->addr     — address where BP hit
    // bp->breakpoint->type     — bp_normal / bp_hardware / bp_memory
    // bp->breakpoint->active   — bool
    // bp->breakpoint->enabled  — bool
    // bp->breakpoint->singleshoot — bool
    _plugin_logprintf("[HSA] BP hit: 0x%llX\n", bp->breakpoint->addr);
}

// Debugger paused (step, exception, etc.)
PLUG_EXPORT void CBPAUSEDEBUG(CBTYPE, void* info) {
    // info: PLUG_CB_PAUSEDEBUG* (reserved void*)
    // Debugger is now paused — safe to read regs/memory
    REGDUMP regs;
    DbgGetRegDump(&regs);
    _plugin_logprintf("[HSA] Paused at RIP=0x%llX\n", regs.regcontext.cip);
}

// Debugger resumed (run/step was issued)
PLUG_EXPORT void CBRESUMEDEBUG(CBTYPE, void* info) {
    _plugin_logprint("[HSA] Debugger resumed\n");
}

// Exception in debuggee
PLUG_EXPORT void CBEXCEPTION(CBTYPE, void* info) {
    auto* ex = (PLUG_CB_EXCEPTION*)info;
    // ex->Exception: EXCEPTION_DEBUG_INFO*
    // ex->Exception->ExceptionRecord.ExceptionCode
    // ex->Exception->ExceptionRecord.ExceptionAddress
    _plugin_logprintf("[HSA] Exception code=0x%X\n",
        ex->Exception->ExceptionRecord.ExceptionCode);
}

// Thread created
PLUG_EXPORT void CBCREATETHREAD(CBTYPE, void* info) {
    auto* t = (PLUG_CB_CREATETHREAD*)info;
    // t->CreateThread: CREATE_THREAD_DEBUG_INFO*
    // t->dwThreadId: DWORD
}

// Thread exited
PLUG_EXPORT void CBEXITTHREAD(CBTYPE, void* info) {
    auto* t = (PLUG_CB_EXITTHREAD*)info;
    // t->ExitThread: EXIT_THREAD_DEBUG_INFO*
    // t->dwThreadId: DWORD
}

// System breakpoint (first-chance BP on process attach)
PLUG_EXPORT void CBSYSTEMBREAKPOINT(CBTYPE, void* info) {
    _plugin_logprint("[HSA] System breakpoint hit\n");
}

// Selection changed in a view
PLUG_EXPORT void CBSELCHANGED(CBTYPE, void* info) {
    auto* sel = (PLUG_CB_SELCHANGED*)info;
    // sel->hWindow — window that changed
    // sel->VA      — currently selected virtual address
}

// Address info query (for annotating addresses)
PLUG_EXPORT void CBADDRINFO(CBTYPE, void* info) {
    auto* ai = (PLUG_CB_ADDRINFO*)info;
    // ai->addr     — address being queried
    // ai->addrinfo — BRIDGE_ADDRINFO* to fill in
    // ai->retval   — set to true if you handled it
}
```

---

## 4. scriptapi Header Map (Full)

### 4.1. _scriptapi_debug.h — Script::Debug

```cpp
namespace Script { namespace Debug {
    void Wait();                          // Wait until debugger pauses
    void Run();                           // Resume execution (F9)
    void Pause();                         // Pause (F12)
    void Stop();                          // Stop debugging (Shift+F2)
    void StepIn();                        // Step Into (F7)
    void StepOver();                      // Step Over (F8)
    void StepOut();                       // Step Out (Ctrl+F9)
    bool RunToUserCode();                 // Run until user code
    bool SetBreakpoint(duint address);    // Set software BP
    bool DeleteBreakpoint(duint address); // Delete BP
    bool DisableBreakpoint(duint address);
    bool EnableBreakpoint(duint address);
}}
```

### 4.2. _scriptapi_memory.h — Script::Memory

```cpp
namespace Script { namespace Memory {
    duint Read(duint addr, void* buf, duint size, duint* bytesRead = nullptr);
    bool  Write(duint addr, const void* buf, duint size);
    bool  IsValidPtr(duint addr);
    duint RemoteAlloc(duint addr, duint size);    // VirtualAllocEx in debuggee
    bool  RemoteFree(duint addr);                 // VirtualFreeEx
    duint GetBase(duint addr);                    // get allocation base
    duint GetSize(duint addr);                    // get allocation size
    DWORD GetProtect(duint addr);                 // VirtualProtect value
}}
```

### 4.3. _scriptapi_register.h — Script::Register

```cpp
namespace Script { namespace Register {
    duint Get(Script::Register::RegisterEnum reg);
    bool  Set(Script::Register::RegisterEnum reg, duint value);
    // Enum values: RAX, RCX, RDX, RBX, RSP, RBP, RSI, RDI,
    //              R8, R9, R10, R11, R12, R13, R14, R15,
    //              RIP, EFLAGS, DR0, DR1, DR2, DR3, DR6, DR7
    //              GAX/GCX/GDX/GBX/GSP/GBP/GSI/GDI/GIP (generic 32/64)

    // FP/XMM:
    duint GetFLAGS();
    bool  SetFLAGS(duint value);
    duint GetDR0(); duint GetDR1(); duint GetDR2(); duint GetDR3();
    bool  SetDR0(duint v); // hardware BP registers
}}
```

### 4.4. _scriptapi_pattern.h — Script::Pattern

```cpp
namespace Script { namespace Pattern {
    // Pattern format: "AA BB ? CC ??" where ? = wildcard byte
    duint FindMem(duint base, duint size, const char* pattern);
    bool  SearchAndReplace(duint base, duint size,
                           const char* pattern, const char* replace);
}}
```

### 4.5. _scriptapi_comment.h — Script::Comment

```cpp
namespace Script { namespace Comment {
    bool Set(duint addr, const char* text);
    bool Get(duint addr, char* text);           // text buffer >= MAX_COMMENT_SIZE
    bool Delete(duint addr);
    bool GetIterator(COMMENTMAP::iterator& it); // iterate all comments
}}
```

### 4.6. _scriptapi_gui.h — Script::Gui

```cpp
namespace Script { namespace Gui {
    void SelectionGet(int hWindow, SELECTIONDATA* selection);
    void SelectionSet(int hWindow, const SELECTIONDATA* selection);
    void DisassembleAt(duint addr);
    void Message(const char* message);          // show status message
    // hWindow: GUI_DISASM_SEL, GUI_DUMP_SEL, GUI_STACK_SEL
}}
```

### 4.7. _scriptapi_module.h — Script::Module

```cpp
namespace Script { namespace Module {
    bool  GetMain(MODULEINFO* info);            // main module info
    bool  GetModuleAt(duint addr, char* name);  // module name at addr
    duint GetBase(const char* name);            // base address of module
    duint GetSize(const char* name);            // size of module
    bool  GetExport(const char* mod, const char* api, duint* addr);
    bool  Enum(MODULEINFO* list, int count);    // enumerate loaded modules
}}
```

### 4.8. _scriptapi_symbol.h — Script::Symbol

```cpp
namespace Script { namespace Symbol {
    // Enumerate symbols in a module
    bool GetMain(SYMBOLINFO* info);
    bool Enum(const char* mod, SYMBOLCBINFO* cbInfo);
    // SYMBOLCBINFO: callback, user data
}}
```

---

## 5. bridgemain.h — Thread-Safe Bridge APIs (Full)

```cpp
// These Dbg* functions are safe to call from any thread (including HTTP handler thread)

// Memory
bool   DbgMemRead(duint addr, void* buf, duint size);
bool   DbgMemWrite(duint addr, const void* buf, duint size);
bool   DbgMemIsValidReadPtr(duint addr);
duint  DbgMemGetPageSize(duint addr);

// Registers (via REGDUMP struct)
// REGDUMP has: regcontext.cax/cbx/ccx/cdx/csp/cbp/csi/cdi/cip/eflags
// + r8..r15 on x64, + FPU/XMM/YMM context
bool   DbgGetRegDump(REGDUMP* regs);

// Command execution
bool   DbgCmdExec(const char* command);      // async — does not wait
bool   DbgCmdExecDirect(const char* command); // sync — waits for completion

// Expression evaluation
bool   DbgEval(const char* expression, duint* result);
// expression examples: "[EBP+8]", "rip+5", "kernel32:GetProcAddress"

// Breakpoints
bool   DbgIsDebugging();
bool   DbgIsRunning();

// Module info
bool   DbgGetModuleAt(duint addr, char* moduleName);
duint  DbgFunctions()->ModBaseFromAddr(addr);

// Labels / comments (direct DB access, thread-safe)
bool   DbgSetLabelAt(duint addr, const char* label);
bool   DbgGetLabelAt(duint addr, SEGMENTREG segment, char* label);
bool   DbgSetCommentAt(duint addr, const char* comment);
bool   DbgGetCommentAt(duint addr, char* comment);
```

---

## 6. Full HTTP/JSON-RPC Server (cpp-httplib + nlohmann/json)

```cpp
// Helper to send JSON response
static void JsonReply(httplib::Response& res, const json& body) {
    res.set_content(body.dump(), "application/json");
}

void RegisterRoutes(httplib::Server& srv) {

    // ── Status ──────────────────────────────────────────────────────
    srv.Get("/x64dbg/status", [](const httplib::Request&, httplib::Response& res) {
        JsonReply(res, {
            {"ok", true},
            {"debugging", DbgIsDebugging()},
            {"running",   DbgIsRunning()},
        });
    });

    // ── Memory ──────────────────────────────────────────────────────

    // POST /x64dbg/read_memory  {"addr":"0x401000","size":64}
    srv.Post("/x64dbg/read_memory", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint addr = std::stoull(body["addr"].get<std::string>(), nullptr, 16);
        size_t sz  = body["size"].get<size_t>();
        std::vector<uint8_t> buf(sz, 0);
        bool ok = DbgMemRead(addr, buf.data(), sz);
        std::string hex;
        for (auto b : buf) { char tmp[3]; snprintf(tmp,3,"%02x",b); hex+=tmp; }
        JsonReply(res, {{"ok",ok},{"hex",hex},{"addr",body["addr"]}});
    });

    // POST /x64dbg/write_memory {"addr":"0x401000","hex":"9090"}
    srv.Post("/x64dbg/write_memory", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint addr = std::stoull(body["addr"].get<std::string>(), nullptr, 16);
        std::string hex_str = body["hex"].get<std::string>();
        std::vector<uint8_t> buf;
        for (size_t i = 0; i < hex_str.size(); i += 2)
            buf.push_back((uint8_t)std::stoul(hex_str.substr(i,2),nullptr,16));
        bool ok = DbgMemWrite(addr, buf.data(), buf.size());
        JsonReply(res, {{"ok",ok},{"written",(int)buf.size()}});
    });

    // POST /x64dbg/is_valid_ptr {"addr":"0x401000"}
    srv.Post("/x64dbg/is_valid_ptr", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint addr = std::stoull(body["addr"].get<std::string>(), nullptr, 16);
        JsonReply(res, {{"valid", DbgMemIsValidReadPtr(addr)}});
    });

    // ── Registers ────────────────────────────────────────────────────

    // GET /x64dbg/registers
    srv.Get("/x64dbg/registers", [](const httplib::Request&, httplib::Response& res) {
        REGDUMP regs; DbgGetRegDump(&regs);
        auto& r = regs.regcontext;
        JsonReply(res, {
            {"rax",r.cax}, {"rbx",r.cbx}, {"rcx",r.ccx}, {"rdx",r.cdx},
            {"rsp",r.csp}, {"rbp",r.cbp}, {"rsi",r.csi}, {"rdi",r.cdi},
            {"rip",r.cip}, {"rflags",r.eflags},
            // x64 extra regs
            {"r8",r.r8},  {"r9",r.r9},  {"r10",r.r10}, {"r11",r.r11},
            {"r12",r.r12},{"r13",r.r13},{"r14",r.r14}, {"r15",r.r15}
        });
    });

    // POST /x64dbg/set_register {"reg":"rax","value":"0xdeadbeef"}
    srv.Post("/x64dbg/set_register", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        std::string cmd = body["reg"].get<std::string>() + "=" + body["value"].get<std::string>();
        bool ok = DbgCmdExecDirect(cmd.c_str());
        JsonReply(res, {{"ok",ok}});
    });

    // ── Debug Control ────────────────────────────────────────────────

    // POST /x64dbg/run
    srv.Post("/x64dbg/run",        [](auto&,auto& res){ DbgCmdExecDirect("run");       JsonReply(res,{{"ok",true}}); });
    // POST /x64dbg/pause
    srv.Post("/x64dbg/pause",      [](auto&,auto& res){ DbgCmdExecDirect("pause");     JsonReply(res,{{"ok",true}}); });
    // POST /x64dbg/step_into
    srv.Post("/x64dbg/step_into",  [](auto&,auto& res){ DbgCmdExecDirect("StepInto");  JsonReply(res,{{"ok",true}}); });
    // POST /x64dbg/step_over
    srv.Post("/x64dbg/step_over",  [](auto&,auto& res){ DbgCmdExecDirect("StepOver");  JsonReply(res,{{"ok",true}}); });
    // POST /x64dbg/step_out
    srv.Post("/x64dbg/step_out",   [](auto&,auto& res){ DbgCmdExecDirect("StepOut");   JsonReply(res,{{"ok",true}}); });

    // ── Breakpoints ──────────────────────────────────────────────────

    // POST /x64dbg/set_bp {"addr":"0x401000","type":"soft"}
    // type: "soft"(bp), "hw_exec"(bph), "hw_read"(bprm), "hw_write"(bpwm), "mem"(bpm)
    srv.Post("/x64dbg/set_bp", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        std::string addr = body["addr"].get<std::string>();
        std::string type = body.value("type","soft");
        std::string cmd;
        if      (type == "soft")     cmd = "bp "    + addr;
        else if (type == "hw_exec")  cmd = "bph "   + addr;
        else if (type == "hw_read")  cmd = "bprm "  + addr;
        else if (type == "hw_write") cmd = "bpwm "  + addr;
        else if (type == "mem")      cmd = "bpm "   + addr;
        bool ok = DbgCmdExecDirect(cmd.c_str());
        JsonReply(res, {{"ok",ok},{"cmd",cmd}});
    });

    // POST /x64dbg/del_bp {"addr":"0x401000"}
    srv.Post("/x64dbg/del_bp", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        std::string cmd = "bc " + body["addr"].get<std::string>();
        JsonReply(res, {{"ok", DbgCmdExecDirect(cmd.c_str())}});
    });

    // ── Expression / Eval ────────────────────────────────────────────

    // POST /x64dbg/eval {"expr":"[ESP+4]"}
    srv.Post("/x64dbg/eval", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint result = 0;
        bool ok = DbgEval(body["expr"].get<std::string>().c_str(), &result);
        char buf[32]; snprintf(buf, 32, "0x%llX", (unsigned long long)result);
        JsonReply(res, {{"ok",ok},{"value",result},{"hex",buf}});
    });

    // ── Annotations ──────────────────────────────────────────────────

    // POST /x64dbg/set_comment {"addr":"0x401000","text":"interesting func"}
    srv.Post("/x64dbg/set_comment", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint addr = std::stoull(body["addr"].get<std::string>(), nullptr, 16);
        bool ok = DbgSetCommentAt(addr, body["text"].get<std::string>().c_str());
        JsonReply(res, {{"ok",ok}});
    });

    // POST /x64dbg/set_label {"addr":"0x401000","label":"my_func"}
    srv.Post("/x64dbg/set_label", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint addr = std::stoull(body["addr"].get<std::string>(), nullptr, 16);
        bool ok = DbgSetLabelAt(addr, body["label"].get<std::string>().c_str());
        JsonReply(res, {{"ok",ok}});
    });

    // ── Modules ──────────────────────────────────────────────────────

    // GET /x64dbg/modules
    srv.Get("/x64dbg/modules", [](const httplib::Request&, httplib::Response& res) {
        // List modules via DbgCmdExec("modlist") and capture from log,
        // or use DbgFunctions()->GetModuleList() if available in SDK version
        json mods = json::array();
        // Simplified: use DbgCmdExecDirect to dump module list to log
        DbgCmdExecDirect("modlist");
        JsonReply(res, {{"ok",true},{"note","check x64dbg log for module list"}});
    });

    // ── Pattern Scan ─────────────────────────────────────────────────

    // POST /x64dbg/pattern_find {"base":"0x400000","size":0x100000,"pattern":"48 8B ? ? ? 90"}
    srv.Post("/x64dbg/pattern_find", [](const httplib::Request& req, httplib::Response& res) {
        auto body = json::parse(req.body);
        duint base = std::stoull(body["base"].get<std::string>(), nullptr, 16);
        duint size = body["size"].get<duint>();
        std::string pat = body["pattern"].get<std::string>();
        // Read memory and scan
        std::vector<uint8_t> buf(size, 0);
        DbgMemRead(base, buf.data(), size);
        // Use Script::Pattern::FindMem (safe here since we already have the bytes)
        duint found = Script::Pattern::FindMem(base, size, pat.c_str());
        char hex[32]; snprintf(hex, 32, "0x%llX", (unsigned long long)found);
        JsonReply(res, {{"found", found != 0},{"addr", hex}});
    });
}
```

---

## 7. MCP Command Dispatch Table

| HTTP endpoint | Method | Body | Returns | Uses |
|:-------------|:-------|:-----|:--------|:-----|
| `/x64dbg/status` | GET | — | `{debugging,running}` | `DbgIsDebugging` |
| `/x64dbg/read_memory` | POST | `addr,size` | `{hex}` | `DbgMemRead` |
| `/x64dbg/write_memory` | POST | `addr,hex` | `{ok,written}` | `DbgMemWrite` |
| `/x64dbg/is_valid_ptr` | POST | `addr` | `{valid}` | `DbgMemIsValidReadPtr` |
| `/x64dbg/registers` | GET | — | all regs | `DbgGetRegDump` |
| `/x64dbg/set_register` | POST | `reg,value` | `{ok}` | `DbgCmdExecDirect` |
| `/x64dbg/run` | POST | — | `{ok}` | `DbgCmdExecDirect("run")` |
| `/x64dbg/pause` | POST | — | `{ok}` | `DbgCmdExecDirect("pause")` |
| `/x64dbg/step_into` | POST | — | `{ok}` | `DbgCmdExecDirect("StepInto")` |
| `/x64dbg/step_over` | POST | — | `{ok}` | `DbgCmdExecDirect("StepOver")` |
| `/x64dbg/step_out` | POST | — | `{ok}` | `DbgCmdExecDirect("StepOut")` |
| `/x64dbg/set_bp` | POST | `addr,type?` | `{ok}` | `DbgCmdExecDirect("bp/bph/bpm")` |
| `/x64dbg/del_bp` | POST | `addr` | `{ok}` | `DbgCmdExecDirect("bc")` |
| `/x64dbg/eval` | POST | `expr` | `{value,hex}` | `DbgEval` |
| `/x64dbg/set_comment` | POST | `addr,text` | `{ok}` | `DbgSetCommentAt` |
| `/x64dbg/set_label` | POST | `addr,label` | `{ok}` | `DbgSetLabelAt` |
| `/x64dbg/modules` | GET | — | modules | `DbgCmdExecDirect` |
| `/x64dbg/pattern_find` | POST | `base,size,pattern` | `{found,addr}` | `Script::Pattern::FindMem` |

---

## 8. Build & Install

```bash
# Build with MSVC (x64)
cl.exe /LD /EHsc /std:c++17 ^
  /I "x64dbg\pluginsdk" ^
  hsa_x64dbg_plugin.cpp httplib.h json.hpp ^
  /Fe:hsa_bridge.dp64 ^
  /link x64dbg\pluginsdk\x64\pluginsdk.lib

# Install
copy hsa_bridge.dp64 "C:\x64dbg\release\x64\plugins\"
copy hsa_bridge.dp32 "C:\x64dbg\release\x32\plugins\"

# Test (with x64dbg open and a process being debugged)
curl -s http://127.0.0.1:15556/x64dbg/status
curl -s -X POST http://127.0.0.1:15556/x64dbg/read_memory \
     -H "Content-Type: application/json" \
     -d "{\"addr\":\"0x401000\",\"size\":16}"
```

<!-- BM25: library=plugin-x64dbg target=x64dbg C++ plugin MCP bridge DbgMemRead scriptapi -->
