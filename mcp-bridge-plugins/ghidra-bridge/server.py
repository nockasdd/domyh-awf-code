# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp>=1.26.0,<2",
# ]
# ///
"""
HSA Ghidra MCP Bridge Server (runs OUTSIDE Ghidra)
===================================================
This stdio bridge talks to the Ghidra HTTP plugin loaded inside Ghidra.
It keeps instance discovery bounded so the agent can pin the right program
before calling rename/type/struct tools.
"""

import json
import os
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghidra-mcp-bridge")


class BridgeError(RuntimeError):
    """Bridge-side failure. Raising this makes FastMCP set isError, so the
    agent sees a failed call instead of prose describing a failure."""


GHIDRA_HTTP_HOST = os.environ.get("HSA_GHIDRA_HTTP_HOST", "127.0.0.1")
GHIDRA_HTTP_PORT = int(os.environ.get("HSA_GHIDRA_HTTP_PORT", "28572"))
GHIDRA_HTTP_PORT_RANGE = int(os.environ.get("HSA_GHIDRA_HTTP_PORT_RANGE", "32"))
GHIDRA_HTTP_PROBE_TIMEOUT = max(0.05, int(os.environ.get("HSA_GHIDRA_PROBE_TIMEOUT_MS", "350")) / 1000)
GHIDRA_HTTP_SCAN_WORKERS = max(1, int(os.environ.get("HSA_GHIDRA_SCAN_WORKERS", "32")))
BRIDGE_TOKEN = os.environ.get("HSA_BRIDGE_TOKEN", "").strip()


def write_bridge_config() -> str:
    """Drop the token where the plugin can read it.

    Ghidra does not forward the launching shell's environment to the JVM, so the
    plugin reads HSA_BRIDGE_TOKEN and then this file, which sits next to the
    plugin script itself.
    """
    if not BRIDGE_TOKEN:
        return ""
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "hsa_bridge_token")
    try:
        with open(target, "w") as fh:
            fh.write(BRIDGE_TOKEN)
        # chmod after the write, not as a mode argument: os.open's mode is masked
        # by the process umask, and on Windows it is not applied at all, so the
        # bearer token would land world-readable.
        os.chmod(target, 0o600)
        return target
    except Exception:
        # A bridge that cannot write the file still works for anyone who did
        # export the token, so this is reported, not fatal.
        return ""


def _port_candidates(scan_ports: Optional[List[int]] = None) -> List[int]:
    if scan_ports:
        ports = []
        for value in scan_ports:
            try:
                port = int(value)
                if 0 < port < 65536:
                    ports.append(port)
            except Exception:
                continue
        if ports:
            return list(dict.fromkeys(ports))

    env_ports = os.environ.get("HSA_GHIDRA_PORTS", "")
    if env_ports:
        ports = []
        for part in env_ports.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                port = int(part)
                if 0 < port < 65536:
                    ports.append(port)
            except Exception:
                continue
        if ports:
            return list(dict.fromkeys(ports))

    return list(range(GHIDRA_HTTP_PORT, GHIDRA_HTTP_PORT + max(1, GHIDRA_HTTP_PORT_RANGE)))


def _resolve_base_url(params: dict | None = None) -> str:
    if params:
        port = params.get("port")
        if isinstance(port, int) and port > 0:
            return "http://%s:%s" % (GHIDRA_HTTP_HOST, port)
        if isinstance(port, str) and port.isdigit():
            return "http://%s:%s" % (GHIDRA_HTTP_HOST, int(port))
    base = os.environ.get("HSA_GHIDRA_HTTP_BASE")
    if base:
        return base.rstrip("/")
    return "http://%s:%s" % (GHIDRA_HTTP_HOST, GHIDRA_HTTP_PORT)


def _request_json(url: str, payload: dict) -> dict:
    if not BRIDGE_TOKEN:
        raise BridgeError(
            "HSA_BRIDGE_TOKEN is not set. The Ghidra plugin refuses to start without it, "
            "because rename_symbol and create_struct write to the program. Set the same "
            "token for this bridge and for Ghidra."
        )
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer %s" % BRIDGE_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        if e.code == 401:
            raise BridgeError(
                "Ghidra plugin rejected the token. HSA_BRIDGE_TOKEN must be identical for "
                "this bridge and for the plugin (env, or hsa_bridge_token next to the script)."
            )
        raise BridgeError("Ghidra plugin returned %d: %s" % (e.code, detail))


def ghidra_request(command: str, params: dict) -> dict:
    try:
        return _request_json(_resolve_base_url(params), {"command": command, "params": params})
    except BridgeError:
        # A missing or rejected token is a setup problem the agent must see
        # verbatim, not another dict that format_result turns into prose.
        raise
    except urllib.error.URLError as e:
        return {"ok": False, "error": "Cannot connect to Ghidra plugin: %s" % e}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(res: dict) -> str:
    if not res.get("ok", False):
        raise BridgeError(str(res.get("error", "Unknown error")))
    return json.dumps(res.get("data", {}), indent=2, default=str)


def _probe_instance(port: int) -> dict | None:
    try:
        with urllib.request.urlopen("http://%s:%s" % (GHIDRA_HTTP_HOST, port), timeout=GHIDRA_HTTP_PROBE_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, dict) and data.get("status") == "ok":
                data["port"] = port
                return data
    except Exception:
        return None
    return None


def _probe_instances(ports: List[int]) -> List[dict]:
    """Probe the range concurrently. A serial scan costs the full timeout on
    every closed port, which is the whole range when Ghidra is not running —
    long enough that the MCP client gives up and reports the tools as missing."""
    if not ports:
        return []
    results: dict[int, dict] = {}
    max_workers = min(len(ports), GHIDRA_HTTP_SCAN_WORKERS)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(_probe_instance, port): port for port in ports if port > 0}
        for future in as_completed(future_map):
            port = future_map[future]
            try:
                info = future.result()
            except Exception:
                info = None
            if info is not None:
                results[port] = info
    return [results[port] for port in ports if port in results]


@mcp.tool()
def ghidra_list_instances(scan_ports: Optional[List[int]] = None) -> str:
    ports = _port_candidates(scan_ports)
    instances = _probe_instances(ports)
    return json.dumps({
        "ok": True,
        "instances": instances,
        "count": len(instances),
        "ports_scanned": ports,
    }, indent=2, default=str)


@mcp.tool()
def ghidra_get_info() -> str:
    return format_result(ghidra_request("get_info", {}))


@mcp.tool()
def ghidra_list_functions(offset: int = 0, limit: int = 50) -> str:
    return format_result(ghidra_request("list_functions", {"offset": offset, "limit": min(limit, 200)}))


@mcp.tool()
def ghidra_search_functions(pattern: str, max_results: int = 50) -> str:
    return format_result(ghidra_request("search_functions", {"pattern": pattern, "max_results": min(max_results, 200)}))


@mcp.tool()
def ghidra_decompile(address: str) -> str:
    return format_result(ghidra_request("decompile", {"address": address}))


@mcp.tool()
def ghidra_get_disasm(address: str, count: int = 20) -> str:
    return format_result(ghidra_request("get_disasm", {"address": address, "count": count}))


@mcp.tool()
def ghidra_get_xrefs(address: str, direction: str = "to") -> str:
    return format_result(ghidra_request("get_xrefs", {"address": address, "direction": direction}))


@mcp.tool()
def ghidra_get_symbols(pattern: str = "", max_results: int = 100) -> str:
    return format_result(ghidra_request("get_symbols", {"pattern": pattern, "max_results": min(max_results, 500)}))


@mcp.tool()
def ghidra_get_data_types(pattern: str = "", max_results: int = 100) -> str:
    return format_result(ghidra_request("get_data_types", {"pattern": pattern, "max_results": min(max_results, 500)}))


@mcp.tool()
def ghidra_rename_symbol(address: str, name: str, source_type: str = "user") -> str:
    return format_result(ghidra_request("rename_symbol", {"address": address, "name": name, "source_type": source_type}))


@mcp.tool()
def ghidra_set_function_signature(address: str, signature: str) -> str:
    return format_result(ghidra_request("set_function_signature", {"address": address, "signature": signature}))


@mcp.tool()
def ghidra_create_struct(name: str, members: Optional[List[dict]] = None) -> str:
    return format_result(ghidra_request("create_struct", {"name": name, "members": members or []}))


@mcp.tool()
def ghidra_apply_data_type(address: str, type_name: str, length: int = 0) -> str:
    return format_result(ghidra_request("apply_data_type", {"address": address, "type_name": type_name, "length": length}))


@mcp.tool()
def ghidra_create_class_layout(name: str, fields: Optional[List[dict]] = None, vtable: Optional[str] = None) -> str:
    return format_result(ghidra_request("create_class_layout", {"name": name, "fields": fields or [], "vtable": vtable}))


if __name__ == "__main__":
    if BRIDGE_TOKEN and not write_bridge_config():
        print(
            "HSA bridge: could not write hsa_bridge_token next to the plugin. Ghidra may not "
            "see HSA_BRIDGE_TOKEN unless it is exported in the environment Ghidra launches from."
        )
    mcp.run()
