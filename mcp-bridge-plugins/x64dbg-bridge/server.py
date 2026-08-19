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

# ── Auto-Connect Logic ────────────────────────────────────────

_client: X64DbgClient | None = None

X64DBG_PATH = os.environ.get(
    "X64DBG_PATH",
    "E:/Deverloper/snapshot_2025-08-19_19-40/release/x64/x64dbg.exe"
)


def get_client() -> X64DbgClient:
    """Get or create X64DbgClient (no auto-attach)."""
    global _client
    if _client is not None:
        return _client
    _client = X64DbgClient(X64DBG_PATH)
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
        return f"❌ Error listing sessions: {e}"


@mcp.tool()
def x64_auto_connect(pid: int = 0, session_id: str = "") -> str:
    """Auto-detect and connect to a running x64dbg session.
    If no session found, returns instructions to start one.
    """
    try:
        client = get_client()
        sessions = client.list_sessions()
        if not sessions:
            return ("❌ No x64dbg sessions found.\n"
                    "Use x64_start_session to launch x64dbg with a target binary.")

        wanted_pid = resolve_pid(pid, session_id)
        session = None
        if wanted_pid is not None:
            for candidate in sessions:
                if getattr(candidate, "pid", None) == wanted_pid:
                    session = candidate
                    break
            if session is None:
                return f"❌ No x64dbg session found for PID {wanted_pid}."
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
        return f"❌ Error: {e}"


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
        return f"❌ Error starting session: {e}"


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
        return f"❌ Error attaching: {e}"


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
        return f"❌ Error: {e}"


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
        return f"❌ Error: {e}"


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
        return f"❌ Error: {e}"


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
            return f"❌ API '{api_name}' not found. Make sure the module is loaded."
        
        return f"### API: {api_name} at `{hex(api_addr)}`\n\nUse x64_find_references('{hex(api_addr)}') to find callers."
    except Exception as e:
        return f"❌ Error: {e}"


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
        return f"❌ Error: {e}"


@mcp.tool()
def x64_search_command(command: str, pid: int = 0, session_id: str = "") -> str:
    """Execute any raw x64dbg command.
    Note: cmd_sync returns success/fail boolean, not text output.
    For data retrieval, use specific tools instead.
    See: https://help.x64dbg.com/en/latest/commands/

    Args:
        command: x64dbg command string (e.g. 'bp MessageBoxA', 'bc *')
    """
    try:
        client = ensure_attached(resolve_pid(pid, session_id))
        result = client.cmd_sync(command)
        return f"### Command: {command}\nSuccess: {result}"
    except Exception as e:
        return f"❌ Error: {e}"


# ── Entry Point ───────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
