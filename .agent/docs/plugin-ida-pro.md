---
library: plugin-ida-pro
version: 1
latest: true
category: mcp-plugin
target_app: IDA Pro 8.x / 9.x
transport: WebSocket ws://127.0.0.1:15555
plugin_type: IDAPython (.py in IDA plugins folder)
last_updated: 2026-03-27
---

# plugin-ida-pro — HSA MCP Bridge for IDA Pro

> Full IDAPython plugin reference: threading model, all module APIs, Hex-Rays Decompiler SDK, type system, debugger control, and complete WebSocket dispatch table.

---

## 1. Architecture & Threading Model

IDA Pro runs a single-threaded GUI/Database engine. All IDA DB operations MUST run on the Main Thread.
The plugin spawns a background asyncio WebSocket server. Every incoming command is dispatched to
Main Thread via `ida_kernwin.execute_sync` before any IDA API is called.

```
LLM Agent
  │  MCP tool call
  ▼
MCP Bridge (TypeScript)  ──ws://127.0.0.1:15555──►  IDAPython WebSocket Server
                                                        │  (asyncio loop, background thread)
                                                        │  receive JSON {"cmd":"...","params":{}}
                                                        │
                                                        ▼  execute_sync(fn, MFF_READ|MFF_WRITE)
                                                     IDA Main Thread
                                                        │  call IDA API (ida_hexrays, ida_funcs, …)
                                                        │  return result
                                                        ▼
                                                     send JSON {"ok":true,"result":...}
```

### 1.1. execute_sync Helper

```python
import ida_kernwin

def sync_exec(fn, write=False):
    """
    Push fn() to IDA Main Thread.
    write=True uses MFF_WRITE (for name/comment/patch operations).
    """
    box = {}
    def wrapper():
        try:
            box["v"] = fn()
        except Exception as e:
            box["err"] = str(e)
    flags = ida_kernwin.MFF_WRITE if write else ida_kernwin.MFF_READ
    ida_kernwin.execute_sync(wrapper, flags)
    if "err" in box:
        raise RuntimeError(box["err"])
    return box.get("v")
```

### 1.2. MFF Flags Reference

| Flag | Value | When to use |
|:-----|:------|:------------|
| `MFF_READ` | 1 | Read-only DB access (get_func, decompile, get_bytes) |
| `MFF_WRITE` | 2 | Mutates DB (set_name, set_cmt, patch_byte, apply_tinfo) |
| `MFF_NOWAIT` | 4 | Fire-and-forget, no return value needed |
| `MFF_FAST` | 8 | Used internally; do not combine with MFF_WRITE |

---

## 2. IDAPython Module Reference (Full)

### 2.1. ida_funcs — Function Analysis

```python
import ida_funcs, idautils

# Get function object at address
func = ida_funcs.get_func(ea)              # → func_t or None
# func.start_ea  — function start address
# func.size()    — byte size of function
# func.flags     — FUNC_* flags (FUNC_NORET, FUNC_THUNK, …)

# Get function name
name = ida_funcs.get_func_name(ea)         # → str

# Total function count
count = ida_funcs.get_func_qty()           # → int

# Iterate ALL functions in binary
for ea in idautils.Functions():
    f = ida_funcs.get_func(ea)
    print(hex(ea), ida_funcs.get_func_name(ea), f.size())

# Iterate function chunks (tails)
it = ida_funcs.func_tail_iterator_t(func)
while it.main() or it.next():
    chunk = it.chunk()
    print(hex(chunk.start_ea), chunk.size())

# Create a new function at ea
ida_funcs.add_func(ea)                     # → bool

# Delete function
ida_funcs.del_func(ea)                     # → bool

# Get function containing ea
func = ida_funcs.get_func(ea)              # returns None if ea not inside any function
```

### 2.2. ida_bytes — Read/Write/Patch Binary

```python
import ida_bytes

# Read single byte / word / dword / qword
b  = ida_bytes.get_byte(ea)
w  = ida_bytes.get_word(ea)
dw = ida_bytes.get_dword(ea)
qw = ida_bytes.get_qword(ea)

# Read N bytes as bytes object
raw = ida_bytes.get_bytes(ea, size)        # → bytes

# Patch byte / word / dword
ida_bytes.patch_byte(ea, 0x90)            # NOP
ida_bytes.patch_word(ea, 0x9090)
ida_bytes.patch_dword(ea, value)

# Type flags of item at ea
flags = ida_bytes.get_full_flags(ea)
is_code  = ida_bytes.is_code(flags)
is_data  = ida_bytes.is_data(flags)
is_align = ida_bytes.is_align(flags)
is_unknown = ida_bytes.is_unknown(flags)

# Read string literal
# STRTYPE_C=0, STRTYPE_C_16=2
content = ida_bytes.get_strlit_contents(ea, -1, ida_nalt.STRTYPE_C)  # → bytes or None

# Create code/data item
ida_bytes.create_insn(ea)
ida_bytes.create_data(ea, ida_bytes.FF_DWORD, 4, ida_idaapi.BADADDR)
```

### 2.3. ida_name — Symbol Naming

```python
import ida_name

# Get name at ea
name = ida_name.get_name(ea)              # → str (empty if unnamed)

# Set name at ea
# SN_CHECK   — verify name is valid
# SN_NOCHECK — skip validity check
# SN_LOCAL   — mark as local label
# SN_FORCE   — add numeric suffix if conflict
ok = ida_name.set_name(ea, "my_func", ida_name.SN_CHECK)  # → bool

# Lookup ea by name (ea=0 means global)
found_ea = ida_name.get_name_ea(0, "printf")  # → ea or BADADDR

# Demangle a name
demangled = ida_name.demangle_name("?foo@@YAXXZ", ida_name.MNG_LONG_FORM)
```

### 2.4. ida_kernwin — UI & Thread Sync

```python
import ida_kernwin

# Thread sync (see section 1.1)
ida_kernwin.execute_sync(fn, ida_kernwin.MFF_READ)

# Navigation
ida_kernwin.jumpto(ea)                    # Jump IDA view to address
ida_kernwin.refresh_idaview_anyway()      # Redraw disassembly view

# Get current cursor address
cur = ida_kernwin.get_screen_ea()         # → ea

# Message output
ida_kernwin.msg("Hello from plugin
")

# Ask user input
answer = ida_kernwin.ask_str("default", 0, "Enter new name:")  # → str or None
confirmed = ida_kernwin.ask_yn(0, "Rename this function?")     # → 0/1/-1

# Open a chooser (list selection UI)
# ida_kernwin.choose_itype_t, choose_simple_t — advanced UI
```

### 2.5. ida_hexrays — Hex-Rays Decompiler

```python
import ida_hexrays

# Check if decompiler is available
if not ida_hexrays.init_hexrays_plugin():
    raise RuntimeError("Hex-Rays decompiler not available")

# Decompile function at ea → cfuncptr_t
cf = ida_hexrays.decompile(ea)
# cf is None if decompilation fails
pseudocode_str = str(cf)                  # → C-like pseudocode string

# cfuncptr_t attributes:
# cf.body        → cinsn_t  (root statement of AST)
# cf.lvars       → lvar_saved_info_t (local variables)
# cf.arguments   → lvar_saved_info_t list (function args)
# cf.entry_ea    → ea_t (function entry)
# cf.hdrlines    → int (number of header lines in pseudocode)

# Get pseudocode as list of lines (for syntax highlighting)
sv = cf.get_pseudocode()                  # → strvec_t
for i in range(len(sv)):
    print(sv[i].line)

# AST Traversal with ctree_visitor_t
class AssignmentFinder(ida_hexrays.ctree_visitor_t):
    def __init__(self):
        ida_hexrays.ctree_visitor_t.__init__(self, ida_hexrays.CV_FAST)
        self.assigns = []
    def visit_expr(self, e):
        if e.op == ida_hexrays.cot_asg:   # assignment operator
            self.assigns.append(e.ea)
        return 0
    def visit_insn(self, i):
        return 0                           # must implement both

v = AssignmentFinder()
v.apply_to(cf.body, None)

# Microcode (MMAT_* maturity levels)
# MMAT_GENERATED=1  MMAT_PREOPTIMIZED=2  MMAT_LOCOPT=3
# MMAT_CALLS=4      MMAT_GLBOPT1=5       MMAT_GLBOPT2=6
# MMAT_GLBOPT3=7    MMAT_LVARS=8         MMAT_FINAL=9

func = ida_funcs.get_func(ea)
mba = ida_hexrays.gen_microcode(
    ida_hexrays.mba_ranges_t(func),
    None,                                 # hf (hexrays_failure_t*), can be None
    None,                                 # reqmat (mba_maturity_t*), None = MMAT_FINAL
    ida_hexrays.DECOMP_NO_WAIT,
    ida_hexrays.MMAT_PREOPTIMIZED         # stop at this maturity
)
if mba:
    print(f"Blocks: {mba.qty}")

# Hex-Rays events (register callback)
class HxHook(ida_hexrays.Hexrays_Hooks):
    def open_pseudocode(self, vu):
        # vu: vdui_t — pseudocode view
        ida_kernwin.msg(f"Opened pseudocode for {hex(vu.cfunc.entry_ea)}
")
        return 0

hook = HxHook()
hook.hook()
# hook.unhook() to unregister
```

### 2.6. ida_dbg — Debugger Control

```python
import ida_dbg, ida_idd

# Start debugging a new process
# Returns: 1=ok, -1=error, 0=cancelled
ret = ida_dbg.start_process(
    "/path/to/exe",                       # exe path
    "arg1 arg2",                          # cmdline args
    "/working/dir"                        # working dir
)

# Attach to existing process by PID
ida_dbg.attach_process(pid, -1)           # -1 = first available thread

# Run/pause/step
ida_dbg.continue_process()
ida_dbg.request_pause()
ida_dbg.request_step_into()
ida_dbg.request_step_over()

# Breakpoints
# BPT_DEFAULT = hardware or software auto-select
# BPT_SOFT    = software INT3 breakpoint
# BPT_EXEC    = hardware execute breakpoint
# BPT_WRITE   = hardware write watchpoint
# BPT_READ    = hardware read/write watchpoint
ok = ida_dbg.add_bpt(ea, 1, ida_idd.BPT_DEFAULT)    # ea, size, type
ok = ida_dbg.del_bpt(ea)
bpt = ida_dbg.bpt_t()
ok  = ida_dbg.get_bpt(ea, bpt)
# bpt.ea, bpt.type, bpt.size, bpt.flags, bpt.condition

# Read CPU register
rv = ida_idd.regval_t()
ida_dbg.get_reg_val("rip", rv)
print(hex(rv.ival))                       # integer value

# Write register
rv2 = ida_idd.regval_t()
rv2.ival = 0x401000
ida_dbg.set_reg_val("rip", rv2)

# Read process memory during debug session
buf = ida_dbg.dbg_read_memory(ea, 16)    # → bytes or None

# Appcall: call a function in the debugged process
# ida_idd.Appcall.proto("void foo(int a, char* b)")
# result = ida_idd.Appcall.call(ea, arg1, arg2)

# Exit process
ida_dbg.exit_process()
```

### 2.7. ida_segment — Segment Operations

```python
import ida_segment

# Get segment at ea
seg = ida_segment.getseg(ea)
# seg.start_ea, seg.size(), seg.name (use ida_segment.get_segm_name(seg))
# seg.type: SEG_CODE=0, SEG_DATA=2, SEG_BSS=3, SEG_XTRN=9

# Iterate all segments
for i in range(ida_segment.get_segm_qty()):
    s = ida_segment.getnseg(i)
    print(hex(s.start_ea), ida_segment.get_segm_name(s), s.size())

# Create a new segment
ida_segment.add_segm(
    0,           # para: 0=auto
    0x10000,     # start ea
    0x11000,     # end ea
    "MY_SEG",    # name
    "DATA"       # sclass: "CODE", "DATA", "CONST", "BSS"
)
```

### 2.8. ida_ua — Instruction Decode

```python
import ida_ua

# Decode instruction at ea
insn = ida_ua.insn_t()
length = ida_ua.decode_insn(insn, ea)     # → int (bytes decoded) or 0 on fail

# insn attributes:
# insn.ea       — address of instruction
# insn.size     — byte length
# insn.itype    — internal instruction type ID
# insn.ops[]    — operands (op_t): up to 8 operands
# insn.ops[0].type  — o_reg, o_mem, o_phrase, o_displ, o_imm, o_far, o_near
# insn.ops[0].value — immediate value
# insn.ops[0].reg   — register index

mnemonic = ida_ua.print_insn_mnem(ea)     # → str, e.g. "mov"

# Print full disassembly line
line = idc.GetDisasm(ea)                  # → "mov rax, [rbx+8]"
```

### 2.9. idautils — Iterators & Helpers

```python
import idautils

# All executable heads (instructions/data items)
for ea in idautils.Heads(start_ea, end_ea):
    print(hex(ea))

# All named addresses (public/local symbols)
for ea, name in idautils.Names():
    print(hex(ea), name)

# All string literals
for s in idautils.Strings():
    print(hex(s.ea), s.length, str(s))

# Cross-references TO an address (callers / data refs)
for xref in idautils.XrefsTo(ea):
    print(f"  from {hex(xref.frm)} type={xref.type} iscode={xref.iscode}")

# Cross-references FROM an address (callees / data reads)
for xref in idautils.XrefsFrom(ea, 0):
    print(f"  to {hex(xref.to)} type={xref.type}")

# Code cross-refs only
for xref in idautils.CodeRefsTo(ea, 0):   # 0=don't follow flows
    print(hex(xref))

# Data cross-refs
for xref in idautils.DataRefsTo(ea):
    print(hex(xref))
```

### 2.10. ida_typeinf / idaapi — Type System

```python
import idaapi, ida_typeinf

# Apply a C declaration to an address
tif = ida_typeinf.tinfo_t()
ok = ida_typeinf.parse_decl(tif, None, "int (*)(char *, int)", 0)
if ok:
    ida_typeinf.apply_tinfo(ea, tif, ida_typeinf.TINFO_DEFINITE)

# Get type info of an address
tif2 = ida_typeinf.tinfo_t()
ok = idaapi.get_tinfo(tif2, ea)
if ok:
    print(tif2._print())                  # → "int (*)(char *, int)"

# Create a struct type programmatically
sid = idaapi.add_struc(idaapi.BADADDR, "MyStruct", False)
st  = idaapi.get_struc(sid)
idaapi.add_struc_member(st, "field_0", 0, idaapi.FF_DWORD, None, 4)
idaapi.add_struc_member(st, "field_4", 4, idaapi.FF_QWORD, None, 8)

# Set struct member type
member = idaapi.get_member_by_name(st, "field_0")
member_tinfo = idaapi.tinfo_t()
# ... fill member_tinfo ...
idaapi.set_member_tinfo(st, member, 0, member_tinfo, 0)  # → SMT_OK on success

# Apply struct to memory region
struct_tif = idaapi.tinfo_t()
struct_tif.get_named_type(None, "MyStruct")
idaapi.apply_tinfo(ea, struct_tif, idaapi.TINFO_DEFINITE)
```

---

## 3. Complete WebSocket Plugin Implementation

```python
# hsa_ida_plugin.py
# Install: copy to %IDADIR%/plugins/ (Windows) or $IDADIR/plugins/ (Linux/Mac)

import idaapi, ida_kernwin, ida_funcs, ida_hexrays, ida_typeinf
import ida_name, ida_bytes, ida_dbg, ida_idd, ida_nalt, ida_ida, ida_segment, ida_ua
import idautils, idc
import asyncio, json, threading, traceback
import websockets

PLUGIN_NAME    = "HSA MCP Bridge"
PLUGIN_VERSION = "1.0.0"
WS_HOST        = "127.0.0.1"
WS_PORT        = 15555

# ── Thread-safe sync executor ───────────────────────────────────────

def sync_exec(fn, write=False):
    box = {}
    def wrapper():
        try:    box["v"] = fn()
        except Exception as e: box["err"] = str(e)
    flags = ida_kernwin.MFF_WRITE if write else ida_kernwin.MFF_READ
    ida_kernwin.execute_sync(wrapper, flags)
    if "err" in box: raise RuntimeError(box["err"])
    return box.get("v")

# ── Command implementations ─────────────────────────────────────────

def cmd_get_info():
    def _():
        info = idaapi.get_inf_structure()
        return {
            "file":       idaapi.get_input_file_path(),
            "imagebase":  hex(ida_nalt.get_imagebase()),
            "is_64bit":   info.is_64bit(),
            "is_dll":     info.is_dll(),
            "proc":       ida_ida.inf_get_procname(),
            "segments":   ida_segment.get_segm_qty(),
            "functions":  ida_funcs.get_func_qty(),
        }
    return sync_exec(_)

def cmd_list_functions(offset=0, limit=200):
    def _():
        result = []
        for i, ea in enumerate(idautils.Functions()):
            if i < offset: continue
            if i >= offset + limit: break
            f = ida_funcs.get_func(ea)
            result.append({
                "ea":   hex(ea),
                "name": ida_funcs.get_func_name(ea),
                "size": f.size() if f else 0,
            })
        return result
    return sync_exec(_)

def cmd_get_pseudocode(ea):
    def _():
        if not ida_hexrays.init_hexrays_plugin():
            return {"error": "Hex-Rays not available"}
        cf = ida_hexrays.decompile(ea)
        if not cf:
            return {"error": "Decompile failed"}
        lines = []
        sv = cf.get_pseudocode()
        for i in range(len(sv)):
            lines.append(sv[i].line)
        return {"pseudocode": str(cf), "lines": lines, "entry_ea": hex(cf.entry_ea)}
    return sync_exec(_)

def cmd_get_microcode(ea, maturity="preoptimized"):
    maturity_map = {
        "generated":    ida_hexrays.MMAT_GENERATED,
        "preoptimized": ida_hexrays.MMAT_PREOPTIMIZED,
        "calls":        ida_hexrays.MMAT_CALLS,
        "final":        ida_hexrays.MMAT_FINAL,
    }
    mat = maturity_map.get(maturity, ida_hexrays.MMAT_PREOPTIMIZED)
    def _():
        func = ida_funcs.get_func(ea)
        if not func: return {"error": "No function at ea"}
        mba = ida_hexrays.gen_microcode(
            ida_hexrays.mba_ranges_t(func), None, None,
            ida_hexrays.DECOMP_NO_WAIT, mat)
        return {"microcode": str(mba) if mba else None, "blocks": mba.qty if mba else 0}
    return sync_exec(_)

def cmd_rename_symbol(ea, name):
    def _():
        ok = ida_name.set_name(ea, name, ida_name.SN_CHECK | ida_name.SN_FORCE)
        ida_kernwin.refresh_idaview_anyway()
        return {"ok": ok, "name": name}
    return sync_exec(_, write=True)

def cmd_read_bytes(ea, size):
    def _():
        raw = ida_bytes.get_bytes(ea, size)
        return {"hex": raw.hex() if raw else None, "ea": hex(ea), "size": size}
    return sync_exec(_)

def cmd_patch_bytes(ea, hex_str):
    def _():
        data = bytes.fromhex(hex_str)
        for i, b in enumerate(data):
            ida_bytes.patch_byte(ea + i, b)
        ida_kernwin.refresh_idaview_anyway()
        return {"ok": True, "patched": len(data)}
    return sync_exec(_, write=True)

def cmd_set_comment(ea, comment, is_function=False):
    def _():
        if is_function:
            idc.set_func_cmt(ea, comment, 0)
        else:
            idc.set_cmt(ea, comment, 0)
        return {"ok": True}
    return sync_exec(_, write=True)

def cmd_get_xrefs_to(ea):
    def _():
        return [{"from": hex(r.frm), "type": r.type, "iscode": r.iscode}
                for r in idautils.XrefsTo(ea)]
    return sync_exec(_)

def cmd_get_xrefs_from(ea):
    def _():
        return [{"to": hex(r.to), "type": r.type, "iscode": r.iscode}
                for r in idautils.XrefsFrom(ea, 0)]
    return sync_exec(_)

def cmd_get_strings(min_len=4):
    def _():
        sc = idautils.Strings()
        sc.setup(minlen=min_len)
        return [{"ea": hex(s.ea), "value": str(s), "length": s.length,
                 "type": s.strtype} for s in sc]
    return sync_exec(_)

def cmd_get_imports():
    def _():
        result = []
        nimps = idaapi.get_import_module_qty()
        for i in range(nimps):
            mod = idaapi.get_import_module_name(i)
            def cb(ea, name, ordinal, mod=mod):
                result.append({"module": mod, "ea": hex(ea), "name": name, "ordinal": ordinal})
                return True
            idaapi.enum_import_names(i, cb)
        return result
    return sync_exec(_)

def cmd_apply_type(ea, c_decl):
    def _():
        tif = ida_typeinf.tinfo_t()
        ok = ida_typeinf.parse_decl(tif, None, c_decl, 0)
        if not ok: return {"ok": False, "error": "parse_decl failed"}
        ida_typeinf.apply_tinfo(ea, tif, ida_typeinf.TINFO_DEFINITE)
        return {"ok": True}
    return sync_exec(_, write=True)

def cmd_debug_add_bp(ea, bp_type="soft"):
    bp_map = {"soft": ida_idd.BPT_SOFT, "exec": ida_idd.BPT_EXEC,
              "write": ida_idd.BPT_WRITE, "read": ida_idd.BPT_READ}
    def _():
        ok = ida_dbg.add_bpt(ea, 1, bp_map.get(bp_type, ida_idd.BPT_DEFAULT))
        return {"ok": ok, "ea": hex(ea), "type": bp_type}
    return sync_exec(_, write=True)

def cmd_debug_get_reg(reg_name):
    def _():
        rv = ida_idd.regval_t()
        ok = ida_dbg.get_reg_val(reg_name, rv)
        return {"ok": ok, "reg": reg_name, "value": hex(rv.ival)}
    return sync_exec(_)

def cmd_jump_to(ea):
    def _():
        ida_kernwin.jumpto(ea)
        ida_kernwin.refresh_idaview_anyway()
        return {"ok": True, "ea": hex(ea)}
    return sync_exec(_)

# ── WebSocket dispatch table ────────────────────────────────────────

DISPATCH = {
    # Info
    "get_info":         lambda p: cmd_get_info(),
    # Functions
    "list_functions":   lambda p: cmd_list_functions(p.get("offset",0), p.get("limit",200)),
    # Decompiler
    "get_pseudocode":   lambda p: cmd_get_pseudocode(int(p["ea"],16)),
    "get_microcode":    lambda p: cmd_get_microcode(int(p["ea"],16), p.get("maturity","preoptimized")),
    # Naming & comments
    "rename_symbol":    lambda p: cmd_rename_symbol(int(p["ea"],16), p["name"]),
    "set_comment":      lambda p: cmd_set_comment(int(p["ea"],16), p["comment"], p.get("func",False)),
    # Memory
    "read_bytes":       lambda p: cmd_read_bytes(int(p["ea"],16), p["size"]),
    "patch_bytes":      lambda p: cmd_patch_bytes(int(p["ea"],16), p["hex"]),
    # Navigation
    "jump_to":          lambda p: cmd_jump_to(int(p["ea"],16)),
    # XRefs
    "get_xrefs_to":     lambda p: cmd_get_xrefs_to(int(p["ea"],16)),
    "get_xrefs_from":   lambda p: cmd_get_xrefs_from(int(p["ea"],16)),
    # Strings
    "get_strings":      lambda p: cmd_get_strings(p.get("min_len",4)),
    # Imports
    "get_imports":      lambda p: cmd_get_imports(),
    # Type system
    "apply_type":       lambda p: cmd_apply_type(int(p["ea"],16), p["decl"]),
    # Debugger
    "debug_add_bp":     lambda p: cmd_debug_add_bp(int(p["ea"],16), p.get("type","soft")),
    "debug_get_reg":    lambda p: cmd_debug_get_reg(p["reg"]),
}

# ── WebSocket server ────────────────────────────────────────────────

async def ws_handler(websocket, path):
    async for raw in websocket:
        try:
            msg    = json.loads(raw)
            cmd    = msg.get("cmd")
            params = msg.get("params", {})
            handler = DISPATCH.get(cmd)
            if handler:
                result = handler(params)
                await websocket.send(json.dumps({"ok": True, "result": result}))
            else:
                await websocket.send(json.dumps({"ok": False, "error": f"Unknown: {cmd}"}))
        except Exception as e:
            await websocket.send(json.dumps({"ok": False, "error": str(e),
                                             "trace": traceback.format_exc()}))

def run_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    srv  = websockets.serve(ws_handler, WS_HOST, WS_PORT)
    loop.run_until_complete(srv)
    ida_kernwin.msg(f"[HSA] WebSocket server on ws://{WS_HOST}:{WS_PORT}\n")
    loop.run_forever()

# ── Plugin entry ────────────────────────────────────────────────────

class HsaIdaPlugin(idaapi.plugin_t):
    flags        = idaapi.PLUGIN_KEEP
    comment      = "HSA MCP Bridge — expose IDA DB over WebSocket"
    help         = ""
    wanted_name  = "HSA IDA Bridge"
    wanted_hotkey = ""

    def init(self):
        threading.Thread(target=run_ws_server, daemon=True).start()
        return idaapi.PLUGIN_KEEP

    def run(self, arg): pass
    def term(self):     pass

def PLUGIN_ENTRY():
    return HsaIdaPlugin()
```

---

## 4. MCP Command Dispatch Table (Full)

| cmd | Required params | Returns | IDA API |
|:----|:----------------|:--------|:--------|
| `get_info` | — | file, imagebase, proc, counts | `get_inf_structure`, `get_input_file_path` |
| `list_functions` | `offset?`, `limit?` | `[{ea,name,size}]` | `idautils.Functions()` |
| `get_pseudocode` | `ea` | `{pseudocode, lines}` | `ida_hexrays.decompile` |
| `get_microcode` | `ea`, `maturity?` | `{microcode, blocks}` | `gen_microcode` |
| `rename_symbol` | `ea`, `name` | `{ok}` | `ida_name.set_name` |
| `set_comment` | `ea`, `comment`, `func?` | `{ok}` | `idc.set_cmt / set_func_cmt` |
| `read_bytes` | `ea`, `size` | `{hex}` | `ida_bytes.get_bytes` |
| `patch_bytes` | `ea`, `hex` | `{ok, patched}` | `ida_bytes.patch_byte` |
| `jump_to` | `ea` | `{ok}` | `ida_kernwin.jumpto` |
| `get_xrefs_to` | `ea` | `[{from,type}]` | `idautils.XrefsTo` |
| `get_xrefs_from` | `ea` | `[{to,type}]` | `idautils.XrefsFrom` |
| `get_strings` | `min_len?` | `[{ea,value}]` | `idautils.Strings` |
| `get_imports` | — | `[{module,ea,name}]` | `idaapi.enum_import_names` |
| `apply_type` | `ea`, `decl` | `{ok}` | `ida_typeinf.apply_tinfo` |
| `debug_add_bp` | `ea`, `type?` | `{ok}` | `ida_dbg.add_bpt` |
| `debug_get_reg` | `reg` | `{value}` | `ida_dbg.get_reg_val` |

---

## 5. Install & Verify

```bash
# Windows
copy hsa_ida_plugin.py "%IDADIR%\plugins\"
# macOS/Linux
cp hsa_ida_plugin.py "$IDADIR/plugins/"

# Test connection (after opening IDA with any binary)
python3 -c "
import asyncio, websockets, json
async def test():
    async with websockets.connect('ws://127.0.0.1:15555') as ws:
        await ws.send(json.dumps({'cmd':'get_info','params':{}}))
        print(await ws.recv())
asyncio.run(test())
"
```

<!-- BM25: library=plugin-ida-pro target=IDA Pro IDAPython MCP bridge execute_sync hexrays decompile -->
