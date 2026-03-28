"""
HSA MCP Bridge Plugin for IDA Pro 8.x / 9.x
=============================================
Install: Copy this single file to %IDADIR%/plugins/hsa_ida_plugin.py

This plugin runs INSIDE IDA Pro as a proper idaapi.plugin_t.
It opens an HTTP server on port 28472 (localhost only) that accepts
JSON commands from the external MCP bridge (server.py).

Architecture:
  Agent -> HSA Engine -> server.py (MCP stdio) -> HTTP -> [THIS PLUGIN inside IDA]

IDA 8.3 compatible: Uses only APIs available in IDA 8.x.
No external pip dependencies (uses only stdlib + IDAPython).
"""

import idaapi
import ida_kernwin
import ida_funcs
import ida_name
import ida_bytes
import ida_nalt
import ida_lines
import ida_ida
import idautils
import idc

import json
import threading
import traceback

# Use http.server from stdlib (no pip install needed in IDA's Python)
from http.server import HTTPServer, BaseHTTPRequestHandler

PLUGIN_NAME    = "HSA MCP Bridge"
PLUGIN_VERSION = "1.0.0"
PLUGIN_HOTKEY  = "Ctrl-Shift-H"
HTTP_HOST      = "127.0.0.1"
HTTP_PORT      = 28472

# ── Thread-safe IDA execution ──────────────────────────────────────
# ALL IDA API calls MUST run on the main thread via execute_sync.

def sync_exec(fn, write=False):
    """Execute a function on IDA's main thread and return the result."""
    box = {}
    def wrapper():
        try:
            box["v"] = fn()
        except Exception as e:
            box["err"] = str(e)
            box["tb"] = traceback.format_exc()
    flags = ida_kernwin.MFF_WRITE if write else ida_kernwin.MFF_READ
    ida_kernwin.execute_sync(wrapper, flags)
    if "err" in box:
        raise RuntimeError(box["err"])
    return box.get("v")


# ── Command Handlers ───────────────────────────────────────────────
# Each handler returns a dict that will be JSON-serialized back.

def cmd_get_info(_params):
    """Get basic info about the loaded database."""
    def _inner():
        return {
            "plugin": PLUGIN_NAME,
            "version": PLUGIN_VERSION,
            "file": ida_nalt.get_input_file_path(),
            "processor": ida_ida.inf_get_procname() if hasattr(ida_ida, 'inf_get_procname') else idc.get_inf_attr(idc.INF_PROCNAME),
            "imagebase": hex(idaapi.get_imagebase()),
            "min_ea": hex(idc.get_inf_attr(idc.INF_MIN_EA)),
            "max_ea": hex(idc.get_inf_attr(idc.INF_MAX_EA)),
            "num_functions": ida_funcs.get_func_qty(),
        }
    return sync_exec(_inner)


def cmd_list_functions(params):
    """List functions with offset/limit pagination."""
    offset = int(params.get("offset", 0))
    limit = int(params.get("limit", 50))

    def _inner():
        result = []
        for i, ea in enumerate(idautils.Functions()):
            if i < offset:
                continue
            if len(result) >= limit:
                break
            func = ida_funcs.get_func(ea)
            name = ida_name.get_name(ea) or f"sub_{ea:X}"
            result.append({
                "ea": hex(ea),
                "name": name,
                "size": func.size() if func else 0,
            })
        return {"functions": result, "total": ida_funcs.get_func_qty()}
    return sync_exec(_inner)


def cmd_decompile(params):
    """Decompile a function at the given address."""
    addr = params.get("address") or params.get("ea")
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        try:
            import ida_hexrays
        except ImportError:
            return {"error": "Hex-Rays decompiler not available"}

        func = ida_funcs.get_func(ea)
        if not func:
            return {"error": f"No function at {hex(ea)}"}

        try:
            cfunc = ida_hexrays.decompile(func.start_ea)
            if not cfunc:
                return {"error": f"Decompilation failed at {hex(ea)}"}

            lines = []
            sv = cfunc.get_pseudocode()
            for i in range(sv.size()):
                raw_line = sv[i].line
                try:
                    line = ida_lines.tag_remove(raw_line)
                except:
                    line = idaapi.tag_remove(raw_line)
                lines.append(line)

            return {
                "address": hex(func.start_ea),
                "name": ida_name.get_name(func.start_ea) or f"sub_{func.start_ea:X}",
                "pseudocode": "\n".join(lines),
                "lines": len(lines),
            }
        except Exception as e:
            return {"error": f"Decompile error: {str(e)}"}

    return sync_exec(_inner)


def cmd_get_disasm(params):
    """Get disassembly lines around an address."""
    addr = params.get("address") or params.get("ea")
    count = int(params.get("count", 20))
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        lines = []
        current = ea
        for _ in range(count):
            disasm = idc.generate_disasm_line(current, 0)
            if disasm is None:
                break
            lines.append({
                "ea": hex(current),
                "disasm": disasm,
                "bytes": ida_bytes.get_bytes(current, idc.get_item_size(current)).hex() if ida_bytes.get_bytes(current, idc.get_item_size(current)) else "",
            })
            current = idc.next_head(current)
            if current == idaapi.BADADDR:
                break
        return {"lines": lines}
    return sync_exec(_inner)


def cmd_rename_symbol(params):
    """Rename a symbol at address."""
    addr = params.get("address") or params.get("ea")
    name = params.get("name")
    if not addr or not name:
        return {"error": "Missing 'address' and/or 'name' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        ok = ida_name.set_name(ea, name, ida_name.SN_CHECK)
        return {"ok": ok, "address": hex(ea), "name": name}
    return sync_exec(_inner, write=True)


def cmd_set_comment(params):
    """Set a comment at address."""
    addr = params.get("address") or params.get("ea")
    comment = params.get("comment", "")
    is_func = params.get("func", False)
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        if is_func:
            func = ida_funcs.get_func(ea)
            if func:
                idc.set_func_cmt(func.start_ea, comment, 1)
                return {"ok": True, "type": "function"}
        idc.set_cmt(ea, comment, 0)
        return {"ok": True, "type": "inline"}
    return sync_exec(_inner, write=True)


def cmd_read_bytes(params):
    """Read raw bytes from address."""
    addr = params.get("address") or params.get("ea")
    size = int(params.get("size", 16))
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        data = ida_bytes.get_bytes(ea, size)
        if data is None:
            return {"error": f"Cannot read {size} bytes at {hex(ea)}"}
        return {"hex": data.hex(), "address": hex(ea), "size": size}
    return sync_exec(_inner)


def cmd_get_xrefs(params):
    """Get cross-references to/from an address."""
    addr = params.get("address") or params.get("ea")
    direction = params.get("direction", "to")  # "to" or "from"
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        refs = []
        if direction == "to":
            for xref in idautils.XrefsTo(ea):
                refs.append({
                    "from": hex(xref.frm),
                    "to": hex(xref.to),
                    "type": xref.type,
                })
        else:
            for xref in idautils.XrefsFrom(ea):
                refs.append({
                    "from": hex(xref.frm),
                    "to": hex(xref.to),
                    "type": xref.type,
                })
        return {"xrefs": refs, "count": len(refs), "direction": direction}
    return sync_exec(_inner)


def cmd_get_strings(params):
    """Get all strings in the database."""
    min_len = int(params.get("min_length", 4))

    def _inner():
        strings = []
        sc = idautils.Strings()
        for s in sc:
            if s.length >= min_len:
                strings.append({
                    "ea": hex(s.ea),
                    "value": str(s),
                    "length": s.length,
                })
                if len(strings) >= 500:  # Cap at 500
                    break
        return {"strings": strings, "count": len(strings)}
    return sync_exec(_inner)


def cmd_search_string(params):
    """Search for a string pattern in the binary's string table."""
    pattern = params.get("pattern", "")
    case_sensitive = params.get("case_sensitive", False)
    max_results = min(int(params.get("max_results", 100)), 500)
    if not pattern:
        return {"error": "Missing 'pattern' parameter"}

    def _inner():
        import re
        results = []
        sc = idautils.Strings()
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error:
            # Fallback to plain substring match
            regex = None

        for s in sc:
            s_val = str(s)
            matched = False
            if regex:
                matched = bool(regex.search(s_val))
            else:
                if case_sensitive:
                    matched = pattern in s_val
                else:
                    matched = pattern.lower() in s_val.lower()

            if matched:
                # Find xrefs to this string for context
                xrefs = [hex(x.frm) for x in idautils.XrefsTo(s.ea)]
                results.append({
                    "ea": hex(s.ea),
                    "value": s_val,
                    "length": s.length,
                    "xrefs": xrefs[:10],
                })
                if len(results) >= max_results:
                    break
        return {"results": results, "count": len(results), "pattern": pattern}
    return sync_exec(_inner)


def cmd_search_bytes(params):
    """Search for a hex byte pattern in the binary (supports ?? wildcards).
    Example: '48 8B ?? 10' or 'E8 ?? ?? ?? ??'
    """
    hex_pattern = params.get("hex_pattern", "").strip()
    start_addr = params.get("start", None)
    max_results = min(int(params.get("max_results", 50)), 200)
    if not hex_pattern:
        return {"error": "Missing 'hex_pattern' parameter"}

    def _inner():
        # Convert hex pattern to IDA binary search format
        # IDA uses  "48 8B ? 10" with single ? for wildcard
        search_str = hex_pattern.replace("??", "?").strip()

        min_ea = idc.get_inf_attr(idc.INF_MIN_EA)
        max_ea = idc.get_inf_attr(idc.INF_MAX_EA)
        ea = int(start_addr, 16) if start_addr else min_ea

        results = []
        while ea < max_ea and len(results) < max_results:
            ea = ida_bytes.bin_search(
                ea, max_ea,
                bytes.fromhex(hex_pattern.replace("??", "00").replace(" ", "")),
                None,  # mask (None = no wildcards via this param)
                ida_bytes.BIN_SEARCH_FORWARD,
                0  # flags
            )
            if ea == idaapi.BADADDR:
                break

            # Get context: function name if in a function
            func = ida_funcs.get_func(ea)
            func_name = ida_name.get_name(func.start_ea) if func else None
            disasm = idc.generate_disasm_line(ea, 0)

            results.append({
                "ea": hex(ea),
                "function": func_name,
                "disasm": disasm,
            })
            ea += 1

        return {"results": results, "count": len(results), "pattern": hex_pattern}
    return sync_exec(_inner)


def cmd_get_segments(params):
    """List all segments in the binary."""
    def _inner():
        segments = []
        for seg_ea in idautils.Segments():
            seg = idaapi.getseg(seg_ea)
            if seg:
                # Get permissions safely across IDA versions
                perm_str = "---"
                try:
                    p = seg.perm
                    perm_str = "%s%s%s" % (
                        "R" if p & 4 else "-",  # SFL_READ = 4
                        "W" if p & 2 else "-",  # SFL_WRITE = 2
                        "X" if p & 1 else "-",  # SFL_EXEC = 1
                    )
                except Exception:
                    pass

                seg_class = ""
                try:
                    seg_class = idaapi.get_segm_class(seg) or ""
                except Exception:
                    pass

                segments.append({
                    "name": idaapi.get_segm_name(seg) or "unknown",
                    "start": hex(seg.start_ea),
                    "end": hex(seg.end_ea),
                    "size": hex(seg.size()),
                    "perm": perm_str,
                    "class": seg_class,
                })
        return {"segments": segments, "count": len(segments)}
    return sync_exec(_inner)


def cmd_search_functions(params):
    """Search functions by name pattern (substring or regex)."""
    pattern = params.get("pattern", "")
    max_results = min(int(params.get("max_results", 50)), 200)
    if not pattern:
        return {"error": "Missing 'pattern' parameter"}

    def _inner():
        import re
        results = []
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            regex = None

        for ea in idautils.Functions():
            name = ida_name.get_name(ea) or f"sub_{ea:X}"
            matched = False
            if regex:
                matched = bool(regex.search(name))
            else:
                matched = pattern.lower() in name.lower()

            if matched:
                func = ida_funcs.get_func(ea)
                results.append({
                    "ea": hex(ea),
                    "name": name,
                    "size": func.size() if func else 0,
                })
                if len(results) >= max_results:
                    break
        return {"results": results, "count": len(results), "pattern": pattern}
    return sync_exec(_inner)



# ── Command Dispatch Table ─────────────────────────────────────────

COMMANDS = {
    "get_info":        cmd_get_info,
    "list_functions":  cmd_list_functions,
    "decompile":       cmd_decompile,
    "get_pseudocode":  cmd_decompile,   # alias
    "get_disasm":      cmd_get_disasm,
    "rename":          cmd_rename_symbol,
    "rename_symbol":   cmd_rename_symbol,
    "set_comment":     cmd_set_comment,
    "read_bytes":      cmd_read_bytes,
    "get_xrefs":         cmd_get_xrefs,
    "xrefs":             cmd_get_xrefs,   # alias
    "get_strings":       cmd_get_strings,
    "search_string":     cmd_search_string,
    "search_bytes":      cmd_search_bytes,
    "get_segments":      cmd_get_segments,
    "search_functions":  cmd_search_functions,
}


# ── HTTP Request Handler ──────────────────────────────────────────
# Using stdlib http.server — NO external dependencies needed.

class HsaBridgeHandler(BaseHTTPRequestHandler):
    """Handle incoming JSON commands from the MCP bridge."""

    def log_message(self, format, *args):
        """Redirect http.server logs to IDA Output window."""
        ida_kernwin.execute_sync(
            lambda: ida_kernwin.msg(f"[HSA] {format % args}\n"),
            ida_kernwin.MFF_NOWAIT,
        )

    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        info = {
            "status": "ok",
            "plugin": PLUGIN_NAME,
            "version": PLUGIN_VERSION,
            "port": HTTP_PORT,
            "commands": list(COMMANDS.keys()),
        }
        self.wfile.write(json.dumps(info).encode())

    def do_POST(self):
        """Execute a command."""
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            req = json.loads(body.decode("utf-8"))

            cmd_name = req.get("command") or req.get("cmd")
            params = req.get("params", {})

            if not cmd_name:
                self._send_error(400, "Missing 'command' field")
                return

            handler = COMMANDS.get(cmd_name)
            if not handler:
                self._send_error(404, f"Unknown command: {cmd_name}. Available: {list(COMMANDS.keys())}")
                return

            result = handler(params)
            self._send_json(200, {"ok": True, "data": result})

        except Exception as e:
            self._send_error(500, f"{str(e)}\n{traceback.format_exc()}")

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _send_error(self, code, msg):
        self._send_json(code, {"ok": False, "error": msg})


# ── Plugin Class ───────────────────────────────────────────────────

class HsaMcpBridgePlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP  # Stay loaded for entire session
    wanted_name = PLUGIN_NAME
    wanted_hotkey = PLUGIN_HOTKEY
    comment = "HSA MCP Bridge — HTTP server for AI agent control"
    help = "Starts HTTP server on port 28472 for MCP bridge communication"

    _server = None
    _thread = None

    def init(self):
        """Called when IDA loads the plugin. Auto-starts HTTP server."""
        ida_kernwin.msg(f"[HSA] {PLUGIN_NAME} v{PLUGIN_VERSION} loaded.\n")
        # Auto-start HTTP server (no need for manual hotkey activation)
        self._start_server()
        return idaapi.PLUGIN_KEEP

    def _start_server(self):
        """Start the HTTP server in a background thread."""
        if self._server is not None:
            return  # Already running
        try:
            self._server = HTTPServer((HTTP_HOST, HTTP_PORT), HsaBridgeHandler)
            self._thread = threading.Thread(
                target=self._server.serve_forever,
                daemon=True,
                name="hsa-mcp-bridge",
            )
            self._thread.start()
            ida_kernwin.msg(f"[HSA] ✅ HTTP server auto-started on http://{HTTP_HOST}:{HTTP_PORT}\n")
            ida_kernwin.msg(f"[HSA] Available commands: {', '.join(COMMANDS.keys())}\n")
        except OSError as e:
            ida_kernwin.msg(f"[HSA] ❌ Failed to start server: {e}\n")
            if "already in use" in str(e).lower() or "10048" in str(e):
                ida_kernwin.msg(f"[HSA] Port {HTTP_PORT} is already in use. Another instance running?\n")

    def run(self, _arg):
        """Called when user activates the plugin (hotkey or menu)."""
        if self._server is not None:
            ida_kernwin.msg(f"[HSA] Server already running on http://{HTTP_HOST}:{HTTP_PORT}\n")
            return
        self._start_server()

    def term(self):
        """Called when IDA is shutting down."""
        if self._server:
            ida_kernwin.msg(f"[HSA] Shutting down HTTP server...\n")
            self._server.shutdown()
            self._server = None
            self._thread = None


def PLUGIN_ENTRY():
    """IDA plugin entry point — MUST return a plugin_t instance."""
    return HsaMcpBridgePlugin()
