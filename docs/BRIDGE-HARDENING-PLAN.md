# Bridge Hardening Plan

> Scope: `domyh-hsa-mcp` (MCP server) + `mcp-bridge-plugins` (5 bridges)
> Every item cites verified `file:line`. Items were checked against the source,
> not against documentation — several doc claims were wrong and are called out.
> Unreal and Blender are deferred to the last phase per owner instruction.

**Status legend:** `VERIFIED` = read from source this session. `UNVERIFIED` = from
research, needs a read before acting.

---

## Phase 0 — Repo consolidation (blocks everything)

The bridge plugins moved to `domyh-awf/mcp-bridge-plugins/`, but both path
resolvers still find the stale copy at `auto_domyh/mcp-bridge-plugins/`. The
move is not yet effective at runtime.

### 0.1 Both resolvers pick the old copy — VERIFIED

`domyh-hsa-mcp/src/tools/t17_bridge.ts:531-550` `candidatePaths()` walks up from
`projectPath` to the filesystem root. Running the real function against the real
filesystem:

```
domyh-awf        -> OK  domyh-awf/mcp-bridge-plugins/ida-bridge     (correct)
domyh-hsa-mcp    -> OK  auto_domyh/mcp-bridge-plugins/ida-bridge    (STALE)
umbrella root    -> OK  auto_domyh/mcp-bridge-plugins/ida-bridge    (STALE)
unrelated proj   -> OK  auto_domyh/mcp-bridge-plugins/ida-bridge    (STALE)
no projectPath   -> OK  auto_domyh/mcp-bridge-plugins/ida-bridge    (STALE)
```

`domyh-hsa-mcp/scripts/sync-local.js:158-168` `findBridgeSource()` has the same
ancestor walk. Running it verbatim:

```
findBridgeSource(domyh-hsa-mcp)
  -> E:\Deverloper\NewDeverloper\auto_domyh\mcp-bridge-plugins
  expected: ...\domyh-awesome-code-agent\domyh-awf\mcp-bridge-plugins
  *** MISMATCH ***
```

Why it silently passes: `auto_domyh/mcp-bridge-plugins/` still exists, so
`existsSync` succeeds and the loop stops there. It never reaches `domyh-awf/`.

### 0.2 The two copies have already diverged — VERIFIED

Source-only diff (`--exclude=.venv --exclude=__pycache__ --exclude=node_modules
--exclude=dist`) shows 3 files differ, all in `ida-bridge`:

| File | New copy (`domyh-awf`) has | Old copy lacks |
|---|---|---|
| `hsa_ida_plugin.py` | `HsaBridgeHTTPServer` with `SO_EXCLUSIVEADDRUSE`, `allow_reuse_address = False` (`:1361-1371`) | plain `HTTPServer` |
| `server.py` | `_has_requested_identity` / `_instance_matches` gating (`:186-196`, `:200-210`) | no instance matching |
| `README.md` | "Agent call contract" section (`:45-52`) | — |

The new copy is the better one. Any bridge call today runs the old code.

### 0.3 Also in the new tree — VERIFIED

- `ue-bridge/src/ue-ws-client.ts` — 76 lines, imported by nothing. Dead code;
  consistent with the finding that no bridge uses WebSocket.
- `__pycache__/` and `.venv/` directories are inside the plugin tree and must
  stay untracked.

**Fix:** delete `auto_domyh/mcp-bridge-plugins/`, then add a
`mcp-bridge-plugins/.gitignore` covering `.venv/`, `__pycache__/`,
`node_modules/`, `dist/`. After deletion both resolvers fall through to
`domyh-awf/` and no code change is needed.

Alternative if the old copy must be kept: make `candidatePaths` and
`findBridgeSource` prefer `domyh-awf` explicitly rather than nearest-ancestor.
That is a worse fix — it hardcodes a layout into the MCP server.

**Do not delete the old copy without owner confirmation.** It is 13,143 files
including a populated `.venv` that would have to be rebuilt.

---

## Phase 1 — Correctness bugs (no design decisions needed)

### 1.1 Errors from Python bridges are reported to the agent as success — VERIFIED

MCP reads `isError` from the tool result (`t17_bridge.ts:785`). Three Python
bridges return a plain string on failure, so `isError` is always `false`:

- `ghidra-bridge/server.py:96` — `return "❌ Ghidra Error: %s"`
- `ida-bridge/server.py:290-296` — `format_result` returns a JSON error blob
- `x64dbg-bridge/server.py` — 9 sites, e.g. `:122,164,191,208,284,341,396,415,447`,
  all `return f"❌ Error: {e}"`

The correct pattern already exists in this repo, in the other language:
`unity-bridge/src/index.ts:40` and `ue-bridge/src/index.ts:31` both
`return { isError: true, content: [...] }`.

Impact: every failed IDA/Ghidra/x64dbg call is delivered to the model as a
success with prose embedded. The agent cannot tell failure from success.

**Fix:** one shared `toMcpResult()` helper used by all three Python bridges.
Raise the exception instead of formatting a string; FastMCP converts a raised
exception to `isError: true` natively. Smallest change with the largest effect
in the whole plan — it is currently corrupting every agent session that touches
these bridges.

### 1.2 Ghidra plugin cannot be loaded by Ghidra — VERIFIED

`ghidra-bridge/hsa_ghidra_plugin.py:357` — `class HsaGhidraBridgePlugin(object)`.
No base class, no `initialize()`, no `run()`, no `dispose()`. Ghidra does not
auto-load `.py` outside Jython, so `:390-391` (`if __name__ == "__main__"`) is
unreachable under Ghidra's loader.

The same repo already solves this for IDA at `ida-bridge/hsa_ida_plugin.py:1374-1428`
(`class HsaMcpBridgePlugin(idaapi.plugin_t)`, `init()`, `run()`, `term()`,
port-fallback loop, daemon thread).

**Fix:** mirror the IDA structure — `extends GhidraPlugin implements
ApplicationLevelPlugin`, add `initialize()`/`dispose()`, ship `Module.manifest`
and `extension.properties` under a proper `Extensions/` directory. The Ghidra
bridge does not function without this.

### 1.3 `ghidra_apply_data_type` is a stub that reports success — VERIFIED

`ghidra-bridge/hsa_ghidra_plugin.py:290-291`:
```python
def cmd_apply_data_type(params):
    return _json_ok({"ok": False, "error": "Address data type application is not yet implemented"})
```
It is wrapped in `_json_ok` (`:37`), so `format_result` (`server.py:94-97`) sees
`ok: true` and returns the error JSON as a **successful result**. It is declared
`mutates: true` at `t17_bridge.ts:238` and advertised as a working tool.

**Fix:** implement it or remove it from both `COMMANDS` (`:298-313`) and
`GHIDRA_TOOLS`. A stub that reports success is worse than an absent tool.

### 1.4 x64dbg README documents tools that do not exist — VERIFIED

`x64dbg-bridge/README.md:49-68` documents `x64_get_registers`, `x64_read_memory`,
`x64_get_disasm`, `x64_step_over`, `x64_step_into`, `x64_run`, `x64_pause`,
`x64_set_breakpoint`, `x64_get_callstack`. Eight of the nine do not exist. The
real ten are at `x64dbg-bridge/server.py:114-465`. Only `x64_get_modules` is real.

**Fix:** rewrite the README from `server.py`. Anyone reading it today is being
told the bridge can step the debugger.

### 1.5 x64dbg hardcodes one developer's absolute path — VERIFIED

`x64dbg-bridge/server.py:32-35` hardcodes
`E:/Deverloper/snapshot_2025-08-19_19-40/release/x64/x64dbg.exe`, and the same
literal is duplicated at `t17_bridge.ts:527`.

The upstream library already solves it — `_resolve_x64dbg_path_with_env` at
`x64dbg_automate/mcp_server.py:313` and `_resolve_debugger_path` at `:335` do
bitness-aware `x96dbg.exe` → `x64dbg.exe`/`x32dbg.exe` resolution.

**Fix:** use the upstream resolver; fail with a clear message instead of
silently defaulting to one machine's snapshot path.

---

## Phase 2 — Concurrency and startup latency

### 2.1 Ghidra HTTP server is single-threaded — VERIFIED

`ghidra-bridge/hsa_ghidra_plugin.py:368` — `server.setExecutor(None)`. One slow
decompile blocks every other request. The decompile handler has a 120s timeout
(`:126-128`).

Fixed upstream at `GhidraMCPPlugin.java:1014-1046` (3-thread pool, named daemon
threads).

**Fix:** install a small fixed thread pool. One line plus the executor object.

### 2.2 Ghidra port scan takes 64 seconds — VERIFIED

`ghidra-bridge/server.py:102` uses a 2s timeout; `:113-119` loops serially over
32 ports. Worst case ≈ 64s, serial.

The IDA bridge directly beside it is already correct — `ida-bridge/server.py:461-467`
uses `ThreadPoolExecutor` with `max_workers=min(len(ports), 32)` (`:33`) and a
350ms timeout (`:32`).

Measured upstream (`bridge_mcp_ghidra/discovery.py:143-152`): a dropped (not
refused) port costs the full timeout, and a serial scan of a 16-port range
measured 15.2s of a 16.8s startup — close enough to an MCP client start timeout
to fail the connection, which presents as "the Ghidra tools are missing".

**Fix:** copy the concurrent-scan + ordered-yield pattern; drop the timeout to
350ms to match IDA. 64s → under 1s. One function.

### 2.3 UE Python server is single-threaded — VERIFIED, NEW

`ue-bridge/resources/init_unreal.py:62` — `HTTPServer(...)`, not
`ThreadingHTTPServer`. The handler blocks on `event.wait(timeout=30.0)` at `:39`
while the game thread runs the job. During that window every other request
blocks, including another agent's `ue_python_status`.

Same class of defect as 2.1, in a different language.

**Fix:** `ThreadingHTTPServer`. Note the interaction with 3.1 — a thread per
request means `request_queue` concurrency must be checked, not just assumed.

---

## Phase 3 — Security

Deferred only in the sense that 1.1 and Phase 0 land first. This is the
highest-severity group.

### 3.1 No authentication on any of the five bridges — VERIFIED

| Bridge | Listener | Auth |
|---|---|---|
| ghidra | `hsa_ghidra_plugin.py:366` `HttpServer.create` | none |
| ida | `hsa_ida_plugin.py:1400` | none |
| ue | `init_unreal.py:62` `HTTPServer(('127.0.0.1', 30011))` | none |
| x64dbg | ZMQ via x64dbg-automate | upstream's, loopback |
| unity | stdio only | n/a |

Four independent upstream implementations converged on the same contract:
mandatory bearer token on non-loopback bind, and **refuse to start** when bound
off-loopback without a token. Ours implements it zero times.

**Fix:** shared `HSA_BRIDGE_TOKEN`, constant-time compare in every handler,
refuse a non-loopback bind without a token. Fail closed.

### 3.2 UE Python executor runs arbitrary code with no auth — VERIFIED, and reassessed

`init_unreal.py:92` — `exec(code, exec_globals)` with full `__builtins__`
(`:88-91`). Body arrives base64-decoded from `:25`. Any local process can reach
it.

**Reassessment of the research agent's recommendation.** The agent proposed
replacing `exec` with a dispatch table. Running that idea against the actual
code surfaces two things the agent did not account for:

1. **The liveness probe is itself `exec`.** `ue-bridge/src/index.ts:205` sends
   `print("pong")` through the same `/execute` endpoint to decide whether the
   server is up. Replacing `exec` with an action enum breaks this probe — it
   needs a separate `/health` endpoint that does not execute anything. This is a
   design constraint, not an implementation detail.

2. **`ue_python_status` is `ensurePythonExecutor()`** (`index.ts:292-298`), which
   *deploys the file* as a side effect (`:236-248`). So "check status" is not
   read-only. Any redesign must separate the probe from the deploy.

Recommended shape, in order:
- **First:** shared token (3.1). Stops the unauthenticated case outright.
- **Then:** a closed action enum for the common Unreal operations, with no path
  that accepts source code.
- **Keep** `execute_python` as an explicit opt-in: token required, 1MB cap,
  every call logged. ChiR24 took this same route — they had to drop `exec` too
  to make the bridge tolerable.

**Trade-off:** the action enum removes arbitrary Python, which agents currently
use to reach `unreal.*` APIs with no wrapper. Token-only keeps that capability
and keeps the risk. The hybrid keeps capability but makes it auditable. This is
a scope call for the owner, not a technical one — hence the split.

### 3.3 x64dbg passes a raw model-supplied command to the debugger — VERIFIED

`x64dbg-bridge/server.py:462` — `client.cmd_sync(command)`. No allowlist, no
validation. x64dbg commands can write memory and patch binaries.

Contrast the upstream library, which validates: `raise ValueError(f"Cannot
resolve address: {s}")` at `mcp_server.py:78`, format validation at `:231`,
protect-filter validation at `:158,181`.

**Fix:** per-target input validators driven by the existing
`BridgeToolManifest.inputs` (declared `t17_bridge.ts:80-88`, **never read
anywhere** — grepped). Enforce at `callBridgeTool` (`t17_bridge.ts:918`) and use
`mutates` to require explicit opt-in, generalising what `ida_batch` already does
at `:838-847`.

---

## Phase 4 — Capability

### 4.1 One batch tool in five bridges — VERIFIED

`ida_batch` (`t17_bridge.ts:222`) is the only batch surface, and it needed a
10-line validator to stop the agent misusing it (`:838-847`).

Upstream equivalents: bethington ships `batch_get_comments`,
`batch_set_comments`, `batch_rename_function_components`; x64dbg-automate ships
`read_memory_many(reads: list[str], format)` at `mcp_server.py:752`.

**Fix:** add plural endpoints. This is where "agent can retry and gather in one
pass" improves most, and it needs no architectural change.

### 4.2 Tool manifests are hardcoded and hand-synchronised — VERIFIED

`IDA_TOOLS` (`t17_bridge.ts:191-223`, 31), `UNITY_TOOLS` (`:255-278`, 22),
`UE_TOOLS` (`:280-294`, 13), plus Ghidra and x64dbg — roughly 91 entries, all
hardcoded, no dynamic registration. Adding a Python handler without editing the
TypeScript means the tool is invisible.

Upstream: bethington serves `/mcp/schema` and the bridge calls
`_notify_tools_changed(ctx)`; Epic 5.8 ships `bEnableToolSearch` so `tools/list`
returns 3 meta-tools instead of the full schema; ChiR24 negotiates capabilities
over a `bridge_hello` handshake.

**Fix:** have each plugin serve a schema endpoint and have the TS side fetch it
on connect, falling back to the hardcoded manifest when the plugin does not
implement it. Deferring this is why 4.3 cannot be done properly.

### 4.3 `ue` has no discovery — VERIFIED

`t17_bridge.ts:371` — `ue: undefined` in `BRIDGE_DISCOVERY`. `discover` returns
`supported: false` and a note (`:1041-1050`). The agent cannot tell whether the
editor is alive.

`unity` is also `undefined` (`:370`).

**Fix (UE):** probe `GET http://127.0.0.1:30010/remote/info` with a 2s timeout,
return `{reachable, editorVersion, projectName, projectDir}`. Roughly 10 lines
against a 600-line upstream handshake — we need one instance, not many.

**Fix (UE, related):** `ue_python_status` must distinguish
`remote_control_down` / `python_module_not_loaded` / `python_ready` instead of
the current boolean, and must not deploy as a side effect of a status check
(see 3.2).

### 4.4 `x64dbg_automate.mcp_server` ships 50 tools and is already a dependency — UNVERIFIED

The research reports `x64dbg_automate/mcp_server.py` is 1603 lines with 50
`@mcp.tool()` functions, MIT, maintained by the same author as the plugin, and
already in our dependency tree — we have been reimplementing ~10 weak tools on
top of it. It has our defect too (errors returned as strings), and it solves the
bitness-aware path problem from 1.5.

**Read `mcp_server.py` before acting on this.** If confirmed, adopt it as the
x64dbg base and keep only the tools that add something it lacks —
`x64_find_string` / `x64_find_pattern` do scoped multi-region scanning with
module filtering and it is said to have no equivalent.

---

## Phase 5 — Indexing (C++ priority)

### 5.1 C++ symbol extraction computes the wrong line and column — VERIFIED

`domyh-hsa-mcp/src/parsers/extractor.ts:901-903`:
```typescript
const line = sourceCode.substring(0, match.index).split('\n').length;
const col = match.index - lineStart;
```
All six C++ patterns (`:784-842`) begin with `(?:^|\n)`, so `match.index` points
at the `\n` **preceding** the match. `line` is one too low and `col` is −1.

Ran the real regexes against a real C++ file:
```
function   reported_line=7  col=-1  reads=""    <- reads the wrong line
class      reported_line=3  col=-1  reads=""
method     reported_line=7  col=-1  reads=""
```
Every C++ symbol is stored with the wrong `line` and `col`; `endLine: line`
(`:927`) is wrong too. An agent jumping to a symbol lands on the line above.

**Fix:** advance past the newline before measuring.

### 5.2 The indent filter that guards 5.1 is dead — VERIFIED

`extractor.ts:906-908` reads `lines[line - 1]` to measure indentation and skips
matches with `indent > 0`. Because `line` is already off by one, it reads the
blank line before the match, gets `indent = 0`, and the filter never fires.

Currently harmless (it drops nothing), but it means the guard protecting against
in-class definitions is inert. **Fix 5.1 alone re-arms it**, and it will then
delete every in-class method definition, because in-class methods are all
indented. These two must be fixed together.

### 5.3 Out-of-line method definitions are recorded under the wrong symbol — VERIFIED

For `void Foo::Update() {`, the `function` pattern (`:787`) matches first and
records `Update`. The `method` pattern (`:823`) also matches but is applied
later. The comment at `:912-913` states the intent — store
`MySQLLeaderboardRepository::ExecuteUpdate` so `trace_flow` can find it — and
the current regexes do not achieve that for out-of-line definitions.

**Fix:** try the qualified-method patterns before the free-function pattern.

### 5.4 No C/C++ grammar; the Swift grammar dependency is dead — VERIFIED

`ts-queries.ts:25-170` `PACKS` covers 7 languages: python, go, rust, java,
csharp, ruby, php. `tree-sitter-adapter.ts:29-38` `SUPPORTED_EXTENSIONS` maps
exactly those 7. C, C++, and Swift have no pack.

`tests/unit/tree-sitter-wasm.test.ts:75-76` locks this in deliberately:
`// Declared before but never had a grammar package installed.` So the gap is
intentional, not accidental.

`package.json:60` declares `"tree-sitter-swift": "^0.7.1"`. Grep across the repo
excluding `node_modules` finds it only in `package.json`, `package-lock.json`,
and one warning line. Nothing imports it, nothing resolves it. The same warning
line records `install: node-gyp rebuild` — npm is still building a native addon
for something unused. `tests/unit/tree-sitter-wasm.test.ts:80` gives the reason:
`// No prebuilt wasm published for this grammar.` The adapter needs a prebuilt
`.wasm` (`:109`), so it cannot work.

C++ is the priority language and is the only one whose primary path has wrong
coordinates. C# — the same family — already has a pack.

**Fix:** add `tree-sitter-cpp` (and `tree-sitter-c`) as packs 8 and 9, modelled
on the C# entry at `ts-queries.ts:106-126`, plus the extension mappings. Queries
should capture what regex can never reach: `template_declaration`,
`field_declaration`, `namespace_definition`, preproc nodes.

**Must be ordered after 5.1-5.3.** `tree-sitter-adapter.ts:133-137` falls back to
regex on wasm-load failure, and that fallback is currently broken. Fix the
fallback first, then add the grammar.

**Remove `tree-sitter-swift`** from `package.json` — 0 readers, no wasm, and it
costs a native build on every install. Owner decision: it is a dependency change.

**Do not invest in Swift.** With no wasm, adding a pack achieves nothing; the
regex path at `extractor.ts:1063-1066` and `skeleton.ts:92-95` stays.

**Trade-off:** tree-sitter costs ~2-5MB resident and first-parse latency versus
the regex path. It buys correctness and, more importantly, call edges and
import edges for C++ — the regex path produces **definitions only, no call
graph at all**. That gap is the larger loss today.

---

## Phase 6 — Test coverage

### 6.1 No test spawns a bridge subprocess — VERIFIED

`tests/unit/tool-capability-matrix.test.ts:491-508` is scoped
`describe('hsa_bridge (no spawn)')` with the comment "Bridge is covered only on
paths that do not spawn a plugin subprocess." `bridge-env.test.ts` (2 tests)
checks env defaults. `bridge-identity.test.ts` (5 tests) checks payload shaping.
None exercises `startBridgeClient`, the port probe, tool dispatch, or error
handling.

**Consequence:** the 64-second scan (2.2) and the unloadable Ghidra plugin
(1.2) both pass CI today. A regression suite that spawns each bridge and asserts
on `isError` (1.1) is what makes phases 1-3 hold.

---

## Deferred by owner instruction

- **Unreal** — full evaluation, `init_unreal.py` redesign beyond 3.2, and the
  Epic 5.8 `ModelContextProtocol` migration path.
- **Blender** — `ahujasid/mcp-for-blender` was researched but not traced against
  this codebase.

## Suggested order

Phase 0 → 1.1 → 1.2 → 2.2 → 1.3 → 1.4 → 1.5 → 2.1 → 2.3 → Phase 6 →
3.1 → 3.3 → 5.1-5.3 → 4.1 → 4.3 → 5.4 → 3.2 → 4.2 → 4.4

Rationale: 1.1 first because it is small and it is silently corrupting sessions
right now. 5.1-5.3 before 5.4 because the regex fallback must be correct before
it becomes the safety net. Phase 6 after the cheap fixes so the suite has real
assertions to guard. 3.2 last of the security group because it needs the token
from 3.1 in place first.
