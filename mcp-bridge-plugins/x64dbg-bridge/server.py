# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp>=1.26.0,<2",
#   "x64dbg_automate[mcp]>=0.9.0,<1",
# ]
# ///
"""
HSA x64dbg MCP Bridge — Custom Search & Auto-Connect Server
=============================================================
This supplements the official x64dbg-automate-mcp with:
1. Auto-connect: finds running x64dbg sessions automatically
2. Search tools: string search, pattern search, reference search
3. Convenience wrappers for common RE tasks

Called by bridge-handler.ts as the primary x64dbg bridge server.
It imports the official MCP tools AND adds custom tools.
"""

import os
import json
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from x64dbg_automate import X64DbgClient

mcp = FastMCP("x64dbg-hsa-bridge")


class BridgeError(RuntimeError):
    """Bridge-side failure. Raising this makes FastMCP set isError, so the
    agent sees a failed call instead of prose describing a failure."""

# ── Auto-Connect Logic ────────────────────────────────────────

_client: X64DbgClient | None = None


def _resolve_x64dbg_path() -> str:
    """Fail loudly when unset. A hardcoded fallback here used to point at one
    developer's snapshot directory, so a fresh install silently targeted a path
    that does not exist on the machine actually running it."""
    path = os.environ.get("X64DBG_PATH", "").strip()
    if not path:
        raise BridgeError(
            "X64DBG_PATH is not set. Point it at x96dbg.exe (preferred) or directly "
            "at x64dbg.exe / x32dbg.exe for the x64dbg install you want to drive."
        )
    return path


def get_client() -> X64DbgClient:
    """Get or create X64DbgClient (no auto-attach)."""
    global _client
    if _client is not None:
        return _client
    _client = X64DbgClient(_resolve_x64dbg_path())
    return _client


def ensure_attached(pid: int | None = None) -> X64DbgClient:
    """Ensure client is attached to a session. Auto-attach if not."""
    client = get_client()

    if pid is not None and pid > 0:
        client.attach_session(pid)
        return client

    # Check if we have an active session
    try:
        client.is_debugging()
        return client
    except Exception:
        pass

    # Try to find and attach to a session
    sessions = client.list_sessions()
    if sessions:
        client.attach_session(sessions[0].pid)
        return client

    raise RuntimeError(
        "No x64dbg session found. Open x64dbg and load a binary, "
        "or use x64_start_session to launch one."
    )


def format_sessions(sessions) -> str:
    data = []
    for session in sessions or []:
        data.append({
            "pid": getattr(session, "pid", None),
            "name": getattr(session, "name", "") or getattr(session, "process_name", "") or "",
            "path": getattr(session, "path", "") or getattr(session, "exe", "") or "",
        })
    return json.dumps({
        "ok": True,
        "sessions": data,
        "count": len(data),
    }, indent=2, default=str)


def resolve_pid(pid: int = 0, session_id: str = "") -> int | None:
    if pid and pid > 0:
        return pid
    if session_id:
        try:
            parsed = int(session_id)
            return parsed if parsed > 0 else None
        except ValueError:
            return None
    return None


def _match_scope(region, module_name: str = "", module_path: str = "") -> bool:
    info = str(getattr(region, "info", "") or "")
    if not module_name and not module_path:
        return True
    if module_name and module_name.lower() in info.lower():
        return True
    if module_path and module_path.lower() in info.lower():
        return True
    return False


# ── Session Management Tools ─────────────────────────────────

@mcp.tool()
def x64_list_sessions(scan_ports: Optional[List[int]] = None) -> str:
    """List available x64dbg sessions before attaching."""
    try:
        client = get_client()
        sessions = client.list_sessions()
        return format_sessions(sessions)
    except Exception as e:
        raise BridgeError(f"Error listing sessions: {e}") from e


@mcp.tool()
def x64_auto_connect(pid: int = 0, session_id: str = "") -> str:
    """Auto-detect and connect to a running x64dbg session.
    If no session found, returns instructions to start one.
    """
    try:
        client = get_client()
        sessions = client.list_sessions()
        if not sessions:
            raise BridgeError(
                "No x64dbg sessions found. Use x64_start_session to launch x64dbg "
                "with a target binary."
            )

        wanted_pid = resolve_pid(pid, session_id)
        session = None
        if wanted_pid is not None:
            for candidate in sessions:
                if getattr(candidate, "pid", None) == wanted_pid:
                    session = candidate
                    break
            if session is None:
                raise BridgeError(f"No x64dbg session found for PID {wanted_pid}.")
        if session is None:
            session = sessions[0]
        client.attach_session(session.pid)

        # Try to get status, but don't fail if ZMQ times out
        status_info = ""
        try:
            is_dbg = client.is_debugging()
            is_run = client.is_running()
            status_info = f"  Debugging: {is_dbg}\n  Running: {is_run}"
        except Exception:
            status_info = "  Status: Connected (debugger status unavailable — try pausing first)"

        return (
            f"✅ Connected to x64dbg (PID {session.pid})\n"
            f"{status_info}"
        )
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_start_session(executable: str, args: str = "") -> str:
    """Start a new x64dbg session with a target executable.

    Args:
        executable: Full path to the .exe to debug (e.g. 'C:/Windows/System32/notepad.exe')
        args: Optional command line arguments for the target
    """
    try:
        client = get_client()
        client.start_session(executable, args if args else None)

        # Wait for session to initialize
        import time
        time.sleep(3)

        is_dbg = client.is_debugging()
        pid = client.debugee_pid() if is_dbg else None
        return (
            f"✅ x64dbg started with {executable}\n"
            f"  Debugging: {is_dbg}\n"
            f"  Target PID: {pid}"
        )
    except Exception as e:
        raise BridgeError(f"Error starting session: {e}") from e


@mcp.tool()
def x64_attach_process(pid: int) -> str:
    """Attach x64dbg to a running process by PID.

    Args:
        pid: Process ID to attach to
    """
    try:
        client = get_client()
        client.attach(pid)
        import time
        time.sleep(2)
        return f"✅ Attached to process PID {pid}"
    except Exception as e:
        raise BridgeError(f"Error attaching: {e}") from e


# ── Search Tools ──────────────────────────────────────────────

@mcp.tool()
def x64_find_string(pattern: str, max_results: int = 50, pid: int = 0, session_id: str = "", module_name: str = "", module_path: str = "") -> str:
    """Search for a string pattern in the debugged process memory.
    Scans readable memory regions for ASCII/UTF-16 string occurrences.

    Args:
        pattern: String to search for (e.g. 'kernel32', 'password', 'http://')
        max_results: Maximum matches to return (default 50)
    """
    try:
        client = ensure_attached(resolve_pid(pid, session_id))
        mem = client.memmap()
        results = []
        pattern_bytes = pattern.encode('ascii')
        pattern_utf16 = pattern.encode('utf-16-le')
        for region in mem:
            if len(results) >= max_results:
                break
            # Only scan readable regions of reasonable size (< 10MB)
            if region.region_size > 10 * 1024 * 1024 or region.region_size == 0:
                continue
            if not _match_scope(region, module_name, module_path):
                continue
            try:
                data = client.read_memory(region.base_address, region.region_size)
                if not data:
                    continue
                # Search ASCII
                offset = 0
                while offset < len(data) and len(results) < max_results:
                    idx = data.find(pattern_bytes, offset)
                    if idx == -1:
                        break
                    addr = region.base_address + idx
                    # Extract surrounding context (up to 60 bytes)
                    ctx_start = max(0, idx - 10)
                    ctx_end = min(len(data), idx + len(pattern_bytes) + 50)
                    context = data[ctx_start:ctx_end].decode('ascii', errors='replace')
                    results.append({
                        "address": hex(addr),
                        "type": "ASCII",
                        "context": context.replace('\x00', '.').replace('\n', '\\n'),
                        "module": region.info if hasattr(region, 'info') else "",
                    })
                    offset = idx + 1

                # Search UTF-16LE
                offset = 0
                while offset < len(data) and len(results) < max_results:
                    idx = data.find(pattern_utf16, offset)
                    if idx == -1:
                        break
                    addr = region.base_address + idx
                    results.append({
                        "address": hex(addr),
                        "type": "UTF-16",
                        "context": pattern,
                        "module": region.info if hasattr(region, 'info') else "",
                    })
                    offset = idx + 2
            except Exception:
                continue

        if not results:
            return f"No matches found for \"{pattern}\""
        
        output = f"### String Search: \"{pattern}\" ({len(results)} matches)\n\n"
        for r in results:
            output += f"- `{r['address']}` [{r['type']}] {r['module']} → `{r['context'][:60]}`\n"
        return output
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_find_pattern(hex_pattern: str, max_results: int = 50, pid: int = 0, session_id: str = "", module_name: str = "", module_path: str = "") -> str:
    """Search for a hex byte pattern in process memory (no wildcards in this mode).

    Args:
        hex_pattern: Hex bytes without spaces, e.g. '488B4110' or 'E8'
        max_results: Maximum matches (default 50)
    """
    try:
        client = ensure_attached(resolve_pid(pid, session_id))
        # Clean hex input
        clean = hex_pattern.replace(" ", "").replace("0x", "")
        search_bytes = bytes.fromhex(clean)
        
        mem = client.memmap()
        results = []

        for region in mem:
            if len(results) >= max_results:
                break
            if region.region_size > 10 * 1024 * 1024 or region.region_size == 0:
                continue
            if not _match_scope(region, module_name, module_path):
                continue
            try:
                data = client.read_memory(region.base_address, region.region_size)
                if not data:
                    continue
                offset = 0
                while offset < len(data) and len(results) < max_results:
                    idx = data.find(search_bytes, offset)
                    if idx == -1:
                        break
                    addr = region.base_address + idx
                    # Show surrounding bytes
                    ctx_start = max(0, idx)
                    ctx_bytes = data[ctx_start:ctx_start + 16].hex(' ')
                    results.append({
                        "address": hex(addr),
                        "bytes": ctx_bytes,
                        "module": region.info if hasattr(region, 'info') else "",
                    })
                    offset = idx + 1
            except Exception:
                continue

        if not results:
            return f"No matches found for pattern {hex_pattern}"
        
        output = f"### Pattern Search: {hex_pattern} ({len(results)} matches)\n\n"
        for r in results:
            output += f"- `{r['address']}` {r['module']} → `{r['bytes']}`\n"
        return output
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_find_references(address: str, pid: int = 0, session_id: str = "", module_name: str = "", module_path: str = "") -> str:
    """Find all references to a specific address in code sections.
    Searches for the address value in E8 (call) and FF15 (call [addr]) patterns.

    Args:
        address: Hex address (e.g. '0x7FF9E67E0000' or 'rip')
    """
    try:
        client = ensure_attached(resolve_pid(pid, session_id))

        # Resolve address via eval
        addr_val, _ = client.eval_sync(address)
        addr_bytes = addr_val.to_bytes(8, 'little')

        mem = client.memmap()
        results = []

        # Search for absolute references (mov/lea with full address)
        for region in mem:
            if len(results) >= 50:
                break
            if region.region_size > 10 * 1024 * 1024 or region.region_size == 0:
                continue
            if not _match_scope(region, module_name, module_path):
                continue
            try:
                data = client.read_memory(region.base_address, region.region_size)
                if not data:
                    continue
                offset = 0
                while offset < len(data) and len(results) < 50:
                    idx = data.find(addr_bytes[:4], offset)  # Search 4-byte ref
                    if idx == -1:
                        break
                    ref_addr = region.base_address + idx
                    results.append({
                        "address": hex(ref_addr),
                        "module": region.info if hasattr(region, 'info') else "",
                    })
                    offset = idx + 1
            except Exception:
                continue

        if not results:
            return f"No references found to {address} ({hex(addr_val)})"
        
        output = f"### References to {address} ({hex(addr_val)}) — {len(results)} matches\n\n"
        for r in results:
            output += f"- `{r['address']}` {r['module']}\n"
        return output
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_find_api_calls(api_name: str, pid: int = 0, session_id: str = "", module_name: str = "", module_path: str = "") -> str:
    """Find calls to a specific API by searching for the API address in import tables.

    Args:
        api_name: API function name (e.g. 'CreateFileA', 'VirtualAlloc', 'MessageBoxW')
    """
    try:
        client = ensure_attached(resolve_pid(pid, session_id))
        # Resolve API address via x64dbg expression evaluator
        api_addr, ok = client.eval_sync(api_name)
        if not ok or api_addr == 0:
            raise BridgeError(f"API '{api_name}' not found. Make sure the module is loaded.")
        
        return f"### API: {api_name} at `{hex(api_addr)}`\n\nUse x64_find_references('{hex(api_addr)}') to find callers."
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_get_modules(pid: int = 0, session_id: str = "", module_name: str = "", module_path: str = "", scan_ports: Optional[List[int]] = None) -> str:
    """List all loaded modules in the debugged process with base addresses and sizes."""
    try:
        client = ensure_attached(resolve_pid(pid, session_id))
        mem = client.memmap()
        
        # Group regions by module info
        modules = {}
        for region in mem:
            info = region.info if hasattr(region, 'info') else ""
            if not _match_scope(region, module_name, module_path):
                continue
            if info and info not in modules:
                modules[info] = {
                    "name": info,
                    "base": hex(region.base_address),
                    "size": region.region_size,
                }
            elif info in modules:
                modules[info]["size"] += region.region_size

        return json.dumps({
            "ok": True,
            "modules": sorted(modules.values(), key=lambda x: x["name"]),
            "count": len(modules),
            "pid": resolve_pid(pid, session_id),
        }, indent=2, default=str)
    except Exception as e:
        raise BridgeError(str(e)) from e


# ── Command Allowlist ─────────────────────────────────────────

# The dispatcher (src/tools/t17_bridge.ts) screens the command before the string
# ever reaches this process, but the bridge is a separate MCP server and cannot
# assume the dispatcher is its only caller. Anything speaking MCP to this port
# directly would otherwise reach cmd_sync unchecked. The two lists are the same
# set; they are kept in step by tests/unit/bridge-x64-allowlist.test.ts reading
# this file, because a second copy that drifts is how the hole reopens.
#
# Read-only WITH RESPECT TO THE DEBUGGEE. Every verb reads state or configures
# the debugger's own breakpoints and traces. Deliberately absent:
#   d, dump, savedata, dd   write the target's memory to a file
#   erun, run, rtr, rte, go  advance or end the debuggee
#   writemem, patch         write the target's memory
#   TraceSetLogFile, TraceSetDir   redirect trace output to a file
X64DBG_COMMAND_ALLOWLIST = frozenset({
    # Breakpoints: set, list and remove.
    "bp", "bph", "bphws", "bphwc", "bpr", "bpc", "bpdll",
    # Traces and the configuration that decides what a trace captures.
    "trace", "tracelog", "tracesetlog", "tracesetcommand", "tracesetcondition",
    "tracesetcmdlog",
    # Disassembly and symbolic reads.
    "dasm", "disasm", "lm", "lmv", "sym", "symenum", "type", "anal",
})

# x64dbg accepts these as a command separator, with or without surrounding
# spaces, so 'lm|dd' is one token and a verb-scoped check would not see the
# separator at all.
X64DBG_CHAIN_CHARS = (";", "&&", "||", "|", "\n")


def validate_command(command: str) -> None:
    """Refuse a command the allowlist does not cover.

    The whole string is screened for a separator, not just the tokens after the
    verb, so a chain cannot hide inside the verb. Over-refusing is the safe
    direction: a breakpoint expression that needs one of these characters has a
    dedicated tool, and a separator that slips past is a write the caller never
    approved.
    """
    trimmed = (command or "").strip()
    if not trimmed:
        raise BridgeError("command must not be empty.")
    for sep in X64DBG_CHAIN_CHARS:
        if sep in trimmed:
            raise BridgeError(
                f"Refusing chained x64dbg command {command!r}. Run one command per "
                "call — chaining would bypass the allowlist."
            )
    verb = trimmed.split()[0]
    if verb.lower() not in X64DBG_COMMAND_ALLOWLIST:
        raise BridgeError(
            f"x64dbg command {verb!r} is not in the read-only allowlist. Allowed: "
            f"{', '.join(sorted(X64DBG_COMMAND_ALLOWLIST))}. A command that writes "
            "or changes process state needs a dedicated tool, not a raw one."
        )


@mcp.tool()
def x64_search_command(command: str, pid: int = 0, session_id: str = "") -> str:
    """Execute one read-only x64dbg command from a fixed allowlist.

    cmd_sync returns a success boolean, not text output. For data retrieval use
    the specific tools instead of a command.
    See: https://help.x64dbg.com/en/latest/commands/

    Args:
        command: a single x64dbg command (e.g. 'bp MessageBoxA', 'bpc 0x401000')
    """
    try:
        validate_command(command)
        client = ensure_attached(resolve_pid(pid, session_id))
        result = client.cmd_sync(command)
        return f"### Command: {command}\nSuccess: {result}"
    except BridgeError:
        raise
    except Exception as e:
        raise BridgeError(str(e)) from e


# ── Memory & Disassembly Tools ────────────────────────────────

# The dispatcher screens the command string before it reaches the bridge, but
# the bridge is a separate process and cannot assume that is the only caller.
# This cap is the backstop for a request that would otherwise read a whole
# region in one call.
MAX_READ_SIZE = 4096


def _resolve_address(client: X64DbgClient, address: str) -> int:
    """Turn '0x401000', '401000' or 'kernel32!MessageBoxA' into an integer.

    eval_sync is the only resolver the client exposes, and it is also what makes
    symbol names work — a plain int() would accept only hex and turn every
    symbol into a ValueError.
    """
    if not address or not str(address).strip():
        raise BridgeError("address is required")
    resolved, ok = client.eval_sync(str(address).strip())
    if not ok or not resolved:
        raise BridgeError(
            f"Could not resolve address '{address}'. Use hex ('0x401000'), a bare "
            "hex value, or a symbol name x64dbg can evaluate."
        )
    return int(resolved)


@mcp.tool()
def x64_read_memory(address: str, size: int = 64, pid: int = 0, session_id: str = "") -> str:
    """Read raw bytes from the debuggee's memory.

    Args:
        address: Hex address, bare hex value, or a symbol name
        size: Number of bytes to read (default 64, max 4096)
    """
    try:
        if size <= 0:
            raise BridgeError(f"size must be positive, got {size}")
        if size > MAX_READ_SIZE:
            raise BridgeError(
                f"size {size} exceeds the {MAX_READ_SIZE}-byte cap. Read a range in "
                "steps, or use x64_find_pattern to locate the address first."
            )
        client = ensure_attached(resolve_pid(pid, session_id))
        addr = _resolve_address(client, address)
        data = client.read_memory(addr, size)
        if not data:
            raise BridgeError(f"No readable memory at {address} ({hex(addr)})")
        return (
            f"### Memory at {address} ({hex(addr)}), {len(data)} bytes\n\n"
            f"- hex: `{data.hex(' ')}`\n"
            f"- ascii: `{data.decode('ascii', errors='replace')}`"
        )
    except BridgeError:
        raise
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_write_memory(address: str, hex_bytes: str, pid: int = 0, session_id: str = "") -> str:
    """Write raw bytes into the debuggee's memory.

    Args:
        address: Hex address, bare hex value, or a symbol name
        hex_bytes: Bytes to write as hex, spaces ignored (e.g. '90 C3' or '90C3')
    """
    try:
        if not hex_bytes or not hex_bytes.strip():
            raise BridgeError("hex_bytes is required")
        try:
            payload = bytes.fromhex(hex_bytes.replace(" ", "").replace("0x", ""))
        except ValueError as e:
            raise BridgeError(f"hex_bytes is not valid hex: {e}") from e
        if not payload:
            raise BridgeError("hex_bytes decoded to zero bytes")

        client = ensure_attached(resolve_pid(pid, session_id))
        addr = _resolve_address(client, address)
        ok = client.write_memory(addr, payload)
        if not ok:
            raise BridgeError(f"x64dbg rejected the write to {address} ({hex(addr)})")
        return (
            f"### Wrote {len(payload)} byte(s) to {address} ({hex(addr)})\n\n"
            f"- hex: `{payload.hex(' ')}`"
        )
    except BridgeError:
        raise
    except Exception as e:
        raise BridgeError(str(e)) from e


@mcp.tool()
def x64_disassemble(address: str, count: int = 1, pid: int = 0, session_id: str = "") -> str:
    """Disassemble instructions starting at an address.

    Args:
        address: Hex address, bare hex value, or a symbol name
        count: Number of instructions to decode (default 1, max 64)
    """
    try:
        if count <= 0:
            raise BridgeError(f"count must be positive, got {count}")
        if count > 64:
            raise BridgeError(f"count {count} exceeds the 64-instruction cap.")
        client = ensure_attached(resolve_pid(pid, session_id))
        addr = _resolve_address(client, address)

        lines = []
        cursor = addr
        for _ in range(count):
            instr = client.disassemble_at(cursor)
            if instr is None:
                if not lines:
                    raise BridgeError(
                        f"x64dbg could not disassemble at {address} ({hex(addr)}). "
                        "The address may be unmapped or not executable."
                    )
                lines.append(f"- {hex(cursor)}: <end of decodable range>")
                break
            args = " ".join(arg.mnemonic for arg in instr.arg)
            lines.append(f"- {hex(cursor)}: {instr.instruction} {args}".rstrip())
            # A zero-length instruction would make this loop spin forever.
            if instr.instr_size <= 0:
                lines.append(f"- {hex(cursor)}: <zero-length instruction, stopped>")
                break
            cursor += instr.instr_size

        return f"### Disassembly at {address} ({hex(addr)})\n\n" + "\n".join(lines)
    except BridgeError:
        raise
    except Exception as e:
        raise BridgeError(str(e)) from e


# get_breakpoints takes one BreakpointType per call, and BpNone is 0 — asking
# for it returns nothing while still looking like a valid request, so "all" is
# an explicit list of the three types this tool exposes.
BP_TYPE_FLAGS = {
    "bp_type_all": ("BpNormal", "BpHardware", "BpMemory"),
    "bp_type_normal": ("BpNormal",),
    "bp_type_hardware": ("BpHardware",),
    "bp_type_memory": ("BpMemory",),
}


@mcp.tool()
def x64_list_breakpoints(bp_type: str = "bp_type_all", pid: int = 0, session_id: str = "") -> str:
    """List the breakpoints set in the debugged process.

    Args:
        bp_type: One of 'bp_type_all', 'bp_type_normal', 'bp_type_hardware', 'bp_type_memory'
    """
    try:
        if bp_type not in BP_TYPE_FLAGS:
            raise BridgeError(
                f"Unknown bp_type '{bp_type}'. Use one of: {', '.join(BP_TYPE_FLAGS)}."
            )

        # Not a top-level export of x64dbg_automate, so it comes from models.
        from x64dbg_automate.models import BreakpointType

        client = ensure_attached(resolve_pid(pid, session_id))

        entries = []
        for flag_name in BP_TYPE_FLAGS[bp_type]:
            for bp in client.get_breakpoints(getattr(BreakpointType, flag_name)):
                entries.append({
                    "address": hex(bp.addr),
                    "type": flag_name.replace("Bp", "").lower(),
                    "enabled": bp.enabled,
                    "active": bp.active,
                    "hit_count": bp.hitCount,
                    "name": bp.name,
                    "module": bp.mod,
                    "condition": bp.breakCondition,
                    "command": bp.commandText,
                })
        entries.sort(key=lambda e: int(e["address"], 16))

        return json.dumps({
            "ok": True,
            "bp_type": bp_type,
            "count": len(entries),
            "breakpoints": entries,
        }, indent=2, default=str)
    except BridgeError:
        raise
    except Exception as e:
        raise BridgeError(str(e)) from e


# ── Entry Point ───────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
