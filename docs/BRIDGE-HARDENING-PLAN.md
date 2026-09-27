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

### 1.2 Ghidra plugin cannot be loaded by Ghidra — VERIFIED, fix now known to be larger than a Python edit

`ghidra-bridge/hsa_ghidra_plugin.py:385` is a Python class. Ghidra's plugin
manager will never discover it, and no amount of Python-side restructuring
changes that.

`PluginUtils.forName()` resolves plugins through
`ClassSearcher.getClasses(Plugin.class)`, and `ClassSearcher.findClasses()`
(`ClassSearcher.java:399`) matches **by file name only, without opening the
file** — it is a bytecode scan of the classpath. Discovery therefore requires a
real `.class` file annotated `@PluginInfo`
(`RetentionPolicy.RUNTIME`, `PluginInfo.java:41`). A PyGhidra or Jython proxy
has no bytecode on disk, so it is invisible to the scanner.

Correction to the Jython removal: Ghidra **11.2** renamed the `Python` module
to `Jython` (GP-4659, 2024-06-03) and **11.3** added `PyGhidra` alongside it.
Jython was de-bundled into `Ghidra/Extensions/Jython` only in **12.1**
(GP-6754, 2026-04-24), and even then as an opt-in extension, not a deletion.
Both `JythonScriptProvider` and `PyGhidraScriptProvider` are `ScriptProvider`
implementations — script runners, not plugin providers. Neither auto-starts
anything at boot.

Every production HTTP-bridge project for Ghidra is therefore a **Java** plugin:

| Project | Approach |
|---|---|
| `bethington/ghidra-mcp` (4k★) | Java `GhidraMCPPlugin` in an extension ZIP, server starts with the plugin on `127.0.0.1:8089`; the Python half is a separate out-of-process MCP→HTTP translator. The reference implementation for this exact shape. |
| `mandiant/Ghidrathon` (790★) | Java extension glue + Jep, Python 3 script provider |
| `evyatar9/GptHidra` (406★) | Java extension |
| `clearbluejar/pyghidra-mcp` (428★) | No plugin at all — external CLI, out-of-process |
| `nightwing-us/pyghidra-decaf` (6★) | Generates Java stub classes at setup so Python can reach real discovery. Young, low adoption. |

**Fix:** port `hsa_ghidra_plugin.py` to a Java `GhidraPlugin` packaged as a Ghidra
extension (`Module.manifest` + `extension.properties` under `Ghidra/Extensions/`),
keeping the Python file as the reference for the command set to port. This is
the one item in Phase 1 that cannot land as a small diff — it needs a build for
the extension and an install step the other bridges do not have.

### 1.3 `ghidra_apply_data_type` is a stub that reports success — VERIFIED, FIXED

Original: `ghidra-bridge/hsa_ghidra_plugin.py:290-291` returned
`_json_ok({"ok": False, "error": "...not yet implemented"})`, so `format_result`
(`server.py:94-97`) saw `ok: true` and handed the model a **successful result
containing a failure**, for a tool declared `mutates: true` at
`t17_bridge.ts:238`.

Fixed at `hsa_ghidra_plugin.py:293`: resolve the type from the program data type
manager, clear the covered listing range, and `createData` at the address,
returning the created length. It is still subject to 1.2 — the file does not
load under Ghidra until the Java port lands — but the command is no longer a
lie once it does.

**Fix:** implement it or remove it from both `COMMANDS` (`:298-313`) and
`GHIDRA_TOOLS`. A stub that reports success is worse than an absent tool.

### 1.4 x64dbg README documents tools that do not exist — VERIFIED, FIXED

`x64dbg-bridge/README.md:49-68` documented `x64_get_registers`,
`x64_read_memory`, `x64_get_disasm`, `x64_step_over`, `x64_step_into`,
`x64_run`, `x64_pause`, `x64_set_breakpoint`, `x64_get_callstack`. Eight of the
nine do not exist. Only `x64_get_modules` was real.

The README now carries the ten `@mcp.tool()` functions `server.py` actually
defines, cross-checked 10/10 against `t17_bridge.ts:243-252`, plus a "What this
bridge does not do" section stating that register/memory/step/callstack work
belongs to the upstream `x64dbg-automate` MCP server.

### 1.5 x64dbg hardcodes one developer's absolute path — VERIFIED, FIXED

`x64dbg-bridge/server.py:32-35` hardcoded
`E:/Deverloper/snapshot_2025-08-19_19-40/release/x64/x64dbg.exe`, and the same
literal was duplicated at `t17_bridge.ts:527`, so the server kept supplying the
value on every launch.

The upstream library already solves resolution —
`_resolve_x64dbg_path_with_env` at `x64dbg_automate/mcp_server.py:105` and
`_resolve_debugger_path` at `:127` do bitness-aware `x96dbg.exe` →
`x64dbg.exe`/`x32dbg.exe` lookup across four candidate layouts. Those are
private to the upstream module, so `server.py:38` reads `X64DBG_PATH` and
raises `BridgeError` when it is unset, and the literal is gone from
`buildBridgeEnvironment`.

---

## Phase 2 — Concurrency and startup latency

### 2.1 Ghidra HTTP server is single-threaded — VERIFIED

`ghidra-bridge/hsa_ghidra_plugin.py:368` — `server.setExecutor(None)`. One slow
decompile blocks every other request. The decompile handler has a 120s timeout
(`:126-128`).

**FIXED** at `hsa_ghidra_plugin.py:415`:
`server.setExecutor(Executors.newFixedThreadPool(4))`. The port loop and the
daemon flag moved with it — `threading.Thread.daemon = True` rather than
`setDaemon(True)`, which Python 3.10 removed while Jython 2.7 still accepts it.

Upstream reference remains `GhidraMCPPlugin.java:1014-1046` (3-thread pool, named
daemon threads).

### 2.2 Ghidra port scan takes 64 seconds — VERIFIED, FIXED

`ghidra-bridge/server.py:102` used a 2s timeout; `:113-119` looped serially over
32 ports. Worst case ≈ 64s, serial.

The IDA bridge directly beside it was already correct — `ida-bridge/server.py:461-467`
uses `ThreadPoolExecutor` with `max_workers=min(len(ports), 32)` (`:33`) and a
350ms timeout (`:32`).

**FIXED.** `server.py:105` now probes with the same `ThreadPoolExecutor` shape,
`GHIDRA_HTTP_PROBE_TIMEOUT` at IDA's 350ms and `GHIDRA_HTTP_SCAN_WORKERS` at 32,
both env-overridable. Results are re-ordered to the scan order so the output does
not depend on which probe finished first.

Measured over the real 28572-28603 range with nothing listening:

| | elapsed |
|---|---|
| serial, 2s timeout (before) | 11.484s |
| 8 workers | 1.615s |
| 16 workers | 0.715s |
| 32 workers (shipped) | 0.375s |

10.3x over serial at the previous 2s timeout; the worker cap is left where IDA
has it because the sweep is still improving at 32.

### 2.3 UE Python server is single-threaded — VERIFIED, FIXED

`ue-bridge/resources/init_unreal.py:62` used `HTTPServer(...)`, not
`ThreadingHTTPServer`. The handler blocks on `event.wait(timeout=30.0)` at `:39`
while the game thread runs the job, so during that window every other request
blocks — including another agent's `ue_python_status`. Three 30s calls queued
behind each other rather than running together.

Same class of defect as 2.1, in a different language.

**FIXED** at `init_unreal.py:9` and `:62`. Measured on this machine, three
concurrent 0.5s POSTs: 1.59s on `HTTPServer`, 0.50s on `ThreadingHTTPServer`.
The queue is what orders the work, so switching the serving side does not change
ordering.

**Also fixed in the same commit** — `ue-bridge/src/ue-ws-client.ts:64` raced a
30s timer against the response. The timer was never cleared when the response
won, and a late timeout could delete a request id that a reconnect had already
reused, so the follow-up call waited for a reply nothing would send. The timer is
now cleared on both resolve and reject.

Interaction with 3.1 remains: a thread per request means `request_queue`
concurrency must be checked, not just assumed.

---

## Phase 3 — Security

Deferred only in the sense that 1.1 and Phase 0 land first. This is the
highest-severity group.

### 3.1 No authentication on any of the five bridges — VERIFIED, FIXED

| Bridge | Listener | Auth before | Auth after |
|---|---|---|---|
| ghidra | `hsa_ghidra_plugin.py` `HttpServer.create` | none | `HSA_BRIDGE_TOKEN` |
| ida | `hsa_ida_plugin.py` `ThreadingHTTPServer` | none | `HSA_BRIDGE_TOKEN` |
| ue | `init_unreal.py` `ThreadingHTTPServer` | none | `HSA_BRIDGE_TOKEN` |
| unity | `HsaUnityServer.cs` `HttpListener` on 30030 | none | `HSA_BRIDGE_TOKEN` |
| x64dbg | stdio FastMCP over `X64DbgClient` | n/a | n/a — see below |

Four independent upstream implementations converged on the same contract:
mandatory bearer token on non-loopback bind, and **refuse to start** when bound
off-loopback without a token. Ours implemented it zero times.

**x64dbg is not a fifth case.** `x64dbg-bridge/server.py:23-24` is a stdio
FastMCP server that drives the debugger through `x64dbg_automate.X64DbgClient`;
it opens no HTTP listener of its own, so there is no socket to put a token on.
Its risk is the command surface instead — that is 3.3.

**Contract delivered on all four HTTP bridges:**

- Shared `HSA_BRIDGE_TOKEN`, read by the host process and by the bridge process.
- Constant-time compare — `hmac.compare_digest` in the three Python hosts;
  a hand-rolled XOR accumulator in C#, because
  `CryptographicOperations.FixedTimeEquals` is .NET 5.0+ and the Unity plugin
  targets 2019.4.
- **Refuse to start** without a token, rather than starting open.
- 401 before the body is read, and a size cap checked before the body is
  buffered.
- `GET /health` stays unauthenticated on all four. It discloses nothing
  actionable, it keeps instance discovery from needing the token, and on UE it
  keeps a liveness probe from consuming a Game Thread slot or an exec log line.
- The bridge re-raises its own setup error instead of folding it into a result
  dict, so a missing token reaches the agent as a failed call rather than as
  prose describing a failure.

**The token file, per host.** An editor-side script runs *inside* the host
process, so `os.environ` there is the editor's environment, not the bridge
server's. A bare env var would read empty and the server would refuse to start.
Each host therefore also reads a file the bridge writes, and the environment
still wins when set:

| Host | File | Written by | Path known how |
|---|---|---|---|
| UE | `<project>/Saved/HSA/bridge_config.json` | `ue-bridge/src/index.ts` `writeBridgeConfig` | the project UE is told to deploy into |
| IDA | `%IDADIR%/plugins/hsa_bridge_token` | `ida-bridge/server.py` `write_bridge_config` | `HSA_IDA_PLUGIN_DIR` |
| Ghidra | `hsa_bridge_token` beside the script | `ghidra-bridge/server.py` `write_bridge_config` | `__file__`, always known |
| Unity | `<project>/Library/HsaBridgeConfig.json` | `unity-bridge/src/index.ts` `writeBridgeConfig` | `UNITY_PROJECT_DIR` |

UE's is under `Saved/`, which Unreal keeps out of version control. Unity's is
under `Library/`, which Unity keeps out of version control. Ghidra's lands in
the source tree, so it is covered by a `.gitignore` rule — without one, the
writer drops a live credential into a directory git will happily stage.

IDA and Unity need an explicit path from the operator rather than a guess. The
bridge cannot infer `%IDADIR%` or a Unity project root reliably, and guessing
would put the token in the wrong place more often than not, which reads as "auth
is broken" rather than "path is unset". Both writers decline to write when the
path is missing and say which variable to set, so the failure names its cause.

**Verification.** Each host was exercised against its real handler with the
host SDK stubbed, and each refusal-to-start was proven by probing the port and
getting a connection refusal rather than a response.

| Host | Checks |
|---|---|
| UE | no token → `NOT listening -> URLError`; health 200; no/wrong token 401; over cap 413 |
| IDA | `TOKEN='ida-token' CAP=4096`; health 200 `auth_required = True`; no/wrong token 401; over cap 413; 5 concurrent 0.5s calls in **0.69s** vs **2.50s** serial |
| Ghidra | health 200 `auth_required = True`; no/wrong token 401; over cap 413 |
| Unity | no token → `StartCalled=1` and connection refused; health 200 `auth_required=true`; no token 401; wrong token 401; **prefix** token 401; right token 200; 4194305 bytes → 413; env token overrides the config file |

The Unity run is a real `HttpListener` under `dotnet build` / `net8.0`, with the
file's auth slice copied verbatim and only the route table replaced by a
sentinel, because `HttpListenerContext` is sealed and cannot be faked.

The token writers were checked separately: both write the token to the expected
path, and IDA declines rather than guessing when `HSA_IDA_PLUGIN_DIR` is unset.
That test is what surfaced the two defects below.

The IDA concurrency number is a side effect of the same edit: the plugin had no
way to stop its server, so one slow `cmd_batch` blocked every other call behind
it. The Unity prefix case is the one a byte-by-byte `==` would also pass only by
accident — it is included to show the length check is doing real work.

**Two defects the writer test found, after 3.1 was already pushed:**

1. `mode: 0o600` in the writers' file-creation call does nothing. `os.open`'s
   mode is masked by the process umask, and on Windows it is not applied at
   all; the same is true of `fs.writeFileSync`'s `mode`. Measured: the Ghidra
   token landed at mode `666`. All four writers now `chmod` after the write.
2. The Ghidra token file is written into the source tree and was not ignored by
   git. `git status` showed it as untracked, one `git add -A` from being
   committed. Now covered by a `.gitignore` rule, asserted with
   `git check-ignore`.

Commits: `d5a0881` (UE), `4b9c8ef` (IDA), `320719a` (Ghidra), `0ae303e` (Unity).

### 3.2 UE Python executor runs arbitrary code with no auth — VERIFIED, and reassessed

`init_unreal.py` — `exec(code, exec_globals)` with full `__builtins__`.
Body arrives base64-decoded. Before 3.1 any local process could reach it.

**Reassessment of the research agent's recommendation.** The agent proposed
replacing `exec` with a dispatch table. Running that idea against the actual
code surfaces two things the agent did not account for:

1. **The liveness probe is itself `exec`.** `ue-bridge/src/index.ts` sent
   `print("pong")` through the same `/execute` endpoint to decide whether the
   server was up. Replacing `exec` with an action enum breaks this probe — it
   needs a separate `/health` endpoint that does not execute anything. This is a
   design constraint, not an implementation detail.

2. **`ue_python_status` is `ensurePythonExecutor()`**, which *deploys the file*
   as a side effect. So "check status" is not read-only. Any redesign must
   separate the probe from the deploy.

**Owner decision: keep `exec`, make it auditable** — "Token + giữ exec, có log".
3.1 is the token. Two of the three supporting conditions landed with it:

- 1MB cap on the code body, refused before the body is read.
- Every call logged with its outcome and duration.

Both the constraints above were also resolved as part of 3.1: `ensurePythonExecutor`
now probes `/health` rather than sending `print("pong")` through `/execute`, and
it reports a mismatch between the server's `auth_required` and the token it
holds, instead of silently deploying.

**What is still open.** The closed action enum — a wrapper for the common
`unreal.*` operations, with no path that accepts source code — was not taken.
It remains the one piece of 3.2 that would reduce capability rather than
localise risk, and it is the reason `ue_execute_python` is still a raw
`exec`. Not started.

**Trade-off:** the action enum removes arbitrary Python, which agents currently
use to reach `unreal.*` APIs with no wrapper. Token-only keeps that capability
and keeps the risk. The hybrid keeps capability but makes it auditable. The
owner chose the last of these.

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

#### 3.3 as implemented — two layers, and a false completion

The `inputs` fix shipped first (`validateToolPayload`, tests in
`tests/unit/bridge-schema.test.ts`). The command allowlist did not, and was
recorded as complete. It was not.

Grep for `ALLOWED_COMMAND|DENIED|allowlist|allow_list|DANGEROUS` across
`x64dbg-bridge/` returned **0 matches**. The manifest marked
`x64_search_command` as `mutates: true` and that was the whole of it. **A
consent gate is not a command allowlist:** `allow_mutations: true` records that
the user agreed, not that their agreement covered every command the verb can
reach. An approved call could still send `bc *`, `erun` or `d`.

Shipped: `X64DBG_COMMAND_ALLOWLIST` + `validateX64Command`, wired into both the
call and the batch path. Two details that turned out to matter:

- **The list is read-only with respect to the debuggee, not absolutely.**
  `d`/`dump` read the debuggee's memory and then *write a file*; `rtr`/`rte`
  advance the process. Both were in the first draft of the list, while the
  manifest description already claimed "read-only".
- **Chaining is screened on the whole string, not the tokens after the verb.**
  `lm|dd` puts the separator inside what whitespace-splitting calls the verb, so
  a token-scoped check rejects it for the wrong reason and says so.

A second, unrelated hole surfaced while testing this: `mutatesTool` was
reachable only through `validateBatchRequest`, and only `action: "batch"` called
it. **`action: "call"` never asked for consent at all** — `ida_rename`,
`ghidra_rename_symbol`, `ue_execute_python` and `x64_write_memory` all ran from
a single call with no `allow_mutations`. The path that looked stricter because it
named one explicit tool was the looser one. The two fixes are independent and
committed separately (`4614c14`, `4417932`).

### 3.4 UE bridges wedge instead of failing — DONE

`init_unreal.py` left the socket mid-conversation on one return path, and exited
the process on an error path that should have returned. Both turn a
debuggee-side fault into a dispatcher that stops answering, which reads as a
hang rather than a failure.

### 3.5 `ue_execute_python` ran arbitrary code with no record — DONE

Consent plus an audit entry. Consent is not a log: without the record, a session
that ran Python leaves no trace of what was approved.

### 3.6 `ue_execute_python` accepted any expression — DONE (off by default)

An AST allowlist, default off, so the restriction is opt-in rather than a
behaviour change for anyone already relying on arbitrary code.

### 3.7 Unity script creation accepted any path — DONE

`unity_create_script` wrote wherever it was told. Path validation is now in the
C# `HsaUnityServer.cs` handler.

**Not verified in a live editor.** 3.4, 3.6 and 3.7 were exercised against
harnesses only — a stubbed `unreal` module and an extracted C# validator. None
has been run inside a real UE or Unity Editor.

### 3.8 A check that exists proves nothing until something calls it — DONE

Found while reading two external bridges, and it names the failure mode both
this file and 3.3 kept stepping into: a control written, a test written for the
control, and the control never wired into the path. 3.3 was exactly that — the
allowlist was absent, and 3.3b was a gate that existed and was reachable only
from `action: "batch"`.

`ChiR24/Unreal_mcp` addresses it in `tests/unit/plugin/prequeue-gate-contracts.test.ts:6-11`,
and states it as a rule:

> a passing predicate proves nothing if nobody CALLS it. Every assertion here
> fails if the corresponding enforcement line is deleted

Its assertions read the C++ **source text** and check call ordering, so deleting
the enforcement line fails CI. The same repo's `Private/Safety/AGENTS.md:38`
applies the same idea to a ban: `UPackage::SavePackage` is machine-enforced
forbidden, and a raw call fails the build. "This is not advisory."

Applied here, in both directions:

- **Wiring.** `test_the_tool_itself_refuses_before_touching_the_client` asserts
  `x64_search_command` calls the validator and never reaches `cmd_sync` on a
  refused verb. The predicate's own tests would all pass with the call deleted.
- **Drift.** `TestAllowlistParityWithDispatcher` reads the dispatcher's
  `X64DBG_COMMAND_ALLOWLIST` out of `t17_bridge.ts` and compares it to the
  bridge's. Verified by mutation: adding `'zap'` to the dispatcher list fails the
  test. It **fails** rather than skips when the sibling repo is missing, because
  a skipped parity check is exactly how a second copy drifts unnoticed.

Also taken from `Unreal_mcp`, on the gap it documents about itself — its
`execute_python` authorises *whether* code runs (Admin scope) but not *what* it
contains, and its `system-control-security.test.ts` asserts metadata strings
rather than enforcement (`src/tools/catalog/.../system-control-security.test.ts:10-44`).
Our 3.6 AST allowlist is the position worth holding: restrict the content, not
only the permission.

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

### 4.4 `x64dbg_automate.mcp_server` ships 50 tools and is already a dependency — RESOLVED (counts wrong, conclusion reversed)

The research reports `x64dbg_automate/mcp_server.py` is 1603 lines with 50
`@mcp.tool()` functions, MIT, maintained by the same author as the plugin, and
already in our dependency tree — we have been reimplementing ~10 weak tools on
top of it. It has our defect too (errors returned as strings), and it solves the
bitness-aware path problem from 1.5.

**Read `mcp_server.py` before acting on this.** Done. The counts are wrong and
the conclusion does not survive them.

The file is **1168 lines with 46 `@mcp.tool()`** functions, not 1603/50. More
decisive than the counts:

- **46 tools, 46 of which return errors as strings.** `return f"Error: {e}"`
  appears 46 times; `isError` appears **zero** times. This is defect 1.1
  reproduced at scale, not the one instance we already fixed.
- **No authentication of any kind.** Grep for token/auth/secret across the
  module returns 0 hits.
- **`execute_command` runs `client.cmd_sync(command)` raw**, with no allowlist.
  Adopting it wholesale would have imported the exact hole 3.3 had to close.

It does solve 1.5: `_pe_bitness` reads the PE Machine field (`0x8664`→64,
`0x14C`→32). That is worth having and worth porting, not worth adopting 46
tools for.

**Resolution — Option A, keep our bridge, port selectively.** Wrapping a
46-tool server with no auth, no `isError` and an unfiltered raw-command
passthrough would have undone 1.1 and 3.3 in one move, to gain tool count
rather than capability. Four tools were missing against our manifest:
`read_memory`, `write_memory`, `disassemble`, `list_breakpoints`. They are
ported against the `X64DbgClient` API this bridge already depends on
(`read_memory`, `write_memory`, `disassemble_at`, `get_breakpoints`), with
`pyproject.toml` already pinning `x64dbg-automate[mcp]>=0.7.0` — so the
dependency claim holds even though the adoption plan did not.

Bitness-aware address handling is left as the obvious next port from upstream.

**Note on where the allowlist lives:** the dispatcher enforces the 3.3 command
allowlist, and `x64dbg-bridge/server.py` now enforces the same set itself
(`10f1c95`). The bridge is a separate process reachable on its own port, so
enforcing in one place only would have left a caller speaking MCP directly to it
with no filter at all. The two lists are one policy in two copies, kept in step
by a parity test that reads the dispatcher's source and compares — see
`McpPrequeueGate`-style layering under 3.8.


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

**Status — DONE.** Each bridge is now spawned as a real subprocess and the suite
asserts on the result (`8cc733c`, `tests/unit/bridge-spawn.test.ts`). The
separate finding in 3.3b came from a different test — the new single-call
consent test *failed* against the code as written, returning `success: true`
where it should have refused, and that failure is what exposed the missing gate.

---

## Outstanding after implementation

Carried forward deliberately rather than left implied-done.

- **3.4, 3.6 and 3.7 have not run in a live editor.** They were exercised
  against a stubbed `unreal` module and an extracted C# validator. The logic is
  tested; the integration is not.
- **The x64dbg allowlist is a denylist of writers expressed as an allowlist of
  readers.** It was built from knowledge of x64dbg rather than from its source:
  `WebSearch` returned nothing, `WebFetch` on help.x64dbg.com and the upstream
  repository 404'd, and `gh` is not authenticated here. A verb that neither
  writes to the debuggee, nor to a file, nor advances the process, and that I
  simply did not think of, would be admitted. Widening coverage means reading
  x64dbg's command table, not adding entries by feel.
- **Neither repository has been pushed.** All work is committed locally.

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
