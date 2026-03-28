"""
HSA IDA MCP Bridge Server (runs OUTSIDE IDA Pro)
=================================================
This is the MCP stdio bridge that HSA Engine spawns as a subprocess.
It connects to the IDA plugin's HTTP server (hsa_ida_plugin.py) running
inside IDA Pro on port 28472.

Flow: HSA Engine → stdio → [this server] → HTTP → [IDA plugin inside IDA]
"""

import asyncio
import argparse
import json
from mcp.server.fastmcp import FastMCP
from hsa_ida_compat import compat

mcp = FastMCP("ida-mcp-bridge")
IDA_HTTP_BASE = "http://127.0.0.1:28472"


def ida_request(command: str, params: dict) -> dict:
    """Send a command to the IDA plugin HTTP server."""
    if compat.is_headless:
        return {"error": "Headless mode — HTTP bridge not used."}
    try:
        import urllib.request
        import urllib.error
        payload = json.dumps({"command": command, "params": params}).encode("utf-8")
        req = urllib.request.Request(
            IDA_HTTP_BASE,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"Cannot connect to IDA plugin: {e}. Is IDA running with hsa_ida_plugin.py loaded?"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(res: dict) -> str:
    """Format IDA response for agent consumption."""
    if not res.get("ok", False):
        error = res.get("error", "Unknown error")
        return f"❌ IDA Error: {error}"
    data = res.get("data", {})
    return json.dumps(data, indent=2, default=str)


# ── MCP Tools ──────────────────────────────────────────────────────

@mcp.tool()
def ida_get_info() -> str:
    """Get basic info about the loaded IDA database (file, imagebase, functions count)."""
    return format_result(ida_request("get_info", {}))


@mcp.tool()
def ida_list_functions(offset: int = 0, limit: int = 50) -> str:
    """List functions in the database with pagination.
    
    Args:
        offset: Start index (default 0)
        limit: Max functions to return (default 50, max 200)
    """
    return format_result(ida_request("list_functions", {"offset": offset, "limit": min(limit, 200)}))


@mcp.tool()
def ida_decompile(address: str) -> str:
    """Decompile a function at the given hex address using Hex-Rays.
    
    Args:
        address: Hex address like '0x401000' or '401000'
    """
    if compat.is_headless:
        # Headless mode uses idalib directly
        try:
            import ida_hexrays
            import ida_funcs as _ida_funcs
            ea = int(address, 16) if address.startswith("0x") else int(address, 16)
            cfunc = ida_hexrays.decompile(ea)
            if cfunc:
                return str(cfunc)
            return f"❌ Decompilation failed at {address}"
        except Exception as e:
            return f"❌ Headless decompile error: {e}"
    
    return format_result(ida_request("decompile", {"address": address}))


@mcp.tool()
def ida_get_disasm(address: str, count: int = 20) -> str:
    """Get disassembly lines starting from an address.
    
    Args:
        address: Hex address like '0x401000'
        count: Number of instructions to disassemble (default 20)
    """
    return format_result(ida_request("get_disasm", {"address": address, "count": count}))


@mcp.tool()
def ida_rename(address: str, name: str) -> str:
    """Rename a symbol/function at the given address.
    
    Args:
        address: Hex address of the symbol
        name: New name for the symbol
    """
    return format_result(ida_request("rename_symbol", {"address": address, "name": name}))


@mcp.tool()
def ida_set_comment(address: str, comment: str, func: bool = False) -> str:
    """Set a comment at an address.
    
    Args:
        address: Hex address
        comment: Comment text
        func: If True, set as function comment instead of inline
    """
    return format_result(ida_request("set_comment", {"address": address, "comment": comment, "func": func}))


@mcp.tool()
def ida_read_bytes(address: str, size: int = 16) -> str:
    """Read raw bytes from the database.
    
    Args:
        address: Hex address to read from
        size: Number of bytes to read (default 16)
    """
    return format_result(ida_request("read_bytes", {"address": address, "size": size}))


@mcp.tool()
def ida_get_xrefs(address: str, direction: str = "to") -> str:
    """Get cross-references to or from an address.
    
    Args:
        address: Hex address
        direction: 'to' (who references this address) or 'from' (what this address references)
    """
    return format_result(ida_request("get_xrefs", {"address": address, "direction": direction}))


@mcp.tool()
def ida_get_strings(min_length: int = 4) -> str:
    """Get all strings found in the database.
    
    Args:
        min_length: Minimum string length (default 4)
    """
    return format_result(ida_request("get_strings", {"min_length": min_length}))


@mcp.tool()
def ida_search_string(pattern: str, case_sensitive: bool = False, max_results: int = 100) -> str:
    """Search for strings matching a pattern (substring or regex) in the binary.
    Returns matching strings with their addresses and cross-references.

    Args:
        pattern: Search pattern (substring or regex like 'kernel32|ntdll')
        case_sensitive: Case-sensitive matching (default False)
        max_results: Maximum results to return (default 100, max 500)
    """
    return format_result(ida_request("search_string", {
        "pattern": pattern,
        "case_sensitive": case_sensitive,
        "max_results": max_results,
    }))


@mcp.tool()
def ida_search_bytes(hex_pattern: str, start: str = "", max_results: int = 50) -> str:
    """Search for a hex byte pattern in the binary. Supports ?? wildcards.

    Args:
        hex_pattern: Hex bytes separated by spaces, e.g. '48 8B ?? 10' or 'E8 ?? ?? ?? ??'
        start: Start address for search (hex, default: beginning of binary)
        max_results: Maximum results (default 50, max 200)
    """
    params = {"hex_pattern": hex_pattern, "max_results": max_results}
    if start:
        params["start"] = start
    return format_result(ida_request("search_bytes", params))


@mcp.tool()
def ida_get_segments() -> str:
    """List all segments in the binary (.text, .data, .rdata, etc.) with permissions."""
    return format_result(ida_request("get_segments", {}))


@mcp.tool()
def ida_search_functions(pattern: str, max_results: int = 50) -> str:
    """Search functions by name pattern (substring or regex).
    Useful when you know a partial function name but not the address.

    Args:
        pattern: Function name pattern (e.g. 'main', 'crypt.*init', 'sub_4[0-9]+')
        max_results: Maximum results (default 50, max 200)
    """
    return format_result(ida_request("search_functions", {
        "pattern": pattern,
        "max_results": max_results,
    }))


# ── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HSA IDA MCP Bridge Server")
    parser.add_argument("--headless", type=str, help="Path to binary for idalib headless mode (IDA 9.x+ only)")
    args = parser.parse_args()

    if args.headless:
        if not compat.init_idalib_if_headless(args.headless):
            print("Failed to init idalib. Falling back to HTTP bridge mode.")
    
    mcp.run()
